#!/usr/bin/env python3
"""Multi-agent coordination CLI — HandoffPacket v2 + deterministic replay.

Runs a 4-step coordination pipeline:
  resolver   → resolve user query to RIU(s) via keyword matching
  traversal  → run real PIS traversal for the selected RIU
  researcher → add research notes / gap annotations (stubbed)
  final      → aggregate results, set overall task status

Usage:
  python -m scripts.palette_intelligence_system.coordination run "add guardrails to my llm app"
  python -m scripts.palette_intelligence_system.coordination show <task_id>
  python -m scripts.palette_intelligence_system.coordination replay <task_id>
  python -m scripts.palette_intelligence_system.coordination list

Replay Semantics:
  `replay` finds the first step with status 'failed', preserves all upstream
  'success' steps (their outputs are NOT re-executed), resets the failed step
  and all downstream steps to 'pending', then re-executes from that point.
  Upstream outputs are kept intact. Downstream outputs are cleared before
  re-execution. Replay is NOT idempotent if the underlying YAML data has
  changed between runs — but it IS safe: prior outputs are never corrupted.
  The `attempt` counter on each step tracks how many times it has been run.

Failure Injection:
  `--fail-step <name>` injects a RuntimeError at the named step, useful for
  testing replay recovery without needing broken data.

Dependencies:
  stdlib + pyyaml only. No network calls.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Any, Dict, List, Optional

from .cli import keyword_resolve
from .loader import PISData, load_all
from .traverse import traverse

# ── Constants ──────────────────────────────────────────────────────

SCHEMA_VERSION = "handoffpacket.v2"
STEP_ORDER = ("resolver", "traversal", "researcher", "final")


# ── Paths ──────────────────────────────────────────────────────────

def _default_state_dir() -> Path:
    override = os.environ.get("PIS_COORDINATION_STATE_DIR")
    if override:
        return Path(override)
    return Path(__file__).resolve().parent / "state" / "tasks"


def _task_path(task_id: str) -> Path:
    return _default_state_dir() / f"{task_id}.json"


def _ensure_state_dir() -> Path:
    d = _default_state_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d


# ── Atomic I/O ─────────────────────────────────────────────────────

def _atomic_write(path: Path, data: Dict[str, Any]) -> None:
    """Write JSON atomically via temp file + rename."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", delete=False, dir=str(path.parent), suffix=".tmp"
    ) as tf:
        json.dump(data, tf, indent=2, default=str)
        tf.write("\n")
        tmp = tf.name
    os.replace(tmp, str(path))


def _load_packet(task_id: str) -> Dict[str, Any]:
    path = _task_path(task_id)
    if not path.exists():
        raise FileNotFoundError(f"Task not found: {task_id}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _save_packet(packet: Dict[str, Any]) -> None:
    packet["updated_at"] = _utcnow()
    _atomic_write(_task_path(packet["task_id"]), packet)


# ── Time ───────────────────────────────────────────────────────────

def _utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


# ── Packet Factory ─────────────────────────────────────────────────

def _new_step(name: str) -> Dict[str, Any]:
    return {
        "name": name,
        "status": "pending",
        "started_at": None,
        "ended_at": None,
        "attempt": 0,
        "error": None,
    }


def _new_packet(user_query: str) -> Dict[str, Any]:
    task_id = f"task-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    return {
        "schema_version": SCHEMA_VERSION,
        "task_id": task_id,
        "created_at": _utcnow(),
        "updated_at": _utcnow(),
        "user_query": user_query,
        "status": "pending",
        "resolved_rius": [],
        "steps": {name: _new_step(name) for name in STEP_ORDER},
        "outputs": {},
        "gaps": [],
        "errors": [],
        "provenance": {
            "tool": "scripts.palette_intelligence_system.coordination",
            "version": "v2",
            "traversal_module": "scripts.palette_intelligence_system.traverse",
            "resolver_module": "scripts.palette_intelligence_system.cli.keyword_resolve",
        },
    }


# ── Step Helpers ───────────────────────────────────────────────────

def _mark_running(packet: Dict[str, Any], step_name: str) -> None:
    step = packet["steps"][step_name]
    step["status"] = "running"
    step["started_at"] = _utcnow()
    step["attempt"] = step.get("attempt", 0) + 1


def _mark_success(packet: Dict[str, Any], step_name: str) -> None:
    step = packet["steps"][step_name]
    step["status"] = "success"
    step["ended_at"] = _utcnow()
    step["error"] = None


def _mark_failed(packet: Dict[str, Any], step_name: str, error: str) -> None:
    step = packet["steps"][step_name]
    step["status"] = "failed"
    step["ended_at"] = _utcnow()
    step["error"] = error
    packet["status"] = "failed"
    packet["errors"].append({"step": step_name, "ts": _utcnow(), "error": error})


# ── Step Implementations ──────────────────────────────────────────

def _step_resolver(packet: Dict[str, Any], data: PISData, fail_step: Optional[str]) -> None:
    """Resolve user query → RIU(s) using keyword_resolve from cli.py."""
    if fail_step == "resolver":
        raise RuntimeError("Injected failure at resolver step")

    lib_id, confidence, top_3 = keyword_resolve(data, packet["user_query"])

    candidates: List[Dict[str, Any]] = []
    for cand_id, cand_conf in top_3:
        entry = data.knowledge.get(cand_id, {})
        related = entry.get("related_rius", [])
        candidates.append({
            "lib_id": cand_id,
            "riu_id": related[0] if related else None,
            "confidence": round(cand_conf, 1),
            "riu_name": data.classification.get(related[0], {}).get("name", "") if related else "",
        })

    # Select best candidate
    selected = None
    if lib_id:
        entry = data.knowledge.get(lib_id, {})
        related = entry.get("related_rius", [])
        if related:
            selected = {
                "riu_id": related[0],
                "confidence": round(confidence, 1),
                "resolved_from": lib_id,
            }

    if not selected and candidates:
        # Use best even at low confidence
        best = candidates[0]
        if best.get("riu_id"):
            selected = {
                "riu_id": best["riu_id"],
                "confidence": best["confidence"],
                "resolved_from": best["lib_id"],
            }

    if selected:
        packet["resolved_rius"] = [selected]
    else:
        packet["gaps"].append("No RIU candidates resolved from query")

    packet["outputs"]["resolver"] = {
        "resolved_count": len(packet["resolved_rius"]),
        "selected_riu": selected["riu_id"] if selected else None,
        "candidates": candidates,
    }


def _step_traversal(packet: Dict[str, Any], data: PISData, fail_step: Optional[str]) -> None:
    """Run real PIS traversal for the resolved RIU."""
    if fail_step == "traversal":
        raise RuntimeError("Injected failure at traversal step")

    if not packet.get("resolved_rius"):
        raise RuntimeError("No RIUs resolved; cannot run traversal")

    primary = packet["resolved_rius"][0]
    riu_id = primary.get("riu_id")
    lib_id = primary.get("resolved_from")

    if not riu_id and not lib_id:
        raise RuntimeError("No RIU or LIB ID available for traversal")

    result = traverse(data, riu_id=riu_id, lib_id=lib_id, track_health=False)

    # Store structured output (JSON-safe via asdict)
    result_dict = asdict(result)
    packet["outputs"]["traversal"] = {
        "riu_id": result.query_riu,
        "riu_name": result.query_riu_name,
        "classification": result.classification,
        "completeness": result.completeness.total if result.completeness else None,
        "completeness_label": result.completeness.label if result.completeness else None,
        "recommendation": result.recommendation.service_name if result.recommendation else None,
        "recommendation_cost": result.recommendation.cost_estimate if result.recommendation else None,
        "alternatives": [a.service_name for a in result.alternatives],
        "gaps": result.gaps,
        "health_status": result.health_status,
        "full_result": result_dict,
    }

    # Propagate gaps from traversal to task level
    for gap in result.gaps:
        if gap not in packet["gaps"]:
            packet["gaps"].append(gap)


def _step_researcher(packet: Dict[str, Any], data: PISData, fail_step: Optional[str]) -> None:
    """Researcher step: add research notes and gap annotations (stubbed/deterministic)."""
    if fail_step == "researcher":
        raise RuntimeError("Injected failure at researcher step")

    trav = packet.get("outputs", {}).get("traversal", {})
    notes: List[str] = []
    research_gaps: List[str] = []

    cls = trav.get("classification", "")
    completeness = trav.get("completeness")
    recommendation = trav.get("recommendation")
    gaps = trav.get("gaps", [])

    if cls == "internal_only":
        notes.append("Internal-only RIU — no external service evaluation needed")
    elif cls == "both" and recommendation:
        notes.append(f"Primary recommendation: {recommendation} (cost: {trav.get('recommendation_cost', '?')})")
        if trav.get("alternatives"):
            notes.append(f"Alternatives available: {', '.join(trav['alternatives'])}")

    if completeness is not None and completeness < 60:
        research_gaps.append(f"Completeness {completeness}/100 — data enrichment needed")

    recipe_gaps = [g for g in gaps if "recipe" in g.lower()]
    if recipe_gaps:
        research_gaps.append("Missing integration recipes — Perplexity research recommended")

    signal_gaps = [g for g in gaps if "signal" in g.lower() or "people-library" in g.lower()]
    if signal_gaps:
        research_gaps.append("No people-library signal validation — check for expert endorsements")

    if not notes:
        notes.append("No additional Researcher notes (stubbed deterministic path)")

    for rg in research_gaps:
        if rg not in packet["gaps"]:
            packet["gaps"].append(rg)

    packet["outputs"]["researcher"] = {
        "notes": notes,
        "research_gaps": research_gaps,
        "mode": "stubbed-deterministic",
    }


def _step_final(packet: Dict[str, Any], data: PISData, fail_step: Optional[str]) -> None:
    """Final step: aggregate results, determine overall task status."""
    selected = None
    if packet.get("resolved_rius"):
        selected = packet["resolved_rius"][0].get("riu_id")

    failed_steps = [
        name for name in STEP_ORDER
        if name != "final" and packet["steps"][name]["status"] == "failed"
    ]

    packet["outputs"]["final"] = {
        "selected_riu": selected,
        "summary": f"Coordinated resolver → traversal → researcher for {selected or 'no RIU'}",
        "total_gaps": len(packet["gaps"]),
        "failed_steps": failed_steps,
        "next_action": (
            "Review gaps and decide whether to enrich routing/recipes"
            if packet["gaps"]
            else "Proceed with recommendation synthesis"
        ),
    }


# ── Step Dispatch ──────────────────────────────────────────────────

_STEP_RUNNERS = {
    "resolver": _step_resolver,
    "traversal": _step_traversal,
    "researcher": _step_researcher,
    "final": _step_final,
}


# ── Run / Replay Engine ───────────────────────────────────────────

def _run_steps(
    packet: Dict[str, Any],
    data: PISData,
    start_step: str,
    fail_step: Optional[str] = None,
) -> None:
    """Execute steps from start_step onward. On failure, skip downstream."""
    started = False
    packet["status"] = "running"

    for step_name in STEP_ORDER:
        if step_name == start_step:
            started = True
        if not started:
            continue

        _mark_running(packet, step_name)
        _save_packet(packet)

        try:
            _STEP_RUNNERS[step_name](packet, data, fail_step)
            _mark_success(packet, step_name)
            _save_packet(packet)
        except Exception as e:
            _mark_failed(packet, step_name, str(e))
            # Skip downstream (except we don't re-enter the loop for them)
            _save_packet(packet)
            return

    packet["status"] = "completed"
    _save_packet(packet)


def _first_failed_step(packet: Dict[str, Any]) -> Optional[str]:
    for name in STEP_ORDER:
        if packet["steps"][name]["status"] == "failed":
            return name
    return None


def _reset_for_replay(packet: Dict[str, Any], start_step: str) -> None:
    """Reset failed step + downstream to 'pending', clear their outputs."""
    start_idx = STEP_ORDER.index(start_step)
    for name in STEP_ORDER[start_idx:]:
        step = packet["steps"][name]
        step["status"] = "pending"
        step["started_at"] = None
        step["ended_at"] = None
        step["error"] = None
        # Don't reset attempt — it accumulates across replays
        packet["outputs"].pop(name, None)
    packet["status"] = "pending"


# ── CLI Commands ───────────────────────────────────────────────────

def cmd_run(user_query: str, fail_step: Optional[str] = None) -> int:
    _ensure_state_dir()
    packet = _new_packet(user_query)
    _save_packet(packet)

    data = load_all()
    _run_steps(packet, data, start_step="resolver", fail_step=fail_step)

    final = _load_packet(packet["task_id"])
    print(final["task_id"])
    print(f"status={final['status']}")
    return 0 if final["status"] == "completed" else 1


def cmd_show(task_id: str) -> int:
    packet = _load_packet(task_id)
    print(json.dumps(packet, indent=2, default=str))
    failed = _first_failed_step(packet)
    if failed:
        print(f"\n# replay_next: {failed} (failed+downstream only)")
    return 0


def cmd_replay(task_id: str, fail_step: Optional[str] = None) -> int:
    packet = _load_packet(task_id)
    failed = _first_failed_step(packet)
    if not failed:
        print(f"{task_id}: no failed step; nothing to replay")
        return 0

    _reset_for_replay(packet, failed)
    _save_packet(packet)

    data = load_all()
    _run_steps(packet, data, start_step=failed, fail_step=fail_step)

    final = _load_packet(task_id)
    print(task_id)
    print(f"replayed_from={failed}")
    print(f"status={final['status']}")
    return 0 if final["status"] == "completed" else 1


def cmd_list() -> int:
    state_dir = _ensure_state_dir()
    files = sorted(state_dir.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not files:
        print("No tasks found.")
        return 0
    for path in files:
        try:
            with open(path, encoding="utf-8") as f:
                p = json.load(f)
            print(f"{p.get('task_id', '?')}\t{p.get('status', '?')}\t{p.get('user_query', '')}")
        except Exception as e:
            print(f"{path.name}\tERROR\t{e}")
    return 0


# ── Argument Parser ────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="PIS coordination — HandoffPacket v2 + task replay"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_run = sub.add_parser("run", help="Run a new coordination task")
    p_run.add_argument("user_query")
    p_run.add_argument("--fail-step", choices=["resolver", "traversal", "researcher"],
                       help="Inject failure at this step (for testing)")

    p_show = sub.add_parser("show", help="Show task packet (JSON)")
    p_show.add_argument("task_id")

    p_replay = sub.add_parser("replay", help="Replay from first failed step")
    p_replay.add_argument("task_id")
    p_replay.add_argument("--fail-step", choices=["resolver", "traversal", "researcher"],
                          help="Inject failure at this step during replay")

    sub.add_parser("list", help="List all task packets")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "run":
            return cmd_run(args.user_query, getattr(args, "fail_step", None))
        if args.command == "show":
            return cmd_show(args.task_id)
        if args.command == "replay":
            return cmd_replay(args.task_id, getattr(args, "fail_step", None))
        if args.command == "list":
            return cmd_list()
    except FileNotFoundError as e:
        print(str(e), file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
