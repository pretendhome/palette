---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-031
source_hash: sha256:04aa73400ed82558
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, early-warning, knowledge-entry, monitoring, observability, reliability]
related: [RIU-061, RIU-062, RIU-063, RIU-070, RIU-532, RIU-533]
handled_by: [architect, builder, debugger, monitor, narrator, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What monitoring tells me an integration is degrading before it fails completely?

Degradation signals appear before failures — monitor leading indicators, not just errors. Focus on trends and percentiles, not just averages.

## Definition

Degradation signals appear before failures — monitor leading indicators, not just errors. Focus on trends and percentiles, not just averages.
      
      **Leading indicators (early warning signals):**
      
      | Indicator | What It Signals | Alert Threshold |
      |-----------|-----------------|-----------------|
      | Latency p99 increasing | Slowdown before timeout | >2x baseline |
      | Error rate trending up | Intermittent failures beginning | >1% or 2x baseline |
      | Queue depth growing | Processing falling behind | >2x normal depth |
      | Retry rate increasing | Transient failures increasing | >5% of requests |
      | Rate limit % consumed | Approaching throttling | >70%, >85%, >95% |
      | Connection pool exhaustion | Resource contention | >80% utilization |
      | Network RTT increasing | Infrastructure degradation | >1.5x baseline |
      | Token/quota consumption | AI cost/rate limits approaching | >70% of budget |
      
      **SLI/SLO framework (RIU-070):**
      Define Service Level Indicators and Objectives:
      ```yaml
      integration_name: "legacy-order-api"
      slis:
        - name: availability
          query: "successful_requests / total_requests"
          target: 99.9%
        - name: latency_p99
          query: "percentile(latency, 99)"
          target: 500ms
        - name: error_rate
          query: "error_count / total_requests"
          target: <0.1%
      slo_window: 30d
      burn_rate_alert: 10x  # Alert if burning error budget 10x faster than sustainable
      ```
      Use CloudWatch Application Signals for SLI/SLO tracking.
      
      **Infrastructure-level monitoring:**
      - **Network Flow Monitor**: Visualize network performance across AWS workloads, detect RTT degradation
      - **EBS latency monitoring**: Track storage I/O latency — often hidden cause of integration slowdowns
      - **Lambda debugging**: Monitor for unintended function versions, infinite loops, downstream availability
      - **SQS throttling/backpressure**: Queue metrics indicate processing falling behind
      
      **Distributed tracing (find degradation source):**
      - **OpenTelemetry**: Auto-instrument with Java Agent (no code changes)
      - **AWS X-Ray + ServiceLens**: Connect metrics, logs, and traces
      - **Trace slow requests**: Identify which integration hop is degrading
      - **Correlation IDs**: Track requests across AI → legacy boundaries
      
      **CloudWatch monitoring setup:**
      ```
      # Anomaly detection for latency
      ANOMALY_DETECTION_BAND(latency_p99, 2)
      
      # Metrics Insights for dynamic monitoring
      SELECT AVG(latency), COUNT(*) as requests, 
             SUM(CASE WHEN status >= 500 THEN 1 ELSE 0 END) as errors
      FROM integration_metrics
      GROUP BY integration_name
      ```
      
      **Alert tiering (escalation):**
      | Severity | Trigger | Action |
      |----------|---------|--------|
      | Info | p99 >1.5x baseline | Log, dashboard highlight |
      | Warning | p99 >2x OR error rate >1% | Page on-call, investigate |
      | Critical | p99 >3x OR error rate >5% OR SLO breach | Immediate response, consider failover |
      
      **AI-specific degradation signals:**
      - Token consumption rate increasing (prompts getting longer/retries)
      - Model latency increasing (provider degradation)
      - Confidence scores dropping (model quality issues)
      - Guardrail block rate spiking (input quality degrading)
      - Cost per request increasing unexpectedly
      
      **Dashboard essentials (RIU-061):**
      - Real-time: Request rate, error rate, p50/p95/p99 latency
      - Trends: Hour-over-hour, day-over-day comparisons
      - Capacity: Queue depth, connection pools, rate limit %
      - Infrastructure: Network RTT, EBS latency, Lambda concurrency
      - Dependencies: Upstream/downstream health status
      - Cost: Token usage, API call costs (for AI integrations)
      
      **PALETTE integration:**
      - Define SLIs/SLOs in RIU-070 (SLO/SLI Definition)
      - Configure alerts in RIU-061 (Observability Baseline)
      - Document escalation in RIU-062 (Incident Runbook)
      - Track degradation patterns in RIU-063 (Performance Baselines)
      
      Key insight: By the time you see errors, users already experienced failures. Monitor *latency percentiles* and *trends* — they degrade before errors spike. Set alerts at 70% of your failure threshold, not 100%.

## Evidence

- **Tier 1 (entry-level)**: [How to monitor application health using SLOs with Amazon CloudWatch Application Signals](https://aws.amazon.com/blogs/mt/how-to-monitor-application-health-using-slos-with-amazon-cloudwatch-application-signals/)
- **Tier 1 (entry-level)**: [Distributed tracing with OpenTelemetry](https://aws.amazon.com/blogs/opensource/distributed-tracing-with-opentelemetry/)
- **Tier 1 (entry-level)**: [Visualizing network performance with Network Flow Monitor](https://aws.amazon.com/blogs/networking-and-content-delivery/visualizing-network-performance-of-your-aws-cloud-workloads-with-network-flow-monitor/)
- **Tier 1 (entry-level)**: [Operating Lambda: Debugging configurations – Part 3](https://aws.amazon.com/blogs/compute/operating-lambda-debugging-integrations-part-3/)
- **Tier 1 (entry-level)**: [Understanding and monitoring latency for Amazon EBS volumes](https://aws.amazon.com/blogs/storage/understanding-and-monitoring-latency-for-amazon-ebs-volumes-using-amazon-cloudwatch/)
- **Tier 1 (entry-level)**: [Integrate Amazon CloudWatch alarms with Amazon CloudWatch Metrics Insights](https://aws.amazon.com/blogs/mt/integrate-amazon-cloudwatch-alarms-with-amazon-cloudwatch-metrics-insights/)
- **Tier 1 (entry-level)**: [OpenTelemetry: What is OpenTelemetry](https://opentelemetry.io/docs/what-is-opentelemetry/)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-061](../rius/RIU-061.md)
- [RIU-062](../rius/RIU-062.md)
- [RIU-063](../rius/RIU-063.md)
- [RIU-070](../rius/RIU-070.md)
- [RIU-532](../rius/RIU-532.md)
- [RIU-533](../rius/RIU-533.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)
- [Monitor](../agents/monitor.md)
- [Narrator](../agents/narrator.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-031.
Evidence tier: 1.
Journey stage: all.
