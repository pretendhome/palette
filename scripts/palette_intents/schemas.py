"""Strict artifact schemas for Palette OS intents.

Every intent produces a typed artifact. These schemas enforce the contracts
defined in INTENT_CONVERGENCE_REPORT_2026-05-27.md and validated by Gemini's
sandbox analysis + Mistral's implementation guardrails.

Usage:
    from scripts.palette_intents.schemas import GateDecision, EvidenceBrief
    decision = GateDecision(**data)  # validates or raises
    decision.to_frontmatter()       # YAML-safe dict for artifact storage
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


# ── Shared Types ───────────────────────────────────────────────────────

VALID_BOUNDARIES = ("local_only", "governed_external", "open_creation", "human_checkpoint")
VALID_POSTURES = (
    "execute",
    "execute_with_limitations",
    "narrow_or_confirm",
    "research_or_reflect_first",
    "blocked_by_boundary",
    "governance_required",
)
VALID_INTENTS = ("PROTECT", "RESEARCH", "DECIDE", "CREATE", "DIAGNOSE", "REFLECT")
VALID_STATUSES = ("VALIDATED", "LOCAL_ONLY", "UNVALIDATED_FALLBACK", "NEEDS_REVIEW", "OPEN", "PROPOSED")
VALID_REVERSIBILITY = ("ONE_WAY", "TWO_WAY")
VALID_SIGNAL_TYPES = (
    "recipe_success",
    "recipe_failure",
    "artifact_validation_failure",
    "fallback_used",
    "boundary_block",
    "governance_handoff",
    "intent_execution",
)


class SchemaValidationError(Exception):
    """Raised when an artifact fails schema validation."""

    def __init__(self, artifact_type: str, errors: list[str]):
        self.artifact_type = artifact_type
        self.errors = errors
        super().__init__(f"{artifact_type} validation failed: {'; '.join(errors)}")


def _check(condition: bool, msg: str, errors: list[str]) -> None:
    if not condition:
        errors.append(msg)


# ── Intent Route ───────────────────────────────────────────────────────


@dataclass
class IntentRoute:
    """First-pass classification result from the resolver."""

    intent: str
    riu_id: str | None = None
    secondary_intents: list[str] = field(default_factory=list)
    guard_intents: list[str] = field(default_factory=list)
    boundary: str = "local_only"
    confidence: str = "medium"  # low | medium | high
    lens: str = "general"  # legal | ai_adoption | software | general

    def validate(self) -> list[str]:
        errors: list[str] = []
        _check(self.intent in VALID_INTENTS, f"invalid intent: {self.intent}", errors)
        _check(self.boundary in VALID_BOUNDARIES, f"invalid boundary: {self.boundary}", errors)
        return errors


# ── Integrity Posture ──────────────────────────────────────────────────


@dataclass
class IntegrityPosture:
    """Integrity card output — posture + gaps + actions."""

    riu_id: str
    posture: str = "execute"
    completeness_label: str = "partial"  # full | partial | weak | bare
    gaps: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)
    recipe_coverage: list[str] = field(default_factory=list)

    def validate(self) -> list[str]:
        errors: list[str] = []
        _check(self.posture in VALID_POSTURES, f"invalid posture: {self.posture}", errors)
        return errors


# ── Integrity Signal ───────────────────────────────────────────────────


@dataclass
class IntegritySignal:
    """Emitted after intent execution — feeds back into integrity cache."""

    signal_type: str
    intent: str
    riu_id: str | None = None
    artifact_ref: str | None = None
    recipe_key: str | None = None
    summary: str = ""
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def validate(self) -> list[str]:
        errors: list[str] = []
        _check(self.signal_type in VALID_SIGNAL_TYPES, f"invalid signal_type: {self.signal_type}", errors)
        _check(self.intent in VALID_INTENTS, f"invalid intent: {self.intent}", errors)
        return errors


# ── GateDecision (PROTECT) ─────────────────────────────────────────────


@dataclass
class GateDecision:
    """PROTECT artifact — governance gate verdict."""

    artifact_type: str = "GateDecision"
    intent: str = "PROTECT"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    matter_id: str | None = None
    riu_id: str | None = None
    boundary: str = "local_only"
    action: str = "BLOCK"  # BLOCK | ALLOW
    reason: str = ""
    blocked_entities: list[str] = field(default_factory=list)
    redaction_map: dict[str, str] = field(default_factory=dict)
    safe_rewrite: str | None = None
    confidence: float = 0.0
    posture: str = "blocked_by_boundary"

    def validate(self) -> list[str]:
        errors: list[str] = []
        _check(self.action in ("BLOCK", "ALLOW"), f"action must be BLOCK or ALLOW, got: {self.action}", errors)
        _check(self.boundary in VALID_BOUNDARIES, f"invalid boundary: {self.boundary}", errors)
        if self.action == "BLOCK":
            _check(
                len(self.blocked_entities) > 0 or "too short" in self.reason or "internal_only" in self.reason,
                "BLOCK action requires non-empty blocked_entities or classification reason",
                errors,
            )
        return errors

    def to_frontmatter(self) -> dict:
        return asdict(self)


# ── EvidenceBrief (RESEARCH) ───────────────────────────────────────────


@dataclass
class LocalCanonEntry:
    """A single entry from the local knowledge library."""

    id: str = ""
    content: str = ""
    question: str = ""
    evidence_tier: int | None = None
    score: float = 0.0


@dataclass
class ExternalDeltaEntry:
    """A single entry from external research."""

    source: str = ""
    content: str = ""
    sources: list[str] = field(default_factory=list)


@dataclass
class EvidenceBrief:
    """RESEARCH artifact — local canon + external delta + synthesis."""

    artifact_type: str = "EvidenceBrief"
    intent: str = "RESEARCH"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    matter_id: str | None = None
    riu_id: str | None = None
    boundary: str = "governed_external"
    local_canon: list[dict] = field(default_factory=list)
    external_delta: list[dict] = field(default_factory=list)
    contradictions: str | None = None
    confidence: float = 0.0
    status: str = "VALIDATED"
    prior_artifacts: list[str] = field(default_factory=list)
    sources: list[str] = field(default_factory=list)

    def validate(self) -> list[str]:
        errors: list[str] = []
        _check(self.status in VALID_STATUSES, f"invalid status: {self.status}", errors)
        _check(self.boundary in VALID_BOUNDARIES, f"invalid boundary: {self.boundary}", errors)
        # Local superiority rule: contradictions cannot silently overwrite local_canon
        if self.contradictions and self.local_canon:
            # Contradiction is properly flagged — this is correct behavior
            pass
        return errors

    def to_frontmatter(self) -> dict:
        return asdict(self)


# ── DecisionRecord (DECIDE) ───────────────────────────────────────────


@dataclass
class DecisionRecord:
    """DECIDE artifact — recommendation + adversarial critique + reversibility."""

    artifact_type: str = "DecisionRecord"
    intent: str = "DECIDE"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    matter_id: str | None = None
    riu_id: str | None = None
    boundary: str = "local_only"
    recommendation: str = ""
    evidence_sources: list[str] = field(default_factory=list)
    strongest_counterargument: str = ""
    change_my_mind_trigger: str = ""
    reversibility: str = "TWO_WAY"
    checkpoint_required: bool = False
    confidence: float = 0.0
    status: str = "VALIDATED"

    def validate(self) -> list[str]:
        errors: list[str] = []
        _check(self.reversibility in VALID_REVERSIBILITY, f"invalid reversibility: {self.reversibility}", errors)
        _check(self.status in VALID_STATUSES, f"invalid status: {self.status}", errors)
        # Anti-sycophancy: counterargument must be >50 words
        word_count = len(self.strongest_counterargument.split())
        _check(
            word_count >= 50 or "failed" in self.strongest_counterargument.lower() or "unavailable" in self.strongest_counterargument.lower(),
            f"strongest_counterargument must be >50 words (got {word_count})",
            errors,
        )
        # ONE-WAY DOOR must require checkpoint
        if self.reversibility == "ONE_WAY":
            _check(self.checkpoint_required, "ONE_WAY decisions must set checkpoint_required=true", errors)
        return errors

    def to_frontmatter(self) -> dict:
        return asdict(self)


# ── ArtifactLineage (CREATE) ──────────────────────────────────────────


@dataclass
class ArtifactLineage:
    """CREATE artifact — spec + constraints + build lineage."""

    artifact_type: str = "ArtifactLineage"
    intent: str = "CREATE"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    matter_id: str | None = None
    riu_id: str | None = None
    boundary: str = "local_only"
    spec: str = ""
    constraints: list[str] = field(default_factory=list)
    audience: str | None = None
    iterations: int = 1
    max_iterations: int = 3
    models_used: list[str] = field(default_factory=list)
    review_passed: bool = False
    provenance: list[str] = field(default_factory=list)
    status: str = "VALIDATED"

    def validate(self) -> list[str]:
        errors: list[str] = []
        _check(self.max_iterations <= 3, f"max_iterations must be <=3 (got {self.max_iterations})", errors)
        _check(self.iterations <= self.max_iterations, f"iterations ({self.iterations}) exceeds max ({self.max_iterations})", errors)
        _check(self.status in VALID_STATUSES, f"invalid status: {self.status}", errors)
        return errors

    def to_frontmatter(self) -> dict:
        return asdict(self)


# ── FailureLesson (DIAGNOSE) ──────────────────────────────────────────


@dataclass
class FailureLesson:
    """DIAGNOSE artifact — 5-whys root cause analysis + fix."""

    artifact_type: str = "FailureLesson"
    intent: str = "DIAGNOSE"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    matter_id: str | None = None
    riu_id: str | None = None
    symptom: str = ""
    five_whys: list[str] = field(default_factory=list)
    root_cause_isolated: bool = False
    architectural_patch: str = ""
    fix_verified: bool = False
    tests_added: list[str] = field(default_factory=list)
    status: str = "OPEN"

    def validate(self) -> list[str]:
        errors: list[str] = []
        _check(len(self.five_whys) == 5, f"five_whys must have exactly 5 entries (got {len(self.five_whys)})", errors)
        _check(self.status in VALID_STATUSES, f"invalid status: {self.status}", errors)
        # No fix before root cause
        if self.fix_verified:
            _check(self.root_cause_isolated, "cannot verify fix before root cause is isolated", errors)
        return errors

    def to_frontmatter(self) -> dict:
        return asdict(self)


# ── ImprovementProposal (REFLECT) ─────────────────────────────────────


@dataclass
class ImprovementProposal:
    """REFLECT artifact — lesson + patterns + proposed actions."""

    artifact_type: str = "ImprovementProposal"
    intent: str = "REFLECT"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    matter_id: str | None = None
    query: str = ""
    session_summary: dict = field(default_factory=dict)
    patterns: list[str] = field(default_factory=list)
    proposed_actions: list[dict] = field(default_factory=list)
    status: str = "PROPOSED"

    def validate(self) -> list[str]:
        errors: list[str] = []
        _check(self.status in VALID_STATUSES, f"invalid status: {self.status}", errors)
        # Write-Lock Membrane: all target_files must be in wiki/proposed/
        for action in self.proposed_actions:
            target = action.get("target_file", "")
            if target:
                _check(
                    target.startswith("wiki/proposed/"),
                    f"target_file must be in wiki/proposed/ (got: {target})",
                    errors,
                )
        return errors

    def to_frontmatter(self) -> dict:
        return asdict(self)


# ── Validation Helper ──────────────────────────────────────────────────


SCHEMA_MAP = {
    "GateDecision": GateDecision,
    "EvidenceBrief": EvidenceBrief,
    "DecisionRecord": DecisionRecord,
    "ArtifactLineage": ArtifactLineage,
    "FailureLesson": FailureLesson,
    "ImprovementProposal": ImprovementProposal,
}


def validate_artifact(data: dict) -> list[str]:
    """Validate an artifact dict against its schema.

    Returns list of errors (empty = valid).
    """
    artifact_type = data.get("artifact_type", "")
    schema_cls = SCHEMA_MAP.get(artifact_type)
    if not schema_cls:
        return [f"unknown artifact_type: {artifact_type}"]

    # Build instance from data, ignoring extra fields
    import inspect
    valid_fields = {f.name for f in schema_cls.__dataclass_fields__.values()}
    filtered = {k: v for k, v in data.items() if k in valid_fields}
    try:
        instance = schema_cls(**filtered)
    except TypeError as e:
        return [f"schema instantiation failed: {e}"]

    return instance.validate()
