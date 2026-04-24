---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-147
source_hash: sha256:804a122fd5845f5d
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, continuity, handoff, knowledge-entry, knowledge-transfer, restartability]
related: [RIU-003, RIU-104, RIU-607]
handled_by: [architect, builder, narrator, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I create a handoff bundle that enables restartability when an engagement transitions to a new team or person?

RIU-104 defines the handoff bundle as a package with five mandatory sections. Section 1 — State Summary: a 1-2 page narrative covering what was accomplished, what is in progress, and what is not started. Written for someone with zero prior context. Include the current phase, completion percentage, and any deadlines. Section 2 — Decision Log: the complete decisions.md with all decisions made, their rationale, who approved them, and which are one-way doors (RIU-003). This is the most critical section — decisions are the hardest knowledge to reconstruct. Section 3 — Open Questions: a prioritized list of unresolved questions, blocked items, and pending decisions. For each, note who owns the resolution and any known constraints. Section 4 — Artifact Inventory: a manifest of all artifacts produced, their locations, versions, and status (draft, reviewed, approved). Include links/paths to every document, code repository, configuration file, and dataset. Section 5 — Next Steps: a concrete list of the next 5-10 actions the successor should take, in order, with estimated effort. Include any context needed for each action. Common failure mode: implicit knowledge not captured — the outgoing person knows things that are not written down. Mitigate by having the successor attempt a "cold start" using only the bundle and report gaps before the outgoing person leaves. This gap analysis is the most valuable quality check.

## Definition

RIU-104 defines the handoff bundle as a package with five mandatory sections. Section 1 — State Summary: a 1-2 page narrative covering what was accomplished, what is in progress, and what is not started. Written for someone with zero prior context. Include the current phase, completion percentage, and any deadlines. Section 2 — Decision Log: the complete decisions.md with all decisions made, their rationale, who approved them, and which are one-way doors (RIU-003). This is the most critical section — decisions are the hardest knowledge to reconstruct. Section 3 — Open Questions: a prioritized list of unresolved questions, blocked items, and pending decisions. For each, note who owns the resolution and any known constraints. Section 4 — Artifact Inventory: a manifest of all artifacts produced, their locations, versions, and status (draft, reviewed, approved). Include links/paths to every document, code repository, configuration file, and dataset. Section 5 — Next Steps: a concrete list of the next 5-10 actions the successor should take, in order, with estimated effort. Include any context needed for each action. Common failure mode: implicit knowledge not captured — the outgoing person knows things that are not written down. Mitigate by having the successor attempt a "cold start" using only the bundle and report gaps before the outgoing person leaves. This gap analysis is the most valuable quality check.

## Evidence

- **Tier 1 (entry-level)**: [AWS CAF: People Perspective — Knowledge Management](https://aws.amazon.com/cloud-adoption-framework/)
- **Tier 1 (entry-level)**: [Atlassian: Project Handoff Best Practices](https://www.atlassian.com/work-management/project-management)

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

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-147.
Evidence tier: 1.
Journey stage: all.
