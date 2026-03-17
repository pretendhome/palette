#!/usr/bin/env python3
"""
rossi_bridge.py — Implementation-specific Telegram Bridge (Business Plan Project)
Dedicated bot for a client's business plan project. Scoped entirely to one implementation.

Setup:
  1. Message @BotFather → /newbot → copy your token
  2. export ROSSI_BOT_TOKEN="your-token"
  3. export ANTHROPIC_API_KEY="your-key"
  4. export ROSSI_CLIENT_NAME="Client Name"  # name shown in bot responses
  5. python3 rossi_bridge.py

Commands:
  /status      — current project state and fundability score
  /gaps        — the 5 critical gaps blocking funding
  /fixes       — the 3 critical fixes (priority order)
  /decisions   — open decisions waiting on Rossi team
  /revenue     — revenue model and Creative Growth comparison
  /grants      — grant targets, timeline, amounts
  /help        — command list
"""
from __future__ import annotations

import os
import sys
import time
import json
import datetime
import re
import tempfile
import threading
import httpx
import anthropic

try:
    from relay_store import TelegramRelayStore
except Exception:
    TelegramRelayStore = None

# ── Config ─────────────────────────────────────────────────────────────────────

BOT_TOKEN     = os.environ.get("ROSSI_BOT_TOKEN", "")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
POLL_TIMEOUT  = 30
MAX_HISTORY   = 20

CLIENT_NAME   = os.environ.get("ROSSI_CLIENT_NAME", "Client")
SESSION_LOG   = os.environ.get("ROSSI_SESSION_LOG", "session.jsonl")
IMPLEMENTATION_ID = os.environ.get("ROSSI_IMPLEMENTATION_ID", "retail-rossi-store")
IMPLEMENTATIONS_ROOT = os.environ.get("PALETTE_IMPLEMENTATIONS_ROOT", "/home/mical/fde/implementations")
RELAY_ENABLED = os.environ.get("ROSSI_RELAY_ENABLED", "1").lower() not in {"0", "false", "no"}
RELAY_ALLOWLIST_RAW = os.environ.get("ROSSI_RELAY_ALLOWLIST", "").strip()
DEFAULT_ACTOR_MODE = os.environ.get("ROSSI_DEFAULT_ACTOR_MODE", "sahar").strip().lower()

TELEGRAM = f"https://api.telegram.org/bot{BOT_TOKEN}"

_relay_store = None
_active_trace_by_chat: dict[int, dict] = {}
_actor_mode_by_chat: dict[int, str] = {}


def _parse_allowlist(raw: str) -> set[str]:
    if not raw:
        return set()
    return {p.strip() for p in raw.split(",") if p.strip()}


RELAY_ALLOWLIST = _parse_allowlist(RELAY_ALLOWLIST_RAW)

# ── Rossi system prompt ─────────────────────────────────────────────────────────

ROSSI_SYSTEM = f"""You are the Rossi Mission Project AI assistant, built specifically for {CLIENT_NAME} \
and the Rossi team. You have deep knowledge of the Rossi Mission Project business plan, strategy, \
research, and open decisions.

WHO YOU ARE TALKING TO:
{CLIENT_NAME} is one of the owners of Rossi Mission Project — a graffiti art gallery and streetwear brand \
at 791 Valencia Street, San Francisco. They are a decision-maker on organizational structure, artist \
relationships, and the path to funding.

WHAT ROSSI IS:
Rossi Mission Project is an artist-first graffiti gallery and streetwear brand in the Mission District, SF. \
Core model: represent graffiti/street artists through gallery exhibitions, product lines (originals, prints, \
merch), and events. Operate on a 50/50 profit split with artists. Build a "signature style + champion + \
documentation = career launch" pipeline modeled on Barry McGee and Chito. Expand via a network/tribe model \
(not franchise) to Portland, Seattle, Oakland, and beyond.

CURRENT STATUS:
- Underwriter fundability score: 79/100 — CONDITIONAL FAIL (close, but not fundable yet)
- Business plan is 80% excellent: vision strong, model differentiated, fiscal sponsorship structure sound
- Missing 20%: validation — connecting vision to actual evidence from the existing operation
- Timeline to "strong yes": 4–6 weeks of focused work on 5 critical gaps

THE 5 CRITICAL GAPS (in priority order):
1. NO BASELINE DATA (CRITICAL) — Zero actual numbers from 791 Valencia. Plan projects $500K Year 1 retail \
but we don't know if current run rate is $150K or $400K. Fix: pull 12 months of Square/Shopify POS data. \
Takes 1–2 days. Template at remediation/condition-1-trailing-actuals.md.

2. CASH FLOW TIMING (DANGER) — Annual totals look fine (-$75K Year 1). But TIMING is deadly. \
Grants arrive 60–90 days after award. Months 1–3: burning $8–10K/month. Month 11–12: cash drops to $10K. \
One bad month = insolvency. Need $185–200K in funding (not $150K). \
Template at remediation/condition-2-monthly-cashflow.md.

3. ARTIST PIPELINE UNPROVEN (MODERATE) — The career-launch thesis (Chito, Barry McGee model) \
is derived from others. Funders ask: has Rossi done this for anyone yet, even informally? \
Need 2–3 documented artist success stories. Template at remediation/condition-3-pipeline-validation.md.

4. GOVERNANCE TOO LEAN (MODERATE) — Plan references an advisory board but doesn't show who's on it. \
Funders want 3–5 named advisors with relevant credentials. \
Template at remediation/condition-4-simplified-governance.md.

5. MISSING VISUAL CREDENTIALS (LOW) — No photos, no show documentation, no press. \
Plan reads like a startup pitch when Rossi already exists. Fix: add a 1-page visual proof section. \
Template at remediation/condition-5-bear-case-scenario.md.

THE 3 CRITICAL FIXES (from FINAL_RECOMMENDATIONS.md):

FIX 1 — FLIP THE REVENUE MODEL:
Current (risky): Retail $500K (64%), Grants $50K (6%)
Target (Creative Growth model): Retail $350K (45%), Grants $200K (26%)
Why: $350K retail = $4,375 gross per artist (conservative, achievable). \
$200K grants = apply for $250K+ at 70–80% success rate.
Grant targets: SFAC, CAC, Zellerbach Family Foundation, Walter and Elise Haas Fund, SF Foundation.

FIX 2 — GET BASELINE DATA:
Pull from Square/Shopify: monthly revenue by category, transaction count, average order value, \
top 10 artists by sales, foot traffic. 1–2 days of work. This transforms projections from theoretical to validated.

FIX 3 — DOCUMENT THE ARTIST PIPELINE:
Select 2–3 artists Rossi has already championed. Write 1-page case studies: before Rossi (unknown), \
what Rossi did (shows, documentation, promotion), after Rossi (sales, press, career progress). \
This proves the thesis with evidence.

THE COMPARABLE:
Creative Growth Art Center (Oakland) — 50-year-old nonprofit gallery. $3.26M revenue, 140 artists, \
50/50 artist split, $1.1M art sales, $1.26M grants. Form 990 validated. This is proof that Rossi's \
model works at scale.

OPEN DECISIONS (waiting on Rossi team input):
1. Organizational Structure — Nonprofit vs For-Profit vs Hybrid. Research complete. Decision: Rossi team.
2. Network Expansion Model — Partner gallery criteria, growth targets. Research complete.
3. Artist Contract Structure — 50/50 split terms, IP rights details. Research complete.
4. Geographic Expansion — Which markets first (Portland? Seattle? Oakland?). Research complete.
5. Brand Collaboration Policy — What corporate collabs are allowed, approval process.

HOW TO RESPOND:
- Be direct and practical. {CLIENT_NAME} is a business owner, not a student.
- When they ask about a gap or fix, give them the specific action, timeline, and template location.
- When they ask about a decision, explain the options and what's at stake — don't decide for them.
- If they share actual data (revenue numbers, artist stories, etc.), acknowledge it and explain how it \
changes the fundability picture.
- Keep answers concise. Use bullet points. No corporate fluff.
- You are scoped entirely to Rossi. Do not discuss other projects or Palette internals.

WHAT YOU DON'T KNOW:
- Actual current revenue (that's Gap #1 — the client needs to provide this)
- Who the advisory board candidates are
- Which specific artists to document in the pipeline case studies
- Whether they've applied to any grants yet
When these come up, ask the client directly."""


# ── Chat state ──────────────────────────────────────────────────────────────────

class ChatState:
    def __init__(self):
        self.history     = []
        self.turn        = 0
        self.last_answer = ""

    def add(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})
        if len(self.history) > MAX_HISTORY:
            self.history = self.history[-MAX_HISTORY:]


states: dict[int, ChatState] = {}

def get_state(chat_id: int) -> ChatState:
    if chat_id not in states:
        states[chat_id] = ChatState()
    return states[chat_id]


def get_actor_mode(chat_id: int) -> str:
    mode = _actor_mode_by_chat.get(chat_id, DEFAULT_ACTOR_MODE)
    if mode not in {"sahar", "eiad", "auto"}:
        return "sahar"
    return mode


def set_actor_mode(chat_id: int, mode: str) -> str:
    mode = mode.strip().lower()
    if mode not in {"sahar", "eiad", "auto"}:
        mode = "sahar"
    _actor_mode_by_chat[chat_id] = mode
    return mode


# ── Session logging ─────────────────────────────────────────────────────────────

def log_exchange(chat_id: int, question: str, answer: str) -> None:
    entry = {
        "ts":       datetime.datetime.now().isoformat(),
        "chat_id":  chat_id,
        "question": question[:600],
        "answer":   answer[:1200],
    }
    try:
        with open(SESSION_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"[log] error: {e}", flush=True)


# ── Relay artifacts (v1 pilot) ────────────────────────────────────────────────

def relay_store():
    global _relay_store
    if not RELAY_ENABLED or TelegramRelayStore is None:
        return None
    if _relay_store is None:
        _relay_store = TelegramRelayStore(IMPLEMENTATIONS_ROOT, IMPLEMENTATION_ID)
        _relay_store.ensure_layout()
    return _relay_store


def _active_trace(chat_id: int) -> dict | None:
    return _active_trace_by_chat.get(chat_id)


def relay_begin_trace(chat_id: int, text: str, *, msg_id: int | None = None, sender_id: int | None = None, sender_label: str | None = None) -> dict | None:
    store = relay_store()
    if not store:
        return None
    trace_id = store.new_trace_id("telegram")
    event = store.append_event(
        {
            "trace_id": trace_id,
            "source": "telegram",
            "direction": "inbound",
            "channel": "telegram",
            "session_id": str(chat_id),
            "sender_id": f"telegram:{sender_id}" if sender_id is not None else "",
            "sender_label": sender_label or "",
            "message_id": f"tg:{msg_id}" if msg_id is not None else "",
            "message_text": text,
            "status": "received",
            "provenance": "telegram-bridge",
        }
    )
    ctx = {
        "trace_id": trace_id,
        "inbound_event_id": event["event_id"],
        "chat_id": chat_id,
        "msg_id": msg_id,
    }
    _active_trace_by_chat[chat_id] = ctx
    return ctx


def relay_end_trace(chat_id: int) -> None:
    _active_trace_by_chat.pop(chat_id, None)


def relay_log_outbound(chat_id: int, text: str) -> None:
    store = relay_store()
    ctx = _active_trace(chat_id)
    if not store or not ctx:
        return
    store.append_event(
        {
            "trace_id": ctx["trace_id"],
            "source": "telegram",
            "direction": "outbound",
            "channel": "telegram",
            "session_id": str(chat_id),
            "reply_to": f"tg:{ctx['msg_id']}" if ctx.get("msg_id") is not None else "",
            "message_text": text,
            "status": "sent",
            "provenance": "telegram-bridge",
        }
    )


def relay_create_request(chat_id: int, raw_text: str, *, sender_id: int | None = None, sender_label: str | None = None) -> tuple[str, str] | None:
    """
    Create an inbox relay artifact from a Telegram command.
    Syntax:
      /relay orch_summary_request Ask Orch for a one-paragraph Rossi funding summary
    """
    store = relay_store()
    ctx = _active_trace(chat_id)
    if not store or not ctx:
        return None
    m = re.match(r"^/relay\s+([a-zA-Z0-9_:-]+)\s+(.+)$", raw_text.strip(), re.DOTALL)
    if not m:
        return ("error", "Usage: `/relay <intent> <request text>`")
    intent, user_request = m.group(1).strip(), m.group(2).strip()
    allowlist = {
        "daily_update",
        "orch_summary_request",
        "status_request",
        "update_request",
        "triage_request",
    }
    if intent not in allowlist:
        return ("error", f"Intent `{intent}` not allowed. Allowed: {', '.join(sorted(allowlist))}")
    idempotency_key = f"tg:{ctx.get('msg_id')}|{intent}"
    if store.has_seen_idempotency(idempotency_key):
        return ("duplicate", "Duplicate request detected (same Telegram message + intent). Ignored.")
    publish_requested = False
    publish_target_path = ""
    publish_commit_message = ""
    if intent == "update_request" and user_request.lower().startswith("publish:"):
        # Optional explicit publish request syntax (still not executed in v1):
        # /relay update_request publish:<repo/path.md> | <request text>
        pm = re.match(r"^publish:([^\|]+)\|\s*(.+)$", user_request, re.DOTALL | re.IGNORECASE)
        if pm:
            publish_requested = True
            publish_target_path = pm.group(1).strip()
            user_request = pm.group(2).strip()
            publish_commit_message = f"relay: update {publish_target_path}"

    path = store.write_request(
        trace_id=ctx["trace_id"],
        intent=intent,
        user_request=user_request,
        requested_by=f"telegram:{chat_id}",
        target_agent="orch",
        source_event_ids=[ctx["inbound_event_id"]],
        related_session=str(chat_id),
        idempotency_key=idempotency_key,
        publish_to_github_requested=publish_requested,
        publish_target_path=publish_target_path,
        publish_commit_message=publish_commit_message,
        # Better attribution than a hardcoded label once Rossi team members join.
        requested_by_label=(sender_label or "telegram-user"),
    )
    store.mark_idempotency_seen(idempotency_key, ctx["trace_id"], ctx["inbound_event_id"])
    store.append_event(
        {
            "trace_id": ctx["trace_id"],
            "source": "relay",
            "direction": "internal",
            "channel": "telegram",
            "session_id": str(chat_id),
            "artifact_path": str(path),
            "intent": intent,
            "status": "request_created",
            "provenance": "relay-store",
        }
    )
    return ("ok", str(path))


# ── Telegram API helpers ────────────────────────────────────────────────────────

def tg(method: str, **kwargs) -> dict:
    with httpx.Client(timeout=35.0) as client:
        resp = client.post(f"{TELEGRAM}/{method}", json=kwargs)
        return resp.json()


def send(chat_id: int, text: str) -> None:
    relay_log_outbound(chat_id, text)
    chunk_size = 4000
    for i in range(0, len(text), chunk_size):
        tg("sendMessage",
           chat_id    = chat_id,
           text       = text[i : i + chunk_size],
           parse_mode = "Markdown")
        if i + chunk_size < len(text):
            time.sleep(0.3)


def typing(chat_id: int) -> None:
    tg("sendChatAction", chat_id=chat_id, action="typing")


# ── Voice transcription ─────────────────────────────────────────────────────────

_whisper_model = None

def _get_whisper():
    global _whisper_model
    if _whisper_model is None:
        import whisper
        print("[rossi-bot] loading whisper model (base)...", flush=True)
        _whisper_model = whisper.load_model("base")
        print("[rossi-bot] whisper ready.", flush=True)
    return _whisper_model


def transcribe_voice(file_id: str) -> str:
    info = tg("getFile", file_id=file_id)
    if not info.get("ok"):
        raise RuntimeError(f"getFile failed: {info}")
    file_path = info["result"]["file_path"]
    url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
    with httpx.Client(timeout=30.0) as client:
        resp = client.get(url)
        resp.raise_for_status()
    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        tmp.write(resp.content)
        tmp_path = tmp.name
    try:
        model  = _get_whisper()
        result = model.transcribe(tmp_path)
        return result["text"].strip()
    finally:
        os.unlink(tmp_path)


# ── Claude ──────────────────────────────────────────────────────────────────────

def _actor_instructions(actor_mode: str) -> str:
    if actor_mode == "sahar":
        return (
            "ACTIVE RESPONSE LENS: SAHAR (owner / creative + decision-maker)\n"
            "- Recommendation first, options second.\n"
            "- Emphasize the single best next step, what decision is needed, and what input is missing.\n"
            "- Keep responses concise and momentum-oriented.\n"
            "- If the question is about the drop, prefer single-image-first branding coherence guidance unless user provides a different decision state.\n"
        )
    if actor_mode == "eiad":
        return (
            "ACTIVE RESPONSE LENS: EIAD (operator / execution + feasibility)\n"
            "- Emphasize sequencing, dependencies, blockers, and fastest safe path.\n"
            "- Provide checklist-style answers with owners/inputs when possible.\n"
            "- Distinguish what can move now vs what requires owner approval.\n"
        )
    return (
        "ACTIVE RESPONSE LENS: AUTO\n"
        "- Infer whether the user needs an owner-style decision answer or operator-style execution answer.\n"
        "- Explicitly label 'Decision needed' vs 'Execution next step' when both appear.\n"
    )


def reply(state: ChatState, user_message: str, *, actor_mode: str = "sahar") -> str:
    state.add("user", user_message)
    client = anthropic.Anthropic()
    message = client.messages.create(
        model      = "claude-sonnet-4-6",
        max_tokens = 1024,
        system     = ROSSI_SYSTEM + "\n\n" + _actor_instructions(actor_mode),
        messages   = state.history,
    )
    response = message.content[0].text
    state.add("assistant", response)
    return response


# ── Command handlers ────────────────────────────────────────────────────────────

def cmd_start(chat_id: int) -> None:
    send(chat_id,
        "👋 *Rossi Mission Project AI*\n\n"
        f"Hi {CLIENT_NAME} — I'm your dedicated assistant for the Rossi business plan. "
        "I know everything in the research, strategy, and open decisions.\n\n"
        "*Quick commands:*\n"
        "`/status` — current fundability score and what's blocking it\n"
        "`/gaps` — the 5 critical gaps (in priority order)\n"
        "`/fixes` — the 3 critical fixes and what to do first\n"
        "`/decisions` — open decisions waiting on you\n"
        "`/revenue` — revenue model and the Creative Growth comparison\n"
        "`/grants` — grant targets, amounts, and timeline\n"
        "`/help` — this menu\n\n"
        "Or just ask me anything about the project.\n"
        "You can also send a *voice message* — I'll transcribe it."
    )


def cmd_help(chat_id: int) -> None:
    actor_mode = get_actor_mode(chat_id)
    send(chat_id,
        "*Rossi Mission Project — Commands*\n\n"
        "`/status` — fundability score and current state\n"
        "`/gaps` — 5 critical gaps blocking funding\n"
        "`/fixes` — 3 critical fixes in priority order\n"
        "`/decisions` — open decisions for Rossi team\n"
        "`/revenue` — revenue model and Creative Growth comparable\n"
        "`/grants` — grant targets, timeline, and amounts\n"
        "`/as_sahar` — owner/decision framing\n"
        "`/as_eiad` — operator/execution framing\n"
        "`/as_auto` — auto lens selection (experimental)\n"
        "`/relay <intent> <text>` — create a Palette relay request artifact (safe, no exec)\n"
        "`/relay daily_update <text>` — intuitive alias for status-style daily priorities\n"
        "`/help` — this menu\n\n"
        f"*Actor mode:* `{actor_mode}`"
    )


def cmd_set_actor_mode(chat_id: int, mode: str) -> None:
    mode = set_actor_mode(chat_id, mode)
    labels = {
        "sahar": f"{CLIENT_NAME} (owner / decision-focused)",
        "eiad": "Eiad (operator / execution-focused)",
        "auto": "Auto (bot chooses framing)",
    }
    send(chat_id, f"✅ Actor mode set to *{labels[mode]}*")


def cmd_status(chat_id: int, state: ChatState) -> None:
    typing(chat_id)
    prompt = ("Give me a concise status update on the Rossi Mission Project: "
              "current fundability score, what's blocking it, and the path to 'strong yes'. "
              "Use bullet points. Keep it under 200 words.")
    response = reply(state, prompt, actor_mode=get_actor_mode(chat_id))
    send(chat_id, response)


def cmd_gaps(chat_id: int, state: ChatState) -> None:
    typing(chat_id)
    prompt = ("List the 5 critical gaps blocking Rossi's funding, in priority order. "
              "For each: the problem in one sentence, the fix, and the time to complete it.")
    response = reply(state, prompt, actor_mode=get_actor_mode(chat_id))
    send(chat_id, response)


def cmd_fixes(chat_id: int, state: ChatState) -> None:
    typing(chat_id)
    prompt = ("Give me the 3 critical fixes for Rossi's business plan in priority order. "
              "For each fix: what the problem is, what to do, and the specific target numbers. "
              f"Be direct — what should {CLIENT_NAME} do first thing tomorrow?")
    response = reply(state, prompt, actor_mode=get_actor_mode(chat_id))
    send(chat_id, response)


def cmd_decisions(chat_id: int, state: ChatState) -> None:
    typing(chat_id)
    prompt = ("List all open decisions that are waiting on the Rossi team. "
              "For each: what the decision is, why it matters, and what options exist. "
              "Don't make the decision — lay out what they need to decide.")
    response = reply(state, prompt, actor_mode=get_actor_mode(chat_id))
    send(chat_id, response)


def cmd_revenue(chat_id: int, state: ChatState) -> None:
    typing(chat_id)
    prompt = ("Explain Rossi's current revenue model and the proposed revised model. "
              "Compare to Creative Growth Art Center (the validated comparable). "
              "Show the numbers: current vs target vs Creative Growth. "
              "Why does this change matter for fundability?")
    response = reply(state, prompt, actor_mode=get_actor_mode(chat_id))
    send(chat_id, response)


def cmd_grants(chat_id: int, state: ChatState) -> None:
    typing(chat_id)
    prompt = ("List the grant targets for Rossi: which funders, amounts to apply for, "
              "likely success rates, and timeline. What's the total target and how does it "
              f"change the revenue model? What should {CLIENT_NAME} do to start the grant process?")
    response = reply(state, prompt, actor_mode=get_actor_mode(chat_id))
    send(chat_id, response)


def _relay_allowed(sender_id: int | None) -> bool:
    if not RELAY_ALLOWLIST:
        return True
    if sender_id is None:
        return False
    return str(sender_id) in RELAY_ALLOWLIST or f"telegram:{sender_id}" in RELAY_ALLOWLIST


def cmd_relay(chat_id: int, text: str, *, sender_id: int | None = None, sender_label: str | None = None) -> None:
    if not _relay_allowed(sender_id):
        send(chat_id, "⛔ `/relay` is restricted. Ask the Rossi admin to allow your Telegram user ID.")
        return
    result = relay_create_request(chat_id, text, sender_id=sender_id, sender_label=sender_label)
    if result is None:
        send(chat_id, "Relay store unavailable. Check `ROSSI_RELAY_ENABLED` and local relay module.")
        return
    kind, detail = result
    if kind == "ok":
        send(
            chat_id,
            "🧾 *Relay request created* (no live Orch call yet)\n\n"
            f"`{detail}`\n\n"
            "Next: a Palette consumer can process this inbox artifact and write an outbox response.\n"
            "GitHub publish (if requested) is metadata only and still requires explicit approval + a separate publisher.",
        )
        return
    if kind == "duplicate":
        send(chat_id, f"⚠️ {detail}")
        return
    send(chat_id, f"⚠️ {detail}")


# ── Message router ──────────────────────────────────────────────────────────────

def handle_message(chat_id: int, text: str, *, msg_id: int | None = None, sender_id: int | None = None, sender_label: str | None = None) -> None:
    state = get_state(chat_id)
    text  = text.strip()

    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] chat={chat_id} | {text[:80]}", flush=True)
    relay_begin_trace(chat_id, text, msg_id=msg_id, sender_id=sender_id, sender_label=sender_label)

    try:
        if text.startswith("/start"):
            cmd_start(chat_id)
            return
        if text.startswith("/help"):
            cmd_help(chat_id)
            return
        if text.startswith("/as_sahar"):
            cmd_set_actor_mode(chat_id, "sahar")
            return
        if text.startswith("/as_eiad"):
            cmd_set_actor_mode(chat_id, "eiad")
            return
        if text.startswith("/as_auto"):
            cmd_set_actor_mode(chat_id, "auto")
            return
        if text.startswith("/status"):
            cmd_status(chat_id, state)
            return
        if text.startswith("/gaps"):
            cmd_gaps(chat_id, state)
            return
        if text.startswith("/fixes"):
            cmd_fixes(chat_id, state)
            return
        if text.startswith("/decisions"):
            cmd_decisions(chat_id, state)
            return
        if text.startswith("/revenue"):
            cmd_revenue(chat_id, state)
            return
        if text.startswith("/grants"):
            cmd_grants(chat_id, state)
            return
        if text.startswith("/relay"):
            cmd_relay(chat_id, text, sender_id=sender_id, sender_label=sender_label)
            return

        # Regular message
        typing(chat_id)
        response = reply(state, text, actor_mode=get_actor_mode(chat_id))
        send(chat_id, response)

        # Log the exchange
        h = state.history
        question = h[-3]["content"] if len(h) >= 3 and h[-3]["role"] == "assistant" else text
        log_exchange(chat_id, question, text)
    finally:
        relay_end_trace(chat_id)


# ── Polling loop ────────────────────────────────────────────────────────────────

def run() -> None:
    print("[rossi-bot] starting long-poll loop", flush=True)
    offset = 0
    while True:
        try:
            result = tg("getUpdates", offset=offset, timeout=POLL_TIMEOUT)
            if not result.get("ok"):
                print(f"[warn] getUpdates error: {result}", flush=True)
                time.sleep(5)
                continue

            for update in result.get("result", []):
                offset  = update["update_id"] + 1
                msg     = update.get("message") or update.get("edited_message")
                if not msg:
                    continue
                chat_id = msg["chat"]["id"]
                text    = msg.get("text") or msg.get("caption", "")
                voice   = msg.get("voice")

                if voice and not text:
                    try:
                        typing(chat_id)
                        ts = datetime.datetime.now().strftime("%H:%M:%S")
                        print(f"[{ts}] chat={chat_id} voice={voice['file_id'][:12]}...", flush=True)
                        text = transcribe_voice(voice["file_id"])
                        print(f"[{ts}] transcribed: {text[:80]}", flush=True)
                    except Exception as e:
                        print(f"[error] transcribe: {e}", flush=True)
                        send(chat_id, f"⚠️ Couldn't transcribe voice message: {e}")
                        continue

                if text:
                    try:
                        handle_message(
                            chat_id,
                            text,
                            msg_id=msg.get("message_id"),
                            sender_id=(msg.get("from") or {}).get("id"),
                            sender_label=(msg.get("from") or {}).get("first_name") or (msg.get("from") or {}).get("username"),
                        )
                    except Exception as e:
                        print(f"[error] handle_message: {e}", flush=True)
                        send(chat_id, f"⚠️ Error: {e}")

        except httpx.RequestError as e:
            print(f"[error] network: {e}", flush=True)
            time.sleep(10)
        except KeyboardInterrupt:
            print("\n[rossi-bot] stopped.", flush=True)
            sys.exit(0)
        except Exception as e:
            print(f"[error] unexpected: {e}", flush=True)
            time.sleep(5)


# ── Entry point ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("ERROR: ROSSI_BOT_TOKEN not set")
        print("  1. Message @BotFather on Telegram")
        print("  2. /newbot — give it a name like 'Rossi Mission AI'")
        print("  3. Copy the token, then:")
        print("  export ROSSI_BOT_TOKEN='your-token-here'")
        sys.exit(1)
    if not ANTHROPIC_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set")
        sys.exit(1)
    run()
