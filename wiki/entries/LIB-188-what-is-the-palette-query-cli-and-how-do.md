---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-188
source_hash: sha256:3bdce595d4d2884b
compiled_at: 2026-05-15T15:33:55Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [behavioral-structure, cli, governance, knowledge-entry, orchestration, traceability]
related: [RIU-001, RIU-513]
handled_by: [architect, builder, researcher]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What is the palette query CLI and how does it enforce behavioral structure for agents?

The `palette query` command is a single CLI entry point that runs the full agent chain with five internal steps, each logged and traceable:

## Definition

The `palette query` command is a single CLI entry point that runs the full agent chain with five internal steps, each logged and traceable:

1. **resolve**: Taxonomy classification — maps the query to an RIU.
2. **retrieve**: Hybrid search — FTS5 + vector + keyword across the knowledge library within the classified domain.
3. **route**: Agent selection — picks the right agent based on RIU agent_types and trust tiers.
4. **respond**: Agent invocation — the selected agent generates a response grounded in retrieved knowledge.
5. **extract**: Memory candidate — if the response contains a high-confidence fact, propose it for governance review.

All five steps route through the peers bus as registered messages. The CLI is a bus CLIENT, not a bypass — every command produces a governed envelope.

**Why this matters**: The sequence IS the intelligence. By making execution order explicit and logged, the system becomes reproducible (same query → same path), debuggable (which step failed?), and compliant (did the agent follow the prescribed sequence?).

 **Design principle**: One command. Five steps. Logged. Traceable. Bus-routed.

## Evidence

- **Tier 1 (entry-level)**: Kiro V3 Feedback — CLI scope recommendation (`Documents/conference/V3_FEEDBACK_kiro.md`)
- **Tier 1 (entry-level)**: [Linus Lee, Thrive Capital — Hobgoblin CLI architecture](https://aicouncil.com)
- **Tier 1 (entry-level)**: [Anthropic — Claude Code CLI architecture and tool patterns](https://docs.anthropic.com/en/docs/claude-code)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-513](../rius/RIU-513.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-188.
Evidence tier: 1.
Journey stage: orchestration.
