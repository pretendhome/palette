#!/usr/bin/env python3
"""palette reflect — Turn experience into reusable memory.

Usage:
  palette reflect "What did we learn from today's BDB sprint?"
  palette reflect --matter sarah-llc-001 "What patterns emerged?"
  palette reflect --json "What should become a KL entry?"

Produces: ImprovementProposal artifact (lesson + patterns + proposed_action).
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
    palette_checkpoint,
    print_unvalidated_warning,
    resolve_query,
    store_artifact,
    GAP_LOG,
    ARTIFACTS_DIR,
)


# ── Gather Session State ────────────────────────────────────────────────


def gather_session_artifacts(matter_id: str | None) -> list[dict]:
    """Gather all artifacts from this session/matter for reflection."""
    artifacts = []
    for type_dir in ARTIFACTS_DIR.iterdir():
        if not type_dir.is_dir():
            continue
        for f in sorted(type_dir.glob("*.md"), reverse=True)[:30]:
            try:
                text = f.read_text()
                if not text.startswith("---"):
                    continue
                end = text.index("---", 3)
                import yaml
                fm = yaml.safe_load(text[3:end])
                # Filter by matter if specified, otherwise take today's
                if matter_id:
                    if fm.get("matter_id") != matter_id:
                        continue
                else:
                    ts = fm.get("timestamp", "")
                    if isinstance(ts, str) and ts[:10] != datetime.now(timezone.utc).strftime("%Y-%m-%d"):
                        continue
                artifacts.append({
                    "path": str(f),
                    "type": fm.get("artifact_type", ""),
                    "intent": fm.get("intent", ""),
                    "timestamp": fm.get("timestamp", ""),
                    "action": fm.get("action", ""),
                    "confidence": fm.get("confidence", 0),
                    "status": fm.get("status", ""),
                    "riu_id": fm.get("riu_id", ""),
                })
            except Exception:
                pass
    return artifacts


def gather_gap_signals(limit: int = 20) -> list[dict]:
    """Read recent gap signals."""
    signals = []
    if not GAP_LOG.exists():
        return signals
    lines = GAP_LOG.read_text().strip().split("\n")
    for line in lines[-limit:]:
        try:
            signals.append(json.loads(line))
        except Exception:
            pass
    return signals


# ── Pattern Detection ───────────────────────────────────────────────────


def detect_patterns(artifacts: list[dict], signals: list[dict]) -> list[str]:
    """Identify patterns across artifacts and signals."""
    patterns = []

    # Pattern: repeated RIU with low confidence
    riu_confidences: dict[str, list[float]] = {}
    for a in artifacts:
        riu = a.get("riu_id", "")
        conf = a.get("confidence", 0)
        if riu:
            riu_confidences.setdefault(riu, []).append(conf)

    for riu, confs in riu_confidences.items():
        if len(confs) >= 2 and sum(confs) / len(confs) < 50:
            patterns.append(f"Low confidence pattern: {riu} averaged {sum(confs)/len(confs):.0f}% across {len(confs)} queries — knowledge gap likely")

    # Pattern: PROTECT blocks dominating
    block_count = sum(1 for a in artifacts if a.get("action") == "BLOCK")
    total = len(artifacts)
    if total > 3 and block_count / total > 0.6:
        patterns.append(f"High block rate: {block_count}/{total} queries blocked — user may need more public research framing guidance")

    # Pattern: UNVALIDATED_FALLBACK signals
    fallback_count = sum(1 for a in artifacts if a.get("status") == "UNVALIDATED_FALLBACK")
    if fallback_count > 0:
        patterns.append(f"Unvalidated fallbacks: {fallback_count} queries fell back to unvalidated — knowledge gaps need filling")

    # Pattern: gap signals clustering
    intent_failures = {}
    for s in signals:
        if s.get("type") == "intent_execution" and not s.get("success"):
            intent = s.get("intent", "unknown")
            intent_failures[intent] = intent_failures.get(intent, 0) + 1
    for intent, count in intent_failures.items():
        if count >= 2:
            patterns.append(f"Repeated failures in {intent}: {count} failures — investigate root cause")

    if not patterns:
        patterns.append("No concerning patterns detected — system operating within expected parameters")

    return patterns


# ── Proposal Generation ─────────────────────────────────────────────────


def generate_proposals(patterns: list[str], artifacts: list[dict], query: str) -> list[dict]:
    """Generate improvement proposals from patterns."""
    proposals = []

    for pattern in patterns:
        if "knowledge gap" in pattern.lower() or "low confidence" in pattern.lower():
            # Extract RIU from pattern
            import re
            riu_match = re.search(r"RIU-\d+", pattern)
            riu = riu_match.group(0) if riu_match else "unknown"
            proposals.append({
                "action": f"Add knowledge entries for {riu}",
                "target_file": f"wiki/proposed/KL-PROP-{riu.lower()}-coverage.yaml",
                "priority": "high",
                "pattern": pattern,
            })
        elif "block rate" in pattern.lower():
            proposals.append({
                "action": "Create safe query rewriting guide for this domain",
                "target_file": "wiki/proposed/KL-PROP-safe-query-patterns.yaml",
                "priority": "medium",
                "pattern": pattern,
            })
        elif "fallback" in pattern.lower():
            proposals.append({
                "action": "Fill knowledge gaps that caused fallbacks",
                "target_file": "wiki/proposed/KL-PROP-fallback-gaps.yaml",
                "priority": "high",
                "pattern": pattern,
            })
        elif "failures" in pattern.lower():
            proposals.append({
                "action": "Investigate and fix repeated intent failures",
                "target_file": "wiki/proposed/KL-PROP-intent-reliability.yaml",
                "priority": "critical",
                "pattern": pattern,
            })

    return proposals


# ── Main REFLECT Logic ──────────────────────────────────────────────────


def run_reflect(
    query: str,
    matter_id: str | None = None,
    show_json: bool = False,
) -> tuple[dict, IntentState]:
    """Execute REFLECT intent. Returns (ImprovementProposal dict, final IntentState)."""

    t0 = time.time()

    # 1. Resolve (light — only if query looks like a domain question)
    riu_id = None
    riu_name = ""
    if not query.lower().startswith(("what did", "what patterns", "what should", "what have", "what worked")):
        resolved = resolve_query(query)
        riu_id = resolved.get("riu_id")
        riu_name = resolved.get("riu_name", "")

    # 2. Build state
    state = IntentState(
        intent="REFLECT",
        query=query,
        riu=riu_id,
        riu_name=riu_name,
        boundary="local_only",
        matter_id=matter_id,
    )

    # 2b. Checkpoint (REFLECT is always local, but check anyway)
    checked = palette_checkpoint(state)
    if checked.intent != "REFLECT" and not show_json:
        print(f"  {YELLOW}[CHECKPOINT]{RESET} Transition suggested: → {checked.intent}")

    # 3. Gather session artifacts
    artifacts = gather_session_artifacts(matter_id)

    # 4. Gather gap signals
    signals = gather_gap_signals()

    # 5. Detect patterns
    patterns = detect_patterns(artifacts, signals)

    # 6. Generate proposals
    proposals = generate_proposals(patterns, artifacts, query)

    # 7. Build summary
    summary = {
        "total_artifacts": len(artifacts),
        "by_intent": {},
        "by_status": {},
    }
    for a in artifacts:
        intent = a.get("intent", "unknown")
        summary["by_intent"][intent] = summary["by_intent"].get(intent, 0) + 1
        status = a.get("status", "unknown")
        summary["by_status"][status] = summary["by_status"].get(status, 0) + 1

    # 8. Build ImprovementProposal artifact
    improvement_proposal = {
        "artifact_type": "ImprovementProposal",
        "intent": "REFLECT",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "matter_id": matter_id,
        "query": query,
        "session_summary": summary,
        "patterns": patterns,
        "proposed_actions": proposals,
        "status": "PROPOSED",
    }

    # 9. Store artifact
    body = "# Improvement Proposal\n\n"
    body += f"**Reflection**: {query}\n\n"
    body += f"## Session Summary\n\n"
    body += f"- Total artifacts reviewed: {len(artifacts)}\n"
    for intent, count in summary["by_intent"].items():
        body += f"- {intent}: {count}\n"
    body += f"\n## Patterns Detected\n\n"
    for p in patterns:
        body += f"- {p}\n"
    body += f"\n## Proposed Actions\n\n"
    for prop in proposals:
        body += f"- **[{prop['priority']}]** {prop['action']}\n"
        body += f"  Target: `{prop['target_file']}`\n"
    body += f"\n---\n*Status: PROPOSED — requires GOVERN to promote to source of truth*\n"

    artifact_path = store_artifact("improvement_proposal", improvement_proposal, body)
    state.artifacts.append(artifact_path)

    # 10. Emit integrity signal
    elapsed_ms = round((time.time() - t0) * 1000, 1)
    emit_integrity_signal(
        intent="REFLECT",
        riu_id=riu_id,
        success=True,
        artifact_path=artifact_path,
        details=f"patterns={len(patterns)} proposals={len(proposals)} elapsed={elapsed_ms}ms",
    )

    # 11. Display
    if not show_json:
        print()
        print(f"  {DIM}{'━' * 60}{RESET}")
        print(f"  {BOLD}{WHITE}  ◆ palette reflect{RESET}  {DIM}turning experience into memory{RESET}")
        print(f"  {DIM}{'━' * 60}{RESET}")
        print()
        print(f"  {DIM}Reflection:{RESET}  {BOLD}{query}{RESET}")
        print()
        print(f"  {CYAN}[GATHER]{RESET} Reviewed {len(artifacts)} artifacts, {len(signals)} gap signals")
        if matter_id:
            print(f"  {DIM}  Matter: {matter_id}{RESET}")
        print()

        # Session summary
        print(f"  {'─' * 50}")
        print(f"  {CYAN}[SESSION]{RESET}")
        for intent, count in summary["by_intent"].items():
            print(f"  {DIM}  {intent}: {count} artifacts{RESET}")
        print()

        # Patterns
        print(f"  {'─' * 50}")
        print(f"  {CYAN}[PATTERNS]{RESET} {len(patterns)} detected")
        print()
        for p in patterns:
            print(f"  {YELLOW}•{RESET} {p}")
        print()

        # Proposals
        if proposals:
            print(f"  {'─' * 50}")
            print(f"  {CYAN}[PROPOSALS]{RESET} {len(proposals)} improvement(s)")
            print()
            for prop in proposals:
                color = RED if prop["priority"] == "critical" else YELLOW if prop["priority"] == "high" else DIM
                print(f"  {color}[{prop['priority'].upper()}]{RESET} {prop['action']}")
                print(f"  {DIM}  → {prop['target_file']}{RESET}")
                print()

        print(f"  {'─' * 50}")
        print()
        print(f"  {DIM}[STORED] {artifact_path}{RESET}")
        print(f"  {DIM}  Status: PROPOSED — requires GOVERN to promote{RESET}")
        print(f"  {DIM}[TIME]   {elapsed_ms}ms{RESET}")
        print()
    else:
        print(json.dumps(improvement_proposal, indent=2, default=str))

    return improvement_proposal, state


# ── CLI ─────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        prog="palette reflect",
        description="Turn experience into reusable memory.",
    )
    parser.add_argument("query", help="What to reflect on")
    parser.add_argument("--matter", "-m", help="Matter ID to scope reflection")
    parser.add_argument("--json", "-j", action="store_true", help="JSON output")
    args = parser.parse_args()

    run_reflect(args.query, matter_id=args.matter, show_json=args.json)


if __name__ == "__main__":
    main()
