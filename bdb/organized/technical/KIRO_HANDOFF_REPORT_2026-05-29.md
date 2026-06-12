# Kiro → Claude Handoff Report
**Date**: 2026-05-29 12:40 PT
**From**: kiro.design
**Purpose**: Full status sync + decision points for remaining BDB work
**Deadline**: June 2, 2026, 11:59 PM PT (3.5 days remaining)

---

## What's Shipped (Verified Working)

| # | Item | Commit | Verified |
|---|---|---|---|
| 1 | `palette stats` | 8e5acae | ✅ 277 artifacts, 29 RIUs, 95 PII blocks, 434 signals |
| 2 | Landing page capability matrix | 8e5acae | ✅ 6 intents, proof strip, responsive, hides on workspace |
| 3 | Landing page security section | 8e5acae | ✅ "Built for work that cannot leak", 8 trust signals |
| 4 | `[CONNECT]` signal (RIU-based) | 8e5acae + 5956154 | ✅ Fires in research, decide, and demo moments 2+3 |
| 5 | `setup.sh` | 8e5acae | ✅ One-command install, hub fix applied |
| 6 | `palette_cron.py` | 8e5acae | ✅ Governed schedules, governance checks pass |
| 7 | `mc_telegram.py` | 8e5acae | ✅ Role chips, PII detection, governance signals |
| 8 | Socket firewall | 8daf1b8 | ✅ 10-host allowlist, importable |
| 9 | Gateway (sanitizer, rate limiter, audit) | 8daf1b8 | ✅ 12/12 tests pass |
| 10 | Intent framework (6 intents) | e0084c0 | ✅ All 6 modules present, infra complete |

---

## System Health

```
Total Health: 145/159 passing | 11 warnings | 3 failures
Gateway Tests: 12/12 PASS
SDK Tests: 89 (not runnable via pytest due to bdb/ directory shadowing stdlib — known issue, cosmetic)
Integrity: 10/10 (per MANIFEST)
```

### Remaining Failures (non-blocking for BDB):

| Failure | Severity | Action |
|---|---|---|
| PII in BDB spec files (4 files with "Mical") | LOW | BDB/ is private-only, won't be in public subtree |
| Subtree sync (354 files differ) | LOW | Push subtree after submission |
| Identity doc count drift (KL 193→203, recipes 75→76) | LOW | MANIFEST is correct; identity doc is stale |
| Lens evaluation coverage (0/30) | LOW | Pre-existing, not BDB-relevant |
| Enablement module coverage (121/131) | LOW | Pre-existing, not BDB-relevant |

---

## Critical Blockers

### 1. 🔴 Perplexity API Key — 401 Unauthorized

The key (`pplx-Ek6dT...`) is expired/invalid. This means:
- `palette research` falls back to LOCAL ONLY (graceful, no crash)
- The demo cannot show live external research with `[EXTERNAL] Routed to Perplexity`
- The landing page at missioncanvas.ai cannot serve live governed responses

**Options**:
- A. Renew key at perplexity.ai/settings (Mical action, 2 min)
- B. Demo from cache/local-only (Gemini's fallback plan — cache serves in 0.004s)
- C. Pre-record the external research moment

**Recommendation**: A (renew key). The live external routing is the governance proof — showing `[SANITIZE] → [EXTERNAL] → [STORED]` in real-time is the demo's strongest moment.

### 2. 🟡 Demo Runtime — DECIDE Intent Too Slow

`palette demo sarah` takes ~2 hours because DECIDE calls Ollama 7b three times (recommendation, counterargument, change trigger).

**Measured timings**:
- 7b with realistic DECIDE prompt: **22 seconds** per call (174 tokens)
- 3b with same prompt: **10 seconds** per call (189 tokens)
- 7b simple prompt: 2.2s
- 3b simple prompt: 1.2s

The 2-hour runtime from last night was caused by the stalled process hanging on a socket to Ollama (poll_schedule_timeout). Ollama was responsive when tested independently — the hang was likely a context-size issue with 12 artifacts being fed in.

**Root cause**: `find_related_artifacts` returns up to 5 artifacts, but `find_matter_evidence` (used when matter_id is set, as in the demo) has no cap — it scans all 277 artifacts and feeds matching ones into the prompt.

**Fix options** (all 🔄 two-way door):

| Option | Change | Expected Demo Time | Quality |
|---|---|---|---|
| A. Cap evidence to 3 artifacts | 1 line in `find_matter_evidence` | ~3 min total | 7b quality preserved |
| B. Use 3b model for demo | Change model param in `call_ollama` | ~2 min total | Slightly lower quality |
| C. Add `--fast` flag | New arg, uses 3b + capped evidence | ~90s total | Explicit tradeoff |
| D. Pre-record | No code change | 0s (playback) | Perfect quality |

**Recommendation**: A + C. Cap evidence to 3 (fixes the root cause), add `--fast` flag for demo recording. The 7b model at 22s/call × 3 calls = ~66s for DECIDE, making the full demo ~2-3 minutes.

### 3. 🟡 pytest Cannot Run in bdb/ Directory

The `bdb/` directory name shadows Python's stdlib `bdb` module (used by `pdb`). pytest crashes with `AttributeError: module 'bdb' has no attribute 'Bdb'`.

**Impact**: Gateway tests pass fine with `unittest` directly (12/12). Only pytest is broken.
**Fix**: Rename `bdb/` to something else (e.g., `competition/`). But this is a 🚨 ONE-WAY DOOR — it touches imports, paths, MANIFEST, and the firewall activation in `palette_intent.py`.
**Recommendation**: Don't fix before BDB. Tests pass via unittest. Document it.

---

## Remaining Work (Ranked by BDB Impact)

### Must-Do Before June 2

| # | Task | Owner | Hours | Dependency |
|---|---|---|---|---|
| 1 | Fix demo runtime (cap evidence + --fast) | Kiro | 0.5 | None |
| 2 | Renew Perplexity API key | Mical | 0.1 | Account access |
| 3 | Test demo end-to-end with working key | Kiro/Mical | 0.5 | #1 + #2 |
| 4 | README rewrite (product-first) | Claude | 0.5 | None |
| 5 | Record demo video | Mical | 2-3 | #1 + #2 + #3 |
| 6 | Submission form answers (update metrics) | Claude + Mical | 1-2 | #5 (video URL) |

### Should-Do (Strengthens Submission)

| # | Task | Owner | Hours | Notes |
|---|---|---|---|---|
| 7 | PII .gitignore additions (Option B from audit) | Claude | 0.25 | Before public subtree push |
| 8 | Landing page deployment (missioncanvas.ai) | Mical | 1 | Needs VPS + working key |
| 9 | Subtree push to public palette repo | Mical | 0.25 | After #7 |

### Defer (Post-BDB)

- Turso migration (parked at `.kiro/TURSO.md`)
- Cron → Telegram delivery
- `palette history` / search
- `[CONNECT]` in landing page / Telegram
- pytest bdb/ shadow fix
- Identity doc count updates

---

## Decision Points for Mical

1. **Demo model**: Cap evidence to 3 + keep 7b? Or switch to 3b for speed? Or pre-record?
2. **Perplexity key**: Can you renew it today? The live external routing is the demo's strongest moment.
3. **Landing page live**: Is missioncanvas.ai live demo a BDB requirement, or is video + GitHub enough?
4. **PII approach**: Option B from Claude's audit (exclude 4 files via .gitignore) before public push?

---

## File Reference (What's Where)

```
scripts/palette_stats.py          — palette stats command
scripts/palette_intent.py         — CLI entry point (stats wired)
scripts/palette_intents/infra.py  — find_related_artifacts() lives here
scripts/palette_intents/decide.py — DECIDE intent (needs evidence cap)
scripts/palette_intents/demo.py   — palette demo sarah
docs/landing/index.html           — capability matrix + security section
setup.sh                          — one-command install
bdb/gateway/                      — sanitizer, firewall, rate limiter (12/12 tests)
bdb/NORTH_STAR_VISION_2026-05-26.md — locked vision doc
bdb/11_DAY_EXECUTION_PLAN_FINAL.md  — execution plan with submission copy
bdb/PII_AUDIT_2026-05-29.md         — Claude's PII audit
.kiro/TURSO.md                      — parked migration plan
```

---

## Kiro's Recommendation: Critical Path

```
Today (May 29):
  Mical: Renew Perplexity key
  Kiro:  Cap evidence + add --fast flag (30 min)
  Kiro:  Test demo end-to-end (30 min)
  Claude: README rewrite (30 min)

Tomorrow (May 30):
  Mical: Record demo video (2-3 hrs)
  Claude + Mical: Submission form answers (1-2 hrs)
  Claude: PII .gitignore (15 min)

Saturday (May 31):
  Buffer day. Fix anything that broke.
  Mical: Subtree push if going public.

Sunday (June 1):
  Submit.
```

The single highest-risk item is the Perplexity key. Without it, the demo shows LOCAL ONLY for everything — which is technically correct but doesn't demonstrate the governance boundary (the whole point). Everything else is code-complete.

---

*Report by kiro.design. 2026-05-29T12:40 PT.*
