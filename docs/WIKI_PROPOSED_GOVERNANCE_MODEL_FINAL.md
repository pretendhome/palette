# wiki/proposed/ Governance Model — Final Version

**Author**: kiro.design (incorporating feedback from claude.analysis, gemini.specialist, codex.implementation, and the operator's decisions)
**Date**: 2026-04-03
**Status**: FINAL — pending the operator signature
**Decision type**: 🚨 ONE-WAY DOOR
**Votes**: Gemini APPROVE (conditional), Claude APPROVE (with issues, all resolved below), Codex OBJECT-WITH-ALTERNATIVE (transport failure — payload empty, treated as advisory)

---

## Design Principle

The secret sauce of Palette has always been slowing things down, not speeding them up. Convergence before execution. Semantic blueprints before code. ONE-WAY DOOR gates before irreversible action.

This governance model is the convergence machine for autonomous knowledge changes. Agents CAN move fast — but unanimous vote forces them to slow down and actually converge before anything changes. The gradient descent resolution process doesn't exist to speed up decisions. It exists to make sure the decision that emerges is one that every agent can stand behind.

---

## Three Tiers of Change

### Tier 1: Obviously Right (any single agent, no vote needed)

Changes where the correct answer is objectively verifiable and the risk of being wrong is zero.

**Examples:**
- Typographic error: "recieve" → "receive"
- Broken URL: link returns 404, replacement is the same content at a new address
- Factual anachronism: referencing LLMs in a context predating computers
- Arithmetic error: text says 120 when the source file contains 121
- Dead reference: source retracted or domain expired, replacement is the archived version

**The bar**: A reasonable person reading the before and after would say "obviously, yes" with zero hesitation. If you have to argue why it's correct, it's not Tier 1.

**Process**:
1. Agent makes the fix in source YAML
2. Agent runs a dry-run recompile to verify no schema breakage (per Gemini)
3. If recompile passes: apply, log in `proposed/archive/` with fix, agent, timestamp
4. If recompile fails: escalate to Tier 2

**Retroactive challenge**: Any agent may challenge a Tier 1 fix within 7 days by filing a bus message with the original fix ID, the reason for challenge, and a proposed reversion. The fix remains live during challenge review. The challenge triggers a Tier 2 vote on the original fix. (Per Claude Issue 5.)

### Tier 2: Two-Way Door (unanimous agent vote required)

Changes that are reversible but involve judgment.

**Examples:**
- New KL entry proposed from voice interaction or workspace feedback
- Adding a source citation to an existing entry
- Modifying an answer to incorporate new information
- Adding or changing related_rius mappings
- Changing tags or journey stage classification

**Voting eligibility**: Only agents at WORKING or PRODUCTION trust tier (per assumptions.md Section 3) cast binding votes. UNVALIDATED agents may participate in discussion, file proposals, and vote — but their votes are recorded as advisory and do not count toward or against the unanimous threshold. An UNVALIDATED agent cannot veto. (Per Claude Issue 1.)

**Voting roster** (canonical KL):
- claude.analysis (WORKING)
- kiro.design (WORKING)
- codex.implementation (WORKING)

Roster changes are Tier 3 (human approval). Adding or removing a voter changes the power dynamics. (Per Claude Issue 2.)

**Quorum**: Minimum 2 binding votes required for any Tier 2 decision. If the roster drops below 3 agents, all Tier 2 changes escalate to the operator until the roster is restored.

**The process:**

1. **Propose**: Any agent files a proposed entry in `wiki/proposed/` with the standard schema.

2. **Vote** (48-hour window): Every roster agent must vote. Votes are:
   - `approve` — I agree this should be promoted.
   - `object` — I disagree. This blocks promotion and escalates to human review.
   - `object-with-alternative` — I disagree AND here is my proposed solution. Triggers the resolution process.

3. **Abstain-timeout rule**: If an agent does not vote within 48h, their vote is recorded as `abstain-timeout`. Abstain-timeout does NOT block promotion if: (a) all non-abstaining voters voted unanimously APPROVE, AND (b) at least 2 binding votes were cast. If abstain-timeout reduces binding votes below 2, escalate to the operator. (Per Claude Issue 3.)

4. **Outcome**:
   - **Unanimous approve** (from binding voters, quorum met) → auto-promote to KL. Recompile wiki. Log in `proposed/archive/`.
   - **Any single binding objection** → escalate to the operator. The objecting agent's reasoning and proposed alternative (if any) are included.

**Proposer voting**: At current scale (3 agents), the proposing agent's vote counts. When the roster reaches 5+, revisit recusal. (Per Claude Issue 6.)

**Expiry**: Tier 2 proposals expire after 14 days without unanimous approval. Can be resubmitted.

### Tier 3: One-Way Door (human approval required, always)

Changes that are irreversible or structurally consequential.

**Examples:**
- Removing a KL entry
- Changing an evidence tier downward
- Modifying the taxonomy (adding/removing RIUs)
- Changing the governance model itself
- Any change to the voting roster or promotion rubric

**Rule**: Agents may propose and discuss. Agents may vote to signal consensus. But the operator approves or rejects. No auto-promotion regardless of vote outcome.

**Cooling-off period**: Tier 3 decisions take effect 24h after the operator's approval to ensure all agents' runtime caches are synchronized. (Per Gemini.)

---

## The Resolution Process (Gradient Descent for Decisions)

When agents disagree on a Tier 2 change, the disagreement is signal, not failure.

### How it works:

1. **Agent A proposes** a change.
2. **Agent B objects with alternative** — "I disagree because X. Here is my proposed solution Y."
3. **Now there are two proposals.** Both agents must articulate:
   - What problem does your version solve?
   - What evidence supports it?
   - What is the risk of the other version?
4. **All other agents vote** on which proposal is stronger. This is information gathering, not majority-rules.
5. **The proposers may revise.** Proposals converge through iteration.
6. **Vote again.** If unanimous on either version → promote. If still split → game theory escalation.

### Game Theory Escalation

If two proposals remain deadlocked after one round of revision:

1. Both proposing agents present their final case.
2. ALL agents (including proposers) cast a final vote with written reasoning.
3. The full record — both proposals, all votes, all reasoning — goes to the operator.
4. The operator decides. The decision is logged in `decisions.md` as a precedent.

**N=2 deadlock rule**: If only 2 agents are active and they disagree, a mandatory 24h convergence window applies — both proposers must attempt to merge their diffs before human escalation. (Per Gemini.)

Precedents matter. Similar future disagreements reference the decision, reducing re-litigation.

---

## Workspace KL Governance (Lighter Process)

Workspace-specific knowledge (rossi, oil-investor, fde-toolkit, known-marketing) gets a lighter process. (Per the operator Q2.)

| Tier | What | Who | Window |
|------|------|-----|--------|
| W1 | Workspace fix (typo, broken link) | Any agent | Immediate |
| W2 | Workspace addition/modification | Workspace owner + 1 other agent | 24h |
| W3 | Workspace deletion or structural change | the operator | No expiry |

- Abstain-timeout does NOT block W2 (workspace iteration cannot stall on offline agents)
- Each workspace config defines which agents are workspace-active
- **Promotion to canonical KL**: If a workspace entry proves valuable across 2+ workspaces, any agent may propose it as a Tier 2 canonical entry. Full governance applies.

---

## Proposed Entry Schema

```yaml
id: PROP-001
proposed_by: kiro.design
proposed_at: 2026-04-03T16:45:00Z
tier: 2                          # 1 | 2 | 3
type: new_kl_entry               # new_kl_entry | correction | new_mapping | new_source | fix
target: LIB-NEW                  # existing ID for corrections, LIB-NEW for new entries
content:
  question: "..."
  answer: "..."
  sources:
    - title: "..."
      url: "..."
  related_rius: [RIU-XXX]
  evidence_tier: 2
  evidence_tier_justification: "Primary source from AWS documentation (Tier 1 vendor)"
  tags: [...]
rationale: "What gap this fills or what error this corrects"
source_of_insight: "voice interaction | agent analysis | workspace feedback | semantic audit"
contradiction_check:
  checked_against: [LIB-045, LIB-067]
  conflicts_found: none
votes:
  - agent: claude.analysis
    trust_tier: WORKING
    vote: approve
    reasoning: "Source verified. Maps correctly to RIU-XXX. No contradiction."
    date: 2026-04-04
  - agent: kiro.design
    trust_tier: WORKING
    vote: approve
    reasoning: "Fills gap identified in coverage report."
    date: 2026-04-04
  - agent: gemini.specialist
    trust_tier: UNVALIDATED
    vote: approve
    reasoning: "Consistent with domain knowledge."
    binding: false  # advisory only
    date: 2026-04-04
status: promoted                 # proposed | voting | approved | escalated | promoted | rejected | expired
resolution: null                 # or: { round: 2, alternatives: [...], final_vote: {...} }
promoted_at: 2026-04-05T10:00:00Z
```

(Schema includes `evidence_tier_justification` and `contradiction_check` per Claude Issue 4.)

---

## Human Approval Queue

File: `wiki/proposed/APPROVAL_QUEUE.md` (auto-generated, DO_NOT_EDIT)

Priority-sorted list of everything awaiting the operator's review. (Per the operator Q3.)

```
[EXPIRES in 3d] PROP-007: Add KL entry on multi-agent orchestration patterns
  Tier: 2 | Proposed by: kiro.design | Votes: 2/3 approve, 1 object
  Objection: claude.analysis — "Source is blog post, not primary documentation"
  Action needed: resolve objection or approve/reject

[TIER 3] PROP-012: Remove LIB-084 (game engine entry, out of scope)
  Proposed by: claude.analysis | Votes: 3/3 signal approve
  Action needed: the operator approves or rejects
```

Regenerated every time a proposal is filed, voted on, or expires. The operator can scan in 60 seconds.

---

## Compiled Proposed Entries

Proposed entries are compiled into `wiki/proposed/` with a PROPOSED banner. (Per the operator Q4.)

```markdown
---
STATUS: PROPOSED — NOT YET IN CANONICAL KNOWLEDGE LIBRARY
proposed_by: kiro.design
votes: 2/3 approve
expires: 2026-04-17
---
```

When promoted: moved to `wiki/entries/`, banner removed, standard frontmatter applied.
When rejected or expired: moved to `wiki/proposed/archive/`.

---

## Review Trigger (Sunset Clause)

After every 20 processed Tier 2 proposals, this governance model is automatically flagged for human review. (Per the operator Q1.)

The review considers:
- Promotion rate (succeeded vs failed vs expired)
- Veto patterns (is one agent blocking disproportionately?)
- Precedent utility (are logged precedents reducing re-litigation?)
- Time-to-resolution (are proposals resolving faster over time?)

The operator may amend the model at review. Amendments are Tier 3.

---

## Acceptance Criteria for Agent Reviewers

When voting on a Tier 2 proposal, each agent evaluates:

1. **Has source**: At least one citation with a verifiable URL
2. **No contradiction**: Does not conflict with existing KL entries (must fill `contradiction_check`)
3. **Valid mapping**: Maps to at least one real RIU in the taxonomy
4. **Tier justified**: Evidence tier matches source quality (must fill `evidence_tier_justification`)
5. **Substantive**: Answer is >100 words and actionable

An agent MUST object if any criterion fails. An agent SHOULD object-with-alternative if they see a better way.

---

## Summary

| Tier | What | Who decides | Process |
|------|------|-------------|---------|
| 1 | Obviously right | Any single agent | Fix + dry-run recompile + log. 7-day challenge window. |
| 2 | Two-way door | All WORKING+ agents unanimously | Propose → 48h vote → unanimous = promote, any objection = escalate |
| 3 | One-way door | the operator | Agents signal, the operator decides. 24h cooling-off. |
| W1 | Workspace fix | Any agent | Same as Tier 1 |
| W2 | Workspace change | Owner + 1 agent | 24h vote, no abstain-blocking |
| W3 | Workspace structural | the operator | Same as Tier 3 |

---

## Feedback Incorporated

| Source | Feedback | Resolution |
|--------|----------|------------|
| Gemini | Dry-run recompile for Tier 1 | Added to Tier 1 process |
| Gemini | Define "active" status | Replaced with fixed voting roster |
| Gemini | N=2 deadlock handling | Added 24h convergence window |
| Gemini | Tier 3 cooling-off period | Added 24h after the operator approval |
| Claude Issue 1 | Trust tier interaction | UNVALIDATED = advisory only, no veto |
| Claude Issue 2 | Quorum definition | Fixed roster, min 2 binding votes |
| Claude Issue 3 | Abstain-timeout deadlock | Non-blocking if quorum ≥ 2 unanimous |
| Claude Issue 4 | Missing schema fields | Added evidence_tier_justification + contradiction_check |
| Claude Issue 5 | Retroactive challenge process | 7-day window, challenge triggers Tier 2 vote |
| Claude Issue 6 | Conflict of interest | Proposer votes at current scale, revisit at 5+ |
| the operator Q1 | Sunset clause | Review after every 20 proposals |
| the operator Q2 | Workspace KL governance | Lighter W1/W2/W3 process |
| the operator Q3 | Approval queue | APPROVAL_QUEUE.md auto-generated |
| the operator Q4 | Compile proposed entries | Yes, with PROPOSED banner |
| Codex | Object-with-alternative | Transport failure (empty payload). Codex should review this final version and confirm or re-object. |

---

*This document is ready for the operator's signature. It is itself a Tier 3 decision.*
