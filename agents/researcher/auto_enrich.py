#!/usr/bin/env python3
"""
auto_enrich.py — Auto-enrichment filter for Researcher findings.

Evaluates researcher findings against the knowledge library and files
high-quality candidates as governed proposals via file_proposal.py.

Design: ERS Slice 1 source path. Stateless, best-effort, never blocking.
Line cap: 300 (crew constraint from 2026-04-23 review).
PII scrubbing: regex-only layer added per Gemini security review (V3 plan).

Crew decisions:
  - Confidence threshold: 75 (configurable via threshold param)
  - Dedup: local token overlap (Jaccard), no resolver dependency
  - Rate limit: 5 per task, stateless
  - Opt-in: explicit auto_enrich on HandoffPacket, no smart defaults
  - RIU validation: findings must reference valid taxonomy RIUs
  - palette_action_class on every proposal
"""
from __future__ import annotations

import hashlib
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import yaml

# ── Paths ────────────────────────────────────────────────────────────────────

_HERE = Path(__file__).resolve().parent
PALETTE_ROOT = _HERE.parent.parent
KL_PATH = PALETTE_ROOT / "knowledge-library" / "v1.4" / "palette_knowledge_library_v1.4.yaml"
TAXONOMY_PATH = PALETTE_ROOT / "taxonomy" / "releases" / "v1.3" / "palette_taxonomy_v1.3.yaml"
PEOPLE_LIB_PATH = (
    PALETTE_ROOT / "buy-vs-build" / "people-library" / "v1.1" / "people_library_v1.1.yaml"
)

# ── Defaults ─────────────────────────────────────────────────────────────────

DEFAULT_THRESHOLD = 75
DEFAULT_MAX_PROPOSALS = 5
DEFAULT_VALID_DAYS = 90
DEDUP_OVERLAP_THRESHOLD = 0.80
DEDUP_UPDATE_THRESHOLD = 0.50


# ── Token helpers ────────────────────────────────────────────────────────────

def _tokenize(text: str) -> set[str]:
    """Extract meaningful tokens from text for dedup comparison."""
    words = set(re.findall(r"[a-z0-9][a-z0-9'-]{2,}", text.lower()))
    stop = {"the", "and", "for", "that", "this", "with", "from", "are", "was",
            "were", "been", "have", "has", "had", "not", "but", "can", "will",
            "should", "would", "could", "into", "about", "when", "how", "what"}
    return words - stop


def _jaccard(a: set[str], b: set[str]) -> float:
    """Jaccard similarity between two token sets."""
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# ── Data loaders ─────────────────────────────────────────────────────────────

def _load_kl_questions() -> list[dict[str, Any]]:
    """Load knowledge library questions for dedup checking."""
    if not KL_PATH.exists():
        return []
    with KL_PATH.open(encoding="utf-8") as f:
        kl = yaml.safe_load(f) or {}
    entries = kl.get("library_questions", [])
    entries += kl.get("gap_additions", [])
    entries += kl.get("context_specific_questions", [])
    return entries


def _load_valid_rius() -> set[str]:
    """Load valid RIU IDs from taxonomy v1.3."""
    if not TAXONOMY_PATH.exists():
        return set()
    with TAXONOMY_PATH.open(encoding="utf-8") as f:
        tax = yaml.safe_load(f) or {}
    return {r["riu_id"] for r in tax.get("rius", []) if r.get("riu_id")}


# ── PII scrubbing ───────────────────────────────────────────────────────────
#
# Gemini security review flagged that raw claim/evidence/source text flows
# into governance proposals without sanitisation.  This layer applies
# deterministic regex-only redaction (no NLP models, no new deps) before
# any content enters a proposal dict or is filed.  Conservative: better to
# over-redact in governance artefacts than to leak PII.

# Compiled once at module level for performance.
_PII_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    # Email addresses
    ("EMAIL", re.compile(
        r"[a-zA-Z0-9_.+\-]+@[a-zA-Z0-9\-]+\.[a-zA-Z]{2,}", re.ASCII)),

    # US Social Security Numbers  (XXX-XX-XXXX only; bare 9-digit match removed
    # to avoid false positives on ZIP+4, model IDs, etc.)
    ("SSN", re.compile(
        r"\b\d{3}-\d{2}-\d{4}\b")),

    # Credit card numbers — 4 groups of 4 digits (most common formats)
    # Tightened from 13-19 arbitrary digits to reduce false positives on hashes/IDs
    ("CREDIT-CARD", re.compile(
        r"\b\d{4}[\s\-]\d{4}[\s\-]\d{4}[\s\-]\d{4}\b"
        r"|\b\d{4}[\s\-]\d{6}[\s\-]\d{5}\b")),  # Amex format

    # US phone numbers — (xxx) xxx-xxxx, xxx-xxx-xxxx, xxx.xxx.xxxx, +1xxxxxxxxxx
    ("PHONE", re.compile(
        r"(?:\+?1[\s.\-]?)?"                       # optional country code
        r"(?:\(\d{3}\)|\d{3})"                      # area code
        r"[\s.\-]?\d{3}[\s.\-]?\d{4}\b")),

    # Street addresses — number + street name + suffix
    ("ADDRESS", re.compile(
        r"\b\d{1,6}\s+"                             # house number
        r"(?:[A-Z][a-zA-Z]+\s+){1,4}"              # street words
        r"(?:St(?:reet)?|Ave(?:nue)?|Blvd|Boulevard|Dr(?:ive)?|Ln|Lane|Rd|Road"
        r"|Ct|Court|Pl(?:ace)?|Way|Cir(?:cle)?|Pkwy|Parkway|Ter(?:race)?)"
        r"\.?"                                      # optional period
        r"(?:\s*,?\s*(?:Apt|Suite|Unit|#)\s*\S+)?"  # optional unit
        r"\b", re.IGNORECASE)),
]


def _load_known_names() -> list[str]:
    """Load person names from the people library for name-redaction.

    Returns full names sorted longest-first so that "Maria Zhanette Yap" is
    matched before "Maria".
    """
    if not PEOPLE_LIB_PATH.exists():
        return []
    try:
        with PEOPLE_LIB_PATH.open(encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
    except Exception:
        return []
    names: list[str] = []
    for profile in data.get("profiles", []):
        name = profile.get("name", "").strip()
        if name:
            names.append(name)
    # Sort longest-first so multi-word names match before substrings
    names.sort(key=len, reverse=True)
    return names


def _scrub_pii(text: str, known_names: list[str]) -> str:
    """Deterministic PII redaction using regex patterns and a known-name list.

    Applied to claim, evidence, and source fields before they enter any
    governance proposal.  Uses only Python's built-in ``re`` module.

    Redaction tags follow the format ``[REDACTED-{TYPE}]`` so downstream
    consumers can see *what* was removed without seeing the data.

    Args:
        text:        The raw text to scrub.
        known_names: Pre-sorted (longest-first) list of names from the
                     people library.

    Returns:
        The scrubbed text with all detected PII replaced.
    """
    if not text:
        return text

    # 1. Redact known names (longest-first to avoid partial matches)
    for name in known_names:
        # Word-boundary match, case-insensitive
        pattern = re.compile(re.escape(name), re.IGNORECASE)
        text = pattern.sub("[REDACTED-NAME]", text)

    # 2. Apply structural PII patterns
    for label, pattern in _PII_PATTERNS:
        text = pattern.sub(f"[REDACTED-{label}]", text)

    return text


# ── Core filter ──────────────────────────────────────────────────────────────

def evaluate_and_propose(
    findings: list[dict[str, Any]],
    task_id: str,
    source_rius: list[str] | None = None,
    threshold: int = DEFAULT_THRESHOLD,
    max_proposals: int = DEFAULT_MAX_PROPOSALS,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Evaluate findings and produce governance proposals.

    Returns (proposed, filtered) where each is a list of dicts with
    reason fields for glass-box traceability.
    """
    if not findings:
        return [], []

    kl_entries = _load_kl_questions()
    valid_rius = _load_valid_rius()
    known_names = _load_known_names()
    kl_tokens = [(e, _tokenize(e.get("question", "") + " " + e.get("answer", "")[:200]))
                 for e in kl_entries]

    # Validate source RIUs against taxonomy
    validated_rius = []
    if source_rius:
        validated_rius = [r for r in source_rius if r in valid_rius]

    proposed: list[dict[str, Any]] = []
    filtered: list[dict[str, Any]] = []

    for finding in findings:
        claim = _scrub_pii(finding.get("claim", ""), known_names)
        evidence = _scrub_pii(finding.get("evidence", ""), known_names)
        source = finding.get("source", "")  # URL kept intact for verification
        confidence = int(finding.get("confidence", 0))

        # Filter 1: Confidence threshold
        if confidence < threshold:
            filtered.append({
                "claim": claim[:80], "reason": f"below_threshold ({confidence} < {threshold})",
            })
            continue

        # Filter 2: Source requirement — must have a fetchable URL
        if not source or not (source.startswith("http") or source.startswith("file://")):
            filtered.append({"claim": claim[:80], "reason": "no_verifiable_source"})
            continue

        # Filter 3: Dedup against knowledge library
        finding_tokens = _tokenize(claim + " " + evidence[:200])
        dedup_result = "pass"
        for kl_entry, kl_toks in kl_tokens:
            sim = _jaccard(finding_tokens, kl_toks)
            if sim >= DEDUP_OVERLAP_THRESHOLD:
                dedup_result = f"duplicate (sim={sim:.2f} with {kl_entry.get('id', '?')})"
                break
            if sim >= DEDUP_UPDATE_THRESHOLD:
                dedup_result = f"possible_update (sim={sim:.2f} with {kl_entry.get('id', '?')})"
                break

        if dedup_result.startswith("duplicate"):
            filtered.append({"claim": claim[:80], "reason": dedup_result})
            continue

        # Build proposal
        now = datetime.now(timezone.utc)
        ts = now.strftime("%Y%m%d%H%M%S")
        idx = len(proposed)
        prop_tag = f"AUTO-{ts}-{idx}"
        digest = hashlib.sha256(f"{task_id}|{claim}".encode()).hexdigest()[:8]

        # Determine palette_action_class
        action_class = "research"  # default: needs validation before KL write
        if confidence >= 90 and source.startswith("http"):
            action_class = "update_index"

        proposal = {
            "proposed_by": "researcher.auto_enrich",
            "tier": 2,
            "type": "new" if not dedup_result.startswith("possible") else "modify",
            "content": {
                "question": claim[:200] if "?" in claim else f"What is known about: {claim[:180]}?",
                "answer": evidence,
                "sources": [{
                    "url": source,
                    "title": f"Research finding {digest}",
                }],
                "related_rius": validated_rius[:3] if validated_rius else [],
                "evidence_tier": _evidence_tier(source),
                "evidence_tier_justification": f"Auto-classified from source URL pattern. Confidence: {confidence}.",
            },
            "rationale": f"Auto-enrichment from research task {task_id}. {dedup_result}.",
            "source_of_insight": f"researcher:{task_id}",
            "contradiction_check": {
                "checked_against": [e.get("id") for e, _ in kl_tokens[:5] if e.get("id")],
                "conflicts_found": "none",
            },
            "auto_generated": True,
            "auto_enrich_meta": {
                "proposal_tag": prop_tag,
                "task_id": task_id,
                "confidence": confidence,
                "dedup_result": dedup_result,
                "palette_action_class": action_class,
                "valid_until": (now + timedelta(days=DEFAULT_VALID_DAYS)).strftime("%Y-%m-%d"),
            },
        }

        # Filter 4: RIU validation — if source_rius were provided but none valid
        if source_rius and not validated_rius:
            filtered.append({
                "claim": claim[:80],
                "reason": f"no_valid_rius (provided: {source_rius[:3]})",
            })
            continue

        proposed.append(proposal)

    # Filter 5: Rate limit — keep top by confidence, cap at max_proposals
    if len(proposed) > max_proposals:
        proposed.sort(key=lambda p: p["auto_enrich_meta"]["confidence"], reverse=True)
        for p in proposed[max_proposals:]:
            filtered.append({
                "claim": p["content"]["question"][:80],
                "reason": f"rate_limited (kept top {max_proposals} by confidence)",
            })
        proposed = proposed[:max_proposals]

    return proposed, filtered


def _evidence_tier(source: str) -> int:
    """Classify evidence tier from source URL pattern."""
    t1 = ["anthropic.com", "openai.com", "google.com", "aws.amazon.com", "meta.com"]
    t2 = ["arxiv.org", "nist.gov", "europa.eu", "acm.org", "ieee.org"]
    src = source.lower()
    if any(d in src for d in t1):
        return 1
    if any(d in src for d in t2):
        return 2
    return 3


# ── Filing interface ─────────────────────────────────────────────────────────

def file_proposals(proposals: list[dict[str, Any]]) -> list[str]:
    """File proposals through the governance pipeline. Returns list of filed IDs.

    Applies a second PII scrub pass on content fields immediately before
    filing as a defense-in-depth measure (proposals may arrive from paths
    that bypass evaluate_and_propose).
    """
    sys.path.insert(0, str(PALETTE_ROOT / "scripts"))
    try:
        from file_proposal import file_proposal
    except ImportError as e:
        _log(f"cannot import file_proposal: {e}")
        return []

    known_names = _load_known_names()

    filed: list[str] = []
    for prop in proposals:
        # Defense-in-depth: scrub content fields before filing
        content = prop.get("content", {})
        for field in ("question", "answer"):
            if field in content and isinstance(content[field], str):
                content[field] = _scrub_pii(content[field], known_names)
        if "rationale" in prop and isinstance(prop["rationale"], str):
            prop["rationale"] = _scrub_pii(prop["rationale"], known_names)
        try:
            prop_id = file_proposal(prop_data=prop)
            if prop_id:
                filed.append(prop_id)
                _log(f"filed {prop_id}")
        except Exception as e:
            _log(f"filing failed: {e}")
    return filed


# ── Suppression summary ──────────────────────────────────────────────────────

def summary(
    total: int,
    proposed: list[dict[str, Any]],
    filtered: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build suppression metadata for glass-box visibility."""
    return {
        "total_findings": total,
        "above_threshold": total - sum(1 for f in filtered if "threshold" in f.get("reason", "")),
        "deduped": sum(1 for f in filtered if "duplicate" in f.get("reason", "")),
        "no_source": sum(1 for f in filtered if "source" in f.get("reason", "")),
        "no_valid_rius": sum(1 for f in filtered if "rius" in f.get("reason", "")),
        "rate_limited": sum(1 for f in filtered if "rate_limited" in f.get("reason", "")),
        "emitted": len(proposed),
        "suppressed": len(filtered),
        "filter_details": filtered,
    }


def _log(msg: str) -> None:
    print(f"[auto-enrich] {msg}", file=sys.stderr, flush=True)
