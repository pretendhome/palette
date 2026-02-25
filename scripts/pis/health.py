"""Circuit breaker / health tracking for PIS traversals."""

from __future__ import annotations

import json
import os
import sys
import uuid
from datetime import datetime, timezone


_HEALTH_FILE = os.path.join(os.path.dirname(__file__), "traversal_health.jsonl")
_MAX_HISTORY = 9  # look at last 9 + current = 10


def _load_history(riu_id: str) -> list[dict]:
    """Load the last _MAX_HISTORY entries for a given RIU."""
    if not os.path.exists(_HEALTH_FILE):
        return []
    entries: list[dict] = []
    with open(_HEALTH_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if entry.get("riu_id") == riu_id:
                entries.append(entry)
    return entries[-_MAX_HISTORY:]


def record_and_evaluate(
    riu_id: str,
    completeness: int,
    gaps: list[str],
    missing_layers: list[str] | None = None,
) -> str:
    """Record a traversal result and return health status: ok | degraded | failing."""
    passed = completeness >= 60
    history = _load_history(riu_id)
    prior_failures = sum(1 for e in history if not e.get("passed", True))

    if not passed and prior_failures >= 1:
        health_status = "failing"
    elif not passed:
        health_status = "degraded"
    else:
        health_status = "ok"

    entry = {
        "riu_id": riu_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "completeness": completeness,
        "passed": passed,
        "gaps": gaps,
        "run_id": uuid.uuid4().hex[:12],
        "health_status": health_status,
    }
    if health_status == "failing":
        entry["diagnostic_needed"] = True
        entry["missing_layers"] = missing_layers or []

    with open(_HEALTH_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    if health_status == "failing":
        _print_diagnostic(riu_id, prior_failures + 1, missing_layers or [])

    return health_status


def _print_diagnostic(riu_id: str, failure_count: int, missing_layers: list[str]) -> None:
    print(f"\n[health] {riu_id} FAILING — {failure_count} failures in last 10 traversals", file=sys.stderr)
    if missing_layers:
        print(f"  Missing layers: {', '.join(missing_layers)}", file=sys.stderr)
    print(f"  Action: complete data entries for {riu_id}", file=sys.stderr)


def get_all_health() -> dict[str, dict]:
    """Return latest health status per RIU from the health file."""
    if not os.path.exists(_HEALTH_FILE):
        return {}
    per_riu: dict[str, dict] = {}
    with open(_HEALTH_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            riu = entry.get("riu_id", "")
            if riu:
                per_riu[riu] = entry
    return per_riu
