---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-149
source_hash: sha256:80cb0be92b4b13d8
compiled_at: 2026-04-23T23:21:17Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 3
tags: [cash-flow, crisis-detection, financial-modeling, foundation, funding, knowledge-entry]
related: [RIU-006, RIU-107]
handled_by: [architect, researcher]
journey_stage: foundation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How do I detect financial crises hidden in revenue projections before they become cash flow emergencies?

RIU-107 defines a cash flow crisis detection methodology. Step 1 — Build Monthly Cash Flow Model: convert revenue projections into monthly cash flows for Year 1 (monthly granularity is essential — quarterly hides crises). For each month, calculate: Cash In (revenue received, not booked) minus Cash Out (COGS, salaries, rent, marketing, loan payments, one-time costs). The delta is net cash flow. Track cumulative cash position month by month. Step 2 — Identify Crisis Months: any month where cumulative cash position goes negative is a crisis month. These are often hidden because annual projections look profitable but monthly timing creates cash gaps. Example: Rossi project found a Month 17 crisis — annual projections showed profitability, but seasonal revenue dips combined with fixed costs created a 2-month negative cash window. Step 3 — Calculate Reserve Buffer: minimum 3-month operating expense reserve. If the business cannot survive 3 months of zero revenue, the funding ask is too low. Step 4 — Right-Size Funding Ask: if crises are detected, increase funding ask to cover: crisis months + 3-month reserve + 10% contingency. In the Rossi example, this increased the funding ask from $150K to $185-200K. Key principle: revenue projections are optimistic by nature. Always model a pessimistic scenario (revenue 30% below projections) and check if crises appear earlier or deeper.

## Definition

RIU-107 defines a cash flow crisis detection methodology. Step 1 — Build Monthly Cash Flow Model: convert revenue projections into monthly cash flows for Year 1 (monthly granularity is essential — quarterly hides crises). For each month, calculate: Cash In (revenue received, not booked) minus Cash Out (COGS, salaries, rent, marketing, loan payments, one-time costs). The delta is net cash flow. Track cumulative cash position month by month. Step 2 — Identify Crisis Months: any month where cumulative cash position goes negative is a crisis month. These are often hidden because annual projections look profitable but monthly timing creates cash gaps. Example: Rossi project found a Month 17 crisis — annual projections showed profitability, but seasonal revenue dips combined with fixed costs created a 2-month negative cash window. Step 3 — Calculate Reserve Buffer: minimum 3-month operating expense reserve. If the business cannot survive 3 months of zero revenue, the funding ask is too low. Step 4 — Right-Size Funding Ask: if crises are detected, increase funding ask to cover: crisis months + 3-month reserve + 10% contingency. In the Rossi example, this increased the funding ask from $150K to $185-200K. Key principle: revenue projections are optimistic by nature. Always model a pessimistic scenario (revenue 30% below projections) and check if crises appear earlier or deeper.

## Evidence

- **Tier 3 (entry-level)**: [SBA: Understanding Cash Flow for Small Business](https://www.sba.gov/business-guide/manage-your-business/manage-your-finances)
- **Tier 3 (entry-level)**: [Y Combinator: Default Alive or Default Dead](https://www.paulgraham.com/aord.html)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-006](../rius/RIU-006.md)
- [RIU-107](../rius/RIU-107.md)

## Handled By

- [Architect](../agents/architect.md)
- [Researcher](../agents/researcher.md)

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-149.
Evidence tier: 3.
Journey stage: foundation.
