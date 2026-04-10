# Perplexity Research Prompt — Oil/Energy Investor Workspace

**Purpose**: Comprehensive research to inform building a voice-first decision-convergence workspace for an oil/energy investor. This prompt covers two domains: (1) the oil/energy industry itself, and (2) the product design patterns for building AI-powered decision support tools in this vertical.

**Output format**: Cited findings with source URLs. Every factual claim must have a source. Organize findings by section.

---

## PART 1: Oil & Energy Industry — Domain Knowledge

### 1.1 Commodity Frameworks

Research the following and provide cited explanations:

- **WTI vs Brent crude**: What are they, where do they trade, why does the spread between them matter for investment decisions? What is the current spread range and what has it been historically (5-year range)?
- **Natural gas pricing**: Henry Hub benchmark, LNG export pricing, the disconnect between US gas and global LNG prices. How does natural gas pricing relate to oil (gas-to-oil ratio)?
- **Crack spreads**: What are they, why do refiners watch them, and how do they signal downstream margin health?
- **Upstream vs downstream price sensitivity**: How do oil price movements affect upstream producers differently from downstream refiners and midstream operators?
- **Refining margin logic**: What drives refining margins? What is the 3-2-1 crack spread and why is it the standard benchmark?
- **Key price thresholds**: At what price levels do US shale producers become uneconomic? What are the break-even ranges for major basins (Permian, Eagle Ford, Bakken)?

### 1.2 Industry Structure

Research and provide cited explanations of:

- **Upstream / midstream / downstream** segmentation: What does each segment do, who are the major players in each, and how do their business models differ?
- **Integrated majors vs independents**: Who are the top 5 integrated majors (supermajors)? Who are the top 5-10 independent E&P companies? How do their strategies differ (cash return vs growth)?
- **Oilfield service companies**: Who are the top OFS companies (Schlumberger/SLB, Halliburton, Baker Hughes)? How does their revenue correlate with upstream capex cycles?
- **Reserve replacement**: What is reserve replacement ratio, why does it matter, and which companies are struggling with it?
- **Production growth vs cash discipline**: How has the US shale industry shifted from "growth at all costs" to "capital discipline" post-2020? What are the current shareholder return policies of major producers?
- **Capex cycles**: What is the current capex cycle phase for oil & gas? Are companies investing more or less than pre-COVID levels?

### 1.3 Financial Interpretation Frameworks

Research these oil/energy-specific financial concepts with cited sources:

- **EBITDA vs cash flow in energy**: Why is EBITDAX used in energy? What does the "X" (exploration expense) capture that standard EBITDA misses?
- **Lifting costs / LOE**: What are typical lifting costs per barrel for major basins? How do they compare across conventional vs unconventional?
- **Break-even analysis**: What are the full-cycle vs half-cycle break-even prices for major US shale plays? How do these differ from OPEC producers?
- **Reserve life index**: What is it, what is considered healthy, and who publishes this data?
- **Hedging**: How do E&P companies hedge production? What are the common instruments (swaps, collars, puts)? What percentage of production is typically hedged 1-2 years out?
- **Leverage and covenant risk**: What are the key leverage metrics for energy companies (Net Debt/EBITDA, Debt/Proved Reserves)? What covenant levels trigger concern?
- **Inventory and working capital**: How does crude oil inventory data (EIA weekly report) affect prices? What is the significance of Cushing, Oklahoma storage levels?

### 1.4 Regulatory Entity Map

For each regulatory body, research and cite:
- What they regulate
- What kinds of actions they take that matter to investors
- Where to find their filings/actions online

**Entities**:
- **FERC** (Federal Energy Regulatory Commission) — pipeline tariffs, LNG export/import, interstate natural gas
- **EPA** (Environmental Protection Agency) — emissions rules, methane regulations, water disposal
- **BSEE** (Bureau of Safety and Environmental Enforcement) — offshore safety, drilling regulations
- **BOEM** (Bureau of Ocean Energy Management) — offshore lease sales, exploration permits
- **DOE** (Department of Energy) — Strategic Petroleum Reserve, export licenses, energy policy
- **SEC** — oil & gas reserve reporting rules (SEC modernization of oil and gas reporting)
- **State-level regulators**: Texas Railroad Commission, North Dakota NDIC, New Mexico OCD — what do they control?
- **OPEC / OPEC+** — as policy actors: how do quota decisions work, who are the key members, what is the current compliance picture?

### 1.5 Key Publications & Data Sources

Research and cite the primary information sources an oil investor uses daily:

- **EIA (Energy Information Administration)**: What reports do they publish (Weekly Petroleum Status Report, Short-Term Energy Outlook, Annual Energy Outlook)? URLs for each.
- **IEA (International Energy Agency)**: Oil Market Report — what does it cover, how often, who subscribes?
- **Oil & Gas Journal**: What kind of content, who reads it?
- **S&P Global Platts / Commodity Insights**: What pricing benchmarks do they publish?
- **Argus Media**: What do they cover that Platts doesn't?
- **Baker Hughes Rig Count**: What is it, when is it published, why does it matter?
- **SEC EDGAR**: How to find oil & gas company filings, 10-K reserve disclosures
- **Company investor relations**: What are the key IR pages for the top 10 US E&P companies?
- **FERC eLibrary**: How to search for pipeline/LNG filings
- **Reuters / Bloomberg commodities**: What real-time data do they provide that free sources don't?

### 1.6 Geopolitical Risk Frameworks

Research with cited sources:

- **Strait of Hormuz**: What percentage of global oil flows through it? What happens to prices during escalation events? Historical examples.
- **Sanctions and export restrictions**: How do US sanctions on Iran, Venezuela, Russia affect global supply? What is the current sanctions picture?
- **OPEC+ quota dynamics**: How do quota negotiations work? What happens when members cheat on quotas? Who are the key swing producers?
- **Shipping and logistics chokepoints**: Strait of Hormuz, Suez Canal, Bab el-Mandeb, Strait of Malacca — which matter most for oil and why?
- **Geopolitical shock → price transmission**: How quickly do geopolitical events transmit to oil prices? What is the typical "risk premium" range in $/barrel?
- **Energy transition risk**: How is the shift to renewables affecting long-term oil demand forecasts? What are the IEA's scenarios? What is "peak oil demand" and when is it projected?

### 1.7 Current Market Context (as of March 2026)

- What is the current oil price environment (WTI, Brent)?
- What are the major market-moving factors right now?
- What is the current OPEC+ production policy?
- What are the major regulatory developments in the US affecting oil & gas?
- What is the state of US shale production growth?
- What are analysts forecasting for oil prices in 2026-2027?

---

## PART 2: Building AI-Powered Decision Support for Oil Investors

### 2.1 Voice-First AI Assistants — State of the Art

Research with cited sources:

- What are the current best practices for building **voice-first AI interfaces** for professional/executive users? Not consumer assistants (Alexa/Siri) — professional decision support tools.
- What voice-to-text engines are being used in production for professional applications in 2025-2026? (Whisper, Deepgram, AssemblyAI, Google Speech-to-Text) — latency, accuracy, cost comparisons.
- What text-to-speech engines produce natural executive-quality output? (ElevenLabs, OpenAI TTS, Google Cloud TTS, Amazon Polly)
- Are there any existing **voice-first financial intelligence** products? Bloomberg Terminal voice features? Any startup building voice-first for investors?
- What is the current state of **real-time voice AI** (conversational, not command-based)? Products like Hume AI, Vapi, LiveKit — are any being used for financial applications?

### 2.2 Decision-Convergence Systems — Prior Art

Research whether anyone has built systems with these properties, and cite sources:

- **Project state tracking**: AI systems that maintain persistent state about a user's project/portfolio and use it to inform future interactions (not just chat history, but structured state — blockers, decisions, evidence gaps)
- **Dependency chain reasoning**: Systems that reason about "if X is unresolved, then Y is blocked, which means Z can't proceed" — any implementations in financial/investment contexts?
- **Proactive nudging**: AI systems that proactively surface stale issues or time-sensitive items rather than waiting for the user to ask — any examples in portfolio management or investment research?
- **Decision boards / convergence tracking**: Tools that track decision state (explore → converge → commit) rather than just task completion — any implementations?
- **Agentic workflows in finance**: How are multi-agent AI systems being used in financial services? Any examples of agent orchestration for investment research, portfolio monitoring, or risk management?

### 2.3 AI in Oil & Gas — Current Landscape

Research with cited sources:

- What AI/ML tools are currently being used in oil & gas **investment** (not just operations/drilling)?
- Are there any AI-powered **oil & gas research assistants** or **commodity intelligence platforms**?
- How are firms like **Kensho (S&P Global)**, **Orbital Insight**, **Rystad Energy**, **Enverus** using AI for oil/gas intelligence?
- What are **Bloomberg's AI features** for commodity analysis?
- Any startups building AI specifically for **energy investors** (not operators/drillers)?
- How are **hedge funds and commodity traders** using AI for oil/gas trading decisions?

### 2.4 Workspace Configuration Patterns

Research with cited sources:

- How do enterprise AI tools handle **multi-tenant workspace configuration**? (Notion AI, Glean, Moveworks, Guru — how do they scope AI behavior per workspace/team?)
- What are best practices for **domain-specific knowledge packs** in AI systems? How do companies like Anthropic, OpenAI, Cohere recommend structuring domain knowledge for AI applications?
- How do **financial AI tools** handle the split between **static reference knowledge** (what is EBITDA, what does FERC regulate) vs **live volatile data** (today's oil price, latest OPEC decision)?
- What are the patterns for **workspace onboarding** in AI tools — how does the system get smart about a specific user's context quickly?

### 2.5 Evidence Packs and Artifact Generation

Research with cited sources:

- How are AI systems being used to generate **executive briefs** in financial services? Any examples of automated morning briefs, board updates, or LP reports?
- What are the best practices for **AI-generated artifacts with citations**? How do tools like Perplexity, Elicit, Consensus handle source attribution in generated content?
- Are there any tools that generate **structured decision documents** (not just summaries) — things like recommendation notes, scenario memos, regulatory alert briefs?
- How do AI writing tools handle **template-driven generation** for professional finance contexts?

### 2.6 Live Data Integration Patterns

Research with cited sources:

- What APIs are available for **real-time commodity price data**? (EIA API, Quandl/Nasdaq Data Link, Alpha Vantage, Polygon.io, Tradier) — pricing, latency, coverage.
- How do AI applications integrate **regulatory filing data** (FERC eLibrary, SEC EDGAR) into automated monitoring?
- What are the options for **news/event monitoring APIs** for oil & gas? (NewsAPI, GDELT, Aylien, Event Registry)
- How do existing financial AI tools handle **data freshness** — knowing when their information is stale and needs to be refreshed?

---

## PART 3: Source Quality Requirements

For every finding, classify the source:

- **Tier 1**: Official documentation from major institutions (EIA, IEA, SEC, FERC, OPEC, major oil companies, major tech companies like Anthropic/OpenAI/Google)
- **Tier 2**: Peer-reviewed research, NIST, EU publications, established industry publications (Oil & Gas Journal, Platts, Argus, Wood Mackenzie, Rystad)
- **Tier 3**: Well-established industry blogs, GitHub repos with >500 stars, recognized practitioners

Prioritize Tier 1 and Tier 2 sources. Flag any claims that rely only on Tier 3 sources.

---

## PART 4: What This Research Will Be Used For

This research will directly inform building:

1. **A static knowledge library** (~30-50 entries) covering oil/energy domain concepts that an investor workspace needs to interpret signals, generate briefs, and support decisions
2. **A project_state.yaml template** for an oil investor — what known facts, missing evidence, open decisions, and blocked actions look like in this domain
3. **Artifact templates** for: daily market brief, regulatory alert brief, scenario memo, board/LP update, recommendation note
4. **Live retrieval configuration** — which APIs and data sources to wire up for volatile data
5. **Voice-first interaction design** — how the workspace greets the user, what proactive nudges look like ("Oil dropped 4% overnight — your Permian exposure is X — want a scenario memo?"), and how executive-quality voice output should sound

The goal is not a full trading platform. It is a system where an oil investor can say "how are we doing" and get back a dependency-aware, evidence-cited, temporally-aware brief that knows their portfolio, their blockers, and their decision state — delivered in a voice that sounds like a trusted chief of staff, not a chatbot.

---

## Formatting Instructions

- Use markdown headers matching the section structure above
- Every factual claim gets a `[Source: title — URL]` citation inline
- At the end, provide a consolidated source list grouped by tier
- For each section, note any significant gaps where reliable sources could not be found
- If sources conflict, present both sides with citations
