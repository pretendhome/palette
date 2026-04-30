---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-156
source_hash: sha256:5fbba5508f180437
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [data-integrity, database, knowledge-entry, migration, orchestration, rollback, zero-downtime]
related: [RIU-020, RIU-086, RIU-321]
handled_by: [architect, builder, debugger, researcher, validator]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I plan and execute a database migration without downtime or data loss?

RIU-321 defines database migration in five phases. Phase 1 — Pre-Migration Assessment: document the source schema, data volume, access patterns, and dependencies. Identify: tables with foreign key relationships (migration order matters), stored procedures and triggers (must be migrated or replaced), application queries that will need changes, and data that requires transformation. Phase 2 — Migration Strategy Selection: choose based on constraints. Blue-Green: run old and new databases in parallel, switch traffic atomically. Best for: small-medium databases where you can afford double infrastructure cost temporarily. Strangler Fig: migrate table by table, routing queries to the new database as each table is migrated. Best for: large databases where full parallel operation is too expensive. Online Migration: use change data capture (CDC) to replicate changes in real-time while migrating historical data. Best for: zero-downtime requirements with large data volumes. Phase 3 — Rollback Plan: define how to revert if the migration fails. For blue-green: switch traffic back. For strangler: re-route queries. For online: stop CDC and revert application config. Test the rollback before attempting the migration. Phase 4 — Validation: after migration, run data integrity checks: row counts, checksum comparisons, query result comparisons for critical queries. Validate application behavior with the regression suite (RIU-086). Phase 5 — Monitoring: monitor the new database for 48-72 hours post-migration. Watch for: query performance regressions, connection pool exhaustion, replication lag, and storage growth anomalies.

## Definition

RIU-321 defines database migration in five phases. Phase 1 — Pre-Migration Assessment: document the source schema, data volume, access patterns, and dependencies. Identify: tables with foreign key relationships (migration order matters), stored procedures and triggers (must be migrated or replaced), application queries that will need changes, and data that requires transformation. Phase 2 — Migration Strategy Selection: choose based on constraints. Blue-Green: run old and new databases in parallel, switch traffic atomically. Best for: small-medium databases where you can afford double infrastructure cost temporarily. Strangler Fig: migrate table by table, routing queries to the new database as each table is migrated. Best for: large databases where full parallel operation is too expensive. Online Migration: use change data capture (CDC) to replicate changes in real-time while migrating historical data. Best for: zero-downtime requirements with large data volumes. Phase 3 — Rollback Plan: define how to revert if the migration fails. For blue-green: switch traffic back. For strangler: re-route queries. For online: stop CDC and revert application config. Test the rollback before attempting the migration. Phase 4 — Validation: after migration, run data integrity checks: row counts, checksum comparisons, query result comparisons for critical queries. Validate application behavior with the regression suite (RIU-086). Phase 5 — Monitoring: monitor the new database for 48-72 hours post-migration. Watch for: query performance regressions, connection pool exhaustion, replication lag, and storage growth anomalies.

## Evidence

- **Tier 1 (entry-level)**: [AWS Database Migration Service Best Practices](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html)
- **Tier 1 (entry-level)**: [Martin Fowler: Strangler Fig Pattern](https://martinfowler.com/bliki/StranglerFigApplication.html)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-020](../rius/RIU-020.md)
- [RIU-086](../rius/RIU-086.md)
- [RIU-321](../rius/RIU-321.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Debugger](../agents/debugger.md)
- [Researcher](../agents/researcher.md)
- [Validator](../agents/validator.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-156.
Evidence tier: 1.
Journey stage: orchestration.
