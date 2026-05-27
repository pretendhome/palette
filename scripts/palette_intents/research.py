#!/usr/bin/env python3
"""palette research — Governed external research with local grounding.

Usage:
  palette research "What are the key Delaware LLC fiduciary duty cases?"
  palette research --matter sarah-llc-001 "What fiduciary standards apply?"
  palette research --local-only "What do we know about oversight duties?"
  palette research --json "Delaware LLC Act fiduciary provisions"

Produces: EvidenceBrief artifact (local_canon + external_delta + synthesis).
"""

from __future__ import annotations

import argparse
import json
import os
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
    build_integrity_card_fast,
    bus_post,
    emit_integrity_signal,
    format_pis_line,
    palette_checkpoint,
    pis_summary,
    print_unvalidated_warning,
    record_recipe_failure,
    resolve_query,
    store_artifact,
)


# ── Perplexity Call ─────────────────────────────────────────────────────


def call_perplexity(query: str) -> dict | None:
    """Call Perplexity Sonar Pro. Returns {answer, sources} or None."""
    from urllib import request

    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        return None
    try:
        payload = json.dumps({
            "model": "sonar-pro",
            "messages": [
                {"role": "system", "content": "Answer with citations. Public legal sources only. Be concise and precise."},
                {"role": "user", "content": query},
            ],
        }).encode()
        req = request.Request(
            "https://api.perplexity.ai/chat/completions",
            data=payload,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        )
        with request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read())
            choices = body.get("choices", [])
            message = choices[0].get("message", {}) if choices else {}
            return {
                "answer": message.get("content", ""),
                "sources": body.get("citations", []),
            }
    except Exception:
        return None


# ── Sanitizer Gate (re-check before external call) ──────────────────────


def is_safe_for_external(query: str) -> tuple[bool, str]:
    """Re-verify query safety immediately before Perplexity call."""
    try:
        from bdb.gateway.sanitizer import QuerySanitizer

        sanitizer = QuerySanitizer()
        return sanitizer.is_safe_for_external(query)
    except Exception:
        # If sanitizer unavailable, block by default
        return False, "sanitizer unavailable — blocking external"


# ── Prior Artifacts Lookup ──────────────────────────────────────────────


def find_prior_artifacts(matter_id: str | None) -> list[dict]:
    """Find prior artifacts for this matter (compounding)."""
    if not matter_id:
        return []

    artifacts_dir = REPO_ROOT / ".palette" / "artifacts"
    priors = []
    for type_dir in artifacts_dir.iterdir():
        if not type_dir.is_dir():
            continue
        for artifact_file in sorted(type_dir.glob("*.md"), reverse=True)[:20]:
            try:
                text = artifact_file.read_text()
                if f"matter_id: {matter_id}" in text or f"matter_id: '{matter_id}'" in text:
                    # Parse frontmatter
                    if text.startswith("---"):
                        end = text.index("---", 3)
                        import yaml
                        fm = yaml.safe_load(text[3:end])
                        priors.append({
                            "path": str(artifact_file),
                            "type": fm.get("artifact_type", "unknown"),
                            "timestamp": fm.get("timestamp", ""),
                            "action": fm.get("action", ""),
                            "intent": fm.get("intent", ""),
                        })
            except Exception:
                pass
    return priors


# ── Main RESEARCH Logic ─────────────────────────────────────────────────


def run_research(
    query: str,
    matter_id: str | None = None,
    local_only: bool = False,
    show_json: bool = False,
) -> tuple[dict, IntentState]:
    """Execute RESEARCH intent. Returns (EvidenceBrief dict, final IntentState)."""

    t0 = time.time()

    # 1. Resolve RIU
    resolved = resolve_query(query)
    riu_id = resolved.get("riu_id")
    riu_name = resolved.get("riu_name", "")
    confidence = resolved.get("confidence", 0)
    classification = resolved.get("classification", "both")
    knowledge_entries = resolved.get("knowledge", [])

    # 2. Build state
    state = IntentState(
        intent="RESEARCH",
        query=query,
        riu=riu_id,
        riu_name=riu_name,
        boundary="governed_external",
        confidence=confidence,
        matter_id=matter_id,
    )

    # 3. Integrity card (fast path)
    card = build_integrity_card_fast(riu_id or "unknown", classification, len(knowledge_entries))
    state.integrity_card = asdict(card)
    state.posture = card.posture

    # 4. Checkpoint: should we even be in RESEARCH?
    checked = palette_checkpoint(state)
    if checked.intent != "RESEARCH":
        # Transition detected — for now, warn and continue
        if not show_json:
            print(f"  {YELLOW}[CHECKPOINT]{RESET} Transition suggested: → {checked.intent}")

    # 5. Local canon (always retrieved)
    local_canon = []
    for kl in knowledge_entries[:5]:
        local_canon.append({
            "id": kl.get("lib_id", kl.get("id", "")),
            "content": kl.get("answer_excerpt", kl.get("answer", "")),
            "question": kl.get("question", ""),
            "evidence_tier": kl.get("evidence_tier", None),
            "score": kl.get("score", 0),
        })

    # 6. Prior artifacts (compounding)
    prior_artifacts = find_prior_artifacts(matter_id)

    # 7. External research (if allowed)
    external_delta = []
    external_answer = ""
    external_sources: list[str] = []
    contradictions: str | None = None
    used_external = False

    if not local_only and classification != "internal_only" and card.posture != "blocked_by_boundary":
        # Re-verify safety immediately before external call
        safe, reason = is_safe_for_external(query)
        if safe:
            result = call_perplexity(query)
            if result:
                used_external = True
                external_answer = result.get("answer", "")
                external_sources = result.get("sources", [])
                external_delta.append({
                    "source": "perplexity",
                    "content": external_answer,
                    "sources": external_sources,
                })
                # Check for contradictions with local canon
                contradictions = _detect_contradictions(local_canon, external_answer)
            else:
                record_recipe_failure("perplexity")
        else:
            if not show_json:
                print(f"  {RED}[BLOCKED]{RESET} External blocked at re-check: {reason}")

    # 8. Determine confidence and status
    if used_external and local_canon:
        final_confidence = min(95, confidence + 20)
        status = "VALIDATED"
    elif local_canon:
        final_confidence = confidence
        status = "LOCAL_ONLY"
    else:
        final_confidence = max(10, confidence)
        status = "UNVALIDATED_FALLBACK"

    # 9. Build EvidenceBrief artifact
    evidence_brief = {
        "artifact_type": "EvidenceBrief",
        "intent": "RESEARCH",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "matter_id": matter_id,
        "riu_id": riu_id,
        "boundary": "governed_external" if used_external else "local_only",
        "local_canon": local_canon,
        "external_delta": external_delta,
        "contradictions": contradictions,
        "confidence": final_confidence,
        "status": status,
        "prior_artifacts": [p["path"] for p in prior_artifacts],
        "sources": external_sources,
    }

    # 10. Store artifact
    body = "# Evidence Brief\n\n"
    body += f"**Query**: {query}\n\n"
    if local_canon:
        body += "## Local Canon\n\n"
        for lc in local_canon:
            body += f"- **[{lc['id']}]** {lc['question']}\n  {lc['content']}\n\n"
    if external_answer:
        body += "## External Evidence (Perplexity)\n\n"
        body += f"{external_answer}\n\n"
        if external_sources:
            body += "**Sources**:\n"
            for src in external_sources[:5]:
                body += f"- {src}\n"
            body += "\n"
    if contradictions:
        body += f"## Contradictions\n\n{contradictions}\n\n"
    if prior_artifacts:
        body += "## Connected Prior Artifacts\n\n"
        for p in prior_artifacts:
            body += f"- [{p['type']}] {p['intent']} ({p['timestamp']})\n"

    artifact_path = store_artifact("evidence_brief", evidence_brief, body)
    state.artifacts.append(artifact_path)

    # 11. Emit integrity signal
    elapsed_ms = round((time.time() - t0) * 1000, 1)
    emit_integrity_signal(
        intent="RESEARCH",
        riu_id=riu_id,
        success=True,
        artifact_path=artifact_path,
        details=f"external={used_external} confidence={final_confidence} elapsed={elapsed_ms}ms",
    )

    # 12. Display
    if not show_json:
        print()
        print(f"  {DIM}{'━' * 60}{RESET}")
        print(f"  {BOLD}{WHITE}  ◆ palette research{RESET}  {DIM}governed evidence gathering{RESET}")
        print(f"  {DIM}{'━' * 60}{RESET}")
        print()
        print(f"  {DIM}Query:{RESET}  {BOLD}{query}{RESET}")
        print()
        if riu_id:
            print(f"  {CYAN}[RESOLVE]{RESET} {riu_id} ({riu_name}) — {confidence:.0f}% confidence")
            print(f"  {CYAN}[RETRIEVE]{RESET} Local knowledge: {len(local_canon)} entries")
            pis = pis_summary(riu_id, len(local_canon), classification)
            print(f"  {CYAN}[PIS]{RESET}     {format_pis_line(pis)}")
        if prior_artifacts:
            print(f"  {CYAN}[CONNECT]{RESET} Connected to {len(prior_artifacts)} prior artifact(s):")
            for p in prior_artifacts[:3]:
                print(f"  {DIM}  {p['timestamp'][:10]} [{p['intent']}] {p['type']}{RESET}")
        print()

        if used_external:
            print(f"  {DIM}[SANITIZE]{RESET} Query safe for external: ✓")
            print()
            print(f"  {'━' * 4} GOVERNANCE BOUNDARY {'━' * 35}")
            print()
            print(f"  {GREEN}[EXTERNAL]{RESET} Routed to Perplexity sonar-pro")
            print(f"  {DIM}  Model: Perplexity (governed external research){RESET}")
            print()
            print(f"  {'─' * 50}")
            print(f"  {CYAN}[RESULT]{RESET} {GREEN}[EXTERNAL:Perplexity]{RESET} + {GREEN}[LOCAL]{RESET} support")
            print()
            # Show external answer (truncated for display)
            for line in external_answer.split("\n")[:12]:
                if line.strip():
                    print(f"  {line.strip()}")
            if len(external_answer.split("\n")) > 12:
                print(f"  {DIM}  ... (truncated){RESET}")
            if external_sources:
                print()
                print(f"  {DIM}Sources:{RESET}")
                for src in external_sources[:3]:
                    print(f"  {DIM}  - {src}{RESET}")
            print()
            print(f"  {'─' * 50}")
        else:
            print(f"  {'━' * 4} GOVERNANCE BOUNDARY {'━' * 35}")
            print()
            if local_only:
                print(f"  {YELLOW}[LOCAL ONLY]{RESET} External research disabled (--local-only)")
            elif classification == "internal_only":
                print(f"  {RED}[BLOCKED]{RESET} RIU classified as internal_only")
            else:
                print(f"  {YELLOW}[LOCAL ONLY]{RESET} External unavailable or blocked")
            print()
            print(f"  {'─' * 50}")
            print(f"  {CYAN}[RESULT]{RESET} {GREEN}[LOCAL]{RESET} Confidence: {final_confidence:.0f}%")
            print()
            for lc in local_canon[:3]:
                print(f"  {BOLD}[{lc['id']}]{RESET} {lc['question']}")
                if lc['content']:
                    snippet = lc['content'][:150].rstrip() + ("..." if len(lc['content']) > 150 else "")
                    print(f"  {DIM}  {snippet}{RESET}")
                print()
            print(f"  {'─' * 50}")

        if contradictions:
            print(f"\n  {YELLOW}[CONTRADICTION]{RESET} {contradictions}")

        if status == "UNVALIDATED_FALLBACK":
            print_unvalidated_warning("No local knowledge and external unavailable")

        print()
        print(f"  {DIM}[STORED] {artifact_path}{RESET}")
        if matter_id and riu_id:
            print(f"  {DIM}  Compounding: evidence linked to matter {matter_id} in {riu_id}{RESET}")
        print(f"  {DIM}[CONFIDENCE] {final_confidence:.0f}%{RESET}")
        if final_confidence >= 60:
            print(f"  {DIM}  → Evidence sufficient. Consider: palette decide {f'--matter {matter_id} ' if matter_id else ''}\"<decision question>\"{RESET}")
        print(f"  {DIM}[TIME]   {elapsed_ms}ms{RESET}")
        print()
    else:
        print(json.dumps(evidence_brief, indent=2, default=str))

    return evidence_brief, state


# ── Contradiction Detection ─────────────────────────────────────────────


def _detect_contradictions(local_canon: list[dict], external: str) -> str | None:
    """Contradiction detection: flag if external explicitly contradicts local.

    Only flags strong contradiction signals (overruled, superseded, incorrect).
    Weak signals (however, but) are too common in legal writing.
    """
    if not local_canon or not external:
        return None

    external_lower = external.lower()
    # Only strong contradiction signals — "however" is normal legal prose
    strong_signals = ["overruled", "superseded", "no longer good law", "incorrectly", "was wrong", "rejected by"]

    for signal in strong_signals:
        if signal in external_lower:
            for lc in local_canon:
                lc_keywords = [w for w in lc.get("content", "").lower().split() if len(w) > 6][:5]
                for kw in lc_keywords:
                    idx = external_lower.find(signal)
                    kw_idx = external_lower.find(kw)
                    if idx >= 0 and kw_idx >= 0 and abs(idx - kw_idx) < 150:
                        return f"External source may contradict local [{lc['id']}] — '{signal}' near '{kw}'. Review needed."
    return None


# ── CLI ─────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        prog="palette research",
        description="Governed external research with local grounding.",
    )
    parser.add_argument("query", help="The research question")
    parser.add_argument("--matter", "-m", help="Matter ID for artifact linkage")
    parser.add_argument("--local-only", "-l", action="store_true", help="Skip external, local knowledge only")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    args = parser.parse_args()

    run_research(args.query, matter_id=args.matter, local_only=args.local_only, show_json=args.json)


if __name__ == "__main__":
    main()
