# Palette Lean Audit — Initial Findings

**Auditor**: kiro.design
**Date**: 2026-04-09
**Trigger**: System has grown too fast. Mical wants the smallest system that can be trusted in production.

---

## Ground Truth Numbers

| Area | Count | Concern |
|------|-------|---------|
| ~/fde/ total files | ~4,500+ | Large |
| palette/ files | 2,077 | Core system |
| implementations/ files | 1,113 | Many may be stale |
| talent/ applications | 27 folders | Most are closed/abandoned |
| enablement/ files | 329 | Active |
| product/ files | 534 | Untouched since Mar 2 |
| garbage-collection/ | 226 files | Should be empty or archived |
| backups/ | 84 files | Only Feb 16 backup |
| Git untracked/modified | 61 files | Need commit or .gitignore |
| Bus messages | 952 | Growing |
| Proposed wiki entries (pending) | 26 | Stress test artifacts — should be archived |
| Proposed wiki entries (archived) | 87 | OK |
| Broadcast deliveries tracked | 1,995 | Growing — may need cleanup |

## Immediate Red Flags

### 1. STEERING FILE COMPLIANCE — Agent Memory
assumptions.md says: "No persistent memory across engagements/projects" and "No historical logging beyond what is required for toolkit integrity."

We built agent memory (8 entries), skills (4 entries), and FTS5 search (952 indexed messages) on the broker. These are persistent cross-session state. This MAY violate the steering files.

**Question for Mical**: Is the agent memory system an approved exception to the no-persistent-memory rule? Or should it be governed by a formal amendment to assumptions.md?

### 2. 26 STRESS TEST PROPOSALS STILL PENDING
Gemini's stress test proposals from Apr 4 are still sitting in wiki/proposed/ with status "approved." They are test artifacts polluting the live governance queue. Should be archived.

### 3. PRODUCT/ DIRECTORY UNTOUCHED SINCE MAR 2
534 files, last modified March 2. This is the old product documentation. If it's superseded by the wiki, it should be archived.

### 4. GARBAGE-COLLECTION/ HAS 226 FILES
This directory exists to hold things being cleaned up. It should be empty after cleanup, not accumulating.

### 5. 27 TALENT APPLICATIONS — MOST ARE CLOSED
Only a few are active (Obsidian, Stripe, NSA, iBusiness, Anthropic new roles). The rest are closed or abandoned. Each has 5-20 files. That's ~300 files of stale application materials.

### 6. IMPLEMENTATIONS — STALE VERTICALS
dev (105 files), finance (16), therapy (4), youtube-exploration (19) — these appear abandoned. retail (237) and education (269) may be partially active.

### 7. 61 UNTRACKED GIT FILES
Work from the last week that hasn't been committed. Includes competition files, audit reports, broker changes, plugin code.

## What Needs Architect Input

1. Should agent memory/skills/search be governed by a steering file amendment?
2. Which implementations are active vs archived?
3. Should product/ be archived entirely?
4. Should garbage-collection/ be emptied?
5. What is the canonical location for each system component?
6. How do we validate the entire system in one pass?

## Proposed Audit Structure

### Phase 1: Compliance (steering files)
- Read all 3 steering files
- Check every new system against them
- Flag violations, propose amendments

### Phase 2: Inventory (what exists)
- Walk every directory
- Classify: active / archive / delete
- Check for duplicates and misplaced files

### Phase 3: Validation (does it work)
- Run all validators
- Semantic audit (counts, cross-references)
- Broker health check

### Phase 4: Cleanup (trim)
- Archive stale implementations
- Archive closed talent applications
- Archive stress test proposals
- Commit or .gitignore untracked files
- Empty garbage-collection/

### Phase 5: Documentation (what remains)
- Update MANIFEST.yaml
- Update README.md
- Update CHANGELOG.md
- Verify all counts match

---

*Waiting for Claude's architect response before executing. This report is the starting point.*
