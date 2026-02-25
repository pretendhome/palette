# Prompt-Pack -> Lens Roadmap (OpenAI Academy "ChatGPT for ..." Packs)

**Date**: 2026-02-25  
**Purpose**: Systematically translate role-based prompt packs into Palette lenses

---

## Existing lens attempts found (and improved)

These are the first three versions of the role-pack lens idea:

- `palette/lenses/releases/v0/LENS-PM-001_product_decision.yaml` (updated to `v0.2`)
- `palette/lenses/releases/v0/LENS-ENG-001_engineering_execution.yaml` (updated to `v0.2`)
- `palette/lenses/releases/v0/LENS-DEV-001_developer_delivery.yaml` (updated to `v0.2`)

They now include:
- explicit origin/inspiration metadata
- role-pack alignment notes
- user-intent examples
- interaction/presentation style rules
- stronger output requirements for decision/action framing

---

## Translation Rule (How to convert a prompt pack into a Palette lens)

Prompt packs usually provide:
- role-specific use cases
- prompt patterns
- output examples
- common workflows

Palette lenses should extract:
- **decision frame**
- **output contract**
- **quality checks**
- **when to use / not use**
- **agent + RIU fit**

### What NOT to copy directly
- Generic prompt snippets without Palette context
- Role advice that bypasses RIU routing
- Outputs that omit owner/metric/reversibility where Palette needs them

---

## Proposed Role-Pack Lens Set (initial)

### Already started
- PM (`LENS-PM-001`)
- ENG (`LENS-ENG-001`)
- DEV (`LENS-DEV-001`)

### Next high-value additions
1. `LENS-MGR-001_manager_execution`
   - based on "ChatGPT for managers"
   - focus: delegation clarity, decision cadence, follow-up loops

2. `LENS-EXEC-001_executive_decision`
   - based on "ChatGPT for executives"
   - focus: strategic options, tradeoffs, risk framing, concise readouts

3. `LENS-SALES-001_customer_motion`
   - based on "ChatGPT for sales"
   - focus: account strategy, objection handling, next-step plans

4. `LENS-CS-001_customer_success`
   - based on "ChatGPT for customer success"
   - focus: adoption blockers, success plans, renewal risk indicators

5. `LENS-HR-001_people_ops`
   - based on "ChatGPT for HR"
   - focus: policy drafting, talent ops workflows, process clarity (not legal advice)

6. `LENS-IT-001_it_operations`
   - based on "ChatGPT for IT"
   - focus: troubleshooting triage, rollout comms, SOPs, change windows

7. `LENS-FIN-001_finance_analysis`
   - based on "ChatGPT for finance"
   - focus: assumptions, variance, scenario analysis, decision hygiene

8. `LENS-MKT-001_marketing_execution`
   - based on "ChatGPT for marketing"
   - focus: campaign hypotheses, messaging tests, content ops

---

## Suggested Implementation Order (Pragmatic)

### Phase 1: Strengthen the core trio (done now)
- PM / ENG / DEV

### Phase 2: Add orchestration-heavy business lenses
- Manager
- Executive
- Customer Success

### Phase 3: Add function-specific ops lenses
- Sales
- IT
- HR
- Finance
- Marketing

This order maximizes reuse of the PM/ENG/DEV lens patterns while expanding into high-frequency stakeholder contexts.

---

## Next Step (Recommended)

Use `palette/lenses/PROMPT_PACK_LENS_TEMPLATE_v0.1.yaml` to create:
- `LENS-MGR-001_manager_execution.yaml`
- `LENS-EXEC-001_executive_decision.yaml`

These two will cover a large percentage of role-pack style requests and improve cross-functional framing immediately.

