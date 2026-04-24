---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-073
source_hash: sha256:1b7f747ba12154c1
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, compliance, governance, knowledge-entry, minimum-viable, regulation]
related: [RIU-140, RIU-530, RIU-531, RIU-533]
handled_by: [architect, debugger, narrator, researcher, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What's the minimum viable governance for AI systems in regulated industries?

"Minimum viable" in regulated industries means: enough governance to be defensible to regulators, not comprehensive governance. Start with what can get you shut down (risk, audit, oversight), then iterate.

## Definition

"Minimum viable" in regulated industries means: enough governance to be defensible to regulators, not comprehensive governance. Start with what can get you shut down (risk, audit, oversight), then iterate.
      
      **Minimum viable governance framework:**
      
      ```
      ┌─────────────────────────────────────────────────────────────┐
      │           MINIMUM VIABLE AI GOVERNANCE                       │
      ├─────────────────────────────────────────────────────────────┤
      │                                                             │
      │  TIER 1: NON-NEGOTIABLE (Day 1)                             │
      │  ─────────────────────────────                              │
      │  ✓ Risk assessment completed                                │
      │  ✓ Human oversight for high-stakes decisions                │
      │  ✓ Audit logging enabled                                    │
      │  ✓ Data governance basics (PII, access controls)            │
      │  ✓ Accountability assigned (who owns this?)                 │
      │                                                             │
      │  TIER 2: REQUIRED (Within 30 days)                          │
      │  ─────────────────────────────────                          │
      │  ✓ Policies documented                                      │
      │  ✓ Model documentation (model cards)                        │
      │  ✓ Incident response procedures                             │
      │  ✓ Training for operators                                   │
      │  ✓ Monitoring dashboards                                    │
      │                                                             │
      │  TIER 3: MATURE (Within 90 days)                            │
      │  ───────────────────────────────                            │
      │  ○ Automated compliance checks                              │
      │  ○ Bias/fairness testing                                    │
      │  ○ Third-party audits                                       │
      │  ○ Governance board established                             │
      │  ○ Continuous improvement process                           │
      │                                                             │
      └─────────────────────────────────────────────────────────────┘
      ```
      
      **Tier 1: Non-negotiable controls (Day 1)**
      
      ```yaml
      tier_1_controls:
        risk_assessment:
          requirement: "Document what can go wrong"
          minimum_content:
            - "AI system description and purpose"
            - "Risk identification (what could fail)"
            - "Impact assessment (who gets hurt)"
            - "Risk mitigation (how we prevent/reduce)"
          regulator_question: "Did you assess the risks before deploying?"
          
        human_oversight:
          requirement: "Human decision-maker for significant impacts"
          implementation:
            - "High-stakes decisions require human approval"
            - "Escalation path defined"
            - "Override capability available"
          regulator_question: "Who was responsible for this decision?"
          
        audit_logging:
          requirement: "Prove what happened"
          minimum_logging:
            - "All AI decisions (input, output, timestamp)"
            - "Who accessed the system"
            - "Configuration changes"
          retention: "Per regulatory requirement (often 5-10 years)"
          regulator_question: "Show me the record of this transaction"
          
        data_governance:
          requirement: "Know your data, protect it"
          minimum_controls:
            - "PII identified and protected"
            - "Access controls implemented"
            - "Data lineage documented"
          regulator_question: "Where did this data come from? Who can access it?"
          
        accountability:
          requirement: "Named responsible party"
          implementation:
            - "AI system owner identified"
            - "Decision authority defined"
            - "Escalation contacts documented"
          regulator_question: "Who is accountable for this system?"
      ```
      
      **Industry-specific requirements:**
      
      | Industry | Key Regulation | Minimum Viable Additions |
      |----------|----------------|--------------------------|
      | **Financial Services** | OCC guidance, FFIEC, GDPR, EU AI Act | Model risk management, fair lending testing, explainable credit decisions |
      | **Healthcare** | HIPAA, FDA guidance, HITECH | PHI protection, clinical decision support safeguards, validation studies |
      | **Government (US)** | OMB M-24-10, EO 14110 | Rights-impacting AI inventory, public transparency, procurement requirements |
      | **Government (EU)** | EU AI Act | Risk classification, conformity assessment, CE marking (high-risk) |
      | **Insurance** | State regulations, NAIC guidance | Actuarial review, non-discrimination testing, rate justification |
      
      **Financial Services specifics:**
      
      ```yaml
      fsi_minimum_governance:
        model_risk_management:
          requirement: "SR 11-7 / OCC 2011-12 applies to AI"
          controls:
            - "Model validation (independent review)"
            - "Model inventory maintained"
            - "Performance monitoring"
            - "Model documentation"
            
        fair_lending:
          requirement: "ECOA, Fair Housing Act"
          controls:
            - "Disparate impact testing"
            - "Adverse action notices with reasons"
            - "No prohibited factors in decisions"
            
        consumer_protection:
          requirement: "UDAP/UDAAP"
          controls:
            - "Clear disclosure of AI use"
            - "Accurate representations"
            - "Consumer recourse available"
            
        aws_tools:
          - "Bedrock Guardrails (content filtering)"
          - "SageMaker Model Monitor (drift detection)"
          - "AWS Audit Manager (GenAI framework)"
      ```
      
      **Healthcare specifics:**
      
      ```yaml
      healthcare_minimum_governance:
        hipaa_compliance:
          requirement: "Protected Health Information"
          controls:
            - "PHI not used in training without authorization"
            - "BAA with AI service providers"
            - "Access logging for PHI"
            - "Minimum necessary principle"
            
        clinical_decision_support:
          requirement: "FDA guidance (if applicable)"
          controls:
            - "Intended use clearly defined"
            - "Clinical validation documentation"
            - "Human clinician in the loop"
            - "Clear disclaimers"
            
        patient_safety:
          requirement: "First, do no harm"
          controls:
            - "Failsafe to human for uncertainty"
            - "Adverse event reporting"
            - "Quality monitoring"
      ```
      
      **Government specifics:**
      
      ```yaml
      government_minimum_governance:
        omb_m24_10_requirements:
          # For US federal agencies
          controls:
            - "AI use case inventory"
            - "Rights-impacting AI identification"
            - "Minimum risk management practices"
            - "Chief AI Officer designated"
            
        transparency:
          requirement: "Public accountability"
          controls:
            - "Public disclosure of AI use cases"
            - "Algorithmic impact assessments"
            - "Citizen recourse mechanisms"
            
        procurement:
          requirement: "Responsible AI acquisition"
          controls:
            - "Vendor AI governance assessment"
            - "Contractual compliance requirements"
            - "Ongoing monitoring obligations"
      ```
      
      **Minimum viable checklist (all industries):**
      
      ```yaml
      mvg_checklist:
        # Complete before production deployment
        before_go_live:
          risk:
            - "Risk assessment completed and documented"
            - "Risk owner identified"
            - "Mitigation controls implemented"
            
          oversight:
            - "Human oversight process defined"
            - "Escalation path documented"
            - "Override capability tested"
            
          audit:
            - "Logging enabled for all decisions"
            - "Logs stored immutably"
            - "Query capability verified"
            
          data:
            - "PII/sensitive data identified"
            - "Access controls implemented"
            - "Data lineage documented"
            
          accountability:
            - "System owner named"
            - "Contact information current"
            - "Responsibilities documented"
            
        # Document but can refine post-launch
          policy:
            - "Acceptable use policy drafted"
            - "Incident response procedure exists"
            - "Training plan identified"
            
        # Can iterate after launch
          optimization:
            - "Bias testing planned"
            - "Governance board formation planned"
            - "Automation roadmap defined"
      ```
      
      **Phase-in approach:**
      
      | Phase | Timeline | Focus | Governance Maturity |
      |-------|----------|-------|---------------------|
      | **Launch** | Day 0 | Tier 1 controls | Defensible minimum |
      | **Stabilize** | Days 1-30 | Tier 2 documentation | Documented processes |
      | **Mature** | Days 31-90 | Tier 3 automation | Scalable governance |
      | **Optimize** | Ongoing | Continuous improvement | Best-in-class |
      
      **PALETTE integration:**
      - Configure controls in RIU-530 (AI Governance Config)
      - Implement guardrails via RIU-531 (Guardrail Selection)
      - Document in RIU-533 (FRIA - Fundamental Rights Impact Assessment)
      - Train team using RIU-140 (Training Materials)
      
      Key insight: "Minimum viable" doesn't mean "minimal" — it means "enough to be defensible." When a regulator asks, you need to answer: "Yes, we assessed the risks. Yes, humans are in the loop. Yes, we have records. Here's who's responsible." If you can answer those four questions, you have minimum viable governance.

## Evidence

- **Tier 1 (entry-level)**: [Governance by design: The essential guide for successful AI scaling](https://aws.amazon.com/blogs/machine-learning/governance-by-design-the-essential-guide-for-successful-ai-scaling/)
- **Tier 1 (entry-level)**: [AWS User Guide to GRC for Responsible AI Adoption in Financial Services](https://aws.amazon.com/blogs/security/introducing-the-aws-user-guide-to-governance-risk-and-compliance-for-responsible-ai-adoption-within-financial-services-industries/)
- **Tier 1 (entry-level)**: [Generative AI adoption and compliance with AWS Audit Manager](https://aws.amazon.com/blogs/security/generative-ai-adoption-and-compliance-simplifying-the-path-forward-with-aws-audit-manager/)
- **Tier 1 (entry-level)**: [How AWS helps agencies meet OMB AI governance requirements](https://aws.amazon.com/blogs/publicsector/how-aws-helps-agencies-meet-omb-ai-governance-requirements/)
- **Tier 1 (entry-level)**: [Regulatory Compliance and Governance - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_5_security_privacy/3_5_3_compliance_data_protection/3_5_3-2_regulatory_governance/regulatory_governance.html)
- **Tier 1 (entry-level)**: [NIST AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework)
- **Tier 1 (entry-level)**: [NIST AI 600-1: Generative AI Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-140](../rius/RIU-140.md)
- [RIU-530](../rius/RIU-530.md)
- [RIU-531](../rius/RIU-531.md)
- [RIU-533](../rius/RIU-533.md)

## Handled By

- [Architect](../agents/architect.md)
- [Debugger](../agents/debugger.md)
- [Narrator](../agents/narrator.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-073.
Evidence tier: 1.
Journey stage: all.
