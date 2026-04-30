---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-132
source_hash: sha256:ed539f1d6b49dfbc
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [access, foundation, knowledge-entry, onboarding, permissions, security]
related: [RIU-010, RIU-012]
handled_by: [architect, builder, validator]
journey_stage: foundation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I create an access and permissions readiness checklist that prevents delivery delays from missing credentials or network access?

Build the checklist in three layers using RIU-010. Layer 1 — Enumerate: list every system the engagement touches (APIs, databases, cloud consoles, VPNs, SSO portals). For each, record the credential type (API key, OAuth token, IAM role, service account), the required permission level (read-only vs read-write), and the provisioning owner. Layer 2 — Least Privilege: apply the principle of least privilege (NIST SP 800-53 AC-6). Request only the minimum permissions needed for the current phase. Document justification for any elevated access. Set expiration dates on temporary credentials. Layer 3 — Smoke Tests: write a runnable smoke test per system that validates connectivity and permission scope before development begins. Test read access, write access (to a sandbox), and network path (VPN, VPC peering, firewall rules). A blocked network path discovered on Day 1 is a schedule save; discovered on Day 10 is a schedule slip. Common failure mode: over-privileged tokens that pass smoke tests but violate compliance during security review. Always cross-reference with RIU-012 (PII/Compliance Triage) if regulated data is involved.

## Definition

Build the checklist in three layers using RIU-010. Layer 1 — Enumerate: list every system the engagement touches (APIs, databases, cloud consoles, VPNs, SSO portals). For each, record the credential type (API key, OAuth token, IAM role, service account), the required permission level (read-only vs read-write), and the provisioning owner. Layer 2 — Least Privilege: apply the principle of least privilege (NIST SP 800-53 AC-6). Request only the minimum permissions needed for the current phase. Document justification for any elevated access. Set expiration dates on temporary credentials. Layer 3 — Smoke Tests: write a runnable smoke test per system that validates connectivity and permission scope before development begins. Test read access, write access (to a sandbox), and network path (VPN, VPC peering, firewall rules). A blocked network path discovered on Day 1 is a schedule save; discovered on Day 10 is a schedule slip. Common failure mode: over-privileged tokens that pass smoke tests but violate compliance during security review. Always cross-reference with RIU-012 (PII/Compliance Triage) if regulated data is involved.

## Evidence

- **Tier 1 (entry-level)**: [NIST SP 800-53: Security and Privacy Controls — AC-6 Least Privilege](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- **Tier 1 (entry-level)**: [AWS IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-010](../rius/RIU-010.md)
- [RIU-012](../rius/RIU-012.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-132.
Evidence tier: 1.
Journey stage: foundation.
