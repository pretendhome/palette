# Business Plan Creation Agent - Complete Package

**Created**: 2026-02-10  
**Validated**: Rossi Mission engagement (February 2026) - "very well received"  
**Purpose**: Reusable agent for creating comprehensive business plans

---

## What This Agent Does

Creates comprehensive business plans for small businesses through an 8-phase process:

1. **Discovery**: Customer interview → convergence brief
2. **Comparable Research**: Find 2-3 organizations with financial data
3. **Market Research**: Size, trends, segments, competition
4. **Strategic Framework**: Revenue model, org structure, financials
5. **Product Strategy**: Offerings, pricing, go-to-market
6. **Document Assembly**: Executive summary, plan, appendix
7. **Quality Validation**: Score 75+, gap identification
8. **Customer Review**: Feedback, iteration, approval

**Time**: 9-16 agent hours, 2.5-4.5 customer hours, 1-2 weeks elapsed

---

## What It Produces

**Primary Deliverable**: Business plan document (25-50 pages)
- Executive Summary (2 pages)
- Decision Framework (3 pages) - 3-5 ONE-WAY DOORS
- Market Analysis (5-10 pages) - with [Research: ...] citations
- Revenue Model (5-10 pages) - with [Case Study: ...] benchmarks
- Organizational Structure (3-5 pages)
- Product/Service Strategy (5-10 pages)
- Financial Projections (5-10 pages) - 3-year, monthly cash flow
- Implementation Plan (3-5 pages) - 6-week action plan
- Research Appendix (2-5 pages)

**Supporting Deliverables**:
- comparable_organizations.md - 2-3 comparables with financial data
- market_research.md - TAM/SAM/SOM, segments, competition
- strategic_framework.md - Revenue model, financials, expansion
- validation_report.md - Quality score, gaps, recommendations

---

## Success Story: Rossi Mission

**Customer**: Rossi Mission Project (graffiti art gallery + streetwear brand, SF)

**Challenge**: Needed business plan for expansion, organizational structure, revenue optimization

**Process**: 8-phase Palette agent execution (Feb 2026)

**Breakthrough**: Creative Growth Art Center (Oakland) as comparable
- Form 990: $3.26M revenue, 140 artists, 50/50 split, 50 years
- Proved Rossi's nonprofit artist collective model works at scale
- Replaced weak analogies (Supreme, Stüssy) with credible comparable

**Outcome**: "Very well received"
- 25-page main report + 80 pages supporting docs
- Anky validation score: 82/100 (conditional pass)
- Funding probability: ~30% → ~75%
- 3 ONE-WAY DOORS identified: Revenue model, funding ask, governance
- Month 17 cash crisis detected through modeling
- Funding ask increased: $150K → $185-200K (3-month reserve)

---

## How to Use This Agent

### Step 1: Customer Interview (1-2 hours)

Use the convergence brief template:
- `/home/mical/fde/outputs/business-plan-agent/business_plan_convergence_template.md`

**Key Questions**:
- What do you do? (business description)
- What's your challenge? (pain points)
- What's your goal? (short-term + long-term)
- Who are your customers? (segments, needs)
- What are your constraints? (non-negotiables)

**Output**: convergence_brief.md (approved by customer)

---

### Step 2: Execute Agent Sequence

**Phase 2: Argy - Comparable Research** (1-2 hours)
- Prompt: See `business_plan_agent_prompts.md` → Phase 2
- Output: comparable_organizations.md
- Quality Gate: Must find 1+ credible comparable with financial data

**Phase 3: Argy - Market Research** (1-2 hours)
- Prompt: See `business_plan_agent_prompts.md` → Phase 3
- Output: market_research.md
- Quality Gate: All claims must have [Research: ...] citations

**Phase 4: Rex - Strategic Framework** (2-3 hours)
- Prompt: See `business_plan_agent_prompts.md` → Phase 4
- Output: strategic_framework.md
- Quality Gate: Must identify all cash crises (monthly cash flow)
- 🚨 ONE-WAY DOOR: Revenue model selection (customer approval required)
- 🚨 ONE-WAY DOOR: Funding ask amount (customer approval required)

**Phase 5: Rex + Yuty - Product Strategy** (1-2 hours)
- Develop product/service strategy
- Output: product_strategy.md
- Quality Gate: Yuty validates narrative clarity (5-min pitch test)

**Phase 6: Yuty - Document Assembly** (2-3 hours)
- Prompt: See `business_plan_agent_prompts.md` → Phase 6
- Output: business_plan_draft.md
- Quality Gate: All claims have evidence markers [Research: ...] [Case Study: ...]

**Phase 7: Anky - Quality Validation** (1-2 hours)
- Prompt: See `business_plan_agent_prompts.md` → Phase 7
- Output: validation_report.md
- Quality Gate: Score must be 75+ to proceed

**Phase 8: Customer Review** (1-2 hours)
- Customer reviews draft
- Feedback session
- Iteration (if needed)
- 🚨 ONE-WAY DOOR: Final approval (customer confirms accuracy)

---

## Customization by Industry

### Retail/Physical
- Focus: Location, inventory, foot traffic
- Comparables: Similar retail businesses in same geography
- Revenue model: Retail sales, events, workshops
- Metrics: Sales per sq ft, inventory turns, CAC

### SaaS/Software
- Focus: Product-market fit, retention, scalability
- Comparables: Similar SaaS companies (ARR, churn, CAC/LTV)
- Revenue model: Subscriptions, usage-based, enterprise
- Metrics: MRR, churn, CAC/LTV ratio, NPS

### Service Business
- Focus: Delivery model, capacity, utilization
- Comparables: Similar service businesses (revenue per employee)
- Revenue model: Hourly, project-based, retainer
- Metrics: Utilization rate, revenue per employee, retention

### Food/Beverage
- Focus: Operations, supply chain, margins
- Comparables: Similar restaurants/cafes (revenue per seat)
- Revenue model: Dine-in, takeout, catering, retail
- Metrics: Revenue per seat, food cost %, labor cost %

---

## Customization by Stage

### Startup (Pre-revenue)
- Focus: Validation, MVP, initial customers
- Timeline: 6-12 months to first revenue
- Funding: Seed ($50K-$500K)
- Metrics: Customer interviews, pilot users, early traction

### Growth (Revenue <$1M)
- Focus: Scaling, systems, team building
- Timeline: 12-24 months to $1M
- Funding: Series A ($500K-$2M)
- Metrics: Revenue growth, customer acquisition, retention

### Established (Revenue $1M+)
- Focus: Optimization, expansion, profitability
- Timeline: 24+ months to next milestone
- Funding: Series B+ ($2M+) or profitability
- Metrics: Profit margins, market share, expansion rate

---

## Customization by Complexity

### Simple (Single product/service)
- Agent hours: 8-10 hours
- Document length: 15-25 pages
- Revenue streams: 1-3
- Example: Coffee shop, SaaS tool, consulting service

### Medium (Multiple offerings)
- Agent hours: 12-16 hours
- Document length: 25-40 pages
- Revenue streams: 4-7
- Example: Retail + online, multi-product SaaS, agency

### Complex (Multi-sided marketplace)
- Agent hours: 20+ hours
- Document length: 40-60 pages
- Revenue streams: 7-10
- Example: Marketplace, platform, multi-location retail

---

## Files in This Package

### Core Implementation Files
1. **taxonomy_update_business_plan.yaml** - RIU-105, RIU-106, RIU-107 definitions
2. **library_additions_business_plan.yaml** - LIB-089, LIB-090, LIB-091 entries
3. **business_plan_convergence_template.md** - Customer intake template
4. **business_plan_agent_prompts.md** - Agent execution prompts

### Documentation Files
5. **argy_rossi_process_analysis.md** - Reverse-engineered process from Rossi
6. **rex_business_plan_agent_architecture.md** - Formal process architecture
7. **BUSINESS_PLAN_AGENT_README.md** - This file

---

## RIU References

### RIU-105: Business Plan Creation
**Trigger Signals**: business plan, strategic plan, product strategy, go-to-market plan, market analysis, competitive analysis, business model, revenue model, funding requirements

**Agent Sequence**: Orchestrator → Argy (comparable + market) → Rex (strategy + financials) → Yuty (assembly) → Anky (validation) → Human (review)

**Success Criteria**: Comprehensive, evidence-based, comparable-anchored, financially rigorous, clear, actionable, quality score 75+

**Time**: 9-16 agent hours, 2.5-4.5 customer hours, 1-2 weeks elapsed

---

### RIU-106: Comparable Organization Research
**Trigger Signals**: comparable organizations, case studies, who else does this, market validation, proven models

**Agent**: Argentavis (Argy)

**Success Criteria**: Find 1-3 credible comparables with financial data, benchmark key metrics, validate customer's model

**Time**: 1-2 hours

**Rossi Example**: Creative Growth Art Center ($3.26M, 140 artists, 50/50 split, 50 years)

---

### RIU-107: Financial Crisis Detection
**Trigger Signals**: cash flow, runway, funding requirements, when do we run out of money, burn rate

**Agent**: Tyrannosaurus (Rex)

**Success Criteria**: Monthly cash flow Year 1, identify all negative months, calculate 3-month reserve

**Time**: 1 hour

**Rossi Example**: Month 17 crisis detected, funding ask increased $150K → $185-200K

---

## Library References

### LIB-089: Business Model Frameworks
- Business Model Canvas (Osterwalder)
- Value Proposition Canvas (Osterwalder)
- Lean Canvas (Maurya)
- Strategic Framework (Porter's 5 Forces + SWOT)

### LIB-090: Market Research Methods
- Market sizing (TAM/SAM/SOM)
- Customer research (segments, needs, behavior)
- Competitive analysis (direct, indirect, substitutes)
- Industry analysis (Porter's 5 Forces)

### LIB-091: Business Plan Document Structure
- Executive Summary (2 pages)
- Decision Framework (3 pages) - Palette addition
- Market Analysis (5-10 pages)
- Revenue Model (5-10 pages)
- Organizational Structure (3-5 pages)
- Product/Service Strategy (5-10 pages)
- Financial Projections (5-10 pages)
- Implementation Plan (3-5 pages) - Palette addition
- Research Appendix (2-5 pages)

---

## Quality Standards

### Evidence-Based Claims
- All claims must have [Research: ...] or [Case Study: ...] citations
- No unsourced assertions
- Comparable organizations must have financial data (Form 990, SEC filings)

### Financial Rigor
- Monthly cash flow modeling for Year 1
- All negative cash months identified as crises
- Funding ask includes 3-month reserve buffer
- Projections benchmarked against comparables

### Narrative Clarity
- Non-technical language (no jargon)
- Can explain plan in 5 minutes (Yuty validation)
- Clear structure with logical flow
- Professional quality (ready to share with stakeholders)

### Actionability
- 6-week implementation plan with checkboxes
- Week-by-week tasks
- Resource requirements (time, money, people)
- Risk mitigation (what could go wrong)

---

## Success Metrics

### Agent Performance
- Time to completion: 9-16 hours (target)
- Quality score: 75+ (Anky validation)
- Customer satisfaction: "Well-received" (qualitative)
- Execution rate: Customer actually uses plan (follow-up)

### Business Plan Quality
- Comprehensiveness: All sections covered
- Evidence quality: All claims sourced
- Comparable validity: Credible comparable found
- Financial rigor: Cash crises identified
- Narrative clarity: Can explain in 5 min
- Actionability: Customer can execute

---

## Next Steps

### To Use This Agent
1. Copy convergence brief template
2. Interview customer (1-2 hours)
3. Execute agent sequence (9-16 hours)
4. Customer review and approval (1-2 hours)

### To Extend This Agent
1. Add industry-specific templates (retail, SaaS, service, food)
2. Add stage-specific templates (startup, growth, established)
3. Add complexity-specific templates (simple, medium, complex)
4. Test on 2-3 customers across industries
5. Refine based on feedback

### To Integrate with Palette
1. Add RIU-105, RIU-106, RIU-107 to taxonomy v1.3
2. Add LIB-089, LIB-090, LIB-091 to library v1.3
3. Publish to Palette knowledge base
4. Create demo video (Rossi Mission case study)

---

## Questions?

**For technical questions**: See `rex_business_plan_agent_architecture.md` (formal process design)

**For process questions**: See `argy_rossi_process_analysis.md` (reverse-engineered from Rossi)

**For execution questions**: See `business_plan_agent_prompts.md` (agent prompts)

---

**Status**: Ready for production use  
**Validation**: Rossi Mission (Feb 2026) - "very well received"  
**Next**: Test on 2-3 customers across industries
