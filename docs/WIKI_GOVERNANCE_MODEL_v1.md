# Wiki Governance Model v1

| Field | Value |
|---|---|
| **Author** | claude.analysis, consolidating contributions from kiro.design, codex.implementation, gemini.specialist, mistral.specialist, and the operator |
| **Date** | 2026-04-03 |
| **Status** | FINAL -- ready for the operator signature |
| **Decision Type** | ONE-WAY DOOR |
| **Scope** | Governs all autonomous modifications to the Palette canonical knowledge library (170 entries) and workspace knowledge libraries |

---

## Design Principle

The secret sauce of Palette has always been slowing things down, not speeding them up. Convergence before execution. Semantic blueprints before code. ONE-WAY DOOR gates before irreversible action. This governance model is the convergence machine for autonomous knowledge changes.

---

## Table of Contents

1. [Three Tiers of Change](#1-three-tiers-of-change)
2. [Gradient Descent Resolution Process](#2-gradient-descent-resolution-process)
3. [Workspace Knowledge Library Governance](#3-workspace-knowledge-library-governance)
4. [Canonical Voting Roster](#4-canonical-voting-roster)
5. [Proposed Entry YAML Schema](#5-proposed-entry-yaml-schema)
6. [Approval Queue Specification](#6-approval-queue-specification)
7. [Compiled Proposed Entries](#7-compiled-proposed-entries)
8. [Acceptance Criteria](#8-acceptance-criteria)
9. [Review Trigger (Sunset Clause)](#9-review-trigger-sunset-clause)
10. [Operational Metrics](#10-operational-metrics)
11. [Edge Cases and Stress Testing](#11-edge-cases-and-stress-testing)
12. [Summary Table](#12-summary-table)
13. [Feedback Trail and Provenance](#13-feedback-trail-and-provenance)

---

## 1. Three Tiers of Change

### Summary

| Tier | Name | Approval | Auto-Promote | Examples |
|---|---|---|---|---|
| 1 | Obviously Right | Any single agent, no vote | Yes | Typos, broken URLs, arithmetic errors, dead references |
| 2 | Two-Way Door | Unanimous binding vote, quorum >= 2 | Yes | New KL entries, source citations, answer modifications, RIU mappings, tag/stage changes |
| 3 | One-Way Door | Human approval, always | No | Removing KL entries, downgrading evidence tiers, modifying taxonomy, changing governance model, changing voting roster or promotion rubric |

### Tier Dispute Rule

If agents disagree on whether a change belongs to Tier 1 or Tier 2 (or Tier 2 or Tier 3), **the higher tier applies immediately**. The change is processed at the higher tier while agents discuss classification. If Tier 3 is in dispute, the change goes directly to Tier 3 (the operator decides) — Tier 2 voting cannot determine whether Tier 3 safeguards apply.

---

### 1.1 Tier 1: Obviously Right

**Bar:** Changes that produce no semantic change, verifiable with zero hesitation. Typos, broken URLs, arithmetic errors, dead references.

**Process:**

1. Agent applies the fix to the relevant governed artifact (source YAML, workspace config, or governance document).
2. Agent runs: `python3 scripts/compile_wiki.py && python3 scripts/validate_wiki.py`
3. If both pass: apply the change. Log the fix in `wiki/proposed/archive/` with a Tier 1 record including the fix ID, agent, timestamp, and description.
4. If either fails: escalate to Tier 2. The compilation or validation failure indicates the change is not obviously right.

**Retroactive Challenge:**

- Any agent may challenge a Tier 1 fix within 7 calendar days of application.
- Challenge is filed as a bus message containing: original fix ID, reason for challenge, proposed reversion.
- The fix stays live during review. Reverting a live fix without consensus creates more risk than leaving it.
- A challenge triggers a Tier 2 vote on whether to revert.
- Challenges filed after day 7 are rejected. The fix is permanent. If an agent later discovers a problem, they must file a new proposal (Tier 1 or Tier 2 as appropriate) to correct it.

---

### 1.2 Tier 2: Two-Way Door

**Scope:** All changes that modify the semantic content of the knowledge library but are reversible. Examples: new KL entries, source citations, answer modifications, RIU mappings, tag changes, stage changes.

**Voting Eligibility:**

- Only agents at WORKING or PRODUCTION trust tier (per `assumptions.md` Section 3) cast **binding** votes.
- UNVALIDATED agents may participate in discussion, file proposals, and vote, but their votes are **advisory only** with no veto power.

**Fixed Voting Roster:**

The canonical voting roster is stored in machine-readable YAML at `wiki/proposed/VOTING_ROSTER.yaml`. This governance document summarizes the roster; runtime reads from the YAML file. Changes to the voting roster are Tier 3.

Current binding roster: claude.analysis (WORKING), kiro.design (WORKING), codex.implementation (WORKING).

**Quorum:** Minimum 2 binding votes required. If the roster drops below 3 binding agents, all Tier 2 proposals escalate to the operator.

**Voting Window:** 48 hours from proposal filing.

**Vote Options:**

| Vote | Meaning | Requirements |
|---|---|---|
| `approve` | Meets all acceptance criteria | None beyond the vote |
| `object` | Fails one or more acceptance criteria, cannot auto-promote | Mandatory written reasoning identifying which criteria fail |
| `object-with-alternative` | Gap is valid but proposed solution is not preferred | Must include a complete alternative proposal |

**Abstention Rules:**

| Abstention Type | Trigger | Effect |
|---|---|---|
| `abstain-timeout` | Agent does not vote within 48h | Does NOT block promotion if remaining binding votes are unanimous AND quorum >= 2. If binding votes drop below 2, escalate to the operator. |
| `abstain-transport-failure` | Vote filed with empty or malformed payload | Treated identically to abstain-timeout. Agent is notified and may re-vote within the original 48h window. |
| `abstain-malformed` | Vote filed without reasoning | Vote is invalid and not recorded as a binding vote. Agent is notified and may re-vote within the original 48h window. |

**Proposer Voting:** The proposing agent's vote counts as a binding vote (if the agent holds WORKING or PRODUCTION trust tier). This rule applies at the current scale of 3 agents. Revisit recusal requirements when the roster reaches 5 or more binding agents.

**Objection Semantics:**

- `object`: The proposal fails acceptance criteria and cannot auto-promote. The proposer may revise and resubmit within 24 hours (resubmission resets the 48h voting window). If the proposer does not resubmit within 24h, the proposal escalates to the operator.
- `object-with-alternative`: The identified gap is valid but the proposed solution is not preferred. This triggers the gradient descent resolution process (Section 2).

**Expiry:** A Tier 2 proposal expires after 14 days without unanimous binding approval. Expired proposals may be resubmitted as new proposals. See Section 11, Scenario 9 for resubmission limits.

**Outcome on Success:** Unanimous binding approval with quorum met triggers auto-promotion: the entry moves to canonical KL, recompilation runs, and the proposal is archived in `wiki/proposed/archive/`.

**Outcome on Objection:** Any single binding objection prevents auto-promotion. If not resolved through gradient descent within the 14-day window, the proposal escalates to the operator.

---

### 1.3 Tier 3: One-Way Door

**Scope:** Changes that are irreversible or structurally consequential. Examples: removing KL entries, downgrading evidence tiers, modifying taxonomy (including adding or removing RIUs), changing this governance model, changing the voting roster, changing the promotion rubric.

**Process:**

1. Any agent may propose a Tier 3 change.
2. All agents (binding and advisory) discuss and vote to signal preference.
3. The operator reviews the proposal, the discussion, and the signal votes.
4. The operator approves or rejects. There is no auto-promotion for Tier 3.
5. After the operator approves, a **24-hour cooling-off period** begins before the change takes effect.
6. During cooling-off, agents may raise critical flaws (see Section 11, Scenario 10). If a critical flaw is raised, the operator reviews and may withdraw approval.
7. After cooling-off completes without withdrawal, the change is applied, compiled, validated, and archived.

---

## 2. Gradient Descent Resolution Process

When an `object-with-alternative` vote is cast, the following resolution process begins. The goal is convergence, not speed.

### 2.1 Steps

**Step 1 -- Articulate.** Agent A (proposer) and Agent B (objector-with-alternative) each articulate in writing:
- What problem does this proposal solve?
- What evidence supports the proposed solution?
- What is the specific risk of the other agent's version?

**Step 2 -- Information Gathering.** All other agents (binding and advisory) vote on which articulation is stronger. This is information gathering, not majority-rules. The purpose is to surface considerations that either side may have missed.

**Step 3 -- Revise.** Both proposers may revise their proposals based on the feedback. Revisions should narrow the gap between the two versions.

**Step 4 -- Vote Again.** All binding agents vote on the revised proposals. If either version achieves unanimous binding approval with quorum, it is promoted. If still split, proceed to Step 5.

**Step 5 -- Game Theory Escalation.** Both agents present their final case. All agents cast a final vote with written reasoning. The full record (both proposals, all articulations, all votes, all reasoning) goes to the operator. The operator decides. The decision is logged as a precedent in `decisions.md`.

### 2.2 N=2 Deadlock Rule

If only 2 binding agents are participating (the third having abstained or being offline), and those 2 disagree, a **mandatory 24-hour convergence window** begins. Both agents must attempt to produce a merged proposal that addresses both sets of concerns. If they cannot converge within 24 hours, the full record escalates to the operator.

### 2.3 Amendment Consolidation

The original proposer is responsible for consolidating amendments from the gradient descent process into a revised proposal. If the amending agent disagrees with how their feedback was incorporated, they file a new objection on the consolidated version. This triggers another round of gradient descent. There is no infinite loop risk because the 14-day expiry applies to the original proposal date.

### 2.4 Precedent

Decisions logged in `decisions.md` serve as precedent. When a similar disagreement arises in the future, agents reference the precedent and its reasoning. Precedents do not expire. They are overruled only by new precedents created through the same process when circumstances change. The sunset review (Section 9) is the mechanism for evaluating whether existing precedents still apply.

---

## 3. Workspace Knowledge Library Governance

Workspace KLs (rossi, oil-investor, fde-toolkit, known-marketing) use a lighter governance process. Each workspace configuration file defines which agents are workspace-active.

### 3.1 Workspace Tiers

| Tier | Name | Approval | Window | Examples |
|---|---|---|---|---|
| W1 | Fix | Any single agent, immediate | None | Same scope as Tier 1: typos, broken URLs, dead references |
| W2 | Addition/Modification | Workspace owner + 1 other agent | 24h | New entries, modified answers, new sources |
| W3 | Deletion/Structural | the operator decides | No expiry | Removing entries, restructuring workspace KL |

**W2 Abstain-Timeout:** If the second agent does not vote within 24 hours, the abstain-timeout does NOT block promotion. The workspace owner's approval is sufficient after timeout.

### 3.2 Promotion from Workspace to Canonical KL

A workspace KL entry may be promoted to canonical KL when either condition is met:

- **Citation threshold:** The entry is cited by 2 or more entries in 2 or more different workspace KLs.
- **Decision reference:** The entry is explicitly referenced in a the operator-approved decision.

When either condition is met, any agent may propose the entry as a Tier 2 canonical proposal. Full canonical governance (Section 1.2) applies.

**Anti-gaming rule:** If a single agent added the entry to all citing workspaces, the citation threshold is not met. The entry must be independently cited by at least 2 different agents across 2 different workspaces, or meet the decision reference condition.

---

## 4. Canonical Voting Roster

The canonical voting roster is stored at `wiki/proposed/VOTING_ROSTER.yaml`. The governance document (this file) summarizes the roster for human readability. Runtime processes read from the YAML file. Any discrepancy between this document and the YAML file is resolved in favor of the YAML file.

**Roster YAML** (illustrative — the YAML file at `wiki/proposed/VOTING_ROSTER.yaml` is normative):

```yaml
roster:
  - agent_id: claude.analysis
    trust_tier: WORKING
    binding: true
    added_at: "2026-04-03T00:00:00Z"
    added_by: governance_model_v1
  - agent_id: kiro.design
    trust_tier: WORKING
    binding: true
    added_at: "2026-04-03T00:00:00Z"
    added_by: governance_model_v1
  - agent_id: codex.implementation
    trust_tier: WORKING
    binding: true
    added_at: "2026-04-03T00:00:00Z"
    added_by: governance_model_v1

quorum_minimum: 2

advisory_agents:
  - agent_id: gemini.specialist
    trust_tier: UNVALIDATED
    binding: false
  - agent_id: mistral.specialist
    trust_tier: UNVALIDATED
    binding: false
```

**Roster Change Rules:**

- Adding or removing agents from the roster is a Tier 3 change (requires the operator approval).
- Changing an agent's trust tier is a Tier 3 change.
- Changing the quorum minimum is a Tier 3 change.

---

## 5. Proposed Entry YAML Schema

Every proposed change to the canonical KL must be filed as a YAML document conforming to this schema. The schema applies to Tier 2 and Tier 3 proposals. Tier 1 fixes use a simplified log format (fix ID, agent, timestamp, description, files changed).

```yaml
id: "PROP-YYYY-MM-DD-NNN"          # Unique proposal ID
proposed_by: "agent.identity"       # Filing agent (e.g., claude.analysis)
proposed_at: "YYYY-MM-DDTHH:MM:SSZ" # ISO 8601 timestamp
tier: 2                             # 2 or 3
type: "new|modify|remap|retag|fix"   # Change type (fix = Tier 1 corrections)
target: "LIB-NNN or LIB-NEW"       # Existing KL ID for modifications, LIB-NEW for additions

content:
  question: "The KL question text"
  answer: "The KL answer text (>100 words, actionable)"
  sources:
    - url: "https://..."
      title: "Source title"
      accessed: "YYYY-MM-DD"
  related_rius:
    - "RIU-001"                     # Standard RIU IDs per taxonomy v1.3
    - "RIU-042"
  evidence_tier: 2                  # Numeric: 1, 2, 3, or 4 (matches KL convention)
  evidence_tier_justification: "Why this tier matches the source quality"
  journey_stage: "foundation"       # Optional: foundation|retrieval|orchestration|specialization (default: foundation)
  difficulty: "medium"              # Optional: easy|medium|hard (default: medium)
  tags:
    - "tag1"
    - "tag2"

rationale: "Why this change is needed"
source_of_insight: "What prompted this proposal"

contradiction_check:
  checked_against:
    - "LIB-045"                     # Existing KL entry IDs checked for conflict
    - "LIB-067"
  conflicts_found: "none|description of conflicts"

votes:
  - agent_id: "claude.analysis"     # Matches VOTING_ROSTER.yaml field name
    trust_tier: "WORKING|PRODUCTION|UNVALIDATED"
    vote: "approve|object|object-with-alternative"
    reasoning: "Written reasoning for the vote"
    binding: true
    date: "YYYY-MM-DDTHH:MM:SSZ"

status: "open|approved|objected|expired|escalated|promoted|rejected"
resolution: "Description of final outcome"
promoted_at: "YYYY-MM-DDTHH:MM:SSZ or null"
```

**Validation:** The compile and validate scripts must accept proposed entries and verify schema conformance. A proposed entry that fails schema validation cannot proceed to vote.

---

## 6. Approval Queue Specification

The file `wiki/proposed/APPROVAL_QUEUE.md` is auto-generated. It carries the following header:

```
<!-- DO NOT EDIT — auto-generated by wiki governance pipeline -->
<!-- Regenerated on every proposal, vote, or expiry event -->
```

**Sort Order (priority):**

1. Expiring soonest (proposals closest to their 14-day expiry)
2. Tier 3 before Tier 2 (Tier 3 requires human action)
3. Most votes cast (proposals closest to resolution)

**Format per Item:**

```markdown
### PROP-2026-04-03-001
- **Expiry:** 2026-04-17 (12 days remaining)
- **Tier:** 2
- **Type:** new
- **Target:** LIB-168
- **Proposer:** claude.analysis
- **Votes:** 2/3 binding (claude.analysis: approve, kiro.design: approve, codex.implementation: pending)
- **Objections:** None
- **Action Needed:** Awaiting codex.implementation vote
```

**Regeneration:** The queue is regenerated on every proposal filing, vote cast, vote expiry, or proposal expiry event. The operator should be able to scan the full queue and understand the state of all pending proposals in 60 seconds.

---

## 7. Compiled Proposed Entries

Proposed entries that have been compiled (but not yet promoted) live in `wiki/proposed/`. Each compiled proposed entry includes a frontmatter banner:

```yaml
---
STATUS: PROPOSED
proposed_by: agent.identity
votes: "summary (e.g., 2/3 approve)"
expires: YYYY-MM-DD
---
```

**Lifecycle:**

| Event | Action |
|---|---|
| Promoted (unanimous approve, quorum met) | Moved to `wiki/entries/` or `wiki/rius/`. Banner removed. Logged in `wiki/proposed/archive/`. |
| Rejected (the operator rejects a Tier 3, or objection not resolved) | Moved to `wiki/proposed/archive/` with status `rejected`. |
| Expired (14 days without unanimous approval) | Moved to `wiki/proposed/archive/` with status `expired`. |

The `wiki/proposed/archive/` directory is append-only. Nothing is deleted from the archive. It serves as the full audit trail.

---

## 8. Acceptance Criteria

Every binding voter must evaluate each Tier 2 proposal against these five criteria. An agent MUST file an `object` vote if any criterion fails. An agent SHOULD file an `object-with-alternative` vote if they see a better way to satisfy the criteria.

| # | Criterion | Test |
|---|---|---|
| 1 | **Has source** | At least 1 citation with a verifiable URL is present in `content.sources`. |
| 2 | **No contradiction** | Does not conflict with any existing KL entry. The `contradiction_check` section must be filled with entries checked and conflicts found (or explicitly "none"). |
| 3 | **Valid mapping** | Maps to at least 1 real RIU ID (e.g., RIU-001) that exists in the current taxonomy release. The IDs in `content.related_rius` must resolve against `taxonomy/releases/v1.3/`. |
| 4 | **Tier justified** | The `content.evidence_tier` matches the quality of the cited sources. The `content.evidence_tier_justification` must explain why. |
| 5 | **Substantive** | The `content.answer` is longer than 100 words and is actionable (provides guidance a practitioner can follow). |

**Enforcement:** A vote of `approve` is an assertion that all five criteria are met. If a promoted entry is later found to fail a criterion, any agent may challenge it (retroactive challenge for Tier 1 fixes, or new Tier 2 proposal for corrections).

---

## 9. Review Trigger (Sunset Clause)

After every **20 processed Tier 2 proposals** (approved, rejected, or expired -- not counting open proposals), the governance model is flagged for human review.

**Review scope:**

- Promotion rate (what percentage of proposals were approved?)
- Veto patterns (is one agent objecting disproportionately? Is no one objecting?)
- Precedent utility (are precedents being cited? Are they reducing re-litigation?)
- Time-to-resolution (are proposals resolving within target windows?)

The operator reviews the metrics and may amend the governance model. Any amendment is a Tier 3 change with the full Tier 3 process (including 24-hour cooling-off).

The trigger is usage-based, not time-based. A dormant system does not trigger review simply because time has passed.

---

## 10. Operational Metrics

The following metrics are tracked automatically by the governance pipeline.

| Metric | Target | Rationale |
|---|---|---|
| Time to resolve Tier 2 (uncontested) | < 48 hours | Uncontested proposals should resolve within a single voting window. |
| Time to resolve Tier 2 (contested) | < 7 days | Contested proposals need time for gradient descent but should not linger. |
| Challenge rate on Tier 1 | < 10% | Most Tier 1 changes should be correct. A high challenge rate suggests the Tier 1 bar is too loose. |
| Precedent citation rate | Increasing over time | Precedents should reduce re-litigation. A flat or declining rate suggests precedents are not useful or not discoverable. |
| Expiry rate | < 20% | Most proposals should resolve (approved or rejected), not expire from inaction. A high expiry rate suggests agent disengagement. |

Metrics are reported in the sunset review (Section 9). They are advisory, not enforcement triggers.

---

## 11. Edge Cases and Stress Testing

The following 10 scenarios have been walked through against the model. Each has a clear resolution.

### Scenario 1: Borderline Tier 1/Tier 2

**Situation:** An agent rephrases a KL answer "for clarity" but the rephrasing subtly changes meaning.

**Resolution:** The tier dispute rule applies (Section 1). If any agent believes the change is semantic rather than cosmetic, the higher tier (Tier 2) applies. The proposing agent may argue it is Tier 1, but the dispute is resolved via Tier 2 vote. In practice, agents should default to Tier 2 when in doubt. The cost of running a vote is low; the cost of silently changing meaning is high.

### Scenario 2: Agent Offline for Extended Period

**Situation:** codex.implementation goes offline for a week. Does every Tier 2 proposal expire?

**Resolution:** No. The abstain-timeout rule applies. If codex.implementation does not vote within 48 hours, its non-vote is recorded as `abstain-timeout`. If the remaining 2 binding agents (claude.analysis and kiro.design) both vote `approve`, the proposal is promoted because: (a) remaining votes are unanimous, and (b) quorum of 2 is met. No proposal is blocked by a single agent's absence. However, if the roster drops below 3 binding agents permanently (not just temporarily offline), all Tier 2 escalates to the operator per the quorum rule.

### Scenario 3: UNVALIDATED Agent Files a Brilliant Proposal

**Situation:** gemini.specialist (UNVALIDATED) files an excellent proposal and votes `approve`. One WORKING agent also approves. Can it auto-promote?

**Resolution:** No. Gemini's vote is advisory only (Section 1.2). One WORKING `approve` is only 1 binding vote, which is below the quorum minimum of 2. The proposal needs at least 2 binding `approve` votes. Gemini's advisory vote signals support but does not count toward quorum or unanimity. The proposal must receive `approve` from at least 2 of the 3 WORKING agents (claude.analysis, kiro.design, codex.implementation).

### Scenario 4: Two Agents Deadlock, Third Abstains

**Situation:** claude.analysis votes `approve`, kiro.design votes `object`, and codex.implementation abstains (timeout).

**Resolution:** The single binding objection from kiro.design prevents auto-promotion (Section 1.2: "Any single binding objection prevents auto-promotion"). The abstain-timeout from codex.implementation is irrelevant because unanimity among binding voters has already failed. The proposer may revise and resubmit within 24 hours per the objection semantics, which resets the 48h voting window. If no resubmission, the proposal escalates to the operator. If kiro.design filed `object-with-alternative`, the gradient descent process (Section 2) applies.

### Scenario 5: Late Tier 1 Challenge

**Situation:** An agent discovers a problem with a Tier 1 fix on day 8, one day after the 7-day challenge window closed.

**Resolution:** The retroactive challenge window is strict: 7 calendar days (Section 1.1). A challenge filed on day 8 is rejected. The fix is permanent. However, the agent is not without recourse. They may file a new proposal (Tier 1 if the correction is itself obviously right, or Tier 2 if it involves semantic judgment) to address the problem they found. The 7-day window prevents indefinite uncertainty about Tier 1 fixes, not indefinite inability to correct errors.

### Scenario 6: Self-Citing Workspace Promotion

**Situation:** A workspace entry is added by claude.analysis to rossi, oil-investor, and fde-toolkit workspaces. It is now cited in 3 workspaces. Does the citation threshold trigger promotion?

**Resolution:** No. The anti-gaming rule (Section 3.2) applies. The citation threshold requires the entry to be independently cited by at least 2 different agents across 2 different workspaces. A single agent adding the same entry to multiple workspaces does not demonstrate independent convergence -- it demonstrates one agent's enthusiasm. The entry may still be promoted via the decision reference path (if the operator references it in a decision) or by a standard Tier 2 proposal with its own evidence.

### Scenario 7: The Operator Unavailable for 30 Days

**Situation:** The operator is traveling or otherwise unavailable for 30 days. Does everything stall?

**Resolution:** Tier 1 continues unaffected (no human involvement needed). Tier 2 continues unaffected as long as proposals achieve unanimous binding approval -- auto-promotion does not require the operator. Only the following stall: (a) Tier 3 proposals, which require the operator's approval by design, (b) Tier 2 proposals that receive a binding objection and cannot resolve through gradient descent, (c) situations where the binding roster drops below 3 agents. For planned absences, the operator should review and clear the Tier 3 queue before departure. Uncontested Tier 2 work proceeds autonomously, which is the intended steady state.

### Scenario 8: Object Without Reasoning

**Situation:** An agent files an `object` vote but provides no reasoning.

**Resolution:** The vote is recorded as `abstain-malformed` (Section 1.2). A vote without reasoning is invalid because reasoning is mandatory for `object` and `object-with-alternative` votes. The agent is notified and may re-vote within the original 48h window with proper reasoning. If the agent does not re-vote, the `abstain-malformed` is treated the same as `abstain-timeout` for promotion purposes.

### Scenario 9: Repeated Rejection and Resubmission

**Situation:** A proposal is rejected, resubmitted, rejected again, resubmitted again. Is there a limit?

**Resolution:** Yes. A proposal may be resubmitted a maximum of **3 times** (original + 2 resubmissions). After the third rejection or expiry, the proposal is locked. To reopen the topic, the proposing agent must either: (a) present materially new evidence not available during prior submissions, or (b) reference a new precedent from `decisions.md` that changes the calculus. The new submission must explicitly cite what is different from prior attempts. This prevents indefinite re-litigation while preserving the ability to revisit topics when circumstances genuinely change.

### Scenario 10: Critical Flaw Found During Tier 3 Cooling-Off

**Situation:** The operator approves a Tier 3 change. During the 24-hour cooling-off period, an agent discovers a critical flaw (e.g., the change would silently break 15 existing KL entries).

**Resolution:** The agent files an emergency objection with: (a) the Tier 3 proposal ID, (b) description of the critical flaw, and (c) evidence of impact. The operator is notified immediately. The operator may withdraw approval, in which case the change does not take effect and the proposal returns to discussion. The operator may also acknowledge the flaw and approve anyway (perhaps the breakage is acceptable and planned). The cooling-off period exists precisely for this purpose. If the operator is unreachable during the cooling-off window, the cooling-off period extends until the operator responds. The change does not auto-apply after 24 hours if an emergency objection is pending.

---

## 12. Summary Table

| Aspect | Tier 1 | Tier 2 | Tier 3 | W1 | W2 | W3 |
|---|---|---|---|---|---|---|
| Scope | No semantic change | Semantic, reversible | Irreversible/structural | Workspace fix | Workspace add/modify | Workspace delete/structural |
| Approval | Any 1 agent | Unanimous binding, quorum >= 2 | the operator | Any 1 agent | Owner + 1 agent | the operator |
| Voting window | None | 48h | None (the operator decides) | None | 24h | None |
| Auto-promote | Yes | Yes | No | Yes | Yes (after timeout) | No |
| Expiry | N/A | 14 days | None | N/A | N/A | None |
| Challenge window | 7 days retroactive | N/A (vote-based) | 24h cooling-off | 7 days retroactive | N/A | N/A |
| Resubmission limit | N/A | 3 attempts | No limit (the operator decides) | N/A | N/A | N/A |

---

## 13. Feedback Trail and Provenance

### Contributions

| Contributor | Role | Key Contributions |
|---|---|---|
| **the operator** | Decision authority, design principal | Design principle, tier definitions, veto-as-safety-mechanism philosophy, final disposition of all contested rules, Mistral review disposition |
| **claude.analysis** | Author, consolidator | Drafted all iterations, resolved inter-agent feedback conflicts, wrote edge case analysis, produced final document |
| **kiro.design** | Design reviewer | Workspace governance structure, schema design, approval queue UX requirements |
| **codex.implementation** | Implementation reviewer | Compile/validate pipeline integration, YAML schema validation requirements, runtime roster reading |
| **gemini.specialist** | Advisory reviewer | Cross-referenced against existing KL for contradictions, provided evidence tier analysis |
| **mistral.specialist** | Advisory reviewer | Filed 10 proposed changes (3 accepted, 1 partially accepted, 6 rejected -- see Mistral Disposition below) |

### Mistral Disposition

The following disposition was applied to Mistral's 10 proposed changes, reviewed against the consensus model:

| # | Proposal | Disposition | Reasoning |
|---|---|---|---|
| 1 | Replace "zero hesitation" with "no semantic change" | Partially accepted | Both phrases are used: "no semantic change, verifiable with zero hesitation" |
| 2 | No timeout for Tier 2 | Rejected | Already resolved by the abstain-timeout rule |
| 3 | Retroactive challenge for Tier 1 | Accepted | Already present in the design; Mistral reviewed the original draft, not the final |
| 4 | Split Tier 3 into 3A/3B | Rejected | Over-engineering; adding a new RIU is structurally consequential; the operator can approve quickly for low-risk items |
| 5 | Precedent expiration at 2 years | Rejected | Precedents are overruled by new precedents, not by calendar time; auto-expiry would silently remove institutional memory; the sunset review handles staleness |
| 6 | Tier dispute resolution | Accepted | "Higher tier applies" rule incorporated in Section 1 |
| 7 | Change Tier 2 from unanimous to 4/5 | Rejected | Undermines the veto principle; at 3 agents, 4/5 is impossible; at 5, it lets 1 agent be overruled; false negative cost (good change delayed) is low, false positive cost (bad entry promoted) is high |
| 8 | Onboarding quiz for new agents | Rejected | Over-engineering for current scale; the trust tier system (UNVALIDATED to WORKING to PRODUCTION) is the onboarding mechanism |
| 9 | Operational metrics | Accepted | Incorporated in Section 10 with realistic targets |
| 10 | 1-year time-based sunset | Rejected | Usage-based trigger (every 20 proposals) is superior; a dormant system should not trigger review just because a year passed |

### Provenance

| Version | Date | Author | Change |
|---|---|---|---|
| v1 | 2026-04-03 | claude.analysis | Initial FINAL version, consolidating all agent feedback and the operator decisions |

### Signature Block

```
Status: FINAL -- awaiting the operator signature

The operator: _______________  Date: _______________
```

---

*This document governs real decisions. Every rule is intended to be followed literally by autonomous agents. Ambiguity is a bug. File issues against this document as Tier 3 proposals.*
