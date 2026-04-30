---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-061
source_hash: sha256:1e6a2a34d17512e1
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, architecture, compliance, knowledge-entry, localization, multi-region]
related: [RIU-060, RIU-120, RIU-530, RIU-531]
handled_by: [architect, builder, debugger, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I design AI systems that work across regions with different regulations?

Multi-region AI compliance requires architecture that respects data boundaries while enabling global operations. Design for the strictest regulation, then relax where permitted.

## Definition

Multi-region AI compliance requires architecture that respects data boundaries while enabling global operations. Design for the strictest regulation, then relax where permitted.
      
      **Key regulatory landscape:**
      
      | Region | Key Regulation | Key Requirements |
      |--------|----------------|------------------|
      | **EU** | EU AI Act (Aug 2024), GDPR | Risk classification, data residency, transparency |
      | **US** | State laws (CA, CO), sector rules | Varies by state and sector |
      | **UK** | UK GDPR, AI framework | Similar to EU but diverging |
      | **APAC** | Country-specific (PDPA, etc.) | Data localization requirements vary |
      | **Global** | ISO IEC 42001 | AI management system standard |
      
      **Architecture decision framework:**
      
      ```
      For each region, determine:
      
      1. CAN data leave this region?
         ├── YES → Can use cross-region inference
         └── NO → Need local processing
         
      2. WHAT data is restricted?
         ├── All data → Fully local architecture
         ├── PII only → Anonymize before cross-region
         └── Specific categories → Selective routing
         
      3. WHAT AI risk level applies?
         ├── High-risk (EU AI Act) → Additional requirements
         └── Limited/minimal risk → Standard controls
      ```
      
      **Architecture patterns by compliance requirement:**
      
      **Pattern 1: Cross-Region Inference (CRIS)**
      ```
      Best for: Performance optimization with compliance
      
      ┌─────────────────────────────────────────────────────────┐
      │                    GLOBAL USERS                         │
      └─────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   CRIS Profile    │
                    │  (Geographic/EU)  │
                    └─────────┬─────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
      ┌─────────┐       ┌─────────┐       ┌─────────┐
      │ EU-West │       │EU-Central│       │  EU-N   │
      │ Region  │       │  Region  │       │ Region  │
      └─────────┘       └─────────┘       └─────────┘
      
      Data stays within EU, inference distributed for availability
      ```
      
      ```yaml
      cris_configuration:
        profile_type: "geographic"  # or "global"
        
        geographic_eu:
          regions: ["eu-west-1", "eu-central-1", "eu-north-1"]
          use_case: "EU data residency required"
          data_flow: "Data stays in EU regions only"
          
        global:
          regions: ["all available"]
          use_case: "No data residency restrictions"
          data_flow: "Routed to optimal region"
          
        security:
          - "Data encrypted in transit"
          - "Temporary processing only"
          - "No persistent storage in destination"
      ```
      
      **Pattern 2: Fully Local RAG (Outposts)**
      ```
      Best for: Strictest data residency requirements
      
      ┌─────────────────────────────────────────────────────────┐
      │                  CUSTOMER DATACENTER                     │
      │  ┌─────────────────────────────────────────────────┐    │
      │  │              AWS OUTPOSTS                        │    │
      │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │    │
      │  │  │ Bedrock  │  │ Knowledge│  │  Vector  │      │    │
      │  │  │  Agent   │  │   Base   │  │   DB     │      │    │
      │  │  └──────────┘  └──────────┘  └──────────┘      │    │
      │  │                                                  │    │
      │  │  All AI processing on-premises                   │    │
      │  └─────────────────────────────────────────────────┘    │
      └─────────────────────────────────────────────────────────┘
      
      Data never leaves customer premises
      ```
      
      **Pattern 3: Hybrid RAG (Regional + Edge)**
      ```
      Best for: Balance of capability and compliance
      
      ┌─────────────────────────────────────────────────────────┐
      │                    AWS CLOUD (EU)                        │
      │  ┌──────────┐  ┌──────────┐                            │
      │  │ Bedrock  │  │ Non-PII  │  ← General knowledge       │
      │  │ Agents   │  │   KB     │                            │
      │  └────┬─────┘  └──────────┘                            │
      └───────┼─────────────────────────────────────────────────┘
              │
              │ Orchestration (no PII)
              │
      ┌───────┼─────────────────────────────────────────────────┐
      │       ▼           CUSTOMER EDGE                         │
      │  ┌──────────┐  ┌──────────┐                            │
      │  │ Local    │  │  PII     │  ← Sensitive data local    │
      │  │ LLM      │  │   KB     │                            │
      │  └──────────┘  └──────────┘                            │
      └─────────────────────────────────────────────────────────┘
      
      PII stays local, non-sensitive leverages cloud
      ```
      
      **Per-region configuration:**
      
      ```yaml
      regional_configuration:
        eu:
          data_residency: "strict"
          inference_profile: "geographic-eu"
          knowledge_base_location: "eu-west-1"
          logging_region: "eu-west-1"
          pii_handling: "process locally, anonymize before cross-region"
          ai_act_risk_level: "determine per use case"
          required_controls:
            - "Human oversight for high-risk"
            - "Transparency documentation"
            - "Bias monitoring"
            
        us:
          data_residency: "sector-dependent"
          inference_profile: "geographic-us" # or global
          knowledge_base_location: "us-east-1"
          logging_region: "us-east-1"
          pii_handling: "varies by state (CCPA, etc.)"
          
        apac_singapore:
          data_residency: "strict (PDPA)"
          inference_profile: "geographic-apac"
          knowledge_base_location: "ap-southeast-1"
          required_controls:
            - "Data transfer agreements"
            - "Local representative"
      ```
      
      **Data flow controls:**
      
      ```yaml
      data_flow_controls:
        # IAM policies
        iam_policies:
          - name: "RestrictCRISToEU"
            effect: "Deny"
            action: "bedrock:InvokeModel"
            condition:
              StringNotEquals:
                "bedrock:InferenceProfileArn": "arn:aws:bedrock:*:*:inference-profile/eu.*"
                
        # Service Control Policies (SCPs)
        scps:
          - name: "EnforceEUDataResidency"
            target: "EU Organization Units"
            policy:
              - deny_regions_outside: ["eu-west-1", "eu-central-1", "eu-north-1"]
              - deny_global_inference: true
              
        # Network controls
        network:
          - vpc_endpoints: "Use PrivateLink, no internet"
          - nacls: "Restrict outbound to approved regions"
      ```
      
      **EU AI Act compliance checklist:**
      
      ```yaml
      eu_ai_act_compliance:
        risk_classification:
          - task: "Classify AI system risk level"
            categories: ["Unacceptable", "High-risk", "Limited", "Minimal"]
            action: "Document classification rationale"
            
        high_risk_requirements:
          - "Risk management system"
          - "Data governance"
          - "Technical documentation"
          - "Record-keeping"
          - "Transparency"
          - "Human oversight"
          - "Accuracy, robustness, cybersecurity"
          
        transparency_requirements:
          - "Inform users they're interacting with AI"
          - "Label AI-generated content"
          - "Provide AI Service Cards"
          
        aws_support:
          - "ISO IEC 42001 certification"
          - "AI Service Cards"
          - "Frontier model safety framework"
          - "EU AI Pact signatory"
      ```
      
      **Compliance monitoring:**
      
      ```yaml
      compliance_monitoring:
        automated_checks:
          - "Data flow logging (CloudTrail)"
          - "Region compliance (AWS Config rules)"
          - "Model usage tracking (inference profiles)"
          - "Guardrail effectiveness"
          
        regular_audits:
          - "Quarterly compliance review"
          - "Annual third-party audit"
          - "Regulatory update tracking"
          
        alerts:
          - "Data flow outside approved regions"
          - "Unapproved model access"
          - "Guardrail bypass attempts"
      ```
      
      **PALETTE integration:**
      - Document regional requirements in RIU-530 (AI Governance Config)
      - Configure guardrails per region in RIU-531 (Guardrail Selection)
      - Track compliance in RIU-120 (Integration Mode Selection)
      - Include in Deployment Readiness (RIU-060) for each region
      
      Key insight: Design for the strictest regulation first (usually EU), then relax controls where other regions permit. It's easier to loosen restrictions than to retrofit compliance into a permissive architecture.

## Evidence

- **Tier 1 (entry-level)**: [Building trust in AI: The AWS approach to the EU AI Act](https://aws.amazon.com/blogs/machine-learning/building-trust-in-ai-the-aws-approach-to-the-eu-ai-act/)
- **Tier 1 (entry-level)**: [Unlocking AI flexibility in Switzerland: Cross-region inference for EU data processing](https://aws.amazon.com/blogs/alps/unlocking-ai-flexibility-in-switzerland-a-guide-to-cross-region-inference-for-eu-data-processing-and-model-access/)
- **Tier 1 (entry-level)**: [Securing Amazon Bedrock cross-Region inference: Geographic and global](https://aws.amazon.com/blogs/machine-learning/securing-amazon-bedrock-cross-region-inference-geographic-and-global/)
- **Tier 1 (entry-level)**: [Implement RAG while meeting data residency requirements using AWS hybrid and edge services](https://aws.amazon.com/blogs/machine-learning/implement-rag-while-meeting-data-residency-requirements-using-aws-hybrid-and-edge-services/)
- **Tier 1 (entry-level)**: [Regulatory Compliance and Governance - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_5_security_privacy/3_5_3_compliance_data_protection/3_5_3-2_regulatory_governance/regulatory_governance.html)
- **Tier 1 (entry-level)**: [EU AI Act — Official Text, Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng)
- **Tier 1 (entry-level)**: [EU Digital Strategy: Regulatory Framework for AI](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-060](../rius/RIU-060.md)
- [RIU-120](../rius/RIU-120.md)
- [RIU-530](../rius/RIU-530.md)
- [RIU-531](../rius/RIU-531.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-060](../paths/RIU-060-deployment-readiness-envelope.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-061.
Evidence tier: 1.
Journey stage: all.
