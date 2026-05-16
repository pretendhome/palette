# V3 Refocus List — Full System Alignment
**Date**: 2026-05-16
**Score**: 122/131 (93%) — 2 failures, 7 warnings
**Purpose**: Everything that needs to change to align the system around the product truth: "Your judgment compounds here."
**Handoff to**: Kiro for execution

---

## Product Truth (the standard everything aligns to)

> Palette is where your judgment compounds. Every AI tool gives you an answer and forgets why you asked. Palette remembers what you decided, why you decided it, and makes every future decision better.

Document: `docs/product/PALETTE_MOAT_ITERATIONS_2026-05-16.md`

---

## CRITICAL (Must fix before submission)

### 1. Commit 367+ uncommitted files
**Section 7**: Committed trees don't match. 367 files differ from remote. 5 modified, 11 untracked.
**Why it blocks**: Can't push to production. Can't deploy working product. Can't demo from a URL.
**Fix**: Structured commit in logical chunks (retrieval, CLI, voice, PII, wiki, docs, product).
**Owner**: Kiro (assigned earlier, not yet completed)

### 2. Clean PII from voice audit
**Section 4**: `voice/AUDIT_2026-05-06.md` contains "Mical" 4 times.
**Fix**: Replace personal names with anonymized references or move to `.claude-code/` (non-public).
**Owner**: Kiro
**Time**: 5 min

---

## HIGH PRIORITY (Strengthens submission)

### 3. Update PALETTE_IDENTITY.md — KL count stale
**Section 11**: Identity doc says 176 KL entries, actual is 183.
**Fix**: Update the count in `docs/PALETTE_IDENTITY.md`.
**Owner**: Kiro
**Time**: 5 min

### 4. Resolve 3 stale governance proposals
**Section 13**: PROP-2026-04-04-007, 008, 009 have been in "voting" status for 42 days.
**Fix**: Either archive (--check-expiry flag on file_proposal.py), promote, or reject. They're blocking governance health.
**Owner**: Kiro (can use `--check-expiry` to auto-archive)
**Time**: 10 min

### 5. Terminology drift (high severity cluster)
**Section 5**: 1 high-severity terminology drift cluster detected.
**Fix**: Run terminology audit, identify the drift, fix it.
**Owner**: Kiro
**Time**: 30 min (depends on scope)

### 6. Add product truth section to core/palette-core.md
**Product alignment**: The moat document exists in docs/product/ but is not yet in Tier 1. Every agent should internalize the product truth on startup.
**Fix**: Add a "Product Truth" section to `core/palette-core.md` with the Final Stack (~40 lines from the moat doc).
**Owner**: Kiro (after Mical approves the exact wording — this is a ONE-WAY DOOR change to Tier 1)
**Time**: 15 min
**Gate**: Mical approval required

---

## MEDIUM PRIORITY (System completeness)

### 7. Lens evaluation coverage: 0/30
**Section 12**: No lenses have been evaluated/tested.
**Fix**: Run evaluation on at minimum 3-5 key lenses (Person lens, Founder lens).
**Owner**: Defer to V3.1 (not submission-critical)

### 8. 5 missing integration recipes
**Section 12**: AWS Comprehend, AWS Comprehend PII, AWS Secrets Manager, Guardrails AI, Redis (semantic layer).
**Fix**: Create recipe stubs for each.
**Owner**: Defer to V3.1

### 9. Confidence normalization (0-1 at source)
**Section 15**: RRF scores are in 0-80 range, not 0-1. Works but inconsistent with the plan's target.
**Fix**: Normalize in `hybrid_retrieve()` output. Update thresholds in palette_query.py and query_before_act.py.
**Owner**: Kiro (structural change, needs testing)
**Time**: 1 hour

### 10. Consolidate 3 scripts into 1 module
**Agreed in V3 review**: `palette_query.py` (448 lines) + `session_reflect.py` (343 lines) + `query_before_act.py` (178 lines) should be one module for simplicity.
**Fix**: Merge into single `palette_query.py` with subcommands: `query`, `reflect`, `check`.
**Owner**: Claude Code or Kiro
**Time**: 2 hours

---

## INFORMATIONAL (No action needed, monitoring)

### 11. Constellation integrity: 12 supporting issues
**Section 10**: Constellation validator passes but has 12 minor issues.
**Action**: Monitor. Not blocking.

### 12. 16/121 modules have calibration exemplars
**Section 10**: Low coverage but not a V3 blocker.
**Action**: V3.1 — expand exemplar coverage.

### 13. Bus has only 3 registered peers (of 5 agents)
**Section 15**: Gemini and Mistral not currently registered.
**Action**: They register on demand. Not a permanent issue.

---

## V3 SYSTEMS: ALL GREEN (no action needed)

Section 15 results — everything new in V3 is working:

| Check | Status |
|---|---|
| Hybrid retrieval (FTS5 + vectors + RRF) | PASS |
| FTS5 knowledge library index (864KB) | PASS |
| Vector embeddings (1.8MB, 183 entries) | PASS |
| palette query CLI (5-step pipeline) | PASS |
| Session reflection | PASS |
| Query-before-acting | PASS |
| PII scrubbing in auto_enrich | PASS |
| Perplexity Computer + Reasoning | PASS |
| Learning Mode toggle | PASS |
| V3 test suite (49 tests ALL PASS) | PASS |
| Product truth document | PASS |
| Peers bus operational | PASS |

---

## PRIORITY ORDER FOR KIRO

1. **Commit session** (CRITICAL — unblocks everything)
2. **PII clean** (5 min, during commit)
3. **PALETTE_IDENTITY.md count** (5 min, during commit)
4. **Stale proposals** (10 min, run --check-expiry)
5. **Terminology drift** (30 min)
6. **Product truth → palette-core.md** (15 min, needs Mical approval)
7. **Confidence normalization** (1 hr)
8. **Script consolidation** (2 hrs)

**Total estimated work**: ~4-5 hours to clear all HIGH items.
After items 1-6, the system score should be **130/131** or better.

---

## THE NORTH STAR

Every fix on this list serves one purpose: make the system coherent with the product truth.

> "Palette's moat is that it does not just answer questions. It builds a governed, portable, compounding record of what you are trying to do, what you decided, why you decided it, and what the system learned with you. Every future decision gets better because the system keeps the judgment trail, not just the chat history."

If a fix doesn't serve this, defer it.

---

*Generated by total_health_check.py Section 15 + full system audit. Claude Code, 2026-05-16.*
