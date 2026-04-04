---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-142
source_hash: sha256:612d33175659c98a
compiled_at: 2026-04-04T15:44:26Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [configuration, deployment, devops, environment-parity, knowledge-entry, orchestration]
related: [RIU-065]
handled_by: [builder]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I manage configuration and environment parity to prevent the "works in staging, fails in production" problem?

RIU-065 addresses configuration management through three practices. Practice 1 — Single Source of Configuration: store all configuration in version-controlled files (not environment variables alone). Use a layered config approach: base config (shared across all environments) + environment overlay (env-specific overrides). Tools: AWS Systems Manager Parameter Store, HashiCorp Vault for secrets, or simple YAML files with environment prefixes. Never hardcode configuration in application code. Practice 2 — Environment Parity Checks: write automated checks that compare configuration across environments (dev, staging, production). For each config key, categorize as: must-match (e.g., schema versions, feature flags), intentionally-different (e.g., database URLs, API endpoints), or environment-specific (e.g., log levels, debug flags). Alert on any must-match key that differs between staging and production. Practice 3 — Explicit Difference Documentation: maintain a living document that lists every intentional difference between environments. If a difference is not documented, it is a bug. Common failure modes: (a) undocumented environment variables that exist in production but not staging — catch with config key enumeration; (b) secrets rotation that updates production but not staging; (c) model version pinning that differs across environments — use the same version pinning mechanism everywhere. For AI systems specifically: model version, prompt template version, and guardrail configuration must be environment-parity checked.

## Definition

RIU-065 addresses configuration management through three practices. Practice 1 — Single Source of Configuration: store all configuration in version-controlled files (not environment variables alone). Use a layered config approach: base config (shared across all environments) + environment overlay (env-specific overrides). Tools: AWS Systems Manager Parameter Store, HashiCorp Vault for secrets, or simple YAML files with environment prefixes. Never hardcode configuration in application code. Practice 2 — Environment Parity Checks: write automated checks that compare configuration across environments (dev, staging, production). For each config key, categorize as: must-match (e.g., schema versions, feature flags), intentionally-different (e.g., database URLs, API endpoints), or environment-specific (e.g., log levels, debug flags). Alert on any must-match key that differs between staging and production. Practice 3 — Explicit Difference Documentation: maintain a living document that lists every intentional difference between environments. If a difference is not documented, it is a bug. Common failure modes: (a) undocumented environment variables that exist in production but not staging — catch with config key enumeration; (b) secrets rotation that updates production but not staging; (c) model version pinning that differs across environments — use the same version pinning mechanism everywhere. For AI systems specifically: model version, prompt template version, and guardrail configuration must be environment-parity checked.

## Evidence

- **Tier 1 (entry-level)**: [The Twelve-Factor App: Config](https://12factor.net/config)
- **Tier 1 (entry-level)**: [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-065](../rius/RIU-065.md)

## Handled By

- [Builder](../agents/builder.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-142.
Evidence tier: 1.
Journey stage: orchestration.
