# Fixture: Comparable Organization Research (Business Plan)

**Fixture ID**: ARG-002
**Agent**: Argentavis v1.0
**Scenario**: Customer needs comparable organizations with financial data to anchor a business plan

---

## Input

**Initial Request**: "I need to find comparable organizations for a graffiti art gallery and streetwear brand in San Francisco. They do 50/50 revenue splits with artists."

**Expected Clarifying Questions**:
1. What decision is this research informing?
2. What have you already tried or know?
3. What would 'good enough' look like?
4. What's the timeline/urgency?
5. What will you do with these findings?

**Sample Answers**:
1. Anchoring a business plan — need financial data to validate revenue model
2. Know about Supreme and Stussy as analogies, but they're not real comparables (different model)
3. 1-3 organizations with actual financial data (Form 990, public filings) — similar model, not just similar vibes
4. Need within 2 hours — feeding into strategic framework phase
5. Rex will use comparables to design revenue model and financial projections

---

## Expected Output

**Comparable Organizations** (2-3) with:
- Organization name and location
- Revenue (from verified financial data, not estimates)
- Operating model (artist count, revenue split, programs)
- Data source (Form 990, SEC filing, annual report — cited)
- Relevance assessment (what matches, what doesn't)

**Red Flags to Catch**:
- Customer's initial analogies (Supreme, Stussy) are aspirational, not comparable
- Must find organizations with similar revenue-split or artist-collective model
- Weak comparables should be flagged as weak, not presented as strong

**Sources**: Must have at least 1 with verifiable financial data (not just press coverage)

---

## Success Criteria

- Agent asked all 5 clarifying questions
- Rejected or flagged weak analogies (aspirational brands ≠ comparables)
- Found at least 1 organization with verifiable financial data
- Cited actual data sources (Form 990, filings), not just articles
- Clearly assessed relevance (what matches, what doesn't)
- Flagged gaps (what couldn't be found)
- Did NOT make recommendations — presented findings only

---

## Rossi Mission Reference

In the validated Rossi engagement, Argy found **Creative Growth Art Center** (Oakland):
- Revenue: $3.26M (Form 990)
- Artists: 140
- Split: 50/50 (matches Rossi model)
- Operating: 50 years (proves long-term viability)

This replaced weak analogies (Supreme, Stussy) with a credible nonprofit comparable.

---

## Notes

This fixture tests Argy's core behavior in a business plan context:
- Distinguishing real comparables from aspirational analogies
- Finding verifiable financial data (not just brand mentions)
- Honest assessment of relevance and gaps
- Staying in research mode (no recommendations)
