# Voice Evaluation Workbench — MVP Spec

Date: 2026-04-15
Purpose: Build a single-page demo that pescribed, with those three adjustments. One HTML file. Rime TTS via 
the Hub's existing /api/tts proxy. 4 languages × 4 voices × 3 journey stages (Acceptance/
Resolution/Satisfactionroves immediate fit for Sierra's voice evaluation work.

## Product Definition

Voice Evaluation Workbench is a multilingual evaluation tool that helps teams compare, score, and choose the right AI agent voice for each customer journey stage.

Core question:

> For this journey stage and language, which voice should we ship, and why?

This is not:

- a chatbot
- a multi-agent demo
- a persona playground
- a general voice app

This is:

- a decision tool
- a repeatable evaluation framework
- a lightweight artifact a product/design/engineering team could actually use

## Why This Demo

This demo is designed to map directly to the role:

- voice evaluation, not just voice generation
- multilingual judgment, not just English polish
- structured scoring, not just taste
- recommendation output, not just audio playback
- a usable internal tool, not a speculative concept piece

It should communicate:

- I know what should be evaluated
- I can make voice quality judgment repeatable
- I can work across languages
- I can turn subjective assessment into a decision artifact

## MVP Goal

A reviewer should be able to open the page and, within 60 seconds:

1. understand what the tool does
2. compare several voices on the same phrase
3. score them using a structured rubric
4. leave with a recommendation

## Scope

### In Scope

- one-page interface
- 4 languages: EN, FR, IT, ES
- 3 journey stages: Acceptance, Resolution, Satisfaction
- 4 persona targets
- 3-4 voice variants
- custom phrase input
- audio playback per voice
- scoring rubric
- weighted score calculation
- recommendation output
- exportable scorecard

### Out of Scope

- login/auth
- database
- collaboration features
- live customer conversation
- LLM orchestration
- auto-generated cultural analysis
- speculative "AI persona generation"
- fake controls unsupported by the TTS system

## User Story

As a voice/product designer, I want to evaluate multiple voice options for a specific customer moment in a specific language, so I can choose the best voice with a documented rationale.

## Core User Flow

1. Select journey stage
2. Select persona target
3. Select language
4. Use default phrase or enter custom phrase
5. Click `Generate Comparison`
6. Hear 3-4 voice variants side by side
7. Score each voice
8. Review recommendation
9. Export scorecard

## Information Architecture

### Left Panel: Setup

- journey stage selector
- persona selector
- language selector
- phrase input
- `Generate Comparison` button
- `Reset` button

### Center Panel: Voice Comparison

Show 3-4 voice cards.

Each voice card includes:

- voice name
- short descriptor
- play button
- loading state
- ready/error state
- score summary

### Right Panel: Evaluation

- detailed scoring controls for selected voice
- freeform evaluator notes
- weighted total
- comparison table
- recommended winner
- export button

### Bottom Section: Context + Decision

- locale watchouts
- short recommendation summary
- ship / not yet indicator

## Experience Principles

- extremely clear purpose
- minimal interface clutter
- fast feedback
- obvious comparison workflow
- decision-first, not entertainment-first
- serious internal-tool tone

## Journey Stages

Use Sierra's language directly.

### Acceptance

Definition:
First impression. The voice should make the user feel safe continuing.

Evaluation focus:

- warmth
- clarity
- immediate trust
- emotional permission to continue

### Resolution

Definition:
The voice is helping solve or explain something.

Evaluation focus:

- composure
- pacing
- clarity under longer explanation
- confidence without coldness

### Satisfaction

Definition:
The voice is closing the loop and leaving the user in a resolved state.

Evaluation focus:

- reassurance
- completion
- confidence
- clean emotional landing

## Persona Targets

These shape evaluator expectations and recommendation framing. They do not require a separate backend model.

- Warm guide
- Technical expert
- Luxury concierge
- Calm resolver

## Languages

- EN
- FR
- IT
- ES

## Voice Set

Use only voices already available and stable via the existing TTS layer.

For MVP:

- 3-4 voices maximum
- stable mapping
- clearly labeled
- distinct enough to compare meaningfully

Example placeholder labels:

- Voice A
- Voice B
- Voice C
- Voice D

If using existing Rime-backed voices, keep the mapping fixed across the tool.

## Phrase Strategy

The evaluator can either:

- use a default phrase tied to the selected journey stage and language
- enter a custom phrase

### Default Phrases

#### Acceptance

- EN: Hi, I'm here to help you get this resolved quickly.
- FR: Bonjour, je suis là pour vous aider à régler cela rapidement.
- IT: Ciao, sono qui per aiutarti a risolvere tutto rapidamente.
- ES: Hola, estoy aquí para ayudarte a resolver esto rápidamente.

#### Resolution

- EN: I found the issue and I'll walk you through the next step.
- FR: J'ai identifié le problème et je vais vous guider pour la suite.
- IT: Ho individuato il problema e ti guiderò nel prossimo passaggio.
- ES: He identificado el problema y te guiaré en el siguiente paso.

#### Satisfaction

- EN: Everything is confirmed, and you're all set.
- FR: Tout est confirmé, et tout est prêt de votre côté.
- IT: È tutto confermato ed è tutto pronto.
- ES: Todo está confirmado y ya está listo.

## Scoring Rubric

Each voice is scored from 1 to 5 on:

- Naturalness
- Trust
- Brand fit
- Cultural fit
- Clarity

Optional final binary:

- Ship
- Not yet

### Rubric Definitions

#### Naturalness

Does the voice sound fluid, well-paced, and non-robotic?

#### Trust

Would a customer feel comfortable continuing with this voice?

#### Brand Fit

Does the voice match the intended persona and journey stage?

#### Cultural Fit

Does the delivery feel appropriate for this language and context?

#### Clarity

Is the message easy to understand on first listen?

## Weighting

Use weighted scoring for the recommendation.

- Naturalness: 30%
- Trust: 25%
- Cultural fit: 20%
- Brand fit: 15%
- Clarity: 10%

Weighted score formula:

```text
total =
  naturalness * 0.30 +
  trust * 0.25 +
  cultural_fit * 0.20 +
  brand_fit * 0.15 +
  clarity * 0.10
```

## Locale Watchouts

These should be short, curated, and human-authored.

### FR

- Avoid over-bright enthusiasm.
- Warmth should still feel composed and credible.

### IT

- Pace matters; clipped delivery can feel cold.
- Musicality and phrasing affect perceived warmth.

### ES

- Neutral register matters.
- Literal translation can sound regionally awkward.

### EN

- Calm pacing often matters more than friendliness alone.
- Over-smiling delivery can reduce credibility in support moments.

## Recommendation Logic

The system should produce a recommendation based on:

- weighted score
- evaluator notes
- journey stage
- persona target
- locale watchout context

Output format:

- top-ranked voice
- total score
- short rationale
- one watchout
- ship / not yet recommendation

### Example Recommendation

Voice B is the strongest choice for French Acceptance because it balances warmth and clarity without sounding over-performative. Ship for welcome flows; avoid using it for long technical explanations.

## Export

For MVP, export a markdown scorecard.

### Export Fields

- date/time
- journey stage
- persona
- language
- phrase
- voices evaluated
- score breakdown
- winning voice
- recommendation
- evaluator notes

### Export Example

```md
# Voice Evaluation Scorecard

Stage: Acceptance
Persona: Luxury concierge
Language: FR
Phrase: Bonjour, je suis là pour vous aider à régler cela rapidement.

## Scores
- Voice A: 3.9
- Voice B: 4.6
- Voice C: 4.1
- Voice D: 3.7

## Recommendation
Voice B is the strongest choice for French Acceptance because it balances warmth and clarity without sounding over-performative.

## Watchouts
- Avoid overly bright delivery in French hospitality contexts.

## Evaluator Notes
- Voice B feels premium without becoming stiff.
- Voice D is clear but too synthetic.
```

## Technical Approach

Use the existing local toolchain where possible.

### Frontend

- static HTML
- CSS
- vanilla JavaScript

### Audio Generation

Use the existing TTS proxy rather than exposing credentials in the browser.

Preferred path:

- existing `/api/tts` proxy from the current hub system

Avoid:

- direct browser API calls that expose keys

### Persistence

- local in-memory state only for MVP
- export/download instead of database persistence

## UI States

### Global States

- idle
- generating
- ready
- partial error

### Voice Card States

- idle
- loading
- playable
- failed

### Evaluation States

- not started
- partially scored
- fully scored
- recommendation ready

## MVP Component List

### Required Components

- stage selector
- persona selector
- language selector
- phrase input
- generate button
- voice comparison grid
- audio playback controls
- score form
- recommendation panel
- locale watchout panel
- export button

### Nice-to-Have But Optional

- visual score bars
- compact comparison matrix
- copy-to-clipboard export
- reset scores per voice

## Success Criteria

The MVP is successful if:

- the tool is understandable in under 30 seconds
- the comparison workflow feels obvious
- audio playback is reliable
- scoring is fast and frictionless
- the recommendation feels credible
- the exported scorecard looks like something a real team would use

## Build Constraints

- one page only
- must work without install for the reviewer
- must stay focused on voice evaluation
- should feel like an internal product/design tool, not a toy
- should avoid any claim that cannot be demonstrated directly

## Positioning For Application

This demo should be framed as:

> A multilingual voice evaluation workbench for comparing, scoring, and choosing the right AI agent voice for each customer journey stage.

What it proves:

- evaluative rigor
- multilingual sensitivity
- framework design
- decision tooling
- immediate applicability to Sierra's workflow

## Explicit Product Boundaries

Do not present this as:

- a full Voice Hub replacement
- a customer-facing product
- a general AI persona generator
- an automated cultural intelligence engine

Present it as:

- a focused evaluation tool
- a repeatable framework
- a credible day-1 artifact for voice quality work

## Build Order

1. Static layout
2. Selectors + default phrase logic
3. TTS generation + audio playback
4. Voice card rendering
5. Scoring UI
6. Weighted score calculation
7. Recommendation panel
8. Export
9. Final polish

## Final One-Line Product Description

Mission Canvas is a voice-first workspace where coordinated AI agents turn messy intent into decisions, deliverables, and persistent project memory.

Separate one-line description for this demo:

Voice Evaluation Workbench is a multilingual tool that helps teams compare, score, and choose the right AI agent voice for each customer journey stage.
