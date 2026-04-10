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

Wire contract (V2.2):

  Packet  →  Agent  →  Result

  Packet: id, from, to, task, riu_ids, payload, trace_id
  Result: packet_id, from, status, output, blockers, artifacts, next_agent

  Status is a closed enum: success | failure | blocked
  Result always references Packet: result.packet_id == packet.id
  If status != success, blockers explains why (glass-box).

  The protocol is 7 fields in, 7 fields out, linked by one ID.
  Everything domain-specific lives in payload and output.
  Everything runtime-specific is transport.
"""

from __future__ import annotations

import json
import sys
import os
import uuid
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
from palette.sdk.prompt_cache import (
    PromptBundle,
    PromptSection,
    build_prompt_bundle,
    packet_payload_to_section,
)


@dataclass
class PaletteContext:
    """Everything an agent needs to know about the system it's operating in."""

    pis_data: Any = None
    integrity_gate: IntegrityGate | None = None
    graph_query: GraphQuery | None = None
    palette_root: str = ""
    loaded_at: str = ""

    @classmethod
    def load(cls, root: str | None = None) -> PaletteContext:
        """Load all PIS data layers into a context.

        On failure, returns a degraded context (pis_data=None) with the
        error logged to stderr.
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


# ── Wire Contract: Packet ───────────────────────────────────────────
#
# Python reserves `from` as a keyword, so the internal field is `from_`.
# On the wire (JSON), it serializes as `from` via to_wire()/from_wire().

@dataclass
class HandoffPacket:
    """Structured input to any Palette agent.

    Wire fields: id, from, to, task, riu_ids, payload, trace_id
    """

    id: str = ""
    from_: str = ""
    to: str = ""
    task: str = ""
    riu_ids: list[str] = field(default_factory=list)
    payload: dict[str, Any] = field(default_factory=dict)
    trace_id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if self.riu_ids is None:
            self.riu_ids = []
        if self.payload is None:
            self.payload = {}

    def to_wire(self) -> dict:
        """Serialize to canonical wire format (from_ → from)."""
        return {
            "id": self.id,
            "from": self.from_,
            "to": self.to,
            "task": self.task,
            "riu_ids": self.riu_ids,
            "payload": self.payload,
            "trace_id": self.trace_id,
        }

    @classmethod
    def from_wire(cls, data: dict) -> HandoffPacket:
        """Deserialize from canonical wire format (from → from_)."""
        return cls(
            id=data.get("id", ""),
            from_=data.get("from", data.get("from_", "")),
            to=data.get("to", ""),
            task=data.get("task", ""),
            riu_ids=data.get("riu_ids", []),
            payload=data.get("payload", data.get("context", {})),
            trace_id=data.get("trace_id", ""),
        )


# ── Wire Contract: Result ───────────────────────────────────────────

@dataclass
class HandoffResult:
    """Structured output from any Palette agent.

    Wire fields: packet_id, from, status, output, blockers, artifacts, next_agent
    Status: success | failure | blocked
    """

    packet_id: str = ""
    from_: str = ""
    status: str = "success"
    output: dict[str, Any] = field(default_factory=dict)
    blockers: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    next_agent: str = ""

    def __post_init__(self):
        if self.output is None:
            self.output = {}
        if self.blockers is None:
            self.blockers = []
        if self.artifacts is None:
            self.artifacts = []

    def to_wire(self) -> dict:
        """Serialize to canonical wire format (from_ → from)."""
        return {
            "packet_id": self.packet_id,
            "from": self.from_,
            "status": self.status,
            "output": self.output,
            "blockers": self.blockers,
            "artifacts": self.artifacts,
            "next_agent": self.next_agent,
        }

    @classmethod
    def from_wire(cls, data: dict) -> HandoffResult:
        """Deserialize from canonical wire format (from → from_)."""
        return cls(
            packet_id=data.get("packet_id", ""),
            from_=data.get("from", data.get("from_", "")),
            status=data.get("status", "success"),
            output=data.get("output", data.get("outputs", {})),
            blockers=data.get("blockers", data.get("gaps", [])),
            artifacts=data.get("artifacts", []),
            next_agent=data.get("next_agent", ""),
        )


class AgentBase:
    """Base class for all Palette agents.

    Subclass and implement execute():

        class MyResearcher(AgentBase):
            agent_name = "researcher"

            def execute(self, packet: HandoffPacket) -> HandoffResult:
                pis = self.query_pis("RIU-082")
                return HandoffResult(
                    packet_id=packet.id,
                    from_=self.agent_name,
                    output={"recommendation": pis.recommendation},
                )
    """

    agent_name: str = "unknown"

    def __init__(self, context: PaletteContext | None = None):
        self.ctx = context or PaletteContext.load()

    # ── Stage 1: Foundations ────────────────────────────────────────────

    @property
    def pis_data(self):
        """Direct access to all loaded PIS data."""
        return self.ctx.pis_data

    # ── Stage 2: First Instructions ────────────────────────────────────

    def query_pis(self, riu_id: str = None, lib_id: str = None):
        """Traverse the PIS for a given RIU or knowledge library entry."""
        return traverse(self.ctx.pis_data, riu_id=riu_id, lib_id=lib_id)

    # ── Stage 3: Memory ────────────────────────────────────────────────

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
        return HandoffPacket.from_wire(data)

    def emit_result(self, result: HandoffResult) -> None:
        """Write a HandoffResult to stdout (standard agent protocol)."""
        warnings = self.validate_output(result)
        if warnings:
            print(f"[{self.agent_name}] validation: {warnings}", file=sys.stderr)
        try:
            wire = result.to_wire()
            json.dump(wire, sys.stdout, indent=2, default=str)
        except (TypeError, ValueError) as exc:
            fallback = HandoffResult(
                packet_id=getattr(result, "packet_id", ""),
                from_=self.agent_name,
                status="failure",
                blockers=[f"Output serialization failed: {exc}"],
            )
            json.dump(fallback.to_wire(), sys.stdout, indent=2)
        sys.stdout.write("\n")
        sys.stdout.flush()

    def build_prompt_bundle(
        self,
        packet: HandoffPacket,
        *,
        system_prompt: str = "",
        stable_sections: list[PromptSection] | None = None,
        volatile_sections: list[PromptSection] | None = None,
    ) -> PromptBundle:
        """Construct a cache-friendly prompt bundle.

        Stable material goes first and should change rarely:
        - agent identity
        - system prompt / operating instructions

        Volatile material goes last and can churn every turn:
        - task
        - RIU ids
        - payload
        - trace/session identifiers
        """

        base_stable = [
            PromptSection("Agent", self.agent_name),
            PromptSection("System Prompt", system_prompt),
        ]
        base_volatile = [
            PromptSection("Task", packet.task, cacheable=False),
            packet_payload_to_section("RIU IDs", packet.riu_ids, cacheable=False),
            packet_payload_to_section("Payload", packet.payload, cacheable=False),
            PromptSection("Trace ID", packet.trace_id, cacheable=False),
        ]

        return build_prompt_bundle(
            [*base_stable, *(stable_sections or [])],
            [*base_volatile, *(volatile_sections or [])],
        )

    # ── Stage 4: Verification ──────────────────────────────────────────

    def validate_output(self, result: HandoffResult) -> list[str]:
        """Run integrity checks against a result before emitting it."""
        if self.ctx.integrity_gate is None:
            return []
        return self.ctx.integrity_gate.check_result(result)

    # ── Stage 5: Organization ──────────────────────────────────────────

    def query_graph(
        self,
        subject: str | None = None,
        predicate: str | None = None,
        object: str | None = None,
    ) -> list[dict]:
        """Query the relationship graph by any combination of S/P/O."""
        if self.ctx.graph_query is None:
            return []
        return self.ctx.graph_query.query(
            subject=subject, predicate=predicate, object=object,
        )

    # ── Stage 6: Building ──────────────────────────────────────────────

    def execute(self, packet: HandoffPacket) -> HandoffResult:
        """Override this method with your agent's logic."""
        raise NotImplementedError(
            f"{self.agent_name} must implement execute()"
        )

    # ── Stage 7: Autonomy ──────────────────────────────────────────────

    def self_check(self) -> dict:
        """Run a health check on the agent's connection to PIS."""
        issues = []

        if self.ctx.pis_data is None:
            issues.append("PIS data not loaded")

        if self.ctx.integrity_gate is None:
            issues.append("Integrity gate not available")

        if self.ctx.graph_query is None:
            issues.append("Graph query not available")
        elif self.ctx.graph_query.quad_count == 0:
            issues.append("Relationship graph is empty")

        data = self.ctx.pis_data
        if data:
            if not getattr(data, "knowledge", None):
                issues.append("Knowledge library not loaded")
            if not getattr(data, "routing", None):
                issues.append("Service routing not loaded")
            if not getattr(data, "classification", None):
                issues.append("RIU classification not loaded")
            if not getattr(data, "recipes", None):
                issues.append("Integration recipes not loaded")
            if not getattr(data, "signals", None):
                issues.append("Company signals not loaded")

        return {
            "agent": self.agent_name,
            "status": "healthy" if not issues else "degraded",
            "issues": issues,
            "pis_loaded": self.ctx.loaded_at,
            "palette_root": self.ctx.palette_root,
        }

    # ── Main loop ──────────────────────────────────────────────────────

    def run(self) -> None:
        """Standard entry point: read packet from stdin, execute, emit result."""
        packet = self.read_packet()
        try:
            result = self.execute(packet)
            if not result.packet_id:
                result.packet_id = packet.id
            self.emit_result(result)
        except Exception as e:
            self.emit_result(HandoffResult(
                packet_id=packet.id,
                from_=self.agent_name,
                status="failure",
                blockers=[f"Agent error: {e}"],
            ))
