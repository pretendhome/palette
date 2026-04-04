---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-026
source_hash: sha256:b2980137315519c6
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [compatibility, data-contracts, integration, knowledge-entry, retrieval, schema-design]
related: [RIU-003, RIU-011, RIU-060, RIU-061, RIU-070, RIU-080]
handled_by: [architect, builder, monitor, validator]
journey_stage: retrieval
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I design data contracts between AI services and legacy systems?

Data contracts define the agreement between systems on data format, semantics, and behavior. For AI↔legacy integration, design for compatibility, validation, and evolution.

## Definition

Data contracts define the agreement between systems on data format, semantics, and behavior. For AI↔legacy integration, design for compatibility, validation, and evolution.
      
      **Contract structure (RIU-011 Data Contract Freeze):**
      ```yaml
      contract_id: "order-ai-enrichment-v2"
      version: "2.1.0"
      producer: "legacy-order-system"
      consumer: "ai-enrichment-service"
      
      schema:
        type: object
        required: [order_id, customer_id, items]
        properties:
          order_id: {type: string, pattern: "^ORD-[0-9]{10}$"}
          customer_id: {type: string}
          items: {type: array, items: {$ref: "#/definitions/LineItem"}}
          # AI-added fields (optional for legacy compatibility)
          ai_risk_score: {type: number, minimum: 0, maximum: 1}
          ai_category: {type: string, enum: [standard, priority, review]}
      
      compatibility_mode: BACKWARD  # New consumer can read old data
      validation: strict
      sla:
        latency_p99: 500ms
        availability: 99.9%
      ```
      
      **Schema management with AWS Glue Schema Registry:**
      - Register schemas for all data exchanges
      - Enable compatibility checking (BACKWARD, FORWARD, FULL)
      - Auto-validate on serialization/deserialization
      - Version tracking with IAM-controlled access
      - Works with MSK, Kinesis, and custom applications
      
      **Compatibility strategies:**
      | Strategy | When to Use | Rule |
      |----------|-------------|------|
      | BACKWARD | AI adds fields to legacy data | New fields must be optional |
      | FORWARD | Legacy must accept AI output | Consumers ignore unknown fields |
      | FULL | Bidirectional compatibility | Both rules apply |
      | NONE | Breaking changes allowed | Coordinate deployment |
      
      **Handling AI-specific challenges:**
      - **Non-deterministic outputs**: Define acceptable ranges, not exact values
      - **Confidence scores**: Include as optional fields with documented semantics
      - **Nullable AI fields**: Legacy may not populate fields AI expects — handle gracefully
      - **Format mismatches**: Use transformation layer (Lambda, Step Functions) between systems
      
      **Validation and testing (RIU-080 Contract Tests):**
      - **Schema validation**: Validate all messages against registered schema
      - **Contract tests**: Producer tests verify output matches contract; consumer tests verify handling
      - **Sample payloads**: Include representative examples in contract definition
      - **Edge cases**: Document and test boundary conditions
      
      **Evolution process:**
      1. Propose schema change with compatibility analysis
      2. Register new version in Schema Registry
      3. Update consumer to handle new + old versions
      4. Update producer to emit new version
      5. Deprecate old version after migration period
      
      **PALETTE integration:**
      - Document contracts in RIU-011 (Data Contract Freeze)
      - Test with RIU-080 (Contract Tests)
      - Track schema changes in Decision Log (RIU-003) — often ONE-WAY DOORs
      - Define SLAs in RIU-070 (SLO/SLI Definition)
      
      Key insight: Legacy systems can't change quickly — design contracts with BACKWARD compatibility so AI services can evolve without breaking legacy consumers. The contract is the API between teams, not just systems.

## Evidence

- **Tier 1 (entry-level)**: [Evolve JSON Schemas in Amazon MSK and Amazon Kinesis Data Streams with the AWS Glue Schema Registry](https://aws.amazon.com/blogs/big-data/evolve-json-schemas-in-amazon-msk-and-amazon-kinesis-data-streams-with-the-aws-glue-schema-registry/)
- **Tier 1 (entry-level)**: [Modern data strategy for government tax and labor systems](https://aws.amazon.com/blogs/publicsector/modern-data-strategy-for-government-tax-and-labor-systems/)
- **Tier 1 (entry-level)**: [Organizational Design and Team Structure for AI](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/5_2_governance_and_organization/5_2_2_organizational_design_team_structure.html)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-003](../rius/RIU-003.md)
- [RIU-011](../rius/RIU-011.md)
- [RIU-060](../rius/RIU-060.md)
- [RIU-061](../rius/RIU-061.md)
- [RIU-070](../rius/RIU-070.md)
- [RIU-080](../rius/RIU-080.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-060](../paths/RIU-060-deployment-readiness-envelope.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-026.
Evidence tier: 1.
Journey stage: retrieval.
