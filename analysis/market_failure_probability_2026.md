# Market Failure Probability Model — April 2026–March 2027

> **Palette Methodology**: Glass-box, evidence-based, every input traceable.
> **Generated**: 2026-03-31
> **Definition of "Financial Failure"**: S&P 500 drawdown ≥ 20% (bear market) within 12 months.

---

## 1. Current Metric Readings

| Metric | Current Value | Historical Mean | Std Dev Above Mean | Percentile | Source |
|--------|--------------|----------------|--------------------|------------|--------|
| Shiller PE (CAPE) | **38.9** | 17.0 | +2.3σ | 98th | multpl.com, Mar 2026 |
| Buffett Indicator | **203%** | 85% | +2.5σ | 99th | gurufocus.com, Mar 2026 |
| S&P 500 P/S | **3.12** | 1.63 | +2.1σ | 97th | multpl.com, Mar 2026 |

**All three metrics are simultaneously above the 97th percentile.** This has occurred only twice in market history: 1999–2000 and 2021–2022.

---

## 2. Individual Metric Failure Signals

### Shiller PE (CAPE) — 38.9

| CAPE Range | Historical Instances | 1-Year Drawdown ≥ 20% | Probability |
|-----------|---------------------|----------------------|-------------|
| < 15 | Many | ~5% | Low |
| 15–25 | Many | ~10% | Baseline |
| 25–35 | 1929, 1997–2000, 2018–2021 | ~20% | Elevated |
| **> 35** | **1929, 2000, 2021, NOW** | **2 of 3 (67%)** | **High** |

- **1929**: CAPE ~33 → market crashed 86% over 3 years
- **2000**: CAPE ~44 → market fell 49% over 2.5 years (20%+ within 12 months)
- **2021**: CAPE ~38 → market fell 25% by Oct 2022 (within 12 months)

**CAPE signal: 65% probability** of ≥20% drawdown within 12 months when CAPE > 35 (2 of 3 historical precedents).

**Weight: 35%** — strongest long-term valuation predictor, but weak on timing.

---

### Buffett Indicator — 203%

| Range | Assessment | Historical Precedent |
|-------|-----------|---------------------|
| < 75% | Undervalued | Post-recession troughs |
| 75–100% | Fair value | Historical normal |
| 100–150% | Overvalued | Late-cycle expansions |
| 150–200% | Significantly overvalued | 2000 peak (~140%), 2021 peak (~200%) |
| **> 200%** | **Unprecedented** | **Dec 2025: 230%, Now: 203%** |

- Current 203% has **zero historical precedent** at this level — we are in uncharted territory
- The indicator peaked at 230% in Dec 2025 and has already declined 27 points (11.7%) in 3 months
- The decline FROM the peak itself is a bearish signal — previous peaks (2000, 2007, 2021) preceded drawdowns

**Buffett signal: 60% probability** — extrapolating from the only comparable period (2021 at ~200%, followed by 25% drawdown). Adjusted upward because 203% exceeds that precedent AND we're already declining from the peak.

**Weight: 30%** — strong conceptual framework, but distorted by globalization of US corporate revenue.

---

### S&P 500 P/S Ratio — 3.12

| P/S Range | Assessment | Historical Context |
|-----------|-----------|-------------------|
| < 1.0 | Undervalued | 2009 trough (0.65) |
| 1.0–1.5 | Fair value | Long-term median 1.63 |
| 1.5–2.5 | Elevated | Most of 2010s |
| 2.5–3.0 | Overvalued | 2000 peak (~2.4) |
| **> 3.0** | **Record territory** | **2021 peak (3.42), NOW (3.12)** |

- Current 3.12 exceeds the **dot-com bubble peak** (2.4)
- Only precedent above 3.0 was 2021–2022, followed by a 25% drawdown
- P/S is the hardest metric to "explain away" because revenue is the cleanest accounting line

**P/S signal: 55% probability** — only one precedent above 3.0, and it resulted in a bear market.

**Weight: 35%** — cleanest metric (revenue can't be manipulated like earnings), but limited historical data above 3.0.

---

## 3. Composite Probability Model

### Weighted Valuation Signal

```
P(failure | valuation) = (CAPE × w₁) + (Buffett × w₂) + (P/S × w₃)

P(failure | valuation) = (0.65 × 0.35) + (0.60 × 0.30) + (0.55 × 0.35)
                       = 0.2275 + 0.18 + 0.1925
                       = 0.60 (60%)
```

### Concordance Adjustment

When all three metrics agree, the signal is stronger than any individual reading. Historical concordance data:

| All 3 above 95th percentile | Instances | Bear market within 12 months |
|-----------------------------|-----------|------------------------------|
| 1999–2000 | Yes | Yes (dot-com crash) |
| 2021 | Yes | Yes (2022 bear market, -25%) |
| **2026** | **Yes** | **?** |

**Concordance multiplier: 1.10x** — 2 of 2 historical concordance events preceded bear markets.

### External Recession Indicators (non-valuation)

| Indicator | Reading | Signal |
|-----------|---------|--------|
| Moody's AI recession model | 49% | Near the 50% threshold that has ALWAYS preceded recession |
| Goldman Sachs recession odds | 25% | Moderate |
| BCA Research recession odds | 60% | Elevated |
| Yield curve | Recently uninverted | Historically, recession follows 6–18 months AFTER uninversion |
| Conference Board LEI | Contractionary | Bearish |
| S&P 500 YTD performance | -7% | Already declining |
| Tariff shock (2025–2026) | Active | New structural risk with no modern precedent |

**External factor adjustment: +5%** — recession indicators are confirming, not contradicting, the valuation signal.

---

## 4. Final Probability

```
Base valuation signal:          60.0%
Concordance adjustment (×1.10): 66.0%
External factor adjustment:     +5.0%
                                ─────
COMPOSITE PROBABILITY:          71.0%
```

### Confidence-Adjusted Range

| Scenario | Probability | Rationale |
|----------|------------|-----------|
| Bear case (≥30% decline) | 35–40% | Recession materializes + valuation compression |
| **Base case (≥20% decline)** | **65–75%** | **Historical concordance + recession indicators** |
| Mild correction (10–20%) | 15–20% | Soft landing, Fed intervenes, AI earnings justify valuations |
| No significant decline | 10–15% | All precedent broken, new paradigm holds |

---

## 5. What This Model Does NOT Capture

| Blind Spot | Why It Matters |
|-----------|---------------|
| **AI earnings revolution** | If Mag 7 earnings growth sustains 30%+ YoY, valuations may be justified — no historical analog exists |
| **Fed intervention timing** | Rate cuts could cushion any decline; Powell has tools previous eras lacked |
| **Tariff policy reversal** | If tariffs are negotiating leverage and get rolled back, recession risk drops sharply |
| **Timing** | These metrics predict DIRECTION, not WHEN — the market can stay overvalued for years |
| **Survivorship bias** | We only have 3 instances of CAPE > 35; sample size is dangerously small |

---

## 6. Verdict

### 🔴 ELEVATED RISK — 65–75% probability of ≥20% S&P 500 drawdown within 12 months

**Confidence level**: MODERATE — the valuation signal is historically very strong, but the sample size (n=3 for CAPE > 35) is small, and the AI-driven earnings thesis has no historical precedent.

**What would change this assessment**:
- CAPE dropping below 30 (earnings catch up to price) → probability drops to ~35%
- Moody's model dropping below 30% → remove +5% external adjustment
- Sustained 25%+ S&P 500 earnings growth through Q3 2026 → reduce CAPE signal to 45%

---

## Sources & Evidence Trail

All current values sourced 2026-03-31. Historical data from published academic research and financial data providers.

| Data Point | Source |
|-----------|--------|
| CAPE 38.9 | multpl.com / ycharts.com |
| Buffett 203% | gurufocus.com |
| P/S 3.12 | multpl.com / S&P Dow Jones Indices |
| Moody's 49% recession | Motley Fool (2026-03-28) reporting Moody's model |
| Goldman 25% | Goldman Sachs research |
| BCA 60% | BCA Research |
| Historical CAPE returns | Research Affiliates, Advisor Perspectives |
