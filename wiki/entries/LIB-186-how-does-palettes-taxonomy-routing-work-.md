---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-186
source_hash: sha256:b212f26e189c8b37
compiled_at: 2026-05-27T22:42:24Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 2
tags: [context-selection, foundation, information-retrieval, knowledge-entry, routing, taxonomy]
related: [RIU-001, RIU-200]
handled_by: [architect, narrator, researcher]
journey_stage: foundation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How does Palette's taxonomy routing work and why does it classify before retrieving?

Palette uses a 121-node taxonomy of Reusable Intelligence Units (RIUs) to classify every incoming problem BEFORE retrieval happens. This is the 'context selection, not context accumulation' principle. Instead of searching everything and filtering results, the taxonomy narrows the domain first, then retrieval operates within that domain only.

## Definition

Palette uses a 121-node taxonomy of Reusable Intelligence Units (RIUs) to classify every incoming problem BEFORE retrieval happens. This is the 'context selection, not context accumulation' principle. Instead of searching everything and filtering results, the taxonomy narrows the domain first, then retrieval operates within that domain only.

1. **How it works**: User input → resolver agent classifies to an RIU → RIU determines which knowledge domain, which agent type, and which retrieval scope. The router never searches the full 176-entry knowledge library for every query.

2. **Why classify first**: (a) Reduces irrelevant context entering the prompt (token efficiency). (b) Increases signal-to-noise ratio. (c) Makes routing deterministic — same input → same RIU → same agent. (d) Aligns with IR fundamentals from 1968: 'seek over well-designed representations with specific patterns.'

3. **The 121 RIUs** are organized by 6 workstreams (Clarify & Bound, Interfaces & Inputs, Core Logic, Quality & Safety, Ops & Delivery, Adoption & Change) and 4 journey stages (foundation, retrieval, orchestration, specialization). Each RIU maps to specific agent types and knowledge entries.

**Key insight**: Taxonomy routing is the smallest system that provides context selection. It is deterministic, auditable, and requires zero LLM calls.

## Evidence

- **Tier 2 (entry-level)**: Palette Taxonomy v1.3 (`taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml`)
- **Tier 2 (entry-level)**: [Linus Lee, Thrive Capital — 'Push context to data structures, AS MUCH AS POSSIBLE'](https://aicouncil.com)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-200](../rius/RIU-200.md)

## Handled By

- [Architect](../agents/architect.md)
- [Narrator](../agents/narrator.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-186.
Evidence tier: 2.
Journey stage: foundation.
