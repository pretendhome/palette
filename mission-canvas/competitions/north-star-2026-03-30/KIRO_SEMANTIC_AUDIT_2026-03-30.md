# Semantic Audit + Lean Analysis — Post North Star Competition

**Date**: 2026-03-30
**Auditor**: kiro.design
**Trigger**: End of North Star Competition — 30+ tasks shipped by 5 agents in one day
**Scope**: All artifacts in /home/mical/fde (Palette, Mission Canvas, Enablement)

---

## Ground Truth (Measured)

| Metric | Actual Value | Source |
|--------|-------------|--------|
| Palette KL entries | 168 (131 main + 6 gaps + 31 context) | palette_knowledge_library_v1.4.yaml |
| Palette KL sources | 543 | counted from YAML |
| Taxonomy RIUs | 121 | palette_taxonomy_v1.3.yaml |
| Canvas palette_knowledge.json | 168 entries (synced) | JSON file |
| Canvas palette_routes.json | 121 routes | JSON file |
| Oil workspace KL | 28 entries | oil_knowledge_library_v1.yaml (library_questions key) |
| FDE workspace KL | 15 entries | fde_knowledge_library_v1.yaml (TO BE DELETED) |
| Rossi workspace KL | 0 | no KL file |
| Workspaces | 3 (rossi, oil-investor, fde-toolkit) | workspaces/ directory |
| Test suites | 9 files, 1,845 lines | missioncanvas-site/ |
| Competition docs | 8 files, 101 KB | missioncanvas-site/ |

---

## Finding 1: KL Sync Drift (HIGH)

**What**: Palette KL has 168 entries. Canvas palette_knowledge.json has 162. Six entries are missing from the Canvas export.

**Missing IDs**: LIB-076 through LIB-080 (and one more)

**Impact**: Canvas routing and KL evidence in briefs is missing 6 entries. Coaching signals that reference these entries will not fire.

**Fix**: Re-export palette_knowledge.json from the v1.4 YAML. One command.

---

## Finding 2: Two CSS Files (MEDIUM)

**What**: `styles.css` (16,385 bytes, original) and `style.css` (6,404 bytes, Codex #25) both exist. index.html references only `style.css`. The original `styles.css` is orphaned.

**Similarity**: 20% (different files, not duplicates — style.css is workspace-focused, styles.css was the original base)

**Impact**: 16KB of dead CSS. No functional issue but confusing for anyone reading the codebase.

**Fix**: Delete `styles.css` or merge needed base styles into `style.css`.

---

## Finding 3: Dead Files (MEDIUM)

Six orphaned files totaling ~327KB:

| File | Size | Reason |
|------|------|--------|
| yaml_parser.mjs | 9,896 bytes | Replaced by js-yaml in #3. Not imported by anything. |
| styles.css | 16,385 bytes | Replaced by style.css in #25. Not referenced by index.html. |
| material_motion_poc.mjs | 1,496 bytes | PoC file, never integrated. |
| adapter_contract_check.mjs | 2,678 bytes | Pre-V0.3 contract checker, superseded. |
| test_fetch_signals.mjs | 493 bytes | 16 lines, superseded by stress_test_v03_day2.mjs. |
| raptor-to-debug | 295,783 bytes | Debug trace file from February. |

**Fix**: Delete all six. None are imported or referenced.

---

## Finding 4: FDE Knowledge Library Should Be Deleted (HIGH)

**What**: I created `workspaces/fde-toolkit/fde_knowledge_library_v1.yaml` (15 entries) for task #43. Mical correctly identified this as duplication — the main Palette KL (168 entries) was built for FDEs.

**Impact**: If left in place, the FDE workspace will use this 15-entry subset instead of the full 168-entry Palette KL. Worse coaching, worse routing.

**Fix**: Delete `fde_knowledge_library_v1.yaml`. Wire the FDE workspace to the main Palette KL instead.

---

## Finding 5: Stale Numbers in Living Documents (MEDIUM)

Four documents reference outdated counts:

| Document | Stale Claim | Actual |
|----------|------------|--------|
| MISSION_CANVAS_UNIFIED_ARCHITECTURE.md | 162 KL entries | 168 |
| MISSION_CANVAS_VS_WORKSPACE_COMPARISON.md | 162 KL entries | 168 |
| FEASIBILITY_RIU-011_KIRO.md | 120 RIUs | 121 |
| enablement-coach.md | 167 KL entries | 168 |

**Note**: Competition docs (NORTH_STAR_*.md, *_ENTRY.md) also contain stale numbers but are point-in-time records — do NOT modify.

**Fix**: Update the 4 living documents listed above.

---

## Finding 6: Coaching System Boundary Is Clear But Undocumented (LOW)

**What**: Two files handle coaching — `convergence_chain.mjs` (passive, automatic during narration) and `workspace_coaching.mjs` (active, responds to explicit questions). They share `learner_lens.yaml` as the data store after Claude's #33 unification.

**Verdict**: NOT duplicates. Different triggers, different code paths, shared data store. This is correct architecture.

**Risk**: Without documentation, a future contributor might add coaching functions to the wrong file.

**Fix**: Add a comment block at the top of each file explaining the boundary:
- convergence_chain.mjs: "Passive coaching — fires automatically during narration"
- workspace_coaching.mjs: "Active coaching — responds to explicit user questions"

---

## Finding 7: Oil KL Schema Inconsistency (LOW)

**What**: Oil KL uses `library_questions` key (Palette format). The FDE KL I created used `entries` key. The loader in `convergence_chain.mjs` reads `library_questions`.

**Impact**: No functional issue — oil KL loads correctly (28 entries). But if someone creates a new workspace KL using `entries` key, it will silently load 0 entries.

**Fix**: Document the expected key in the workspace KL format. Or make the loader check both keys.

---

## Finding 8: Competition Docs Are 101KB of Non-Code Artifacts (INFO)

Eight competition-related markdown files total 101KB. These are point-in-time records of the competition and should NOT be modified or deleted. But they should not be referenced as current documentation either.

**Recommendation**: Move to a `docs/competition-2026-03-30/` subdirectory after the competition concludes.

---

## Finding 9: learner_state References in My Entry Doc (INFO)

My `KIRO_NORTH_STAR_ENTRY.md` references `learner_state` in project_state.yaml. This was accurate when I wrote it but is now stale after Claude's #33 unification moved everything to `learner_lens.yaml`.

**Impact**: None (competition doc, point-in-time). But if someone reads my entry as current documentation, they'll get confused.

**Fix**: None needed (competition artifact). Note in the integration report that learner_state was retired.

---

## Lean Analysis Summary

### Confirmed Duplications

| Item | Type | Action |
|------|------|--------|
| fde_knowledge_library_v1.yaml | Content duplication of main Palette KL | DELETE |
| styles.css | Replaced by style.css | DELETE |
| yaml_parser.mjs | Replaced by js-yaml | DELETE |

### Confirmed Dead Code/Files

| Item | Action |
|------|--------|
| material_motion_poc.mjs | DELETE |
| adapter_contract_check.mjs | DELETE |
| test_fetch_signals.mjs | DELETE |
| raptor-to-debug | DELETE |

### NOT Duplications (Verified)

| Item | Why It's Not a Duplicate |
|------|------------------------|
| convergence_chain.mjs coaching vs workspace_coaching.mjs | Different triggers (passive vs active), shared data store |
| style.css vs styles.css | Different content (20% similarity), styles.css is orphaned |
| Competition docs vs each other | Point-in-time records from different agents |

### Sync Fixes Needed

| Item | Fix |
|------|-----|
| palette_knowledge.json (162) vs Palette KL (168) | Re-export |
| 4 living docs with stale counts | Update numbers |

---

## Verdict

The system is in good shape for a day where 5 agents shipped 30+ tasks independently. The main risks are:

1. **KL sync drift** — 6 entries missing from Canvas export. Quick fix.
2. **FDE KL duplication** — should be deleted immediately.
3. **Dead files** — 327KB of orphaned code. Cleanup task.

No architectural debt. No broken abstractions. The coaching system split is correct. The learner unification is complete. The flywheel connections are real.

**Total cleanup effort**: ~30 minutes.
