# Sierra AI Voice Infrastructure — Technical Intelligence Report

**Date:** April 15, 2026  
**Purpose:** Pre-application technical intelligence for Agent Experience Designer, Voice (Multilingual) role  
**Methodology:** Primary sources only — Sierra engineering blog, arXiv paper, Deepgram customer listing, job postings

---

## Summary Table

| Question | Confidence | Key Finding |
|---|---|---|
| TTS Providers | **HIGH** (confirmed) | Deepgram listed Sierra as customer; τ-Voice paper uses ElevenLabs v3 for simulator TTS; τ³-Bench benchmarks OpenAI Realtime, Gemini Live, Grok Voice |
| τ³-Bench scoring | **HIGH** (paper) | 4 voice interaction quality dimensions; pass@1 task completion; 278 tasks across 3 domains |
| Voice Sommelier process | **MEDIUM** (blog) | Subjective/qualitative; no published scorecard; dimensions: breath, rhythm, stress, pitch, vocal textures |
| Locale routing | **MEDIUM** (blog) | "Optimal combination" per locale; human-curated + automated benchmarking; providers not named |
| STT Providers | **HIGH** (confirmed) | Deepgram confirmed ("Powered by Deepgram" customer list includes Sierra) |
| Latency targets | **MEDIUM** (blog) | TTFA = primary metric; "hundreds of milliseconds" cut by custom VAD; no published number targets |
| Voice Sims schema | **HIGH** (blog + paper) | Persona (goal/mood/language/patience) + acoustic effects + LLM judge; CI/CD integrated |

---

## Q1. TTS Providers

### What is confirmed

**Deepgram (STT — confirmed):** Deepgram's March 2026 job posting explicitly lists Sierra as a "Powered by Deepgram" customer alongside Twilio, Cloudflare, Decagon, and Vapi. Source: [Deepgram job posting, Ashby](https://jobs.ashbyhq.com/Deepgram/b9b27091-1a95-4c31-a304-55c31711887a).

**ElevenLabs (used in evaluation toolchain — confirmed):** The τ-Voice arXiv paper (Sierra Research, March 2026) specifies that the **Voice User Simulator** uses **ElevenLabs v3 at 24kHz** for TTS. This is the simulator's voice — not necessarily the production agent voice — but confirms ElevenLabs is integrated into Sierra's evaluation infrastructure. Source: [arXiv:2603.13686](https://arxiv.org/html/2603.13686v1).

**OpenAI Realtime, Google Gemini Live, xAI Grok Voice (benchmarked, not used internally):** τ³-Bench (March 2026) benchmarks these three as external voice agents, not as Sierra's own TTS providers.

### What is unconfirmed

Sierra's blog says: *"modular voice architecture selects the optimal combination of models for each locale."* The specific TTS providers powering **production agents** (i.e., the agent voice customers hear) are not publicly named. Sierra designs custom voices using voice actors and synthesizes them through an unnamed provider. The [Voice Sommelier blog](https://sierra.ai/blog/meet-the-voice-sommelier) mentions named voices like Jade, Tatyana, and Steven — these are Sierra house voices, not provider-attributed. 

**Plausible candidates based on market positioning:** Cartesia (ultra-low-latency streaming, favored by enterprise voice agent builders), ElevenLabs (multilingual expressiveness across 30+ languages). These are the two dominant providers for enterprise voice agents in 2026 — but Sierra has not confirmed either in production. No mention of Azure Neural TTS, Google Cloud TTS, Amazon Polly, or PlayHT in any Sierra-sourced materials.

### Bottom line

| Provider | Role | Confirmation level |
|---|---|---|
| Deepgram | STT (speech-to-text) | **Confirmed** — customer list |
| ElevenLabs v3 | Voice simulator TTS | **Confirmed** — τ-Voice paper |
| Custom VAD model | End-of-speech detection | **Confirmed** — latency blog |
| OpenAI / Gemini / Grok | Benchmarked (not internal) | Confirmed as benchmark targets |
| Cartesia, ElevenLabs (production) | Production TTS | **Unconfirmed** — plausible |
| Azure, Google Cloud, Polly | Production TTS | **No evidence** |

---

## Q2. τ³-Bench Voice Scoring Methodology

**Source:** [arXiv:2603.13686](https://arxiv.org/html/2603.13686v1) — "Benchmarking Full-Duplex Voice Agents on Real-World Domains" — Sierra Research, March 2026

### What τ-Voice measures

τ-Voice extends τ²-Bench to live voice interactions. It measures **two categories** of metrics:

**1. Task Completion (pass@1)**
- Proportion of tasks completed successfully on a single attempt
- Evaluated **deterministically** by comparing final database state against annotated goals
- For spoken output (variable phrasing): uses **LLM evaluation** instead of string matching
- Scale: 278 tasks across Retail (114), Airline (50), Telecom (114)

**2. Voice Interaction Quality — 4 Dimensions**

| Dimension | Formula | What it measures |
|---|---|---|
| **Responsiveness** | avg(R_R, R_Y) | R_R = % user turns that get a response; R_Y = % interruptions where agent yields within 2s |
| **Latency** | avg(L_R, L_Y) | L_R = time from user utterance end → agent response; L_Y = time to stop speaking after interruption |
| **Interrupt rate** | I_A | % of turns where agent speaks before user finishes (>100% = multiple interruptions per turn) |
| **Selectivity** | avg(S_BC, S_VT, S_ND) | Correctly ignoring backchannels (mm-hmm), vocal tics (um), non-directed speech ("hold on") |

### Human vs automated

τ-Voice is **fully automated** — no human raters. The system uses:
- Deterministic database state comparison for task success
- LLM-as-judge for spoken output verification
- Timing logs for interaction quality metrics (responsiveness, latency, interrupt rate, selectivity)

This is **not** Sierra's internal voice quality evaluation — it's a **public research benchmark** measuring task completion and conversational behavior, not voice aesthetics (naturalness, warmth, brand fit). It does not score breath, rhythm, or pitch.

### Key results (March 2026)

| Provider | Clean pass@1 | Realistic pass@1 | Latency | Responsiveness |
|---|---|---|---|---|
| Google Gemini Live | 31% | 26% | 1.14s | 69% |
| OpenAI Realtime | 49% | 35% | 0.90s | 100% |
| xAI Grok Voice | 51% | 38% | 1.15s | 83% |
| GPT-5 (text baseline) | — | 85% | — | — |

The voice-text gap is the headline: best voice agents reach ~51% clean vs. ~85% text. Authentication failures (mishearing names/emails) are the leading error type.

### What τ³-Bench does NOT measure

- Voice naturalness (MOS-style)
- Brand fit or warmth
- Cultural appropriateness
- Acoustic quality of synthesis
- Any dimension from your evaluation rubric (Naturalness, Trust, Brand Fit, Cultural Fit, Clarity)

---

## Q3. Voice Sommelier Evaluation Process

**Source:** [sierra.ai/blog/meet-the-voice-sommelier](https://sierra.ai/blog/meet-the-voice-sommelier) — September 2025

### Process (as described)

The Voice Sommelier role is Sierra's internal voice designer function. The published blog describes a largely **qualitative, judgment-based process** — not a published rubric or scorecard.

**Stage 1 — Brand discovery**
- Understand brand values, tone-of-voice guidelines
- Understand customer mindset, goals, emotional states
- Celebrity touchstone exercise: "If any actor could be the voice of your brand, who would it be?" — surfaces emotional presence, vocal traits (warm/witty, elite/for everyone, funny/serious)

**Stage 2 — Voice dimensions evaluated**

| Dimension | Description |
|---|---|
| Breath | Natural breath patterns |
| Rhythm | Pacing and cadence feel |
| Stress | Emphasis and syllable weighting |
| Pitch | Intonation variation |
| Gravel | Slight roughness |
| Vocal fry | Low, creaky register |
| Breathiness | Airy quality |
| Human ticks | "um", "hmm" (used sparingly) |

**Stage 3 — Journey-stage tuning**

| Stage | Voice target |
|---|---|
| Acceptance | Warm, trust-building — first moment of trust won or lost on tone |
| Resolution | Clear communication, emotional intelligence, confident delivery |
| Satisfaction | Intentional, brand-aligned; customers rate experience more favorably |

**Stage 4 — Iteration**
The blog describes: *"listen, hypothesize, iterate, and test — always remembering voice is just the top layer."*

### No published scorecard

There is **no public rubric or scorecard format** described in any Sierra source. The process is described as collaborative between Voice Sommelier, customers, and agent development teams. Measurement appears to be through:
1. Live call metrics (did customer stick around / Acceptance)
2. Resolution rates
3. Customer satisfaction scores
4. Voice Sims evaluation runs

### Key insight for your demo

Sierra's Acceptance/Resolution/Satisfaction framework is directly derived from the Voice Sommelier's evaluation philosophy — these three stages map to measurable business outcomes (retention, resolution rate, CSAT), not just aesthetic scores. Your rubric (Naturalness, Trust, Brand Fit, Cultural Fit, Clarity) maps well to what Sierra's process targets but formalizes it into a repeatable scorecard — which Sierra does not appear to have published.

---

## Q4. Locale Provider Selection

**Source:** [sierra.ai/blog/multilingual-voice-agents](https://sierra.ai/blog/multilingual-voice-agents) — October 2025

### What Sierra says

*"The right combination of models — across comprehension, orchestration, reasoning, and generation — varies by locale. Transcription that performs accurately in Japanese might miss nuance in Portuguese, while a synthesis model that sounds natural in Arabic might sound too formal in Hindi."*

### Architecture (as described)

- **Modular voice architecture** selects optimal combinations per locale
- The selection covers all four pipeline stages: comprehension (STT), orchestration (routing), reasoning (LLM), and generation (TTS)
- This means different providers or different models within the same provider, per language
- The architecture handles blending and tuning "behind the scenes"

### How selections are made

The multilingual blog describes a **hybrid process**:
1. **Automated benchmarking** — testing accuracy, latency, rhythm, and tone across 34+ languages
2. **Human evaluation** — measuring naturalness and conversational flow
3. **Native speaker testing** — native speakers test and vet interactions before agents go live; capture "rhythm and spontaneity of real speech"
4. **Continuous measurement** — identifies and deploys best-performing combinations per locale

### What is unconfirmed

No specific routing logic is described. Sierra does not say whether selection is:
- A static lookup table (human-curated, reviewed periodically)
- A runtime routing layer (selects provider per-call based on language detection)
- Or both

No provider names are associated with any specific language or language family in any public source.

### Bottom line

Provider selection per locale is **human-curated and continuously benchmarked**, not fully automated at runtime. The "optimal combination" language suggests periodic updates rather than real-time routing decisions. This is consistent with how enterprise voice platforms typically operate: locale configurations are set by engineering teams based on benchmark results, not selected dynamically per call.

---

## Q5. STT Providers

### Confirmed

**Deepgram — confirmed.**

Deepgram's [March 2026 job posting](https://jobs.ashbyhq.com/Deepgram/b9b27091-1a95-4c31-a304-55c31711887a) lists Sierra in its customer roster: *"More than 200,000 developers and 1,300+ organizations build voice offerings that are 'Powered by Deepgram', including Twilio, Cloudflare, **Sierra**, Decagon, Vapi, Daily, Cresta, Granola, and Jack in the Box."*

### Additional context

Sierra's latency blog confirms a **custom VAD (Voice Activity Detection) model** for end-of-speech detection: *"We trained a custom voice activity detection (VAD) model optimized for noisy, multi-speaker environments. It predicts speech completion earlier and more accurately than off-the-shelf alternatives."* This is a Sierra-built model on top of (or replacing) the raw STT streaming input — it sits between the audio stream and the STT finalization step.

### Not confirmed

- **Google Speech / Whisper / AssemblyAI**: No mentions in any Sierra source
- The τ-Voice paper uses ElevenLabs for the **user simulator** voice, but the simulated user's transcript is piped **directly to the LLM, bypassing ASR** — so the paper does not confirm any STT provider for production agents

---

## Q6. Voice Latency Targets

**Source:** [sierra.ai/blog/voice-latency](https://sierra.ai/blog/voice-latency) — October 2025

### Primary metric: TTFA

Sierra explicitly defines **TTFA (Time to First Audio)** as the primary latency metric:

> *"The most important latency metric for conversational AI systems is Time to First Audio (TTFA) — how long it takes for the agent to start speaking after the customer finishes."*

Sierra measures TTFA from the **true end of user speech** (using their custom VAD), not from delayed or approximate timestamps. They explicitly reject gaming TTFA with filler audio ("uh-huh", "let me check") — they measure time to the first **relevant** response.

### Published numbers

**No specific TTFA target (e.g., "<500ms") is stated in the blog.** The published optimizations describe:
- Custom VAD cuts "reaction lag by hundreds of milliseconds"
- Frequent phrase caching cuts playback latency "to zero"
- Streaming begins "as soon as the first tokens arrive"
- Non-streaming providers handled "sentence by sentence" for near-immediate speech

### Industry context (not Sierra-specific)

From the broader voice AI engineering community:
- Sub-500ms TTFA is the industry target for a conversation that "feels instantaneous" — [Gradium, Feb 2026](https://gradium.ai/blog/optimizing-quality-vs-latency)
- The τ-Voice benchmark results show OpenAI Realtime achieves **0.90s average latency** (realistic conditions), Google at 1.14s — suggesting Sierra's own stack likely targets sub-1s
- Industry budget breakdown: STT ~50-100ms, LLM TTFT ~100-200ms, TTS first-byte ~50-80ms, transport ~20-50ms

### Latency stack summary (Sierra architecture)

| Stage | Technique | Impact |
|---|---|---|
| End-of-speech detection | Custom VAD model | Cuts hundreds of ms vs off-the-shelf |
| Reasoning | Concurrent graph (parallel execution) | Reduces sequential dependencies |
| Reasoning | Predictive prefetching (preloads customer data) | Near-zero for common queries |
| Reasoning | Provider hedging (fan-out, fastest wins) | Reduces tail latency |
| Synthesis | Phrase caching (greetings, confirmations) | Near-zero for frequent phrases |
| Synthesis | Streaming (first tokens → playback start) | Eliminates wait-for-full-synthesis |
| Synthesis | Sentence batching (non-streaming providers) | Near-immediate speech for batch providers |

### Sentence-boundary streaming

Sierra uses sentence-level batching for non-streaming TTS providers. For streaming-capable providers, synthesis begins on the first token. The latency blog confirms this but does not specify sentence boundary detection methodology (e.g., punctuation-based, model-based, silence-based).

---

## Q7. Voice Sims Scenario Structure

**Sources:** [sierra.ai/blog/voice-sims-test-agents](https://sierra.ai/uk/blog/voice-sims-test-agents-in-real-world-conditions-before-they-talk-to-your-customers) (September 2025), [sierra.ai/blog/how-voice-sims-work](https://sierra.ai/blog/how-voice-sims-work) (April 2026), [arXiv:2603.13686](https://arxiv.org/html/2603.13686v1) (March 2026)

### Scenario input structure

A Voice Sim scenario is configured with:

| Field | Description |
|---|---|
| **Persona: Goal** | What the simulated user wants to accomplish |
| **Persona: Mood** | Calm, frustrated, confused, impatient, angry |
| **Persona: Language** | Target language (34+ supported) |
| **Persona: Patience level** | How long user will tolerate delays/failures |
| **Location/device** | At home (TV on), street, train, etc. — determines background noise type |
| **Success criteria** | Defined pass/fail conditions evaluated by LLM judge |
| **Scenario description** | Natural language description of the test case |

### How scenarios are created

Two modes:
1. **Auto-generated** — Sierra infers test cases from: SOPs, knowledge bases, coaching transcripts, conversation flows, policies. No manual writing required.
2. **Manual** — Human-defined: scenario description + success criteria + location/device info.

### Architecture: Dual loop

```
[Simulated call loop]                    [Voice loop (agent)]
  ↓ Persona → speech (ElevenLabs v3)      ↓ STT (transcription)
  ↓ + background noise                    ↓ Agent reasoning
  ↓ + DTMF tones                          ↓ TTS (response)
  ↓ ← small audio chunks → ↓             ↓ Timing management
                                          ↓ (pauses, interruptions)
         ← LLM judge evaluates full conversation →
```

The τ-Voice paper specifies the simulation runs in **200ms ticks** (τ=200ms), with both loops exchanging exactly τ ms of audio per tick. This makes conversations reproducible with a fixed seed.

### Acoustic effects applied (from τ-Voice paper)

| Effect | Specification |
|---|---|
| Background noise | Indoor/outdoor, 15 dB SNR ± 3 dB drift |
| Burst noise | ~1/min (ringing phone, car horn), -5 to +10 dB SNR |
| Frame drops | ~2.0% average (G.E. model, 100ms burst) |
| Telephony | G.711 μ-law 8kHz codec |
| Muffling | Dynamic, 20% of utterances |
| Accents | Diverse personas: Mildred Kaplan, Arjun Roy, Wei Lin, Mamadou Diallo, Priya Patil |
| Backchannels | LLM-driven "mm-hmm" |
| Interruptions | LLM-driven mid-sentence interruptions |
| Involuntary sounds | Coughs, sneezes (~0.7/min Poisson) |
| Non-directed speech | "hold on", "one sec" (~0.7/min Poisson) |

### Metrics per sim run

The production Voice Sims system (Agent Studio) tracks:

| Metric category | Examples |
|---|---|
| **Speech accuracy** | STT transcription accuracy (accents, noise, acronyms); license plates, account numbers, dates of birth |
| **Behavioral compliance** | Did agent follow design rules? (authenticate via spoken DOB, avoid reading URLs, use keypad fallback) |
| **Emotional response** | Did agent apologize appropriately? Adopt reassuring tone? Avoid robotic phrasing? |
| **Latency** | Per-turn timing; overall TTFA |
| **Turn-taking** | Did agent pause when interrupted? Speak over customer? |
| **Error localization** | Is the failure in recognition (STT), reasoning (policy), or synthesis (intonation, pronunciation)? |
| **Task completion (pass@1)** | Did the LLM judge determine the conversation met success criteria? |
| **Release regression tracking** | Per-journey metrics over time to catch regressions before production |

### Integration

Voice Sims run in:
- **Agent Studio (no-code):** Audio replay, waveform scrubbing, jump-to-failure point
- **CLI (programmatic):** Baked into CI/CD pipelines; blocks releases on failure
- **Cross-channel parity:** Same evaluation infrastructure as chat and email sims
- Available to Sierra customers at no additional charge

---

## Synthesis: What This Means for Your Demo

### What Sierra has built vs. what you're demoing

| Sierra has | Your demo provides |
|---|---|
| Voice Sims (automated QA at scale) | Voice Evaluation Workbench (human judgment tool) |
| τ-Voice (automated behavioral metrics) | Structured scoring rubric (Naturalness, Trust, Brand fit, etc.) |
| Voice Sommelier (expert qualitative process) | Repeatable scorecard any PM can use |
| Celebrity touchstone exercise | Persona targets (Warm guide, Luxury concierge, etc.) |
| A/R/S framework (outcomes) | A/R/S framework (evaluation stages) |
| Custom voices (Jade, Tatyana, Steven) | Voice variants A/B/C/D |
| Native speaker testing | Cultural fit dimension in rubric |

Your demo fills a gap Sierra's own public toolchain has: **a decision artifact for the human evaluation layer**. τ-Voice measures machine performance. Voice Sims catches bugs. The Voice Sommelier process is expert-dependent and undocumented. Your workbench makes that judgment repeatable and exportable.

### Technical language to use in your application

- **TTFA** (not "response time") — Sierra's explicit metric name
- **Acceptance/Resolution/Satisfaction** — Use exactly; they're Sierra's framework
- **Voice Sims** — Reference when explaining why evaluation needs to happen before deployment
- **τ-Voice metrics** — Reference when explaining that behavioral metrics alone don't capture voice quality
- **Locale-specific model selection** — Use to frame why cultural fit is a scored dimension, not an afterthought
- **Provider hedging / modular architecture** — Explains why voice evaluation across variants matters (Sierra may be switching providers per locale; evaluators need a consistent framework)

### What not to claim

- Do not claim to know Sierra's production TTS providers — say "confirmed Deepgram for STT; TTS providers not publicly disclosed"
- Do not present your rubric as replicating τ-Bench — they measure completely different things
- Do not claim Voice Sims is a scoring tool — it's a QA/regression tool; your workbench is the evaluation tool

---

## Source Index

1. Deepgram job posting (Sierra as customer) — https://jobs.ashbyhq.com/Deepgram/b9b27091-1a95-4c31-a304-55c31711887a
2. τ-Voice arXiv paper — https://arxiv.org/html/2603.13686v1
3. Sierra Voice Latency blog — https://sierra.ai/blog/voice-latency
4. Sierra Voice Sommelier blog — https://sierra.ai/blog/meet-the-voice-sommelier
5. Sierra Multilingual Voice blog — https://sierra.ai/blog/multilingual-voice-agents
6. Sierra Voice Sims launch blog — https://sierra.ai/uk/blog/voice-sims-test-agents-in-real-world-conditions-before-they-talk-to-your-customers
7. Sierra How Voice Sims Work blog — https://sierra.ai/blog/how-voice-sims-work
8. Sierra Voice Post-Training blog — https://sierra.ai/blog/voice-post-training
9. Sierra τ³-Bench blog — https://sierra.ai/blog/bench-advancing-agent-benchmarking-to-knowledge-and-voice
10. τ³-Bench LinkedIn (Bret Taylor) — https://www.linkedin.com/posts/brettaylor_%F0%9D%9C%8F%C2%B3-bench-advancing-agent-evaluation-to-activity-7441883892262969344-1FVH
11. ElevenLabs vs Sierra comparison (ElevenLabs blog) — https://elevenlabs.io/hi/blog/elevenlabs-vs-sierraai
12. myaskai Sierra guide (modular voice architecture quote) — https://myaskai.com/blog/sierra-ai-complete-guide-2026
