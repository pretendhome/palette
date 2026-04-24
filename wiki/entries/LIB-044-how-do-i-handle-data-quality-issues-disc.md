---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-044
source_hash: sha256:0d92f215fb5b16e2
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [data-quality, evaluation, incident-response, knowledge-entry, post-deployment, remediation]
related: [RIU-014, RIU-062, RIU-081, RIU-084, RIU-100, RIU-532]
handled_by: [architect, builder, debugger, narrator, validator]
journey_stage: evaluation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I handle data quality issues discovered after model deployment?

Post-deployment data quality issues require structured incident response: Detect → Assess → Contain → Remediate → Prevent. Speed matters — bad data compounds downstream.

## Definition

Post-deployment data quality issues require structured incident response: Detect → Assess → Contain → Remediate → Prevent. Speed matters — bad data compounds downstream.
      
      **Incident response phases:**
      
      **PHASE 1: DETECT (Minutes)**
      Already covered by monitoring (LIB-034, LIB-038):
      - SageMaker Model Monitor alerts on data drift
      - Glue Data Quality anomaly detection
      - CloudWatch alarms on quality metrics
      - User reports / escalations
      
      **PHASE 2: ASSESS SEVERITY (< 30 minutes)**
      
      Triage questions:
      1. **Scope**: How much data is affected? (% of records)
      2. **Impact**: What decisions were made with bad data?
      3. **Duration**: How long has this been happening?
      4. **Reversibility**: Can affected outputs be corrected?
      5. **Visibility**: Have users/customers been impacted?
      
      Severity classification:
      | Severity | Criteria | Response Time |
      |----------|----------|---------------|
      | Critical | Customer-facing, financial, or safety impact | Immediate |
      | High | Significant business process affected | < 4 hours |
      | Medium | Internal processes affected, workaround exists | < 24 hours |
      | Low | Minimal impact, cosmetic issues | Next sprint |
      
      **PHASE 3: CONTAIN (< 1 hour for Critical/High)**
      
      ```
      Decision tree:
      
      Is bad data still flowing?
      ├── YES → Stop the source
      │   ├── Pause data pipeline
      │   ├── Quarantine incoming data
      │   └── Switch to backup data source (if available)
      │
      └── NO → Assess blast radius
          ├── Identify all downstream systems affected
          └── Document affected time range
      
      Are AI outputs still being served?
      ├── YES, and outputs are dangerous → Rollback model
      │   ├── Revert to last known good model version
      │   └── Enable fallback behavior
      │
      └── YES, but outputs are degraded → Consider options
          ├── Continue with degraded quality (communicate)
          ├── Route to human review (A2I)
          └── Return error/uncertainty indicator
      ```
      
      **PHASE 4: DECIDE - Rollback vs. Fix-Forward**
      
      | Factor | Favor Rollback | Favor Fix-Forward |
      |--------|----------------|-------------------|
      | User impact | High/visible | Low/internal |
      | Fix complexity | Unknown/complex | Simple/understood |
      | Time to fix | > 4 hours | < 1 hour |
      | Previous version quality | Good | Also degraded |
      | Business criticality | Revenue/safety | Analytics/internal |
      
      **Rollback procedure:**
      1. Switch model to previous version (SageMaker endpoint update)
      2. Revert data pipeline to last good state
      3. Mark affected outputs as potentially invalid
      4. Communicate to stakeholders
      
      **Fix-forward procedure:**
      1. Implement data fix (quarantine bad, reprocess)
      2. Test fix in staging
      3. Deploy to production
      4. Validate quality metrics return to baseline
      5. Reprocess affected data if needed
      
      **PHASE 5: REMEDIATE (Hours to Days)**
      
      For affected data:
      - [ ] Identify all records affected (time range, criteria)
      - [ ] Quarantine or flag affected records
      - [ ] Determine if reprocessing is needed
      - [ ] Reprocess with corrected data/model
      - [ ] Validate outputs against known-good examples
      
      For affected users/decisions:
      - [ ] Identify decisions made with bad data
      - [ ] Assess if decisions need to be reversed
      - [ ] Communicate with affected stakeholders
      - [ ] Document business impact for post-mortem
      
      **PHASE 6: PREVENT (Post-incident)**
      
      Root cause analysis:
      ```yaml
      incident_post_mortem:
        incident_id: "DQ-2024-001"
        summary: "Training data contained duplicate records causing model bias"
        
        timeline:
          detected: "2024-06-15 14:30"
          contained: "2024-06-15 15:00"
          resolved: "2024-06-15 18:00"
          
        root_cause: "ETL job failure left partial data, dedup not run"
        
        impact:
          records_affected: 50000
          users_impacted: 200
          business_cost: "$5000 in incorrect recommendations"
          
        actions:
          - action: "Add dedup validation to pipeline"
            owner: "data-team"
            due: "2024-06-22"
            
          - action: "Add monitoring for record count anomalies"
            owner: "mlops-team"
            due: "2024-06-20"
            
          - action: "Update runbook with dedup failure scenario"
            owner: "on-call"
            due: "2024-06-18"
      ```
      
      **Runbook template (RIU-062):**
      ```yaml
      data_quality_incident_runbook:
        detection_sources:
          - SageMaker Model Monitor alerts
          - CloudWatch quality metric alarms
          - User escalations
          
        immediate_actions:
          - Acknowledge alert, start incident channel
          - Assess severity using triage questions
          - Notify on-call and data owner
          
        containment_options:
          - Pause data pipeline: "[link to procedure]"
          - Rollback model: "[link to procedure]"
          - Enable fallback: "[link to procedure]"
          
        escalation_contacts:
          critical: ["on-call-primary", "data-owner", "product-lead"]
          high: ["on-call-primary", "data-owner"]
      ```
      
      **PALETTE integration:**
      - Document incidents in RIU-100 (Incident Log)
      - Update runbook in RIU-062 (Incident Containment)
      - Track model versions in RIU-532 (Model Registry)
      - Add failed scenarios to RIU-014 (Edge-Case Catalog)
      - Update quality tests in RIU-084 (Data Quality Checks)
      
      Key insight: The goal isn't zero data quality issues — it's fast detection and contained blast radius. Every incident should result in a new test that prevents recurrence.

## Evidence

- **Tier 1 (entry-level)**: [AWS DevOps Agent helps you accelerate incident response](https://aws.amazon.com/blogs/aws/aws-devops-agent-helps-you-accelerate-incident-response-and-improve-system-reliability-preview/)
- **Tier 1 (entry-level)**: [Introducing AWS Glue Data Quality anomaly detection](https://aws.amazon.com/blogs/big-data/introducing-aws-glue-data-quality-anomaly-detection/)
- **Tier 1 (entry-level)**: [Monitoring data quality in third-party models with Amazon SageMaker Model Monitor](https://aws.amazon.com/blogs/awsmarketplace/monitoring-data-quality-in-third-party-models-with-amazon-sagemaker-model-monitor/)
- **Tier 1 (entry-level)**: [Automated monitoring with SageMaker Model Monitor and Amazon A2I](https://aws.amazon.com/blogs/machine-learning/automated-monitoring-of-your-machine-learning-models-with-amazon-sagemaker-model-monitor-and-sending-predictions-to-human-review-workflows-using-amazon-a2i/)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-014](../rius/RIU-014.md)
- [RIU-062](../rius/RIU-062.md)
- [RIU-081](../rius/RIU-081.md)
- [RIU-084](../rius/RIU-084.md)
- [RIU-100](../rius/RIU-100.md)
- [RIU-532](../rius/RIU-532.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)
- [Narrator](../agents/narrator.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-044.
Evidence tier: 1.
Journey stage: evaluation.
