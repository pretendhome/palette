# Repo Sanitization Plan — 2026-05-01

**Author**: kiro.design  
**Status**: DRAFT — pending claude.analysis review  
**Decision type**: 🚨 ONE-WAY DOOR (some actions irreversible in working tree)  
**Scope**: pretendhome monorepo + palette/enablement subtrees

---

## Context

On 2026-04-30, commit `84ee76b` attempted a blind find-and-replace (`Glean→Lumen`, `Sierra→Alpine`) across 984 files plus mass-untracking of talent application files. It was reverted 2 minutes later (`f47e18c`). The revert restored all tracked files, but left 8 untracked residue items on disk and the underlying problems unsolved.

**Operator decision**: Make `pretendhome/pretendhome` (the monorepo) **private**. The public-facing repos are `pretendhome/palette` and `pretendhome/enablement` (subtree splits). No history purging needed.

---

## Constraints (Hard)

1. **Glean interview links MUST stay live:**
   - `https://pretendhome.github.io/palette/lab/` ✅ (verified 200)
   - `https://pretendhome.github.io/palette/lab/sa-mcp-readiness-guide.html` ✅ (verified 200)
   - `https://github.com/pretendhome/enablement/blob/main/gold-standard/mcp-integrations/artifacts/starter-template.js` ✅ (verified in subtree)
   - `https://github.com/pretendhome/enablement/blob/main/gold-standard/mcp-integrations/artifacts/mcp-server.js` ✅ (verified in subtree)
   - `https://github.com/pretendhome/enablement/tree/main/gold-standard/mcp-integrations/demo` ✅ (verified in subtree)
   - `https://github.com/pretendhome/enablement/tree/main/gold-standard/mcp-integrations` ✅ (verified in subtree)

2. **Sierra interview links MUST stay live:**
   - `https://pretendhome.github.io/palette/voice-workbench/` ✅ (verified 200)
   - `https://github.com/pretendhome/palette` (general repo) ✅
   - Voice Hub (`peers/hub/`) ✅ (in palette subtree)

3. **Talent skill stays public in palette** — company names genericized, methodology preserved.

4. **PIS data (buy-vs-build/) keeps real company names** — this is market intelligence, not customer data.

5. **No history purging** — operator accepts historical commits contain talent files.

6. **Agent context files (.steering/) stay public in palette** — they demonstrate multi-agent collaboration.

---

## Action Plan

### Phase 0: Delete Untracked Residue (2 min, safe)

Delete 8 untracked items left by the failed rename:

| Item | Type | Action |
|------|------|--------|
| `.claude-code/Lumen_Knowledge_Velocity_System.pdf` | Renamed copy | `rm` |
| `.claude-code/SPEC_LUMEN_LEARNING_PARTNER_ARCHITECTURE.md` | Renamed copy | `rm` |
| `.claude-code/lumen_architecture_pdf.html` | Renamed copy | `rm` |
| `archive/talent-closed-2026-04-09/talent-lumen-interview/` | Full dir copy | `rm -rf` |
| `backups/job-search-backup-2026-02-16/glean/lumen/` | Nested rename | `rm -rf` |
| `implementations/talent/applications/active/glean-enablement-manager/lumen-enablement-manager/` | Dir copy | `rm -rf` |
| `implementations/talent/applications/active/glean-technical-enablement/lumen-technical-enablement/` | Dir copy | `rm -rf` |
| `implementations/talent/applications/rejected/glean-ai-outcomes-manager/lumen-ai-outcomes-manager/` | Dir copy | `rm -rf` |
| `implementations/talent/nsa/job-search/companies/sierra/alpine/` | Dir copy | `rm -rf` |

**Verification**: `git status --short | grep "lumen\|Lumen\|alpine\|Alpine"` returns empty.

---

### Phase 1: Make pretendhome Private (1 min, reversible)

```bash
gh repo edit pretendhome/pretendhome --visibility private
```

**What this does:**
- Monorepo becomes invisible to public
- palette and enablement repos remain public (they are separate repos)
- All Glean/Sierra interview links continue working (they point to palette/enablement, not pretendhome)
- GitHub profile page loses the README (see Phase 5)

**What this does NOT do:**
- Does not affect local development workflow
- Does not affect `git push` to any remote
- Does not affect subtree push/pull

**Verification**: Visit `https://github.com/pretendhome/pretendhome` in incognito → should 404.

---

### Phase 2: Palette Subtree Fixes (small, targeted)

These changes go into the palette subtree (public repo). Each is a separate commit.

#### 2a. Rename Sierra Voice Intelligence doc

```
palette/voice/SIERRA_VOICE_INTELLIGENCE.md → palette/voice/VOICE_INTELLIGENCE.md
```

Update content:
- Title: "Voice AI Infrastructure — Technical Intelligence Report" (remove "Sierra AI")
- Purpose line: "Technical intelligence for voice agent design roles" (remove "Pre-application" and "Agent Experience Designer, Voice (Multilingual) role")
- Keep all technical content intact — it's excellent competitive intelligence that applies broadly

Update `palette/voice/README.md`:
- Change reference from `SIERRA_VOICE_INTELLIGENCE.md` to `VOICE_INTELLIGENCE.md`
- Change link text from "Sierra Voice Infrastructure Intelligence" to "Voice AI Infrastructure Intelligence"

#### 2b. Fix voice workbench footer

In `palette/docs/voice-workbench/index.html`:
- Change: `Built by Mical Elia — Sierra Agent Experience Designer application artifact`
- To: `Built by Mical Elia — Voice Agent Evaluation Framework`

#### 2c. Genericize talent skill company references

Files to modify (16 + 11 + scattered = ~30 replacements total):

**`palette/skills/talent/role-profiles.yaml`** (16 refs):
- Replace specific company names in `lead_with`, `past_interviews`, `learnings` fields
- Example: `"Glean post-mortem"` → `"enterprise search post-mortem"`
- Example: `"talent-glean-interview"` → `"enterprise-search-interview"`
- Keep the STRUCTURE and LEARNINGS, just anonymize the company names

**`palette/skills/talent/methodology.md`** (11 refs):
- Same pattern: genericize company names in examples and learnings
- Example: `"Glean learning"` → `"enterprise search learning"`

**`palette/skills/talent/STAR_STORIES.md`** (1 ref):
- Genericize the single company reference

**`palette/skills/talent/interview-prep-methodology.md`**, **`enablement-test-execution.md`**, **`live-build-execution.md`**, **`job-search-command.md`**:
- Scan and genericize any company references

**`palette/skills/talent/experience-inventory.yaml`**:
- This contains career history — company names here are FACTUAL (Amazon, AWS, etc.)
- These should NOT be changed — they are your real employment history
- Only change references to interview targets (Glean, Sierra, Gap, etc.)

**Replacement mapping for talent skill files:**

| Original | Replacement | Rationale |
|----------|-------------|-----------|
| Glean | enterprise search company | Interview target |
| Sierra | voice AI company | Interview target |
| Gap | retail company | Interview target |
| Capital Group | financial services company | Interview target |
| Perficient | consulting firm | Interview target |
| LVMH | luxury brand | Interview target |
| Anthropic | AI lab (keep as-is in tech context) | Public company, tech reference OK |
| OpenAI | OpenAI (keep) | Public company, tech reference OK |
| Mistral | Mistral (keep) | Public company, tech reference OK |

**Note**: Anthropic, OpenAI, and Mistral are referenced as technology providers, not interview targets. They stay.

#### 2d. Enablement Glean references (5 fixes)

**`enablement/docs/ROAD_TO_SAINITY_OPERATING_SYSTEM_2026-04-23.md`** (1 ref):
- `"Glean gold-standard pattern"` → `"the enterprise search gold-standard pattern"`

**`enablement/docs/YOUTUBE_BUILD_PACK_2026-04-23.md`** (4 refs):
- `"Glean gold-standard module"` → `"the enterprise search gold-standard module"`
- `"What Glean Taught Us"` → `"What the Gold-Standard Module Taught Us"`
- `"Today's Glean gold-standard module"` → `"Today's gold-standard module"`
- `"The Glean module is strong"` → `"The module is strong"`

**These must be committed in the monorepo AND pushed to the enablement subtree.**

---

### Phase 3: Subtree Push (5 min)

After Phase 2 commits:

```bash
cd ~/fde
git subtree push --prefix=palette palette main
git subtree push --prefix=enablement enablement main
```

**Verification**:
- All 6 Glean interview links still return 200
- Voice workbench link still returns 200
- `git show palette/main:voice/VOICE_INTELLIGENCE.md` exists
- `git show palette/main:voice/SIERRA_VOICE_INTELLIGENCE.md` does NOT exist
- `git show enablement/main:docs/YOUTUBE_BUILD_PACK_2026-04-23.md | grep -i glean` returns empty

---

### Phase 4: GitHub Profile README (5 min)

Making pretendhome private removes the profile README. Options:

**Option A — Create a standalone profile README repo:**
- This won't work — `pretendhome/pretendhome` IS the profile repo, and it's now private.
- GitHub shows profile READMEs from the repo matching the username. Private repos don't render.

**Option B — Keep pretendhome public but clean:**
- This contradicts the "make private" decision.

**Option C — Move the README content to palette's README:**
- The palette repo README becomes the de facto portfolio front door.
- Update `palette/README.md` to include the profile content (Voice Workbench link, Voice Hub link, Palette description, Enablement link).

**Recommendation**: Option C. The palette README is already the most-visited page. Enhance it with the profile content. The pretendhome profile page will show pinned repos (palette, enablement) even without a README.

**Operator decision needed**: Confirm Option C or choose differently.

---

### Phase 5: Total Health Agent Updates

The total-health agent should have caught several of these issues. Here's what needs to be added:

#### New Section 15: Public Repository Hygiene

```python
def section_15_public_repo_hygiene(report: HealthReport) -> None:
    """Verify public-facing repos are clean of private/sensitive content."""
```

**Check 15a — Sensitive directories not tracked in subtrees:**
- Verify `implementations/talent/applications/` is NOT in palette or enablement subtree
- Verify `archive/talent-closed-*/` is NOT in subtrees
- Verify `backups/` is NOT in subtrees
- Verify `implementations/talent/nsa/` is NOT in subtrees
- Verify `implementations/talent/trackers/` is NOT in subtrees

**Check 15b — No interview-target company names in public skill files:**
- Scan `palette/skills/talent/*.yaml` and `palette/skills/talent/*.md` for a configurable list of interview-target company names
- Exclude `experience-inventory.yaml` (factual career history)
- Exclude `buy-vs-build/` (market intelligence)
- Flag any hits as warnings

**Check 15c — No untracked rename residue:**
- Run `git status --short` in the monorepo
- Flag any untracked files containing "lumen", "alpine", or other known rename artifacts

**Check 15d — Enablement content is company-agnostic:**
- Scan `enablement/docs/*.md` and `enablement/curriculum/**/*.yaml` for interview-target company names
- Exclude `enablement/gold-standard/` (the MCP lab content references generic "enterprise search" already)
- Flag any hits as warnings

**Check 15e — GitHub Pages links are live:**
- Verify key URLs return HTTP 200:
  - `https://pretendhome.github.io/palette/lab/`
  - `https://pretendhome.github.io/palette/lab/sa-mcp-readiness-guide.html`
  - `https://pretendhome.github.io/palette/voice-workbench/`
- This requires network access — make it opt-in with `--check-urls` flag

**Check 15f — Subtree sync includes no private content:**
- After subtree push, verify the subtree HEAD does not contain files from private directories
- Cross-reference palette subtree file list against a blocklist of private path prefixes

#### Update to Section 4 (Cleanliness) — Interview Target Detection

The existing Section 4 checks for personal names in operational code. It should ALSO check for interview-target company names in public-facing files:

```python
# Add to section_4_cleanliness:
INTERVIEW_TARGETS = ["Glean", "Sierra", "Gap Inc", "Capital Group", 
                     "Perficient", "LVMH", "Baseten", "Friendli"]
# Scan palette/skills/talent/ for these (excluding buy-vs-build/)
```

#### Update to Section 7 (Repo Mirror) — Private/Public Boundary

Section 7 currently checks that the palette subtree matches the palette remote. It should ALSO verify:

- The monorepo `.gitignore` covers all private directories
- No private-only files have leaked into the subtree

#### Documentation: Two-Repo Architecture

Add to `total-health.md`:

```markdown
### Section 15: Public Repository Hygiene

The Palette system operates across two visibility tiers:

| Repo | Visibility | Contains |
|------|-----------|----------|
| `pretendhome/pretendhome` | **PRIVATE** | Full monorepo: palette, enablement, implementations, talent, archive, backups, agent context |
| `pretendhome/palette` | **PUBLIC** | Subtree split of palette/. Intelligence system, agents, skills, voice, wiki |
| `pretendhome/enablement` | **PUBLIC** | Subtree split of enablement/. Curriculum, assessment, gold-standard modules |

**Invariant**: No file in the public subtrees should contain interview-target company names 
(except in PIS market data and factual career history). The total-health agent enforces this.

**Invariant**: All shared interview links must resolve to HTTP 200 after any subtree push.
```

---

## Verification Checklist (Post-Execution)

- [ ] `git status --short | grep "lumen\|Lumen\|alpine\|Alpine"` → empty
- [ ] `https://github.com/pretendhome/pretendhome` in incognito → 404
- [ ] `https://github.com/pretendhome/palette` in incognito → 200
- [ ] `https://github.com/pretendhome/enablement` in incognito → 200
- [ ] All 6 Glean interview links → 200
- [ ] Voice workbench link → 200
- [ ] `git show palette/main:voice/VOICE_INTELLIGENCE.md` → exists
- [ ] `git show palette/main:voice/SIERRA_VOICE_INTELLIGENCE.md` → does NOT exist
- [ ] `git grep -i "Glean" -- palette/skills/talent/` → 0 hits (excluding experience-inventory.yaml)
- [ ] `git grep -i "Sierra" -- palette/skills/talent/` → 0 hits (excluding experience-inventory.yaml)
- [ ] `git grep -i "Glean" -- enablement/docs/` → 0 hits
- [ ] `python3 agents/total-health/total_health_check.py --section 15` → PASS
- [ ] `python3 agents/total-health/total_health_check.py` → no new failures

---

## Risk Assessment

| Action | Risk | Reversibility |
|--------|------|---------------|
| Delete untracked residue | None — files are garbage | Irreversible but harmless |
| Make pretendhome private | Low — subtrees unaffected | Reversible (1 click) |
| Rename Sierra voice doc | Low — internal reference only | Reversible (git revert) |
| Fix voice workbench footer | None — cosmetic | Reversible |
| Genericize talent skill refs | Medium — must not break skill functionality | Reversible (git revert) |
| Fix enablement Glean refs | Low — 5 small text changes | Reversible |
| Subtree push | Medium — public repos updated | Reversible (force-push old HEAD) |
| Profile README loss | Medium — visitors see blank profile | Mitigated by Option C |

---

## Decision Log Entry (for decisions.md)

```
### 2026-05-01: Repo Visibility Restructuring
- **Type**: 🚨 ONE-WAY DOOR (public→private visibility change)
- **Decision**: Make pretendhome/pretendhome private. palette and enablement remain public subtrees.
- **Rationale**: Monorepo contains talent applications, interview prep, salary data, personal trackers. These should never be public. The public-facing work (intelligence system, enablement curriculum, voice tools) is already cleanly separated into subtree repos.
- **Actions**: 
  1. Delete untracked rename residue
  2. Make pretendhome private
  3. Genericize interview-target company names in palette/skills/talent/
  4. Genericize Glean references in enablement/docs/
  5. Rename Sierra voice intelligence doc
  6. Fix voice workbench footer
  7. Push subtrees
  8. Add Section 15 to total-health agent
- **Verified by**: kiro.design (plan), claude.analysis (review), operator (approval)
```
