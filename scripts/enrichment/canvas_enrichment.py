#!/usr/bin/env python3
"""Simplified Canvas -> Palette enrichment loop.

This collapses the earlier multi-stage plan into one operator-friendly CLI:
  1. Read pending MissionCanvas feedback from workspace palette_feedback.yaml files
  2. Validate promotable KL candidates
  3. Auto-promote workspace-scoped candidates into the workspace KL when possible
  4. Queue review items and intelligence signals for human follow-up
  5. Mark handled feedback entries as ingested
  6. Append an audit record

Usage:
  python3 palette/scripts/enrichment/canvas_enrichment.py
  python3 palette/scripts/enrichment/canvas_enrichment.py --workspace oil-investor
  python3 palette/scripts/enrichment/canvas_enrichment.py --workspace oil-investor --dry-run
"""
from __future__ import annotations

import argparse
import json
import uuid
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


SCRIPT_DIR = Path(__file__).resolve().parent
PALETTE_ROOT = SCRIPT_DIR.parents[1]
FDE_ROOT = PALETTE_ROOT.parent
MISSIONCANVAS_ROOT = FDE_ROOT / "missioncanvas-site"
WORKSPACES_DIR = MISSIONCANVAS_ROOT / "workspaces"
AUDIT_LOG_PATH = SCRIPT_DIR / "enrichment_log.jsonl"
REVIEW_QUEUE_PATH = PALETTE_ROOT / "enrichment" / "canvas_candidates" / "pending_review.yaml"

PROMOTABLE_TYPES = {"kl_candidate"}
SIGNAL_TYPES = {"concept_exposure", "decision_record", "mastery_signal"}
DIFFICULTY_BY_PRIORITY = {"critical": "high", "moderate": "medium", "low": "low"}


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def utc_date() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def make_run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:6]


def load_yaml(path: Path, default: Any) -> Any:
    if not path.exists():
        return deepcopy(default)
    raw = path.read_text(encoding="utf-8")
    if not raw.strip():
        return deepcopy(default)
    loaded = yaml.safe_load(raw)
    return loaded if loaded is not None else deepcopy(default)


def save_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(data, sort_keys=False, indent=2, width=120, allow_unicode=False),
        encoding="utf-8",
    )


def append_audit(entry: dict[str, Any]) -> None:
    with AUDIT_LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def normalize_workspace_ids(values: list[str] | None) -> list[str]:
    if not values:
        return []
    ids: list[str] = []
    for value in values:
        for item in value.split(","):
            item = item.strip()
            if item:
                ids.append(item)
    return ids


def discover_workspaces(selected: list[str]) -> list[Path]:
    if selected:
        return [WORKSPACES_DIR / workspace_id for workspace_id in selected]
    return sorted(path.parent for path in WORKSPACES_DIR.glob("*/palette_feedback.yaml"))


def workspace_feedback_path(workspace_dir: Path) -> Path:
    return workspace_dir / "palette_feedback.yaml"


def load_feedback(workspace_dir: Path) -> dict[str, Any]:
    default = {
        "metadata": {
            "workspace_id": workspace_dir.name,
            "last_updated": None,
            "entry_count": 0,
        },
        "feedback": [],
    }
    data = load_yaml(workspace_feedback_path(workspace_dir), default)
    if not isinstance(data, dict):
        return deepcopy(default)
    data.setdefault("metadata", {})
    data.setdefault("feedback", [])
    return data


def save_feedback(workspace_dir: Path, data: dict[str, Any]) -> None:
    data.setdefault("metadata", {})
    data.setdefault("feedback", [])
    data["metadata"]["workspace_id"] = workspace_dir.name
    data["metadata"]["entry_count"] = len(data["feedback"])
    data["metadata"]["last_updated"] = utc_date()
    save_yaml(workspace_feedback_path(workspace_dir), data)


def mark_feedback_ingested(feedback_data: dict[str, Any], entry_ids: list[str]) -> int:
    wanted = set(entry_ids)
    count = 0
    for entry in feedback_data.get("feedback", []):
        if entry.get("id") in wanted:
            entry["status"] = "ingested"
            entry["ingested_at"] = utc_date()
            count += 1
    return count


def find_workspace_knowledge_library(workspace_dir: Path) -> Path | None:
    matches = sorted(workspace_dir.glob("*knowledge_library*.yaml"))
    return matches[0] if matches else None


def load_workspace_library(path: Path | None) -> tuple[dict[str, Any], str]:
    if path is None or not path.exists():
        return (
            {
                "metadata": {
                    "version": "1.0",
                    "generated_date": utc_date(),
                    "domain": "workspace",
                    "total_entries": 0,
                    "source_document": "canvas_enrichment.py",
                },
                "library_questions": [],
            },
            "library_questions",
        )

    data = load_yaml(path, {})
    if not isinstance(data, dict):
        data = {}
    if "library_questions" in data:
        key = "library_questions"
    elif "entries" in data:
        key = "entries"
    else:
        key = "library_questions"
        data[key] = []
    data.setdefault("metadata", {})
    data.setdefault(key, [])
    return data, key


def save_workspace_library(path: Path, data: dict[str, Any], key: str) -> None:
    data.setdefault("metadata", {})
    data.setdefault(key, [])
    data["metadata"]["generated_date"] = utc_date()
    data["metadata"]["total_entries"] = len(data[key])
    save_yaml(path, data)


def load_review_queue() -> dict[str, Any]:
    default = {
        "metadata": {
            "generated_at": utc_timestamp(),
            "last_updated": utc_timestamp(),
            "entry_count": 0,
        },
        "kl_candidates": [],
        "intelligence_signals": [],
    }
    data = load_yaml(REVIEW_QUEUE_PATH, default)
    if not isinstance(data, dict):
        return deepcopy(default)
    data.setdefault("metadata", {})
    data.setdefault("kl_candidates", [])
    data.setdefault("intelligence_signals", [])
    return data


def save_review_queue(data: dict[str, Any]) -> None:
    data["metadata"]["last_updated"] = utc_timestamp()
    data["metadata"]["entry_count"] = len(data.get("kl_candidates", [])) + len(data.get("intelligence_signals", []))
    save_yaml(REVIEW_QUEUE_PATH, data)


def domain_to_industries(domain: str | None) -> list[str]:
    if not domain:
        return []
    label = domain.replace("-", " ").strip()
    return [label.title()] if label else []


def validate_kl_candidate(entry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not entry.get("id"):
        errors.append("missing id")
    if not entry.get("question"):
        errors.append("missing question")
    if not entry.get("answer"):
        errors.append("missing answer")
    return errors


def normalize_kl_candidate(entry: dict[str, Any], workspace_id: str) -> dict[str, Any]:
    domain = entry.get("domain") or "workspace"
    tags = [tag for tag in entry.get("tags", []) if tag]
    if "workspace-resolution" not in tags:
        tags.append("workspace-resolution")
    if workspace_id not in tags:
        tags.append(workspace_id)
    return {
        "id": entry["id"],
        "question": entry["question"],
        "answer": entry["answer"],
        "problem_type": "Workspace_Resolution",
        "related_rius": [],
        "difficulty": DIFFICULTY_BY_PRIORITY.get(entry.get("priority", "moderate"), "medium"),
        "industries": domain_to_industries(domain),
        "tags": tags,
        "sources": [
            {
                "title": f"MissionCanvas workspace resolution ({workspace_id})",
                "url": f"internal://missioncanvas/{workspace_id}/palette_feedback/{entry['id']}",
            }
        ],
        "journey_stage": "foundation",
    }


def queue_contains(items: list[dict[str, Any]], entry_id: str) -> bool:
    return any(item.get("id") == entry_id for item in items)


def promote_to_workspace_library(
    library_data: dict[str, Any],
    key: str,
    normalized: dict[str, Any],
) -> str:
    entries = library_data.get(key, [])
    existing_ids = {item.get("id") for item in entries}
    existing_questions = {item.get("question", "").strip().lower() for item in entries}
    if normalized["id"] in existing_ids or normalized["question"].strip().lower() in existing_questions:
        return "duplicate"
    entries.append(normalized)
    library_data[key] = entries
    return "promoted"


def queue_review_candidate(queue: dict[str, Any], workspace_id: str, normalized: dict[str, Any], original: dict[str, Any]) -> str:
    if queue_contains(queue["kl_candidates"], normalized["id"]):
        return "duplicate"
    queue["kl_candidates"].append(
        {
            "id": normalized["id"],
            "workspace_id": workspace_id,
            "review_status": "pending",
            "queued_at": utc_timestamp(),
            "normalized_entry": normalized,
            "original_feedback": original,
        }
    )
    return "queued"


def queue_signal(queue: dict[str, Any], workspace_id: str, entry: dict[str, Any]) -> str:
    if queue_contains(queue["intelligence_signals"], entry["id"]):
        return "duplicate"
    queue["intelligence_signals"].append(
        {
            "id": entry["id"],
            "type": entry.get("type", "unknown"),
            "workspace_id": workspace_id,
            "queued_at": utc_timestamp(),
            "payload": entry,
        }
    )
    return "queued"


def process_workspace(
    workspace_dir: Path,
    review_queue: dict[str, Any],
    dry_run: bool,
) -> dict[str, Any]:
    workspace_id = workspace_dir.name
    feedback_data = load_feedback(workspace_dir)
    library_path = find_workspace_knowledge_library(workspace_dir)
    library_data, library_key = load_workspace_library(library_path)

    pending_entries = [entry for entry in feedback_data.get("feedback", []) if entry.get("status") != "ingested"]
    results = {
        "workspace_id": workspace_id,
        "pending": len(pending_entries),
        "promoted": 0,
        "queued_candidates": 0,
        "queued_signals": 0,
        "duplicates": 0,
        "ingested": 0,
        "errors": [],
    }

    handled_ids: list[str] = []
    mutated_library = False
    mutated_queue = False

    for entry in pending_entries:
        entry_id = entry.get("id", "<unknown>")
        entry_type = entry.get("type")

        if entry_type in PROMOTABLE_TYPES:
            errors = validate_kl_candidate(entry)
            if errors:
                results["errors"].append(f"{entry_id}: {'; '.join(errors)}")
                continue

            normalized = normalize_kl_candidate(entry, workspace_id)
            if library_path is not None and entry.get("domain") not in {None, "", "general"}:
                outcome = promote_to_workspace_library(library_data, library_key, normalized)
                if outcome == "promoted":
                    results["promoted"] += 1
                    handled_ids.append(entry_id)
                    mutated_library = True
                else:
                    results["duplicates"] += 1
                    handled_ids.append(entry_id)
                continue

            outcome = queue_review_candidate(review_queue, workspace_id, normalized, entry)
            if outcome == "queued":
                results["queued_candidates"] += 1
                handled_ids.append(entry_id)
                mutated_queue = True
            else:
                results["duplicates"] += 1
                handled_ids.append(entry_id)
            continue

        if entry_type in SIGNAL_TYPES:
            outcome = queue_signal(review_queue, workspace_id, entry)
            if outcome == "queued":
                results["queued_signals"] += 1
                handled_ids.append(entry_id)
                mutated_queue = True
            else:
                results["duplicates"] += 1
                handled_ids.append(entry_id)
            continue

        results["errors"].append(f"{entry_id}: unsupported type {entry_type!r}")

    if not dry_run:
        if mutated_library and library_path is not None:
            save_workspace_library(library_path, library_data, library_key)
        if mutated_queue:
            save_review_queue(review_queue)
        if handled_ids:
            results["ingested"] = mark_feedback_ingested(feedback_data, handled_ids)
            save_feedback(workspace_dir, feedback_data)
    else:
        results["ingested"] = len(handled_ids)

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Simplified MissionCanvas feedback enrichment")
    parser.add_argument(
        "--workspace",
        action="append",
        help="Workspace ID(s) to process. Repeat or pass comma-separated values.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without writing changes.",
    )
    args = parser.parse_args()

    run_id = make_run_id()
    selected_workspaces = normalize_workspace_ids(args.workspace)
    workspace_dirs = discover_workspaces(selected_workspaces)

    if not workspace_dirs:
        print("[canvas_enrichment] No workspaces with palette_feedback.yaml found.")
        return 0

    review_queue = load_review_queue()
    summaries: list[dict[str, Any]] = []
    totals = {
        "pending": 0,
        "promoted": 0,
        "queued_candidates": 0,
        "queued_signals": 0,
        "duplicates": 0,
        "ingested": 0,
        "errors": 0,
    }

    print(f"[canvas_enrichment] run={run_id} dry_run={args.dry_run}")
    for workspace_dir in workspace_dirs:
        summary = process_workspace(workspace_dir, review_queue, args.dry_run)
        summaries.append(summary)
        totals["pending"] += summary["pending"]
        totals["promoted"] += summary["promoted"]
        totals["queued_candidates"] += summary["queued_candidates"]
        totals["queued_signals"] += summary["queued_signals"]
        totals["duplicates"] += summary["duplicates"]
        totals["ingested"] += summary["ingested"]
        totals["errors"] += len(summary["errors"])

        print(
            "[canvas_enrichment] "
            f"{summary['workspace_id']}: pending={summary['pending']} promoted={summary['promoted']} "
            f"queued_candidates={summary['queued_candidates']} queued_signals={summary['queued_signals']} "
            f"duplicates={summary['duplicates']} ingested={summary['ingested']} errors={len(summary['errors'])}"
        )
        for err in summary["errors"]:
            print(f"  ERROR {err}")

    print("[canvas_enrichment] summary:")
    print(json.dumps({"run_id": run_id, **totals, "workspaces": [s["workspace_id"] for s in summaries]}, indent=2))

    append_audit(
        {
            "timestamp": utc_timestamp(),
            "action": "canvas_enrichment",
            "source": "canvas_feedback",
            "pipeline_run_id": run_id,
            "workspace_ids": [s["workspace_id"] for s in summaries],
            "dry_run": args.dry_run,
            "new_values": totals,
            "error": None if totals["errors"] == 0 else f"{totals['errors']} validation or routing errors",
        }
    )

    return 0 if totals["errors"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
