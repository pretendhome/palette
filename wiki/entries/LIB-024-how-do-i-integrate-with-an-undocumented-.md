---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-024
source_hash: sha256:05f91f7a3f382e55
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, api-integration, documentation, knowledge-entry, legacy-systems, reverse-engineering]
related: [RIU-008, RIU-009, RIU-017, RIU-060, RIU-061, RIU-062, RIU-081]
handled_by: [architect, builder, debugger, monitor, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I integrate with an undocumented legacy API that 'just works' in production?

Treat this as a discovery + documentation + safe integration problem. Never assume — observe, document, then integrate.

## Definition

Treat this as a discovery + documentation + safe integration problem. Never assume — observe, document, then integrate.
      
      **Phase 1: Discovery (reverse engineering)**
      - **Traffic capture**: Use network monitoring tools to observe actual API calls in production
        - Capture request/response pairs for all known operations
        - Note headers, authentication patterns, content types
        - Record timing characteristics (latency, timeouts)
      - **Interview SMEs**: Find the people who built it or maintain it
        - "What breaks it? What are the edge cases?"
        - "What's the expected load? What happens under stress?"
      - **Code archaeology**: If source available, trace API handlers
      - **AWS Mainframe Modernization + Micro Focus**: For mainframe legacy, generates dependency analysis and interactive reports
      
      **Phase 2: Document what you learn (RIU-017 Connector Spec)**
      Create a contract even if one doesn't exist:
      ```yaml
      endpoint: "/api/v1/orders"
      method: POST
      auth: Basic Auth (header: Authorization)
      request_schema: (inferred from observations)
      response_codes: [200, 400, 500] # observed
      timeout: 30s # observed p99
      rate_limit: unknown # test carefully
      known_edge_cases:
        - "Returns 500 for order_id > 10 digits"
        - "Timezone assumed UTC despite no documentation"
      confidence: low # until validated
      ```
      
      **Phase 3: Safe integration patterns**
      - **API Gateway + Lambda proxy**: Create facade that normalizes legacy behavior
        - Add retry logic, circuit breakers, timeout handling
        - Transform formats (SOAP↔REST, XML↔JSON) if needed
        - Log all requests/responses for debugging
      - **Leave-and-layer pattern**: Use EventBridge to add capabilities without modifying legacy
      - **Strangler pattern**: Gradually route traffic through new facade
      
      **Phase 4: Defensive coding**
      - **Assume nothing**: Validate all responses, even "successful" ones
      - **Timeouts**: Set explicit timeouts (legacy systems often hang)
      - **Circuit breakers**: Fail fast when legacy system degrades
      - **Async processing**: For slow legacy APIs, use async Lambda + DynamoDB tracking
      - **Fallbacks**: Define behavior when legacy is unavailable
      
      **Phase 5: Validation (before production)**
      - **Shadow traffic**: Mirror production requests to new integration, compare results
      - **Smoke tests**: RIU-081 — test critical paths in prod-like environment
      - **Load testing**: Verify legacy can handle expected traffic (often the bottleneck)
      - **Failure injection**: Test circuit breakers and fallbacks
      
      **PALETTE integration:**
      - Document discovered contract in RIU-017 (Connector Spec)
      - Flag integration as ONE-WAY DOOR until validated
      - Track unknowns in Assumptions Register (RIU-008) with validation plan
      - Add to Risk Register (RIU-009): "Undocumented API behavior may change without notice"
      - Create incident runbook (RIU-062) for legacy system failures
      
      Key insight: "Just works in production" means "works for current use cases under current load." Your integration may trigger behavior nobody has seen. Observe before you act, document everything, and build defensive.

## Evidence

- **Tier 1 (entry-level)**: [Modernizing SOAP applications using Amazon API Gateway and AWS Lambda](https://aws.amazon.com/blogs/compute/modernizing-soap-applications-using-amazon-api-gateway-and-aws-lambda/)
- **Tier 1 (entry-level)**: [Seamlessly migrate on-premises legacy workloads using a strangler pattern](https://aws.amazon.com/blogs/architecture/seamlessly-migrate-on-premises-legacy-workloads-using-a-strangler-pattern/)
- **Tier 1 (entry-level)**: [Modernizing Legacy Applications with Event-Driven Architecture: The Leave-and-Layer Pattern](https://aws.amazon.com/blogs/migration-and-modernization/modernizing-legacy-applications-with-event-driven-architecture-the-leave-and-layer-pattern/)
- **Tier 1 (entry-level)**: [Analyzing legacy applications with AWS Mainframe Modernization and Micro Focus](https://aws.amazon.com/blogs/mt/analyzing-legacy-applications-on-demand-with-aws-mainframe-modernization-and-micro-focus/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-008](../rius/RIU-008.md)
- [RIU-009](../rius/RIU-009.md)
- [RIU-017](../rius/RIU-017.md)
- [RIU-060](../rius/RIU-060.md)
- [RIU-061](../rius/RIU-061.md)
- [RIU-062](../rius/RIU-062.md)
- [RIU-081](../rius/RIU-081.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)
- [Monitor](../agents/monitor.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-060](../paths/RIU-060-deployment-readiness-envelope.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-024.
Evidence tier: 1.
Journey stage: all.
