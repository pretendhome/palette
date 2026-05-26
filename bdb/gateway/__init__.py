from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Any
from urllib import error, request

import yaml

from .audit import AuditLogger
from .cache import PerplexityCache
from .fallback import LocalFallback
from .rate_limiter import RateLimiter
from .sanitizer import QuerySanitizer

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG_PATH = BASE_DIR / "config.yaml"
PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"


class PerplexityGateway:
    def __init__(
        self,
        config_path: str | Path | None = None,
        cache: PerplexityCache | None = None,
        audit: AuditLogger | None = None,
        rate_limiter: RateLimiter | None = None,
        sanitizer: QuerySanitizer | None = None,
    ):
        self.config_path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
        self.config = self._load_config()
        self.threshold = int(self.config.get("gateway", {}).get("confidence_threshold", 40))
        self.timeout = int(self.config.get("gateway", {}).get("timeout_seconds", 15))
        self.cache_ttl = int(self.config.get("gateway", {}).get("cache_ttl_hours", 24)) * 3600
        self.default_model = self.config.get("gateway", {}).get("perplexity_model", "sonar-pro")
        self.cache = cache or PerplexityCache()
        self.audit = audit or AuditLogger()
        self.rate_limiter = rate_limiter or RateLimiter(limit=int(self.config.get("gateway", {}).get("max_external_calls_per_day", 100)))
        self.sanitizer = sanitizer or QuerySanitizer(self.config_path)
        self.fallback = LocalFallback()

    def gateway_query(
        self,
        query: str,
        retrieval_result: dict[str, Any],
        user_context: dict[str, Any] | None = None,
        use_external: bool = False,
        user_id: str = "default_user",
        session_id: str = "session_1",
    ) -> dict[str, Any]:
        event = {
            "original_query": query,
            "query_type": self._classify_query_type(query),
            "user_id": user_id,
            "session_id": session_id,
            "timestamp": time.time(),
            "sanitized_query": None,
        }
        result = self._build_local_only_result(query, retrieval_result, use_external)
        if not use_external:
            return result
        if not self.needs_external(retrieval_result, query):
            return result

        is_safe, safety_reason = self.sanitizer.is_safe_for_external(query, user_context)
        sanitized_query, pii_detected = self.sanitizer.sanitize_query(query, user_context)
        result["sanitized_query"] = sanitized_query
        result["governance"]["sanitization_applied"] = True
        result["governance"]["pii_detected"] = pii_detected
        event["sanitized_query"] = sanitized_query

        if not is_safe:
            result["governance"].update({"blocked": True, "block_reason": safety_reason})
            result["merged_context"] = self._local_context(retrieval_result, blocked_reason=safety_reason)
            self.audit.log_blocked(event, safety_reason)
            return result

        if sanitized_query.strip() == query.strip() and pii_detected:
            reason = "sanitized query did not become more generic"
            result["governance"].update({"blocked": True, "block_reason": reason})
            result["merged_context"] = self._local_context(retrieval_result, blocked_reason=reason)
            self.audit.log_blocked(event, reason)
            return result

        cached = self.cache.get(sanitized_query)
        if cached:
            result["external_results"] = cached
            result["sources"]["external"] = cached.get("sources", [])
            result["governance"].update({"external_called": True, "cache_hit": True})
            result["merged_context"] = self.merge_results(retrieval_result, cached)
            self.audit.log_success(event, cached)
            return result

        if not self.rate_limiter.check_limit(user_id):
            fallback = self.fallback.handle_rate_limited()
            result["governance"].update({"blocked": True, "block_reason": fallback["reason"]})
            result["merged_context"] = self._local_context(retrieval_result, blocked_reason=fallback["reason"])
            self.audit.log_blocked(event, fallback["reason"])
            return result

        try:
            external = self.query_perplexity(sanitized_query, retrieval_result=retrieval_result)
        except Exception as exc:  # pragma: no cover - defensive path
            fallback = self.fallback.handle_perplexity_error(str(exc))
            result["governance"].update({"blocked": True, "block_reason": fallback["reason"]})
            result["merged_context"] = self._local_context(retrieval_result, blocked_reason=fallback["reason"])
            self.audit.log_error(event, str(exc))
            return result

        external["answer"] = self.sanitizer.sanitize_response(external.get("answer", ""))
        result["external_results"] = external
        result["sources"]["external"] = external.get("sources", [])
        result["governance"].update({"external_called": True, "cache_hit": False})
        result["merged_context"] = self.merge_results(retrieval_result, external)
        self.cache.set(sanitized_query, external, ttl=self.cache_ttl)
        self.audit.log_success(event, external)
        return result

    def needs_external(self, local_results: dict[str, Any], query: str) -> bool:
        confidence = float(local_results.get("confidence") or 0)
        return confidence < self.threshold

    def _build_targeted_system_prompt(self, retrieval_result: dict[str, Any]) -> str:
        """Build a taxonomy-aware system prompt that tells Perplexity what we already know."""
        riu_id = retrieval_result.get("riu_id", "unknown")
        riu_name = retrieval_result.get("riu_name", "")
        confidence = float(retrieval_result.get("confidence") or 0)
        knowledge = retrieval_result.get("knowledge", [])

        known_questions = [k["question"] for k in knowledge[:3] if k.get("question")]

        prompt = (
            f"You are answering a {riu_name} ({riu_id}) query for a governed AI system.\n"
            f"Local confidence: {confidence:.0f}%. "
        )
        if confidence > 20:
            prompt += "Answer is partially known but needs supplementation.\n"
        else:
            prompt += "No local answer found.\n"

        if known_questions:
            prompt += f"Already known locally: {'; '.join(q[:80] for q in known_questions[:2])}. Do not repeat this.\n"

        prompt += (
            "Focus on: public sources, authoritative citations, recent developments (2024-2026).\n"
            "Return: direct answer with citations. No client-specific advice."
        )
        return prompt

    def _formulate_targeted_query(self, query: str, retrieval_result: dict[str, Any]) -> str:
        """Shape the search query using what the taxonomy already knows is missing."""
        riu_id = retrieval_result.get("riu_id", "")
        riu_name = retrieval_result.get("riu_name", "")
        confidence = float(retrieval_result.get("confidence") or 0)
        knowledge = retrieval_result.get("knowledge", [])

        known_summary = "; ".join(
            k.get("question", "")[:80] for k in knowledge[:2] if k.get("question")
        )

        if confidence < 15:
            gap_type = "completely absent from knowledge library"
        elif confidence < 30:
            gap_type = "partially covered — missing key precedents or recent developments"
        else:
            gap_type = "covered but confidence is marginal — may need current sources"

        if known_summary:
            return (
                f"Context: This question relates to {riu_name} ({riu_id}). "
                f"Known: {known_summary}. "
                f"Knowledge gap: {gap_type}. "
                f"Query: {query}"
            )
        return query

    def query_perplexity(self, sanitized_query: str, model: str | None = None,
                         retrieval_result: dict[str, Any] | None = None) -> dict[str, Any]:
        api_key = os.environ.get("PERPLEXITY_API_KEY")
        if not api_key:
            raise RuntimeError("PERPLEXITY_API_KEY is not set")

        # Use targeted system prompt if retrieval context is available
        if retrieval_result and retrieval_result.get("riu_id"):
            system_content = self._build_targeted_system_prompt(retrieval_result)
            sanitized_query = self._formulate_targeted_query(sanitized_query, retrieval_result)
        else:
            system_content = (
                "You answer public legal research questions only. "
                "Do not infer client-specific advice. Cite public sources when possible."
            )

        payload = {
            "model": model or self.default_model,
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": sanitized_query},
            ],
        }
        req = request.Request(
            PERPLEXITY_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                body = json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as exc:  # pragma: no cover - network dependent
            detail = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"Perplexity HTTP {exc.code}: {detail}") from exc
        except error.URLError as exc:  # pragma: no cover - network dependent
            raise RuntimeError(f"Perplexity network error: {exc.reason}") from exc

        choices = body.get("choices", [])
        message = choices[0].get("message", {}) if choices else {}
        citations = body.get("citations") or []
        return {
            "answer": message.get("content", ""),
            "sources": citations,
            "model": body.get("model", model or self.default_model),
        }

    def merge_results(self, local: dict[str, Any], external: dict[str, Any]) -> str:
        local_context = self._local_context(local)
        external_answer = external.get("answer", "").strip()
        external_sources = external.get("sources", [])
        lines = [local_context]
        lines.append("\n[EXTERNAL:Perplexity]")
        lines.append(external_answer or "No external answer returned.")
        if external_sources:
            lines.append("Sources:")
            lines.extend(f"- {source}" for source in external_sources)
        return "\n".join(lines).strip()

    def process_query(self, query: str, user_id: str = "default_user", session_id: str = "session_1", retrieval_result: dict[str, Any] | None = None, use_external: bool = False, user_context: dict[str, Any] | None = None) -> dict[str, Any]:
        retrieval_result = retrieval_result or {}
        return self.gateway_query(
            query=query,
            retrieval_result=retrieval_result,
            user_context=user_context,
            use_external=use_external,
            user_id=user_id,
            session_id=session_id,
        )

    def _load_config(self) -> dict[str, Any]:
        if not self.config_path.exists():
            return {}
        with open(self.config_path, encoding="utf-8") as handle:
            return yaml.safe_load(handle) or {}

    def _build_local_only_result(self, query: str, retrieval_result: dict[str, Any], external_requested: bool) -> dict[str, Any]:
        return {
            "query": query,
            "sanitized_query": None,
            "local_results": retrieval_result,
            "external_results": None,
            "merged_context": self._local_context(retrieval_result),
            "sources": {
                "local": self._local_sources(retrieval_result),
                "external": [],
            },
            "governance": {
                "external_requested": external_requested,
                "external_called": False,
                "blocked": False,
                "block_reason": None,
                "sanitization_applied": False,
                "pii_detected": [],
                "cache_hit": False,
            },
        }

    def _local_context(self, retrieval_result: dict[str, Any], blocked_reason: str | None = None) -> str:
        lines = ["[LOCAL]"]
        if retrieval_result.get("riu_id"):
            lines.append(
                f"Classification: {retrieval_result.get('riu_id')} ({retrieval_result.get('riu_name') or 'unknown'})"
            )
        if retrieval_result.get("confidence") is not None:
            lines.append(f"Confidence: {float(retrieval_result.get('confidence') or 0):.1f}")
        context = retrieval_result.get("context") or ""
        if context:
            lines.append(context.strip())
        for entry in retrieval_result.get("knowledge", [])[:3]:
            lines.append(f"- {entry.get('lib_id')}: {entry.get('question', '')}")
        if blocked_reason:
            lines.append(f"External research blocked: {blocked_reason}")
        return "\n".join(lines).strip()

    def _local_sources(self, retrieval_result: dict[str, Any]) -> list[str]:
        return [entry.get("lib_id") for entry in retrieval_result.get("knowledge", []) if entry.get("lib_id")]

    def _classify_query_type(self, query: str) -> str:
        lowered = query.lower()
        if any(token in lowered for token in ["precedent", "case law", "fiduciary", "delaware", "court", "statute", "regulation", "filing"]):
            return "legal_precedent"
        return "general_knowledge"


def gateway_query(
    query: str,
    retrieval_result: dict[str, Any],
    user_context: dict[str, Any] | None = None,
    use_external: bool = False,
) -> dict[str, Any]:
    gateway = PerplexityGateway()
    return gateway.gateway_query(
        query=query,
        retrieval_result=retrieval_result,
        user_context=user_context,
        use_external=use_external,
    )
