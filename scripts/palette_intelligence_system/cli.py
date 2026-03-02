"""CLI entry point for PIS traversal.

Usage:
  python3 -m scripts.palette_intelligence_system.cli --riu RIU-082
  python3 -m scripts.palette_intelligence_system.cli --lib LIB-042
  python3 -m scripts.palette_intelligence_system.cli --query "add guardrails to my LLM app"
  python3 -m scripts.palette_intelligence_system.cli --riu RIU-082 --json
  python3 -m scripts.palette_intelligence_system.cli --fixtures
  python3 -m scripts.palette_intelligence_system.cli --health
  echo '{"from":"corythosaurus","riu_ids":["LIB-042"]}' | python3 -m scripts.palette_intelligence_system.cli
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict

from .fixtures import run_all as run_fixtures
from .health import get_all_health
from .loader import PISData, load_all
from .traverse import TraversalResult, traverse


# ── Keyword resolver (no LLM) ──────────────────────────────────────

def _tokenize(text: str) -> set[str]:
    """Split text into lowercase tokens, splitting on hyphens and non-alphanum."""
    words = re.findall(r"[a-zA-Z0-9]+", text)
    return {w.lower() for w in words if len(w) > 2}


def _prefix_match_count(query_tokens: set[str], target_tokens: set[str]) -> float:
    """Count matches allowing prefix overlap (min 4 chars).

    "eval" matches "evaluation", "guardrail" matches "guardrails".
    Exact matches score 1.0, prefix matches score 0.75.
    """
    total = 0.0
    for qt in query_tokens:
        if qt in target_tokens:
            total += 1.0
            continue
        if len(qt) >= 4:
            for tt in target_tokens:
                if len(tt) >= 4 and (tt.startswith(qt) or qt.startswith(tt)):
                    total += 0.75
                    break
    return total


def keyword_resolve(data: PISData, query: str) -> tuple[str | None, float, list[tuple[str, float]]]:
    """Resolve a natural language query to a LIB-XXX by keyword overlap.

    Uses prefix matching so "eval" matches "evaluation", "guardrail" matches "guardrails".
    Returns (best_lib_id | None, confidence 0–100, top_3_candidates).
    """
    tokens = _tokenize(query)
    if not tokens:
        return None, 0.0, []

    scores: list[tuple[str, float]] = []
    for lib_id, entry in data.knowledge.items():
        q_text = entry.get("question", "")
        tags = entry.get("tags", [])
        tag_tokens: set[str] = set()
        for t in tags:
            tag_tokens |= _tokenize(t)
        target_tokens = _tokenize(q_text) | tag_tokens
        if not target_tokens:
            continue
        match_score = _prefix_match_count(tokens, target_tokens)
        if match_score > 0:
            score = match_score / max(len(tokens), 3) * 100
            scores.append((lib_id, score))

    scores.sort(key=lambda x: -x[1])
    top_3 = scores[:3]
    if top_3 and top_3[0][1] >= 40:
        return top_3[0][0], top_3[0][1], top_3
    return None, (top_3[0][1] if top_3 else 0.0), top_3


# ── Human-readable output ──────────────────────────────────────────

def _format_human(r: TraversalResult) -> str:
    lines: list[str] = []
    title = f"{r.query_riu} ({r.query_riu_name})"
    lines.append(f"\n{'═' * 60}")
    lines.append(f" PIS Traversal: {title}")
    lines.append(f"{'═' * 60}")

    if r.resolved_from:
        lines.append(f"  Resolved from: {r.resolved_from}")

    lines.append(f"\n  Classification: {r.classification or '(none)'}" + (
        f" ({r.classification_rationale[:80]}...)" if len(r.classification_rationale) > 80
        else f" ({r.classification_rationale})" if r.classification_rationale else ""
    ))
    if r.completeness:
        lines.append(f"  Completeness: {r.completeness.total}/100 ({r.completeness.label})")
    lines.append(f"  Health: {r.health_status}")

    # Recommendation
    lines.append(f"\n{'─' * 40} Recommendation {'─' * 3}")
    if r.recommendation:
        rec = r.recommendation
        lines.append(f"  {rec.service_name}")
        lines.append(f"  Tier: {rec.quality_tier} | Cost: {rec.cost_model} ({rec.cost_estimate[:60]})")
        lines.append(f"  Status: {rec.integration_status} | Recipe: {'YES' if rec.recipe_available else 'NO'}"
                      + (f" ({rec.recipe_path})" if rec.recipe_path else ""))
        if rec.best_for:
            lines.append(f"  Best for: {', '.join(rec.best_for[:3])}")
        if rec.why_primary:
            lines.append(f"  Why: {rec.why_primary[:120]}")
    else:
        lines.append("  (none — internal_only or no routing)")

    # Alternatives
    if r.alternatives:
        lines.append(f"\n{'─' * 40} Alternatives {'─' * 5}")
        for i, alt in enumerate(r.alternatives, 1):
            recipe_tag = "recipe" if alt.recipe_available else "no recipe"
            lines.append(f"  {i}. {alt.service_name} — {alt.quality_tier}, "
                         f"{alt.integration_status}, {recipe_tag}")
            if alt.why_not:
                lines.append(f"     Why not primary: {alt.why_not}")

    # Signals
    lines.append(f"\n{'─' * 40} Signal Validation {'─' * 1}")
    if r.signal_validation:
        for sig in r.signal_validation:
            names = ", ".join(r["name"] for r in sig.recommenders[:3])
            lines.append(f"  {sig.tool_name} (tier {sig.signal_tier}): {names}")
            lines.append(f"    Action: {sig.palette_action}")
    else:
        lines.append("  No direct people-library signals for this RIU")

    # Knowledge
    lines.append(f"\n{'─' * 40} Knowledge Support {'─' * 1}")
    if r.knowledge_support:
        for k in r.knowledge_support[:5]:
            eval_tag = " (has evaluation signal)" if k.has_eval_signal else ""
            lines.append(f"  {k.lib_id}: \"{k.question}\"{eval_tag}")
    else:
        lines.append("  No knowledge-library entries for this RIU")

    # Gaps
    lines.append(f"\n{'─' * 40} Gaps {'─' * 14}")
    for gap in r.gaps:
        lines.append(f"  - {gap}")
    if not r.gaps:
        lines.append("  (none)")

    lines.append("")
    return "\n".join(lines)


# ── JSON output ─────────────────────────────────────────────────────

def _to_json(r: TraversalResult) -> str:
    d = asdict(r)
    return json.dumps(d, indent=2, default=str)


# ── Health report ───────────────────────────────────────────────────

def _format_health() -> str:
    entries = get_all_health()
    if not entries:
        return "No health data yet. Run some traversals first."
    lines = [f"\n{'═' * 60}", " PIS Health Report", f"{'═' * 60}\n"]
    for riu_id in sorted(entries.keys()):
        e = entries[riu_id]
        status = e.get("health_status", "unknown")
        comp = e.get("completeness", "?")
        marker = "OK" if status == "ok" else ("DEGRADED" if status == "degraded" else "FAILING")
        lines.append(f"  {riu_id:12s}  {marker:10s}  completeness={comp}")
        if e.get("diagnostic_needed"):
            missing = e.get("missing_layers", [])
            lines.append(f"{'':14s}  → missing: {', '.join(missing)}")
    lines.append("")
    return "\n".join(lines)


# ── HandoffPacket (stdin) ───────────────────────────────────────────

def _try_handoff_packet() -> dict | None:
    """Read a HandoffPacket from stdin if available."""
    if sys.stdin.isatty():
        return None
    try:
        raw = sys.stdin.read().strip()
        if not raw:
            return None
        return json.loads(raw)
    except (json.JSONDecodeError, OSError):
        return None


# ── Main ────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="PIS Traversal CLI")
    parser.add_argument("--riu", help="RIU ID to traverse (e.g. RIU-082)")
    parser.add_argument("--lib", help="Knowledge library ID (e.g. LIB-042)")
    parser.add_argument("--query", help="Natural language query (keyword match, no LLM)")
    parser.add_argument("--json", action="store_true", dest="json_output", help="JSON output")
    parser.add_argument("--fixtures", action="store_true", help="Run all fixture tests")
    parser.add_argument("--health", action="store_true", help="Show health report")
    args = parser.parse_args()

    # Check for HandoffPacket on stdin
    packet = _try_handoff_packet()

    if args.fixtures:
        data = load_all()
        print(f"\n{'═' * 60}")
        print(" PIS Fixture Tests")
        print(f"{'═' * 60}\n")
        passed = run_fixtures(data)
        print()
        sys.exit(0 if passed else 1)

    if args.health:
        print(_format_health())
        return

    # Determine what to traverse
    riu_id = args.riu
    lib_id = args.lib
    query = args.query

    if packet:
        # HandoffPacket from Cory or another agent
        riu_ids = packet.get("riu_ids", [])
        payload = packet.get("payload", {})
        if riu_ids:
            # riu_ids may contain LIB-XXX or RIU-XXX
            target = riu_ids[0]
            if target.startswith("LIB-"):
                lib_id = target
            else:
                riu_id = target
        elif payload.get("riu_id"):
            target = payload["riu_id"]
            if target.startswith("LIB-"):
                lib_id = target
            else:
                riu_id = target

    data = load_all()

    if query and not riu_id and not lib_id:
        matched_lib, confidence, top_3 = keyword_resolve(data, query)
        if matched_lib:
            print(f"  Keyword match: {matched_lib} (confidence: {confidence:.0f}%)")
            lib_id = matched_lib
        else:
            print(f"  No confident match (best confidence: {confidence:.0f}%)")
            print("  Use Cory for intent resolution. Top candidates:")
            for cand_id, cand_score in top_3:
                entry = data.knowledge.get(cand_id, {})
                q = entry.get("question", "")[:80]
                print(f"    {cand_id} ({cand_score:.0f}%): {q}")
            sys.exit(1)

    if not riu_id and not lib_id:
        parser.print_help()
        sys.exit(1)

    result = traverse(data, riu_id=riu_id, lib_id=lib_id)

    if args.json_output:
        print(_to_json(result))
    else:
        print(_format_human(result))


if __name__ == "__main__":
    main()
