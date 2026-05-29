---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-192
source_hash: sha256:890caf10e47ca92a
compiled_at: 2026-05-27T22:42:24Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [knowledge-entry, multi-agent, rime-tts, specialization, tessitura, voice, voice-hub]
related: [RIU-021, RIU-505]
handled_by: [architect, researcher, validator]
journey_stage: specialization
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What is Palette's Voice Hub architecture and how does voice-first multi-agent interaction work?

Voice Hub is the primary interface to Palette — a voice-first system where users speak to coordinate multiple AI agents grounded in verified knowledge.

## Definition

Voice Hub is the primary interface to Palette — a voice-first system where users speak to coordinate multiple AI agents grounded in verified knowledge.

**Architecture**: WebSocket + HTTP server on port 7890. Web Speech STT for input, Rime TTS for output. Connected to peers bus (7899) for agent coordination and wiki/knowledge library for retrieval.

**How a voice query flows**:
 1. User speaks → Web Speech API transcribes
2. Transcription → taxonomy classification (resolver)
 3. Classification → knowledge retrieval (palette_retrieve.py)
4. Retrieved context + query → LLM provider generates response
5. Response → Rime TTS speaks the answer

**Multi-agent presence**: The Voice Hub shows which agents are 'present' in the conversation. Research queries route to Perplexity Computer. Synthesis routes to Claude. Validation routes to the validator agent. The user sees agents working as a team.

**Tessitura**: Each agent has a voice profile — pitch, pace, warmth. The voice varies by agent and context. This is not cosmetic — it helps the user distinguish who is speaking and builds trust through consistent personality.

**The pitch that works**: 'A fully integrated voice interface that allows you to be in the room with any agent you want and build as a team together.' Tested at AI Council afterhours, May 13, 2026. Highest interest spike of any framing.

## Evidence

- **Tier 3 (entry-level)**: Palette Voice Hub Server (`peers/hub/server.mjs`)
- **Tier 3 (entry-level)**: Sierra Voice Intelligence Research (`voice/SIERRA_VOICE_INTELLIGENCE.md`)
- **Tier 3 (entry-level)**: AI Council Conference Pitch Testing (`Documents/conference/CONFERENCE_WRAP_UP_2026-05-14.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-021](../rius/RIU-021.md)
- [RIU-505](../rius/RIU-505.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-021](../paths/RIU-021-tiny-ai-eval-harness.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-192.
Evidence tier: 3.
Journey stage: specialization.
