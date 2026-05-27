"""Tests for artifact schema validation.

Validates the contracts from INTENT_CONVERGENCE_REPORT_2026-05-27.md:
- GateDecision: blocked_entities non-empty if BLOCK
- EvidenceBrief: contradictions cannot overwrite local_canon
- DecisionRecord: counterargument >50 words, ONE_WAY requires checkpoint
- ArtifactLineage: max_iterations <=3
- FailureLesson: five_whys.length == 5, no fix before root cause
- ImprovementProposal: target_file in wiki/proposed/
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.palette_intents.schemas import (
    GateDecision,
    EvidenceBrief,
    DecisionRecord,
    ArtifactLineage,
    FailureLesson,
    ImprovementProposal,
    IntentRoute,
    IntegrityPosture,
    IntegritySignal,
    validate_artifact,
)


# ── GateDecision ───────────────────────────────────────────────────────


class TestGateDecision:
    def test_valid_block(self):
        gd = GateDecision(action="BLOCK", blocked_entities=["our exposure"], reason="strategy language detected")
        assert gd.validate() == []

    def test_block_needs_entities_or_reason(self):
        gd = GateDecision(action="BLOCK", blocked_entities=[], reason="")
        errors = gd.validate()
        assert len(errors) > 0
        assert "blocked_entities" in errors[0]

    def test_block_with_classification_reason(self):
        gd = GateDecision(action="BLOCK", blocked_entities=[], reason="RIU-700 classified as internal_only")
        assert gd.validate() == []

    def test_valid_allow(self):
        gd = GateDecision(action="ALLOW", boundary="governed_external")
        assert gd.validate() == []

    def test_invalid_action(self):
        gd = GateDecision(action="MAYBE")
        errors = gd.validate()
        assert any("BLOCK or ALLOW" in e for e in errors)

    def test_invalid_boundary(self):
        gd = GateDecision(action="ALLOW", boundary="yolo")
        errors = gd.validate()
        assert any("boundary" in e for e in errors)

    def test_to_frontmatter(self):
        gd = GateDecision(action="BLOCK", blocked_entities=["client name"])
        fm = gd.to_frontmatter()
        assert fm["artifact_type"] == "GateDecision"
        assert fm["action"] == "BLOCK"


# ── EvidenceBrief ──────────────────────────────────────────────────────


class TestEvidenceBrief:
    def test_valid_with_external(self):
        eb = EvidenceBrief(
            local_canon=[{"id": "KL-123", "content": "test"}],
            external_delta=[{"source": "perplexity", "content": "test"}],
            status="VALIDATED",
        )
        assert eb.validate() == []

    def test_valid_local_only(self):
        eb = EvidenceBrief(
            local_canon=[{"id": "KL-123", "content": "test"}],
            status="LOCAL_ONLY",
            boundary="local_only",
        )
        assert eb.validate() == []

    def test_valid_fallback(self):
        eb = EvidenceBrief(status="UNVALIDATED_FALLBACK")
        assert eb.validate() == []

    def test_invalid_status(self):
        eb = EvidenceBrief(status="MAGIC")
        errors = eb.validate()
        assert any("status" in e for e in errors)

    def test_contradiction_flagged_is_valid(self):
        eb = EvidenceBrief(
            local_canon=[{"id": "KL-001", "content": "local truth"}],
            contradictions="External source contradicts KL-001",
            status="VALIDATED",
        )
        # Contradiction is properly flagged — valid behavior
        assert eb.validate() == []


# ── DecisionRecord ─────────────────────────────────────────────────────


class TestDecisionRecord:
    def test_valid_two_way(self):
        dr = DecisionRecord(
            recommendation="Settle the case.",
            strongest_counterargument=" ".join(["word"] * 55),
            change_my_mind_trigger="If discovery reveals no self-dealing",
            reversibility="TWO_WAY",
        )
        assert dr.validate() == []

    def test_counterargument_too_short(self):
        dr = DecisionRecord(
            recommendation="Settle.",
            strongest_counterargument="Too short.",
            reversibility="TWO_WAY",
        )
        errors = dr.validate()
        assert any("50 words" in e for e in errors)

    def test_one_way_requires_checkpoint(self):
        dr = DecisionRecord(
            recommendation="File the motion.",
            strongest_counterargument=" ".join(["word"] * 55),
            reversibility="ONE_WAY",
            checkpoint_required=False,
        )
        errors = dr.validate()
        assert any("checkpoint_required" in e for e in errors)

    def test_one_way_with_checkpoint_valid(self):
        dr = DecisionRecord(
            recommendation="File the motion.",
            strongest_counterargument=" ".join(["word"] * 55),
            reversibility="ONE_WAY",
            checkpoint_required=True,
        )
        assert dr.validate() == []

    def test_invalid_reversibility(self):
        dr = DecisionRecord(
            strongest_counterargument=" ".join(["word"] * 55),
            reversibility="MAYBE",
        )
        errors = dr.validate()
        assert any("reversibility" in e for e in errors)

    def test_counterargument_failure_message_allowed(self):
        dr = DecisionRecord(
            recommendation="Settle.",
            strongest_counterargument="Counterargument generation failed. Human review required.",
            reversibility="TWO_WAY",
        )
        # "failed" keyword allows short counterargument
        assert dr.validate() == []


# ── ArtifactLineage ───────────────────────────────────────────────────


class TestArtifactLineage:
    def test_valid(self):
        al = ArtifactLineage(spec="Write a memo", iterations=1, max_iterations=3)
        assert al.validate() == []

    def test_max_iterations_exceeded(self):
        al = ArtifactLineage(max_iterations=5)
        errors = al.validate()
        assert any("max_iterations" in e for e in errors)

    def test_iterations_exceeds_max(self):
        al = ArtifactLineage(iterations=4, max_iterations=3)
        errors = al.validate()
        assert any("iterations" in e for e in errors)


# ── FailureLesson ─────────────────────────────────────────────────────


class TestFailureLesson:
    def test_valid(self):
        fl = FailureLesson(
            symptom="Query routed externally",
            five_whys=["1. why?", "2. why?", "3. why?", "4. why?", "5. root cause"],
            root_cause_isolated=True,
        )
        assert fl.validate() == []

    def test_not_enough_whys(self):
        fl = FailureLesson(
            symptom="Bug",
            five_whys=["1. why?", "2. why?"],
        )
        errors = fl.validate()
        assert any("5 entries" in e for e in errors)

    def test_fix_before_root_cause(self):
        fl = FailureLesson(
            symptom="Bug",
            five_whys=["1", "2", "3", "4", "5"],
            root_cause_isolated=False,
            fix_verified=True,
        )
        errors = fl.validate()
        assert any("root cause" in e for e in errors)

    def test_too_many_whys_truncated(self):
        fl = FailureLesson(
            symptom="Bug",
            five_whys=["1", "2", "3", "4", "5", "6"],
        )
        errors = fl.validate()
        assert any("5 entries" in e for e in errors)


# ── ImprovementProposal ──────────────────────────────────────────────


class TestImprovementProposal:
    def test_valid(self):
        ip = ImprovementProposal(
            query="What did we learn?",
            patterns=["Low confidence on RIU-701"],
            proposed_actions=[{"action": "Add KL entry", "target_file": "wiki/proposed/KL-PROP-test.yaml"}],
        )
        assert ip.validate() == []

    def test_write_lock_membrane(self):
        ip = ImprovementProposal(
            proposed_actions=[{"action": "Overwrite KL", "target_file": "knowledge-library/v1.4/bad.yaml"}],
        )
        errors = ip.validate()
        assert any("wiki/proposed/" in e for e in errors)

    def test_taxonomy_write_blocked(self):
        ip = ImprovementProposal(
            proposed_actions=[{"action": "Add RIU", "target_file": "taxonomy/releases/v1.3/new.yaml"}],
        )
        errors = ip.validate()
        assert any("wiki/proposed/" in e for e in errors)


# ── Shared Data Contracts ─────────────────────────────────────────────


class TestIntentRoute:
    def test_valid(self):
        ir = IntentRoute(intent="PROTECT", riu_id="RIU-700", boundary="local_only")
        assert ir.validate() == []

    def test_invalid_intent(self):
        ir = IntentRoute(intent="YELL", boundary="local_only")
        errors = ir.validate()
        assert any("intent" in e for e in errors)


class TestIntegrityPosture:
    def test_valid(self):
        ip = IntegrityPosture(riu_id="RIU-700", posture="blocked_by_boundary")
        assert ip.validate() == []

    def test_invalid_posture(self):
        ip = IntegrityPosture(riu_id="RIU-700", posture="vibes")
        errors = ip.validate()
        assert any("posture" in e for e in errors)


class TestIntegritySignal:
    def test_valid(self):
        sig = IntegritySignal(signal_type="recipe_success", intent="RESEARCH")
        assert sig.validate() == []

    def test_invalid_signal_type(self):
        sig = IntegritySignal(signal_type="magic", intent="RESEARCH")
        errors = sig.validate()
        assert any("signal_type" in e for e in errors)


# ── validate_artifact helper ──────────────────────────────────────────


class TestValidateArtifact:
    def test_valid_gate_decision(self):
        data = {"artifact_type": "GateDecision", "action": "BLOCK", "blocked_entities": ["test"]}
        assert validate_artifact(data) == []

    def test_unknown_type(self):
        errors = validate_artifact({"artifact_type": "MagicArtifact"})
        assert any("unknown" in e for e in errors)

    def test_missing_type(self):
        errors = validate_artifact({})
        assert any("unknown" in e for e in errors)
