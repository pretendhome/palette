# P2-08: wiki/proposed/ Governance Model — Research & Options

**Author**: kiro.design
**Date**: 2026-04-03
**Status**: RESEARCH COMPLETE — options for the operator review
**Decision type**: 🚨 ONE-WAY DOOR (governance decisions are binding)
**Reference**: WIKI_FOCAL_POINT_PROPOSAL.md (Phase 3, Phase 6), WIKI_PHASE_2_SCOPE.md (P2-08)

---

## The Problem

The `wiki/proposed/` directory exists but is empty. Phase 3 of the original proposal says voice interactions and agent work should be able to file proposed knowledge updates here. Phase 6 says working memory (mcp-memory-service) should promote recurring insights into proposed entries. Both are blocked until we define the governance model.

The core tension: **we want the system to learn from usage, but we don't want it to pollute the knowledge library with unvalidated content.**

---

## Research Summary

I studied 5 governance patterns used in production knowledge systems. Here's what I found and how each maps to Palette.

### Pattern 1: Wikipedia's Articles for Creation (AfC)

Wikipedia's draft namespace is the closest analog. New editors submit articles to a staging area. Experienced reviewers check them against notability, sourcing, and neutrality criteria. Articles either get promoted to mainspace or sent back with feedback.

Key design choices:
- Drafts are visible but not indexed by search engines
- Automatic deletion after 6 months of inactivity
- Multiple editors can collaborate on a draft before submission
- Reviewers use structured criteria (notability, sources, neutrality)
- Rejection includes specific feedback, not just "no"

What works for Palette: the staging area concept, structured review criteria, and the "visible but not canonical" status. What doesn't: Wikipedia's scale (thousands of reviewers) — we have 1 human reviewer (the operator) and 5 agents.

### Pattern 2: Karpathy's LLM Wiki Pattern

Karpathy's approach is the opposite of Wikipedia: the LLM writes and maintains all wiki data. The human rarely edits directly. Every query enriches the wiki. No review gate.

Key design choices:
- LLM is the sole author — human doesn't edit
- Every interaction can modify the wiki
- Quality comes from the LLM's judgment, not human review
- Works at ~100 articles / ~400K words scale

What works for Palette: the feedback loop concept (interactions enrich knowledge). What doesn't: no human gate. Palette's knowledge library has evidence tiers and sourcing requirements. Ungated LLM writes would violate the governance model.

### Pattern 3: RFC / Pull Request Model

Open source projects use RFCs (Request for Comments) or pull requests for proposed changes. The proposal is public, reviewable, and must be explicitly approved before merging.

Key design choices:
- Proposal includes rationale, not just content
- Review period with explicit timeline
- Approval requires N reviewers (usually 2+)
- Rejection is documented with reasoning
- History is preserved (you can see what was proposed and why it was declined)

What works for Palette: the structured proposal format, documented review, and preserved history. This maps naturally to the wire contract — a proposed entry is a HandoffPacket from the proposing agent to the reviewer.

### Pattern 4: Andrew Ng's Agentic Document Writer

Ng's framework allows agents to submit documentation entries with a structured feedback loop. Agents submit data about documentation utility, and the system uses this to improve over time.

Key design choices:
- Agents can propose but not commit
- Feedback is structured (utility scores, not free text)
- The pipeline is: propose → review → accept/reject → learn from outcome

What works for Palette: agents as proposers with structured metadata. This is exactly how our peers bus works — agents send HandoffPackets with structured payloads.

### Pattern 5: Multi-Agent Swarm Evaluation

Production multi-agent systems use AI judges that score content on accuracy, clarity, and logic. Multiple agents evaluate independently, and consensus determines promotion.

Key design choices:
- Multiple evaluators reduce single-point-of-failure
- Scoring rubric is explicit and measurable
- Human review is reserved for edge cases
- Automated checks handle the bulk

What works for Palette: we already have multiple agents (Kiro, Claude, Codex) who can review. The scoring rubric maps to our evidence tier system. Human review for ONE-WAY DOOR decisions is already our pattern.

---

## Three Options for Palette

### Option A: Human-Only Gate (Conservative)

```
Agent/Voice → proposed/ → the operator reviews → promote or reject
```

- **Who can propose**: Any agent, any voice interaction
- **What can be proposed**: New KL entries, corrections to existing entries, new RIU-to-KL mappings
- **Review cadence**: Weekly (the operator reviews proposed/ directory)
- **Promotion criteria**: the operator judgment — no automated scoring
- **Source attribution**: Required (proposer agent, source of insight, date)
- **Expiry**: Proposed entries auto-delete after 30 days if not reviewed

Pros: Maximum safety. No bad content enters the KL.
Cons: Bottleneck on the operator. If the operator is busy, proposed entries pile up and expire. Doesn't scale.

### Option B: Agent Pre-Screen + Human Approval (Balanced)

```
Agent/Voice → proposed/ → 2 agents review → the operator approves/rejects
```

- **Who can propose**: Any agent, any voice interaction
- **What can be proposed**: New KL entries, corrections, new mappings, new source citations
- **Review cadence**: Agents review within 24h (via peers bus). The operator reviews agent-approved entries weekly.
- **Promotion criteria**:
  - Agent review checks: (1) has source citation, (2) doesn't contradict existing KL, (3) maps to valid RIU, (4) evidence tier is justified
  - the operator checks: (1) is this actually useful, (2) does it meet the quality bar
- **Source attribution**: Required — proposer, source, date, review agents, review outcome
- **Expiry**: 60 days if not agent-reviewed. 30 days after agent approval if the operator hasn't acted.
- **Conflict handling**: If proposed entry contradicts existing KL, auto-generate a conflict analysis page in `proposed/conflicts/`

Pros: Agents handle the mechanical checks. The operator only sees pre-screened entries. Scales better.
Cons: Agents can be wrong. Two agents agreeing doesn't guarantee quality. Still requires the operator time.

### Option C: Tiered Autonomy (Progressive Trust)

```
TWO-WAY DOOR changes: Agent consensus → auto-promote
ONE-WAY DOOR changes: Agent consensus → the operator approves
```

- **Who can propose**: Any agent, any voice interaction
- **What can be proposed**: Everything in Option B, plus: source URL updates, tag corrections, related_rius additions
- **TWO-WAY DOOR changes** (auto-promotable with 2+ agent consensus):
  - Adding a source citation to an existing entry
  - Correcting a broken URL
  - Adding a related_rius mapping
  - Adding tags
- **ONE-WAY DOOR changes** (require the operator):
  - New KL entries
  - Modifying an existing answer
  - Changing evidence tier
  - Removing content
- **Review cadence**: TWO-WAY DOOR: continuous (agents review via bus). ONE-WAY DOOR: weekly by the operator.
- **Source attribution**: Full provenance chain — proposer, reviewers, consensus score, promotion timestamp
- **Expiry**: TWO-WAY DOOR: 7 days without agent review → auto-expire. ONE-WAY DOOR: 60 days.
- **Conflict handling**: Same as Option B, plus: TWO-WAY DOOR conflicts block auto-promotion and escalate to the operator.

Pros: Most changes happen without the operator. Only consequential changes need human review. Matches Palette's existing ONE-WAY/TWO-WAY DOOR model.
Cons: Most complex to implement. Requires trust in agent consensus. Risk of gradual quality drift if TWO-WAY DOOR threshold is too low.

---

## My Recommendation: Option B (Balanced)

Here's why:

1. **Option A is too conservative.** We already proved with the peers bus that agents can review each other's work effectively. Having the operator review every proposed entry is a bottleneck that will kill the feedback loop before it starts.

2. **Option C is premature.** Auto-promotion requires high trust in agent consensus. Our agents are mostly UNVALIDATED tier. We don't have enough impressions to trust auto-promotion yet. Option C is the right end state, but we should earn it through Option B first.

3. **Option B matches how we already work.** Agents propose (bus messages), agents review (Kiro reviews Gemini, Claude reviews Codex), human approves (the operator says "go" or "no"). The proposed/ directory is just the bus pattern applied to knowledge.

### Specific Recommendations for Option B

**Proposed entry format** (YAML in `wiki/proposed/`):

```yaml
id: PROP-001
proposed_by: kiro.design
proposed_at: 2026-04-03T16:30:00Z
type: new_kl_entry  # or: correction, new_mapping, new_source
target: LIB-NEW  # or existing ID for corrections
content:
  question: "How do I..."
  answer: "..."
  sources:
    - title: "..."
      url: "..."
  related_rius: [RIU-XXX]
  evidence_tier: 2
  tags: [...]
rationale: "Why this should be added — what gap it fills"
source_of_insight: "voice interaction / agent analysis / workspace feedback"
reviews:
  - agent: claude.analysis
    date: 2026-04-04
    verdict: approve
    notes: "Source verified, maps correctly to RIU-XXX"
  - agent: codex.implementation
    date: 2026-04-04
    verdict: approve
    notes: "No contradiction with existing LIB-045"
status: agent_approved  # proposed → agent_reviewed → agent_approved → promoted | rejected | expired
```

**Review cadence**: Agents check `proposed/` daily via peers bus. The operator reviews agent-approved entries on Sundays (or whenever convenient).

**Acceptance criteria for agent reviewers**:
1. Has at least one source citation with a real URL
2. Does not contradict existing KL entries (check by searching for conflicting claims)
3. Maps to at least one valid RIU
4. Evidence tier is justified by the source quality
5. Answer is substantive (>100 words, not a stub)

**Rejection must include**: which criterion failed, what would fix it, and whether resubmission is encouraged.

**Promotion process**: the operator reviews, says "promote" or "reject" (can be a one-word response). If promote, the entry gets added to the KL YAML and the wiki is recompiled. The proposed file moves to `proposed/archive/` with the final status.

---

## What This Enables

With Option B in place:
- **Phase 3** (voice feedback loop) can start: voice interactions file proposed entries
- **Phase 6** (memory-to-wiki promotion) has a target: mcp-memory-service promotes to `proposed/`, not directly to KL
- **The flywheel feedback** from Mission Canvas (palette_feedback.yaml) has a governed path into the knowledge library
- **Gemini's KL contributions** (like LIB-168) go through the same pipeline instead of ad-hoc

---

## Implementation Effort

If you approve Option B:
- Proposed entry schema: 30 min (I write the YAML schema)
- Compiler update to render proposed/ as a "Pending Review" index: 30 min
- Agent review checklist as a peers bus task template: 30 min
- Total: ~1.5 hours to implement the infrastructure

The governance model itself is the decision. The code is straightforward.

---

*Ready for your review. Pick A, B, or C — or tell me what you'd change.*

References:
[1] MediaWiki Article Creation Workflow/Design - https://www.mediawiki.org/wiki/Article_creation_workflow
[2] Karpathy LLM Knowledge Bases - https://deepakness.com/raw/llm-knowledge-bases/
[3] Andrew Ng AI Coding Agents Collaboration Framework - https://www.thenextgentechinsider.com/pulse/andrew-ng-proposes-ai-coding-agents-collaboration-framework
[4] Building Human-In-The-Loop Agentic Workflows - https://towardsdatascience.com/building-human-in-the-loop-agentic-workflows/
[5] Wikipedia AfC submission/draft template - https://en.wikipedia.org/wiki/Template:AfC_submission/draft

Content was rephrased for compliance with licensing restrictions.
