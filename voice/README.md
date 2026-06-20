# Voice — Agent Voice & Personality Design

A complete voice design practice: evaluation tools, pacing framework, live agents, and the methodology that connects them. Every artifact is working code.

<p align="center">
  <a href="https://pretendhome.github.io/palette/"><img src="https://img.shields.io/badge/portfolio-live-c4956a?style=flat-square" alt="Portfolio"></a>
  <a href="https://pretendhome.github.io/palette/voice-demo/"><img src="https://img.shields.io/badge/demo-finding%20the%20tessitura-6366f1?style=flat-square" alt="Demo"></a>
  <a href="https://pretendhome.github.io/palette/voice-workbench/"><img src="https://img.shields.io/badge/workbench-voice%20evaluation-059669?style=flat-square" alt="Workbench"></a>
  <a href="https://pretendhome.github.io/palette/oka.html"><img src="https://img.shields.io/badge/oka-adaptive%20learning-f08b58?style=flat-square" alt="OKA"></a>
</p>

---

## Design Philosophy: Tessitura

In vocal performance, **tessitura** is the range where a singer's voice sounds most natural — not the highest or lowest notes they can hit, but where they sound most like themselves. It's narrower than their full range.

Every brand has a tessitura too. The designer's job is to find it, stay in it, and measure it.

Most TTS-powered agents do length-based pacing: longer sentences naturally slow down. Short empathy phrases rush at informational speed because the model has no signal that the content is emotionally weighted. The result: empathy sounds recited, not felt. Boundary moments sound vague, not firm. Confirmations rush past details the customer needs to capture. The voice is singing outside its tessitura.

This practice designs **tessitura-based pacing** — where each conversational state sits at a measured point within the brand's tessitura. The speed range for Minted's agent (0.83–1.30 speedAlpha) is the measured tessitura: the band within which every state must operate. Going outside that band is the vocal equivalent of straining — technically possible, audibly wrong.

---

## The 5-State Pacing Model

Building on the **Acceptance / Resolution / Satisfaction** framework, this model adds two states — Boundary and Confirmation — because they serve different emotional functions that require different positions within the tessitura:

| State | Emotional Function | Speed | Pre-Pause | Within the Tessitura |
|-------|-------------------|-------|-----------|---------------------|
| **Acceptance** | Acknowledge before solving. | 1.22 (slow) | 400ms | The deepest point — the pause is where the caller feels heard. |
| **Resolution** | Forward-moving, confident. | 0.83 (moderate) | 0ms | The center — efficient but not rushed. |
| **Boundary** | Constraint, honestly. | 0.95 (firm) | 200ms | Firm but still warm — if it sounds cold, it left the tessitura. |
| **Confirmation** | Dates, details, next steps. | 1.30 (slowest) | 200ms | Slowest point — customer must capture this on first listen. |
| **Close** | Warm, coherent with opening. | 0.90 (warm) | 0ms | Returns to opening position. Same person says hello and goodbye. |

**Adaptive recovery (Mirror Sync):** When customer signals show the empathy didn't land — word count increasing, sentiment flat — the agent stops progressing and recalibrates. Not a 6th state. It's what recenters the voice within the tessitura.

---

## Artifacts

### Case Study: Finding Minted's Tessitura

**[Live Demo — A/B Comparison](https://pretendhome.github.io/palette/voice-demo/)** | [Source](../docs/voice-demo/)

4 audio tracks comparing reference models (outside the brand's tessitura) against the designed model (5-state pacing within Minted's tessitura). Metrics table with prosodic measurements. State markers on the timeline.

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

## Key Finding: TTS Models Know Their Range, Not Their Tessitura

TTS speed parameters give directional control, not precise control. The model's internal prosody partially overrides speed hints non-deterministically. In cascade architecture (STT→LLM→TTS), paralinguistic information — tone, emotion, pacing — is lost at the text boundary. Speed parameters are an imprecise proxy for reintroducing it.

**What we discovered finding Minted's tessitura (5 iteration rounds):**
- Rime's cove/mist model has inverted speed mapping (higher speedAlpha = slower)
- Dashes trigger uptalk on the preceding clause — pulls the voice out of tessitura
- Commas control pauses more reliably than dashes
- Sentences over 15 words accelerate at the end — leaves the tessitura on CONFIRMATION
- Emotional words ("matters," "special") at sentence end get uptalk — sounds wrong for the brand
- The TESSITURA MODEL transfers across brands — change the brand, change the range

**What tessitura-aware TTS needs from engineering:**
1. Pause injection — specific-duration silences before utterances (the 400ms empathy pause)
2. State-aware rendering — a parameter that tells TTS "this is within the empathy region of the tessitura"
3. Per-segment speed control within a single utterance — so the voice stays in range across clauses

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

- **[Agentic Voice Industry — Technical Intelligence Report (PDF)](research/agentic_voice_industry_report.pdf)** — Architecture- and benchmark-led survey of the voice AI agent ecosystem as of May 2026. Covers STT/TTS providers, pipeline architecture (cascade vs. S2S), latency targets, multilingual deployment, and simulation infrastructure across 20+ platforms including Sierra, Vapi, Retell AI, PolyAI, Hume, ElevenLabs, Deepgram, Cartesia, and others. Confidence-rated claims with cited sources.
- **[Sierra Voice Intelligence](SIERRA_VOICE_INTELLIGENCE.md)** — Sierra-specific technical analysis: tau-Voice scoring methodology, Voice Sommelier process, Voice Sims scenario structure, locale routing, and latency architecture. Primary sources only.

---

*Built by Mical Neill · [Portfolio](https://pretendhome.github.io/palette/) · [GitHub](https://github.com/pretendhome/palette)*
