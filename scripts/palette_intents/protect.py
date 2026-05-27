#!/usr/bin/env python3
"""palette protect — Governance gate for sensitive queries.

Usage:
  palette protect "What's our exposure if the majority member was self-dealing?"
  palette protect --matter sarah-llc-001 "Should we settle?"
  palette protect --json "Is this query safe for external research?"

Produces: GateDecision artifact (BLOCK or ALLOW with sanitized rewrite).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts.palette_intents.infra import (
    BOLD,
    CYAN,
    DIM,
    GREEN,
    RED,
    RESET,
    WHITE,
    YELLOW,
    IntentState,
    IntegrityCard,
    build_integrity_card_fast,
    bus_post,
    emit_integrity_signal,
    format_pis_line,
    palette_checkpoint,
    pis_summary,
    print_unvalidated_warning,
    resolve_query,
    store_artifact,
)

# ── Strategy / Privilege Detection ──────────────────────────────────────

STRATEGY_INDICATORS = [
    "our exposure",
    "our position",
    "our strategy",
    "our approach",
    "our side",
    "our argument",
    "our case",
    "our leverage",
    "our weakness",
    "their weakness",
    "should we",
    "our client",
    "my client",
    "this matter",
    "privileged",
    "attorney-client",
    "work product",
    "settlement",
    "settle",
    "active case",
    "opposing counsel",
    "negotiation position",
    "confidential",
    "internal strategy",
    "do not share",
    "off the record",
    "between us",
    "not for external",
]


def detect_strategy_language(query: str) -> list[str]:
    """Detect strategy/privilege indicators in query."""
    lowered = query.lower()
    return [ind for ind in STRATEGY_INDICATORS if ind in lowered]


# ── Semantic Strategy Classification ────────────────────────────────────


def _semantic_strategy_check(query: str) -> str | None:
    """Use small local model to detect privilege/strategy intent.

    Only called when keyword check passes (second gate).
    Returns reason string if blocked, None if safe.
    """
    from urllib import request

    prompt = f"""Classify this query. Is it about INTERNAL strategy/privilege (client-specific, confidential, should not be shared externally) or PUBLIC research (general knowledge anyone could ask)?

QUERY: "{query}"

Answer ONLY one word: INTERNAL or PUBLIC"""

    payload = json.dumps({
        "model": "qwen2.5:3b",
        "prompt": prompt,
        "stream": False,
    }).encode()
    req = request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read()).get("response", "").strip().upper()
            if "INTERNAL" in result[:20]:
                return "internal strategy detected by semantic classifier"
    except Exception:
        pass  # If model unavailable, fail open (allow) — keyword check already passed
    return None


# ── Referential Redaction ───────────────────────────────────────────────


def build_redaction_map(query: str, blocked: list[str]) -> dict[str, str]:
    """Build ephemeral token map for blocked entities."""
    redaction_map = {}
    for i, entity in enumerate(blocked):
        token = f"[Entity {chr(65 + i)}]"  # [Entity A], [Entity B], ...
        redaction_map[token] = entity
    return redaction_map


# ── Local Knowledge Helpers ─────────────────────────────────────────────


def _summarize_kl(entry: dict) -> dict:
    """Extract key fields from a knowledge entry for artifact storage."""
    return {
        "id": entry.get("lib_id", entry.get("id", "")),
        "question": entry.get("question", entry.get("title", "")),
        "evidence_tier": entry.get("evidence_tier", None),
    }


def _build_local_answer(query: str, knowledge: list[dict]) -> str:
    """Build a local answer from knowledge entries. No external calls."""
    parts = []
    for entry in knowledge[:3]:
        q = entry.get("question", entry.get("title", ""))
        a = entry.get("answer_excerpt", entry.get("answer", entry.get("content", "")))
        if q and a:
            parts.append(f"**{q}**\n{a}")
    return "\n\n".join(parts) if parts else None


# ── Safe Rewrite ────────────────────────────────────────────────────────


def attempt_safe_rewrite(query: str, blocked: list[str]) -> str | None:
    """Try to produce a sanitized version safe for external research.

    Returns None if query is fundamentally privileged (no safe rewrite possible).
    """
    # If strategy language is the core of the query, no safe rewrite
    lowered = query.lower()
    strategy_core = any(
        ind in lowered
        for ind in ["our exposure", "should we", "our strategy", "our position", "our leverage"]
    )
    if strategy_core:
        return None

    # Otherwise, try stripping blocked indicators and generalizing
    try:
        sys.path.insert(0, str(REPO_ROOT))
        from bdb.gateway.sanitizer import QuerySanitizer

        sanitizer = QuerySanitizer()
        sanitized, _categories = sanitizer.sanitize_query(query)
        safe, _reason = sanitizer.is_safe_for_external(sanitized)
        if safe:
            return sanitized
    except Exception:
        pass

    return None


# ── Main PROTECT Logic ──────────────────────────────────────────────────


def run_protect(
    query: str,
    matter_id: str | None = None,
    show_json: bool = False,
) -> tuple[dict, IntentState]:
    """Execute PROTECT intent. Returns (GateDecision dict, final IntentState)."""

    t0 = time.time()

    # 1. Resolve RIU
    resolved = resolve_query(query)
    riu_id = resolved.get("riu_id")
    riu_name = resolved.get("riu_name", "")
    confidence = resolved.get("confidence", 0)
    classification = resolved.get("classification", "internal_only")

    # 2. Build state
    state = IntentState(
        intent="PROTECT",
        query=query,
        riu=riu_id,
        riu_name=riu_name,
        boundary="local_only",  # PROTECT defaults to local
        confidence=confidence,
        matter_id=matter_id,
    )

    # 3. Integrity card (fast path — use resolve result, skip full PIS load)
    knowledge_entries = resolved.get("knowledge", [])
    card = build_integrity_card_fast(riu_id or "unknown", classification, len(knowledge_entries))
    state.integrity_card = asdict(card)
    state.posture = card.posture

    # 4. Detect strategy/privilege language
    blocked_entities = detect_strategy_language(query)

    # 5. PII detection via sanitizer
    pii_found: list[str] = []
    pii_categories: set[str] = set()
    try:
        sys.path.insert(0, str(REPO_ROOT))
        from bdb.gateway.sanitizer import QuerySanitizer

        sanitizer = QuerySanitizer()
        findings = sanitizer.detect_pii(query)
        pii_found = [m["match"] for m in findings.get("matches", [])]
        pii_categories = set(findings.get("categories", []))
    except Exception:
        pass

    # 6. Determine action
    all_blocked = list(set(blocked_entities + pii_found))

    # Fail safe: empty or very short queries default to BLOCK
    if not query.strip() or len(query.strip()) < 5:
        action = "BLOCK"
        reason_str = "query too short or empty — defaulting to local_only"
        all_blocked = []
    elif blocked_entities or pii_found or pii_categories or classification == "internal_only":
        action = "BLOCK"
        reason = []
        if blocked_entities:
            reason.append(f"strategy language detected: {', '.join(blocked_entities[:3])}")
        if pii_found:
            reason.append(f"PII found: {', '.join(pii_found[:3])}")
        if pii_categories and not pii_found and not blocked_entities:
            reason.append(f"PII category detected: {', '.join(sorted(pii_categories))}")
        if classification == "internal_only" and not blocked_entities and not pii_found and not pii_categories:
            reason.append(f"RIU {riu_id} classified as internal_only")
        reason_str = "; ".join(reason)
    else:
        # 6b. Semantic strategy check (second gate — only if keywords didn't catch it)
        # Uses small model to detect privilege/strategy intent that keywords miss
        semantic_block = _semantic_strategy_check(query)
        if semantic_block:
            action = "BLOCK"
            reason_str = f"semantic analysis: {semantic_block}"
            all_blocked = [semantic_block]
        else:
            action = "ALLOW"
            reason_str = "query appears safe for governed external research"

    # 7. Build redaction map and safe rewrite
    redaction_map = build_redaction_map(query, all_blocked) if all_blocked else {}
    safe_rewrite = attempt_safe_rewrite(query, all_blocked) if action == "BLOCK" else query

    # 7b. If BLOCKED, retrieve local knowledge to answer the question
    local_knowledge: list[dict] = []
    local_answer: str | None = None
    if action == "BLOCK":
        knowledge_entries = resolved.get("knowledge", [])
        local_knowledge = knowledge_entries[:5]  # top 5 relevant entries
        if local_knowledge:
            # Build a local answer from knowledge entries
            local_answer = _build_local_answer(query, local_knowledge)

    # 8. Build GateDecision artifact
    gate_decision = {
        "artifact_type": "GateDecision",
        "intent": "PROTECT",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "matter_id": matter_id,
        "riu_id": riu_id,
        "boundary": "local_only" if action == "BLOCK" else "governed_external",
        "action": action,
        "reason": reason_str,
        "blocked_entities": all_blocked,
        "redaction_map": redaction_map,
        "safe_rewrite": safe_rewrite,
        "confidence": confidence,
        "posture": state.posture,
        "local_knowledge": [_summarize_kl(k) for k in local_knowledge],
        "local_answer": local_answer,
    }

    # 9. Store artifact
    body = f"# PROTECT Gate Decision\n\n"
    body += f"**Query**: {query}\n\n"
    body += f"**Action**: {action}\n\n"
    body += f"**Reason**: {reason_str}\n\n"
    if safe_rewrite and action == "BLOCK":
        body += f"**Safe rewrite available**: {safe_rewrite}\n\n"
    elif action == "ALLOW":
        body += f"**Cleared for external**: {query}\n\n"
    if local_answer:
        body += f"## Local Answer (on-device)\n\n{local_answer}\n\n"

    artifact_path = store_artifact("gate_decision", gate_decision, body)
    state.artifacts.append(artifact_path)

    # 10. Emit integrity signal
    elapsed_ms = round((time.time() - t0) * 1000, 1)
    emit_integrity_signal(
        intent="PROTECT",
        riu_id=riu_id,
        success=True,
        artifact_path=artifact_path,
        details=f"action={action} elapsed={elapsed_ms}ms",
    )

    # 11. Display
    if not show_json:
        print()
        print(f"  {DIM}{'━' * 60}{RESET}")
        print(f"  {BOLD}{WHITE}  ◆ palette protect{RESET}  {DIM}governance gate{RESET}")
        print(f"  {DIM}{'━' * 60}{RESET}")
        print()
        print(f"  {DIM}Query:{RESET}  {BOLD}{query}{RESET}")
        print()
        if riu_id:
            kl_count = len(resolved.get("knowledge", []))
            print(f"  {CYAN}[RESOLVE]{RESET} {riu_id} ({riu_name}) — {confidence:.0f}% confidence")
            print(f"  {CYAN}[RETRIEVE]{RESET} Local knowledge: {kl_count} entries")
            pis = pis_summary(riu_id, kl_count, classification)
            print(f"  {CYAN}[PIS]{RESET}     {format_pis_line(pis)}")
        print()
        print(f"  {'━' * 4} GOVERNANCE BOUNDARY {'━' * 35}")
        print()
        if action == "BLOCK":
            print(f"  {RED}{BOLD}⚠️  BLOCKED{RESET}   {reason_str}")
            if all_blocked:
                print(f"  {DIM}  Entities: {', '.join(all_blocked[:5])}{RESET}")
            print()
            print(f"  {RED}→ LOCAL ONLY{RESET}   Zero data left this machine.")
            print(f"  {DIM}  Model: Ollama (on-device){RESET}")
            if local_knowledge:
                print()
                print(f"  {'─' * 50}")
                print(f"  {CYAN}[RESULT]{RESET} {GREEN}[LOCAL]{RESET} Confidence: {confidence:.0f}%")
                print()
                for kl in local_knowledge[:3]:
                    kl_id = kl.get("lib_id", kl.get("id", ""))
                    kl_q = kl.get("question", kl.get("title", ""))
                    kl_a = kl.get("answer_excerpt", kl.get("answer", kl.get("content", "")))
                    if kl_id and kl_q:
                        print(f"  {BOLD}[{kl_id}]{RESET} {kl_q}")
                        if kl_a:
                            snippet = kl_a[:150].rstrip() + ("..." if len(kl_a) > 150 else "")
                            print(f"  {DIM}  {snippet}{RESET}")
                        print()
                print(f"  {'─' * 50}")
            if safe_rewrite:
                print()
                print(f"  {YELLOW}[SAFE REWRITE]{RESET} Available for RESEARCH transition:")
                print(f"  {DIM}  {safe_rewrite}{RESET}")
        else:
            print(f"  {GREEN}{BOLD}✓  ALLOWED{RESET}   {reason_str}")
            print()
            print(f"  {GREEN}→ GOVERNED EXTERNAL{RESET}   Query safe for sanitized external research.")
            print(f"  {DIM}  Next: palette research {f'--matter {matter_id} ' if matter_id else ''}\"{query}\"{RESET}")
        print()
        print(f"  {DIM}[STORED] {artifact_path}{RESET}")
        if riu_id:
            print(f"  {DIM}  Compounding: this decision improves future queries in {riu_id}{RESET}")
        print(f"  {DIM}[TIME]   {elapsed_ms}ms{RESET}")
        print()
    else:
        print(json.dumps(gate_decision, indent=2))

    return gate_decision, state


# ── CLI ─────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        prog="palette protect",
        description="Governance gate — classify query safety before external routing.",
    )
    parser.add_argument("query", help="The query to evaluate")
    parser.add_argument("--matter", "-m", help="Matter ID for artifact linkage")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    args = parser.parse_args()

    run_protect(args.query, matter_id=args.matter, show_json=args.json)


if __name__ == "__main__":
    main()
