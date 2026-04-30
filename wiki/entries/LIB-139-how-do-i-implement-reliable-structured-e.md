---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-139
source_hash: sha256:5b0db68c4d077e4c
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [document-processing, extraction, knowledge-entry, nlp, retrieval, structured-output]
related: [RIU-021, RIU-032, RIU-086]
handled_by: [architect, builder, validator]
journey_stage: retrieval
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I implement reliable structured extraction from unstructured text and documents?

RIU-032 defines a four-phase extraction pipeline. Phase 1 — Schema Definition: define the target schema as a JSON Schema with required fields, optional fields, types, and constraints (enums, ranges, patterns). Every extracted field must have a confidence score (0.0-1.0) and a provenance reference (which part of the source document the value was extracted from). Phase 2 — Extraction Implementation: use LLM-based extraction with structured output (e.g., Anthropic tool_use, OpenAI function calling, or Bedrock Converse). Provide the schema in the prompt and require the model to return JSON conforming to the schema. For critical fields, implement dual extraction — extract twice with different prompts and compare results. Discrepancies flag for human review. Phase 3 — Fallback Strategy: define what happens when extraction fails or confidence is below threshold. Options: return partial extraction with missing fields flagged, escalate to human review, retry with a more capable model. Never silently drop a failed extraction — log it. Phase 4 — Evaluation Set: build an eval set of 50-100 documents with ground-truth annotations. Measure precision, recall, and F1 per field. The most dangerous failure mode is hallucinated fields — the model invents data that sounds plausible but does not exist in the source document. Mitigate by requiring provenance references and validating them programmatically.

## Definition

RIU-032 defines a four-phase extraction pipeline. Phase 1 — Schema Definition: define the target schema as a JSON Schema with required fields, optional fields, types, and constraints (enums, ranges, patterns). Every extracted field must have a confidence score (0.0-1.0) and a provenance reference (which part of the source document the value was extracted from). Phase 2 — Extraction Implementation: use LLM-based extraction with structured output (e.g., Anthropic tool_use, OpenAI function calling, or Bedrock Converse). Provide the schema in the prompt and require the model to return JSON conforming to the schema. For critical fields, implement dual extraction — extract twice with different prompts and compare results. Discrepancies flag for human review. Phase 3 — Fallback Strategy: define what happens when extraction fails or confidence is below threshold. Options: return partial extraction with missing fields flagged, escalate to human review, retry with a more capable model. Never silently drop a failed extraction — log it. Phase 4 — Evaluation Set: build an eval set of 50-100 documents with ground-truth annotations. Measure precision, recall, and F1 per field. The most dangerous failure mode is hallucinated fields — the model invents data that sounds plausible but does not exist in the source document. Mitigate by requiring provenance references and validating them programmatically.

## Evidence

- **Tier 1 (entry-level)**: [Anthropic: Tool Use and Structured Outputs](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- **Tier 1 (entry-level)**: [Google: Document AI Best Practices](https://cloud.google.com/document-ai/docs/best-practices)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-021](../rius/RIU-021.md)
- [RIU-032](../rius/RIU-032.md)
- [RIU-086](../rius/RIU-086.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-021](../paths/RIU-021-tiny-ai-eval-harness.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-139.
Evidence tier: 1.
Journey stage: retrieval.
