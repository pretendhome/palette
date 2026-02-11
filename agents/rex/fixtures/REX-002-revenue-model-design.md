# Fixture: Revenue Model Design (Business Plan)

**Fixture ID**: REX-002
**Agent**: Rex v1.0
**Scenario**: Design a revenue model for a small business using comparable organization data and market research

---

## Input

**Initial Request**: "Design a revenue model for a graffiti art gallery with streetwear brand. Customer assumes 64% retail revenue. We have comparable data from Creative Growth ($3.26M revenue, 50/50 split, grant-funded)."

**Expected Clarifying Questions**:
1. What system or decision needs architecture?
2. What constraints exist? (capital, team, location, timeline)
3. What are the success criteria?
4. What have you already ruled out or decided?
5. What's the risk tolerance?

**Sample Answers**:
1. Revenue model — how many streams, what mix, what projections
2. Small team (2 founders), SF rent ($5K/mo), seed funding ~$150K, Year 1 focus
3. Sustainable by Month 18, positive cash flow, diversified revenue
4. Will do 50/50 split with artists (confirmed). Physical gallery space (confirmed).
5. Moderate — need proven model, not experimental

---

## Expected Output

**Decision Classification**: 🚨 ONE-WAY DOOR (revenue model selection)

**3-Stage Analysis**:

1. **Gradient Descent** — 3 viable revenue mix options:
   - Option A: Retail-heavy (64% retail as customer assumed)
   - Option B: Balanced (45% retail, 26% grants, rest from events/commissions)
   - Option C: Events-heavy or alternative mix

2. **Game Theory** — Play options against each other:
   - Where does Option A fail? (over-reliance on foot traffic)
   - Where does Option B win? (matches Creative Growth's proven mix)
   - Scenarios where each option is better/worse

3. **Integration Reasoning** — How does this affect downstream decisions?
   - Funding ask amount depends on revenue mix
   - Team structure depends on revenue mix
   - Cash flow timing depends on grant cycles vs. retail seasonality

**Financial Modeling**:
- 3-year revenue projection
- Monthly cash flow for Year 1
- Cash crisis identification (e.g., Month 17)
- Reserve buffer calculation (3-month runway)

**Recommendation** with:
- Tied to comparable data (Creative Growth model)
- Risk assessment for each option
- Pivot signals ("if retail < 30% by Month 6, shift to Option B")

**Confirmation Required**: Must ask for explicit approval before proceeding

---

## Success Criteria

- Asked all 5 clarifying questions
- Flagged as 🚨 ONE-WAY DOOR
- Presented 3 options using 3-stage analysis (not just "here's my recommendation")
- Used comparable data to anchor projections (not guesses)
- Identified cash crises via monthly modeling (not quarterly)
- Challenged customer's assumption (64% retail) with evidence
- Calculated reserve buffer
- Required human confirmation before proceeding

---

## Rossi Mission Reference

In the validated Rossi engagement, Rex:
- Revised revenue mix from 64% retail → 45% retail, 26% grants
- Detected Month 17 cash crisis through monthly cash flow modeling
- Increased funding ask from $150K → $185-200K (added 3-month reserve)
- Anchored all projections to Creative Growth's proven model

---

## Notes

This fixture tests Rex's core behavior in a business plan context:
- 3-stage reasoning (gradient descent → game theory → integration)
- Challenging assumptions with evidence (customer's 64% retail assumption)
- Monthly cash flow modeling (not just annual)
- ONE-WAY DOOR flagging and confirmation
- Integration reasoning (how revenue model affects everything downstream)
