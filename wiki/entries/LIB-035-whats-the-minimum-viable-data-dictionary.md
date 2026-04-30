---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-035
source_hash: sha256:bf7ad2bcf432b3aa
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, data-dictionary, data-governance, documentation, knowledge-entry, semantics]
related: [RIU-004, RIU-011, RIU-012, RIU-080, RIU-081, RIU-084]
handled_by: [architect, builder, researcher, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What's the minimum viable data dictionary for an AI deployment?

A minimum viable data dictionary documents what data exists, what it means, and how it can be used. For AI, also include quality metrics and lineage.

## Definition

A minimum viable data dictionary documents what data exists, what it means, and how it can be used. For AI, also include quality metrics and lineage.
      
      **Minimum data dictionary structure:**
      
      ```yaml
      data_dictionary:
        dataset_name: "customer_orders"
        version: "1.2.0"
        owner: "data-platform-team"
        last_updated: "2024-06-15"
        
        # Dataset-level metadata
        description: "Customer order records used for AI risk scoring"
        source_system: "legacy-orders-db"
        refresh_frequency: "hourly"
        retention_period: "7 years"
        classification: "confidential"  # public | internal | confidential | restricted
        
        # Field definitions (minimum viable = every field used by AI)
        fields:
          - name: "order_id"
            type: "string"
            description: "Unique order identifier"
            format: "ORD-[0-9]{10}"
            nullable: false
            pii: false
            example: "ORD-1234567890"
            
          - name: "customer_id"
            type: "string"
            description: "Customer account identifier"
            nullable: false
            pii: true  # Quasi-identifier
            pii_handling: "hash before AI processing"
            
          - name: "order_total"
            type: "decimal"
            description: "Total order value in USD"
            unit: "USD"
            range: [0, 1000000]
            nullable: false
            
          - name: "order_date"
            type: "timestamp"
            description: "When order was placed"
            timezone: "UTC"
            format: "ISO 8601"
            
        # Data quality baseline
        quality_metrics:
          completeness: 99.5%  # % non-null for required fields
          freshness: "< 1 hour from source"
          volume_baseline: "50,000-100,000 records/day"
          
        # Lineage
        lineage:
          upstream: ["legacy-orders-db.orders", "crm.customers"]
          downstream: ["ai-risk-model", "reporting-dashboard"]
          transformations: ["PII hashing", "currency normalization"]
      ```
      
      **Required fields for each data element:**
      | Field | Required | Why |
      |-------|----------|-----|
      | name | ✅ | Identification |
      | type | ✅ | Schema validation |
      | description | ✅ | Business meaning |
      | nullable | ✅ | Quality checks |
      | pii | ✅ | Compliance |
      | example | Recommended | Understanding |
      | range/enum | Recommended | Validation |
      
      **AI-specific additions (beyond traditional data dictionary):**
      - **pii_handling**: How PII is protected before AI processing
      - **embedding_model**: If field is embedded, which model
      - **drift_sensitivity**: How sensitive AI is to changes in this field
      - **feature_importance**: Relative importance to model (if known)
      - **quality_thresholds**: Alert if quality drops below threshold
      
      **For GenAI/RAG systems, also document:**
      - **chunk_strategy**: How documents are chunked
      - **embedding_dimensions**: Vector size
      - **metadata_extracted**: What metadata accompanies embeddings
      - **update_frequency**: How often knowledge base refreshes
      
      **Storage and governance:**
      - Store in AWS Glue Data Catalog for discoverability
      - Use Glue Schema Registry for schema validation
      - Version control dictionary alongside code (Git)
      - Link to data contracts (RIU-011)
      
      **"Minimum viable" criteria:**
      - [ ] Every field consumed by AI model is documented
      - [ ] PII fields identified with handling instructions
      - [ ] Data types and formats specified
      - [ ] Source system and refresh frequency documented
      - [ ] Quality baseline established (completeness, freshness)
      - [ ] Owner and contact identified
      
      **PALETTE integration:**
      - Document in RIU-011 (Data Contract Freeze)
      - Validate with RIU-084 (Data Quality Checks)
      - Track lineage for RIU-012 (PII/Sensitive Data Map)
      - Reference in RIU-004 (Workstream Decomposition)
      
      Key insight: "Minimum viable" means every field the AI touches has a definition. Unknown fields are technical debt — you can't debug data issues if you don't know what the data means.

## Evidence

- **Tier 1 (entry-level)**: [Implementing data governance on AWS: Automation, tagging, and lifecycle strategy](https://aws.amazon.com/blogs/security/implementing-data-governance-on-aws-automation-tagging-and-lifecycle-strategy-part-1/)
- **Tier 1 (entry-level)**: [Data governance in the age of generative AI](https://aws.amazon.com/blogs/big-data/data-governance-in-the-age-of-generative-ai/)
- **Tier 1 (entry-level)**: [Validate, evolve, and control schemas with AWS Glue Schema Registry](https://aws.amazon.com/blogs/big-data/validate-evolve-and-control-schemas-in-amazon-msk-and-amazon-kinesis-data-streams-with-aws-glue-schema-registry/)
- **Tier 1 (entry-level)**: [AI/ML Organizational Adoption Framework](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/index.html)
- **Tier 1 (entry-level)**: [Databricks: Best practices for data and AI governance](https://docs.databricks.com/gcp/en/lakehouse-architecture/data-governance/best-practices)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-004](../rius/RIU-004.md)
- [RIU-011](../rius/RIU-011.md)
- [RIU-012](../rius/RIU-012.md)
- [RIU-080](../rius/RIU-080.md)
- [RIU-081](../rius/RIU-081.md)
- [RIU-084](../rius/RIU-084.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-035.
Evidence tier: 1.
Journey stage: all.
