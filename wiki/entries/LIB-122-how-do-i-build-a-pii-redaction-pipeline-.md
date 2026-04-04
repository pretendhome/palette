---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-122
source_hash: sha256:b95b4b4dfd88eae9
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [compliance, knowledge-entry, orchestration, pii-redaction, presidio, privacy]
related: [RIU-012, RIU-088]
handled_by: [architect, builder, validator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I build a PII redaction pipeline for AI training data and inference inputs?

Use a dedicated PII detection library — Microsoft Presidio (open-source, supports custom recognizers, runs on-premise) or AWS Comprehend PII (managed, pay-per-request). For AI pipelines, redact PII before it enters the LLM context window — this is a guardrail, not a post-processing step. Build a three-layer pipeline — detection (find PII entities), classification (determine sensitivity level), and action (redact, mask, or tokenize based on policy). Use entity-level redaction (replace names with consistent pseudonyms) rather than full removal to preserve semantic meaning for the model. Test with adversarial inputs — PII detectors miss embedded PII in code snippets, URLs, and structured data. AWS Comprehend PII detection is free when used with Bedrock Guardrails.

## Definition

Use a dedicated PII detection library — Microsoft Presidio (open-source, supports custom recognizers, runs on-premise) or AWS Comprehend PII (managed, pay-per-request). For AI pipelines, redact PII before it enters the LLM context window — this is a guardrail, not a post-processing step. Build a three-layer pipeline — detection (find PII entities), classification (determine sensitivity level), and action (redact, mask, or tokenize based on policy). Use entity-level redaction (replace names with consistent pseudonyms) rather than full removal to preserve semantic meaning for the model. Test with adversarial inputs — PII detectors miss embedded PII in code snippets, URLs, and structured data. AWS Comprehend PII detection is free when used with Bedrock Guardrails.

## Evidence

- **Tier 3 (entry-level)**: [Fast.io: AI Agent Secrets Management Best Practices](https://fast.io/resources/ai-agent-secrets-management/)
- **Tier 3 (entry-level)**: [Palette internal knowledge base](https://github.com/pretendhome/pretendhome)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-012](../rius/RIU-012.md)
- [RIU-088](../rius/RIU-088.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-122.
Evidence tier: 3.
Journey stage: orchestration.
