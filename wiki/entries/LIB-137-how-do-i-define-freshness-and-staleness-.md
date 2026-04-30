---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-137
source_hash: sha256:02441a3788f0d32b
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [data-quality, freshness, knowledge-entry, orphan-detection, retrieval, staleness]
related: [RIU-011, RIU-025, RIU-085]
handled_by: [architect, builder, monitor]
journey_stage: retrieval
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I define freshness and staleness rules to prevent stale data from being surfaced in AI recommendations?

RIU-025 implements deterministic freshness rules in three tiers. Tier 1 — Freshness Classes: classify every data source into freshness categories. Real-time (< 1 minute): user actions, prices, inventory. Near-real-time (< 1 hour): aggregated metrics, event streams. Daily: reports, batch analytics. Weekly+: reference data, taxonomies. Tier 2 — Staleness Rules: for each freshness class, define what happens when data exceeds its expected freshness window. Options: downrank (reduce confidence score), omit (exclude from results), flag (include with staleness warning), fallback (serve cached version with disclaimer). Tier 3 — Orphan Detection: implement last-seen snapshots to detect records that have disappeared from the source but still exist in downstream systems. An orphan is a record whose source_id no longer exists in the authoritative system — it must be flagged or removed, never silently served. Implementation: add last_refreshed_at and freshness_class fields to every data record. Build a staleness monitor (cron or event-driven) that compares current time against last_refreshed_at and applies the appropriate staleness rule. Common failure: missing timestamps on source data make staleness undetectable. Require timestamps as a data contract prerequisite (RIU-011).

## Definition

RIU-025 implements deterministic freshness rules in three tiers. Tier 1 — Freshness Classes: classify every data source into freshness categories. Real-time (< 1 minute): user actions, prices, inventory. Near-real-time (< 1 hour): aggregated metrics, event streams. Daily: reports, batch analytics. Weekly+: reference data, taxonomies. Tier 2 — Staleness Rules: for each freshness class, define what happens when data exceeds its expected freshness window. Options: downrank (reduce confidence score), omit (exclude from results), flag (include with staleness warning), fallback (serve cached version with disclaimer). Tier 3 — Orphan Detection: implement last-seen snapshots to detect records that have disappeared from the source but still exist in downstream systems. An orphan is a record whose source_id no longer exists in the authoritative system — it must be flagged or removed, never silently served. Implementation: add last_refreshed_at and freshness_class fields to every data record. Build a staleness monitor (cron or event-driven) that compares current time against last_refreshed_at and applies the appropriate staleness rule. Common failure: missing timestamps on source data make staleness undetectable. Require timestamps as a data contract prerequisite (RIU-011).

## Evidence

- **Tier 1 (entry-level)**: [Google: Data Management in Machine Learning](https://cloud.google.com/architecture/data-management-in-machine-learning)
- **Tier 1 (entry-level)**: [Databricks: Data Quality at Scale](https://www.databricks.com/blog/data-quality-scale)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-011](../rius/RIU-011.md)
- [RIU-025](../rius/RIU-025.md)
- [RIU-085](../rius/RIU-085.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-137.
Evidence tier: 1.
Journey stage: retrieval.
