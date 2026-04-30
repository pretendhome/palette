---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-131
source_hash: sha256:f10633324f38fedc
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [brand-safety, content-moderation, guardrails, knowledge-entry, specialization, trust]
related: [RIU-082, RIU-606]
handled_by: [architect, builder, validator]
journey_stage: specialization
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I ensure AI-generated content is brand-safe before publishing?

Use AWS Bedrock Guardrails for automated brand safety enforcement — denied topic detection, custom word filters, and content filters across 6 harm categories. Configure guardrails as a mandatory post-processing step on all AI-generated content before it reaches end users. For advanced brand voice compliance, Guardrails AI (open-source) offers composable validators including tone, formality, and custom brand rules. Lakera Guard adds adversarial defense against prompt injection that could bypass brand guidelines. Key pattern — defense in depth. System prompt sets brand voice, guardrails enforce it, and human review gates the highest-visibility content. Automate the 90 percent of content that is clearly safe, human-review the 10 percent that triggers edge-case flags.

## Definition

Use AWS Bedrock Guardrails for automated brand safety enforcement — denied topic detection, custom word filters, and content filters across 6 harm categories. Configure guardrails as a mandatory post-processing step on all AI-generated content before it reaches end users. For advanced brand voice compliance, Guardrails AI (open-source) offers composable validators including tone, formality, and custom brand rules. Lakera Guard adds adversarial defense against prompt injection that could bypass brand guidelines. Key pattern — defense in depth. System prompt sets brand voice, guardrails enforce it, and human review gates the highest-visibility content. Automate the 90 percent of content that is clearly safe, human-review the 10 percent that triggers edge-case flags.

## Evidence

- **Tier 3 (entry-level)**: [Palette internal knowledge base](https://github.com/pretendhome/pretendhome)
- **Tier 3 (entry-level)**: FDE field experience (`internal`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-082](../rius/RIU-082.md)
- [RIU-606](../rius/RIU-606.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-082](../paths/RIU-082-llm-safety-guardrails.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-131.
Evidence tier: 3.
Journey stage: specialization.
