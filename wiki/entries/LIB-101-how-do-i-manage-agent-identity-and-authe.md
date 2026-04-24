---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-101
source_hash: sha256:a20c0f06864f17f8
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [knowledge-entry, orchestration]
related: [RIU-105]
handled_by: [narrator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I manage agent identity and authentication?

Agents are a new class of principal (distinct from users and services).

## Definition

Agents are a new class of principal (distinct from users and services).
Each agent needs verifiable identity for access control and audit.

Three types of principals:
1. Users: Authenticated with OAuth/SSO (human actors, full autonomy)
2. Agents: Verified with SPIFFE or similar (delegated authority)
3. Service accounts: IAM-managed (deterministic applications)

Agent identity requirements:
- Cryptographically verifiable (e.g., SPIFFE, mTLS)
- Distinct from user who invoked it
- Distinct from developer who built it
- Granular permissions (least privilege per agent role)
- Auditable (all actions traceable to agent identity)

Why this matters:
- Enables audit trails (which agent did what, when, why)
- Limits blast radius if agent is compromised
- Allows delegation of authority (agent acts on behalf of user)
- Supports compliance requirements (SOC2, GDPR, HIPAA)

Implementation pattern:
1. Issue unique identity to each agent instance
2. Map identity to role-based permissions
3. Validate identity before every tool invocation
4. Log all actions with agent identity + timestamp
5. Rotate credentials regularly

Example: SalesAgent gets CRM read/write access. HRAgent explicitly denied.
If SalesAgent is compromised, HR data remains protected.

Palette integration:
- Each agent archetype (Researcher, Architect, Builder, etc.) has default permission profile
- Instances inherit profile but can be further restricted
- Architect designs identity architecture for multi-agent systems
- Validator validates identity implementation meets security requirements


## Evidence

- **Tier 1 (entry-level)**: [Google Introduction to Agents (Nov 2025) - Agent Identity section](https://cloud.google.com/use-cases/agents)
- **Tier 1 (entry-level)**: [SPIFFE standard](https://spiffe.io)
- **Tier 1 (entry-level)**: Palette Tier 2 - Agent Security section (`palette/.steering/assumptions.md#agent-security`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-105](../rius/RIU-105.md)

## Handled By

- [Narrator](../agents/narrator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-101.
Evidence tier: 1.
Journey stage: orchestration.
