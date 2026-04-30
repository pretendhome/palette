---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-067
source_hash: sha256:902701246c5a40b7
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, compliance, eu-ai-act, explainability, knowledge-entry, regulation]
related: [RIU-140, RIU-530, RIU-531, RIU-533, RIU-534]
handled_by: [architect, debugger, narrator, researcher, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What explainability is actually required for EU AI Act compliance?

EU AI Act explainability requirements depend on risk classification. "Explainability" means different things at each level: from simple disclosure ("this is AI") to comprehensive decision traceability for high-risk systems.

## Definition

EU AI Act explainability requirements depend on risk classification. "Explainability" means different things at each level: from simple disclosure ("this is AI") to comprehensive decision traceability for high-risk systems.
      
      **EU AI Act risk classification:**
      
      | Risk Level | Examples | Status |
      |------------|----------|--------|
      | **Unacceptable** | Social scoring, real-time biometric ID in public | PROHIBITED |
      | **High-Risk** | Employment, credit, healthcare, education, critical infrastructure | REGULATED |
      | **Limited Risk** | Chatbots, emotion recognition, deepfakes | TRANSPARENCY |
      | **Minimal Risk** | Spam filters, AI-enhanced games | LARGELY UNREGULATED |
      
      **Explainability requirements by risk level:**
      
      ```
      ┌─────────────────────────────────────────────────────────────┐
      │              EXPLAINABILITY REQUIREMENTS                     │
      ├─────────────────────────────────────────────────────────────┤
      │                                                             │
      │  UNACCEPTABLE RISK                                          │
      │  ─────────────────                                          │
      │  N/A - These systems are prohibited                         │
      │                                                             │
      │  HIGH-RISK                                                   │
      │  ─────────                                                   │
      │  ✓ Technical documentation of system design                 │
      │  ✓ Human oversight mechanisms                               │
      │  ✓ Decision traceability and logging                        │
      │  ✓ Explanation capability for affected persons              │
      │  ✓ Conformity assessment                                    │
      │                                                             │
      │  LIMITED RISK                                                │
      │  ────────────                                                │
      │  ✓ Disclosure that user is interacting with AI              │
      │  ✓ Label AI-generated content (deepfakes)                   │
      │  ✓ Notify emotion recognition use                           │
      │                                                             │
      │  MINIMAL RISK                                                │
      │  ────────────                                                │
      │  ○ Voluntary codes of conduct                               │
      │  ○ Best practices encouraged                                │
      │                                                             │
      └─────────────────────────────────────────────────────────────┘
      ```
      
      **High-Risk AI: What explainability actually means**
      
      ```yaml
      high_risk_explainability:
        # Article 13 - Transparency and provision of information
        
        technical_documentation:
          required: true
          must_include:
            - "General description of the AI system"
            - "Detailed description of elements and development process"
            - "Information on training data"
            - "Metrics used for accuracy, robustness, cybersecurity"
            - "Human oversight measures"
            - "Expected lifetime and maintenance"
            
        for_deployers:
          # Organizations using high-risk AI must understand it
          required:
            - "Clear instructions for use"
            - "System capabilities and limitations"
            - "Circumstances that may impact performance"
            - "Human oversight procedures"
            - "Technical measures for interpretation"
            
        for_affected_persons:
          # People impacted by AI decisions have rights
          required:
            - "Right to explanation of individual decision"
            - "Meaningful information about logic involved"
            - "Ability to contest decisions"
          practical_meaning:
            - "Why was this loan denied?"
            - "Why was this candidate rejected?"
            - "Why was this claim flagged?"
            
        logging_requirements:
          # Automatic logging for traceability
          must_log:
            - "Period of use"
            - "Reference database used"
            - "Input data"
            - "Output/decision"
          retention: "Appropriate to intended purpose"
      ```
      
      **Limited Risk: Transparency requirements**
      
      ```yaml
      limited_risk_transparency:
        # Article 50 - Transparency obligations
        
        chatbots_virtual_assistants:
          requirement: "Inform user they are interacting with AI"
          implementation:
            - "Clear statement: 'You are chatting with an AI assistant'"
            - "Visible indicator in UI"
            - "Not buried in terms of service"
          exception: "Obvious from context"
          
        emotion_recognition:
          requirement: "Inform persons being analyzed"
          implementation:
            - "Notice before analysis begins"
            - "Consent where required"
            
        deepfakes_synthetic_content:
          requirement: "Label AI-generated content"
          implementation:
            - "Machine-readable marking"
            - "Disclosure that content is AI-generated"
          exceptions: "Artistic, satirical, or editorial use with safeguards"
      ```
      
      **Implementation checklist by risk level:**
      
      **High-Risk Compliance:**
      ```yaml
      high_risk_checklist:
        # Must have all of these
        documentation:
          - "System design documentation complete"
          - "Training data documented"
          - "Performance metrics recorded"
          - "Risk assessment conducted"
          
        technical_measures:
          - "Logging enabled for all decisions"
          - "Audit trail satisfies Article 12 requirements"
          - "Human oversight mechanisms in place"
          - "Ability to generate explanations"
          
        organizational_measures:
          - "Designated personnel for oversight"
          - "Procedures for handling explanation requests"
          - "Conformity assessment completed"
          - "EU database registration (where required)"
          
        ongoing_obligations:
          - "Post-market monitoring"
          - "Incident reporting procedures"
          - "Regular compliance reviews"
      ```
      
      **Limited-Risk Compliance:**
      ```yaml
      limited_risk_checklist:
        chatbots:
          - "AI disclosure implemented in UI"
          - "Disclosure visible before/during interaction"
          
        content_generation:
          - "AI-generated content labeled"
          - "Machine-readable watermarking (where feasible)"
          
        documentation:
          - "Transparency measures documented"
          - "Evidence of compliance maintained"
      ```
      
      **Practical explanation implementation:**
      
      ```yaml
      explanation_approaches:
        # Different approaches for different needs
        
        user_facing_explanation:
          # What to tell end users
          components:
            - "Plain language summary of decision factors"
            - "Key inputs that influenced outcome"
            - "How to contest or seek review"
          format: "Human-readable, accessible"
          example: |
            "Your application was declined because:
            - Income to debt ratio exceeded threshold
            - Employment duration below minimum
            To appeal, contact support@..."
            
        technical_explanation:
          # For auditors and compliance
          components:
            - "Model version and configuration"
            - "Input features used"
            - "Decision confidence score"
            - "Comparable approved/rejected cases"
          format: "Structured logs, queryable"
          
        regulatory_explanation:
          # For EU authorities
          components:
            - "Full technical documentation"
            - "Conformity assessment"
            - "Risk management records"
            - "Post-market monitoring results"
          format: "Per Annex IV requirements"
      ```
      
      **AWS tools for compliance:**
      
      | Requirement | AWS Tool | How It Helps |
      |-------------|----------|--------------|
      | Documentation | AI Service Cards | Model capabilities and limitations |
      | Logging | CloudTrail + CloudWatch | Decision audit trail |
      | Transparency | Bedrock model info | Model provenance |
      | Monitoring | SageMaker Model Monitor | Performance tracking |
      | Risk Assessment | AWS Audit Manager | GenAI best practices framework |
      
      **Implementation timeline:**
      
      | Date | What Takes Effect |
      |------|-------------------|
      | **Feb 2025** | Prohibited AI practices banned |
      | **Aug 2025** | GPAI model obligations |
      | **Aug 2026** | High-risk AI requirements (most) |
      | **Aug 2027** | High-risk AI in Annex I products |
      
      **Penalties for non-compliance:**
      
      | Violation | Maximum Fine |
      |-----------|--------------|
      | Prohibited AI practices | €35M or 7% global revenue |
      | High-risk AI non-compliance | €15M or 3% global revenue |
      | Incorrect information to authorities | €7.5M or 1% global revenue |
      
      **PALETTE integration:**
      - Document risk classification in RIU-533 (FRIA - Fundamental Rights Impact Assessment)
      - Configure transparency measures in RIU-530 (AI Governance Config)
      - Implement logging per RIU-534 (Audit Trail Config)
      - Train team using RIU-140 (Training Materials)
      
      Key insight: "Explainability" under EU AI Act isn't about technical XAI methods — it's about providing meaningful information to users, deployers, and authorities. A simple, clear explanation of why a decision was made is more compliant than a complex SHAP analysis that no one understands.

## Evidence

- **Tier 1 (entry-level)**: [Building trust in AI: The AWS approach to the EU AI Act](https://aws.amazon.com/blogs/machine-learning/building-trust-in-ai-the-aws-approach-to-the-eu-ai-act/)
- **Tier 1 (entry-level)**: [Regulatory Compliance and Governance - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_5_security_privacy/3_5_3_compliance_data_protection/3_5_3-2_regulatory_governance/regulatory_governance.html)
- **Tier 1 (entry-level)**: [Risk and Compliance Management for Generative AI](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/5_2_governance_and_organization/5_2_3_risk_and_compliance_mngmt.html)
- **Tier 1 (entry-level)**: [Securing generative AI: data, compliance, and privacy considerations](https://aws.amazon.com/blogs/security/securing-generative-ai-data-compliance-and-privacy-considerations/)
- **Tier 1 (entry-level)**: [EU AI Act — Official Text, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-140](../rius/RIU-140.md)
- [RIU-530](../rius/RIU-530.md)
- [RIU-531](../rius/RIU-531.md)
- [RIU-533](../rius/RIU-533.md)
- [RIU-534](../rius/RIU-534.md)

## Handled By

- [Architect](../agents/architect.md)
- [Debugger](../agents/debugger.md)
- [Narrator](../agents/narrator.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-067.
Evidence tier: 1.
Journey stage: all.
