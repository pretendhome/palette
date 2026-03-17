"""Tests for palette.sdk.agent_base — V2.2 wire contract."""

from __future__ import annotations

import io
import json
import sys
import unittest
from unittest.mock import patch

import os
_palette_root = os.path.join(os.path.expanduser("~"), "fde", "palette")
_palette_parent = os.path.dirname(_palette_root)
if _palette_root not in sys.path:
    sys.path.insert(0, _palette_root)
if _palette_parent not in sys.path:
    sys.path.insert(0, _palette_parent)

from palette.sdk.agent_base import (
    AgentBase, HandoffPacket, HandoffResult, PaletteContext,
)
from palette.sdk.integrity_gate import IntegrityGate
from palette.sdk.graph_query import GraphQuery


# ── Minimal fixtures ──────────────────────────────────────────────────

class FakePISData:
    def __init__(self, knowledge=None, routing=None, classification=None,
                 recipes=None, signals=None):
        self.knowledge = knowledge or {"LIB-001": {"id": "LIB-001"}}
        self.routing = routing or {"RIU-082": {"riu_id": "RIU-082"}}
        self.classification = classification or {"RIU-082": {"riu_id": "RIU-082"}}
        self.recipes = recipes or {"bedrock-guardrails": {}}
        self.signals = signals or [{"signal": "test"}]

_UNSET = object()

def _make_context(pis_data=_UNSET, graph_quads=_UNSET) -> PaletteContext:
    data = FakePISData() if pis_data is _UNSET else pis_data
    gate = IntegrityGate(data) if data is not None else None
    gq = GraphQuery(graph_quads) if graph_quads is not _UNSET and graph_quads is not None else None
    return PaletteContext(
        pis_data=data, integrity_gate=gate, graph_query=gq,
        palette_root="/tmp/test-palette",
        loaded_at="2026-01-01T00:00:00+00:00",
    )


# ── PaletteContext ────────────────────────────────────────────────────

class TestPaletteContext(unittest.TestCase):
    def test_load_returns_context(self):
        ctx = PaletteContext.load(_palette_root)
        self.assertIsNotNone(ctx.pis_data)
        self.assertIsNotNone(ctx.integrity_gate)
        self.assertIsNotNone(ctx.graph_query)
        self.assertTrue(ctx.loaded_at)

    def test_load_bad_root_returns_degraded(self):
        ctx = PaletteContext.load("/tmp/nonexistent-palette-root")
        self.assertIsNone(ctx.pis_data)
        self.assertTrue(ctx.loaded_at)


# ── HandoffPacket ─────────────────────────────────────────────────────

class TestHandoffPacket(unittest.TestCase):
    def test_defaults(self):
        p = HandoffPacket()
        self.assertTrue(p.id)  # auto-generated UUID
        self.assertEqual(p.from_, "")
        self.assertEqual(p.task, "")
        self.assertEqual(p.riu_ids, [])
        self.assertEqual(p.payload, {})
        self.assertEqual(p.trace_id, "")

    def test_wire_round_trip(self):
        p = HandoffPacket(
            from_="resolver", to="researcher", task="evaluate guardrails",
            riu_ids=["RIU-082"], payload={"confidence": 0.9}, trace_id="t-001",
        )
        wire = p.to_wire()
        self.assertEqual(wire["from"], "resolver")
        self.assertNotIn("from_", wire)
        p2 = HandoffPacket.from_wire(wire)
        self.assertEqual(p2.from_, "resolver")
        self.assertEqual(p2.task, "evaluate guardrails")
        self.assertEqual(p2.payload, {"confidence": 0.9})

    def test_json_round_trip(self):
        p = HandoffPacket(from_="a", to="b", task="test")
        serialized = json.dumps(p.to_wire())
        deserialized = json.loads(serialized)
        p2 = HandoffPacket.from_wire(deserialized)
        self.assertEqual(p2.from_, "a")
        self.assertEqual(p2.task, "test")

    def test_from_wire_backward_compat(self):
        """Old-format packets with 'context' instead of 'payload' still work."""
        old_wire = {"from": "x", "to": "y", "task": "z", "context": {"key": "val"}}
        p = HandoffPacket.from_wire(old_wire)
        self.assertEqual(p.payload, {"key": "val"})

    def test_none_coercion(self):
        p = HandoffPacket(riu_ids=None, payload=None)
        self.assertEqual(p.riu_ids, [])
        self.assertEqual(p.payload, {})

    def test_id_auto_generated(self):
        p1 = HandoffPacket()
        p2 = HandoffPacket()
        self.assertNotEqual(p1.id, p2.id)


# ── HandoffResult ─────────────────────────────────────────────────────

class TestHandoffResult(unittest.TestCase):
    def test_defaults(self):
        r = HandoffResult()
        self.assertEqual(r.status, "success")
        self.assertEqual(r.blockers, [])
        self.assertEqual(r.output, {})

    def test_wire_round_trip(self):
        r = HandoffResult(
            packet_id="pkt-001", from_="researcher", status="success",
            output={"recommendation": "use Bedrock"},
            blockers=[], artifacts=["plan.md"], next_agent="architect",
        )
        wire = r.to_wire()
        self.assertEqual(wire["from"], "researcher")
        self.assertEqual(wire["packet_id"], "pkt-001")
        self.assertNotIn("from_", wire)
        r2 = HandoffResult.from_wire(wire)
        self.assertEqual(r2.from_, "researcher")
        self.assertEqual(r2.packet_id, "pkt-001")

    def test_from_wire_backward_compat(self):
        """Old-format results with 'outputs'/'gaps' still work."""
        old_wire = {"from": "x", "outputs": {"key": "val"}, "gaps": ["gap1"]}
        r = HandoffResult.from_wire(old_wire)
        self.assertEqual(r.output, {"key": "val"})
        self.assertEqual(r.blockers, ["gap1"])

    def test_packet_id_links_to_packet(self):
        """Invariant #1: result.packet_id == packet.id"""
        p = HandoffPacket(from_="resolver", task="test")
        r = HandoffResult(packet_id=p.id, from_="researcher")
        self.assertEqual(r.packet_id, p.id)


# ── AgentBase ─────────────────────────────────────────────────────────

class TestAgentBase(unittest.TestCase):
    def test_self_check_healthy(self):
        ctx = _make_context(graph_quads=[{"subject": "A", "predicate": "p", "object": "B"}])
        agent = AgentBase(context=ctx)
        status = agent.self_check()
        self.assertEqual(status["status"], "healthy")

    def test_self_check_degraded_no_pis(self):
        ctx = _make_context(pis_data=None)
        agent = AgentBase(context=ctx)
        status = agent.self_check()
        self.assertEqual(status["status"], "degraded")
        self.assertIn("PIS data not loaded", status["issues"])

    def test_self_check_degraded_empty_graph(self):
        ctx = _make_context(graph_quads=[])
        agent = AgentBase(context=ctx)
        self.assertIn("Relationship graph is empty", agent.self_check()["issues"])

    def test_execute_raises_not_implemented(self):
        agent = AgentBase(context=_make_context())
        with self.assertRaises(NotImplementedError):
            agent.execute(HandoffPacket())

    def test_subclass_execute(self):
        class TestAgent(AgentBase):
            agent_name = "test"
            def execute(self, packet):
                return HandoffResult(packet_id=packet.id, from_=self.agent_name, output={"ok": True})

        agent = TestAgent(context=_make_context())
        result = agent.execute(HandoffPacket(task="test"))
        self.assertEqual(result.from_, "test")
        self.assertTrue(result.output["ok"])

    def test_validate_output_no_gate(self):
        agent = AgentBase(context=PaletteContext())
        self.assertEqual(agent.validate_output(HandoffResult()), [])

    def test_validate_output_with_valid_result(self):
        agent = AgentBase(context=_make_context())
        result = HandoffResult(from_="test", output={"note": "no refs"})
        self.assertEqual(agent.validate_output(result), [])

    def test_read_packet_from_stdin(self):
        wire = json.dumps({"from": "resolver", "to": "researcher", "task": "check guardrails"})
        agent = AgentBase(context=_make_context())
        with patch("sys.stdin", io.StringIO(wire)):
            packet = agent.read_packet()
        self.assertEqual(packet.from_, "resolver")
        self.assertEqual(packet.task, "check guardrails")

    def test_read_packet_empty_stdin(self):
        agent = AgentBase(context=_make_context())
        with patch("sys.stdin", io.StringIO("")):
            packet = agent.read_packet()
        self.assertEqual(packet.task, "")

    def test_read_packet_malformed_json(self):
        agent = AgentBase(context=_make_context())
        stderr_buf = io.StringIO()
        with patch("sys.stdin", io.StringIO("not json")), patch("sys.stderr", stderr_buf):
            packet = agent.read_packet()
        self.assertEqual(packet.task, "")
        self.assertIn("Malformed", stderr_buf.getvalue())

    def test_emit_result_writes_canonical_wire(self):
        agent = AgentBase(context=_make_context())
        result = HandoffResult(packet_id="pkt-1", from_="test", output={"key": "val"})
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            agent.emit_result(result)
        wire = json.loads(buf.getvalue())
        self.assertEqual(wire["from"], "test")
        self.assertEqual(wire["packet_id"], "pkt-1")
        self.assertEqual(wire["output"]["key"], "val")
        self.assertNotIn("from_", wire)
        self.assertNotIn("outputs", wire)
        self.assertNotIn("gaps", wire)

    def test_emit_result_non_serializable(self):
        agent = AgentBase(context=_make_context())
        result = HandoffResult(from_="test", output={"func": lambda x: x})
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            agent.emit_result(result)
        wire = json.loads(buf.getvalue())
        # default=str gracefully degrades the lambda
        self.assertEqual(wire["from"], "test")

    def test_run_stdin_to_stdout(self):
        class Echo(AgentBase):
            agent_name = "echo"
            def execute(self, packet):
                return HandoffResult(packet_id=packet.id, from_="echo", output={"echoed": packet.task})

        agent = Echo(context=_make_context())
        stdin_data = json.dumps({"task": "hello"})
        stdout_buf = io.StringIO()
        with patch("sys.stdin", io.StringIO(stdin_data)), patch("sys.stdout", stdout_buf):
            agent.run()
        wire = json.loads(stdout_buf.getvalue())
        self.assertEqual(wire["from"], "echo")
        self.assertEqual(wire["output"]["echoed"], "hello")
        self.assertTrue(wire["packet_id"])  # auto-linked

    def test_run_catches_execute_exception(self):
        class Failing(AgentBase):
            agent_name = "failing"
            def execute(self, packet):
                raise ValueError("intentional test failure")

        agent = Failing(context=_make_context())
        stdout_buf = io.StringIO()
        with patch("sys.stdin", io.StringIO("{}")), patch("sys.stdout", stdout_buf):
            agent.run()
        wire = json.loads(stdout_buf.getvalue())
        self.assertEqual(wire["status"], "failure")
        self.assertIn("intentional test failure", wire["blockers"][0])

    def test_run_auto_links_packet_id(self):
        """Invariant #1: result.packet_id is auto-set from packet.id if not provided."""
        class Minimal(AgentBase):
            agent_name = "minimal"
            def execute(self, packet):
                return HandoffResult(from_="minimal", output={"done": True})

        agent = Minimal(context=_make_context())
        pkt = {"id": "my-packet-id", "task": "test"}
        stdout_buf = io.StringIO()
        with patch("sys.stdin", io.StringIO(json.dumps(pkt))), patch("sys.stdout", stdout_buf):
            agent.run()
        wire = json.loads(stdout_buf.getvalue())
        self.assertEqual(wire["packet_id"], "my-packet-id")


# ── Integration ───────────────────────────────────────────────────────

class TestIntegration(unittest.TestCase):
    def test_full_load_and_query(self):
        ctx = PaletteContext.load(_palette_root)
        agent = AgentBase(context=ctx)
        check = agent.self_check()
        self.assertEqual(check["status"], "healthy")
        result = agent.query_pis(riu_id="RIU-082")
        self.assertIsNotNone(result)
        quads = agent.query_graph(subject="RIU-082")
        self.assertIsInstance(quads, list)

    def test_public_import_path(self):
        """Golden-path: the documented import works."""
        from palette.sdk import AgentBase, HandoffPacket, HandoffResult, PaletteContext
        self.assertTrue(callable(AgentBase))
        self.assertTrue(callable(HandoffPacket))
        self.assertTrue(callable(HandoffResult))
        self.assertTrue(callable(PaletteContext))


if __name__ == "__main__":
    unittest.main()
