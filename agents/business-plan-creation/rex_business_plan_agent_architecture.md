# Rex Architecture: Business Plan Creation Agent

**Agent**: Tyrannosaurus (Architecture)  
**Date**: 2026-02-10  
**Purpose**: Design formal process architecture for reusable Business Plan Creation Agent

---

## 1. Agent Overview

**Purpose**: Create comprehensive business plans for small businesses based on customer conversations and market research

**Success Criteria**:
- Document is comprehensive (covers all strategic elements)
- Document is well-received (customer finds it valuable)
- Document is actionable (customer can execute from it)
- Process is repeatable (works for different customers)
- Time-bounded (8-14 agent hours, 1-2 weeks elapsed)

**Validated**: Rossi Mission engagement (February 2026) - "very well received"

---

## 2. Input Requirements

### From Customer (Required)
- [ ] Business description (what they do, stage, industry)
- [ ] Current challenges/pain points
- [ ] Goals (short-term + long-term)
- [ ] Target customers (segments, needs)
- [ ] Current operations (location, team, resources)
- [ ] Constraints (non-negotiables, values)
- [ ] Timeline (when plan is needed)

### From Agent (Gathered)
- [ ] Comparable organizations (2-3 with financial data)
- [ ] Market research (size, trends, segments)
- [ ] Competitive analysis (direct, indirect, substitutes)
- [ ] Financial benchmarks (revenue mix, costs, growth rates)
- [ ] Industry best practices

---

## 3. Process Architecture

### Phase 1: Discovery & Alignment (Convergence)
**Agent**: Human + Orchestrator  
**Duration**: 1-2 hours  
**Outputs**: convergence_brief.md

**Steps**:
1. Customer interview (structured questions)
   - Business description, stage, industry
   - Current challenges and pain points
   - Goals (short-term + long-term)
   - Target customers
   - Current operations and resources
   - Constraints and non-negotiables

2. Create convergence brief (RIU-001)
   - Goal: What success looks like
   - Roles: Who does what (agents + human)
   - Constraints: What cannot change
   - Non-goals: What's out of scope
   - Success criteria: How we know we're done

3. Scope and timeline agreement
   - Document length (10-50 pages)
   - Timeline (1-2 weeks typical)
   - Customer time required (2-4 hours)

**🚨 ONE-WAY DOOR**: Scope and timeline agreement
- **Why**: Affects resource allocation and expectations
- **Approval**: Customer must confirm before proceeding

**Quality Gate**: Convergence brief must include all 5 elements (Goal, Roles, Constraints, Non-goals, Success Criteria)

---

### Phase 2: Comparable Organization Research
**Agent**: Argentavis (Argy)  
**Duration**: 1-2 hours  
**Outputs**: comparable_organizations.md

**Steps**:
1. Search for comparable organizations
   - Same problem at scale (2-3 organizations)
   - Geographic diversity (if applicable)
   - Stage diversity (startup, growth, established)

2. Extract financial data
   - Form 990 (nonprofits) or public filings (companies)
   - Revenue, costs, model, growth rates
   - Key metrics (customers, employees, locations)

3. Validate customer's model
   - Does comparable prove model works?
   - What's different? (gaps or opportunities)
   - What benchmarks apply?

**Quality Gate**: Must find at least 1 credible comparable with financial data

**Rossi Example**: Creative Growth Art Center (Oakland)
- Form 990: $3.26M revenue, 140 artists, 50/50 split, 50 years
- Proved Rossi's model works at scale
- Replaced weak analogies (Supreme, Stüssy) with credible nonprofit comparable

---

### Phase 3: Market & Competitive Research
**Agent**: Argentavis (Argy)  
**Duration**: 1-2 hours  
**Outputs**: market_research.md

**Steps**:
1. Market sizing
   - TAM (Total Addressable Market)
   - SAM (Serviceable Addressable Market)
   - SOM (Serviceable Obtainable Market)
   - Growth rates and trends

2. Customer segment analysis
   - Demographics, psychographics, behavior
   - Pain points and needs
   - Buying behavior and decision criteria

3. Competitive landscape
   - Direct competitors (same solution, same market)
   - Indirect competitors (different solution, same need)
   - Substitute products (alternative ways to solve problem)
   - Competitive positioning map

4. Industry best practices
   - Revenue models (what works)
   - Cost structures (typical %)
   - Growth patterns (Year 1-3)

**Quality Gate**: All claims must be sourced [Research: ...] or [Case Study: ...]

**Rossi Example**:
- SF retail market: Valencia Street 2-4% vacancy (healthy)
- Workshop pricing: $1,500-3,000 market rate
- Pareto distribution: Top 10% artists generate 60-70% sales

---

### Phase 4: Strategic Framework Development
**Agent**: Tyrannosaurus (Rex)  
**Duration**: 2-3 hours  
**Outputs**: strategic_framework.md

**Steps**:
1. Revenue model design
   - Identify 3-7 revenue streams
   - Benchmark against comparables
   - Project 3-year revenue mix
   - Calculate revenue per stream

2. Organizational structure
   - Legal structure (nonprofit, for-profit, hybrid)
   - Governance model (board size, roles)
   - Team requirements (hires, contractors)
   - Organizational chart

3. Financial modeling
   - 3-year revenue projections
   - Cash flow analysis (monthly for Year 1)
   - Identify cash crises (negative months)
   - Calculate funding requirements (with 3-month reserve)

4. Expansion strategy
   - Geographic expansion (if applicable)
   - Product/service expansion
   - Partnership model
   - Timeline and milestones

**🚨 ONE-WAY DOOR**: Revenue model selection
- **Why**: Affects entire strategy downstream (pricing, team, operations)
- **Approval**: Customer must confirm before proceeding
- **Options**: Provide 3 gradient descent options with tradeoffs

**Quality Gate**: Financial model must identify all cash crises (negative cash months)

**Rossi Example**:
- Revenue model: Flipped from 64% retail to 45% retail, 26% grants (matches Creative Growth)
- Cash crisis: Month 17 identified through modeling
- Funding ask: Increased from $150K to $185-200K (3-month reserve)

---

### Phase 5: Product/Service Strategy
**Agent**: Rex + Yuty collaboration  
**Duration**: 1-2 hours  
**Outputs**: product_strategy.md

**Steps**:
1. Product/service definition
   - Core offerings (what's included)
   - Differentiation (what makes it unique)
   - Value proposition (why customers buy)

2. Pricing strategy
   - Pricing model (subscription, one-time, usage-based)
   - Price points (benchmarked against comparables)
   - Discounts and promotions

3. Go-to-market strategy
   - Customer acquisition channels
   - Marketing tactics
   - Sales process
   - Launch timeline

4. Success metrics
   - Early indicators (0-3 months)
   - Medium-term measures (3-6 months)
   - Long-term goals (6+ months)

**Quality Gate**: Yuty validates narrative clarity (can explain in 5 min?)

**Rossi Example**:
- 3-pillar model: Events, workshops, residencies
- Scarcity economics: 250 SKU cap, limited collaborations
- Artist pipeline: 3-tier system (discovery → development → launch)

---

### Phase 6: Document Assembly
**Agent**: Yutyrannus (Yuty)  
**Duration**: 2-3 hours  
**Outputs**: business_plan_draft.md or .docx

**Steps**:
1. Executive summary (2 pages)
   - Business overview
   - Market opportunity
   - Strategic recommendations
   - Funding requirements
   - Go/no-go recommendation

2. Decision framework (3 pages)
   - 3-5 ONE-WAY DOORS with gradient descent options
   - Human confirmation checkboxes
   - Game theory analysis (when each option wins)

3. Business plan sections (15-25 pages)
   - Market analysis (with [Research: ...] citations)
   - Revenue model (with comparable benchmarks)
   - Organizational structure
   - Product/service strategy
   - Financial projections
   - Implementation plan (6-week action plan)

4. Research appendix (2-5 pages)
   - Comparable organization data
   - Market research sources
   - Financial benchmarks

**Quality Gate**: All claims must have evidence markers [Research: ...] or [Case Study: ...]

**Rossi Example**:
- 25-page main report
- 80 pages total (including supporting docs)
- Every claim cited with [Research: ...] or [Case Study Pattern: ...]

---

### Phase 7: Quality Validation
**Agent**: Ankylosaurus (Anky)  
**Duration**: 1-2 hours  
**Outputs**: validation_report.md

**Steps**:
1. Completeness check
   - All sections present? (executive summary, market, revenue, org, financials, implementation)
   - All ONE-WAY DOORS flagged?
   - All claims sourced?

2. Quality scoring (0-100 scale)
   - Evidence quality: Sourced (10 pts) vs unsourced (0 pts)
   - Comparable validity: Credible (10 pts) vs weak (5 pts) vs none (0 pts)
   - Financial rigor: Modeled (10 pts) vs guessed (0 pts)
   - Actionability: Executable (10 pts) vs aspirational (0 pts)
   - Narrative clarity: Clear (10 pts) vs confusing (0 pts)

3. Gap identification
   - Missing baseline data (customer's actual numbers)
   - Missing case studies (customer's proof points)
   - Inconsistent numbers (revenue doesn't match costs)
   - Unsupported claims (no source)

4. Validation report
   - Score (0-100)
   - What's validated (strengths)
   - What's missing (gaps)
   - Recommendations (fixes)

**Quality Gate**: Score must be 75+ to proceed (conditional pass)

**Rossi Example**:
- Score: 82/100 (conditional pass)
- Validated: Creative Growth comparable, revenue model structure, governance
- Missing: Baseline data, artist case studies, grant reconciliation
- Recommendation: Strong plan, needs real data

---

### Phase 8: Customer Review & Iteration
**Agent**: Human (customer)  
**Duration**: 1 week (async)  
**Outputs**: Final approved business plan

**Steps**:
1. Customer reviews draft
   - Executive summary (5 min)
   - ONE-WAY DOORS (15 min)
   - Full document (30-60 min)

2. Feedback session (30-60 min)
   - Clarifying questions
   - Corrections to assumptions
   - Additional context

3. Iteration (if needed)
   - Agents update based on feedback
   - Re-validate with Anky
   - Customer re-reviews

4. Final approval
   - Customer signs off
   - Document goes live

**🚨 ONE-WAY DOOR**: Final document approval
- **Why**: Customer-facing deliverable, represents their business
- **Approval**: Customer must explicitly confirm

**Quality Gate**: Customer must confirm "this represents my business accurately"

---

## 4. Total Time Budget

**Agent Work**:
- Phase 1: 1-2 hours (Convergence)
- Phase 2: 1-2 hours (Comparable research)
- Phase 3: 1-2 hours (Market research)
- Phase 4: 2-3 hours (Strategic framework)
- Phase 5: 1-2 hours (Product strategy)
- Phase 6: 2-3 hours (Document assembly)
- Phase 7: 1-2 hours (Quality validation)
- **Total**: 9-16 hours

**Customer Time**:
- Phase 1: 1-2 hours (Interview + convergence)
- Phase 4: 30 min (Revenue model approval)
- Phase 8: 1-2 hours (Review + feedback)
- **Total**: 2.5-4.5 hours

**Elapsed Time**: 1-2 weeks (with async customer input)

---

## 5. Customization Points

### By Industry

**Retail/Physical**:
- Focus: Location, inventory, foot traffic
- Comparables: Similar retail businesses in same geography
- Revenue model: Retail sales, events, workshops
- Metrics: Sales per sq ft, inventory turns, customer acquisition cost

**SaaS/Software**:
- Focus: Product-market fit, retention, scalability
- Comparables: Similar SaaS companies (ARR, churn, CAC/LTV)
- Revenue model: Subscriptions, usage-based, enterprise contracts
- Metrics: MRR, churn, CAC/LTV ratio, NPS

**Service Business**:
- Focus: Delivery model, capacity, utilization
- Comparables: Similar service businesses (revenue per employee)
- Revenue model: Hourly, project-based, retainer
- Metrics: Utilization rate, revenue per employee, client retention

**Food/Beverage**:
- Focus: Operations, supply chain, margins
- Comparables: Similar restaurants/cafes (revenue per seat)
- Revenue model: Dine-in, takeout, catering, retail
- Metrics: Revenue per seat, food cost %, labor cost %

### By Stage

**Startup (Pre-revenue)**:
- Focus: Validation, MVP, initial customers
- Timeline: 6-12 months to first revenue
- Funding: Seed round ($50K-$500K)
- Metrics: Customer interviews, pilot users, early traction

**Growth (Revenue <$1M)**:
- Focus: Scaling, systems, team building
- Timeline: 12-24 months to $1M
- Funding: Series A ($500K-$2M)
- Metrics: Revenue growth, customer acquisition, retention

**Established (Revenue $1M+)**:
- Focus: Optimization, expansion, profitability
- Timeline: 24+ months to next milestone
- Funding: Series B+ ($2M+) or profitability
- Metrics: Profit margins, market share, expansion rate

### By Complexity

**Simple (Single product/service)**:
- Agent hours: 8-10 hours
- Document length: 15-25 pages
- Revenue streams: 1-3
- Example: Coffee shop, SaaS tool, consulting service

**Medium (Multiple offerings)**:
- Agent hours: 12-16 hours
- Document length: 25-40 pages
- Revenue streams: 4-7
- Example: Retail + online, multi-product SaaS, agency with services

**Complex (Multi-sided marketplace)**:
- Agent hours: 20+ hours
- Document length: 40-60 pages
- Revenue streams: 7-10
- Example: Marketplace, platform, multi-location retail

---

## 6. Decision Points (Human Approval Required)

### 🚨 ONE-WAY DOOR 1: Scope and Timeline (Phase 1)
**Why**: Affects resource allocation and expectations  
**When**: Before starting research  
**Approval**: Customer

**Gradient Descent Options**:
1. **Quick (8-10 hours, 1 week)**: Executive brief only, limited research
2. **Standard (12-16 hours, 2 weeks)**: Full business plan, comprehensive research
3. **Deep (20+ hours, 3-4 weeks)**: Detailed analysis, multiple scenarios

**Game Theory**:
- Quick wins: Urgent timeline, simple business, internal use only
- Standard wins: Typical case, external stakeholders, funding required
- Deep wins: Complex business, high stakes, investor pitch

---

### 🚨 ONE-WAY DOOR 2: Revenue Model Selection (Phase 4)
**Why**: Affects entire strategy downstream (pricing, team, operations)  
**When**: After market research, before product strategy  
**Approval**: Customer

**Gradient Descent Options**:
1. **Single stream (e.g., retail only)**: Simple, focused, easier to execute
2. **Diversified (3-5 streams)**: Balanced risk, multiple revenue sources
3. **Aggressive (7+ streams)**: Maximum revenue, complex operations

**Game Theory**:
- Single wins: Early stage, limited resources, need focus
- Diversified wins: Growth stage, proven model, want stability
- Aggressive wins: Established, strong team, maximize revenue

**Rossi Example**: Chose diversified (7 streams: retail, workshops, grants, events, online, residencies, collaborations)

---

### 🚨 ONE-WAY DOOR 3: Funding Ask Amount (Phase 4)
**Why**: Affects runway, dilution, investor expectations  
**When**: After financial modeling, before document assembly  
**Approval**: Customer

**Gradient Descent Options**:
1. **Conservative (6-12 months runway)**: Lower ask, faster raise, less dilution
2. **Standard (12-18 months runway)**: Typical ask, balanced risk
3. **Aggressive (18-24 months runway)**: Higher ask, longer runway, more dilution

**Game Theory**:
- Conservative wins: Easy to raise, low dilution, fast execution
- Standard wins: Typical case, balanced risk/reward
- Aggressive wins: Complex execution, want buffer, hard to raise again

**Rossi Example**: Chose aggressive ($185-200K for 18+ months) due to Month 17 cash crisis

---

### 🚨 ONE-WAY DOOR 4: Final Document Approval (Phase 8)
**Why**: Customer-facing deliverable, represents their business  
**When**: After customer review and iteration  
**Approval**: Customer

**Confirmation Required**:
- [ ] This represents my business accurately
- [ ] I can execute this plan
- [ ] I'm comfortable sharing this with stakeholders
- [ ] I approve the funding ask amount

---

## 7. Quality Gates

**Gate 1: Convergence Brief Complete** (Phase 1)
- All 5 elements present (Goal, Roles, Constraints, Non-goals, Success Criteria)
- Customer has approved scope and timeline
- **Pass/Fail**: Must pass to proceed

**Gate 2: Comparable Found** (Phase 2)
- At least 1 credible comparable with financial data
- Comparable validates customer's model (or identifies gaps)
- **Pass/Fail**: Must pass to proceed (or adjust strategy)

**Gate 3: Research Sourced** (Phase 3)
- All claims have [Research: ...] or [Case Study: ...] citations
- No unsourced assertions
- **Pass/Fail**: Must pass to proceed

**Gate 4: Cash Crises Identified** (Phase 4)
- Financial model shows monthly cash flow for Year 1
- All negative cash months identified
- Funding ask includes 3-month reserve buffer
- **Pass/Fail**: Must pass to proceed

**Gate 5: Narrative Clear** (Phase 5)
- Yuty can explain strategy in 5 min
- Non-technical language (no jargon)
- **Pass/Fail**: Must pass to proceed

**Gate 6: Evidence Markers Present** (Phase 6)
- All claims have [Research: ...] or [Case Study: ...] markers
- All ONE-WAY DOORS flagged with 🚨
- **Pass/Fail**: Must pass to proceed

**Gate 7: Quality Score 75+** (Phase 7)
- Anky validation score 75+ (conditional pass)
- Gaps identified and documented
- **Pass/Fail**: Must pass to proceed (or iterate)

**Gate 8: Customer Approval** (Phase 8)
- Customer confirms accuracy
- Customer approves funding ask
- **Pass/Fail**: Must pass to deliver

---

## 8. Output Specifications

### Business Plan Document Structure

**1. Executive Summary** (2 pages)
- Business overview (what, who, where)
- Market opportunity (size, trends, segments)
- Unique value proposition (why customers buy)
- Strategic recommendations (key decisions)
- Financial summary (revenue, costs, funding)
- Go/no-go recommendation

**2. Decision Framework** (3 pages)
- 3-5 ONE-WAY DOORS with gradient descent options
- Human confirmation checkboxes
- Game theory analysis (when each option wins)

**3. Market Analysis** (5-10 pages)
- Market size and trends (TAM, SAM, SOM)
- Customer segments (demographics, needs, behavior)
- Competitive landscape (direct, indirect, substitutes)
- Market positioning (differentiation)
- [Research: ...] citations throughout

**4. Revenue Model** (5-10 pages)
- Revenue streams (3-7 streams with projections)
- Pricing strategy (benchmarked against comparables)
- 3-year revenue projections (Year 1-3)
- Revenue mix evolution (% per stream over time)
- [Case Study: ...] benchmarks

**5. Organizational Structure** (3-5 pages)
- Legal structure (nonprofit, for-profit, hybrid)
- Governance model (board size, roles, meetings)
- Team requirements (hires, contractors, advisors)
- Organizational chart

**6. Product/Service Strategy** (5-10 pages)
- Core offerings (what's included)
- Differentiation (what makes it unique)
- Go-to-market strategy (channels, tactics, timeline)
- Success metrics (early, medium, long-term)

**7. Financial Projections** (5-10 pages)
- 3-year revenue projections (by stream)
- Cost structure (fixed vs variable)
- Cash flow analysis (monthly Year 1, quarterly Year 2-3)
- Funding requirements (with 3-month reserve)
- Key assumptions (growth rates, conversion rates, etc.)

**8. Implementation Plan** (3-5 pages)
- 6-week action plan (week-by-week tasks)
- Milestones and checkpoints
- Resource requirements (time, money, people)
- Risk mitigation (what could go wrong)

**9. Research Appendix** (2-5 pages)
- Comparable organization data (Form 990, financials)
- Market research sources (reports, studies, data)
- Financial benchmarks (industry averages)

**Total Length**: 25-50 pages (depending on complexity)

---

## 9. Agent Coordination Flow

```
Customer Interview (Human)
    ↓
Convergence Brief (Orchestrator) → 🚨 ONE-WAY DOOR (Scope/Timeline)
    ↓
Comparable Research (Argy) → comparable_organizations.md
    ↓
Market Research (Argy) → market_research.md
    ↓
Strategic Framework (Rex) → 🚨 ONE-WAY DOOR (Revenue Model)
    ↓
Financial Modeling (Rex) → 🚨 ONE-WAY DOOR (Funding Ask)
    ↓
Product Strategy (Rex + Yuty) → product_strategy.md
    ↓
Document Assembly (Yuty) → business_plan_draft.md
    ↓
Quality Validation (Anky) → validation_report.md (Score 75+)
    ↓
Customer Review (Human) → feedback.md
    ↓
Iteration (if needed) → Re-validate with Anky
    ↓
Final Approval (Human) → 🚨 ONE-WAY DOOR (Document Live)
    ↓
Delivery
```

---

## 10. Success Metrics

### For Agent Performance
- **Time to completion**: 8-14 agent hours (target)
- **Quality score**: 75+ (Anky validation)
- **Customer satisfaction**: "Well-received" (qualitative)
- **Execution rate**: Customer actually uses plan (follow-up)

### For Business Plan Quality
- **Comprehensiveness**: All sections covered (checklist)
- **Evidence quality**: All claims sourced (no unsourced assertions)
- **Comparable validity**: Credible comparable found (financial data)
- **Financial rigor**: Cash crises identified (monthly cash flow)
- **Narrative clarity**: Can explain in 5 min (Yuty validation)
- **Actionability**: Customer can execute (6-week plan)

---

## 11. Failure Modes & Mitigations

### Failure Mode 1: Generic/Templated Output
**Symptom**: Plan reads like template, not specific to customer  
**Root Cause**: Insufficient customer context or weak comparables  
**Mitigation**:
- Argy must find customer-specific comparables (not generic)
- Anky checks for customization (score penalty for generic language)
- Customer review catches generic sections

### Failure Mode 2: Unrealistic Projections
**Symptom**: Revenue projections not achievable  
**Root Cause**: Not benchmarked against comparables  
**Mitigation**:
- Rex must benchmark all projections against comparables
- Anky checks for "venture-scale growth" in non-venture businesses
- Customer review validates assumptions

### Failure Mode 3: Unclear Narrative
**Symptom**: Customer can't explain plan to stakeholders  
**Root Cause**: Jargon, complexity, poor structure  
**Mitigation**:
- Yuty semantic validation (5-min pitch test)
- Non-technical language requirement
- Customer review catches confusion

### Failure Mode 4: Missing Customer Context
**Symptom**: Plan doesn't reflect customer's reality  
**Root Cause**: Insufficient discovery in Phase 1  
**Mitigation**:
- Convergence brief must capture all context
- Customer review in Phase 8 catches misalignment
- Iteration loop allows corrections

### Failure Mode 5: Hidden Cash Crises
**Symptom**: Customer runs out of money unexpectedly  
**Root Cause**: No monthly cash flow modeling  
**Mitigation**:
- Rex must model monthly cash flow for Year 1
- Quality gate requires all negative months identified
- Funding ask must include 3-month reserve

---

## 12. Next Steps for Implementation

**Step 1: Create RIU-105 (Business Plan Creation)** in taxonomy
- Add to palette_taxonomy_v1.2.yaml
- Define trigger signals, agent sequence, success criteria
- Reference Rossi Mission as validation

**Step 2: Add Library Entries** (3 new entries)
- LIB-089: Business Model Frameworks
- LIB-090: Market Research Methods
- LIB-091: Business Plan Document Structure

**Step 3: Create Agent Prompt Templates**
- Argy: Comparable organization search
- Rex: Revenue model design
- Yuty: Document assembly
- Anky: Quality validation

**Step 4: Create Convergence Brief Template**
- Standardize customer intake questions
- Define scope/timeline options
- Identify ONE-WAY DOORS upfront

**Step 5: Test on 2-3 Customers**
- Different industries (retail, SaaS, service)
- Different stages (startup, growth, established)
- Measure time and quality

**Step 6: Package as Repeatable Offering**
- Create master README
- Document customization points
- Publish to Palette knowledge base

---

**Status**: Architecture complete, ready for Theri implementation

**Next Agent**: Therizinosaurus (Theri) to build agent files (RIU, library, templates)
