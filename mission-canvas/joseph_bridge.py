#!/usr/bin/env python3
"""
joseph_bridge.py — Mission Canvas Telegram Bridge
Connects a Telegram bot to a Mission Canvas workspace via HTTP endpoints.
Optionally uses Perplexity API for live research questions.

Setup:
  1. Start Mission Canvas server: node server.mjs
  2. export JOSEPH_BOT_TOKEN="your-telegram-bot-token"
  3. export MC_WORKSPACE="oil-investor"  (or any workspace ID)
  4. export MC_SERVER="http://localhost:8787"  (or VPS URL)
  5. export PERPLEXITY_API_KEY="pplx-xxx"  (optional — enables /research and smart answers)
  6. python3 joseph_bridge.py

Commands:
  /start      — welcome + command list
  /brief      — daily brief (health, blockers, nudges)
  /gaps       — missing evidence list
  /decisions  — open decisions (blocked vs ready)
  /health     — health score breakdown
  /research   — research a question with Perplexity
  /alerts     — show recent monitor alerts
  /monitors   — show active monitors
  /help       — command list
  /newworkspace <name> | <objective> — create a new workspace

Any other message is routed: research questions go to Perplexity,
workspace questions go through the convergence chain.
Voice messages are transcribed and handled the same way.
"""
from __future__ import annotations

import os
import re
import sys
import time
import json
import datetime
import tempfile
from pathlib import Path

import httpx
import yaml

# ── Config ─────────────────────────────────────────────────────────────────────

BOT_TOKEN       = os.environ.get("JOSEPH_BOT_TOKEN", "")
MC_SERVER       = os.environ.get("MC_SERVER", "http://localhost:8787")
MC_WORKSPACE    = os.environ.get("MC_WORKSPACE", "oil-investor")
PERPLEXITY_KEY  = os.environ.get("PERPLEXITY_API_KEY", "")
WORKSPACES_DIR  = os.environ.get("MC_WORKSPACES_DIR",
                                 os.path.join(os.path.dirname(__file__) or ".", "workspaces"))
POLL_TIMEOUT    = 30
MAX_HISTORY     = 20
SESSION_LOG     = os.environ.get("MC_SESSION_LOG", "joseph_session.jsonl")
CHAT_ID_FILE    = os.environ.get("MC_CHAT_ID_FILE",
                                 os.path.join(os.path.dirname(__file__) or ".", "joseph_chat_ids.json"))

TELEGRAM = f"https://api.telegram.org/bot{BOT_TOKEN}"
PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"

# ── Telegram helpers ───────────────────────────────────────────────────────────

def tg(method: str, **kwargs) -> dict:
    with httpx.Client(timeout=35.0) as client:
        resp = client.post(f"{TELEGRAM}/{method}", json=kwargs)
        return resp.json()


def send(chat_id: int, text: str) -> None:
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


# ── Voice transcription (optional — requires whisper) ──────────────────────────

_whisper_model = None

def _get_whisper():
    global _whisper_model
    if _whisper_model is None:
        import whisper
        print("[mc-bot] loading whisper model (base)...", flush=True)
        _whisper_model = whisper.load_model("base")
        print("[mc-bot] whisper ready.", flush=True)
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


# ── Perplexity research ──────────────────────────────────────────────────────

def perplexity_research(query: str, context: str = "") -> str:
    """Call Perplexity Sonar API for live research. Returns formatted answer."""
    if not PERPLEXITY_KEY:
        return ""

    system = (
        "You are a concise investment research analyst. "
        "Give specific data: numbers, dates, percentages. "
        "Skip disclaimers. Be direct."
    )
    if context:
        system += f"\n\nContext: {context}"

    try:
        with httpx.Client(timeout=45.0) as client:
            resp = client.post(
                PERPLEXITY_URL,
                headers={
                    "Authorization": f"Bearer {PERPLEXITY_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "sonar",
                    "messages": [
                        {"role": "system", "content": system},
                        {"role": "user", "content": query},
                    ],
                    "return_citations": True,
                },
            )
            resp.raise_for_status()
            data = resp.json()

        content = data["choices"][0]["message"]["content"]
        citations = data.get("citations", [])

        result = content
        if citations:
            result += "\n\n_Sources:_"
            for i, c in enumerate(citations[:3], 1):
                url = c if isinstance(c, str) else c.get("url", "")
                if url:
                    result += f"\n{i}. {url}"
        return result
    except Exception as e:
        print(f"[perplexity] error: {e}", flush=True)
        return ""


# ── Research routing ─────────────────────────────────────────────────────────

# Patterns that indicate a research question (not workspace state)
_RESEARCH_PATTERNS = [
    r'(is|are)\s+\w+.*\b(good|bad|worth|viable|promising)\b.*\b(investment|buy|stock|company)',
    r'\b(invest|investing|investment)\b.*\b(in|into)\b',
    r'\b(valuation|funding|ipo|series [a-e]|revenue|market cap)\b',
    r'\b(compare|versus|vs\.?)\b.*\b(company|stock|fund|etf)\b',
    r'\b(what is|tell me about|who is|explain)\b.*\b(company|startup|fund|firm|ceo|founder)\b',
    r'\b(news|latest|update|happening)\b.*\b(market|oil|energy|ai|tech|crypto)\b',
    r'\b(price|trading|shares|stock|equity)\b.*\b(today|now|current|latest)\b',
    r'\b(opec|hormuz|sanctions|tariff|regulation)\b',
    r'\b(anthropic|openai|lovable|perplexity|cursor|runway|braintrust)\b',
]

# Patterns that indicate a workspace question (convergence chain)
_WORKSPACE_PATTERNS = [
    r'(should i|do i|trim|sell|buy|add|hold|exit)',
    r'(what.*focus|what.*first|what.*priority|where.*start)',
    r'(how.*doing|status|update|overview)',
    r'(block|stuck|missing|gap|need)',
    r'(risk|hedge|protect|downside)',
    r'(decision|approve|reject|verify|resolve)',
    r'(brief|health|score|nudge)',
]

def is_research_question(text: str) -> bool:
    """Check if this looks like a research/investment question vs workspace query."""
    q = text.lower().strip()
    for pattern in _RESEARCH_PATTERNS:
        if re.search(pattern, q):
            return True
    return False

def is_workspace_question(text: str) -> bool:
    """Check if this matches workspace state patterns."""
    q = text.lower().strip()
    for pattern in _WORKSPACE_PATTERNS:
        if re.search(pattern, q):
            return True
    return False


# ── Alert & Monitor helpers ──────────────────────────────────────────────────

def load_alerts(workspace_id: str, limit: int = 5) -> list[dict]:
    """Load recent alerts from workspace alerts directory."""
    alerts_dir = Path(WORKSPACES_DIR) / workspace_id / "alerts"
    if not alerts_dir.exists():
        return []
    files = sorted(alerts_dir.glob("*.yaml"), reverse=True)[:limit]
    alerts = []
    for f in files:
        try:
            with open(f) as fh:
                data = yaml.safe_load(fh) or {}
            if "alert" in data:
                alerts.append(data["alert"])
        except Exception:
            pass
    return alerts


def load_monitors(workspace_id: str) -> list[dict]:
    """Load monitor definitions from workspace."""
    monitors_dir = Path(WORKSPACES_DIR) / workspace_id / "monitors"
    if not monitors_dir.exists():
        return []
    monitors = []
    for f in sorted(monitors_dir.glob("*.yaml")):
        try:
            with open(f) as fh:
                data = yaml.safe_load(fh) or {}
            if "monitor" in data:
                monitors.append(data["monitor"])
        except Exception:
            pass
    return monitors


def save_chat_id(chat_id: int) -> None:
    """Persist chat IDs so the monitor daemon can send alerts."""
    try:
        existing = {}
        if os.path.exists(CHAT_ID_FILE):
            with open(CHAT_ID_FILE) as f:
                existing = json.load(f)
        existing[str(chat_id)] = {
            "last_seen": datetime.datetime.now().isoformat(),
            "workspace": _chat_workspace.get(chat_id, MC_WORKSPACE),
        }
        with open(CHAT_ID_FILE, "w") as f:
            json.dump(existing, f, indent=2)
    except Exception as e:
        print(f"[chat-id] save error: {e}", flush=True)


# ── Mission Canvas API calls ──────────────────────────────────────────────────

def mc_post(endpoint: str, payload: dict) -> dict:
    """POST to a Mission Canvas endpoint."""
    url = f"{MC_SERVER}/v1/missioncanvas/{endpoint}"
    with httpx.Client(timeout=30.0) as client:
        resp = client.post(url, json=payload)
        return resp.json()


def mc_get(endpoint: str) -> dict:
    """GET from a Mission Canvas endpoint."""
    url = f"{MC_SERVER}/v1/missioncanvas/{endpoint}"
    with httpx.Client(timeout=30.0) as client:
        resp = client.get(url)
        return resp.json()


def mc_brief(workspace_id: str) -> str:
    """Get the daily brief via the workspace-welcome endpoint."""
    result = mc_post("workspace-welcome", {"workspace_id": workspace_id})
    if result.get("status") != "ok":
        return result.get("error", "Could not load brief.")
    # Format the structured response into readable text
    lines = [
        f"*{result.get('workspace_name', workspace_id)}*",
        f"Health: *{result.get('health_score', '?')}/100* ({result.get('health_label', '?')})",
        f"Target: {result.get('target_score', 85)}/100",
        "",
        f"_{result.get('objective', '')}_",
    ]
    nudges = result.get("nudges", [])
    if nudges:
        lines.append("")
        lines.append(f"*{len(nudges)} items need attention:*")
        for n in nudges:
            yours = " (on you)" if n.get("is_yours") else f" ({n.get('who_resolves', '?')})"
            lines.append(f"\u2022 *{n['summary']}* \u2014 {n.get('age_string', '?')}{yours}")
    return "\n".join(lines)


def mc_ask(question: str, workspace_id: str) -> str:
    """Route a question through the convergence chain."""
    # Rewrite common questions to chain-friendly patterns that detectProjectQuery matches
    q = question.lower().strip()
    rewrites = [
        (r'(should i|do i|trim|sell|buy|add|hold|exit)', 'what decisions are open?'),
        (r'(what.*focus|what.*first|what.*priority|where.*start)', 'what should I do next?'),
        (r'(how.*doing|status|update|overview)', 'how are we doing?'),
        (r'(block|stuck|missing|gap|need)', 'what is blocking us?'),
        (r'(risk|hedge|protect|downside)', 'what are the risks?'),
    ]

    chain_question = question
    for pattern, rewrite in rewrites:
        if re.search(pattern, q):
            chain_question = rewrite
            break

    result = mc_post("route", {
        "input": {"objective": chain_question},
        "workspace_id": workspace_id
    })

    chain = result.get("convergence_chain", {})
    narration = chain.get("narration", "")
    brief = result.get("action_brief_markdown", "")
    error = result.get("error", {})

    if isinstance(error, dict) and error.get("message"):
        return f"Error: {error['message']}"

    response = narration or brief or ""

    if response and chain_question != question:
        response = f"_Re: {question}_\n\n{response}"

    return response or json.dumps(result, indent=2)[:2000]


def smart_answer(question: str, workspace_id: str) -> str:
    """Smart routing: research questions → Perplexity, workspace questions → chain, hybrid → both."""
    is_research = is_research_question(question)
    is_workspace = is_workspace_question(question)

    # Pure research question — go to Perplexity
    if is_research and not is_workspace and PERPLEXITY_KEY:
        # Load workspace context for better answers
        try:
            ws_config = load_yaml_file(Path(WORKSPACES_DIR) / workspace_id / "config.yaml")
            context = ws_config.get("workspace", {}).get("description", "")
        except Exception:
            context = ""
        answer = perplexity_research(question, context)
        if answer:
            # Log the research to workspace session
            log_exchange(0, f"[research] {question}", answer[:600])
            return answer

    # Workspace question or Perplexity unavailable — use chain
    if is_workspace or not PERPLEXITY_KEY:
        return mc_ask(question, workspace_id)

    # Ambiguous — try chain first, enhance with Perplexity if thin
    chain_answer = mc_ask(question, workspace_id)
    if chain_answer and len(chain_answer) > 100:
        return chain_answer

    # Chain gave a thin answer — try Perplexity
    if PERPLEXITY_KEY:
        research = perplexity_research(question)
        if research:
            if chain_answer:
                return f"{chain_answer}\n\n---\n*Research:*\n{research}"
            return research

    return chain_answer or "I couldn't find a good answer. Try rephrasing or use /research for a web search."


def load_yaml_file(path: Path) -> dict:
    """Load a YAML file safely."""
    with open(path) as f:
        return yaml.safe_load(f) or {}


def mc_gaps(workspace_id: str) -> str:
    """Get the evidence gaps by asking about blockers."""
    return mc_ask("what is blocking us?", workspace_id)


def mc_decisions(workspace_id: str) -> str:
    """Get open decisions."""
    return mc_ask("what decisions are pending?", workspace_id)


def mc_health(workspace_id: str) -> str:
    """Get workspace health via the chain."""
    return mc_ask("how are we doing?", workspace_id)


def mc_resolve(evidence_id: str, resolution: str, workspace_id: str) -> str:
    """Resolve a missing evidence gap."""
    result = mc_post("resolve-evidence", {
        "workspace_id": workspace_id,
        "evidence_id": evidence_id,
        "resolution": resolution
    })
    if result.get("status") == "resolved":
        score = result.get("health_score", "?")
        remaining = result.get("remaining_gaps", "?")
        return f"Resolved *{evidence_id}*. Health: {score}/100. {remaining} gaps remaining."
    return result.get("error", "Failed to resolve evidence.")


def mc_add_fact(fact: str, source: str, workspace_id: str) -> str:
    """Add a known fact to the workspace."""
    result = mc_post("add-fact", {
        "workspace_id": workspace_id,
        "fact": fact,
        "source": source
    })
    if result.get("status") == "added":
        score = result.get("health_score", "?")
        total = result.get("total_facts", "?")
        return f"Got it. ({total} facts, health: {score}/100)\n_{fact}_"
    return result.get("error", "Failed to add fact.")


def mc_create_workspace(workspace_id: str, name: str, objective: str, user_name: str = "User") -> str:
    """Create a new workspace."""
    result = mc_post("create-workspace", {
        "workspace_id": workspace_id,
        "name": name,
        "user_name": user_name,
        "objective": objective,
        "risk_posture": "medium",
        "greeting_style": "executive"
    })
    if result.get("status") == "created":
        return f"Workspace *{name}* created. ID: `{workspace_id}`\nWeb UI: {MC_SERVER}/{workspace_id}"
    return result.get("error", "Failed to create workspace.")


# ── Session logging ────────────────────────────────────────────────────────────

def log_exchange(chat_id: int, question: str, answer: str) -> None:
    entry = {
        "ts":       datetime.datetime.now().isoformat(),
        "chat_id":  chat_id,
        "workspace": MC_WORKSPACE,
        "question": question[:600],
        "answer":   answer[:1200],
    }
    try:
        with open(SESSION_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"[log] error: {e}", flush=True)


# ── Per-chat workspace tracking ──────────────────────────────────────────────

_chat_workspace: dict[int, str] = {}

def get_workspace(chat_id: int) -> str:
    return _chat_workspace.get(chat_id, MC_WORKSPACE)

def set_workspace(chat_id: int, ws_id: str) -> None:
    _chat_workspace[chat_id] = ws_id


# ── Command handlers ──────────────────────────────────────────────────────────

def cmd_start(chat_id: int) -> None:
    ws = get_workspace(chat_id)
    has_pplx = " + Perplexity research" if PERPLEXITY_KEY else ""
    send(chat_id,
        f"*Mission Canvas*{has_pplx}\n\n"
        f"Connected to workspace: `{ws}`\n\n"
        "*Commands:*\n"
        "`/brief` \u2014 daily brief (health, blockers, nudges)\n"
        "`/gaps` \u2014 what's missing / what's blocking us\n"
        "`/decisions` \u2014 open decisions\n"
        "`/health` \u2014 health score breakdown\n"
        "`/research <query>` \u2014 research with Perplexity\n"
        "`/alerts` \u2014 recent monitor alerts\n"
        "`/monitors` \u2014 active monitors\n"
        "`/resolve <ID> <answer>` \u2014 resolve an evidence gap\n"
        "`/fact <fact> | <source>` \u2014 add a known fact\n"
        "`/workspace <id>` \u2014 switch workspace\n"
        "`/help` \u2014 this menu\n\n"
        "Or just ask me anything \u2014 I'll figure out if it's a workspace "
        "question or research question. Voice messages work too."
    )


def cmd_help(chat_id: int) -> None:
    ws = get_workspace(chat_id)
    has_pplx = " + Perplexity" if PERPLEXITY_KEY else ""
    send(chat_id,
        f"*Mission Canvas*{has_pplx} \u2014 workspace: `{ws}`\n\n"
        "*Workspace:*\n"
        "`/brief` \u2014 daily brief\n"
        "`/gaps` \u2014 evidence gaps & blockers\n"
        "`/decisions` \u2014 open decisions\n"
        "`/health` \u2014 health score\n"
        "`/resolve ME-001 The answer is...` \u2014 resolve a gap\n"
        "`/fact Revenue is $400K/yr | Square POS data` \u2014 add a fact\n\n"
        "*Research & Alerts:*\n"
        "`/research Is Anthropic a good AI investment?` \u2014 Perplexity search\n"
        "`/alerts` \u2014 recent monitor alerts\n"
        "`/monitors` \u2014 active monitors and status\n\n"
        "*Navigation:*\n"
        "`/workspace oil-investor` \u2014 switch workspace\n"
        "`/workspaces` \u2014 list all workspaces\n"
        "`/help` \u2014 this menu\n\n"
        "Any other message is smart-routed: research questions go to "
        "Perplexity, workspace questions go through the convergence chain."
    )


# ── Message handler ────────────────────────────────────────────────────────────

def handle_message(chat_id: int, text: str) -> None:
    text = text.strip()
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    ws = get_workspace(chat_id)
    print(f"[{ts}] chat={chat_id} ws={ws} | {text[:80]}", flush=True)

    try:
        if text.startswith("/start"):
            cmd_start(chat_id)
            return

        if text.startswith("/help"):
            cmd_help(chat_id)
            return

        if text.startswith("/brief"):
            typing(chat_id)
            result = mc_brief(ws)
            send(chat_id, result)
            return

        if text.startswith("/gaps"):
            typing(chat_id)
            result = mc_gaps(ws)
            send(chat_id, result)
            log_exchange(chat_id, "/gaps", result)
            return

        if text.startswith("/decisions"):
            typing(chat_id)
            result = mc_decisions(ws)
            send(chat_id, result)
            log_exchange(chat_id, "/decisions", result)
            return

        if text.startswith("/health"):
            typing(chat_id)
            result = mc_health(ws)
            send(chat_id, result)
            log_exchange(chat_id, "/health", result)
            return

        if text.startswith("/resolve "):
            parts = text[9:].strip().split(" ", 1)
            if len(parts) < 2:
                send(chat_id, "Usage: `/resolve ME-001 The answer to the evidence gap`")
                return
            typing(chat_id)
            result = mc_resolve(parts[0], parts[1], ws)
            send(chat_id, result)
            log_exchange(chat_id, f"/resolve {parts[0]}", result)
            return

        if text.startswith("/fact "):
            fact_text = text[6:].strip()
            if "|" in fact_text:
                fact, source = fact_text.rsplit("|", 1)
                fact, source = fact.strip(), source.strip()
            else:
                fact, source = fact_text, "user-provided"
            typing(chat_id)
            result = mc_add_fact(fact, source, ws)
            send(chat_id, result)
            log_exchange(chat_id, f"/fact", result)
            return

        if text.startswith("/workspace "):
            new_ws = text[11:].strip().lower().replace(" ", "-")
            set_workspace(chat_id, new_ws)
            send(chat_id, f"Switched to workspace: `{new_ws}`")
            return

        if text.startswith("/workspaces"):
            typing(chat_id)
            result = mc_get("workspaces")
            ws_list = result.get("workspaces", [])
            if ws_list:
                lines = [f"*Available workspaces:*\n"]
                for w in ws_list:
                    marker = " \u25c0" if w["id"] == ws else ""
                    lines.append(f"\u2022 `{w['id']}` \u2014 {w.get('name', w['id'])}{marker}")
                send(chat_id, "\n".join(lines))
            else:
                send(chat_id, "No workspaces found.")
            return

        if text.startswith("/research "):
            query = text[10:].strip()
            if not query:
                send(chat_id, "Usage: `/research Is Anthropic a good AI investment?`")
                return
            if not PERPLEXITY_KEY:
                send(chat_id, "Research requires a Perplexity API key. Ask your admin to set PERPLEXITY_API_KEY.")
                return
            typing(chat_id)
            result = perplexity_research(query)
            if result:
                send(chat_id, f"*Research:* _{query}_\n\n{result}")
                log_exchange(chat_id, f"/research {query}", result)
            else:
                send(chat_id, "Research returned no results. Try rephrasing.")
            return

        if text.startswith("/alerts"):
            typing(chat_id)
            alerts = load_alerts(ws)
            if not alerts:
                send(chat_id, "No alerts yet. Monitors will generate alerts when they run.")
                return
            lines = [f"*Recent Alerts* ({len(alerts)}):\n"]
            for a in alerts:
                ts = a.get("timestamp", "?")
                if isinstance(ts, str) and len(ts) > 16:
                    ts = ts[:16].replace("T", " ")
                name = a.get("monitor_name", a.get("monitor_id", "?"))
                content = a.get("content", "")[:300]
                lines.append(f"*{name}* ({ts})")
                lines.append(content)
                lines.append("")
            send(chat_id, "\n".join(lines))
            return

        if text.startswith("/monitors"):
            typing(chat_id)
            monitors = load_monitors(ws)
            if not monitors:
                send(chat_id, "No monitors configured for this workspace.")
                return
            lines = [f"*Active Monitors* ({len(monitors)}):\n"]
            for m in monitors:
                enabled = "ON" if m.get("enabled", True) else "OFF"
                schedule = m.get("schedule_minutes", "?")
                last_run = m.get("last_run", "never")
                if isinstance(last_run, str) and len(last_run) > 16:
                    last_run = last_run[:16].replace("T", " ")
                total = m.get("total_alerts", 0)
                lines.append(
                    f"*{m.get('name', m['id'])}* [{enabled}]\n"
                    f"  Schedule: every {schedule}m\n"
                    f"  Last run: {last_run}\n"
                    f"  Total alerts: {total}\n"
                    f"  _{m.get('description', '')}_"
                )
                lines.append("")
            send(chat_id, "\n".join(lines))
            return

        if text.startswith("/newworkspace "):
            parts = text[14:].strip().split("|", 1)
            if len(parts) < 2:
                send(chat_id, "Usage: `/newworkspace My Workspace Name | What I'm trying to figure out`")
                return
            name = parts[0].strip()
            objective = parts[1].strip()
            ws_id = name.lower().replace(" ", "-")[:40]
            ws_id = "".join(c for c in ws_id if c.isalnum() or c == "-")
            typing(chat_id)
            result = mc_create_workspace(ws_id, name, objective)
            send(chat_id, result)
            set_workspace(chat_id, ws_id)
            return

        # Regular message — smart routing between research and workspace
        typing(chat_id)
        save_chat_id(chat_id)  # persist for monitor daemon notifications
        response = smart_answer(text, ws)
        send(chat_id, response)
        log_exchange(chat_id, text, response)

    except Exception as e:
        print(f"[error] chat={chat_id}: {e}", flush=True)
        send(chat_id, f"Error: {e}")


# ── Polling loop ──────────────────────────────────────────────────────────────

def run() -> None:
    if not BOT_TOKEN:
        print("[mc-bot] JOSEPH_BOT_TOKEN not set. Exiting.", flush=True)
        sys.exit(1)

    print(f"[mc-bot] starting — server={MC_SERVER} workspace={MC_WORKSPACE}", flush=True)
    print(f"[mc-bot] Perplexity research: {'ENABLED' if PERPLEXITY_KEY else 'DISABLED (set PERPLEXITY_API_KEY)'}", flush=True)

    # Verify server is reachable
    try:
        health = mc_get("health")
        print(f"[mc-bot] server health: {health.get('status', 'unknown')}", flush=True)
    except Exception as e:
        print(f"[mc-bot] WARNING: server not reachable at {MC_SERVER}: {e}", flush=True)
        print("[mc-bot] will retry on first message...", flush=True)

    offset = 0
    while True:
        try:
            result = tg("getUpdates", offset=offset, timeout=POLL_TIMEOUT)
            if not result.get("ok"):
                print(f"[warn] getUpdates error: {result}", flush=True)
                time.sleep(5)
                continue

            for update in result.get("result", []):
                offset = update["update_id"] + 1
                msg = update.get("message") or update.get("edited_message")
                if not msg:
                    continue
                chat_id = msg["chat"]["id"]
                text = msg.get("text") or msg.get("caption", "")
                voice = msg.get("voice")

                if voice and not text:
                    try:
                        typing(chat_id)
                        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] voice from chat={chat_id}", flush=True)
                        text = transcribe_voice(voice["file_id"])
                        print(f"  transcribed: {text[:80]}", flush=True)
                    except Exception as e:
                        print(f"[error] transcribe: {e}", flush=True)
                        send(chat_id, f"Couldn't transcribe voice: {e}")
                        continue

                if text:
                    try:
                        handle_message(chat_id, text)
                    except Exception as e:
                        print(f"[error] handle: {e}", flush=True)

        except KeyboardInterrupt:
            print("\n[mc-bot] stopped.", flush=True)
            break
        except Exception as e:
            print(f"[error] poll: {e}", flush=True)
            time.sleep(5)


if __name__ == "__main__":
    run()
