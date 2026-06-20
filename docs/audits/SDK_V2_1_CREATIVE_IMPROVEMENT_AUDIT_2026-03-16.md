# Palette SDK V2.1 — Creative Improvement Audit

**Date**: 2026-03-16
**Auditor**: Codex
**Scope**: Improvement opportunities beyond Kiro's stress-test fixes
**Baseline**:
- `KIRO_V2_STRESS_TEST_AUDIT_2026-03-16.md`
- Current V2.1 SDK, health agent, orchestrator, and enablement docs
- Health check run on 2026-03-16: `57/58` passing, `1` warning (`3` high-severity drift clusters)

---

## Executive Summary

V2.1 is no longer fragile. The SDK loads, the health agent runs, the tests are real, and the degraded-state pattern is correct.

The next set of improvements should not be framed as "is it broken?" They should be framed as:

**What still makes this feel like an internal framework instead of a productized machine interface?**

My answer: there are five high-leverage improvements.

1. The SDK and the orchestrator need a **single canonical wire contract** again.
2. The SDK's **public surface and quick-start path** need to be executable exactly as documented.
3. The health agent should validate the **golden path**, not just module loadability.
4. The SDK should expose **Stage 1 / Stage 5 discovery data** more directly, not only traversal.
5. Agent adoption needs a **reference path**: one minimal template, one smoke test, one "best possible first agent."

This is not a redesign memo. These are the smallest changes that would most improve adoption, trust, and system coherence.

---

## What Improved Since Kiro's Audit

Kiro's pass was about correctness and resilience. The current system now has:

- graceful degradation on PIS load failure
- defensive output validation
- passing SDK tests
- a working health agent
- materially cleaner operational code

That means the next delta is different:

- less about crash protection
- more about interface coherence
- more about developer experience
- more about proving the system the way a new adopter would actually encounter it

---

## Priority Improvements

## 1. Re-unify the Python SDK and Go Orchestrator wire contract

**Why this matters**

This is the biggest remaining architectural gap.

The repository still claims that Go agents and Python agents speak the same protocol, but today they do not.

**Evidence**

- Go canonical packet/result:
  - `core/packet.go`
  - `core/schema/packet.schema.json`
  - `core/schema/result.schema.json`
- Python SDK packet/result:
  - `sdk/agent_base.py`
- Python SDK-integrated researcher:
  - `agents/researcher/researcher.py`
- Orchestrator parse behavior:
  - `agents/orchestrator/runner.go`

**Current mismatch**

Go packet/result expects fields like:

- packet: `id`, `trace_id`, `from`, `to`, `payload`, `timestamp`
- result: `packet_id`, `from`, `status`, `output`, `produced_artifacts`, `blockers`

Python SDK packet/result currently uses:

- packet: `from_agent`, `to_agent`, `context`
- result: `from_agent`, `status=success|failure|blocked`, `outputs`, `artifacts`, `gaps`

The researcher agent is built against the Python SDK shape, not the Go/core shape:

- reads `packet.context`
- emits `status="success"`
- emits `outputs`, not `output`

The orchestrator currently works around this by trying to parse a Go-style `HandoffResult`, then falling back to inferred status when `packet_id` is missing:

- `agents/orchestrator/runner.go`

That means the process can appear healthy while silently losing structured semantics.

**Why this is dangerous**

- interoperability is partially illusory
- agent results can degrade into "best effort" inference
- tests can pass inside the Python SDK while cross-runtime orchestration remains soft-broken
- "machine enablement" loses its strongest claim: one governed protocol across agents

**Smallest useful fix**

Choose one canonical wire contract and make the Python SDK conform to it.

Recommended path:

1. Treat `core/schema/*.json` as canonical.
2. Make Python `HandoffPacket` / `HandoffResult` align to those field names.
3. If you need friendlier Python names, keep them as aliases or adapters, not primary wire fields.
4. Add one compatibility layer so existing Python agents do not all break at once.

**Effort**

`1-2 days`

**Impact**

Very high. This is the difference between "SDK added" and "cross-runtime protocol stabilized."

---

## 2. Fix the public SDK surface so the documented quick start actually works

**Why this matters**

The first experience of a new adopter should not fail on import.

Right now the README says:

```python
from palette.sdk import AgentBase, HandoffPacket, HandoffResult
```

But `palette/sdk/__init__.py` does not export `HandoffPacket` or `HandoffResult`.

Verified locally:

- `from palette.sdk import AgentBase, HandoffPacket, HandoffResult`
- result: `ImportError`

**Files**

- `sdk/README.md`
- `sdk/__init__.py`

**Why this matters beyond docs**

This is exactly the kind of issue that makes a system feel "almost ready" instead of ready.

It also points to a broader problem:

- the package boundary is not being treated as a product surface yet

**Smallest useful fix**

1. Export `HandoffPacket` and `HandoffResult` from `sdk/__init__.py`.
2. Add one import-smoke test for the documented README path.
3. Add one line in the health check that validates the public SDK import surface, not just module importability.

**Effort**

`15-30 minutes`

**Impact**

High for adoption, low effort.

---

## 3. Upgrade the health agent from "structural checker" to "golden-path verifier"

**Why this matters**

The health agent is now good at answering:

- do files exist?
- do counts match?
- do modules import?
- do drift scans pass?

It is much weaker at answering:

- does the SDK work the way a new agent author would actually experience it?

Today, the health check passes while the README quick-start import path fails.

That is a signal that the health model is still too infrastructure-first.

**Files**

- `agents/health/health_check.py`
- `sdk/README.md`

**Current anti-pattern**

The system checks internals more rigorously than it checks the adoption path.

**Recommended improvement**

Add a new "golden path" section or sub-checks that validate:

1. The documented SDK import path works.
2. A minimal `AgentBase` subclass can be instantiated and run.
3. A Go-orchestrator-style packet can round-trip through a Python SDK agent and still produce a parseable result.
4. `self_check()` catches any degraded layer the README claims is available.

This is especially important because V2.1 is now claiming "ready for agent adoption."

**Smallest useful fix**

Add 3-4 smoke checks to `health_check.py`, preferably using real package imports and one synthetic packet/result round-trip.

**Effort**

`0.5 day`

**Impact**

High. This closes the gap between "healthy internals" and "healthy adoption experience."

---

## 4. Expose first-class discovery data, not just traversal

**Why this matters**

The SDK is framed as the machine half of a 7-stage enablement model.

Stage 1 is "Here's what exists."
Stage 5 is "Here's how it connects."

Right now those stages are only partially surfaced:

- `query_pis()` gives traversal access
- `query_graph()` gives graph access
- but the SDK does not expose taxonomy as a first-class layer
- loader diagnostics are opaque
- collisions / dropped entries are not surfaced as metadata

Kiro already surfaced part of this around taxonomy visibility and dropped knowledge entries. Even if those specific issues are fixed, the deeper product issue remains:

**an SDK user cannot easily inspect the shape and trustworthiness of the data they are standing on.**

**Files**

- `scripts/palette_intelligence_system/loader.py`
- `sdk/agent_base.py`
- `sdk/README.md`

**Recommended improvement**

Add lightweight discovery surfaces:

- `ctx.taxonomy` or `ctx.catalog.taxonomy`
- loader diagnostics object:
  - counts by layer
  - duplicate ID warnings
  - dropped entry warnings
  - load duration
- graph summary helper surfaced from the SDK
- maybe one "catalog summary" method that returns a compact machine-readable overview

This would make the Stage 1 / Stage 5 story materially more real.

**Smallest useful fix**

1. Extend `PISData` or `PaletteContext` with a `diagnostics` field.
2. Expose taxonomy metadata directly.
3. Add one SDK method like `system_summary()` that returns layer counts + graph counts + degraded flags.

**Effort**

`0.5-1 day`

**Impact**

Medium-high. Strong improvement to trust, debugging, and agent reasoning quality.

---

## 5. Add a real agent-authoring golden path: template, reference agent, and adoption loop

**Why this matters**

The biggest remaining question after V2.1 is not "does the SDK work?"

It is:

**How quickly can another agent actually adopt it correctly?**

The changelog already hints at this: the SDK is ready for agent adoption, but agent adoption itself is still the next frontier.

**Files**

- `sdk/README.md`
- `CHANGELOG.md`
- `agents/health/health_check.py`
- current agent implementations

**What is missing**

- one minimal reference agent built the "right" way
- one scaffold or template for new SDK-native agents
- one adoption checklist
- one test harness specifically for a newly authored agent

Without this, adoption depends too much on reading code and inferring conventions.

**Recommended improvement**

Create a single best-practice path:

1. `sdk/templates/minimal_agent.py`
2. `sdk/templates/test_minimal_agent.py`
3. a short "SDK adoption checklist"
4. a health sub-check that detects whether an agent is using the canonical SDK protocol

If you want one candidate, the health agent itself is a good one:

- it already reasons about system health
- it could become a reference SDK-native agent
- dogfooding would tighten the system narrative

**Effort**

`0.5 day`

**Impact**

High for future adoption. This is the shift from framework to platform.

---

## Secondary Improvements

These are not top-5, but they are worthwhile.

### 6. Tighten `GraphQuery` from "works" to "feels sharp"

**Files**

- `sdk/graph_query.py`

**Observation**

`query()` computes a smaller candidate pool, but then filters against `self._quads` instead of the smallest pool directly.

This is not a correctness bug. It is an unfinished optimization signal.

**Improve by**

- filtering from the selected pool
- validating predicate names when requested
- adding typed helpers for common Palette relationships:
  - `services_for_riu()`
  - `knowledge_for_riu()`
  - `agents_for_riu()`

**Effort**

`1-2 hours`

---

### 7. Make the health warning more decision-oriented

**Files**

- `agents/health/health_check.py`

**Observation**

The system reports `3` high-severity drift clusters, but the output is still mostly an audit feed, not a prioritization feed.

**Improve by**

- summarizing top drift clusters in the JSON output
- flagging "new since last run" vs "known open"
- attaching likely owner or file neighborhood

This would make the health agent more action-driving.

**Effort**

`2-3 hours`

---

## Recommended Order

### First

1. Canonical wire contract alignment
2. Public SDK export / README import fix
3. Golden-path health checks

### Second

4. Discovery and diagnostics surfaces
5. Agent-authoring template and adoption loop

### Third

6. GraphQuery polish
7. Health output prioritization

---

## The Main Architectural Pattern I See

Palette V2.1 is strongest when it behaves like a governed system.

It is weaker when it behaves like a codebase that expects adopters to infer the happy path.

That is the real delta now.

The next version should optimize for:

- one protocol
- one documented import path
- one verified golden path
- one reference agent
- one set of discovery surfaces that make the system legible

If those are in place, the SDK stops being "a hardened internal layer" and starts feeling like a stable machine enablement platform.

---

## Short Version

If I had to pick only three changes:

1. **Unify the Python SDK and Go orchestrator wire contract.**
2. **Make the documented SDK path executable exactly as written.**
3. **Teach the health agent to verify the adoption path, not just the internals.**

Those three changes would close the largest gap with the smallest surface area.
