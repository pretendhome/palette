# Palette V2.0 — Version Consistency Audit

**Date**: 2026-03-16
**Auditor**: Kiro
**Purpose**: Ensure all version references are consistent at V2.0 before push

---

## Version Discrepancies Found

| Location | Current Value | Should Be | Status |
|---|---|---|---|
| `MANIFEST.yaml` line 7 | `"2.1"` | `"2.0"` | ❌ NEEDS FIX |
| `FDE_READINESS.md` line 4 | `2.1 (SDK Hardening + Dual Enablement)` | `2.0` | ❌ NEEDS FIX |
| `FDE_READINESS.md` line 22 | `V2.1 improvements` | `V2.0 improvements` | ❌ NEEDS FIX |
| `CHANGELOG.md` line 19 | `[2.1.0] - 2026-03-16` | `[2.0.0] - 2026-03-16` | ❌ NEEDS FIX |
| `CHANGELOG.md` line 21 | `v2.1 (SDK Hardening...)` | `v2.0 (SDK Hardening...)` | ❌ NEEDS FIX |
| `pyproject.toml` line 3 | `version = "1.0.0"` | `version = "2.0.0"` | ❌ NEEDS FIX |
| `agents/debugger/agent.json` line 3 | `"version": "2.1"` | `"version": "2.0"` | ❌ NEEDS FIX |
| `SDK_HARDENING_V2.1_COMPLETE.md` title | `V2.1` | `V2.0` | ❌ NEEDS FIX |

## Already Correct (No Change Needed)

| Location | Value | Notes |
|---|---|---|
| `MANIFEST.yaml` layer versions | v1.3, v1.4, v1.1, v1.0, v0 | These are data layer versions, not system version |
| `core/palette-core.md` | `v1.0` | This is the Tier 1 governance doc version, not system version |
| `sdk/agent_base.py` schema versions | `handoffpacket.v2`, `handoffresult.v1` | These are wire protocol versions, independent of system version |
| Other agent.json files | `"1.0"` or `"0.1"` | These are individual agent versions, not system version |
| `sdk/README.md` | References schema versions only | Correct |

---

## Codex Roadmap Assessment

Now for the substance of your question — is the Codex roadmap adding pieces just to add pieces?

### What's necessary (agree with both Codex and Claude):

**Finding #2 (SDK export fix)** — Already done. Correct call. The documented import path should work.

**Finding #1 (Wire contract alignment)** — This is real and important. The Python SDK uses `from_agent`/`outputs`/`gaps` while the Go orchestrator expects `from`/`output`/`blockers`. Codex is right that this is the architectural center. Claude is right that it should be the first V2.2 milestone. **This is necessary.**

**Finding #3 (Golden-path health checks)** — Codex is right that the health check validates internals but not the adoption path. Adding 3-4 smoke checks that test the actual SDK import + instantiation + round-trip is high-value, low-effort. **This is necessary.**

### What's useful but can wait:

**Finding #4 (Discovery surfaces / system_summary)** — Nice to have. The SDK already exposes `query_pis()` and `query_graph()`. Adding `system_summary()` and loader diagnostics would help debugging but isn't blocking anything. Codex's rename to "SDK observability and discovery" is better language. **Useful, not urgent.**

**Finding #5 (Agent template)** — Codex is right that this belongs after the contract is stable. A template built against the current Python SDK shape would need rewriting after wire contract alignment. **Defer to V2.3.**

### What's polish:

**Finding #6 (GraphQuery optimization)** — The `query()` method works correctly. The optimization is real but the graph is 1,806 quads — performance is not a bottleneck. **Polish.**

**Finding #7 (Health output prioritization)** — "New since last run" tracking would be nice but adds state management complexity. **Polish.**

### My assessment:

Codex's roadmap is **sound and not over-engineered**. The ordering is right. The only thing I'd push back on is: don't do #4 and #5 in V2.2. Do #1 and #3 in V2.2, then #4 and #5 in V2.3. That keeps V2.2 focused on the one thing that matters: **one canonical wire contract, verified by the health check.**

The Codex rename suggestions ("SDK observability and discovery" and "reference agent authoring path") are better product language. Use them.

---

## Summary

- 8 version references need updating from 2.1 → 2.0
- pyproject.toml needs updating from 1.0.0 → 2.0.0
- Codex roadmap is necessary, not bloated
- Wire contract alignment is the real V2.2 milestone
- Everything else follows from that
