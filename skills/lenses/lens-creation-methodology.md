---
id: SKILL-006
name: Lens Creation Methodology
domain: lenses
for_agents: ["Architect", "Builder", "Narrator"]
triggers: ["RIU-001", "RIU-014"]
impressions: 0
status: UNVALIDATED
---

# Lens Creation Methodology

## What a Lens Is

A lens is an optional context overlay that shapes how Palette agents frame their output for a specific role or persona. It does not change *what* gets routed (RIUs handle that) or *who* does the work (agents handle that). It changes *how the output is framed* — sections, forbidden patterns, quality checks, and interaction style.

## When to Create a New Lens

Create a new lens when:
1. A distinct professional role interacts with AI implementation decisions
2. That role needs output framed differently from existing lenses
3. The role has specific quality checks that generic output misses
4. At least 3 RIUs are relevant to the role's decision context

Do NOT create a lens when:
- The role is a sub-specialization of an existing lens (use the parent)
- The framing difference is cosmetic (different words, same structure)
- The role only interacts with 1-2 RIUs (too narrow)

## Creation Process

### Step 1: Define the Role Context (5 min)

Answer these questions:
- **Who is this person?** Job title, what they decide, what they're accountable for.
- **What AI decisions do they face?** Not "use AI" but specific: model selection, deployment, evaluation, governance, etc.
- **What output do they need?** Decisions, plans, reviews, assessments — be specific about the artifact shape.
- **What do they NOT need?** What would waste their time or be inappropriate for their role?

### Step 2: Map to Palette (10 min)

- **Primary RIUs** (3-6): Which RIUs does this role most frequently trigger? Check `taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml`.
- **Primary agents** (2-3): Which agents do the work when this lens is active? Match to agent role boundaries.
- **Library links**: What categories of knowledge library entries should be preferred?

### Step 3: Define the Output Contract (15 min)

This is the lens's core value. Define:

**Required sections** — What must appear in every output under this lens? Name each section. Example: "Threat model", "Cost projection", "Rollback plan".

**Forbidden patterns** — What must never appear? These prevent common role-inappropriate outputs. Example: "unsupported certainty", "no rollback for risky changes".

**Quality checks** — What must be true before the output ships? These are the lens's acceptance criteria. Example: "Every risk has an owner", "Baseline comparison is included".

### Step 4: Set Interaction Style (5 min)

- **Default answer shape**: What order should output sections follow? Name the sequence.
- **Presentation rules**: How should the output look? Lead with what? Use what format?

### Step 5: Define Evaluation Plan (5 min)

- **4 metrics** to compare lens-on vs lens-off output
- **20 minimum sample size** before kill decision
- **Kill criteria**: No improvement on 2+ of 4 metrics → remove the lens

### Step 6: Write the YAML (10 min)

Use template at `lenses/PROMPT_PACK_LENS_TEMPLATE_v0.1.yaml`. Fill all fields. Save to `lenses/releases/v0/LENS-<ROLE>-<NNN>_<slug>.yaml`.

Naming convention:
- Role codes: PM, ENG, DEV, MGR, EXEC, SALES, CS, HR, IT, FIN, MKT, QA, REVIEW, CEO, INT, DS, SEC, DESIGN, DEVOPS, DEVREL, MLOPS
- Number: 001 for first lens in role category
- Slug: lowercase underscore description

### Step 7: Validate (5 min)

Before marking as `pilot`:
- [ ] All required YAML fields populated (no TODOs remaining)
- [ ] At least 3 primary RIUs mapped
- [ ] Output contract has 4+ required sections
- [ ] At least 3 forbidden patterns defined
- [ ] At least 4 quality checks defined
- [ ] Evaluation plan has 4 metrics and kill criteria
- [ ] Lens does not overlap significantly with existing lens
- [ ] `origin.notes` explains what this lens adds vs existing lenses

## Lifecycle

```
draft       → Fill template, map to Palette, define output contract
pilot       → Activate in real sessions, collect 20+ eval runs
validated   → Kill criteria passed, metrics show improvement
production  → 50+ impressions, integrated into Resolver/Orchestrator
retired     → Kill criteria failed or role absorbed into another lens
```

## Current Lens Inventory

| ID | Role | Status | Category |
|----|------|--------|----------|
| PM-001 | Product Decision | pilot | Product & Strategy |
| ENG-001 | Engineering Execution | pilot | Technical |
| DEV-001 | Developer Delivery | pilot | Technical |
| MGR-001 | Manager Execution | pilot | Organizational |
| EXEC-001 | Executive Decision | pilot | Product & Strategy |
| CEO-001 | Product Vision | pilot | Product & Strategy |
| SALES-001 | Customer Motion | pilot | GTM & Commercial |
| CS-001 | Customer Success | pilot | GTM & Commercial |
| MKT-001 | Marketing Execution | pilot | GTM & Commercial |
| FIN-001 | Finance Analysis | pilot | Organizational |
| HR-001 | People Ops | pilot | Organizational |
| IT-001 | IT Operations | pilot | Organizational |
| QA-001 | QA Methodology | pilot | Technical |
| REVIEW-001 | Code Review | pilot | Technical |
| INT-001 | Interview Learning Readiness | pilot | Specialized |
| INT-002 | OpenAI Takehome Grader | pilot | Specialized |
| DS-001 | Data Science | draft | Technical |
| SEC-001 | Security Decision | draft | Technical |
| DESIGN-001 | Product Design | draft | Technical |
| DEVOPS-001 | DevOps & Infrastructure | draft | Technical |
| DEVREL-001 | Developer Relations | draft | GTM & Commercial |
| MLOPS-001 | ML Operations | draft | Technical |

## Role Categories

- **Technical**: ENG, DEV, QA, REVIEW, DS, SEC, DESIGN, DEVOPS, MLOPS
- **Product & Strategy**: PM, EXEC, CEO
- **Organizational**: MGR, HR, IT, FIN
- **GTM & Commercial**: SALES, CS, MKT, DEVREL
- **Specialized**: INT (interview-context lenses)
