"""Tests for palette.sdk.integrity_gate — V2.2 wire contract."""

from __future__ import annotations

import sys, os, unittest

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
    """Mimics HandoffResult with canonical V2.2 field names."""
    def __init__(self, output=None, status="success", blockers=None, artifacts=None):
        self.output = output or {}
        self.status = status
        self.blockers = blockers or []
        self.artifacts = artifacts or []


# ── None guards ───────────────────────────────────────────────────────

class TestNoneGuards(unittest.TestCase):
    def test_none_data_returns_warning(self):
        gate = IntegrityGate(None)
        warnings = gate.check_result(FakeResult())
        self.assertEqual(len(warnings), 1)
        self.assertIn("PIS data is None", warnings[0])

    def test_none_result_returns_warning(self):
        gate = IntegrityGate(FakePISData())
        warnings = gate.check_result(None)
        self.assertIn("result is None", warnings[0])

    def test_empty_data_clean(self):
        gate = IntegrityGate(FakePISData())
        self.assertEqual(gate.check_result(FakeResult()), [])


# ── RIU references ────────────────────────────────────────────────────

class TestRIUReferences(unittest.TestCase):
    def test_valid_riu_no_warning(self):
        data = FakePISData(classification={"RIU-082": {}})
        gate = IntegrityGate(data)
        result = FakeResult(output={"note": "See RIU-082"})
        self.assertEqual(gate.check_result(result), [])

    def test_invalid_riu_warns(self):
        data = FakePISData(classification={"RIU-082": {}})
        gate = IntegrityGate(data)
        result = FakeResult(output={"note": "See RIU-999"})
        self.assertTrue(any("RIU-999" in w for w in gate.check_result(result)))

    def test_nested_riu_extraction(self):
        data = FakePISData(classification={"RIU-001": {}, "RIU-002": {}})
        gate = IntegrityGate(data)
        result = FakeResult(output={"deep": {"nested": ["RIU-001", {"ref": "RIU-002 and RIU-999"}]}})
        warnings = gate.check_result(result)
        self.assertTrue(any("RIU-999" in w for w in warnings))
        self.assertFalse(any("RIU-001" in w for w in warnings))

    def test_no_classification_skips_check(self):
        gate = IntegrityGate(FakePISData())
        self.assertEqual(gate.check_result(FakeResult(output={"note": "RIU-999"})), [])

    def test_checks_artifacts_field(self):
        data = FakePISData(classification={"RIU-082": {}})
        gate = IntegrityGate(data)
        result = FakeResult(artifacts=["See RIU-999 for details"])
        self.assertTrue(any("RIU-999" in w for w in gate.check_result(result)))

    def test_checks_blockers_field(self):
        data = FakePISData(classification={"RIU-082": {}})
        gate = IntegrityGate(data)
        result = FakeResult(blockers=["RIU-998 is uncertain"])
        self.assertTrue(any("RIU-998" in w for w in gate.check_result(result)))


# ── Knowledge references ──────────────────────────────────────────────

class TestKnowledgeReferences(unittest.TestCase):
    def test_valid_lib_no_warning(self):
        data = FakePISData(knowledge={"LIB-042": {}})
        gate = IntegrityGate(data)
        self.assertEqual(gate.check_result(FakeResult(output={"ref": "LIB-042"})), [])

    def test_invalid_lib_warns(self):
        data = FakePISData(knowledge={"LIB-042": {}})
        gate = IntegrityGate(data)
        self.assertTrue(any("LIB-999" in w for w in gate.check_result(FakeResult(output={"ref": "LIB-999"}))))


# ── Service references ────────────────────────────────────────────────

class TestServiceReferences(unittest.TestCase):
    def test_valid_service_no_warning(self):
        data = FakePISData(routing={"RIU-082": {"services": [{"name": "Bedrock Guardrails"}]}})
        gate = IntegrityGate(data)
        result = FakeResult(output={"riu_id": "RIU-082", "recommendation": {"service": "Bedrock Guardrails"}})
        self.assertEqual(gate.check_result(result), [])

    def test_invalid_service_warns(self):
        data = FakePISData(routing={"RIU-082": {"services": [{"name": "Bedrock Guardrails"}]}})
        gate = IntegrityGate(data)
        result = FakeResult(output={"riu_id": "RIU-082", "recommendation": {"service": "FakeService"}})
        self.assertTrue(any("FakeService" in w for w in gate.check_result(result)))

    def test_no_routing_skips_check(self):
        gate = IntegrityGate(FakePISData())
        result = FakeResult(output={"riu_id": "RIU-082", "recommendation": {"service": "anything"}})
        self.assertEqual(gate.check_result(result), [])


# ── Blockers populated (glass-box invariant #3) ──────────────────────

class TestBlockersPopulated(unittest.TestCase):
    def test_failure_without_blockers_warns(self):
        gate = IntegrityGate(FakePISData())
        result = FakeResult(status="failure", blockers=[])
        self.assertTrue(any("blockers" in w.lower() for w in gate.check_result(result)))

    def test_blocked_without_blockers_warns(self):
        gate = IntegrityGate(FakePISData())
        result = FakeResult(status="blocked", blockers=[])
        self.assertTrue(any("blockers" in w.lower() for w in gate.check_result(result)))

    def test_failure_with_blockers_clean(self):
        gate = IntegrityGate(FakePISData())
        result = FakeResult(status="failure", blockers=["something went wrong"])
        warnings = gate.check_result(result)
        self.assertFalse(any("blockers" in w.lower() and "empty" in w.lower() for w in warnings))

    def test_assumptions_without_blockers_warns(self):
        gate = IntegrityGate(FakePISData())
        result = FakeResult(output={"note": "ASSUMPTION: pricing is stable"}, blockers=[])
        self.assertTrue(any("ASSUMPTION" in w for w in gate.check_result(result)))

    def test_assumptions_with_blockers_clean(self):
        gate = IntegrityGate(FakePISData())
        result = FakeResult(output={"note": "ASSUMPTION: pricing is stable"}, blockers=["pricing may change"])
        self.assertFalse(any("ASSUMPTION" in w for w in gate.check_result(result)))


# ── Helpers ───────────────────────────────────────────────────────────

class TestHelpers(unittest.TestCase):
    def test_extract_riu_ids_from_string(self):
        collector = set()
        IntegrityGate._extract_riu_ids("RIU-001 and RIU-082", collector)
        self.assertEqual(collector, {"RIU-001", "RIU-082"})

    def test_extract_riu_ids_from_nested(self):
        collector = set()
        IntegrityGate._extract_riu_ids({"a": ["RIU-001", {"b": "RIU-002"}], "c": "RIU-003"}, collector)
        self.assertEqual(collector, {"RIU-001", "RIU-002", "RIU-003"})

    def test_extract_lib_ids(self):
        collector = set()
        IntegrityGate._extract_lib_ids("See LIB-042 and LIB-089", collector)
        self.assertEqual(collector, {"LIB-042", "LIB-089"})

    def test_count_assumptions(self):
        self.assertEqual(IntegrityGate._count_assumptions("ASSUMPTION: x"), 1)
        self.assertEqual(IntegrityGate._count_assumptions({"a": "ASSUMPTION: x", "b": "ASSUMPTION: y"}), 2)
        self.assertEqual(IntegrityGate._count_assumptions(42), 0)


if __name__ == "__main__":
    unittest.main()
