---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-153
source_hash: sha256:e157c62454490bde
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, compliance, knowledge-entry, review, security, threat-model]
related: [RIU-010, RIU-012, RIU-250, RIU-326]
handled_by: [architect, builder, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I compile a security review packet that passes review without delays?

RIU-250 defines the security review packet with six sections. Section 1 — System Overview: architecture diagram showing all components, data flows, trust boundaries, and external dependencies. Include the deployment model (single-tenant, multi-tenant, serverless). Section 2 — Threat Model: use STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) to identify threats at each trust boundary. For each threat: describe the attack vector, assess likelihood and impact, and document the mitigation. Section 3 — Data Flow Diagram: show how data moves through the system, including at-rest and in-transit encryption, storage locations, retention policies, and deletion procedures. Highlight any PII or regulated data paths. Cross-reference with RIU-012 (PII/Compliance Triage). Section 4 — Permissions Matrix: for every identity (human user, service account, agent), document: what they can access, what permission level (read/write/admin), how authentication works, and how access is revoked. Cross-reference with RIU-010 (Access Checklist). Section 5 — Mitigation Status: for each identified threat, show the current status: mitigated (control implemented and tested), in-progress (control being built), accepted (risk acknowledged by decision authority), or deferred (with timeline). Section 6 — Residual Risk Statement: explicitly state what risks remain after all mitigations. Security reviewers respect honesty about residual risk far more than claims of zero risk. Common delay cause: incomplete data flow diagrams — security reviewers cannot assess what they cannot see.

## Definition

RIU-250 defines the security review packet with six sections. Section 1 — System Overview: architecture diagram showing all components, data flows, trust boundaries, and external dependencies. Include the deployment model (single-tenant, multi-tenant, serverless). Section 2 — Threat Model: use STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) to identify threats at each trust boundary. For each threat: describe the attack vector, assess likelihood and impact, and document the mitigation. Section 3 — Data Flow Diagram: show how data moves through the system, including at-rest and in-transit encryption, storage locations, retention policies, and deletion procedures. Highlight any PII or regulated data paths. Cross-reference with RIU-012 (PII/Compliance Triage). Section 4 — Permissions Matrix: for every identity (human user, service account, agent), document: what they can access, what permission level (read/write/admin), how authentication works, and how access is revoked. Cross-reference with RIU-010 (Access Checklist). Section 5 — Mitigation Status: for each identified threat, show the current status: mitigated (control implemented and tested), in-progress (control being built), accepted (risk acknowledged by decision authority), or deferred (with timeline). Section 6 — Residual Risk Statement: explicitly state what risks remain after all mitigations. Security reviewers respect honesty about residual risk far more than claims of zero risk. Common delay cause: incomplete data flow diagrams — security reviewers cannot assess what they cannot see.

## Evidence

- **Tier 1 (entry-level)**: [Microsoft: STRIDE Threat Modeling](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)
- **Tier 1 (entry-level)**: [OWASP: Threat Modeling](https://owasp.org/www-community/Threat_Modeling)
- **Tier 1 (entry-level)**: [NIST SP 800-53: Security Assessment and Authorization](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-010](../rius/RIU-010.md)
- [RIU-012](../rius/RIU-012.md)
- [RIU-250](../rius/RIU-250.md)
- [RIU-326](../rius/RIU-326.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-153.
Evidence tier: 1.
Journey stage: all.
