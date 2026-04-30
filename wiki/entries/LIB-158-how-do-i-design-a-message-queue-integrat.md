---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-158
source_hash: sha256:0a65b88de77916d1
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [async, kafka, knowledge-entry, message-queue, orchestration, reliability, sqs]
related: [RIU-320, RIU-323]
handled_by: [architect, builder]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I design a message queue integration pattern for reliable async processing?

RIU-323 defines message queue integration across four design areas. Area 1 — Consumer Pattern Selection: choose based on processing requirements. Competing Consumers: multiple consumers process from the same queue for throughput. Best for: stateless, idempotent processing (image resizing, email sending). Fan-Out: one message triggers multiple independent consumers. Best for: event notification (order placed triggers inventory update, email, analytics). Sequential Processing: messages processed in strict order. Best for: state machines, financial transactions. Use SQS FIFO or Kafka partitions with key-based ordering. Area 2 — Error Handling: implement a three-tier error strategy. Transient errors (network timeout, throttling): retry with exponential backoff (1s, 2s, 4s, 8s, cap at 60s). Poison messages (malformed, schema violation): send to dead letter queue (DLQ) after 3 retries. Business errors (validation failure): route to error topic for human review. Never silently drop a message — every message must reach either successful processing, DLQ, or error topic. Area 3 — Idempotency: design consumers to be idempotent — processing the same message twice produces the same result. Use message deduplication IDs (SQS) or consumer group offsets (Kafka). Store processed message IDs to detect duplicates. Area 4 — Monitoring: track queue depth (growing = consumers falling behind), processing latency (time from enqueue to process), DLQ depth (growing = systematic errors), and consumer lag (Kafka). Alert on DLQ depth > 0 and queue depth exceeding 10x normal.

## Definition

RIU-323 defines message queue integration across four design areas. Area 1 — Consumer Pattern Selection: choose based on processing requirements. Competing Consumers: multiple consumers process from the same queue for throughput. Best for: stateless, idempotent processing (image resizing, email sending). Fan-Out: one message triggers multiple independent consumers. Best for: event notification (order placed triggers inventory update, email, analytics). Sequential Processing: messages processed in strict order. Best for: state machines, financial transactions. Use SQS FIFO or Kafka partitions with key-based ordering. Area 2 — Error Handling: implement a three-tier error strategy. Transient errors (network timeout, throttling): retry with exponential backoff (1s, 2s, 4s, 8s, cap at 60s). Poison messages (malformed, schema violation): send to dead letter queue (DLQ) after 3 retries. Business errors (validation failure): route to error topic for human review. Never silently drop a message — every message must reach either successful processing, DLQ, or error topic. Area 3 — Idempotency: design consumers to be idempotent — processing the same message twice produces the same result. Use message deduplication IDs (SQS) or consumer group offsets (Kafka). Store processed message IDs to detect duplicates. Area 4 — Monitoring: track queue depth (growing = consumers falling behind), processing latency (time from enqueue to process), DLQ depth (growing = systematic errors), and consumer lag (Kafka). Alert on DLQ depth > 0 and queue depth exceeding 10x normal.

## Evidence

- **Tier 1 (entry-level)**: [AWS: Building Scalable and Resilient Applications with SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
- **Tier 1 (entry-level)**: [Martin Kleppmann: Designing Data-Intensive Applications (2017)](https://dataintensive.net/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-320](../rius/RIU-320.md)
- [RIU-323](../rius/RIU-323.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-158.
Evidence tier: 1.
Journey stage: orchestration.
