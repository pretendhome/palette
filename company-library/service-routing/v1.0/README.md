# Service Routing v1.0 — Phase 2 Complete

**Status**: All 37 "both" RIUs have routing entries (+ 3 additional from Phase 1)
**Date**: 2026-02-24
**Total entries**: 40 (20 full-depth, 20 stubs)

## What this file answers

"For a given RIU, which external service should Palette route to?"

## Coverage

| Category | Count | Status |
|---|---|---|
| Original (Phase 1) | 8 | Full depth with cost estimates |
| Phase 2 high-signal | 12 | Full depth with validated pricing (2026) |
| Phase 2 stubs | 20 | Candidate services listed, no cost validation |
| **Total** | **40** | **All "both" RIUs covered** |

## Phase 2 additions (12 full-depth)

### LLMOps (4)
- **RIU-520**: Prompt Version Control — Braintrust ($249/mo), Helicone ($79/mo), LangSmith ($39/seat/mo)
- **RIU-521**: LLM Model Version Management — OpenRouter (5.5% fee), LiteLLM (free OSS), Vercel AI Gateway ($5/mo free)
- **RIU-522**: Token Budget Management — Helicone, OpenRouter (built-in), LiteLLM (built-in)
- **RIU-524**: LLM Output Quality Monitoring — Braintrust, Arize AI ($50/mo), Evidently AI (OSS free)

### Evaluation & Safety (3)
- **RIU-021**: Golden Set + Offline Eval — Braintrust (10k free scores), LangSmith, Evidently AI
- **RIU-082**: LLM Safety Guardrails — Bedrock Guardrails ($0.15/1K text units), Lakera (10k free req/mo), Guardrails AI (OSS free)
- **RIU-108**: Agent Security — Bedrock Guardrails, Lakera, HashiCorp Vault ($360/mo)

### Research (3)
- **RIU-106**: Comparable Org Research — Perplexity (integrated), Crunchbase ($49/mo), PitchBook ($12K+/yr)
- **RIU-109**: Business Plan Creation — Perplexity (integrated), Gamma ($15/mo API), NotebookLM ($9/license/mo)
- **RIU-140**: Competitive Scan — Perplexity (integrated)

### Observability (2)
- **RIU-061**: Observability Baseline — Datadog ($31/host/mo), Honeycomb (20M free events), Grafana ($19/mo), New Relic (100GB free)
- **RIU-542**: Observability Stack Design — same services as RIU-061

## Key findings from research

1. **WhyLabs is dead** — acquired by Apple, platform discontinued. Removed from consideration. Use Arize AI or Evidently AI instead.
2. **Braintrust raised $80M** (Feb 2026) at $800M valuation — positioning as "the observability layer for AI"
3. **Gamma Generate API is GA** since Jan 2026 — ready for Palette integration
4. **OpenRouter pricing clarified**: 0% markup on model prices; 5.5% credit purchase fee; BYOK 5% fee
5. **Bedrock Guardrails 80-85% price reduction** (Dec 2024) — PII and word filters now FREE

## Files changed in Phase 2

- `service_routing_v1.0.yaml` — 12 full entries + 20 stubs added
- `../people-library/v1.1/people_library_company_signals_v1.1.yaml` — 9 new tools added (v1.1)
- `../integrations/openrouter/recipe.yaml` — NEW
- `../integrations/gamma-api/recipe.yaml` — NEW
- `../integrations/wispr-flow/recipe.yaml` — NEW
