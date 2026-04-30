---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-093
source_hash: sha256:e683043ef7a2ff83
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [all, architecture, decision-framework, knowledge-entry, one-way-door, risk-management]
related: [RIU-001, RIU-003]
handled_by: [architect, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I identify ONE-WAY DOOR decisions in AI and game development?

ONE-WAY DOOR decisions are irreversible or high-cost to undo. Per Palette Tier 1:

## Definition

ONE-WAY DOOR decisions are irreversible or high-cost to undo. Per Palette Tier 1:

**ONE-WAY DOOR Indicators**:
- "This will affect every system we build"
- "Changing this later requires rewriting X"
- "This locks us into vendor Y"
- "This determines our scaling limits"
- "This affects our cost structure permanently"

**AI/ML ONE-WAY DOORS**:
- Ethical AI guidelines and data governance frameworks
- Model architecture selection (fine-tuning vs RAG vs prompt engineering)
- Production deployment commitments
- Database schema for ML features
- Compliance framework selection (EU AI Act, HIPAA, SOX)

**Game Development ONE-WAY DOORS**:
- Game engine selection (Godot vs Unity vs Unreal)
- Network architecture (client-server vs P2P)
- Database choice (PostgreSQL vs MongoDB vs DynamoDB)
- Authentication system (OAuth, JWT, custom)
- Core game mechanics structure (affects all future content)
- Deployment platform (web vs native vs hybrid)

**TWO-WAY DOOR Examples** (easily reversible):
- Hyperparameter tuning
- Prompt iterations
- UI framework choice
- Logging library
- Asset organization
- Development workflow

**Protocol**:
1. **Flag explicitly**: "🚨 ONE-WAY DOOR — confirmation required before proceeding"
2. **Pause execution**: Human confirmation mandatory
3. **Log in decisions.md**: Must include explicit rationale
4. **Toolkit-changing decisions**: Also add to manual header list in decisions.md

**When uncertain**: Treat as ONE-WAY DOOR (safer to over-flag than under-flag)

**From Palette implementation**:
- Agent archetype selection was ONE-WAY DOOR (affects all future agent design)
- Fixture format was ONE-WAY DOOR (establishes validation pattern)
- Researcher's clarification protocol was TWO-WAY DOOR (can iterate on questions)


## Evidence

- **Tier 3 (entry-level)**: Palette Tier 1 - Decision Handling (`palette/.steering/palette-core.md`)
- **Tier 3 (entry-level)**: Palette Tier 2 - Decision Safety Model (`palette/.steering/assumptions.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-003](../rius/RIU-003.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-093.
Evidence tier: 3.
Journey stage: all.
