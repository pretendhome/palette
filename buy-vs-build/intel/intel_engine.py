#!/usr/bin/env python3
"""
Intel Engine v1.0 — Financial Intelligence Query System

The investment-domain equivalent of Palette's Researcher agent.
Checks internal voice library and thesis signals before external search.

Usage:
  CLI:      python3 intel_engine.py --query "Is the refining supercycle thesis intact?"
  CLI:      python3 intel_engine.py --thesis THESIS-OIL-REFINING
  CLI:      python3 intel_engine.py --brief  (all thesis categories summary)
  Bot:      Called by joseph_bridge.py when user sends /intel

Requires: pyyaml, httpx (optional — for Perplexity)
"""

import argparse
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

INTEL_DIR = Path(__file__).parent
VOICES_PATH = INTEL_DIR / "people-library" / "v1.0" / "financial_voices.yaml"
SIGNALS_PATH = INTEL_DIR / "people-library" / "v1.0" / "thesis_signals.yaml"
CATEGORIES_PATH = INTEL_DIR / "thesis-categories" / "v1.0" / "categories.yaml"
SCORES_PATH = INTEL_DIR / "scoring" / "forecaster_scores.yaml"


def load_yaml(path: Path) -> dict:
    """Load a YAML file, return parsed content."""
    with open(path) as f:
        return yaml.safe_load(f)


def load_voices() -> list[dict]:
    """Load financial voices library."""
    data = load_yaml(VOICES_PATH)
    return data.get("profiles", [])


def load_categories() -> list[dict]:
    """Load thesis categories."""
    data = load_yaml(CATEGORIES_PATH)
    return data.get("categories", [])


def load_signals() -> dict:
    """Load thesis signals cross-reference."""
    data = load_yaml(SIGNALS_PATH)
    return data.get("thesis_coverage", {})


def load_scores() -> dict:
    """Load forecaster scoring data."""
    return load_yaml(SCORES_PATH)


# ═══════════════════════════════════════════════════════════════
# CORE: THESIS LOOKUP
# ═══════════════════════════════════════════════════════════════


def lookup_thesis(thesis_id: str) -> dict:
    """Look up a thesis category and its covering voices."""
    categories = load_categories()
    signals = load_signals()
    voices = load_voices()

    # Find the category
    category = None
    for cat in categories:
        if cat["id"] == thesis_id:
            category = cat
            break

    if not category:
        return {"error": f"Thesis category {thesis_id} not found."}

    # Get signal coverage
    coverage = signals.get(thesis_id, {})
    covering_voices = coverage.get("voices", [])

    # Enrich with full voice data
    voice_map = {v["id"]: v for v in voices}
    enriched_voices = []
    for cv in covering_voices:
        full = voice_map.get(cv["id"], {})
        enriched_voices.append({
            "id": cv["id"],
            "name": cv["name"],
            "signal_strength": cv["signal_strength"],
            "edge": cv["edge"],
            "platforms": full.get("platforms", {}),
            "track_record": full.get("track_record", {}),
            "perplexity_query": full.get("perplexity_query", ""),
        })

    return {
        "category": category,
        "voice_count": len(enriched_voices),
        "voices": enriched_voices,
        "consensus_note": coverage.get("consensus_note", ""),
        "decay_half_life_days": category.get("decay_half_life_days", 7),
    }


# ═══════════════════════════════════════════════════════════════
# CORE: QUERY ROUTING
# ═══════════════════════════════════════════════════════════════


def route_query(query: str) -> list[dict]:
    """Route a natural language query to relevant thesis categories and voices."""
    categories = load_categories()
    query_lower = query.lower()

    # Simple keyword matching — route to categories whose key_questions or
    # name/description contain query terms
    matches = []
    for cat in categories:
        score = 0
        searchable = " ".join([
            cat.get("name", ""),
            cat.get("description", ""),
            " ".join(cat.get("key_questions", [])),
        ]).lower()

        # Score by keyword overlap
        for word in query_lower.split():
            if len(word) > 3 and word in searchable:
                score += 1

        if score > 0:
            matches.append({"category": cat, "relevance_score": score})

    matches.sort(key=lambda x: x["relevance_score"], reverse=True)

    # For each matched category, pull the thesis lookup
    results = []
    for m in matches[:3]:  # top 3 categories
        lookup = lookup_thesis(m["category"]["id"])
        lookup["relevance_score"] = m["relevance_score"]
        results.append(lookup)

    return results


# ═══════════════════════════════════════════════════════════════
# CORE: BRIEF GENERATION
# ═══════════════════════════════════════════════════════════════


def generate_brief() -> str:
    """Generate a summary brief across all thesis categories."""
    categories = load_categories()
    signals = load_signals()

    lines = []
    lines.append("# Intel Brief")
    lines.append(f"**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")

    for cat in categories:
        cid = cat["id"]
        coverage = signals.get(cid, {})
        voice_count = len(coverage.get("voices", []))
        consensus = coverage.get("consensus_note", "No consensus note.")
        decay = cat.get("decay_half_life_days", "?")

        lines.append(f"## {cat['name']}")
        lines.append(f"**Voices**: {voice_count} | **Signal decay**: {decay}d half-life")
        lines.append(f"**Consensus**: {consensus}")

        # List top voices
        for v in coverage.get("voices", [])[:3]:
            strength = v.get("signal_strength", "?")
            lines.append(f"- **{v['name']}** ({strength}): {v.get('edge', '')}")

        # Key questions
        for q in cat.get("key_questions", [])[:2]:
            lines.append(f"  - {q}")

        lines.append("")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# CORE: PERPLEXITY RESEARCH (optional)
# ═══════════════════════════════════════════════════════════════


def perplexity_search(query: str) -> dict | None:
    """Run a Perplexity Sonar search if API key is available."""
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
                        "You are a financial research analyst. Provide concise, "
                        "sourced analysis. Focus on recent developments (2025-2026). "
                        "Include specific data points, dates, and sources."
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
# CORE: FULL INTEL PASS
# ═══════════════════════════════════════════════════════════════


def intel_pass(query: str, use_perplexity: bool = False) -> str:
    """
    Full intel pass — the main entry point.

    1. Route query to thesis categories
    2. Pull covering voices and their signals
    3. Optionally run Perplexity search for fresh data
    4. Return formatted intel report
    """
    lines = []
    lines.append(f"# Intel Report: {query}")
    lines.append(f"**Generated**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")

    # Step 1: Route to categories
    results = route_query(query)

    if not results:
        lines.append("No matching thesis categories found. Try a broader query or use `--brief` for all categories.")
        return "\n".join(lines)

    # Step 2: Present internal intelligence
    lines.append("## Internal Intelligence")
    lines.append("")

    for r in results:
        cat = r["category"]
        lines.append(f"### {cat['name']}")
        lines.append(f"**Relevance**: {r['relevance_score']} | **Voices**: {r['voice_count']} | **Decay**: {r['decay_half_life_days']}d")
        lines.append(f"**Consensus**: {r.get('consensus_note', 'None')}")
        lines.append("")

        for v in r.get("voices", []):
            strength = v.get("signal_strength", "?")
            edge = v.get("edge", "")
            lines.append(f"- **{v['name']}** (signal: {strength})")
            lines.append(f"  Edge: {edge}")

            # Show track record highlights
            tr = v.get("track_record", {})
            strengths = tr.get("strengths", [])
            if strengths:
                lines.append(f"  Track record: {strengths[0]}")

            # Show Perplexity query for follow-up
            pq = v.get("perplexity_query", "")
            if pq:
                lines.append(f"  Research query: `{pq}`")

            lines.append("")

    # Step 3: Perplexity search (if enabled)
    if use_perplexity:
        lines.append("## Live Research (Perplexity)")
        lines.append("")

        # Build a focused query from the thesis context
        top_cat = results[0]["category"]
        focused_query = f"{query} — focus on {top_cat['name']}, recent developments 2025-2026"

        result = perplexity_search(focused_query)
        if result:
            lines.append(result["content"])
            lines.append("")
            if result.get("citations"):
                lines.append("**Sources:**")
                for i, cite in enumerate(result["citations"], 1):
                    if isinstance(cite, str):
                        lines.append(f"  {i}. {cite}")
                    elif isinstance(cite, dict):
                        lines.append(f"  {i}. [{cite.get('title', 'Source')}]({cite.get('url', '')})")
        else:
            lines.append("Perplexity search unavailable (no API key or connection error).")

        lines.append("")

    # Step 4: Suggested follow-up
    lines.append("## Suggested Follow-Up")
    for r in results:
        for v in r.get("voices", [])[:2]:
            pq = v.get("perplexity_query", "")
            if pq:
                lines.append(f"- Search: `{pq}`")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# TELEGRAM BOT INTEGRATION
# ═══════════════════════════════════════════════════════════════


def format_telegram(report: str, max_length: int = 4000) -> str:
    """Format an intel report for Telegram (convert markdown, truncate)."""
    # Telegram Markdown uses *bold* not **bold**, and doesn't support # headers
    import re
    report = re.sub(r'^#{1,3}\s+', '', report, flags=re.MULTILINE)  # strip # headers
    report = report.replace('**', '*')  # **bold** → *bold*
    report = report.replace('`', '')  # backticks can break Telegram markdown
    if len(report) > max_length:
        report = report[:max_length - 50] + "\n\n... (truncated — run full report via CLI)"
    return report


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════


def main():
    parser = argparse.ArgumentParser(description="Intel Engine — Financial Intelligence System")
    parser.add_argument("--query", "-q", type=str, help="Natural language query")
    parser.add_argument("--thesis", "-t", type=str, help="Thesis category ID (e.g., THESIS-OIL-UPSTREAM)")
    parser.add_argument("--brief", "-b", action="store_true", help="Generate full brief across all categories")
    parser.add_argument("--perplexity", "-p", action="store_true", help="Include live Perplexity search")
    parser.add_argument("--telegram", action="store_true", help="Format output for Telegram")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.brief:
        output = generate_brief()
    elif args.thesis:
        result = lookup_thesis(args.thesis)
        if args.json:
            print(json.dumps(result, indent=2, default=str))
            return
        # Format as readable text
        lines = []
        cat = result.get("category", {})
        lines.append(f"# {cat.get('name', args.thesis)}")
        lines.append(f"**Voices**: {result.get('voice_count', 0)}")
        lines.append(f"**Consensus**: {result.get('consensus_note', 'None')}")
        lines.append("")
        for v in result.get("voices", []):
            lines.append(f"- **{v['name']}** ({v['signal_strength']}): {v['edge']}")
        output = "\n".join(lines)
    elif args.query:
        output = intel_pass(args.query, use_perplexity=args.perplexity)
    else:
        parser.print_help()
        return

    if args.telegram:
        output = format_telegram(output)

    print(output)


if __name__ == "__main__":
    main()
