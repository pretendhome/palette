---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-117
source_hash: sha256:06e9f00f46b24ac9
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [instructor, knowledge-entry, orchestration, pydantic, schema-validation, structured-output]
related: [RIU-022, RIU-028]
handled_by: [architect, builder, validator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I enforce structured output schemas from LLMs without manual parsing?

Use a schema-constrained generation library that validates LLM output against Pydantic models or JSON Schema at inference time. Instructor (Python) wraps the LLM call and retries on validation failure — supports OpenAI, Anthropic, and open-source models. Outlines uses constrained decoding (grammar-based sampling) for guaranteed schema compliance without retries but only works with open-source models. Decision — use Instructor for cloud LLM APIs (retry-based, model-agnostic), use Outlines for self-hosted models where you control decoding. Always define output schemas as Pydantic models, not raw JSON — you get type safety, validation, and documentation for free.

## Definition

Use a schema-constrained generation library that validates LLM output against Pydantic models or JSON Schema at inference time. Instructor (Python) wraps the LLM call and retries on validation failure — supports OpenAI, Anthropic, and open-source models. Outlines uses constrained decoding (grammar-based sampling) for guaranteed schema compliance without retries but only works with open-source models. Decision — use Instructor for cloud LLM APIs (retry-based, model-agnostic), use Outlines for self-hosted models where you control decoding. Always define output schemas as Pydantic models, not raw JSON — you get type safety, validation, and documentation for free.

## Evidence

- **Tier 3 (entry-level)**: [Instructor: Validation in Instructor](https://python.useinstructor.com/concepts/validation/)
- **Tier 3 (entry-level)**: [Pydantic: How to Use Pydantic for LLMs](https://pydantic.dev/articles/llm-intro)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-022](../rius/RIU-022.md)
- [RIU-028](../rius/RIU-028.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-022](../paths/RIU-022-prompt-interface-contract.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-117.
Evidence tier: 3.
Journey stage: orchestration.
