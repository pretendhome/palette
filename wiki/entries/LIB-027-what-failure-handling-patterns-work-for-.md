---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-027
source_hash: sha256:67a591d27164e350
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, error-recovery, failure-handling, knowledge-entry, resilience, third-party]
related: [RIU-009, RIU-061, RIU-062, RIU-063, RIU-070, RIU-081, RIU-100]
handled_by: [architect, builder, debugger, monitor, narrator, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What failure handling patterns work for brittle third-party integrations?

Brittle integrations fail unpredictably — design for failure with defense in depth: prevent, detect, handle, recover.

## Definition

Brittle integrations fail unpredictably — design for failure with defense in depth: prevent, detect, handle, recover.
      
      **Layer 1: Prevent cascading failures**
      - **Circuit Breaker**: Stop calling failing service temporarily
        - States: CLOSED (normal) → OPEN (failing, reject calls) → HALF-OPEN (test recovery)
        - Prevents your system from being dragged down by third-party failures
      - **Timeouts**: Set explicit, aggressive timeouts (don't wait forever)
      - **Bulkheads**: Isolate third-party calls so one failure doesn't exhaust all resources
      
      **Layer 2: Buffer and decouple**
      - **Queue-based load leveling**: SQS between your system and third-party
        - Absorbs spikes, survives temporary outages
        - Lambda processes queue with controlled concurrency
      - **Async where possible**: Don't block user requests on third-party calls
      
      **Layer 3: Retry safely**
      - **Exponential backoff with jitter**: `delay = base * 2^attempt + random()`
      - **Idempotency**: Use AWS Lambda Powertools idempotency decorator
        - Stores idempotency keys in DynamoDB
        - Prevents duplicate operations on retry (critical for payments, orders)
      - **Retry limits**: Cap retries (e.g., 3-5 attempts), then fail to DLQ
      
      **Layer 4: Fallback strategies**
      | Pattern | Description | Use When |
      |---------|-------------|----------|
      | Cross-Region Fallback | Same service, different region | Regional outage |
      | Multi-Model Fallback | Different AI model, same provider | Model-specific issues |
      | Multi-Provider Fallback | Different provider entirely | Provider outage |
      | Cached Response | Return stale data | Freshness not critical |
      | Degraded Mode | Disable feature, continue core | Non-essential integration |
      | Manual Fallback | Route to human | High-stakes decisions |
      
      **Layer 5: Capture and recover**
      - **Dead Letter Queues (DLQ)**: Capture failed messages for later processing
      - **Lambda Destinations**: Get detailed failure info (better than DLQ alone)
      - **Recovery jobs**: Scheduled process to retry DLQ messages when service recovers
      
      **Monitoring and alerting (RIU-061)**
      - Alert on: error rate spike, latency increase, circuit breaker state change
      - CloudWatch Rules → SNS for immediate notification
      - Dashboard: success rate, p99 latency, DLQ depth, circuit breaker status
      - Test failover in non-production regularly
      
      **PALETTE integration:**
      - Document failure modes in Risk Register (RIU-009)
      - Define fallback behavior in Incident Runbook (RIU-062)
      - Test failure scenarios with RIU-081 (Smoke Tests)
      - Track third-party SLAs in RIU-070 (SLO/SLI Definition)
      
      Key insight: Third-party integrations are *always* brittle — even "reliable" services fail. Design assuming the integration will fail, and your system will be resilient when it inevitably does.

## Evidence

- **Tier 1 (entry-level)**: [Amazon Bedrock Reliability Patterns](https://github.com/aws-samples/sample-amazon-bedrock-reliability-patterns)
- **Tier 1 (entry-level)**: [Queue Integration with Third-party Services on AWS](https://aws.amazon.com/blogs/architecture/queue-integration-with-third-party-services-on-aws/)
- **Tier 1 (entry-level)**: [Handling Lambda functions idempotency with AWS Lambda Powertools](https://aws.amazon.com/blogs/compute/handling-lambda-functions-idempotency-with-aws-lambda-powertools/)
- **Tier 1 (entry-level)**: [Implementing AWS Lambda error handling patterns](https://aws.amazon.com/blogs/compute/implementing-aws-lambda-error-handling-patterns/)
- **Tier 1 (entry-level)**: [Handling Errors, Retries, and adding Alerting to Step Function State Machine Executions](https://aws.amazon.com/blogs/developer/handling-errors-retries-and-adding-alerting-to-step-function-state-machine-executions/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-009](../rius/RIU-009.md)
- [RIU-061](../rius/RIU-061.md)
- [RIU-062](../rius/RIU-062.md)
- [RIU-063](../rius/RIU-063.md)
- [RIU-070](../rius/RIU-070.md)
- [RIU-081](../rius/RIU-081.md)
- [RIU-100](../rius/RIU-100.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)
- [Monitor](../agents/monitor.md)
- [Narrator](../agents/narrator.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-027.
Evidence tier: 1.
Journey stage: all.
