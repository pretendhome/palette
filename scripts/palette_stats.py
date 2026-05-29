#!/usr/bin/env python3
"""palette stats — visible compounding metrics."""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

PALETTE_DIR = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = PALETTE_DIR / ".palette" / "artifacts"
CRON_LOG = PALETTE_DIR / ".palette" / "cron_log.ndjson"
GAP_SIGNALS = PALETTE_DIR / "peers" / "gap_signals.ndjson"
TOTAL_RIUS = 131


def count_artifacts():
    """Count artifacts by type."""
    counts = {}
    total = 0
    for d in sorted(ARTIFACTS_DIR.iterdir()) if ARTIFACTS_DIR.exists() else []:
        if d.is_dir():
            n = sum(1 for _ in d.rglob("*.md"))
            if n:
                counts[d.name] = n
                total += n
    return total, counts


def count_rius():
    """Count unique RIU IDs across all artifacts."""
    rius = set()
    if not ARTIFACTS_DIR.exists():
        return 0
    for f in ARTIFACTS_DIR.rglob("*.md"):
        try:
            for line in f.open():
                if line.startswith("riu_id:"):
                    val = line.split(":", 1)[1].strip().strip("'\"")
                    if val and val != "null":
                        rius.add(val)
                    break
                if not line.startswith(("---", " ", "\n")) and ":" not in line:
                    break
        except (OSError, UnicodeDecodeError):
            pass
    return len(rius)


def count_pii_blocks():
    """Count gate decisions with action: BLOCK."""
    gate_dir = ARTIFACTS_DIR / "gate_decision"
    if not gate_dir.exists():
        return 0
    count = 0
    for f in gate_dir.glob("*.md"):
        try:
            for line in f.open():
                if line.startswith("action:") and "BLOCK" in line:
                    count += 1
                    break
                if not line.startswith(("---", " ", "\n")) and ":" not in line:
                    break
        except (OSError, UnicodeDecodeError):
            pass
    return count


def count_cron():
    """Count cron executions and governed percentage."""
    if not CRON_LOG.exists():
        return 0, 100
    total = 0
    governed = 0
    for line in CRON_LOG.open():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
            total += 1
            if entry.get("boundary") in ("governed_external", "local_only"):
                governed += 1
        except json.JSONDecodeError:
            pass
    pct = int((governed / total) * 100) if total else 100
    return total, pct


def count_gap_signals():
    """Count integrity signals from gap_signals.ndjson."""
    if not GAP_SIGNALS.exists():
        return 0
    return sum(1 for line in GAP_SIGNALS.open() if line.strip())


def first_artifact_date():
    """Earliest artifact file mtime."""
    if not ARTIFACTS_DIR.exists():
        return None
    earliest = None
    for f in ARTIFACTS_DIR.rglob("*.md"):
        try:
            mtime = f.stat().st_mtime
            if earliest is None or mtime < earliest:
                earliest = mtime
        except OSError:
            pass
    return datetime.fromtimestamp(earliest, tz=timezone.utc) if earliest else None


def run(as_json=False):
    total_artifacts, by_type = count_artifacts()
    rius = count_rius()
    pii_blocks = count_pii_blocks()
    cron_total, cron_pct = count_cron()
    signals = count_gap_signals()
    first = first_artifact_date()
    now = datetime.now(timezone.utc)
    age_days = (now - first).days if first else 0

    if as_json:
        json.dump({
            "artifacts_total": total_artifacts,
            "artifacts_by_type": by_type,
            "rius_activated": rius,
            "rius_total": TOTAL_RIUS,
            "pii_blocks": pii_blocks,
            "cron_executions": cron_total,
            "cron_governed_pct": cron_pct,
            "integrity_signals": signals,
            "first_artifact": first.isoformat() if first else None,
            "age_days": age_days,
        }, sys.stdout, indent=2)
        print()
        return

    print()
    print("  mission canvas — your judgment trail")
    print()
    print(f"  Artifacts stored:     {total_artifacts}")
    for name, count in by_type.items():
        print(f"    {name}:{' ' * max(1, 18 - len(name))}{count}")
    print(f"  RIUs activated:       {rius} / {TOTAL_RIUS} ({int(rius/TOTAL_RIUS*100)}%)")
    print(f"  Cron executions:      {cron_total} ({cron_pct}% governed)")
    print(f"  PII blocks:           {pii_blocks}")
    print(f"  Integrity signals:    {signals}")
    if first:
        print(f"  First artifact:       {first.strftime('%Y-%m-%d')}")
        print(f"  Compounding for:      {age_days} days")
    print()
    print("  Your judgment compounds here.")
    print()


if __name__ == "__main__":
    as_json = "--json" in sys.argv
    run(as_json=as_json)
