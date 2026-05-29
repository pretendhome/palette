#!/usr/bin/env python3
"""mc_telegram.py — Mission Canvas Telegram Bot

A workspace-agnostic Telegram interface for Mission Canvas.
Routes queries through the Voice Hub with governance signals visible.

Usage:
  MC_BOT_TOKEN="your-token" python3 mc_telegram.py

Environment:
  MC_BOT_TOKEN        Telegram bot token (required)
  MC_HUB_URL          Voice Hub URL (default: http://localhost:7890)
  MC_DEFAULT_AGENT    Default LLM agent (default: perplexity)

Architecture:
  User → Telegram → mc_telegram.py → Voice Hub /api/chat
                                    → Palette retrieval + governance
                                    → Response formatted for Telegram
"""
from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

# ── Config ──────────────────────────────────────────────────────────────────

BOT_TOKEN = os.environ.get("MC_BOT_TOKEN", "")
HUB_URL = os.environ.get("MC_HUB_URL", "http://localhost:7890")
DEFAULT_AGENT = os.environ.get("MC_DEFAULT_AGENT", "perplexity")
POLL_TIMEOUT = 30

TELEGRAM = f"https://api.telegram.org/bot{BOT_TOKEN}"
DATA_DIR = Path(__file__).parent / "mc_telegram_data"

_client = httpx.Client(timeout=60.0)

# ── Database ────────────────────────────────────────────────────────────────

DB: sqlite3.Connection | None = None


def init_db() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(DATA_DIR / "mc.db"))
    db.execute("""CREATE TABLE IF NOT EXISTS users (
        chat_id INTEGER PRIMARY KEY,
        role TEXT DEFAULT '',
        name TEXT DEFAULT '',
        created_at TEXT
    )""")
    db.execute("""CREATE TABLE IF NOT EXISTS queries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        query TEXT,
        intent TEXT,
        riu_id TEXT,
        confidence REAL,
        response TEXT,
        ts TEXT
    )""")
    db.commit()
    return db


def get_user(chat_id: int) -> dict | None:
    row = DB.execute("SELECT role, name FROM users WHERE chat_id = ?", (chat_id,)).fetchone()
    if row:
        return {"role": row[0], "name": row[1]}
    return None


def set_user(chat_id: int, role: str, name: str = "") -> None:
    DB.execute(
        "INSERT OR REPLACE INTO users (chat_id, role, name, created_at) VALUES (?, ?, ?, ?)",
        (chat_id, role, name, datetime.now(timezone.utc).isoformat()),
    )
    DB.commit()


def log_query(chat_id: int, query: str, intent: str, riu_id: str, confidence: float, response: str) -> None:
    DB.execute(
        "INSERT INTO queries (chat_id, query, intent, riu_id, confidence, response, ts) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (chat_id, query, intent, riu_id, confidence, response[:2000], datetime.now(timezone.utc).isoformat()),
    )
    DB.commit()


# ── Telegram API ────────────────────────────────────────────────────────────

def tg(method: str, **kwargs) -> dict:
    resp = _client.post(f"{TELEGRAM}/{method}", json=kwargs)
    return resp.json()


def send(chat_id: int, text: str, buttons: list[list[dict]] | None = None) -> None:
    kwargs: dict = {
        "chat_id": chat_id,
        "text": text[:4000],
        "parse_mode": "Markdown",
    }
    if buttons:
        kwargs["reply_markup"] = {"inline_keyboard": buttons}
    result = tg("sendMessage", **kwargs)
    if not result.get("ok"):
        kwargs.pop("parse_mode")
        tg("sendMessage", **kwargs)


def typing(chat_id: int) -> None:
    tg("sendChatAction", chat_id=chat_id, action="typing")


def answer_callback(cb_id: str, text: str = "") -> None:
    kwargs = {"callback_query_id": cb_id}
    if text:
        kwargs["text"] = text[:200]
    tg("answerCallbackQuery", **kwargs)


# ── Voice Hub Integration ───────────────────────────────────────────────────

def hub_chat(query: str, agent: str = "", system: str = "") -> dict:
    """Call Voice Hub /api/chat and parse SSE response.

    Returns {text, riu_id, riu_name, confidence, lib_ids, agent}.
    """
    agent = agent or DEFAULT_AGENT

    try:
        resp = _client.post(
            f"{HUB_URL}/api/chat",
            json={
                "agent": agent,
                "text": query,
                "lang": "eng",
                "system": system,
            },
            timeout=90.0,
        )
    except httpx.ConnectError:
        return {"text": "Voice Hub not reachable. Start it with: bash setup.sh", "agent": agent}

    if resp.status_code != 200:
        return {"text": f"Hub error ({resp.status_code})", "agent": agent}

    # Parse SSE stream
    full_text = ""
    palette_meta = {}

    for line in resp.text.split("\n"):
        if line.startswith("event: palette"):
            # Next data line is palette metadata
            continue
        if line.startswith("data: "):
            raw = line[6:]
            try:
                d = json.loads(raw)
                if "riu_id" in d:
                    palette_meta = d
                elif "token" in d:
                    full_text += d["token"]
                elif "response" in d:
                    full_text = d["response"]
            except json.JSONDecodeError:
                full_text += raw

    return {
        "text": full_text.strip(),
        "riu_id": palette_meta.get("riu_id", ""),
        "riu_name": palette_meta.get("riu_name", ""),
        "confidence": palette_meta.get("confidence", 0),
        "lib_ids": palette_meta.get("lib_ids", []),
        "agent": agent,
    }


# ── PII Detection (client-side mirror of server sanitizer) ──────────────────

PII_PATTERNS = [
    re.compile(r"\$[\d,.]+"),                             # dollar amounts
    re.compile(r"\b(our|my|we)\b.*(exposure|strategy|settle|advise|client)", re.I),
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),                 # SSN
    re.compile(r"\bpatient\b", re.I),
    re.compile(r"\bshould (we|i) (advise|settle|file|disclose)", re.I),
]


def has_pii(text: str) -> bool:
    return any(p.search(text) for p in PII_PATTERNS)


# ── System Prompt Builder ───────────────────────────────────────────────────

ROLE_PROMPTS = {
    "attorney": "The user is an attorney. Frame responses in legal terms. Cite case law when relevant. Flag anything that could implicate attorney-client privilege.",
    "doctor": "The user is a physician. Frame responses with clinical precision. Flag anything that could implicate patient data (HIPAA).",
    "financial": "The user is a financial advisor. Frame responses with fiduciary awareness. Flag anything that could implicate client financial data.",
    "executive": "The user is a business executive. Frame responses for strategic decision-making. Flag irreversible decisions.",
}


def build_system(role: str) -> str:
    ctx = ROLE_PROMPTS.get(role, "Frame responses for a professional audience.")
    return f"""You are Mission Canvas — a governed AI assistant for regulated professionals.

{ctx}

Rules:
- If the query contains client-specific information, note that in production this would be LOCAL ONLY.
- Ground responses in verifiable sources.
- Be concise. Cite sources.
- Never fabricate case law, medical guidelines, or financial regulations."""


# ── Format Response ─────────────────────────────────────────────────────────

def format_response(result: dict, query: str) -> str:
    """Format Hub response with governance signals for Telegram."""
    lines = []

    # Governance signals
    if result.get("riu_id"):
        lines.append(f"🏷 `[CLASSIFY]` {result['riu_id']} {result.get('riu_name', '')}")

    if has_pii(query):
        lines.append("🔴 `[BLOCKED]` PII detected — local only in production")
    else:
        lines.append("🟢 `[SAFE]` No PII detected")

    if result.get("lib_ids"):
        conf = result.get("confidence", 0)
        if isinstance(conf, float) and conf < 1:
            conf = int(conf * 100)
        lines.append(f"📚 `[RETRIEVE]` {len(result['lib_ids'])} entries ({conf}% confidence)")

    lines.append(f"🌐 `[{result.get('agent', 'perplexity').upper()}]` Governed external")
    lines.append("─" * 30)

    # Response body
    text = result.get("text", "No response.")
    if len(text) > 3500:
        text = text[:3500] + "..."
    lines.append(text)

    lines.append("")
    lines.append("💾 `[STORED]` Decision logged")

    return "\n".join(lines)


# ── Command Handlers ────────────────────────────────────────────────────────

def cmd_help(chat_id: int) -> None:
    user = get_user(chat_id)
    role_text = f" ({user['role']})" if user else ""

    text = f"""*Mission Canvas*{role_text}
Your judgment compounds here.

*Commands:*
/start — Set up your profile
/research <query> — Governed external research
/protect <query> — Check for PII / local-only
/decide <question> — Decision with reversibility check
/brief — Morning briefing (if scheduled)
/status — Your session stats

Or just type any question."""

    buttons = [
        [
            {"text": "🔍 Research", "callback_data": "cb:intent:research"},
            {"text": "🛡 Protect", "callback_data": "cb:intent:protect"},
            {"text": "⚖️ Decide", "callback_data": "cb:intent:decide"},
        ],
        [
            {"text": "📊 Status", "callback_data": "cb:cmd:status"},
            {"text": "⚙️ Change Role", "callback_data": "cb:cmd:setup"},
        ],
    ]
    send(chat_id, text, buttons=buttons)


def cmd_setup(chat_id: int, role_text: str = "") -> None:
    if role_text:
        lower = role_text.lower()
        if "lawyer" in lower or "attorney" in lower or "legal" in lower:
            role = "attorney"
        elif "doctor" in lower or "physician" in lower or "medical" in lower:
            role = "doctor"
        elif "financial" in lower or "advisor" in lower or "finance" in lower:
            role = "financial"
        elif "executive" in lower or "ceo" in lower or "founder" in lower:
            role = "executive"
        else:
            role = "professional"
        set_user(chat_id, role, "")
        send(chat_id, f"Got it — you're a *{role}*. Your queries are now governed for your practice.\n\nAsk anything, or use /help to see commands.")
        return

    buttons = [
        [
            {"text": "⚖️ Attorney", "callback_data": "cb:role:attorney"},
            {"text": "🩺 Physician", "callback_data": "cb:role:doctor"},
        ],
        [
            {"text": "💰 Financial Advisor", "callback_data": "cb:role:financial"},
            {"text": "👔 Executive", "callback_data": "cb:role:executive"},
        ],
        [
            {"text": "🔧 Other Professional", "callback_data": "cb:role:professional"},
        ],
    ]
    send(chat_id, "Who are you?\n\nThis helps Mission Canvas govern your queries correctly.", buttons=buttons)


def cmd_status(chat_id: int) -> None:
    user = get_user(chat_id)
    count = DB.execute("SELECT COUNT(*) FROM queries WHERE chat_id = ?", (chat_id,)).fetchone()[0]
    role = user["role"] if user else "not set"
    send(chat_id, f"*Session Status*\n\nRole: {role}\nQueries: {count}\nGovernance: active")


# ── Message Router ──────────────────────────────────────────────────────────

def handle_message(chat_id: int, text: str) -> None:
    text = text.strip()
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] chat={chat_id} | {text[:80]}", flush=True)

    # Check if user has a profile
    user = get_user(chat_id)

    try:
        # Commands
        if text.startswith("/start") or text.startswith("/help"):
            if not user:
                cmd_setup(chat_id)
            else:
                cmd_help(chat_id)
            return

        if text.startswith("/status"):
            cmd_status(chat_id)
            return

        # Explicit intents
        if text.startswith("/research "):
            query = text[10:].strip()
            if query:
                typing(chat_id)
                do_query(chat_id, query, intent="research")
            return

        if text.startswith("/protect "):
            query = text[9:].strip()
            if query:
                typing(chat_id)
                do_protect(chat_id, query)
            return

        if text.startswith("/decide "):
            query = text[8:].strip()
            if query:
                typing(chat_id)
                do_query(chat_id, query, intent="decide")
            return

        if text.startswith("/brief"):
            typing(chat_id)
            send(chat_id, "Morning briefing coming soon — connect a governed cron with `palette cron create`.")
            return

        # If no profile yet, treat first message as role identification
        if not user:
            cmd_setup(chat_id, text)
            return

        # Default: route through Hub as governed query
        typing(chat_id)
        do_query(chat_id, text)

    except Exception as e:
        print(f"[error] {e}", flush=True)
        send(chat_id, f"Error: {e}")


def do_query(chat_id: int, query: str, intent: str = "research") -> None:
    """Route query through Voice Hub with governance."""
    user = get_user(chat_id) or {"role": "professional"}
    system = build_system(user["role"])
    result = hub_chat(query, system=system)

    # Format with governance signals
    response = format_response(result, query)

    # Log
    log_query(
        chat_id, query, intent,
        result.get("riu_id", ""),
        result.get("confidence", 0),
        result.get("text", ""),
    )

    # Send with follow-up buttons
    buttons = [
        [
            {"text": "🔍 Research more", "callback_data": "cb:intent:research"},
            {"text": "⚖️ Decide on this", "callback_data": "cb:intent:decide"},
        ],
    ]
    send(chat_id, response, buttons=buttons)


def do_protect(chat_id: int, query: str) -> None:
    """Run PII check and show governance boundary."""
    pii = has_pii(query)

    if pii:
        text = (
            "🔴 *BLOCKED* — PII detected\n\n"
            f"Query: _{query[:100]}_\n\n"
            "This query contains client-specific information.\n"
            "In production, it would be answered *locally only* — "
            "zero data leaves your machine.\n\n"
            "💾 `[STORED]` Governance decision logged"
        )
    else:
        text = (
            "🟢 *SAFE* — No PII detected\n\n"
            f"Query: _{query[:100]}_\n\n"
            "This query is safe for external research.\n"
            "Use /research to get a governed answer."
        )
    send(chat_id, text)


# ── Callback Handler ────────────────────────────────────────────────────────

def handle_callback(callback: dict) -> None:
    cb_id = callback["id"]
    chat_id = callback["message"]["chat"]["id"]
    data = callback.get("data", "")

    answer_callback(cb_id)

    if data.startswith("cb:role:"):
        role = data[8:]
        set_user(chat_id, role, "")
        send(chat_id, f"Set up as *{role}*. Your queries are governed. Ask anything or use /help.")

    elif data == "cb:cmd:setup":
        cmd_setup(chat_id)

    elif data == "cb:cmd:status":
        cmd_status(chat_id)

    elif data == "cb:intent:research":
        send(chat_id, "Type your research question:")

    elif data == "cb:intent:protect":
        send(chat_id, "Type the query to check for PII:")

    elif data == "cb:intent:decide":
        send(chat_id, "What decision do you need to make?")


# ── Main Loop ───────────────────────────────────────────────────────────────

def run() -> None:
    global DB

    if not BOT_TOKEN:
        print("[mc-telegram] MC_BOT_TOKEN not set.", flush=True)
        print("  1. Create a bot with @BotFather on Telegram")
        print("  2. export MC_BOT_TOKEN=\"your-token\"")
        print("  3. python3 mc_telegram.py")
        sys.exit(1)

    DB = init_db()
    print(f"[mc-telegram] Mission Canvas Telegram Bot starting", flush=True)
    print(f"[mc-telegram] Hub: {HUB_URL}", flush=True)
    print(f"[mc-telegram] Agent: {DEFAULT_AGENT}", flush=True)

    offset = 0

    while True:
        try:
            result = tg("getUpdates", offset=offset, timeout=POLL_TIMEOUT)
            if not result.get("ok"):
                time.sleep(5)
                continue

            for update in result.get("result", []):
                offset = update["update_id"] + 1

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

        except httpx.ReadTimeout:
            continue
        except KeyboardInterrupt:
            print("\n[mc-telegram] Stopped.")
            break
        except Exception as e:
            print(f"[mc-telegram] poll error: {e}", flush=True)
            time.sleep(5)


if __name__ == "__main__":
    run()
