# Remediation Loop — Architecture Spec

**Author**: kiro.design (Architect mode)
**Date**: 2026-04-23
**Status**: PROPOSED
**Scope**: Unify validator, debugger, builder v2 agents into a working remediation loop

---

## Problem

Three agents exist. All pass their own tests. None can talk to each other. The routing identities are wrong, the infrastructure is duplicated 3x, and there's no integration test proving the loop works end-to-end.

## Goal

A working remediation loop: Validator detects failure → Debugger diagnoses → Builder fixes → Validator verifies. Smallest possible code. Nothing we don't need.

## Design Principles

1. **One shared bus client** — not three copies of urllib boilerplate
2. **Identity registry** — one place that maps agent names to bus identities
3. **Each agent does one thing** — validate, diagnose, or build. No overlap.
4. **Integration test proves the wire** — not just unit tests per agent

---

## Architecture

### File: `agents/remediation/bus_client.py` (~60 lines)

Shared infrastructure. Every agent imports this instead of reimplementing urllib/json/register/send/fetch/buffer.

```python
# The only file that knows about BROKER_BASE, urllib, JSON envelopes
BROKER_BASE = "http://127.0.0.1:7899"

# Identity registry — THE source of truth for routing
AGENTS = {
    "validator": "validator.engine",
    "debugger":  "debugger.engine",
    "builder":   "builder.engine",
    "human":     "human.operator",
}

def register(identity, capabilities, role): ...
def send(from_id, to_id, message_type, intent, payload, risk="none", thread_id=None, in_reply_to=None): ...
def fetch(identity): ...
def peek(identity): ...
def health(): ...
```

Every agent calls `bus_client.send(AGENTS["debugger"], ...)` instead of hardcoding `"codex.implementation"`. The routing bug becomes impossible because the identity map is in one place.

### File: `agents/remediation/evidence.py` (~30 lines)

Shared evidence packet creation. Both validator and debugger create evidence — same format, same directory.

```python
EVIDENCE_DIR = palette_root / "artifacts" / "validation"

def create(task, error, input_payload=None) -> Path: ...
def read(path) -> dict: ...
def is_sound(path) -> tuple[bool, str]: ...
```

### File: `agents/remediation/circuit_breaker.py` (~25 lines)

Shared circuit breaker. All three agents have the same pattern: count attempts per task, escalate after N.

```python
def check(task_id, counts, limit=3) -> bool: ...  # True = tripped
def reset(task_id, counts): ...
```

### Agents (stripped to core logic only)

Each agent imports from the shared modules and contains ONLY its domain logic:

| Agent | File | Core logic | Estimated lines |
|-------|------|-----------|----------------|
| Validator | `validator_v2.py` | Schema validation, stress testing, taxonomy checks, auto_remediate routing | ~400 (down from 877) |
| Debugger | `debugger_v2.py` | Failure classification, root cause diagnosis, fix proposal generation | ~400 (down from 944) |
| Builder | `builder_v2.py` | Spec validation, patch application, drift detection, verification test generation | ~200 (down from 363) |

Total system: ~1,100 lines (down from 2,184) + ~115 shared infrastructure.

### File: `agents/remediation/test_loop.py` (~80 lines)

THE integration test. Proves the wire works end-to-end:

```
1. Create a test Python file with a known bug (e.g., undefined variable)
2. Validator validates it → detects failure → sends to debugger.engine
3. Verify message arrives at debugger.engine (peek the bus)
4. Debugger consumes evidence → diagnoses → proposes fix → sends to builder.engine
5. Verify message arrives at builder.engine (peek the bus)
6. Builder applies patch → generates verification test → sends to validator.engine
7. Verify message arrives at validator.engine (peek the bus)
8. Validator runs verification test → PASS
9. Verify the test file is now fixed on disk
10. Clean up
```

If this test passes, the loop is closed. If any step fails, we know exactly which wire is broken.

---

## Routing Map (canonical)

```
Validator ──failure──→ Debugger ──fix proposal──→ Builder ──verify──→ Validator
    │                      │                          │
    │ (circuit breaker)    │ (high blast radius)      │ (architecture decision)
    ↓                      ↓                          ↓
human.operator         human.operator              architect (future)
```

Normal flow: `validator.engine` → `debugger.engine` → `builder.engine` → `validator.engine`
Escalation: any agent → `human.operator` (circuit breaker, high risk, or high blast radius)

---

## What Changes in Each Agent

### Validator
- Import `bus_client`, `evidence`, `circuit_breaker` instead of reimplementing
- Change `auto_remediate()` default target from `"codex.implementation"` to `AGENTS["debugger"]`
- Remove ~200 lines of duplicated infrastructure

### Debugger
- Import shared modules
- Change `target_agent = "codex.implementation"` to `bus_client.AGENTS["builder"]`
- Remove ~200 lines of duplicated infrastructure

### Builder
- Import shared modules
- Already routes to `validator.engine` correctly — no routing change needed
- Fix: ast.parse() before writing to disk (the write-before-verify bug)
- Fix: verification test must actually verify (not `return True`)

---

## What We Do NOT Change

- Agent domain logic (validation checks, diagnosis algorithms, patch application)
- Test suites (all existing tests continue to pass)
- Bus protocol (wire contract, envelope format, broker API)
- Agent identities (validator.engine, debugger.engine, builder.engine)

---

## Execution Plan

### Phase 1: Shared infrastructure (30 min)
Create `agents/remediation/` with `bus_client.py`, `evidence.py`, `circuit_breaker.py`.

### Phase 2: Rewire agents (45 min)
Replace duplicated infrastructure in each agent with imports from shared modules. Fix the 2 routing bugs. Fix builder's write-before-verify and empty verification test.

### Phase 3: Integration test (30 min)
Write and run `test_loop.py`. This is the proof.

### Phase 4: Verify all existing tests still pass (15 min)
Run all three test suites. Zero regressions.

---

## Success Criteria

1. `test_loop.py` passes end-to-end (the loop actually works)
2. All three existing test suites pass (zero regressions)
3. Total system is under 1,300 lines (down from 2,184 + 1,045 tests)
4. Zero hardcoded agent identities outside `bus_client.AGENTS`
5. Zero duplicated urllib/json/register/send code

---

## Decision Classification

🔄 TWO-WAY DOOR — all v2 files stay on disk. The refactored versions are new files that import from shared modules. If anything breaks, revert to the originals.
