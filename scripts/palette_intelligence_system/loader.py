"""Load all 4 PIS data layers + classification from YAML files."""

from __future__ import annotations

import glob as globmod
import os
from dataclasses import dataclass, field

import yaml


@dataclass
class PISData:
    knowledge: dict[str, dict] = field(default_factory=dict)   # LIB-XXX → entry
    routing: dict[str, dict] = field(default_factory=dict)      # RIU-XXX → routing entry
    recipes: dict[str, dict] = field(default_factory=dict)      # service_name (lowered) → recipe
    signals: list[dict] = field(default_factory=list)            # crossref signal entries
    classification: dict[str, dict] = field(default_factory=dict)  # RIU-XXX → classification entry


def _palette_root() -> str:
    return os.environ.get(
        "PALETTE_ROOT",
        os.path.join(os.path.expanduser("~"), "fde", "palette"),
    )


def _load_yaml_docs(path: str) -> list[dict]:
    """Load a multi-document YAML file and return all docs as a list."""
    with open(path, "r") as f:
        return [doc for doc in yaml.safe_load_all(f) if doc is not None]


def _normalize_gap_addition(item: dict) -> dict:
    """Convert a gap_additions entry to standard knowledge entry format."""
    proposed = item.get("proposed_answer", {})
    return {
        "id": item["id"],
        "question": item.get("question", ""),
        "answer": proposed.get("primary_action", "") + " " + proposed.get("implementation", ""),
        "problem_type": item.get("problem_type", ""),
        "related_rius": proposed.get("related_rius", []),
        "difficulty": item.get("difficulty", "medium"),
        "industries": item.get("industries", []),
        "tags": item.get("tags", []),
        "journey_stage": item.get("journey_stage", ""),
        "sources": item.get("sources", []),
        "_from_gap_additions": True,
    }


def _load_knowledge(root: str) -> dict[str, dict]:
    path = os.path.join(root, "knowledge-library", "v1.4", "palette_knowledge_library_v1.4.yaml")
    docs = _load_yaml_docs(path)
    entries: dict[str, dict] = {}
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        for item in doc.get("library_questions", []):
            entries[item["id"]] = item
        # Also load gap_additions (proposed entries with different schema)
        for item in doc.get("gap_additions", []):
            if item.get("id") and item["id"] not in entries:
                entries[item["id"]] = _normalize_gap_addition(item)
    return entries


def _load_routing(root: str) -> dict[str, dict]:
    path = os.path.join(root, "buy-vs-build", "service-routing", "v1.0", "service_routing_v1.0.yaml")
    docs = _load_yaml_docs(path)
    entries: dict[str, dict] = {}
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        for item in doc.get("routing_entries", []):
            entries[item["riu_id"]] = item
    return entries


def _load_recipes(root: str) -> dict[str, dict]:
    pattern = os.path.join(root, "buy-vs-build", "integrations", "*", "recipe.yaml")
    entries: dict[str, dict] = {}
    for path in globmod.glob(pattern):
        docs = _load_yaml_docs(path)
        for doc in docs:
            if not isinstance(doc, dict):
                continue
            name = doc.get("service_name", "")
            if name:
                entries[name.lower()] = {**doc, "_recipe_path": path}
    return entries


def _load_signals(root: str) -> list[dict]:
    path = os.path.join(
        root, "buy-vs-build", "people-library", "v1.1",
        "people_library_company_signals_v1.1.yaml",
    )
    docs = _load_yaml_docs(path)
    entries: list[dict] = []
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        entries.extend(doc.get("signals", []))
    return entries


def _load_classification(root: str) -> dict[str, dict]:
    path = os.path.join(root, "buy-vs-build", "service-routing", "v1.0", "riu_classification_v1.0.yaml")
    docs = _load_yaml_docs(path)
    entries: dict[str, dict] = {}
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        for item in doc.get("rius", []):
            entries[item["riu_id"]] = item
    return entries


def load_all(root: str | None = None) -> PISData:
    """Load all PIS data layers. Returns a PISData dataclass."""
    root = root or _palette_root()
    return PISData(
        knowledge=_load_knowledge(root),
        routing=_load_routing(root),
        recipes=_load_recipes(root),
        signals=_load_signals(root),
        classification=_load_classification(root),
    )
