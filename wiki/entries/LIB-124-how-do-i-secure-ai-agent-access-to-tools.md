---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-124
source_hash: sha256:207b085fc17bcce9
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [access-control, agent-security, guardrails, iam, knowledge-entry, orchestration]
related: [RIU-066, RIU-082, RIU-108]
handled_by: [architect, builder, validator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I secure AI agent access to tools, APIs, and sensitive data?

Agent security requires identity-based access control at the tool level — each agent gets its own service identity with least-privilege permissions. Use AWS Bedrock Guardrails for content-level safety (denied topics, PII filtering) and IAM roles for resource-level access control. For tool-calling agents, implement an approval layer for high-risk actions (financial transactions, data deletion, external API calls) — flag these as ONE-WAY DOOR operations requiring human confirmation. Lakera Guard adds prompt injection detection as a pre-processing firewall. HashiCorp Vault manages agent credentials with automatic rotation. Key principle — the agent should never have broader access than the human it serves.

## Definition

Agent security requires identity-based access control at the tool level — each agent gets its own service identity with least-privilege permissions. Use AWS Bedrock Guardrails for content-level safety (denied topics, PII filtering) and IAM roles for resource-level access control. For tool-calling agents, implement an approval layer for high-risk actions (financial transactions, data deletion, external API calls) — flag these as ONE-WAY DOOR operations requiring human confirmation. Lakera Guard adds prompt injection detection as a pre-processing firewall. HashiCorp Vault manages agent credentials with automatic rotation. Key principle — the agent should never have broader access than the human it serves.

## Evidence

- **Tier 1 (entry-level)**: [Fast.io: AI Agent Secrets Management Best Practices for 2026](https://fast.io/resources/ai-agent-secrets-management/)
- **Tier 1 (entry-level)**: [Auxiliobits: Secure Secret Management in Agentic AI Stacks](https://www.auxiliobits.com/blog/secure-credentials-in-agent-stacks-secret%E2%80%91management-in-aws-azure-gpu-inference-layers/)
- **Tier 1 (entry-level)**: [AI Agents in Action, Second Edition](https://www.manning.com/books/ai-agents-in-action-second-edition)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-066](../rius/RIU-066.md)
- [RIU-082](../rius/RIU-082.md)
- [RIU-108](../rius/RIU-108.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-082](../paths/RIU-082-llm-safety-guardrails.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-124.
Evidence tier: 1.
Journey stage: orchestration.
