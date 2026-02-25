"""Core PIS traversal: RIU → structured recommendation."""

from __future__ import annotations

from dataclasses import dataclass, field

from . import score as scoring
from .health import record_and_evaluate
from .loader import PISData
from .score import CompletenessScore


# ── Result dataclasses ──────────────────────────────────────────────

@dataclass
class ServiceRecommendation:
    service_name: str
    quality_tier: str
    cost_model: str
    cost_estimate: str
    integration_status: str       # integrated | available | recipe_needed | evaluate | no_api
    recipe_available: bool
    recipe_path: str | None
    signal_strength: str
    best_for: list[str]
    why_primary: str
    why_not: str | None = None


@dataclass
class KnowledgeHit:
    lib_id: str
    question: str                 # first 120 chars
    journey_stage: str
    has_eval_signal: bool


@dataclass
class SignalHit:
    tool_name: str
    signal_tier: int
    recommenders: list[dict]      # [{id, name, reason}]
    palette_action: str


@dataclass
class TraversalResult:
    # Input
    query_riu: str
    query_riu_name: str
    resolved_from: str | None = None

    # Classification
    classification: str = ""
    classification_rationale: str = ""

    # Recommendation
    recommendation: ServiceRecommendation | None = None
    alternatives: list[ServiceRecommendation] = field(default_factory=list)

    # Supporting evidence
    knowledge_support: list[KnowledgeHit] = field(default_factory=list)
    signal_validation: list[SignalHit] = field(default_factory=list)

    # Gaps (first-class, always populated)
    gaps: list[str] = field(default_factory=list)

    # Scoring
    completeness: CompletenessScore | None = None

    # Health
    health_status: str = "ok"


# ── Ranking ─────────────────────────────────────────────────────────

_STATUS_ORDER = {
    "integrated": 0,
    "available": 1,
    "recipe_needed": 2,
    "evaluate": 3,
    "no_api": 4,
}
_TIER_ORDER = {"tier_1": 0, "tier_2": 1, "tier_3": 2}
_STRENGTH_ORDER = {"high": 0, "medium": 1, "low": 2}


def _rank_key(svc: ServiceRecommendation) -> tuple:
    """Sort key: lower is better."""
    status = _STATUS_ORDER.get(svc.integration_status, 5)
    # Recipe available is a bonus — move available-with-recipe ahead of available-without
    recipe_bonus = 0 if svc.recipe_available else 1
    tier = _TIER_ORDER.get(svc.quality_tier, 3)
    strength = _STRENGTH_ORDER.get(svc.signal_strength, 3)
    return (status, recipe_bonus, tier, strength)


def _explain_why_not(primary: ServiceRecommendation, alt: ServiceRecommendation) -> str:
    """Construct a specific reason why this alternative ranks below the primary."""
    reasons: list[str] = []
    # Integration status difference
    p_status = _STATUS_ORDER.get(primary.integration_status, 5)
    a_status = _STATUS_ORDER.get(alt.integration_status, 5)
    if a_status > p_status:
        reasons.append(f"{alt.integration_status} vs {primary.service_name}'s {primary.integration_status}")
    # Tier difference
    p_tier = _TIER_ORDER.get(primary.quality_tier, 3)
    a_tier = _TIER_ORDER.get(alt.quality_tier, 3)
    if a_tier > p_tier:
        reasons.append(f"{alt.quality_tier} (vs {primary.quality_tier})")
    # Recipe gap
    if primary.recipe_available and not alt.recipe_available:
        reasons.append("no integration recipe")
    # Signal strength
    p_str = _STRENGTH_ORDER.get(primary.signal_strength, 3)
    a_str = _STRENGTH_ORDER.get(alt.signal_strength, 3)
    if a_str > p_str:
        reasons.append(f"{alt.signal_strength} signal (vs {primary.signal_strength})")
    if not reasons:
        reasons.append(f"same tier as {primary.service_name} but listed lower")
    return "; ".join(reasons)


# ── Traversal ───────────────────────────────────────────────────────

def _resolve_riu_from_lib(data: PISData, lib_id: str) -> tuple[str | None, list[str]]:
    """Resolve LIB-XXX → (primary RIU, secondary RIUs)."""
    entry = data.knowledge.get(lib_id)
    if not entry:
        return None, []
    rius = entry.get("related_rius", [])
    if not rius:
        return None, []
    return rius[0], rius[1:]


def _build_service_recommendations(
    data: PISData, routing_entry: dict,
) -> list[ServiceRecommendation]:
    """Build ServiceRecommendation objects from a routing entry."""
    services = routing_entry.get("services", [])
    recs: list[ServiceRecommendation] = []
    for svc in services:
        name = svc.get("name", "")
        name_lower = name.lower()
        # Look up recipe — try exact lowercased name, and also first word
        recipe = data.recipes.get(name_lower)
        if not recipe:
            # Try matching on first significant word (e.g. "AWS Bedrock Guardrails" → "openrouter" won't match,
            # but "Gamma" → "gamma" will)
            for rkey, rval in data.recipes.items():
                if rkey in name_lower or name_lower in rkey:
                    recipe = rval
                    break

        recipe_available = recipe is not None
        recipe_path = recipe.get("_recipe_path") if recipe else None

        # Determine integration_status — recipe file's status can override routing if more specific
        integration_status = svc.get("integration_status", "evaluate")

        recs.append(ServiceRecommendation(
            service_name=name,
            quality_tier=svc.get("quality_tier", "tier_3"),
            cost_model=svc.get("cost_model", "unknown"),
            cost_estimate=svc.get("cost_estimate", "unknown"),
            integration_status=integration_status,
            recipe_available=recipe_available,
            recipe_path=recipe_path,
            signal_strength=svc.get("signal_strength", "low"),
            best_for=svc.get("best_for", []),
            why_primary=svc.get("notes", ""),
        ))
    # Sort by ranking policy
    recs.sort(key=_rank_key)
    return recs


def _find_signals(data: PISData, riu_id: str) -> list[SignalHit]:
    """Find people-library signals for a given RIU."""
    hits: list[SignalHit] = []
    for sig in data.signals:
        primary = sig.get("riu_primary", "")
        secondary = sig.get("riu_secondary", [])
        if primary == riu_id or riu_id in secondary:
            recommenders = []
            for r in sig.get("recommenders", []):
                recommenders.append({
                    "id": r.get("id", ""),
                    "name": r.get("name", ""),
                    "reason": r.get("reason", r.get("note", "")),
                })
            hits.append(SignalHit(
                tool_name=sig.get("tool", ""),
                signal_tier=sig.get("signal_tier", 0),
                recommenders=recommenders,
                palette_action=sig.get("palette_action", ""),
            ))
    return hits


def _find_knowledge(data: PISData, riu_id: str) -> list[KnowledgeHit]:
    """Find knowledge entries whose related_rius include this RIU."""
    hits: list[KnowledgeHit] = []
    for entry in data.knowledge.values():
        if riu_id in entry.get("related_rius", []):
            hits.append(KnowledgeHit(
                lib_id=entry["id"],
                question=entry.get("question", "")[:120],
                journey_stage=entry.get("journey_stage", ""),
                has_eval_signal=bool(entry.get("evaluation_signal")),
            ))
    return hits


def traverse(
    data: PISData,
    riu_id: str | None = None,
    lib_id: str | None = None,
    *,
    track_health: bool = True,
) -> TraversalResult:
    """Run a full PIS traversal for a given RIU or knowledge entry."""
    resolved_from: str | None = None

    # ── Resolution ──
    if lib_id and not riu_id:
        resolved_from = lib_id
        primary, _secondary = _resolve_riu_from_lib(data, lib_id)
        if not primary:
            return TraversalResult(
                query_riu=lib_id,
                query_riu_name="(unresolved)",
                resolved_from=lib_id,
                gaps=[f"Knowledge entry {lib_id} not found or has no related_rius"],
                completeness=scoring.compute(False, False, False, False, False, False, False),
                health_status="failing",
            )
        riu_id = primary

    if not riu_id:
        raise ValueError("Either riu_id or lib_id must be provided")

    result = TraversalResult(query_riu=riu_id, query_riu_name="", resolved_from=resolved_from)

    # ── Step 1: Classification ──
    cls_entry = data.classification.get(riu_id)
    has_classification = cls_entry is not None
    if cls_entry:
        result.classification = cls_entry.get("classification", "")
        result.classification_rationale = cls_entry.get("rationale", "").strip()
        result.query_riu_name = cls_entry.get("name", riu_id)
    else:
        result.gaps.append(f"No classification entry for {riu_id}")
        # Try to get name from routing
        routing_entry = data.routing.get(riu_id)
        if routing_entry:
            result.query_riu_name = routing_entry.get("riu_name", riu_id)
        else:
            result.query_riu_name = riu_id

    # ── Step 2: Service routing ──
    routing_entry = data.routing.get(riu_id)
    has_routing = routing_entry is not None and bool(routing_entry.get("services"))
    primary_not_stub = False
    has_recipe = False

    if result.classification == "internal_only":
        result.recommendation = None
        result.gaps.append(f"RIU is internal_only — no external service needed")
    elif routing_entry and has_routing:
        recs = _build_service_recommendations(data, routing_entry)
        if recs:
            result.recommendation = recs[0]
            result.recommendation.why_primary = (
                result.recommendation.why_primary
                or f"Top-ranked service for {riu_id}"
            )
            primary = recs[0]
            for alt in recs[1:]:
                alt.why_not = _explain_why_not(primary, alt)
            result.alternatives = recs[1:]

            primary_not_stub = result.recommendation.integration_status != "no_api"
            has_recipe = result.recommendation.recipe_available

            if not primary_not_stub:
                result.gaps.append(
                    f"Primary service ({result.recommendation.service_name}) has no API"
                )
            if not has_recipe:
                result.gaps.append(
                    f"No integration recipe for {result.recommendation.service_name}"
                )

            # Check if ALL services are no_api
            if all(r.integration_status == "no_api" for r in recs):
                result.gaps.append("All services for this RIU have no_api status")
    else:
        if result.classification != "internal_only":
            result.gaps.append(f"No service routing entry for {riu_id}")

    # ── Step 3: Recipe check already done per-service above ──

    # ── Step 4: People signals ──
    result.signal_validation = _find_signals(data, riu_id)
    has_signal = len(result.signal_validation) > 0
    if not has_signal:
        result.gaps.append(f"No people-library signal validation for {riu_id}")

    # ── Step 5: Knowledge entries ──
    result.knowledge_support = _find_knowledge(data, riu_id)
    has_knowledge = len(result.knowledge_support) > 0
    has_eval_signal = any(k.has_eval_signal for k in result.knowledge_support)
    if not has_knowledge:
        result.gaps.append(f"No knowledge-library entries for {riu_id}")

    # ── Scoring ──
    result.completeness = scoring.compute(
        has_classification=has_classification,
        has_routing=has_routing,
        primary_not_stub=primary_not_stub,
        has_recipe=has_recipe,
        has_signal=has_signal,
        has_knowledge=has_knowledge,
        has_eval_signal=has_eval_signal,
        is_internal_only=(result.classification == "internal_only"),
    )

    # ── Health tracking ──
    if track_health:
        missing_layers: list[str] = []
        if not has_classification:
            missing_layers.append("classification")
        if not has_routing and result.classification != "internal_only":
            missing_layers.append("service_routing")
        if not has_recipe and result.classification != "internal_only":
            missing_layers.append("integration_recipe")
        if not has_signal:
            missing_layers.append("people_signals")
        if not has_knowledge:
            missing_layers.append("knowledge_library")

        result.health_status = record_and_evaluate(
            riu_id=riu_id,
            completeness=result.completeness.total,
            gaps=result.gaps,
            missing_layers=missing_layers,
        )

    return result
