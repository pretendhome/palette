# Remaining Build Spec — For Kiro
**Date**: 2026-05-28
**From**: claude.analysis
**Status**: SPEC for Kiro — Codex approved the narrow trio (all shipped). These are the next items that strengthen BDB without destabilizing the demo.

---

## What's Done (Codex-Approved Trio — All Shipped)

| # | Item | Status | Who |
|---|---|---|---|
| 1 | `palette stats` | ✅ Shipped | Kiro — `scripts/palette_stats.py`, wired into `palette_intent.py` |
| 2 | Landing page capability matrix | ✅ Shipped | Kiro — 6 intents grid + proof strip on `docs/landing/index.html` |
| 3 | Landing page security section | ✅ Shipped | Kiro — trust list, "Built for work that cannot leak" |
| 4 | `setup.sh` | ✅ Shipped | Claude — one-command install |
| 5 | `palette_cron.py` | ✅ Shipped & tested | Claude — governed scheduled intents |
| 6 | `mc_telegram.py` | ✅ Shipped | Claude — generalized Telegram bot |

Verified: `palette stats` returns 260 artifacts, 29 RIUs, 89 PII blocks, 401 signals. The compounding proof is real.

---

## What's Left (Ranked by BDB Impact)

### 1. `[CONNECT]` Signal — Prior Decision Linking
**Priority**: HIGH for demo
**Risk**: LOW if scoped to CLI only
**Codex ruling**: "Build only if already mostly present. CLI-only for BDB."

**What it does**: When a query classifies to an RIU, scan `.palette/artifacts/` for prior artifacts with the same RIU. Display before the response:

```
[CONNECT]  Connected to 2 prior decisions:
  2026-05-27 [RESEARCH] Delaware fiduciary duty precedents
  2026-05-28 [PROTECT]  What's our exposure (BLOCKED)
```

**Implementation**:
- Add `find_related_artifacts(riu_id: str) -> list[dict]` to `scripts/palette_intents/infra.py`
- Reuse the same frontmatter parsing pattern from `palette_stats.py` (line-by-line, no YAML import required)
- Call it in the RESEARCH and DECIDE intents only (highest demo value)
- Return at most 5 recent matches
- Include BLOCKED artifacts (a blocked decision is high-value context)

**Codex constraints**:
- RIU-only join key (no keyword matching for BDB)
- Span across intents (RESEARCH + PROTECT both contribute)
- Include cron artifacts only if they already have `riu_id` in frontmatter (they do — confirmed from cron test run)
- Flat file scan is acceptable at demo volume
- Do NOT touch server.mjs, landing page, or Telegram for this — CLI only

**Files to touch**:
- `scripts/palette_intents/infra.py` — add `find_related_artifacts()`
- `scripts/palette_intents/research.py` — call and display after `[RESOLVE]`
- `scripts/palette_intents/decide.py` — call and display after `[RESOLVE]`

**Estimated**: 1-2 hours

---

### 2. `palette demo sarah` Polish
**Priority**: HIGH — this is what gets recorded for the video
**Risk**: LOW

**Current state**: The demo command exists at `scripts/palette_intents/demo.py`. It runs 3 moments sequentially.

**What might need attention**:
- Does it show the `[CONNECT]` signal on moment 2 and 3? (It should, once Feature 1 is built)
- Is the output clean enough for screen recording?
- Does it run in under 2 minutes?
- Does Moment 2 (RESEARCH) actually call Perplexity? (API key is expired — 401. Fallback to local-only needs to be graceful.)

**Check and fix if needed**:
- Test `palette demo sarah` end-to-end
- Ensure each moment's output includes governance boundary markers
- Ensure `[CONNECT]` appears in moments 2 and 3
- Handle Perplexity 401 gracefully (show `[EXTERNAL] Perplexity unavailable — local only` instead of crash)

**Files**: `scripts/palette_intents/demo.py`
**Estimated**: 1 hour (mostly testing, minimal code)

---

### 3. Landing Page — Wire to Live Hub
**Priority**: MEDIUM for BDB (judges may click the link)
**Risk**: MEDIUM (needs VPS deployment)

**Current state**: The landing page at `docs/landing/index.html` has the "Who are you?" flow and connects to `HUB_URL` (auto-detects localhost vs VPS). The capability matrix and security section are shipped.

**What's needed for production**:
- Deploy to GitHub Pages (CNAME already at `mission-canvas/CNAME` → `missioncanvas.ai`)
- OR deploy index.html as a static file on the VPS
- Hub server needs to be running on VPS with CORS allowing missioncanvas.ai origin (already `*`)
- Test: can a visitor at missioncanvas.ai type a question and get a governed response?

**Blockers**:
- Perplexity API key expired (401) — needs renewal for live external research
- VPS Hub may not be running — needs `setup.sh` or manual start

**Decision for Mical**: Is live demo on missioncanvas.ai a BDB requirement, or is the video + GitHub repo enough?

**Files**: `docs/landing/index.html` (already built), VPS deployment
**Estimated**: 1-2 hours (deployment, not code)

---

### 4. README.md Rewrite
**Priority**: MEDIUM — judges will look at GitHub
**Risk**: LOW

**Current state**: README.md is architecture-first ("Palette is the operating system for human judgment"). Codex said in the execution plan: "Rewrite README: product-first, not architecture-first."

**What it should be**:
```markdown
# Mission Canvas

Your judgment compounds here.

## Quick Start
git clone ... && cd palette && bash setup.sh

## What It Does
[6 intents — one sentence each]

## See It Work
palette demo sarah

## Your Judgment Trail
palette stats
```

**Files**: `palette/README.md`
**Estimated**: 30 minutes

---

### 5. PII Audit Before Public Push
**Priority**: HIGH before going public
**Risk**: HIGH if skipped

**From the execution plan (Day 8)**:
- Grep for real names, API keys, client data in committed files
- Ensure `bdb/` has no `.db` files with real data
- Ensure no PII in test fixtures
- Check `.env` files are gitignored

**This should be a crew task, not a solo build.** Claude + Kiro can split the grep patterns.

**Estimated**: 1 hour

---

### 6. Submission Form Answers
**Priority**: P0 — must happen before June 2
**Risk**: LOW (text, not code)

**From the execution plan (Day 9)**:
- Finalize all submission form fields
- Update metrics to current numbers (129→??? tests, 131 RIUs, 203 KL)
- Gather all links: video URL, GitHub URL, landing page URL
- Write Computer prompt captions

**The draft exists** at `bdb/11_DAY_EXECUTION_PLAN_FINAL.md` (Part: SUBMISSION COPY). Needs updating with current numbers from `palette stats`.

**Estimated**: 1-2 hours (Mical + Claude)

---

## What NOT to Build Before June 2

Per Codex:
- ❌ Cron → Telegram delivery (wait for Kiro to clear P0 files)
- ❌ `palette history` / search
- ❌ Skill marketplace
- ❌ Dashboard
- ❌ More channels (Slack, Discord, WhatsApp)
- ❌ Natural language cron parsing
- ❌ Docker image
- ❌ npm package

---

## Suggested Build Order for Remaining Days

| Day | What | Who | Hours |
|---|---|---|---|
| **Now** | `[CONNECT]` signal (CLI only) | Kiro | 1-2 |
| **Now** | README rewrite | Claude | 0.5 |
| **Thu May 29** | Demo polish + test recording | Kiro + Mical | 2 |
| **Thu May 29** | PII audit | Claude + Kiro | 1 |
| **Fri May 30** | Submission form answers | Claude + Mical | 1-2 |
| **Fri May 30** | Landing page deployment (if doing live demo) | Mical | 1 |
| **Sat May 31** | Record final demo video | Mical | 2-3 |
| **Sun June 1** | Submit | Mical | 0.5 |

---

## Key File Reference

| File | Owner | Status |
|---|---|---|
| `scripts/palette_stats.py` | Kiro | ✅ Shipped |
| `scripts/palette_intent.py` | Kiro | ✅ Updated (stats wired) |
| `scripts/palette_intents/infra.py` | — | Needs `find_related_artifacts()` |
| `scripts/palette_intents/research.py` | — | Needs `[CONNECT]` call |
| `scripts/palette_intents/decide.py` | — | Needs `[CONNECT]` call |
| `scripts/palette_intents/demo.py` | — | Needs test + polish |
| `docs/landing/index.html` | Kiro | ✅ Updated (cap matrix + security) |
| `palette/README.md` | — | Needs rewrite |
| `palette/setup.sh` | Claude | ✅ Shipped (Kiro patched) |
| `scripts/palette_cron.py` | Claude | ✅ Shipped |
| `mission-canvas/mc_telegram.py` | Claude | ✅ Shipped |

---

*Spec by claude.analysis. Kiro: pick up what makes sense. The `[CONNECT]` signal is the highest-value remaining item — it's literally the compounding proof in the demo. Everything else is polish.*
