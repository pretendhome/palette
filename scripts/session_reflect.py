#!/usr/bin/env python3
"""session_reflect.py — End-of-session learning extraction.

CQ-inspired pattern: review what happened, extract what's worth keeping,
propose learnings through the governance pipeline.

Usage:
  python3 scripts/session_reflect.py                    # reflect on current session log
  python3 scripts/session_reflect.py --dry-run           # show proposals without filing
  python3 scripts/session_reflect.py --log path/to/log   # reflect on specific log file

The session log is a NDJSON file (one JSON object per line) written by
palette_query.py's bus completion messages. This script reads the log,
identifies patterns, and files governed proposals for high-value learnings.

Governance integration:
  - Gap signals → Tier 1 gap proposal (lightweight, flags content needed)
  - Retrieval patterns → logged but NOT proposed (observation, not knowledge)
  - New concepts discovered → Tier 2 proposal if evidence supports it
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

PALETTE_ROOT = Path(__file__).resolve().parent.parent
SESSION_LOG = PALETTE_ROOT / "peers" / "session_log.ndjson"
PROPOSED_DIR = PALETTE_ROOT / "wiki" / "proposed"

BUS_URL = "http://127.0.0.1:7899"


# ── Bus helper (best-effort) ────────────────────────────────────────────

def bus_send(intent: str, content: str):
    """Best-effort bus notification."""
    try:
        import urllib.request
        import uuid
        msg = {
            "protocol_version": "1.0.0",
            "message_id": str(uuid.uuid4()),
            "thread_id": None,
            "in_reply_to": None,
            "from_agent": "palette.session-reflect",
            "to_agent": "group",
            "message_type": "informational",
            "intent": intent,
            "risk_level": "none",
            "requires_ack": False,
            "payload": {"content": content},
            "created_at": datetime.now(timezone.utc).isoformat(),
            "ttl_seconds": 3600,
        }
        req = urllib.request.Request(
            f"{BUS_URL}/send",
            data=json.dumps(msg).encode(),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass


# ── Session log reader ──────────────────────────────────────────────────

def read_session_log(log_path: Path) -> list[dict]:
    """Read NDJSON session log. Returns list of query records."""
    if not log_path.exists():
        return []
    entries = []
    with open(log_path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def append_to_session_log(record: dict, log_path: Path):
    """Append a query record to the session log."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a") as f:
        f.write(json.dumps(record) + "\n")


# ── Analysis ────────────────────────────────────────────────────────────

def analyze_session(entries: list[dict]) -> dict:
    """Analyze a session's query history for patterns."""
    if not entries:
        return {"total_queries": 0, "gaps": [], "successes": [], "patterns": {}}

    gaps = []
    successes = []
    riu_counter: Counter[str] = Counter()
    lib_counter: Counter[str] = Counter()
    agent_counter: Counter[str] = Counter()
    low_confidence = []

    for e in entries:
        riu = e.get("riu_id")
        if riu:
            riu_counter[riu] += 1

        lib = e.get("lib_id")
        if lib:
            lib_counter[lib] += 1

        agent = e.get("agent")
        if agent:
            agent_counter[agent] += 1

        confidence = e.get("confidence", 0)
        if confidence < 30:
            gaps.append({
                "query": e.get("query", "")[:100],
                "riu_id": riu,
                "confidence": confidence,
            })
        elif confidence >= 70:
            successes.append({
                "query": e.get("query", "")[:100],
                "lib_id": lib,
                "riu_id": riu,
                "confidence": confidence,
            })
        else:
            low_confidence.append({
                "query": e.get("query", "")[:100],
                "confidence": confidence,
                "riu_id": riu,
            })

    return {
        "total_queries": len(entries),
        "gaps": gaps,
        "successes": successes,
        "low_confidence": low_confidence,
        "patterns": {
            "top_rius": riu_counter.most_common(5),
            "top_libs": lib_counter.most_common(5),
            "agent_distribution": dict(agent_counter),
        },
    }


# ── Proposal generation ────────────────────────────────────────────────

def generate_gap_proposals(analysis: dict) -> list[dict]:
    """Generate Tier 1 gap proposals for content holes."""
    proposals = []
    seen_rius = set()

    for gap in analysis["gaps"]:
        riu = gap.get("riu_id")
        if not riu or riu in seen_rius:
            continue
        seen_rius.add(riu)

        proposals.append({
            "proposed_by": "palette.session-reflect",
            "tier": 1,
            "type": "new",
            "rationale": (
                f"Session reflection: query '{gap['query']}' matched {riu} at only "
                f"{gap['confidence']:.0f}% confidence. This RIU may need a dedicated "
                f"knowledge entry or the existing entries need better coverage."
            ),
            "source_of_insight": "session_reflection",
            "content": {
                "question": f"What knowledge is missing for {riu} that caused low-confidence retrieval?",
                "gap_query": gap["query"],
                "gap_confidence": gap["confidence"],
                "related_rius": [riu],
            },
            "contradiction_check": {
                "checked": True,
                "conflicts": "none — this is a gap signal, not a content claim",
            },
        })

    return proposals


# ── Report generation ───────────────────────────────────────────────────

def format_report(analysis: dict) -> str:
    """Format a human-readable session reflection report."""
    lines = []
    lines.append("## Session Reflection")
    lines.append(f"**Date**: {date.today().isoformat()}")
    lines.append(f"**Queries analyzed**: {analysis['total_queries']}")
    lines.append("")

    if analysis["gaps"]:
        lines.append(f"### Content Gaps ({len(analysis['gaps'])})")
        for g in analysis["gaps"]:
            lines.append(f"- **{g['riu_id']}** ({g['confidence']:.0f}%): {g['query']}")
        lines.append("")

    if analysis["successes"]:
        lines.append(f"### Strong Retrievals ({len(analysis['successes'])})")
        for s in analysis["successes"]:
            lines.append(f"- **{s['lib_id']}** ({s['confidence']:.0f}%): {s['query']}")
        lines.append("")

    if analysis["low_confidence"]:
        lines.append(f"### Moderate Confidence ({len(analysis['low_confidence'])})")
        for lc in analysis["low_confidence"]:
            lines.append(f"- **{lc['riu_id']}** ({lc['confidence']:.0f}%): {lc['query']}")
        lines.append("")

    patterns = analysis["patterns"]
    if patterns["top_rius"]:
        lines.append("### Most Queried RIUs")
        for riu, count in patterns["top_rius"]:
            lines.append(f"- {riu}: {count} queries")
        lines.append("")

    if patterns["agent_distribution"]:
        lines.append("### Agent Routing Distribution")
        for agent, count in patterns["agent_distribution"].items():
            lines.append(f"- {agent}: {count}")
        lines.append("")

    return "\n".join(lines)


# ── File proposals through governance ───────────────────────────────────

def file_gap_proposal(proposal: dict, dry_run: bool = False) -> bool:
    """File a gap proposal via file_proposal.py."""
    if dry_run:
        print(f"  [DRY RUN] Would file gap proposal for {proposal['content'].get('related_rius', [])}")
        return True

    # Write proposal YAML to temp file, invoke file_proposal.py
    import tempfile
    import subprocess

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        yaml.dump(proposal, f, default_flow_style=False)
        temp_path = f.name

    try:
        result = subprocess.run(
            [sys.executable, str(PALETTE_ROOT / "scripts" / "file_proposal.py"), temp_path],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode == 0:
            print(f"  Filed gap proposal for {proposal['content'].get('related_rius', [])}")
            return True
        else:
            print(f"  Failed to file proposal: {result.stderr[:200]}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"  Error filing proposal: {e}", file=sys.stderr)
        return False
    finally:
        Path(temp_path).unlink(missing_ok=True)


# ── Main ────────────────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(
        prog="session_reflect",
        description="End-of-session learning extraction. Reviews query history, "
                    "identifies patterns and gaps, proposes learnings through governance.",
    )
    parser.add_argument("--log", type=Path, default=SESSION_LOG,
                        help="Path to session log (NDJSON)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show proposals without filing")
    parser.add_argument("--json", action="store_true",
                        help="Output analysis as JSON")
    parser.add_argument("--clear", action="store_true",
                        help="Clear session log after reflection")
    args = parser.parse_args()

    entries = read_session_log(args.log)

    if not entries:
        print("No session log entries found.")
        print(f"Session log path: {args.log}")
        print("\nTo populate: run `palette query` commands, which log to the bus.")
        print("Or create entries manually in NDJSON format.")
        sys.exit(0)

    analysis = analyze_session(entries)

    if args.json:
        print(json.dumps(analysis, indent=2))
        return

    # Print report
    report = format_report(analysis)
    print(report)

    # Generate and file gap proposals
    proposals = generate_gap_proposals(analysis)
    if proposals:
        print(f"### Gap Proposals ({len(proposals)})")
        filed = 0
        for p in proposals:
            if file_gap_proposal(p, dry_run=args.dry_run):
                filed += 1
        print(f"\n{'Would file' if args.dry_run else 'Filed'} {filed}/{len(proposals)} proposals.")
    else:
        print("No gap proposals needed — retrieval quality looks good.")

    # Clear session log if requested
    if args.clear:
        args.log.unlink(missing_ok=True)
        print("Session log cleared.")

    # Send reflection summary to bus
    bus_send(
        intent=f"Session reflection: {analysis['total_queries']} queries, "
               f"{len(analysis['gaps'])} gaps, {len(analysis['successes'])} strong",
        content=json.dumps({
            "total_queries": analysis["total_queries"],
            "gaps": len(analysis["gaps"]),
            "successes": len(analysis["successes"]),
            "proposals_filed": len(proposals),
        }),
    )


if __name__ == "__main__":
    main()
