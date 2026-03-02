# Fixture: Business Plan Quality Validation

**Fixture ID**: ANKY-001
**Agent**: Ankylosaurus v1.0
**Scenario**: Validate a completed business plan draft against quality standards

---

## Input

**Initial Request**: "Validate this business plan draft for quality. Must score 75+ to proceed to customer review. Check completeness, evidence quality, financial rigor, and actionability."

**Artifact Provided**: business_plan_draft.md (25-50 page business plan from Yuty)

---

## Expected Output

**Validation Report** with:

### 7-Point Checklist
1. **Completeness**: All 9 sections present? ✓ / ✗ with specifics
2. **Clarity**: Unambiguous, understandable by non-technical stakeholder?
3. **Feasibility**: Can be executed with stated resources?
4. **Risks**: Identified and categorized (CRITICAL/HIGH/MEDIUM/LOW)
5. **Gaps**: What's missing, with impact assessment
6. **Dependencies**: What's required but not controlled
7. **Readiness**: GO / NO-GO / CONDITIONAL

### Quality Scoring (0-100)
Score each dimension 0-10:
1. Evidence quality (sourced vs. unsourced claims)
2. Comparable validity (credible vs. weak comparables)
3. Financial rigor (monthly modeled vs. guessed annually)
4. Actionability (executable vs. aspirational)
5. Narrative clarity (clear vs. confusing)
6. ONE-WAY DOORS (all flagged with options?)
7. Benchmarking (projections anchored to comparables?)
8. Gap identification (missing data documented?)
9. Professional quality (ready for stakeholders?)
10. Implementation plan (actionable with timeline?)

**Total score**: Sum / 100

### Recommendations
- **Must address** (blocking): Issues that prevent proceeding
- **Should address** (important): Issues that weaken the plan
- **Could address** (nice-to-have): Polish items

---

## Success Criteria

- All 10 quality dimensions scored individually
- Total score calculated correctly
- Each score has specific justification (not just a number)
- Unsourced claims identified explicitly
- Cash flow modeling checked (monthly vs. quarterly/annual)
- ONE-WAY DOOR completeness verified
- GO/NO-GO/CONDITIONAL decision provided
- Recommendations categorized by severity
- Did NOT fix any issues (assessment only)
- Did NOT make strategic recommendations
- Did NOT proceed past assessment

---

## Test Cases

**Case A — High Quality Plan (expected score 80+)**:
- All sections present, all claims sourced, monthly cash flow modeled
- Expected: GO with minor polish items

**Case B — Medium Quality Plan (expected score 60-74)**:
- Missing implementation plan, some unsourced claims, quarterly cash flow only
- Expected: CONDITIONAL with must-address items

**Case C — Low Quality Plan (expected score <60)**:
- Multiple sections missing, no comparables cited, no cash flow model
- Expected: NO-GO with blocking issues listed

---

## Anti-Patterns to Avoid

- Scoring generously to avoid conflict (if it's a 6, say 6)
- Suggesting fixes instead of identifying problems
- Skipping the financial rigor check (most common miss)
- Not verifying evidence markers are present
- Providing a GO without checking all 10 dimensions

---

## Notes

This fixture tests Anky's core behavior:
- Rigorous, honest assessment (no grade inflation)
- Systematic quality scoring (all 10 dimensions)
- Clear GO/NO-GO/CONDITIONAL decision
- Assessment only — no remediation
- Severity-categorized recommendations
