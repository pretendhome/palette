from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

# Competition demo guardrail, not a production certification boundary.

PATTERNS: dict[str, str] = {
    "case_number": r"\b\d{1,2}:\d{2}-[a-z]{2}-\d{4,6}\b",
    "docket": r"\b(?:No|Docket|Case)\s*\.?\s*\d{2,}-\d{3,}\b",
    "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
    "ein": r"\b\d{2}-\d{7}\b",
    "phone": r"\b(?:\+1[-. ]?)?(?:\(?\d{3}\)?[-. ]?)\d{3}[-. ]?\d{4}\b",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
    "dollar_amount": r"\$\s?[\d,]+(?:\.\d{2})?(?:\s*(?:million|billion|m|b))?\b",
    "date_specific": r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b",
    "party_v_party": r"\b[A-Z][A-Za-z&'.-]+\s+(?:v\.?|vs\.?)\s+[A-Z][A-Za-z0-9&'., -]+\b",
}

REPLACEMENTS: dict[str, str] = {
    "case_number": "[CASE_REF]",
    "docket": "[DOCKET_REF]",
    "ssn": "[SSN]",
    "ein": "[EIN]",
    "phone": "[PHONE]",
    "email": "[EMAIL]",
    "dollar_amount": "[AMOUNT]",
    "date_specific": "[DATE]",
    "party_v_party": "[CASE_NAME]",
}

ALLOWED_KEYWORDS = {
    "precedent",
    "precedents",
    "case law",
    "statute",
    "statutory",
    "regulation",
    "regulatory",
    "fiduciary",
    "delaware",
    "contract clause",
    "jurisdiction",
    "filing",
    "court rule",
    "published opinion",
}

BLOCKED_INDICATORS_DEFAULT = [
    "our client",
    "my client",
    "should we",
    "strategy",
    "settlement",
    "settle",
    "privileged",
    "attorney-client",
    "active case",
    "our case",
    "this matter",
]

CONTEXTUAL_PHRASES = [
    (re.compile(r"\bour client\b", re.IGNORECASE), "a client"),
    (re.compile(r"\bmy client\b", re.IGNORECASE), "a client"),
    (re.compile(r"\bour case\b", re.IGNORECASE), "a case"),
    (re.compile(r"\bthis matter\b", re.IGNORECASE), "the matter"),
]

PARTY_SUFFIXES = r"(?:Corp|Corporation|Inc|LLC|Ltd|Co|Company|LP|LLP)"
PARTY_NAME_RE = re.compile(
    rf"\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*\s+(?:{PARTY_SUFFIXES})|[A-Z][a-z]+\s+[A-Z][a-z]+)\b"
)


class QuerySanitizer:
    def __init__(self, config_path: str | Path | None = None):
        self.config_path = Path(config_path) if config_path else Path(__file__).with_name("config.yaml")
        self.custom_patterns: list[tuple[re.Pattern[str], str]] = []
        self.blocked_indicators = list(BLOCKED_INDICATORS_DEFAULT)
        self._load_config()

    def _load_config(self) -> None:
        if not self.config_path.exists():
            return
        with open(self.config_path, encoding="utf-8") as handle:
            config = yaml.safe_load(handle) or {}
        for pattern, replacement in config.get("custom_patterns", []):
            self.custom_patterns.append((re.compile(pattern, re.IGNORECASE), replacement))
        self.blocked_indicators = list(config.get("blocked_indicators", self.blocked_indicators))

    def detect_pii(self, query: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        matches: list[dict[str, str]] = []
        categories: set[str] = set()
        for pii_type, pattern in PATTERNS.items():
            for match in re.finditer(pattern, query, flags=re.IGNORECASE):
                categories.add(pii_type)
                matches.append({"type": pii_type, "match": match.group(0)})

        blocked_hits = [token for token in self.blocked_indicators if token.lower() in query.lower()]
        if blocked_hits:
            categories.add("blocked_indicator")

        if context:
            for party in context.get("client_names", []) + context.get("party_names", []):
                if party and re.search(re.escape(party), query, flags=re.IGNORECASE):
                    categories.add("party_name")
                    matches.append({"type": "party_name", "match": party})
            for ref in context.get("case_refs", []) + context.get("matter_refs", []):
                if ref and re.search(re.escape(ref), query, flags=re.IGNORECASE):
                    categories.add("matter_ref")
                    matches.append({"type": "matter_ref", "match": ref})

        if self._has_named_parties(query):
            categories.add("party_name")
        return {
            "categories": sorted(categories),
            "matches": matches,
            "blocked_indicators": blocked_hits,
        }

    def sanitize_query(self, query: str, context: dict[str, Any] | None = None) -> tuple[str, list[str]]:
        findings = self.detect_pii(query, context)
        sanitized = query
        for pii_type, pattern in PATTERNS.items():
            sanitized = re.sub(pattern, REPLACEMENTS[pii_type], sanitized, flags=re.IGNORECASE)
        for compiled, replacement in self.custom_patterns:
            sanitized = compiled.sub(replacement, sanitized)
        if context:
            for party in context.get("client_names", []) + context.get("party_names", []):
                sanitized = re.sub(re.escape(party), "[CLIENT]", sanitized, flags=re.IGNORECASE)
            for ref in context.get("case_refs", []) + context.get("matter_refs", []):
                sanitized = re.sub(re.escape(ref), "[CASE_REF]", sanitized, flags=re.IGNORECASE)
        sanitized = self._scrub_contextual_language(sanitized)
        sanitized = self._scrub_named_parties(sanitized)
        sanitized = self._normalize(sanitized)
        return sanitized, findings["categories"]

    def sanitize_response(self, response: str) -> str:
        sanitized, _ = self.sanitize_query(response)
        return sanitized

    def is_safe_for_external(self, query: str, context: dict[str, Any] | None = None) -> tuple[bool, str]:
        findings = self.detect_pii(query, context)
        lowered = query.lower()
        if findings["blocked_indicators"]:
            return False, f"blocked indicators: {', '.join(findings['blocked_indicators'])}"
        if any(cat in findings["categories"] for cat in {
            "case_number", "docket", "ssn", "ein", "email", "phone", "matter_ref"
        }):
            return False, "contains direct client or matter identifiers"
        if "party_name" in findings["categories"] and "dollar_amount" in findings["categories"]:
            return False, "contains party names with dollar amounts"
        if not any(keyword in lowered for keyword in ALLOWED_KEYWORDS):
            return False, "query is not clearly public legal research"
        return True, "public legal research query"

    def sanitize(self, text: str) -> str:
        sanitized, _ = self.sanitize_query(text)
        return sanitized

    def sanitize_result(self, text: str) -> str:
        return self.sanitize_response(text)

    def _has_named_parties(self, text: str) -> bool:
        return bool(PARTY_NAME_RE.search(text))

    def _scrub_named_parties(self, text: str) -> str:
        def repl(match: re.Match[str]) -> str:
            value = match.group(0)
            if value.startswith("["):
                return value
            return "[CLIENT]"
        return PARTY_NAME_RE.sub(repl, text)

    def _scrub_contextual_language(self, text: str) -> str:
        for pattern, replacement in CONTEXTUAL_PHRASES:
            text = pattern.sub(replacement, text)
        return text

    def _normalize(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\s+([?.!,;:])", r"\1", text)
        return text.strip()
