# Kiro Autonomous Agent — Ready-to-Go Task Queue

**Prepared by**: kiro.design
**Date**: 2026-04-01
**Status**: READY — waiting for autonomous agent access

---

## Task 1: Repo Cleanup (Easy, ~10 min)

**Repos**: pretendhome/pretendhome
**Description**: Clean up dead files and fix gitignore gaps in missioncanvas-site/

Delete these files:
- missioncanvas-site/raptor-to-debug (296KB debug trace from February)
- missioncanvas-site/for-business-owners.html (2KB, unused pre-V0.3 page)

Add to missioncanvas-site/.gitignore:
```
workspaces/*/sessions/
workspaces/*/learner_lens.yaml
workspaces/*/palette_feedback.yaml
workspaces/*/alerts/
workspaces/*/monitors/
workspaces/*/artifacts/
```

Remove any tracked runtime state files that match the new gitignore patterns.

**Acceptance criteria**: Dead files deleted, gitignore updated, `git status` shows no runtime state files as tracked.

---

## Task 2: Move Tests to tests/ Directory (Easy, ~15 min)

**Repos**: pretendhome/pretendhome
**Description**: Organize test files in missioncanvas-site/

Move these files to missioncanvas-site/tests/:
- stress_test.mjs
- stress_test_convergence.mjs
- stress_test_deep.mjs
- stress_test_session.mjs
- stress_test_v03_day2.mjs
- stress_test_enablement_hook.mjs
- stress_test_flywheel_feedback.mjs
- test_edge_cases.mjs
- test_fde_toolkit_integration.mjs
- test_fetch_signals.mjs

Update any import paths in the test files (they import from ../server.mjs etc).
Run each test to verify it still passes.

**Acceptance criteria**: All tests in tests/ directory, all tests pass, no test files in root.

---

## Task 3: Move Historical Docs to docs/ (Easy, ~10 min)

**Repos**: pretendhome/pretendhome
**Description**: Organize documentation in missioncanvas-site/

Move to missioncanvas-site/docs/:
- NORTH_STAR_ARCHITECTURE.md
- WIRE_CONTRACT_UNIVERSAL_PROTOCOL_PROPOSAL.md
- ONBOARDING.md
- DATA_BOUNDARY.md

Move to missioncanvas-site/docs/historical/:
- CODEX_RIME_INTEGRATION_BRIEF.md
- OPENCLAW_ITERATION_LOG.md
- OPENCLAW_RESEARCH_NOTES.md

Move from monorepo root to missioncanvas-site/docs/research/:
- oil-energy-investor-workspace-research.md
- palette-stt-research.md

Move from monorepo root to missioncanvas-site/docs/historical/:
- OPENCLAW_CLAWDTALK_SETUP_2026-03-17.md
- OPENCLAW_HACKATHON_COLD_START.md
- OPENCLAW_SYSTEM_RECORD_2026-03-17.md

**Acceptance criteria**: No orphaned docs at monorepo root (except README.md), missioncanvas-site root has only source files + config + README.

---

## Task 4: Palette Subtree Sync (Easy, ~5 min)

**Repos**: pretendhome/pretendhome, pretendhome/palette
**Description**: Push the broker broadcast fix to both repos.

File changed: palette/peers/broker/index.mjs
Change: Added `OR to_agent = 'broadcast'` to fetchUndelivered and peekUndelivered queries.

Push to pretendhome/pretendhome main branch, then sync to pretendhome/palette via subtree push.

**Acceptance criteria**: Both repos have the broadcast fix, git log shows the commit in both.

---

## Task 5: README for Mission Canvas (Medium, ~20 min)

**Repos**: pretendhome/pretendhome
**Description**: Write a proper README.md for missioncanvas-site/ that covers:

1. What it is (one paragraph)
2. How to run (`./start.sh rossi` for web, `./start.sh oil-investor --voice` for voice)
3. Architecture overview (convergence chain, workspaces, coaching, wire contract)
4. API endpoints (16 endpoints with method, path, purpose)
5. Test suites (how to run, what they cover)
6. Workspaces (rossi, oil-investor, fde-toolkit — what each proves)

Reference existing docs: NORTH_STAR_ARCHITECTURE.md for vision, WIRE_CONTRACT_UNIVERSAL_PROTOCOL_PROPOSAL.md for protocol.

**Acceptance criteria**: README covers all 6 sections, is accurate against current code, includes working examples.

---

## Task 6: Enablement RIU-524 Threshold Fix (Easy, ~10 min)

**Repos**: pretendhome/enablement
**Description**: Fix the 2 threshold policy warnings in enablement/curriculum/workstreams/

The integrity validator reports:
- RIU-524: critical control-sensitive module WORKING threshold should require competence on all core-control dimensions
- RIU-524: critical control-sensitive module should name mandatory dimensions in WORKING threshold

Find the module.yaml for RIU-524 and add the required mandatory dimensions to the WORKING threshold.

**Acceptance criteria**: `python3 scripts/integrity.py` reports 0 warnings.

---

## Future Tasks (after initial cleanup)

### Palette Enrichment Pipeline
Build canvas_enrichment.py that reads palette_feedback.yaml from workspaces and promotes validated entries to workspace KL. Start simple — one script, one function.

### Wire Contract Phase 2
Refactor Canvas mutation endpoints to use HandoffPacket/HandoffResult internally. Start with resolve-evidence as the pilot.

### Mission Canvas Repo Extraction
Create pretendhome/mission-canvas as a standalone repo with proper structure from KIRO_REPO_AUDIT_2026-03-31.md.
