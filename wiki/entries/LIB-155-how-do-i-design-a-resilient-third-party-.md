---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-155
source_hash: sha256:0735c8714b17c67c
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [api, circuit-breaker, fallback, integration, knowledge-entry, orchestration, resilience]
related: [RIU-085, RIU-320]
handled_by: [architect, builder, monitor]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I design a resilient third-party API integration with circuit breakers and fallback handling?

RIU-320 defines API integration resilience in four layers. Layer 1 — Circuit Breaker: implement a circuit breaker (Closed/Open/Half-Open states) per external API. When failure rate exceeds threshold (typically 50% over 10 requests), open the circuit and stop calling the API. After a cooldown period (30-60 seconds), enter half-open state and send a probe request. If it succeeds, close the circuit. This prevents cascading failures when an upstream API is down. Layer 2 — Rate Limiting: respect the API provider's rate limits proactively. Implement client-side rate limiting with token bucket or sliding window. Buffer requests when approaching limits. Log rate limit headers from responses (X-RateLimit-Remaining, X-RateLimit-Reset) and adapt behavior dynamically. Layer 3 — Fallback Handling: define what happens when the API is unavailable. Options ranked by user experience: (a) serve cached response with staleness indicator; (b) degrade gracefully — return partial results with explanation; (c) queue request for retry when API recovers; (d) return user-friendly error with estimated recovery time. Never show a raw 500 error to end users. Layer 4 — Monitoring: track per-API metrics: availability (% of successful calls), latency (p50/p95/p99), error rate by type (4xx vs 5xx), and cost per call. Alert on availability drops and latency spikes. Implement distributed tracing to correlate API failures with user-visible impacts. Design principle: treat every external API as unreliable by default. The integration should function (degraded) even when the API is completely down.

## Definition

RIU-320 defines API integration resilience in four layers. Layer 1 — Circuit Breaker: implement a circuit breaker (Closed/Open/Half-Open states) per external API. When failure rate exceeds threshold (typically 50% over 10 requests), open the circuit and stop calling the API. After a cooldown period (30-60 seconds), enter half-open state and send a probe request. If it succeeds, close the circuit. This prevents cascading failures when an upstream API is down. Layer 2 — Rate Limiting: respect the API provider's rate limits proactively. Implement client-side rate limiting with token bucket or sliding window. Buffer requests when approaching limits. Log rate limit headers from responses (X-RateLimit-Remaining, X-RateLimit-Reset) and adapt behavior dynamically. Layer 3 — Fallback Handling: define what happens when the API is unavailable. Options ranked by user experience: (a) serve cached response with staleness indicator; (b) degrade gracefully — return partial results with explanation; (c) queue request for retry when API recovers; (d) return user-friendly error with estimated recovery time. Never show a raw 500 error to end users. Layer 4 — Monitoring: track per-API metrics: availability (% of successful calls), latency (p50/p95/p99), error rate by type (4xx vs 5xx), and cost per call. Alert on availability drops and latency spikes. Implement distributed tracing to correlate API failures with user-visible impacts. Design principle: treat every external API as unreliable by default. The integration should function (degraded) even when the API is completely down.

## Evidence

- **Tier 1 (entry-level)**: [Michael Nygard: Release It! — Stability Patterns (2nd Edition, 2018)](https://pragprog.com/titles/mnee2/release-it-second-edition/)
- **Tier 1 (entry-level)**: [AWS: Implementing Resilient Applications](https://docs.aws.amazon.com/prescriptive-guidance/latest/modernization-integrating-microservices/reliability.html)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-085](../rius/RIU-085.md)
- [RIU-320](../rius/RIU-320.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-155.
Evidence tier: 1.
Journey stage: orchestration.
