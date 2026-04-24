---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-032
source_hash: sha256:7b552c50701f849d
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, contracts, documentation, governance, knowledge-entry, testing]
related: [RIU-003, RIU-004, RIU-015, RIU-016, RIU-060, RIU-061, RIU-080, RIU-084]
handled_by: [architect, builder, monitor, researcher, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I document integration contracts so they're enforceable and testable?

Enforceable contracts are machine-readable, version-controlled, and automatically tested. Document the contract, not just the API.

## Definition

Enforceable contracts are machine-readable, version-controlled, and automatically tested. Document the contract, not just the API.
      
      **Contract documentation structure (RIU-015):**
      ```yaml
      contract_id: "order-enrichment-v2"
      version: "2.1.0"
      owner: "ai-platform-team"
      consumers: ["legacy-orders", "reporting-service"]
      last_updated: "2024-06-15"
      
      # What this integration does
      description: "AI enrichment of order data with risk scoring"
      
      # Request specification
      request:
        schema: "$ref: ./schemas/order-input.json"
        required_fields: [order_id, customer_id, items]
        content_type: "application/json"
        
      # Response specification  
      response:
        schema: "$ref: ./schemas/enriched-order.json"
        success_codes: [200, 202]
        error_codes: [400, 422, 500]
        
      # Non-functional requirements
      sla:
        latency_p99: 500ms
        availability: 99.9%
        rate_limit: 1000/min
        
      # Behavioral contract
      invariants:
        - "order_id in response == order_id in request"
        - "ai_risk_score is always between 0 and 1"
        - "response time < 30s or timeout with 504"
      ```
      
      **Standard formats by integration type:**
      | Integration Type | Format | Tool |
      |------------------|--------|------|
      | REST APIs | OpenAPI 3.x | Swagger, Stoplight |
      | Async/Events | AsyncAPI | AsyncAPI Studio |
      | Data schemas | JSON Schema | Glue Schema Registry |
      | GraphQL | GraphQL SDL | Apollo |
      | gRPC | Protocol Buffers | protoc |
      
      **Making contracts enforceable:**
      
      1. **Schema validation at runtime**
         - API Gateway request/response validation
         - Glue Schema Registry for streaming data
         - Lambda middleware for custom validation
      
      2. **Contract tests in CI/CD (RIU-080)**
         - **Pact** (industry standard): Consumer-driven contract testing
         - Producer tests: "My output matches the contract"
         - Consumer tests: "I can handle expected outputs"
         - Run on every commit (fast, <5 min)
      
      3. **Breaking change detection**
         - Schema Registry compatibility modes (BACKWARD, FORWARD, FULL)
         - PR checks that compare contract versions
         - Block deployment if compatibility broken
      
      **Consumer-driven contract testing (Pact pattern):**
      ```
      Consumer defines expected interactions
            ↓
      Contract published to Pact Broker
            ↓
      Provider verifies it can fulfill contract
            ↓
      Both sides deploy independently with confidence
      ```
      
      **Testing pyramid for contracts:**
      - **Unit tests**: Schema validation (fastest)
      - **Contract tests**: Pact consumer/provider tests
      - **Integration tests**: Service virtualization with mocks
      - **E2E tests**: Full integration in staging (slowest)
      
      **Version control and governance:**
      - Store contracts in Git alongside code
      - Require PR review for contract changes
      - Tag contracts with semantic versioning
      - Maintain changelog of breaking vs. non-breaking changes
      - Flag breaking changes as ONE-WAY DOORs (RIU-003)
      
      **AI-specific contract considerations:**
      - Document expected output variability (non-deterministic)
      - Include confidence score ranges in contract
      - Specify model version in response metadata
      - Define acceptable hallucination handling
      
      **PALETTE integration:**
      - Document contracts in RIU-015 (Contract for Outputs)
      - Test with RIU-080 (Contract Tests)
      - Version with RIU-016 (API Contract Review + Versioning Plan)
      - Validate data with RIU-084 (Data Quality Checks)
      
      Key insight: A contract that isn't tested automatically isn't enforceable. If it's not in CI/CD, it's just documentation — and documentation drifts.

## Evidence

- **Tier 1 (entry-level)**: [Generative AI Lifecycle Operational Excellence framework on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/introduction.html)
- **Tier 1 (entry-level)**: [Validate, evolve, and control schemas with AWS Glue Schema Registry](https://aws.amazon.com/blogs/big-data/validate-evolve-and-control-schemas-in-amazon-msk-and-amazon-kinesis-data-streams-with-aws-glue-schema-registry/)
- **Tier 1 (entry-level)**: [Automated Contract Compliance Analysis](https://awslabs.github.io/generative-ai-atlas/topics/6_0_example_application_and_reference_code/6_1_reference_applications_by_industry/6_1_5_cross_industry/automated_contract_analysis.html)
- **Tier 1 (entry-level)**: [Building a serverless distributed application using a saga orchestration pattern](https://aws.amazon.com/blogs/compute/building-a-serverless-distributed-application-using-a-saga-orchestration-pattern/)
- **Tier 1 (entry-level)**: [Application integration patterns for microservices: Orchestration and coordination](https://aws.amazon.com/blogs/compute/application-integration-patterns-for-microservices-orchestration-and-coordination/)
- **Tier 1 (entry-level)**: [Understanding idempotency: The art of doing a task once and only once](https://catalog.us-east-1.prod.workshops.aws/workshops/94007ed4-af54-4bdc-bf93-00b320d03925)
- **Tier 1 (entry-level)**: [Handle unpredictable processing times with operational consistency using Step Functions](https://aws.amazon.com/blogs/compute/handle-unpredictable-processing-times-with-operational-consistency-when-integrating-asynchronous-aws-services-with-an-aws-step-functions-state-machine/)
- **Tier 1 (entry-level)**: [A multi-dimensional approach helps you proactively prepare for failures](https://aws.amazon.com/blogs/architecture/a-multi-dimensional-approach-helps-you-proactively-prepare-for-failures-part-1-application-layer/)
- **Tier 1 (entry-level)**: [Detecting data drift using Amazon SageMaker](https://aws.amazon.com/blogs/architecture/detecting-data-drift-using-amazon-sagemaker/)
- **Tier 1 (entry-level)**: [Detect NLP data drift using custom Amazon SageMaker Model Monitor](https://aws.amazon.com/blogs/machine-learning/detect-nlp-data-drift-using-custom-amazon-sagemaker-model-monitor/)
- **Tier 1 (entry-level)**: [Automate model retraining with Amazon SageMaker Pipelines when drift is detected](https://aws.amazon.com/blogs/machine-learning/automate-model-retraining-with-amazon-sagemaker-pipelines-when-drift-is-detected/)
- **Tier 1 (entry-level)**: [Bring your own container to project model accuracy drift with Amazon SageMaker Model Monitor](https://aws.amazon.com/blogs/machine-learning/bring-your-own-container-to-project-model-accuracy-drift-with-amazon-sagemaker-model-monitor/)
- **Tier 1 (entry-level)**: [Generative AI Lifecycle Operational Excellence framework on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/introduction.html)
- **Tier 1 (entry-level)**: [Pact: Consumer-Driven Contract Testing](https://docs.pact.io/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-003](../rius/RIU-003.md)
- [RIU-004](../rius/RIU-004.md)
- [RIU-015](../rius/RIU-015.md)
- [RIU-016](../rius/RIU-016.md)
- [RIU-060](../rius/RIU-060.md)
- [RIU-061](../rius/RIU-061.md)
- [RIU-080](../rius/RIU-080.md)
- [RIU-084](../rius/RIU-084.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-060](../paths/RIU-060-deployment-readiness-envelope.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-032.
Evidence tier: 1.
Journey stage: all.
