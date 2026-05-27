#!/usr/bin/env python3
"""
joseph_bot_v2.py — Investment Intelligence Bot (Clean Rebuild)

Single-process Telegram bot with:
  - Disruption thesis tracking (12 theses from AI Council conference)
  - Live Perplexity research on demand
  - Monitor scheduler (runs between poll cycles)
  - SQLite state: signals, research log, user interests, brief history
  - Narrator filter: condenses raw research into phone-friendly blurbs
  - Inline keyboard buttons for tap-to-act UX

One file. One service. One restart. No server dependencies.

Setup:
  export JOSEPH_BOT_TOKEN="telegram-bot-token"
  export PERPLEXITY_API_KEY="pplx-xxx"
  python3 joseph_bot_v2.py
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import re
import sqlite3
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import httpx
import yaml

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

BOT_TOKEN = os.environ.get("JOSEPH_BOT_TOKEN", "")
PERPLEXITY_KEY = os.environ.get("PERPLEXITY_API_KEY", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

TELEGRAM = f"https://api.telegram.org/bot{BOT_TOKEN}"
PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"
POLL_TIMEOUT = 30

# Data paths
BOT_DIR = Path(__file__).resolve().parent
DATA_DIR = BOT_DIR / "joseph_data"
DB_PATH = DATA_DIR / "joseph.db"
THESES_PATH = BOT_DIR.parent / "buy-vs-build" / "tech" / "disruption_theses.yaml"
MONITORS_DIR = DATA_DIR / "monitors"
INTEL_DIR = BOT_DIR.parent / "buy-vs-build" / "intel"

# If theses not found at first path, try alternate locations
if not THESES_PATH.exists():
    alt = Path("/root/fde/buy-vs-build/tech/disruption_theses.yaml")
    if alt.exists():
        THESES_PATH = alt
        INTEL_DIR = Path("/root/fde/buy-vs-build/intel")


# ═══════════════════════════════════════════════════════════════════════════════
# SQLITE STATE
# ═══════════════════════════════════════════════════════════════════════════════

def init_db() -> sqlite3.Connection:
    """Initialize SQLite database with all tables."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    MONITORS_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            thesis_id TEXT,
            content TEXT NOT NULL,
            source TEXT DEFAULT 'perplexity',
            monitor_id TEXT
        );
        CREATE TABLE IF NOT EXISTS research_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            query TEXT NOT NULL,
            result TEXT,
            thesis_id TEXT
        );
        CREATE TABLE IF NOT EXISTS user_interests (
            thesis_id TEXT PRIMARY KEY,
            tap_count INTEGER DEFAULT 0,
            last_accessed TEXT
        );
        CREATE TABLE IF NOT EXISTS brief_state (
            key TEXT PRIMARY KEY,
            value TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_signals_thesis ON signals(thesis_id);
        CREATE INDEX IF NOT EXISTS idx_signals_ts ON signals(ts);
        CREATE INDEX IF NOT EXISTS idx_research_ts ON research_log(ts);
    """)
    conn.commit()
    return conn


DB: sqlite3.Connection = None  # type: ignore  — initialized in run()

# Company conversation state: {chat_id: {"company": str, "ts": float}}
_company_context: dict[int, dict] = {}
COMPANY_CTX_TIMEOUT = 600  # 10 minutes


# ═══════════════════════════════════════════════════════════════════════════════
# TELEGRAM
# ═══════════════════════════════════════════════════════════════════════════════

_client = httpx.Client(timeout=35.0)


def tg(method: str, **kwargs) -> dict:
    resp = _client.post(f"{TELEGRAM}/{method}", json=kwargs)
    return resp.json()


def send(chat_id: int, text: str, buttons: list[list[dict]] | None = None) -> None:
    """Send message with optional inline keyboard. Falls back to no-markdown on error."""
    kwargs: dict = {
        "chat_id": chat_id,
        "text": text[:4000],
        "parse_mode": "Markdown",
    }
    if buttons:
        kwargs["reply_markup"] = {"inline_keyboard": buttons}

    result = tg("sendMessage", **kwargs)
    if not result.get("ok"):
        # Markdown failed — retry without parse_mode
        kwargs.pop("parse_mode")
        tg("sendMessage", **kwargs)


def typing(chat_id: int) -> None:
    tg("sendChatAction", chat_id=chat_id, action="typing")


def answer_callback(cb_id: str, text: str = "") -> None:
    kwargs = {"callback_query_id": cb_id}
    if text:
        kwargs["text"] = text[:200]
    tg("answerCallbackQuery", **kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
# PERPLEXITY + NARRATOR FILTER
# ═══════════════════════════════════════════════════════════════════════════════

def perplexity(query: str, system: str = "", condense: bool = True) -> str:
    """Call Perplexity. If condense=True, runs narrator filter for phone-friendly output."""
    if not PERPLEXITY_KEY:
        return "Perplexity API key not set."

    if not system:
        system = (
            "You are a concise investment research analyst. "
            "Give specific data: numbers, dates, percentages. "
            "Skip disclaimers. Be direct. Maximum 150 words."
        )

    try:
        resp = _client.post(
            PERPLEXITY_URL,
            headers={"Authorization": f"Bearer {PERPLEXITY_KEY}", "Content-Type": "application/json"},
            json={
                "model": "sonar",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": query},
                ],
                "return_citations": True,
            },
            timeout=45.0,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        citations = data.get("citations", [])

        # Narrator filter: condense to phone-friendly
        if condense and len(content) > 300:
            content = _narrator_condense(content)

        if citations:
            content += "\n\n_Sources:_"
            for i, c in enumerate(citations[:3], 1):
                url = c if isinstance(c, str) else c.get("url", "")
                if url:
                    content += f"\n{i}. {url}"

        return content
    except Exception as e:
        print(f"[perplexity] error: {e}", flush=True)
        return f"Research error: {e}"


def _narrator_condense(text: str) -> str:
    """Narrator agent: condense raw research into phone-optimized blurb.

    Rules (from narrator.md):
    - Evidence-based only, no speculation
    - Translate technical to business value
    - Never outrun available evidence
    - Be concise: 2-3 key points with numbers
    """
    if not PERPLEXITY_KEY:
        # Fallback: just truncate intelligently
        sentences = text.split(". ")
        return ". ".join(sentences[:4]) + "."

    try:
        resp = _client.post(
            PERPLEXITY_URL,
            headers={"Authorization": f"Bearer {PERPLEXITY_KEY}", "Content-Type": "application/json"},
            json={
                "model": "sonar",
                "messages": [
                    {"role": "system", "content": (
                        "You are a narrator that condenses research for a mobile investor. "
                        "Rules: (1) Keep specific numbers and dates. (2) Cut all filler, caveats, "
                        "and general context. (3) Maximum 3 bullet points. (4) Each bullet is one "
                        "sentence with a specific data point. (5) If nothing material, say so in "
                        "one sentence. Never speculate."
                    )},
                    {"role": "user", "content": f"Condense this for a phone screen:\n\n{text[:2000]}"},
                ],
            },
            timeout=20.0,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception:
        # Fallback: truncate
        sentences = text.split(". ")
        return ". ".join(sentences[:4]) + "."


# ═══════════════════════════════════════════════════════════════════════════════
# DISRUPTION THESES
# ═══════════════════════════════════════════════════════════════════════════════

_theses_cache: list[dict] | None = None


def load_theses() -> list[dict]:
    global _theses_cache
    if _theses_cache is not None:
        return _theses_cache
    if not THESES_PATH.exists():
        return []
    with open(THESES_PATH) as f:
        data = yaml.safe_load(f) or {}
    _theses_cache = data.get("theses", [])
    return _theses_cache


def thesis_brief(thesis_id: str) -> str:
    """Deep-dive a specific thesis. Records user interest."""
    theses = load_theses()
    thesis = next((t for t in theses if t["id"] == thesis_id.upper()), None)

    if not thesis:
        # Fuzzy match
        q = thesis_id.lower().replace("-", " ")
        for t in theses:
            if q in t["name"].lower() or q in t["id"].lower():
                thesis = t
                break

    if not thesis:
        ids = "\n".join(f"  {t['id']}" for t in theses)
        return f"Thesis not found: {thesis_id}\n\nAvailable:\n{ids}"

    # Record interest
    _record_interest(thesis["id"])

    # Get signal history
    signals = DB.execute(
        "SELECT ts, content FROM signals WHERE thesis_id = ? ORDER BY ts DESC LIMIT 3",
        (thesis["id"],)
    ).fetchall()

    lines = [
        f"*{thesis['name']}*",
        f"Confidence: {thesis.get('confidence', '?')} | Timeframe: {thesis.get('timeframe', '?')}",
        "",
        thesis.get("thesis", "")[:300],
        "",
    ]

    # Exposed
    exposed = thesis.get("exposed_companies", [])
    if exposed:
        lines.append("*Exposed:*")
        for c in exposed[:4]:
            if not c["name"].startswith(("Every ", "Any ", "Companies ")):
                ticker = f" [{c.get('ticker')}]" if c.get("ticker") not in ("various", "", None) else ""
                lines.append(f"  {c['name']}{ticker} — {c.get('risk', '')[:80]}")
        lines.append("")

    # Beneficiaries
    beneficiaries = thesis.get("beneficiaries", [])
    if beneficiaries:
        lines.append("*Winners:*")
        for b in beneficiaries[:4]:
            ticker = f" [{b.get('ticker')}]" if b.get("ticker") not in ("private", "private/open-source", "", None) else ""
            lines.append(f"  {b['name']}{ticker} — {b.get('why', '')[:80]}")
        lines.append("")

    # Signal history
    if signals:
        lines.append(f"*Recent signals ({len(signals)}):*")
        for s in signals:
            ts = s["ts"][:10]
            lines.append(f"  {ts}: {s['content'][:100]}")
        lines.append("")

    # Watchlist
    triggers = thesis.get("watchlist_triggers", [])[:3]
    if triggers:
        lines.append("*Watching for:*")
        for t in triggers:
            lines.append(f"  {t[:80]}")

    return "\n".join(lines)


def disruption_overview() -> str:
    """All theses summary."""
    theses = load_theses()
    if not theses:
        return "No disruption theses loaded."

    # Get signal counts per thesis
    counts = {}
    for row in DB.execute("SELECT thesis_id, COUNT(*) as cnt FROM signals GROUP BY thesis_id").fetchall():
        counts[row["thesis_id"]] = row["cnt"]

    priority = {"very_high": 0, "high": 1, "medium-high": 2, "medium": 3}
    theses_sorted = sorted(theses, key=lambda t: priority.get(t.get("confidence", "medium"), 3))

    lines = [f"*Disruption Radar* ({len(theses)} theses)", ""]

    for t in theses_sorted:
        conf = t.get("confidence", "?").replace("_", " ")
        signal_count = counts.get(t["id"], 0)
        signal_str = f" | {signal_count} signals" if signal_count else ""
        lines.append(f"*{t['name']}* [{conf}]{signal_str}")
        brief = t.get("morning_brief", "").split(".")[0][:100]
        lines.append(f"  {brief}.")
        lines.append(f"  /tech thesis {t['id']}")
        lines.append("")

    return "\n".join(lines)


def vulnerable() -> str:
    """Most exposed companies across theses."""
    theses = load_theses()
    exposures: dict[str, list[str]] = {}

    for t in theses:
        for c in t.get("exposed_companies", []):
            name = c.get("name", "")
            if name.startswith(("Every ", "Any ", "Companies ")):
                continue
            exposures.setdefault(name, []).append(t["name"][:40])

    ranked = sorted(exposures.items(), key=lambda x: len(x[1]), reverse=True)

    lines = ["*Most Exposed Companies*", ""]
    for name, thesis_names in ranked[:12]:
        lines.append(f"*{name}* — {len(thesis_names)} exposure(s)")
        for tn in thesis_names:
            lines.append(f"  {tn}")
        lines.append("")

    return "\n".join(lines)


def beneficiaries() -> str:
    """Top beneficiary companies."""
    theses = load_theses()
    benefits: dict[str, list[str]] = {}

    for t in theses:
        for b in t.get("beneficiaries", []):
            name = b.get("name", "")
            benefits.setdefault(name, []).append(t["name"][:40])

    ranked = sorted(benefits.items(), key=lambda x: len(x[1]), reverse=True)

    lines = ["*Top Beneficiaries*", ""]
    for name, thesis_names in ranked[:12]:
        lines.append(f"*{name}* — {len(thesis_names)} tailwind(s)")
        for tn in thesis_names:
            lines.append(f"  {tn}")
        lines.append("")

    return "\n".join(lines)


def lookup_company(query: str) -> str:
    """Company-centric view: find a company across ALL theses and aggregate risk/opportunity."""
    theses = load_theses()
    q = query.lower().strip()

    exposures: list[dict] = []
    tailwinds: list[dict] = []

    for t in theses:
        conf = t.get("confidence", "?").replace("_", " ")
        tf = t.get("timeframe", "?")
        for c in t.get("exposed_companies", []):
            name = c.get("name", "")
            ticker = c.get("ticker", "")
            if q in name.lower() or q == ticker.lower():
                exposures.append({
                    "thesis": t["name"], "thesis_id": t["id"],
                    "risk": c.get("risk", ""), "detail": c.get("detail", ""),
                    "confidence": conf, "timeframe": tf,
                })
        for b in t.get("beneficiaries", []):
            name = b.get("name", "")
            ticker = b.get("ticker", "")
            if q in name.lower() or q == ticker.lower():
                tailwinds.append({
                    "thesis": t["name"], "thesis_id": t["id"],
                    "why": b.get("why", ""),
                    "confidence": conf, "timeframe": tf,
                })

    if not exposures and not tailwinds:
        # Fall back to live Perplexity research
        research_query = (
            f"Investment profile for {query}: current stock price, market cap, "
            f"recent earnings, key risks, AI exposure, competitive position, "
            f"and any recent news. Be specific with numbers."
        )
        result = perplexity(research_query, condense=False)
        return f"\U0001f3af *{query.upper()}*\n\n_Not in thesis data — live research:_\n\n{result}"

    # Determine the display name from the first match
    display = query.upper()
    for t in theses:
        for c in t.get("exposed_companies", []) + t.get("beneficiaries", []):
            name = c.get("name", "")
            ticker = c.get("ticker", "")
            if q in name.lower() or q == ticker.lower():
                tk = f" [{ticker}]" if ticker and ticker not in ("various", "private") else ""
                display = f"{name}{tk}"
                break
        if display != query.upper():
            break

    lines = [f"\U0001f3af *{display}*", ""]

    if exposures:
        lines.append(f"\u26a0\ufe0f *EXPOSED IN {len(exposures)} THESIS{'ES' if len(exposures) != 1 else ''}*")
        for e in exposures:
            lines.append(f"  *{e['thesis']}* [{e['confidence']}]")
            lines.append(f"  Risk: {e['risk']}")
            if e["detail"]:
                lines.append(f"  {e['detail'][:120]}")
            lines.append(f"  Timeframe: {e['timeframe']}")
            lines.append(f"  /tech thesis {e['thesis_id']}")
            lines.append("")

    if tailwinds:
        lines.append(f"\u2705 *BENEFITS FROM {len(tailwinds)} THESIS{'ES' if len(tailwinds) != 1 else ''}*")
        for tw in tailwinds:
            lines.append(f"  *{tw['thesis']}* [{tw['confidence']}]")
            lines.append(f"  Why: {tw['why']}")
            lines.append(f"  Timeframe: {tw['timeframe']}")
            lines.append(f"  /tech thesis {tw['thesis_id']}")
            lines.append("")

    # Verdict
    net = len(tailwinds) - len(exposures)
    if net > 0:
        verdict = f"\U0001f7e2 Net positive ({len(tailwinds)} tailwinds vs {len(exposures)} exposures)"
    elif net < 0:
        verdict = f"\U0001f534 Net negative ({len(exposures)} exposures vs {len(tailwinds)} tailwinds)"
    else:
        verdict = f"\U0001f7e1 Mixed ({len(exposures)} exposures, {len(tailwinds)} tailwinds)"
    lines.append(f"*VERDICT:* {verdict}")

    return "\n".join(lines)


def search_theses(query: str) -> str:
    """Search across all theses for a company or topic."""
    theses = load_theses()
    query_lower = query.lower()
    words = [w for w in query_lower.split() if len(w) > 2]

    results = []
    for t in theses:
        searchable = " ".join([
            t.get("name", ""), t.get("thesis", ""), t.get("morning_brief", ""),
            " ".join(c.get("name", "") + " " + c.get("risk", "") + " " + c.get("ticker", "")
                     for c in t.get("exposed_companies", [])),
            " ".join(b.get("name", "") + " " + b.get("why", "") + " " + b.get("ticker", "")
                     for b in t.get("beneficiaries", [])),
        ]).lower()
        score = sum(1 for w in words if w in searchable)
        if score > 0:
            results.append((score, t))

    results.sort(key=lambda x: x[0], reverse=True)

    if not results:
        return f"No matches for '{query}'. Try /tech disruption for full list."

    # Record interest for top match
    _record_interest(results[0][1]["id"])

    lines = [f"*Search: {query}*", ""]
    for _, t in results[:4]:
        lines.append(f"*{t['name']}*")
        brief = t.get("morning_brief", "").split(".")[0][:100]
        lines.append(f"  {brief}.")
        lines.append(f"  /tech thesis {t['id']}")
        lines.append("")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# PIS LANDSCAPE (people library + company signals — read-only)
# ═══════════════════════════════════════════════════════════════════════════════

def pis_landscape() -> str:
    """PIS tech landscape: tools, voices, clusters from people library."""
    people_path = THESES_PATH.parent.parent / "people-library" / "v1.1" / "people_library_v1.1.yaml"
    signals_path = THESES_PATH.parent.parent / "people-library" / "v1.1" / "people_library_company_signals_v1.1.yaml"

    if not people_path.exists():
        return "PIS people library not found."

    with open(people_path) as f:
        content = f.read()
    docs = list(yaml.safe_load_all(content))
    people_data = {}
    for doc in docs:
        if doc:
            people_data.update(doc)
    profiles = people_data.get("profiles", [])
    active = [p for p in profiles if p.get("status") != "archived"]

    lines = [
        f"*Tech Landscape* ({len(active)} voices)",
        "",
    ]

    # Signals (tools) if available
    if signals_path.exists():
        with open(signals_path) as f:
            sig_content = f.read()
        sig_docs = list(yaml.safe_load_all(sig_content))
        sig_data = {}
        for doc in sig_docs:
            if doc:
                sig_data.update(doc)
        signals = sig_data.get("signals", [])

        tier1 = [s for s in signals if s.get("signal_tier") == 1]
        if tier1:
            lines.append("*Tier 1 Tools:*")
            for t in tier1[:8]:
                recs = ", ".join(r.get("name", "?") for r in t.get("recommenders", [])[:2])
                lines.append(f"  {t.get('tool', '?')} — {t.get('palette_action', '?')} ({recs})")
            lines.append("")

        actions = sig_data.get("actions_summary", {})
        for action_type in ("integrate", "evaluate"):
            a = actions.get(action_type, {})
            tools = a.get("tools", [])
            if tools:
                lines.append(f"*{action_type.upper()}*: {', '.join(tools[:6])}")
        lines.append("")

    # Cluster summary
    clusters: dict[str, list[str]] = {}
    for p in active:
        cluster = p.get("cluster", p.get("domain", "other"))
        if isinstance(cluster, list):
            cluster = cluster[0] if cluster else "other"
        clusters.setdefault(cluster, []).append(p.get("name", "?"))

    lines.append("*Voice Clusters:*")
    for cluster_name, members in sorted(clusters.items()):
        display = cluster_name.replace("_", " ").title()
        lines.append(f"  {display}: {', '.join(members[:4])}")
    lines.append("")

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# MORNING BRIEF (diff-based, narrator-filtered)
# ═══════════════════════════════════════════════════════════════════════════════

def morning_brief(chat_id: int) -> None:
    """The ONE morning command. Diff-based, phone-optimized, with buttons."""
    theses = load_theses()
    now = datetime.now()
    day_str = now.strftime("%a %b %d")

    lines = [f"*{day_str}*", ""]

    # ── NEW: Perplexity scan (only if we haven't scanned in last 6 hours) ──
    last_scan = _get_state("last_news_scan")
    news_items = []

    if PERPLEXITY_KEY and (not last_scan or _hours_since(last_scan) >= 6):
        news_items = _scan_news(theses)
        _set_state("last_news_scan", now.isoformat())

    if news_items:
        lines.append("*NEW*")
        for item in news_items[:3]:
            lines.append(f"  {item['text'][:140]}")
            if item.get("thesis"):
                tag = item["thesis"].replace("DISRUPT-", "").lower().replace("-", " ")
                lines.append(f"  _{tag}_")
            lines.append("")
    else:
        lines.append("*NEW*")
        lines.append("  No major events since last check")
        lines.append("")

    # ── TRENDS: rotate 2 theses not shown in 7 days ──
    shown_recently = _get_state("trends_shown_ids") or ""
    shown_list = [s for s in shown_recently.split(",") if s]
    eligible = [t for t in theses if t["id"] not in shown_list]

    if not eligible:
        _set_state("trends_shown_ids", "")
        eligible = theses[:]

    priority = {"very_high": 0, "high": 1, "medium-high": 2, "medium": 3}
    eligible.sort(key=lambda t: priority.get(t.get("confidence", "medium"), 3))

    # Weight by user interest
    interests = _get_all_interests()
    for t in eligible:
        t["_weight"] = interests.get(t["id"], 0)
    eligible.sort(key=lambda t: (-t.get("_weight", 0), priority.get(t.get("confidence", "medium"), 3)))

    picks = eligible[:2]
    if picks:
        lines.append(f"*TRENDS* ({len(theses)} tracked)")
        for t in picks:
            conf = t.get("confidence", "?").replace("_", " ")
            brief = t.get("morning_brief", "").strip().split(".")[0][:120]
            lines.append(f"  *{t['name']}* [{conf}]")
            lines.append(f"  {brief}.")
            lines.append("")

        # Mark shown
        new_shown = shown_list + [t["id"] for t in picks]
        _set_state("trends_shown_ids", ",".join(new_shown[-20:]))  # keep last 20

    text = "\n".join(lines)

    # Buttons
    buttons = [
        [
            {"text": "\u26a1 Disruption", "callback_data": "cb:run:disruption"},
            {"text": "\U0001f3af Exposed", "callback_data": "cb:run:vulnerable"},
            {"text": "\U0001f3c6 Winners", "callback_data": "cb:run:beneficiaries"},
        ],
    ]

    # Research buttons for news items
    for item in news_items[:2]:
        key = _store_research(item.get("research_prompt", item["text"][:60]))
        label = item["text"][:28] + "..."
        buttons.append([{"text": f"\U0001f50d {label}", "callback_data": f"cb:research:{key}"}])

    send(chat_id, text, buttons=buttons)


def _scan_news(theses: list[dict]) -> list[dict]:
    """Scan last 24h for thesis-relevant events. Returns structured items."""
    triggers = []
    for t in theses:
        for trigger in t.get("watchlist_triggers", [])[:2]:
            triggers.append(trigger)

    system = (
        "You are a tech investment analyst. Scan the last 24 hours ONLY.\n"
        "Report events matching these triggers:\n"
        + "\n".join(f"- {t}" for t in triggers[:12]) + "\n\n"
        "Rules:\n"
        "- ONLY events from last 24 hours\n"
        "- ONLY materially significant (funding >$100M, GA launches, regulatory, earnings)\n"
        "- If NOTHING significant: respond with NO_NEWS\n"
        "- Maximum 4 items, one sentence each with specific numbers\n"
        "- Format: COMPANY: what happened (numbers)\n"
    )

    try:
        resp = _client.post(
            PERPLEXITY_URL,
            headers={"Authorization": f"Bearer {PERPLEXITY_KEY}", "Content-Type": "application/json"},
            json={
                "model": "sonar",
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": "What significant tech/AI/market events happened in the last 24 hours?"},
                ],
            },
            timeout=30.0,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[news] error: {e}", flush=True)
        return []

    if "NO_NEWS" in content:
        return []

    items = []
    for line in content.strip().split("\n"):
        line = line.strip().lstrip("- *")
        if line and len(line) > 10:
            # Match to thesis
            thesis_id = _match_thesis(line, theses)
            items.append({
                "text": line,
                "thesis": thesis_id,
                "research_prompt": line.split(".")[0][:60],
            })
            # Record signal
            if thesis_id:
                DB.execute("INSERT INTO signals (ts, thesis_id, content, source) VALUES (?, ?, ?, ?)",
                           (datetime.now().isoformat(), thesis_id, line[:300], "news_scan"))
                DB.commit()

    return items[:4]


def _match_thesis(text: str, theses: list[dict]) -> str | None:
    """Match a news item to a thesis. Returns thesis_id or None."""
    text_lower = text.lower()
    best_id = None
    best_score = 0

    for t in theses:
        score = 0
        for c in t.get("exposed_companies", []) + t.get("beneficiaries", []):
            name = c.get("name", "")
            for word in name.lower().split():
                if len(word) > 3 and word in text_lower:
                    score += 2
        for trigger in t.get("watchlist_triggers", []):
            words = [w for w in trigger.lower().split() if len(w) > 3]
            score += sum(1 for w in words if w in text_lower)

        if score > best_score:
            best_score = score
            best_id = t["id"]

    return best_id if best_score >= 3 else None


# ═══════════════════════════════════════════════════════════════════════════════
# MARKET STRESS
# ═══════════════════════════════════════════════════════════════════════════════

CAPE_BANDS = [(15, 0.08, "Undervalued"), (20, 0.12, "Fair"), (25, 0.18, "Elevated"),
              (30, 0.28, "High"), (35, 0.38, "Very high"), (40, 0.48, "Extreme"), (999, 0.58, "Unprecedented")]
BUFFETT_BANDS = [(75, 0.06, "Undervalued"), (90, 0.10, "Fair"), (115, 0.16, "Elevated"),
                 (150, 0.28, "High"), (180, 0.40, "Very high"), (999, 0.55, "Extreme")]
PS_BANDS = [(1.0, 0.06, "Undervalued"), (1.5, 0.10, "Fair"), (2.0, 0.18, "Elevated"),
            (2.5, 0.30, "High"), (3.0, 0.42, "Very high"), (999, 0.55, "Extreme")]


def cmd_stress() -> str:
    """Market stress probability."""
    if not PERPLEXITY_KEY:
        return "Requires Perplexity API."

    system = """Reply with ONLY three lines:
CAPE: <number>
BUFFETT: <number>
PS: <number>
Use the most recent Shiller PE, Buffett Indicator (market cap/GDP %), and S&P 500 P/S ratio."""

    try:
        resp = _client.post(
            PERPLEXITY_URL,
            headers={"Authorization": f"Bearer {PERPLEXITY_KEY}", "Content-Type": "application/json"},
            json={"model": "sonar", "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": "Current Shiller PE CAPE, Buffett Indicator, S&P 500 P/S ratio?"},
            ]},
            timeout=30.0,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error fetching metrics: {e}"

    # Parse
    values = {}
    for key, label in [("cape", "CAPE"), ("buffett", "BUFFETT"), ("ps", "PS")]:
        m = re.search(rf'{label}\s*[:=]\s*([\d.]+)', content)
        if m:
            values[key] = float(m.group(1))

    if len(values) < 3:
        return f"Couldn't parse metrics.\nRaw: {content[:300]}"

    # Score
    def score(val, bands):
        for upper, risk, label in bands:
            if val <= upper:
                return risk, label
        return bands[-1][1], bands[-1][2]

    cape_risk, cape_label = score(values["cape"], CAPE_BANDS)
    buff_risk, buff_label = score(values["buffett"], BUFFETT_BANDS)
    ps_risk, ps_label = score(values["ps"], PS_BANDS)

    composite = 0.40 * cape_risk + 0.35 * buff_risk + 0.25 * ps_risk
    elevated = sum(1 for r in [cape_risk, buff_risk, ps_risk] if r >= 0.16)
    if elevated == 3:
        composite = min(composite * 1.15, 0.70)

    if composite < 0.12: label = "LOW"
    elif composite < 0.20: label = "MODERATE"
    elif composite < 0.35: label = "ELEVATED"
    elif composite < 0.50: label = "HIGH"
    else: label = "SEVERE"

    return (
        f"*Market Stress: {label}*\n"
        f"P(>20% drawdown, 12mo): *{composite:.0%}*\n\n"
        f"CAPE: {values['cape']:.1f} ({cape_label}) — {values['cape']/16.5:.1f}x avg\n"
        f"Buffett: {values['buffett']:.0f}% ({buff_label}) — {values['buffett']/80:.1f}x avg\n"
        f"P/S: {values['ps']:.2f} ({ps_label}) — {values['ps']/1.4:.1f}x avg\n\n"
        f"_{elevated}/3 metrics elevated or higher._"
    )


# ═══════════════════════════════════════════════════════════════════════════════
# INTEL (reads from intel engine data)
# ═══════════════════════════════════════════════════════════════════════════════

def cmd_intel(query: str) -> str:
    """Financial intelligence from voices library."""
    voices_path = INTEL_DIR / "people-library" / "v1.0" / "financial_voices.yaml"
    categories_path = INTEL_DIR / "thesis-categories" / "v1.0" / "categories.yaml"

    if not voices_path.exists():
        return "Intel data not found."

    with open(voices_path) as f:
        voices_data = yaml.safe_load(f) or {}
    voices = voices_data.get("profiles", [])

    with open(categories_path) as f:
        cat_data = yaml.safe_load(f) or {}
    categories = cat_data.get("categories", [])

    if not query:
        # Brief: show all categories with voice counts and top voices
        lines = ["*Intel Brief*", ""]
        for cat in categories:
            cat_voices = [v for v in voices if cat["id"] in v.get("thesis_categories", [])]
            top_names = ", ".join(v["name"] for v in cat_voices[:3] if v.get("signal_quality") == "high")
            lines.append(f"*{cat['name']}*")
            lines.append(f"  Voices: {len(cat_voices)}" + (f" | Top: {top_names}" if top_names else ""))
            lines.append("")
        return "\n".join(lines)
    else:
        # Search voices + categories
        query_lower = query.lower()

        # Match categories by ID or name
        matched_cat = None
        for cat in categories:
            if query_lower in cat["id"].lower() or query_lower in cat["name"].lower():
                matched_cat = cat
                break

        if matched_cat:
            cat_voices = [v for v in voices if matched_cat["id"] in v.get("thesis_categories", [])]
            lines = [f"*{matched_cat['name']}*", f"Voices: {len(cat_voices)}", ""]
            for v in sorted(cat_voices, key=lambda x: x.get("signal_quality", "") == "high", reverse=True):
                lines.append(f"*{v['name']}* ({v.get('signal_quality', '?')})")
                lines.append(f"  {v.get('why_follow', '')[:100]}")
                lines.append("")
            return "\n".join(lines)

        # Match voices by name, tags, cluster
        matching = [v for v in voices
                    if query_lower in v.get("name", "").lower()
                    or query_lower in " ".join(v.get("expertise_tags", [])).lower()
                    or query_lower in v.get("cluster", "").lower()
                    or query_lower in v.get("why_follow", "").lower()]

        if matching:
            lines = [f"*Intel: {query}*", ""]
            for v in matching[:5]:
                lines.append(f"*{v['name']}* ({v.get('signal_quality', '?')})")
                cats_str = ", ".join(v.get("thesis_categories", [])[:3])
                lines.append(f"  {v.get('why_follow', '')[:80]}")
                if cats_str:
                    lines.append(f"  Covers: {cats_str}")
                lines.append("")
            return "\n".join(lines)
        else:
            return perplexity(f"financial analysis: {query}")


# ═══════════════════════════════════════════════════════════════════════════════
# STATE HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def _get_state(key: str) -> str | None:
    row = DB.execute("SELECT value FROM brief_state WHERE key = ?", (key,)).fetchone()
    return row["value"] if row else None


def _set_state(key: str, value: str) -> None:
    DB.execute("INSERT OR REPLACE INTO brief_state (key, value) VALUES (?, ?)", (key, value))
    DB.commit()


def _hours_since(iso_ts: str) -> float:
    dt = datetime.fromisoformat(iso_ts)
    return (datetime.now() - dt).total_seconds() / 3600


def _record_interest(thesis_id: str) -> None:
    DB.execute("""
        INSERT INTO user_interests (thesis_id, tap_count, last_accessed) VALUES (?, 1, ?)
        ON CONFLICT(thesis_id) DO UPDATE SET tap_count = tap_count + 1, last_accessed = ?
    """, (thesis_id, datetime.now().isoformat(), datetime.now().isoformat()))
    DB.commit()


def _get_all_interests() -> dict[str, int]:
    rows = DB.execute("SELECT thesis_id, tap_count FROM user_interests").fetchall()
    return {r["thesis_id"]: r["tap_count"] for r in rows}


# Callback research storage
_pending_research: dict[str, str] = {}
_research_counter = 0


def _store_research(query: str) -> str:
    global _research_counter
    _research_counter += 1
    key = f"r{_research_counter}"
    _pending_research[key] = query
    if len(_pending_research) > 50:
        for k in list(_pending_research.keys())[:20]:
            del _pending_research[k]
    return key


# ═══════════════════════════════════════════════════════════════════════════════
# MONITOR SCHEDULER (runs between poll cycles)
# ═══════════════════════════════════════════════════════════════════════════════

def run_monitors() -> None:
    """Check all monitors and fire if schedule elapsed. Called between poll cycles."""
    if not PERPLEXITY_KEY:
        return

    if not MONITORS_DIR.exists():
        # Copy monitors from theses source if available
        src = THESES_PATH.parent.parent.parent / "mission-canvas" / "workspaces" / "oil-investor" / "monitors"
        if not src.exists():
            src = Path("/root/fde/palette/mission-canvas/workspaces/oil-investor/monitors")
        if src.exists():
            import shutil
            for f in src.glob("*.yaml"):
                dest = MONITORS_DIR / f.name
                if not dest.exists():
                    shutil.copy2(f, dest)

    for monitor_file in MONITORS_DIR.glob("*.yaml"):
        try:
            with open(monitor_file) as f:
                data = yaml.safe_load(f) or {}
            monitor = data.get("monitor", {})
            if not monitor.get("enabled", True):
                continue

            # Check schedule
            last_run = monitor.get("last_run")
            schedule = monitor.get("schedule_minutes", 720)
            if last_run:
                elapsed = (datetime.now() - datetime.fromisoformat(last_run)).total_seconds() / 60
                if elapsed < schedule:
                    continue

            # Run monitor
            queries = monitor.get("search_queries", [])
            system_prompt = monitor.get("system_prompt", "")
            combined = "Brief update on:\n" + "\n".join(f"- {q}" for q in queries)

            resp = _client.post(
                PERPLEXITY_URL,
                headers={"Authorization": f"Bearer {PERPLEXITY_KEY}", "Content-Type": "application/json"},
                json={"model": "sonar", "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": combined},
                ]},
                timeout=60.0,
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"]

            # Update last_run
            monitor["last_run"] = datetime.now().isoformat()
            data["monitor"] = monitor
            with open(monitor_file, "w") as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)

            # Check for NO_TRIGGER
            if "NO_TRIGGER" in content or len(content.strip()) < 20:
                print(f"[monitor] '{monitor['id']}' — no trigger", flush=True)
                continue

            # Alert!
            print(f"[monitor] '{monitor['id']}' — ALERT", flush=True)
            alert_text = _narrator_condense(content) if len(content) > 300 else content

            # Store signal
            DB.execute("INSERT INTO signals (ts, thesis_id, content, source, monitor_id) VALUES (?, ?, ?, ?, ?)",
                       (datetime.now().isoformat(), None, alert_text[:500], "monitor", monitor["id"]))
            DB.commit()

            # Notify
            if TELEGRAM_CHAT_ID:
                send(int(TELEGRAM_CHAT_ID),
                     f"\U0001f514 *{monitor.get('name', monitor['id'])}*\n\n{alert_text[:3000]}")

        except Exception as e:
            print(f"[monitor] error {monitor_file.name}: {e}", flush=True)


# ═══════════════════════════════════════════════════════════════════════════════
# COMMAND HANDLERS
# ═══════════════════════════════════════════════════════════════════════════════

def handle_message(chat_id: int, text: str) -> None:
    text = text.strip()
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] chat={chat_id} | {text[:80]}", flush=True)

    try:
        if text.startswith("/start") or text.startswith("/help"):
            cmd_help(chat_id)
            return

        if text.startswith("/brief"):
            typing(chat_id)
            morning_brief(chat_id)
            return

        if text.startswith("/stress"):
            typing(chat_id)
            send(chat_id, cmd_stress())
            return

        if text.startswith("/tech"):
            typing(chat_id)
            arg = text[5:].strip()
            if not arg or arg in ("disruption", "disrupt"):
                send(chat_id, disruption_overview())
            elif arg.startswith("thesis "):
                send(chat_id, thesis_brief(arg[7:].strip()))
            elif arg in ("vulnerable", "exposed"):
                send(chat_id, vulnerable())
            elif arg in ("beneficiaries", "winners"):
                send(chat_id, beneficiaries())
            elif arg in ("landscape", "pis", "tools", "voices"):
                send(chat_id, pis_landscape())
            elif arg.startswith(("company ", "ticker ", "lookup ")):
                company_name = arg.split(None, 1)[1]
                _company_context[chat_id] = {"company": company_name, "ts": time.time()}
                send(chat_id, lookup_company(company_name))
            else:
                send(chat_id, search_theses(arg))
            return

        if text.startswith("/intel"):
            typing(chat_id)
            arg = text[6:].strip()
            send(chat_id, cmd_intel(arg))
            return

        if text.startswith("/research "):
            query = text[10:].strip()
            if not query:
                send(chat_id, "Usage: /research Will Databricks displace AWS?")
                return
            typing(chat_id)
            result = perplexity(query)
            # Log research
            thesis_id = _match_thesis(query, load_theses())
            DB.execute("INSERT INTO research_log (ts, query, result, thesis_id) VALUES (?, ?, ?, ?)",
                       (datetime.now().isoformat(), query, result[:1000], thesis_id))
            DB.commit()
            send(chat_id, f"\U0001f50d *{query[:50]}*\n\n{result}")
            return

        if text.startswith("/monitors"):
            typing(chat_id)
            if not MONITORS_DIR.exists():
                send(chat_id, "No monitors configured.")
                return
            lines = ["*Active Monitors*", ""]
            for f in MONITORS_DIR.glob("*.yaml"):
                with open(f) as fh:
                    data = yaml.safe_load(fh) or {}
                m = data.get("monitor", {})
                last = m.get("last_run", "never")
                if isinstance(last, str) and len(last) > 16:
                    last = last[:16]
                lines.append(f"*{m.get('name', m.get('id', f.stem))}*")
                lines.append(f"  Every {m.get('schedule_minutes', '?')}m | Last: {last}")
                lines.append("")
            send(chat_id, "\n".join(lines))
            return

        if text.startswith("/signals"):
            typing(chat_id)
            rows = DB.execute("SELECT ts, thesis_id, content FROM signals ORDER BY ts DESC LIMIT 10").fetchall()
            if not rows:
                send(chat_id, "No signals recorded yet.")
                return
            lines = ["*Recent Signals*", ""]
            for r in rows:
                ts_short = r["ts"][:10]
                thesis = r["thesis_id"] or "unclassified"
                lines.append(f"{ts_short} [{thesis}]")
                lines.append(f"  {r['content'][:100]}")
                lines.append("")
            send(chat_id, "\n".join(lines))
            return

        # ── Company follow-up: if we have an active company context, route there first ──
        ctx = _company_context.get(chat_id)
        if ctx and (time.time() - ctx["ts"]) < COMPANY_CTX_TIMEOUT:
            typing(chat_id)
            company = ctx["company"]
            ctx["ts"] = time.time()  # refresh timeout on each follow-up
            follow_up_query = f"Regarding {company}: {text}"
            result = perplexity(follow_up_query, condense=False)
            DB.execute("INSERT INTO research_log (ts, query, result, thesis_id) VALUES (?, ?, ?, ?)",
                       (datetime.now().isoformat(), follow_up_query, result[:1000], None))
            DB.commit()
            send(chat_id, f"\U0001f3af *{company.title()}* — follow-up\n\n{result}")
            return

        # ── Default: smart routing ──
        typing(chat_id)

        # Check if it matches a thesis search
        theses_result = search_theses(text)
        if "No matches" not in theses_result:
            send(chat_id, theses_result)
            return

        # Fall through to Perplexity research
        result = perplexity(text)
        thesis_id = _match_thesis(text, load_theses())
        DB.execute("INSERT INTO research_log (ts, query, result, thesis_id) VALUES (?, ?, ?, ?)",
                   (datetime.now().isoformat(), text, result[:1000], thesis_id))
        DB.commit()
        send(chat_id, result)

    except Exception as e:
        print(f"[error] {e}", flush=True)
        send(chat_id, f"Error: {e}")


def handle_callback(callback: dict) -> None:
    """Handle inline button taps."""
    cb_id = callback["id"]
    chat_id = callback["message"]["chat"]["id"]
    data = callback.get("data", "")

    parts = data.split(":", 2)
    if len(parts) < 3:
        answer_callback(cb_id)
        return

    _, cb_type, payload = parts

    if cb_type == "research":
        query = _pending_research.get(payload)
        if not query:
            answer_callback(cb_id, "Expired — ask again")
            return
        answer_callback(cb_id, "Searching...")
        typing(chat_id)
        result = perplexity(query)
        DB.execute("INSERT INTO research_log (ts, query, result, thesis_id) VALUES (?, ?, ?, ?)",
                   (datetime.now().isoformat(), query, result[:1000], None))
        DB.commit()
        send(chat_id, f"\U0001f50d *{query[:50]}*\n\n{result}")

    elif cb_type == "run":
        answer_callback(cb_id)
        typing(chat_id)
        if payload == "disruption":
            send(chat_id, disruption_overview())
        elif payload == "vulnerable":
            send(chat_id, vulnerable())
        elif payload == "beneficiaries":
            send(chat_id, beneficiaries())
        elif payload == "brief":
            morning_brief(chat_id)
        elif payload == "intel":
            send(chat_id, cmd_intel(""))
        elif payload == "stress":
            send(chat_id, cmd_stress())
        elif payload.startswith("thesis_"):
            send(chat_id, thesis_brief(payload[7:]))
        elif payload == "research_prompt":
            send(chat_id, "Just type your question — I'll research it.\n\n_Examples:_\n_Will Databricks displace AWS?_\n_Redis Agent Memory Server latest_")
        elif payload == "signals":
            rows = DB.execute("SELECT ts, thesis_id, content FROM signals ORDER BY ts DESC LIMIT 10").fetchall()
            if not rows:
                send(chat_id, "No signals recorded yet.")
            else:
                lines = ["*Recent Signals*", ""]
                for r in rows:
                    lines.append(f"{r['ts'][:10]} [{r['thesis_id'] or '?'}]")
                    lines.append(f"  {r['content'][:100]}")
                    lines.append("")
                send(chat_id, "\n".join(lines))
        elif payload == "monitors":
            lines = ["*Active Monitors*", ""]
            for f in MONITORS_DIR.glob("*.yaml"):
                with open(f) as fh:
                    data = yaml.safe_load(fh) or {}
                m = data.get("monitor", {})
                last = m.get("last_run", "never")
                if isinstance(last, str) and len(last) > 16:
                    last = last[:16]
                lines.append(f"*{m.get('name', m.get('id', f.stem))}*")
                lines.append(f"  Every {m.get('schedule_minutes', '?')}m | Last: {last}")
                lines.append("")
            send(chat_id, "\n".join(lines))
        else:
            send(chat_id, f"Unknown: {payload}")

    elif cb_type == "cmd":
        answer_callback(cb_id)
        typing(chat_id)
        if payload == "stress":
            send(chat_id, cmd_stress())
        elif payload == "vulnerable":
            send(chat_id, vulnerable())
        elif payload == "beneficiaries":
            send(chat_id, beneficiaries())

    else:
        answer_callback(cb_id)


def cmd_help(chat_id: int) -> None:
    """Help with tappable buttons."""
    text = "*Investment Intelligence Bot*\n\nTap any button or type a question."

    buttons = [
        [
            {"text": "\u2600\ufe0f Brief", "callback_data": "cb:run:brief"},
            {"text": "\U0001f4b9 Stress", "callback_data": "cb:run:stress"},
            {"text": "\U0001f4ca Intel", "callback_data": "cb:run:intel"},
        ],
        [
            {"text": "\u26a1 Disruption", "callback_data": "cb:run:disruption"},
            {"text": "\U0001f3af Exposed", "callback_data": "cb:run:vulnerable"},
            {"text": "\U0001f3c6 Winners", "callback_data": "cb:run:beneficiaries"},
        ],
        [
            {"text": "\u2601\ufe0f Cloud Peak", "callback_data": "cb:run:thesis_DISRUPT-CLOUD-PEAK"},
            {"text": "\U0001f512 Security", "callback_data": "cb:run:thesis_DISRUPT-AGENT-SECURITY"},
            {"text": "\U0001f4be Context", "callback_data": "cb:run:thesis_DISRUPT-CONTEXT-ENGINE"},
        ],
        [
            {"text": "\U0001f4bb Code Crisis", "callback_data": "cb:run:thesis_DISRUPT-CODE-SUPPLY"},
            {"text": "\U0001f3ed On-Prem", "callback_data": "cb:run:thesis_DISRUPT-LEGACY-COMEBACK"},
            {"text": "\U0001f4a1 Inference", "callback_data": "cb:run:thesis_DISRUPT-INFERENCE-ECONOMICS"},
        ],
        [
            {"text": "\U0001f50d Research...", "callback_data": "cb:run:research_prompt"},
            {"text": "\U0001f4c8 Signals", "callback_data": "cb:run:signals"},
            {"text": "\U0001f4e1 Monitors", "callback_data": "cb:run:monitors"},
        ],
    ]

    send(chat_id, text, buttons=buttons)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════════════════════════

def run() -> None:
    global DB

    if not BOT_TOKEN:
        print("[bot] JOSEPH_BOT_TOKEN not set.", flush=True)
        sys.exit(1)

    DB = init_db()
    print(f"[bot] v2 starting", flush=True)
    print(f"[bot] Perplexity: {'ON' if PERPLEXITY_KEY else 'OFF'}", flush=True)
    print(f"[bot] Theses: {THESES_PATH} ({'found' if THESES_PATH.exists() else 'NOT FOUND'})", flush=True)
    print(f"[bot] DB: {DB_PATH}", flush=True)

    offset = 0
    last_monitor_check = 0

    while True:
        try:
            # ── Run monitors every 5 minutes ──
            now_ts = time.time()
            if now_ts - last_monitor_check > 300:
                try:
                    run_monitors()
                except Exception as e:
                    print(f"[monitor] error: {e}", flush=True)
                last_monitor_check = now_ts

            # ── Poll Telegram ──
            result = tg("getUpdates", offset=offset, timeout=POLL_TIMEOUT)
            if not result.get("ok"):
                time.sleep(5)
                continue

            for update in result.get("result", []):
                offset = update["update_id"] + 1

                # Callback queries (button taps)
                callback = update.get("callback_query")
                if callback:
                    try:
                        handle_callback(callback)
                    except Exception as e:
                        print(f"[error] callback: {e}", flush=True)
                    continue

                msg = update.get("message") or update.get("edited_message")
                if not msg:
                    continue

                chat_id = msg["chat"]["id"]
                text = msg.get("text") or msg.get("caption", "")

                if text:
                    try:
                        handle_message(chat_id, text)
                    except Exception as e:
                        print(f"[error] handle: {e}", flush=True)

        except KeyboardInterrupt:
            print("\n[bot] stopped.", flush=True)
            break
        except Exception as e:
            print(f"[error] poll: {e}", flush=True)
            time.sleep(5)


if __name__ == "__main__":
    run()
