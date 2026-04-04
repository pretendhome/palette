---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-028
source_hash: sha256:c3dc644bc66d03ac
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, api-versioning, backward-compatibility, change-management, governance, knowledge-entry]
related: [RIU-003, RIU-007, RIU-016, RIU-061, RIU-062, RIU-080, RIU-532]
handled_by: [architect, builder, debugger, monitor, narrator, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I version APIs when both AI and legacy systems depend on them?

API versioning with mixed consumers (AI + legacy) requires balancing innovation speed with stability. Use a combination of versioning strategy, compatibility layers, and clear deprecation policies.

## Definition

API versioning with mixed consumers (AI + legacy) requires balancing innovation speed with stability. Use a combination of versioning strategy, compatibility layers, and clear deprecation policies.
      
      **Versioning strategies:**
      | Strategy | Example | Pros | Cons | Best For |
      |----------|---------|------|------|----------|
      | URL Path | `/v1/orders`, `/v2/orders` | Clear, cacheable | URL proliferation | Public APIs |
      | Header | `X-API-Version: 2` | Clean URLs | Hidden versioning | Internal APIs |
      | Query Param | `/orders?version=2` | Easy to test | Cache complications | Debug/testing |
      
      **Recommended: Header-based with CloudFront + Lambda@Edge**
      - Route requests to different backends based on `X-API-Version` header
      - Store version configuration in DynamoDB, cache in Lambda@Edge
      - Preserve clean URLs while supporting multiple versions
      
      **Compatibility layer (API Gateway mapping templates):**
      - Transform requests/responses to maintain compatibility
      - Backend can evolve while old consumers see consistent interface
      - Clone API to create v2, use mapping templates to bridge differences
      - Both versions coexist, consumers migrate on their schedule
      
      **Version lifecycle (adapt Kubernetes model):**
      1. **Alpha**: Experimental, may change without notice, AI services only
      2. **Beta**: Stable interface, may have bugs, early adopters
      3. **Stable**: Production-ready, backward-compatible changes only
      4. **Deprecated**: Still works, sunset date announced, warnings emitted
      5. **Removed**: No longer available
      
      **Deprecation policy:**
      - Announce deprecation minimum 6 months before removal (longer for legacy)
      - Emit deprecation warnings in response headers
      - Provide migration guide and tooling to identify deprecated usage
      - Monitor deprecated endpoint usage — don't remove until traffic drops
      - Document in API changelog and notify consumers directly
      
      **AI-specific considerations:**
      - AI outputs may be non-deterministic — version the *contract*, not the exact output
      - Include model version in response metadata for debugging
      - AI services can consume newer versions faster — use them as early adopters
      - Legacy systems need longer deprecation windows — plan accordingly
      
      **Implementation with AWS:**
      - **API Gateway**: Create separate stages or cloned APIs per version
      - **CloudFront + Lambda@Edge**: Route based on headers
      - **Mapping templates**: Transform between versions without backend changes
      - **Strangler pattern**: Facade provides uniform access during migration
      
      **PALETTE integration:**
      - Document API versions in RIU-016 (API Contract Review + Versioning Plan)
      - Track breaking changes as ONE-WAY DOORs in Decision Log (RIU-003)
      - Define deprecation timeline in Constraint Profile (RIU-007)
      - Test all supported versions with RIU-080 (Contract Tests)
      
      Key insight: Legacy systems can't upgrade quickly — maintain N-1 (or N-2) version support. AI systems can move faster — use them to validate new versions before legacy consumers migrate.

## Evidence

- **Tier 1 (entry-level)**: [Implementing header-based API Gateway versioning with Amazon CloudFront](https://aws.amazon.com/blogs/compute/implementing-header-based-api-gateway-versioning-with-amazon-cloudfront/)
- **Tier 1 (entry-level)**: [Using API Gateway mapping templates to handle changes in your back-end APIs](https://aws.amazon.com/blogs/compute/using-api-gateway-mapping-templates-to-handle-changes-in-your-back-end-apis/)
- **Tier 1 (entry-level)**: [Modernizing SOAP applications using Amazon API Gateway and AWS Lambda](https://aws.amazon.com/blogs/compute/modernizing-soap-applications-using-amazon-api-gateway-and-aws-lambda/)
- **Tier 1 (entry-level)**: [Preparing for Kubernetes API deprecations](https://aws.amazon.com/blogs/containers/preparing-for-kubernetes-api-deprecations-when-going-from-1-15-to-1-16/)
- **Tier 1 (entry-level)**: [Google Cloud API Design Guide — Versioning](https://cloud.google.com/apis/design/versioning)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-003](../rius/RIU-003.md)
- [RIU-007](../rius/RIU-007.md)
- [RIU-016](../rius/RIU-016.md)
- [RIU-061](../rius/RIU-061.md)
- [RIU-062](../rius/RIU-062.md)
- [RIU-080](../rius/RIU-080.md)
- [RIU-532](../rius/RIU-532.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)
- [Monitor](../agents/monitor.md)
- [Narrator](../agents/narrator.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-028.
Evidence tier: 1.
Journey stage: all.
