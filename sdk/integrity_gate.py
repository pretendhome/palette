"""
IntegrityGate — Pre-emit validation for agent outputs.

Adapts the 8 integrity checks from integrity.py into a single-result
validator that agents call before emitting a HandoffResult.

This is Stage 4 (Verification) of the machine enablement engine:
"Here's how to check your work."
"""

from __future__ import annotations

import re
from typing import Any


class IntegrityGate:
    """Validates a single HandoffResult against PIS data integrity rules.

    Not a full system audit (that's integrity.py). This is scoped validation:
    "Is what this agent is about to emit consistent with the system?"
    """

    def __init__(self, pis_data: Any):
        self.data = pis_data

    def check_result(self, result) -> list[str]:
        """Run all gate checks against a HandoffResult.

        Returns a list of warning strings (empty = clean).
        Warnings are informational, not blocking — glass-box, not gatekeeping.
        """
        if self.data is None:
            return ["IntegrityGate: PIS data is None — skipping checks"]
        if result is None:
            return ["IntegrityGate: result is None — nothing to check"]
        warnings = []
        warnings.extend(self._check_riu_references(result))
        warnings.extend(self._check_service_references(result))
        warnings.extend(self._check_knowledge_references(result))
        warnings.extend(self._check_gaps_populated(result))
        return warnings

    def _check_riu_references(self, result) -> list[str]:
        """Verify any RIU IDs mentioned in outputs, artifacts, or gaps exist in taxonomy."""
        warnings = []
        classification = getattr(self.data, "classification", {}) or {}
        if not classification:
            return warnings

        # Extract RIU references from outputs, artifacts, and gaps
        riu_ids = set()
        outputs = getattr(result, "outputs", None) or {}
        self._extract_riu_ids(outputs, riu_ids)
        artifacts = getattr(result, "artifacts", None) or []
        self._extract_riu_ids(artifacts, riu_ids)
        gaps = getattr(result, "gaps", None) or []
        self._extract_riu_ids(gaps, riu_ids)

        for riu_id in riu_ids:
            if riu_id not in classification:
                warnings.append(
                    f"RIU reference '{riu_id}' not found in taxonomy "
                    f"({len(classification)} RIUs loaded)"
                )
        return warnings

    def _check_service_references(self, result) -> list[str]:
        """Verify any service recommendations reference routed services."""
        warnings = []
        routing = getattr(self.data, "routing", {}) or {}
        if not routing:
            return warnings

        outputs = getattr(result, "outputs", None) or {}
        recommendation = outputs.get("recommendation")
        if not recommendation:
            return warnings

        # If recommending a service for a specific RIU, check it's routed
        riu_id = outputs.get("riu_id") or outputs.get("query_riu")
        service_name = (
            recommendation.get("service")
            or recommendation.get("name")
            or recommendation.get("service_name")
        )
        if riu_id and service_name and riu_id in routing:
            entry = routing[riu_id]
            service_names = []
            for svc in entry.get("services", []):
                service_names.append(svc.get("name", "").lower())
            if service_name.lower() not in service_names:
                warnings.append(
                    f"Service '{service_name}' not in routing for {riu_id}. "
                    f"Routed services: {service_names}"
                )
        return warnings

    def _check_knowledge_references(self, result) -> list[str]:
        """Verify any LIB IDs mentioned in outputs, artifacts, or gaps exist in knowledge library."""
        warnings = []
        knowledge = getattr(self.data, "knowledge", {}) or {}
        if not knowledge:
            return warnings

        lib_ids = set()
        outputs = getattr(result, "outputs", None) or {}
        self._extract_lib_ids(outputs, lib_ids)
        artifacts = getattr(result, "artifacts", None) or []
        self._extract_lib_ids(artifacts, lib_ids)
        gaps = getattr(result, "gaps", None) or []
        self._extract_lib_ids(gaps, lib_ids)

        for lib_id in lib_ids:
            if lib_id not in knowledge:
                warnings.append(
                    f"Knowledge reference '{lib_id}' not found in library "
                    f"({len(knowledge)} entries loaded)"
                )
        return warnings

    def _check_gaps_populated(self, result) -> list[str]:
        """Verify that agents don't emit empty gaps when outputs suggest uncertainty."""
        warnings = []
        outputs = getattr(result, "outputs", None) or {}
        status = getattr(result, "status", "success")
        gaps = getattr(result, "gaps", []) or []

        # If status is not success but gaps is empty, flag it
        if status == "failure" and not gaps:
            warnings.append(
                "Result status is 'failure' but gaps list is empty. "
                "Glass-box: explain what went wrong."
            )

        # If outputs contain ASSUMPTION labels, flag that gaps should mention them
        assumption_count = self._count_assumptions(outputs)
        if assumption_count > 0 and not gaps:
            warnings.append(
                f"Output contains {assumption_count} ASSUMPTION label(s) "
                "but gaps list is empty. Assumptions should surface as gaps."
            )

        return warnings

    # ── Helpers ─────────────────────────────────────────────────────────

    @staticmethod
    def _extract_riu_ids(obj: Any, collector: set[str]) -> None:
        """Recursively find RIU-NNN patterns in any nested structure."""
        if isinstance(obj, str):
            for m in re.finditer(r"RIU-\d{3}", obj):
                collector.add(m.group())
        elif isinstance(obj, dict):
            for v in obj.values():
                IntegrityGate._extract_riu_ids(v, collector)
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                IntegrityGate._extract_riu_ids(item, collector)

    @staticmethod
    def _extract_lib_ids(obj: Any, collector: set[str]) -> None:
        """Recursively find LIB-NNN patterns in any nested structure."""
        if isinstance(obj, str):
            for m in re.finditer(r"LIB-\d{3}", obj):
                collector.add(m.group())
        elif isinstance(obj, dict):
            for v in obj.values():
                IntegrityGate._extract_lib_ids(v, collector)
        elif isinstance(obj, (list, tuple)):
            for item in obj:
                IntegrityGate._extract_lib_ids(item, collector)

    @staticmethod
    def _count_assumptions(obj: Any) -> int:
        """Count ASSUMPTION: labels in any nested structure."""
        if isinstance(obj, str):
            return obj.upper().count("ASSUMPTION:")
        elif isinstance(obj, dict):
            return sum(
                IntegrityGate._count_assumptions(v) for v in obj.values()
            )
        elif isinstance(obj, (list, tuple)):
            return sum(
                IntegrityGate._count_assumptions(item) for item in obj
            )
        return 0
