---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-060
source_hash: sha256:7129f88fdd87810a
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [criteria, evaluation, knowledge-entry, metrics, scaling-readiness, validation]
related: [RIU-003, RIU-060, RIU-120, RIU-532, RIU-540]
handled_by: [architect, builder, narrator, validator]
journey_stage: evaluation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What metrics indicate an AI system is ready to scale beyond pilot?

Scaling readiness isn't just "it works" — it's "it works reliably, economically, and we can support it at scale." Evaluate across four dimensions: technical, operational, business, and organizational.

## Definition

Scaling readiness isn't just "it works" — it's "it works reliably, economically, and we can support it at scale." Evaluate across four dimensions: technical, operational, business, and organizational.
      
      **Scaling readiness scorecard:**
      
      ```
      ┌─────────────────────────────────────────────────────────────┐
      │              SCALING READINESS ASSESSMENT                    │
      ├─────────────────────────────────────────────────────────────┤
      │  TECHNICAL        OPERATIONAL      BUSINESS     ORGANIZATIONAL│
      │  ──────────       ───────────      ────────     ──────────────│
      │  Performance ✓    Monitoring ✓    ROI proven ✓  Team ready ✓  │
      │  Reliability ✓    Runbooks ✓      Demand ✓      Process ✓     │
      │  Cost viable ✓    On-call ✓       Stakeholder ✓ Governance ✓  │
      │                                                              │
      │  ALL FOUR DIMENSIONS MUST PASS TO SCALE                      │
      └─────────────────────────────────────────────────────────────┘
      ```
      
      **DIMENSION 1: Technical Readiness**
      
      | Metric | Pilot Threshold | Scale Threshold | How to Measure |
      |--------|-----------------|-----------------|----------------|
      | **Latency p99** | <5s | <2s | CloudWatch percentiles |
      | **TTFT** | <1s | <500ms | Custom metric |
      | **Error rate** | <5% | <1% | CloudWatch errors/total |
      | **Availability** | 95% | 99.9% | Uptime calculation |
      | **Quality score** | >70% | >85% | Evaluation pipeline |
      | **Throughput** | Handles pilot load | 2x projected scale | Load testing |
      | **Cost per request** | Understood | Within budget | Cost allocation |
      
      ```yaml
      technical_checklist:
        performance:
          - metric: "latency_p99"
            current: "1.2s"
            threshold: "<2s"
            status: "PASS"
            
          - metric: "error_rate"
            current: "0.8%"
            threshold: "<1%"
            status: "PASS"
            
          - metric: "quality_score"
            current: "87%"
            threshold: ">85%"
            status: "PASS"
            
        scalability:
          - test: "Load test at 2x projected scale"
            result: "Passed, latency stable"
            status: "PASS"
            
          - test: "Auto-scaling validation"
            result: "Scales within 60 seconds"
            status: "PASS"
            
        cost:
          - metric: "cost_per_request"
            current: "$0.03"
            budget: "$0.05"
            status: "PASS"
            
          - metric: "projected_monthly_cost"
            current: "$15,000"
            budget: "$20,000"
            status: "PASS"
      ```
      
      **DIMENSION 2: Operational Readiness**
      
      | Requirement | Pilot | Scale | Status |
      |-------------|-------|-------|--------|
      | **Monitoring dashboards** | Basic | Comprehensive | Required |
      | **Alerting** | Manual checks | Automated alerts | Required |
      | **Runbooks** | Notes | Formal documentation | Required |
      | **On-call rotation** | Ad-hoc | Formal rotation | Required |
      | **Incident response** | Reactive | Defined process | Required |
      | **Deployment automation** | Manual/semi | Fully automated | Required |
      | **Rollback tested** | Not tested | Tested & documented | Required |
      
      ```yaml
      operational_checklist:
        observability:
          - "CloudWatch dashboards configured" # PASS/FAIL
          - "Alerts for critical metrics" # PASS/FAIL
          - "Distributed tracing enabled" # PASS/FAIL
          - "Log retention configured" # PASS/FAIL
          
        documentation:
          - "SOP documented (LIB-056)" # PASS/FAIL
          - "Runbooks for common issues" # PASS/FAIL
          - "Architecture diagram current" # PASS/FAIL
          - "Escalation paths defined" # PASS/FAIL
          
        team_readiness:
          - "On-call rotation established" # PASS/FAIL
          - "Team trained on operations" # PASS/FAIL
          - "Handoff from pilot team complete" # PASS/FAIL
      ```
      
      **DIMENSION 3: Business Readiness**
      
      | Metric | Evidence Required | Threshold |
      |--------|-------------------|-----------|
      | **ROI demonstrated** | Before/after comparison | Positive ROI |
      | **User satisfaction** | Survey or feedback | >4.0/5.0 |
      | **Adoption rate** | % of target users active | >70% of pilot users |
      | **Business KPI impact** | Measurable improvement | Meeting targets |
      | **Stakeholder approval** | Sign-off documented | Approved |
      | **Demand validated** | Pipeline of additional users | Demand exists |
      
      ```yaml
      business_checklist:
        value_proven:
          - metric: "ROI"
            baseline: "Manual process: $50/task"
            current: "AI-assisted: $15/task"
            improvement: "70% cost reduction"
            status: "PASS"
            
          - metric: "user_satisfaction"
            score: "4.3/5.0"
            threshold: ">4.0"
            status: "PASS"
            
          - metric: "pilot_adoption"
            active_users: "85 of 100"
            threshold: ">70%"
            status: "PASS"
            
        demand_validated:
          - "Waitlist for access: 500 users"
          - "Business units requesting: 5"
          - "Executive sponsor committed: Yes"
          
        stakeholder_approval:
          - approver: "Product Lead"
            status: "Approved"
          - approver: "Finance"
            status: "Approved"
          - approver: "Legal/Compliance"
            status: "Approved"
      ```
      
      **DIMENSION 4: Organizational Readiness**
      
      | Requirement | Description | Status |
      |-------------|-------------|--------|
      | **Ownership assigned** | Clear team owns production | Required |
      | **Governance in place** | AI governance review passed | Required |
      | **Support model defined** | Who handles what issues | Required |
      | **Training materials** | Operators and users trained | Required |
      | **Change management** | Process for updates defined | Required |
      | **Budget approved** | Funding for scale operation | Required |
      
      ```yaml
      organizational_checklist:
        ownership:
          - "Production owner identified: AI Platform Team"
          - "On-call rotation staffed"
          - "Escalation matrix documented"
          
        governance:
          - "AI Governance review: Passed"
          - "Security review: Passed"
          - "Compliance review: Passed"
          
        enablement:
          - "User training materials complete"
          - "Operator training complete"
          - "AI Ambassadors identified"
          
        resources:
          - "Scaling budget approved"
          - "Team capacity available"
          - "Infrastructure provisioned"
      ```
      
      **Go/No-Go decision framework:**
      
      ```yaml
      scaling_decision:
        gate_criteria:
          technical: "All metrics within threshold"
          operational: "All checklist items PASS"
          business: "ROI positive + stakeholder approval"
          organizational: "Team + governance + budget ready"
          
        decision_matrix:
          all_pass: "GO - Proceed with scaling"
          one_fail: "CONDITIONAL - Address gaps, re-evaluate in 2 weeks"
          multiple_fail: "NO-GO - Not ready, create remediation plan"
          
        escalation:
          decision_maker: "AI Governance Lead + Product Lead"
          meeting: "Scaling Readiness Review"
          artifacts: "This scorecard with evidence"
      ```
      
      **Red flags (not ready to scale):**
      - Quality score unstable or declining
      - Support tickets per user increasing
      - Cost per request higher than projected
      - Pilot users not adopting
      - No formal on-call rotation
      - Runbooks don't exist or untested
      - ROI not demonstrated with data
      
      **PALETTE integration:**
      - Use as Deployment Readiness gate (RIU-060)
      - Track metrics in RIU-540 (Evaluation Harness)
      - Document approval in decisions.md (RIU-003)
      - Update RIU-532 (Model Registry) with scale status
      
      Key insight: "It works" is pilot criteria. "It works, we can afford it, we can support it, and users want more" is scaling criteria. Don't skip dimensions — technical success with organizational unreadiness still fails.

## Evidence

- **Tier 1 (entry-level)**: [Beyond pilots: A proven framework for scaling AI to production](https://aws.amazon.com/blogs/machine-learning/beyond-pilots-a-proven-framework-for-scaling-ai-to-production/)
- **Tier 1 (entry-level)**: [Business Value and use cases - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/1_0_generative_ai_fundamentals/1_2_business_value_and_use_cases/1_2_business_value_and_use_cases.html)
- **Tier 1 (entry-level)**: [Enabling customers to deliver production-ready AI agents at scale](https://aws.amazon.com/blogs/machine-learning/enabling-customers-to-deliver-production-ready-ai-agents-at-scale/)
- **Tier 1 (entry-level)**: [Google: Practitioners Guide to MLOps](https://services.google.com/fh/files/misc/practitioners_guide_to_mlops_whitepaper.pdf)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-003](../rius/RIU-003.md)
- [RIU-060](../rius/RIU-060.md)
- [RIU-120](../rius/RIU-120.md)
- [RIU-532](../rius/RIU-532.md)
- [RIU-540](../rius/RIU-540.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Narrator](../agents/narrator.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-060](../paths/RIU-060-deployment-readiness-envelope.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-060.
Evidence tier: 1.
Journey stage: evaluation.
