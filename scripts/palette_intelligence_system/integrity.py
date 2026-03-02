"""PIS Cross-Layer Integrity Engine — scan all 117 RIUs across 6 data sources.

Loads taxonomy, classification, knowledge library, service routing, integration
recipes, and people signals.  Resolves every cross-layer relationship, produces
per-RIU integrity cards with completeness scores, runs 8 structural consistency
checks, and outputs a prioritised action list.

Usage:
  python3 -m scripts.palette_intelligence_system.integrity              # full human-readable report
  python3 -m scripts.palette_intelligence_system.integrity --json        # JSON output
  python3 -m scripts.palette_intelligence_system.integrity --riu RIU-082 # single RIU deep dive
  python3 -m scripts.palette_intelligence_system.integrity --gaps-only   # only actionable gaps
  python3 -m scripts.palette_intelligence_system.integrity --checks-only # consistency checks only
  python3 -m scripts.palette_intelligence_system.integrity --both-only   # filter to "both" RIUs
  python3 -m scripts.palette_intelligence_system.integrity --internal-only
  python3 -m scripts.palette_intelligence_system.integrity --weak        # weak + bare completeness
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any

import yaml

from . import score as scoring
from .loader import load_all as _loader_load_all, _palette_root, _load_yaml_docs


# ── Data structures ────────────────────────────────────────────────


@dataclass
class IntegrityData:
    """All 6 PIS data sources + reverse indexes."""
    taxonomy: dict[str, dict] = field(default_factory=dict)        # RIU-XXX → entry
    classification: dict[str, dict] = field(default_factory=dict)  # RIU-XXX → entry
    knowledge: dict[str, dict] = field(default_factory=dict)       # LIB-XXX → entry
    routing: dict[str, dict] = field(default_factory=dict)         # RIU-XXX → routing entry
    recipes: dict[str, dict] = field(default_factory=dict)         # service_name (lowered) → recipe
    signals: list[dict] = field(default_factory=list)              # crossref signal entries
    people: list[dict] = field(default_factory=list)               # people profiles

    # Reverse indexes (built at load time)
    riu_to_knowledge: dict[str, list[str]] = field(default_factory=dict)
    riu_to_signals: dict[str, list[dict]] = field(default_factory=dict)
    riu_to_recipes: dict[str, list[str]] = field(default_factory=dict)
    service_to_recipe: dict[str, str] = field(default_factory=dict)


@dataclass
class ServiceEntry:
    name: str
    quality_tier: str
    integration_status: str
    recipe_available: bool
    recipe_name: str | None = None


@dataclass
class RecipeCoverage:
    service_name: str
    has_recipe: bool
    recipe_key: str | None = None


@dataclass
class SignalEntry:
    tool_name: str
    signal_tier: int
    recommender_names: list[str]
    palette_action: str


@dataclass
class RIUIntegrityCard:
    riu_id: str
    riu_name: str
    classification: str                       # internal_only | both | MISSING
    knowledge_entries: list[str] = field(default_factory=list)
    knowledge_count: int = 0
    services: list[ServiceEntry] = field(default_factory=list)
    recipe_coverage: list[RecipeCoverage] = field(default_factory=list)
    people_signals: list[SignalEntry] = field(default_factory=list)
    completeness: int = 0
    completeness_label: str = "bare"
    gaps: list[str] = field(default_factory=list)
    actions: list[str] = field(default_factory=list)


@dataclass
class ConsistencyResult:
    check_name: str
    passed: int
    total: int
    ok: bool
    details: list[str] = field(default_factory=list)


@dataclass
class IntegrityStats:
    total_rius: int = 0
    classified: int = 0
    internal_only: int = 0
    both: int = 0
    with_knowledge: int = 0
    with_routing: int = 0
    with_recipes: int = 0
    with_signals: int = 0
    avg_completeness: float = 0.0
    full_count: int = 0
    partial_count: int = 0
    weak_count: int = 0
    bare_count: int = 0
    top_gaps: list[tuple[str, int]] = field(default_factory=list)


@dataclass
class IntegrityReport:
    cards: list[RIUIntegrityCard] = field(default_factory=list)
    stats: IntegrityStats = field(default_factory=IntegrityStats)
    consistency_checks: list[ConsistencyResult] = field(default_factory=list)
    timestamp: str = ""


# ── Loading ────────────────────────────────────────────────────────


def _load_taxonomy(root: str) -> dict[str, dict]:
    """Load taxonomy RIUs from v1.3 YAML."""
    path = os.path.join(root, "taxonomy", "releases", "v1.3", "palette_taxonomy_v1.3.yaml")
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    entries: dict[str, dict] = {}
    for item in data.get("rius", []):
        riu_id = item.get("riu_id", "")
        if riu_id:
            entries[riu_id] = item
    return entries


def _load_people(root: str) -> list[dict]:
    """Load people profiles from v1.1 YAML."""
    path = os.path.join(
        root, "buy-vs-build", "people-library", "v1.1",
        "people_library_v1.1.yaml",
    )
    docs = _load_yaml_docs(path)
    profiles: list[dict] = []
    for doc in docs:
        if not isinstance(doc, dict):
            continue
        profiles.extend(doc.get("profiles", []))
    return profiles


# Override registry (loaded once, cached)
_override_cache: dict[str, str] | None = None


def _load_overrides() -> dict[str, str]:
    """Load explicit service→recipe overrides from YAML registry."""
    global _override_cache
    if _override_cache is not None:
        return _override_cache

    override_path = os.path.join(
        _palette_root(), "buy-vs-build", "service-routing", "v1.0",
        "service_recipe_overrides.yaml",
    )
    _override_cache = {}
    if os.path.exists(override_path):
        with open(override_path, "r") as f:
            data = yaml.safe_load(f) or {}
        for entry in data.get("overrides", []):
            svc = entry.get("service_name", "")
            rkey = entry.get("recipe_key", "")
            if svc and rkey:
                _override_cache[svc.lower()] = rkey.lower()
    return _override_cache


def _find_recipe_for_service(recipes: dict[str, dict], service_name: str) -> str | None:
    """Match a service name to a recipe key using overrides then normalised matching."""
    import re

    # Strategy 0: explicit override registry (highest confidence)
    overrides = _load_overrides()
    override_key = overrides.get(service_name.lower())
    if override_key:
        # Check if the override key exists in recipes
        if override_key in recipes:
            return override_key
        # Also check normalised form
        norm_override = re.sub(r"[^a-z0-9]", "", override_key)
        for rkey in recipes:
            if re.sub(r"[^a-z0-9]", "", rkey) == norm_override:
                return rkey

    norm = re.sub(r"[^a-z0-9]", "", service_name.lower())

    # Strategy 1: exact normalised match
    for rkey in recipes:
        rkey_norm = re.sub(r"[^a-z0-9]", "", rkey)
        if rkey_norm == norm:
            return rkey

    # Strategy 2: substring match
    for rkey in recipes:
        rkey_norm = re.sub(r"[^a-z0-9]", "", rkey)
        if len(rkey_norm) >= 4 and (rkey_norm in norm or norm in rkey_norm):
            return rkey

    # Strategy 3: word overlap
    name_words = {w for w in service_name.lower().split() if len(w) > 2}
    for rkey in recipes:
        rkey_words = {w for w in rkey.split() if len(w) > 2}
        if name_words and rkey_words and len(name_words & rkey_words) >= max(len(name_words) // 2, 1):
            return rkey

    return None


def _build_reverse_indexes(data: IntegrityData) -> None:
    """Build reverse indexes for fast lookups."""
    # RIU → knowledge entries
    for lib_id, entry in data.knowledge.items():
        for riu in entry.get("related_rius", []):
            data.riu_to_knowledge.setdefault(riu, []).append(lib_id)

    # RIU → signals
    for sig in data.signals:
        primary = sig.get("riu_primary", "")
        secondary = sig.get("riu_secondary", [])
        if primary:
            data.riu_to_signals.setdefault(primary, []).append(sig)
        for riu in secondary:
            data.riu_to_signals.setdefault(riu, []).append(sig)

    # Service → recipe (normalised)
    for rkey in data.recipes:
        data.service_to_recipe[rkey] = rkey

    # RIU → recipes (via routing services)
    for riu_id, routing_entry in data.routing.items():
        for svc in routing_entry.get("services", []):
            svc_name = svc.get("name", "")
            recipe_key = _find_recipe_for_service(data.recipes, svc_name)
            if recipe_key:
                data.riu_to_recipes.setdefault(riu_id, []).append(recipe_key)


def load_integrity_data(root: str | None = None) -> IntegrityData:
    """Load all 6 PIS data sources into a single structure."""
    root = root or _palette_root()

    # Reuse loader.load_all() for 5 sources
    pis = _loader_load_all(root)

    data = IntegrityData(
        taxonomy=_load_taxonomy(root),
        classification=pis.classification,
        knowledge=pis.knowledge,
        routing=pis.routing,
        recipes=pis.recipes,
        signals=pis.signals,
        people=_load_people(root),
    )

    _build_reverse_indexes(data)
    return data


# ── Per-RIU card builder ──────────────────────────────────────────


def build_card(data: IntegrityData, riu_id: str) -> RIUIntegrityCard:
    """Build a cross-layer integrity card for a single RIU."""
    tax_entry = data.taxonomy.get(riu_id, {})
    cls_entry = data.classification.get(riu_id)
    routing_entry = data.routing.get(riu_id)

    riu_name = tax_entry.get("name", cls_entry.get("name", riu_id) if cls_entry else riu_id)
    classification = cls_entry.get("classification", "MISSING") if cls_entry else "MISSING"

    card = RIUIntegrityCard(
        riu_id=riu_id,
        riu_name=riu_name,
        classification=classification,
    )

    gaps: list[str] = []
    actions: list[str] = []

    # ── Classification ──
    has_classification = cls_entry is not None
    if not has_classification:
        gaps.append("No classification entry")
        actions.append("Add classification to riu_classification_v1.0.yaml")

    is_internal_only = classification == "internal_only"

    # ── Knowledge ──
    knowledge_ids = data.riu_to_knowledge.get(riu_id, [])
    card.knowledge_entries = knowledge_ids
    card.knowledge_count = len(knowledge_ids)
    has_knowledge = card.knowledge_count > 0
    has_eval_signal = False
    if has_knowledge:
        for kid in knowledge_ids:
            entry = data.knowledge.get(kid, {})
            if entry.get("evaluation_signal"):
                has_eval_signal = True
                break
    else:
        gaps.append("No knowledge-library entries")
        actions.append("Add knowledge entry referencing this RIU")

    # ── Routing + services ──
    has_routing = routing_entry is not None and bool(routing_entry.get("services"))
    primary_not_stub = False
    has_recipe = False

    if not is_internal_only:
        if has_routing:
            for svc in routing_entry.get("services", []):
                svc_name = svc.get("name", "")
                recipe_key = _find_recipe_for_service(data.recipes, svc_name)
                recipe_available = recipe_key is not None
                card.services.append(ServiceEntry(
                    name=svc_name,
                    quality_tier=svc.get("quality_tier", "tier_3"),
                    integration_status=svc.get("integration_status", "evaluate"),
                    recipe_available=recipe_available,
                    recipe_name=recipe_key,
                ))
                card.recipe_coverage.append(RecipeCoverage(
                    service_name=svc_name,
                    has_recipe=recipe_available,
                    recipe_key=recipe_key,
                ))
            # Primary service (first after implicit ranking by data order)
            if card.services:
                primary = card.services[0]
                primary_not_stub = primary.integration_status != "no_api"
                has_recipe = any(rc.has_recipe for rc in card.recipe_coverage)

            # Gaps for services without recipes
            missing_recipes = [rc.service_name for rc in card.recipe_coverage if not rc.has_recipe]
            if missing_recipes:
                gaps.append(f"Missing integration recipe for: {', '.join(missing_recipes)}")
                for svc_name in missing_recipes:
                    actions.append(f"Add integration recipe for {svc_name}")
        else:
            gaps.append("No service routing entry (classified as 'both')")
            actions.append("Add routing entry to service_routing_v1.0.yaml")

    # ── People signals ──
    signal_entries = data.riu_to_signals.get(riu_id, [])
    has_signal = len(signal_entries) > 0
    for sig in signal_entries:
        recommenders = [r.get("name", "") for r in sig.get("recommenders", [])]
        card.people_signals.append(SignalEntry(
            tool_name=sig.get("tool", ""),
            signal_tier=sig.get("signal_tier", 0),
            recommender_names=recommenders,
            palette_action=sig.get("palette_action", ""),
        ))
    if not has_signal and not is_internal_only:
        gaps.append("No people signal coverage")
        actions.append("Identify people/tools tracking this RIU")

    # ── Completeness scoring ──
    score = scoring.compute(
        has_classification=has_classification,
        has_routing=has_routing,
        primary_not_stub=primary_not_stub,
        has_recipe=has_recipe,
        has_signal=has_signal,
        has_knowledge=has_knowledge,
        has_eval_signal=has_eval_signal,
        is_internal_only=is_internal_only,
    )
    card.completeness = score.total
    card.completeness_label = score.label
    card.gaps = gaps
    card.actions = actions

    return card


# ── Consistency checks ────────────────────────────────────────────


def _run_consistency_checks(data: IntegrityData) -> list[ConsistencyResult]:
    """Run 8 structural cross-layer consistency checks."""
    checks: list[ConsistencyResult] = []

    # 1. Taxonomy↔Classification: every taxonomy RIU has a classification entry
    tax_ids = set(data.taxonomy.keys())
    cls_ids = set(data.classification.keys())
    missing = sorted(tax_ids - cls_ids)
    checks.append(ConsistencyResult(
        check_name="Taxonomy↔Classification",
        passed=len(tax_ids) - len(missing),
        total=len(tax_ids),
        ok=len(missing) == 0,
        details=[f"{r} missing classification" for r in missing],
    ))

    # 2. Classification↔Routing: every "both" RIU has a routing entry
    both_rius = sorted(
        rid for rid, entry in data.classification.items()
        if entry.get("classification") == "both"
    )
    both_with_routing = [r for r in both_rius if r in data.routing]
    missing_routing = [r for r in both_rius if r not in data.routing]
    checks.append(ConsistencyResult(
        check_name="Classification↔Routing",
        passed=len(both_with_routing),
        total=len(both_rius),
        ok=len(missing_routing) == 0,
        details=[f"{r} classified 'both' but no routing entry" for r in missing_routing],
    ))

    # 3. Routing↔Recipe: every service in routing has a matching recipe
    total_services = 0
    services_with_recipe = 0
    missing_recipe_details: list[str] = []
    for riu_id, routing_entry in sorted(data.routing.items()):
        for svc in routing_entry.get("services", []):
            total_services += 1
            svc_name = svc.get("name", "")
            if _find_recipe_for_service(data.recipes, svc_name):
                services_with_recipe += 1
            else:
                missing_recipe_details.append(f"{svc_name} ({riu_id})")
    checks.append(ConsistencyResult(
        check_name="Routing↔Recipe",
        passed=services_with_recipe,
        total=total_services,
        ok=len(missing_recipe_details) == 0,
        details=missing_recipe_details,
    ))

    # 4. Signals↔Taxonomy: every riu_primary in signals exists in taxonomy
    signal_rius: list[str] = []
    invalid_signal_rius: list[str] = []
    for sig in data.signals:
        primary = sig.get("riu_primary", "")
        if primary:
            signal_rius.append(primary)
            if primary not in data.taxonomy:
                invalid_signal_rius.append(f"{primary} (tool: {sig.get('tool', '?')})")
    checks.append(ConsistencyResult(
        check_name="Signals↔Taxonomy",
        passed=len(signal_rius) - len(invalid_signal_rius),
        total=len(signal_rius),
        ok=len(invalid_signal_rius) == 0,
        details=invalid_signal_rius,
    ))

    # 5. Knowledge↔Taxonomy: every related_rius reference exists in taxonomy
    total_refs = 0
    invalid_refs: list[str] = []
    for lib_id, entry in data.knowledge.items():
        for riu in entry.get("related_rius", []):
            total_refs += 1
            if riu not in data.taxonomy:
                invalid_refs.append(f"{riu} (from {lib_id})")
    checks.append(ConsistencyResult(
        check_name="Knowledge↔Taxonomy",
        passed=total_refs - len(invalid_refs),
        total=total_refs,
        ok=len(invalid_refs) == 0,
        details=invalid_refs,
    ))

    # 6. Orphan recipes: recipes not matching any service in routing
    all_routing_services: set[str] = set()
    for routing_entry in data.routing.values():
        for svc in routing_entry.get("services", []):
            all_routing_services.add(svc.get("name", ""))
    orphan_recipes: list[str] = []
    for rkey in sorted(data.recipes.keys()):
        matched = False
        for svc_name in all_routing_services:
            if _find_recipe_for_service({rkey: data.recipes[rkey]}, svc_name):
                matched = True
                break
        if not matched:
            orphan_recipes.append(rkey)
    checks.append(ConsistencyResult(
        check_name="Orphan recipes",
        passed=len(data.recipes) - len(orphan_recipes),
        total=len(data.recipes),
        ok=len(orphan_recipes) == 0,
        details=[f"Recipe '{r}' not matched by any routing service" for r in orphan_recipes],
    ))

    # 7. Orphan signals: signals referencing RIUs not in taxonomy
    orphan_signals: list[str] = []
    for sig in data.signals:
        primary = sig.get("riu_primary", "")
        if primary and primary not in data.taxonomy:
            orphan_signals.append(f"{sig.get('tool', '?')} → {primary}")
        for sec in sig.get("riu_secondary", []):
            if sec not in data.taxonomy:
                orphan_signals.append(f"{sig.get('tool', '?')} → {sec} (secondary)")
    checks.append(ConsistencyResult(
        check_name="Orphan signals",
        passed=len(data.signals) - len(orphan_signals),
        total=len(data.signals),
        ok=len(orphan_signals) == 0,
        details=orphan_signals,
    ))

    # 8. People↔Signals: every tool mentioned in people profiles appears in signals crossref
    signal_tools = {sig.get("tool", "").lower() for sig in data.signals}
    people_tools: set[str] = set()
    missing_people_tools: list[str] = []
    for profile in data.people:
        for tool_entry in profile.get("tools_mentioned", []):
            tool_name = tool_entry if isinstance(tool_entry, str) else tool_entry.get("name", "")
            if tool_name:
                people_tools.add(tool_name.lower())
                if tool_name.lower() not in signal_tools:
                    missing_people_tools.append(f"{tool_name} (from {profile.get('id', '?')})")
    checks.append(ConsistencyResult(
        check_name="People↔Signals",
        passed=len(people_tools) - len(set(t.split(" (from")[0].lower() for t in missing_people_tools)),
        total=len(people_tools) if people_tools else len(data.people),
        ok=len(missing_people_tools) == 0,
        details=missing_people_tools,
    ))

    return checks


# ── Stats computation ─────────────────────────────────────────────


def _compute_stats(cards: list[RIUIntegrityCard]) -> IntegrityStats:
    """Compute aggregate statistics from integrity cards."""
    stats = IntegrityStats(total_rius=len(cards))

    gap_counter: dict[str, int] = {}

    for card in cards:
        if card.classification != "MISSING":
            stats.classified += 1
        if card.classification == "internal_only":
            stats.internal_only += 1
        elif card.classification == "both":
            stats.both += 1
        if card.knowledge_count > 0:
            stats.with_knowledge += 1
        if card.services:
            stats.with_routing += 1
        if any(rc.has_recipe for rc in card.recipe_coverage):
            stats.with_recipes += 1
        if card.people_signals:
            stats.with_signals += 1

        if card.completeness_label == "full":
            stats.full_count += 1
        elif card.completeness_label == "partial":
            stats.partial_count += 1
        elif card.completeness_label == "weak":
            stats.weak_count += 1
        else:
            stats.bare_count += 1

        for gap in card.gaps:
            # Normalise gap text for counting
            key = gap.split(":")[0].strip() if ":" in gap else gap
            gap_counter[key] = gap_counter.get(key, 0) + 1

    if cards:
        stats.avg_completeness = round(sum(c.completeness for c in cards) / len(cards), 1)

    stats.top_gaps = sorted(gap_counter.items(), key=lambda x: -x[1])[:10]

    return stats


# ── Core engine ───────────────────────────────────────────────────


def scan_all(data: IntegrityData) -> IntegrityReport:
    """Scan all RIUs and produce cross-layer integrity report."""
    cards = []
    for riu_id in sorted(data.taxonomy.keys()):
        card = build_card(data, riu_id)
        cards.append(card)

    return IntegrityReport(
        cards=cards,
        stats=_compute_stats(cards),
        consistency_checks=_run_consistency_checks(data),
        timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    )


def scan_single(data: IntegrityData, riu_id: str) -> IntegrityReport:
    """Scan a single RIU and produce a focused report."""
    if riu_id not in data.taxonomy:
        print(f"ERROR: {riu_id} not found in taxonomy", file=sys.stderr)
        sys.exit(1)
    card = build_card(data, riu_id)
    return IntegrityReport(
        cards=[card],
        stats=_compute_stats([card]),
        consistency_checks=[],
        timestamp=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    )


# ── Human-readable output ────────────────────────────────────────


def _bar(count: int, max_count: int, width: int = 20) -> str:
    """Render a simple bar chart."""
    if max_count == 0:
        return "░" * width
    filled = round(count / max_count * width)
    return "█" * filled + "░" * (width - filled)


def _format_card(card: RIUIntegrityCard, verbose: bool = True) -> str:
    """Format a single RIU integrity card for human output."""
    lines: list[str] = []
    lines.append(
        f"{card.riu_id} {card.riu_name}"
        f"    completeness: {card.completeness}/100 [{card.completeness_label}]"
    )
    lines.append(f"  classification: {card.classification}")

    if card.knowledge_entries:
        lines.append(f"  knowledge: {', '.join(card.knowledge_entries)}")
    else:
        lines.append("  knowledge: (none)")

    if card.services:
        svc_parts = []
        for svc in card.services:
            status_tag = f" ({svc.integration_status})" if svc.integration_status != "integrated" else ""
            svc_parts.append(f"{svc.name}{status_tag}")
        lines.append(f"  routing: {', '.join(svc_parts)}")
    elif card.classification == "both":
        lines.append("  routing: (none — MISSING)")

    if card.recipe_coverage:
        rc_parts = []
        for rc in card.recipe_coverage:
            mark = "✓" if rc.has_recipe else "✗"
            rc_parts.append(f"{rc.service_name} {mark}")
        lines.append(f"  recipes: {', '.join(rc_parts)}")

    if card.people_signals:
        sig_parts = []
        for sig in card.people_signals:
            names = ", ".join(sig.recommender_names[:3])
            sig_parts.append(f"{sig.tool_name} [{names}]")
        lines.append(f"  signals: {'; '.join(sig_parts)}")
    elif card.classification == "both":
        lines.append("  signals: (none)")

    if card.gaps:
        lines.append("  GAPS:")
        for g in card.gaps:
            lines.append(f"    → {g}")

    if verbose and card.actions:
        lines.append("  ACTIONS:")
        for a in card.actions:
            lines.append(f"    → {a}")

    return "\n".join(lines)


def _format_report(report: IntegrityReport, *, gaps_only: bool = False,
                   checks_only: bool = False) -> str:
    """Format the full integrity report for human output."""
    lines: list[str] = []
    s = report.stats

    lines.append("═" * 60)
    lines.append("  PIS CROSS-LAYER INTEGRITY REPORT")
    lines.append(f"  {report.timestamp} | {s.total_rius} RIUs scanned")
    lines.append("═" * 60)

    if not checks_only:
        lines.append("")
        lines.append("AGGREGATE")
        lines.append(f"  Classification:  {s.classified}/{s.total_rius} ({_pct(s.classified, s.total_rius)})")
        lines.append(f"  Internal-only:   {s.internal_only} | Both: {s.both}")
        lines.append(f"  Knowledge:       {s.with_knowledge}/{s.total_rius} RIUs have ≥1 entry ({_pct(s.with_knowledge, s.total_rius)})")
        if s.both > 0:
            lines.append(f"  Routing:         {s.with_routing}/{s.both} \"both\" RIUs covered ({_pct(s.with_routing, s.both)})")
            lines.append(f"  Recipes:         {s.with_recipes}/{s.both} \"both\" RIUs have ≥1 recipe ({_pct(s.with_recipes, s.both)})")
            lines.append(f"  People signals:  {s.with_signals}/{s.both} \"both\" RIUs have signal coverage ({_pct(s.with_signals, s.both)})")
        lines.append(f"  Avg completeness: {s.avg_completeness}/100")
        lines.append("")

        max_dist = max(s.full_count, s.partial_count, s.weak_count, s.bare_count, 1)
        lines.append("  Completeness distribution:")
        lines.append(f"    full (≥85):     {s.full_count:3d}  {_bar(s.full_count, max_dist)}")
        lines.append(f"    partial (60-84): {s.partial_count:2d}  {_bar(s.partial_count, max_dist)}")
        lines.append(f"    weak (30-59):   {s.weak_count:3d}  {_bar(s.weak_count, max_dist)}")
        lines.append(f"    bare (<30):     {s.bare_count:3d}  {_bar(s.bare_count, max_dist)}")

    # Consistency checks
    if report.consistency_checks:
        lines.append("")
        lines.append("CONSISTENCY CHECKS")
        for check in report.consistency_checks:
            mark = "✓" if check.ok else "✗"
            lines.append(f"  {mark} {check.check_name}: {check.passed}/{check.total}")
            if not check.ok and check.details:
                for d in check.details[:5]:
                    lines.append(f"      {d}")
                if len(check.details) > 5:
                    lines.append(f"      ... and {len(check.details) - 5} more")

    if not checks_only:
        # Top gaps
        if s.top_gaps:
            lines.append("")
            lines.append("TOP GAPS (by frequency)")
            for i, (gap, count) in enumerate(s.top_gaps[:10], 1):
                lines.append(f"  {i}. {gap} ({count} RIUs)")

        # Cards
        if not gaps_only:
            # Show "both" cards first (sorted by completeness ascending), then internal_only
            both_cards = sorted(
                [c for c in report.cards if c.classification == "both"],
                key=lambda c: c.completeness,
            )
            internal_cards = sorted(
                [c for c in report.cards if c.classification == "internal_only"],
                key=lambda c: c.completeness,
            )

            if both_cards:
                lines.append("")
                lines.append("═" * 60)
                lines.append("  CARDS: \"both\" RIUs (sorted by completeness, ascending)")
                lines.append("═" * 60)
                for card in both_cards:
                    lines.append("")
                    lines.append(_format_card(card))

            if internal_cards:
                lines.append("")
                lines.append("═" * 60)
                lines.append("  CARDS: \"internal_only\" RIUs (sorted by completeness, ascending)")
                lines.append("═" * 60)
                for card in internal_cards:
                    lines.append("")
                    lines.append(_format_card(card, verbose=False))
        else:
            # Gaps-only mode: show only cards that have gaps
            gap_cards = [c for c in report.cards if c.gaps]
            gap_cards.sort(key=lambda c: c.completeness)
            lines.append("")
            lines.append("═" * 60)
            lines.append(f"  RIUs WITH GAPS ({len(gap_cards)} of {s.total_rius})")
            lines.append("═" * 60)
            for card in gap_cards:
                lines.append("")
                lines.append(_format_card(card))

    lines.append("")
    return "\n".join(lines)


def _pct(n: int, total: int) -> str:
    if total == 0:
        return "0%"
    return f"{round(n / total * 100)}%"


# ── JSON output ───────────────────────────────────────────────────


def _to_json(report: IntegrityReport) -> str:
    """Serialize report to JSON."""
    def _default(obj: Any) -> Any:
        if hasattr(obj, "__dict__"):
            return obj.__dict__
        return str(obj)

    return json.dumps(asdict(report), indent=2, default=_default, ensure_ascii=False)


# ── CLI ───────────────────────────────────────────────────────────


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PIS Cross-Layer Integrity Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--riu", type=str, help="Single RIU deep dive (e.g., RIU-082)")
    parser.add_argument("--gaps-only", action="store_true", help="Only show RIUs with gaps")
    parser.add_argument("--checks-only", action="store_true", help="Only show consistency checks")
    parser.add_argument("--both-only", action="store_true", help="Filter to 'both' RIUs only")
    parser.add_argument("--internal-only", action="store_true", help="Filter to 'internal_only' RIUs only")
    parser.add_argument("--weak", action="store_true", help="Show weak + bare completeness only")
    args = parser.parse_args()

    data = load_integrity_data()

    if args.riu:
        report = scan_single(data, args.riu)
    else:
        report = scan_all(data)

    # Apply filters
    if args.both_only:
        report.cards = [c for c in report.cards if c.classification == "both"]
        report.stats = _compute_stats(report.cards)
    elif args.internal_only:
        report.cards = [c for c in report.cards if c.classification == "internal_only"]
        report.stats = _compute_stats(report.cards)

    if args.weak:
        report.cards = [c for c in report.cards if c.completeness_label in ("weak", "bare")]
        report.stats = _compute_stats(report.cards)

    if args.json:
        print(_to_json(report))
    else:
        print(_format_report(report, gaps_only=args.gaps_only, checks_only=args.checks_only))


if __name__ == "__main__":
    main()
