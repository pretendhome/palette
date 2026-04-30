---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-089
source_hash: sha256:a354c7cbd562f4ab
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [knowledge-entry, orchestration]
related: [RIU-105]
handled_by: [narrator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I implement least privilege for AI agents?

Agents should only have access to resources required for their specific role.

## Definition

Agents should only have access to resources required for their specific role.

Principles:
- Grant minimum permissions needed to accomplish the task
- Separate agent identity from user identity and service accounts
- Use role-based access control (RBAC) for agent permissions
- Audit and log all agent actions for accountability

Implementation:
- Define agent roles with explicit permission boundaries
- Use policy engines to enforce constraints outside model reasoning
- Implement "before_tool" callbacks to validate parameters
- Require explicit approval for elevated permissions

Example: Research agent (Researcher) gets read-only database access. 
Build agent (Builder) gets write access only to /src directory.
Architecture agent (Architect) designs security posture but cannot execute.

Blast radius containment:
If one agent is compromised, damage is limited to its permission scope.


## Evidence

- **Tier 1 (entry-level)**: [Google Introduction to Agents (Nov 2025) - Agent Identity section](https://cloud.google.com/use-cases/agents)
- **Tier 1 (entry-level)**: [SPIFFE standard for agent identity](https://spiffe.io)
- **Tier 1 (entry-level)**: Palette Tier 2 - Agent Security section (`palette/.steering/assumptions.md#agent-security`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-105](../rius/RIU-105.md)

## Handled By

- [Narrator](../agents/narrator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-089.
Evidence tier: 1.
Journey stage: orchestration.
