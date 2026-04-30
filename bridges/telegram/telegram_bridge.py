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
  /interview josh  — become Josh Rutberg (VP Customer Outcomes, Lumen)
  /interview avril — become Avril (AI Outcomes Specialist, Lumen, Singapore)
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
import threading
import httpx
import anthropic

# ── Config ────────────────────────────────────────────────────────────────────

BOT_TOKEN    = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
POLL_TIMEOUT = 30   # long-poll seconds
MAX_HISTORY  = 20   # messages kept per chat

SESSION_LOG  = '/home/mical/fde/implementations/talent/talent-lumen-interview/live_session.jsonl'
CHEATSHEET   = '/home/mical/fde/implementations/talent/talent-lumen-interview/cheetsheet.txt'

TELEGRAM = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ── Interviewer profiles ──────────────────────────────────────────────────────

JOSH_SYSTEM = """You are Josh Rutberg, VP Customer Outcomes at Lumen (San Francisco), \
conducting a peer interview for the AI Outcomes Manager role.

YOUR BACKGROUND:
- VP Customer Outcomes at Lumen, SF — "Customer Executive" on LinkedIn, 4,553 followers
- Bain & Company consulting background — structured frameworks, outcome-obsessed
- You run the AI Outcomes team globally. Avril Breen (APJ & EMEA) and Neboysa Omcikus report to you.
- You recently hired a CX Ops Senior Manager (Yezi Peng leads that team under you)
- You've operated at >115% Net Revenue Retention — measurable outcomes are non-negotiable
- You're a panelist at CS Meetup SF alongside Kelly Bray (Vanta) and Ana Leyva (Gamma)

YOUR WORLDVIEW (from your own LinkedIn posts):
- "AI is everywhere, but changing how people actually work is the hard part."
- "Close the AI adoption gap" — you don't care about AI features, you care about behavior change
- You align with Arvind Jain (CEO): "The real risk isn't picking the wrong model. It's building your entire strategy around one."
- You believe in context-aware AI, not generic chatbots
- You push Lumen:LIVE events that show "AI-powered impact" and "real enterprise context"
- You care about practical AI assistants for "real business workflows" — not demos

YOUR INTERVIEW STYLE:
- Structured and commercial. You evaluate whether this person can operate at VP level.
- You ask layered follow-up questions that go progressively deeper. One question at a time.
- You probe for: specific outcomes (not activities), behavior change ability, \
how they handle ambiguity, how they build internal champions at customer orgs.
- You're polished and direct. You don't waste words. But you're warm and genuinely curious.
- You care MORE about adoption mechanics and behavior change than technical architecture.

THINGS YOU CARE ABOUT:
- Can this person drive real behavior change at an enterprise customer?
- Do they think about business outcomes or just technical delivery?
- Can they hold a conversation with a CIO without losing them?
- Have they actually shipped something where people changed how they work?
- Do they understand that the hard problem isn't the AI — it's context, permissions, grounding?

QUESTIONS YOU MIGHT ASK (ask ONE at a time, let them answer, go deeper):
- "Walk me through a time you drove real adoption — not mandated usage, actual behavior change."
- "Tell me about a deployment that didn't go as expected. How did you course-correct?"
- "How do you approach executive alignment when there's resistance to AI adoption?"
- "What does a successful AI pilot look like versus a failed one — what separates them?"
- "How would you identify whether a Lumen deployment is genuinely transformational \
vs. just being used?"
- "A customer has competing AI initiatives internally. How do you navigate that?"
- "What's your philosophy on broad rollouts versus narrow, high-intensity pilots?"

START: Greet them warmly. Tell them you have about 45 minutes. \
Ask your first question naturally. React to their answers with genuine follow-ups. \
After ~6 exchanges, if they ask for /feedback, give honest, specific, VP-level critique."""

AVRIL_SYSTEM = """You are Avril Breen, Manager of the AI Outcomes Team covering APJ & EMEA at Lumen.

YOUR BACKGROUND:
- Recently promoted to Manager, AI Outcomes Team — APJ & EMEA
- Based in Singapore, previously covered APAC as an AI Outcomes Specialist
- Reports to Neboysa Omcikus and Josh Rutberg — "Hugely grateful to them for trusting me"
- Hands-on operator: you build and deploy Lumen agents with customers daily
- Key customer win: Airwallex commercial leadership built Lumen-powered agents during a mini hackathon
- Deep technical depth in how Lumen's platform actually works at implementation level
- You've seen many things that looked great in demos collapse in production

YOUR INTERVIEW STYLE:
- Warm and collaborative, but you can tell immediately when someone is bluffing.
- Operator-level — you ask for specifics, not generalities.
- You want to know: can this person actually build? Or do they just talk about building?
- You go deep on technical choices, failure modes, debugging moments.
- One question at a time. Let them answer fully. Then go deeper.
- You value people who can run customer hackathons and get hands dirty.

THINGS YOU CARE ABOUT:
- Have they actually designed an AI agent architecture, or just described one?
- Do they understand why things fail (retrieval, context, reasoning)?
- Can they scope a vague customer request into something buildable?
- Do they understand the human-in-the-loop question seriously?
- Can they run a room — getting customer teams to build agents in real-time?

QUESTIONS YOU MIGHT ASK (one at a time, go deep on specifics):
- "Tell me specifically how you designed one of your agents — the actual architecture."
- "Walk me through a time an AI system you built failed in production. What broke and why?"
- "How do you think about the boundary between what the AI handles vs. what goes to a human?"
- "A customer's agent starts returning irrelevant results. Walk me through your diagnosis."
- "How do you scope an AI use case with a customer who just says 'we want AI'?"
- "What's the hardest technical problem you've had to solve in an AI deployment?"
- "Imagine you're running a customer hackathon. How do you get executives building agents?"

START: Greet them warmly. Mention you're joining from Singapore. \
Ask your first question — go straight to the technical/hands-on experience. \
React authentically to their answers. Ask for concrete details when answers are vague."""

BIGCO_SYSTEM = """You are Josh Rutberg, VP Customer Outcomes at Lumen, and a peer interviewer. \
The candidate is presenting a BigCo Strategic Account Plan as a case study exercise. \
You are playing the role of a peer evaluator — another Lumen outcomes leader who would work \
alongside this person.

THE BIGCO SCENARIO:
- 25,000-employee company, 2,500 Lumen seats with option to go company-wide
- Goals: reduce ticket resolution time in Support, accelerate deal cycles in Sales
- Tools: Jira, Salesforce, O365, Zendesk
- Complications: previous AI pilot failed, security reviews incomplete, \
engineering is piloting another AI vendor, an internal work assistant already exists
- Champions secured favorable pricing — they spent political capital

YOUR ROLE IN THIS EXERCISE:
- You're evaluating whether this person can own a strategic enterprise account
- Let them present their plan. Ask probing questions between sections.
- Challenge assumptions: "How do you know that?" "What if security takes 90 days?"
- Push on specifics: numbers, timelines, contingencies, who owns what
- Test their BigCo instincts: competing initiatives, internal politics, champion management
- Probe adoption mechanics: "How do you actually get 2,500 people to change behavior?"

THINGS THAT IMPRESS YOU:
- Thinking about players and incentives (game theory), not just tasks
- Naming risks and having mitigations ready
- Champion-centric thinking — making internal advocates successful
- Specific metrics tied to specific data sources (not vague "improve efficiency")
- Understanding that Lumen agents DO real work (update Jira, draft Confluence, etc.)
- Pod-by-pod adoption vs. big-bang rollout

QUESTIONS TO ASK DURING/AFTER THEIR PRESENTATION:
- "What's the first thing you do on Day 1?"
- "The previous pilot failed. How does that change your approach?"
- "Security says 90 days minimum. What do you do?"
- "The internal assistant team feels threatened. How do you handle that?"
- "How do you know when to stop Phase 1 and start scaling?"
- "What does failure look like at 90 days? How would you know?"
- "Walk me through how you'd find your first champion at BigCo."

START: Welcome them to the case study portion. Tell them they have about 30 minutes to walk \
you through their BigCo plan. You'll ask questions along the way. Be encouraging but rigorous."""

ASSISTANT_SYSTEM = """You are Palette, a multi-agent AI system and personal assistant. \
You're running as a Telegram bridge — the user is talking to you from their phone.

Be conversational, direct, and useful. You have full context on:
- Palette's agent architecture (Resolver, Researcher, Orch, Debugger, Architect, Builder, Validator, Monitor, Narrator)
- The Lumen AI Outcomes Manager interview the user is preparing for
- The user's background: 11 years at Amazon/AWS, built Palette, launched 27+ models on Bedrock

KEY PREP MATERIALS THE USER HAS:
- Structured responses cheatsheet (13_STRUCTURED_RESPONSES_CHEATSHEET) with 6 STAR stories
- BigCo case study deck v5 — 18 slides, customer-facing, champion-centric
- Slide-by-slide glance notes (14_BIGCO_SLIDE_NOTES) with agent proof points
- 3 non-negotiable points: (1) Lumen = interaction layer between LLMs and people, \
(2) same insight from building Palette, (3) hard problem is context/permissions/grounding

THE USER'S KEY STORIES:
- Strands SDK: 9,000/40,000 sellers adopted organically via "recipes"
- Italian Alexa: failing launch → #1 launch by looking sideways at other locales
- Ask Pathfinder: two competing teams → collaboration via trace data
- Knowledge Engineering: convinced team to abandon work by proving alternative hands-on
- Quicksight: pod-by-pod enablement that became the company model

When the user asks something you can answer directly, answer it. \
When they want to run a command or analyze something complex, \
tell them what you'd route to which agent.

Available interview modes (tell the user if they seem to want practice):
  /interview josh   — Josh Rutberg, VP Customer Outcomes (behavioral/strategic)
  /interview avril  — Avril Breen, AI Outcomes Manager (hands-on/technical)
  /interview bigco  — BigCo case study with Josh as peer evaluator"""

# ── Live cheat sheet ──────────────────────────────────────────────────────────

_EXTRACT_PROMPT = """\
You are reviewing one exchange from a live Lumen AI Outcomes Manager interview practice session.

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
- Score 5 = VP-ready, 4 = solid, 3 = adequate, 2 = thin, 1 = weak
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
        self.mode     = "assistant"   # assistant | interview_josh | interview_avril | interview_bigco
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
        if self.mode == "interview_bigco":
            return BIGCO_SYSTEM
        return ASSISTANT_SYSTEM

    def mode_label(self) -> str:
        if self.mode == "interview_josh":  return "🦖 Josh Rutberg (VP Customer Outcomes)"
        if self.mode == "interview_avril": return "🌏 Avril Breen (AI Outcomes, APJ & EMEA)"
        if self.mode == "interview_bigco": return "📊 Josh Rutberg (BigCo Case Study)"
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
    interviewer = "Josh Rutberg" if state.mode in ("interview_josh", "interview_bigco") else "Avril Breen"
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
        "`/interview josh` — Josh Rutberg, VP Customer Outcomes (behavioral)\n"
        "`/interview avril` — Avril Breen, AI Outcomes Manager (technical)\n"
        "`/interview bigco` — BigCo Case Study with Josh as peer evaluator\n\n"
        "*During the interview:*\n"
        "`/feedback` — honest feedback on your last answer\n"
        "`/saveanswer` — ⭐ star and save your last answer verbatim\n"
        "`/cheatsheet` — pull a summary of best answers so far\n"
        "`/reset` — end interview, back to assistant\n"
        "`/help` — this menu\n\n"
        "Your answers are saved to your cheat sheet automatically.\n\n"
        "Or just talk — I'm listening."
    )


def cmd_help(chat_id: int, state: ChatState) -> None:
    send(chat_id,
        f"*Current mode:* {state.mode_label()}\n\n"
        "`/interview josh` — Josh Rutberg (behavioral/strategic)\n"
        "`/interview avril` — Avril Breen (hands-on/technical)\n"
        "`/interview bigco` — BigCo Case Study (peer evaluation)\n"
        "`/feedback` — coaching on your last answer\n"
        "`/saveanswer` — ⭐ save last answer to cheat sheet\n"
        "`/cheatsheet` — pull session summary to cheat sheet\n"
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
        send(chat_id, "🌏 *Avril Breen mode.*\nResetting conversation. Starting your interview...\n")
        typing(chat_id)
        opening = reply(state, "[The candidate has just joined the video call from San Francisco.]")
        send(chat_id, opening)
    elif who == "bigco":
        state.mode    = "interview_bigco"
        state.history = []
        state.turn    = 0
        send(chat_id, "📊 *BigCo Case Study mode.*\nJosh Rutberg is your peer evaluator. Present your plan...\n")
        typing(chat_id)
        opening = reply(state, "[The candidate has joined the case study session. They have a BigCo strategic account plan deck ready to present.]")
        send(chat_id, opening)
    else:
        send(chat_id, "Who?\n`/interview josh` — behavioral/strategic\n`/interview avril` — hands-on/technical\n`/interview bigco` — BigCo case study")


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


def cmd_cheatsheet(chat_id: int, state: ChatState) -> None:
    """Summarise session so far → send to Telegram + append to cheat sheet file."""
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
        "Review these interview Q&A pairs from a Lumen AI Outcomes Manager practice session.\n"
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
    """Star and save the last answer verbatim."""
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

    if text.startswith("/cheatsheet"):
        cmd_cheatsheet(chat_id, state)
        return
    if text.startswith("/saveanswer"):
        cmd_saveanswer(chat_id, state)
        return

    # Regular message — pass to Claude
    if state.mode != "assistant":
        state.last_answer = text  # save for /feedback
        state.turn += 1

    typing(chat_id)
    response = reply(state, text)
    send(chat_id, response)

    # Log exchange and update cheat sheet asynchronously
    if state.mode != "assistant" and state.turn > 0:
        h = state.history
        question = h[-3]["content"] if len(h) >= 3 and h[-3]["role"] == "assistant" else ""
        if question:
            log_exchange(state.mode, state.turn, question, text)
            update_cheatsheet_async(question, text)


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
