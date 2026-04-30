---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-145
source_hash: sha256:0f37671d51506dfe
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, approval, governance, human-review, knowledge-entry, one-way-door, safety]
related: [RIU-003, RIU-085, RIU-086, RIU-087]
handled_by: [architect, builder, monitor, validator]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I implement a human review gate for one-way door decisions in AI systems?

RIU-087 defines a gating process for irreversible decisions. Step 1 — Identify One-Way Doors: catalog all decisions that are difficult or impossible to reverse. In AI systems, common one-way doors include: production data deletion, model deployment to customer-facing systems, API contract changes that break backward compatibility, granting data access to third parties, and compliance certifications. Tag each in decisions.md with "ONE-WAY DOOR" label. Step 2 — Review Checklist: for each one-way door category, define a review checklist. Example for model deployment: (a) regression suite passes (RIU-086), (b) cost/latency within budget envelope (RIU-085), (c) security review complete (RIU-250), (d) rollback plan documented and tested, (e) monitoring alerts configured. Step 3 — Sign-Off Protocol: require explicit sign-off from the designated decision authority (identified via RIU-002 RACI). Sign-off must be recorded in decisions.md with: decision description, reviewer name, date, conditions, and any dissenting opinions. Step 4 — Bypass Prevention: the gate must not be bypassable by the agent or automation. Implement as a hard block in the workflow — the system cannot proceed without the recorded sign-off. Common failure: gates get bypassed during "urgent" incidents. Counter by defining an emergency bypass protocol that requires two approvers and mandatory post-incident review. The gate is itself a two-way door (you can change the gate criteria), but the decisions it protects are one-way doors.

## Definition

RIU-087 defines a gating process for irreversible decisions. Step 1 — Identify One-Way Doors: catalog all decisions that are difficult or impossible to reverse. In AI systems, common one-way doors include: production data deletion, model deployment to customer-facing systems, API contract changes that break backward compatibility, granting data access to third parties, and compliance certifications. Tag each in decisions.md with "ONE-WAY DOOR" label. Step 2 — Review Checklist: for each one-way door category, define a review checklist. Example for model deployment: (a) regression suite passes (RIU-086), (b) cost/latency within budget envelope (RIU-085), (c) security review complete (RIU-250), (d) rollback plan documented and tested, (e) monitoring alerts configured. Step 3 — Sign-Off Protocol: require explicit sign-off from the designated decision authority (identified via RIU-002 RACI). Sign-off must be recorded in decisions.md with: decision description, reviewer name, date, conditions, and any dissenting opinions. Step 4 — Bypass Prevention: the gate must not be bypassable by the agent or automation. Implement as a hard block in the workflow — the system cannot proceed without the recorded sign-off. Common failure: gates get bypassed during "urgent" incidents. Counter by defining an emergency bypass protocol that requires two approvers and mandatory post-incident review. The gate is itself a two-way door (you can change the gate criteria), but the decisions it protects are one-way doors.

## Evidence

- **Tier 1 (entry-level)**: [Amazon Leadership Principles: One-Way and Two-Way Door Decisions](https://www.aboutamazon.com/about-us/leadership-principles)
- **Tier 1 (entry-level)**: [NIST AI RMF: Govern Function — Decision Authority](https://www.nist.gov/artificial-intelligence/ai-risk-management-framework)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-003](../rius/RIU-003.md)
- [RIU-085](../rius/RIU-085.md)
- [RIU-086](../rius/RIU-086.md)
- [RIU-087](../rius/RIU-087.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-145.
Evidence tier: 1.
Journey stage: all.
