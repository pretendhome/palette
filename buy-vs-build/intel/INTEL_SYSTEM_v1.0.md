# Intel System — Financial Intelligence Architecture v1.0

**Date**: 2026-05-01
**Status**: WORKING
**Parallel to**: Palette Intelligence System (PIS) — same schema pattern, independent data and code
**Domain**: Oil/energy investment, AI portfolio tracking, macro stress indicators

---

## 1. What This Is

The Intel System is the investment-domain equivalent of PIS. It answers:

1. **"Who says what?"** — Which trusted financial voices have signals on a given thesis?
2. **"What's the consensus?"** — Do multiple voices agree, and is that consensus crowded or genuine?
3. **"What should I research?"** — Which voices and queries will give the most decision-relevant intelligence?

It is NOT connected to PIS. PIS tracks tech influencers and AI tools for build decisions. Intel tracks financial voices for investment decisions.

---

## 2. Architecture: Three Layers

```
palette/buy-vs-build/
├── intel/                                    ← THIS SYSTEM
│   ├── INTEL_SYSTEM_v1.0.md                 ← This document
│   ├── intel_engine.py                      ← Query engine (CLI + bot integration)
│   │
│   ├── people-library/                       ← LAYER 1: Financial Voices
│   │   └── v1.0/
│   │       ├── financial_voices.yaml         ← 25 profiles across 5 clusters
│   │       └── thesis_signals.yaml           ← Voice → thesis cross-reference
│   │
│   ├── thesis-categories/                    ← LAYER 2: Investment Thesis Categories
│   │   └── v1.0/
│   │       └── categories.yaml              ← 9 thesis categories with decay rates
│   │
│   └── scoring/                              ← LAYER 3: Prediction Accuracy Tracking
│       └── forecaster_scores.yaml            ← Brier scores, calibration, weights
│
├── PALETTE_INTELLIGENCE_SYSTEM_v1.0.md       ← PIS (SEPARATE — do not touch)
├── people-library/                            ← PIS people library (SEPARATE)
└── v1.0/                                      ← PIS company-RIU index (SEPARATE)
```

---

## 3. Layer 1: Financial Voices (25 profiles)

### Clusters

| Cluster | Voices | Domain |
|---------|--------|--------|
| oil_energy_analysts | FIN-001 to FIN-005 | Oil/energy markets |
| ai_investment_voices | FIN-008 to FIN-013 | AI company investments |
| macro_stress_indicators | FIN-014, FIN-017, FIN-018 | Macro stress |
| hidden_gem_predictors | FIN-003, FIN-004, FIN-005, FIN-016, FIN-019, FIN-021 to FIN-025 | Cross-domain, high accuracy |
| cross_domain_bridge | FIN-006, FIN-007, FIN-015, FIN-020 | Energy + AI + macro integration |

### Signal Types

- **analyst** — journalist or institutional strategist
- **newsletter** — independent paid/free newsletter
- **fund_manager** — manages capital with verified returns
- **academic** — university-based with public models
- **platform** — forecasting platform (Good Judgment, Polymarket)
- **insider** — company founder or executive

### Signal Quality

- **high** — multi-source validation, documented track record
- **medium** — single strong signal or partial track record
- **low** — single recommender, no verified track record
- **unvalidated** — newly added, not yet assessed

---

## 4. Layer 2: Thesis Categories (9 categories)

| Category | Domain | Decay (days) | Voices |
|----------|--------|-------------|--------|
| THESIS-OIL-UPSTREAM | oil-energy | 4 | 7 |
| THESIS-OIL-REFINING | oil-energy | 4 | 3 |
| THESIS-OIL-MIDSTREAM | oil-energy | 7 | 2 (gap) |
| THESIS-ENERGY-TRANSITION | oil-energy | 14 | 4 |
| THESIS-AI-INFRASTRUCTURE | ai-investment | 10 | 5 |
| THESIS-AI-COMPANIES | ai-investment | 10 | 5 |
| THESIS-MACRO-VALUATIONS | macro-stress | 21 | 5 |
| THESIS-MACRO-LIQUIDITY | macro-stress | 21 | 4 |
| THESIS-MACRO-GEOPOLITICAL | macro-stress | 10 | 5 |

### Decay Half-Lives

Signals lose value over time. Decay rate varies by domain:
- **Oil/energy**: 4 days (supply shocks, OPEC decisions change fast)
- **AI investment**: 10 days (weekly earnings/product cycles)
- **Macro stress**: 21 days (monthly economic data releases)

Formula: `freshness = e^(-ln(2) / half_life * age_days)`

---

## 5. Layer 3: Scoring (Brier-based)

### Algorithm

1. **Weight by accuracy**: `w = softmax(-BrierScore / temperature)`
2. **Aggregate**: `p_agg = sum(w_i * p_i) / sum(w_i)`
3. **Extremize** (Tetlock): push consensus toward 0/1 by factor `d = 1.5 + 0.5 * log(N)`
4. **Detect crowded trades**: consensus >85% AND dispersion <5% → flag, boost contrarian 1.5x
5. **Apply decay**: weight predictions by freshness using domain-specific half-lives

### Status

Scoring is schema-ready but has no logged predictions yet. Scores will populate as predictions are logged and resolved through the `/intel` command.

---

## 6. Entry Points

### CLI

```bash
# Full brief across all thesis categories
python3 intel_engine.py --brief

# Query a specific topic
python3 intel_engine.py --query "Is the refining supercycle thesis intact?"

# Look up a thesis category directly
python3 intel_engine.py --thesis THESIS-OIL-UPSTREAM

# Include live Perplexity search
python3 intel_engine.py --query "OPEC production decision" --perplexity

# Format for Telegram
python3 intel_engine.py --brief --telegram
```

### Telegram Bot (joseph_bridge.py)

```
/intel                    — Full brief across all categories
/intel oil upstream       — Query routed to THESIS-OIL-UPSTREAM
/intel crack spreads      — Query routed to THESIS-OIL-REFINING
/intel AI capex           — Query routed to THESIS-AI-INFRASTRUCTURE
/intel CAPE ratio         — Query routed to THESIS-MACRO-VALUATIONS
```

### Local Use (your PC)

Same engine, any workspace. For personal use:

```bash
cd ~/fde/palette/buy-vs-build/intel
python3 intel_engine.py --query "Should I invest in a startup doing X?"
```

The engine is workspace-agnostic — it reads the same voice library regardless of context. For different domains (startup planning, etc.), add new thesis categories to `categories.yaml` and new voices to `financial_voices.yaml`.

---

## 7. Relationship to Other Systems

| System | Purpose | Connection to Intel |
|--------|---------|-------------------|
| PIS (buy-vs-build/) | Tech tool routing for builds | NONE — separate data, separate code |
| Joseph Bot (mission-canvas/) | Telegram interface | Intel engine called via `/intel` command |
| Monitor Daemon | Scheduled market alerts | Independent — monitors run on schedule, intel runs on demand |
| Knowledge Library | Palette sourced knowledge | Independent — intel has its own voice library |

---

## 8. Gaps and Roadmap

### Current Gaps
- **THESIS-OIL-MIDSTREAM**: Only 2 voices — needs a dedicated midstream analyst
- **THESIS-OIL-REFINING**: Thin coverage — Rory Johnston is the only deep source
- **Scoring**: No predictions logged yet — system learns as predictions accumulate

### v1.1 Roadmap
- [ ] Add 3-5 more voices (midstream, refining, emerging market)
- [ ] Log first 10 predictions and track to resolution
- [ ] Connect `/intel` to joseph_bridge.py
- [ ] Build Perplexity auto-enrichment for voice profiles (monthly cadence)
- [ ] Add startup/venture thesis categories for personal use

---

*Created 2026-05-01. Research basis: Perplexity search passes for high-impact voices, hidden-gem predictors, and prediction market algorithms.*
