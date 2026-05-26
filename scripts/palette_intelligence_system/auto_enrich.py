#!/usr/bin/env python3
"""auto_enrich.py — Gap-signal aggregator and KL entry proposer.

Reads gap signals from peers/gap_signals.ndjson.
Clusters gap signals by RIU over a rolling window.
Proposes new KL entries from accumulated search results.
Writes proposals to knowledge-library/proposals/ for human review.

This is Step 5 of the obligatory routing loop:
  CLASSIFY → RETRIEVE → SEARCH → INFER → STORE + IMPROVE → RETURN

The IMPROVE part reads accumulated gap signals and proposes taxonomy
and knowledge library updates. Human review is required for all
taxonomy changes (ONE-WAY DOOR). KL entry proposals at Tier 3 can
be auto-filed but require human review before promotion.

Usage:
    python3 scripts/palette_intelligence_system/auto_enrich.py
    python3 scripts/palette_intelligence_system/auto_enrich.py --days 14
    python3 scripts/palette_intelligence_system/auto_enrich.py --json
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GAP_LOG = REPO_ROOT / "peers" / "gap_signals.ndjson"
SESSION_LOG = REPO_ROOT / "peers" / "session_log.ndjson"
PROPOSALS_DIR = REPO_ROOT / "knowledge-library" / "proposals"


def read_gap_signals(days: int = 7) -> list[dict]:
    """Read gap signals from the persistent NDJSON log within rolling window."""
    signals = []
    if not GAP_LOG.exists():
        return signals
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    with open(GAP_LOG) as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                ts_str = entry.get("timestamp", "")
                if ts_str:
                    ts = datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
                    if ts > cutoff:
                        signals.append(entry)
            except (json.JSONDecodeError, KeyError, ValueError):
                pass
    return signals


def cluster_signals_by_riu(signals: list[dict]) -> dict[str, list]:
    """Group gap signals by RIU ID."""
    clusters: dict[str, list] = {}
    for signal in signals:
        riu_id = signal.get("riu_id") or "unclassified"
        clusters.setdefault(riu_id, []).append(signal)
    return clusters


def emit_gap_report(clusters: dict[str, list]) -> dict:
    """Build prioritized gap report from signal clusters."""
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_signals": sum(len(v) for v in clusters.values()),
        "total_rius_affected": len(clusters),
        "high_priority": [],   # 5+ signals — likely needs new KL entries
        "medium_priority": [], # 3-4 signals — worth investigating
        "low_priority": [],    # 1-2 signals — monitor
        "unclassified": [],    # no RIU match at all — may need new RIU nodes
    }
    for riu_id, signals in sorted(clusters.items(), key=lambda x: -len(x[1])):
        entry = {
            "riu_id": riu_id,
            "signal_count": len(signals),
            "signal_types": list(set(s.get("signal_type", "unknown") for s in signals)),
            "sample_queries": [s.get("query", "")[:100] for s in signals[:3]],
            "avg_confidence": round(
                sum(s.get("confidence", 0) for s in signals) / len(signals), 1
            ) if signals else 0,
        }
        if riu_id == "unclassified":
            report["unclassified"].append(entry)
        elif len(signals) >= 5:
            report["high_priority"].append(entry)
        elif len(signals) >= 3:
            report["medium_priority"].append(entry)
        else:
            report["low_priority"].append(entry)
    return report


def write_gap_report(report: dict) -> Path:
    """Write gap report to proposals directory for human review."""
    PROPOSALS_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_path = PROPOSALS_DIR / f"gap_report_{date_str}.json"
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    return out_path


def main():
    parser = argparse.ArgumentParser(
        description="Auto-enrich: aggregate gap signals, propose KL updates"
    )
    parser.add_argument("--days", type=int, default=7, help="Rolling window in days")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    args = parser.parse_args()

    signals = read_gap_signals(days=args.days)
    clusters = cluster_signals_by_riu(signals)
    report = emit_gap_report(clusters)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Gap Report — {report['generated_at']}")
        print(f"Total signals: {report['total_signals']} across {report['total_rius_affected']} RIUs")
        print()
        if report["high_priority"]:
            print("HIGH PRIORITY (5+ signals — likely needs new KL entries):")
            for e in report["high_priority"]:
                print(f"  {e['riu_id']}: {e['signal_count']} signals (avg conf: {e['avg_confidence']}%)")
                for q in e["sample_queries"]:
                    print(f"    - {q}")
            print()
        if report["medium_priority"]:
            print("MEDIUM PRIORITY (3-4 signals):")
            for e in report["medium_priority"]:
                print(f"  {e['riu_id']}: {e['signal_count']} signals (avg conf: {e['avg_confidence']}%)")
            print()
        if report["unclassified"]:
            print("UNCLASSIFIED (no RIU match — may need new taxonomy nodes):")
            for e in report["unclassified"]:
                print(f"  {e['signal_count']} signals with no RIU classification")
                for q in e["sample_queries"]:
                    print(f"    - {q}")
            print()
        print(f"Low priority: {len(report['low_priority'])} RIUs with 1-2 signals")

    out = write_gap_report(report)
    if not args.json:
        print(f"\nReport written to: {out}")


if __name__ == "__main__":
    main()
