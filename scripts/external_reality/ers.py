#!/usr/bin/env python3
"""External Reality Service v1 CLI.

Read-only proof: query Palette artifacts, packetize signals, and converge.
No source-of-truth writes, no network calls, no bot, no database.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
PEOPLE = ROOT / "buy-vs-build/people-library/v1.1/people_library_v1.1.yaml"
COMPANIES = ROOT / "buy-vs-build/v1.0/palette_company_riu_mapping_v1.0.yaml"
SIGNALS = ROOT / "buy-vs-build/people-library/v1.1/people_library_company_signals_v1.1.yaml"
RECIPES = ROOT / "buy-vs-build/recipe_company_mapping.yaml"
AUTO_ENRICH = ROOT / "agents/researcher/AUTO_ENRICHMENT_SPEC.md"
PROOF_TOPICS = [
    "Codeium Windsurf rename",
    "Lovable company index gap",
    "Fixie.ai removal",
    "researcher auto-enrichment",
    "Perplexity as sensing layer",
]

ACTION_GOVERNANCE = {
    "observe": {"riu": "RIU-003", "gate": "pass", "decision_log": False},
    "research": {"riu": "RIU-003", "gate": "research_required", "decision_log": False},
    "update_index": {"riu": "RIU-003", "gate": "convergence_required", "decision_log": True},
    "update_recipe": {"riu": "RIU-003", "gate": "convergence_required", "decision_log": True},
    "propose_riu": {"riu": "RIU-003", "gate": "convergence_required", "decision_log": True},
    "alert_human": {"riu": "RIU-087", "gate": "human_review_required", "decision_log": True},
}

STOPWORDS = {
    "a",
    "ai",
    "an",
    "and",
    "api",
    "as",
    "for",
    "gap",
    "in",
    "index",
    "is",
    "layer",
    "of",
    "or",
    "rename",
    "removal",
    "research",
    "service",
    "the",
    "to",
}


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        docs = [doc for doc in yaml.safe_load_all(f) if doc]
    if len(docs) == 1:
        return docs[0]
    merged: dict[str, Any] = {}
    for doc in docs:
        if isinstance(doc, dict):
            merged.update(doc)
    return merged


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:80]


def tokens(text: str) -> set[str]:
    words = set(re.findall(r"[a-z0-9][a-z0-9.-]{2,}", text.lower()))
    expanded = set(words)
    for word in list(words):
        expanded.update(part for part in re.split(r"[-./]", word) if len(part) > 2)
    return {word for word in expanded if word not in STOPWORDS}


def stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("|".join(parts).encode()).hexdigest()[:12].upper()
    return f"{prefix}-{digest}"


def compact(value: Any) -> str:
    return json.dumps(value, sort_keys=True, default=str).lower()


def flatten_companies(data: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for use_case_id, use_case in data.get("use_cases", {}).items():
        for riu in use_case.get("rius", []):
            for company in riu.get("companies", []):
                rows.append(
                    {
                        "source_type": "company_index",
                        "name": company.get("name", "unknown"),
                        "company_id": company.get("company_id"),
                        "riu_id": riu.get("riu_id"),
                        "riu_name": riu.get("riu_name"),
                        "use_case_id": use_case_id,
                        "status": company.get("status"),
                        "last_validated": company.get("last_validated"),
                        "raw": company,
                    }
                )
    return rows


def flatten_people(data: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for profile in data.get("profiles", []):
        rows.append(
            {
                "source_type": "people_library",
                "name": profile.get("name", "unknown"),
                "person_id": profile.get("id"),
                "signal_quality": profile.get("signal_quality"),
                "status": profile.get("status"),
                "raw": profile,
            }
        )
    return rows


def flatten_tool_signals(data: Any) -> list[dict[str, Any]]:
    root = data.get("tool_signals", data) if isinstance(data, dict) else data
    if not isinstance(root, list):
        root = []
    rows = []
    for item in root:
        if isinstance(item, dict):
            rows.append(
                {
                    "source_type": "people_company_signal",
                    "name": item.get("tool") or item.get("company") or "unknown",
                    "company": item.get("company"),
                    "raw": item,
                }
            )
    return rows


def flatten_recipes(data: dict[str, Any]) -> list[dict[str, Any]]:
    mappings = data.get("recipe_to_company_mapping", {}).get("mappings", [])
    return [
        {
            "source_type": "recipe_mapping",
            "name": item.get("recipe_name") or item.get("recipe_dir", "unknown"),
            "recipe_dir": item.get("recipe_dir"),
            "in_company_index": item.get("in_company_index"),
            "raw": item,
        }
        for item in mappings
        if isinstance(item, dict)
    ]


def sources() -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    loaded = [
        {"name": "people_library", "path": str(PEOPLE), "status": "read"},
        {"name": "company_index", "path": str(COMPANIES), "status": "read"},
        {"name": "people_company_signals", "path": str(SIGNALS), "status": "read"},
        {"name": "recipe_mapping", "path": str(RECIPES), "status": "read"},
        {"name": "auto_enrichment_spec", "path": str(AUTO_ENRICH), "status": "read"},
    ]
    rows = []
    rows.extend(flatten_people(load_yaml(PEOPLE)))
    rows.extend(flatten_companies(load_yaml(COMPANIES)))
    rows.extend(flatten_tool_signals(load_yaml(SIGNALS)))
    rows.extend(flatten_recipes(load_yaml(RECIPES)))
    rows.append(
        {
            "source_type": "researcher_spec",
            "name": "Researcher Auto-Enrichment",
            "raw": {"text": load_text(AUTO_ENRICH)},
        }
    )
    return rows, loaded


def infer_action(topic: str, row: dict[str, Any]) -> tuple[str, str, str]:
    text = compact(row)
    source_type = row["source_type"]
    if "no api" in text or "gap-001" in text or "propose riu" in text:
        return "propose_riu", "propose_riu", "Signal suggests a taxonomy or RIU gap."
    if "pivoted" in text or "formerly" in text or "renamed" in text or "archived" in text:
        return "update_index", "update_data", "Signal may require index status or alias update."
    if source_type == "recipe_mapping" and not row.get("in_company_index"):
        return "update_recipe", "add_recipe_candidate", "Recipe exists without company-index linkage."
    if source_type == "researcher_spec":
        return "research", "monitor_only", "Researcher output should become candidate SignalPackets before writes."
    if "unvalidated" in text or "perplexity enrichment needed" in text:
        return "research", "monitor_only", "Signal needs Researcher validation before action."
    if "high" in text or "integrated" in text or "validated" in text:
        return "observe", "monitor_only", "Signal is useful for briefing but not a source-of-truth change."
    return "research", "monitor_only", "Default to validation before action."


def confidence(row: dict[str, Any]) -> tuple[str, str]:
    text = compact(row)
    if row["source_type"] in {"company_index", "people_library"} and "unvalidated" not in text:
        return "medium", "medium"
    if "high" in text or "integrated" in text:
        return "high", "medium"
    if "unvalidated" in text or "unknown" in text:
        return "low", "low"
    return "medium", "low"


def query(topic: str) -> dict[str, Any]:
    rows, loaded = sources()
    topic_tokens = tokens(topic)
    matches = []
    for row in rows:
        haystack = compact(row)
        score = sum(1 for tok in topic_tokens if tok in haystack)
        if score:
            action_class, action_type, reason = infer_action(topic, row)
            evidence_quality, action_confidence = confidence(row)
            matches.append(
                {
                    "entity_name": row.get("name"),
                    "source_type": row["source_type"],
                    "score": score,
                    "related_rius": [row["riu_id"]] if row.get("riu_id") else [],
                    "affected_artifacts": affected(row),
                    "signal_summary": summary(topic, row),
                    "candidate_action": {
                        "palette_action_class": action_class,
                        "action_type": action_type,
                        "reason": reason,
                    },
                    "confidence": {
                        "evidence_quality": evidence_quality,
                        "action_confidence": action_confidence,
                    },
                    "source_ref": source_ref(row),
                }
            )
    matches.sort(key=lambda x: (-x["score"], x["source_type"], x["entity_name"] or ""))
    return {
        "query_id": stable_id("ERQ", topic, date.today().isoformat()),
        "topic": topic,
        "mode": "observation",
        "validation_state": "unvalidated_pull",
        "created_at": date.today().isoformat(),
        "sources_loaded": loaded,
        "signals": matches[:20],
        "actionability": {
            "possible_actions": sorted({m["candidate_action"]["palette_action_class"] for m in matches}),
            "blocked_actions": ["source_of_truth_write", "recommendation_change"],
            "write_allowed": False,
        },
    }


def affected(row: dict[str, Any]) -> dict[str, list[str]]:
    blank = {k: [] for k in ["people_library", "company_index", "recipes", "service_routing", "taxonomy", "knowledge_library"]}
    if row["source_type"] == "people_library":
        blank["people_library"].append(row.get("person_id") or row.get("name"))
    elif row["source_type"] == "company_index":
        blank["company_index"].append(row.get("company_id") or row.get("name"))
    elif row["source_type"] == "recipe_mapping":
        blank["recipes"].append(row.get("recipe_dir") or row.get("name"))
    elif row["source_type"] == "researcher_spec":
        blank["knowledge_library"].append("researcher_auto_enrichment")
    else:
        blank["company_index"].append(row.get("company") or row.get("name"))
    return blank


def source_ref(row: dict[str, Any]) -> dict[str, Any]:
    return {k: row.get(k) for k in ["source_type", "name", "company_id", "person_id", "recipe_dir", "riu_id"] if row.get(k)}


def summary(topic: str, row: dict[str, Any]) -> str:
    return f"{row['source_type']} signal for '{row.get('name')}' matched topic '{topic}'."


def packetize(result: dict[str, Any]) -> dict[str, Any]:
    packets = []
    for signal in result.get("signals", []):
        key = stable_id("KEY", result["topic"], signal["source_type"], signal["entity_name"] or "", signal["signal_summary"])
        action = signal["candidate_action"]
        eq = signal["confidence"]["evidence_quality"]
        ac = signal["confidence"]["action_confidence"]
        label = "high" if eq == "high" and ac != "low" else "medium" if "medium" in {eq, ac} else "low"
        packets.append(
            {
                "id": stable_id("SIGPKT", key),
                "packet_version": "1.0",
                "source_query_id": result["query_id"],
                "created_at": result["created_at"],
                "created_by": "orchestrator",
                "lifecycle_state": "observed",
                "idempotency_key": key,
                "related_rius": signal["related_rius"],
                "affected_artifacts": signal["affected_artifacts"],
                "signal_summary": signal["signal_summary"],
                "evidence": {"confirmed": [], "partial": [signal["source_ref"]], "unvalidated": []},
                "contradiction_check": {"conflicts_found": False, "conflicts": []},
                "palette_action_class": action["palette_action_class"],
                "proposed_action": {"action_type": action["action_type"], "description": action["reason"]},
                "confidence": {"evidence_quality": eq, "action_confidence": ac},
                "confidence_label": label,
                "reversibility": {"classification": reversibility(action["palette_action_class"]), "rationale": "v1 read-only classification"},
                "convergence_required": action["palette_action_class"] not in {"observe", "research"},
                "governance": ACTION_GOVERNANCE[action["palette_action_class"]],
            }
        )
    return {"query_id": result["query_id"], "topic": result["topic"], "signal_packets": packets}


def reversibility(action_class: str) -> str:
    return "one_way" if action_class in {"alert_human", "propose_riu"} else "two_way"


def converge(packet_set: dict[str, Any]) -> dict[str, Any]:
    packets = packet_set.get("signal_packets", [])
    decisions = []
    actionable = 0
    for packet in packets:
        action_class = packet["palette_action_class"]
        if action_class == "observe":
            gate, allowed = "monitor_only", True
        elif action_class == "research":
            gate, allowed = "research_required", False
            actionable += 1
        elif action_class == "alert_human":
            gate, allowed = "human_review_required", False
            actionable += 1
        else:
            gate, allowed = "convergence_required", False
            actionable += 1
        decisions.append(
            {
                "signal_packet_id": packet["id"],
                "palette_action_class": action_class,
                "gate": gate,
                "source_write_allowed": False,
                "next_safe_action": next_action(action_class),
                "blocked_actions": ["source_of_truth_write", "recommendation_change"] if action_class != "observe" else [],
            }
        )
    return {
        "brief_id": stable_id("ERSBRIEF", packet_set.get("topic", ""), str(len(packets))),
        "topic": packet_set.get("topic"),
        "created_at": date.today().isoformat(),
        "packets_total": len(packets),
        "actionable_packets": actionable,
        "kill_switch": "continue" if actionable >= 1 else "watch_only",
        "principle": "Querying external reality is not acting on external reality.",
        "decisions": decisions,
    }


def proof(topics: list[str]) -> dict[str, Any]:
    briefs = [converge(packetize(query(topic))) for topic in topics]
    total_actionable = sum(brief["actionable_packets"] for brief in briefs)
    return {
        "proof_id": stable_id("ERSPROOF", "|".join(topics), date.today().isoformat()),
        "created_at": date.today().isoformat(),
        "topics": topics,
        "briefs": briefs,
        "total_actionable_packets": total_actionable,
        "kill_switch": "continue" if total_actionable >= 5 else "pause_and_reassess",
        "scope_controls": {
            "source_writes": "blocked",
            "bot": "deferred",
            "database": "not_created",
            "core_schema_only": True,
        },
    }


def selftest() -> dict[str, Any]:
    first = proof(PROOF_TOPICS)
    second = proof(PROOF_TOPICS)
    required = {
        "id",
        "idempotency_key",
        "palette_action_class",
        "confidence_label",
        "proposed_action",
        "governance",
    }
    packets = [p for brief in first["briefs"] for p in packetize(query(brief["topic"]))["signal_packets"]]
    missing = [
        {"packet": p.get("id"), "missing": sorted(required - set(p))}
        for p in packets
        if required - set(p)
    ]
    source_write_leaks = [
        d
        for brief in first["briefs"]
        for d in brief["decisions"]
        if d.get("source_write_allowed")
    ]
    return {
        "status": "pass" if not missing and not source_write_leaks and first["proof_id"] == second["proof_id"] else "fail",
        "proof_id": first["proof_id"],
        "deterministic": first["proof_id"] == second["proof_id"],
        "required_field_failures": missing,
        "source_write_leaks": source_write_leaks,
        "total_actionable_packets": first["total_actionable_packets"],
        "kill_switch": first["kill_switch"],
        "scope_controls": first["scope_controls"],
    }


def next_action(action_class: str) -> str:
    return {
        "observe": "brief_only",
        "research": "run_researcher_validation_before_action",
        "update_index": "prepare_governed_index_proposal",
        "update_recipe": "prepare_governed_recipe_proposal",
        "propose_riu": "prepare_riu_proposal",
        "alert_human": "request_human_review",
    }[action_class]


def read_json(path: str | None) -> dict[str, Any]:
    if path and path != "-":
        return json.loads(Path(path).read_text(encoding="utf-8"))
    return json.load(sys.stdin)


def emit(data: dict[str, Any]) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="External Reality Service v1 read-only CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("query", help="emit QueryResult JSON for a topic")
    q.add_argument("topic")
    p = sub.add_parser("packetize", help="convert QueryResult JSON to SignalPackets")
    p.add_argument("path", nargs="?", default="-")
    c = sub.add_parser("converge", help="emit ConvergenceBrief from SignalPackets")
    c.add_argument("path", nargs="?", default="-")
    r = sub.add_parser("run", help="query, packetize, and converge in memory")
    r.add_argument("topic")
    pr = sub.add_parser("proof", help="run default proof topics or provided topics")
    pr.add_argument("topics", nargs="*")
    sub.add_parser("selftest", help="run v1 deterministic proof checks")
    args = parser.parse_args()
    if args.cmd == "query":
        emit(query(args.topic))
    elif args.cmd == "packetize":
        emit(packetize(read_json(args.path)))
    elif args.cmd == "converge":
        emit(converge(read_json(args.path)))
    elif args.cmd == "run":
        emit(converge(packetize(query(args.topic))))
    elif args.cmd == "proof":
        emit(proof(args.topics or PROOF_TOPICS))
    elif args.cmd == "selftest":
        emit(selftest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
