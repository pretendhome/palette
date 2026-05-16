#!/usr/bin/env python3
"""
Tech Engine v1.1 — PIS-Powered Tech Intelligence + Disruption Theses for Telegram

Reads the Palette Intelligence System (PIS) people library, company signals,
and disruption theses (from AI Council conference intelligence).
READ-ONLY — never modifies PIS files.

Generates tech briefs showing:
  - What trusted practitioners are using and recommending
  - Tier 1/2/3 tool landscape with palette actions
  - Per-cluster signal summaries
  - Perplexity queries ready to run for live updates
  - Disruption theses: where big tech is vulnerable, who benefits
  - Morning disruption brief: what an investor should know today

Usage:
  CLI:      python3 tech_engine.py --brief
  CLI:      python3 tech_engine.py --query "voice AI tools"
  CLI:      python3 tech_engine.py --cluster lovable_orbit
  CLI:      python3 tech_engine.py --tier 1
  CLI:      python3 tech_engine.py --action evaluate
  CLI:      python3 tech_engine.py --disruption           # all theses summary
  CLI:      python3 tech_engine.py --thesis DISRUPT-CLOUD-PEAK
  CLI:      python3 tech_engine.py --vulnerable            # most exposed companies
  CLI:      python3 tech_engine.py --morning               # morning investor brief
  Bot:      Called by joseph_bridge.py when user sends /tech
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

# PIS paths — READ ONLY
BUY_VS_BUILD = Path(__file__).parent.parent
TECH_DIR = Path(__file__).parent
PEOPLE_LIB = BUY_VS_BUILD / "people-library" / "v1.1" / "people_library_v1.1.yaml"
COMPANY_SIG = BUY_VS_BUILD / "people-library" / "v1.1" / "people_library_company_signals_v1.1.yaml"
PIS_ARCH = BUY_VS_BUILD / "PALETTE_INTELLIGENCE_SYSTEM_v1.0.md"
DISRUPTION_THESES = TECH_DIR / "disruption_theses.yaml"


def load_yaml_multi(path: Path) -> dict:
    """Load a YAML file that may have multi-document separators."""
    with open(path) as f:
        content = f.read()
    # Handle multi-doc YAML by merging documents
    docs = list(yaml.safe_load_all(content))
    merged = {}
    for doc in docs:
        if doc:
            merged.update(doc)
    return merged


def load_people() -> list[dict]:
    """Load PIS people library profiles."""
    data = load_yaml_multi(PEOPLE_LIB)
    return data.get("profiles", [])


def load_signals() -> dict:
    """Load PIS company signals."""
    data = load_yaml_multi(COMPANY_SIG)
    return data


# ═══════════════════════════════════════════════════════════════
# TECH BRIEF — full landscape summary
# ═══════════════════════════════════════════════════════════════


def generate_brief() -> str:
    """Generate a full tech landscape brief from PIS data."""
    people = load_people()
    sig_data = load_signals()
    signals = sig_data.get("signals", [])
    actions = sig_data.get("actions_summary", {})
    gaps = sig_data.get("taxonomy_gaps", [])

    active = [p for p in people if p.get("status") != "archived"]

    lines = []
    lines.append("# Tech Intelligence Brief")
    lines.append(f"**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append(f"**Source**: PIS v1.1 — {len(active)} active voices, {len(signals)} tools tracked")
    lines.append("")

    # Tier 1 tools
    tier1 = [s for s in signals if s.get("signal_tier") == 1]
    lines.append("## Tier 1 Tools (High Signal)")
    for t in tier1:
        tool = t.get("tool", "?")
        action = t.get("palette_action", "?")
        recs = t.get("recommenders", [])
        rec_names = ", ".join(r.get("name", "?") for r in recs[:3])
        strength = t.get("aggregate_signal_strength", "?")
        lines.append(f"- **{tool}** — action: `{action}` | signal: {strength}")
        lines.append(f"  Recommended by: {rec_names}")
        note = t.get("palette_note", "")
        if note:
            lines.append(f"  Note: {note[:120]}")
        lines.append("")

    # Actions summary
    lines.append("## Action Summary")
    for action_type in ["integrate", "evaluate", "monitor", "skip"]:
        a = actions.get(action_type, {})
        tools = a.get("tools", [])
        if tools:
            lines.append(f"**{action_type.upper()}** ({a.get('count', len(tools))}): {', '.join(tools[:8])}")
    lines.append("")

    # Taxonomy gaps
    if gaps:
        lines.append("## Taxonomy Gaps")
        for g in gaps:
            lines.append(f"- **{g.get('title', '?')}** — affected: {', '.join(g.get('affected_tools', []))}")
            lines.append(f"  Proposed: {g.get('proposed_name', '?')} ({g.get('proposed_riu', '?')})")
        lines.append("")

    # Clusters
    lines.append("## Voice Clusters")
    clusters = {}
    for p in active:
        # Try to determine cluster from profile structure
        cluster = _get_cluster(p)
        clusters.setdefault(cluster, []).append(p)

    for cluster_name, members in clusters.items():
        display = cluster_name.replace("_", " ").title()
        names = ", ".join(p.get("name", "?") for p in members)
        lines.append(f"- **{display}**: {names}")
    lines.append("")

    # Top research queries
    lines.append("## Ready-to-Run Research Queries")
    for p in active[:8]:
        lens = p.get("lens", {})
        focus = lens.get("focus", "")
        name = p.get("name", "?")
        if focus:
            lines.append(f"- {name}: _{focus}_")
    lines.append("")

    return "\n".join(lines)


def _get_cluster(profile: dict) -> str:
    """Extract cluster name from profile metadata."""
    # Check for explicit cluster fields
    palette_rel = profile.get("palette_relevance", {})
    if isinstance(palette_rel, dict):
        why = palette_rel.get("why_follow", "")
        if "Lovable" in why:
            return "lovable_orbit"

    # Fallback: derive from affiliation
    aff = profile.get("affiliation", {})
    company = ""
    if isinstance(aff, dict):
        company = aff.get("primary_company", aff.get("company", ""))
    elif isinstance(aff, str):
        company = aff

    name = profile.get("name", "")

    # Match to known clusters
    if name in ("Ruben Hassid", "Anisha Jain", "Axelle Malek", "Maria Malonzo"):
        return "ruben_hassid_network"
    if name in ("Anton Osika", "Felix Haas", "Oskar Elvhage", "Joel Nordström"):
        return "lovable_orbit"
    if name in ("Tanay Kothari", "Victoria Liang"):
        return "wispr_flow_orbit"
    if name in ("Olivia Moore", "Filip Mark", "Guillermo Rauch"):
        return "vc_infrastructure_lens"
    if name in ("Alex Patrascu", "Sebastien Jefferies"):
        return "ai_creative_tools"
    if name in ("Andrej Karpathy", "Chip Huyen"):
        return "frontier_ai_engineering"
    if name in ("Matthieu Lorrain", "PJ Accetturo"):
        return "ai_production_commercial"

    return "other"


# ═══════════════════════════════════════════════════════════════
# QUERY — search PIS for specific topic
# ═══════════════════════════════════════════════════════════════


def query_tech(query: str, use_perplexity: bool = False) -> str:
    """Query PIS data for a specific tech topic."""
    people = load_people()
    sig_data = load_signals()
    signals = sig_data.get("signals", [])
    query_lower = query.lower()

    lines = []
    lines.append(f"# Tech Intel: {query}")
    lines.append(f"**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")

    # Search tools
    matching_tools = []
    for s in signals:
        searchable = " ".join([
            s.get("tool", ""),
            s.get("palette_note", ""),
            s.get("company", ""),
            " ".join(s.get("riu_name", "").split()),
            " ".join(r.get("reason", "") for r in s.get("recommenders", [])),
        ]).lower()
        score = sum(1 for w in query_lower.split() if len(w) > 2 and w in searchable)
        if score > 0:
            matching_tools.append((score, s))

    matching_tools.sort(key=lambda x: x[0], reverse=True)

    # Search people
    matching_people = []
    for p in people:
        if p.get("status") == "archived":
            continue
        searchable = " ".join([
            p.get("name", ""),
            " ".join(p.get("expertise_tags", [])),
            p.get("lens", {}).get("focus", ""),
            " ".join(p.get("lens", {}).get("activate_when", [])),
        ]).lower()
        score = sum(1 for w in query_lower.split() if len(w) > 2 and w in searchable)
        if score > 0:
            matching_people.append((score, p))

    matching_people.sort(key=lambda x: x[0], reverse=True)

    if not matching_tools and not matching_people:
        lines.append("No matches in PIS. Try broader terms or `/tech brief` for full landscape.")
        return "\n".join(lines)

    # Show matching tools
    if matching_tools:
        lines.append("## Matching Tools")
        for _, t in matching_tools[:6]:
            tool = t.get("tool", "?")
            tier = t.get("signal_tier", "?")
            action = t.get("palette_action", "?")
            strength = t.get("aggregate_signal_strength", "?")
            recs = ", ".join(r.get("name", "?") for r in t.get("recommenders", [])[:3])
            lines.append(f"- **{tool}** (Tier {tier}) — action: `{action}`, signal: {strength}")
            lines.append(f"  Recommenders: {recs}")
            note = t.get("palette_note", "")
            if note:
                lines.append(f"  {note[:150]}")
            lines.append("")

    # Show matching people
    if matching_people:
        lines.append("## Relevant Voices")
        for _, p in matching_people[:5]:
            name = p.get("name", "?")
            signal = p.get("signal_quality", "?")
            lens = p.get("lens", {})
            focus = lens.get("focus", "")
            lines.append(f"- **{name}** (signal: {signal})")
            if focus:
                lines.append(f"  Focus: {focus}")
            lines.append("")

    # Perplexity search
    if use_perplexity:
        lines.append("## Live Research")
        result = _perplexity_search(query)
        if result:
            lines.append(result.get("content", "No results."))
            cites = result.get("citations", [])
            if cites:
                lines.append("\n**Sources:**")
                for i, c in enumerate(cites[:5], 1):
                    if isinstance(c, str):
                        lines.append(f"  {i}. {c}")
        else:
            lines.append("Perplexity unavailable.")
        lines.append("")

    # Follow-up queries
    if matching_people:
        lines.append("## Research Queries")
        for _, p in matching_people[:3]:
            lens = p.get("lens", {})
            focus = lens.get("focus", "")
            if focus:
                lines.append(f"- {p.get('name', '?')}: _{focus}_")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# TIER / ACTION / CLUSTER lookups
# ═══════════════════════════════════════════════════════════════


def list_by_tier(tier: int) -> str:
    """List all tools at a specific signal tier."""
    sig_data = load_signals()
    signals = sig_data.get("signals", [])
    matching = [s for s in signals if s.get("signal_tier") == tier]

    lines = [f"# Tier {tier} Tools ({len(matching)} total)", ""]
    for t in matching:
        tool = t.get("tool", "?")
        action = t.get("palette_action", "?")
        recs = ", ".join(r.get("name", "?") for r in t.get("recommenders", [])[:3])
        lines.append(f"- **{tool}** — `{action}` — {recs}")

    return "\n".join(lines)


def list_by_action(action: str) -> str:
    """List all tools with a specific palette action."""
    sig_data = load_signals()
    signals = sig_data.get("signals", [])
    matching = [s for s in signals if s.get("palette_action") == action]

    lines = [f"# Action: {action.upper()} ({len(matching)} tools)", ""]
    for t in matching:
        tool = t.get("tool", "?")
        tier = t.get("signal_tier", "?")
        recs = ", ".join(r.get("name", "?") for r in t.get("recommenders", [])[:3])
        lines.append(f"- **{tool}** (Tier {tier}) — {recs}")

    return "\n".join(lines)


def list_cluster(cluster: str) -> str:
    """List all people in a specific cluster."""
    people = load_people()
    active = [p for p in people if p.get("status") != "archived"]

    matching = [p for p in active if _get_cluster(p) == cluster]

    if not matching:
        return f"No profiles found for cluster: {cluster}"

    display = cluster.replace("_", " ").title()
    lines = [f"# Cluster: {display} ({len(matching)} voices)", ""]
    for p in matching:
        name = p.get("name", "?")
        signal = p.get("signal_quality", "?")
        lens = p.get("lens", {})
        focus = lens.get("focus", "")

        # Get tool recommendations
        recs = p.get("notable_recommendations", {})
        tools = recs.get("tools", []) if isinstance(recs, dict) else []
        tool_names = ", ".join(t.get("name", "?") for t in tools[:5] if isinstance(t, dict))

        lines.append(f"## {name} (signal: {signal})")
        if focus:
            lines.append(f"Focus: {focus}")
        if tool_names:
            lines.append(f"Recommends: {tool_names}")
        lines.append("")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# DISRUPTION THESES — Conference-derived investment intelligence
# ═══════════════════════════════════════════════════════════════


def load_theses() -> list[dict]:
    """Load disruption theses from YAML."""
    if not DISRUPTION_THESES.exists():
        return []
    with open(DISRUPTION_THESES) as f:
        data = yaml.safe_load(f) or {}
    return data.get("theses", [])


def disruption_brief() -> str:
    """Generate a summary of all disruption theses — the morning overview."""
    theses = load_theses()
    if not theses:
        return "No disruption theses loaded. Check disruption_theses.yaml."

    lines = [
        "# Disruption Radar",
        f"**{len(theses)} active theses** | Source: AI Council May 2026 + global inference",
        "",
    ]

    # Group by confidence
    very_high = [t for t in theses if t.get("confidence") == "very_high"]
    high = [t for t in theses if t.get("confidence") == "high"]
    medium = [t for t in theses if t.get("confidence") in ("medium", "medium-high")]

    if very_high:
        lines.append("## VERY HIGH CONFIDENCE")
        for t in very_high:
            lines.append(f"- **{t['name']}** ({t['id']})")
            lines.append(f"  _{t.get('morning_brief', '')[:200]}_")
            lines.append("")

    if high:
        lines.append("## HIGH CONFIDENCE")
        for t in high:
            lines.append(f"- **{t['name']}** ({t['id']})")
            lines.append(f"  _{t.get('morning_brief', '')[:200]}_")
            lines.append("")

    if medium:
        lines.append("## MEDIUM CONFIDENCE")
        for t in medium:
            lines.append(f"- **{t['name']}** ({t['id']})")
            lines.append(f"  _{t.get('morning_brief', '')[:200]}_")
            lines.append("")

    lines.append(f"Use `/tech thesis <ID>` to deep-dive any thesis.")
    return "\n".join(lines)


def lookup_thesis(thesis_id: str) -> str:
    """Deep-dive a specific disruption thesis."""
    theses = load_theses()
    thesis_id_upper = thesis_id.upper()

    thesis = None
    for t in theses:
        if t["id"] == thesis_id_upper:
            thesis = t
            break

    if not thesis:
        # Try fuzzy match on name keywords
        query_words = set(thesis_id.lower().split("-"))
        for t in theses:
            name_words = set(t["name"].lower().split())
            if len(query_words & name_words) >= 2:
                thesis = t
                break

    if not thesis:
        ids = ", ".join(t["id"] for t in theses)
        return f"Thesis not found: {thesis_id}\n\nAvailable: {ids}"

    lines = [
        f"# {thesis['name']}",
        f"**ID**: {thesis['id']}",
        f"**Direction**: {thesis.get('direction', '?')}",
        f"**Timeframe**: {thesis.get('timeframe', '?')}",
        f"**Confidence**: {thesis.get('confidence', '?')}",
        "",
        f"## Thesis",
        thesis.get("thesis", ""),
        "",
    ]

    # Evidence
    evidence = thesis.get("evidence", [])
    if evidence:
        lines.append(f"## Evidence ({len(evidence)} signals)")
        for e in evidence[:6]:
            session = e.get("session", "?")
            speaker = e.get("speaker", "?")
            quote = e.get("quote", "")
            lines.append(f"- **{session}** ({speaker}): \"{quote[:150]}\"")
        lines.append("")

    # Exposed
    exposed = thesis.get("exposed_companies", [])
    if exposed:
        lines.append(f"## Exposed Companies ({len(exposed)})")
        for c in exposed:
            ticker = c.get("ticker", "")
            ticker_str = f" [{ticker}]" if ticker and ticker != "various" else ""
            lines.append(f"- **{c['name']}**{ticker_str}")
            lines.append(f"  Risk: {c.get('risk', '?')}")
            detail = c.get("detail", "")
            if detail:
                lines.append(f"  {detail[:200]}")
            lines.append("")

    # Beneficiaries
    beneficiaries = thesis.get("beneficiaries", [])
    if beneficiaries:
        lines.append(f"## Beneficiaries ({len(beneficiaries)})")
        for b in beneficiaries:
            ticker = b.get("ticker", "")
            ticker_str = f" [{ticker}]" if ticker and ticker not in ("private", "private/open-source") else " (private)"
            lines.append(f"- **{b['name']}**{ticker_str}")
            lines.append(f"  {b.get('why', '?')[:200]}")
            lines.append("")

    # Watchlist
    triggers = thesis.get("watchlist_triggers", [])
    if triggers:
        lines.append("## Watchlist Triggers")
        for trigger in triggers:
            lines.append(f"- {trigger}")
        lines.append("")

    return "\n".join(lines)


def vulnerable_companies() -> str:
    """List all companies exposed across all disruption theses, ranked by exposure count."""
    theses = load_theses()
    exposure_map: dict[str, list[dict]] = {}

    for t in theses:
        for c in t.get("exposed_companies", []):
            name = c.get("name", "Unknown")
            if name.startswith("Every ") or name.startswith("Any ") or name.startswith("Companies "):
                continue  # skip generic entries
            key = name
            exposure_map.setdefault(key, []).append({
                "thesis": t["id"],
                "thesis_name": t["name"],
                "risk": c.get("risk", ""),
                "ticker": c.get("ticker", ""),
            })

    if not exposure_map:
        return "No company-level exposures found."

    # Sort by number of theses they appear in
    ranked = sorted(exposure_map.items(), key=lambda x: len(x[1]), reverse=True)

    lines = [
        "# Most Vulnerable Companies",
        f"Ranked by number of disruption theses they're exposed to",
        "",
    ]

    for name, exposures in ranked:
        ticker = exposures[0].get("ticker", "")
        ticker_str = f" [{ticker}]" if ticker and ticker != "various" else ""
        lines.append(f"## {name}{ticker_str} — {len(exposures)} exposure(s)")
        for exp in exposures:
            lines.append(f"- **{exp['thesis_name']}**: {exp['risk'][:150]}")
        lines.append("")

    return "\n".join(lines)


def beneficiary_companies() -> str:
    """List all companies that benefit across disruption theses, ranked by frequency."""
    theses = load_theses()
    benefit_map: dict[str, list[dict]] = {}

    for t in theses:
        for b in t.get("beneficiaries", []):
            name = b.get("name", "Unknown")
            key = name
            benefit_map.setdefault(key, []).append({
                "thesis": t["id"],
                "thesis_name": t["name"],
                "why": b.get("why", ""),
                "ticker": b.get("ticker", ""),
            })

    ranked = sorted(benefit_map.items(), key=lambda x: len(x[1]), reverse=True)

    lines = [
        "# Top Beneficiary Companies",
        f"Ranked by number of disruption theses they benefit from",
        "",
    ]

    for name, benefits in ranked[:20]:
        ticker = benefits[0].get("ticker", "")
        ticker_str = f" [{ticker}]" if ticker and ticker not in ("private", "private/open-source", "various", "") else ""
        if not ticker_str and ticker in ("private", "private/open-source"):
            ticker_str = " (private)"
        lines.append(f"## {name}{ticker_str} — benefits from {len(benefits)} thesis(es)")
        for ben in benefits:
            lines.append(f"- **{ben['thesis_name']}**: {ben['why'][:150]}")
        lines.append("")

    return "\n".join(lines)


def morning_disruption_brief() -> str:
    """The morning brief Joseph reads over coffee.
    Prioritized by confidence × timeframe urgency."""
    theses = load_theses()
    if not theses:
        return "No disruption theses loaded."

    # Priority order: very_high first, then by shortest timeframe
    priority_order = {"very_high": 0, "high": 1, "medium-high": 2, "medium": 3}
    theses_sorted = sorted(theses, key=lambda t: priority_order.get(t.get("confidence", "medium"), 3))

    lines = [
        "# Morning Disruption Brief",
        f"_{datetime.now(timezone.utc).strftime('%A, %B %d, %Y')}_",
        f"**{len(theses)} active disruption theses tracked**",
        "",
        "## What Matters Today",
        "",
    ]

    # Top 3 highest-confidence theses get their morning_brief
    for t in theses_sorted[:3]:
        conf = t.get("confidence", "?").upper().replace("_", " ").replace("-", " ")
        lines.append(f"**{t['name']}** [{conf}]")
        lines.append(t.get("morning_brief", "").strip())
        lines.append("")

    # Watchlist triggers to monitor today
    lines.append("## Today's Watchlist")
    all_triggers = []
    for t in theses_sorted[:5]:
        for trigger in t.get("watchlist_triggers", [])[:2]:
            all_triggers.append((t["name"], trigger))

    for thesis_name, trigger in all_triggers[:8]:
        lines.append(f"- {trigger}")
    lines.append("")

    # Quick vulnerability scan
    lines.append("## Vulnerable (multiple exposures)")
    exposure_counts: dict[str, int] = {}
    for t in theses:
        for c in t.get("exposed_companies", []):
            name = c.get("name", "")
            if name.startswith("Every ") or name.startswith("Any ") or name.startswith("Companies "):
                continue
            exposure_counts[name] = exposure_counts.get(name, 0) + 1

    multi_exposed = [(name, count) for name, count in exposure_counts.items() if count >= 2]
    multi_exposed.sort(key=lambda x: x[1], reverse=True)
    for name, count in multi_exposed[:6]:
        lines.append(f"- **{name}** — exposed across {count} theses")
    lines.append("")

    # Beneficiaries appearing across multiple theses
    lines.append("## Beneficiaries (multiple tailwinds)")
    benefit_counts: dict[str, int] = {}
    for t in theses:
        for b in t.get("beneficiaries", []):
            name = b.get("name", "")
            benefit_counts[name] = benefit_counts.get(name, 0) + 1

    multi_benefit = [(name, count) for name, count in benefit_counts.items() if count >= 2]
    multi_benefit.sort(key=lambda x: x[1], reverse=True)
    for name, count in multi_benefit[:6]:
        lines.append(f"- **{name}** — benefits from {count} theses")
    lines.append("")

    lines.append("_Use `/tech thesis <ID>` to deep-dive. `/tech vulnerable` for full exposure list._")
    return "\n".join(lines)


def query_disruption(query: str) -> str:
    """Search disruption theses for a company, topic, or keyword."""
    theses = load_theses()
    query_lower = query.lower()
    query_words = [w for w in query_lower.split() if len(w) > 2]

    results = []
    for t in theses:
        # Build searchable text from thesis content
        searchable_parts = [
            t.get("name", ""),
            t.get("thesis", ""),
            t.get("morning_brief", ""),
        ]
        for c in t.get("exposed_companies", []):
            searchable_parts.append(c.get("name", ""))
            searchable_parts.append(c.get("risk", ""))
            searchable_parts.append(c.get("ticker", ""))
        for b in t.get("beneficiaries", []):
            searchable_parts.append(b.get("name", ""))
            searchable_parts.append(b.get("why", ""))
            searchable_parts.append(b.get("ticker", ""))
        for e in t.get("evidence", []):
            searchable_parts.append(e.get("quote", ""))
        for trigger in t.get("watchlist_triggers", []):
            searchable_parts.append(trigger)

        searchable = " ".join(searchable_parts).lower()
        score = sum(1 for w in query_words if w in searchable)
        if score > 0:
            results.append((score, t))

    results.sort(key=lambda x: x[0], reverse=True)

    if not results:
        return f"No disruption theses match '{query}'. Try `/tech disruption` for full list."

    lines = [
        f"# Disruption Search: {query}",
        f"**{len(results)} matching theses**",
        "",
    ]

    for score, t in results[:5]:
        lines.append(f"## {t['name']} ({t['id']})")
        lines.append(f"Confidence: {t.get('confidence', '?')} | Timeframe: {t.get('timeframe', '?')}")
        lines.append("")

        # Show matching exposed companies
        for c in t.get("exposed_companies", []):
            c_text = f"{c.get('name', '')} {c.get('risk', '')} {c.get('ticker', '')}".lower()
            if any(w in c_text for w in query_words):
                ticker = c.get("ticker", "")
                ticker_str = f" [{ticker}]" if ticker and ticker != "various" else ""
                lines.append(f"  EXPOSED: **{c['name']}**{ticker_str} — {c.get('risk', '')[:120]}")

        # Show matching beneficiaries
        for b in t.get("beneficiaries", []):
            b_text = f"{b.get('name', '')} {b.get('why', '')} {b.get('ticker', '')}".lower()
            if any(w in b_text for w in query_words):
                lines.append(f"  BENEFITS: **{b['name']}** — {b.get('why', '')[:120]}")

        lines.append(f"  _{t.get('morning_brief', '')[:200]}_")
        lines.append("")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# PERPLEXITY (optional)
# ═══════════════════════════════════════════════════════════════


def _perplexity_search(query: str) -> dict | None:
    """Run a Perplexity search for tech intelligence."""
    api_key = os.environ.get("PERPLEXITY_API_KEY")
    if not api_key:
        return None
    try:
        import httpx
    except ImportError:
        return None

    resp = httpx.post(
        "https://api.perplexity.ai/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "sonar",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a tech industry analyst. Provide concise, sourced analysis "
                        "of AI tools, companies, and technology trends. Focus on recent "
                        "developments (2025-2026). Include funding, product launches, and "
                        "practitioner adoption signals."
                    ),
                },
                {"role": "user", "content": query},
            ],
            "max_tokens": 1000,
        },
        timeout=30,
    )
    if resp.status_code == 200:
        data = resp.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        citations = data.get("citations", [])
        return {"content": content, "citations": citations}
    return None


# ═══════════════════════════════════════════════════════════════
# TELEGRAM FORMAT
# ═══════════════════════════════════════════════════════════════


def format_telegram(text: str, max_length: int = 4000) -> str:
    """Format for Telegram (convert markdown, truncate)."""
    import re
    text = re.sub(r'^#{1,3}\s+', '', text, flags=re.MULTILINE)  # strip # headers
    text = text.replace('**', '*')  # **bold** → *bold*
    text = text.replace('`', '')  # backticks can break Telegram markdown
    if len(text) > max_length:
        text = text[:max_length - 50] + "\n\n... (truncated — run full report via CLI)"
    return text


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(description="Tech Engine — PIS-powered tech intelligence + disruption theses")
    parser.add_argument("--brief", "-b", action="store_true", help="Full tech landscape brief")
    parser.add_argument("--query", "-q", type=str, help="Search PIS for a topic")
    parser.add_argument("--tier", "-t", type=int, help="List tools by signal tier (1, 2, or 3)")
    parser.add_argument("--action", "-a", type=str, help="List tools by palette action (integrate/evaluate/monitor/skip)")
    parser.add_argument("--cluster", "-c", type=str, help="List voices in a cluster")
    parser.add_argument("--disruption", "-d", action="store_true", help="All disruption theses summary")
    parser.add_argument("--thesis", type=str, help="Deep-dive a specific thesis (e.g., DISRUPT-CLOUD-PEAK)")
    parser.add_argument("--vulnerable", "-v", action="store_true", help="Most exposed companies across all theses")
    parser.add_argument("--beneficiaries", action="store_true", help="Top beneficiary companies across all theses")
    parser.add_argument("--morning", "-m", action="store_true", help="Morning disruption brief for investors")
    parser.add_argument("--perplexity", "-p", action="store_true", help="Include live Perplexity search")
    parser.add_argument("--telegram", action="store_true", help="Format for Telegram")

    args = parser.parse_args()

    if args.brief:
        output = generate_brief()
    elif args.tier:
        output = list_by_tier(args.tier)
    elif args.action:
        output = list_by_action(args.action)
    elif args.cluster:
        output = list_cluster(args.cluster)
    elif args.disruption:
        output = disruption_brief()
    elif args.thesis:
        output = lookup_thesis(args.thesis)
    elif args.vulnerable:
        output = vulnerable_companies()
    elif args.beneficiaries:
        output = beneficiary_companies()
    elif args.morning:
        output = morning_disruption_brief()
    elif args.query:
        output = query_tech(args.query, use_perplexity=args.perplexity)
    else:
        parser.print_help()
        return

    if args.telegram:
        output = format_telegram(output)

    print(output)


if __name__ == "__main__":
    main()
