# Palette Lean Audit — Comprehensive Report

**Auditor**: kiro.design
**Date**: 2026-04-09
**Health Check**: 101/112 passing, 2 failures, 9 warnings
**Scope**: Full system audit per Mical directive

---

## Executive Summary

The system works. 101 of 112 health checks pass. The core — taxonomy (121 RIUs), knowledge library (176 entries), wiki (176 pages), enablement (121 modules, 14 paths), governance pipeline — is solid.

But the system has grown beyond what the steering files govern. We have 4,500+ files, 854 untracked palette files, 27 talent folders (most closed), and new subsystems (agent memory, skills, search, portfolio generator) that aren't in MANIFEST or governed by steering.

**The fix is not deletion. It's governance.** Claude is right — the system is bloated with unlabeled capability, not waste. The audit should make what exists findable and verifiable.

---

## Health Check Results

### Failures (2)
1. **Lens count mismatch**: MANIFEST says 26, actual is 27. Gemini added LENS-UX-GOOGLE.
2. **Lens evaluation coverage**: 0/27 lenses evaluated. No lens has ever been tested.

### Warnings (9)
- 83 files with personal names in palette subtree
- 2 plugin files differ between implementations/ and plugins/
- 12 modified palette files uncommitted
- 854 untracked palette files
- Various minor count drifts

---

## Phase 1: Steering File Compliance

### Agent Memory System — NEEDS AMENDMENT
assumptions.md says: "No persistent memory across engagements/projects"

We built:
- `/memory` endpoint: 8 entries across agents (2,200 char limit per agent)
- `/skills` endpoint: 4 skills registered
- `/search` endpoint: 952 messages indexed via FTS5
- `broadcast_deliveries` table: 1,995 delivery records

**Claude's proposed amendment** (Tier 2, requires vote):
> Agent memory, skill registrations, and message search are approved persistent state, governed by: (a) memory entries must be auditable, (b) skills must be registered with version and trust tier, (c) search indices may be rebuilt from source messages, (d) all persistent state must be listed in MANIFEST.yaml.

**🚨 ONE-WAY DOOR**: This changes the state policy. Requires Mical approval.

### Everything Else — COMPLIANT
- Frontmatter-native state in Decision Board ✅
- Wiki governance pipeline follows the model ✅
- Peers bus wire contract matches peers-messaging.md ✅
- No unauthorized network calls in plugins ✅

---

## Phase 2: Inventory Classification

### ARCHIVE (do now)
| Directory | Files | Reason |
|-----------|-------|--------|
| implementations/dev/ | 105 | Abandoned experiments |
| implementations/finance/ | 16 | One-time exercise |
| implementations/therapy/ | 4 | Abandoned |
| implementations/youtube-exploration/ | 19 | Superseded by enablement |
| product/ | 534 | Superseded by wiki |
| 17 closed talent folders | ~250 | Applications closed |
| garbage-collection/ contents | 226 | Flush to tarball |

**Total archivable: ~1,154 files** (25% of system)

### KEEP (active)
| Directory | Files | Reason |
|-----------|-------|--------|
| palette/ | 2,077 | Core system |
| enablement/ | 329 | Active curriculum + portfolio |
| implementations/education/ | 269 | ARON/Nora/OKA active |
| implementations/retail/ | 237 | Rossi active |
| implementations/obsidian/ | 21 | Decision Board active |
| implementations/talent/ (8 active) | ~150 | Active pipeline |

### NEEDS DECISION
| Item | Question |
|------|----------|
| backups/ (84 files) | Keep as-is or consolidate? |
| demo/ (3 files) | Still needed? |
| lib/ (2 files) | What is this? |
| skills/ (5 files) | Duplicate of palette/skills/? |
| missioncanvas-site symlink | Keep or remove? |

---

## Phase 3: Validation (post-cleanup)

Run after Phase 4 cleanup:
```bash
# Wiki
python3 palette/scripts/validate_wiki.py
# Health
python3 palette/agents/total-health/total_health_check.py
# Enablement
python3 enablement/scripts/integrity.py
# Palette state
python3 palette/scripts/validate_palette_state.py
```

---

## Phase 4: Immediate Actions

### Quick wins (do now, no approval needed)
1. Archive 26 stress test proposals: `mv wiki/proposed/PROP-2026-04-04-{087..109}.yaml wiki/proposed/archive/`
2. Fix MANIFEST lens count: 26 → 27
3. Sync plugin files: copy decision-board from implementations/ to plugins/
4. Commit 61 untracked git files

### Needs Mical approval (🚨 ONE-WAY DOOR)
1. Agent memory steering amendment
2. Archive product/ directory
3. Archive closed talent folders
4. Archive stale implementations (dev, finance, therapy, youtube)

---

## Phase 5: Post-Audit Documentation

After cleanup:
1. Update MANIFEST.yaml with new systems (portfolio, memory, skills, search)
2. Update README.md counts
3. Write CHANGELOG entry for v3.1 (lean audit)
4. Run full validation suite
5. Commit everything

---

## The Honest Assessment

The system is not broken. It's ungoverned at the edges. The core (taxonomy + KL + wiki + enablement + governance) is rock solid — 101/112 health checks pass. What grew without governance:

1. Agent memory/skills/search — useful but not in steering files
2. Portfolio generator — useful but not in MANIFEST
3. Decision Board plugin — shipped but not in MANIFEST
4. 27 talent folders — most closed, none archived
5. 854 untracked palette files — work that happened but wasn't committed

The fix: govern what we keep, archive what we don't, and make the steering files match reality.

Mical's standard: "I design the smallest system that can be trusted in production."

After this audit, the system should be ~3,300 files instead of ~4,500. Every file earns its place. Every new system is in MANIFEST. Every steering file matches reality.

---

*Waiting for Mical approval on ONE-WAY DOOR items before executing cleanup.*
