---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-029
source_hash: sha256:ff8ecf33ed43be07
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, integration-testing, knowledge-entry, quality-assurance, testing, validation]
related: [RIU-060, RIU-062, RIU-063, RIU-080, RIU-081, RIU-540]
handled_by: [architect, builder, debugger, monitor, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# What's the minimum viable integration test suite for AI-to-legacy connections?

A minimum viable integration test suite validates that AI and legacy systems communicate correctly without requiring exhaustive coverage. Focus on critical paths, failure modes, and contract compliance.

## Definition

A minimum viable integration test suite validates that AI and legacy systems communicate correctly without requiring exhaustive coverage. Focus on critical paths, failure modes, and contract compliance.
      
      **Minimum test categories (must have all 5):**
      
      **1. Contract Tests (RIU-080)**
      - Validate AI service outputs match expected schema
      - Validate legacy system accepts AI-formatted requests
      - Version-controlled contracts define expected requests/responses
      - Run on every code change (shift-left)
      ```
      Test: AI enrichment output matches contract v2.1
      Input: Sample order payload
      Assert: Response validates against JSON schema
      Assert: Required fields present (order_id, ai_risk_score)
      ```
      
      **2. Connectivity Smoke Tests (RIU-081)**
      - AI service can reach legacy endpoint
      - Authentication succeeds (tokens, API keys, certificates)
      - Basic request/response round-trip works
      - Run pre/post deployment
      ```
      Test: Legacy order API reachable
      Assert: GET /health returns 200 within 5s
      Assert: POST /orders with valid payload returns 201
      ```
      
      **3. Data Flow Tests**
      - End-to-end data pipeline: ingestion → processing → AI → legacy
      - For RAG: document ingestion → embedding → vector store → retrieval
      - Verify data transformations preserve required fields
      ```
      Test: Order flows from legacy to AI enrichment to legacy update
      Assert: Original order_id preserved
      Assert: AI-added fields present in final record
      ```
      
      **4. Error Handling Tests**
      - Legacy timeout → AI handles gracefully
      - Legacy returns error → AI logs and falls back
      - Invalid data from legacy → AI rejects with clear message
      - Use service virtualization to simulate failure scenarios
      ```
      Test: Legacy API returns 500
      Assert: AI service returns degraded response (not 500)
      Assert: Error logged with correlation ID
      Assert: Retry attempted with backoff
      ```
      
      **5. Auth/Authz Tests**
      - Service-to-service authentication works
      - Role-based access controls enforced
      - Token refresh/rotation handled
      ```
      Test: AI service authenticates to legacy with service account
      Assert: Valid token accepted
      Assert: Expired token triggers refresh
      Assert: Invalid token rejected with 401
      ```
      
      **Optional but recommended:**
      - **Load/Performance**: OLAF or similar for SageMaker endpoints — verify latency under expected load
      - **UI Journey**: Amazon Nova Act headless mode for end-to-end user flows
      - **Model Accuracy**: Smoke test new model versions before production
      
      **Test data strategy:**
      - Create fixtures representing common cases + known edge cases
      - Use service virtualization (mocks) for legacy system simulation
      - Sanitize production data for realistic test scenarios
      - Store fixtures alongside tests in version control
      
      **CI/CD integration:**
      - Contract tests: Every commit (fast, <5 min)
      - Smoke tests: Every deployment (medium, <15 min)
      - Full integration: Nightly or pre-release (longer, <1 hour)
      
      **"Minimum viable" criteria:**
      - [ ] All 5 test categories have at least 1 test each
      - [ ] Tests run automatically in CI/CD
      - [ ] Critical path (happy path) covered
      - [ ] At least 1 failure scenario per integration point
      - [ ] Tests pass in staging before production deployment
      
      **PALETTE integration:**
      - Define test suite in RIU-081 (E2E Smoke Tests)
      - Contract tests per RIU-080
      - Document test coverage gaps in Assumptions Register (RIU-008)
      - Include test execution in Deployment Readiness (RIU-060)

## Evidence

- **Tier 1 (entry-level)**: [Generative AI Lifecycle Operational Excellence framework on AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/gen-ai-lifecycle-operational-excellence/introduction.html)
- **Tier 1 (entry-level)**: [Testing approaches for Amazon SageMaker ML models](https://aws.amazon.com/blogs/machine-learning/testing-approaches-for-amazon-sagemaker-ml-models/)
- **Tier 1 (entry-level)**: [Implement automated smoke testing using Amazon Nova Act headless mode](https://aws.amazon.com/blogs/machine-learning/implement-automated-smoke-testing-using-amazon-nova-act-headless-mode/)
- **Tier 1 (entry-level)**: [Speed meets scale: Load testing SageMaker AI endpoints with OLAF](https://aws.amazon.com/blogs/machine-learning/speed-meets-scale-load-testing-sagemakerai-endpoints-with-observe-ais-testing-tool/)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-060](../rius/RIU-060.md)
- [RIU-062](../rius/RIU-062.md)
- [RIU-063](../rius/RIU-063.md)
- [RIU-080](../rius/RIU-080.md)
- [RIU-081](../rius/RIU-081.md)
- [RIU-540](../rius/RIU-540.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)
- [Monitor](../agents/monitor.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-060](../paths/RIU-060-deployment-readiness-envelope.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-029.
Evidence tier: 1.
Journey stage: all.
