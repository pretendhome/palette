from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))

from core.gateway import PerplexityGateway
from core.gateway.audit import AuditLogger
from core.gateway.cache import PerplexityCache
from core.gateway.rate_limiter import RateLimiter
from core.gateway.sanitizer import QuerySanitizer


class GatewayTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmpdir = tempfile.TemporaryDirectory()
        tmp_path = Path(self.tmpdir.name)
        config_path = Path(__file__).resolve().parents[1] / "config.yaml"
        self.gateway = PerplexityGateway(
            config_path=config_path,
            cache=PerplexityCache(tmp_path / "cache.db"),
            audit=AuditLogger(tmp_path / "audit.db"),
            rate_limiter=RateLimiter(tmp_path / "limit.db", limit=100),
            sanitizer=QuerySanitizer(config_path),
        )

    def tearDown(self) -> None:
        self.tmpdir.cleanup()

    def sample_retrieval(self, confidence: float = 35.0) -> dict:
        return {
            "query": "placeholder",
            "confidence": confidence,
            "riu_id": "RIU-042",
            "riu_name": "Legal Research",
            "classification": "external_preferred",
            "knowledge": [
                {"lib_id": "LIB-001", "question": "What are Delaware fiduciary duties?"}
            ],
            "context": "Local legal research context.",
        }

    def test_sanitizer_strips_case_numbers(self):
        sanitized, categories = self.gateway.sanitizer.sanitize_query(
            "Case 1:24-cv-05678 concerns Delaware fiduciary duty."
        )
        self.assertIn("[CASE_REF]", sanitized)
        self.assertIn("case_number", categories)

    def test_sanitizer_strips_party_names_from_v_format(self):
        sanitized, categories = self.gateway.sanitizer.sanitize_query(
            "What are the holdings in Smith v. Jones Corp on fiduciary duty?"
        )
        self.assertTrue("[CASE_NAME]" in sanitized or "[CLIENT]" in sanitized)
        self.assertTrue("party_v_party" in categories or "party_name" in categories)

    def test_sanitizer_strips_email(self):
        sanitized, categories = self.gateway.sanitizer.sanitize_query(
            "Email me at lawyer@example.com about Delaware precedent."
        )
        self.assertIn("[EMAIL]", sanitized)
        self.assertIn("email", categories)

    def test_sanitizer_strips_ssn_and_ein(self):
        sanitized, categories = self.gateway.sanitizer.sanitize_query(
            "SSN 123-45-6789 and EIN 12-3456789 in a filing question."
        )
        self.assertIn("[SSN]", sanitized)
        self.assertIn("[EIN]", sanitized)
        self.assertIn("ssn", categories)
        self.assertIn("ein", categories)

    def test_is_safe_for_external_blocks_strategy_questions(self):
        allowed, reason = self.gateway.sanitizer.is_safe_for_external(
            "Should we settle for $2.5M with Smith Corp in our case?"
        )
        self.assertFalse(allowed)
        self.assertTrue("blocked" in reason or "contains" in reason)

    def test_is_safe_for_external_allows_precedent_questions(self):
        allowed, reason = self.gateway.sanitizer.is_safe_for_external(
            "What are the key Delaware precedents for breach of fiduciary duty?"
        )
        self.assertTrue(allowed)
        self.assertEqual(reason, "public legal research query")

    def test_gateway_returns_local_only_when_confidence_high(self):
        result = self.gateway.gateway_query(
            query="What are Delaware precedents for breach of fiduciary duty?",
            retrieval_result=self.sample_retrieval(confidence=72.0),
            use_external=True,
        )
        self.assertIsNone(result["external_results"])
        self.assertFalse(result["governance"]["external_called"])
        self.assertFalse(result["governance"]["blocked"])

    def test_gateway_calls_perplexity_when_confidence_low(self):
        with mock.patch.object(
            self.gateway,
            "query_perplexity",
            return_value={"answer": "External answer", "sources": ["https://example.com"], "model": "sonar-pro"},
        ):
            result = self.gateway.gateway_query(
                query="What are Delaware precedents for breach of fiduciary duty?",
                retrieval_result=self.sample_retrieval(confidence=20.0),
                use_external=True,
            )
        self.assertEqual(result["external_results"]["answer"], "External answer")
        self.assertTrue(result["governance"]["external_called"])
        self.assertEqual(result["sources"]["external"], ["https://example.com"])

    def test_gateway_blocks_unsafe_query_even_when_confidence_low(self):
        with mock.patch.object(self.gateway, "query_perplexity") as patched:
            result = self.gateway.gateway_query(
                query="Should we settle with Smith Corp for $2.5M in our case?",
                retrieval_result=self.sample_retrieval(confidence=15.0),
                use_external=True,
            )
        self.assertTrue(result["governance"]["blocked"])
        self.assertFalse(patched.called)
        self.assertIsNone(result["external_results"])

    def test_sanitize_response_catches_echoed_identifiers(self):
        sanitized = self.gateway.sanitizer.sanitize_response(
            "The answer references lawyer@example.com and 123-45-6789 in Smith v. Jones Corp."
        )
        self.assertNotIn("lawyer@example.com", sanitized)
        self.assertNotIn("123-45-6789", sanitized)

    def test_cache_hit_bypasses_second_external_call(self):
        with mock.patch.object(
            self.gateway,
            "query_perplexity",
            return_value={"answer": "External answer", "sources": ["https://example.com"], "model": "sonar-pro"},
        ) as patched:
            query = "What are Delaware precedents for breach of fiduciary duty?"
            retrieval = self.sample_retrieval(confidence=10.0)
            first = self.gateway.gateway_query(query=query, retrieval_result=retrieval, use_external=True)
            second = self.gateway.gateway_query(query=query, retrieval_result=retrieval, use_external=True)
        self.assertFalse(first["governance"]["cache_hit"])
        self.assertTrue(second["governance"]["cache_hit"])
        self.assertEqual(patched.call_count, 1)

    def test_gateway_works_without_optional_ollama_layer(self):
        with mock.patch.object(self.gateway.sanitizer, "sanitize_response", side_effect=lambda text: text):
            with mock.patch.object(
                self.gateway,
                "query_perplexity",
                return_value={"answer": "External answer", "sources": [], "model": "sonar-pro"},
            ):
                result = self.gateway.gateway_query(
                    query="What Delaware filing procedures apply to fiduciary duty claims?",
                    retrieval_result=self.sample_retrieval(confidence=18.0),
                    use_external=True,
                )
        self.assertTrue(result["governance"]["external_called"])


if __name__ == "__main__":
    unittest.main()
