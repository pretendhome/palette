---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-119
source_hash: sha256:56e419690932cf20
compiled_at: 2026-04-29T20:17:20Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 1
tags: [experimentation, feature-flags, kill-switch, knowledge-entry, orchestration, rollout]
related: [RIU-064, RIU-068]
handled_by: [architect, builder, monitor]
journey_stage: orchestration
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I implement feature flags and kill switches for AI model rollouts?

Feature flags gate model versions, prompt variants, and pipeline configurations behind runtime toggles. Use a dedicated feature flag platform (LaunchDarkly or Statsig) rather than config files — you need instant kill switches without redeployment. Key patterns — percentage rollouts (10% to 50% to 100%), targeting rules (route enterprise customers to stable model, beta users to experimental), and kill switches (disable a model variant in seconds if quality degrades). Statsig adds built-in A/B testing and statistical significance tracking. LaunchDarkly is more mature for enterprise governance. Decision — if you need experiment analytics, use Statsig. If you need enterprise audit trails and approval workflows, use LaunchDarkly. Both support server-side SDKs for backend AI services.

## Definition

Feature flags gate model versions, prompt variants, and pipeline configurations behind runtime toggles. Use a dedicated feature flag platform (LaunchDarkly or Statsig) rather than config files — you need instant kill switches without redeployment. Key patterns — percentage rollouts (10% to 50% to 100%), targeting rules (route enterprise customers to stable model, beta users to experimental), and kill switches (disable a model variant in seconds if quality degrades). Statsig adds built-in A/B testing and statistical significance tracking. LaunchDarkly is more mature for enterprise governance. Decision — if you need experiment analytics, use Statsig. If you need enterprise audit trails and approval workflows, use LaunchDarkly. Both support server-side SDKs for backend AI services.

## Evidence

- **Tier 1 (entry-level)**: [LaunchDarkly: Feature Flags and Feature Management](https://launchdarkly.com/)
- **Tier 1 (entry-level)**: [Fast.io: AI Agent Secrets Management Best Practices](https://fast.io/resources/ai-agent-secrets-management/)
- **1**: Palette Remediation Loop — Automated Validation, Diagnosis, and Fix Pipeline (`agents/remediation/ARCHITECTURE_SPEC.md`)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-064](../rius/RIU-064.md)
- [RIU-068](../rius/RIU-068.md)

## Handled By

- [Architect](../agents/architect.md)
- [Builder](../agents/builder.md)
- [Monitor](../agents/monitor.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-119.
Evidence tier: 1.
Journey stage: orchestration.
