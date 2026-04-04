---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-021
source_hash: sha256:c4a073b7ecb52da9
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [all, conflict-resolution, cross-functional, governance, knowledge-entry, rule-harmonization]
related: [RIU-003, RIU-007, RIU-008]
handled_by: [architect]
journey_stage: all
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I handle business rules that conflict across departments?

Rule conflicts are natural in enterprises — don't try to eliminate tension, establish governance to resolve it systematically.

## Definition

Rule conflicts are natural in enterprises — don't try to eliminate tension, establish governance to resolve it systematically.
      
      **Conflict detection:**
      - Document all rules with owning department and business justification
      - During rule ingestion, check for overlapping conditions with different outcomes
      - Flag conflicts explicitly: "Rule A (Sales) says X; Rule B (Compliance) says Y"
      - Store in centralized rule catalog (RIU-044) with cross-references
      
      **Resolution governance (Hybrid CoE model):**
      - **Executive Sponsor**: Final arbiter for unresolved conflicts affecting strategy
      - **AI Governance Lead**: Day-to-day conflict triage and resolution tracking
      - **Cross-Functional Oversight Team**: Representatives from each department evaluate conflicts
      - Use AIR workshop methodology when prioritization disputes arise
      
      **Priority framework:**
      1. **Regulatory/Compliance rules** → Always highest priority (non-negotiable)
      2. **Security/Safety rules** → Second priority
      3. **Customer-facing rules** → Third priority
      4. **Operational efficiency rules** → Lowest priority, most negotiable
      
      Document priority hierarchy in Constraint Profile (RIU-007) and get executive sign-off.
      
      **Resolution patterns:**
      - **Scope separation**: Rules apply to different contexts (e.g., "Sales rule for prospects, Compliance rule for regulated customers")
      - **Time-based precedence**: Newer rule supersedes unless explicitly versioned
      - **Escalation**: Use "Disagree and Commit" — debate respectfully, then fully commit to decision
      - **Merge**: Create unified rule that satisfies both intents
      
      **Technical implementation:**
      - Implement rule priority field (integer) in rule schema
      - When conflicts detected at runtime, highest priority wins
      - Log all conflict resolutions for audit trail
      - Alert when new rules create conflicts with existing rules
      
      **PALETTE integration:**
      - Document conflict resolutions in Decision Log (RIU-003) as they're often ONE-WAY DOORs
      - Track unresolved conflicts in Open Questions until governance resolves
      - Store harmonized rules in Assumptions Register (RIU-008) with validation plan
      
      Key insight: The goal isn't eliminating conflicts — it's making conflict resolution fast, transparent, and auditable. Establish the governance *before* you need it.

## Evidence

- **Tier 1 (entry-level)**: [Governance - Generative AI Atlas](https://awslabs.github.io/generative-ai-atlas/topics/4_0_systematic_path_to_production_framework/4_4_governance/index.html)
- **Tier 1 (entry-level)**: [Organizational Design and Team Structure for AI](https://awslabs.github.io/generative-ai-atlas/topics/5_0_organization_adoption_framework/5_2_governance_and_organization/5_2_2_organizational_design_team_structure.html)
- **Tier 1 (entry-level)**: [Governance by design: The essential guide for successful AI scaling](https://aws.amazon.com/blogs/machine-learning/governance-by-design-the-essential-guide-for-successful-ai-scaling/)
- **Tier 1 (entry-level)**: [Disagree and Commit - AWS Enterprise Strategy](https://aws.amazon.com/blogs/enterprise-strategy/guts-part-three-having-backbone-disagreeing-and-committing/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-003](../rius/RIU-003.md)
- [RIU-007](../rius/RIU-007.md)
- [RIU-008](../rius/RIU-008.md)

## Handled By

- [Architect](../agents/architect.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-021.
Evidence tier: 1.
Journey stage: all.
