#!/usr/bin/env python3
"""
morning_brief.py — Phone-optimized investor morning brief

Generates a concise, fresh-only brief by:
  1. NEW: Perplexity scan of last 24h filtered by disruption watchlist triggers
  2. DISRUPTION: Match new events to thesis exposures (only when a trigger fires)
  3. TRENDS: Rotate 2-3 theses per day, never repeat within 7 days

Each item is 1-2 lines + a ready-to-paste research prompt.
Whole output fits on one phone screen (~1500 chars target).

Usage:
  from morning_brief import generate_morning_brief
  text = generate_morning_brief(perplexity_key="pplx-xxx")
"""
from __future__ import annotations

import json
import os
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml

try:
    import httpx
except ImportError:
    httpx = None  # type: ignore

TECH_DIR = Path(__file__).parent
THESES_PATH = TECH_DIR / "disruption_theses.yaml"
BRIEF_STATE_PATH = TECH_DIR / "brief_state.yaml"

PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"


# ── Thesis data ──────────────────────────────────────────────────────────────

def _load_theses() -> list[dict]:
    if not THESES_PATH.exists():
        return []
    with open(THESES_PATH) as f:
        data = yaml.safe_load(f) or {}
    return data.get("theses", [])


# ── Staleness tracker ────────────────────────────────────────────────────────

def _load_state() -> dict:
    if BRIEF_STATE_PATH.exists():
        with open(BRIEF_STATE_PATH) as f:
            return yaml.safe_load(f) or {}
    return {}


def _save_state(state: dict) -> None:
    with open(BRIEF_STATE_PATH, "w") as f:
        yaml.dump(state, f, default_flow_style=False, sort_keys=False)


def _thesis_shown_recently(state: dict, thesis_id: str, days: int = 7) -> bool:
    """Check if a thesis was shown in the TRENDS section within N days."""
    shown = state.get("trends_shown", {})
    last = shown.get(thesis_id)
    if not last:
        return False
    if isinstance(last, str):
        last_dt = datetime.fromisoformat(last)
    else:
        last_dt = last
    return (datetime.now() - last_dt).days < days


def _mark_shown(state: dict, thesis_ids: list[str]) -> None:
    shown = state.setdefault("trends_shown", {})
    now = datetime.now().isoformat()
    for tid in thesis_ids:
        shown[tid] = now


# ── Perplexity: fresh news scan ──────────────────────────────────────────────

def _build_scan_prompt(theses: list[dict]) -> str:
    """Build a focused prompt that asks Perplexity to scan for watchlist hits."""
    # Collect the most specific triggers across all theses
    triggers = []
    for t in theses:
        for trigger in t.get("watchlist_triggers", [])[:2]:
            triggers.append(trigger)

    # Also collect exposed company names for targeted scanning
    companies = set()
    for t in theses:
        for c in t.get("exposed_companies", []):
            name = c.get("name", "")
            if not name.startswith(("Every ", "Any ", "Companies ")):
                companies.add(name)
        for b in t.get("beneficiaries", []):
            companies.add(b.get("name", ""))

    top_companies = sorted(companies)[:20]

    return f"""You are a concise tech investment analyst. Scan the last 24 hours for significant events.

ONLY report events that match these criteria:
{chr(10).join(f'- {t}' for t in triggers[:15])}

Companies to watch: {', '.join(top_companies)}

Rules:
- ONLY events from the last 24 hours
- ONLY materially significant events (funding rounds >$50M, major product launches, regulatory moves, leadership changes, earnings surprises)
- Skip routine feature updates, minor partnerships, opinion pieces
- If NOTHING significant happened, respond with exactly: NO_NEWS
- Maximum 5 items
- Each item: one sentence with specific numbers/dates, no commentary

Format each item as:
COMPANY: what happened (specific numbers)
"""


def _scan_fresh_news(perplexity_key: str, theses: list[dict]) -> list[str]:
    """Run Perplexity scan for fresh events matching our watchlist."""
    if not httpx or not perplexity_key:
        return []

    prompt = _build_scan_prompt(theses)

    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(
                PERPLEXITY_URL,
                headers={
                    "Authorization": f"Bearer {perplexity_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "sonar",
                    "messages": [
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": "What significant tech/AI/market events happened in the last 24 hours?"},
                    ],
                },
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[morning] Perplexity error: {e}", flush=True)
        return []

    if "NO_NEWS" in content:
        return []

    # Parse into individual items (one per line, skip blanks)
    items = []
    for line in content.strip().split("\n"):
        line = line.strip()
        if line and len(line) > 10 and not line.startswith("#"):
            # Clean up markdown artifacts
            line = line.lstrip("- •*")
            line = line.strip()
            if line:
                items.append(line)

    return items[:5]


# ── Match news to theses ─────────────────────────────────────────────────────

def _match_to_thesis(news_item: str, theses: list[dict]) -> dict | None:
    """Check if a news item matches any disruption thesis."""
    item_lower = news_item.lower()

    best_match = None
    best_score = 0

    for t in theses:
        score = 0

        # Check exposed company names
        for c in t.get("exposed_companies", []):
            name = c.get("name", "")
            if not name.startswith(("Every ", "Any ", "Companies ")):
                # Check company name words (at least 2 chars)
                for word in name.lower().split():
                    if len(word) > 2 and word in item_lower:
                        score += 2

        # Check beneficiary names
        for b in t.get("beneficiaries", []):
            for word in b.get("name", "").lower().split():
                if len(word) > 2 and word in item_lower:
                    score += 2

        # Check watchlist trigger keywords
        for trigger in t.get("watchlist_triggers", []):
            trigger_words = [w for w in trigger.lower().split() if len(w) > 3]
            matches = sum(1 for w in trigger_words if w in item_lower)
            if matches >= 2:
                score += matches

        if score > best_score:
            best_score = score
            best_match = t

    return best_match if best_score >= 3 else None


def _make_research_prompt(news_item: str) -> str:
    """Generate a concise research follow-up prompt from a news item."""
    # Extract the core topic — first 60 chars, clean
    clean = news_item.split(".")[0].strip()
    if len(clean) > 80:
        clean = clean[:77] + "..."
    return clean


# ── Main brief generator ─────────────────────────────────────────────────────

def generate_morning_brief(perplexity_key: str = "") -> str:
    """Generate the phone-optimized morning brief.

    Returns Telegram-formatted markdown, ~1500 chars target.
    """
    theses = _load_theses()
    state = _load_state()
    now = datetime.now()

    lines = []
    day_str = now.strftime("%a %b %d")
    lines.append(f"*{day_str}*")
    lines.append("")

    # ── SECTION 1: NEW TODAY ──
    news_items = _scan_fresh_news(perplexity_key, theses) if perplexity_key else []

    if news_items:
        lines.append("*NEW*")
        for item in news_items[:3]:
            # Truncate to ~120 chars for phone
            display = item[:140]
            thesis_match = _match_to_thesis(item, theses)

            if thesis_match:
                tag = thesis_match["id"].replace("DISRUPT-", "").lower().replace("-", " ")
                lines.append(f"  {display}")
                lines.append(f"  _{tag}_")
            else:
                lines.append(f"  {display}")

            research = _make_research_prompt(item)
            lines.append(f"  /research {research}")
            lines.append("")
    else:
        lines.append("*NEW*")
        lines.append("  No major events in last 24h")
        lines.append("")

    # ── SECTION 2: DISRUPTION SIGNALS ──
    # Only show if news items matched theses
    disruption_items = []
    if news_items:
        for item in news_items:
            match = _match_to_thesis(item, theses)
            if match:
                # Find which companies are affected
                exposed_names = [c["name"] for c in match.get("exposed_companies", [])
                                 if not c["name"].startswith(("Every ", "Any ", "Companies "))]
                if exposed_names:
                    short_item = item.split(".")[0][:80]
                    exposed_str = ", ".join(exposed_names[:2])
                    disruption_items.append(
                        f"  {short_item}\n  Exposed: {exposed_str}\n  /tech thesis {match['id']}"
                    )

    if disruption_items:
        lines.append("*DISRUPTION*")
        for d in disruption_items[:2]:
            lines.append(d)
            lines.append("")

    # ── SECTION 3: TREND PULSE ──
    # Rotate 2-3 theses that haven't been shown in 7 days
    eligible = [t for t in theses if not _thesis_shown_recently(state, t["id"])]

    if not eligible:
        # All shown recently — reset and pick from high-confidence
        state["trends_shown"] = {}
        eligible = theses[:]

    # Prioritize by confidence
    priority = {"very_high": 0, "high": 1, "medium-high": 2, "medium": 3}
    eligible.sort(key=lambda t: priority.get(t.get("confidence", "medium"), 3))

    # Pick 2 (deterministic per day — use day-of-year as seed for consistency)
    day_seed = now.timetuple().tm_yday
    random.seed(day_seed)
    picks = eligible[:min(4, len(eligible))]
    random.shuffle(picks)
    picks = picks[:2]

    if picks:
        lines.append(f"*TRENDS* ({len(theses)} tracked)")
        for t in picks:
            conf = t.get("confidence", "?").replace("_", " ")
            brief = t.get("morning_brief", "").strip()
            # Take first sentence only, max 100 chars
            first_sentence = brief.split(".")[0].strip()
            if len(first_sentence) > 120:
                first_sentence = first_sentence[:117] + "..."
            lines.append(f"  *{t['name']}* [{conf}]")
            lines.append(f"  {first_sentence}.")
            lines.append(f"  /tech thesis {t['id']}")
            lines.append("")

        # Mark these as shown
        _mark_shown(state, [t["id"] for t in picks])

    # ── FOOTER ──
    lines.append("/tech disruption  /tech vulnerable  /stress")

    # Save state
    _save_state(state)

    return "\n".join(lines)


# ── Telegram-ready format ────────────────────────────────────────────────────

def format_telegram(text: str) -> str:
    """Light formatting pass for Telegram compatibility."""
    # Already formatted for Telegram markdown — just cap length
    if len(text) > 4000:
        text = text[:3950] + "\n\n(truncated)"
    return text


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    key = os.environ.get("PERPLEXITY_API_KEY", "")
    print(generate_morning_brief(key))
