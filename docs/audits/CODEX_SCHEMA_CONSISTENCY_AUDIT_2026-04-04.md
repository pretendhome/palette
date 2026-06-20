# Codex Schema Consistency Audit — 2026-04-04

Author: codex.implementation  
Scope: consistency across the canonical knowledge library, wiki compiler, governance proposal schema, promotion path, and voting roster contract.

## Verdict

The voting roster contract is clean.

The main remaining inconsistencies are between:
- the governance proposal schema in `docs/WIKI_GOVERNANCE_MODEL_v1.md`
- the canonical KL structure in `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`
- the promotion path in `scripts/promote_proposal.py`
- the proposed-entry rendering path in `scripts/compile_wiki.py`

Two of the issues below are operational, not just documentary.

## Findings

### 1. High — Proposal schema is not lossless relative to canonical KL

Files:
- `docs/WIKI_GOVERNANCE_MODEL_v1.md`
- `scripts/compile_wiki.py`
- `scripts/promote_proposal.py`

Evidence:
- `docs/WIKI_GOVERNANCE_MODEL_v1.md:255-269` defines proposal `content` with:
  - `question`
  - `answer`
  - `sources`
  - `related_rius`
  - `evidence_tier`
  - `evidence_tier_justification`
  - `tags`
- `scripts/compile_wiki.py:255-262` reads canonical KL entries with:
  - `question`
  - `answer`
  - `sources`
  - `related_rius`
  - `journey_stage`
  - `tags`
  - `difficulty`
- `scripts/promote_proposal.py:54-65` promotes proposals by inventing defaults for:
  - `journey_stage = "foundation"`
  - `difficulty = "medium"`
  and drops other canonical conventions such as `problem_type` and `industries` entirely.

Why this matters:
- A proposal cannot currently round-trip into the canonical KL without either:
  - silent data loss, or
  - invented defaults.
- That means the proposal schema is not a full write contract for the canonical library.

Recommendation:
- Either extend the governance proposal schema so it can promote losslessly into canonical KL, or
- explicitly define a normalization layer and document which canonical fields may be omitted or defaulted.

### 2. High — `evidence_tier` is written into canonical KL, but compiler ignores it

Files:
- `docs/WIKI_GOVERNANCE_MODEL_v1.md`
- `scripts/promote_proposal.py`
- `scripts/compile_wiki.py`

Evidence:
- `docs/WIKI_GOVERNANCE_MODEL_v1.md:265-266` defines `content.evidence_tier` and `content.evidence_tier_justification` in the proposal schema.
- `scripts/promote_proposal.py:60` writes `evidence_tier` into the canonical KL entry.
- `scripts/compile_wiki.py:278-291` recomputes evidence tier from source tiers / heuristics and never reads `entry.get("evidence_tier")`.

Why this matters:
- Canonical KL now has a field that the compiler does not treat as authoritative.
- This creates schema drift and ambiguous ownership:
  - is evidence tier a promoted canonical field, or
  - is it always derived from sources at compile time?

Recommendation:
- Choose one model and enforce it consistently:
  - If evidence tier is canonical, compiler should honor the top-level field when present.
  - If evidence tier is derived, promotion should not write a top-level canonical `evidence_tier`.

### 3. Medium — Proposed-entry rendering under-implements the governance schema

Files:
- `docs/WIKI_GOVERNANCE_MODEL_v1.md`
- `scripts/compile_wiki.py`

Evidence:
- `docs/WIKI_GOVERNANCE_MODEL_v1.md:332-339` says compiled proposed entries should include frontmatter with:
  - `STATUS`
  - `proposed_by`
  - `votes`
  - `expires`
- `scripts/compile_wiki.py:595-609` renders proposed entries with only:
  - `STATUS`
  - `proposed_by`
  - binding approve count
  - question
  - tier
  - type
  - answer
- It ignores proposal fields that are part of the governance contract, including:
  - `sources`
  - `related_rius`
  - `evidence_tier`
  - `contradiction_check`
  - richer vote status
  - `expires`

Why this matters:
- The governance doc promises a richer compiled proposed-entry surface than the compiler actually emits.
- This is currently more of a contract/documentation mismatch than a data-integrity failure, but it will confuse reviewers and weaken the proposal UX.

Recommendation:
- Either narrow the governance doc to the current minimalist render contract, or
- extend proposed-entry rendering to reflect the schema the governance model says exists.

### 4. Low — Approval queue example still uses `KL-168`

File:
- `docs/WIKI_GOVERNANCE_MODEL_v1.md`

Evidence:
- `docs/WIKI_GOVERNANCE_MODEL_v1.md:319` uses `Target: KL-168` in the queue example.
- Current canonical ID convention elsewhere is `LIB-XXX`.

Why this matters:
- Small issue, but it reintroduces naming drift the governance cleanup had already removed elsewhere.

Recommendation:
- Change `KL-168` to `LIB-168` in the approval queue example.

### 5. Low — Voting roster contract is internally consistent

Files:
- `docs/WIKI_GOVERNANCE_MODEL_v1.md`
- `wiki/proposed/VOTING_ROSTER.yaml`

Evidence:
- `docs/WIKI_GOVERNANCE_MODEL_v1.md:280-286` uses `votes[].agent_id`.
- `wiki/proposed/VOTING_ROSTER.yaml:4-27` uses `agent_id` consistently for both binding and advisory agents.

Why this matters:
- This confirms the earlier roster field-name mismatch has actually been resolved.

Recommendation:
- No further change needed on the roster contract from the Codex side.

## Summary

The roster contract is clean.

The main remaining schema issue is that the governance proposal layer, the promotion layer, and the canonical KL layer do not yet share one fully consistent write contract.

If this is left unresolved:
- proposals will continue to promote with invented defaults
- canonical entries may accumulate fields the compiler does not treat as authoritative
- proposed-entry pages will continue to underrepresent proposal state relative to the governance model
