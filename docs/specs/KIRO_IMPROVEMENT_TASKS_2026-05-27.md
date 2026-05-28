# Kiro — Safe Improvement Tasks
**Date**: 2026-05-27
**From**: claude.analysis
**Priority**: Work through in order. All are additive — no refactors, no renames, no moving files.
**Rule**: 129/129 tests must still pass after each change. Run `uv run pytest -q scripts/palette_intents/tests/ scripts/palette_intelligence_system/test_*.py` after each.

---

## Task 1: Wire `validate_artifact()` into the 3 demo-critical intents

**What**: The schema validation exists (`schemas.py`) but no intent actually calls it. The artifacts get stored without validation.

**Where**: `protect.py`, `research.py`, `decide.py` — after building the artifact dict, before `store_artifact()`.

**How**:
```python
from scripts.palette_intents.schemas import validate_artifact

# After building gate_decision/evidence_brief/decision_record dict:
schema_errors = validate_artifact(gate_decision)
if schema_errors:
    emit_integrity_signal(intent="PROTECT", riu_id=riu_id, success=False,
                          details=f"schema validation: {'; '.join(schema_errors)}")
```

**Why safe**: Validation is read-only — it checks the dict, doesn't modify it. If validation fails, we log it but still store the artifact. No behavior change for the user.

**Estimate**: 30 min across 3 files.

---

## Task 2: Wire `palette_checkpoint()` into CREATE, DIAGNOSE, REFLECT

**What**: Only RESEARCH calls `palette_checkpoint()` today. The other 3 intents import it but never call it.

**Where**: `create.py`, `diagnose.py`, `reflect.py` — after building IntentState and integrity card, before the main logic.

**How**: Same pattern as research.py line 170-174:
```python
checked = palette_checkpoint(state)
if checked.intent != "CREATE":
    if not show_json:
        print(f"  {YELLOW}[CHECKPOINT]{RESET} Transition suggested: → {checked.intent}")
```

**Why safe**: Checkpoint only returns a different state if posture is `blocked_by_boundary` or `governance_required`. For normal queries it returns the same state unchanged. No behavior change unless the integrity card flags something.

**Estimate**: 20 min across 3 files.

---

## Task 3: Wire PIS summary line into CREATE, DIAGNOSE, REFLECT display

**What**: PROTECT, RESEARCH, DECIDE show `[PIS] 131 RIUs traversed → N nodes matched`. The other 3 don't.

**Where**: `create.py`, `diagnose.py`, `reflect.py` — in the display section, after the `[RESOLVE]` line.

**How**: Same pattern as protect.py:
```python
from scripts.palette_intents.infra import pis_summary, format_pis_line

# After riu_id is set:
if riu_id:
    pis = pis_summary(riu_id, len(knowledge_entries), classification)
    print(f"  {CYAN}[PIS]{RESET}     {format_pis_line(pis)}")
```

**Why safe**: Display-only. No logic change. If riu_id is None, the line doesn't show.

**Estimate**: 15 min across 3 files.

---

## Task 4: Add `--matter` linkage to demo path convenience command

**What**: The demo runs 3 separate commands. There's no way to chain them with a shared `matter_id` except manually passing `--matter` each time.

**Where**: New file: `scripts/palette_intents/demo.py` (or add to `palette_intent.py`)

**How**: Add a `palette demo sarah` command that runs:
```python
gate, state1 = run_protect("What's our exposure if the majority member was self-dealing?", matter_id="sarah-llc-001")
brief, state2 = run_research("What fiduciary duty standards apply to LLC co-founders in Delaware?", matter_id="sarah-llc-001")
record, state3 = run_decide("Given what we found, what would opposing counsel argue?", matter_id="sarah-llc-001")
```

**Why safe**: New file, new command. Doesn't touch existing intents. Calls existing `run_protect/run_research/run_decide` functions.

**Estimate**: 1 hour (includes display formatting between steps).

---

## Task 5: Emit `recipe_failure` integrity signal in DECIDE when Ollama is down

**What**: RESEARCH tracks Perplexity failures via `record_recipe_failure("perplexity")`. DECIDE uses Ollama but doesn't track failures — if Ollama is down, it prints a warning but doesn't update the integrity cache.

**Where**: `decide.py` — after `call_ollama()` returns None.

**How**:
```python
recommendation = call_ollama(recommendation_prompt, ...)
if not recommendation:
    record_recipe_failure("ollama")
    # ... existing fallback handling
```

Same for the counterargument call.

**Why safe**: `record_recipe_failure` is already imported in research.py and tested. Just needs the same call in decide.py. No behavior change — it logs to the cache, which the health check already reads.

**Estimate**: 10 min.

---

## Task 6: Add `matter_id` to REFLECT session sweep (Gemini's polish item #3)

**What**: REFLECT already filters by `matter_id` when provided. But the artifact frontmatter for EvidenceBrief and DecisionRecord doesn't always have `matter_id` set unless the user passes `--matter`. The demo script (Task 4) would fix this for the Sarah scenario.

**Where**: No code change needed IF Task 4 is done (all demo artifacts get `matter_id: sarah-llc-001`). This is a verification task.

**How**: After running `palette demo sarah`, run `palette reflect --matter sarah-llc-001 "What did Sarah's morning teach us?"` and verify it sweeps all 3 artifacts.

**Why safe**: Read-only verification. No code change.

**Estimate**: 10 min.

---

## Task 7: Add firewall activation to `palette_orchestrate.py`

**What**: The firewall activates in `palette_intent.py` but NOT in `palette_orchestrate.py` (the multi-model orchestration script). If someone uses `palette orchestrate` directly, the firewall is bypassed.

**Where**: `scripts/palette_orchestrate.py` — at the top of `main()`.

**How**: Same 4-line block as `palette_intent.py`:
```python
try:
    from bdb.gateway.socket_firewall import activate_firewall
    activate_firewall()
except Exception:
    pass
```

**Why safe**: Firewall is idempotent — calling `activate_firewall()` twice is a no-op. Doesn't change any orchestration logic.

**Estimate**: 5 min.

---

## Task 8: Add PROTECT → RESEARCH transition hint in output

**What**: When PROTECT returns `action: ALLOW`, the output says "Query safe for governed external research" but doesn't show the next command. When it returns `action: BLOCK` with a `safe_rewrite`, it shows the rewrite but not the command.

**Where**: `protect.py` — in the display section.

**How**: After the ALLOW block:
```python
print(f"  {DIM}  Next: palette research \"{query}\"{RESET}")
```

After the BLOCK + safe_rewrite block:
```python
print(f"  {DIM}  Next: palette research \"{safe_rewrite}\"{RESET}")
```

**Why safe**: Display-only. No logic change.

**Estimate**: 10 min.

---

## What I Explicitly Did NOT Include

- **Context firewall** (purge high-tier artifacts on boundary downgrade): Real engineering, needs design. Risk of breaking compounding if done wrong.
- **Full PIS load** instead of fast-path: 568ms penalty. Not worth it before June 2.
- **Recipe adapter layer** (Gemini's fix #4): Requires defining adapter interface. Post-BDB.
- **Transition matrix execution** (actually auto-transitioning between intents): The checkpoint detects when transition should happen but doesn't execute it. Making it auto-transition risks infinite loops without the semaphore system. Post-BDB.
- **Renaming or moving files**: Zero refactors. Everything is additive.

---

## Total Estimate

Tasks 1-8: ~3 hours. All additive. All pass existing tests.

*— claude.analysis, 2026-05-27*
