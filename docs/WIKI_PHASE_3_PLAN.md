# Wiki Phase 3: Voice Feedback Loop — Implementation Plan

**Author**: kiro.design
**Date**: 2026-04-03
**Status**: READY AFTER GOVERNANCE SIGN-OFF
**Decision type**: 🔄 TWO-WAY DOOR
**Depends on**: Phase 1 (DONE), Phase 2 (DONE), Governance Model v1 (FINAL -- pending the operator signature)

---

## What Phase 3 Is

Voice interactions and workspace feedback generate proposed knowledge updates that flow into `wiki/proposed/`, get voted on by agents per the governance model, and either auto-promote to the canonical KL or escalate to the operator.

This is the feedback loop that makes Palette self-improving.

---

## What Already Exists

| Component | Status | Location |
|---|---|---|
| Governance model (tiers, voting, resolution) | FINAL -- pending signature | `docs/WIKI_GOVERNANCE_MODEL_v1.md` |
| Voting roster | DONE | `wiki/proposed/VOTING_ROSTER.yaml` |
| Proposed entry schema | DEFINED | Governance model Section 5 |
| Canvas enrichment pipeline | EXISTS (460 lines) | `scripts/enrichment/canvas_enrichment.py` |
| Workspace feedback data | 22 entries (21 oil-investor, 1 rossi) | `workspaces/*/palette_feedback.yaml` |
| Pending review queue | 6 signals queued | `scripts/enrichment/pending_review.yaml` |
| Wiki compiler | DONE (8/8 validation) | `scripts/compile_wiki.py` |
| Wiki validator | DONE (8 checks) | `scripts/validate_wiki.py` |
| `wiki/proposed/` directory | EXISTS (empty except roster) | `wiki/proposed/` |

## Preconditions

Before implementation starts, lock the governance contract:

1. The operator signs Governance Model v1.
2. `wiki/proposed/VOTING_ROSTER.yaml` and the proposed-entry schema are treated as frozen inputs for the first implementation pass.
3. Phase 3 tooling must preserve deterministic compile output, validator cleanliness, and append-only archive behavior established in Phases 1 and 2.

## What Needs to Be Built

### 1. Compiler/Validator Support for Proposed Entries

Before proposal automation, the compiler and validator need explicit support for governed proposed-entry YAML and archive semantics:
- Accept the governance proposal schema as a first-class input surface
- Validate schema conformance before vote requests are emitted
- Fail closed on malformed proposal status, votes, or roster references
- Preserve deterministic rebuild behavior and append-only archive expectations

### 2. Proposal Filing Script (`scripts/file_proposal.py`)

Takes a proposed entry (from any source — agent, enrichment pipeline, CLI) and:
- Validates against the governance schema (Section 5)
- Assigns a PROP-ID (`PROP-YYYY-MM-DD-NNN`)
- Writes to `wiki/proposed/PROP-YYYY-MM-DD-NNN.yaml`
- Compiles a proposed wiki page with PROPOSED banner into `wiki/proposed/PROP-YYYY-MM-DD-NNN.md`
- Posts a vote request to the peers bus
- Regenerates APPROVAL_QUEUE.md

### 3. Vote Recording Script (`scripts/record_vote.py`)

Takes a vote (from bus message or CLI) and:
- Validates vote format (approve/object/object-with-alternative + reasoning)
- Checks voter is on the roster and binding
- Appends vote to the proposal YAML
- Checks if unanimous + quorum met → auto-promote
- Checks if objection → escalate or trigger gradient descent
- Regenerates APPROVAL_QUEUE.md

### 4. Promotion Script (`scripts/promote_proposal.py`)

When a proposal achieves unanimous binding approval:
- Appends the entry to `palette_knowledge_library_v1.4.yaml`
- Moves proposal to `wiki/proposed/archive/`
- Recompiles wiki
- Runs validation (8/8 must pass)
- Posts confirmation to bus

### 5. Bridge: Enrichment Pipeline → Governance

The existing `canvas_enrichment.py` outputs to `pending_review.yaml`. Phase 3 bridges this to the governance model:
- `concept_exposure` signals with sufficient depth → file as Tier 2 proposals
- `kl_candidate` entries → file as Tier 2 proposals
- `mastery_signal` entries → file as Tier 1 fixes (update learner state)

### 6. APPROVAL_QUEUE.md Generator

Auto-generates the human-readable queue per governance Section 6.

Compiler rendering of `wiki/proposed/*.yaml` as browsable pages with PROPOSED banner is part of the compiler/validator support gate above, not a later optional step.

---

## Execution Order

```
0. Governance v1 sign-off and contract freeze
1. Compiler/validator support for proposed-entry schema and `wiki/proposed/` rendering
2. file_proposal.py (core filing path + queue regeneration)
3. record_vote.py (voting loop + malformed vote handling)
4. promote_proposal.py (promotion, archive, recompile, validate)
5. Bridge: enrichment → governance
6. End-to-end test: file a real proposal from oil-investor feedback
```

---

## Estimated Effort

| Task | Effort |
|---|---|
| Compiler/validator support | 45m |
| file_proposal.py | 1h |
| record_vote.py | 1h |
| promote_proposal.py | 30m |
| APPROVAL_QUEUE.md generator | built into filing/voting scripts |
| Enrichment bridge | 30m |
| End-to-end test | 30m |
| **Total** | **~4.25h** |

---

*Ready to build after governance sign-off.*
