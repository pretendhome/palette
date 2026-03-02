"""Completeness scoring for a PIS traversal result."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CompletenessScore:
    total: int            # 0–100
    label: str            # full | partial | weak | bare
    components: dict[str, bool]


def _label(total: int) -> str:
    if total >= 85:
        return "full"
    if total >= 60:
        return "partial"
    if total >= 30:
        return "weak"
    return "bare"


def compute(
    has_classification: bool,
    has_routing: bool,
    primary_not_stub: bool,
    has_recipe: bool,
    has_signal: bool,
    has_knowledge: bool,
    has_eval_signal: bool,
    is_internal_only: bool = False,
) -> CompletenessScore:
    if is_internal_only:
        # Internal-only RIUs don't need routing, recipes, or signals.
        # Score only on what's relevant: classification + knowledge.
        components = {
            "riu_classified": has_classification,
            "knowledge_support_exists": has_knowledge,
            "eval_signal_present": has_eval_signal,
        }
        weights = {
            "riu_classified": 30,
            "knowledge_support_exists": 45,
            "eval_signal_present": 25,
        }
    else:
        components = {
            "riu_classified": has_classification,
            "routing_entry_exists": has_routing,
            "primary_service_not_stub": primary_not_stub,
            "recipe_available": has_recipe,
            "signal_validation_exists": has_signal,
            "knowledge_support_exists": has_knowledge,
            "eval_signal_present": has_eval_signal,
        }
        weights = {
            "riu_classified": 10,
            "routing_entry_exists": 20,
            "primary_service_not_stub": 15,
            "recipe_available": 15,
            "signal_validation_exists": 15,
            "knowledge_support_exists": 15,
            "eval_signal_present": 10,
        }
    total = sum(weights[k] for k, v in components.items() if v)
    return CompletenessScore(total=total, label=_label(total), components=components)
