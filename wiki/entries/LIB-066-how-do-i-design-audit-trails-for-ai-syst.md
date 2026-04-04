---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-066
source_hash: sha256:01860d9b30c7abb5
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, audit-trails, compliance, governance, knowledge-entry, transparency]
related: [RIU-140, RIU-530, RIU-531, RIU-534]
handled_by: [architect, debugger, narrator, researcher, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I design audit trails for AI systems that satisfy compliance requirements?

AI audit trails must answer: "What decision was made, by what model, with what inputs, under what configuration, and who approved it?" Design for both real-time monitoring and historical reconstruction.

## Definition

AI audit trails must answer: "What decision was made, by what model, with what inputs, under what configuration, and who approved it?" Design for both real-time monitoring and historical reconstruction.
      
      **What auditors ask (design to answer these):**
      
      | Auditor Question | Required Data | Source |
      |------------------|---------------|--------|
      | "What model made this decision?" | Model ID, version, endpoint | Request metadata |
      | "What was the input?" | Full request payload | Request logs |
      | "What was the output?" | Full response | Response logs |
      | "What guardrails were applied?" | Guardrail ID, actions taken | Guardrail logs |
      | "Who had access?" | IAM principals, roles | CloudTrail |
      | "What configuration was active?" | Prompts, thresholds, settings | Config audit |
      | "Was human oversight applied?" | Approval records | Workflow logs |
      | "Can this decision be reproduced?" | All inputs + config | Lineage tracking |
      
      **Audit log schema:**
      
      ```yaml
      ai_audit_log:
        # Request identification
        request_id: "uuid-v4"
        trace_id: "correlation-id-for-full-trace"
        timestamp: "2024-06-15T10:30:00Z"
        
        # Who
        principal:
          type: "IAMUser | IAMRole | ServiceAccount"
          arn: "arn:aws:iam::123456789012:user/jane"
          source_ip: "10.0.1.50"
          user_agent: "MyApp/1.0"
          
        # What model
        model:
          model_id: "anthropic.claude-3-sonnet"
          endpoint: "arn:aws:bedrock:us-east-1::foundation-model/..."
          inference_profile: "customer-a-profile"
          
        # Configuration at time of request
        configuration:
          prompt_version: "v1.2.3"
          guardrail_id: "guardrail-abc123"
          guardrail_version: "1"
          system_prompt_hash: "sha256:abc123..."
          
        # Input (with PII handling)
        input:
          type: "text | structured"
          content_hash: "sha256:..."  # Hash if PII
          content: "..."  # Full content if permitted
          token_count: 150
          
        # Output
        output:
          content_hash: "sha256:..."
          content: "..."
          token_count: 500
          finish_reason: "end_turn"
          
        # Safety and guardrails
        guardrail_result:
          action: "NONE | BLOCKED | MODIFIED"
          triggered_policies:
            - policy: "content-filter"
              severity: "MEDIUM"
              action: "allowed"
            - policy: "pii-filter"
              severity: "HIGH"
              action: "redacted"
              
        # Performance
        metrics:
          latency_ms: 1250
          time_to_first_token_ms: 350
          
        # Business context
        context:
          tenant_id: "acme-corp"
          application: "customer-support-bot"
          use_case: "product-inquiry"
          environment: "production"
          
        # Human oversight (if applicable)
        human_oversight:
          required: true
          approval_status: "approved | pending | rejected"
          approver: "arn:aws:iam::..."
          approval_timestamp: "2024-06-15T10:31:00Z"
      ```
      
      **Regulatory requirements by framework:**
      
      | Regulation | Key Audit Requirements | Retention |
      |------------|------------------------|-----------|
      | **EU AI Act** | Decision traceability, risk assessments, human oversight records | 10 years (high-risk) |
      | **GDPR** | Data processing records, consent, right to explanation | Duration of processing + years |
      | **HIPAA** | Access logs, PHI handling, breach records | 6 years |
      | **SOX** | Financial decision audit, controls evidence | 7 years |
      | **SOC 2** | Access controls, change management, incident response | Per audit period |
      | **CCPA** | Data access, deletion requests | 24 months |
      
      **AWS implementation architecture:**
      
      ```
      ┌─────────────────────────────────────────────────────────────┐
      │                    AI AUDIT ARCHITECTURE                     │
      ├─────────────────────────────────────────────────────────────┤
      │                                                             │
      │  ┌─────────┐        ┌─────────────────────────────────┐    │
      │  │ Bedrock │───────▶│ CloudWatch Logs (Request/Response)│   │
      │  │  API    │        └─────────────────────────────────┘    │
      │  └────┬────┘                      │                        │
      │       │                           ▼                        │
      │       │              ┌─────────────────────────────────┐   │
      │       │              │   S3 (Long-term retention)       │   │
      │       │              │   - Immutable (Object Lock)      │   │
      │       │              │   - Lifecycle policies           │   │
      │       │              └─────────────────────────────────┘   │
      │       │                                                     │
      │       ▼                                                     │
      │  ┌─────────────────────────────────────────────────────┐   │
      │  │          CloudTrail (API Activity)                   │   │
      │  │  - All Bedrock API calls                            │   │
      │  │  - IAM actions                                       │   │
      │  │  - Config changes                                    │   │
      │  └─────────────────────────────────────────────────────┘   │
      │                                                             │
      │  ┌─────────────────────────────────────────────────────┐   │
      │  │          AWS Audit Manager                           │   │
      │  │  - GenAI best practices framework                    │   │
      │  │  - Evidence collection                               │   │
      │  │  - Compliance reports                                │   │
      │  └─────────────────────────────────────────────────────┘   │
      │                                                             │
      └─────────────────────────────────────────────────────────────┘
      ```
      
      **Immutability and tamper-proofing:**
      
      ```yaml
      immutability_controls:
        s3_object_lock:
          mode: "GOVERNANCE"  # or COMPLIANCE for stricter
          retention_period: "7 years"
          purpose: "Prevent deletion/modification"
          
        cloudtrail:
          log_file_validation: true  # Digest files for integrity
          kms_encryption: true
          multi_region: true
          
        access_controls:
          write: "Automated systems only (no human write access)"
          read: "Auditors + compliance team"
          delete: "Requires compliance approval + waiting period"
          
        integrity_verification:
          - "CloudTrail digest validation"
          - "S3 object lock prevents modification"
          - "Checksums on all log entries"
      ```
      
      **Audit Manager GenAI framework (8 principles):**
      
      ```yaml
      audit_manager_framework:
        framework_id: "generative-ai-best-practices"
        
        control_sets:
          accuracy:
            - "Model evaluation results documented"
            - "Golden set test scores tracked"
            
          fairness:
            - "Bias testing conducted"
            - "Demographic parity monitored"
            
          privacy:
            - "PII handling documented"
            - "Data retention policies enforced"
            
          resilience:
            - "Failover tested"
            - "Recovery procedures documented"
            
          explainability:
            - "Decision rationale logged"
            - "Model cards available"
            
          safety:
            - "Guardrails configured"
            - "Content filtering active"
            
          security:
            - "Access controls implemented"
            - "Encryption enabled"
            
          sustainability:
            - "Resource usage tracked"
            - "Efficiency optimizations documented"
      ```
      
      **Query and retrieval patterns:**
      
      ```yaml
      audit_queries:
        # Common audit queries
        by_user:
          query: "SELECT * FROM audit_logs WHERE principal.arn = ?"
          use_case: "Investigate user activity"
          
        by_time_range:
          query: "SELECT * FROM audit_logs WHERE timestamp BETWEEN ? AND ?"
          use_case: "Incident investigation"
          
        by_decision_outcome:
          query: "SELECT * FROM audit_logs WHERE output.content LIKE '%denied%'"
          use_case: "Review negative decisions"
          
        guardrail_triggers:
          query: "SELECT * FROM audit_logs WHERE guardrail_result.action != 'NONE'"
          use_case: "Safety review"
          
        tools:
          - "Amazon Athena (S3 queries)"
          - "CloudWatch Logs Insights"
          - "OpenSearch (full-text search)"
      ```
      
      **High-risk AI (EU AI Act) additional requirements:**
      
      ```yaml
      high_risk_ai_audit:
        required_documentation:
          - "Risk management system documentation"
          - "Data governance records"
          - "Technical documentation"
          - "Conformity assessment"
          - "Human oversight procedures"
          
        logging_requirements:
          - "All decisions affecting individuals"
          - "Modifications to the system"
          - "Performance monitoring data"
          
        retention: "10 years minimum"
        
        access_for_authorities:
          - "Must be provided on request"
          - "Readable format"
          - "Complete traceability"
      ```
      
      **PALETTE integration:**
      - Define audit requirements in RIU-530 (AI Governance Config)
      - Configure logging in RIU-531 (Guardrail Selection)
      - Document in RIU-140 (Training Materials) for compliance team
      - Track in RIU-534 (Audit Trail Config)
      
      Key insight: Design audit trails for reconstruction, not just recording. An auditor should be able to take any AI decision and reconstruct exactly why it happened — model version, configuration, inputs, and any human oversight. If you can't reproduce it, you can't defend it.

## Evidence

- **Tier 1 (entry-level)**: [Regulatory Compliance and Governance - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_5_security_privacy/3_5_3_compliance_data_protection/3_5_3-2_regulatory_governance/regulatory_governance.html)
- **Tier 1 (entry-level)**: [Risk and Compliance Management for Generative AI](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/5_2_governance_and_organization/5_2_3_risk_and_compliance_mngmt.html)
- **Tier 1 (entry-level)**: [Align and monitor your Amazon Bedrock chatbot with AWS Audit Manager](https://aws.amazon.com/blogs/machine-learning/align-and-monitor-your-amazon-bedrock-powered-insurance-assistance-chatbot-to-responsible-ai-principles-with-aws-audit-manager/)
- **Tier 1 (entry-level)**: [Safeguard generative AI applications with Amazon Bedrock Guardrails](https://aws.amazon.com/blogs/machine-learning/safeguard-generative-ai-applications-with-amazon-bedrock-guardrails/)
- **Tier 1 (entry-level)**: [NIST AI Risk Management Framework (AI RMF 1.0)](https://www.nist.gov/itl/ai-risk-management-framework)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-140](../rius/RIU-140.md)
- [RIU-530](../rius/RIU-530.md)
- [RIU-531](../rius/RIU-531.md)
- [RIU-534](../rius/RIU-534.md)

## Handled By

- [Architect](../agents/architect.md)
- [Debugger](../agents/debugger.md)
- [Narrator](../agents/narrator.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-066.
Evidence tier: 1.
Journey stage: all.
