---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-118
source_hash: sha256:b0f691b97d345a8c
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 2
tags: [caching, cost-optimization, knowledge-entry, orchestration, performance, redis]
related: [RIU-035, RIU-523]
handled_by: [architect, builder, monitor]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# When should I add a caching layer to my LLM pipeline and what strategy should I use?

Add caching when you see repeated identical or semantically similar queries consuming LLM tokens. Three patterns — exact-match cache (Redis/Upstash, simple key-value, highest hit rate for deterministic queries), semantic cache (GPTCache or custom embedding similarity, catches paraphrases but adds latency), and response fragment cache (cache intermediate steps like retrieval results, not final LLM output). Start with exact-match on the highest-volume query patterns. Measure cache hit rate before adding semantic caching complexity. Invalidation strategy must match your data freshness requirements — TTL-based for most AI use cases, event-based invalidation for real-time data. Upstash Redis is serverless with per-request pricing (no idle cost), ElastiCache for high-throughput on AWS.

## Definition

Add caching when you see repeated identical or semantically similar queries consuming LLM tokens. Three patterns — exact-match cache (Redis/Upstash, simple key-value, highest hit rate for deterministic queries), semantic cache (GPTCache or custom embedding similarity, catches paraphrases but adds latency), and response fragment cache (cache intermediate steps like retrieval results, not final LLM output). Start with exact-match on the highest-volume query patterns. Measure cache hit rate before adding semantic caching complexity. Invalidation strategy must match your data freshness requirements — TTL-based for most AI use cases, event-based invalidation for real-time data. Upstash Redis is serverless with per-request pricing (no idle cost), ElastiCache for high-throughput on AWS.

## Evidence

- **Tier 2 (entry-level)**: [Redis: What is Semantic Caching? Complete Guide](https://redis.io/blog/what-is-semantic-caching/)
- **Tier 2 (entry-level)**: [arXiv: Reducing LLM Costs via Semantic Embedding Caching](https://arxiv.org/html/2411.05276v2)
- **Tier 2 (entry-level)**: [Hands-On Large Language Models](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-035](../rius/RIU-035.md)
- [RIU-523](../rius/RIU-523.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)

## Learning Path

- [RIU-035](../paths/RIU-035-caching-strategy.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-118.
Evidence tier: 2.
Journey stage: orchestration.
