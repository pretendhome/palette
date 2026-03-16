"""Tests for palette.sdk.integrity_gate — IntegrityGate validation checks."""

from __future__ import annotations

import sys
import os
import unittest

_palette_root = os.path.join(os.path.expanduser("~"), "fde", "palette")
_palette_parent = os.path.dirname(_palette_root)
if _palette_root not in sys.path:
    sys.path.insert(0, _palette_root)
if _palette_parent not in sys.path:
    sys.path.insert(0, _palette_parent)

from palette.sdk.integrity_gate import IntegrityGate


# ── Minimal fixtures ──────────────────────────────────────────────────

class FakePISData:
    def __init__(self, classification=None, routing=None, knowledge=None):
        self.classification = classification or {}
        self.routing = routing or {}
        self.knowledge = knowledge or {}


class FakeResult:
    def __init__(self, outputs=None, status="success", gaps=None):
        self.outputs = outputs or {}
        self.status = status
        self.gaps = gaps or []


# ── None / empty data guards ─────────────────────────────────────────

class TestNoneGuards(unittest.TestCase):

    def test_none_data_returns_warning(self):
        gate = IntegrityGate(None)
        warnings = gate.check_result(FakeResult())
        self.assertEqual(len(warnings), 1)
        self.assertIn("PIS data is None", warnings[0])

    def test_none_result_returns_warning(self):
        gate = IntegrityGate(FakePISData())
        warnings = gate.check_result(None)
        self.assertEqual(len(warnings), 1)
        self.assertIn("result is None", warnings[0])

    def test_empty_data_clean(self):
        gate = IntegrityGate(FakePISData())
        warnings = gate.check_result(FakeResult())
        self.assertEqual(warnings, [])


# ── RIU reference checks ─────────────────────────────────────────────

class TestRIUReferences(unittest.TestCase):

    def test_valid_riu_no_warning(self):
        data = FakePISData(classification={"RIU-082": {"riu_id": "RIU-082"}})
        gate = IntegrityGate(data)
        result = FakeResult(outputs={"note": "See RIU-082 for guardrails"})
        self.assertEqual(gate.check_result(result), [])

    def test_invalid_riu_warns(self):
        data = FakePISData(classification={"RIU-082": {"riu_id": "RIU-082"}})
        gate = IntegrityGate(data)
        result = FakeResult(outputs={"note": "See RIU-999"})
        warnings = gate.check_result(result)
        self.assertTrue(any("RIU-999" in w for w in warnings))

    def test_nested_riu_extraction(self):
        data = FakePISData(classification={
            "RIU-001": {}, "RIU-002": {},
        })
        gate = IntegrityGate(data)
        result = FakeResult(outputs={
            "deep": {"nested": ["RIU-001", {"ref": "RIU-002 and RIU-999"}]}
        })
        warnings = gate.check_result(result)
        # RIU-001 and RIU-002 exist, RIU-999 doesn't
        self.assertTrue(any("RIU-999" in w for w in warnings))
        self.assertFalse(any("RIU-001" in w for w in warnings))
        self.assertFalse(any("RIU-002" in w for w in warnings))

    def test_no_classification_skips_check(self):
        data = FakePISData(classification={})
        gate = IntegrityGate(data)
        result = FakeResult(outputs={"note": "RIU-999"})
        self.assertEqual(gate.check_result(result), [])


# ── Knowledge reference checks ───────────────────────────────────────

class TestKnowledgeReferences(unittest.TestCase):

    def test_valid_lib_no_warning(self):
        data = FakePISData(knowledge={"LIB-042": {"id": "LIB-042"}})
        gate = IntegrityGate(data)
        result = FakeResult(outputs={"ref": "LIB-042"})
        self.assertEqual(gate.check_result(result), [])

    def test_invalid_lib_warns(self):
        data = FakePISData(knowledge={"LIB-042": {"id": "LIB-042"}})
        gate = IntegrityGate(data)
        result = FakeResult(outputs={"ref": "LIB-999"})
        warnings = gate.check_result(result)
        self.assertTrue(any("LIB-999" in w for w in warnings))


# ── Service reference checks ─────────────────────────────────────────

class TestServiceReferences(unittest.TestCase):

    def test_valid_service_no_warning(self):
        data = FakePISData(routing={
            "RIU-082": {"services": [{"name": "Bedrock Guardrails"}]}
        })
        gate = IntegrityGate(data)
        result = FakeResult(outputs={
            "riu_id": "RIU-082",
            "recommendation": {"service": "Bedrock Guardrails"},
        })
        self.assertEqual(gate.check_result(result), [])

    def test_invalid_service_warns(self):
        data = FakePISData(routing={
            "RIU-082": {"services": [{"name": "Bedrock Guardrails"}]}
        })
        gate = IntegrityGate(data)
        result = FakeResult(outputs={
            "riu_id": "RIU-082",
            "recommendation": {"service": "FakeService"},
        })
        warnings = gate.check_result(result)
        self.assertTrue(any("FakeService" in w for w in warnings))

    def test_no_routing_skips_check(self):
        data = FakePISData(routing={})
        gate = IntegrityGate(data)
        result = FakeResult(outputs={
            "riu_id": "RIU-082",
            "recommendation": {"service": "anything"},
        })
        self.assertEqual(gate.check_result(result), [])


# ── Gaps populated checks ────────────────────────────────────────────

class TestGapsPopulated(unittest.TestCase):

    def test_failure_without_gaps_warns(self):
        gate = IntegrityGate(FakePISData())
        result = FakeResult(status="failure", gaps=[])
        warnings = gate.check_result(result)
        self.assertTrue(any("failure" in w.lower() and "gaps" in w.lower() for w in warnings))

    def test_failure_with_gaps_clean(self):
        gate = IntegrityGate(FakePISData())
        result = FakeResult(status="failure", gaps=["something went wrong"])
        warnings = gate.check_result(result)
        self.assertFalse(any("failure" in w.lower() and "gaps" in w.lower() for w in warnings))

    def test_assumptions_without_gaps_warns(self):
        gate = IntegrityGate(FakePISData())
        result = FakeResult(outputs={"note": "ASSUMPTION: pricing is stable"}, gaps=[])
        warnings = gate.check_result(result)
        self.assertTrue(any("ASSUMPTION" in w for w in warnings))

    def test_assumptions_with_gaps_clean(self):
        gate = IntegrityGate(FakePISData())
        result = FakeResult(
            outputs={"note": "ASSUMPTION: pricing is stable"},
            gaps=["pricing may change"],
        )
        warnings = gate.check_result(result)
        self.assertFalse(any("ASSUMPTION" in w for w in warnings))


# ── Helper extraction tests ──────────────────────────────────────────

class TestHelpers(unittest.TestCase):

    def test_extract_riu_ids_from_string(self):
        collector = set()
        IntegrityGate._extract_riu_ids("RIU-001 and RIU-082", collector)
        self.assertEqual(collector, {"RIU-001", "RIU-082"})

    def test_extract_riu_ids_from_nested(self):
        collector = set()
        IntegrityGate._extract_riu_ids(
            {"a": ["RIU-001", {"b": "RIU-002"}], "c": "RIU-003"},
            collector,
        )
        self.assertEqual(collector, {"RIU-001", "RIU-002", "RIU-003"})

    def test_extract_lib_ids(self):
        collector = set()
        IntegrityGate._extract_lib_ids("See LIB-042 and LIB-089", collector)
        self.assertEqual(collector, {"LIB-042", "LIB-089"})

    def test_count_assumptions(self):
        self.assertEqual(IntegrityGate._count_assumptions("ASSUMPTION: x"), 1)
        self.assertEqual(IntegrityGate._count_assumptions({"a": "ASSUMPTION: x", "b": "ASSUMPTION: y"}), 2)
        self.assertEqual(IntegrityGate._count_assumptions("clean text"), 0)
        self.assertEqual(IntegrityGate._count_assumptions(42), 0)


if __name__ == "__main__":
    unittest.main()
