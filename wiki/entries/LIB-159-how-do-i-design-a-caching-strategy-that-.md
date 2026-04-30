---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-159
source_hash: sha256:3d11aed13763a88b
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [caching, invalidation, knowledge-entry, latency, orchestration, performance, ttl]
related: [RIU-025, RIU-085, RIU-324]
handled_by: [architect, builder, monitor]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I design a caching strategy that improves performance without serving stale data?

RIU-324 defines caching strategy across five design dimensions. Dimension 1 — Cache Placement: choose the right layer. Client-side cache (browser, mobile): best for static assets and user preferences. Application cache (in-memory, Redis): best for computed results, API responses, and session data. CDN cache: best for public content, media, static resources. For AI systems: cache LLM responses for identical prompts (semantic caching), embedding vectors for repeated queries, and retrieval results for common searches. Dimension 2 — TTL (Time-to-Live): set per data type. Reference data (country codes, taxonomies): hours to days. Computed results (search rankings, recommendations): minutes to hours. Real-time data (prices, inventory): seconds or no cache. Err toward shorter TTLs initially and extend based on observed staleness impact. Dimension 3 — Invalidation Strategy: choose from: time-based (TTL expiration), event-based (invalidate when source data changes), and version-based (cache key includes data version). Event-based is most accurate but requires change notification infrastructure. Combine with TTL as a safety net — even event-based invalidation should have a max TTL. Dimension 4 — Cache Warming: pre-populate cache with high-traffic queries during deployment to avoid cold-start latency spikes. Implement background refresh for expiring entries (refresh 10% before TTL to prevent thundering herd). Dimension 5 — Failure Handling: when cache is unavailable, the system must still function (cache-aside pattern). Never make the cache a single point of failure. Monitor cache hit rate (target > 80%), miss storm rate, and memory usage.

## Definition

RIU-324 defines caching strategy across five design dimensions. Dimension 1 — Cache Placement: choose the right layer. Client-side cache (browser, mobile): best for static assets and user preferences. Application cache (in-memory, Redis): best for computed results, API responses, and session data. CDN cache: best for public content, media, static resources. For AI systems: cache LLM responses for identical prompts (semantic caching), embedding vectors for repeated queries, and retrieval results for common searches. Dimension 2 — TTL (Time-to-Live): set per data type. Reference data (country codes, taxonomies): hours to days. Computed results (search rankings, recommendations): minutes to hours. Real-time data (prices, inventory): seconds or no cache. Err toward shorter TTLs initially and extend based on observed staleness impact. Dimension 3 — Invalidation Strategy: choose from: time-based (TTL expiration), event-based (invalidate when source data changes), and version-based (cache key includes data version). Event-based is most accurate but requires change notification infrastructure. Combine with TTL as a safety net — even event-based invalidation should have a max TTL. Dimension 4 — Cache Warming: pre-populate cache with high-traffic queries during deployment to avoid cold-start latency spikes. Implement background refresh for expiring entries (refresh 10% before TTL to prevent thundering herd). Dimension 5 — Failure Handling: when cache is unavailable, the system must still function (cache-aside pattern). Never make the cache a single point of failure. Monitor cache hit rate (target > 80%), miss storm rate, and memory usage.

## Evidence

- **Tier 1 (entry-level)**: [AWS ElastiCache: Caching Strategies](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/Strategies.html)
- **Tier 1 (entry-level)**: [Martin Fowler: Patterns of Enterprise Application Architecture](https://martinfowler.com/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-025](../rius/RIU-025.md)
- [RIU-085](../rius/RIU-085.md)
- [RIU-324](../rius/RIU-324.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-159.
Evidence tier: 1.
Journey stage: orchestration.
