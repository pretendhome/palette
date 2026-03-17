"""Golden-path wire contract tests — V2.2 protocol defense.

These tests prove the canonical wire contract survives a real round trip:
  orchestrator packet (JSON) → Python SDK agent (stdin→execute→stdout) → canonical result (JSON)

Design rationale (learned from V2.2 migration):
  - Assert EXACT field sets, not just presence of expected fields.
    The _validation_warnings leak (caught by Codex) survived 58 tests because
    no test asserted "only these fields, nothing else."
  - Exercise real stdin→stdout, not just class construction.
    The researcher's legacy error path emitted status="error" and timestamp
    for months because tests only tested SDK classes, never the actual I/O.
  - Test backward compat on input, strictness on output.
    The migration policy is: accept old field names, always emit canonical.
    This must be continuously defended.
  - Test failure paths, not just happy paths.
    Exception handling in run() was the last seam to stabilize.
"""

from __future__ import annotations

import io
import json
import unittest
from unittest.mock import patch

from palette.sdk.agent_base import AgentBase, HandoffPacket, HandoffResult

# ── Canonical field sets (from core/schema/*.json, additionalProperties: false)

PACKET_FIELDS = {"id", "from", "to", "task", "riu_ids", "payload", "trace_id"}
RESULT_FIELDS = {"packet_id", "from", "status", "output", "blockers", "artifacts", "next_agent"}
STATUS_ENUM = {"success", "failure", "blocked"}


# ── Minimal test agents ──────────────────────────────────────────────────────

class EchoAgent(AgentBase):
    """Returns packet task in output. Happy path."""
    agent_name = "echo"

    def execute(self, packet):
        return HandoffResult(
            from_=self.agent_name,
            status="success",
            output={"echoed": packet.task, "riu_count": len(packet.riu_ids)},
        )


class BlockedAgent(AgentBase):
    """Always returns blocked with blockers."""
    agent_name = "blocked"

    def execute(self, packet):
        return HandoffResult(
            from_=self.agent_name,
            status="blocked",
            blockers=["waiting on human approval", "external API unavailable"],
        )


class CrashingAgent(AgentBase):
    """Raises an exception during execute."""
    agent_name = "crasher"

    def execute(self, packet):
        raise RuntimeError("database connection lost")


# ── Helpers ───────────────────────────────────────────────────────────────────

def _make_context():
    """Minimal PaletteContext stub — no PIS, no gate, no graph."""
    from palette.sdk.agent_base import PaletteContext
    return PaletteContext(pis_data=None, integrity_gate=None, graph_query=None)


def _run_agent(agent, packet_json: str) -> dict:
    """Feed packet JSON through agent.run(), return parsed result."""
    stdout_buf = io.StringIO()
    with patch("sys.stdin", io.StringIO(packet_json)), \
         patch("sys.stdout", stdout_buf):
        agent.run()
    return json.loads(stdout_buf.getvalue())


def _canonical_packet(**overrides) -> str:
    """Build a canonical packet JSON as the Go orchestrator would."""
    pkt = {
        "id": "pkt-golden-001",
        "from": "orchestrator",
        "to": "echo",
        "task": "evaluate guardrails for Bedrock deployment",
        "riu_ids": ["RIU-082", "RIU-045"],
        "payload": {
            "decision_context": "choosing between Bedrock and SageMaker",
            "constraints": ["stay within scope", "report blockers"],
        },
        "trace_id": "trace-golden-001",
    }
    pkt.update(overrides)
    return json.dumps(pkt)


# ── Tests ─────────────────────────────────────────────────────────────────────

class TestGoldenPathHappy(unittest.TestCase):
    """Canonical packet → SDK agent → canonical result."""

    def test_result_has_exactly_canonical_fields(self):
        """Wire output must have EXACTLY the 7 result fields. Nothing more."""
        agent = EchoAgent(context=_make_context())
        wire = _run_agent(agent, _canonical_packet())
        self.assertEqual(set(wire.keys()), RESULT_FIELDS,
                         f"Extra or missing fields: {set(wire.keys()) ^ RESULT_FIELDS}")

    def test_packet_id_links_back(self):
        """result.packet_id must equal the packet.id that was sent in."""
        agent = EchoAgent(context=_make_context())
        wire = _run_agent(agent, _canonical_packet(id="pkt-link-test"))
        self.assertEqual(wire["packet_id"], "pkt-link-test")

    def test_status_in_closed_enum(self):
        """Status must be one of success|failure|blocked."""
        agent = EchoAgent(context=_make_context())
        wire = _run_agent(agent, _canonical_packet())
        self.assertIn(wire["status"], STATUS_ENUM)

    def test_payload_fields_accessible(self):
        """Agent can read payload fields from canonical packet."""
        agent = EchoAgent(context=_make_context())
        wire = _run_agent(agent, _canonical_packet(
            task="test payload access",
            riu_ids=["RIU-001", "RIU-002", "RIU-003"],
        ))
        self.assertEqual(wire["output"]["echoed"], "test payload access")
        self.assertEqual(wire["output"]["riu_count"], 3)


class TestGoldenPathFailure(unittest.TestCase):
    """Exception in execute → canonical failure result."""

    def test_exception_produces_canonical_result(self):
        """Even when execute() crashes, wire output is exactly 7 canonical fields."""
        agent = CrashingAgent(context=_make_context())
        wire = _run_agent(agent, _canonical_packet())
        self.assertEqual(set(wire.keys()), RESULT_FIELDS,
                         f"Failure path leaked extra fields: {set(wire.keys()) - RESULT_FIELDS}")

    def test_exception_status_is_failure(self):
        agent = CrashingAgent(context=_make_context())
        wire = _run_agent(agent, _canonical_packet())
        self.assertEqual(wire["status"], "failure")

    def test_exception_populates_blockers(self):
        agent = CrashingAgent(context=_make_context())
        wire = _run_agent(agent, _canonical_packet())
        self.assertTrue(len(wire["blockers"]) > 0)
        self.assertIn("database connection lost", wire["blockers"][0])

    def test_exception_preserves_packet_id(self):
        """packet_id must survive even when execute() throws."""
        agent = CrashingAgent(context=_make_context())
        wire = _run_agent(agent, _canonical_packet(id="pkt-crash-test"))
        self.assertEqual(wire["packet_id"], "pkt-crash-test")


class TestGoldenPathBlocked(unittest.TestCase):
    """Blocked status path stays canonical."""

    def test_blocked_has_canonical_fields(self):
        agent = BlockedAgent(context=_make_context())
        wire = _run_agent(agent, _canonical_packet())
        self.assertEqual(set(wire.keys()), RESULT_FIELDS)

    def test_blocked_status_and_blockers(self):
        agent = BlockedAgent(context=_make_context())
        wire = _run_agent(agent, _canonical_packet())
        self.assertEqual(wire["status"], "blocked")
        self.assertEqual(len(wire["blockers"]), 2)


class TestGoldenPathBackwardCompat(unittest.TestCase):
    """Old-format packet in → canonical result out.

    Proves the migration policy: liberal in what you accept, strict in what you emit.
    This is the test that would have caught the researcher's packet.context breakage.
    """

    def test_legacy_packet_accepted_canonical_result_emitted(self):
        """Send a packet with old field names (context, from_agent). Get canonical result."""
        legacy_packet = json.dumps({
            "id": "pkt-legacy-001",
            "from_agent": "orchestrator",
            "to_agent": "echo",
            "task": "legacy format test",
            "riu_ids": ["RIU-001"],
            "context": {"decision_context": "testing backward compat"},
        })
        agent = EchoAgent(context=_make_context())
        wire = _run_agent(agent, legacy_packet)

        # Output must be strictly canonical — no old field names leak out
        self.assertEqual(set(wire.keys()), RESULT_FIELDS,
                         "Legacy input must not cause legacy output")
        self.assertNotIn("from_agent", wire)
        self.assertNotIn("outputs", wire)
        self.assertNotIn("gaps", wire)
        self.assertNotIn("timestamp", wire)
        self.assertNotIn("_validation_warnings", wire)

    def test_legacy_packet_task_still_readable(self):
        """Agent can still read task from a legacy-format packet."""
        legacy_packet = json.dumps({
            "task": "can you read this",
            "context": {"depth": "deep"},
        })
        agent = EchoAgent(context=_make_context())
        wire = _run_agent(agent, legacy_packet)
        self.assertEqual(wire["output"]["echoed"], "can you read this")


class TestGoldenPathNoLeaks(unittest.TestCase):
    """Regression guards for specific fields that leaked in the past."""

    def test_no_validation_warnings_on_wire(self):
        """_validation_warnings must never appear on wire output.
        This was the exact bug Codex caught — it leaked as a top-level field
        from emit_result() and violated additionalProperties: false.
        """
        agent = EchoAgent(context=_make_context())
        wire = _run_agent(agent, _canonical_packet())
        self.assertNotIn("_validation_warnings", wire)
        self.assertNotIn("validation_warnings", wire)

    def test_no_timestamp_on_wire(self):
        """timestamp was removed from the wire contract in V2.2."""
        agent = EchoAgent(context=_make_context())
        wire = _run_agent(agent, _canonical_packet())
        self.assertNotIn("timestamp", wire)

    def test_no_schema_version_on_wire(self):
        """schema_version was removed from the wire contract in V2.2."""
        agent = EchoAgent(context=_make_context())
        wire = _run_agent(agent, _canonical_packet())
        self.assertNotIn("schema_version", wire)

    def test_no_constraints_on_wire(self):
        """constraints moved into payload in V2.2."""
        agent = EchoAgent(context=_make_context())
        wire = _run_agent(agent, _canonical_packet())
        self.assertNotIn("constraints", wire)

    def test_no_produced_artifacts_on_wire(self):
        """produced_artifacts was renamed to artifacts in V2.2."""
        agent = EchoAgent(context=_make_context())
        wire = _run_agent(agent, _canonical_packet())
        self.assertNotIn("produced_artifacts", wire)


if __name__ == "__main__":
    unittest.main()
