---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-071
source_hash: sha256:a388b6055b83c4df
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, auditability, compliance, documentation, explainability, knowledge-entry]
related: [RIU-004, RIU-140, RIU-530, RIU-532, RIU-534]
handled_by: [architect, narrator, researcher, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What documentation proves AI system decisions are auditable and explainable?

Audit-ready documentation answers three questions: "What did the AI do?" (decision logs), "Why did it do that?" (explainability), and "Who was responsible?" (governance). Maintain these artifacts continuously, not just before audits.

## Definition

Audit-ready documentation answers three questions: "What did the AI do?" (decision logs), "Why did it do that?" (explainability), and "Who was responsible?" (governance). Maintain these artifacts continuously, not just before audits.
      
      **Documentation package for AI auditability:**
      
      ```
      ┌─────────────────────────────────────────────────────────────┐
      │              AI AUDIT DOCUMENTATION PACKAGE                  │
      ├─────────────────────────────────────────────────────────────┤
      │                                                             │
      │  ┌─────────────────────────────────────────────────────┐   │
      │  │ SYSTEM DOCUMENTATION                                 │   │
      │  │ • Model cards (what the AI is and does)             │   │
      │  │ • Architecture documentation (how it works)          │   │
      │  │ • Technical specifications                          │   │
      │  └─────────────────────────────────────────────────────┘   │
      │                                                             │
      │  ┌─────────────────────────────────────────────────────┐   │
      │  │ GOVERNANCE DOCUMENTATION                             │   │
      │  │ • Risk assessments                                   │   │
      │  │ • Policies and procedures                           │   │
      │  │ • Human oversight records                           │   │
      │  └─────────────────────────────────────────────────────┘   │
      │                                                             │
      │  ┌─────────────────────────────────────────────────────┐   │
      │  │ OPERATIONAL DOCUMENTATION                            │   │
      │  │ • Decision logs (audit trails)                      │   │
      │  │ • Incident records                                  │   │
      │  │ • Performance monitoring                            │   │
      │  └─────────────────────────────────────────────────────┘   │
      │                                                             │
      │  ┌─────────────────────────────────────────────────────┐   │
      │  │ EXPLAINABILITY DOCUMENTATION                         │   │
      │  │ • Decision rationale                                │   │
      │  │ • Input/output traceability                         │   │
      │  │ • Verification evidence                             │   │
      │  └─────────────────────────────────────────────────────┘   │
      │                                                             │
      └─────────────────────────────────────────────────────────────┘
      ```
      
      **1. Model Card (per AI model/system):**
      
      ```yaml
      model_card:
        # Identity
        model_name: "Customer Support AI Assistant v2.1"
        model_id: "cs-assistant-prod-v2.1"
        owner: "AI Platform Team"
        last_updated: "2024-06-15"
        
        # Purpose and Use
        intended_use:
          primary: "Answer customer questions about products and orders"
          secondary: "Route complex inquiries to human agents"
          out_of_scope:
            - "Medical or legal advice"
            - "Financial transactions"
            - "Personal data modifications"
            
        # Model Details
        technical_details:
          base_model: "anthropic.claude-3-sonnet-20240229"
          fine_tuning: "None (prompt-based)"
          knowledge_base: "Product catalog + FAQ (updated weekly)"
          guardrails: "Bedrock Guardrail ID: gr-abc123"
          
        # Performance
        performance:
          accuracy_metrics:
            task: "Answer correctness"
            score: "87% on evaluation set (n=1000)"
            evaluation_date: "2024-06-01"
          latency:
            p50: "800ms"
            p99: "2.1s"
          known_limitations:
            - "May struggle with multi-part questions"
            - "Cannot access real-time inventory"
            - "Occasionally misattributes product features"
            
        # Fairness and Safety
        responsible_ai:
          bias_testing: "Conducted 2024-05-15, no significant demographic bias detected"
          content_filtering: "Enabled for harmful content, PII"
          human_oversight: "Escalation to human for low-confidence responses"
          
        # Compliance
        compliance:
          applicable_regulations: ["GDPR", "CCPA"]
          data_processing: "No PII stored beyond session"
          audit_framework: "AWS Audit Manager GenAI Best Practices"
      ```
      
      **2. Risk Assessment Documentation:**
      
      ```yaml
      risk_assessment:
        assessment_id: "RA-2024-CS-001"
        system: "Customer Support AI Assistant"
        assessment_date: "2024-05-15"
        assessor: "AI Governance Team"
        
        risk_register:
          - risk_id: "R001"
            description: "AI provides incorrect product information"
            category: "Accuracy"
            likelihood: "Medium"
            impact: "Medium"
            risk_score: "Medium"
            controls:
              - "Knowledge base validation"
              - "Citation requirements"
              - "Human escalation for uncertainty"
            owner: "Product Data Team"
            status: "Controlled"
            
          - risk_id: "R002"
            description: "AI discloses customer PII inappropriately"
            category: "Privacy"
            likelihood: "Low"
            impact: "High"
            risk_score: "Medium"
            controls:
              - "PII guardrails enabled"
              - "Output filtering"
              - "Session isolation"
            owner: "Security Team"
            status: "Controlled"
            
        mitigation_tracking:
          - risk_id: "R001"
            action: "Implement citation requirements"
            status: "Complete"
            completion_date: "2024-04-20"
            evidence: "PR #1234, Test results"
            
        next_review: "2024-08-15"
      ```
      
      **3. Decision Audit Logs:**
      
      ```yaml
      audit_log_requirements:
        # What to log for every AI decision
        per_decision:
          required:
            - "request_id (unique identifier)"
            - "timestamp"
            - "user/session identifier"
            - "input (or hash if PII)"
            - "output"
            - "model_version"
            - "prompt_version"
            - "guardrail_results"
            - "confidence_score (if available)"
            
          for_explainability:
            - "retrieved_context (RAG sources)"
            - "citations"
            - "reasoning_trace (if available)"
            
          for_governance:
            - "human_review_status"
            - "approval_records"
            - "escalation_records"
            
        retention:
          standard: "2 years"
          regulated_high_risk: "10 years"
          query_capability: "Retrievable within 72 hours"
          
        immutability:
          - "S3 Object Lock (GOVERNANCE mode)"
          - "CloudTrail log file validation"
          - "No delete permissions for audit logs"
      ```
      
      **4. Human Oversight Documentation:**
      
      ```yaml
      human_oversight_records:
        review_process:
          description: "How humans review AI outputs"
          documentation:
            - "Review criteria and guidelines"
            - "Reviewer qualifications"
            - "Review workflow diagrams"
            
        approval_records:
          per_approval:
            - "Decision ID"
            - "Reviewer identity"
            - "Timestamp"
            - "Decision (approve/reject/modify)"
            - "Reason (if rejected/modified)"
            
        escalation_records:
          per_escalation:
            - "Trigger reason"
            - "Escalation path taken"
            - "Resolution"
            - "Time to resolution"
            
        oversight_metrics:
          - "% of decisions reviewed"
          - "Approval/rejection rates"
          - "Average review time"
          - "Escalation frequency"
      ```
      
      **5. Explainability Evidence:**
      
      ```yaml
      explainability_documentation:
        decision_rationale:
          # How to explain individual decisions
          components:
            - "Input factors considered"
            - "Sources/citations used"
            - "Confidence level"
            - "Alternative options considered (if applicable)"
            
        verification_methods:
          automated_reasoning:
            tool: "Bedrock Guardrails Automated Reasoning"
            use: "Verify responses against logical rules"
            evidence: "Verification results per decision"
            
          citation_verification:
            use: "Link claims to source documents"
            evidence: "Timestamped citations with source links"
            
          human_verification:
            use: "Spot-check accuracy"
            evidence: "Review records with findings"
            
        for_affected_persons:
          # When someone asks "why did AI decide this?"
          documentation:
            - "Plain language explanation template"
            - "Process for handling explanation requests"
            - "Response time SLA"
            - "Appeal/contestation process"
      ```
      
      **Audit preparation checklist:**
      
      ```yaml
      audit_preparation:
        before_audit:
          - "Verify all documentation is current"
          - "Ensure audit logs are queryable"
          - "Prepare system access for auditors"
          - "Brief relevant personnel"
          - "Compile evidence for controls"
          
        evidence_collection:
          - "Model cards (current versions)"
          - "Risk assessments (most recent + history)"
          - "Sample audit logs (representative period)"
          - "Human oversight records"
          - "Incident response records"
          - "Training records (staff)"
          - "Policy documents"
          
        tools:
          - "AWS Audit Manager (evidence collection)"
          - "CloudTrail (API activity)"
          - "CloudWatch Logs (operational logs)"
          - "S3 (document storage)"
      ```
      
      **AWS Audit Manager 8 Principles:**
      
      | Principle | What to Document |
      |-----------|------------------|
      | Accuracy | Evaluation results, error rates, validation procedures |
      | Fairness | Bias testing results, demographic analysis |
      | Privacy | Data handling policies, PII controls, consent records |
      | Resilience | Failover testing, recovery procedures |
      | Explainability | Decision rationale, citation systems |
      | Safety | Guardrail configurations, content filtering |
      | Security | Access controls, encryption, audit logs |
      | Sustainability | Resource usage, efficiency metrics |
      
      **PALETTE integration:**
      - Store model cards in RIU-532 (Model Registry)
      - Document governance in RIU-530 (AI Governance Config)
      - Configure audit logging in RIU-534 (Audit Trail Config)
      - Train team on requirements using RIU-140 (Training Materials)
      
      Key insight: Documentation isn't for auditors — it's for you. If you can't explain why the AI made a decision six months ago, you can't defend it, improve it, or trust it. Audit-ready documentation is operational documentation done well.

## Evidence

- **Tier 1 (entry-level)**: [Risk and Compliance Management for Generative AI](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/5_2_governance_and_organization/5_2_3_risk_and_compliance_mngmt.html)
- **Tier 1 (entry-level)**: [Generative AI adoption and compliance with AWS Audit Manager](https://aws.amazon.com/blogs/security/generative-ai-adoption-and-compliance-simplifying-the-path-forward-with-aws-audit-manager/)
- **Tier 1 (entry-level)**: [Build verifiable explainability with Automated Reasoning checks for Amazon Bedrock Guardrails](https://aws.amazon.com/blogs/machine-learning/build-verifiable-explainability-into-financial-services-workflows-with-automated-reasoning-checks-for-amazon-bedrock-guardrails/)
- **Tier 1 (entry-level)**: [Generative AI Lifecycle Operational Excellence framework on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/introduction.html)
- **Tier 1 (entry-level)**: [Anthropic Transparency Hub — Model Report](https://www.anthropic.com/transparency/model-report)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-004](../rius/RIU-004.md)
- [RIU-140](../rius/RIU-140.md)
- [RIU-530](../rius/RIU-530.md)
- [RIU-532](../rius/RIU-532.md)
- [RIU-534](../rius/RIU-534.md)

## Handled By

- [Architect](../agents/architect.md)
- [Narrator](../agents/narrator.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-071.
Evidence tier: 1.
Journey stage: all.
