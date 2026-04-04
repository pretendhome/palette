---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-166
source_hash: sha256:36b4901885a29a86
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [decision-rights, foundation, governance, knowledge-entry, operating-model, team-topology]
related: [RIU-001, RIU-002, RIU-600, RIU-601]
handled_by: [architect, researcher]
journey_stage: foundation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I design an AI operating model that balances centralized platform efficiency with decentralized execution speed?

RIU-601 defines the AI operating model through four structural decisions. Decision 1 — Team Topology: choose between three models. Centralized CoE: one AI team serves all business units. Best for: small organizations (< 500 employees) or early AI maturity. Risk: bottleneck, disconnected from business needs. Federated: each business unit has its own AI team. Best for: diverse business units with different needs. Risk: duplication, inconsistent standards. Hub-and-Spoke (recommended for most): central platform team (hub) provides infrastructure, MLOps, guardrails, and standards. Business unit AI teams (spokes) build use cases on the shared platform. The hub does not build use cases; the spokes do not build infrastructure. Decision 2 — Decision Rights Matrix: explicitly document who decides what. Platform decisions (cloud provider, MLOps tooling, security standards): central team. Use case prioritization: business unit. Model selection for a specific use case: business unit AI team within platform guardrails. Budget allocation: central team sets platform budget; business units set use case budgets. Decision 3 — Escalation Paths: define what happens when central and federated teams disagree. Common conflicts: business unit wants a tool not on the approved list, business unit wants to deploy a model that fails guardrails, two business units want conflicting platform changes. Resolve via the AI council (monthly) or VP-level escalation (urgent). Decision 4 — Shadow AI Prevention: business units will build AI outside the platform if the platform is too slow or restrictive. Prevent by: making the platform easy to use, providing self-service capabilities, and measuring time-to-first-model as a platform KPI.

## Definition

RIU-601 defines the AI operating model through four structural decisions. Decision 1 — Team Topology: choose between three models. Centralized CoE: one AI team serves all business units. Best for: small organizations (< 500 employees) or early AI maturity. Risk: bottleneck, disconnected from business needs. Federated: each business unit has its own AI team. Best for: diverse business units with different needs. Risk: duplication, inconsistent standards. Hub-and-Spoke (recommended for most): central platform team (hub) provides infrastructure, MLOps, guardrails, and standards. Business unit AI teams (spokes) build use cases on the shared platform. The hub does not build use cases; the spokes do not build infrastructure. Decision 2 — Decision Rights Matrix: explicitly document who decides what. Platform decisions (cloud provider, MLOps tooling, security standards): central team. Use case prioritization: business unit. Model selection for a specific use case: business unit AI team within platform guardrails. Budget allocation: central team sets platform budget; business units set use case budgets. Decision 3 — Escalation Paths: define what happens when central and federated teams disagree. Common conflicts: business unit wants a tool not on the approved list, business unit wants to deploy a model that fails guardrails, two business units want conflicting platform changes. Resolve via the AI council (monthly) or VP-level escalation (urgent). Decision 4 — Shadow AI Prevention: business units will build AI outside the platform if the platform is too slow or restrictive. Prevent by: making the platform easy to use, providing self-service capabilities, and measuring time-to-first-model as a platform KPI.

## Evidence

- **Tier 1 (entry-level)**: [Matthew Skelton and Manuel Pais: Team Topologies (2019)](https://teamtopologies.com/)
- **Tier 1 (entry-level)**: [AWS CAF: People Perspective — Operating Model](https://aws.amazon.com/cloud-adoption-framework/)
- **Tier 1 (entry-level)**: [Gartner: AI Center of Excellence Framework](https://www.gartner.com/en/information-technology/glossary/center-of-excellence-coe)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-002](../rius/RIU-002.md)
- [RIU-600](../rius/RIU-600.md)
- [RIU-601](../rius/RIU-601.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise
- [RIU-600](../paths/RIU-600-multi-brand-ai-strategy.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-166.
Evidence tier: 1.
Journey stage: foundation.
