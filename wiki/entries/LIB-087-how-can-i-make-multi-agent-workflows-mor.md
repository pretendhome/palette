---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-087
source_hash: sha256:0cf987f7d148d8d0
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [knowledge-entry, orchestration]
related: [RIU-530, RIU-531, RIU-532]
handled_by: [architect, debugger, narrator, validator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How can I make multi-agent workflows more readable in execution logs?


Use semantic color coding to visualize agent handoffs and coordination.

## Definition

Use semantic color coding to visualize agent handoffs and coordination.

Palette's 8 agents have semantic colors:
- Researcher: Blue 🔵 - Research/trust/water
- Builder: Orange 🟠 - Build/action/fire
- Debugger: Red 🔴 - Debug/alert/critical
- Architect: Purple 🟣 - Design/vision/architecture
- Narrator: Green 🟢 - Narrative/growth/GTM
- Validator: Gray ⚪ - Validate/stability/foundation
- Monitor: Yellow 🟡 - Signal/monitor/light
- Orchestrator: White ⚫ - Coordinate/neutral/air

In decisions.md, use colors/emojis to show workflow:
"Researcher (🔵) researched → Architect (🟣) designed → Builder (🟠) built → 
 Validator (⚪) validated → Monitor (🟡) monitored"

This improves readability by:
- Making agent roles visually distinct
- Showing handoff points clearly
- Enabling quick workflow scanning
- Reducing cognitive load when reading logs

Use when: Multi-agent engagements (3+ agents)
Skip when: Single-agent executions (unnecessary overhead)


## Evidence

- **Tier 3 (entry-level)**: Palette UX Engagement - Cross-Domain Pattern 1 (`palette/docs/PERSONA_ARTIFACT_CONVERGENCE_BRIEF_2026-02-19.md`)
- **Tier 3 (entry-level)**: [Semantic Color Coding in Developer Tools](https://www.webportfolios.dev/guides/best-color-palettes-for-developer-portfolio)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-530](../rius/RIU-530.md)
- [RIU-531](../rius/RIU-531.md)
- [RIU-532](../rius/RIU-532.md)

## Handled By

- [Architect](../agents/architect.md)
- [Debugger](../agents/debugger.md)
- [Narrator](../agents/narrator.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-087.
Evidence tier: 3.
Journey stage: orchestration.
