---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-002
source_hash: sha256:f151237175545c70
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, architecture, decision-framework, knowledge-entry, reversibility, risk-management]
related: [RIU-001, RIU-003]
handled_by: [architect, researcher]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What's the difference between a ONE-WAY DOOR and TWO-WAY DOOR decision in AI system architecture?

ONE-WAY DOOR decisions are difficult or impossible to reverse and require human approval before execution — flag these as "🚨 ONE-WAY DOOR — confirmation required" and log in decisions.md via RIU-003 (Decision Log + One-Way Door Registry). Examples in AI/ML: ethical AI guidelines, data governance frameworks, model architecture selection, production deployment commitments, and database schema for ML features. TWO-WAY DOOR decisions are easily reversible and support Amazon's "Bias for Action" — agents may proceed autonomously with monitoring. Examples: hyperparameter tuning, prompt iterations, A/B test configurations. Key insight: don't treat AI/ML projects as deterministic software; acknowledge uncertainty and establish governance templates before implementation. For ONE-WAY DOORs, estimate value of right decisions against cost of wrong ones, secure executive sponsorship, and use MLOps assessment to ensure architectural decisions support long-term ROI.

## Definition

ONE-WAY DOOR decisions are difficult or impossible to reverse and require human approval before execution — flag these as "🚨 ONE-WAY DOOR — confirmation required" and log in decisions.md via RIU-003 (Decision Log + One-Way Door Registry). Examples in AI/ML: ethical AI guidelines, data governance frameworks, model architecture selection, production deployment commitments, and database schema for ML features. TWO-WAY DOOR decisions are easily reversible and support Amazon's "Bias for Action" — agents may proceed autonomously with monitoring. Examples: hyperparameter tuning, prompt iterations, A/B test configurations. Key insight: don't treat AI/ML projects as deterministic software; acknowledge uncertainty and establish governance templates before implementation. For ONE-WAY DOORs, estimate value of right decisions against cost of wrong ones, secure executive sponsorship, and use MLOps assessment to ensure architectural decisions support long-term ROI.

## Evidence

- **Tier 1 (entry-level)**: [Mental Models for Your Digital Transformation](https://aws.amazon.com/blogs/enterprise-strategy/mental-models-for-your-digital-transformation/)
- **Tier 1 (entry-level)**: [AI/ML Organizational Adoption Framework](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/index.html)
- **Tier 1 (entry-level)**: [AWS Cloud Adoption Framework for Artificial Intelligence, Machine Learning, and Generative AI](https://docs.aws.amazon.com/whitepapers/latest/aws-caf-for-ai/aws-caf-for-ai.html)
- **Tier 1 (entry-level)**: [Machine Learning Lens - AWS Well-Architected](https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/machine-learning-lens.html)
- **Tier 1 (entry-level)**: [Unlocking the Business Value of Machine Learning—With Organizational Learning](https://aws.amazon.com/blogs/enterprise-strategy/unlocking-the-business-value-of-machine-learning-with-organizational-learning/)
- **Tier 1 (entry-level)**: [Eviden's Comprehensive Approach to MLOps Assessment](https://aws.amazon.com/blogs/apn/develop-and-deploy-machine-learning-models-with-eviden-comprehensive-approach-to-mlops-assessment/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-003](../rius/RIU-003.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-002.
Evidence tier: 1.
Journey stage: all.
