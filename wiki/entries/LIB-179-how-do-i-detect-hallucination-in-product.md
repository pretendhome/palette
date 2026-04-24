---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-179
source_hash: sha256:816b8a3c92db4a06
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [foundation, hallucination, knowledge-entry, monitoring, production, quality]
related: [RIU-524]
handled_by: [monitor, validator]
journey_stage: foundation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I detect hallucination in production LLM outputs?

Hallucination detection in production requires multiple complementary strategies because no single method catches all types. Start with reference-based checking: compare LLM output claims against your source documents using semantic similarity. If the output asserts a fact not grounded in the provided context, flag it. Second, implement self-consistency checking: ask the same question multiple times with different temperatures and compare outputs. Inconsistent answers on factual questions indicate hallucination. Third, add structured output validation: if the LLM should return JSON with specific fields, validate the schema and check that referenced entities exist in your database. Fourth, deploy an LLM-as-judge pipeline where a second model evaluates whether the first model's output is grounded in the provided context. This catches subtle hallucinations that string matching misses. Fifth, track hallucination rates per query type and model version. Some query patterns trigger hallucination more than others. Build a regression suite of known hallucination-inducing prompts and test every model update against it. The goal is not zero hallucination — it is known, measured, bounded hallucination with clear fallback paths.

## Definition

Hallucination detection in production requires multiple complementary strategies because no single method catches all types. Start with reference-based checking: compare LLM output claims against your source documents using semantic similarity. If the output asserts a fact not grounded in the provided context, flag it. Second, implement self-consistency checking: ask the same question multiple times with different temperatures and compare outputs. Inconsistent answers on factual questions indicate hallucination. Third, add structured output validation: if the LLM should return JSON with specific fields, validate the schema and check that referenced entities exist in your database. Fourth, deploy an LLM-as-judge pipeline where a second model evaluates whether the first model's output is grounded in the provided context. This catches subtle hallucinations that string matching misses. Fifth, track hallucination rates per query type and model version. Some query patterns trigger hallucination more than others. Build a regression suite of known hallucination-inducing prompts and test every model update against it. The goal is not zero hallucination — it is known, measured, bounded hallucination with clear fallback paths.


## Evidence

- **Tier 1 (entry-level)**: [Anthropic — Reducing Hallucination in AI Systems](https://docs.anthropic.com/en/docs/build-with-claude/reduce-hallucinations)
- **Tier 1 (entry-level)**: [Google — Grounding and Hallucination Detection](https://cloud.google.com/vertex-ai/generative-ai/docs/grounding/overview)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-524](../rius/RIU-524.md)

## Handled By

- [Monitor](../agents/monitor.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-524](../paths/RIU-524-llm-output-quality-monitoring.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-179.
Evidence tier: 1.
Journey stage: foundation.
