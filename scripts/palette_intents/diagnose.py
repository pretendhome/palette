#!/usr/bin/env python3
"""palette diagnose — Find the failure, repair it, remember the lesson.

Usage:
  palette diagnose "Why did the privileged query route externally?"
  palette fix "Why is the demo too slow?"
  palette diagnose --json "Why did the bus message not arrive?"

Produces: FailureLesson artifact (symptom + five_whys + root_cause + fix + lesson).
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
    emit_integrity_signal,
    print_unvalidated_warning,
    resolve_query,
    store_artifact,
)


# ── Model Caller ────────────────────────────────────────────────────────


def call_ollama(prompt: str, system: str = "", model: str = "qwen2.5:7b") -> str | None:
    """Call local Ollama."""
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


# ── Five Whys ───────────────────────────────────────────────────────────


def run_five_whys(symptom: str, context: str) -> list[str]:
    """Generate 5-whys analysis using local model."""
    prompt = f"""You are a root cause analyst. Perform a 5-Whys analysis on this failure.

SYMPTOM: {symptom}

CONTEXT: {context}

Rules:
- Each "why" must be more specific than the last
- Each answer must be a concrete, testable claim
- The 5th why should reach an architectural or systemic cause
- Format each as: "N. Why [question]? → [answer]"

Generate exactly 5 whys."""

    result = call_ollama(prompt, system="You are a precise root cause analyst. No fluff. Each why digs deeper.")
    if not result:
        return [
            "1. Why did this fail? → Unable to generate analysis (model unavailable)",
            "2. Why is the model unavailable? → Ollama may not be running",
            "3. Why might Ollama not be running? → Service not started after reboot",
            "4. Why wasn't it auto-started? → No systemd service configured",
            "5. Why no systemd service? → Development environment, not production",
        ]

    # Parse into list
    lines = [l.strip() for l in result.strip().split("\n") if l.strip()]
    whys = []
    for line in lines:
        if any(line.startswith(f"{i}") for i in range(1, 6)):
            whys.append(line)
    # Pad to exactly 5
    while len(whys) < 5:
        whys.append(f"{len(whys)+1}. [Analysis incomplete — human input needed]")
    return whys[:5]


# ── Fix Proposal ────────────────────────────────────────────────────────


def propose_fix(symptom: str, five_whys: list[str]) -> dict:
    """Propose a minimal fix based on root cause."""
    root_cause = five_whys[-1] if five_whys else "Unknown"

    prompt = f"""Based on this root cause analysis, propose the MINIMAL fix.

SYMPTOM: {symptom}
ROOT CAUSE (5th why): {root_cause}

Provide:
1. One-line description of the fix
2. Whether this is an architectural patch (changes system design) or a local patch (changes one file/config)
3. What test would verify the fix works

Be specific. Name files, functions, or configs where possible."""

    result = call_ollama(prompt, system="Minimal fix only. No scope creep.", model="qwen2.5:3b")

    return {
        "description": result.strip() if result else "Fix proposal requires human input",
        "type": "unknown",
        "verified": False,
    }


# ── Main DIAGNOSE Logic ─────────────────────────────────────────────────


def run_diagnose(
    query: str,
    matter_id: str | None = None,
    show_json: bool = False,
) -> tuple[dict, IntentState]:
    """Execute DIAGNOSE intent. Returns (FailureLesson dict, final IntentState)."""

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
        intent="DIAGNOSE",
        query=query,
        riu=riu_id,
        riu_name=riu_name,
        boundary="local_only",
        confidence=confidence,
        matter_id=matter_id,
    )

    # 3. Integrity card
    card = build_integrity_card_fast(riu_id or "unknown", classification, len(knowledge_entries))
    state.integrity_card = asdict(card)

    # 4. Build context from local knowledge
    context_parts = []
    for kl in knowledge_entries[:3]:
        context_parts.append(f"[{kl.get('lib_id', '')}] {kl.get('answer_excerpt', '')[:150]}")
    context = "\n".join(context_parts) if context_parts else "No local knowledge available for this failure domain."

    if not show_json:
        print()
        print(f"  {DIM}{'━' * 60}{RESET}")
        print(f"  {BOLD}{WHITE}  ◆ palette diagnose{RESET}  {DIM}failure isolation and repair{RESET}")
        print(f"  {DIM}{'━' * 60}{RESET}")
        print()
        print(f"  {DIM}Symptom:{RESET}  {BOLD}{query}{RESET}")
        print()
        if riu_id:
            print(f"  {CYAN}[RESOLVE]{RESET} {riu_id} ({riu_name}) — {confidence:.0f}% confidence")
        if confidence < 40:
            print(f"  {YELLOW}[LOW CONFIDENCE]{RESET} Classification uncertain — diagnosis may be unreliable")
        print(f"  {DIM}[REASONING]{RESET} Running 5-Whys analysis...")

    # 5. Run 5-Whys
    five_whys = run_five_whys(query, context)

    # 6. Determine if root cause is isolated
    root_cause_isolated = len(five_whys) == 5 and not any("incomplete" in w.lower() for w in five_whys)

    # If classification confidence was too low, mark as unreliable
    if confidence < 40:
        root_cause_isolated = False

    # 7. Propose fix
    if not show_json:
        print(f"  {DIM}[FIX]{RESET} Proposing minimal repair...")

    fix = propose_fix(query, five_whys)

    # 8. Build FailureLesson artifact
    failure_lesson = {
        "artifact_type": "FailureLesson",
        "intent": "DIAGNOSE",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "matter_id": matter_id,
        "riu_id": riu_id,
        "confidence": confidence,
        "symptom": query,
        "five_whys": five_whys,
        "root_cause_isolated": root_cause_isolated,
        "architectural_patch": fix["description"],
        "fix_verified": fix["verified"],
        "tests_added": [],
        "status": "OPEN",
    }

    # 9. Store artifact
    body = "# Failure Lesson\n\n"
    body += f"**Symptom**: {query}\n\n"
    body += "## Five Whys\n\n"
    for w in five_whys:
        body += f"{w}\n\n"
    body += f"## Root Cause Isolated: {'✅ Yes' if root_cause_isolated else '❌ No — needs human input'}\n\n"
    body += f"## Proposed Fix\n\n{fix['description']}\n\n"
    body += f"## Status: OPEN\n\n"
    body += "- [ ] Fix implemented\n- [ ] Tests added\n- [ ] Fix verified\n"

    artifact_path = store_artifact("failure_lesson", failure_lesson, body)
    state.artifacts.append(artifact_path)

    # 10. Emit integrity signal
    elapsed_ms = round((time.time() - t0) * 1000, 1)
    emit_integrity_signal(
        intent="DIAGNOSE",
        riu_id=riu_id,
        success=root_cause_isolated,
        artifact_path=artifact_path,
        details=f"root_cause_isolated={root_cause_isolated} elapsed={elapsed_ms}ms",
    )

    # 11. Display
    if not show_json:
        print()
        print(f"  {'━' * 4} DIAGNOSIS {'━' * 43}")
        print()
        print(f"  {CYAN}[5-WHYS]{RESET}")
        print()
        for i, w in enumerate(five_whys):
            color = RED if i == 4 else YELLOW if i >= 3 else DIM
            print(f"  {color}{w}{RESET}")
        print()
        print(f"  {'─' * 50}")
        if root_cause_isolated:
            print(f"  {GREEN}[ROOT CAUSE]{RESET} Isolated ✅")
        else:
            print(f"  {YELLOW}[ROOT CAUSE]{RESET} Not fully isolated — human input needed")
        print()
        print(f"  {'─' * 50}")
        print(f"  {CYAN}[FIX]{RESET}")
        print()
        for line in fix["description"].split("\n")[:6]:
            if line.strip():
                print(f"  {line.strip()}")
        print()
        print(f"  {'─' * 50}")
        print()
        print(f"  {DIM}[STORED] {artifact_path}{RESET}")
        print(f"  {DIM}  Status: OPEN — fix not yet verified{RESET}")
        print(f"  {DIM}[TIME]   {elapsed_ms}ms{RESET}")
        print()
    else:
        print(json.dumps(failure_lesson, indent=2, default=str))

    return failure_lesson, state


# ── CLI ─────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        prog="palette diagnose",
        description="Find the failure, repair it, remember the lesson.",
    )
    parser.add_argument("query", help="The failure symptom to diagnose")
    parser.add_argument("--matter", "-m", help="Matter ID for artifact linkage")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    args = parser.parse_args()

    run_diagnose(args.query, matter_id=args.matter, show_json=args.json)


if __name__ == "__main__":
    main()
