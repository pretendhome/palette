"""Tests for palette.sdk.agent_base — PaletteContext, HandoffPacket, HandoffResult, AgentBase."""

from __future__ import annotations

import io
import json
import sys
import unittest
from dataclasses import asdict
from unittest.mock import patch

# Ensure palette package is importable
import os

_palette_root = os.path.join(os.path.expanduser("~"), "fde", "palette")
_palette_parent = os.path.dirname(_palette_root)
if _palette_root not in sys.path:
    sys.path.insert(0, _palette_root)
if _palette_parent not in sys.path:
    sys.path.insert(0, _palette_parent)

from palette.sdk.agent_base import (
    AgentBase,
    HandoffPacket,
    HandoffResult,
    PaletteContext,
)
from palette.sdk.integrity_gate import IntegrityGate
from palette.sdk.graph_query import GraphQuery


# ── Minimal fixtures ──────────────────────────────────────────────────

_UNSET = object()


class FakePISData:
    """Minimal stand-in for PISData with the attrs AgentBase.self_check expects."""
    def __init__(self, knowledge=_UNSET, routing=_UNSET, classification=_UNSET, recipes=_UNSET, signals=_UNSET):
        self.knowledge = {"LIB-001": {"id": "LIB-001"}} if knowledge is _UNSET else knowledge
        self.routing = {"RIU-082": {"riu_id": "RIU-082"}} if routing is _UNSET else routing
        self.classification = {"RIU-082": {"riu_id": "RIU-082", "classification": "both"}} if classification is _UNSET else classification
        self.recipes = {"example": {"service_name": "Example"}} if recipes is _UNSET else recipes
        self.signals = [{"tool": "Example", "signal_tier": "watch"}] if signals is _UNSET else signals


def _make_context(pis_data=_UNSET, graph_quads=_UNSET) -> PaletteContext:
    data = FakePISData() if pis_data is _UNSET else pis_data
    gate = IntegrityGate(data) if data is not None else None
    gq = GraphQuery(graph_quads) if graph_quads is not _UNSET and graph_quads is not None else None
    return PaletteContext(
        pis_data=data,
        integrity_gate=gate,
        graph_query=gq,
        palette_root="/tmp/test-palette",
        loaded_at="2026-01-01T00:00:00+00:00",
    )


# ── PaletteContext tests ──────────────────────────────────────────────

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
        self.assertIsNone(ctx.integrity_gate)
        # Graph also None (no YAML found)
        self.assertIsNone(ctx.graph_query)
        # But it doesn't crash — loaded_at is still set
        self.assertTrue(ctx.loaded_at)


# ── HandoffPacket tests ───────────────────────────────────────────────

class TestHandoffPacket(unittest.TestCase):

    def test_defaults(self):
        p = HandoffPacket()
        self.assertEqual(p.schema_version, "handoffpacket.v2")
        self.assertEqual(p.from_agent, "")
        self.assertEqual(p.task, "")
        self.assertEqual(p.riu_ids, [])

    def test_round_trip(self):
        p = HandoffPacket(
            from_agent="resolver",
            to_agent="researcher",
            task="evaluate guardrails",
            riu_ids=["RIU-082"],
            context={"confidence": 0.9},
            constraints=["no-api-calls"],
            artifacts=["plan.md"],
        )
        d = asdict(p)
        p2 = HandoffPacket(**d)
        self.assertEqual(asdict(p), asdict(p2))

    def test_json_round_trip(self):
        p = HandoffPacket(from_agent="a", to_agent="b", task="test")
        serialized = json.dumps(asdict(p))
        deserialized = json.loads(serialized)
        p2 = HandoffPacket(**deserialized)
        self.assertEqual(p.from_agent, p2.from_agent)
        self.assertEqual(p.task, p2.task)

    def test_extra_fields_ignored_on_construction(self):
        data = {"from_agent": "x", "to_agent": "y", "task": "z", "unknown_field": 123}
        filtered = {k: v for k, v in data.items() if k in HandoffPacket.__dataclass_fields__}
        p = HandoffPacket(**filtered)
        self.assertEqual(p.from_agent, "x")

    def test_none_coerced_to_empty_list(self):
        """Finding 3: HandoffPacket(riu_ids=None) should coerce to []."""
        p = HandoffPacket(riu_ids=None, constraints=None, artifacts=None, context=None)
        self.assertEqual(p.riu_ids, [])
        self.assertEqual(p.constraints, [])
        self.assertEqual(p.artifacts, [])
        self.assertEqual(p.context, {})
        # Should be safe to iterate
        self.assertEqual(len(p.riu_ids), 0)
        for _ in p.constraints:
            pass  # no crash


# ── HandoffResult tests ──────────────────────────────────────────────

class TestHandoffResult(unittest.TestCase):

    def test_defaults(self):
        r = HandoffResult()
        self.assertEqual(r.status, "success")
        self.assertEqual(r.gaps, [])
        self.assertEqual(r.validation_warnings, [])

    def test_round_trip(self):
        r = HandoffResult(
            from_agent="researcher",
            status="success",
            outputs={"recommendation": "use Bedrock"},
            gaps=["pricing uncertain"],
            next_agent="architect",
        )
        d = asdict(r)
        r2 = HandoffResult(**d)
        self.assertEqual(asdict(r), asdict(r2))


# ── AgentBase tests ───────────────────────────────────────────────────

class TestAgentBase(unittest.TestCase):

    def test_self_check_healthy(self):
        ctx = _make_context(
            graph_quads=[{"subject": "A", "predicate": "p", "object": "B"}],
        )
        agent = AgentBase(context=ctx)
        status = agent.self_check()
        self.assertEqual(status["status"], "healthy")
        self.assertEqual(status["issues"], [])

    def test_self_check_degraded_no_pis(self):
        ctx = _make_context(pis_data=None)
        agent = AgentBase(context=ctx)
        status = agent.self_check()
        self.assertEqual(status["status"], "degraded")
        self.assertIn("PIS data not loaded", status["issues"])

    def test_self_check_degraded_empty_graph(self):
        ctx = _make_context(graph_quads=[])
        agent = AgentBase(context=ctx)
        status = agent.self_check()
        self.assertIn("Relationship graph is empty", status["issues"])

    def test_self_check_detects_missing_recipes_signals(self):
        """Finding 7: self_check should flag missing recipes and signals."""
        data = FakePISData(recipes={}, signals=[])
        ctx = _make_context(pis_data=data, graph_quads=[{"subject": "A", "predicate": "p", "object": "B"}])
        agent = AgentBase(context=ctx)
        status = agent.self_check()
        self.assertEqual(status["status"], "degraded")
        self.assertIn("Integration recipes not loaded", status["issues"])
        self.assertIn("Company signals not loaded", status["issues"])

    def test_execute_raises_not_implemented(self):
        ctx = _make_context()
        agent = AgentBase(context=ctx)
        with self.assertRaises(NotImplementedError):
            agent.execute(HandoffPacket())

    def test_subclass_execute(self):
        class TestAgent(AgentBase):
            agent_name = "test"
            def execute(self, packet):
                return HandoffResult(from_agent=self.agent_name, outputs={"ok": True})

        ctx = _make_context()
        agent = TestAgent(context=ctx)
        result = agent.execute(HandoffPacket(task="test"))
        self.assertEqual(result.from_agent, "test")
        self.assertTrue(result.outputs["ok"])

    def test_validate_output_with_valid_result(self):
        ctx = _make_context()
        agent = AgentBase(context=ctx)
        result = HandoffResult(from_agent="test", outputs={"note": "no refs"})
        warnings = agent.validate_output(result)
        self.assertEqual(warnings, [])

    def test_validate_output_no_gate(self):
        ctx = PaletteContext()
        agent = AgentBase(context=ctx)
        warnings = agent.validate_output(HandoffResult())
        self.assertEqual(warnings, [])

    def test_read_packet_from_stdin(self):
        packet_data = json.dumps({
            "from_agent": "resolver",
            "to_agent": "researcher",
            "task": "check guardrails",
        })
        ctx = _make_context()
        agent = AgentBase(context=ctx)
        with patch("sys.stdin", io.StringIO(packet_data)):
            packet = agent.read_packet()
        self.assertEqual(packet.from_agent, "resolver")
        self.assertEqual(packet.task, "check guardrails")

    def test_read_packet_empty_stdin(self):
        ctx = _make_context()
        agent = AgentBase(context=ctx)
        with patch("sys.stdin", io.StringIO("")):
            packet = agent.read_packet()
        self.assertEqual(packet.task, "")

    def test_emit_result_writes_json(self):
        ctx = _make_context()
        agent = AgentBase(context=ctx)
        result = HandoffResult(from_agent="test", outputs={"key": "val"})
        buf = io.StringIO()
        with patch("sys.stdout", buf):
            agent.emit_result(result)
        output = json.loads(buf.getvalue())
        self.assertEqual(output["from_agent"], "test")
        self.assertEqual(output["outputs"]["key"], "val")

    def test_run_stdin_to_stdout(self):
        class Echo(AgentBase):
            agent_name = "echo"
            def execute(self, packet):
                return HandoffResult(from_agent="echo", outputs={"echoed": packet.task})

        ctx = _make_context()
        agent = Echo(context=ctx)
        stdin_data = json.dumps({"task": "hello"})
        stdout_buf = io.StringIO()
        with patch("sys.stdin", io.StringIO(stdin_data)), patch("sys.stdout", stdout_buf):
            agent.run()
        output = json.loads(stdout_buf.getvalue())
        self.assertEqual(output["from_agent"], "echo")
        self.assertEqual(output["outputs"]["echoed"], "hello")

    def test_run_catches_execute_exception(self):
        class Failing(AgentBase):
            agent_name = "failing"
            def execute(self, packet):
                raise ValueError("intentional test failure")

        ctx = _make_context()
        agent = Failing(context=ctx)
        stdout_buf = io.StringIO()
        with patch("sys.stdin", io.StringIO("{}")), patch("sys.stdout", stdout_buf):
            agent.run()
        output = json.loads(stdout_buf.getvalue())
        self.assertEqual(output["status"], "failure")
        self.assertIn("intentional test failure", output["gaps"][0])


# ── Integration: full load ────────────────────────────────────────────

class TestIntegration(unittest.TestCase):

    def test_full_load_and_query(self):
        ctx = PaletteContext.load(_palette_root)
        agent = AgentBase(context=ctx)
        check = agent.self_check()
        self.assertEqual(check["status"], "healthy")
        # Query PIS
        result = agent.query_pis(riu_id="RIU-082")
        self.assertIsNotNone(result)
        # Query graph
        quads = agent.query_graph(subject="RIU-082")
        self.assertIsInstance(quads, list)


if __name__ == "__main__":
    unittest.main()
