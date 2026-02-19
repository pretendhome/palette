#!/usr/bin/env python3
"""
telegram_bridge.py — Palette × Telegram Bridge
Phone ↔ AI agent. Talk to Palette from anywhere.

Setup:
  1. Message @BotFather on Telegram → /newbot → copy your token
  2. export TELEGRAM_BOT_TOKEN="your-token"
  3. export ANTHROPIC_API_KEY="your-key"
  4. python3 telegram_bridge.py

Commands:
  /start           — welcome + help
  /interview josh  — become Josh Rutberg (VP Customer Outcomes, Glean)
  /interview avril — become Avril (AI Outcomes Specialist, Glean, Singapore)
  /feedback        — get honest feedback on your last answer
  /reset           — end interview, back to assistant
  /help            — list commands
"""
from __future__ import annotations

import os
import sys
import time
import json
import datetime
import tempfile
import httpx
import anthropic

# ── Config ────────────────────────────────────────────────────────────────────

BOT_TOKEN    = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
POLL_TIMEOUT = 30   # long-poll seconds
MAX_HISTORY  = 20   # messages kept per chat

TELEGRAM = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ── Interviewer profiles ──────────────────────────────────────────────────────

JOSH_SYSTEM = """You are Josh Rutberg, VP Customer Outcomes at Glean (San Francisco), \
conducting a second-round interview for the AI Outcomes Manager role.

YOUR BACKGROUND:
- VP Customer Outcomes at Glean, SF
- Bain & Company consulting background — you think in structured, layered frameworks
- 15+ years driving enterprise transformation at large tech companies
- You've operated at >115% Net Revenue Retention — you care deeply about measurable outcomes
- Focus areas: customer transformation, strategic value, go-to-market, executive alignment

YOUR INTERVIEW STYLE:
- Structured and commercial. You evaluate whether this person can operate at VP level.
- You ask layered follow-up questions that go progressively deeper. One question at a time.
- You probe for: specific outcomes (not activities), executive communication ability, \
how they handle ambiguity, how they build internal champions at customer orgs.
- You're polished and direct. You don't waste words. But you're not cold.
- You're genuinely curious about Palette — it's interesting to you as an AI-native system.

THINGS YOU CARE ABOUT:
- Can this person run a full customer engagement end-to-end?
- Do they think about business outcomes or just technical delivery?
- Can they hold a conversation with a CIO without losing them?
- Have they actually shipped something that moved a metric?

QUESTIONS YOU MIGHT ASK (ask ONE at a time, let them answer, go deeper):
- "Walk me through a specific AI initiative you drove — from scoping to measurable outcomes."
- "Tell me about a deployment that didn't go as expected. How did you course-correct?"
- "How do you approach executive alignment when there's resistance to AI adoption?"
- "What does a successful AI pilot look like versus a failed one — what separates them?"
- "How would you identify whether a Glean deployment is genuinely transformational \
vs. just being used?"
- "What's your philosophy on how much you should customize vs. use out-of-the-box?"

START: Greet them professionally. Tell them you have about 45 minutes. \
Ask your first question naturally. React to their answers with genuine follow-ups. \
After ~6 exchanges, if they ask for /feedback, give honest, specific, VP-level critique."""

AVRIL_SYSTEM = """You are Avril, an AI Outcomes Specialist at Glean (Singapore office), \
conducting a second-round interview for the AI Outcomes Manager role.

YOUR BACKGROUND:
- Hands-on AI Outcomes operator at Glean — you build and deploy agents with customers daily
- Based in Singapore, covering the APAC region
- Deep technical depth in how Glean's platform actually works at the implementation level
- You've seen many things that looked great in demos collapse in production
- You care about real execution, not consultant-speak

YOUR INTERVIEW STYLE:
- Warm and collaborative, but you can tell immediately when someone is bluffing.
- Operator-level — you ask for specifics, not generalities.
- You want to know: can this person actually build? Or do they just talk about building?
- You go deep on technical choices, failure modes, debugging moments.
- One question at a time. Let them answer fully. Then go deeper.

THINGS YOU CARE ABOUT:
- Have they actually designed an AI agent architecture, or just described one?
- Do they understand why things fail (retrieval, context, reasoning)?
- Can they scope a vague customer request into something buildable?
- Do they understand the human-in-the-loop question seriously?

QUESTIONS YOU MIGHT ASK (one at a time, go deep on specifics):
- "Tell me specifically how you designed one of your agents — the actual architecture."
- "Walk me through a time an AI system you built failed in production. What broke and why?"
- "How do you think about the boundary between what the AI handles vs. what goes to a human?"
- "A customer's agent starts returning irrelevant results. Walk me through your diagnosis."
- "How do you scope an AI use case with a customer who just says 'we want AI'?"
- "What's the hardest technical problem you've had to solve in an AI deployment?"

START: Greet them warmly. Mention you're joining from Singapore. \
Ask your first question — go straight to the technical/hands-on experience. \
React authentically to their answers. Ask for concrete details when answers are vague."""

ASSISTANT_SYSTEM = """You are Palette, a multi-agent AI system and personal assistant. \
You're running as a Telegram bridge — the user is talking to you from their phone.

Be conversational, direct, and useful. You have full context on:
- Palette's agent architecture (Cory, Argy, Orch, Raptor, Rex, Theri, Anky, Para, Yuty)
- The Glean AI Outcomes Manager interview the user is preparing for
- The user's background: 11 years at Amazon/AWS, built Palette, launched 27+ models on Bedrock

When the user asks something you can answer directly, answer it. \
When they want to run a command or analyze something complex, \
tell them what you'd route to which agent.

Available interview modes (tell the user if they seem to want practice):
  /interview josh  — VP Customer Outcomes, strategic/commercial focus
  /interview avril — AI Outcomes Specialist, hands-on technical focus"""

# ── Chat state ────────────────────────────────────────────────────────────────

class ChatState:
    def __init__(self):
        self.mode     = "assistant"   # assistant | interview_josh | interview_avril
        self.history  = []            # [{role, content}, ...]
        self.turn     = 0
        self.last_answer = ""         # for /feedback

    def add(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})
        if len(self.history) > MAX_HISTORY:
            self.history = self.history[-MAX_HISTORY:]

    def system_prompt(self) -> str:
        if self.mode == "interview_josh":
            return JOSH_SYSTEM
        if self.mode == "interview_avril":
            return AVRIL_SYSTEM
        return ASSISTANT_SYSTEM

    def mode_label(self) -> str:
        if self.mode == "interview_josh":  return "🦖 Josh Rutberg (VP Customer Outcomes)"
        if self.mode == "interview_avril": return "🌏 Avril (AI Outcomes, Singapore)"
        return "🤖 Palette Assistant"


states: dict[int, ChatState] = {}

def get_state(chat_id: int) -> ChatState:
    if chat_id not in states:
        states[chat_id] = ChatState()
    return states[chat_id]


# ── Telegram API helpers ──────────────────────────────────────────────────────

def tg(method: str, **kwargs) -> dict:
    with httpx.Client(timeout=35.0) as client:
        resp = client.post(f"{TELEGRAM}/{method}", json=kwargs)
        return resp.json()


def send(chat_id: int, text: str) -> None:
    """Send a message, splitting if > 4096 chars (Telegram limit)."""
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


# ── Voice transcription ───────────────────────────────────────────────────────

_whisper_model = None

def _get_whisper():
    global _whisper_model
    if _whisper_model is None:
        import whisper
        print("[palette-telegram] loading whisper model (base)...", flush=True)
        _whisper_model = whisper.load_model("base")
        print("[palette-telegram] whisper ready.", flush=True)
    return _whisper_model


def transcribe_voice(file_id: str) -> str:
    """Download a Telegram voice file and transcribe it with Whisper."""
    # Get file path from Telegram
    info = tg("getFile", file_id=file_id)
    if not info.get("ok"):
        raise RuntimeError(f"getFile failed: {info}")
    file_path = info["result"]["file_path"]

    # Download the OGG/Opus file
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


# ── Claude ────────────────────────────────────────────────────────────────────

def reply(state: ChatState, user_message: str) -> str:
    """Send message to Claude, return response."""
    state.add("user", user_message)

    client = anthropic.Anthropic()
    message = client.messages.create(
        model      = "claude-sonnet-4-6",
        max_tokens = 1024,
        system     = state.system_prompt(),
        messages   = state.history,
    )
    response = message.content[0].text
    state.add("assistant", response)
    return response


def get_feedback(state: ChatState, last_answer: str) -> str:
    """Ask Claude to give honest interview feedback on the last answer."""
    interviewer = "Josh Rutberg" if state.mode == "interview_josh" else "Avril"
    prompt = (
        f"Step out of character for a moment. As {interviewer}, give honest, specific, "
        f"constructive feedback on this answer the candidate just gave:\n\n"
        f"\"{last_answer}\"\n\n"
        f"What was strong? What was weak? What should they change? "
        f"Be direct — this is coaching, not flattery. 3-5 bullet points."
    )
    client = anthropic.Anthropic()
    message = client.messages.create(
        model      = "claude-sonnet-4-6",
        max_tokens = 600,
        system     = state.system_prompt(),
        messages   = state.history + [{"role": "user", "content": prompt}],
    )
    return message.content[0].text


# ── Command handlers ──────────────────────────────────────────────────────────

def cmd_start(chat_id: int) -> None:
    send(chat_id,
        "👋 *Palette is live.*\n\n"
        "I'm your AI agent, accessible from Telegram.\n\n"
        "*Interview simulation:*\n"
        "`/interview josh` — Josh Rutberg, VP Customer Outcomes\n"
        "`/interview avril` — Avril, AI Outcomes Specialist (Singapore)\n\n"
        "*Controls:*\n"
        "`/feedback` — get honest feedback on your last answer\n"
        "`/reset` — end interview, back to assistant\n"
        "`/help` — this menu\n\n"
        "Or just talk — I'm listening."
    )


def cmd_help(chat_id: int, state: ChatState) -> None:
    send(chat_id,
        f"*Current mode:* {state.mode_label()}\n\n"
        "`/interview josh` — simulate Josh (VP, strategic)\n"
        "`/interview avril` — simulate Avril (hands-on, technical)\n"
        "`/feedback` — coaching on your last answer\n"
        "`/reset` — back to assistant\n"
        "`/help` — this menu"
    )


def cmd_interview(chat_id: int, state: ChatState, who: str) -> None:
    who = who.strip().lower()
    if who == "josh":
        state.mode    = "interview_josh"
        state.history = []
        state.turn    = 0
        send(chat_id, "🦖 *Josh Rutberg mode.*\nResetting conversation. Starting your interview...\n")
        typing(chat_id)
        opening = reply(state, "[The candidate has just joined the video call.]")
        send(chat_id, opening)
    elif who == "avril":
        state.mode    = "interview_avril"
        state.history = []
        state.turn    = 0
        send(chat_id, "🌏 *Avril mode.*\nResetting conversation. Starting your interview...\n")
        typing(chat_id)
        opening = reply(state, "[The candidate has just joined the video call from San Francisco.]")
        send(chat_id, opening)
    else:
        send(chat_id, "Who?\n`/interview josh` or `/interview avril`")


def cmd_feedback(chat_id: int, state: ChatState) -> None:
    if state.mode == "assistant":
        send(chat_id, "Not in interview mode. Use `/interview josh` or `/interview avril` first.")
        return
    if not state.last_answer:
        send(chat_id, "Answer a question first, then ask for feedback.")
        return
    typing(chat_id)
    fb = get_feedback(state, state.last_answer)
    send(chat_id, f"📋 *Feedback on your last answer:*\n\n{fb}")


def cmd_reset(chat_id: int, state: ChatState) -> None:
    state.mode    = "assistant"
    state.history = []
    state.turn    = 0
    send(chat_id, "✅ Interview ended. Back to assistant mode.\n\nWhat do you need?")


# ── Message router ────────────────────────────────────────────────────────────

def handle_message(chat_id: int, text: str) -> None:
    state = get_state(chat_id)
    text  = text.strip()

    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] chat={chat_id} mode={state.mode} | {text[:60]}", flush=True)

    # Commands
    if text.startswith("/start"):
        cmd_start(chat_id)
        return
    if text.startswith("/help"):
        cmd_help(chat_id, state)
        return
    if text.startswith("/reset"):
        cmd_reset(chat_id, state)
        return
    if text.startswith("/feedback"):
        cmd_feedback(chat_id, state)
        return
    if text.startswith("/interview"):
        parts = text.split(maxsplit=1)
        who   = parts[1] if len(parts) > 1 else ""
        cmd_interview(chat_id, state, who)
        return

    # Regular message — pass to Claude
    if state.mode != "assistant":
        state.last_answer = text  # save for /feedback
        state.turn += 1

    typing(chat_id)
    response = reply(state, text)
    send(chat_id, response)


# ── Polling loop ──────────────────────────────────────────────────────────────

def run() -> None:
    print(f"[palette-telegram] starting long-poll loop", flush=True)
    print(f"[palette-telegram] bot: {TELEGRAM.split('bot')[1][:8]}...", flush=True)

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
                msg    = update.get("message") or update.get("edited_message")
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
                        handle_message(chat_id, text)
                    except Exception as e:
                        print(f"[error] handle_message: {e}", flush=True)
                        send(chat_id, f"⚠️ Error: {e}")

        except httpx.RequestError as e:
            print(f"[error] network: {e}", flush=True)
            time.sleep(10)
        except KeyboardInterrupt:
            print("\n[palette-telegram] stopped.", flush=True)
            sys.exit(0)
        except Exception as e:
            print(f"[error] unexpected: {e}", flush=True)
            time.sleep(5)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN not set")
        print("  export TELEGRAM_BOT_TOKEN='your-token-from-BotFather'")
        sys.exit(1)
    if not ANTHROPIC_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set")
        sys.exit(1)
    run()
