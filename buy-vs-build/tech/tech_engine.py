#!/usr/bin/env python3
"""
Tech Engine v1.0 — PIS-Powered Tech Intelligence for Telegram

Reads the Palette Intelligence System (PIS) people library and company signals
READ-ONLY — never modifies PIS files.

Generates tech briefs showing:
  - What trusted practitioners are using and recommending
  - Tier 1/2/3 tool landscape with palette actions
  - Per-cluster signal summaries
  - Perplexity queries ready to run for live updates

Usage:
  CLI:      python3 tech_engine.py --brief
  CLI:      python3 tech_engine.py --query "voice AI tools"
  CLI:      python3 tech_engine.py --cluster lovable_orbit
  CLI:      python3 tech_engine.py --tier 1
  CLI:      python3 tech_engine.py --action evaluate
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
PEOPLE_LIB = BUY_VS_BUILD / "people-library" / "v1.1" / "people_library_v1.1.yaml"
COMPANY_SIG = BUY_VS_BUILD / "people-library" / "v1.1" / "people_library_company_signals_v1.1.yaml"
PIS_ARCH = BUY_VS_BUILD / "PALETTE_INTELLIGENCE_SYSTEM_v1.0.md"


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
    parser = argparse.ArgumentParser(description="Tech Engine — PIS-powered tech intelligence")
    parser.add_argument("--brief", "-b", action="store_true", help="Full tech landscape brief")
    parser.add_argument("--query", "-q", type=str, help="Search PIS for a topic")
    parser.add_argument("--tier", "-t", type=int, help="List tools by signal tier (1, 2, or 3)")
    parser.add_argument("--action", "-a", type=str, help="List tools by palette action (integrate/evaluate/monitor/skip)")
    parser.add_argument("--cluster", "-c", type=str, help="List voices in a cluster")
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
