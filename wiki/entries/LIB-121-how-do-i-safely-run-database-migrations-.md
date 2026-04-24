---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-121
source_hash: sha256:e4f12bf9662d4690
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [database-migration, flyway, knowledge-entry, orchestration, rollback, schema-change]
related: [RIU-067]
handled_by: [architect, builder]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I safely run database migrations in AI systems without downtime or data loss?

Use a versioned migration tool (Flyway for JVM/SQL, Alembic for Python/SQLAlchemy) with mandatory dry-run before apply. Every migration must be reversible — write both up and down scripts. For AI systems specifically, schema changes to feature stores or embedding tables require coordinated deployment with the model that reads them. Pattern — deploy new schema version alongside old (expand phase), update application code (migrate phase), drop old columns (contract phase). Never run ALTER TABLE on production without a tested rollback script. Use blue-green deployment for vector database index rebuilds — build new index in parallel, swap pointer when ready.

## Definition

Use a versioned migration tool (Flyway for JVM/SQL, Alembic for Python/SQLAlchemy) with mandatory dry-run before apply. Every migration must be reversible — write both up and down scripts. For AI systems specifically, schema changes to feature stores or embedding tables require coordinated deployment with the model that reads them. Pattern — deploy new schema version alongside old (expand phase), update application code (migrate phase), drop old columns (contract phase). Never run ALTER TABLE on production without a tested rollback script. Use blue-green deployment for vector database index rebuilds — build new index in parallel, swap pointer when ready.

## Evidence

- **Tier 3 (entry-level)**: [Debugg.ai: Best Schema Migration Tools for 2024](https://debugg.ai/resources/best-schema-migration-tools-2024)
- **Tier 3 (entry-level)**: [Bytebase: Top Database Schema Migration Tools 2026](https://www.bytebase.com/blog/top-database-schema-change-tool-evolution/)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-067](../rius/RIU-067.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-121.
Evidence tier: 3.
Journey stage: orchestration.
