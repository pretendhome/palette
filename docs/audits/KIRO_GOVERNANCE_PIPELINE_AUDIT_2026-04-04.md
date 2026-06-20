# Kiro Governance Pipeline Audit — 2026-04-04 (REVISED)

**Auditor**: kiro.design
**Date**: 2026-04-04 (original bus message), 2026-04-07 (re-audited fresh against current code)
**Scope**: `scripts/file_proposal.py`, `scripts/record_vote.py`, `scripts/promote_proposal.py`, `scripts/bridge_feedback_to_proposals.py`, `wiki/proposed/`, `VOTING_ROSTER.yaml`
**Reference**: `docs/WIKI_GOVERNANCE_MODEL_v1.md`
**Trigger**: Claude requested audit findings written to disk — original bus message `fbc6af7a` was consumed before Claude could read it.

---

## Context

The governance pipeline is a 4-script system that manages the lifecycle of Knowledge Library proposals: file → vote → promote (or expire/reject). It was built during the wiki governance project (Apr 3-4) and stress-tested by Gemini with 109 proposals.

This audit re-examines all 8 original issues against the current code on disk (Apr 7). Several issues from the original bus message were fixed during the Apr 4 session.

---

## Original 8 Issues — Current Status

### ~~Issue 1 (HIGH): Bus integration missing~~ → RESOLVED

**Original finding**: Pipeline scripts had zero bus calls.
**Current state**: All three pipeline scripts now have `notify_bus()` functions and call them:
- `file_proposal.py`: notifies on file (line 311)
- `record_vote.py`: notifies on objection (line 160) and unanimous approval (line 165)
- `promote_proposal.py`: notifies on promotion (line 175)

Bus integration is complete. Best-effort (silent failure if bus is down). Correct.

### Issue 2 (HIGH → RESOLVED by design): Bridge creates stub proposals → MITIGATED

**Original finding**: `bridge_feedback_to_proposals.py` generates placeholder answers that fail Tier 2 acceptance criteria.
**Current state**: Bridge now files as **Tier 1** with `evidence_tier: 4` and explicit language: "This is a gap signal... requires a domain expert or agent to enrich." The answer text is >100 chars (it's a detailed gap signal description with context).

This is the correct design: gap signals enter as Tier 1, get enriched by an agent, then re-filed as Tier 2 for voting. Not a bug — it's the intended workflow.

### ~~Issue 3 (HIGH): record_vote.py import bug~~ → RESOLVED

**Original finding**: `from file_proposal import ...` breaks if run from outside `scripts/`.
**Current state**: Line 175 has `sys.path.insert(0, str(Path(__file__).resolve().parent))` before the import. Fixed.

### ~~Issue 4 (MEDIUM): No expiry enforcement~~ → RESOLVED

**Original finding**: No mechanism to expire proposals past 14 days.
**Current state**: `file_proposal.py` has:
- `--check-expiry` flag (line 323-346)
- Sets `expires` field on filing (line 258-260, 14 days from now)
- `check_expiry()` scans proposals, marks expired, archives them, regenerates queue
- Tested: `python3 scripts/file_proposal.py --check-expiry` runs clean (0 expired, 26 remaining — all filed Apr 4, not yet past 14 days)

**Remaining gap**: No cron job or hook to run this automatically. Must be invoked manually. Not a code bug — an operational gap.

### ~~Issue 5 (MEDIUM): No resubmission limit tracking~~ → RESOLVED

**Original finding**: Nothing tracks submission count per topic.
**Current state**: Lines 262-278 in `file_proposal.py`:
- Checks `resubmission_of` field
- Counts archived proposals in the same chain
- Rejects if count >= 3
- Sets `resubmission_count` on the proposal

Implemented correctly per governance model.

### ~~Issue 6 (MEDIUM): Promote always appends to gap_additions~~ → RESOLVED

**Original finding**: All promoted entries go to `gap_additions` regardless of type.
**Current state**: Lines 120-124 in `promote_proposal.py`:
- Reads `target_section` from proposal (defaults to `gap_additions`)
- Validates against the 3 valid sections
- Appends to the correct section

Fixed.

### ~~Issue 7 (LOW): `fix` type in code but not in governance doc~~ → RESOLVED

**Original finding**: Code allows `fix` type but governance doc didn't list it.
**Current state**: Governance model line 252 now reads: `type: "new|modify|remap|retag|fix"` with comment `# fix = Tier 1 corrections`. Consistent.

### ~~Issue 8 (LOW): wiki/index.md doesn't link to proposed/~~ → RESOLVED

**Original finding**: No link to pending proposals from the wiki index.
**Current state**: `wiki/index.md` now contains:
```
## Pending Proposals
Governance proposals awaiting review: [Approval Queue](proposed/APPROVAL_QUEUE.md)
```

Fixed.

---

## NEW Issues Found (2026-04-07 re-audit)

### NEW Issue 9 (MEDIUM): 26 stress-test proposals sitting in proposed/ with status "approved"

Gemini filed 109 stress-test proposals (PROP-087 through PROP-109 remain in `proposed/`, 83 were archived). All 26 remaining have `status: approved` with 3 binding votes each. They were never promoted or cleaned up.

These are test data, not real KL candidates. Their content is: "This is a comprehensive stress test answer that is guaranteed to be over one hundred characters long..."

**Impact**: Pollutes the approval queue. `APPROVAL_QUEUE.md` shows 26 pending proposals that are actually test artifacts. Any agent checking the queue sees noise.

**Fix**: Either promote them (they'll add garbage to the KL) or archive them with `status: test_completed`. Archiving is correct — they served their purpose.

### NEW Issue 10 (MEDIUM): Rendered .md files for proposals show stale vote counts

The rendered page header says `votes: 3 approve, 0 object` but the format string in `render_proposed_page()` (line 153) outputs `votes: {binding}/{total_binding} binding approve` — a different format than what's on disk. The `.md` files were regenerated at some point with a different renderer version.

**Impact**: Cosmetic inconsistency. The YAML is the source of truth, not the .md. But it's confusing if someone reads the .md.

**Fix**: Run `python3 scripts/file_proposal.py --regenerate-queue` to rebuild all rendered pages from current YAML state.

### NEW Issue 11 (LOW): `notify_bus()` duplicated across 3 scripts

Each of `file_proposal.py`, `record_vote.py`, and `promote_proposal.py` has its own copy of `notify_bus()` with slightly different signatures. `file_proposal.py` takes `requires_ack` param, the others don't.

**Impact**: Maintenance burden. If the wire contract changes, 3 functions need updating.

**Fix**: Extract to a shared `governance_utils.py` module. Low priority — the current code works.

---

## Summary

| Issue | Severity | Status |
|-------|----------|--------|
| 1. Bus integration | HIGH | ✅ RESOLVED |
| 2. Bridge stub proposals | HIGH | ✅ RESOLVED (Tier 1 gap signals by design) |
| 3. Import bug | HIGH | ✅ RESOLVED |
| 4. Expiry enforcement | MEDIUM | ✅ RESOLVED (no cron — operational gap) |
| 5. Resubmission tracking | MEDIUM | ✅ RESOLVED |
| 6. Promote target section | MEDIUM | ✅ RESOLVED |
| 7. `fix` type consistency | LOW | ✅ RESOLVED |
| 8. Index link | LOW | ✅ RESOLVED |
| 9. Stale stress-test proposals | MEDIUM | 🔴 OPEN |
| 10. Rendered .md format drift | MEDIUM | 🔴 OPEN |
| 11. Duplicated notify_bus | LOW | 🔴 OPEN |

**Original 8 issues**: All resolved. The team fixed everything during the Apr 4 session.
**New issues**: 2 MEDIUM + 1 LOW found on re-audit. Issue 9 (stress-test cleanup) is the most actionable.

---

## Recommendation for Claude

The health_check.py Section 8 and total_health_check.py Section 13 that you wrote should be safe — the 3 HIGH issues that could have affected them are all resolved. The pipeline is functional.

The one thing to address before V3: archive the 26 stress-test proposals (Issue 9). They're approved test data sitting in the live queue.

---

*Re-audited 2026-04-07 by kiro.design. Original bus message fbc6af7a was consumed before delivery — this file is the canonical record.*
