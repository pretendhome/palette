---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-152
source_hash: sha256:fd5b311e46970be3
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [data-quality, deduplication, entity-resolution, knowledge-entry, matching, retrieval]
related: [RIU-013, RIU-232]
handled_by: [builder, researcher, validator]
journey_stage: retrieval
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I implement a deduplication system that avoids both missed duplicates and false merges?

RIU-232 defines deduplication in four stages. Stage 1 — Candidate Generation (Blocking): reduce the comparison space by grouping records that are likely duplicates using blocking keys (e.g., first 3 characters of name + zip code). Without blocking, comparing N records requires N*(N-1)/2 comparisons — this is O(N^2) and infeasible for large datasets. Stage 2 — Similarity Scoring: for each candidate pair, compute similarity using multiple signals. For text: edit distance (Levenshtein), token overlap (Jaccard), semantic similarity (embedding cosine). For structured records: field-level exact match + fuzzy match. Combine signals into a composite score (weighted average or learned model). Stage 3 — Threshold Decision: define three zones. Match zone (score > 0.90): automatically merge. Review zone (0.70-0.90): flag for human review. Non-match zone (< 0.70): no action. Tune thresholds on a labeled sample of 200+ pairs. The review zone is critical — it catches cases where the algorithm is uncertain and prevents both false positives (merging distinct records) and false negatives (missing real duplicates). Stage 4 — Conflict Resolution: when merging, define field-level resolution rules. Options: most recent wins, most complete wins, source priority (gold-tier system wins), or human review for conflicts. Never silently discard data during merge — preserve the full merge history so merges can be reversed. The most dangerous failure mode is false positive deduplication — merging records for two different entities. This is data loss and often irreversible.

## Definition

RIU-232 defines deduplication in four stages. Stage 1 — Candidate Generation (Blocking): reduce the comparison space by grouping records that are likely duplicates using blocking keys (e.g., first 3 characters of name + zip code). Without blocking, comparing N records requires N*(N-1)/2 comparisons — this is O(N^2) and infeasible for large datasets. Stage 2 — Similarity Scoring: for each candidate pair, compute similarity using multiple signals. For text: edit distance (Levenshtein), token overlap (Jaccard), semantic similarity (embedding cosine). For structured records: field-level exact match + fuzzy match. Combine signals into a composite score (weighted average or learned model). Stage 3 — Threshold Decision: define three zones. Match zone (score > 0.90): automatically merge. Review zone (0.70-0.90): flag for human review. Non-match zone (< 0.70): no action. Tune thresholds on a labeled sample of 200+ pairs. The review zone is critical — it catches cases where the algorithm is uncertain and prevents both false positives (merging distinct records) and false negatives (missing real duplicates). Stage 4 — Conflict Resolution: when merging, define field-level resolution rules. Options: most recent wins, most complete wins, source priority (gold-tier system wins), or human review for conflicts. Never silently discard data during merge — preserve the full merge history so merges can be reversed. The most dangerous failure mode is false positive deduplication — merging records for two different entities. This is data loss and often irreversible.

## Evidence

- **Tier 3 (entry-level)**: [Christen: Data Matching — Concepts and Techniques (Springer, 2012)](https://doi.org/10.1007/978-3-642-31164-2)
- **Tier 3 (entry-level)**: [Fellegi-Sunter Model: Theory of Record Linkage (JASA, 1969)](https://doi.org/10.1080/01621459.1969.10501049)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-013](../rius/RIU-013.md)
- [RIU-232](../rius/RIU-232.md)

## Handled By

- [Builder](../agents/builder.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-152.
Evidence tier: 3.
Journey stage: retrieval.
