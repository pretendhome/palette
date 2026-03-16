"""
AgentBase — Machine Enablement Engine

Parallel to the human enablement coach's 7 stages:

  Stage 1 (Foundations)      → load_all()          "Here's what exists"
  Stage 2 (First Instructions) → query_pis()       "Here's how to ask"
  Stage 3 (Memory)           → HandoffPacket       "Here's how to carry context"
  Stage 4 (Verification)     → validate_output()   "Here's how to check your work"
  Stage 5 (Organization)     → query_graph()       "Here's how it connects"
  Stage 6 (Building)         → execute() protocol  "Here's how to create"
  Stage 7 (Autonomy)         → integrity self-check "Here's how to be independent"

Any agent that inherits from AgentBase gets instant access to the full
Palette Intelligence System — the same knowledge the human enablement coach
teaches progressively, delivered as structured interfaces.
"""

from __future__ import annotations

import json
import sys
import os
import datetime
from dataclasses import dataclass, field, asdict
from typing import Any

# Add palette root and its parent to path for PIS and package imports
_palette_root = os.environ.get(
    "PALETTE_ROOT",
    os.path.join(os.path.expanduser("~"), "fde", "palette"),
)
_palette_parent = os.path.dirname(_palette_root)
if _palette_root not in sys.path:
    sys.path.insert(0, _palette_root)
if _palette_parent not in sys.path:
    sys.path.insert(0, _palette_parent)

from scripts.palette_intelligence_system.loader import load_all
from scripts.palette_intelligence_system.traverse import traverse
from palette.sdk.integrity_gate import IntegrityGate
from palette.sdk.graph_query import GraphQuery


@dataclass
class PaletteContext:
    """Everything an agent needs to know about the system it's operating in.

    This is the machine equivalent of what the enablement coach builds
    up over 7 stages with a human learner — delivered all at once.
    """

    pis_data: Any = None
    integrity_gate: IntegrityGate | None = None
    graph_query: GraphQuery | None = None
    palette_root: str = ""
    loaded_at: str = ""

    @classmethod
    def load(cls, root: str | None = None) -> PaletteContext:
        """Load all PIS data layers into a context.

        On failure, returns a degraded context (pis_data=None) with the
        error logged to stderr.  Agents can check self_check() and decide
        whether to proceed or halt.
        """
        root = root or _palette_root
        data = None
        integrity = None
        graph = None

        try:
            data = load_all(root)
        except Exception as exc:
            print(f"[PaletteContext] PIS load failed: {exc}", file=sys.stderr)

        if data is not None:
            integrity = IntegrityGate(data)

        try:
            graph = GraphQuery.from_yaml(root)
        except Exception as exc:
            print(f"[PaletteContext] Graph load failed: {exc}", file=sys.stderr)

        return cls(
            pis_data=data,
            integrity_gate=integrity,
            graph_query=graph,
            palette_root=root,
            loaded_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        )


@dataclass
class HandoffPacket:
    """Structured input to any Palette agent."""

    schema_version: str = "handoffpacket.v2"
    from_agent: str = ""
    to_agent: str = ""
    task: str = ""
    riu_ids: list[str] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    constraints: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)


@dataclass
class HandoffResult:
    """Structured output from any Palette agent."""

    schema_version: str = "handoffresult.v1"
    from_agent: str = ""
    status: str = "success"  # success | failure | blocked
    outputs: dict[str, Any] = field(default_factory=dict)
    artifacts: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    validation_warnings: list[str] = field(default_factory=list)
    next_agent: str = ""


class AgentBase:
    """Base class for all Palette agents.

    Provides the machine enablement interface: query, traverse, validate,
    and graph-query the Palette Intelligence System.

    Subclass and implement execute():

        class MyResearcher(AgentBase):
            agent_name = "researcher"

            def execute(self, packet: HandoffPacket) -> HandoffResult:
                # Your agent logic here
                pis = self.query_pis("RIU-082")
                return HandoffResult(
                    from_agent=self.agent_name,
                    outputs={"recommendation": pis.recommendation},
                )
    """

    agent_name: str = "unknown"

    def __init__(self, context: PaletteContext | None = None):
        self.ctx = context or PaletteContext.load()

    # ── Stage 1: Foundations — "Here's what exists" ─────────────────────

    @property
    def pis_data(self):
        """Direct access to all loaded PIS data (taxonomy, knowledge,
        routing, signals, classification)."""
        return self.ctx.pis_data

    # ── Stage 2: First Instructions — "Here's how to ask" ──────────────

    def query_pis(self, riu_id: str = None, lib_id: str = None):
        """Traverse the PIS for a given RIU or knowledge library entry.

        Returns a TraversalResult with recommendation, alternatives,
        knowledge support, signal validation, completeness score, and gaps.
        """
        return traverse(self.ctx.pis_data, riu_id=riu_id, lib_id=lib_id)

    # ── Stage 3: Memory — "Here's how to carry context" ────────────────

    def read_packet(self) -> HandoffPacket:
        """Read a HandoffPacket from stdin (standard agent protocol)."""
        raw = sys.stdin.read().strip()
        if not raw:
            return HandoffPacket()
        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, ValueError) as exc:
            print(f"[{self.agent_name}] Malformed packet JSON: {exc}", file=sys.stderr)
            return HandoffPacket()
        return HandoffPacket(**{
            k: v for k, v in data.items()
            if k in HandoffPacket.__dataclass_fields__
        })

    def emit_result(self, result: HandoffResult) -> None:
        """Write a HandoffResult to stdout (standard agent protocol)."""
        # Auto-validate before emitting
        warnings = self.validate_output(result)
        result.validation_warnings = warnings
        try:
            json.dump(asdict(result), sys.stdout, indent=2, default=str)
        except (TypeError, ValueError) as exc:
            # Fallback: emit a failure result describing the serialization error
            fallback = HandoffResult(
                from_agent=getattr(result, "from_agent", self.agent_name),
                status="failure",
                gaps=[f"Output serialization failed: {exc}"],
            )
            json.dump(asdict(fallback), sys.stdout, indent=2)
        sys.stdout.write("\n")
        sys.stdout.flush()

    # ── Stage 4: Verification — "Here's how to check your work" ────────

    def validate_output(self, result: HandoffResult) -> list[str]:
        """Run integrity checks against a result before emitting it.

        Returns a list of warnings (empty = clean).
        """
        if self.ctx.integrity_gate is None:
            return []
        return self.ctx.integrity_gate.check_result(result)

    # ── Stage 5: Organization — "Here's how it connects" ───────────────

    def query_graph(
        self,
        subject: str | None = None,
        predicate: str | None = None,
        object: str | None = None,
    ) -> list[dict]:
        """Query the relationship graph by any combination of S/P/O.

        Examples:
            self.query_graph(subject="Architect", predicate="handles_riu")
            self.query_graph(predicate="recommends", object="OpenRouter")
            self.query_graph(subject="RIU-082")
        """
        if self.ctx.graph_query is None:
            return []
        return self.ctx.graph_query.query(
            subject=subject, predicate=predicate, object=object,
        )

    # ── Stage 6: Building — "Here's how to create" ─────────────────────

    def execute(self, packet: HandoffPacket) -> HandoffResult:
        """Override this method with your agent's logic.

        This is the only method a new agent needs to implement.
        Everything else (loading, querying, validating, emitting)
        is handled by the base class.
        """
        raise NotImplementedError(
            f"{self.agent_name} must implement execute()"
        )

    # ── Stage 7: Autonomy — "Here's how to be independent" ─────────────

    def self_check(self) -> dict:
        """Run a health check on the agent's connection to PIS.

        Returns a dict with status and any issues found.
        """
        issues = []

        if self.ctx.pis_data is None:
            issues.append("PIS data not loaded")

        if self.ctx.integrity_gate is None:
            issues.append("Integrity gate not available")

        if self.ctx.graph_query is None:
            issues.append("Graph query not available")
        elif self.ctx.graph_query.quad_count == 0:
            issues.append("Relationship graph is empty")

        # Verify core data layers are populated
        data = self.ctx.pis_data
        if data:
            if not getattr(data, "knowledge", None):
                issues.append("Knowledge library not loaded")
            if not getattr(data, "routing", None):
                issues.append("Service routing not loaded")
            if not getattr(data, "classification", None):
                issues.append("RIU classification not loaded")

        return {
            "agent": self.agent_name,
            "status": "healthy" if not issues else "degraded",
            "issues": issues,
            "pis_loaded": self.ctx.loaded_at,
            "palette_root": self.ctx.palette_root,
        }

    # ── Main loop (stdin → execute → stdout) ───────────────────────────

    def run(self) -> None:
        """Standard entry point: read packet from stdin, execute, emit result."""
        packet = self.read_packet()
        try:
            result = self.execute(packet)
            self.emit_result(result)
        except Exception as e:
            self.emit_result(HandoffResult(
                from_agent=self.agent_name,
                status="failure",
                gaps=[f"Agent error: {e}"],
            ))
