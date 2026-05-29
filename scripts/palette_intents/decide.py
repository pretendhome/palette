#!/usr/bin/env python3
"""palette decide — Turn ambiguity into judgment with rationale.

Usage:
  palette decide "Should Sarah settle or litigate?"
  palette decide --matter sarah-llc-001 "Given the fiduciary evidence, what's our best path?"
  palette decide --json "Should we use local-only models for this workflow?"

Produces: DecisionRecord artifact (recommendation + evidence + counterargument + reversibility).
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
    find_related_artifacts,
    format_pis_line,
    palette_checkpoint,
    pis_summary,
    print_unvalidated_warning,
    record_recipe_failure,
    resolve_query,
    store_artifact,
)


# ── Model Callers ───────────────────────────────────────────────────────


def call_ollama(prompt: str, system: str = "", model: str = "qwen2.5:7b") -> str | None:
    """Call local Ollama. Zero external connection."""
    from urllib import request

    payload = json.dumps({
        "model": model,
        "prompt": f"{system}\n\n{prompt}" if system else prompt,
        "stream": False,
    }).encode()
    req = request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read()).get("response", "")
    except Exception:
        return None


# ── Prior Artifact Retrieval ────────────────────────────────────────────


def find_matter_evidence(matter_id: str | None) -> list[dict]:
    """Find all prior artifacts for this matter — the compounding moment."""
    if not matter_id:
        return []

    artifacts_dir = REPO_ROOT / ".palette" / "artifacts"
    evidence = []
    for type_dir in artifacts_dir.iterdir():
        if not type_dir.is_dir():
            continue
        for artifact_file in sorted(type_dir.glob("*.md"), reverse=True)[:20]:
            try:
                text = artifact_file.read_text()
                if f"matter_id: {matter_id}" in text or f"matter_id: '{matter_id}'" in text:
                    if text.startswith("---"):
                        end = text.index("---", 3)
                        import yaml

                        fm = yaml.safe_load(text[3:end])
                        evidence.append({
                            "path": str(artifact_file),
                            "type": fm.get("artifact_type", "unknown"),
                            "intent": fm.get("intent", ""),
                            "timestamp": fm.get("timestamp", ""),
                            "action": fm.get("action", ""),
                            "boundary": fm.get("boundary", ""),
                            "confidence": fm.get("confidence", 0),
                            "local_canon": fm.get("local_canon", []),
                            "recommendation": fm.get("recommendation", ""),
                        })
            except Exception:
                pass
    return evidence


def build_evidence_context(evidence: list[dict]) -> str:
    """Build a context string from prior artifacts for the decision model."""
    if not evidence:
        return "No prior evidence available."

    parts = []
    for e in evidence:
        if e["type"] == "GateDecision":
            parts.append(f"[PROTECT] Action: {e['action']} | Boundary: {e['boundary']}")
        elif e["type"] == "EvidenceBrief":
            canon = e.get("local_canon", [])
            for lc in canon[:3]:
                parts.append(f"[RESEARCH] {lc.get('question', '')}: {lc.get('content', '')[:200]}")
        elif e["type"] == "DecisionRecord":
            parts.append(f"[PRIOR DECISION] {e.get('recommendation', '')[:200]}")
    return "\n".join(parts) if parts else "No prior evidence available."


# ── ONE-WAY DOOR Detection ──────────────────────────────────────────────

ONE_WAY_INDICATORS = [
    "settle",
    "settlement",
    "fire",
    "terminate",
    "deploy to production",
    "sign the contract",
    "commit to",
    "irreversible",
    "delete",
    "drop the case",
    "file the motion",
    "publish",
    "announce",
    "merge",
    "acquire",
]


def detect_one_way_door(query: str, recommendation: str) -> bool:
    """Detect if this decision is a ONE-WAY DOOR (irreversible)."""
    combined = (query + " " + recommendation).lower()
    return any(ind in combined for ind in ONE_WAY_INDICATORS)


# ── Main DECIDE Logic ───────────────────────────────────────────────────


def run_decide(
    query: str,
    matter_id: str | None = None,
    show_json: bool = False,
) -> tuple[dict, IntentState]:
    """Execute DECIDE intent. Returns (DecisionRecord dict, final IntentState)."""

    t0 = time.time()

    # 1. Resolve RIU
    resolved = resolve_query(query)
    riu_id = resolved.get("riu_id")
    riu_name = resolved.get("riu_name", "")
    confidence = resolved.get("confidence", 0)
    classification = resolved.get("classification", "internal_only")
    knowledge_entries = resolved.get("knowledge", [])

    # 2. Build state
    state = IntentState(
        intent="DECIDE",
        query=query,
        riu=riu_id,
        riu_name=riu_name,
        boundary="local_only",  # DECIDE defaults to local (strategy is privileged)
        confidence=confidence,
        matter_id=matter_id,
    )

    # 3. Integrity card
    card = build_integrity_card_fast(riu_id or "unknown", classification, len(knowledge_entries))
    state.integrity_card = asdict(card)
    state.posture = card.posture

    # 4. Retrieve prior evidence (THE COMPOUNDING MOMENT)
    prior_evidence = find_matter_evidence(matter_id)
    if not prior_evidence and riu_id:
        # RIU-based connection: find related artifacts even without matter_id
        riu_related = find_related_artifacts(riu_id)
        if riu_related:
            prior_evidence = riu_related
    evidence_context = build_evidence_context(prior_evidence)

    # 4b. If no prior evidence and matter was specified, degrade to UNVALIDATED
    no_evidence_warning = False
    if matter_id and len(prior_evidence) == 0:
        no_evidence_warning = True

    # 5. Local knowledge
    local_knowledge = []
    for kl in knowledge_entries[:5]:
        local_knowledge.append({
            "id": kl.get("lib_id", ""),
            "question": kl.get("question", ""),
            "content": kl.get("answer_excerpt", ""),
        })

    # 6. Generate recommendation (local model — privileged strategy stays on device)
    recommendation_prompt = f"""You are a senior legal strategist. Based on the evidence below, provide a clear recommendation.

QUESTION: {query}

PRIOR EVIDENCE:
{evidence_context}

LOCAL KNOWLEDGE:
{json.dumps(local_knowledge, indent=2)[:2000]}

Provide:
1. A clear recommendation (1-2 sentences)
2. The key evidence supporting it (2-3 points)
3. What would change your mind (1 specific trigger)

Be direct. No hedging."""

    if not show_json:
        print()
        print(f"  {DIM}{'━' * 60}{RESET}")
        print(f"  {BOLD}{WHITE}  ◆ palette decide{RESET}  {DIM}judgment under ambiguity{RESET}")
        print(f"  {DIM}{'━' * 60}{RESET}")
        print()
        print(f"  {DIM}Query:{RESET}  {BOLD}{query}{RESET}")
        print()
        if riu_id:
            print(f"  {CYAN}[RESOLVE]{RESET} {riu_id} ({riu_name}) — {confidence:.0f}% confidence")
            print(f"  {CYAN}[RETRIEVE]{RESET} Local knowledge: {len(local_knowledge)} entries")
            pis = pis_summary(riu_id, len(local_knowledge), classification)
            print(f"  {CYAN}[PIS]{RESET}     {format_pis_line(pis)}")
        if prior_evidence:
            print(f"  {CYAN}[CONNECT]{RESET} Connected to {len(prior_evidence)} prior artifact(s):")
            for p in prior_evidence[:3]:
                print(f"  {DIM}  {str(p['timestamp'])[:10]} [{p['intent']}] {p['type']}{RESET}")
        elif no_evidence_warning:
            print(f"  {YELLOW}[CONNECT]{RESET} No prior evidence for matter '{matter_id}'")
            print(f"  {YELLOW}  ⚠ Decision will be UNVALIDATED — consider running RESEARCH first{RESET}")
        print()
        print(f"  {DIM}[REASONING]{RESET} Local model generating recommendation...")

    recommendation = call_ollama(recommendation_prompt, system="You are a decisive legal strategist. Be direct and specific.")

    if not recommendation:
        record_recipe_failure("ollama")
        if not show_json:
            print_unvalidated_warning("Local model unavailable")
        recommendation = "Unable to generate recommendation — local model unavailable."

    # 7. Mandatory adversarial critique (MUST be >50 words)
    critique_prompt = f"""You are an adversarial critic. Your job is to find the strongest counterargument to this recommendation.

ORIGINAL QUESTION: {query}
RECOMMENDATION: {recommendation}

Write the STRONGEST possible counterargument. You must:
- Identify the weakest assumption in the recommendation
- Explain what could go wrong
- Name a specific scenario where this recommendation fails

Your counterargument MUST be at least 60 words. Be specific, not generic."""

    if not show_json:
        print(f"  {DIM}[CRITIQUE]{RESET} Adversarial model generating counterargument...")

    counterargument = call_ollama(critique_prompt, system="You are a ruthless critic. Find the fatal flaw.")

    # Validate: counterargument must be >50 words
    if not counterargument or len(counterargument.split()) < 50:
        # Retry with stronger prompt
        retry_prompt = f"""The previous counterargument was too weak or too short. Try again.

RECOMMENDATION: {recommendation}

Write AT LEAST 80 words of specific, concrete counterargument. Name real risks. Be adversarial."""

        counterargument_retry = call_ollama(retry_prompt, system="You must write at least 80 words of critique.")
        if counterargument_retry and len(counterargument_retry.split()) > 50:
            counterargument = counterargument_retry
        elif not counterargument:
            record_recipe_failure("ollama")
            counterargument = "Counterargument generation failed. Human review required before proceeding."

    # 8. Extract change_my_mind trigger (use smaller model — it's just one sentence)
    trigger_prompt = f"""Based on this decision, name ONE specific, measurable event or discovery that would reverse the recommendation.

QUESTION: {query}
RECOMMENDATION: {recommendation[:300]}

Format: "If [specific event/discovery], then reconsider."
One sentence only."""

    change_trigger = call_ollama(trigger_prompt, system="One sentence. Specific. Measurable.", model="qwen2.5:3b")
    if not change_trigger:
        change_trigger = "If new evidence contradicts the core assumption, reconsider."

    # 9. ONE-WAY DOOR check
    is_one_way = detect_one_way_door(query, recommendation)
    reversibility = "ONE_WAY" if is_one_way else "TWO_WAY"
    checkpoint_required = is_one_way

    # 10. Build DecisionRecord artifact
    decision_record = {
        "artifact_type": "DecisionRecord",
        "intent": "DECIDE",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "matter_id": matter_id,
        "riu_id": riu_id,
        "boundary": "local_only",
        "recommendation": recommendation.strip(),
        "evidence_sources": [p["path"] for p in prior_evidence],
        "strongest_counterargument": counterargument.strip(),
        "change_my_mind_trigger": change_trigger.strip(),
        "reversibility": reversibility,
        "checkpoint_required": checkpoint_required,
        "confidence": confidence,
        "status": "UNVALIDATED_FALLBACK" if (no_evidence_warning or not recommendation or not counterargument) else "VALIDATED",
    }

    # 11. Store artifact
    body = "# Decision Record\n\n"
    body += f"**Query**: {query}\n\n"
    body += f"## Recommendation\n\n{recommendation.strip()}\n\n"
    body += f"## Strongest Counterargument\n\n{counterargument.strip()}\n\n"
    body += f"## Change My Mind\n\n{change_trigger.strip()}\n\n"
    body += f"## Reversibility\n\n**{reversibility}**"
    if checkpoint_required:
        body += " — 🚨 Human checkpoint required before proceeding"
    body += "\n\n"
    if prior_evidence:
        body += "## Evidence Sources\n\n"
        for p in prior_evidence:
            body += f"- [{p['type']}] {p['intent']} ({str(p['timestamp'])[:10]})\n"

    artifact_path = store_artifact("decision_record", decision_record, body)
    state.artifacts.append(artifact_path)

    # 12. Emit integrity signal
    elapsed_ms = round((time.time() - t0) * 1000, 1)
    emit_integrity_signal(
        intent="DECIDE",
        riu_id=riu_id,
        success=True,
        artifact_path=artifact_path,
        details=f"reversibility={reversibility} checkpoint={checkpoint_required} elapsed={elapsed_ms}ms",
    )

    # 13. Display
    if not show_json:
        print()
        print(f"  {'━' * 4} GOVERNANCE BOUNDARY {'━' * 35}")
        print()
        if checkpoint_required:
            print(f"  {RED}{BOLD}🚨 ONE-WAY DOOR{RESET} — Human confirmation required")
        else:
            print(f"  {GREEN}🔄 TWO-WAY DOOR{RESET} — Reversible, proceed with confidence")
        print(f"  {DIM}  Boundary: local_only | Model: Ollama (on-device){RESET}")
        print()
        print(f"  {'─' * 50}")
        print(f"  {CYAN}[RECOMMENDATION]{RESET}")
        print()
        for line in recommendation.strip().split("\n")[:10]:
            if line.strip():
                print(f"  {line.strip()}")
        print()
        print(f"  {'─' * 50}")
        print(f"  {YELLOW}[COUNTERARGUMENT]{RESET} ({len(counterargument.split())} words)")
        print()
        for line in counterargument.strip().split("\n")[:8]:
            if line.strip():
                print(f"  {DIM}{line.strip()}{RESET}")
        print()
        print(f"  {'─' * 50}")
        print(f"  {CYAN}[CHANGE MY MIND]{RESET}")
        print(f"  {DIM}{change_trigger.strip()}{RESET}")
        print()
        print(f"  {'─' * 50}")
        print()
        print(f"  {DIM}[STORED] {artifact_path}{RESET}")
        if matter_id and riu_id:
            print(f"  {DIM}  Compounding: decision linked to {len(prior_evidence)} prior artifacts in {riu_id}{RESET}")
        print(f"  {DIM}[TIME]   {elapsed_ms}ms{RESET}")
        print()
    else:
        print(json.dumps(decision_record, indent=2, default=str))

    return decision_record, state


# ── CLI ─────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        prog="palette decide",
        description="Turn ambiguity into judgment with rationale.",
    )
    parser.add_argument("query", help="The decision question")
    parser.add_argument("--matter", "-m", help="Matter ID for artifact linkage")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    args = parser.parse_args()

    run_decide(args.query, matter_id=args.matter, show_json=args.json)


if __name__ == "__main__":
    main()
