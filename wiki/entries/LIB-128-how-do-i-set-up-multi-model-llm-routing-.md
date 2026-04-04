---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-128
source_hash: sha256:e328e3d2a555452e
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [cost-optimization, fallback, knowledge-entry, llm-routing, multi-model, openrouter, orchestration]
related: [RIU-252, RIU-521, RIU-522]
handled_by: [architect, monitor, researcher, validator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I set up multi-model LLM routing with automatic fallback and cost tracking?

Use OpenRouter as the routing layer — single OpenAI-compatible API that routes to 500+ models across providers. Change base URL and API key, existing code unchanged. Key features — automatic fallback routing (if Claude fails, route to GPT-4o), cost tracking per model per API key, and routing suffixes (nitro for fastest, floor for cheapest). Zero percent model markup, 5.5 percent credit purchase fee. For self-hosted alternative, LiteLLM provides similar routing with zero markup but requires infrastructure management. Decision — use OpenRouter for simplicity and zero-ops, LiteLLM if you need on-premise or want zero fees. Both support budget limits and usage analytics. This is critical infrastructure for Palette's SageMaker disruptor thesis.

## Definition

Use OpenRouter as the routing layer — single OpenAI-compatible API that routes to 500+ models across providers. Change base URL and API key, existing code unchanged. Key features — automatic fallback routing (if Claude fails, route to GPT-4o), cost tracking per model per API key, and routing suffixes (nitro for fastest, floor for cheapest). Zero percent model markup, 5.5 percent credit purchase fee. For self-hosted alternative, LiteLLM provides similar routing with zero markup but requires infrastructure management. Decision — use OpenRouter for simplicity and zero-ops, LiteLLM if you need on-premise or want zero fees. Both support budget limits and usage analytics. This is critical infrastructure for Palette's SageMaker disruptor thesis.

## Evidence

- **Tier 3 (entry-level)**: [Redis: Machine Learning Inference Cost Optimization](https://redis.io/blog/machine-learning-inference-cost/)
- **Tier 3 (entry-level)**: [Palette internal knowledge base](https://github.com/pretendhome/pretendhome)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-252](../rius/RIU-252.md)
- [RIU-521](../rius/RIU-521.md)
- [RIU-522](../rius/RIU-522.md)

## Handled By

- [Architect](../agents/architect.md)
- [Monitor](../agents/monitor.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-252](../paths/RIU-252-model-evaluation-selection.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-128.
Evidence tier: 3.
Journey stage: orchestration.
