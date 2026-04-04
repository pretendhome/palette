---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-163
source_hash: sha256:d04e8896c4ba90bb
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [audit, content-quality, coverage, deduplication, evaluation, knowledge-base, knowledge-entry]
related: [RIU-232, RIU-400]
handled_by: [builder, researcher, validator]
journey_stage: evaluation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I audit a knowledge base for coverage, duplication, staleness, and structural issues?

RIU-400 defines a KB audit in four dimensions. Dimension 1 — Coverage Analysis: map the KB content against the known query universe. Identify coverage gaps by: (a) analyzing support tickets and search queries that returned no results; (b) mapping KB articles against product features and finding undocumented features; (c) checking for user journey gaps — can a user complete their entire workflow using only KB content? Score coverage as percentage of known topics covered. Target: 85%+ for mature KBs. Dimension 2 — Duplication Analysis: identify articles that cover the same topic. Use embedding similarity to find near-duplicates (cosine similarity > 0.85). For each duplicate set: determine the authoritative article, merge unique information from duplicates into it, and redirect or remove duplicates. Duplication inflates search results and confuses users — a KB with 500 articles where 100 are duplicates performs worse than a KB with 400 unique articles. Dimension 3 — Staleness Analysis: for each article, check: last modified date (stale if > 6 months without review), referenced product versions (stale if referencing deprecated versions), broken links (indicate unmaintained content), and factual accuracy (spot-check 10% of articles against current product behavior). Dimension 4 — Structural Analysis: evaluate information architecture. Check: consistent formatting, appropriate categorization, search findability (test 20 common queries), and navigation paths (can users browse to relevant content?). Prioritize fixes by impact: fix high-traffic gaps before low-traffic staleness.

## Definition

RIU-400 defines a KB audit in four dimensions. Dimension 1 — Coverage Analysis: map the KB content against the known query universe. Identify coverage gaps by: (a) analyzing support tickets and search queries that returned no results; (b) mapping KB articles against product features and finding undocumented features; (c) checking for user journey gaps — can a user complete their entire workflow using only KB content? Score coverage as percentage of known topics covered. Target: 85%+ for mature KBs. Dimension 2 — Duplication Analysis: identify articles that cover the same topic. Use embedding similarity to find near-duplicates (cosine similarity > 0.85). For each duplicate set: determine the authoritative article, merge unique information from duplicates into it, and redirect or remove duplicates. Duplication inflates search results and confuses users — a KB with 500 articles where 100 are duplicates performs worse than a KB with 400 unique articles. Dimension 3 — Staleness Analysis: for each article, check: last modified date (stale if > 6 months without review), referenced product versions (stale if referencing deprecated versions), broken links (indicate unmaintained content), and factual accuracy (spot-check 10% of articles against current product behavior). Dimension 4 — Structural Analysis: evaluate information architecture. Check: consistent formatting, appropriate categorization, search findability (test 20 common queries), and navigation paths (can users browse to relevant content?). Prioritize fixes by impact: fix high-traffic gaps before low-traffic staleness.

## Evidence

- **Tier 3 (entry-level)**: [KCS (Knowledge-Centered Service): Practices Guide](https://www.serviceinnovation.org/kcs/)
- **Tier 3 (entry-level)**: [Gartner: Knowledge Management Best Practices](https://www.gartner.com/en/information-technology/glossary/knowledge-management)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-232](../rius/RIU-232.md)
- [RIU-400](../rius/RIU-400.md)

## Handled By

- [Builder](../agents/builder.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Learning Path

- [RIU-400](../paths/RIU-400-kb-content-audit.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-163.
Evidence tier: 3.
Journey stage: evaluation.
