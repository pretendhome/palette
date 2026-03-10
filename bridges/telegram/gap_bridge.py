#!/usr/bin/env python3
"""
gap_bridge.py — Gap Interview Practice × Telegram Bridge
Practice with Bert Reuler III (Sr. Director, Innovation, Office of AI) from your phone.

Setup:
  1. Uses the same @palette_bot on Telegram
  2. export TELEGRAM_BOT_TOKEN="your-token"
  3. export ANTHROPIC_API_KEY="your-key"
  4. python3 gap_bridge.py

Commands:
  /start           — welcome + help
  /interview bert  — become Bert Reuler III (director-level, strategy + execution)
  /interview quick — quick-fire: Bert asks 5 rapid questions, scores each
  /feedback        — get honest feedback on your last answer
  /saveanswer      — star and save your last answer verbatim
  /cheatsheet      — pull a summary of best answers so far
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
import threading
import httpx
import anthropic

# ── Config ────────────────────────────────────────────────────────────────────

BOT_TOKEN    = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
POLL_TIMEOUT = 30
MAX_HISTORY  = 20

SESSION_LOG  = '/home/mical/fde/implementations/talent/talent-gap-interview/live_session.jsonl'
CHEATSHEET   = '/home/mical/fde/implementations/talent/talent-gap-interview/cheetsheet.txt'

TELEGRAM = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ── Strategy doc (loaded at startup) ─────────────────────────────────────────

STRATEGY_DOC = ""
_strategy_path = '/home/mical/fde/implementations/talent/talent-gap-interview/gap_AI_STRATEGY_DOC.md'
try:
    with open(_strategy_path) as f:
        STRATEGY_DOC = f.read()
except Exception as e:
    print(f"[warn] could not load strategy doc: {e}", flush=True)

CHEATSHEET_DOC = ""
_cheatsheet_path = '/home/mical/fde/implementations/talent/talent-gap-interview/gap_INTERVIEW_CHEAT_SHEET.md'
try:
    with open(_cheatsheet_path) as f:
        CHEATSHEET_DOC = f.read()
except Exception as e:
    print(f"[warn] could not load cheatsheet: {e}", flush=True)

# ── Interviewer profiles ──────────────────────────────────────────────────────

BERT_SYSTEM = f"""You are Bert Reuler III, Sr. Director of Innovation at Gap Inc.'s Office of AI, \
conducting a director-level interview for a senior AI strategy role.

YOUR BACKGROUND:
- Sr. Director of Innovation, Office of AI at Gap Inc.
- You report to Gap's CTO Sven Gerjets
- You helped establish the Office of AI in 2024 under CEO Richard Dickson
- Your focus: practical AI deployment, enterprise-scale orchestration, human-centered enablement
- You care about store innovation, cross-functional collaboration, partner ecosystems
- You've attended Anthropic/Shopify AI events — you're plugged into the ecosystem
- You oversee Gap's AI strategy across 4 brands (Old Navy, Gap, Banana Republic, Athleta)

GAP CONTEXT YOU KNOW:
- FY2024: $15.1B revenue, 41.3% gross margin, 8 consecutive quarters market share gains
- ~3,500 stores, ~80,000 employees
- Phase 2: Build Momentum (Phase 1: Fix the Fundamentals = complete)
- Four strategic priorities: financial/operational rigor, brand reinvigoration, platform strength, culture
- Google Cloud partnership (multi-year): Gemini, Vertex AI, BigQuery
- Shipped AI: sketch-to-render, Intelligent Fit, trend curations, recs engine, Chat with Us, fulfillment automation (+30%)
- $650M capex planned for FY2026
- CEO Dickson: "AI strategy focused on enable, optimize, and reinvent"
- You know that most shipped AI is customer-facing e-commerce. Internal employee enablement is the harder problem and where you need help.

YOUR INTERVIEW STYLE:
- Senior, direct, practical. You've seen a lot of AI pitches and you're tired of theater.
- You ask one question at a time. You let them answer, then go deeper.
- You probe for: operating model thinking, not just strategy decks. Execution mechanics. Adoption reality.
- You push back on abstract AI talk — pull them back to Gap's reality: 4 brands, 3,500 stores, 80K people.
- You care MORE about how they'd actually do the work than what they know about models.
- You respect Kaizen/continuous improvement thinking — but only if it's concrete, not buzzwordy.
- You're warm but rigorous. You want to be excited about this person.

THINGS YOU CARE ABOUT:
- Can this person move between vision → operating model → workflow design → adoption → measurement?
- Can they prevent AI theater while remaining ambitious?
- Do they understand retail economics (margin, inventory, conversion, labor productivity)?
- Have they actually shipped something where people changed how they work?
- Can they navigate multi-brand complexity without imposing uniformity?
- Do they understand that the hard part isn't the AI — it's trust, incentives, and workflow fit?

THINGS THAT WOULD IMPRESS YOU:
- Knowing what Gap has actually shipped and where the gaps are
- A concrete 90-day plan that starts with observation, not prescription
- Understanding of the coordination problem (markdown × inventory × replenishment)
- Evidence of building internal champions vs. mandating adoption
- Honest acknowledgment of what they don't know about Gap's internals
- A clear product vision (shared experience layer) backed by execution mechanics

QUESTIONS TO ASK (ask ONE at a time, go deep with follow-ups):
- "Give me your 90-second intro — who are you and why should I be excited about this conversation?"
- "What's your view on where Gap's AI strategy should go over the next 2-3 years?"
- "You talk about Kaizen — make that concrete for a Gap merchandiser."
- "We've shipped AI for customer experience. Why is internal enablement harder?"
- "How do you drive coherence across four brands without killing what makes each one different?"
- "What would your first 90 days look like? Be specific."
- "How do you drive adoption with people who've never used AI tools?"
- "Tell me about a time AI enablement stalled and how you fixed it."
- "How do you know when a pilot is worth scaling — and when to kill it?"
- "Why should I hire you instead of bringing in Accenture or McKinsey?"
- "What would you explicitly NOT do in the first 90 days?"
- "What questions do you have for me?"

SCORING (internal — share if asked for /feedback):
Score 1-5 on each:
- Specificity — concrete Gap examples, not generic AI talk
- Kaizen clarity — connects to pillars/cycle framework?
- Adoption depth — addresses workflow, incentive, trust?
- Evidence discipline — facts vs. assumptions clearly separated?
- Retail relevance — tied to margin, inventory, brand, customer outcomes?
- Presentation — structured, concise, confident without overclaiming?

CANDIDATE CONTEXT (what you're evaluating):
{CHEATSHEET_DOC[:3000]}

START: Greet them warmly but professionally. You have about 30 minutes. \
This is a director-level conversation, not a recruiter screen. \
Ask your first question naturally. React to their answers with genuine follow-ups. \
Push for specifics when answers are abstract. Pull them back to Gap's reality when they drift."""

BERT_QUICK_SYSTEM = f"""You are Bert Reuler III, Sr. Director of Innovation at Gap Inc.'s Office of AI. \
You're running a rapid-fire round: 5 tough questions, each scored immediately.

GAP CONTEXT: FY2024 $15.1B revenue, 41.3% margin, ~3,500 stores, ~80K employees, \
4 brands, Google Cloud partnership (Gemini/Vertex AI/BigQuery), Office of AI est. 2024, \
shipped: sketch-to-render, Intelligent Fit, trend curations, recs, Chat with Us, \
fulfillment automation (+30%). Internal employee enablement is the gap.

FORMAT:
- Ask one question
- Wait for answer
- Score immediately (1-5 on: specificity, retail relevance, adoption depth, presentation)
- Give 1 sentence of feedback
- Move to next question
- After 5 questions, give overall assessment

Keep it fast. Keep it sharp. No small talk.

QUESTIONS (pick 5, vary the difficulty):
1. "90-day plan. Go."
2. "Culture & People pillar has no shipped AI. Why is that hard?"
3. "Old Navy merchandiser asks 'what should I mark down?' — how does your system answer that?"
4. "We have Google Cloud. Why do I need you?"
5. "A pilot is showing 60% adoption after 6 weeks. Scale or kill?"
6. "Four brands, four cultures. How do you get coherence without uniformity?"
7. "What's the biggest risk in your approach?"
8. "Tell me about a failure. 30 seconds."
9. "Accenture pitched us last week. Why you?"
10. "What's one thing you'd tell me I don't want to hear?"

START: "Let's do rapid fire. Five questions. Keep answers under 90 seconds. I'll score each one. Ready? Here's the first."
"""

ASSISTANT_SYSTEM = f"""You are Palette, a multi-agent AI system and personal assistant. \
You're running as a Telegram bridge — the user is talking to you from their phone.

Be conversational, direct, and useful. You have full context on:
- The Gap Inc. AI strategy role the user is interviewing for with Bert Reuler III
- The user's Kaizen-based AI improvement cycle strategy for Gap
- The user's background: 11 years at Amazon/AWS, built Palette, taxonomy/KM expert

KEY STRATEGY (user's own framework):
- Gap's 4 enduring pillars: Product & Brand, Customer Experience, Operations & Supply Chain, Culture & People
- 5 of 7 shipped AI features are customer-facing e-commerce; Culture & People has zero public delivery
- Kaizen improvement cycle: Observe → Diagnose → Apply → Measure → Share → repeat
- Shared AI experience layer as the long-term output (one front door, common controls, brand-specific outcomes)
- Palette architecture maps directly to the Culture & People gap

THE USER'S KEY STORIES:
- Ask Pathfinder: shared experience layer at AWS, fixed impression bias with parent-child tagging
- QuickSuite / Finance POD: skipped official rollout, found one champion, let pull do the work
- POI Knowledge Graph: built for Alexa, quality created pull, adopted company-wide by delivery org
- Italian Alexa: failing launch → #1 by looking sideways at other locales, became cross-locale playbook
- Diagnostics: research agent using gradient descent + game theory against internal data

Available interview modes:
  /interview bert  — Bert Reuler III, director-level (strategy + execution)
  /interview quick — Rapid-fire: 5 questions, scored immediately
  /feedback        — coaching on your last answer
  /saveanswer      — save last answer to cheat sheet
  /cheatsheet      — pull session summary
  /reset           — end interview

STRATEGY DOC SUMMARY:
{STRATEGY_DOC[:2000]}"""

# ── Live cheat sheet ──────────────────────────────────────────────────────────

_EXTRACT_PROMPT = """\
You are reviewing one exchange from a live Gap Inc. director-level interview practice session.

INTERVIEWER: {question}

CANDIDATE: {answer}

Extract the following. Be concise — this is a cheat sheet, not a report.

Format exactly like this:

**Q: [5-8 word compression of the question]**
**A: [one sentence capturing the core of their answer]**
- [key phrase, framework, or point worth remembering]
- [key phrase, framework, or point worth remembering]
Score: [1-5] — [one word: e.g. Strong / Solid / Thin / Vague / Weak]

Rules:
- Q line: compress to essential context only, no filler
- A line: one tight sentence — the "headline" of what they said
- Bullets: 2-4 max, only the most reusable phrases or moves
- Score 5 = director-ready, 4 = solid, 3 = adequate, 2 = thin, 1 = weak
- If score is 1, output exactly: SKIP"""


def log_exchange(mode: str, turn: int, question: str, answer: str) -> None:
    entry = {
        "ts":       datetime.datetime.now().isoformat(),
        "mode":     mode,
        "turn":     turn,
        "question": question[:600],
        "answer":   answer[:1200],
    }
    try:
        with open(SESSION_LOG, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"[cheatsheet] log error: {e}", flush=True)


def _cheatsheet_worker(question: str, answer: str) -> None:
    try:
        client = anthropic.Anthropic()
        msg = client.messages.create(
            model      = "claude-haiku-4-5-20251001",
            max_tokens = 350,
            messages   = [{"role": "user", "content": _EXTRACT_PROMPT.format(
                question=question[:600], answer=answer[:1200]
            )}],
        )
        text = msg.content[0].text.strip()
        if text.upper() == "SKIP" or not text:
            return
        ts    = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        block = f"\n\n<!-- live: {ts} -->\n{text}\n"
        with open(CHEATSHEET, "a") as f:
            f.write(block)
        print(f"[cheatsheet] appended: {text[:60]}", flush=True)
    except Exception as e:
        print(f"[cheatsheet] worker error: {e}", flush=True)


def update_cheatsheet_async(question: str, answer: str) -> None:
    t = threading.Thread(target=_cheatsheet_worker, args=(question, answer), daemon=True)
    t.start()


# ── Chat state ────────────────────────────────────────────────────────────────

class ChatState:
    def __init__(self):
        self.mode     = "assistant"
        self.history  = []
        self.turn     = 0
        self.last_answer = ""

    def add(self, role: str, content: str) -> None:
        self.history.append({"role": role, "content": content})
        if len(self.history) > MAX_HISTORY:
            self.history = self.history[-MAX_HISTORY:]

    def system_prompt(self) -> str:
        if self.mode == "interview_bert":
            return BERT_SYSTEM
        if self.mode == "interview_quick":
            return BERT_QUICK_SYSTEM
        return ASSISTANT_SYSTEM

    def mode_label(self) -> str:
        if self.mode == "interview_bert":  return "🏢 Bert Reuler III (Sr. Director, Office of AI)"
        if self.mode == "interview_quick": return "⚡ Bert Reuler III (Rapid Fire)"
        return "🎨 Palette Assistant (Gap Prep)"


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
    chunk_size = 4000
    for i in range(0, len(text), chunk_size):
        chunk = text[i : i + chunk_size]
        # Try Markdown first, fall back to plain text if Telegram rejects it
        resp = tg("sendMessage",
                   chat_id    = chat_id,
                   text       = chunk,
                   parse_mode = "Markdown")
        if not resp.get("ok"):
            print(f"[warn] Markdown send failed, retrying plain: {resp.get('description','')[:80]}", flush=True)
            tg("sendMessage", chat_id=chat_id, text=chunk)
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
        print("[gap-bridge] loading whisper model (base)...", flush=True)
        _whisper_model = whisper.load_model("base")
        print("[gap-bridge] whisper ready.", flush=True)
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


# ── Claude ────────────────────────────────────────────────────────────────────

def reply(state: ChatState, user_message: str) -> str:
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
    interviewer = "Bert Reuler III"
    prompt = (
        f"Step out of character for a moment. As {interviewer}, give honest, specific, "
        f"constructive feedback on this answer the candidate just gave:\n\n"
        f"\"{last_answer}\"\n\n"
        f"Score 1-5 on: Specificity, Kaizen clarity, Adoption depth, Evidence discipline, "
        f"Retail relevance, Presentation.\n\n"
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
        "🏢 *Gap Interview Prep is live.*\n\n"
        "Practicing for Bert Reuler III, Sr. Director, Office of AI.\n\n"
        "*Interview modes:*\n"
        "`/interview bert` — Full director-level interview (30 min)\n"
        "`/interview quick` — Rapid fire: 5 questions, scored immediately\n\n"
        "*During the interview:*\n"
        "`/feedback` — honest feedback on your last answer\n"
        "`/saveanswer` — ⭐ save your last answer verbatim\n"
        "`/cheatsheet` — pull a summary of best answers so far\n"
        "`/reset` — end interview, back to assistant\n"
        "`/help` — this menu\n\n"
        "Your answers are saved to your cheat sheet automatically.\n\n"
        "Or just talk — I have your full strategy doc loaded."
    )


def cmd_help(chat_id: int, state: ChatState) -> None:
    send(chat_id,
        f"*Current mode:* {state.mode_label()}\n\n"
        "`/interview bert` — Bert Reuler III (director-level)\n"
        "`/interview quick` — Rapid fire (5 questions, scored)\n"
        "`/feedback` — coaching on your last answer\n"
        "`/saveanswer` — ⭐ save last answer to cheat sheet\n"
        "`/cheatsheet` — pull session summary\n"
        "`/reset` — back to assistant\n"
        "`/help` — this menu"
    )


def cmd_interview(chat_id: int, state: ChatState, who: str) -> None:
    who = who.strip().lower()
    if who == "bert":
        state.mode    = "interview_bert"
        state.history = []
        state.turn    = 0
        send(chat_id, "🏢 *Bert Reuler III mode.*\nSr. Director, Innovation (Office of AI).\nStarting your interview...\n")
        typing(chat_id)
        opening = reply(state, "[The candidate has just joined the MS Teams call.]")
        send(chat_id, opening)
    elif who == "quick":
        state.mode    = "interview_quick"
        state.history = []
        state.turn    = 0
        send(chat_id, "⚡ *Rapid Fire mode.*\n5 questions from Bert. Keep answers under 90 seconds.\n")
        typing(chat_id)
        opening = reply(state, "[The candidate is ready for rapid fire.]")
        send(chat_id, opening)
    else:
        send(chat_id, "Who?\n`/interview bert` — full director-level interview\n`/interview quick` — rapid fire (5 questions)")


def cmd_feedback(chat_id: int, state: ChatState) -> None:
    if state.mode == "assistant":
        send(chat_id, "Not in interview mode. Use `/interview bert` or `/interview quick` first.")
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


def cmd_cheatsheet(chat_id: int, state: ChatState) -> None:
    qa_pairs = []
    h = state.history
    for i in range(len(h) - 1):
        if h[i]["role"] == "assistant" and h[i + 1]["role"] == "user":
            qa_pairs.append(f"Q: {h[i]['content'][:300]}\nA: {h[i+1]['content'][:500]}")

    if not qa_pairs:
        send(chat_id, "No interview answers yet to summarise.")
        return

    typing(chat_id)
    prompt = (
        "Review these interview Q&A pairs from a Gap Inc. director-level practice session.\n"
        "Extract the strongest phrases, frameworks, and talking points, grouped by theme.\n\n"
        + "\n\n---\n".join(qa_pairs[-8:])
    )
    client = anthropic.Anthropic()
    msg = client.messages.create(
        model      = "claude-sonnet-4-6",
        max_tokens = 900,
        messages   = [{"role": "user", "content": prompt}],
    )
    summary = msg.content[0].text.strip()

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(CHEATSHEET, "a") as f:
        f.write(f"\n\n## /cheatsheet pull — {ts}\n{summary}\n")

    send(chat_id, f"📝 *Cheat sheet updated:*\n\n{summary[:3000]}")


def cmd_saveanswer(chat_id: int, state: ChatState) -> None:
    if not state.last_answer:
        send(chat_id, "Answer a question first, then use /saveanswer.")
        return
    question = ""
    h = state.history
    for msg in reversed(h[:-2]):
        if msg["role"] == "assistant":
            question = msg["content"][:300]
            break
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    with open(CHEATSHEET, "a") as f:
        f.write(f"\n\n## ⭐ Saved — {ts}\n**Q:** {question}\n**A:** {state.last_answer}\n")
    send(chat_id, "⭐ Answer saved to cheat sheet.")


# ── Message router ────────────────────────────────────────────────────────────

def handle_message(chat_id: int, text: str) -> None:
    state = get_state(chat_id)
    text  = text.strip()

    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] chat={chat_id} mode={state.mode} | {text[:60]}", flush=True)

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
    if text.startswith("/cheatsheet"):
        cmd_cheatsheet(chat_id, state)
        return
    if text.startswith("/saveanswer"):
        cmd_saveanswer(chat_id, state)
        return

    if state.mode != "assistant":
        state.last_answer = text
        state.turn += 1

    typing(chat_id)
    response = reply(state, text)
    send(chat_id, response)

    if state.mode != "assistant" and state.turn > 0:
        h = state.history
        question = h[-3]["content"] if len(h) >= 3 and h[-3]["role"] == "assistant" else ""
        if question:
            log_exchange(state.mode, state.turn, question, text)
            update_cheatsheet_async(question, text)


# ── Polling loop ──────────────────────────────────────────────────────────────

def run() -> None:
    print(f"[gap-bridge] starting long-poll loop", flush=True)
    print(f"[gap-bridge] bot: {TELEGRAM.split('bot')[1][:8]}...", flush=True)
    print(f"[gap-bridge] strategy doc loaded: {len(STRATEGY_DOC)} chars", flush=True)
    print(f"[gap-bridge] cheatsheet loaded: {len(CHEATSHEET_DOC)} chars", flush=True)

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
            print("\n[gap-bridge] stopped.", flush=True)
            sys.exit(0)
        except Exception as e:
            print(f"[error] unexpected: {e}", flush=True)
            time.sleep(5)


if __name__ == "__main__":
    if not BOT_TOKEN:
        print("ERROR: TELEGRAM_BOT_TOKEN not set")
        print("  export TELEGRAM_BOT_TOKEN='your-token-from-BotFather'")
        sys.exit(1)
    if not ANTHROPIC_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set")
        sys.exit(1)
    run()
