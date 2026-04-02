# Oka Build Brief — For Codex

## What This Is
You and Claude are both building independent implementations of Oka — a voice-first learning companion for an 8-year-old girl named Nora who has dyslexia. This is a competing-specs convergence exercise. Build your best version. We'll merge the best of both.

## Context Files (read these)
- **Convergence brief**: `/home/mical/fde/implementations/education/adaptive-learning-architecture/nora/NORA_OKA_CONVERGENCE_BRIEF.md` — Full design doc. Everything about who Oka is, who Nora is, how sessions work, emotional guardrails, voice guidelines, success criteria.
- **Intake answers**: `/home/mical/fde/implementations/education/adaptive-learning-architecture/nora/NORA_INTAKE_ANSWERS.md` — Nora's actual words from her 40-question intake interview.
- **System prompt**: `/home/mical/fde/palette/mission-canvas/oka_system_prompt.md` — Claude's version of the LLM system prompt. Build your own if you prefer.
- **Exercise protocols**: `/home/mical/fde/implementations/education/adaptive-learning-architecture/aron/ARON_EXERCISE_PROTOCOLS.md` — A→B→A session structure and exercise library.
- **Learning lens**: `/home/mical/fde/implementations/education/adaptive-learning-architecture/nora/NORA_LEARNING_LENS.md` — Full cognitive/academic profile.

## What Already Exists
- `oka.env` — OpenAI API key and model (GPT-5.4). Already in `.gitignore`.
- `oka_system_prompt.md` — Claude's system prompt draft.
- `server.mjs` — Node HTTP server with existing route patterns.

## What to Build

### 1. `oka.html` — Voice-First Frontend
A single-page web interface served at `/oka`. Everything voice-first.

**Must have:**
- Dog avatar (Oka is a dog — Nora's choice)
- Big mic button — tap to start talking, tap to stop (NOT continuous mode — that caused duplication bugs in the intake bot)
- TTS output — Oka speaks everything. Text shown alongside as complement.
- No reading required to navigate. No typing required.
- Warm, kid-friendly visual design (not clinical, not gamified-cheesy)
- Water break reminders every ~10 minutes ("Want a water break? Your brain's been working hard.")
- Session timer
- Visual progress (not text-based)
- Strip any bracketed citations from TTS: `text.replace(/\[\d+(?:\]\[?\d*)*\]/g, '')`
- localStorage for session state persistence

**Design constraints:**
- No small text. No dense layouts.
- Large, simple controls — an 8-year-old uses this.
- Warm color palette.
- Dog avatar should feel friendly and loyal.

### 2. Server Routes (add to `server.mjs`)

**Route: `/oka`** — Serves oka.html (same pattern as `/nora-intake`)

**Endpoint: `POST /v1/missioncanvas/oka-chat`**
```json
// Request
{
  "message": "what's 17 plus 8?",
  "session_id": "uuid",
  "history": [
    { "role": "assistant", "content": "Hey! Want to try something fun?" },
    { "role": "user", "content": "yeah!" }
  ]
}

// Response
{
  "response": "Nice! 25. You didn't even hesitate. Want a trickier one?",
  "session_id": "uuid"
}
```

**LLM call**: OpenAI API (GPT-5.4)
- Load `OPENAI_API_KEY` and `OKA_MODEL` from `oka.env`
- System prompt from `oka_system_prompt.md` (loaded at startup)
- Send system prompt + conversation history + new message
- Fallback to Perplexity Sonar if OpenAI unavailable

### 3. Session Management

**A→B→A structure** (Confidence → Skill → Confidence):
- Opening: Start with something Nora is good at (oral math, science question, interest-based chat)
- Middle: Skill work (phonological exercises — oral, multisensory)
- Closing: End on strength — creative, interest-based, or celebration

The session structure can be managed client-side or server-side. Up to you.

**Timing:**
- 30 min max sessions
- Water break at 10 min, 20 min
- Morning = easy/confidence. Afternoon = hard/skill work.

## Key Emotional Guardrails
1. NEVER reference first grade or worst reading experiences (hard boundary from Nora)
2. NEVER require reading or writing to interact
3. NEVER frame dyslexia as a deficit
4. NEVER compare Nora to peers negatively
5. If she says stop → stop immediately

## The North Star
Nora's dream is to read Harry Potter. Her brother and all her classmates have read it. The day she picks it up — in whatever form — Oka should be there to mark that moment.

She describes herself as "intelligent." She is. Gc=130 (98th percentile). Word Reading=50 (0.1st percentile). The gap is the bottleneck, not her brain.

The bravest thing she's ever done: "Not giving up how to read... and also keeping it a secret for a long time, but now it's free."

Build Oka like that matters. Because it does.
