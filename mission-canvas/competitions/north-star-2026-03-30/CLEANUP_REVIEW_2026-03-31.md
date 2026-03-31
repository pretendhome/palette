# Mission Canvas Cleanup Review

**Date:** `2026-03-31`  
**Scope:** post-competition quality pass after the North Star archive was frozen

## What Looks Good

- The core product direction is clearer now:
  - `index.html` is the main Mission Canvas surface
  - `setup.html` is the onboarding surface
  - `who.html` is the narrow demo artifact
- `style.css` is not duplicate dead weight. It is an active overlay that imports `styles.css`.
- The competition archive in `north-star-competition-2026-03-30/` is the right place for the frozen judging record.

## What Needed Fixing

### 1. Repo guidance had drifted

The root `README.md` still described an older OpenClaw-centric prototype and omitted the current workspace/coaching/identity surfaces.

**Fix applied:**
- updated `README.md` to reflect the current product surface and active endpoints

### 2. The identity artifact was too hardcoded

`who.js` always relayed to `claude.analysis`, which made the artifact less reusable than the current system deserves.

**Fix applied:**
- `config.js` now exposes `identityBackendAgent`
- `who.js` now reads that config and also supports `?backend_agent=...`

## Current Duplication That Is Probably Fine

### Competition docs in root and archive

There are still competition-era docs in the repo root and copies in the frozen archive folder.

**Recommendation:**
- keep the archive as the canonical judging record
- avoid adding new competition edits to the root copies
- later, either delete or clearly mark the root copies as working notes if they are no longer needed

### Multiple entry pages

Current public surfaces include:
- `index.html`
- `setup.html`
- `who.html`
- `voice.html`
- `index_classic.html`
- `for-business-owners.html`

**Read:** this is the main remaining drift area.

Not all of these are necessarily wrong, but the product story is now much clearer than this surface list suggests.

## Recommended Next Leaning Pass

1. Decide the canonical public surface set:
   - keep `index.html`, `setup.html`, `who.html`
   - explicitly archive or remove `voice.html`, `index_classic.html`, and any landing pages that no longer support the current story

2. Mark archive-only docs more aggressively:
   - make the frozen archive the obvious source of truth for competition history

3. Tighten trace semantics in coaching packets:
   - use session/turn trace ids rather than workspace ids

4. Finish wire-native consumption:
   - consume `coaching_packets`, not only legacy `coaching_signals`

## Bottom Line

The repo is in better shape than it looked at first pass. The biggest remaining issue is not broken code. It is surface-area sprawl from rapid exploration.

The next cleanup step should be narrowing what counts as the current product, not another broad refactor.
