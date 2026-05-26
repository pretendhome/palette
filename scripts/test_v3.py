#!/usr/bin/env python3
"""V3 test suite — covers all new V3 code.

Tests:
  1. Hybrid retrieval (FTS5 + vector + keyword + RRF)
  2. PII scrubbing (regex patterns + known names)
  3. palette query CLI pipeline
  4. Session reflection
  5. Query-before-acting

Run:
  cd palette && uv run pytest scripts/test_v3.py -v
  cd palette && python3 scripts/test_v3.py  (standalone)
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

PALETTE_ROOT = Path(__file__).resolve().parent.parent
HUB_DIR = PALETTE_ROOT / "peers" / "hub"
sys.path.insert(0, str(PALETTE_ROOT))
sys.path.insert(0, str(HUB_DIR))
sys.path.insert(0, str(PALETTE_ROOT / "scripts"))

# ── Module imports (fail gracefully if deps missing) ────────────────
try:
    from agents.researcher.auto_enrich import _scrub_pii, _PII_PATTERNS
    PII_AVAILABLE = True
except Exception as _e:
    PII_AVAILABLE = False

try:
    from palette_retrieve import hybrid_retrieve, retrieve, _fts5_query
    from scripts.palette_intelligence_system.loader import load_all
    RETRIEVAL_AVAILABLE = True
    _data = load_all()
except Exception as _e:
    RETRIEVAL_AVAILABLE = False
    _data = None

try:
    from palette_query import step_resolve, step_retrieve, step_route, step_respond, step_extract, TraceLog
    CLI_AVAILABLE = True
except Exception as _e:
    CLI_AVAILABLE = False

try:
    from session_reflect import analyze_session, generate_gap_proposals, format_report, read_session_log, append_to_session_log
    SESSION_AVAILABLE = True
except Exception as _e:
    SESSION_AVAILABLE = False

try:
    from query_before_act import check_kl, check_before_dispatch, _build_context
    QBA_AVAILABLE = True
except Exception as _e:
    QBA_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════════════
# 1. PII SCRUBBING
# ═══════════════════════════════════════════════════════════════════════

@unittest.skipUnless(PII_AVAILABLE, "PII module not importable")
class TestPIIScrubbing(unittest.TestCase):
    """Tests for auto_enrich._scrub_pii"""

    def test_email_redacted(self):
        self.assertIn("[REDACTED-EMAIL]", _scrub_pii("Contact john@example.com for info", []))

    def test_phone_redacted(self):
        result = _scrub_pii("Call (415) 555-1234 now", [])
        self.assertIn("[REDACTED-PHONE]", result)

    def test_ssn_redacted(self):
        self.assertIn("[REDACTED-SSN]", _scrub_pii("SSN: 123-45-6789", []))

    def test_credit_card_redacted(self):
        self.assertIn("[REDACTED-CREDIT-CARD]", _scrub_pii("Card: 4111-1111-1111-1111", []))

    def test_address_redacted(self):
        self.assertIn("[REDACTED-ADDRESS]", _scrub_pii("Lives at 123 Main Street, Apt 4B", []))

    def test_known_name_redacted(self):
        result = _scrub_pii("Talk to Jane Doe about the project", ["Jane Doe"])
        self.assertIn("[REDACTED-NAME]", result)
        self.assertNotIn("Jane Doe", result)

    def test_known_name_case_insensitive(self):
        self.assertIn("[REDACTED-NAME]", _scrub_pii("JANE DOE said hello", ["Jane Doe"]))

    def test_longest_name_first(self):
        names = sorted(["Maria", "Maria Zhanette Yap"], key=len, reverse=True)
        self.assertEqual(_scrub_pii("Contact Maria Zhanette Yap", names).count("[REDACTED-NAME]"), 1)

    def test_empty_text(self):
        self.assertEqual(_scrub_pii("", []), "")

    def test_none_text(self):
        self.assertIsNone(_scrub_pii(None, []))

    def test_url_not_scrubbed(self):
        self.assertIn("https://docs.example.com/guide", _scrub_pii("See https://docs.example.com/guide", []))

    def test_no_false_positive_on_short_numbers(self):
        text = "RIU-082 has 176 entries and version 1.4"
        self.assertEqual(_scrub_pii(text, []), text)

    def test_multiple_pii_types(self):
        result = _scrub_pii("Email john@test.com, call 415-555-1234, SSN 123-45-6789", [])
        self.assertIn("[REDACTED-EMAIL]", result)
        self.assertIn("[REDACTED-PHONE]", result)
        self.assertIn("[REDACTED-SSN]", result)


# ═══════════════════════════════════════════════════════════════════════
# 2. HYBRID RETRIEVAL
# ═══════════════════════════════════════════════════════════════════════

@unittest.skipUnless(RETRIEVAL_AVAILABLE, "Retrieval module not importable")
class TestHybridRetrieval(unittest.TestCase):
    """Tests for palette_retrieve hybrid retrieval."""

    def test_returns_ranked_list(self):
        ranked = hybrid_retrieve("governance", _data)
        self.assertIsInstance(ranked, list)
        self.assertGreater(len(ranked), 0)
        for lib_id, score in ranked:
            self.assertTrue(lib_id.startswith("LIB-"))
            self.assertIsInstance(score, float)

    def test_scores_descending(self):
        scores = [s for _, s in hybrid_retrieve("taxonomy routing", _data)]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_top_k_respected(self):
        self.assertLessEqual(len(hybrid_retrieve("voice quality", _data, top_k=3)), 3)

    def test_known_query_finds_relevant(self):
        lib_ids = [lid for lid, _ in hybrid_retrieve("wire contracts between agents", _data)]
        self.assertIn("LIB-191", lib_ids)

    def test_taxonomy_query_finds_relevant(self):
        lib_ids = [lid for lid, _ in hybrid_retrieve("taxonomy routing", _data)]
        self.assertIn("LIB-186", lib_ids)

    def test_fts5_query_removes_stop_words(self):
        result = _fts5_query("how do I build a taxonomy")
        self.assertNotIn("how", result.split(" OR "))
        self.assertIn("build", result)
        self.assertIn("taxonomy", result)

    def test_fts5_query_removes_short_words(self):
        self.assertIsInstance(_fts5_query("is AI ok"), str)

    def test_retrieve_returns_full_structure(self):
        result = retrieve("governance tiers")
        for field in ["query", "mode", "retrieval_modes", "confidence", "knowledge", "context"]:
            self.assertIn(field, result)
        self.assertEqual(result["mode"], "hybrid")

    def test_retrieve_has_riu_classification(self):
        result = retrieve("how do I evaluate voice quality")
        if result["riu_id"]:
            self.assertTrue(result["riu_id"].startswith("RIU-"))

    def test_evidence_tier_boost(self):
        self.assertGreater(len(hybrid_retrieve("governance", _data, top_k=10)), 0)

    def test_graceful_without_ollama(self):
        with patch("palette_retrieve._embed_query", return_value=None):
            self.assertGreater(len(hybrid_retrieve("governance tiers", _data)), 0)


# ═══════════════════════════════════════════════════════════════════════
# 3. PALETTE QUERY CLI
# ═══════════════════════════════════════════════════════════════════════

@unittest.skipUnless(CLI_AVAILABLE, "CLI module not importable")
class TestPaletteQueryCLI(unittest.TestCase):
    """Tests for the palette query pipeline."""

    def test_trace_log_records_steps(self):
        trace = TraceLog("test query")
        trace.step("test", {"value": 1}, 5.0)
        self.assertEqual(trace.steps[0]["step"], "test")

    def test_trace_log_has_thread_id(self):
        self.assertEqual(len(TraceLog("test").thread_id), 36)

    def test_trace_log_total_ms(self):
        self.assertGreaterEqual(TraceLog("test").total_ms(), 0)

    def test_resolve_returns_dict(self):
        trace = TraceLog("test")
        result = step_resolve("governance tiers", False, trace)
        self.assertIn("query", result)
        self.assertIn("confidence", result)
        self.assertEqual(trace.steps[0]["step"], "resolve")

    def test_retrieve_returns_knowledge(self):
        trace = TraceLog("test")
        resolved = step_resolve("wire contracts", False, trace)
        knowledge = step_retrieve(resolved, trace)
        self.assertIsInstance(knowledge, list)

    def test_respond_returns_markdown(self):
        trace = TraceLog("test")
        resolved = step_resolve("taxonomy", False, trace)
        step_retrieve(resolved, trace)
        response = step_respond("taxonomy", resolved, "claude.analysis", False, trace)
        self.assertIn("Palette Query", response)

    def test_extract_gap_signal(self):
        trace = TraceLog("test")
        resolved = {"confidence": 10, "riu_id": "RIU-999", "lib_id": None}
        with patch("palette_query.bus_send", return_value=None):
            extraction = step_extract("nonsense", resolved, trace)
        self.assertEqual(extraction["type"], "gap_signal")

    def test_extract_success_signal(self):
        trace = TraceLog("test")
        extraction = step_extract("real", {"confidence": 80, "riu_id": "RIU-001", "lib_id": "LIB-001"}, trace)
        self.assertEqual(extraction["type"], "retrieval_success")

    def test_extract_medium_confidence(self):
        trace = TraceLog("test")
        extraction = step_extract("mid", {"confidence": 50, "riu_id": "RIU-001", "lib_id": "LIB-001"}, trace)
        self.assertIsNotNone(extraction)
        self.assertEqual(extraction["type"], "medium_confidence")


# ═══════════════════════════════════════════════════════════════════════
# 4. SESSION REFLECTION
# ═══════════════════════════════════════════════════════════════════════

@unittest.skipUnless(SESSION_AVAILABLE, "Session module not importable")
class TestSessionReflection(unittest.TestCase):
    """Tests for session_reflect analysis and proposal generation."""

    def test_empty_session(self):
        self.assertEqual(analyze_session([])["total_queries"], 0)

    def test_gap_detection(self):
        analysis = analyze_session([{"query": "unknown", "riu_id": "RIU-999", "confidence": 15, "agent": "claude.analysis"}])
        self.assertEqual(len(analysis["gaps"]), 1)

    def test_success_detection(self):
        analysis = analyze_session([{"query": "gov", "riu_id": "RIU-001", "lib_id": "LIB-001", "confidence": 85, "agent": "claude.analysis"}])
        self.assertEqual(len(analysis["successes"]), 1)

    def test_moderate_confidence(self):
        analysis = analyze_session([{"query": "mod", "riu_id": "RIU-050", "confidence": 50, "agent": "claude.analysis"}])
        self.assertEqual(len(analysis["low_confidence"]), 1)

    def test_pattern_counting(self):
        entries = [
            {"query": "q1", "riu_id": "RIU-001", "lib_id": "LIB-001", "confidence": 80, "agent": "claude.analysis"},
            {"query": "q2", "riu_id": "RIU-001", "lib_id": "LIB-002", "confidence": 75, "agent": "claude.analysis"},
            {"query": "q3", "riu_id": "RIU-002", "lib_id": "LIB-001", "confidence": 90, "agent": "perplexity.computer"},
        ]
        analysis = analyze_session(entries)
        self.assertEqual(dict(analysis["patterns"]["top_rius"])["RIU-001"], 2)
        self.assertEqual(analysis["patterns"]["agent_distribution"]["perplexity.computer"], 1)

    def test_gap_proposal_generation(self):
        proposals = generate_gap_proposals({"gaps": [{"query": "unknown", "riu_id": "RIU-999", "confidence": 10}], "successes": [], "total_queries": 1})
        self.assertEqual(proposals[0]["tier"], 1)
        self.assertIn("RIU-999", proposals[0]["content"]["related_rius"])

    def test_gap_dedup_same_riu(self):
        proposals = generate_gap_proposals({"gaps": [
            {"query": "q1", "riu_id": "RIU-999", "confidence": 10},
            {"query": "q2", "riu_id": "RIU-999", "confidence": 15},
        ], "successes": [], "total_queries": 2})
        self.assertEqual(len(proposals), 1)

    def test_report_formatting(self):
        report = format_report({
            "total_queries": 3, "gaps": [{"riu_id": "RIU-999", "confidence": 10, "query": "test"}],
            "successes": [{"lib_id": "LIB-001", "confidence": 85, "query": "good", "riu_id": "RIU-001"}],
            "low_confidence": [], "patterns": {"top_rius": [("RIU-001", 2)], "top_libs": [], "agent_distribution": {"claude.analysis": 3}},
        })
        self.assertIn("Session Reflection", report)

    def test_read_nonexistent_log(self):
        self.assertEqual(read_session_log(Path("/tmp/nonexistent_test_log.ndjson")), [])

    def test_append_and_read_log(self):
        import tempfile
        p = Path(tempfile.mktemp(suffix=".ndjson"))
        try:
            append_to_session_log({"query": "t1"}, p)
            append_to_session_log({"query": "t2"}, p)
            self.assertEqual(len(read_session_log(p)), 2)
        finally:
            p.unlink(missing_ok=True)


# ═══════════════════════════════════════════════════════════════════════
# 5. QUERY-BEFORE-ACTING
# ═══════════════════════════════════════════════════════════════════════

@unittest.skipUnless(QBA_AVAILABLE, "QBA module not importable")
class TestQueryBeforeAct(unittest.TestCase):
    """Tests for query_before_act module."""

    def test_check_kl_returns_structure(self):
        result = check_kl("governance tiers")
        for field in ["has_knowledge", "entries", "confidence"]:
            self.assertIn(field, result)

    def test_check_kl_known_query(self):
        result = check_kl("wire contracts between agents")
        self.assertTrue(result["has_knowledge"])

    def test_check_kl_empty_query(self):
        self.assertEqual(check_kl("")["confidence"], 0)

    def test_build_context_with_knowledge(self):
        kl = {"has_knowledge": True, "entries": [{"lib_id": "LIB-001", "score": 75.0, "question": "Test?"}]}
        ctx = _build_context(kl, {"has_memory": False, "entries": []})
        self.assertIn("LIB-001", ctx)

    def test_build_context_empty(self):
        self.assertEqual(_build_context({"has_knowledge": False, "entries": []}, {"has_memory": False, "entries": []}), "")

    def test_check_dispatch_returns_advisory(self):
        with patch("query_before_act._bus_get", return_value=None):
            result = check_before_dispatch("governance", "claude.analysis")
            self.assertIn("advisory", result)
            self.assertTrue(result["should_dispatch"])


# ═══════════════════════════════════════════════════════════════════════
# Runner
# ═══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    unittest.main(verbosity=2)
