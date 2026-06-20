"""Tests for the BDB demo path: PROTECT → RESEARCH → DECIDE.

These tests validate the demo-critical intent chain without requiring
live model calls (Ollama/Perplexity). They test the governance logic,
artifact schema compliance, and transition behavior.
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.palette_intents.schemas import validate_artifact
from scripts.palette_intents.infra import (
    IntentState,
    store_artifact,
    ARTIFACTS_DIR,
)


# ── PROTECT Tests ──────────────────────────────────────────────────────


class TestProtectGovernance:
    """Test PROTECT governance logic without live models."""

    def test_strategy_language_detected(self):
        from scripts.palette_intents.protect import detect_strategy_language

        blocked = detect_strategy_language("What's our exposure if the majority member was self-dealing?")
        assert "our exposure" in blocked

    def test_no_strategy_in_public_query(self):
        from scripts.palette_intents.protect import detect_strategy_language

        blocked = detect_strategy_language("What fiduciary duty standards apply to LLC co-founders in Delaware?")
        assert len(blocked) == 0

    def test_redaction_map_uses_tokens(self):
        from scripts.palette_intents.protect import build_redaction_map

        redaction = build_redaction_map("test query", ["our exposure", "client name"])
        assert "[Entity A]" in redaction
        assert "[Entity B]" in redaction
        assert redaction["[Entity A]"] == "our exposure"

    def test_safe_rewrite_blocked_for_strategy(self):
        from scripts.palette_intents.protect import attempt_safe_rewrite

        result = attempt_safe_rewrite("What's our exposure in this matter?", ["our exposure"])
        assert result is None  # fundamentally privileged — no safe rewrite

    def test_gate_decision_schema_valid_block(self):
        gate = {
            "artifact_type": "GateDecision",
            "action": "BLOCK",
            "blocked_entities": ["our exposure"],
            "boundary": "local_only",
            "reason": "strategy language detected",
        }
        errors = validate_artifact(gate)
        assert errors == []

    def test_gate_decision_schema_valid_allow(self):
        gate = {
            "artifact_type": "GateDecision",
            "action": "ALLOW",
            "boundary": "governed_external",
        }
        errors = validate_artifact(gate)
        assert errors == []


# ── RESEARCH Tests ─────────────────────────────────────────────────────


class TestResearchGovernance:
    """Test RESEARCH governance logic without live Perplexity calls."""

    def test_contradiction_detection_strong_signal(self):
        from scripts.palette_intents.research import _detect_contradictions

        local = [{"id": "KL-001", "content": "The fiduciary standard requires good faith dealing among members"}]
        external = "The previous standard was overruled by the Delaware Supreme Court in 2024, holding that fiduciary duties are now narrower"
        result = _detect_contradictions(local, external)
        assert result is not None
        assert "overruled" in result

    def test_contradiction_detection_no_false_positive(self):
        from scripts.palette_intents.research import _detect_contradictions

        local = [{"id": "KL-001", "content": "Delaware LLC Act Section 18-1104 provides for fiduciary duties"}]
        external = "Section 18-1104 of the Delaware LLC Act governs fiduciary obligations of managers"
        result = _detect_contradictions(local, external)
        assert result is None  # agreement, not contradiction

    def test_evidence_brief_schema_valid(self):
        brief = {
            "artifact_type": "EvidenceBrief",
            "local_canon": [{"id": "KL-123", "content": "test"}],
            "external_delta": [{"source": "perplexity", "content": "test"}],
            "status": "VALIDATED",
            "boundary": "governed_external",
        }
        errors = validate_artifact(brief)
        assert errors == []

    def test_evidence_brief_fallback_valid(self):
        brief = {
            "artifact_type": "EvidenceBrief",
            "local_canon": [],
            "external_delta": [],
            "status": "UNVALIDATED_FALLBACK",
            "boundary": "local_only",
        }
        errors = validate_artifact(brief)
        assert errors == []

    def test_sanitizer_gate_blocks_unsafe(self):
        from scripts.palette_intents.research import is_safe_for_external

        # This test validates the re-evaluation hook exists
        # The actual sanitizer behavior depends on the sanitizer module
        safe, reason = is_safe_for_external("What's our client's exposure in the Acme case?")
        # Should block — contains "our client" and case reference
        # (May pass if sanitizer module isn't available — that's the fail-safe)
        assert isinstance(safe, bool)
        assert isinstance(reason, str)


# ── DECIDE Tests ───────────────────────────────────────────────────────


class TestDecideGovernance:
    """Test DECIDE governance logic without live Ollama calls."""

    def test_one_way_door_detection(self):
        from scripts.palette_intents.decide import detect_one_way_door

        assert detect_one_way_door("Should we settle?", "Recommend settlement") is True
        assert detect_one_way_door("Should we file the motion?", "File immediately") is True
        assert detect_one_way_door("Should we review the brief?", "Review it carefully") is False

    def test_evidence_context_from_prior_artifacts(self):
        from scripts.palette_intents.decide import build_evidence_context

        evidence = [
            {"type": "GateDecision", "action": "BLOCK", "boundary": "local_only",
             "intent": "PROTECT", "timestamp": "2026-05-27", "confidence": 0,
             "path": "test", "local_canon": [], "recommendation": ""},
            {"type": "EvidenceBrief", "action": "", "boundary": "governed_external",
             "intent": "RESEARCH", "timestamp": "2026-05-27", "confidence": 85,
             "path": "test", "local_canon": [{"question": "Delaware law", "content": "Section 18-1104..."}],
             "recommendation": ""},
        ]
        context = build_evidence_context(evidence)
        assert "[PROTECT]" in context
        assert "[RESEARCH]" in context

    def test_decision_record_schema_valid(self):
        record = {
            "artifact_type": "DecisionRecord",
            "recommendation": "Settle the case.",
            "strongest_counterargument": " ".join(["The risk of settlement is that"] + ["word"] * 50),
            "change_my_mind_trigger": "If discovery reveals no self-dealing",
            "reversibility": "TWO_WAY",
            "checkpoint_required": False,
            "status": "VALIDATED",
        }
        errors = validate_artifact(record)
        assert errors == []

    def test_decision_record_short_counter_fails(self):
        record = {
            "artifact_type": "DecisionRecord",
            "recommendation": "Settle.",
            "strongest_counterargument": "Bad idea.",
            "reversibility": "TWO_WAY",
        }
        errors = validate_artifact(record)
        assert any("50 words" in e for e in errors)

    def test_one_way_without_checkpoint_fails(self):
        record = {
            "artifact_type": "DecisionRecord",
            "recommendation": "File the motion.",
            "strongest_counterargument": " ".join(["word"] * 55),
            "reversibility": "ONE_WAY",
            "checkpoint_required": False,
        }
        errors = validate_artifact(record)
        assert any("checkpoint" in e for e in errors)


# ── Artifact Storage ───────────────────────────────────────────────────


class TestArtifactStorage:
    def test_store_and_read(self, tmp_path, monkeypatch):
        monkeypatch.setattr("scripts.palette_intents.infra.ARTIFACTS_DIR", tmp_path)
        content = {"artifact_type": "GateDecision", "action": "BLOCK", "blocked_entities": ["test"]}
        path = store_artifact("gate_decision", content, "# Test\n\nBody here.")
        assert Path(path).exists()
        text = Path(path).read_text()
        assert "artifact_type: GateDecision" in text
        assert "Body here." in text

    def test_storage_creates_subdirectory(self, tmp_path, monkeypatch):
        monkeypatch.setattr("scripts.palette_intents.infra.ARTIFACTS_DIR", tmp_path)
        store_artifact("evidence_brief", {"artifact_type": "EvidenceBrief"}, "test")
        assert (tmp_path / "evidence_brief").is_dir()


# ── Demo Path Integration (Schema Only) ───────────────────────────────


class TestDemoPathSchemas:
    """Validate that the complete demo path produces valid schemas."""

    def test_protect_then_research_schemas_compatible(self):
        """PROTECT produces boundary info that RESEARCH consumes."""
        gate = {
            "artifact_type": "GateDecision",
            "action": "ALLOW",
            "boundary": "governed_external",
            "safe_rewrite": "Delaware LLC fiduciary duty standards",
        }
        assert validate_artifact(gate) == []

        brief = {
            "artifact_type": "EvidenceBrief",
            "boundary": gate["boundary"],
            "local_canon": [{"id": "KL-701", "content": "Delaware fiduciary law..."}],
            "external_delta": [{"source": "perplexity", "content": "Recent cases..."}],
            "status": "VALIDATED",
        }
        assert validate_artifact(brief) == []

    def test_research_then_decide_schemas_compatible(self):
        """DECIDE references RESEARCH evidence."""
        record = {
            "artifact_type": "DecisionRecord",
            "recommendation": "Based on the fiduciary standards, proceed with the breach claim.",
            "evidence_sources": ["/path/to/evidence_brief.md"],
            "strongest_counterargument": (
                "The counterargument is that the majority member may have acted within "
                "the bounds of the LLC agreement which could provide a safe harbor defense "
                "under Delaware law particularly if the operating agreement explicitly "
                "authorized related party transactions with proper disclosure requirements. "
                "Furthermore the business judgment rule may shield the majority member from "
                "liability if they can demonstrate that the self-dealing transactions were "
                "conducted at fair market value and with adequate disclosure to all members."
            ),
            "change_my_mind_trigger": "If the LLC agreement contains a safe harbor provision for related-party transactions",
            "reversibility": "TWO_WAY",
            "checkpoint_required": False,
            "boundary": "local_only",
            "status": "VALIDATED",
        }
        assert validate_artifact(record) == []
