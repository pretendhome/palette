# Palette V2.0 — Reflection (Post-Audit)

**Date**: 2026-03-16
**Health check**: 57/58 | SDK tests: 60/60 | Coordination: 21/21
**Audits completed**: Kiro stress test (12 findings), Codex creative improvement (7 findings), Kiro version sweep
**Context**: This is the second reflection this session. The first was pre-audit (in SDK_HARDENING_V2.1_COMPLETE.md). This one incorporates what three different AI tools found when they stress-tested the work.

---

## What the System Learned Since the Last Reflection

The first reflection identified 5 improvements. Here's what happened:

| # | Previous Improvement | Status |
|---|---------------------|--------|
| 1. Derive counts from files, not declarations | **Open** — still valid, still the right fix for count-drift |
| 2. SDK adoption visibility in health check | **Open** — Codex reframed this as "golden-path health checks" (V2.2 item 2) |
| 3. Fix terminology drift | **Open** — still 57/58, still the same 3 clusters (Canva AI, NotebookLM, Runway) |
| 4. Make health agent an SDK agent | **Open** — Codex identified this as "reference agent authoring path" (V2.3 item 4) |
| 5. Validate IntegrityGate against real failures | **Partially addressed** — Kiro found that IntegrityGate wasn't checking artifacts/gaps (fixed), but real-world validation still needed |

**Key observation**: None of the 5 improvements were wrong. But the audits revealed something the first reflection missed entirely: **the wire contract divergence between Go and Python is the highest-priority architectural issue**, and it wasn't on the list.

---

## What Three AI Tools Found That One Didn't

| Tool | Approach | Strongest Finding |
|------|----------|-------------------|
| **Claude** (builder) | Implemented the 8-iteration plan, wrote SDK, tests, health agent | Built the system but didn't stress-test the cross-runtime boundary |
| **Kiro** (stress tester) | 5 rounds of adversarial testing + manual code review | 27 knowledge entries silently dropped during loading (Finding 8) — invisible to every other check |
| **Codex** (product thinker) | "What makes this feel internal vs productized?" | Wire contract divergence is the architectural center; everything else depends on it |

The pattern: **builders optimize for the path they're building. Stress testers find the gaps between paths. Product thinkers find the gaps between the system and its users.** All three perspectives were necessary. No single tool caught everything.

---

## The Wire Contract: Why It's the #1 Improvement

The Explore agent's research confirmed exactly what Codex suspected, but worse:

**Current field name divergences** (Python SDK vs Go/JSON Schema):

| Purpose | Go/Schema | Python SDK |
|---------|-----------|------------|
| Sender | `from` | `from_agent` |
| Receiver | `to` | `to_agent` |
| Agent data | `payload` | `context` |
| Output | `output` | `outputs` |
| Files | `produced_artifacts` | `artifacts` |
| Blockers | `blockers` | `gaps` |

**Why this is dangerous**: The Go orchestrator's `tryParseResult()` checks for `packet_id != ""` to decide if parsing succeeded. A Python SDK result will have `packet_id` set (field name matches), so the orchestrator *accepts* the result — but `from`, `output`, `produced_artifacts`, and `blockers` all deserialize to zero values because the Python names don't match. **The orchestrator silently loses all semantic content while appearing to succeed.**

The Resolver works around this by hand-crafting Go-compatible JSON instead of using the SDK. That means the SDK's first real adopter (Researcher) would be the first agent to hit this silent failure in a real orchestrated pipeline.

**Why this matters for the future**: Codex is right that a unified wire contract is the prerequisite for exposing the protocol as an MCP server or API. If the packet/result schema is the canonical interface, it needs to be one thing — not two things that look similar but silently diverge. An MCP server would formalize the schema as tool definitions. An API would expose it as endpoints. Both require one contract, not two.

---

## 5 Improvements for V2.2 (Updated)

### 1. Unify the wire contract (Go/Python/Schema)

**The single most important change.** Choose `core/schema/*.json` as canonical. Make the Python SDK conform. Add a compatibility shim so the Researcher doesn't break.

- **Files**: `sdk/agent_base.py` (HandoffPacket + HandoffResult field names), `core/schema/*.json` (verify as source of truth), `agents/researcher/researcher.py` (update to new names)
- **Approach**: Python dataclass fields keep Pythonic names internally, but `emit_result()` serializes to Go-canonical JSON keys (using a custom `to_wire()` method or `__json__` override). `read_packet()` deserializes from Go-canonical keys.
- **Effort**: 1-2 days
- **Impact**: Unlocks MCP/API exposure. Fixes silent data loss in orchestrated pipelines. Makes "one governed protocol" real instead of aspirational.

### 2. Golden-path health checks (blocked on #1)

After the wire contract is stable, add smoke checks that test the actual adoption path:
- Documented SDK import works
- Minimal AgentBase subclass can instantiate and run
- A packet can round-trip through Python SDK and produce Go-parseable JSON
- `self_check()` catches any degraded layer the README claims is available

- **File**: `agents/health/health_check.py`
- **Effort**: 0.5 day
- **Impact**: Closes the gap between "healthy internals" and "healthy adoption experience"

### 3. Fix terminology drift (57/58 → 58/58)

Still the same 3 high-severity clusters from the last reflection. Create `service_names.yaml` as canonical registry.

- **Files**: new `service_names.yaml`, health check Section 5
- **Effort**: 2 hours
- **Impact**: Brings health check to 58/58. Small but visible.

### 4. SDK observability and discovery

Expose what the system knows about itself:
- `system_summary()` method on PaletteContext — layer counts, graph counts, degraded flags, load duration
- Loader diagnostics — duplicate ID warnings, dropped entry warnings
- Direct taxonomy access (currently only reachable through classification)

- **Files**: `scripts/palette_intelligence_system/loader.py`, `sdk/agent_base.py`
- **Effort**: 0.5-1 day
- **Impact**: Makes Stage 1 ("Here's what exists") materially more real

### 5. Reference agent authoring path (blocked on #1, #2)

After contract and health checks are stable:
- `sdk/templates/minimal_agent.py` — one canonical "right way" to build an agent
- `sdk/templates/test_minimal_agent.py` — one test template
- Health sub-check that detects SDK adoption per agent

- **Files**: new `sdk/templates/`, `agents/health/health_check.py`
- **Effort**: 0.5 day
- **Impact**: Shift from framework to platform. The difference between "read the code" and "follow the path."

---

## Architectural Patterns Observed

### Pattern: Multi-tool audit surfaces different failure classes

Single-tool development creates blind spots in the builder's own assumptions. The three-tool audit pattern (build → stress test → product review) caught issues at three different altitudes:
- **Implementation bugs** (Kiro): crashes, missing data, count mismatches
- **Interface coherence** (Codex): the gap between what's built and what adopters experience
- **Operational trust** (Claude/Kiro overlap): the gap between what's tested and what production encounters

This pattern should be repeated at each version boundary.

### Anti-pattern: "Works in isolation" ≠ "Works in composition"

The Python SDK passes all 60 tests. The Go orchestrator passes its tests. But they don't actually speak the same language. The integration boundary — where one system's output becomes another's input — was the least tested surface. This is the classic multi-service composition failure.

### Pattern: Wire contract as platform primitive

Codex's observation that the wire contract could become an MCP server or API reframes the protocol from "internal plumbing" to "platform surface." If HandoffPacket/HandoffResult are the interface that external tools call, then the schema isn't just a serialization format — it's the product. This changes the priority calculus: contract stability becomes a prerequisite for everything else.

---

## The Short Version

The system learned that **building the SDK and proving the SDK works are different problems, solved by different tools.** Claude built it. Kiro broke it. Codex asked whether anyone else could use it. The wire contract is the dependency that determines whether V2.0's "machine enablement" claim is real or internal-only.

V2.2 starts with one question: **one protocol or two?** The answer is one. Everything else follows.
