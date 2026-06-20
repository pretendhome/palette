# Oka Build Brief — For Codex

## What This Is
This brief is for improving Oka as a voice-first dyslexia learning tool for Nora. The goal is no longer just "build a warm companion." The goal is to build a system that adapts to her level in real time, protects confidence, and improves reading through low-pressure, intelligent support.

This is not a generic literacy app.

This should feel:
- personalized
- emotionally safe
- precise in how it helps
- adaptive without making adaptation visible
- strong enough for a parent to trust and a builder to implement

## Read Order
Read these before making changes:

1. `/home/mical/fde/implementations/education/adaptive-learning-architecture/nora/NORA_INTAKE_ANSWERS.md`
2. `/home/mical/fde/implementations/education/adaptive-learning-architecture/nora/NORA_OKA_CONVERGENCE_BRIEF.md`
3. `/home/mical/fde/palette/mission-canvas/OKA_TULLIA_LENS_DESIGN_SPEC.md`
4. `/home/mical/fde/palette/mission-canvas/oka_system_prompt_active.md`
5. `/home/mical/fde/palette/mission-canvas/oka.html`
6. `/home/mical/fde/palette/mission-canvas/server.mjs`

## What Already Exists
- `oka.html` — current `/oka` frontend
- `oka_system_prompt_active.md` — active runtime prompt
- `oka_system_prompt.md` — earlier prompt draft
- `oka_system_prompt_codex.md` — Codex-facing prompt variant
- `server.mjs` — serves `/oka` and `/v1/missioncanvas/oka-chat`
- `oka.env` — API keys and model config

## Product Shift

The previous Oka framing emphasized:
- companionship
- story-based reading moments
- oral skill support

The new requirement adds a much more explicit learning loop:
- one word at a time
- child tries first
- exact sound-level hinting
- second chance
- calm answer only if still stuck
- dynamic difficulty adaptation based on actual performance

This means Oka now needs to behave like:

`emotionally safe voice companion + adaptive single-word reading engine`

Not:

`open-ended chat bot that occasionally does literacy exercises`

## Core Interaction Model

### 1. Word-First Reading Flow

The reading engine should present:
- exactly one focus word at a time
- large, visually clear
- highlighted in purple by default
- red if it is an irregular / "red word"

Rules:
- Oka does not read the word first
- Nora attempts the word independently
- the screen should feel calm, uncluttered, and focused

### 2. Adaptive Support Ladder

If Nora struggles:

1. Give one precise hint
2. Let her try again
3. If still stuck, give the word calmly

The hint must target the hardest sound or letter only.

Do not:
- explain three things at once
- turn the hint into a mini-lesson
- jump straight to the answer
- stack failures

### 3. Difficulty Adaptation

Track and adjust in real time:
- word length success rate
- response time
- hint usage
- recurring sound/letter trouble

If too easy:
- slightly increase complexity
- reduce support
- allow more independent wait time

If too hard:
- simplify immediately
- offer easier success
- fall back to a previous level

### 4. Reading Before Writing

Reading is primary.

Writing is optional and occasional:
- keyboard only
- very short words
- must match current reading level

If reading is at 4-letter words, writing should also be 4-letter words.

### 5. Voice + Visual Coupling

When Nora says a word:
- the same word appears clearly on screen
- the word can animate slightly
- the visual should reinforce spoken-to-printed mapping

### 6. Confidence Protection

The system must:
- avoid pressure
- reduce difficulty after repeated struggle
- create quick recovery wins
- end loops on success more often than on failure

## What to Build

### 1. `oka.html` — Adaptive Reading Frontend

The frontend should support two layers:

**Layer A: Companion shell**
- dog avatar
- big mic button
- TTS playback
- large transcript / response area
- session timer
- water-break reminders
- visual calm and low clutter

**Layer B: Reading engine UI**
- one large focus word
- purple default highlight
- red-word mode for irregular words
- subtle motion when spoken word is recognized
- one hint region only
- no multi-step instruction clutter
- success / reset flow that feels gentle, not gamey

The interface must not require reading to navigate, but it can still show one large focus word for reading work.

### 2. `server.mjs` — Adaptive Session Logic

The chat endpoint should evolve from general conversation routing toward session-aware support.

At minimum the server should be able to support:
- current phase
- current word difficulty
- current word length band
- error / hint history
- confidence protection triggers
- repeated struggle fallback

You do not need a giant ML system for v1.
You do need a simple, intelligible adaptation state machine.

### 3. Prompt Behavior

The active prompt must reflect the new interaction rules:
- Nora should try first
- one hint at a time
- answer only after a second failed attempt
- minimal explanation
- calm recovery
- adaptive support

The prompt should preserve Oka's warmth while becoming more operationally precise.

## Build Priorities

### Priority 1
Implement the single-word adaptive reading loop.

### Priority 2
Add the performance-tracking logic needed to personalize:
- length
- sounds
- hint need
- pacing

### Priority 3
Add optional matched-level keyboard writing moments.

### Priority 4
Refine visual linking, subtle animations, and reportable parent/teacher insights later.

## Emotional Guardrails
1. Never ask about first grade or the worst reading experiences.
2. Never frame dyslexia as damage or defect.
3. Never compare Nora negatively to peers.
4. Never pressure her to keep going after overload.
5. Never turn a failed attempt into a shame spiral.
6. Never make Oka sound like a school test.

## UX Guardrails
1. One focal task at a time.
2. One word at a time.
3. One hint at a time.
4. Minimal text clutter.
5. Large touch targets.
6. Strong contrast and dyslexia-friendly readability.

## Technical Guardrails
1. Prefer a simple explicit state model over opaque adaptation logic.
2. Keep all adaptation inspectable and debuggable.
3. Make word progression rules easy to tune.
4. Preserve local session state.
5. Keep the tool runnable from the existing Mission Canvas server.

## The North Star
The system should feel, to Nora, like:

- "I can do this."
- "It gets me."
- "It changes when I need it to."
- "It knows when to help and when to back off."

And to an adult reviewing it:

- "This tool is careful."
- "This tool is adaptive."
- "This tool is emotionally intelligent."
- "This tool has a real reading-engine design, not just a chat prompt."
