# Voice Hub Learning Mode — Design Brief

**Status**: PARKED — build after Voice Hub v2 is stable
**Date**: 2026-04-14
**Context**: During Voice Hub v2 build, the operator realized the same taxonomy-routed retrieval that powers knowledge answers can route to enablement modules instead. The infrastructure is already built.

## The Idea

Every question already classifies to an RIU. Each RIU has both:
- A **knowledge entry** (the answer) — already wired in Voice Hub v2
- An **enablement module** (the learning path) — exists in `enablement/`, mapped to the same RIU

Two modes from the same retrieval:
1. **"Answer me"** → current behavior — pull knowledge, ground the LLM, respond
2. **"Teach me"** → route to the enablement module, walk through it conversationally via voice

## What Exists

- `palette_retrieve.py` — already classifies queries to RIUs and pulls knowledge entries
- 121 enablement curriculum modules mapped to RIUs
- Constellation system with published learning paths (RIU-021 published, others in progress)
- Content engine spec (`palette/peers/hub/` adjacent) defining learning path structure
- Enablement Coach with 7-stage onboarding and 4 adaptive interaction patterns

## What Needs Building

1. **Retrieval extension**: Add `enablement_path` field to `palette_retrieve.py` output — check if a published learning path exists for the resolved RIU
2. **Mode toggle in UI**: Either a button/toggle ("Build | Learn") or a voice command ("teach me about X" vs "how do I X")
3. **Learning system prompt**: When in learn mode, the LLM becomes a tutor — walks through the enablement module conversationally, checks understanding, adapts based on responses
4. **Possibly a separate interface**: A copy of Voice Hub stripped down for learning only — no agent selector, no bus, just learner + Palette knowledge + voice. Cleaner for demo.

## Design Questions (for when we build)

- **Split or mode toggle?** A separate learning interface is cleaner for demo. A mode toggle is more integrated for daily use. Could do both — toggle in the Hub, standalone for demo.
- **Which agent powers learning?** Claude is the best tutor. But Mistral could handle French-language learning paths. The language selector becomes a learning language selector.
- **Adaptive behavior**: The Enablement Coach already has patterns for stuck/skip/off-script/overwhelmed. Wire those into the voice tutor's system prompt.
- **Assessment**: The enablement system has 3-layer evaluation (automated → AI rubric → human). Voice adds a 4th layer: spoken assessment. "Explain back to me what you just learned."

## The Story (for Alpine and beyond)

"The same taxonomy that routes knowledge retrieval also routes learning. A developer asks 'how do I build a RAG pipeline?' and gets a grounded answer. They ask 'teach me about RAG pipelines' and get a conversational learning path — same knowledge, different mode. One ontology, two surfaces. This is the SDK for Humans."

## Files to Read When Building

- `palette/peers/hub/palette_retrieve.py` — current retrieval, extend this
- `palette/peers/hub/server.mjs` — `/api/chat` endpoint, add mode parameter
- `enablement/` — curriculum modules
- `palette/skills/education/` — adaptive learning methodology
- `palette/mission-canvas/oka.html` — OKA is already a voice-first learning agent, patterns transfer
- `memory/feedback_sdk_for_humans.md` — the positioning story

## Estimated Build Time

~3 hours on top of the working Voice Hub v2.
