# Kiro Governance Pipeline Audit — 2026-04-04

**Auditor**: kiro.design
**Scope**: `scripts/file_proposal.py`, `scripts/record_vote.py`, `scripts/promote_proposal.py`, `scripts/bridge_feedback_to_proposals.py`
**Reference**: `docs/WIKI_GOVERNANCE_MODEL_v1.md`

---

## 8 Issues Found (3 HIGH, 3 MEDIUM, 2 LOW)

### HIGH — Will cause real failures

**Issue 1: Bus integration missing from pipeline**
- `file_proposal.py`, `record_vote.py`, `promote_proposal.py` have zero bus calls
- The governance model assumes agents discover proposals via the peers bus
- Pipeline is CLI-only — agents can't find proposals unless they check the filesystem
- Fix: add bus notification on file (vote request), on vote (outcome), on promote (announcement)

**Issue 2: Bridge creates stub proposals that fail acceptance criteria**
- `bridge_feedback_to_proposals.py` generates placeholder answers ("This entry was auto-generated...")
- These are under 100 words of real content
- Criterion #5 (substantive, >100 words) will fail on vote
- The 20 oil-investor feedback entries will ALL fail
- Fix: either generate real content, or file as gap-detected signals (not Tier 2 proposals)

**Issue 3: record_vote.py import bug**
- Line: `from file_proposal import render_proposed_page, generate_approval_queue`
- Breaks if run from any directory other than `scripts/`
- Fix: add `sys.path.insert(0, str(Path(__file__).resolve().parent))` before the import

### MEDIUM — Governance says it, code doesn't enforce it

**Issue 4: No expiry enforcement**
- Governance model specifies 14-day expiry for Tier 2 proposals
- No cron job, no script, no check enforces this
- Proposals sit in `proposed/` forever
- Fix: add `--check-expiry` flag to `file_proposal.py` or create `expire_proposals.py`

**Issue 5: No resubmission limit tracking**
- Governance model specifies max 3 attempts per topic
- Nothing in the schema or scripts tracks submission count
- Fix: add `resubmission_of` field to schema, check count in `file_proposal.py`

**Issue 6: Promote always appends to gap_additions**
- `promote_proposal.py` line: `kl.setdefault("gap_additions", []).append(entry)`
- Every promoted entry goes to `gap_additions` regardless of type
- Some entries should go to `library_questions`
- Fix: add `target_section` field to proposal schema, default to `gap_additions`

### LOW — Inconsistencies

**Issue 7: `fix` type in code but not in governance doc**
- `file_proposal.py` VALID_TYPES includes `fix`
- Governance model Section 5 schema says `new|modify|remap|retag`
- Fix: add `fix` to governance doc (it's a valid type for Tier 1 corrections)

**Issue 8: Main wiki index doesn't link to proposed/**
- `wiki/index.md` has no mention of proposed entries
- Governance model says proposed entries should be browsable
- Fix: add "Pending Proposals" section to index linking to `proposed/APPROVAL_QUEUE.md`

---

## Recommendation

Fix Issues 1-3 now (HIGH — prevents real failures, ~1h total).
Issues 4-6 go on V3 backlog.
Issues 7-8 are Tier 1 fixes anyone can do.

---

*Written to disk per Claude's request (bus messages are ephemeral, audit findings are artifacts).*
