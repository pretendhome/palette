---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-030
source_hash: sha256:b078d297bdbad4d4
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [compatibility, data-transformation, foundation, integration, knowledge-entry, schema-mapping]
related: [RIU-011, RIU-060, RIU-061, RIU-080, RIU-084]
handled_by: [architect, builder, monitor, validator]
journey_stage: foundation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I handle schema mismatches between AI output and legacy system input?

Schema mismatches are inevitable when connecting AI (flexible, evolving) to legacy (rigid, stable). Use a transformation layer with validation at boundaries.

## Definition

Schema mismatches are inevitable when connecting AI (flexible, evolving) to legacy (rigid, stable). Use a transformation layer with validation at boundaries.
      
      **Architecture pattern: Transformation Layer**
      ```
      AI Service → [Transformation Layer] → Legacy System
                         ↓
                   - Schema mapping
                   - Field conversion
                   - Validation
                   - Default values
                   - Error handling
      ```
      
      **Mismatch types and solutions:**
      
      | Mismatch Type | Example | Solution |
      |---------------|---------|----------|
      | Field naming | `aiRiskScore` vs `RISK_SCORE` | Field mapping in transformation |
      | Data types | String "123" vs Integer 123 | Type coercion with validation |
      | Missing fields | AI omits optional field | Default values or null handling |
      | Extra fields | AI adds fields legacy ignores | Filter to expected schema |
      | Format differences | JSON vs XML | API Gateway + Lambda transformation |
      | Nested vs flat | `{address: {city}}` vs `address_city` | Flatten/unflatten logic |
      | Enum mismatches | "HIGH" vs "3" | Lookup table conversion |
      
      **Control AI output schema (prevent mismatches at source):**
      - **Amazon Nova constrained decoding**: Define output schema in tool configuration, use Converse API
      - **Prompt templates as contracts**: Enforce output format in system prompt
      - **JSON mode**: Request structured JSON output matching legacy schema
      ```python
      # Nova constrained output example
      tool_config = {
          "output_schema": {
              "type": "object",
              "properties": {
                  "RISK_SCORE": {"type": "integer", "minimum": 0, "maximum": 100},
                  "CATEGORY_CODE": {"type": "string", "enum": ["A", "B", "C"]}
              },
              "required": ["RISK_SCORE", "CATEGORY_CODE"]
          }
      }
      ```
      
      **Transformation implementation (AWS):**
      - **Simple transformations**: API Gateway mapping templates (no code)
      - **Complex transformations**: Lambda function between AI and legacy
      - **Streaming data**: Glue Schema Registry for validation + SerDe for conversion
      - **Batch data**: Glue ETL jobs with schema mapping
      
      **Validation at boundaries (AWS Glue Data Quality):**
      - Schema matching: Output conforms to expected structure
      - Referential integrity: Foreign keys exist in legacy system
      - Data type validation: Values within expected ranges
      - Completeness: Required fields present
      ```
      Rules: [
        SchemaMatch "ai_output" "legacy_input_schema",
        ColumnValues "RISK_SCORE" between 0 and 100,
        IsComplete "ORDER_ID",
        ReferentialIntegrity "CUSTOMER_ID" "legacy.customers.id"
      ]
      ```
      
      **Error handling for mismatches:**
      1. **Validation failure**: Log error with details, route to DLQ
      2. **Transformation failure**: Return clear error message, don't fail silently
      3. **Partial success**: Decide policy — reject entire record or accept partial?
      4. **Unknown fields**: Log warning, strip and continue (don't break on extras)
      
      **Testing schema compatibility (RIU-080):**
      - Contract tests validate transformation outputs
      - Test with edge cases: nulls, empty strings, boundary values
      - Test with malformed AI outputs (defensive)
      - Regression tests when either schema changes
      
      **PALETTE integration:**
      - Document schema mappings in RIU-011 (Data Contract Freeze)
      - Validate with RIU-084 (Data Quality Checks)
      - Test transformations with RIU-080 (Contract Tests)
      - Track schema changes as potential ONE-WAY DOORs
      
      Key insight: Don't trust AI output blindly — validate at the boundary before sending to legacy. Constrained decoding prevents most mismatches; transformation layer handles the rest.

## Evidence

- **Tier 1 (entry-level)**: [Structured outputs with Amazon Nova: A guide for builders](https://aws.amazon.com/blogs/machine-learning/structured-outputs-with-amazon-nova-a-guide-for-builders/)
- **Tier 1 (entry-level)**: [Validate, evolve, and control schemas with AWS Glue Schema Registry](https://aws.amazon.com/blogs/big-data/validate-evolve-and-control-schemas-in-amazon-msk-and-amazon-kinesis-data-streams-with-aws-glue-schema-registry/)
- **Tier 1 (entry-level)**: [Set up advanced rules to validate quality with AWS Glue Data Quality](https://aws.amazon.com/blogs/big-data/set-up-advanced-rules-to-validate-quality-of-multiple-datasets-with-aws-glue-data-quality/)
- **Tier 1 (entry-level)**: [Modernizing SOAP applications using Amazon API Gateway and AWS Lambda](https://aws.amazon.com/blogs/compute/modernizing-soap-applications-using-amazon-api-gateway-and-aws-lambda/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-011](../rius/RIU-011.md)
- [RIU-060](../rius/RIU-060.md)
- [RIU-061](../rius/RIU-061.md)
- [RIU-080](../rius/RIU-080.md)
- [RIU-084](../rius/RIU-084.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-060](../paths/RIU-060-deployment-readiness-envelope.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-030.
Evidence tier: 1.
Journey stage: foundation.
