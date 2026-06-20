# Joseph Command Center — Setup Checklist

## Phase 1 — Shape The Workspace Around Joseph

1. Run the onboarding lens prompt in Claude Code from this directory.
2. Create `lens.yaml` locally and keep it local-only.
3. Create `profile.md` with only sanitized context.
4. Capture Joseph's active domains in plain language.
5. Decide whether this workspace sits above `oil-investor` or stays separate.

## Phase 2 — Map Sources And Boundaries

1. Identify Joseph's source folders:
   - memos
   - spreadsheets
   - notes
   - research
   - contracts or files that must remain excluded
2. Record which folders are safe to read locally.
3. Record which files must never leave the machine.
4. Update the workspace notes with those boundaries.

## Phase 3 — Choose The Front Door

1. Pick the primary surface:
   - web
   - Telegram
   - voice
   - hybrid
2. Decide which surface is for:
   - convergence
   - alerts
   - quick questions
   - deep work
3. Update `config.yaml` if the primary frontend should change.

## Phase 4 — Tune Startup Behavior

1. Decide what Joseph should see first:
   - daily brief
   - decision board
   - meeting brief
   - workspace map
2. Update `artifacts.defaults` if needed.
3. Update the startup artifact in `config.yaml` if needed.
4. Add at least three real known facts to `project_state.yaml`.
5. Resolve or rewrite the default missing evidence items once real answers exist.

## Phase 5 — Turn On The Ambient Loop

1. Decide what the system should watch.
2. Choose a cadence that is useful and not noisy.
3. Keep the first monitor set narrow.
4. Verify the alert channel before adding more monitors.

## Phase 6 — Verify The Workspace Is Real

1. Load `http://127.0.0.1:8787/joseph-command-center`.
2. Confirm the welcome payload loads without error.
3. Ask:
   - `what is blocking us?`
   - `what decisions are pending?`
   - `how are we doing?`
4. Confirm the answers reflect Joseph's real setup rather than template language.
5. If they still sound generic, the onboarding is not finished.

## Success Criteria

- Joseph recognizes the workspace as his.
- It starts from his priorities, not from a canned domain.
- It preserves the existing `oil-investor` flow if he still wants it.
- It knows where his useful files are.
- It has a credible first monitor loop.
- It produces artifacts he would actually reuse.
