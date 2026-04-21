# Tax Preparation Skill — Research & Architecture

**Created**: 2026-04-16
**Status**: Research phase
**Goal**: AI-assisted tax copilot — gathers documents, classifies transactions, drafts forms, flags ambiguities, prepares reviewer-ready package

---

## Honest Scope

This is NOT an autonomous tax filing agent. It's a copilot that:
- ✅ Gathers and organizes tax documents
- ✅ Classifies transactions (business vs personal, deduction categories)
- ✅ Drafts form entries with source citations
- ✅ Flags ambiguities and edge cases for human review
- ✅ Produces a reviewer-ready package (for CPA or self-review)
- ❌ Does NOT file taxes autonomously
- ❌ Does NOT replace professional tax advice
- ❌ Does NOT do tax math in the LLM (deterministic code only)

**Key principle**: LLM handles extraction, ambiguity detection, and explanation. Deterministic code handles tax math, form mapping, and validation rules.

---

## Architecture (5-Agent Design)

| Agent | Role | LLM vs Deterministic |
|-------|------|---------------------|
| Ingestion | Parse receipts, W-2s, 1099s, bank statements | LLM for extraction, code for normalization |
| Tax Rules | Retrieve applicable IRS rules per situation | RAG over IRS publications, not model memory |
| Calculator | Compute tax amounts, deductions, credits | 100% deterministic — no LLM math |
| Reviewer | Flag inconsistencies, missing docs, audit risks | LLM for reasoning, code for threshold checks |
| Export | Generate form drafts, summary package | Templates + LLM for explanatory notes |

---

## Key Resources

### GitHub Repos (ranked by usefulness)

| Repo | Use | Notes |
|------|-----|-------|
| AI Tax Agent | Tax workflow scaffolding | Prototype for basic tax return prep — data input, calculations, doc generation |
| TaxHacker | Document ingestion | Self-hosted AI accounting — receipt/invoice/transaction parsing with LLM |
| FinRobot | Agent orchestration patterns | Director/task-manager coordination for financial workflows |
| TaxGPT | Inspiration only | 2023-era GPT-4 tax Q&A — outdated but useful patterns |

### APIs & Services

| Service | Use | Notes |
|---------|-----|-------|
| IRS API (client ID program) | Official IRS integration | Limited to select products (e-Services, IVES, IRIS) |
| TaxBandits API | Filing rails | 1099, W-2, 940, 941, ACA, W-9/TIN workflows |

### IRS Reference Materials (for RAG)

- IRS Publication 17 (general individual tax guide)
- IRS Publication 535 (business expenses)
- IRS Publication 463 (travel, gift, car expenses)
- Form 1040 instructions
- Schedule C instructions (self-employment)
- Schedule SE instructions (self-employment tax)

---

## Build Plan

### Phase 1: Document Ingestion
- Upload W-2, 1099, bank statements, receipts
- LLM extracts structured data (amounts, dates, categories)
- Normalize into a standard transaction ledger
- Source: TaxHacker patterns

### Phase 2: Transaction Classification
- Categorize each transaction (income type, deduction category)
- Flag ambiguous items for human review
- Apply IRS rules from RAG (not model memory)

### Phase 3: Form Drafting
- Map classified transactions to form fields
- Deterministic tax math (brackets, standard vs itemized, credits)
- Generate draft 1040 + schedules

### Phase 4: Review Package
- Summary of all income, deductions, credits
- Flagged items needing human decision
- Confidence score per line item
- Comparison to prior year (if available)
- Export as PDF or markdown

### Phase 5 (future): Filing Integration
- TaxBandits API for supported forms
- Human approval gate before any submission
- Full audit trail

---

## Safety Controls (Non-Negotiable)

1. **No autonomous filing** — human approval required before any submission
2. **No LLM tax math** — all calculations in deterministic code
3. **Source citations** — every recommendation cites specific IRS publication/section
4. **Confidence thresholds** — items below threshold flagged for human review
5. **Full decision log** — every classification decision recorded with rationale
6. **Disclaimer** — "This is not tax advice. Consult a qualified tax professional."

---

## What We Need to Know First

Before building, clarify:
1. Personal taxes only, or business (Schedule C / 1099) too?
2. Which tax year? (2025 filing in 2026?)
3. Do you have a CPA reviewing, or self-filing?
4. What documents do you have? (W-2s, 1099s, K-1s, receipts, bank statements?)
5. Any specific complexity? (Foreign income, rental property, crypto, stock options?)

---

## Next Steps

- [ ] Answer the scoping questions above
- [ ] Clone AI Tax Agent repo and evaluate
- [ ] Set up IRS publication RAG corpus
- [ ] Build ingestion agent (Phase 1)
- [ ] Test with sample documents
