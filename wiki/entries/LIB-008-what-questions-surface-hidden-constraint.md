---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-008
source_hash: sha256:19d2db2822ae4352
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, blockers, compliance, constraint-discovery, knowledge-entry, risk-assessment]
related: [RIU-001, RIU-003, RIU-007, RIU-012, RIU-530]
handled_by: [architect, researcher, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What questions surface hidden constraints that will block AI deployment later?

Ask these questions during discovery and document answers in your Constraint Profile (RIU-007):

## Definition

Ask these questions during discovery and document answers in your Constraint Profile (RIU-007):
      
      **Regulatory & Compliance:**
      - Which regulations apply? (EU AI Act, GDPR, HIPAA, CCPA, SOX, FedRAMP)
      - Is a Business Associate Addendum (BAA) required? (Healthcare)
      - What model explainability requirements exist? (EU AI Act high-risk systems)
      - What audit trail and traceability requirements apply?
      
      **Data & Privacy:**
      - Where must data reside? (Sovereignty, cross-border transfer restrictions)
      - What PII/PHI handling is required? (Encryption at rest/in transit, anonymization)
      - Who owns the training data? Any licensing restrictions?
      - Can data leave the customer's environment for model training/inference?
      
      **Infrastructure & Security:**
      - What network latency is acceptable? (Critical for real-time AI)
      - What authentication/IAM controls are required?
      - Is the model supply chain auditable? (Backdoor/vulnerability risks)
      - Is Infrastructure as Code (IaC) required for deployment?
      
      **Organizational & Procurement:**
      - How long is legal/security review? (Often 4-12 weeks in enterprise)
      - Are there existing vendor contracts that constrain tool selection?
      - Do unions or workforce agreements affect automation deployment?
      - Is there executive sponsorship aligned with legal/compliance/business units?
      - What team knowledge gaps require training before deployment?
      
      Flag any answer that implies a ONE-WAY DOOR decision (RIU-003). Use RIU-530 (AI Risk Classification) for regulated industries.

## Evidence

- **Tier 1 (entry-level)**: [Regulatory Compliance and Governance - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_5_security_privacy/3_5_3_compliance_data_protection/3_5_3-2_regulatory_governance/regulatory_governance.html)
- **Tier 1 (entry-level)**: [HIPAA compliance for generative AI solutions on AWS](https://aws.amazon.com/blogs/industries/hipaa-compliance-for-generative-ai-solutions-on-aws/)
- **Tier 1 (entry-level)**: [Risk and Compliance Management for Generative AI](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/5_2_governance_and_organization/5_2_3_risk_and_compliance_mngmt.html)
- **Tier 1 (entry-level)**: [Navigating the responsible use of AI in government procurement](https://aws.amazon.com/blogs/publicsector/navigating-the-responsible-use-of-ai-in-government-procurement/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-003](../rius/RIU-003.md)
- [RIU-007](../rius/RIU-007.md)
- [RIU-012](../rius/RIU-012.md)
- [RIU-530](../rius/RIU-530.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-008.
Evidence tier: 1.
Journey stage: all.
