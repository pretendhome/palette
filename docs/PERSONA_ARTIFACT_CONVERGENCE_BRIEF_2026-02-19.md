# Persona Artifact Convergence Brief (Yuty-First)

**Date**: 2026-02-19  
**Authoring mode**: Palette system introspection (Yuty framing + Argy evidence + Rex constraints + Anky risk check)  
**Scope**: Decide whether Palette should add a reusable persona artifact mapped to RIUs + Library + Company matrix.

---

## 1) Convergence Statement

## Goal
Determine whether adding a persona layer improves Palette outcomes enough to justify added complexity.

## Core question
Should Palette add a new artifact for pre-defined personas, or keep persona assignment ad-hoc per session?

## Non-goals
- Do **not** make persona mandatory for all flows.
- Do **not** replace agent archetypes (Argy/Rex/Theri/etc.) with personas.
- Do **not** let persona overrule RIU routing or ONE-WAY DOOR policy.

## Success criteria
1. We can show persona value with measurable outcome deltas (quality, speed, fewer retries, better gate decisions).
2. We preserve current agent boundaries and avoid cognitive bloat.
3. The artifact can be optional and safely ignored when not needed.

---

## 2) What Actually Worked Yesterday (Evidence)

Using local evidence from `2026-02-18`:

1. `product/eval` became a real product loop, not just docs.
2. Routing quality moved from severe failure to stable pass:
- Run `20260218T232816Z_67d94431`: pass rate `0%`, OWD recall `0%`, novelty `1.00`.
- Run `20260218T235438Z_89f5e8eb`: pass rate `100%`, OWD recall `100%`, novelty `5.00`.
3. The OWD fix was concrete and minimal:
- `missioncanvas-site/openclaw_adapter_core.mjs` expanded `OWD_TERMS` from technical-only to include business irreversibility language.
4. Product-governance artifacts were generated automatically:
- `product/eval/status_board.md`
- `product/eval/issues/triage_queue.md`
- `product/pm_reviews/iteration_1_auto.md`

Interpretation:
- The strongest improvements came from **explicit framing + measurable gates + fast feedback loop**, not from generalized “chat style.”
- The product-manager lens helped by enforcing: thresholding, ownership mapping, and go/no-go decisions.

---

## 3) What the Product Persona Helped With

## Observed benefits
1. **Decision compression**: Converted raw eval metrics into a decision note format (`keep/stop/priorities/gate`).
2. **Ownership clarity**: Auto-mapped failure dimensions to responsible agents (`Yuty/Rex/Theri/Anky/Argy/Para`).
3. **Operational cadence**: Created a repeatable review ritual after each run.
4. **Behavioral discipline**: Kept focus on pass rate, novelty, and safety, not narrative drift.

## Limitations introduced
1. **Metric illusion risk**: PM notes can look “production ready” even when metrics are synthetic/proxy-heavy.
2. **Over-structuring risk**: Too many governance artifacts can increase process drag.
3. **Role overfit risk**: A PM lens can bias toward triage/gating and underweight deep technical debt.
4. **Language lock-in risk**: Persona language can become performative if not grounded in evidence.

Conclusion:
- Persona helped when it acted as a **decision lens**, not as a personality mask.

---

## 4) Should Palette Add a Persona Artifact?

## Recommendation
**Yes, but only as an optional “Lens Artifact,” not a mandatory persona layer.**

Reasoning:
- Palette already has agent function boundaries.
- What is missing is a reusable **context lens** that shapes outputs for a specific stakeholder objective.
- Calling it “Lens” avoids confusion with agent identity or role-playing.

So the new artifact should be:
- optional,
- explicit,
- evidence-linked,
- measurable,
- easy to bypass.

---

## 5) Proposed Artifact: `Lens Profile` (v0)

## Definition
A `Lens Profile` is a reusable context overlay that influences framing, constraints, and output contract for a session.

## Purpose
Improve decision quality for specific stakeholder contexts (PM, Exec, Engineer, Sales, IT, etc.) without changing base agent responsibilities.

## Minimal schema
```yaml
lens_id: LENS-001
name: Product Decision Lens
description: Optimize for measurable quality gates, prioritization, and release risk.
optional: true
trigger_signals:
  - roadmap
  - prioritization
  - go/no-go
  - launch readiness
riu_coverage:
  - RIU-001
  - RIU-062
  - RIU-073
library_refs:
  - LIB-xxx
  - LIB-yyy
company_signals:
  - category: B2B SaaS
  - stage: growth
output_contract:
  required_sections:
    - Decision
    - Evidence
    - Risks
    - Next 3 actions
  forbidden_patterns:
    - unsupported claims
    - vague owners
quality_checks:
  - decision is reversible/irreversible labeled
  - owner + due date present
  - success metric present
```

## Important boundary
Lens can shape **how outputs are framed**, but never overrides:
- agent constraints,
- RIU routing safety,
- OWD confirmation requirements.

---

## 6) Where It Lives in Palette

Recommended path:
- `palette/lenses/README.md`
- `palette/lenses/releases/v0/*.yaml`
- `palette/lenses/evals/`

Why not `personas/`?
- “Persona” implies identity simulation.
- “Lens” better matches Palette’s architecture: constraint overlay + output contract.

---

## 7) Yuty Prompt Upgrade (Start Here)

Below is the improved Yuty prompt to drive next-step convergence.

```md
You are Yutyrannus in Palette.
Goal: decide whether a Lens Artifact should exist for this engagement.

Inputs:
- Last 10 eval runs (metrics + failure clusters)
- Latest PM note draft
- Adapter/routing changes made this cycle
- RIU + Library + Company mapping context

Task:
1) Summarize what materially improved quality this cycle (evidence only).
2) Separate improvements caused by:
   a) code changes,
   b) evaluation process,
   c) lens/persona framing.
3) Propose whether to keep persona usage ad-hoc or define reusable Lens Profiles.
4) If Lens Profiles are recommended, define a minimal v0 schema and 2 pilot lenses.
5) List risks of this new layer and mitigations.

Output format (strict):
- Decision: adopt / defer / reject
- Why now
- Evidence
- Risks
- Pilot plan (2 weeks)
- Kill criteria

Rules:
- No claims without evidence from artifacts.
- If evidence is weak, output "defer".
- Keep language concrete and operator-ready.
```

---

## 8) How OpenAI Academy Role Packs Fit (Argy Research)

Observed from the referenced OpenAI Academy resources:
- Cross-functional role packs exist by function (Product, Engineers, Sales, Marketing, IT, HR, Managers, Finance, Customer Success, Executives).
- “ChatGPT for Any Role” frames role adaptation as a repeatable practice.

What this implies for Palette:
- External precedent supports role-specific overlays.
- But Palette should implement this as **structured lenses** tied to RIUs, not freeform persona scripts.

Source links reviewed:
- https://academy.openai.com/home/clubs/work-users-ynjqu/resources/chatgpt-for-any-role
- https://academy.openai.com/home/clubs/work-users-ynjqu/resources/use-cases-product
- https://academy.openai.com/home/clubs/work-users-ynjqu/resources/use-cases-engineers
- https://academy.openai.com/home/clubs/work-users-ynjqu/resources/use-cases-sales
- https://academy.openai.com/home/clubs/work-users-ynjqu/resources/use-cases-marketing
- https://academy.openai.com/home/clubs/work-users-ynjqu/resources/use-cases-it
- https://academy.openai.com/home/clubs/work-users-ynjqu/resources/use-cases-hr
- https://academy.openai.com/home/clubs/work-users-ynjqu/resources/use-cases-for-managers
- https://academy.openai.com/home/clubs/work-users-ynjqu/resources/use-cases-finance
- https://academy.openai.com/home/clubs/work-users-ynjqu/resources/use-cases-customer-success
- https://academy.openai.com/home/clubs/work-users-ynjqu/resources/use-cases-executives

---

## 9) Proposed Pilot (No Big Bang)

## Two-week pilot, two lenses
1. `LENS-PM-001` Product Decision Lens
2. `LENS-ENG-001` Engineering Execution Lens

## Test design
- A/B by session:
  - A: normal Palette flow (no lens)
  - B: same flow + lens overlay
- Compare:
  - convergence turns,
  - artifact acceptance rate,
  - rework count,
  - OWD false positives/negatives,
  - operator satisfaction.

## Kill criteria
Kill lens layer if any of these happen:
1. No measurable improvement after 20+ comparable runs.
2. Added latency/process overhead > 20% with no quality gain.
3. Clear increase in hallucinated certainty or constraint violations.

---

## 10) Decision Status

**Current decision**: `ADOPT AS PILOT` (optional Lens Artifact v0).  
**Confidence**: Medium-high.  
**Rationale**: Strong evidence that framing and evaluation discipline improved outcomes; low-risk path exists if done as optional overlay with kill criteria.

