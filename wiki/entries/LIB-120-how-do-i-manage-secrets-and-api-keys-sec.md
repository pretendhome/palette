---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-120
source_hash: sha256:595ff01070f3c5f4
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [api-keys, credentials, knowledge-entry, orchestration, secrets-management, security]
related: [RIU-066, RIU-108]
handled_by: [architect, builder, validator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I manage secrets and API keys securely for AI agent workflows?

Never store secrets in code, environment variables, or config files. Use a secrets manager — AWS Secrets Manager for AWS-native workflows (automatic rotation, IAM integration), HashiCorp Vault for multi-cloud or on-premise. For AI agents specifically, each agent should have its own IAM role or service account with least-privilege access. Rotate API keys on a schedule (90 days minimum). Use short-lived credentials (STS AssumeRole) instead of long-lived keys wherever possible. Agent credential access should be auditable — log which agent accessed which secret and when. Decision — if you are AWS-only, use Secrets Manager. If multi-cloud or complex rotation policies, use Vault.

## Definition

Never store secrets in code, environment variables, or config files. Use a secrets manager — AWS Secrets Manager for AWS-native workflows (automatic rotation, IAM integration), HashiCorp Vault for multi-cloud or on-premise. For AI agents specifically, each agent should have its own IAM role or service account with least-privilege access. Rotate API keys on a schedule (90 days minimum). Use short-lived credentials (STS AssumeRole) instead of long-lived keys wherever possible. Agent credential access should be auditable — log which agent accessed which secret and when. Decision — if you are AWS-only, use Secrets Manager. If multi-cloud or complex rotation policies, use Vault.

## Evidence

- **Tier 3 (entry-level)**: [Fast.io: AI Agent Secrets Management Best Practices for 2026](https://fast.io/resources/ai-agent-secrets-management/)
- **Tier 3 (entry-level)**: [GitGuardian: Top Secrets Management Tools for 2026](https://blog.gitguardian.com/top-secrets-management-tools-for-2024/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-066](../rius/RIU-066.md)
- [RIU-108](../rius/RIU-108.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-120.
Evidence tier: 3.
Journey stage: orchestration.
