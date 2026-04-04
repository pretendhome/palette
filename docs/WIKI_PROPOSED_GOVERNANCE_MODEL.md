# wiki/proposed/ Governance Model — Consensus Protocol

**Author**: kiro.design (consolidating the operator's design direction)
**Date**: 2026-04-03
**Status**: DRAFT — pending team vote
**Decision type**: 🚨 ONE-WAY DOOR

---

## The Model: Unanimous Consensus with Veto Escalation

Every proposed change to the Palette knowledge base follows one path. The path has gates. The gates are defined by the nature of the change and the degree of agreement among agents.

---

## Three Tiers of Change

### Tier 1: Obviously Right (any single agent, no vote needed)

Changes where the correct answer is objectively verifiable and the risk of being wrong is zero.

**Examples:**
- Typographic error: "recieve" → "receive"
- Broken URL: link returns 404, replacement is the same content at a new address
- Factual anachronism: referencing LLMs in a context predating computers
- Arithmetic error: "121 RIUs" when the taxonomy file contains 121 entries and the text says 120
- Dead reference: source was retracted or domain expired, replacement is the archived version

**The bar**: A reasonable person reading the before and after would say "obviously, yes" with zero hesitation. If you have to argue why it's correct, it's not Tier 1.

**Rule**: Any single agent may fix and recompile. Log the change in `proposed/archive/` with the fix, the agent, and the timestamp. No vote. No review. But any other agent may retroactively challenge — if challenged, the fix is reverted and escalated to Tier 2.

### Tier 2: Two-Way Door (unanimous agent vote required)

Changes that are reversible but involve judgment — adding content, modifying answers, creating mappings, adding sources.

**Examples:**
- New KL entry proposed from voice interaction or workspace feedback
- Adding a source citation to an existing entry
- Modifying an answer to incorporate new information
- Adding or changing related_rius mappings
- Changing tags or journey stage classification

**The process:**

1. **Propose**: Any agent files a proposed entry in `wiki/proposed/` with the standard schema (see below).

2. **Vote**: Every active agent must vote. No abstentions. Votes are: `approve`, `object`, or `object-with-alternative`.
   - `approve`: I agree this should be promoted.
   - `object`: I disagree. This blocks promotion and escalates to human review.
   - `object-with-alternative`: I disagree AND here is my proposed solution. This triggers the resolution process (see below).

3. **Outcome**:
   - **Unanimous approve** → auto-promote to KL. Recompile wiki. Log in `proposed/archive/`.
   - **Any single objection** → escalate to the operator. The objecting agent's reasoning and proposed alternative (if any) are included in the escalation.

**The veto principle**: Any single agent can block any Tier 2 change. This is by design. The cost of a false negative (good change delayed) is low. The cost of a false positive (bad change promoted) is high. Veto protects quality.

### Tier 3: One-Way Door (human approval required, always)

Changes that are irreversible or structurally consequential.

**Examples:**
- Removing a KL entry
- Changing an evidence tier downward (Tier 1 → Tier 2)
- Modifying the taxonomy (adding/removing RIUs)
- Changing the governance model itself
- Any change to the promotion rubric

**Rule**: Agents may propose and discuss. Agents may vote to signal consensus. But the operator approves or rejects. No auto-promotion regardless of vote outcome.

---

## The Resolution Process (Gradient Descent for Decisions)

When agents disagree on a Tier 2 change, the disagreement is not a failure — it's signal. The resolution process uses the disagreement to find a better answer.

### How it works:

1. **Agent A proposes** a change.
2. **Agent B objects with alternative** — "I disagree because X. Here is my proposed solution Y."
3. **Now there are two proposals.** Both agents must articulate their case:
   - What problem does your version solve?
   - What evidence supports it?
   - What is the risk of the other version?
4. **All other agents vote** on which proposal is stronger. This is not majority-rules — it's information gathering. The votes and reasoning are visible to everyone.
5. **The proposers may revise.** Agent A can incorporate Agent B's feedback. Agent B can incorporate Agent A's. The proposals converge.
6. **Vote again.** If unanimous on either version → promote. If still split → escalate to the operator with both proposals, all votes, and all reasoning.

This is gradient descent applied to decisions. Early iterations produce divergent proposals. Each round of argument and counter-argument reduces the distance between them. Eventually they converge on a solution that incorporates the best of both — or the disagreement is genuine and needs human judgment.

### Game Theory Escalation

If two proposals remain deadlocked after one round of revision:

1. Both proposing agents present their final case.
2. All agents (including the proposers) cast a final vote with written reasoning.
3. The full record — both proposals, all votes, all reasoning — goes to the operator.
4. The operator decides. The decision is logged in `decisions.md` as a precedent.

The precedent matters. Similar future disagreements can reference the decision, reducing the need to re-litigate.

---

## Proposed Entry Schema

```yaml
id: PROP-001
proposed_by: kiro.design
proposed_at: 2026-04-03T16:45:00Z
tier: 2                          # 1 = obviously right, 2 = two-way door, 3 = one-way door
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
  tags: [...]
rationale: "What gap this fills or what error this corrects"
source_of_insight: "voice interaction | agent analysis | workspace feedback | semantic audit"
votes:
  - agent: claude.analysis
    vote: approve
    reasoning: "Source verified. Maps correctly to RIU-XXX. No contradiction."
    date: 2026-04-04
  - agent: codex.implementation
    vote: approve
    reasoning: "Consistent with existing entries. Evidence tier justified."
    date: 2026-04-04
  - agent: kiro.design
    vote: approve
    reasoning: "Fills gap identified in coverage report."
    date: 2026-04-04
status: promoted                 # proposed | voting | approved | escalated | promoted | rejected | expired
resolution: null                 # or: { round: 2, alternatives: [...], final_vote: {...} }
promoted_at: 2026-04-05T10:00:00Z
```

---

## Review Cadence

- **Tier 1 fixes**: Immediate. Any agent, any time. Logged retroactively.
- **Tier 2 votes**: 48-hour voting window. All active agents must vote within the window. If an agent doesn't vote within 48h, their vote is recorded as `abstain-timeout` and does NOT count as approval — the change cannot auto-promote without explicit unanimous approval.
- **Tier 3 escalations**: the operator reviews when ready. No expiry on ONE-WAY DOOR proposals.
- **Expired proposals**: Tier 2 proposals expire after 14 days without unanimous approval. Can be resubmitted.

---

## Acceptance Criteria for Agent Reviewers

When voting on a Tier 2 proposal, each agent evaluates:

1. **Has source**: At least one citation with a verifiable URL
2. **No contradiction**: Does not conflict with existing KL entries
3. **Valid mapping**: Maps to at least one real RIU in the taxonomy
4. **Tier justified**: Evidence tier matches the source quality
5. **Substantive**: Answer is >100 words and actionable (not a stub, not marketing copy)

An agent MUST object if any criterion fails. An agent SHOULD object-with-alternative if they see a better way to address the same gap.

---

## What This Enables

- **Phase 3** (voice feedback): Voice interactions file Tier 2 proposals. Agents vote. Unanimous = auto-promote.
- **Phase 6** (memory promotion): mcp-memory-service files proposals into `proposed/`. Same voting process.
- **Flywheel feedback**: Mission Canvas palette_feedback.yaml entries become Tier 2 proposals.
- **Quality protection**: Any single agent can veto. The operator is the final arbiter on disagreements.
- **Learning**: Precedent decisions in `decisions.md` reduce future re-litigation. The system gets faster at deciding as it accumulates precedent.

---

## Summary

| Tier | What | Who decides | Process |
|------|------|-------------|---------|
| 1 | Obviously right (typos, broken links, factual errors) | Any single agent | Fix immediately, log it, retroactive challenge possible |
| 2 | Two-way door (new content, modifications, mappings) | All agents unanimously | Propose → vote → unanimous = promote, any objection = escalate |
| 3 | One-way door (deletions, tier changes, taxonomy, governance) | the operator | Agents discuss and vote to signal, the operator decides |

The gradient descent principle: disagreement produces better solutions. Objecting agents must propose alternatives. Proposals converge through iteration. Deadlocks go to human judgment and create precedent.

---

*Ready for team vote on this governance model itself (which is, fittingly, a Tier 3 decision — the operator approves).*

---

## Design Principle

The secret sauce of Palette has always been slowing things down, not speeding them up. Convergence before execution. Semantic blueprints before code. ONE-WAY DOOR gates before irreversible action.

This governance model applies the same principle to autonomous knowledge changes. Agents CAN move fast — but the unanimous vote requirement forces them to slow down and actually converge before anything changes. The gradient descent resolution process doesn't exist to speed up decisions. It exists to make sure the decision that emerges is one that every agent can stand behind.

Speed is easy. Convergence is hard. This is the convergence machine for autonomous knowledge governance.
