---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-172
source_hash: sha256:b1d5fb9cf3353d15
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, coordination, engagement-operations, knowledge-entry, multi-agent, orchestration, workflow]
related: [RIU-029, RIU-087, RIU-607, RIU-608]
handled_by: [architect, builder, narrator, orchestrator, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I define a typed workflow for multi-agent engagements that makes implicit coordination explicit?

RIU-608 defines a YAML-based workflow format for multi-agent engagements. Structure: a workflow has five top-level sections. Section 1 — Phases: ordered list of engagement phases. Each phase has: name, description, assigned agents (primary + supporting), estimated duration, entry criteria (what must be true to start this phase), and exit criteria (what must be true to complete this phase). Phases execute sequentially by default; mark phases as parallelizable if they have no dependencies. Section 2 — Agent Assignments: for each agent, document: role in this engagement, phases they participate in, tools they are authorized to use (cross-reference RIU-029), and handoff protocol (how they pass work to the next agent). Section 3 — Quality Gates: define checkpoints between phases where an Validator (validator) agent reviews the work product. Each gate has: what is being validated, acceptance criteria, and what happens if validation fails (rework, escalate, or skip with documented risk acceptance). Section 4 — Decision Checkpoints: points where a human must make a decision before the workflow can proceed. Flag one-way door decisions (RIU-087). Include the information the human needs to make the decision and the deadline. Section 5 — Memory Update Expectations: define when MEMORY.md must be updated (at minimum: after each phase completion, after each quality gate, and after each decision checkpoint). The workflow is a living document — update it when the engagement pivots. The anti-pattern is defining a rigid workflow that blocks necessary pivots. Build in explicit "reassess workflow" checkpoints every 2-3 phases. Validate the workflow with Validator before the engagement begins.

## Definition

RIU-608 defines a YAML-based workflow format for multi-agent engagements. Structure: a workflow has five top-level sections. Section 1 — Phases: ordered list of engagement phases. Each phase has: name, description, assigned agents (primary + supporting), estimated duration, entry criteria (what must be true to start this phase), and exit criteria (what must be true to complete this phase). Phases execute sequentially by default; mark phases as parallelizable if they have no dependencies. Section 2 — Agent Assignments: for each agent, document: role in this engagement, phases they participate in, tools they are authorized to use (cross-reference RIU-029), and handoff protocol (how they pass work to the next agent). Section 3 — Quality Gates: define checkpoints between phases where an Validator (validator) agent reviews the work product. Each gate has: what is being validated, acceptance criteria, and what happens if validation fails (rework, escalate, or skip with documented risk acceptance). Section 4 — Decision Checkpoints: points where a human must make a decision before the workflow can proceed. Flag one-way door decisions (RIU-087). Include the information the human needs to make the decision and the deadline. Section 5 — Memory Update Expectations: define when MEMORY.md must be updated (at minimum: after each phase completion, after each quality gate, and after each decision checkpoint). The workflow is a living document — update it when the engagement pivots. The anti-pattern is defining a rigid workflow that blocks necessary pivots. Build in explicit "reassess workflow" checkpoints every 2-3 phases. Validate the workflow with Validator before the engagement begins.

## Evidence

- **Tier 1 (entry-level)**: [Anthropic: Multi-Agent Orchestration Patterns](https://docs.anthropic.com/en/docs/build-with-claude/agent-patterns)
- **Tier 1 (entry-level)**: [AWS Step Functions: Workflow Studio](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html)
- **Tier 1 (entry-level)**: [CrewAI: Multi-Agent Framework Design Patterns](https://docs.crewai.com/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-029](../rius/RIU-029.md)
- [RIU-087](../rius/RIU-087.md)
- [RIU-607](../rius/RIU-607.md)
- [RIU-608](../rius/RIU-608.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Narrator](../agents/narrator.md)
- [Orchestrator](../agents/orchestrator.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-172.
Evidence tier: 1.
Journey stage: all.
