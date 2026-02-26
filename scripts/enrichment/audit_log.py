"""JSONL append-only audit log for enrichment operations."""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from typing import Any

from .config import ENRICHMENT_LOG_PATH


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_entry(
    *,
    action: str,
    person_id: str | None = None,
    source: str = "github",
    fields_changed: list[str] | None = None,
    previous_values: dict[str, Any] | None = None,
    new_values: dict[str, Any] | None = None,
    api_calls: int = 0,
    error: str | None = None,
    pipeline_run_id: str = "",
) -> None:
    """Append a single audit entry to the enrichment log."""
    entry = {
        "timestamp": _now(),
        "action": action,
        "person_id": person_id,
        "source": source,
        "fields_changed": fields_changed or [],
        "previous_values": previous_values or {},
        "new_values": new_values or {},
        "api_calls": api_calls,
        "error": error,
        "pipeline_run_id": pipeline_run_id,
    }
    try:
        with open(ENRICHMENT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except OSError as exc:
        print(f"[audit] write error: {exc}")


def read_log(person_id: str | None = None, limit: int = 50) -> list[dict]:
    """Read recent log entries, optionally filtered by person_id."""
    if not os.path.exists(ENRICHMENT_LOG_PATH):
        return []
    entries: list[dict] = []
    with open(ENRICHMENT_LOG_PATH, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            if person_id and entry.get("person_id") != person_id:
                continue
            entries.append(entry)
    return sorted(entries, key=lambda e: e.get("timestamp", ""), reverse=True)[:limit]
