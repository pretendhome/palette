---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-036
source_hash: sha256:04db324f42bef8ad
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [data-quality, knowledge-entry, label-validation, semantic-validation, specialization, training-data]
related: [RIU-003, RIU-014, RIU-080, RIU-081, RIU-082, RIU-084]
handled_by: [architect, builder, validator]
journey_stage: specialization
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I validate that training data labels mean what stakeholders think they mean?

Label validation has two dimensions: syntactic (is the label correctly applied?) and semantic (does the label mean what we think it means?). Most tools focus on syntactic — you must explicitly validate semantic alignment with stakeholders.

## Definition

Label validation has two dimensions: syntactic (is the label correctly applied?) and semantic (does the label mean what we think it means?). Most tools focus on syntactic — you must explicitly validate semantic alignment with stakeholders.
      
      **Semantic validation process:**
      
      **Step 1: Label definition workshop (before labeling starts)**
      - Gather stakeholders (business, SMEs, data scientists, labelers)
      - For each label/category, document:
        - **Definition**: What does this label mean in business terms?
        - **Inclusion criteria**: What must be true for this label?
        - **Exclusion criteria**: What disqualifies this label?
        - **Boundary examples**: Edge cases that are barely in/out
        - **Common confusions**: Labels this might be mistaken for
      ```yaml
      label: "high_risk_order"
      definition: "Order with elevated fraud probability requiring manual review"
      inclusion:
        - "Order value > $5000 AND new customer"
        - "Shipping address differs from billing by > 500 miles"
      exclusion:
        - "Existing customer with 3+ successful orders"
      boundary_examples:
        - "Repeat customer, high value, different address" → NOT high_risk
        - "New customer, $4900, same address" → NOT high_risk (borderline)
      confused_with: "flagged_order" (different - that's fraud detected, not suspected)
      ```
      
      **Step 2: Pilot labeling with SME calibration**
      - Label 50-100 samples with both SMEs and labelers
      - Compare labels: Where do they disagree?
      - Disagreements reveal semantic ambiguity in definitions
      - Refine guidelines based on confusion patterns
      
      **Step 3: Inter-annotator agreement measurement**
      - Use modified Dawid-Skene (MDS) model for consolidation (20% fewer errors than majority voting)
      - Metrics to track:
        - **Cohen's Kappa**: Agreement accounting for chance (target: >0.8)
        - **Krippendorff's Alpha**: Multi-annotator agreement (target: >0.8)
        - **Confusion matrix by labeler**: Which labels are confused most?
      - Low agreement = definition problem, not labeler problem
      
      **Step 4: Stakeholder validation checkpoint**
      - Present labeled samples to business stakeholders
      - Ask: "Is this what you meant by [label]?"
      - Show edge cases and boundary decisions
      - Get explicit sign-off before full labeling proceeds
      - Document as ONE-WAY DOOR decision (RIU-003)
      
      **Step 5: Continuous validation during labeling**
      - Sample 5-10% for quality audit
      - Use SageMaker Ground Truth Review UI for inspection
      - Track consensus checks: same samples to multiple labelers
      - Implement feedback loops: labelers can flag ambiguous cases
      
      **AWS tools for label validation:**
      - **SageMaker Ground Truth**: Verification and adjustment workflows
      - **Ground Truth Plus**: Review UI with filtering and feedback
      - **Label chaining**: Verify labels from previous jobs
      - **Consolidation algorithms**: MDS for intelligent aggregation
      
      **Red flags that labels don't mean what stakeholders think:**
      - Low inter-annotator agreement (<0.7 kappa)
      - High SME override rate on reviewed samples
      - Model predictions stakeholders call "wrong" despite correct labels
      - Different departments using same label differently
      - Labelers frequently asking clarifying questions
      
      **For GenAI/LLM evaluation:**
      - Same principles apply to preference labels (chosen/rejected)
      - Document what "better response" means explicitly
      - Calibrate evaluators on edge cases before full evaluation
      - Use LLM-as-a-judge to check alignment with human preferences
      
      **PALETTE integration:**
      - Document label definitions in RIU-082 (Label/Category Alignment Check)
      - Track agreement metrics in RIU-084 (Data Quality Checks)
      - Store boundary examples in RIU-014 (Edge-Case Catalog)
      - Get stakeholder sign-off in decisions.md as ONE-WAY DOOR
      
      Key insight: If two experts disagree on a label, the definition is ambiguous — fix the definition before blaming the labelers. Semantic validation happens in workshops and reviews, not in code.

## Evidence

- **Tier 1 (entry-level)**: [Use the wisdom of crowds with Amazon SageMaker Ground Truth to annotate data more accurately](https://aws.amazon.com/blogs/machine-learning/use-the-wisdom-of-crowds-with-amazon-sagemaker-ground-truth-to-annotate-data-more-accurately/)
- **Tier 1 (entry-level)**: [Verifying and adjusting your data labels with Amazon SageMaker Ground Truth](https://aws.amazon.com/blogs/machine-learning/verifying-and-adjusting-your-data-labels-to-create-higher-quality-training-datasets-with-amazon-sagemaker-ground-truth/)
- **Tier 1 (entry-level)**: [Inspect your data labels with Amazon SageMaker Ground Truth Plus](https://aws.amazon.com/blogs/machine-learning/inspect-your-data-labels-with-a-visual-no-code-tool-to-create-high-quality-training-datasets-with-amazon-sagemaker-ground-truth-plus/)
- **Tier 1 (entry-level)**: [Data Management - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/3_0_architecture_and_design_patterns/3_9_AIOps/aiops_datamanagement.html)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-003](../rius/RIU-003.md)
- [RIU-014](../rius/RIU-014.md)
- [RIU-080](../rius/RIU-080.md)
- [RIU-081](../rius/RIU-081.md)
- [RIU-082](../rius/RIU-082.md)
- [RIU-084](../rius/RIU-084.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-082](../paths/RIU-082-llm-safety-guardrails.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-036.
Evidence tier: 1.
Journey stage: specialization.
