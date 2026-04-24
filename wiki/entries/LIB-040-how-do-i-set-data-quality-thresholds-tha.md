---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-040
source_hash: sha256:2b0ba54cd870266f
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [accuracy, evaluation, knowledge-entry, quality-thresholds, tradeoffs, velocity]
related: [RIU-061, RIU-063, RIU-081, RIU-082, RIU-083, RIU-084]
handled_by: [architect, builder, monitor, validator]
journey_stage: evaluation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I set data quality thresholds that balance accuracy and velocity?

Quality thresholds aren't one-size-fits-all. Set them based on business impact: tighter for high-stakes data, looser for speed-critical flows.

## Definition

Quality thresholds aren't one-size-fits-all. Set them based on business impact: tighter for high-stakes data, looser for speed-critical flows.
      
      **The tradeoff framework:**
      ```
      Accuracy ←――――――――――――――――――→ Velocity
      
      Higher thresholds:           Lower thresholds:
      - More data rejected         - More data passes
      - Higher quality output      - More noise in output
      - Slower throughput          - Faster throughput
      - Higher investigation cost  - Higher error cost downstream
      ```
      
      **Step 1: Classify data by business impact**
      
      | Tier | Description | Example | Threshold Approach |
      |------|-------------|---------|-------------------|
      | Critical | Errors cause financial/legal harm | Financial transactions, PII | Strict, block on failure |
      | Important | Errors degrade user experience | Customer-facing AI outputs | Moderate, alert + continue |
      | Standard | Errors are inconvenient | Internal analytics | Relaxed, log only |
      | Experimental | Errors are expected | Dev/test data | Minimal checks |
      
      **Step 2: Establish baselines**
      Before setting thresholds, measure current state:
      ```yaml
      baseline_metrics:
        completeness: 98.5%  # % non-null for required fields
        uniqueness: 99.9%    # % unique for key fields
        validity: 97.2%      # % matching format/range rules
        freshness: "< 1 hour"
        volume: "45,000-55,000 records/day"
      ```
      
      **Step 3: Set thresholds by tier**
      
      ```yaml
      # AWS Glue DQDL example
      Rules = [
        # Critical tier - strict
        Completeness "customer_id" >= 99.9,
        IsUnique "transaction_id",
        ColumnValues "amount" between 0 and 1000000,
        
        # Important tier - moderate  
        Completeness "email" >= 95.0,
        ColumnValues "status" in ["active", "pending", "closed"],
        
        # Standard tier - relaxed
        Completeness "notes" >= 80.0
      ]
      ```
      
      **Step 4: Define threshold types**
      
      | Type | Use Case | Example |
      |------|----------|---------|
      | Absolute | Known business rules | `amount >= 0` |
      | Statistical | Detect anomalies | `mean(amount) within 2 std of baseline` |
      | Relative | Detect drift | `today's completeness >= 95% of 7-day avg` |
      | Dynamic | Adapt to patterns | `compare to same day last week` |
      
      **Step 5: Configure actions by severity**
      
      ```yaml
      threshold_actions:
        critical_failure:
          action: "block"
          notify: ["on-call", "data-owner"]
          quarantine: true
          
        warning:
          action: "continue"
          notify: ["data-team"]
          log: true
          
        info:
          action: "continue"
          log: true
      ```
      
      **Implementation with AWS Glue Data Quality:**
      - Use DQDL labels to tag rules by priority/owner
      - Route failed records to separate S3 bucket (quarantine)
      - Emit metrics to CloudWatch for dashboards/alerts
      - Set up dynamic rules comparing to historical values
      
      **Threshold tuning methodology:**
      1. Start with baselines from historical data
      2. Set initial thresholds at baseline - 2 standard deviations
      3. Run in "alert only" mode for 2 weeks
      4. Analyze alerts: false positives? missed issues?
      5. Adjust thresholds based on business feedback
      6. Gradually tighten for critical data
      
      **Balancing accuracy vs. velocity:**
      
      | Scenario | Favor Accuracy | Favor Velocity |
      |----------|----------------|----------------|
      | Real-time AI inference | | ✅ |
      | Financial reporting | ✅ | |
      | Customer-facing features | Balance | Balance |
      | Training data pipelines | ✅ | |
      | Exploratory analytics | | ✅ |
      | Compliance/audit data | ✅ | |
      
      **PALETTE integration:**
      - Define thresholds in RIU-084 (Data Quality Checks)
      - Document baseline in RIU-081 (Smoke Tests)
      - Track quality metrics in RIU-063 (Performance Baselines)
      - Alert on breaches via RIU-061 (Observability Baseline)
      
      Key insight: The right threshold makes the cost of false positives (good data rejected) roughly equal to the cost of false negatives (bad data accepted). If you're constantly overriding alerts, thresholds are too tight. If errors reach users, they're too loose.

## Evidence

- **Tier 1 (entry-level)**: [Enable strategic data quality management with AWS Glue DQDL labels](https://aws.amazon.com/blogs/big-data/enable-strategic-data-quality-management-with-aws-glue-dqdl-labels/)
- **Tier 1 (entry-level)**: [Accelerate your data quality journey for lakehouse architecture](https://aws.amazon.com/blogs/big-data/accelerate-your-data-quality-journey-for-lakehouse-architecture-with-amazon-sagemaker-apache-iceberg-on-aws-amazon-s3-tables-and-aws-glue-data-quality/)
- **Tier 1 (entry-level)**: [AWS Glue Data Quality Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/bd8bdbc7-11cb-4d16-9e76-1404e6d37e53)
- **Tier 1 (entry-level)**: [Business Value and use cases - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/1_0_generative_ai_fundamentals/1_2_business_value_and_use_cases/1_2_business_value_and_use_cases.html)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-061](../rius/RIU-061.md)
- [RIU-063](../rius/RIU-063.md)
- [RIU-081](../rius/RIU-081.md)
- [RIU-082](../rius/RIU-082.md)
- [RIU-083](../rius/RIU-083.md)
- [RIU-084](../rius/RIU-084.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-082](../paths/RIU-082-llm-safety-guardrails.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-040.
Evidence tier: 1.
Journey stage: evaluation.
