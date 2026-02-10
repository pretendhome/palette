# Palette Company-RIU Mapping Library v1.0

**Version**: 1.0  
**Generated**: 2026-02-10  
**Status**: BASELINE + PERPLEXITY VALIDATION PENDING  
**Purpose**: Map AI companies to Palette RIUs to validate which problems are real (funded = market validation)

---

## Overview

This library extends Palette's taxonomy by mapping real AI companies to the RIUs (Repeatable Implementation Units) they solve. It serves three purposes:

1. **Market Validation**: Companies getting funded = real problems worth solving
2. **Gap Identification**: RIUs with no companies = potential white space or not AI-suitable
3. **Teaching Resource**: Show students which AI problems are hot (most companies/funding)

---

## Structure

```
use_cases/
  ├── customer_engagement_support/
  │   ├── RIU-050 (20+ companies, $700M+)
  │   └── RIU-051 (0 companies, GAP)
  ├── sales_revenue_operations/
  │   ├── RIU-200 (25+ companies, $2B+)
  │   └── RIU-290 (0 companies, GAP)
  └── [10 more use cases]
```

---

## Metadata

- **Total Use Cases**: 12
- **Total RIUs Mapped**: 104
- **Total Companies**: 127 (baseline)
- **Agentic-Native Companies**: 23
- **Gap RIUs**: 15
- **Funding Range**: Seed to Series F+
- **Date Range**: 2011-2026 (prioritized 2023-2026)

---

## Query Patterns Supported

1. "Show me all companies solving RIU-050" → Direct lookup
2. "What's the hottest AI use case?" → Sort by company_count + funding_total
3. "Which RIUs have no companies?" → Filter where company_count = 0
4. "Show me agentic-native companies" → Filter where agentic_native = true
5. "What use cases does Intercom solve?" → Reverse lookup from company name

---

## Data Quality

**Baseline Confidence**: MEDIUM
- Company counts: HIGH (well-known companies)
- Funding amounts: MEDIUM (public data, may be outdated)
- Agentic-native classifications: MEDIUM (based on public descriptions)
- RIU mappings: MEDIUM (inferred from problem patterns)

**Perplexity Validation Needed**:
- Confirm funding amounts (especially 2024-2026 rounds)
- Add missing companies (YC recent batches, stealth companies)
- Validate agentic-native classifications
- Update with 2025-2026 companies

---

## Integration with Palette

**File Location**: `/home/mical/fde/palette/company-library/v1.0/`

**Cross-Reference Strategy**:
- Company library references RIU IDs from taxonomy v1.2
- Taxonomy remains unchanged (stable)
- Company library versioned independently (updates frequently)
- Teaching materials pull from both: taxonomy for RIU definitions, company library for market validation

---

## Usage in Teaching

**For Interview Prep**:
- Show "hot RIUs" (top 10 by company count) to demonstrate market validation
- Show "gap RIUs" to discuss white space opportunities
- Use agentic concentration to teach "what problems are good for agents?"

**For Customer Conversations**:
- "Here are 20 companies solving this problem" → Validates customer's idea
- "No companies solve this yet" → Discuss why (too niche? not AI-suitable? early?)
- "Here's the funding range" → Set expectations for market size

---

## Changelog

**v1.0** (2026-02-10):
- Initial baseline with 127 companies
- 12 use case categories
- 104 RIUs mapped
- 15 gap RIUs identified
- Agentic-native flag added

---

## Next Steps

1. Run Perplexity validation queries
2. Merge Perplexity results with baseline
3. Build v1.1 with validated data
4. Create teaching materials referencing this library

---

**See**: `palette_company_riu_mapping_v1.0.yaml` for full structured data
