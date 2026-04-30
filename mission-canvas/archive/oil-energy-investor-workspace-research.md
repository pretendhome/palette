# Oil & Energy Investor Workspace: Comprehensive Research Report

**Research date:** March 30, 2026  
**Purpose:** Domain knowledge foundation for a voice-first decision-convergence workspace for an oil/energy investor. Covers commodity frameworks, financial interpretation, regulatory landscape, current market context, and AI product design patterns.

---

## Executive Summary

Oil markets are in a geopolitically-driven spike as of March 2026. Brent crude hit $105.85/bbl on March 26 — up ~40% in 30 days — driven by active military conflict near the Strait of Hormuz, Iranian production shut-ins, and U.S.-Russia sanctions complexities. OPEC+ frozen quotas are being overridden by Saudi Arabia's swing producer response to the crisis. WTI trades at roughly a $6–10 discount to Brent. The crack spread widened sharply to $55.78/bbl on March 20. US shale producers remain disciplined rather than reactive: returning 68% of FCF to shareholders. The EIA forecasts Brent to ease from $95+ to ~$70/bbl by year-end 2026 once Hormuz disruption resolves, then $64/bbl average in 2027.

On the AI product side, the tools to build a voice-first decision workspace now exist and are production-ready. Deepgram Nova-3 for STT (sub-300ms, 5-7% WER), ElevenLabs or OpenAI TTS for executive-quality output, LiveKit for real-time voice infrastructure, Vapi for rapid telephony deployment. Bloomberg ASKB launched in Q1 2026 as the first agentic AI on a professional financial terminal, validating the product category. Enverus AI and Rystad Energy are the most advanced oil-specific intelligence platforms. The gap in the market is a portable, voice-first, investor-owned workspace that integrates live commodity data, FERC/SEC filings monitoring, and portfolio-specific state tracking — none of the current tools deliver that end-to-end.

---

# PART 1: Oil & Energy Industry — Domain Knowledge

## 1.1 Commodity Frameworks

### WTI vs. Brent Crude

**West Texas Intermediate (WTI)** is the primary US crude oil benchmark, priced at Cushing, Oklahoma and traded on the NYMEX. **Brent** is the international benchmark, reflecting seaborne oil from the North Sea, and is used to price approximately two-thirds of the world's internationally traded crude.

The spread between WTI and Brent typically reflects logistical and quality differences. When US crude production surges and export infrastructure is constrained, WTI trades at a discount to Brent. When US export capacity is ample and global supply is tight, the spread compresses. The spread matters for investment decisions because it affects US refiner input costs, US E&P netback realizations, and international crude trade routing.

**Current spread (March 2026):** WTI is trading approximately $6–11/bbl below Brent. Brent settled at $105.85 on March 26 ([Fortune](https://fortune.com/article/price-of-oil-03-26-2026/)); WTI settled near $94–95/bbl in mid-March ([24/7 Wall Street](https://247wallst.com/investing/2026/03/18/one-of-these-oil-services-stocks-is-pulling-away-from-the-pack-baker-hughes-haliburton-slb/)). This wider-than-normal spread reflects Hormuz disruption affecting seaborne Brent-linked grades more than landlocked WTI.

**5-year historical spread (2021–2025):** Historically ranged from roughly $1.50–$6/bbl WTI discount. The spread reached unusual levels in 2022 during the post-Ukraine supply shock. Data from [FRED / St. Louis Fed](https://fred.stlouisfed.org/graph?graph_id=126777) and [Investing.com historical data](https://www.investing.com/commodities/brent-wti-crude-spread-futures-historical-data) show recent (early 2026) spread in the $-5.93 to $-6.17 range before the Hormuz escalation widened it further. [RBN Energy's Brent vs. WTI Spread tracker](https://rbnenergy.com/market-data/brent-vs-wti-spread) is the primary practitioner resource.

### Natural Gas Pricing

**Henry Hub** is the US natural gas benchmark, priced at the Erath, Louisiana pipeline hub and traded on NYMEX. It reached a historic inflation-adjusted low in 2024, averaging **$2.21/MMBtu** for the full year — the lowest annual average on record — with a monthly low of $1.51/MMBtu in March 2024, per [EIA's 2024 analysis](https://www.eia.gov/todayinenergy/detail.php?id=64184).

**LNG export pricing** is not based on Henry Hub. US LNG exports are typically priced at Henry Hub plus a liquefaction fee (roughly $3.00–$3.50/MMBtu) plus shipping. European and Asian LNG trades at JKM (Japan-Korea Marker) or TTF (Dutch Title Transfer Facility) prices, which are substantially higher. This creates a fundamental disconnect: US domestic gas can be near $2/MMBtu while European buyers pay $10–15/MMBtu. The spread is the economic engine for US LNG export expansion. [Capital Economics](https://www.capitaleconomics.com/publications/commodities-update/higher-lng-demand-drive-henry-hub-prices) forecasts Henry Hub to rise from ~$3.00/MMBtu to $4.00 by end-2026 and $4.50/MMBtu by end-2027 as LNG export capacity expands.

**Gas-to-oil ratio:** The historic rule of thumb is a 6:1 ratio by energy content (1 barrel of oil ≈ 6 MMBtu of gas). At $60/bbl oil and $3/MMBtu gas, oil prices a $10/MMBtu energy-equivalent versus gas at $3 — a 3:1 premium. This ratio drives decisions about associated gas management, gas re-injection vs. flaring, and which resource type operators prioritize.

### Crack Spreads

The **3-2-1 crack spread** is the industry standard benchmark for US refining margins. It models a refinery converting 3 barrels of crude into 2 barrels of gasoline and 1 barrel of distillate (diesel/heating oil), approximating the actual product yield of a typical US Gulf Coast refinery, per [EIA's crack spread explainer](https://www.eia.gov/todayinenergy/includes/crackspread_explain.php).

**Formula:** \( \text{Crack Spread} = \frac{2 \times \text{Gasoline} + 1 \times \text{Distillate}}{3} - \text{Crude} \)

Expressed in $/barrel, it represents the gross refining margin before operating costs. Per [IB Interview Questions' guide](https://ibinterviewquestions.com/guides/energy-investment-banking/crack-spreads-refining-margins-3-2-1), an example with WTI at $72/bbl, RBOB at $100.80/bbl, and heating oil at $107.10/bbl yields a crack spread of $30.90/bbl.

**Current reading (March 2026):** The 3-2-1 crack spread hit **$55.78/bbl on March 20**, a $15.59/bbl week-over-week surge as refined product prices outpaced crude — a direct consequence of Hormuz disruption tightening product markets while high crude prices compressed upstream margins in the opposite direction for refiners vs. producers ([RBN Energy, March 26 2026](https://rbnenergy.com/daily-posts/analyst-insight/refinery-margins-skyrocket-fuel-gains-outpace-crude)).

Refiners watch crack spreads as a real-time proxy for their gross margin. A widening crack spread signals better refining economics; narrowing signals compression. Gulf Coast crack spreads had fallen to $12–18/bbl in 2025 before the March 2026 spike, per [Deloitte's 2026 outlook](https://www.deloitte.com/us/en/insights/industry/oil-and-gas/oil-and-gas-industry-outlook.html).

Variations: **2-1-1** (better for European diesel-heavy refiners) and **5-3-2** (more distillate-heavy refineries).

### Upstream vs. Downstream Price Sensitivity

**Upstream E&P companies** are highly leveraged to oil prices. Their revenue is essentially (production volume × realized price), so a $10/bbl move in oil directly impacts EBITDA — often amplified, because operating costs are largely fixed in the short term. Academic research confirms that upstream firms are "more sensitive to changes in oil prices (i.e., more risky) than downstream firms" ([ScienceDirect, volatility transmission study](https://www.sciencedirect.com/science/article/abs/pii/S1059056024001540)).

**Downstream refiners** have a more complex relationship with oil prices. When crude rises:
- Revenue from refined products rises (passed through to consumers with a lag)
- Input costs rise faster if product price response lags
- Net effect depends on the crack spread

When oil prices drop sharply, refiners can see *improved* margins if product prices fall more slowly. This is why refiners sometimes outperform E&Ps during price collapses.

**Midstream operators** (pipelines, storage) are the most insulated. Their revenues are primarily fee-based — take-or-pay contracts tied to throughput volumes, not commodity prices. They function more like infrastructure utilities. Price sensitivity is indirect: a prolonged low-price environment that kills upstream production eventually reduces throughput volumes.

### Refining Margin Logic and the 3-2-1

Refining margins are driven by:
1. **Crude oil input cost** — WTI or Brent basis depending on refinery location and crude slate
2. **Refined product prices** — Gasoline (RBOB) and distillate/ULSD are the primary outputs
3. **Operational complexity** — More complex (cracking/coking) refineries can run cheaper, heavier crude and achieve better yields
4. **Utilization rates** — Higher throughput spreads fixed costs, improving realized margins

The 3-2-1 is a *simplified* benchmark. Real refiners track "margin capture" — the percentage of the 3-2-1 they actually realize as EBITDA. A well-run refinery with 80% margin capture on a $25/bbl 3-2-1 earns $20/bbl in EBITDA, per [IB IQ](https://ibinterviewquestions.com/guides/energy-investment-banking/crack-spreads-refining-margins-3-2-1).

### US Shale Break-Even Prices by Basin

Break-evens come in two forms:
- **Half-cycle (incremental):** The price needed to cover well-level costs on a new well drilled into already-acquired acreage. These are the "keep drilling" break-evens and are lower.
- **Full-cycle:** The price needed to cover all costs including land acquisition, G&A, and infrastructure. These are the "create value" break-evens and are higher.

**Current (2025–2026) basin break-evens for new wells:**

| Basin | New Well Break-Even | Existing Well LOE | Notes |
|-------|---------------------|-------------------|-------|
| **Permian (Delaware)** | ~$61/bbl WTI | ~$33/bbl | Lowest cost, most activity ([Statista, 2026](https://www.statista.com/statistics/748207/breakeven-prices-for-us-oil-producers-by-oilfield/)) |
| **Eagle Ford** | ~$55–65/bbl | ~$30/bbl | Texas, good pipeline access |
| **Bakken** | ~$58/bbl | ~$38/bbl | Rising 4% YoY per [LinkedIn analysis](https://www.linkedin.com/posts/leen-weijers-49a69b51_oil-gas-oilgas-activity-7427396228935475200-QHsT) |
| **Conventional wells** | ~$30–50/bbl | Low teens | Older vertical wells |

**Full-cycle Permian:** The most productive wells achieve full-cycle costs around $36.40/bbl; the average for 2018–2021-vintage Tight Oil wells was $50.80/bbl, per [Incorrys full-cycle cost study](https://www.incorrys.com/videos/NorthAmericanOilandGasFulCycleCost-Aug2021.pdf). These costs have risen since then with inflation and service cost increases.

**OPEC comparison:** Saudi Arabia's lifting costs are ~$2–4/bbl; full fiscal break-even (government budget balance) is ~$70–80/bbl.

---

## 1.2 Industry Structure

### Upstream / Midstream / Downstream

**Upstream** (Exploration & Production): Finds, drills, and produces crude oil and natural gas from the ground. Revenue is price-sensitive; capital-intensive; exploration adds reserves; production converts reserves to cash. Includes E&P companies, national oil companies (NOCs), and integrated majors' E&P divisions.

**Midstream**: Transports, stores, and processes crude oil, natural gas, and NGLs. Uses pipelines, tankers, rail, and truck. Includes gas processing plants and fractionation facilities. Revenue typically fee-based via long-term take-or-pay contracts. Companies include Williams Companies, Enterprise Products, Kinder Morgan, MPLX.

**Downstream**: Refines crude into finished products (gasoline, diesel, jet fuel, petrochemicals), markets, and sells. Revenue tied to crack spreads and product demand. Companies include Valero, Marathon Petroleum, Phillips 66, HollyFrontier, per [AFPM's industry overview](https://www.afpm.org/newsroom/infographic/infographic-downstream-midstream-and-upstream).

### Integrated Majors vs. Independents

**Supermajors (Integrated):**
| Company | Headquarters | 2026 Market Cap |
|---------|-------------|----------------|
| ExxonMobil (XOM) | Houston, TX | ~$640B |
| Chevron (CVX) | Houston, TX | ~$394B |
| Shell (SHEL) | London/Netherlands | ~$200B+ |
| BP | London | ~$100B+ |
| TotalEnergies | Paris | ~$150B+ |

Data: [Blackridge Research, March 2026](https://www.blackridgeresearch.com/blog/list-of-largest-major-top-oil-and-gas-companies-in-united-states-of-america-usa). Integrated majors operate across all three segments, providing natural hedges (downstream benefits when upstream is hit). Their strategy emphasizes balance sheet strength, dividends, and energy transition positioning.

**Top Independent E&Ps (US, by 2025 production):**
1. ExxonMobil (upstream): 1.95 MMboe/d
2. Expand Energy (formerly Chesapeake Energy): 1.75 MMboe/d
3. ConocoPhillips: 1.42 MMboe/d
4. Devon Energy (post-Coterra merger): ~1.6 MMboe/d (now largest independent Lower 48)
5. EOG Resources, Diamondback Energy, Pioneer (now part of ExxonMobil)

Per [Marcellus Drilling News / Enverus 2026 ranking](https://marcellusdrilling.com/2026/01/top-50-public-ep-operators-of-2025-ranked-by-og-production/).

**Strategy divergence:** Independents like Diamondback, EOG, Devon now return >68% of FCF to shareholders via buybacks and dividends — up from 35% in 2019. Supermajors maintain both capital returns and energy transition spending. [Wood Mackenzie (Feb 2026)](https://www.woodmac.com/blogs/energy-pulse/the-us-oil-industry-is-consolidating-as-growth-slows/) documents the Devon-Coterra $58B merger as representative of the "scale and stable cash flows" paradigm driving consolidation.

### Oilfield Services Companies

The "Big Three" OFS companies:

| Company | 2025 Revenue | Key Business | Trend |
|---------|-------------|--------------|-------|
| **SLB** (Schlumberger) | Declining 1.6% full-year | Digital, subsurface, production | Digital ARR >$1B first time; dividend raised 3.5% |
| **Baker Hughes (BKR)** | $27.73B (+) | Industrial & Energy Tech; LNG equipment | Record $32.4B backlog; diversifying into power systems |
| **Halliburton (HAL)** | Down 3.24% full-year | Completions-heavy, North America-focused | Operating income fell 39.82%; most cyclical |

Data: [24/7 Wall Street analysis, March 2026](https://247wallst.com/investing/2026/03/18/one-of-these-oil-services-stocks-is-pulling-away-from-the-pack-baker-hughes-haliburton-slb/).

OFS revenue is a lagging function of upstream capex. When E&P companies increase drilling budgets (capex cycle turns up), OFS revenues follow 6–12 months later. Baker Hughes's strategic pivot toward non-cyclical industrial energy technology (power systems, data centers, gas infrastructure) is notable as a hedge against upstream cyclicality.

### Reserve Replacement

**Reserve Replacement Ratio (RRR)** = New reserves added / Reserves produced. A ratio above 100% means the company is growing its reserves base; below 100% means depletion is outpacing discovery.

**Reserve Life Index (RLI)** = Proved reserves / Annual production. Measures how many years of current production remain without new investment.

- **Healthy RLI:** >10–15 years considered acceptable; >15 years signals a strong position
- **Global oil and gas average:** ~12 years (IHS Markit, per [KPI Depot](https://kpidepot.com/kpi/reserve-life-index))
- **Interpretation nuance:** As [Energy Income Partners notes](https://eipinvestments.com/eva-pao-february-4-2023/), RLI can be misleading — the most economic reserves are drilled first, and a "low" RLI may simply mean a company is prioritizing high-return, fast-payback inventory rather than booking marginal reserves

**Who's struggling:** Companies in mature basins without active exploration programs. The industry trend toward capital discipline means less exploratory drilling, which pressures reserve replacement across the sector.

### Production Growth vs. Capital Discipline

Post-2020, US shale shifted fundamentally from "growth at all costs" to free cash flow maximization. Key data points:
- Cumulative FCF was approximately **-$300B from 2010–2020** as operators subsidized growth
- In 2022 alone, FCF reached **+$210B** — a structural reversal, per [LinkedIn pressure pumper analysis](https://www.linkedin.com/posts/leen-weijers-49a69b51_oil-gas-oilgas-activity-7427396228935475200-QHsT)
- Top 20 independents now return **68% of FCF** to shareholders vs. 35% in 2019

[OilPrice.com via Rystad Energy (Jan 2025)](https://oilprice.com/Energy/Crude-Oil/Shale-40s-Capital-Discipline-Outweighs-Trump-20s-Pro-Growth-Rhetoric.html) calls this "Shale 4.0" — a period where capital discipline and inventory quality gate decisions, not price optimism.

### Capex Cycles

Current capex phase: **Recovery cycle with discipline constraints.** The capital intensity cycle turned up after COVID and continues trending higher, but operators are deploying cash into shareholder returns and debt reduction rather than aggressive rig additions. 2026 capex guidance across the industry is "flat to modestly higher" with low-single-digit production growth expected ([Energy News Beat, March 2026](https://energynewsbeat.co/us-rig-count-up-for-a-second-week/)). The rig count declined ~7% in 2025 and ~5% in 2024, per [Reuters Baker Hughes report, March 2026](https://www.reuters.com/business/energy/us-drillers-cut-oil-gas-rigs-first-time-three-weeks-says-baker-hughes-2026-03-20/).

---

## 1.3 Financial Interpretation Frameworks

### EBITDA vs. EBITDAX in Energy

**EBITDAX** = Earnings Before Interest, Taxes, Depreciation/Depletion, Amortization, and **Exploration Expense**.

The "X" matters because E&P companies use different accounting methods for exploration:
- **Successful efforts method:** Only successful well costs are capitalized; dry hole costs are expensed immediately
- **Full cost method:** All exploration costs are pooled and amortized

This creates non-comparability between companies. EBITDAX removes exploration expense from the calculation, normalizing both accounting methods and enabling apples-to-apples comparison across E&P companies, per [Mercer Capital's explanation](https://mercercapital.com/insights/blogs/energy-valuation-insights-blog/2019/how-to-value-your-ep-company/) and [Investopedia](https://www.investopedia.com/terms/e/ebitdax.asp). Per [Weaver's analysis](https://weaver.com/resources/using-ebitdax-or-ebitda-ep-company-valuation/), EBITDAX is the preferred metric for companies with significant exploration spending; EBITDA is better for mature producers with steady production and minimal exploration.

### Lifting Costs / LOE (Lease Operating Expenses)

Lifting costs are the cash operating costs to produce a barrel of oil equivalent from an existing well. They include:
- Artificial lift (pumping)
- Well maintenance and minor workovers
- Water disposal (especially significant in Eagle Ford)
- Field processing
- Labor

**Typical LOE ranges (2025):**

| Basin | LOE per Boe | Notes |
|-------|-------------|-------|
| Permian Resources (Delaware) | **$5.45/Boe** guidance | 2026 plan per [Permian Resources IR](https://permianres.com/permian-resources-announces-strong-fourth-quarter-2025-results-and-provides-full-year-2026-plan-with-improved-capital-efficiency-and-increased-base-dividend/) |
| Bakken | Higher, ~$9–12/Boe | Artificial lift costs, water disposal |
| Eagle Ford | Moderate, ~$8–11/Boe | Water disposal significant |
| Conventional vertical | Varies widely | Low volumes but low well costs |

**Source:** [EIA Upstream Cost Trends study](https://www.eia.gov/analysis/studies/drilling/pdf/upstream.pdf) provides the baseline methodology; current data from company 10-Ks and quarterly earnings.

**Conventional vs. unconventional:** Conventional wells often have lower per-barrel LOE due to natural reservoir pressure and simpler completions, but lower production rates mean fixed costs dominate at smaller scale.

### Break-Even Analysis: Full-Cycle vs. Half-Cycle

(See Section 1.1 for basin-specific figures.)

**Half-cycle:** Well-level economics assuming acreage already paid for. Permian half-cycle breakevens can be as low as $25–35/bbl for the best Delaware Basin locations.

**Full-cycle:** Includes G&A, land acquisition, exploration, and infrastructure. More relevant for whether a company is creating value. Permian full-cycle averages $50–65/bbl depending on acreage vintage.

**OPEC producers:** Saudi Arabia's lifting cost is ~$2–4/bbl; full fiscal break-even (government budget needed to balance) is ~$70–80/bbl — a critical distinction for understanding Saudi behavior in OPEC+ negotiations.

### Reserve Life Index

See Section 1.2 for definition and benchmarks. Published data sources include:
- **Company 10-K filings** (SEC EDGAR): Annual reserves disclosure required under SEC Subpart 1200
- **IHS Markit / S&P Global Commodity Insights**: Third-party reserves data
- **Wood Mackenzie / Rystad Energy**: Proprietary reserves databases

### Hedging

E&P companies hedge production to protect cash flow and satisfy lender requirements. The three primary instruments:

| Instrument | Mechanism | Upside Capture | Cost |
|-----------|-----------|----------------|------|
| **Fixed-price swap** | Lock in a set price for production | None — full price locked | None |
| **Costless collar** | Buy put (floor) + sell call (ceiling) | Partial — capped at ceiling | None upfront |
| **Put option** | Right to sell at strike price | Full — unlimited above strike | Premium ($3–9/bbl) |

In 2024–2025, producers shifted toward outright puts rather than collars, wanting full upside exposure while protecting the downside, per [IB IQ hedging toolkit](https://ibinterviewquestions.com/guides/energy-investment-banking/hedging-toolkit-swaps-collars-puts).

**Typical hedge ratios:**
- **PE-backed / highly leveraged E&Ps:** 70–90% of PDP production for 12–24 months (lender requirement)
- **Large-cap investment-grade (XOM, CVX, COP):** Minimal or zero — rely on balance sheet strength
- **Mid-cap public E&Ps:** 30–60% of near-term production
- **Post-2020 trend:** Many producers moved to 30–50% modest positions using puts/collars rather than heavy swap programs

As of early 2025, [Evaluate Energy analysis](https://info.evaluateenergy.com/most-north-american-oil-production-left-unhedged-in-early-2025/) found only 19% of Q4 production from 38 tracking companies was hedged for Q2 2025 — meaning over 80% of production was unhedged at historically elevated price levels.

### Leverage and Covenant Risk

Key leverage metrics for oil and gas companies:

| Metric | Definition | Concern Threshold | Note |
|--------|-----------|------------------|------|
| **Net Debt / EBITDA** | Financial leverage | >2.5–3.0x triggers concern in energy | Lenders typically require <3.0–3.5x |
| **Net Debt / EBITDAX** | Oil & gas-specific leverage | >2.5x = caution | Preferred by E&P lenders |
| **Debt / Proved Reserves** | Asset-to-debt | Context-dependent | Used in RBL (Reserve-Based Lending) |
| **Interest Coverage** | EBITDA / Interest Expense | <3.0x signals stress | Tech companies have much wider buffers |

Data: [Damodaran's 2026 Debt Update via LinkedIn](https://www.linkedin.com/pulse/data-update-7-2026-debt-default-taxes-aswath-damodaran-jk9gc) confirms that across sectors, real estate and utilities have the tightest debt buffers; energy sits in the middle. Reserve-Based Lending (RBL) facilities common in oil & gas have semi-annual redeterminations tied to proved reserves value — these "borrowing base" redeterminations are the key covenant risk event for smaller E&Ps.

### Inventory and Working Capital

The **EIA Weekly Petroleum Status Report** (published every Wednesday at 10:30 AM ET) is the most market-moving weekly data release in oil. It reports:
- US crude oil inventories at Cushing, Oklahoma (the WTI delivery point)
- US total petroleum inventories
- Refinery utilization rates
- Import/export volumes
- Gasoline and distillate stocks

**Cushing, Oklahoma** is critical because it is the physical delivery point for NYMEX WTI futures contracts. When Cushing storage fills, WTI prices face downward pressure (the April 2020 negative price event was a Cushing-driven storage overflow). When Cushing draws down rapidly, it signals strong demand or reduced supply and is typically bullish.

URL: [EIA Weekly Petroleum Status Report](https://www.eia.gov/petroleum/supply/weekly/)

---

## 1.4 Regulatory Entity Map

### FERC (Federal Energy Regulatory Commission)

**What they regulate:** Interstate natural gas pipelines (rates, terms of service, construction), LNG export and import facility siting under Section 3 of the Natural Gas Act, electricity markets and transmission.

**Actions that matter to investors:**
- Approving or denying LNG export terminal permits — a multi-year process that gates US LNG export capacity expansion
- Setting pipeline tariff rates — affects midstream company revenues
- Environmental review (NEPA impact statements) for new LNG facilities

Currently regulates 27 operational LNG facilities and has active proceedings for new terminals, per [FERC's LNG page](https://www.ferc.gov/natural-gas/lng).

**Where to find filings:** [FERC eLibrary](https://elibrary.ferc.gov) — general search allows queries by docket number, company name, document type. All FERC orders, tariff filings, and environmental documents are publicly accessible.

### EPA (Environmental Protection Agency)

**What they regulate:** Methane emissions (NSPS OOOOa/OOOOb rules), air quality, water disposal from drilling (produced water), Clean Air Act permitting for new facilities.

**Actions that matter to investors:** Methane regulation directly increases E&P operating costs. EPA's evolving rules on produced water disposal (injection wells, reuse) affect Permian economics. Carbon pricing proposals could affect long-term asset values.

**Where to find filings:** [EPA.gov/oil-natural-gas](https://www.epa.gov/oil-natural-gas)

### BSEE (Bureau of Safety and Environmental Enforcement)

**What they regulate:** Offshore oil and gas safety — drilling permits, production safety systems, equipment inspections for offshore platforms on the Outer Continental Shelf.

**Actions that matter to investors:** Can halt offshore drilling (permit moratoria), enforce safety shutdowns after incidents, issue new rules that increase offshore operating costs.

**Website:** [BSEE.gov](https://www.bsee.gov)

### BOEM (Bureau of Ocean Energy Management)

**What they regulate:** Offshore oil and gas leasing — who can drill, where, when. Manages the 5-year OCS Leasing Program.

**Actions that matter to investors:** Lease sale schedules determine future offshore E&P activity. The **OBBBA (One Big Beautiful Bill Act, 2025)** mandated 36 offshore lease sales through 2040, accelerating the program dramatically. BOEM is now executing this schedule: BBG1 (Gulf of America, Dec 2025), BBC1 (Cook Inlet, March 2026), BBG2 (March 2026), per [BOEM Lease Sales page](https://www.boem.gov/oil-gas-energy/lease-sales) and [Harvard EELP tracker](https://eelp.law.harvard.edu/tracker/offshore-oil-and-gas-drilling-leasing-program/).

**Website:** [BOEM.gov](https://www.boem.gov)

### DOE (Department of Energy)

**What they regulate:** Strategic Petroleum Reserve (SPR) management, LNG export authorization (the DOE issues licenses allowing LNG facilities to export to non-FTA countries — a separate approval from FERC's construction permits), nuclear and energy R&D policy.

**Actions that matter to investors:** SPR releases directly inject supply into the market (as in 2022). LNG export authorizations (required for new projects exporting to non-FTA nations) are a policy decision that has been used as a geopolitical lever. Biden's 2024 LNG export pause was a DOE action; Trump reversed it in 2025.

**Website:** [Energy.gov](https://www.energy.gov)

### SEC — Oil & Gas Reserve Reporting

The SEC's **Modernization of Oil and Gas Reporting** rules (effective January 1, 2010) — [SEC.gov](https://www.sec.gov/rules-regulations/2008/12/modernization-oil-gas-reporting) — govern how public companies disclose reserves in 10-K filings:

Key rules:
- **12-month average pricing:** Companies must use the average of first-day-of-month prices for the trailing 12 months to calculate proved reserves (not current spot price), improving comparability
- **Proved reserves definition:** Expanded to include unconventional resources (shale, oil sands)
- **Probable and possible reserves:** Companies may (but are not required to) disclose 2P and 3P reserves
- **Third-party qualified engineers:** Required for reserve reports

**Where to find filings:** [SEC EDGAR](https://www.sec.gov/cgi-bin/browse-edgar) — search for oil & gas companies' 10-K filings; reserves are disclosed under Subpart 1200 of Regulation S-K (Items 1201-1208).

### State-Level Regulators

**Texas Railroad Commission (RRC):**
The primary regulator for the world's most productive onshore oil region. Despite the name, it has not regulated railroads since that function moved to TxDOT. Functions:
- Issues drilling permits for all Texas oil and gas wells
- Collects production and well completion reports (P5 forms)
- Regulates well plugging and remediation
- Regulates pipeline safety and natural gas utilities
- Sets spacing and density rules

The RRC's production data (public records) is a key input for Permian Basin supply analysis. Investors track RRC permit filings as a leading indicator of future drilling activity, per [RRC Oil & Gas Division](https://www.rrc.texas.gov/oil-and-gas/).

**NDIC (North Dakota Industrial Commission):**
Regulates Bakken oil production in North Dakota. Similar permit tracking, well spacing (1280-acre spacing units), and production reporting functions. Key for monitoring Bakken activity.

**New Mexico OCD (Oil Conservation Division):**
Regulates the New Mexico Permian (Delaware Basin) — increasingly important as Delaware Basin production rivals or exceeds the Midland. Issues permits, monitors production, manages environmental compliance.

### OPEC and OPEC+

**OPEC** (Organization of Petroleum Exporting Countries): 12 member nations including Saudi Arabia, Iraq, UAE, Kuwait, Iran, Nigeria, and others. OPEC controls roughly 40% of global oil production.

**OPEC+**: Expanded group of 22 countries adding Russia, Kazakhstan, Azerbaijan, and others. Together, OPEC+ accounts for approximately half of global supply (~53 million b/d of ~106 million b/d total global demand), per [Reuters, December 2025](https://www.reuters.com/markets/commodities/energy/opec-spark-spending-race-with-new-oil-quota-system-2025-12-02/).

**How quotas work:**
- OPEC ministers meet periodically (monthly JMMC + full ministerial ~twice yearly) to set production targets
- Each member gets a national quota; the JMMC monitors compliance
- Quotas are regularly exceeded by chronic overproducers (Iraq, Kazakhstan, UAE in recent periods)
- Overproducers agree to "compensation cuts" to make up past excess — they rarely fully deliver
- **Current compliance picture:** In March 2025, OPEC+ producers with quotas pumped **319,000 b/d above target** (vs. 294,000 b/d overproduction in February 2025), per [S&P Global Platts survey](https://www.spglobal.com/energy/en/news-research/latest-news/crude-oil/041025-opec-nudges-up-crude-output-amid-mounting-volatility-poor-compliance)

**Key swing producer:** Saudi Arabia — can adjust production rapidly by hundreds of thousands of barrels per day. In February 2026, Saudi Arabia increased production by 340,000–782,000 b/d despite formal OPEC+ freeze agreements, in response to Hormuz crisis, per [Discovery Alert analysis](https://discoveryalert.com.au/strategic-production-decisions-opec-market-2026/).

**New MSC mechanism (November 2025):** OPEC+ approved a framework to assess each member's Maximum Sustainable Capacity (MSC) from January–September 2026, using a US auditing firm for 19 of 22 members. Results will set 2027 production baselines. This is expected to reward UAE and Saudi Arabia (high capacity, low costs) while disadvantaging African members with declining capacity, per [OilPrice.com](https://oilprice.com/Energy/Energy-General/OPEC-Keeps-Oil-Output-Steady-and-Approves-Historic-Capacity-Mechanicsm.html).

---

## 1.5 Key Publications & Data Sources

### EIA (Energy Information Administration)

The authoritative US government source for energy data. Tier 1 source.

| Report | Frequency | Content | URL |
|--------|-----------|---------|-----|
| **Weekly Petroleum Status Report** | Weekly (Wed, 10:30 AM ET) | Crude/product inventories, Cushing levels, refinery utilization | [eia.gov/petroleum/supply/weekly](https://www.eia.gov/petroleum/supply/weekly/) |
| **Short-Term Energy Outlook (STEO)** | Monthly | Near-term price forecasts, supply/demand balance, production outlook | [eia.gov/outlooks/steo](https://www.eia.gov/outlooks/steo/) |
| **Annual Energy Outlook (AEO)** | Annual | Long-term US energy forecasts to 2050 | [eia.gov/outlooks/aeo](https://www.eia.gov/outlooks/aeo/) |
| **EIA Open Data API** | Real-time | Programmatic access to all EIA datasets — crude prices, inventories, production | [eia.gov/opendata](https://www.eia.gov/opendata/) |

The EIA API is **free and unlimited** — the best free source for WTI/Brent prices, Henry Hub spot prices, and inventory data.

### IEA (International Energy Agency)

Intergovernmental organization advising developed economies (OECD members). Tier 1 source.

- **Oil Market Report (OMR):** Published monthly, covers global supply, demand, stocks, prices, and trade flows. Available to IEA member governments; full version requires subscription. Key highlights released free monthly. The March 12, 2026 OMR PDF is available at [iea.blob.core.windows.net](https://iea.blob.core.windows.net/assets/a25ddf53-cd6c-4910-ac90-16bfd28399e7/-12MAR2026_OilMarketReport.pdf).
- **Oil 2025 (Annual Medium-Term Report):** 5-year supply/demand analysis released annually, [IEA PDF](https://iea.blob.core.windows.net/assets/c0087308-f434-4284-b5bb-bfaf745c81c3/Oil2025.pdf)
- **World Energy Outlook (WEO):** Annual long-term scenarios (STEPS, APS, NZE). Released each November. The WEO 2025 introduced revised demand peak timelines — see Section 1.6.

### S&P Global Platts / Commodity Insights

Dominant pricing reference agency (PRA) for oil and gas. Tier 1 for physical market pricing. Publishes:
- Dated Brent (the main North Sea benchmark)
- RBOB gasoline spot prices
- ULSD/heating oil
- Natural gas (Henry Hub, regional hubs)
- LNG JKM (Japan Korea Marker)
- The Platts OPEC+ Survey — the industry-standard monthly OPEC production tracking survey

Per [Steel Eye analysis](https://www.steel-eye.com/news/the-price-keepers-the-world-of-commodity-benchmarks-part-one), Platts is "the historical titan and undisputed market leader, especially in global oil markets." Saudi Arabia's 2009 switch from Platts WTI-based pricing to Argus ASCI is noted as a landmark in benchmark evolution.

### Argus Media

Platts' primary global competitor. Founded 1970. Key differentiation:
- **First PRA to apply IOSCO Principles** for oil price reporting — enhancing transparency credibility
- **Russian Urals crude:** Argus is the main publisher of Russian crude prices
- **US Gulf Coast oil grades:** Argus is primary for many physical US crude benchmarks
- Saudi Arabia switched its US crude pricing reference to Argus's ASCI index in 2009
- Argus is generally considered more price-competitive than Platts for subscriptions

Per [Guttman Energy](https://www.guttmanenergy.com/fueling-energy-solutions/understanding-fuel-indices/) and [Reddit Commodities discussion](https://www.reddit.com/r/Commodities/comments/1f84ar7/why_do_the_big_dogs_use_argus_or_platts/): Argus excels at daily window pricing assessments for physical crude and power markets.

### Oil & Gas Journal

Trade publication covering drilling, production, refining, petrochemicals, and policy. Read primarily by engineers and operations professionals rather than investors. Useful for technical developments, equipment advances, and basin-level operational data. Tier 2 source.

### Baker Hughes Rig Count

**Published:** Every Friday at 1:00 PM ET (Baker Hughes North American rig count).

**What it measures:** Active operating drilling rigs, separated by oil vs. gas, horizontal vs. vertical, by basin and country. US total rig count is the most-watched weekly activity indicator.

**Why it matters:** Changes in rig count are a leading indicator of future production (with a 6–9 month lag). It is a proxy for industry capex sentiment. Recent data: 592 US rigs as of late March 2026, down from 621 a year ago, per [CME Group / Baker Hughes data](https://www.cmegroup.com/education/events/econoday/627136). Higher rig counts add downward pressure to long-term prices through future supply additions.

**URL:** [Baker Hughes Rig Count](https://rigcount.bakerhughes.com/north-america-rig-count)

### SEC EDGAR

**How to find oil & gas filings:**
- Go to [sec.gov/cgi-bin/browse-edgar](https://www.sec.gov/cgi-bin/browse-edgar)
- Search by company name or ticker, select "Annual Report (10-K)"
- Under 10-K, reserves disclosures are in **Subpart 1200** (Items 1201–1208)
- Key reserve metrics: proved reserves by category, standardized measure of discounted future net cash flows (SMCF), 5-year development program

### Top US E&P Company IR Pages

| Company | IR Page | Key Metrics to Track |
|---------|---------|---------------------|
| ExxonMobil | [investor.exxonmobil.com](https://investor.exxonmobil.com) | Production guidance, capex budget, dividend |
| Chevron | [chevron.com/investors](https://www.chevron.com/investors) | Permian growth, buyback program |
| ConocoPhillips | [conocophillips.com/investors](https://www.conocophillips.com/investors) | Reserve replacement, FCF yield |
| EOG Resources | [investors.eogresources.com](https://investors.eogresources.com) | "Premium" well inventory, LOE |
| Diamondback Energy | [ir.diamondbackenergy.com](https://ir.diamondbackenergy.com) | Permian operations, synergy tracking |
| Devon Energy / new Coterra merger | Watch for combined IR post-merger completion | Scale, dividend framework |
| Permian Resources | [permianres.com](https://permianres.com) | Delaware Basin low-cost operations |

### FERC eLibrary

**URL:** [elibrary.ferc.gov](https://elibrary.ferc.gov)

General search allows queries by docket number, company name, document type (tariff filings, orders, EIS documents). All FERC orders and pipeline/LNG documents are public. Useful for monitoring LNG project approvals, pipeline rate proceedings, and environmental review milestones.

### Bloomberg and Reuters Commodities

**Bloomberg Terminal:** Real-time commodity price streaming, analytical tools (crack spread calculations, forward curve analysis), news, and — as of Q1 2026 — **ASKB** agentic AI (see Section 2.3). Key Bloomberg commodity functions: `CL1 Comdty` (WTI front-month), `CO1 Comdty` (Brent front-month), `NG1 Comdty` (Henry Hub), `CRAK` (crack spread index).

**Reuters/Refinitiv:** Similar real-time commodity feeds. Critical for breaking geopolitical news affecting prices. Available via Thomson Reuters Eikon terminal.

What free sources lack: real-time streaming prices (EIA is delayed), forward curves, proprietary assessments for physical grades.

---

## 1.6 Geopolitical Risk Frameworks

### Strait of Hormuz

The Strait of Hormuz is a 21-mile-wide waterway connecting the Persian Gulf to the Gulf of Oman and Arabian Sea. **As of 2024, approximately 20 million barrels per day (b/d) flowed through it, representing ~20% of global petroleum liquids consumption**, per [EIA analysis](https://www.eia.gov/todayinenergy/detail.php?id=65504). This amounts to ~27% of global seaborne oil trade.

Key exporters through the Strait: Saudi Arabia (38% of Hormuz crude flows, 5.5 million b/d), UAE, Iraq, Kuwait, Iran. Approximately **84% of Hormuz crude flows to Asian markets** — China, India, Japan, South Korea.

In 2026, an active conflict near the Strait has materially reduced flows and is the primary driver of the current oil price spike. Saudi Arabia is offsetting some flows via its East-West pipeline to Red Sea ports, per EIA analysis.

**Historical escalation examples:**
- **1987–1988 "Tanker War":** US Navy escorted Kuwaiti tankers; prices rose 30%+
- **2019 Iranian tanker attacks:** Prices spiked $5–8/bbl before subsiding
- **2024 Houthi Red Sea attacks:** Diverted shipping from Suez Canal, raising freight costs and product prices without materially cutting crude supply
- **2026 Hormuz actual closure threat:** Brent up ~50% from year-start to March 9

### Sanctions and Export Restrictions

**Iran:** Under US sanctions since 1979 (with gaps). Current status: active Iran conflict generating calls for sanction tightening; IEA member countries released 400 million barrels from emergency reserves on March 11, 2026, per [IEA OMR March 2026](https://iea.blob.core.windows.net/assets/a25ddf53-cd6c-4910-ac90-16bfd28399e7/-12MAR2026_OilMarketReport.pdf). Iran's production (~3.23 million b/d per Platts survey) is exempt from OPEC+ quotas.

**Venezuela:** US eased PDVSA sanctions in March 2026, allowing US companies to buy Venezuelan oil following Venezuela political changes. The Treasury issued a "comprehensive authorization" allowing PDVSA to sell directly to US businesses and internationally, per [AP News, March 18 2026](https://apnews.com/article/trump-iran-war-venezuela-oil-supplies-prices-3a3ca446459b3ab0127c08ad0808cc15). This is a market-supportive move during Hormuz disruption.

**Russia:** Sanctioned post-2022 Ukraine invasion. A "price cap" mechanism ($60/bbl on Russian seaborne crude) was the primary tool. March 2026 developments: US issued 30-day waivers allowing India and then all countries to purchase Russian oil already at sea, as part of supply management during the Iran crisis, per [Steptoe Sanctions Update, March 23 2026](https://www.steptoe.com/en/news-publications/stepwise-risk-outlook/sanctions-update-march-23-2026.html).

### OPEC+ Quota Dynamics

(See Section 1.4 for OPEC+ structure.) The key dynamic for investors: **Quota announcements often diverge from actual production.** The Platts OPEC+ Survey is the industry standard for tracking actual output vs. targets. Chronic overproducers (Iraq, Kazakhstan, UAE in recent cycles) deplete cartel credibility. Saudi Arabia exercises override authority during crises.

**Quota negotiation mechanics:** Ministers meet; Saudi Arabia and Russia signal the outcome in advance via bilateral communications; the formal meeting ratifies or modestly modifies the signal. Major surprises are rare but possible when US-Saudi relations deteriorate or when global recession concerns escalate.

### Shipping Chokepoints

| Chokepoint | Daily Volume | Primary Relevance | Alternative Route |
|-----------|-------------|------------------|------------------|
| **Strait of Hormuz** | 20 million b/d (oil); ~20% global LNG | Most critical for Middle East crude export | Saudi EW pipeline (limited); very few alternatives |
| **Suez Canal** | ~6–8 million b/d (2023) | Egypt-controlled; key for Europe-Asia flows | Cape of Good Hope (~10 day delay, higher cost) |
| **Bab el-Mandeb** | ~4.7 million b/d | Red Sea bottleneck; connecting Suez | Cape route bypass; disrupted by Houthis 2024 |
| **Strait of Malacca** | ~16 million b/d | Key for Asia-Pacific | Lombok Strait (Indonesia); longer |

Hormuz closure would be catastrophically disruptive — there is no adequate bypass for Persian Gulf producers. Suez/Bab el-Mandeb disruptions add cost and delay but can be routed around.

### Geopolitical Shock → Price Transmission

Oil prices typically react within **hours to days** of major geopolitical events, with the initial spike driven by risk premium and uncertainty rather than actual supply changes. The "risk premium" historically runs:
- **Minor escalation (threats, minor incidents):** $2–5/bbl
- **Moderate disruption (partial closure, sanctions escalation):** $5–15/bbl
- **Major disruption (full closure, large sanctioned producer offline):** $20–40+/bbl

The current Hormuz-related crisis has added approximately $30–35/bbl to Brent since early 2026.

### Energy Transition Risk

**IEA World Energy Outlook 2025 (November 2025):** Under the Stated Policies Scenario (STEPS), oil demand is expected to plateau around 2030 at ~102 million b/d before beginning a slow decline, per [IEA via S&P Global Energy](https://www.spglobal.com/energy/en/news-research/latest-news/refined-products/111225-iea-sees-global-oil-demand-rising-until-2050-under-current-policies). Under the Current Policies Scenario (CPS — which reflects current actual policies without new commitments), global oil demand rises to 105 million b/d by 2035 and 113 million b/d by 2050.

**Key shift in WEO 2025 vs. prior years:** The IEA extended its gas demand peak from 2030 to 2035. The fossil fuel peak narrative softened, driven by weak climate action and energy security fears, per [Scientific American](https://www.scientificamerican.com/article/iea-now-predicts-oil-and-gas-demand-to-rise-beyond-2030-departing-from/).

**Rystad Energy's Global Energy Scenarios 2025:** Projects clean energy investment surpassing oil and gas by 2025 — a structural turning point in global energy finance, per [Rystad's flagship report](https://www.rystadenergy.com/flagship-report-energy-scenarios-2025). Data center capex reached $770B in 2025, surpassing upstream oil and gas for the first time.

**For investors:** The "peak oil demand" question is central to long-cycle capex decisions. At current policies, peak demand is ~2030 per IEA STEPS, which means 4 years of growth before a plateau — short enough to make 20-year oilfield investments questionable without high return hurdles.

---

## 1.7 Current Market Context (March 2026)

### Oil Price Environment

As of March 26–30, 2026:
- **Brent:** $100–105/bbl ([Fortune, March 26](https://fortune.com/article/price-of-oil-03-26-2026/))
- **WTI:** ~$94–100/bbl range in March ([Barchart data](https://www.barchart.com/futures/quotes/CLH26))
- **WTI-Brent spread:** Approximately $6–10/bbl (WTI at discount)
- **Context:** Brent is up approximately 40% in one month and ~50% from January 1 to March 9, per [EIA STEO March 2026](https://www.eia.gov/outlooks/steo/)

**One month ago (late February 2026):** Brent was ~$71.49/bbl (per Yahoo Finance March 25 2026 oil price article). The move in the past month — ~$30+/bbl — is one of the largest one-month spikes in decades.

### Major Market-Moving Factors (March 2026)

1. **Strait of Hormuz military conflict:** Active military operations near the Strait have reduced petroleum shipments and shut in some Middle East production. IEA characterized an "effective closure" scenario in its STEO assumptions.
2. **Iran war:** US military action or support for Israel against Iran is cited across multiple sources as the primary geopolitical driver. US eased Venezuela sanctions as a partial supply offset.
3. **Russian sanctions complexity:** US issued 30-day waivers on Russian oil at sea (March 5 and broader March 12), avoiding a simultaneous Russian + Iranian supply shock.
4. **IEA emergency reserves release:** Member countries agreed March 11 to release 400 million barrels of strategic reserves, per IEA OMR.
5. **OPEC+ production freeze overridden:** Saudi Arabia unilaterally increased production by 340,000–782,000 b/d in February despite Q1 2026 freeze commitments, acting as swing producer in the crisis.

### OPEC+ Production Policy

- **Q1 2026:** Formal freeze reaffirmed at each monthly meeting (January, February, March). Eight OPEC+ members have maintained 3.24 million b/d of voluntary cuts representing ~3% of global demand, per [CNBC, November 30 2025](https://www.cnbc.com/2025/11/30/opec-holds-2026-group-wide-oil-output-steady-agrees-capacity-mechanism.html)
- **Saudi swing producer override:** Saudi Arabia informally overriding freeze in response to geopolitical crisis, per [Discovery Alert, March 2026](https://discoveryalert.com.au/strategic-production-decisions-opec-market-2026/)
- **2026 capacity assessments ongoing:** The new MSC mechanism is running from January–September 2026 to set 2027 production baselines

### US Shale Production

- **Current US crude production:** Forecast to average **13.6 million b/d in 2026**, rising to 13.8 million b/d in 2027, per [EIA STEO](https://www.eia.gov/outlooks/steo/)
- **Higher prices enabling activity increase:** WTI in the $95–100+ range is unlocking modest rig additions, but operators are prioritizing balance sheet and returns over volume, per [Energy News Beat, March 2026](https://energynewsbeat.co/us-rig-count-up-for-a-second-week/)
- **Rig count:** 592 US rigs as of late March 2026 (down 29 from 621 a year ago), per [CME/Baker Hughes](https://www.cmegroup.com/education/events/econoday/627136)
- **Consolidation:** Devon Energy-Coterra $58B merger creates the largest Lower 48 independent producer at ~1.6 MMboe/d, per [Wood Mackenzie](https://www.woodmac.com/blogs/energy-pulse/the-us-oil-industry-is-consolidating-as-growth-slows/)

### Analyst Price Forecasts for 2026–2027

| Source | 2026 Brent Forecast | 2027 Brent Forecast | Notes |
|--------|--------------------|--------------------|-------|
| **EIA STEO (March 2026)** | Avg $79/b (revised up 37%) | Avg $64/b | Conflict-dependent; expects prices to fall below $80 in Q3 2026 as Hormuz reopens |
| **S&P Global Ratings (March 16 2026)** | Raised by $15/bbl | — | Reflecting longer-than-expected oil flow disruption |
| **EIA pre-conflict forecast (Feb 2026)** | $58/b | $53/b | Context for how quickly forecasts changed |

Per [EIA STEO](https://www.eia.gov/outlooks/steo/): "This price forecast is highly dependent on our modeled assumptions of both the duration of conflict in the Middle East and resulting outages in oil production."

---

# PART 2: Building AI-Powered Decision Support for Oil Investors

## 2.1 Voice-First AI Assistants — State of the Art

### Professional Voice AI Landscape (2025–2026)

The state of the art for professional voice AI has shifted dramatically. As [the 2026 voice AI comparison guide notes](https://zackproser.com/blog/voice-ai-tools-professionals-comparison-2026), "The key differentiator is no longer speech recognition accuracy — most tools achieve 95%+ accuracy — but rather workflow integration and industry-specific intelligence."

The architecture of a production voice AI system for professional use has four components:

```
[User Voice Input] → [STT Engine] → [LLM Reasoning] → [TTS Engine] → [Voice Output]
       ↕                                    ↕
[VAD / turn-taking]               [Tool calls / live data]
```

### Speech-to-Text (STT) Engines

| Engine | WER | Streaming Latency | Cost/Hour | Best For |
|--------|-----|------------------|-----------|---------|
| **Deepgram Nova-3** | 5.26–6.84% | Sub-300ms | $0.0043 | Real-time production; lowest latency, most cost-effective |
| **OpenAI GPT-4o Transcribe** | <5% | Ultra-low | Moderate | Highest accuracy; deep OpenAI ecosystem integration |
| **AssemblyAI Universal-2** | <6% | ~270ms | $0.0108 | Enterprise features, speaker diarization |
| **Google Cloud STT** | <7% | Low | Variable | 100+ languages; GCP ecosystem |
| **OpenAI Whisper** (self-hosted) | ~10.6% | Not natively streaming | GPU costs | Open source; research; does not support real-time streaming without custom engineering |

Data: [Deepgram vs. Whisper comparison](https://deepgram.com/learn/whisper-vs-deepgram) and [NextLevel STT model comparison](https://nextlevel.ai/best-speech-to-text-models/).

**For a voice-first financial workspace:** Deepgram Nova-3 or OpenAI GPT-4o Transcribe are the production choices. Deepgram's sub-300ms streaming latency and 3× lower cost advantage make it the default for real-time conversational interfaces. Whisper is not suitable for real-time streaming without substantial custom engineering.

### Text-to-Speech (TTS) Engines

| Engine | Voice Quality | Latency | Key Advantage | Notes |
|--------|--------------|---------|---------------|-------|
| **ElevenLabs** | 9.2/10 (highest) | Moderate | Hyper-realistic; voice cloning; emotional control | More expensive; "narrator-like" tone; better for high-fidelity output than real-time conversation |
| **OpenAI TTS** | 8.1/10; led in human preference (42.93%) | Fast (4s/500 words) | Simple integration; no subscription; superior context awareness (63.4% vs 44.7%) | Best integration simplicity; good enough for business applications |
| **Cartesia** | High | Extremely low | Sub-250ms latency; cost-effective | Newer; purpose-built for real-time applications |
| **Google Cloud TTS** | High | Low | 220+ voices; 40+ languages; WaveNet | Complex integration |
| **Amazon Polly** | Good | Low | AWS ecosystem; Neural voices | Older architecture; less natural than newer providers |

Data: [ElevenLabs vs OpenAI TTS comparison](https://amitkoth.com/elevenlabs-vs-openai-tts/), [FahimAI comparison 2025](https://www.fahimai.com/elevenlabs-vs-ttsopenai), [Safina AI TTS comparison](https://safina.ai/en/blog/best-tts-providers-2025/).

**For an executive-quality "chief of staff" voice:** ElevenLabs with a custom professional voice clone delivers the highest quality; OpenAI TTS delivers 90% of the quality at 10% of integration time. Cartesia is the emerging choice for sub-250ms real-time requirements.

### Voice Infrastructure Frameworks

**Vapi:** Turnkey platform for building voice AI agents. Handles call routing, turn-taking (branded as "smart endpointing"), telephony integration, built-in call analysis. Enterprise-grade security for healthcare and financial services. Faster to deploy; optimized for common voice patterns. Per [Vapi.ai](https://vapi.ai).

**LiveKit:** Open-source WebRTC framework. "LEGOs of voice AI" — fully customizable, supports video, end-to-end encrypted streams (critical for proprietary shareholder/investor content), better turn-taking configurability, scales to thousands of participants. Best for complex custom voice AI products. Per [Modal's LiveKit vs. Vapi analysis](https://modal.com/blog/livekit-vs-vapi-article).

**Hume AI (EVI — Empathic Voice Interface):** Voice AI that detects and responds to emotional cues in real-time. Compatible with Claude, GPT, Gemini, Llama. Per [Hume AI EVI page](https://www.hume.ai/empathic-voice-interface). Differentiator: emotional intelligence in the voice interaction — detecting frustration, uncertainty, urgency. For an investor workspace dealing with high-stakes decisions, this is a meaningful capability.

### Existing Voice-First Financial Intelligence Products

**Bloomberg Terminal voice features:** Bloomberg has added AI-driven document analysis and news summarization (ASKB agentic AI, launched February 2026) — but this is primarily text-based AI, not voice-first. No evidence of Bloomberg offering full voice-first conversational interface as of March 2026.

**Gaps in the market:** No evidence of a voice-first, portfolio-aware, geopolitical-context-integrated oil investor workspace exists as a commercial product. The infrastructure exists; the domain application layer does not.

---

## 2.2 Decision-Convergence Systems — Prior Art

### Project State Tracking

The concept of an AI system that maintains **structured state** about a user's project — not just chat history, but blockers, decisions, evidence gaps — maps to several emerging patterns:

**Portfolio management AI with structured state:** MongoDB's multi-agent portfolio management architecture ([MongoDB blog, May 2025](https://www.mongodb.com/company/blog/innovation/reimagining-investment-portfolio-management-with-agentic-ai)) uses three agents (market analysis, market news, market assistant) operating on persistent state stored in MongoDB. The market analysis and news agents run on daily schedules, updating structured state; the market assistant uses this state to answer portfolio manager questions. This is architecturally analogous to a decision-convergence workspace.

**Financial domain knowledge as persistent product:** A key lesson from building financial AI agents ([LinkedIn/WitanLabs, March 2026](https://www.linkedin.com/posts/nuno-f-campos_github-witanlabsresearch-log-how-we-built-activity-7434607728091656193-zhYQ)): "Financial expertise outlived every tool we built. We went through four tool backends. If you're building a domain-specific agent, the domain knowledge is the product; the tools are replaceable."

### Dependency Chain Reasoning

**Agentic AI in financial services:** Moody's analysis ([January 2026](https://www.moodys.com/web/en/us/creditview/blog/agentic-ai-in-financial-services.html)) documents that agentic AI systems in finance are moving "from passive data retrieval to real-time analytical execution," with agents that can "autonomously monitor markets, detect non-obvious correlations, and optimize portfolio allocations." The dependency chain concept (if X is unresolved, Y is blocked) appears in production in M&A advisory contexts where AI pre-screens deals and flags structural risks that block recommendation.

### Proactive Nudging

Bloomberg's **ASKB agentic AI** (launched February 2026) is the closest production example. It operates through "a coordinated network of AI agents that work in parallel to analyze Bloomberg's extensive data and content universe," per [Bloomberg's announcement](https://www.bloomberg.com/company/stories/meet-askb-bloomberg-introduces-agentic-ai-to-the-bloomberg-terminal/). ASKB supports **ASKB Workflows** — reusable templates for multi-step research tasks — but proactive nudging (pushing alerts to users about stale decisions) is not documented.

CFA Institute documentation ([CFA Institute Research Center](https://rpc.cfainstitute.org/research/the-automation-ahead-content-series/agentic-ai-for-finance)) notes that agentic AI for portfolio construction can use "dynamic assessments" rather than "rigid filters" — but the shift from reactive to proactive remains an open research frontier.

### Decision Boards / Convergence Tracking

No commercial products explicitly implement "decision state tracking" (explore → converge → commit) as a first-class concept. The closest analogs are:
- **Linear / Jira** (software project management): Track issue states with dependency blocking
- **Notion AI** (knowledge management): Project context persistence but not decision-state formalized
- **Hebbia** (financial AI): Document synthesis for investment research — but state tracking is informal

**Gap:** The exact pattern described — maintaining a structured `project_state.yaml` with blockers, evidence gaps, open decisions, and proactive surfacing when time-sensitive items emerge — has no direct commercial equivalent in oil/energy or any vertical as of March 2026. This is the design space being occupied.

### Agentic Workflows in Finance

**Governance requirement for agentic finance AI** ([Moody's](https://www.moodys.com/web/en/us/creditview/blog/agentic-ai-in-financial-services.html)): "Effective governance demands robust data curation, structured decision-tracking, and human-in-the-loop oversight." This is a design requirement, not optional — especially for a professional investor workspace where decisions have financial consequence.

**Production examples:**
- **Walmart/JP Morgan:** Already deploying AI agents in production as infrastructure ([Nate's Newsletter, October 2025](https://natesnewsletter.substack.com/p/executive-briefing-your-2025-ai-agent))
- **FinRobot (academic):** Multi-agent architecture for portfolio optimization and risk analysis
- **Moody's Research Assistant:** Users consuming 60% more research while cutting task completion times by 30%; >90% of interactions focused on high-value analytics

---

## 2.3 AI in Oil & Gas — Current Landscape

### AI for Oil & Gas Investment (Not Operations)

Most AI in oil & gas is operational (reservoir modeling, predictive maintenance, drilling optimization). The investment intelligence layer is less developed.

**Key platforms for oil investors:**

**Enverus Intelligence Research (EIR):** The most oil-industry-specific investment intelligence platform. Per [Enverus AI launch, December 2025](https://www.enverus.com/newsroom/enverus-ai-powering-the-next-era-of-energy-intelligence/):
- "Trained on petabytes of Enverus' data, decades of lease terms, production data, invoices and grid behavior"
- Embedded in workflows of 8,000+ companies
- Capabilities: acquisition target identification, benchmarking drilling performance vs. operators, summarizing investor priorities from earnings calls, extracting lease clauses
- Launched an "Ask Enverus AI Anything" interface in December 2025
- Used by DG Petro Oil & Gas for decision-making, M&A screening
- Most relevant existing platform for a professional oil investor

**Rystad Energy:** Global independent energy intelligence firm. Provides proprietary supply/demand models, project-level production forecasts, M&A analysis, and scenarios. Used by IOCs, hedge funds, and governments. Key AI application: analyzing how "national oil companies can turn data into strategic insight," per [Rystad article](https://www.rystadenergy.com/insights/harnessing-the-power-of-ai-how-national-oil-companies-can-turn-data-into-strategi). AI enhances subsurface modeling, production decline analysis, and capital efficiency benchmarking. Tier 2 source.

**Kensho Technologies (S&P Global):** AI innovation hub for S&P Global. Primarily NLP and event-driven analysis — detecting geopolitical events' impact on commodity prices, earnings sentiment, M&A probability signals. Per [Kensho.com](https://kensho.com). Tools are embedded in S&P Global's products; not directly accessible as standalone investor tool.

**Orbital Insight (now Privateer):** Uses satellite imagery and computer vision to track oil storage levels globally — measuring floating-roof tank fill levels from space. Institutional intelligence product used by hedge funds for physical supply analysis. Per [Business Insider coverage](https://www.businessinsider.com/gv-backed-orbital-insights-images-from-space-track-oil-storage-2020-4). Key application: getting early read on OPEC compliance (comparing reported vs. satellite-observed storage changes).

### Bloomberg AI for Commodity Analysis

**ASKB (launched February 2026):** Agentic AI directly on the Bloomberg Terminal. Per [Bloomberg press release](https://www.bloomberg.com/company/stories/meet-askb-bloomberg-introduces-agentic-ai-to-the-bloomberg-terminal/):
- Conversational AI with access to Bloomberg's full content universe (hundreds of millions of company documents, news, analytics)
- Multi-agent system: agents work in parallel to retrieve, interpret, and synthesize
- Generates BQL code for extended Excel/BQuant analysis
- ASKB Workflows: reusable templates for standardized research tasks
- AI Summary for Company News and AI-Powered News Summaries also launched November 2025

**Document Search & Analysis (DSX):** Launched mid-2025, allows users to query across earnings transcripts, CIMs, and custom documents. Per [Bloomberg Pro Tips](https://www.bloomberg.com/professional/insights/markets/bloomberg-pro-tips-use-ai-to-analyze-a-company-against-its-peers/).

Bloomberg does not have a voice-first interface for this as of March 2026.

### AI for Energy Investors Specifically

- **Enverus:** Closest to a full investment intelligence platform for oil
- **Wood Mackenzie:** Deep asset-level data, M&A analytics; some AI-enhanced interfaces
- **No voice-first startup building for oil investors** found in research as of March 2026

**Hedge fund AI for oil trading:** Evidence is limited to general AI trading research. The most sophisticated commodity trading firms (Citadel, Millennium, DE Shaw) use proprietary quantitative models incorporating satellite data (via Orbital Insight/Privateer), sentiment analysis, and ML price forecasting — not documented publicly.

---

## 2.4 Workspace Configuration Patterns

### Multi-Tenant AI Workspace Configuration

Enterprise AI tools use several patterns for scoping AI behavior per workspace:

**System prompt + knowledge pack:** The primary pattern. A static system prompt containing domain knowledge, behavioral rules, and user context is injected at the start of each session. This is how Anthropic's Claude system prompts work, how ChatGPT's "Custom Instructions" work, and how Perplexity's Spaces function. Per [GitHub awesome-ai-system-prompts](https://github.com/dontriskit/awesome-ai-system-prompts): domain-specific knowledge is embedded in system prompts to "constrain agent behavior, provide domain-specific knowledge, and establish operational boundaries."

**RAG (Retrieval-Augmented Generation):** Static knowledge that is too large for a system prompt is stored in a vector database and retrieved dynamically at inference time. [RTInsights](https://www.rtinsights.com/ai-isnt-static-why-are-we-still-feeding-it-yesterdays-data/) describes the three-layer architecture: large context windows (breadth) + prompt caching (efficiency) + RAG (freshness).

**Knowledge graph architecture:** For enterprise-scale context with complex entity relationships, tools like Atlan use knowledge graphs to "structure how entities connect across business domains" — e.g., linking risk assessment processes, customer workflows, and investigation protocols. Per [Atlan enterprise context layer guide, February 2026](https://atlan.com/know/how-to-implement-enterprise-context-layer-for-ai/).

### Static Reference Knowledge vs. Live Volatile Data

**The core design split for a financial AI workspace:**

| Category | Examples | Update Frequency | Source Pattern |
|----------|---------|-----------------|----------------|
| **Static reference** | "What is EBITDAX?" / "What does FERC regulate?" / "How does the 3-2-1 crack spread work?" | Annual or event-driven | System prompt / static knowledge pack |
| **Slow-changing context** | Company positions, portfolio composition, active decisions | Weekly to monthly | Structured state file (e.g., `project_state.yaml`) |
| **Volatile market data** | WTI/Brent current price, inventory data, rig count | Real-time to daily | Live API calls (EIA, Bloomberg, price APIs) |
| **Event-triggered data** | FERC orders, OPEC announcements, earnings releases | Irregular | News monitoring API + webhook |

Per [Question Base data freshness analysis](https://www.questionbase.com/resources/blog/data-freshness-next-generation-enterprise-ai): "Stale data costs businesses up to 30% of data value annually." Domain-specific freshness thresholds matter — financial trading data needs millisecond updates; a "what is the current Permian break-even" static knowledge item needs annual updates.

The critical design principle: the workspace needs to know what it knows vs. what it needs to look up. Static domain knowledge should never be real-time fetched; live prices should never be answered from cached training data.

### Workspace Onboarding Patterns

Fast onboarding of AI to a specific user's context follows a known pattern from tools like Glean, Moveworks, and Notion AI:

1. **Structured intake questionnaire:** The system asks about the user's portfolio, positions, investment thesis, key decisions in progress, and primary data sources
2. **Document ingestion:** Existing investment memos, thesis documents, and portfolio summaries are processed into the knowledge base
3. **Entity registration:** Key companies, basins, counterparties, and regulatory proceedings are registered as tracked entities
4. **Decision state initialization:** Active decisions and their current evidence state are seeded into the project state

The "chief of staff" model: the workspace starts with whatever context the investor provides and progressively learns more through each interaction, updating the state file after each session.

---

## 2.5 Evidence Packs and Artifact Generation

### AI-Generated Executive Briefs in Financial Services

**Production patterns:**
- **Bloomberg's AI News Summaries (November 2025):** AI-enhanced tools for "AI Summary for Company News" and "AI-Powered News Summaries" help investors process 5,000 Bloomberg stories/day + 1.5M external stories, per [Bloomberg press release](https://www.bloomberg.com/company/press/investors-harness-bloombergs-expanded-ai-tools-to-discover-and-summarize-news/)
- **Morgan Stanley AI @ Work, Goldman Sachs GS AI:** Both firms have deployed internal AI assistants for research summarization, with tight citation requirements
- **V7 Go (financial AI):** Citation-based document analysis where every data point includes page number, paragraph, and exact source text — essential for audit trails, per [V7 Labs analysis](https://www.v7labs.com/blog/best-ai-tools-for-investment-banking)

**Morning brief automation:** No public production example of fully automated, portfolio-specific oil investor morning briefs was found. The Yardeni Research morning briefing model (human-authored, data-driven) represents the content target; the automation layer is the build opportunity.

### AI-Generated Artifacts with Citations

**Best practices documented:**
- **Perplexity:** Citations as first-class outputs — every claim linked to source. Real-time web access means citations are live URLs, not training data references
- **Elicit / Consensus:** Academic paper search with citations; structured evidence tables
- **V7 Go:** Citation engine that links extracted data to exact source page/paragraph

**Template-driven generation:** Enterprise AI tools recommend providing structured templates as part of the generation prompt. For a "daily market brief" template, the system prompt would include the desired sections (price summary, notable events, portfolio impact, open questions) and the LLM fills in current data from retrieved sources.

### Structured Decision Documents

**Recommendation note / scenario memo patterns:**
Tools like Hebbia (financial AI for PE and hedge funds) are designed to generate structured investment research documents from uploaded data. The AI synthesizes multiple documents into a structured output following a provided template. Evidence from [Bloomberg ASKB](https://www.bloomberg.com/company/stories/meet-askb-bloomberg-introduces-agentic-ai-to-the-bloomberg-terminal/): ASKB supports reusable "ASKB Workflows" — standardized templates for multi-step research tasks.

**Gap:** No tool generates documents that also track the *decision state* of the investor (which scenarios have been analyzed, what evidence is still missing, what the pending decision is). The artifact generation and the decision tracking are separate concerns in current tools.

---

## 2.6 Live Data Integration Patterns

### Real-Time Commodity Price APIs

| API | Oil/Gas Coverage | Latency | Cost Tier | Notes |
|-----|-----------------|---------|-----------|-------|
| **EIA Open Data API** | WTI/Brent spot, Henry Hub, inventories | Daily (free) | **Free** | Best free source; [eia.gov/opendata](https://www.eia.gov/opendata/) |
| **OilPriceAPI** | 100+ commodities; WTI, Brent, NGLs | Real-time | $9/mo entry | 7-day free trial with 10,000 requests |
| **Nasdaq Data Link (Quandl)** | Wide commodity coverage, historical depth | Daily to real-time depending on dataset | Institutional tiers | [data.nasdaq.com](https://data.nasdaq.com/publishers/QDL) |
| **Polygon.io** | Stocks, options, forex, crypto; **futures in beta** | Real-time (WebSocket) | Developer-tier from $29/mo | Note: Rebranding to Massive; commodity futures not fully available yet as of Nov 2025 |
| **Alpha Vantage** | Commodity futures (WTI, Brent, natural gas) | Daily (free), intraday (paid) | Free tier available | Limited real-time capability |
| **Bloomberg API** | Full real-time commodity universe | Real-time | Terminal subscription ($2,000+/mo) | Definitive professional feed |

Per [Best Oil Price APIs 2025 comparison](https://www.oilpriceapi.com/blog/best-oil-price-apis-2025): "The EIA API is the best free option for daily WTI and Brent prices with unlimited requests."

**Recommendation for voice workspace:** EIA API (free, official) for delayed US data; OilPriceAPI for real-time coverage without Bloomberg subscription.

### Regulatory Filing Monitoring

**FERC eLibrary:** Accessible at [elibrary.ferc.gov](https://elibrary.ferc.gov). Searchable by docket number, company, document type. FERC provides an API for submissions: [FERC Submission API guide](https://www.ferc.gov/media/ferc-submission-api-step-step-guide). Automated monitoring requires polling the search API or subscribing to email alerts per docket.

**SEC EDGAR:** The EDGAR full-text search API (`efts.sec.gov`) allows programmatic retrieval of all filings. For oil & gas companies, 10-K annual reports and 8-K material event disclosures are the primary monitoring targets. The [EDGAR full-text search](https://efts.sec.gov/LATEST/search-index?q=%22proved+reserves%22&dateRange=custom&startdt=2026-01-01) supports real-time filing alerts.

### News and Event Monitoring APIs

| API | Coverage | Key Feature | Best For |
|-----|----------|-------------|---------|
| **NewsAPI.org** | 150,000+ global sources | Metadata only (no full text without publisher deals) | General aggregation, alert bots |
| **Finlight** | Finance/geopolitical sources; high-trust | Full article access, real-time WebSocket streaming, sentiment | Financial market monitoring |
| **AYLIEN** | Structured NLP; entity extraction | Topic modeling, event clustering | Macro analysts; structured event analysis |
| **GDELT** | TV news + global media | Instant event detection pipeline | Geopolitical shock monitoring |
| **Event Registry** | 300,000+ sources | Event-based organization | Research, alert systems |

Per [Finlight News APIs comparison](https://finlight.me/blog/news-apis-for-developers-in-2025): For oil/energy investment monitoring, Finlight's focus on "precision over volume, high-trust financial sources, and real-time WebSocket streaming" makes it the best fit for the volatile/event-triggered data layer.

### Data Freshness Architecture

The critical design principle: **AI applications must know when their information is stale and mark it as such.** Per [Question Base analysis](https://www.questionbase.com/resources/blog/data-freshness-next-generation-enterprise-ai):
- Real-time trading: millisecond-level updates required
- Daily market data: EIA Wednesday report cycle
- Regulatory events: event-driven (no fixed schedule)
- Static domain knowledge: annual review

A production architecture for the oil investor workspace uses **domain-specific freshness thresholds** — the system knows that "WTI current price" has a 15-minute freshness TTL, "Permian break-even" has a 6-month TTL, and "what is a crack spread" has a multi-year TTL.

---

# PART 3: Source Quality Classification

## Tier 1 Sources (Official Institutional)

- [EIA Short-Term Energy Outlook](https://www.eia.gov/outlooks/steo/) — official US government energy statistics
- [EIA Weekly Petroleum Status Report](https://www.eia.gov/petroleum/supply/weekly/) — official inventory data
- [EIA Open Data API](https://www.eia.gov/opendata/) — free programmatic access
- [IEA Oil Market Report, March 12 2026](https://iea.blob.core.windows.net/assets/a25ddf53-cd6c-4910-ac90-16bfd28399e7/-12MAR2026_OilMarketReport.pdf) — IEA member governments; global oil balance
- [IEA Oil 2025 Medium-Term Report](https://iea.blob.core.windows.net/assets/c0087308-f434-4284-b5bb-bfaf745c81c3/Oil2025.pdf) — 5-year supply/demand analysis
- [SEC Modernization of Oil & Gas Reporting](https://www.sec.gov/rules-regulations/2008/12/modernization-oil-gas-reporting) — SEC final rule, reserve reporting standards
- [FERC LNG regulation page](https://www.ferc.gov/natural-gas/lng) — official FERC LNG authority documentation
- [FERC eLibrary](https://elibrary.ferc.gov) — official filings database
- [BOEM Lease Sales](https://www.boem.gov/oil-gas-energy/lease-sales) — official offshore lease schedule
- [Texas Railroad Commission Oil & Gas Division](https://www.rrc.texas.gov/oil-and-gas/) — Texas production regulation
- [Bloomberg ASKB announcement](https://www.bloomberg.com/company/stories/meet-askb-bloomberg-introduces-agentic-ai-to-the-bloomberg-terminal/) — Bloomberg official product announcement
- [Enverus AI announcement](https://www.enverus.com/newsroom/enverus-ai-powering-the-next-era-of-energy-intelligence/) — Enverus official announcement

## Tier 2 Sources (Established Industry Publications and Research)

- [S&P Global Platts OPEC+ Survey](https://www.spglobal.com/energy/en/news-research/latest-news/crude-oil/041025-opec-nudges-up-crude-output-amid-mounting-volatility-poor-compliance) — the industry-standard OPEC production tracking
- [Wood Mackenzie blog](https://www.woodmac.com/blogs/energy-pulse/the-us-oil-industry-is-consolidating-as-growth-slows/) — established energy intelligence firm
- [Rystad Energy insights](https://www.rystadenergy.com) — global independent energy intelligence
- [Deloitte 2026 Oil & Gas Industry Outlook](https://www.deloitte.com/us/en/insights/industry/oil-and-gas/oil-and-gas-industry-outlook.html) — Big 4 annual industry analysis
- [IB Interview Questions Energy guides](https://ibinterviewquestions.com/guides/energy-investment-banking/crack-spreads-refining-margins-3-2-1) — practitioner-grade financial frameworks
- [Evaluate Energy hedging data](https://info.evaluateenergy.com/most-north-american-oil-production-left-unhedged-in-early-2025/) — company-level hedging analytics
- [Mercer Capital EBITDAX article](https://mercercapital.com/insights/blogs/energy-valuation-insights-blog/2019/how-to-value-your-ep-company/) — valuation firm
- [Incorrys full-cycle cost study](https://www.incorrys.com/videos/NorthAmericanOilandGasFulCycleCost-Aug2021.pdf) — upstream cost analysis
- [Deepgram vs. Whisper comparison](https://deepgram.com/learn/whisper-vs-deepgram) — vendor but with primary benchmark data
- [Capital Economics LNG/Henry Hub forecast](https://www.capitaleconomics.com/publications/commodities-update/higher-lng-demand-drive-henry-hub-prices) — established macro research firm
- [Moody's agentic AI in financial services](https://www.moodys.com/web/en/us/creditview/blog/agentic-ai-in-financial-services.html) — Moody's published analysis
- [CFA Institute agentic AI for finance](https://rpc.cfainstitute.org/research/the-automation-ahead-content-series/agentic-ai-for-finance) — CFA Institute Research and Policy Center

## Tier 3 Sources (Industry Practitioners, Well-Regarded)

- [OilPrice.com / Rystad Energy analysis](https://oilprice.com/Energy/Crude-Oil/Shale-40s-Capital-Discipline-Outweighs-Trump-20s-Pro-Growth-Rhetoric.html) — OilPrice.com citing Rystad; Rystad is Tier 2 but OilPrice.com is Tier 3
- [Energy News Beat rig count and capex analysis](https://energynewsbeat.co/us-rig-count-up-for-a-second-week/) — trade publication
- [RBN Energy market commentary](https://rbnenergy.com) — well-regarded natural gas/liquids analysis
- [LiveKit vs. Vapi framework comparison](https://modal.com/blog/livekit-vs-vapi-article) — Modal vendor blog but with technical specificity
- [Hume AI EVI page](https://www.hume.ai/empathic-voice-interface) — vendor product documentation

## Source Gaps Noted

1. **Bakken current break-even specific figures:** Most recent basin-level break-even data is from 2025 Dallas Fed surveys (paywalled) and LinkedIn practitioner analysis; no direct Tier 1 publication.
2. **Current OPEC+ compliance by member (March 2026):** The S&P Global Platts survey is behind a subscription; snippets via search results.
3. **IEA Oil Market Report full text:** The March 2026 OMR is available as a PDF but the subscription version contains fuller data tables.
4. **Hedge fund AI for commodity trading specifics:** Proprietary information; no public sources describe actual production systems at Citadel, Millennium, etc.
5. **NDIC and New Mexico OCD investor-specific resources:** Less documented than Texas RRC; basic regulatory pages available but not investor-focused analysis.

---

# PART 4: Application Mapping

## Immediate Applications for the Workspace Build

### Static Knowledge Library (~30–50 entries)

High-priority entries based on this research:
1. WTI vs. Brent: definition, spread mechanics, current benchmark
2. Henry Hub: definition, historic range, LNG disconnect
3. 3-2-1 crack spread: formula, interpretation, current reading
4. EBITDAX vs. EBITDA: definition, when to use each
5. LOE / lifting costs: typical ranges by basin
6. Break-even prices: half-cycle vs. full-cycle by basin
7. Reserve Life Index: calculation, healthy range
8. Hedging instruments: swaps, collars, puts — mechanics and use cases
9. Net Debt/EBITDA: leverage thresholds for energy
10. Upstream/midstream/downstream: segmentation and price sensitivity
11. OFS companies: Big Three, revenue-capex cycle relationship
12. Capital discipline / Shale 4.0: post-2020 paradigm shift
13. Strait of Hormuz: volumes, historical disruption patterns, current status
14. OPEC+ quotas: how they work, compliance picture, Saudi swing role
15. EIA weekly report: what it contains, why Wednesday matters
16. Cushing, Oklahoma: role, when storage levels are bullish/bearish
17. FERC: what it regulates, where filings live
18. BOEM/BSEE: offshore leasing vs. safety regulation
19. SEC reserve reporting: 12-month average pricing rule, Subpart 1200
20. Texas RRC: functions, why permit filings matter to investors
21. Supermajors vs. independents: top companies, strategy differences
22. IEA STEPS vs. CPS scenarios: peak oil demand implications
23. Reserve-Based Lending (RBL): how borrowing bases work, redetermination risk
24. Proved vs. probable vs. possible reserves: 1P/2P/3P definitions
25. Royalties and working interests: basic upstream ownership structure

### `project_state.yaml` Template for Oil Investor

```yaml
investor_profile:
  name: ""
  investment_style: ""  # e.g., "long-only equity, energy sector focus"
  time_horizon: ""  # e.g., "6-18 months"
  
portfolio:
  positions: []  # [{company, ticker, position_size, avg_cost, thesis_one_liner}]
  watchlist: []  # [{company, reason}]
  geographic_exposure:
    permian_pct: null
    international_pct: null
    midstream_pct: null

market_context:
  as_of_date: null
  wti_price: null
  brent_price: null
  henry_hub: null
  crack_spread_321: null
  cushing_inventory_mmbbl: null
  opec_plus_status: ""  # e.g., "Q1 2026 freeze; Saudi swing production active"
  
known_facts:
  - fact: ""
    confidence: null  # 1-5
    source: ""
    date_verified: null

open_decisions:
  - id: ""
    question: ""
    status: ""  # explore | converge | commit
    evidence_for: []
    evidence_against: []
    evidence_gaps: []
    deadline: null
    blocked_by: []

blockers:
  - id: ""
    description: ""
    blocks: []  # list of decision IDs
    resolution_path: ""
    
active_regulatory_proceedings:
  - entity: ""  # e.g., "FERC Docket CP25-..."
    type: ""  # LNG approval, pipeline tariff, EPA methane rule
    status: ""
    significance: ""
    next_milestone: null

pending_catalysts:
  - event: ""  # e.g., "EIA Weekly Report Wed March 31"
    expected_date: null
    relevance: ""
    
last_updated: null
```

### Artifact Templates

**1. Daily Market Brief**
```
DAILY MARKET BRIEF — [DATE] [TIME] ET

COMMODITY SNAPSHOT
WTI: $[X]/bbl ([+/-] from yesterday)
Brent: $[X]/bbl ([+/-] from yesterday)
Henry Hub: $[X]/MMBtu
3-2-1 Crack Spread: $[X]/bbl
Cushing Inventory: [X] MMbbl ([direction] vs. 5-yr avg)

OVERNIGHT MOVES & DRIVERS
[Top 2-3 price drivers with source citations]

PORTFOLIO IMPACT
[For each position: exposure to today's moves]

OPEN DECISION STATUS
[Any decisions with new evidence from overnight]

PROACTIVE FLAG
[Time-sensitive items needing attention]
```

**2. Regulatory Alert Brief**
```
REGULATORY ALERT — [AGENCY] — [DATE]

ACTION: [FERC Order / EPA Rule / BOEM Lease Sale / ...]
DOCKET/REFERENCE: [Number]
DATE FILED/EFFECTIVE: [Date]
SOURCE: [URL]

WHAT IT SAYS:
[2-3 sentence plain language summary]

PORTFOLIO RELEVANCE:
[Which positions are affected and how]

INVESTOR IMPLICATION:
[Bullish/Bearish/Neutral with reasoning]

EVIDENCE QUALITY: [Tier 1/2/3]
```

**3. Scenario Memo**
```
SCENARIO MEMO — [TITLE] — [DATE]

TRIGGER: [What prompted this scenario analysis]

SCENARIO: [Name]
Base case probability: [%]
Bull case probability: [%]  
Bear case probability: [%]

BASE CASE ASSUMPTIONS:
- [Price deck]
- [OPEC+ behavior]
- [US production trajectory]

PORTFOLIO IMPACT BY SCENARIO:
[Table: Position | Bull | Base | Bear | Net position]

KEY VARIABLES TO WATCH:
[2-3 specific data points that would move scenarios]

DECISION IMPLICATION:
[Which open decisions does this inform?]
```

**4. Board/LP Update**
```
[QUARTER/PERIOD] ENERGY PORTFOLIO UPDATE

PERIOD PERFORMANCE: [Return vs. benchmark]

MARKET CONTEXT:
[100-word synthesis of the pricing environment during the period]

PORTFOLIO POSITIONING:
[Key changes made, thesis status for major positions]

RISK SUMMARY:
[Top 3 risks: geopolitical, regulatory, commodity price]

FORWARD LOOK:
[Key catalysts and timeline for the next quarter]

DATA SOURCES: [Cite EIA, IEA, Bloomberg, company filings as appropriate]
```

### Live Retrieval Configuration

| Data Need | Primary Source | API / Access |
|-----------|---------------|--------------|
| WTI/Brent spot price | EIA | [EIA OpenData API](https://www.eia.gov/opendata/) — free |
| Real-time price (intraday) | OilPriceAPI | $9/mo; 10K requests free trial |
| Henry Hub gas | EIA | EIA OpenData API |
| Weekly inventory data | EIA | Wednesday 10:30 AM ET release; EIA API |
| Baker Hughes rig count | Baker Hughes | Weekly; CSV download from rigcount.bakerhughes.com |
| FERC pipeline/LNG filings | FERC eLibrary | [elibrary.ferc.gov](https://elibrary.ferc.gov) — public |
| BOEM lease sale schedule | BOEM | [boem.gov/oil-gas-energy/lease-sales](https://www.boem.gov/oil-gas-energy/lease-sales) |
| SEC 10-K reserves data | EDGAR | EDGAR full-text search API |
| Oil & gas news monitoring | Finlight or NewsAPI | Real-time WebSocket streaming |
| OPEC statements | OPEC.org | RSS feed / web monitoring |

### Voice Interaction Design

**Wake sequence / proactive morning brief:**
> "Good morning. Brent is at $101.40 — down $4.45 overnight as Hormuz tensions eased slightly following the Saudi production statement. Your Permian Resources position is net positive given lower crude input costs improving their LOE picture. There are two items flagged: the EIA inventory report comes out Wednesday at 10:30 Eastern, and a FERC order on the Mountain Valley Pipeline extension was issued yesterday — that's relevant to your Williams Companies position. Want the brief on either, or the full daily summary?"

**Design principles for the voice output:**
1. **Lead with delta from yesterday** — not what everything is, but what changed
2. **Portfolio-specific relevance first** — price news is noise unless it affects the investor's positions
3. **Cite the source in speech** — "according to EIA" or "per S&P Global's survey" maintains credibility
4. **Offer action, not just information** — every brief ends with a choice or a call to action
5. **Confidence-qualified claims** — distinguish between "the rig count fell 7% year-over-year" (fact) and "analysts expect prices to ease by Q3" (forecast)

