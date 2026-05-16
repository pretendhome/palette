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
  /stress     — market stress probability (CAPE + Buffett + P/S)
  /tech       — tech landscape brief (PIS-powered, 43 tools, 21 voices)
  /intel      — financial intelligence brief (voices, thesis signals, consensus)
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

RESOLVER_URL    = os.environ.get("RESOLVER_URL", "http://localhost:8788")

TELEGRAM = f"https://api.telegram.org/bot{BOT_TOKEN}"
PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"

# ── Telegram helpers ───────────────────────────────────────────────────────────

def tg(method: str, **kwargs) -> dict:
    with httpx.Client(timeout=35.0) as client:
        resp = client.post(f"{TELEGRAM}/{method}", json=kwargs)
        return resp.json()


def send(chat_id: int, text: str, buttons: list[list[dict]] | None = None) -> None:
    """Send a message, optionally with inline keyboard buttons.

    buttons format: [[{"text": "Label", "callback_data": "cb:action:data"}], ...]
    Each inner list is a row of buttons.
    """
    chunk_size = 4000
    reply_markup = None
    if buttons:
        reply_markup = {"inline_keyboard": buttons}

    for i in range(0, len(text), chunk_size):
        kwargs = {
            "chat_id": chat_id,
            "text": text[i : i + chunk_size],
            "parse_mode": "Markdown",
        }
        # Only attach buttons to the last chunk
        if reply_markup and i + chunk_size >= len(text):
            kwargs["reply_markup"] = reply_markup
        tg("sendMessage", **kwargs)
        if i + chunk_size < len(text):
            time.sleep(0.3)


def typing(chat_id: int) -> None:
    tg("sendChatAction", chat_id=chat_id, action="typing")


def answer_callback(callback_query_id: str, text: str = "") -> None:
    """Answer a callback query (dismisses the loading spinner on the button)."""
    kwargs = {"callback_query_id": callback_query_id}
    if text:
        kwargs["text"] = text[:200]
    tg("answerCallbackQuery", **kwargs)


# ── Callback state (in-memory, maps callback IDs to research queries) ────────

_pending_research: dict[str, str] = {}  # key: short_id, value: research query
_research_counter = 0


def _store_research(query: str) -> str:
    """Store a research query and return a short callback ID."""
    global _research_counter
    _research_counter += 1
    key = f"r{_research_counter}"
    _pending_research[key] = query
    # Keep only last 50 to prevent memory leak
    if len(_pending_research) > 50:
        oldest = list(_pending_research.keys())[:20]
        for k in oldest:
            del _pending_research[k]
    return key


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


# ── Monitor intent detection ──────────────────────────────────────────────────

# Patterns that indicate the user wants to CREATE a monitor/alert (not research)
_MONITOR_REQUEST_PATTERNS = [
    r'\b(ping|alert|notify|tell|text|message|flag)\b.*\b(me|us)\b.*\b(when|if|second|moment|once|as soon)\b',
    r'\b(watch|monitor|track)\b.*\b(for|when|if)\b',
    r'\b(let me know|heads up|keep.*(eye|watch))\b.*\b(when|if|on)\b',
    r'\b(set\s*(up\s+)?(an?\s+)?alert|create\s*(a\s+)?monitor|add\s*(a\s+)?watch)\b',
]


def is_monitor_request(text: str) -> bool:
    """Check if the user is asking to set up a monitoring alert."""
    q = text.lower().strip()
    for pattern in _MONITOR_REQUEST_PATTERNS:
        if re.search(pattern, q):
            return True
    return False


def create_monitor_from_request(text: str, workspace_id: str) -> str:
    """Parse a natural-language monitoring request and create a monitor YAML.

    Returns a confirmation message for the user.
    """
    q = text.lower()
    now = datetime.datetime.now()
    monitor_id = f"user-{now.strftime('%Y%m%d-%H%M%S')}"

    # ── Extract schedule urgency ──
    # "the second", "immediately", "as soon as" → fast (15 min)
    # "daily" → 1440 min, "hourly" → 60 min, default → 30 min
    if re.search(r'(the second|immediately|right away|as soon as|instant)', q):
        schedule = 15
    elif re.search(r'\bdaily\b', q):
        schedule = 1440
    elif re.search(r'\bhourly\b', q):
        schedule = 60
    else:
        schedule = 30

    # ── Extract threshold if present ──
    threshold_match = re.search(r'(\d+(?:\.\d+)?)\s*%', q)
    threshold = threshold_match.group(1) + "%" if threshold_match else None

    direction = "either direction"
    if re.search(r'\b(drop|fall|crash|decline|down)\b', q) and not re.search(r'\b(rise|up|rally|gain)\b', q):
        direction = "downward"
    elif re.search(r'\b(rise|up|rally|gain|surge)\b', q) and not re.search(r'\b(drop|fall|crash|decline|down)\b', q):
        direction = "upward"

    # ── Extract what to monitor ──
    # Strip the intent verbs to isolate the subject
    subject = re.sub(r'^.*?\b(when|if|that|second|moment|once)\b\s*', '', q, count=1).strip()
    # Clean trailing punctuation
    subject = re.sub(r'[.!?]+$', '', subject).strip()
    if not subject or len(subject) < 3:
        subject = re.sub(r'\b(ping|alert|notify|tell|watch|monitor|track|me|us)\b', '', q).strip()

    # Build human-readable name
    name = subject[:60].strip().title() if subject else "Custom Alert"
    if threshold:
        name = f"{name} ({threshold})"

    # ── Build search queries ──
    search_queries = [
        f"{subject} latest significant change today",
        f"{subject} breaking news price movement",
    ]
    if threshold:
        search_queries.append(f"{subject} {threshold} move change")

    # ── Build system prompt ──
    system_lines = [
        "You are a real-time market monitor. Your ONLY job is to detect whether a specific condition has been met.",
        f"Condition: {subject}",
    ]
    if threshold:
        system_lines.append(f"Threshold: {threshold} move {direction}")
    system_lines += [
        "",
        "If the condition has NOT been met, respond with exactly: NO_TRIGGER",
        "If the condition HAS been met or is very close, respond with a brief factual report including specific numbers, percentages, and time.",
        "Do NOT include general market commentary. Only report if the specific trigger condition is met.",
    ]

    monitor_data = {
        "monitor": {
            "id": monitor_id,
            "name": name,
            "description": f"User-requested alert: {text[:200]}",
            "enabled": True,
            "schedule_minutes": schedule,
            "search_queries": search_queries,
            "system_prompt": "\n".join(system_lines),
            "filter_keywords": [],
            "notify_channels": ["telegram"],
            "context": {
                "workspace_id": workspace_id,
                "relevance_threshold": "high",
                "max_alerts_per_run": 1,
                "trigger_condition": text[:300],
                "threshold": threshold,
                "direction": direction,
            },
            "last_run": None,
            "last_alert_count": 0,
            "total_alerts": 0,
        }
    }

    # ── Save to workspace monitors dir ──
    monitors_dir = Path(WORKSPACES_DIR) / workspace_id / "monitors"
    monitors_dir.mkdir(parents=True, exist_ok=True)
    monitor_path = monitors_dir / f"{monitor_id}.yaml"
    with open(monitor_path, "w") as f:
        yaml.dump(monitor_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    # ── Confirmation ──
    confirm_lines = [
        f"*Monitor created:* {name}",
        f"Checking every {schedule} minutes",
    ]
    if threshold:
        confirm_lines.append(f"Trigger: {threshold} move {direction}")
    confirm_lines.append(f"\nUse /monitors to see all active monitors.")
    return "\n".join(confirm_lines)


# ── Intent routing ───────────────────────────────────────────────────────────
# Primary: Resolver service (LLM-based cluster → RIU → grounded prompt)
# Fallback: regex workspace patterns (if resolver is down)

# Fast-path patterns for workspace questions (fallback only)
_WORKSPACE_PATTERNS = [
    r'(should i|do i|trim|sell|buy|add|hold|exit)',
    r'(what.*focus|what.*first|what.*priority|where.*start)',
    r'(how.*doing|status|update|overview)',
    r'(block|stuck|missing|gap|need)',
    r'(risk|hedge|protect|downside)',
    r'(decision|approve|reject|verify|resolve)',
    r'(brief|health|score|nudge)',
]

def is_workspace_question(text: str) -> bool:
    """Check if this matches workspace state patterns (fallback)."""
    q = text.lower().strip()
    for pattern in _WORKSPACE_PATTERNS:
        if re.search(pattern, q):
            return True
    return False


def call_resolver(text: str, session_id: str = "", context: str = "") -> dict | None:
    """Call the Resolver service. Returns parsed response or None if unavailable."""
    try:
        with httpx.Client(timeout=15.0) as client:
            resp = client.post(
                f"{RESOLVER_URL}/resolve",
                json={"input": text, "session_id": session_id, "context": context},
            )
            if resp.status_code == 200:
                return resp.json()
    except Exception as e:
        print(f"[resolver] unavailable: {e}", flush=True)
    return None


def format_resolver_response(result: dict, question: str) -> str:
    """Format a resolver result as a Telegram-friendly message."""
    status = result.get("status")

    if status == "resolved":
        prompt = result.get("grounded_prompt", "")
        return prompt or "I'm not sure how to help with that."

    if status == "clarify":
        return result.get("question", "Could you tell me more?")

    if status == "out_of_scope":
        return result.get("message", "I'm not sure how to help with that.")


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
    """Smart routing — three tiers:
       1. Monitor requests → create monitor (pattern match, instant)
       2. Resolver service → LLM-based intent classification → grounded prompt
       3. Fallback → regex workspace detection + Perplexity default
    """

    # 1. Monitor/alert requests — pattern match, no LLM needed
    if is_monitor_request(question):
        return create_monitor_from_request(question, workspace_id)

    # 2. Resolver service — the primary brain
    #    Classifies intent via cluster → RIU → knowledge library → grounded prompt
    session_id = str(workspace_id)  # one session per workspace for multi-turn
    try:
        ws_config = load_yaml_file(Path(WORKSPACES_DIR) / workspace_id / "config.yaml")
        ws_context = ws_config.get("workspace", {}).get("description", "")
    except Exception:
        ws_context = ""

    resolver_result = call_resolver(question, session_id, ws_context)

    if resolver_result:
        status = resolver_result.get("status")

        if status == "resolved":
            # Resolver matched with confidence — use the grounded prompt
            grounded = resolver_result.get("grounded_prompt", "")
            knowledge = resolver_result.get("knowledge", {})
            agent = resolver_result.get("suggested_agent", "")

            # If the suggested agent is "researcher" → enhance with Perplexity
            if agent == "researcher" and PERPLEXITY_KEY:
                research = perplexity_research(grounded or question, ws_context)
                if research:
                    formatted = format_resolver_response(resolver_result, question)
                    return f"{research}\n\n---\n{formatted}"

            # For all other agents → return the grounded prompt + metadata
            return format_resolver_response(resolver_result, question)

        if status == "clarify":
            # Resolver needs more info — pass the question to the user
            return format_resolver_response(resolver_result, question)

        if status == "out_of_scope":
            # Resolver couldn't match — try Perplexity as fallback
            if PERPLEXITY_KEY:
                answer = perplexity_research(question, ws_context)
                if answer:
                    return answer
            return format_resolver_response(resolver_result, question)

    # 3. Fallback — resolver unavailable, use regex + Perplexity
    if is_workspace_question(question):
        return mc_ask(question, workspace_id)

    if PERPLEXITY_KEY:
        answer = perplexity_research(question, ws_context)
        if answer:
            return answer

    return mc_ask(question, workspace_id)


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


def _cmd_morning_brief(chat_id: int) -> None:
    """Generate the phone-optimized morning brief with inline buttons."""
    tech_dir = Path(__file__).parent.parent / "buy-vs-build" / "tech"
    brief_path = tech_dir / "morning_brief.py"

    if not brief_path.exists():
        send(chat_id, "Morning brief engine not found.")
        return

    sys.path.insert(0, str(tech_dir))
    try:
        import morning_brief
        result = morning_brief.generate_morning_brief(PERPLEXITY_KEY)
        text = morning_brief.format_telegram(result)

        # Build section navigation buttons
        buttons = [
            [
                {"text": "\U0001f4f0 News", "callback_data": "cb:section:news"},
                {"text": "\u26a1 Disrupt", "callback_data": "cb:section:disruption"},
                {"text": "\U0001f4ca Trends", "callback_data": "cb:section:trends"},
            ],
            [
                {"text": "\U0001f4b9 Stress", "callback_data": "cb:cmd:stress"},
                {"text": "\U0001f3af Exposed", "callback_data": "cb:cmd:vulnerable"},
                {"text": "\U0001f3c6 Winners", "callback_data": "cb:cmd:beneficiaries"},
            ],
        ]

        # Extract research prompts from the brief text and add research buttons
        research_buttons = []
        for line in result.split("\n"):
            if line.strip().startswith("/research "):
                query = line.strip()[10:]
                key = _store_research(query)
                short_label = query[:30] + "..." if len(query) > 30 else query
                research_buttons.append(
                    {"text": f"\U0001f50d {short_label}", "callback_data": f"cb:research:{key}"}
                )

        # Add research buttons as rows (one per row, max 3)
        for rb in research_buttons[:3]:
            buttons.append([rb])

        send(chat_id, text, buttons=buttons)
    except Exception as e:
        print(f"[error] morning brief: {e}", flush=True)
        send(chat_id, f"Morning brief error: {e}")
    finally:
        sys.path.pop(0)
        sys.modules.pop("morning_brief", None)


def _cmd_stress() -> str:
    """Run the market stress model: fetch current metrics via Perplexity, compute risk."""
    from market_stress import fetch_current_metrics, compute_stress, format_stress_report

    if not PERPLEXITY_KEY:
        return "Market stress requires Perplexity API. Set PERPLEXITY_API_KEY."

    metrics = fetch_current_metrics(PERPLEXITY_KEY)
    if not metrics:
        return (
            "Couldn't fetch current market metrics. "
            "Try `/research current Shiller PE CAPE, Buffett Indicator, S&P 500 P/S ratio`"
        )

    result = compute_stress(
        cape=metrics["cape"],
        buffett=metrics["buffett"],
        ps_ratio=metrics["ps_ratio"],
    )
    return format_stress_report(result)


def _cmd_tech(query: str) -> str:
    """Run the Tech Engine — PIS-powered tech intelligence (read-only on PIS data)."""
    tech_dir = Path(__file__).parent.parent / "buy-vs-build" / "tech"
    engine_path = tech_dir / "tech_engine.py"

    if not engine_path.exists():
        return "Tech engine not found. Expected at: " + str(engine_path)

    sys.path.insert(0, str(tech_dir))
    try:
        import tech_engine

        if not query or query.lower() in ("", "brief", "all"):
            return tech_engine.format_telegram(tech_engine.generate_brief())
        elif query.lower().startswith("tier "):
            try:
                tier = int(query.split()[1])
                return tech_engine.format_telegram(tech_engine.list_by_tier(tier))
            except (ValueError, IndexError):
                return "Usage: `/tech tier 1` (or 2 or 3)"
        elif query.lower().startswith("action "):
            action = query.split(None, 1)[1].strip().lower()
            return tech_engine.format_telegram(tech_engine.list_by_action(action))
        elif query.lower().startswith("cluster "):
            cluster = query.split(None, 1)[1].strip().lower().replace(" ", "_")
            return tech_engine.format_telegram(tech_engine.list_cluster(cluster))
        elif query.lower() in ("disruption", "disrupt", "theses"):
            return tech_engine.format_telegram(tech_engine.disruption_brief())
        elif query.lower().startswith("thesis "):
            thesis_id = query.split(None, 1)[1].strip()
            return tech_engine.format_telegram(tech_engine.lookup_thesis(thesis_id))
        elif query.lower() in ("vulnerable", "exposed", "risk", "risks"):
            return tech_engine.format_telegram(tech_engine.vulnerable_companies())
        elif query.lower() in ("beneficiaries", "winners", "benefit"):
            return tech_engine.format_telegram(tech_engine.beneficiary_companies())
        elif query.lower() in ("morning", "morning brief", "investor"):
            return tech_engine.format_telegram(tech_engine.morning_disruption_brief())
        else:
            # Check if query matches a disruption topic before falling back to PIS
            disruption_result = tech_engine.query_disruption(query)
            if "No disruption theses match" not in disruption_result:
                return tech_engine.format_telegram(disruption_result)
            report = tech_engine.query_tech(query, use_perplexity=bool(PERPLEXITY_KEY))
            return tech_engine.format_telegram(report)
    finally:
        sys.path.pop(0)
        sys.modules.pop("tech_engine", None)


def _cmd_intel(query: str) -> str:
    """Run the Intel Engine — financial intelligence query system."""
    intel_dir = Path(__file__).parent.parent / "buy-vs-build" / "intel"
    engine_path = intel_dir / "intel_engine.py"

    if not engine_path.exists():
        return "Intel engine not found. Expected at: " + str(engine_path)

    # Add intel dir to path so we can import it
    sys.path.insert(0, str(intel_dir))
    try:
        import intel_engine

        if not query or query.lower() in ("", "brief", "all"):
            return intel_engine.format_telegram(intel_engine.generate_brief())
        elif query.upper().startswith("THESIS-"):
            result = intel_engine.lookup_thesis(query.upper())
            if "error" in result:
                return result["error"]
            cat = result.get("category", {})
            lines = [f"*{cat.get('name', query)}*"]
            lines.append(f"Voices: {result.get('voice_count', 0)}")
            lines.append(f"Consensus: {result.get('consensus_note', 'None')}\n")
            for v in result.get("voices", []):
                lines.append(f"• *{v['name']}* ({v['signal_strength']}): {v['edge']}")
            return "\n".join(lines)
        else:
            report = intel_engine.intel_pass(query, use_perplexity=bool(PERPLEXITY_KEY))
            return intel_engine.format_telegram(report)
    finally:
        sys.path.pop(0)
        # Remove cached module so re-import picks up changes
        sys.modules.pop("intel_engine", None)


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

    # Load workspace config for personalized greeting
    ws_config_path = Path(WORKSPACES_DIR) / ws / "config.yaml"
    ws_user_name = None
    ws_description = None
    if ws_config_path.exists():
        try:
            cfg = load_yaml_file(ws_config_path)
            ws_info = cfg.get("workspace", {})
            ws_user_name = ws_info.get("user_name")
            ws_description = ws_info.get("description")
        except Exception:
            pass

    greeting = f"Hi {ws_user_name}! " if ws_user_name else ""
    desc_line = f"_{ws_description}_\n\n" if ws_description else ""

    send(chat_id,
        f"*Mission Canvas*{has_pplx}\n\n"
        f"{greeting}Connected to workspace: `{ws}`\n"
        f"{desc_line}"
        "*What you can do:*\n"
        "`/brief` \u2014 morning brief (fresh news + disruptions + trends)\n"
        "`/tech disruption` \u2014 all 12 disruption theses\n"
        "`/tech IBM` \u2014 search any company or topic\n"
        "`/stress` \u2014 market stress (CAPE + Buffett + P/S)\n"
        "`/intel` \u2014 financial intelligence brief\n"
        "`/research <query>` \u2014 live Perplexity search\n"
        "`/help` \u2014 full command list\n\n"
        "Or just ask in plain English. Voice works too.\n\n"
        "*Start here:*\n"
        "\u2022 `/brief` \u2014 what happened + what to watch\n"
        "\u2022 `/tech vulnerable` \u2014 most exposed companies\n"
        "\u2022 _\"Will Redis solve the context engine problem?\"_"
    )


def cmd_help(chat_id: int) -> None:
    ws = get_workspace(chat_id)
    has_pplx = " + Perplexity" if PERPLEXITY_KEY else ""
    send(chat_id,
        f"*Mission Canvas*{has_pplx} \u2014 workspace: `{ws}`\n\n"
        "*Morning:*\n"
        "`/brief` \u2014 fresh news + disruptions + trends\n"
        "`/stress` \u2014 market stress (CAPE + Buffett + P/S)\n\n"
        "*Disruption Intel:*\n"
        "`/tech disruption` \u2014 all 12 disruption theses\n"
        "`/tech thesis DISRUPT-CLOUD-PEAK` \u2014 deep-dive a thesis\n"
        "`/tech vulnerable` \u2014 most exposed companies\n"
        "`/tech beneficiaries` \u2014 who wins\n"
        "`/tech morning` \u2014 investor morning brief\n"
        "`/tech Redis` \u2014 search any company/topic\n\n"
        "*Research:*\n"
        "`/intel` \u2014 financial voices + thesis signals\n"
        "`/research <query>` \u2014 live Perplexity search\n"
        "`/tech brief` \u2014 full PIS landscape (tools, voices)\n\n"
        "*Workspace:*\n"
        "`/gaps` \u2014 evidence gaps & blockers\n"
        "`/decisions` \u2014 open decisions\n"
        "`/health` \u2014 workspace health score\n"
        "`/alerts` \u2014 recent monitor alerts\n"
        "`/monitors` \u2014 active monitors\n"
        "`/resolve ID answer` \u2014 resolve a gap\n"
        "`/fact text | source` \u2014 add a fact\n"
        "`/workspace id` \u2014 switch workspace\n\n"
        "Or just ask in plain English. Voice works too."
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
            _cmd_morning_brief(chat_id)
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

        if text.startswith("/stress"):
            typing(chat_id)
            result = _cmd_stress()
            send(chat_id, result)
            log_exchange(chat_id, "/stress", result)
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

        if text.startswith("/tech"):
            typing(chat_id)
            try:
                tech_arg = text[5:].strip()
                result = _cmd_tech(tech_arg)
                send(chat_id, result)
                log_exchange(chat_id, f"/tech {tech_arg}", result)
            except Exception as e:
                print(f"[error] /tech: {e}", flush=True)
                send(chat_id, f"Tech engine error: {e}")
            return

        if text.startswith("/intel"):
            typing(chat_id)
            try:
                intel_arg = text[6:].strip()
                result = _cmd_intel(intel_arg)
                send(chat_id, result)
                log_exchange(chat_id, f"/intel {intel_arg}", result)
            except Exception as e:
                print(f"[error] /intel: {e}", flush=True)
                send(chat_id, f"Intel engine error: {e}")
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


# ── Callback query handler (inline button taps) ─────────────────────────────

def handle_callback(callback: dict) -> None:
    """Handle an inline keyboard button tap."""
    cb_id = callback["id"]
    chat_id = callback["message"]["chat"]["id"]
    data = callback.get("data", "")

    print(f"[callback] chat={chat_id} data={data}", flush=True)

    # Parse callback_data format: "cb:type:payload"
    parts = data.split(":", 2)
    if len(parts) < 3:
        answer_callback(cb_id, "Unknown action")
        return

    _, cb_type, payload = parts

    if cb_type == "research":
        # Look up stored research query and run Perplexity
        query = _pending_research.get(payload)
        if not query:
            answer_callback(cb_id, "Query expired — ask again")
            return
        answer_callback(cb_id, "Searching...")
        typing(chat_id)
        result = perplexity_research(query)
        if result:
            send(chat_id, f"\U0001f50d *{query[:60]}*\n\n{result}")
        else:
            send(chat_id, "No results. Try rephrasing.")

    elif cb_type == "section":
        # Expand a brief section
        answer_callback(cb_id)
        typing(chat_id)
        ws = get_workspace(chat_id)

        if payload == "news":
            # Re-run brief and extract just the NEW section
            _cmd_morning_brief(chat_id)

        elif payload == "disruption":
            result = _cmd_tech("disruption")
            send(chat_id, result)

        elif payload == "trends":
            result = _cmd_tech("morning")
            send(chat_id, result)

    elif cb_type == "cmd":
        # Run a command directly
        answer_callback(cb_id)
        typing(chat_id)

        if payload == "stress":
            result = _cmd_stress()
            send(chat_id, result)
        elif payload == "vulnerable":
            result = _cmd_tech("vulnerable")
            send(chat_id, result)
        elif payload == "beneficiaries":
            result = _cmd_tech("beneficiaries")
            send(chat_id, result)
        else:
            send(chat_id, f"Unknown command: {payload}")

    else:
        answer_callback(cb_id, "Unknown callback")


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

                # ── Handle callback queries (inline button taps) ──
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
