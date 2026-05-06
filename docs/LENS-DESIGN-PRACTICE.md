# Design Practice Lens — Mical Neill
## How I Design · How I Work with Engineering · How I Work with Product

*Extracted from LENS-PERSON-001. Company-agnostic — applicable to any voice agent design role.*

---

## 1. HOW I DESIGN

### Process: Iterate to Discover, Then Converge

I don't plan then execute. I iterate to discover the right solution, then converge. The Minted case study followed this exactly:

1. **Read the critique prompt** — two voice samples, evaluate them
2. **Measured before opining** — WPS, pitch, pause duration, digit timing, persona coherence. 48 data points before writing a single paragraph
3. **Found the structural problem** — both models do length-based pacing, not tessitura-based pacing. 0-7% empathy rate delta where the target is 15%. This is the insight that engineers building better models wouldn't see — the problem is in the pacing design, not the model quality
4. **Designed the fix** — 5-state pacing model extending David's A/R/S framework. Each state has measurable parameters (speed, pause, register). Not taste — structure
5. **Built it** — system prompt, brand lens, conversation script, audio generation, demo player, live bot, evaluation matrix
6. **Tested it** — measured the output. Empathy hit 2.9 WPS (16% slower than non-empathy average). Pre-pause at 400ms. Closing pitch consistent. Design met targets
7. **Found the gap** — TTS speed parameters give directional control, not precise control. Model prosody partially overrides speed hints. Documented what I learned, didn't hide what didn't work

### Design Decision-Making: Evidence Over Taste

Every design decision traces to evidence, not preference:

| Decision | Evidence | Alternative Rejected |
|----------|----------|---------------------|
| 5 states, not 3 | Boundary and Confirmation serve different emotional functions than Resolution. Measured: Boundary is 3.3 WPS (firmer than empathy at 2.9), Confirmation is slowest at 2.5 WPS | Could have kept David's 3 states with adjective modifiers. Rejected because the customer's cognitive task changes — evaluating choices vs absorbing constraints vs capturing details — and each needs its own pacing |
| 400ms pre-pause | Natural empathetic speech has a 200-400ms pause before acknowledgment. Sample A had 140ms (below perceptible threshold). Sample B had 520ms (acceptable). Designed for 400ms | Could have relied on speed reduction alone. Rejected because the pause is where the caller feels heard — no speed change creates that |
| Minted as brand | Widest emotional range of any e-commerce brand I evaluated. Wedding invitations and bulk tracking require completely different voice behavior from the same agent. Operational complexity (marketplace artists ship independently) creates real Boundary moments | Could have chosen a playful brand or a complex media brand. Rejected because Minted tests the tessitura hardest — the emotional stakes are highest |
| Luna (Arcana) voice | Warm-composed without bubbly. Enough range for empathy→boundary without sounding like two different people. A brighter voice works for a playful casual brand but trivializes a wedding proof correction | Auditioned multiple voices. Luna passed because it can slow down without sounding sleepy and be firm without sounding cold |

### Off-the-Shelf vs Designed

This is the core thesis. Off-the-shelf (adjective-prompted: "be warm, professional, empathetic") produces 0% empathy rate delta. The model slows for longer sentences, not for emotional content. Designed (5-state pacing with state-specific parameters) produces 16% delta. Same voice, same brand, same scenario — different pacing intelligence. The improvement came from design, not from swapping to a better model.

### Craftsmanship

Every artifact in the portfolio is working code, not mockups:
- Demo player: 4 audio tracks with state markers on the timeline, A/B comparison, metrics table
- Live bot V1: real-time state tracking, measured WPS from TTS audio, pre-pause display
- Live bot V2: customer response signals, convergence detection, closing sentiment delta
- Evaluation matrix: 3-layer assessment (prosodic + rubric + task outcome) with composite scoring
- Brand lens: YAML-formatted translation of Minted values to measurable voice behavior
- System prompt: 283 lines encoding pacing rules, persona, scenario, and exception handling

Design in code. The design judgment IS the implementation.

---

## 2. HOW I WORK WITH ENGINEERING

### The Pattern: Show the Structural Problem with Evidence, Not Opinion

**Alexa Automotive (2019-2023)**: Engineers were building sophisticated vector databases to fix voice quality issues in POI (point of interest) data across 13 locales and 47 providers. I showed them that the problem was structural: Italian automotive service categories don't map 1:1 to American ones. "Autofficina" is not "auto shop" — it covers services that Americans split across 3 different categories. I fixed the mapping, not the model. One of the biggest quality improvements the system had seen.

The engineers' approach was technically correct but solving the wrong problem. I earned trust by showing the evidence — here is how the taxonomy maps, here is where it breaks, here are the queries that fail because of it — not by pulling rank or arguing taste.

**Voice agent case study (same pattern)**: The TTS finding. I designed 5 pacing states within Minted's tessitura (0.83–1.30 speedAlpha). The empathy state hit the 16% target — but only after 5 iteration rounds to find the right speed values. The model's internal prosody partially overrides speed hints non-deterministically. TTS models know their range but not their tessitura.

I documented this as an engineering problem, not a design complaint: "Real tessitura-aware pacing needs either SSML-level control with pause and emphasis tags, or state-aware TTS models that understand which speeds serve which emotional moments."

### What I Want from Engineering (Prioritized)

1. **Pause injection** (highest impact, likely easiest) — insert specific-duration silences before utterances, not just between them. The 400ms pre-pause before empathy is where the caller feels heard. No speed adjustment creates this.
2. **State-aware rendering** (medium effort, high value) — a parameter or tag that tells TTS "this is an empathy moment" so it adjusts pitch range and breathiness, not just tempo.
3. **Per-segment speed control** (hardest, most powerful) — so a confirmation line can slow down for the date and speed up for the narrative within one utterance.

I define the interface and the acceptance criteria. Engineering decides the implementation. I test whether the platform achieves the design intent and bring the gap back as a design question, not a complaint.

### Technical Communication

I can explain complex systems to non-technical audiences (taught English to Italian police using The Economist, not textbooks) and can go deep with engineers (measured WPS, pitch contours, pause durations, digit-string timing across both voice samples). I adjust the technical depth to the listener without losing accuracy.

When I describe what I need from engineering: measurable targets, prioritized by impact/effort ratio, with acceptance criteria I can test myself.

---

## 3. HOW I WORK WITH PRODUCT

### The Pattern: Evaluation Frameworks as Product Infrastructure

The evaluation matrix isn't just for this case study. It's a product primitive:

**Layer 1 — Prosodic metrics** (automated, brand-agnostic): WPS per state, pause duration, pitch delta, brand name articulation, TTFA. Same measurements work for a premium curated marketplace and a casual lifestyle brand. This is the automated quality gate — runs on every voice change, every prompt change, every model update. Like unit tests for voice quality.

**Layer 2 — Interaction quality rubric** (human-rated, universal dimensions): emotional acknowledgment, clarity under stress, confidence without coldness, trust during confirmation, closure quality. Rated 1-5 by non-expert listeners. Dimensions are fixed across the platform — only the brand-calibrated thresholds change.

**Layer 3 — Task outcome** (binary, per use case): did the agent solve the problem? Plus closing sentiment delta — did the customer's emotional state improve?

### Three Product Primitives for Voice Quality

1. **Brand voice profile** — the parameterized pacing/tone configuration that makes each brand's agent distinct. This is the design system input. Ghostwriter needs these to be parameterized, not bespoke.
2. **Quality gate** — automated prosodic checks that run before any voice update ships to production. No deployment without passing the gate.
3. **Simulation framework** — test voice changes against realistic customer scenarios before they go live. Voice Sims already do this for task completion and latency. Adding emotional pacing metrics closes the loop between design intent and production behavior.

### Customer Feedback → Design Decisions

The closing sentiment delta IS customer feedback driving design. The system measures the customer's emotional trajectory in real time. When the measurement shows the pacing didn't land (convergence detection), the agent changes behavior. That's a closed loop: customer signal → design adaptation → measurable outcome.

At AWS, I built adoption instrumentation tracking behavior change — not "did they attend training" but "did their work change." Same principle: measure the outcome that matters, not the activity.

### Scaling to 50 Brands

The brand-to-pacing-parameter translation breaks first. Right now it's manual (read brand values, translate to voice behavior, set WPS targets). At scale, this needs a brand voice intake tool: deployment team answers 10 structured questions about the brand's emotional register, system generates a pacing profile. Like a design system for voice — not bespoke, but parameterized from a shared foundation.

The key product decision: what's configurable per brand vs what's fixed across the platform.
- Layer 1 targets: parameterized per brand (a premium brand's empathy pace differs from a casual brand's)
- Layer 2 dimensions: fixed across platform (emotional acknowledgment is universal)
- Layer 3: defined per use case

### Speed and Adaptability

Alice's words: "Very fast-paced, need folks that ebb and flow. Nothing is perfect but we want to build something nearly perfect."

This matches exactly how I work. The 5-state model is a framework, not a finished product. Ship the architecture, refine the parameters. The Minted case study went from critique to working demo with measured results in under a week. Each iteration produced observable learning that fed the next. Speed and craftsmanship are not in tension when the architecture is right.

---

## STAR-READY STORIES

### Design Decision Under Pressure
**S**: Voice model critique — two voice samples from different providers, evaluate cold with no context on which was which.
**T**: Identify the structural failure, not just grade the samples.
**A**: Measured 48 prosodic data points. Found the length-based pacing pattern. Designed a 5-state fix. Built a working proof of concept.
**R**: Designed agent hit 16% empathy rate delta (target ≥15%), 400ms pre-pause, consistent closing pitch. Baseline hit 0%.

### Working with Engineering (Structural vs Technical Fix)
**S**: Alexa automotive POI quality failures across 13 locales and 47 providers.
**T**: Engineers were building vector databases to improve voice quality. Quality wasn't improving.
**A**: Mapped how different countries categorize automotive services. Found structural mismatches — categories that don't translate 1:1. Fixed the taxonomy mapping, not the model.
**R**: One of the biggest quality improvements the system had seen. Engineering trusted the fix because I showed the data, not my opinion.

### Working with Product (Measurement Changes the Design)
**S**: Ask Pathfinder at AWS — knowledge retrieval for 12,000 sellers/month.
**T**: Improve retrieval accuracy. Previous approach was industry-based taxonomy.
**A**: Reclassified from industry-based to function-based. Users search by what they need to do, not what industry they're in. No model changes — structural fix only.
**R**: 28% retrieval accuracy improvement. +17% engagement, +50% satisfaction, +67% feature adoption. Measured behavior change, not completion rates.

### Buy-In When Difficult
**S**: Amazon Italy — Kaizen improvement competition.
**T**: Generate improvement ideas from a customer service center where employees had never been asked.
**A**: Asked every employee for ideas. Championed an L2 employee's idea through the corporate process.
**R**: First L2 employee to win the company-wide Think Big competition. Proof: creating the environment for innovation matters more than being the innovator.
