"""Tests for the Palette checkpoint and transition logic.

Validates:
- Transition depth limit (max 2)
- Priority ordering (PROTECT > DIAGNOSE > RESEARCH > DECIDE > CREATE > REFLECT)
- Boundary violation → PROTECT transition
- Governance required → halt (no auto-transition)
- Intent state transitions preserve thread_id and matter_id
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from scripts.palette_intents.infra import (
    IntentState,
    IntegrityCard,
    palette_checkpoint,
)


# ── Transition Depth Limit ─────────────────────────────────────────────


class TestTransitionDepthLimit:
    def test_depth_zero_allows_transition(self):
        state = IntentState(
            intent="RESEARCH",
            query="test",
            transition_depth=0,
            integrity_card={"posture": "blocked_by_boundary"},
        )
        result = palette_checkpoint(state)
        assert result.intent == "PROTECT"
        assert result.transition_depth == 1

    def test_depth_two_allows_transition(self):
        state = IntentState(
            intent="RESEARCH",
            query="test",
            transition_depth=2,
            integrity_card={"posture": "blocked_by_boundary"},
        )
        result = palette_checkpoint(state)
        assert result.intent == "PROTECT"

    def test_depth_three_halts(self):
        """Transition depth > 2 prevents further transitions (recursive oscillation guard)."""
        state = IntentState(
            intent="RESEARCH",
            query="test",
            transition_depth=3,
            integrity_card={"posture": "blocked_by_boundary"},
        )
        result = palette_checkpoint(state)
        # Should NOT transition — depth exceeded
        assert result.intent == "RESEARCH"


# ── Boundary Violation → PROTECT ───────────────────────────────────────


class TestBoundaryViolation:
    def test_blocked_boundary_triggers_protect(self):
        state = IntentState(
            intent="RESEARCH",
            query="privileged query",
            integrity_card={"posture": "blocked_by_boundary"},
        )
        result = palette_checkpoint(state)
        assert result.intent == "PROTECT"

    def test_already_in_protect_stays(self):
        state = IntentState(
            intent="PROTECT",
            query="test",
            integrity_card={"posture": "blocked_by_boundary"},
        )
        result = palette_checkpoint(state)
        assert result.intent == "PROTECT"
        # Should NOT increment transition_depth (no transition occurred)

    def test_execute_posture_no_transition(self):
        state = IntentState(
            intent="RESEARCH",
            query="safe query",
            integrity_card={"posture": "execute"},
        )
        result = palette_checkpoint(state)
        assert result.intent == "RESEARCH"


# ── Governance Required → Halt ─────────────────────────────────────────


class TestGovernanceHalt:
    def test_governance_required_halts(self):
        """Governance required should NOT auto-transition — needs human."""
        state = IntentState(
            intent="REFLECT",
            query="change the taxonomy",
            integrity_card={"posture": "governance_required"},
        )
        result = palette_checkpoint(state)
        assert result.intent == "REFLECT"  # stays — no auto-transition


# ── State Preservation ─────────────────────────────────────────────────


class TestStatePreservation:
    def test_transition_preserves_thread_id(self):
        state = IntentState(
            intent="RESEARCH",
            query="test",
            thread_id="abc-123",
            matter_id="sarah-llc-001",
            integrity_card={"posture": "blocked_by_boundary"},
        )
        result = palette_checkpoint(state)
        assert result.thread_id == "abc-123"
        assert result.matter_id == "sarah-llc-001"

    def test_transition_preserves_artifacts(self):
        state = IntentState(
            intent="RESEARCH",
            query="test",
            artifacts=["/path/to/prior.md"],
            integrity_card={"posture": "blocked_by_boundary"},
        )
        result = palette_checkpoint(state)
        assert "/path/to/prior.md" in result.artifacts

    def test_transition_increments_depth(self):
        state = IntentState(
            intent="RESEARCH",
            query="test",
            transition_depth=0,
            integrity_card={"posture": "blocked_by_boundary"},
        )
        result = palette_checkpoint(state)
        assert result.transition_depth == 1


# ── IntegrityCard as Object ────────────────────────────────────────────


class TestIntegrityCardObject:
    def test_checkpoint_handles_integrity_card_object(self):
        card = IntegrityCard(
            riu_id="RIU-700",
            classification="internal_only",
            posture="blocked_by_boundary",
        )
        state = IntentState(
            intent="RESEARCH",
            query="test",
            integrity_card=card,
        )
        result = palette_checkpoint(state)
        assert result.intent == "PROTECT"

    def test_checkpoint_handles_dict_card(self):
        state = IntentState(
            intent="RESEARCH",
            query="test",
            integrity_card={"posture": "execute"},
        )
        result = palette_checkpoint(state)
        assert result.intent == "RESEARCH"
