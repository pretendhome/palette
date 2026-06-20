# Palette V2.1 — Kiro Stress Test Audit

**Date**: 2026-03-16
**Auditor**: Kiro
**Scope**: SDK hardening (V2.1), health check, data integrity, MANIFEST accuracy
**Baseline**: Claude Code's SDK_HARDENING_V2.1_COMPLETE.md — "all validation passed"
**Method**: 5 stress test rounds, each targeting a different layer

---

## Executive Summary

Claude Code did excellent work. The SDK architecture is sound, the test suite is thorough for the happy path, and the health check improvements are real. But I found **12 issues** across 4 categories that should be addressed before the V2 push. None are blockers — but 3 are high-severity (data integrity) and the rest are medium (robustness) or low (cosmetic).

**Score: 56/59 health check is accurate. The SDK is solid. But it has blind spots.**

---

## ROUND 1: SDK Edge Cases (Robustness)

These are inputs that a real agent in production could encounter.

### FINDING 1: `read_packet()` crashes on malformed JSON
**Severity**: HIGH
**File**: `sdk/agent_base.py`, line ~140
**Issue**: `read_packet()` calls `json.loads(raw)` with no try/except. If an upstream agent emits malformed output (truncated JSON, encoding error, binary data), the downstream agent crashes with an unhandled `JSONDecodeError`.
**Impact**: In a multi-agent pipeline, one bad agent kills the chain.
**Fix**: Wrap `json.loads()` in try/except, return empty `HandoffPacket()` on failure, log to stderr.
**Effort**: 3 lines.

### FINDING 2: `emit_result()` crashes on non-serializable outputs
**Severity**: MEDIUM
**File**: `sdk/agent_base.py`, line ~150
**Issue**: If an agent puts a non-JSON-serializable object in `HandoffResult.outputs` (a function, a datetime, a custom class), `json.dump(asdict(result))` raises `TypeError` and the agent crashes with no output at all.
**Impact**: Silent failure — no result emitted, no error in stdout.
**Fix**: Wrap `json.dump()` in try/except, emit a failure result with the serialization error as a gap.
**Effort**: 5 lines.

### FINDING 3: `HandoffPacket` accepts None for list fields
**Severity**: LOW
**File**: `sdk/agent_base.py`, dataclass definition
**Issue**: `HandoffPacket(riu_ids=None)` sets `riu_ids=None` instead of `[]`. Any downstream code doing `len(packet.riu_ids)` or `for r in packet.riu_ids` crashes.
**Impact**: Defensive coding burden on every consumer.
**Fix**: Add `__post_init__` that coerces None to empty list for list fields. Or document that None is not a valid value.
**Effort**: 5 lines.

### FINDING 4: No type validation on packet deserialization
**Severity**: LOW
**File**: `sdk/agent_base.py`, `read_packet()`
**Issue**: `HandoffPacket(from_agent=123, task=['not', 'a', 'string'])` succeeds silently. Integer and list values are accepted where strings are expected.
**Impact**: Subtle bugs downstream when string methods are called on non-string values.
**Fix**: Not urgent — Python's duck typing handles most cases. But worth noting for future schema validation.

---

## ROUND 2: Data Integrity Cross-Checks

### FINDING 5: 3 agents missing from relationship graph
**Severity**: MEDIUM
**File**: `RELATIONSHIP_GRAPH.yaml`
**Issue**: MANIFEST declares 11 agents. The relationship graph only has 8 with `handles_riu` relationships. Missing: `resolver`, `business-plan-creation`, `health`.
**Impact**: `agent.query_graph(subject="Resolver")` returns nothing. Any agent using the graph to discover what the resolver handles gets an empty result.
**Why it matters**: The graph is supposed to be the "how it all connects" layer (Stage 5). If 3 agents aren't in it, the graph is incomplete.
**Fix**: Add relationship entries for resolver, business-plan-creation, and health agents.
**Effort**: ~30 min.

### FINDING 6: IntegrityGate only checks `outputs` field
**Severity**: MEDIUM
**File**: `sdk/integrity_gate.py`
**Issue**: The gate checks RIU/LIB/service references in `result.outputs` but NOT in `result.artifacts` or `result.gaps`. A result with `artifacts=["See RIU-999"]` passes validation even though RIU-999 doesn't exist.
**Impact**: Fabricated references in artifacts and gaps go undetected.
**Fix**: Extend `_check_riu_references` and `_check_knowledge_references` to also scan `artifacts` and `gaps` fields.
**Effort**: ~10 lines.

### FINDING 7: `self_check()` doesn't verify `recipes` or `signals` layers
**Severity**: LOW
**File**: `sdk/agent_base.py`, `self_check()`
**Issue**: PIS data has 5 layers: `classification`, `knowledge`, `routing`, `recipes`, `signals`. The self_check only verifies 3 of them. If recipes or signals fail to load, the agent reports "healthy."
**Impact**: Degraded data in unchecked layers goes undetected.
**Fix**: Add checks for `recipes` and `signals` in `self_check()`.
**Effort**: 4 lines.

---

## ROUND 3: Knowledge Library Count Discrepancy

### FINDING 8: 27 knowledge entries lost during PIS loading
**Severity**: HIGH
**File**: `scripts/palette_intelligence_system/loader.py` + `knowledge-library/v1.4/`
**Issue**: The YAML file has 163 top-level entries. The MANIFEST declares 163. The health check counts 163 (via grep). But the PIS loader returns a dict with only 136 keys. **27 entries are silently dropped during loading.**
**Impact**: Agents querying the knowledge library through the SDK see 136 entries, not 163. Any query for a dropped entry returns nothing. The health check says "163 — PASS" while the SDK sees 136.
**Root cause**: Likely duplicate keys in the YAML (two entries with the same `lib_id`), or entries without a `lib_id` that get dropped during dict conversion.
**Fix**: Audit the knowledge library YAML for duplicate or missing `lib_id` values. Fix the loader to warn on duplicates.
**Effort**: ~1 hour to diagnose, ~30 min to fix.

---

## ROUND 4: MANIFEST Accuracy

### FINDING 9: MANIFEST "Updated" date is stale
**Severity**: LOW
**File**: `MANIFEST.yaml`, line 2
**Issue**: Says `# Updated: 2026-03-15` but V2.1 work was done on 2026-03-16.
**Fix**: Update to 2026-03-16.
**Effort**: 1 line.

### FINDING 10: Taxonomy not exposed as a PIS data layer
**Severity**: LOW (informational)
**File**: `scripts/palette_intelligence_system/loader.py`
**Issue**: The PIS loader returns `classification` (117 RIUs) but not `taxonomy` as a separate attribute. The SDK's `self_check()` doesn't check for taxonomy because it doesn't exist as a data layer. The taxonomy YAML exists on disk but is only accessible through classification.
**Impact**: No direct SDK access to taxonomy metadata (names, descriptions, workstreams) — only to classification data (internal/external/both).
**Fix**: Not necessarily a bug — classification may be the intended abstraction. But worth documenting.

---

## ROUND 5: Structural Observations

### FINDING 11: Schema version mismatch between Packet and Result
**Severity**: LOW
**File**: `sdk/agent_base.py`
**Issue**: `HandoffPacket.schema_version = "handoffpacket.v2"` but `HandoffResult.schema_version = "handoffresult.v1"`. No validation that versions are compatible.
**Impact**: If schemas evolve independently, there's no mechanism to detect incompatible packet/result pairs.
**Fix**: Not urgent. Document the versioning strategy.

### FINDING 12: `SDK_HARDENING_V2.1_COMPLETE.md` contains personal names
**Severity**: LOW
**File**: `SDK_HARDENING_V2.1_COMPLETE.md`
**Issue**: The health check correctly flags this file for containing personal names. This is the only remaining cleanliness failure.
**Fix**: Either exclude this file from the name scan (it's a session artifact, not operational code) or anonymize the names in it.
**Effort**: 1 line in health check exclusions, or 2 minutes of find-replace.

---

## Summary Table

| # | Finding | Severity | Category | Effort |
|---|---------|----------|----------|--------|
| 1 | read_packet() crashes on malformed JSON | HIGH | Robustness | 3 lines |
| 2 | emit_result() crashes on non-serializable outputs | MEDIUM | Robustness | 5 lines |
| 3 | HandoffPacket accepts None for list fields | LOW | Robustness | 5 lines |
| 4 | No type validation on packet deserialization | LOW | Robustness | Document |
| 5 | 3 agents missing from relationship graph | MEDIUM | Data Integrity | 30 min |
| 6 | IntegrityGate only checks outputs field | MEDIUM | Data Integrity | 10 lines |
| 7 | self_check() misses recipes and signals layers | LOW | Data Integrity | 4 lines |
| 8 | 27 knowledge entries lost during PIS loading | HIGH | Data Integrity | 1.5 hours |
| 9 | MANIFEST updated date stale | LOW | Cosmetic | 1 line |
| 10 | Taxonomy not exposed as PIS data layer | LOW | Informational | Document |
| 11 | Schema version mismatch Packet vs Result | LOW | Informational | Document |
| 12 | SDK_HARDENING file has personal names | LOW | Cleanliness | 1 line |

---

## Fixes Applied in This Session

| Finding | Fix | Verified |
|---|---|---|
| 1 (read_packet crash) | Added try/except around json.loads, returns empty packet + stderr log | ✅ Malformed JSON returns empty packet |
| 2 (emit_result crash) | Added `default=str` for graceful degradation + try/except fallback | ✅ Lambda serialized as string repr |
| 6 (IntegrityGate scope) | Extended RIU and LIB checks to scan artifacts and gaps fields | ✅ RIU-999 in artifacts and LIB-998 in gaps both caught |
| 9 (MANIFEST date) | Updated to 2026-03-16 | ✅ |

**All 58 SDK tests pass. All 21 coordination tests pass. All 33 query engine tests pass. Health check 56/59 (unchanged).**

---

## Recommended Fix Order

**Before V2 push (high-severity + quick wins):**
1. Finding 1: read_packet() crash protection (3 lines, HIGH)
2. Finding 8: Diagnose knowledge library 163→136 drop (HIGH, needs investigation)
3. Finding 2: emit_result() crash protection (5 lines, MEDIUM)
4. Finding 6: IntegrityGate scan artifacts+gaps (10 lines, MEDIUM)
5. Finding 9: MANIFEST date (1 line)
6. Finding 12: Name scan exclusion (1 line)

**After V2 push (improvements):**
7. Finding 5: Add 3 missing agents to graph (30 min)
8. Finding 7: self_check() for recipes+signals (4 lines)
9. Finding 3: None coercion for list fields (5 lines)

**Document only:**
10. Finding 4, 10, 11

---

## What Claude Code Got Right

To be clear — the V2.1 work is genuinely good:

- The 7-stage machine enablement mapping is elegant and well-documented
- The degraded-context pattern (load fails → returns degraded, doesn't crash) is exactly right
- The IntegrityGate concept (glass-box warnings, not gatekeeping) is architecturally sound
- 58 tests in 1.9s with real PIS integration tests is solid coverage
- The health check fixes (startswith, word-boundary regex, dynamic patterns) are all correct
- The researcher SDK adoption preserves backward compatibility perfectly

The issues I found are in the gaps between what was tested and what production will encounter. That's normal — and that's what stress testing is for.

---

**Auditor**: Kiro
**Method**: 5 rounds of automated stress testing + manual code review
**Time**: ~45 minutes
**Tests run**: SDK (58), Coordination (21), Query Engine (33), Health Check, + 5 custom stress test scripts
