---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-189
source_hash: sha256:8ee77121e3114fdf
compiled_at: 2026-05-15T15:33:55Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [enablement, knowledge-entry, learning-mode, sdk-for-humans, specialization, tessitura, voice]
related: [RIU-021, RIU-022]
handled_by: [architect, builder, validator]
journey_stage: specialization
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How does Voice Hub Learning Mode work and what is the teach-while-doing pattern?

Voice Hub Learning Mode adds a second surface to the same retrieval infrastructure. The same taxonomy routing and knowledge library that answers questions can also TEACH about the domain.

## Definition

Voice Hub Learning Mode adds a second surface to the same retrieval infrastructure. The same taxonomy routing and knowledge library that answers questions can also TEACH about the domain.

**Two modes from one system**:
- 'Answer me' → performance support. Pull knowledge, ground the LLM, respond with the answer. Current behavior.
- 'Teach me' → learning mode. Route to the enablement module mapped to the same RIU, walk through it conversationally via voice.

 **How it works**: Every RIU already maps to both a knowledge entry (the answer) and an enablement module (the learning path). The mode toggle determines which surface gets activated. Detection is via voice command ('teach me about X' vs 'how do I X') or UI toggle.

**The SDK for Humans thesis**: Users learn how to do things AS they do them. The system doesn't just make you more efficient — it makes you more capable. After the interaction, you understand the domain better, not just the answer.

**Tessitura**: In learning mode, the voice adapts — slower pace, more check-for-understanding pauses, Socratic questioning. This is the tessitura concept: each agent has a voice personality that varies by context.

## Evidence

- **Tier 3 (entry-level)**: Voice Hub Learning Mode Design Brief (`.steering/claude-code/VOICE_HUB_LEARNING_MODE.md`)
- **Tier 3 (entry-level)**: [AI Council Keynote — 'Education is the next frontier. We learn through failing.'](https://aicouncil.com)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-021](../rius/RIU-021.md)
- [RIU-022](../rius/RIU-022.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-021](../paths/RIU-021-tiny-ai-eval-harness.md) — hands-on exercise
- [RIU-022](../paths/RIU-022-prompt-interface-contract.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-189.
Evidence tier: 3.
Journey stage: specialization.
