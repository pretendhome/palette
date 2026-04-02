# Stress Test Execution Plan (Rossi + Palette Core)

Date: 2026-02-27
Source: `.codex/STRESS_TESTS_PROPOSED_BY_KIRO.md`

## Scope
This plan operationalizes Kiro's Stress Tests 4-6 and adds two follow-on tests (7-8) for current Telegram relay usage.

## Preflight (Run Once)
- From repo root: `/home/mical/fde`
- Use local Python env where `scripts.pis` works.

```bash
cd /home/mical/fde
python3 -m scripts.pis.query_engine check
python3 -m scripts.pis.coordination run "sanity check task"
python3 -m scripts.pis.coordination list | tail -5
```

Expected:
- `check` passes on clean baseline.
- coordination run creates a task file in `palette/scripts/pis/state/tasks/`.

---

## Stress Test 6 (Run First): PIS Data Layer Drift Detection

Goal: prove `query_engine check` catches taxonomy/classification/routing/recipe drift.

### 6A Baseline
```bash
cd /home/mical/fde
python3 -m scripts.pis.query_engine check
```
Pass if baseline is clean.

### 6B-6F Drift injections (recommended on throwaway branch)
Create a branch:
```bash
git checkout -b stress/drift-detection-20260227
```

Inject each drift one at a time and run `check` after each:
1. Add RIU in taxonomy only (no classification entry)
2. Add classification as `both` but no service routing entry
3. Add routing entry with non-existent recipe service
4. Add orphaned recipe not referenced in routing
5. Add non-existent agent in taxonomy entry

Run after each edit:
```bash
python3 -m scripts.pis.query_engine check
```

Pass criteria:
- Each injected drift causes a clear failure.
- Error message references the broken layer and target file/entry.

Cleanup:
```bash
git checkout -- .
git checkout main
```

---

## Stress Test 5 (Run Second): Handoff Replay Under Partial Failure + Data Drift

Goal: validate replay semantics and data consistency markers.

### 5A Create controlled failure
```bash
cd /home/mical/fde
python3 -m scripts.pis.coordination run "add observability to my system" --fail-step traversal
python3 -m scripts.pis.coordination list | tail -3
```
Capture failed `task_id`.

### 5B Introduce drift before replay
Make one small PIS change (e.g., classification flip for a non-critical RIU) and save.

### 5C Replay
```bash
python3 -m scripts.pis.coordination replay <task_id>
python3 -m scripts.pis.coordination show <task_id>
```

Pass criteria:
- Upstream successful step outputs remain preserved unless intentionally re-run.
- Failed step and downstream steps are re-executed.
- Packet history shows attempt increments and failure/recovery timeline.
- Any data drift effect is visible and explainable from outputs.

---

## Stress Test 4 (Run Third): Cross-Implementation Consistency

Goal: determine whether implementations follow shared Palette patterns or drift.

Implementations:
- `implementations/retail/retail-rossi-store`
- `implementations/talent/talent-gap-interview`
- `implementations/education/education-alpha` (or closest existing education impl)

Workflow to trace in each:
- user query intake
- RIU traversal logic or equivalent decision path
- handoff/agent role mapping
- persistence format for state/artifacts

Checklist per implementation:
- Uses common intent naming conventions
- Uses shared role semantics (Cory/Argy/Rex/etc.)
- Uses compatible state schema (or documented deviation)
- Uses shared code where expected (not copy-paste forks)

Pass criteria:
- >=80% structural consistency across traced categories
- All divergences categorized: intentional vs accidental
- Accidental divergences have owner + fix path

---

## Additional Tests (Proposed)

## Stress Test 7: Telegram Intent Contract Regression

Goal: ensure relay intents and handlers don't drift (e.g., `daily_update` alias support).

Run:
1. `/relay status_request test`
2. `/relay daily_update test`
3. `/relay update_request test`
4. `/relay unknown_intent test`

Pass criteria:
- 1-3 accepted and routed to inbox/outbox.
- unknown intent returns explicit allowed-intents error.
- consumer logs correct intent labels and no crashes.

## Stress Test 8: Group Chat Multi-Actor Routing Integrity

Goal: verify clarity and behavior in shared group with Sahar/Eiad + bot.

Run scenarios:
1. plain human message (no bot mention, no slash command)
2. `/relay daily_update ...`
3. `@rossi_mission_bot` direct ask
4. overlapping asks from 2 humans within 60 seconds

Pass criteria:
- Bot responds only when expected by chat policy.
- Each relay request creates unique inbox artifact with trace ID.
- No cross-user attribution confusion in artifacts.

---

## Recommended Order and Timebox
1. Test 6 (60 min)
2. Test 5 (90 min)
3. Test 4 (120-180 min)
4. Test 7 (30 min)
5. Test 8 (45 min)

Total: ~6-7 hours across one focused session or split over 2 days.

---

## Reporting Template (Use per test)
- Test ID:
- Date/time:
- Branch/commit:
- Commands run:
- Result: pass/fail
- Failures observed:
- Severity:
- Recommended fix:
- Owner:
- Re-test needed:
