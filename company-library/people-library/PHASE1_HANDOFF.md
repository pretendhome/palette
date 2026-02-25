# Phase 1 Handoff — People Library Enrichment
**Date**: 2026-02-24
**Status**: IN PROGRESS — 13/18 profiles enriched, watch list pending
**Next action**: Write `people_library_v1.1.yaml` + complete 5 missing profiles + evaluate watch list

---

## Project Context

This is the **Palette Intelligence System (PIS)** — a market intelligence and service routing layer for Palette, an agentic AI system with a long-term goal of disrupting SageMaker ("one interface that routes any task to the cheapest/best service").

**Key files you need to know:**
- Source library: `/home/mical/fde/palette/company-library/people-library/v1.0/people_library_v1.0.yaml`
- Output target: `/home/mical/fde/palette/company-library/people-library/v1.1/people_library_v1.1.yaml` *(create this)*
- Architecture doc: `/home/mical/fde/palette/company-library/PALETTE_INTELLIGENCE_SYSTEM_v1.0.md`
- Knowledge library (for reference): `/home/mical/fde/palette/knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`

**The people library** is a signal network — 18 profiles of AI influencers, founders, VCs, and builders. Their tool recommendations feed the company-library → service routing decisions → integration roadmap.

---

## Phase 1 Scope

1. **Enrich all 18 profiles** — update `signal_quality`, add new tool signals, update metrics
2. **Resolve 3 stubs** — PERSON-007 (Filip Mark), PERSON-017 (Pablo Palafox), PERSON-018 (Lazar Jovanovic)
3. **Evaluate watch list** — 10 candidates → promote top 5 as PERSON-019 through PERSON-023
4. **Output**: `people_library_v1.1.yaml` in a new `v1.1/` directory

---

## Enrichment Findings (Completed — Use These Directly)

### CLUSTER: RUBEN HASSID NETWORK

#### PERSON-001: Ruben Hassid
- **Signal quality**: HIGH (confirmed)
- **Status**: Active
- **Role**: Founder, EasyGen + "How to AI" Substack (312K subscribers, #2 Education on Substack)
- **New tools recommended in 2026**:
  - **Claude.ai** — calls it "the single most important AI tool for knowledge work"; dedicated a full newsletter issue to it
  - **Wispr.ai** — uses as keyboard replacement, claims 200+ WPM equivalent
  - **Gamma.app** — replacing PowerPoint for presentations
  - **Grok** — his go-to "all-rounder," currently rates it above ChatGPT
  - ChatGPT — actively telling readers to "kill old ChatGPT habits"
- **Company metrics**:
  - EasyGen: $41,532 MRR within 195 days of launch; 26,000+ weekly users; bootstrapped
  - How to AI newsletter: 312,000+ subscribers; 120M organic LinkedIn reach over 2 years
- **Key activity**: Published "Happy New AI Year" Jan 2026 — declared 2026 "the year to evolve from 2022-2025 AI patterns"
- **Sources**: ruben.substack.com, easygen.io, starterstory.com

#### PERSON-002: Anisha Jain
- **Signal quality**: LOW *(downgrade from HIGH — was unvalidated assumption)*
- **Status**: Active but minimal public footprint
- **Role**: Contributor/educator at "How to AI" (Ruben Hassid's brand), based in London
- **Key finding**: LinkedIn confirmed, affiliation confirmed, but generates zero independently indexed content. The "Claude competitive intelligence technique" query returned no attributable results. Signal is derivative of Ruben's brand.
- **Sources**: linkedin.com/in/theanishajain, websitebuilderexpert.com

#### PERSON-003: Axelle Malek
- **Signal quality**: MEDIUM (confirmed)
- **Status**: Active
- **Role**: AI content creator; Twitter Account Manager at rubenhassid.ai; co-author on "How to Prompt" (how-to-prompt.ai)
- **New tools/signals**:
  - **Kling AI** — multiple LinkedIn posts including "Kling AI is disrupting an entire industry" (strong signal)
  - Suno AI — covered AI music generation
  - AI avatars — content creation guide posted
  - Seedance/Veo comparison — NOT attributable to Axelle specifically (broader coverage)
- **Audience metrics** (self-reported): 12,000+ daily followers; 1.5M daily LinkedIn impressions; 68.2% founders/C-levels
- **Sources**: linkedin.com/in/axellemalek, ruben.substack.com/p/spend

#### PERSON-004: Maria Zhanette Yap
- **Signal quality**: LOW *(downgrade from MEDIUM — was unvalidated)*
- **Status**: Active but minimal footprint
- **Role**: Community Manager at "wait, that's AI?" (AI community/newsletter); affiliated with "How to AI"
- **Key finding**: Posts about AI announcements (Anthropic free courses, Google AI access) but no substantial independent content. No appearance on "top AI creators" lists.
- **Sources**: linkedin.com/in/maria-zhanette-yap, signalhire.com

---

### CLUSTER: VC / INFRASTRUCTURE LENS

#### PERSON-005: Olivia Moore
- **Signal quality**: HIGH (confirmed)
- **Status**: Active — highly prolific
- **Role**: Partner, AI investing team, a16z (Andreessen Horowitz). Twin sister Justine Moore is also a partner on the same team.
- **New tools in her personal AI stack (2025 viral X post)**:
  1. **Comet** (Perplexity's AI browser) — default browser; uses shortcuts for outreach and competitive analysis
  2. **Julius AI** — data analyst, replacing ChatGPT for Excel; notebook feature for templated daily analyses
  3. **Happenstance** — AI people/network search (LinkedIn + Gmail + Twitter); investor sourcing
  4. **Granola** — AI meeting notes; runs without a visible bot
  5. **Gamma** — AI slide decks; "AI handles first 80%, human skill is editing and directing"
  6. **Willow** — AI voice dictation
  7. **Superhuman** — AI email
  8. **Overlap** (YC S24) — AI clip editing for video highlights
  9. **Krea** (krea.ai) — AI creative tool (also Creandum-backed — overlap with Filip Mark's portfolio)
- **Key publications**:
  - "State of Consumer AI 2025: Product Hits, Misses, and What's Next" (co-authored with Justine Moore)
  - a16z "Big Ideas 2026": prediction — 2026 is the year AI voice agents gain enterprise foothold; "prompt box dies" for mainstream users
  - Top 100 Gen AI Consumer Apps 5th Edition (Aug 2025): ChatGPT #1, Lovable #23, Cursor #26
- **Sources**: a16z.com/author/olivia-moore, homescreen.news/p/olivia-moore-s-ai-stack, cognitiverevolution.ai

#### PERSON-006: Guillermo Rauch
- **Signal quality**: HIGH (confirmed)
- **Status**: Active — CNBC interview Feb 5, 2026; speaking at HumanX 2026 (April)
- **Role**: Co-Founder & CEO, Vercel
- **Tools/products**:
  - **v0** (Vercel's own) — primary workflow tool; used to ship production code via Git integration
  - **Vercel AI Gateway** — unified API for 100+ models: OpenAI, Anthropic, Google, Meta, xAI, Mistral, DeepSeek, Amazon Bedrock, Cohere, Perplexity, Alibaba; includes smart routing, fallbacks, image/video generation (Grok Imagine, Veo, Kling 3.0, Wan), web search, no token markup, BYOK
- **Company metrics**:
  - Valuation: $9.3B (Series F, Sept 2025)
  - Total funding: $863M over 6 rounds
  - ARR: ~$200M mid-2025 (~80% YoY)
  - v0: $42M ARR as of Feb 2025; 3.5M+ unique users; enterprise = 50%+ of v0 revenue
  - AI SDK: 3M downloads/week
  - Key customers: OpenAI, Anthropic, PayPal, Nike, Walmart
- **Key thesis**: "The world is going from pages to agents" — Vercel building "the AI cloud" for autonomous agents
- **Competitive intelligence flag**: Vercel AI Gateway is a direct competitor to nexos.ai (Creandum portfolio, Filip Mark)
- **Sources**: cnbc.com (Feb 5 2026 interview), vercel.com/ai-gateway, sacra.com/c/vercel, acquired.fm

#### PERSON-007: Filip Mark *(STUB → NOW ENRICHED)*
- **Signal quality**: MEDIUM (confirmed — new hire, limited personal content)
- **Status**: Active — joined Creandum early 2025
- **Role**: Vice President, Investments — Creandum (Stockholm)
- **Background**: Stockholm School of Economics → Bain & Company → EQT Group → Passionfroot (Berlin, operator) → Creandum VP (~early 2025)
- **LinkedIn**: se.linkedin.com/in/filiphmark
- **Twitter/X**: No personal account identified
- **Investment thesis**: Agnostic by sector; drawn to "products that define culture" (cites Spotify, iZettle as archetypes); seed and Series A focus
- **Creandum AI portfolio** (firm-level signal, which Filip operates within):
  1. **Lovable** (Sweden) — AI app builder; Creandum led pre-Series A $15M; now $6.6B valuation
  2. **Black Forest Labs** (Germany) — text-to-image AI; $300M Series B $3.25B valuation; used by Adobe, Meta, Canva
  3. **Complyance** — AI-native enterprise GRC; $20M Series A led by GV (Feb 2026)
  4. **GetVocal** — AI customer support; €24M Series A led by Creandum
  5. **Jack & Jill AI** (UK) — AI recruiting; Creandum-led seed $20M; entering US
  6. **Superscale** (Berlin) — "AI CMO" automated ad generation; $5M pre-seed Creandum; OpenAI/Anthropic angels
  7. **nexos.ai** (Lithuania) — AI gateway routing 200+ LLM endpoints; $8M seed Index + Creandum
  8. **Vesence** — AI agents in Microsoft Office for law firms; 90%+ weekly adoption
  9. **Doinstruct** — AI learning/training; €16.5M Series A
  10. **plancraft** — AI for construction SaaS; €38M round
- **Key crossref**: Krea.ai is in both Olivia Moore's personal AI stack AND Creandum's portfolio
- **Sources**: creandum.com/team/filip-mark, sifted.eu, creandum.com/commitments

---

### CLUSTER: LOVABLE ORBIT

#### PERSON-008: Anton Osika
- **Signal quality**: HIGH (confirmed — one of the best-documented founders in European tech)
- **Status**: Active
- **Role**: CEO and co-founder, Lovable (Stockholm)
- **Company metrics**:
  - ARR: $200M+ (November 2025) — up from $7M end of 2024 (~2,800% YoY)
  - Users: 8 million (November 2025), up from 2.3M July 2025
  - Projects built: 25M+ total; 100,000 new per day
  - Funding: $653M total across 4 rounds; $330M Series B (December 2025)
  - Valuation: $6.6B (December 2025)
  - Backers: CapitalG, Menlo Ventures, Nvidia (NVentures), Salesforce Ventures, Databricks Ventures, DST Global
  - Enterprise: Fortune 500 clients include Klarna, Deutsche Telekom, Uber, Zendesk
- **Key thesis**: "The last piece of software companies ever buy" — expanding toward enterprise infrastructure (databases, payments, hosting)
- **Sources**: techcrunch.com (Nov + Dec 2025), lovable.dev/blog/series-b

#### PERSON-009: Felix Haas
- **Signal quality**: HIGH (confirmed)
- **Status**: Active — published through January 2026
- **Role**: Designer at Lovable; angel investor (14+ startups); founder/author of "Design + AI" Substack (designplusai.com)
- **AI Design Stack 2026** (his article, Dec 16 2025):
  - ChatGPT → concept stress-testing and scoping (starting point)
  - **Lovable** → turning prompts into working products (primary build tool)
  - **Claude** → "desk partner" (cited by his readers for design workflows)
  - Figma → optional polish; he argues it's now "an inhibitor" if used first
- **The Approval Interface** concept: His named design pattern — users review and approve AI-generated outputs rather than constructing actions step by step. Roots in Pinterest-style interaction. Full canonical article exists on his Substack but not directly surfaced — search `designplusai.com` → "approval interface"
- **Recent articles**:
  - "AI Design Stack 2026" (Dec 16, 2025)
  - "How to Build Stunning Slide Decks with AI" (Jan 19, 2026)
  - "The Rise of the Founding Designer" (Nov 2025)
  - "The Golden Age of the Design Founder" (Nov 2025)
- **Audience**: 50,000+ readers across LinkedIn, X, and Substack
- **Sources**: designplusai.com, se.linkedin.com/in/felixhhaas

#### PERSON-010: Oskar Elvhage
- **Signal quality**: MEDIUM (confirmed — but low-traction, flag as early-stage)
- **Status**: Active
- **Role**: Founder & CEO, AgentMaMa.ai (Stockholm); also re-founder of Shopello
- **Company status**: Pre-revenue / early access / pilot phase. First pilot customers in e-commerce (Google Ads focus). Hiring Lead Engineer / future CTO.
- **Channels supported**: Google Ads, Meta, TikTok, LinkedIn, YouTube
- **No personal tool endorsements found** — his product IS the AI tool
- **Sources**: linkedin.com/in/oskar-elvhage, agentmama.ai

#### PERSON-011: Joel Nordström
- **Signal quality**: HIGH (confirmed)
- **Status**: Active — major product launch Feb 2026
- **Role**: CEO and co-founder, Atlar (Stockholm). Co-founded with Joel Wägmark and Johannes Elgh.
- **AI product launch**: AI agents for treasury (Feb 2026) — cash positioning agent, payments briefing agent live; bank reconciliation + forecasting agents announced
- **New customers (2025-2026)**:
  - **Epidemic Sound** (Feb 2026)
  - **Trustly** — global payments company; Atlar centralizes operational bank accounts, payments, cash forecasting, integrated with NetSuite
  - **Tide** — major SME platform; full treasury suite
  - **HSBC Innovation Banking UK** — API integration partnership
  - **Light** — AI-native accounting platform; Atlar bank connectivity embedded
- **Full customer list**: Lovable, Mangopay, Tide, Trustly, Zilch, Epidemic Sound, Aiven, Acne Studios, GetYourGuide, Forto, Juni, Liberis
- **Funding**: €5M seed (Index Ventures lead); later-stage amounts not public
- **Sources**: atlar.com/blog (AI agents announcement, Tide partnership), treasury-management.com

---

### CLUSTER: WISPR FLOW ORBIT — NOT ENRICHED YET

#### PERSON-012: Tanay Kothari — *PENDING (throttled)*
#### PERSON-013: Victoria Liang — *PENDING (throttled)*
*Use v1.0 data as-is. Add `perplexity_enrichment_status: pending` flag.*

---

### CLUSTER: AI CREATIVE TOOLS — NOT ENRICHED YET

#### PERSON-014: Alex Patrascu — *PENDING (throttled)*
#### PERSON-015: Sebastien Jefferies — *PENDING (throttled)*
*Use v1.0 data as-is. Add `perplexity_enrichment_status: pending` flag.*

---

### STANDALONE

#### PERSON-016: Grant Lee — *PENDING (throttled)*
*Use v1.0 data as-is. Add `perplexity_enrichment_status: pending` flag.*

---

### STUBS — RESOLVED

#### PERSON-017: Pablo Palafox → **PROMOTE TO FULL PROFILE**
- **Who**: Co-founder & CEO, HappyRobot (YC S23) — B2B AI voice-agent platform for logistics/freight
- **Why he appeared**: a16z led HappyRobot's Series A AND participated in Series B — Olivia Moore (a16z) is the connection
- **Company metrics**:
  - $15.6M Series A led by a16z (Dec 2024)
  - $44M Series B led by Base10 (Sept 2025, ~$500M valuation)
  - 100,000+ daily AI-driven calls
  - 8 of top 10 freight brokers as customers; 2 of top 3 ocean carriers
  - Eight-figure ARR run rate; revenue 10x between Series A and B
- **Background**: PhD Computer Vision TU Munich; Meta Reality Labs research intern
- **Public presence**: linkedin.com/in/pablorpalafox, x.com/pablorpalafox, podcast appearances (Deepgram AI Minds, Cognitive Revolution-adjacent)
- **Palette relevance**: Enterprise AI voice agents for industrial workflows — "Titanium Economy" thesis (AI transforming real-economy sectors)
- **Signal type**: founder_builder
- **Signal quality**: HIGH
- **Sources**: a16z.com/announcement/investing-in-happyrobot, prnewswire.com, deepgram.com podcast

#### PERSON-018: Lazar Jovanovic → **ARCHIVE**
- **Who**: Most likely the "Professional Vibe Coder" at Lovable; created "50in50 Challenge" (50 AI projects in 50 days); featured on Lenny's Newsletter
- **Why archive**: Signal is derivative of Lovable's brand (Anton Osika already covers this). No founding role, no investment activity, no research output. Name ambiguity (5+ LinkedIn profiles). Lovable signal already covered by PERSON-008 and PERSON-009.
- **What to do**: Do NOT create a full profile. Add a brief `archived_stubs` entry in the YAML with this reasoning.

---

## Watch List — NOT EVALUATED YET (throttled)

The watch list agent hit the credit limit before returning results. These 10 candidates need evaluation:

| Name | Why tracked | Priority query | Notes |
|---|---|---|---|
| Chip Huyen | "Teaches AI through storytelling" (Maria Yap) | "Chip Huyen AI author ML systems 2026" | Likely high signal — ML Systems Design book, Stanford lecturer |
| Tatiana Tsiguleva | "Midjourney tips and prompts" (Maria Yap) | "Tatiana Tsiguleva Midjourney AI creator LinkedIn" | Likely low signal — niche image creator |
| Matthieu Lorrain | "Creative Lead at Google DeepMind" (Maria Yap) | "Matthieu Lorrain Google DeepMind Creative Lead 2026" | High potential — institutional signal |
| Wyndo Mitra Buwana | "Practical no-fluff AI systems" (Maria Yap) | "Wyndo Mitra Buwana LinkedIn AI systems 2026" | Unknown |
| Greg Isenberg | "Internet-first companies, AI businesses" (Maria Yap) | "Greg Isenberg AI internet companies 2026" | Likely medium signal — well-known builder |
| Andrej Karpathy | Coined "vibe coding"; Eureka Labs; 1.4M Twitter | "Andrej Karpathy Eureka Labs 2026 vibe coding" | Very high signal — but may be too famous to be actionable |
| Rory Flynn | "Makes AI fun and accessible" (Maria Yap) | "Rory Flynn LinkedIn AI creator 2026" | Unknown |
| Simon Meyer | "Cinematic AI ads" (Maria Yap) | "Simon Meyer cinematic AI ads LinkedIn creator 2026" | Niche creative signal |
| PJ Accetturo | "Viral AI ads" (Maria Yap) | "PJ Accetturo viral AI ads LinkedIn 2026" | Niche creative signal |
| David Blagojevic | "Hooking video creation" (Maria Yap) | "David Blagojevic AI video hooks LinkedIn 2026" | Niche creative signal |

**For each candidate, evaluate**:
1. Who are they? (role, company, what they do)
2. Are they active in AI in 2025-2026?
3. Do they add signal NOT already covered by existing 18 profiles?
4. Score 1-5 → promote top 5 as PERSON-019 through PERSON-023

**Educated pre-scoring** (do your own research to verify):
- Andrej Karpathy: likely 5/5 but may be too famous — evaluate whether he adds unique signal vs. noise
- Matthieu Lorrain: likely 4/5 — Google DeepMind creative lead is unusual and institutional
- Chip Huyen: likely 4/5 — ML practitioner with real audience and depth
- Greg Isenberg: likely 3/5 — builder signal but overlaps existing profiles
- Rest: run searches and assess

---

## What to Build: `people_library_v1.1.yaml`

Create `/home/mical/fde/palette/company-library/people-library/v1.1/people_library_v1.1.yaml`

**Schema changes from v1.0 → v1.1:**

Add these fields to each profile:

```yaml
perplexity_enrichment_status: complete | pending | not_applicable
enrichment_date: "2026-02-24"
enrichment_notes: "brief summary of what changed"
```

Update these fields where data was found:
- `signal_quality`: change from unvalidated → real rating
- `last_verified`: update to "2026-02-24"
- Add new entries to `notable_recommendations` where new tools were found
- Add or update `company_metrics` where new data was found

**Changes to make per profile**:

| Profile | signal_quality | Key changes |
|---|---|---|
| PERSON-001 Ruben | HIGH (keep) | Add Claude, Grok, Wispr, Gamma to tools; update EasyGen MRR to $41K |
| PERSON-002 Anisha | LOW (downgrade) | Note: minimal independent signal |
| PERSON-003 Axelle | MEDIUM (keep) | Add Kling AI as strong signal |
| PERSON-004 Maria | LOW (downgrade) | Note: community manager, minimal footprint |
| PERSON-005 Olivia | HIGH (keep) | Add full AI stack (Comet, Julius, Happenstance, Granola, Gamma, Willow, Overlap, Krea); add Big Ideas 2026 prediction |
| PERSON-006 Guillermo | HIGH (keep) | Update Vercel metrics ($9.3B, $200M ARR); add AI Gateway model list |
| PERSON-007 Filip | MEDIUM (keep) | Full profile built — add background, Creandum portfolio, nexos.ai/Vercel competitive flag |
| PERSON-008 Anton | HIGH (keep) | Update to $200M ARR, $6.6B valuation, $330M Series B, 8M users |
| PERSON-009 Felix | HIGH (keep) | Add "AI Design Stack 2026" article; Claude as reader-recommended tool |
| PERSON-010 Oskar | MEDIUM (keep) | Add: pre-revenue, pilot phase, AgentMaMa early-stage flag |
| PERSON-011 Joel | HIGH (upgrade from MEDIUM) | Add AI treasury agents launch; Epidemic Sound, Trustly, Tide as customers |
| PERSON-012-016 | unchanged | Add `perplexity_enrichment_status: pending` |
| PERSON-017 Pablo | Build full profile | New entry: HappyRobot CEO, a16z-backed, enterprise AI voice |
| PERSON-018 Lazar | Archive | Move to `archived_stubs` section |
| PERSON-019-023 | Build | Top 5 from watch list (evaluate first) |

**Metadata updates**:
```yaml
version: "1.1"
generated_date: "2026-02-24"
total_profiles: 19+  # 18 existing - 1 archived + Pablo + watch list promotions
enrichment_pass: "2026-02-24 — partial (13/18 complete, 5 pending)"
```

---

## Key Intelligence Flags (Cross-Profile)

These are new signals that should also feed the **company-library** and **service routing**:

1. **Krea.ai**: In both Olivia Moore's personal AI stack AND Creandum's portfolio — double signal, add to company-library
2. **Vercel AI Gateway vs nexos.ai**: Direct competitors — both routing 100+ LLM endpoints. Flag in competitive analysis.
3. **Atlar + Lovable relationship**: Lovable is an Atlar customer — Lovable orbit is tighter than previously mapped
4. **Ruben Hassid → Claude**: His newsletter shift from ChatGPT to Claude is a consumer AI adoption signal
5. **Granola** (AI meetings without visible bot): New tool not in company-library — high practitioner adoption signal (Olivia Moore uses it)
6. **Julius AI**: Data analysis tool recommended by a16z partner — not in company-library
7. **HappyRobot** (Pablo Palafox): Enterprise AI voice agents for logistics — new RIU candidate (voice agent workflows)

---

## Files to Create / Update After v1.1

1. `/home/mical/fde/palette/company-library/people-library/v1.1/README.md` — document what changed
2. Update `/home/mical/fde/palette/company-library/people-library/v1.0/README.md` — note superseded by v1.1
3. Update `/home/mical/.claude/projects/-home-mical/memory/MEMORY.md` — update library path to v1.1
4. (Optional) Update `people_library_company_signals_v1.0.yaml` — add Krea, Granola, Julius AI, HappyRobot

---

## Source YAML Structure Note

The v1.0 YAML file is a **multi-document YAML** (two documents separated by `---`). Parse with `yaml.safe_load_all()` not `yaml.safe_load()`:

```python
import yaml
with open('people_library_v1.0.yaml', 'r') as f:
    docs = list(yaml.safe_load_all(f))
metadata = docs[0]   # has: version, generated_date, total_profiles, clusters_identified
data = docs[1]       # has: profiles[], watch_list{}
```

---

*Handoff document created 2026-02-24. Continue from here.*
