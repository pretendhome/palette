"""
GraphQuery — Queryable interface to the Palette relationship graph.

Turns the RELATIONSHIP_GRAPH.yaml (1,800+ quads, 13 predicates, 9 entity types)
from a documentation artifact into a callable query interface.

This is Stage 5 (Organization) of the machine enablement engine:
"Here's how it all connects."
"""

from __future__ import annotations

import os
import sys
from typing import Any


class GraphQuery:
    """Query the Palette relationship graph by subject, predicate, and/or object.

    The graph stores bidirectional relationships:
      Agent → handles_riu → RIU     (and reverse: RIU → routed_to → Agent)
      Person → recommends → Tool    (and reverse: Tool → recommended_by → Person)
      RIU → has_service → Service
      RIU → has_knowledge → LIB
      Lens → applies_to → RIU

    Query any combination of S/P/O to filter:
      query(subject="Architect")                    → everything about Architect
      query(predicate="handles_riu")                → all agent→RIU mappings
      query(subject="RIU-082", predicate="has_service") → services for RIU-082
      query(object="OpenRouter")                    → everything pointing to OpenRouter
    """

    def __init__(self, quads: list[dict]):
        self._quads = quads
        self._by_subject: dict[str, list[dict]] = {}
        self._by_predicate: dict[str, list[dict]] = {}
        self._by_object: dict[str, list[dict]] = {}
        self._index()

    def _index(self) -> None:
        """Build lookup indexes for fast querying."""
        for q in self._quads:
            s = q.get("subject", "")
            p = q.get("predicate", "")
            o = q.get("object", "")
            self._by_subject.setdefault(s, []).append(q)
            self._by_predicate.setdefault(p, []).append(q)
            self._by_object.setdefault(o, []).append(q)

    @property
    def quad_count(self) -> int:
        return len(self._quads)

    @property
    def predicates(self) -> list[str]:
        """All predicate types in the graph."""
        return sorted(self._by_predicate.keys())

    @property
    def subjects(self) -> list[str]:
        """All unique subjects in the graph."""
        return sorted(self._by_subject.keys())

    def query(
        self,
        subject: str | None = None,
        predicate: str | None = None,
        object: str | None = None,
    ) -> list[dict]:
        """Filter quads by any combination of subject, predicate, object.

        Returns matching quads as dicts with keys: id, subject, predicate, object, meta.
        Uses indexed lookups for single-field queries, intersection for multi-field.
        """
        # Start with the most selective index
        candidates = None

        if subject is not None:
            candidates = set(id(q) for q in self._by_subject.get(subject, []))
            pool = self._by_subject.get(subject, [])
        if predicate is not None:
            pred_set = set(id(q) for q in self._by_predicate.get(predicate, []))
            if candidates is None:
                candidates = pred_set
                pool = self._by_predicate.get(predicate, [])
            else:
                candidates &= pred_set
        if object is not None:
            obj_set = set(id(q) for q in self._by_object.get(object, []))
            if candidates is None:
                candidates = obj_set
                pool = self._by_object.get(object, [])
            else:
                candidates &= obj_set

        if candidates is None:
            return list(self._quads)

        # Filter from the smallest pool
        return [q for q in self._quads if id(q) in candidates]

    def objects_for(self, subject: str, predicate: str) -> list[str]:
        """Shorthand: get all objects for a given subject+predicate.

        Example:
            graph.objects_for("Architect", "handles_riu")
            → ["RIU-001", "RIU-014", "RIU-062", ...]
        """
        return [
            q["object"]
            for q in self.query(subject=subject, predicate=predicate)
        ]

    def subjects_for(self, predicate: str, object: str) -> list[str]:
        """Shorthand: get all subjects for a given predicate+object.

        Example:
            graph.subjects_for("recommends", "OpenRouter")
            → ["PERSON-019", "PERSON-020"]
        """
        return [
            q["subject"]
            for q in self.query(predicate=predicate, object=object)
        ]

    def neighbors(self, entity: str) -> dict[str, list[str]]:
        """Get all relationships for an entity (as subject or object).

        Returns: {predicate: [connected_entities]}

        Example:
            graph.neighbors("RIU-082")
            → {
                "routed_to": ["Validator", "Builder"],
                "has_service": ["Bedrock Guardrails", "Lakera Guard"],
                "has_knowledge": ["LIB-042", "LIB-089"],
                "classified_as": ["both"],
              }
        """
        result: dict[str, list[str]] = {}

        # As subject: entity → predicate → object
        for q in self._by_subject.get(entity, []):
            result.setdefault(q["predicate"], []).append(q["object"])

        # As object: subject → predicate → entity (reverse)
        for q in self._by_object.get(entity, []):
            pred = f"<-{q['predicate']}"
            result.setdefault(pred, []).append(q["subject"])

        return result

    def summary(self) -> dict:
        """System-level summary of the graph."""
        return {
            "total_quads": len(self._quads),
            "predicates": {p: len(qs) for p, qs in self._by_predicate.items()},
            "unique_subjects": len(self._by_subject),
            "unique_objects": len(self._by_object),
        }

    @classmethod
    def from_yaml(cls, palette_root: str | None = None) -> GraphQuery | None:
        """Load the relationship graph from RELATIONSHIP_GRAPH.yaml."""
        root = palette_root or os.environ.get(
            "PALETTE_ROOT",
            os.path.join(os.path.expanduser("~"), "fde", "palette"),
        )
        path = os.path.join(root, "RELATIONSHIP_GRAPH.yaml")
        if not os.path.exists(path):
            return None

        try:
            import yaml
            with open(path) as f:
                data = yaml.safe_load(f)
            quads = data.get("quads", [])
            return cls(quads)
        except Exception as exc:
            print(
                f"[GraphQuery] Failed to load {path}: {exc}",
                file=sys.stderr,
            )
            return None
