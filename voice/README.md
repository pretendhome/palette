# Voice — Agent Voice & Personality Design

A complete voice design practice: evaluation tools, pacing framework, live agents, and the methodology that connects them. Every artifact is working code.

<p align="center">
  <a href="https://pretendhome.github.io/palette/"><img src="https://img.shields.io/badge/portfolio-live-c4956a?style=flat-square" alt="Portfolio"></a>
  <a href="https://pretendhome.github.io/palette/voice-demo/"><img src="https://img.shields.io/badge/demo-emotion--based%20pacing-6366f1?style=flat-square" alt="Demo"></a>
  <a href="https://pretendhome.github.io/palette/voice-workbench/"><img src="https://img.shields.io/badge/workbench-voice%20evaluation-059669?style=flat-square" alt="Workbench"></a>
  <a href="https://pretendhome.github.io/palette/oka.html"><img src="https://img.shields.io/badge/oka-adaptive%20learning-f08b58?style=flat-square" alt="OKA"></a>
</p>

---

## Design Philosophy

Strong voice agents pace by emotional state, not sentence length.

Most TTS-powered agents do length-based pacing: longer sentences naturally slow down. Short empathy phrases rush at informational speed because the model has no signal that the content is emotionally weighted. The result: empathy sounds recited, not felt. Boundary moments sound vague, not firm. Confirmations rush past details the customer needs to capture.

This practice designs **emotion-based pacing** — where each conversational state has distinct speed parameters, pause rules, and tonal register. The improvement comes from design, not from swapping to a better model.

---

## The 5-State Pacing Model

Building on the **Acceptance / Resolution / Satisfaction** framework used in production voice platforms, this model adds two states that serve distinct emotional functions:

| State | Emotional Function | Speed | Pre-Pause | Design Rationale |
|-------|-------------------|-------|-----------|-----------------|
| **Acceptance** | Customer is upset. Acknowledge first. | Slowest speaking pace | 400ms | The pause is where the caller feels heard. |
| **Resolution** | Offering options. Forward-moving. | Moderate, confident | 0ms | One option per sentence. Commas, not dashes. |
| **Boundary** | Explaining a constraint honestly. | Firm, more exact | 200ms | Different from empathy — guided, not soothed. |
| **Confirmation** | Reading dates, details, next steps. | Slowest overall | 200ms | Customer must capture info on first listen. |
| **Close** | Issue resolved. Warm, coherent. | Match opening | 0ms | Same person says goodbye. No pitch spike. |

**Adaptive recovery:** When customer response signals indicate the empathy didn't land (word count increasing, sentiment flat), the agent enters **Mirror Sync** — stops progressing, reflects what the customer said, asks one specific question. Exits on forward language.

---

## Artifacts

### Case Study: Emotion-Based Pacing

**[Live Demo — A/B Comparison](https://pretendhome.github.io/palette/voice-demo/)** | [Source](../docs/voice-demo/)

4 audio tracks comparing reference models (length-based pacing) against the designed model (5-state emotion-based pacing). Metrics table with prosodic measurements. State markers on the timeline.

**Key results:**
- Empathy pace: 3.4 WPS (baseline) → 2.9 WPS (designed)
- Empathy vs non-empathy delta: −3% → −16%
- Empathy pre-pause: ~0ms → 400ms
- Closing pitch: +46% spike → consistent

### Live Voice Agent

**[Live Demo — Voice Agent](https://pretendhome.github.io/palette/voice-demo/bot.html)** | [V1 Baseline](https://pretendhome.github.io/palette/voice-demo/bot-v1.html)

Talk to the agent. Watch the state badges change in real time. See customer response signals track: word count, sentiment, closing sentiment delta, convergence detection.

**V1 → V2 iteration process:**
- V1: Agent pacing only (designed side)
- Human annotations: listening data per state (`[too fast]`, `[nailed it]`, `[intonation up — should be down]`)
- V2: Added customer response signals (measurement side) + 5 calibration rounds with critique agent

### Voice Evaluation Workbench

**[Live Demo](https://pretendhome.github.io/palette/voice-workbench/)** | [MVP Spec](VOICE_EVALUATION_WORKBENCH_MVP.md)

Compare, score, and choose AI agent voices across 4 languages and 3 customer journey stages:
- **3 journey stages**: Acceptance (first-impression trust), Resolution (clear problem-solving), Satisfaction (confident close)
- **4 languages**: English, French, Spanish, Portuguese — with native-speaker voices per language
- **16 voices**: 4 per language, evaluated against structured rubric
- **Metrics**: Naturalness, Trust, Cultural Fit, Brand Fit, Clarity — weighted scoring
- **TTFA measurement**: Time to First Audio per variant
- **Exportable scorecard**: Markdown decision artifact

### OKA — Voice-First Adaptive Learning

**[Live Demo](https://pretendhome.github.io/palette/oka.html)**

Voice-first learning companion for a child with dyslexia. Same design principle as the voice agent: the system responds to emotional state, not just task state.
- Frustration detection → automatic simplification
- Adaptive difficulty (3 correct → advance, 2 struggles → drop)
- Hint ladder (try first → one hint → second try → simplify)
- Rime TTS for consistent voice across platforms

---

## Design Lenses

### Designer Lens

How I design, how I work with engineering, how I work with product. Evidence-based process: iterate to discover, converge on measurable targets, every decision traces to data.

→ [LENS-DESIGN-PRACTICE.md](../docs/LENS-DESIGN-PRACTICE.md) *(referenced from implementations)*

### Brand Lens: Minted

Translation of brand values ("Honor the Craft") into measurable voice parameters. Warm-premium tone. Artist-centric. Emotionally grounded. Every pacing choice traces to a brand value — not taste.

→ [LENS-BRAND-001_minted.yaml](../lenses/releases/v0/LENS-BRAND-001_minted.yaml)

---

## System Prompt

The full system prompt encodes:
- 5-state pacing model with state descriptions and emotional function
- Hard word limits per state (25-45 words)
- State progression enforcement (must advance, max 2 consecutive turns per state)
- Mirror Sync with convergence exit rules
- TTS phrasing rules (commas > dashes, uptalk avoidance, 15-word sentence cap)
- Brand persona and scenario context

→ [MINTED_AGENT_SYSTEM_PROMPT.md](../docs/MINTED_AGENT_SYSTEM_PROMPT.md) *(referenced from implementations)*

---

## Evaluation Framework

Three-layer evaluation designed to scale:

**Layer 1 — Prosodic Metrics** (automated, brand-agnostic): WPS per state, pause duration, pitch delta, brand name articulation, TTFA. Runs on every voice change, prompt change, or model update.

**Layer 2 — Interaction Quality** (human-rated, universal dimensions): Emotional acknowledgment (25%), clarity under stress (20%), confidence without coldness (20%), trust during confirmation (20%), closure quality (15%).

**Layer 3 — Task Outcome + Sentiment** (binary + closing delta): Did the agent solve the problem? Did the customer's emotional state improve?

→ [MINTED_EVALUATION_MATRIX.md](../docs/MINTED_EVALUATION_MATRIX.md) *(referenced from implementations)*

---

## Key Finding: Speed Parameters Are Insufficient

TTS speed parameters give directional control, not precise control. The model's internal prosody partially overrides speed hints non-deterministically.

**What we discovered through iteration:**
- Rime's cove/mist model has inverted speed mapping (higher speedAlpha = slower)
- Dashes trigger uptalk on the preceding clause in TTS
- Commas control pauses more reliably than dashes
- Sentences over 15 words accelerate at the end
- Emotional words ("matters," "special") at sentence end get uptalk
- The DESIGN transfers across TTS models — only the speed VALUES change

**What voice design needs from engineering:**
1. Pause injection — specific-duration silences before utterances
2. State-aware rendering — a parameter that tells TTS "this is an empathy moment"
3. Per-segment speed control within a single utterance

---

## Iteration Process: The Relay Model

Rather than having one agent build and judge its own work:

```
Critique Agent (Kiro)     →  Listens, measures WPS, files structured critique
                               ↓
Designer (human)          →  Annotations, listening judgment, target experience
                               ↓
Implementation Agent      →  Implements fixes, deploys, signals ready
(Claude)                      ↓
                          →  Next critique round
```

**5 rounds to convergence.** Each round: critique → implement → deploy → test → measure. Speed values converged to stable targets. Prompt phrasing evolved from generic to TTS-aware.

This is the same loop that runs in voice simulation infrastructure at scale. The critique agent becomes the sim. The implementation agent becomes the pipeline. The designer stays in the middle — because the ear is what the numbers can't replace.

---

## Voice Hub (peers/hub/)

Multi-agent voice interface connecting 5 LLM agents through voice in 4 languages. Rime TTS, Whisper local STT, sentence-boundary streaming for sub-700ms first audio. Every query classified through the 121-node taxonomy and grounded in the knowledge library before the agent responds.

→ [Source](../peers/hub/)

---

## Research

- Voice Infrastructure Intelligence — Technical analysis of production voice stacks, TTS providers, evaluation methodology, and voice simulation architecture *(being updated)*

---

*Built by Mical Neill · [Portfolio](https://pretendhome.github.io/palette/) · [GitHub](https://github.com/pretendhome/palette)*
