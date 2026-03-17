"""
IntegrityGate — Pre-emit validation for agent outputs.

Validates a HandoffResult against PIS data before it hits the wire.
This is Stage 4 (Verification): "Here's how to check your work."

Checks:
  1. RIU references in output, artifacts, blockers exist in taxonomy
  2. Service recommendations match routing table
  3. Knowledge references exist in library
  4. Non-success status has blockers (glass-box invariant)
"""

from __future__ import annotations

import re
from typing import Any


class IntegrityGate:
    """Validates a HandoffResult against PIS data integrity rules.

    Warnings are informational, not blocking — glass-box, not gatekeeping.
    """

    def __init__(self, pis_data: Any):
        self.data = pis_data

    def check_result(self, result) -> list[str]:
        """Run all gate checks. Returns list of warnings (empty = clean)."""
        if self.data is None:
            return ["IntegrityGate: PIS data is None — skipping checks"]
        if result is None:
            return ["IntegrityGate: result is None — nothing to check"]
        warnings = []
        warnings.extend(self._check_riu_references(result))
        warnings.extend(self._check_service_references(result))
        warnings.extend(self._check_knowledge_references(result))
        warnings.extend(self._check_blockers_populated(result))
        return warnings

    def _check_riu_references(self, result) -> list[str]:
        """Verify any RIU IDs mentioned in output, artifacts, or blockers exist in taxonomy."""
        warnings = []
        classification = getattr(self.data, "classification", {}) or {}
        if not classification:
            return warnings

        riu_ids = set()
        output = getattr(result, "output", None) or getattr(result, "outputs", None) or {}
        self._extract_riu_ids(output, riu_ids)
        artifacts = getattr(result, "artifacts", None) or []
        self._extract_riu_ids(artifacts, riu_ids)
        blockers = getattr(result, "blockers", None) or getattr(result, "gaps", None) or []
        self._extract_riu_ids(blockers, riu_ids)

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

        output = getattr(result, "output", None) or getattr(result, "outputs", None) or {}
        recommendation = output.get("recommendation")
        if not recommendation:
            return warnings

        riu_id = output.get("riu_id") or output.get("query_riu")
        service_name = (
            recommendation.get("service")
            or recommendation.get("name")
            or recommendation.get("service_name")
        )
        if riu_id and service_name and riu_id in routing:
            entry = routing[riu_id]
            service_names = [svc.get("name", "").lower() for svc in entry.get("services", [])]
            if service_name.lower() not in service_names:
                warnings.append(
                    f"Service '{service_name}' not in routing for {riu_id}. "
                    f"Routed services: {service_names}"
                )
        return warnings

    def _check_knowledge_references(self, result) -> list[str]:
        """Verify any LIB IDs mentioned in output, artifacts, or blockers exist in library."""
        warnings = []
        knowledge = getattr(self.data, "knowledge", {}) or {}
        if not knowledge:
            return warnings

        lib_ids = set()
        output = getattr(result, "output", None) or getattr(result, "outputs", None) or {}
        self._extract_lib_ids(output, lib_ids)
        artifacts = getattr(result, "artifacts", None) or []
        self._extract_lib_ids(artifacts, lib_ids)
        blockers = getattr(result, "blockers", None) or getattr(result, "gaps", None) or []
        self._extract_lib_ids(blockers, lib_ids)

        for lib_id in lib_ids:
            if lib_id not in knowledge:
                warnings.append(
                    f"Knowledge reference '{lib_id}' not found in library "
                    f"({len(knowledge)} entries loaded)"
                )
        return warnings

    def _check_blockers_populated(self, result) -> list[str]:
        """Verify non-success results explain why (glass-box invariant #3)."""
        warnings = []
        output = getattr(result, "output", None) or getattr(result, "outputs", None) or {}
        status = getattr(result, "status", "success")
        blockers = getattr(result, "blockers", None) or getattr(result, "gaps", None) or []

        if status in ("failure", "blocked") and not blockers:
            warnings.append(
                f"Result status is '{status}' but blockers list is empty. "
                "Glass-box: explain what went wrong."
            )

        assumption_count = self._count_assumptions(output)
        if assumption_count > 0 and not blockers:
            warnings.append(
                f"Output contains {assumption_count} ASSUMPTION label(s) "
                "but blockers list is empty. Assumptions should surface as blockers."
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
            return sum(IntegrityGate._count_assumptions(v) for v in obj.values())
        elif isinstance(obj, (list, tuple)):
            return sum(IntegrityGate._count_assumptions(item) for item in obj)
        return 0
