---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-043
source_hash: sha256:ff4b5660c26836c2
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [checklist, evaluation, knowledge-entry, production-readiness, quality-criteria, standards]
related: [RIU-012, RIU-021, RIU-060, RIU-062, RIU-081, RIU-082, RIU-083, RIU-084]
handled_by: [architect, builder, debugger, validator]
journey_stage: evaluation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What's the checklist for 'production-ready' data quality in AI systems?

Use this checklist before deploying AI systems to production. All items should be "PASS" or explicitly "N/A with rationale" before go-live.

## Definition

Use this checklist before deploying AI systems to production. All items should be "PASS" or explicitly "N/A with rationale" before go-live.
      
      **SECTION 1: Security & Privacy (MUST PASS ALL)**
      
      - [ ] **PII inventory complete**: All PII/PHI fields identified and documented (RIU-012)
      - [ ] **PII handling implemented**: Anonymization, masking, or encryption in place
      - [ ] **Legal/security approval**: Explicit sign-off for any sensitive data use
      - [ ] **Access controls configured**: IAM policies, fine-grained permissions
      - [ ] **Audit logging enabled**: CloudTrail tracking all data access
      - [ ] **Vector embeddings secured**: Encryption + access controls for RAG systems
      
      **SECTION 2: Data Documentation (MUST PASS ALL)**
      
      - [ ] **Data dictionary exists**: All fields used by AI are documented (LIB-035)
      - [ ] **Data lineage documented**: Origin, transformations, dependencies tracked
      - [ ] **Data catalog entry**: Dataset registered in DataZone/Glue Catalog
      - [ ] **Data owner identified**: Clear accountability for each dataset
      - [ ] **Retention policy defined**: How long data is kept, when deleted
      
      **SECTION 3: Data Quality Rules (MUST PASS ALL)**
      
      - [ ] **Schema validation**: All fields match expected types/formats
      - [ ] **Completeness thresholds**: Required fields meet minimum fill rates
        ```
        Example: customer_id completeness >= 99.9%
        ```
      - [ ] **Validity rules**: Values within expected ranges/enums
        ```
        Example: status IN ('active', 'pending', 'closed')
        ```
      - [ ] **Uniqueness constraints**: Key fields are unique where required
      - [ ] **Referential integrity**: Foreign keys exist in referenced tables
      - [ ] **Semantic validation**: Business rules verified (LIB-041)
      
      **SECTION 4: Data Quality Baselines (MUST PASS ALL)**
      
      - [ ] **Baseline metrics established**:
        ```yaml
        baseline:
          completeness: 98.5%
          validity: 97.2%
          freshness: "< 1 hour"
          volume: "45,000-55,000 records/day"
        ```
      - [ ] **Quality thresholds defined**: Warning and critical levels set (LIB-040)
      - [ ] **Monitoring configured**: CloudWatch dashboards and alerts
      - [ ] **Drift detection enabled**: Statistical monitoring for distribution shifts
      
      **SECTION 5: Data Pipeline Quality (MUST PASS ALL)**
      
      - [ ] **Quality gates implemented**: Bad data routed to rejected layer
      - [ ] **Quality checks automated**: Run on every pipeline execution
      - [ ] **Quarantine process defined**: How rejected data is reviewed/fixed
      - [ ] **Alerting configured**: Notifications when quality drops
      - [ ] **Recovery procedures documented**: How to reprocess failed data
      
      **SECTION 6: Evaluation Data (MUST PASS for AI/ML)**
      
      - [ ] **Golden set exists**: Curated evaluation dataset (RIU-021)
      - [ ] **Golden set versioned**: Immutable snapshots with version IDs
      - [ ] **Label quality validated**: Inter-annotator agreement measured (LIB-036)
      - [ ] **Edge cases included**: Boundary conditions and known failures
      - [ ] **Distribution representative**: Evaluation data reflects production distribution
      
      **SECTION 7: Operational Readiness (MUST PASS ALL)**
      
      - [ ] **Data freshness acceptable**: Latency from source meets requirements
      - [ ] **Volume tested**: Pipeline handles expected + 2x peak load
      - [ ] **Failure handling tested**: Pipeline recovers from source outages
      - [ ] **Runbook exists**: Documented procedures for data issues (RIU-062)
      - [ ] **On-call identified**: Clear ownership for data quality incidents
      
      **Scoring:**
      ```
      PASS: All checkboxes in section are ✓ or N/A with documented rationale
      FAIL: Any checkbox unchecked without rationale
      
      Production readiness: ALL sections must PASS
      ```
      
      **Quick reference thresholds:**
      | Metric | Minimum for Production |
      |--------|------------------------|
      | Schema compliance | 100% |
      | Required field completeness | 99%+ |
      | Validity rate | 95%+ |
      | Uniqueness (keys) | 100% |
      | Freshness | Per SLA |
      | Quality check automation | 100% coverage |
      
      **PALETTE integration:**
      - Document quality rules in RIU-084 (Data Quality Checks)
      - Store baselines in RIU-081 (E2E Smoke Tests)
      - Track in Deployment Readiness (RIU-060)
      - Include in go-live gate review
      
      Key insight: "Production-ready" isn't a feeling — it's this checklist with evidence for each item. If you can't show proof, you're not ready.

## Evidence

- **Tier 1 (entry-level)**: [Generative AI Lifecycle Operational Excellence framework on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/introduction.html)
- **Tier 1 (entry-level)**: [Data governance in the age of generative AI](https://aws.amazon.com/blogs/big-data/data-governance-in-the-age-of-generative-ai/)
- **Tier 1 (entry-level)**: [From raw to refined: building a data quality pipeline with AWS Glue and Amazon S3 Tables](https://aws.amazon.com/blogs/storage/from-raw-to-refined-building-a-data-quality-pipeline-with-aws-glue-and-amazon-s3-tables/)
- **Tier 1 (entry-level)**: [Implementing data governance on AWS](https://aws.amazon.com/blogs/security/implementing-data-governance-on-aws-automation-tagging-and-lifecycle-strategy-part-1/)
- **Tier 1 (entry-level)**: [Databricks: Best practices for data and AI governance](https://docs.databricks.com/gcp/en/lakehouse-architecture/data-governance/best-practices)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-012](../rius/RIU-012.md)
- [RIU-021](../rius/RIU-021.md)
- [RIU-060](../rius/RIU-060.md)
- [RIU-062](../rius/RIU-062.md)
- [RIU-081](../rius/RIU-081.md)
- [RIU-082](../rius/RIU-082.md)
- [RIU-083](../rius/RIU-083.md)
- [RIU-084](../rius/RIU-084.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-021](../paths/RIU-021-tiny-ai-eval-harness.md) — hands-on exercise
- [RIU-060](../paths/RIU-060-deployment-readiness-envelope.md) — hands-on exercise
- [RIU-082](../paths/RIU-082-llm-safety-guardrails.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-043.
Evidence tier: 1.
Journey stage: evaluation.
