---
id: SKILL-ENA-001
name: Agentic Enablement System
domain: Enablement
for_agents: [Architect, Builder, Narrator, Validator]
triggers: [RIU-001, RIU-014, RIU-062, RIU-070]
impressions: 0
status: UNVALIDATED
validated_on: Pending first deployment
deployable: enablement/agentic-enablement-system/onboarding/enablement-coach.md
---

# Agentic Enablement System

Validated methodology for onboarding any non-CLI professional to building their own personal AI software suite. Engine is domain-agnostic — ships with Agentic Enablement as default domain pack, generalizes to any role/domain.

## When to Use

- Onboarding someone to Palette or any AI toolkit (non-technical audience)
- Enabling an enterprise team member on GenAI for their specific workflow
- Building a personalized learning path for any professional skill
- Deploying a coaching system that works through web chat UIs

## Deployable Artifact

`enablement/agentic-enablement-system/onboarding/enablement-coach.md` — drop into a Claude Project. Learner starts a chat, coach runs the full program automatically.

## Core Architecture (Engine + Domain Pack)

**Engine (Layer 1 — universal, does not change per domain):**
- LearnerLens: 4-section profile (identity, assessment, goals, state). 3-5 intake questions. Assessment is internal only — never shown as scores.
- Coaching Loop: Resume → Do → Check → Capture → Advance. Four interaction patterns (stuck, skip, off-script, overwhelmed).
- Progress File: Single learner-owned plain-language document. Portable across tools. Source of truth for cross-session memory.
- Verification: 5 patterns (show-me, teach-back, outcome check, before-and-after, trust-and-verify). Framed as collaboration, not assessment.
- Safety: No overselling vendor certainty. Backup before building. Flag one-way doors. Glass-box.
- Language: Plain language first. Metaphors over definitions. One concept per session. Use their words. Never "it's simple."

**Domain Pack (Layer 2 — swaps per context):**
- 7-stage universal progression: Orient → First Use → Retain → Verify → Organize → Extend → Own
- Domain-specific: stage names, activities, success criteria, translation table, worked examples
- Default pack: Agentic Enablement (Foundations → First Instructions → Memory → Verification → Organization → Building → Autonomy)

## Governance

13 Tier 1 rules (always true), 12 Tier 2 assumptions (testing), 12 Tier 3 experiments (speculative). Full classification in `enablement/agentic-enablement-system/iterations/iteration-08-tier-classification.md`.

## Creating a New Domain Pack

1. One-sentence domain definition
2. Instantiate the 7 universal stages (name, framing, activities, success criteria, time)
3. Build translation table (domain terms → plain language)
4. Write 1-2 worked examples (realistic learner persona)
5. Identify tool landscape

Full guide: `enablement/agentic-enablement-system/iterations/iteration-07-generalization.md`

## Quality Checks

- [ ] Intake produces a usable profile in <15 minutes
- [ ] Every session ends with an updated progress file
- [ ] Learner can resume from progress file in a new conversation
- [ ] No scores or ratings shown to the learner
- [ ] Every recommendation links to a reason from the lens
- [ ] Verification framed as collaboration, not testing

## Source

- Full build: `enablement/agentic-enablement-system/` (8 iterations, assembled prompt, decisions)
- Lineage: Codex coaching loop, education lenses (LENS-CHILD-001), real learner conversations
- GitHub: `pretendhome/pretendhome` → `enablement/agentic-enablement-system/`
