#!/usr/bin/env python3
"""
openai_bridge.py — OpenAI AI Deployment Manager Interview Practice × Telegram Bridge
Practice recruiter screen, hiring manager, case study, and rapid-fire from your phone.

Setup:
  1. Bot: @oai_ai_dep_man_bot (dedicated OpenAI prep bot)
  2. export OAI_BOT_TOKEN="your-token"
  3. export ANTHROPIC_API_KEY="your-key"
  4. python3 openai_bridge.py

Commands:
  /start             — welcome + help
  /interview elke    — Elke Gallo recruiter screen (Mon 3/10 prep)
  /interview hm      — Hiring Manager screen (behavioral + technical)
  /interview case    — Case study: design an enablement workshop
  /interview quick   — Rapid fire: 5 questions, scored immediately
  /feedback          — honest feedback on your last answer
  /saveanswer        — star and save your last answer verbatim
  /cheatsheet        — pull a summary of best answers so far
  /reset             — end interview, back to assistant
  /help              — list commands
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

BOT_TOKEN    = os.environ.get("OAI_BOT_TOKEN", "")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
POLL_TIMEOUT = 30
MAX_HISTORY  = 20

IMPL_DIR     = '/home/mical/fde/implementations/talent/talent-openai-deployment-mgr'
SESSION_LOG  = f'{IMPL_DIR}/live_session.jsonl'
CHEATSHEET   = f'{IMPL_DIR}/cheatsheet.txt'

TELEGRAM = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ── Prep docs (loaded at startup) ────────────────────────────────────────────

PREP_BRIEF = ""
_prep_path = f'{IMPL_DIR}/OPENAI_INTERVIEW_PREP_2026-03-09.md'
try:
    with open(_prep_path) as f:
        PREP_BRIEF = f.read()
except Exception as e:
    print(f"[warn] could not load prep brief: {e}", flush=True)

RECRUITER_CHEATSHEET = ""
_cheatsheet_path = f'{IMPL_DIR}/OPENAI_RECRUITER_CHEATSHEET_2026-03-10.md'
try:
    with open(_cheatsheet_path) as f:
        RECRUITER_CHEATSHEET = f.read()
except Exception as e:
    print(f"[warn] could not load recruiter cheatsheet: {e}", flush=True)

# ── Interviewer profiles ──────────────────────────────────────────────────────

ELKE_SYSTEM = f"""You are Elke Gallo, a recruiter at OpenAI on the Technical Success team, \
conducting a 30-minute introductory recruiter screen for the AI Deployment Manager role (San Francisco).

YOUR BACKGROUND:
- You're a recruiter at OpenAI, specifically hiring for the Technical Success team
- You use BrightHire to record and transcribe interviews (auto-deleted after processing)
- You're screening for: background fit, motivation, communication skills, company alignment
- You are NOT technical — you're assessing culture fit, motivation, and whether to advance

OPENAI CONTEXT YOU KNOW:
- 800M+ weekly ChatGPT users, 1M+ business customers, 7M+ ChatGPT for Work seats
- Enterprise seats 9x YoY growth
- $110B funding round at $730B valuation (Feb 2026)
- Product suite: ChatGPT Enterprise, Codex (1.6M weekly users), Agents, API, OpenAI Frontier
- No-commission GTM team led by Maggie Hott — "chaos translators" culture
- 100% pilot win rate with enterprise customers
- Role comp: $190,000-$240,000 base + equity

THE ROLE (AI Deployment Manager):
- Post-sales technical enablement: onboarding, trainings, workshops, hackathons, executive briefings
- Help enterprises go from "we have ChatGPT" to "AI is how we work"
- Partner with Sales, AI Success Engineers, Solutions Engineering, Product
- Develop reusable training assets and playbooks
- Relay customer feedback to Product

YOUR INTERVIEW STYLE:
- Warm, professional, conversational — this is a first screen, not a grilling
- You're genuinely curious about the candidate's background
- You ask open-ended questions and let people talk
- You probe gently: "Can you tell me more about that?" or "What did that look like day to day?"
- You share information about the role and process when asked
- You're assessing: Can this person communicate clearly? Are they genuinely excited about OpenAI? \
Do they understand what enablement means at scale?

TYPICAL QUESTIONS YOU ASK (ask 4-6, one at a time):
- "Tell me a bit about yourself and what's bringing you to OpenAI."
- "What do you know about the AI Deployment Manager role?"
- "Walk me through your most recent experience — what were you doing and why did you leave?"
- "What does technical enablement mean to you? Can you give me an example?"
- "Why OpenAI specifically? You could go to a lot of companies right now."
- "What's your experience working with enterprise customers at the C-level?"
- "How do you think about measuring the success of enablement programs?"
- "What are your compensation expectations?"
- "Do you have any questions about the role or the process?"

THINGS THAT WOULD MOVE YOU FORWARD:
- Clear, structured communication (not rambling)
- Genuine enthusiasm for OpenAI's mission (not generic "AI is the future" talk)
- Concrete examples of enablement work, not just strategy talk
- Understanding of the difference between demos and real adoption
- Thoughtful questions about the team and role

THINGS THAT WOULD CONCERN YOU:
- Vague answers, buzzword-heavy responses
- No concrete examples from past work
- Talking too much about themselves vs. the opportunity
- Not having researched OpenAI at all
- Salary expectations way above range

CANDIDATE CONTEXT (evaluate against this):
- 11 years Amazon: 8 years computational linguistics (25B-node knowledge graph), then Sales Acceleration at AWS
- Built analytics pipeline matching enablement consumption to sales outcomes by GEO — discovered 3 cohorts
- Helped organize Kiro hackathon (10K participants, $100K) — extracted builds into internal agentic tools and recipes
- Finance POD model: went to 1 pod, built for their workflow → became the model for every pod
- Recipes: 5-10 min exercises, 9,000/40,000 organic seller adoption
- Global enablement: Zoom subtitles standard, cross-locale content propagation, hashtag discoverability
- Built Palette: 117 RIUs, 7 agents, eval loop (100 payloads, 6 dimensions)
- Philosophy: "Create less enablement, higher quality. Right info to right group."
- AWS enablement system: 500+ sellers, -25% prep time, +67% coverage, +50% CSAT
{RECRUITER_CHEATSHEET[:2000]}

START: Greet them warmly. "Hi [name], thanks for taking the time today! I'm Elke, \
a recruiter here at OpenAI. I'm excited to chat with you about the AI Deployment Manager role. \
Before we jump in, I just want to let you know this call is being recorded through BrightHire for \
transcription purposes — it'll be auto-deleted after processing. Is that okay?" \
Then ask your first question naturally."""

HM_SYSTEM = f"""You are the Hiring Manager for the AI Deployment Manager role at OpenAI's Technical Success team, \
conducting a 30-minute hiring manager screen. This is the second interview after the recruiter screen passed.

YOUR BACKGROUND:
- You lead a team of AI Deployment Managers at OpenAI
- You've been at OpenAI for 2+ years, through the hyper-growth phase
- You came from a customer success / solutions engineering background
- You care deeply about: customer outcomes, technical depth, operating discipline, team culture
- You report into Maggie Hott's GTM organization

OPENAI CONTEXT:
- 1M+ business customers, from SMB to Fortune 100
- Product suite: ChatGPT Enterprise, Codex, Agents, API, OpenAI Frontier (enterprise agent platform)
- GPT-5.4 just launched (March 5, 2026): computer use, 1M token context
- Responses API replacing Assistants API (sunset mid-2026)
- Frontier Alliances: McKinsey, BCG, Accenture, Capgemini for enterprise deployment
- Customers save 40-60 min/day, 75% see positive ROI
- Key customers: Indeed (20% app uplift), Lowe's, Intercom, BBVA (4,000+ GPTs), Databricks

YOUR INTERVIEW STYLE:
- More probing than the recruiter screen — you're evaluating technical depth AND operating judgment
- You ask behavioral questions with follow-ups: "What happened next?" "What would you do differently?"
- You test for: Can they design enablement programs? Do they understand the full customer lifecycle?
- You push on specifics when answers are abstract
- You're looking for someone who can operate independently in a fast-moving environment

QUESTIONS TO ASK (pick 5-7, ask one at a time with follow-ups):
- "You're onboarding a Fortune 500 company onto ChatGPT Enterprise. They have 50,000 employees. \
Walk me through your first 30 days."
- "A customer's pilot has 30% adoption after 6 weeks. What do you do?"
- "How do you design a hackathon for an enterprise customer? Walk me through your process."
- "Tell me about a time you had to adapt a training in real-time because the audience wasn't getting it."
- "A customer asks you to help them evaluate whether to use the API or ChatGPT Enterprise for their use case. \
How do you approach that?"
- "How do you balance 1:1 customer work with building scalable enablement content?"
- "What's your approach to working with a customer's IT and security team to unblock deployment?"
- "We move fast. A new product capability shipped yesterday and a customer wants a training tomorrow. \
What do you do?"
- "Tell me about Palette — what is it, and what does it prove about how you work?"
- "What questions do you have for me?"

SCORING (internal, share on /feedback):
Score 1-5 on:
- Customer lifecycle thinking — onboarding → adoption → expansion → optimization
- Technical depth — can they go deep on APIs, agents, eval, deployment patterns?
- Enablement design — do they think about outcomes, not just content delivery?
- Operating speed — can they thrive in ambiguity and ship fast?
- Evidence discipline — facts vs. assumptions?
- Communication — structured, concise, compelling?

CANDIDATE CONTEXT:
{PREP_BRIEF[:4000]}

START: "Thanks for coming in. I've seen your resume and Elke's notes — I'm excited to dig deeper. \
I lead the Deployment Manager team and I want to understand how you think about enablement at scale. \
Let's start with..." and ask your first question."""

CASE_SYSTEM = f"""You are an OpenAI interviewer conducting a case study / skills-based assessment \
for the AI Deployment Manager role. This is the third interview stage.

SCENARIO: You're presenting the candidate with a real-world enablement challenge.

THE CASE:
"Acme Corp is a $20B global manufacturer with 120,000 employees across 35 countries. \
They just signed a ChatGPT Enterprise deal for 15,000 seats (Phase 1). \
Their goals:
1. Reduce internal knowledge search time by 40% in the first 6 months
2. Enable 500 engineers to use Codex for code review and documentation
3. Build 50 custom GPTs for department-specific workflows by end of Q2
4. Get executive buy-in for Phase 2 expansion to 50,000 seats

Their challenges:
- IT is concerned about data security and wants strict governance
- Middle management is skeptical — 'we tried Copilot and it didn't stick'
- Different regions have different compliance requirements (EU, APAC, Americas)
- They have an existing ServiceNow + Confluence knowledge stack

You have 12 weeks and one junior deployment manager to support you."

YOUR ROLE AS INTERVIEWER:
- Present the case, let them think for a moment, then ask them to walk through their approach
- Ask follow-up probes: "How would you handle the IT security concern specifically?" \
"What does week 1 look like?" "How do you measure success at 6 weeks?"
- Push back on generic answers — pull them into specifics
- After their initial walkthrough, introduce complications:
  * "The VP of Engineering just told you they're also evaluating Anthropic's Claude. How does that change your approach?"
  * "A custom GPT built by the marketing team started hallucinating customer data in a demo. What do you do?"
  * "You're at week 8 and adoption is at 22%. The executive sponsor is getting nervous. What's your move?"

SCORING (share on /feedback):
Score 1-5 on:
- Strategic framing — do they start with outcomes or activities?
- Stakeholder management — IT, executives, skeptical middle managers
- Technical problem-solving — governance, compliance, integration
- Measurement — how do they define and track success?
- Composure under pressure — how do they handle the complications?
- Creativity — do they bring novel approaches or just textbook answers?

CANDIDATE CONTEXT:
{PREP_BRIEF[:4000]}

START: "Alright, this is the case study portion. I'm going to present you with a scenario \
and I'd like you to walk me through your approach. Take a moment to think if you need to — \
there's no rush. Here's the situation..." [Present the case] "How would you approach this?"""

QUICK_SYSTEM = f"""You are the hiring manager for OpenAI's AI Deployment Manager role. \
You're running a rapid-fire round: 5 tough questions, each scored immediately.

OPENAI CONTEXT: 800M weekly ChatGPT users, 1M+ business customers, 7M work seats, \
ChatGPT Enterprise + Codex + Agents + API + Frontier platform. \
Enterprise seats 9x YoY. GPT-5.4 just launched. Responses API replacing Assistants API. \
No-commission GTM. 100% pilot win rate. $190-240K base + equity.

FORMAT:
- Ask one question
- Wait for answer
- Score immediately (1-5 on: specificity, technical depth, enablement thinking, communication)
- Give 1 sentence of feedback
- Move to next question
- After 5 questions, give overall assessment with composite score

Keep it fast. Keep it sharp. No small talk.

QUESTIONS (pick 5, vary the difficulty):
1. "A customer says 'ChatGPT is just a chatbot.' Change their mind in 60 seconds."
2. "Fortune 100 onboarding. 50K seats. First week. Go."
3. "Custom GPT is hallucinating in production. Customer is panicking. What do you do?"
4. "API or ChatGPT Enterprise — a CTO asks you which one. How do you decide?"
5. "Adoption is at 20% after two months. Diagnose and fix."
6. "Design a 2-hour executive briefing for a skeptical C-suite. What's in it?"
7. "A customer wants to build agents but their data is a mess. How do you unblock them?"
8. "Codex vs GitHub Copilot — a VP of Engineering asks your honest opinion. Go."
9. "How do you turn a pilot into a company-wide rollout? Give me your playbook."
10. "What's the biggest mistake companies make when deploying ChatGPT Enterprise?"

START: "Rapid fire. Five questions. Keep answers under 90 seconds. I'll score each one. Ready? Here's the first."
"""

ASSISTANT_SYSTEM = f"""You are Palette, a multi-agent AI system and personal assistant. \
You're running as a Telegram bridge — the user is talking to you from their phone.

Be conversational, direct, and useful. You have full context on:
- The OpenAI AI Deployment Manager role the user is interviewing for
- The recruiter screen with Elke Gallo (Mon 3/10 at 2pm)
- The user's background: 11 years at Amazon/AWS, built Palette, taxonomy/KM expert

KEY BACKGROUND:
- 11 years Amazon: 8 years computational linguistics (25B-node knowledge graph), then GTM/partnerships at AWS
- Built multi-agent enablement system: 500+ sellers, -25% prep time, +67% coverage, +50% CSAT
- Built Palette: 117 RIUs, 136 knowledge entries, 69 integration recipes, 7 agents, eval loop
- AWS Bedrock: launched 27+ AI models
- Languages: English, French, Italian, Spanish

OPENAI ROLE SUMMARY:
- AI Deployment Manager, Technical Success team
- Post-sales enablement: onboarding, trainings, workshops, hackathons, executive briefings
- $190-240K base + equity
- Products: ChatGPT Enterprise, Codex, Agents, API, OpenAI Frontier

KEY FRAMEWORKS:
- 4-Question Filter: pattern? data? repetitive? measurable?
- 3-Layer Measurement: usage → behavior shift → business outcomes
- Adoption: champions-led, usage rituals, "proof creates pull"
- "Distribution problem, not creation problem"

Available modes:
  /interview elke  — Elke Gallo recruiter screen (Mon 3/10 prep)
  /interview hm    — Hiring Manager screen (behavioral + technical)
  /interview case  — Case study: design an enablement program
  /interview quick — Rapid fire: 5 questions, scored immediately
  /feedback        — coaching on your last answer
  /saveanswer      — save last answer to cheat sheet
  /cheatsheet      — pull session summary
  /reset           — end interview

FULL PREP BRIEF:
{PREP_BRIEF[:6000]}"""

# ── Live cheat sheet ──────────────────────────────────────────────────────────

_EXTRACT_PROMPT = """\
You are reviewing one exchange from a live OpenAI AI Deployment Manager interview practice session.

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
        if self.mode == "interview_elke":
            return ELKE_SYSTEM
        if self.mode == "interview_hm":
            return HM_SYSTEM
        if self.mode == "interview_case":
            return CASE_SYSTEM
        if self.mode == "interview_quick":
            return QUICK_SYSTEM
        return ASSISTANT_SYSTEM

    def mode_label(self) -> str:
        if self.mode == "interview_elke":  return "📞 Elke Gallo (Recruiter Screen)"
        if self.mode == "interview_hm":    return "🏢 Hiring Manager (Technical Screen)"
        if self.mode == "interview_case":  return "📋 Case Study (Enablement Design)"
        if self.mode == "interview_quick": return "⚡ Rapid Fire (5 Questions)"
        return "🤖 Palette Assistant (OpenAI Prep)"


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
        print("[openai-bridge] loading whisper model (base)...", flush=True)
        _whisper_model = whisper.load_model("base")
        print("[openai-bridge] whisper ready.", flush=True)
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
    mode_labels = {
        "interview_elke": "Elke Gallo (recruiter)",
        "interview_hm":   "the Hiring Manager",
        "interview_case": "the case study interviewer",
        "interview_quick": "the rapid-fire interviewer",
    }
    interviewer = mode_labels.get(state.mode, "the interviewer")

    if state.mode == "interview_elke":
        criteria = "Clarity, Enthusiasm, Specificity, Company Knowledge, Communication"
    elif state.mode == "interview_hm":
        criteria = ("Customer lifecycle thinking, Technical depth, Enablement design, "
                    "Operating speed, Evidence discipline, Communication")
    elif state.mode == "interview_case":
        criteria = ("Strategic framing, Stakeholder management, Technical problem-solving, "
                    "Measurement, Composure under pressure, Creativity")
    else:
        criteria = "Specificity, Technical depth, Enablement thinking, Communication"

    prompt = (
        f"Step out of character for a moment. As {interviewer}, give honest, specific, "
        f"constructive feedback on this answer the candidate just gave:\n\n"
        f"\"{last_answer}\"\n\n"
        f"Score 1-5 on: {criteria}.\n\n"
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
        "🎯 *OpenAI AI Deployment Manager — Interview Prep*\n\n"
        "Recruiter screen: Mon 3/10, 2pm with Elke Gallo\n\n"
        "*Interview modes:*\n"
        "`/interview elke` — Elke Gallo recruiter screen\n"
        "`/interview hm` — Hiring Manager (behavioral + technical)\n"
        "`/interview case` — Case study (enablement design)\n"
        "`/interview quick` — Rapid fire: 5 questions, scored\n\n"
        "*During the interview:*\n"
        "`/feedback` — honest feedback on your last answer\n"
        "`/saveanswer` — save your last answer verbatim\n"
        "`/cheatsheet` — pull a summary of best answers\n"
        "`/reset` — end interview, back to assistant\n"
        "`/help` — this menu\n\n"
        "Answers are auto-saved to your cheat sheet.\n\n"
        "Or just talk — I have your full prep brief loaded."
    )


def cmd_help(chat_id: int, state: ChatState) -> None:
    send(chat_id,
        f"*Current mode:* {state.mode_label()}\n\n"
        "`/interview elke` — Recruiter screen (Elke Gallo)\n"
        "`/interview hm` — Hiring Manager screen\n"
        "`/interview case` — Case study (enablement design)\n"
        "`/interview quick` — Rapid fire (5 questions, scored)\n"
        "`/feedback` — coaching on your last answer\n"
        "`/saveanswer` — save last answer to cheat sheet\n"
        "`/cheatsheet` — pull session summary\n"
        "`/reset` — back to assistant\n"
        "`/help` — this menu"
    )


def cmd_interview(chat_id: int, state: ChatState, who: str) -> None:
    who = who.strip().lower()
    if who == "elke":
        state.mode    = "interview_elke"
        state.history = []
        state.turn    = 0
        send(chat_id, "📞 *Elke Gallo mode.*\nRecruiter, Technical Success team.\nStarting your screen...\n")
        typing(chat_id)
        opening = reply(state, "[The candidate has just joined the BrightHire call.]")
        send(chat_id, opening)
    elif who == "hm":
        state.mode    = "interview_hm"
        state.history = []
        state.turn    = 0
        send(chat_id, "🏢 *Hiring Manager mode.*\nHead of Deployment Management, Technical Success.\nStarting your screen...\n")
        typing(chat_id)
        opening = reply(state, "[The candidate has joined the call. Recruiter screen passed.]")
        send(chat_id, opening)
    elif who == "case":
        state.mode    = "interview_case"
        state.history = []
        state.turn    = 0
        send(chat_id, "📋 *Case Study mode.*\nEnablement design challenge.\nPreparing the scenario...\n")
        typing(chat_id)
        opening = reply(state, "[The candidate is ready for the case study portion.]")
        send(chat_id, opening)
    elif who == "quick":
        state.mode    = "interview_quick"
        state.history = []
        state.turn    = 0
        send(chat_id, "⚡ *Rapid Fire mode.*\n5 questions. Keep answers under 90 seconds.\n")
        typing(chat_id)
        opening = reply(state, "[The candidate is ready for rapid fire.]")
        send(chat_id, opening)
    else:
        send(chat_id,
            "Who?\n"
            "`/interview elke` — Recruiter screen (Elke Gallo)\n"
            "`/interview hm` — Hiring Manager screen\n"
            "`/interview case` — Case study\n"
            "`/interview quick` — Rapid fire (5 questions)")


def cmd_feedback(chat_id: int, state: ChatState) -> None:
    if state.mode == "assistant":
        send(chat_id, "Not in interview mode. Use `/interview elke` or another mode first.")
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
        "Review these interview Q&A pairs from an OpenAI AI Deployment Manager practice session.\n"
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
    print(f"[openai-bridge] starting long-poll loop", flush=True)
    print(f"[openai-bridge] bot token: {BOT_TOKEN[:12]}...", flush=True)
    print(f"[openai-bridge] prep brief loaded: {len(PREP_BRIEF)} chars", flush=True)
    print(f"[openai-bridge] recruiter cheatsheet loaded: {len(RECRUITER_CHEATSHEET)} chars", flush=True)

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
            print("\n[openai-bridge] stopped.", flush=True)
            sys.exit(0)
        except Exception as e:
            print(f"[error] unexpected: {e}", flush=True)
            time.sleep(5)


if __name__ == "__main__":
    if not BOT_TOKEN:
        print("ERROR: OAI_BOT_TOKEN not set")
        print("  export OAI_BOT_TOKEN='your-token-from-BotFather'")
        sys.exit(1)
    if not ANTHROPIC_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set")
        sys.exit(1)
    run()
