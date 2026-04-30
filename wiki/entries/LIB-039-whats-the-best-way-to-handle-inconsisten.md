---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-039
source_hash: sha256:7f47e8608e7d4b0d
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, cross-functional, data-governance, knowledge-entry, semantic-harmonization, standards]
related: [RIU-003, RIU-011, RIU-080, RIU-081, RIU-082]
handled_by: [architect, builder, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What's the best way to handle inconsistent data definitions across departments?

Inconsistent definitions are a governance problem, not a technical problem. You can't automate your way out — you need shared vocabulary with enforcement.

## Definition

Inconsistent definitions are a governance problem, not a technical problem. You can't automate your way out — you need shared vocabulary with enforcement.
      
      **The problem:**
      - Sales says "customer" = anyone with an account
      - Finance says "customer" = anyone who has paid
      - Support says "customer" = anyone who has contacted us
      - AI model trained on "customer" data — which definition?
      
      **Solution: Canonical business glossary + enforcement**
      
      **Step 1: Establish governance structure**
      - **Data governance champion**: Single accountable owner
      - **Cross-functional governance committee**: Representatives from each department
      - **Domain owners**: Department-level authority for their data
      - Use Amazon DataZone domain units to organize by business unit
      
      **Step 2: Create canonical business glossary**
      ```yaml
      glossary_term:
        term: "customer"
        canonical_definition: "Entity with at least one completed paid transaction"
        owner: "Finance"
        approved_date: "2024-03-15"
        
        department_mappings:
          sales: 
            local_term: "account"
            relationship: "superset"  # All customers are accounts, not all accounts are customers
          support:
            local_term: "contact"
            relationship: "overlapping"  # Some contacts are customers, some aren't
            
        usage_guidance: "For AI training on 'customer' data, use this definition unless explicitly scoped otherwise"
        
        related_terms: ["prospect", "lead", "account", "user"]
      ```
      
      **Step 3: Map conflicting definitions**
      | Department | Their Term | Canonical Term | Relationship | Transformation |
      |------------|-----------|----------------|--------------|----------------|
      | Sales | account | customer | superset | Filter: has_paid = true |
      | Support | contact | customer | overlapping | Join with transactions |
      | Marketing | lead | prospect | equivalent | Direct mapping |
      
      **Step 4: Enforce through tooling**
      - **Amazon SageMaker Catalog**: Metadata enforcement rules require glossary terms before publishing
      - **Amazon DataZone**: Unified portal with business context and access governance
      - **AWS Glue Schema Registry**: Schema validation with canonical field names
      - **Collibra integration**: Bidirectional sync for enterprise-wide consistency
      
      **Step 5: Technical implementation**
      ```
      Source Data (dept definitions)
              ↓
      Transformation Layer (mapping rules)
              ↓
      Canonical Data Layer (glossary-aligned)
              ↓
      AI/Analytics Consumption
      ```
      
      **Resolution process for conflicts:**
      1. **Identify conflict**: Same term, different meanings
      2. **Document both definitions**: What does each department actually mean?
      3. **Determine canonical**: Which definition serves enterprise-wide use?
      4. **Create mappings**: How to transform from local to canonical
      5. **Get sign-off**: Cross-functional committee approval
      6. **Enforce**: Metadata rules require canonical terms for shared assets
      
      **Common pitfalls:**
      - Creating glossary but not enforcing it (becomes shelfware)
      - Forcing one department's definition on others (creates resistance)
      - Not documenting mappings (breaks downstream when source changes)
      - Treating this as IT problem (it's a business alignment problem)
      
      **For AI specifically:**
      - Document which definition was used for training data
      - Include glossary version in model metadata
      - Alert if source data definition changes (potential drift)
      - Validate that inference data uses same definition as training
      
      **PALETTE integration:**
      - Document canonical definitions in RIU-042 (Taxonomy Alignment)
      - Track definition changes as potential ONE-WAY DOORs (RIU-003)
      - Validate alignment with RIU-082 (Label/Category Alignment Check)
      - Include in data dictionary (RIU-011)
      
      Key insight: The goal isn't to force everyone to use the same definition — it's to know which definition applies in each context and transform accordingly. Map, don't mandate.

## Evidence

- **Tier 1 (entry-level)**: [Organize content across business units with Amazon DataZone domain units](https://aws.amazon.com/blogs/big-data/organize-content-across-business-units-with-enterprise-wide-data-governance-using-amazon-datazone-domain-units-and-authorization-policies/)
- **Tier 1 (entry-level)**: [Enforce business glossary classification rules in Amazon SageMaker Catalog](https://aws.amazon.com/blogs/big-data/enforce-business-glossary-classification-rules-in-amazon-sagemaker-catalog/)
- **Tier 1 (entry-level)**: [Amazon DataZone Now Generally Available](https://aws.amazon.com/blogs/aws/amazon-datazone-now-generally-available-collaborate-on-data-projects-across-organizational-boundaries/)
- **Tier 1 (entry-level)**: [Unifying metadata governance across Amazon SageMaker and Collibra](https://aws.amazon.com/blogs/big-data/unifying-metadata-governance-across-amazon-sagemaker-and-collibra/)
- **Tier 1 (entry-level)**: [Databricks: Best practices for data and AI governance](https://docs.databricks.com/gcp/en/lakehouse-architecture/data-governance/best-practices)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-003](../rius/RIU-003.md)
- [RIU-011](../rius/RIU-011.md)
- [RIU-080](../rius/RIU-080.md)
- [RIU-081](../rius/RIU-081.md)
- [RIU-082](../rius/RIU-082.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-082](../paths/RIU-082-llm-safety-guardrails.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-039.
Evidence tier: 1.
Journey stage: all.
