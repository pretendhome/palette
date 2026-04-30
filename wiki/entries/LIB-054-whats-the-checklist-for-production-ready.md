---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-054
source_hash: sha256:2350ba30bf2f4857
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [checklist, evaluation, knowledge-entry, production-readiness, reliability-criteria, standards]
related: [RIU-060, RIU-100, RIU-101, RIU-102]
handled_by: [architect, builder, narrator]
journey_stage: evaluation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What's the checklist for 'production-ready' AI reliability?

Use this checklist before declaring an AI system production-ready. All sections must PASS or have documented exceptions approved by the AI Governance Lead.

## Definition

Use this checklist before declaring an AI system production-ready. All sections must PASS or have documented exceptions approved by the AI Governance Lead.
      
      **SECTION 1: ARCHITECTURE RELIABILITY (Must pass all)**
      
      - [ ] **High availability configured**
        - Multi-AZ deployment for stateful components
        - Cross-region capability for critical workloads
        - No single points of failure identified
        
      - [ ] **Redundancy implemented**
        - Fallback model configured (alternative provider/model)
        - Cross-region inference profiles (Bedrock) or multi-endpoint (SageMaker)
        - RAG fallback to non-retrieval response
        
      - [ ] **Scaling configured**
        - Auto-scaling policies defined and tested
        - Quota headroom validated (>50% buffer recommended)
        - Load tested at 2x expected peak
        
      - [ ] **State management**
        - Conversation/session state persisted (DynamoDB)
        - Cache layer for performance (ElastiCache)
        - State recovery tested after restart
        
      **SECTION 2: FAILURE HANDLING (Must pass all)**
      
      - [ ] **Circuit breakers implemented**
        - Per-model circuit breaker configured
        - Failure thresholds defined
        - Fallback behavior tested
        
      - [ ] **Retry logic**
        - Exponential backoff with jitter
        - Max retry limits set
        - Idempotency implemented for state-changing operations
        
      - [ ] **Timeout configuration**
        - Explicit timeouts at every integration point
        - Cascading timeout budget (each stage < total)
        - Timeout handling tested
        
      - [ ] **Graceful degradation**
        - Fallback chain defined (LIB-050)
        - Human escalation path configured
        - "I don't know" responses enabled for low confidence
        
      **SECTION 3: OBSERVABILITY (Must pass all)**
      
      - [ ] **Metrics configured**
        ```
        Required metrics:
        - Latency: p50, p95, p99, TTFT, TPOT
        - Throughput: RPM, TPM
        - Errors: Error rate, error types
        - Quality: Confidence scores, guardrail triggers
        - Cost: Per-request cost, daily spend
        - Resources: CPU, memory, GPU utilization
        ```
        
      - [ ] **Logging implemented**
        - Structured logs with consistent schema
        - Trace IDs for request correlation
        - PII redaction in logs
        - Log retention policy defined
        
      - [ ] **Distributed tracing**
        - End-to-end trace through AI pipeline
        - X-Ray or OpenTelemetry configured
        - Trace sampling rate appropriate
        
      - [ ] **Dashboards created**
        - Real-time operations dashboard
        - Quality metrics dashboard
        - Cost dashboard
        - Alert status visible
        
      - [ ] **Alerting configured**
        - Leading indicator alerts (LIB-048)
        - Severity tiers defined (Critical/High/Warning/Info)
        - Escalation paths configured
        - On-call rotation documented
        
      **SECTION 4: OPERATIONAL READINESS (Must pass all)**
      
      - [ ] **Runbooks created**
        - Incident response runbook (LIB-045)
        - Common failure scenarios documented
        - Escalation matrix defined (LIB-051)
        - Rollback procedures tested
        
      - [ ] **On-call established**
        - Primary and secondary on-call assigned
        - Escalation contacts documented
        - Paging configured and tested
        - Handoff procedures defined
        
      - [ ] **Deployment process**
        - CI/CD pipeline implemented
        - Canary/blue-green deployment configured
        - Rollback automation tested
        - Change approval process defined
        
      - [ ] **Documentation complete**
        - Architecture diagram current
        - API documentation published
        - Dependency map maintained
        - Contact information current
        
      **SECTION 5: TESTING COMPLETED (Must pass all)**
      
      - [ ] **Functional testing**
        - Golden set evaluation passing (>baseline)
        - Edge cases tested
        - Negative tests (bad inputs) passing
        
      - [ ] **Integration testing**
        - All integrations verified
        - Contract tests passing
        - Error handling tested
        
      - [ ] **Performance testing**
        - Load test at 2x peak completed
        - Latency SLOs met under load
        - No resource exhaustion
        
      - [ ] **Chaos testing**
        - Failure injection completed (LIB-053)
        - Recovery validated
        - Fallbacks verified
        
      - [ ] **Shadow/canary completed**
        - Shadow test with production traffic
        - Metrics compared to baseline
        - No regressions identified
        
      **SECTION 6: SAFETY & COMPLIANCE (Must pass all)**
      
      - [ ] **Guardrails configured**
        - Content filters enabled
        - Sensitive information filters active
        - Denied topics configured
        - Guardrail effectiveness tested
        
      - [ ] **Security validated**
        - IAM least privilege verified
        - Network security configured
        - Secrets management implemented
        - Security review completed
        
      - [ ] **Compliance verified**
        - Regulatory requirements documented
        - PII handling compliant
        - Audit logging enabled
        - Data retention compliant
        
      **SECTION 7: SLOs DEFINED (Must pass all)**
      
      - [ ] **SLOs documented**
        ```yaml
        slos:
          availability: 99.9%
          latency_p99: 2000ms
          error_rate: <0.1%
          quality_score: >85%
          cost_per_request: <$0.05
        ```
        
      - [ ] **SLO monitoring configured**
        - Burn rate alerts set
        - Error budget tracking enabled
        - SLO dashboard created
        
      - [ ] **SLO review process**
        - Weekly SLO review scheduled
        - Escalation for SLO breach defined
        
      **SCORING:**
      ```
      Each section: PASS = All items checked or N/A with approval
      
      Production readiness:
      - All 7 sections PASS → Ready for production
      - Any section FAIL → Not production-ready
      
      Approval required:
      - Engineering Lead: Sections 1-5
      - AI Governance Lead: Section 6
      - Product Lead: Section 7 (SLOs)
      ```
      
      **Quick reference thresholds:**
      
      | Requirement | Minimum for Production |
      |-------------|------------------------|
      | Availability | 99.9% (or per SLO) |
      | Latency p99 | < 3x baseline |
      | Error rate | < 1% |
      | Quality score | > 80% |
      | Load test | 2x peak traffic |
      | Chaos tests | 3+ scenarios |
      | Runbook coverage | All critical paths |
      | On-call coverage | 24/7 |
      
      **PALETTE integration:**
      - Use as Deployment Readiness gate (RIU-060)
      - Track in RIU-100 (Incident preparedness)
      - Reference in RIU-102 (Escalation Matrix)
      - Update post-incident as needed
      
      Key insight: "Production-ready" is a bar, not a feeling. Every checkbox should have evidence. If you can't prove it, you haven't done it.

## Evidence

- **Tier 1 (entry-level)**: [Reliability for GenerativeAI applications - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_7_resilience_high_availability/resilience.html)
- **Tier 1 (entry-level)**: [Deploying generative AI applications - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_9_AIOps/aiops_deployment.html)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-060](../rius/RIU-060.md)
- [RIU-100](../rius/RIU-100.md)
- [RIU-101](../rius/RIU-101.md)
- [RIU-102](../rius/RIU-102.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Narrator](../agents/narrator.md)

## Learning Path

- [RIU-060](../paths/RIU-060-deployment-readiness-envelope.md) — hands-on exercise
- [RIU-102](../paths/RIU-102-enablement-pack.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-054.
Evidence tier: 1.
Journey stage: evaluation.
