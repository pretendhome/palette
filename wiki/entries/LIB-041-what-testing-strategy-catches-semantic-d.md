---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-041
source_hash: sha256:1d8ee5cd5f77ba19
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [knowledge-entry, pre-production, quality-assurance, retrieval, semantic-validation, testing]
related: [RIU-021, RIU-081, RIU-082, RIU-084, RIU-540]
handled_by: [architect, builder, validator]
journey_stage: retrieval
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What testing strategy catches semantic data bugs before production?

Semantic bugs are data that passes schema validation but is meaningfully wrong (swapped columns, wrong units, misinterpreted categories). Catch them with "unit tests for data" that verify business meaning, not just structure.

## Definition

Semantic bugs are data that passes schema validation but is meaningfully wrong (swapped columns, wrong units, misinterpreted categories). Catch them with "unit tests for data" that verify business meaning, not just structure.
      
      **Types of semantic data bugs:**
      | Bug Type | Example | Schema Catches? | Semantic Test Catches? |
      |----------|---------|-----------------|------------------------|
      | Swapped columns | customer_id in order_id field | ❌ (both strings) | ✅ (format check) |
      | Wrong units | Pounds stored as kilograms | ❌ (both numbers) | ✅ (range check) |
      | Misinterpreted enum | "HIGH"=3 vs "HIGH"=1 | ❌ (valid enum) | ✅ (business rule) |
      | Stale reference | customer_id doesn't exist | ❌ (valid format) | ✅ (referential check) |
      | Aggregation error | Sum doesn't equal parts | ❌ (valid number) | ✅ (consistency check) |
      | Timezone confusion | UTC stored as local time | ❌ (valid timestamp) | ✅ (range/distribution) |
      
      **Testing pyramid for data quality:**
      ```
                    ┌─────────────────┐
                    │  Manual Review  │  ← Sample inspection
                    ├─────────────────┤
                    │ Cross-Dataset   │  ← Compare sources
                    │  Validation     │
                    ├─────────────────┤
                    │ Business Rule   │  ← Domain constraints
                    │    Tests        │
                    ├─────────────────┤
                    │ Statistical     │  ← Distribution checks
                    │    Tests        │
                    └─────────────────┘
                    │ Schema Tests    │  ← Type/format (base)
                    └─────────────────┘
      ```
      
      **Layer 1: Unit tests for data (Deequ / AWS Glue Data Quality)**
      ```python
      # Deequ example - semantic assertions
      from pydeequ.checks import Check
      
      check = Check(spark, CheckLevel.Error, "Semantic Validation") \
          # Format checks (catch swapped columns)
          .hasPattern("order_id", r"^ORD-\d{10}$") \
          .hasPattern("customer_id", r"^CUST-\d{8}$") \
          
          # Range checks (catch unit errors)
          .isNonNegative("amount") \
          .isLessThanOrEqualTo("amount", 1000000) \
          .isContainedIn("currency", ["USD", "EUR", "GBP"]) \
          
          # Business rule checks
          .isContainedIn("priority", ["high", "low"]) \
          .satisfies("discount <= amount", "discount can't exceed amount") \
          
          # Referential checks
          .isContainedIn("customer_id", valid_customer_ids) \
          
          # Consistency checks
          .satisfies("line_total == quantity * unit_price", "line math")
      ```
      
      **Layer 2: Statistical tests (catch distribution shifts)**
      ```yaml
      statistical_checks:
        - metric: "mean(amount)"
          expected_range: [100, 500]  # Based on historical baseline
          
        - metric: "null_rate(email)"
          max_threshold: 0.05  # No more than 5% nulls
          
        - metric: "distinct_count(category)"
          expected: 12  # Should always have exactly 12 categories
          
        - metric: "value_distribution(status)"
          expected:
            active: 0.70-0.80
            pending: 0.15-0.25
            closed: 0.05-0.10
      ```
      
      **Layer 3: Cross-dataset validation (catch integration bugs)**
      - Compare source and target after transformation
      - Verify row counts match (or explain difference)
      - Check that joins don't duplicate/lose records
      - Use Apache Griffin for large-scale dataset comparison
      ```python
      # Griffin-style comparison
      assert count(source) == count(target), "Row count mismatch"
      assert sum(source.amount) == sum(target.amount), "Amount sum mismatch"
      assert distinct(source.customer_id) == distinct(target.customer_id)
      ```
      
      **Layer 4: Example-based tests (golden set)**
      - Curate specific examples with known correct outputs
      - Include edge cases and boundary conditions
      - Run as regression tests on every pipeline change
      ```yaml
      golden_examples:
        - input: {order_id: "ORD-0000000001", amount: 0}
          expected: {risk_score: "low"}  # Zero-value order = low risk
          
        - input: {order_id: "ORD-9999999999", amount: 999999}
          expected: {risk_score: "high"}  # Max-value order = high risk
          
        - input: {customer_id: null}
          expected: {should_fail_validation: true}
      ```
      
      **CI/CD integration:**
      - Run data unit tests on every pipeline change
      - Block deployment if semantic tests fail
      - Sample production data into test environment weekly
      - Compare test results against known-good baseline
      
      **AWS implementation:**
      - **Deequ**: Unit tests for Spark-based pipelines
      - **AWS Glue Data Quality**: DQDL rules in Glue jobs
      - **Apache Griffin on EMR**: Large-scale dataset comparison
      - **CloudWatch**: Alert on test failures
      
      **PALETTE integration:**
      - Define semantic tests in RIU-082 (Label/Category Alignment Check)
      - Store golden examples in RIU-021 (Golden Set)
      - Run as part of RIU-081 (E2E Smoke Tests)
      - Document business rules in RIU-044 (Business Rules Documentation)
      
      Key insight: Schema tests are necessary but not sufficient. The most dangerous bugs are semantically wrong data that looks structurally correct. Test what the data *means*, not just what it *looks like*.

## Evidence

- **Tier 1 (entry-level)**: [Deequ - Unit tests for data](https://github.com/awslabs/deequ)
- **Tier 1 (entry-level)**: [AWS Glue Data Quality Workshop](https://catalog.us-east-1.prod.workshops.aws/workshops/bd8bdbc7-11cb-4d16-9e76-1404e6d37e53)
- **Tier 1 (entry-level)**: [Automate large-scale data validation using Amazon EMR and Apache Griffin](https://aws.amazon.com/blogs/big-data/automate-large-scale-data-validation-using-amazon-emr-and-apache-griffin/)
- **Tier 1 (entry-level)**: [Great Expectations: Official Documentation](https://docs.greatexpectations.io/docs/home/)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-021](../rius/RIU-021.md)
- [RIU-081](../rius/RIU-081.md)
- [RIU-082](../rius/RIU-082.md)
- [RIU-084](../rius/RIU-084.md)
- [RIU-540](../rius/RIU-540.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-021](../paths/RIU-021-tiny-ai-eval-harness.md) — hands-on exercise
- [RIU-082](../paths/RIU-082-llm-safety-guardrails.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-041.
Evidence tier: 1.
Journey stage: retrieval.
