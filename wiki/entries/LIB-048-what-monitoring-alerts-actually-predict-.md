---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-048
source_hash: sha256:8768b4255edbc463
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [alerting, all, knowledge-entry, monitoring, observability, signal-vs-noise]
related: [RIU-061, RIU-063, RIU-100, RIU-532, RIU-533]
handled_by: [architect, builder, monitor, narrator, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What monitoring alerts actually predict AI system failures vs noise?

Most AI alerts are noise. Focus on leading indicators that predict failures before user impact, not lagging indicators that confirm failures already happened.

## Definition

Most AI alerts are noise. Focus on leading indicators that predict failures before user impact, not lagging indicators that confirm failures already happened.
      
      **The alert quality problem:**
      - Security teams face 3,000+ daily alerts, 60-90% uninvestigated
      - Alert fatigue leads to ignored critical signals
      - AI systems generate MORE noise (non-deterministic, gradual degradation)
      
      **Alert classification: Signal vs. Noise**
      
      | Alert Type | Signal (Actionable) | Noise (Ignore/Tune) |
      |------------|---------------------|---------------------|
      | Error rate spike | ✅ >2x baseline in 5 min | ❌ Minor fluctuation |
      | Latency increase | ✅ p99 >3x baseline | ❌ p50 within normal |
      | Quality score drop | ✅ Sustained >10% drop | ❌ Single low-score response |
      | Token usage spike | ✅ >2x sustained | ❌ Brief spike (one request) |
      | User feedback | ✅ Negative trend over hours | ❌ Individual complaint |
      | Cost threshold | ✅ Projected to exceed budget | ❌ Within 10% of baseline |
      
      **Leading indicators (predict failures):**
      
      | Indicator | What It Predicts | Alert Threshold |
      |-----------|------------------|-----------------|
      | **p99 latency trending up** | Timeout failures imminent | >1.5x baseline sustained 10min |
      | **Token usage increasing** | Cost explosion / prompt issues | >2x baseline sustained |
      | **Confidence scores dropping** | Quality degradation | Avg confidence <0.7 |
      | **Retry rate increasing** | Transient failures becoming persistent | >5% of requests |
      | **Queue depth growing** | Processing falling behind | >2x normal depth |
      | **Embedding distance increasing** | Data drift / semantic shift | Cosine similarity <0.9 |
      | **Guardrail trigger rate up** | Input quality degrading | >5% of inputs blocked |
      
      **Lagging indicators (confirm failures — still useful but reactive):**
      - Error count
      - User complaints
      - Escalation rate
      - Failed evaluations
      
      **Alert prioritization framework:**
      
      ```yaml
      alert_tiers:
        critical:
          criteria:
            - "Customer-facing error rate > 5%"
            - "Security/compliance breach detected"
            - "Complete service outage"
          response: "Immediate page, drop everything"
          
        high:
          criteria:
            - "Quality score < 70% sustained 15 min"
            - "p99 latency > 3x baseline"
            - "Cost projection > 150% of budget"
          response: "Page on-call within 15 min"
          
        warning:
          criteria:
            - "Leading indicators trending negative"
            - "Quality score dropped 10%"
            - "Anomaly detected but not confirmed"
          response: "Review in next 4 hours, investigate trend"
          
        info:
          criteria:
            - "Minor fluctuations within expected range"
            - "Single instance anomalies"
          response: "Log for context, no immediate action"
      ```
      
      **Noise reduction techniques:**
      
      1. **Use anomaly detection, not static thresholds**
         ```
         # Bad: Static threshold
         ALARM: latency > 500ms
         
         # Good: Anomaly band
         ALARM: latency > ANOMALY_DETECTION_BAND(latency, 2)
         ```
      
      2. **Require sustained violations**
         ```
         # Bad: Alert on single data point
         ALARM IF error_rate > 5%
         
         # Good: Require sustained violation
         ALARM IF error_rate > 5% FOR 3 consecutive minutes
         ```
      
      3. **Correlate related metrics**
         - Don't alert on latency AND errors separately
         - Alert on combined signal: "latency high AND error rate rising"
      
      4. **Suppress during known events**
         - Deployment windows
         - Scheduled maintenance
         - Expected traffic spikes
      
      5. **Auto-resolve transient alerts**
         - If condition clears within 5 minutes, log but don't page
      
      **Effective CloudWatch alarm patterns:**
      
      ```yaml
      # Leading indicator: Latency trending up
      - alarm_name: "AI-LatencyTrending"
        metric: "InvocationLatency"
        statistic: "p99"
        threshold: "ANOMALY_DETECTION_BAND(2)"
        period: 300
        evaluation_periods: 3
        treat_missing: "notBreaching"
        
      # Leading indicator: Token usage spike
      - alarm_name: "AI-TokenUsageSpike"
        metric: "InputTokenCount + OutputTokenCount"
        statistic: "Sum"
        threshold: "> 2x 7-day average"
        period: 300
        evaluation_periods: 2
        
      # Composite: Multiple signals
      - alarm_name: "AI-QualityDegradation-Composite"
        type: "composite"
        rule: "AI-LatencyTrending AND AI-ConfidenceLow"
        description: "Multiple quality signals degrading together"
      ```
      
      **Metrics that are usually noise:**
      - Individual request failures (expected in distributed systems)
      - Brief latency spikes (often just cold starts)
      - Single user complaints (without pattern)
      - Minor fluctuations in token usage
      - Scheduled job completion variations
      
      **PALETTE integration:**
      - Define alert tiers in RIU-061 (Observability Baseline)
      - Document leading indicators in RIU-063 (Performance Baselines)
      - Track alert effectiveness in RIU-100 (Incident Log) — were alerts useful?
      - Tune thresholds based on false positive rate
      
      Key insight: A good alert is one that, when it fires, you always investigate and usually find a real problem. If you're ignoring alerts, you have too many or wrong thresholds. Track false positive rate and tune ruthlessly.

## Evidence

- **Tier 1 (entry-level)**: [Application Performance Monitoring for Generative AI](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_4_scalability_performance/3_4_1_application_runtime_optimization/3_4_1_1_application_performance/3_4_1_1_2_application_performance_monitoring.html)
- **Tier 1 (entry-level)**: [Application Observability for GenAI Systems](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_1_system_and_application_design_patterns_for_genai/3_1_1_foundation_architecture_components/3_1_1_7_application_observability/index.html)
- **Tier 1 (entry-level)**: [Risk and Compliance Management for Generative AI](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/5_2_governance_and_organization/5_2_3_risk_and_compliance_mngmt.html)
- **Tier 1 (entry-level)**: [Build resilient generative AI agents](https://aws.amazon.com/blogs/architecture/build-resilient-generative-ai-agents/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-061](../rius/RIU-061.md)
- [RIU-063](../rius/RIU-063.md)
- [RIU-100](../rius/RIU-100.md)
- [RIU-532](../rius/RIU-532.md)
- [RIU-533](../rius/RIU-533.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)
- [Narrator](../agents/narrator.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-048.
Evidence tier: 1.
Journey stage: all.
