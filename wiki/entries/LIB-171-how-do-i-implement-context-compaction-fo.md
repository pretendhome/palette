---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-171
source_hash: sha256:6908fa71af4f1fec
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, compaction, context-management, continuity, engagement-operations, knowledge-entry, memory]
related: [RIU-003, RIU-104, RIU-607]
handled_by: [architect, builder, narrator, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I implement context compaction for long engagements to maintain continuity across sessions?

RIU-607 defines the COMPACT protocol for preserving engagement state when approaching context window limits. Trigger: initiate compaction when context usage exceeds 70% of the window, or at any natural session break in a multi-phase engagement. Phase 1 — Memory Flush: extract all canonical facts from the current session and write them to MEMORY.md. Canonical facts include: key decisions made (with rationale), current phase and status, numeric values that must not drift (metrics, counts, IDs), relationships between entities, and any corrections or clarifications from earlier in the session. Apply the "would a new person need this?" test — if yes, it goes in MEMORY.md. Phase 2 — Daily Log: write a daily log entry with: date, what was accomplished, what is in progress, blockers, and a continuation note. The continuation note answers: "If this session ends right now, what should the next session do first?" It must be specific: "Resume at Phase 3, Step 2 — the extraction schema is defined but the eval set has not been built yet. The schema is at artifacts/extraction_schema.json." Phase 3 — Decision Update: update decisions.md with any new decisions, including one-way door flags (RIU-003). Phase 4 — Next Session Start: the next session must read MEMORY.md + latest daily log + decisions.md before touching any phase artifacts. This three-file read is the minimum context needed to resume without regression. The two most common continuity failures: (1) number drift — metrics mentioned in conversation diverge from documented values over multiple sessions; (2) lost operational context — the "why" behind a decision is forgotten, leading to re-litigation. Both are prevented by consistent compaction discipline.

## Definition

RIU-607 defines the COMPACT protocol for preserving engagement state when approaching context window limits. Trigger: initiate compaction when context usage exceeds 70% of the window, or at any natural session break in a multi-phase engagement. Phase 1 — Memory Flush: extract all canonical facts from the current session and write them to MEMORY.md. Canonical facts include: key decisions made (with rationale), current phase and status, numeric values that must not drift (metrics, counts, IDs), relationships between entities, and any corrections or clarifications from earlier in the session. Apply the "would a new person need this?" test — if yes, it goes in MEMORY.md. Phase 2 — Daily Log: write a daily log entry with: date, what was accomplished, what is in progress, blockers, and a continuation note. The continuation note answers: "If this session ends right now, what should the next session do first?" It must be specific: "Resume at Phase 3, Step 2 — the extraction schema is defined but the eval set has not been built yet. The schema is at artifacts/extraction_schema.json." Phase 3 — Decision Update: update decisions.md with any new decisions, including one-way door flags (RIU-003). Phase 4 — Next Session Start: the next session must read MEMORY.md + latest daily log + decisions.md before touching any phase artifacts. This three-file read is the minimum context needed to resume without regression. The two most common continuity failures: (1) number drift — metrics mentioned in conversation diverge from documented values over multiple sessions; (2) lost operational context — the "why" behind a decision is forgotten, leading to re-litigation. Both are prevented by consistent compaction discipline.

## Evidence

- **Tier 1 (entry-level)**: [Anthropic: Context Window Management Best Practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
- **Tier 1 (entry-level)**: [Letta (formerly MemGPT): Long-Term Memory for LLM Agents](https://github.com/letta-ai/letta)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-003](../rius/RIU-003.md)
- [RIU-104](../rius/RIU-104.md)
- [RIU-607](../rius/RIU-607.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Narrator](../agents/narrator.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-171.
Evidence tier: 1.
Journey stage: all.
