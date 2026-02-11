# Fixture: Business Plan Document Assembly

**Fixture ID**: YUTY-001
**Agent**: Yutyrannus v1.0
**Scenario**: Assemble research and strategy artifacts into a professional business plan document

---

## Input

**Initial Request**: "Assemble a business plan from the following artifacts: comparable_organizations.md, market_research.md, strategic_framework.md, product_strategy.md. Target: 25-50 pages, professional quality, ready for stakeholders."

**Artifacts Provided**:
- Comparable research (Argy output): 2-3 organizations with financial data
- Market research (Argy output): TAM/SAM/SOM, segments, competition
- Strategic framework (Rex output): Revenue model, financial projections, org structure
- Product strategy (Rex + Yuty output): Offerings, pricing, go-to-market

---

## Expected Output

**Business Plan Document** (25-50 pages) with sections:
1. Executive Summary (2 pages, decision-focused)
2. Decision Framework (3 pages, 3-5 ONE-WAY DOORS with options)
3. Market Analysis (5-10 pages)
4. Revenue Model (5-10 pages)
5. Organizational Structure (3-5 pages)
6. Product/Service Strategy (5-10 pages)
7. Financial Projections (5-10 pages)
8. Implementation Plan (3-5 pages, 6-week action plan)
9. Research Appendix (2-5 pages)

**Evidence Requirements** — every claim must have one of:
- `[Research: source URL or document]`
- `[Case Study: organization name]`
- `[Case Study Pattern: comparable data point]`
- `[Evidence: working code/demo at path]`

**Narrative Requirements**:
- Translates technical/financial data into business value
- Executive summary passes "5-minute pitch test" (can explain in 5 min)
- No marketing fluff — evidence-based claims only
- Limitations and risks explicitly acknowledged

---

## Success Criteria

- Document is 25-50 pages
- All 9 sections present
- Every claim has an evidence marker
- Executive summary is decision-focused (not generic overview)
- Decision framework identifies 3+ ONE-WAY DOORS
- Financial projections include monthly cash flow (not just annual)
- Implementation plan has checkboxes (actionable, not aspirational)
- No unsupported claims or marketing language
- Passes 5-minute pitch test (narrative clarity)
- Did NOT promise unvalidated capabilities
- Did NOT hide limitations

---

## Anti-Patterns to Avoid

- "This revolutionary platform will disrupt..." (marketing fluff)
- "Revenue is projected to grow 300%..." (without [Research: ...] citation)
- "The market opportunity is limitless..." (no market is limitless)
- Hiding Month 17 cash crisis in annual averages
- Using aspirational comparables (Supreme) instead of validated ones (Creative Growth)

---

## Notes

This fixture tests Yuty's core behavior:
- Evidence-obsessed narrative (every claim cited)
- Translating technical to business value
- Honesty about limitations
- Professional document structure
- No overpromising or marketing language
