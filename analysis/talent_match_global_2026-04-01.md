# Talent Match — Global Job Search (Crash-Resilient Markets)
> **Skill**: SKILL-TAL-003 (Unified Methodology)
> **Phases Executed**: Phase 0 (Discovery & Classification) + Phase 1 (Fit Assessment)
> **Generated**: 2026-04-01
> **Context**: Market failure probability model (65-75% US crash risk) drove expansion to UK, Australia, Spain, Denmark
> **Source Data**: `role-profiles.yaml`, `experience-inventory.yaml`, `global_job_search_2026-04-01.md`

---

## Phase 0: Discovery & Classification

### Profile Assignment

| # | Company | Role | Location | profile_id | Rationale |
|---|---------|------|----------|-----------|-----------|
| 1 | Anthropic | Solutions Architect, Applied AI | London | `forward_deployed_engineer` | "Solutions Architect" in FDE titles; enterprise LLM architecture |
| 2 | Anthropic | Sydney Office (emerging roles) | Sydney | `enablement_systems_builder` | Ground-floor office; enablement/education roles expected |
| 3 | Cohere | Solutions Architect, Public Sector | London | `forward_deployed_engineer` | SA title + "technical pre-sales/post-sales" + "customer-facing" |
| 4 | Mistral | TME / London Hub | Paris/London | `enablement_systems_builder` | Already in pipeline — ESB profile validated |
| 5 | Databricks | EMEA Hub roles | London | `enablement_strategy` | Databricks already in ES companies_targeted; enablement mandate |
| 6 | Databricks | Sr. Software Engineer | Aarhus | `knowledge_data_engineer` | Code-heavy role, data platform; KDE is closest |
| 7 | Google DeepMind | Applied AI / Engineering | London | `knowledge_data_engineer` | Research/knowledge architecture focus |
| 8 | Datadog | DevRel / Technical Community | Madrid | `enablement_systems_builder` | "Developer Advocate" in ESB titles; community enablement |
| 9 | OpenAI | EU FDE/SA roles | London/Dublin | `customer_success_ai` | OpenAI already in CSAI companies_targeted |
| 10 | Anthropic | AI Engineer | Dublin | `forward_deployed_engineer` | Engineering role, enterprise AI focus |
| 11 | Red Hat AI | AI Consulting / GTM | Spain/EMEA | `enablement_strategy` | "Consulting, enabling, GTM execution" → ES keywords |
| 12 | Hugging Face | DevRel / Community | Remote EU | `enablement_systems_builder` | Community/DevRel → ESB |

### Palette Company Intelligence Cross-Reference

Companies with Palette context advantage (from `people_library_company_signals_v1.1.yaml`):

| Company | Palette Context | Competitive Edge |
|---------|----------------|-----------------|
| **Anthropic** | INTEGRATED — Claude API daily, built Palette ON Claude, 146 tests | "I'm a power user who built a production system on your platform" |
| **Mistral** | TRACKED — Dedicated AWS partner, People Library signal | "I organized enterprise enablement featuring your product" |
| **Google DeepMind** | MONITORED — NotebookLM tracked in signals | Limited edge — research-heavy |
| **OpenAI** | TRACKED — Takehome submitted, recruiter relationship | "Previous screens went perfectly" |
| **Perplexity** | INTEGRATED — Researcher agent uses Sonar API | "Built an agent that routes through your API" |
| **Databricks** | TRACKED — In ES companies_targeted | Standard industry knowledge |
| **Cohere** | NEW — Not previously tracked | No existing context — research needed |
| **Datadog** | NEW — Not tracked | No existing context |

---

## Phase 1: Fit Assessment

### Scoring Key
- Each requirement scored 0-100 against evidence in `experience-inventory.yaml`
- Must-haves weighted 2x, nice-to-haves 1x
- Weighted average → Tier assignment
- **Tier 1 (85-100)**: Full prep | **Tier 2 (75-84)**: Apply, targeted prep | **Tier 3 (65-74)**: Apply if warm lead | **<65**: Pass

---

### 1. Anthropic — Solutions Architect, Applied AI (London)
**Profile**: `forward_deployed_engineer` | **CAPE Hedge**: UK 16.7 (vs US 38.9)

| Requirement | Weight | Score | Evidence |
|-------------|--------|-------|----------|
| Systems architecture | 2x | 92 | ERA-2 POI Graph (25B nodes, 47 providers) + ERA-5 Palette (12 agents, 2,013 quads) |
| Customer delivery | 2x | 88 | ERA-4 Ask Pathfinder (12K sellers/month, 250+ sessions, 25% prep reduction) |
| Technical depth (Python, APIs) | 2x | 90 | ERA-5 Palette (Python, Claude API daily, Go, SQL, MCP protocol, 146 tests) |
| LLM/RAG experience | 1x | 90 | ERA-3 AGI attribution + ERA-5 Palette RAG routing (121 RIUs, 168 KL entries) |
| Startup experience | 1x | 78 | ERA-5 Palette (independent build, open source) — not venture-backed startup |

**Weighted Score**: ((92+88+90)×2 + (90+78)×1) / 8 = **(540+168)/8 = 88.5 → TIER 1**

**Killer Differentiator**: Built a production multi-agent system ON Claude (Palette). No other SA candidate walks in already having architected enterprise solutions on the exact platform they'd be selling.

**Biggest Gap**: No direct B2B SaaS sales motion experience — ERA-4 is enablement, not quota-carrying sales.

**Palette Context**: MAXIMUM — "I don't just understand Claude, I've built 12 agents, 146 tests, and 69 integration recipes on it."

**Market Crash Hedge**: UK CAPE 16.7 vs US 38.9. Anthropic's £225-340K London comp absorbs any cost-of-living premium. If US market corrects, UK Anthropic office is insulated by separate entity economics.

---

### 2. Anthropic — Sydney Office (Ground Floor)
**Profile**: `enablement_systems_builder` | **CAPE Hedge**: Australia 20.2

| Requirement | Weight | Score | Evidence |
|-------------|--------|-------|----------|
| Technical content creation | 2x | 88 | ERA-4 Ask Pathfinder (3-layer architecture, 100+ use cases, 250+ sessions) |
| Developer enablement | 2x | 90 | ERA-4 (12K sellers, 20K users, 140K partner ecosystem) |
| AI product fluency | 2x | 95 | ERA-5 Palette (Claude API daily, Claude Code daily) + ERA-4 Mistral/xAI partnerships |
| Curriculum/assessment design | 1x | 85 | ERA-5 Palette (121 modules, calibration exemplars, 3-layer eval) |
| Open source / community | 1x | 72 | github.com/pretendhome/palette — public but not community-driven |
| Multilingual | 1x | 95 | French (fluent), Italian (fluent), Spanish (proficient) — rare for APAC |

**Weighted Score**: ((88+90+95)×2 + (85+72+95)×1) / 9 = **(546+252)/9 = 88.7 → TIER 1**

**Killer Differentiator**: Ground-floor hire at a brand-new office. Founding team members shape the role. Anthropic already knows you (2 Paris applications). Fluent in 4 languages — rare in APAC, valuable for AU/NZ + broader Asia expansion.

**Biggest Gap**: Roles not yet posted for ESB profile. Current postings are External Affairs (policy) and Startup AE (sales). SA/enablement roles expected but not confirmed.

**Palette Context**: MAXIMUM + timing advantage — apply to London SA, express Sydney interest, leverage internal familiarity.

**Market Crash Hedge**: Australia CAPE 20.2, commodity-backed, Asia-facing. Lowest US contagion of all 4 countries.

---

### 3. Cohere — Solutions Architect, Public Sector (London)
**Profile**: `forward_deployed_engineer` | **CAPE Hedge**: UK 16.7

| Requirement | Weight | Score | Evidence |
|-------------|--------|-------|----------|
| Systems architecture | 2x | 90 | ERA-2 POI Graph + ERA-5 Palette |
| Customer delivery | 2x | 85 | ERA-4 Ask Pathfinder (enterprise-scale delivery) |
| Technical depth (Python, APIs) | 2x | 85 | ERA-5 Palette (Python, API integration) — not Cohere-specific yet |
| LLM/RAG experience | 1x | 85 | ERA-3 + ERA-5 |
| Startup experience | 1x | 78 | ERA-5 Palette |

**Weighted Score**: ((90+85+85)×2 + (85+78)×1) / 8 = **(520+163)/8 = 85.4 → TIER 1**

**Killer Differentiator**: Public sector angle — ERA-1 multilingual knowledge engineering across 4 countries and government-adjacent institutional environments. Comparative linguistics background is rare in defense/public sector AI.

**Biggest Gap**: No Cohere product experience (unlike Anthropic where you use Claude daily). Public sector security clearance may be required.

**Palette Context**: NEW — no existing Cohere context. Would need product deep dive. But the SA role description ("grow the Public Sector business, develop technical pre-sales and post-sales solutions") maps directly to ERA-4 delivery patterns.

**Action**: Research Cohere's product (Command R+, Embed, Rerank) before applying. Build product fluency.

---

### 4. Mistral — TME / London Hub
**Profile**: `enablement_systems_builder` | **CAPE Hedge**: EU ~22

| Requirement | Weight | Score | Evidence |
|-------------|--------|-------|----------|
| Technical content creation | 2x | 92 | ERA-4 Ask Pathfinder + ERA-5 Palette enablement system V1 |
| Developer enablement | 2x | 92 | ERA-4 (250+ sessions, 12K sellers, 140K ecosystem) |
| AI product fluency | 2x | 95 | ERA-4 dedicated Mistral partner at AWS + ERA-5 daily Claude/Vibe usage |
| Curriculum/assessment design | 1x | 85 | ERA-5 Palette (121 modules, calibration, 3-layer eval) |
| Open source / community | 1x | 78 | Palette is open source; Mistral is OSS-first |
| Multilingual | 1x | 95 | French fluent (Mistral = Paris HQ), Italian fluent, Spanish proficient |

**Weighted Score**: ((92+92+95)×2 + (85+78+95)×1) / 9 = **(558+258)/9 = 90.7 → TIER 1**

**Killer Differentiator**: "Already done the job from the other side" — organized enterprise enablement featuring Mistral at AWS. French fluent for Paris HQ. Power user of Vibe (Mistral's CLI).

**Biggest Gap**: None critical. Pipeline already warm (Tech + HM + Specialist rounds expected).

**Palette Context**: DEEP — dedicated Mistral partner, STORY-2 (Mistral partnership at AWS), Vibe CLI daily usage. Prep materials already built in `implementations/talent/talent-mistral-tme/`.

**Status**: ALREADY IN PIPELINE — continue. London roles expand geographic options if Paris doesn't land.

---

### 5. Databricks — EMEA Hub (London)
**Profile**: `enablement_strategy` | **CAPE Hedge**: UK 16.7

| Requirement | Weight | Score | Evidence |
|-------------|--------|-------|----------|
| Scaled enablement/adoption | 2x | 92 | ERA-4 (12K sellers, 250+ sessions, 20K users, +67% adoption) |
| Executive engagement | 2x | 90 | ERA-4 Data Forum (291 leaders, 98 CxOs) |
| Measurement & outcomes | 2x | 90 | ERA-4 three-level measurement (+17% engagement, +67% adoption, +50% CSAT) |
| AI/ML technical depth | 1x | 80 | ERA-2 POI Graph + ERA-3 AGI + ERA-5 Palette |
| Change management | 1x | 82 | ERA-1 (200+ associates, 4 countries, multilingual programs) |

**Weighted Score**: ((92+90+90)×2 + (80+82)×1) / 8 = **(544+162)/8 = 88.3 → TIER 1**

**Killer Differentiator**: $850M UK investment + training 100,000 people mandate = massive enablement need. Your ERA-4 proof (12K users, three-level measurement) is exactly what scales this.

**Biggest Gap**: Databricks is a data platform, not a model company. Your LLM-native positioning (Palette, Claude) is adjacent but not core to their Spark/Delta Lake/Unity Catalog stack.

**Palette Context**: Standard — Databricks in ES companies_targeted. Would need product deep dive on Unity Catalog, Delta Lake, Mosaic AI.

**Market Crash Hedge**: STRONG — $850M committed investment, new EMEA HQ, long-term hiring plan. Even in a downturn, committed capex tends to follow through.

---

### 6. Databricks — Sr. Software Engineer (Aarhus, Denmark)
**Profile**: `knowledge_data_engineer` | **CAPE Hedge**: Denmark ~22

| Requirement | Weight | Score | Evidence |
|-------------|--------|-------|----------|
| Knowledge architecture / ontology | 2x | 90 | ERA-2 POI Graph (25B nodes, hierarchical ontology) |
| Data pipelines | 2x | 82 | ERA-2 Spark ETL + ERA-5 Palette validation pipelines |
| Entity resolution / data fusion | 2x | 88 | ERA-2 vector-based entity resolution, 47 providers |
| LLM/RAG | 1x | 80 | ERA-3 + ERA-5 |
| Multilingual | 1x | 95 | 4 languages — high value in Denmark context |

**Weighted Score**: ((90+82+88)×2 + (80+95)×1) / 8 = **(520+175)/8 = 86.9 → TIER 1**

**Killer Differentiator**: Deep Spark experience (ERA-2 POI ETL pipelines) maps directly to Databricks' core stack.

**Biggest Gap**: "Sr. Software Engineer" implies heavy IC coding. Your recent years are more architect/enablement than daily code output. ERA-5 Palette is the freshest code evidence.

**Palette Context**: Limited. Denmark is the smallest market of the four.

**Assessment**: Tier 1 on paper but the role is more code-IC than your trajectory. **Adjusted to Tier 2** given career direction.

---

### 7. Google DeepMind — Applied AI (London)
**Profile**: `knowledge_data_engineer` | **CAPE Hedge**: UK 16.7

| Requirement | Weight | Score | Evidence |
|-------------|--------|-------|----------|
| Knowledge architecture / ontology | 2x | 92 | ERA-2 POI Graph (25B nodes, hierarchical ontology, 47 providers) |
| Data pipelines | 2x | 82 | ERA-2 Spark ETL |
| Entity resolution / data fusion | 2x | 88 | ERA-2 vector entity resolution |
| LLM/RAG | 1x | 82 | ERA-3 attribution + ERA-5 Palette RAG |
| Multilingual | 1x | 95 | 4 languages |

**Weighted Score**: ((92+82+88)×2 + (82+95)×1) / 8 = **(524+177)/8 = 87.6 → TIER 1**

**Killer Differentiator**: 25B-node knowledge graph is DeepMind-scale data engineering. Comparative linguistics background maps to NLP research support.

**Biggest Gap**: DeepMind is research-first. Your profile is applied/enterprise. The "Applied AI" track exists but is a minority of roles. Also Google's interview bar (L5/L6 coding) is notoriously high on algorithmic questions.

**Assessment**: Tier 1 on knowledge engineering fit, but **adjusted to Tier 2** given Google's specific interview format and research orientation.

---

### 8. Datadog — DevRel / Technical Community (Madrid)
**Profile**: `enablement_systems_builder` | **CAPE Hedge**: Spain 18.2

| Requirement | Weight | Score | Evidence |
|-------------|--------|-------|----------|
| Technical content creation | 2x | 88 | ERA-4 Ask Pathfinder (100+ use cases, 250+ sessions) |
| Developer enablement | 2x | 88 | ERA-4 (12K sellers, 20K users) |
| AI product fluency | 2x | 70 | Datadog is observability, not AI-native. Palette uses no Datadog products. |
| Curriculum/assessment design | 1x | 85 | ERA-5 Palette |
| Open source / community | 1x | 72 | Palette is open source |
| Multilingual | 1x | 90 | Spanish proficient — direct value for Madrid |

**Weighted Score**: ((88+88+70)×2 + (85+72+90)×1) / 9 = **(492+247)/9 = 82.1 → TIER 2**

**Killer Differentiator**: Spanish language ability is rare for DevRel roles. Madrid cost of living is significantly lower than London/Sydney.

**Biggest Gap**: Datadog product fluency = zero. Observability (metrics, traces, logs) is adjacent to your AI work but not the same domain. Significant product learning curve.

**Palette Context**: NEW — WhyLabs was discontinued (Apple acquisition), but Palette evaluated Arize AI and Evidently AI as alternatives. Some domain overlap in AI observability.

---

### 9. OpenAI — EU FDE/SA roles (London/Dublin)
**Profile**: `customer_success_ai` | **CAPE Hedge**: UK 16.7 / Ireland ~18

| Requirement | Weight | Score | Evidence |
|-------------|--------|-------|----------|
| Customer-facing delivery | 2x | 90 | ERA-4 Ask Pathfinder (12K sellers, 250+ sessions) |
| AI product deployment | 2x | 88 | ERA-4 partners (Mistral, xAI) + ERA-5 Palette |
| Outcome measurement | 2x | 90 | ERA-4 three-level measurement + ERA-3 evaluation frameworks |
| Technical depth | 1x | 85 | ERA-2 POI + ERA-5 Palette |
| Executive relationships | 1x | 90 | ERA-4 Data Forum (98 CxOs) |

**Weighted Score**: ((90+88+90)×2 + (85+90)×1) / 8 = **(536+175)/8 = 88.9 → TIER 1**

**Killer Differentiator**: Recruiter screen "literally went perfectly." Submitted takehome. Warm relationship exists. OpenAI EU expansion gives a second shot at the company without re-entering US pipeline.

**Biggest Gap**: No current EU-specific roles posted. Need to monitor and reactivate recruiter when roles appear.

**Palette Context**: STRONG — OpenAI takehome submitted, prep materials built, Sora tracked in signals.

**Action**: Reactivate recruiter contact. Ask about EU-based deployment manager or SA roles.

---

### 10. Anthropic — AI Engineer (Dublin)
**Profile**: `forward_deployed_engineer` | **CAPE Hedge**: Ireland ~18

| Requirement | Weight | Score | Evidence |
|-------------|--------|-------|----------|
| Systems architecture | 2x | 92 | ERA-2 POI + ERA-5 Palette |
| Customer delivery | 2x | 75 | ERA-4 — but AI Engineer is more IC than customer-facing |
| Technical depth (Python, APIs) | 2x | 90 | ERA-5 Palette (daily Python, Claude API) |
| LLM/RAG experience | 1x | 90 | ERA-3 + ERA-5 |
| Startup experience | 1x | 78 | ERA-5 Palette |

**Weighted Score**: ((92+75+90)×2 + (90+78)×1) / 8 = **(514+168)/8 = 85.3 → TIER 1**

**Killer Differentiator**: Same Claude-native advantage as London SA. Dublin = English-speaking EU + tech hub tax benefits.

**Biggest Gap**: "AI Engineer" at Anthropic is heavy IC engineering (systems, inference, safety). More coding-intensive than your recent trajectory.

**Assessment**: Tier 1 on requirements mapping, **adjusted to Tier 2** given the IC coding intensity mismatch.

---

### 11. Red Hat AI — Spain/EMEA
**Profile**: `enablement_strategy` | **CAPE Hedge**: Spain 18.2

| Requirement | Weight | Score | Evidence |
|-------------|--------|-------|----------|
| Scaled enablement/adoption | 2x | 88 | ERA-4 (12K sellers, 250+ sessions) |
| Executive engagement | 2x | 85 | ERA-4 Data Forum (291 leaders) |
| Measurement & outcomes | 2x | 82 | ERA-4 three-level measurement |
| AI/ML technical depth | 1x | 75 | Red Hat = open source infra, not frontier AI |
| Change management | 1x | 82 | ERA-1 (4 countries, multilingual) |

**Weighted Score**: ((88+85+82)×2 + (75+82)×1) / 8 = **(510+157)/8 = 83.4 → TIER 2**

**Killer Differentiator**: Spanish proficiency + EU work pattern experience (Milan + Paris years). Red Hat AI GTM enablement maps to ERA-4 patterns.

**Biggest Gap**: Red Hat AI is enterprise infrastructure AI (RHEL AI, InstructLab), not frontier model company. Less aligned with your long-term trajectory (SageMaker disruptor vision).

---

### 12. Hugging Face — DevRel (Remote EU)
**Profile**: `enablement_systems_builder` | **CAPE Hedge**: Remote EU (diversified)

| Requirement | Weight | Score | Evidence |
|-------------|--------|-------|----------|
| Technical content creation | 2x | 88 | ERA-4 + ERA-5 |
| Developer enablement | 2x | 85 | ERA-4 |
| AI product fluency | 2x | 82 | ERA-5 Palette uses HF-adjacent tools (transformers, embeddings) but not HF Hub directly |
| Curriculum/assessment design | 1x | 85 | ERA-5 Palette |
| Open source / community | 1x | 82 | Palette is open source; HF is the OSS AI hub |
| Multilingual | 1x | 92 | 4 languages — HF is global/multilingual |

**Weighted Score**: ((88+85+82)×2 + (85+82+92)×1) / 9 = **(510+259)/9 = 85.4 → TIER 1**

**Killer Differentiator**: Multilingual DevRel at the world's largest open-source AI platform. Comparative linguistics + knowledge engineering + 4 languages = rare combination.

**Biggest Gap**: No direct HF Hub contribution history. Would need to build visible open-source presence on the platform.

---

## Consolidated Pipeline Tracker

| # | Company | Role | Location | profile_id | Fit Score | Tier | Status | CAPE Hedge | Palette Context | Priority |
|---|---------|------|----------|-----------|-----------|------|--------|-----------|----------------|----------|
| 4 | **Mistral** | TME / London | Paris/London | ESB | **90.7** | **1** | INTERVIEWING | 22 | DEEP | **P0** |
| 9 | **OpenAI** | EU FDE/SA | London/Dublin | CSAI | **88.9** | **1** | REACTIVATE | 16.7 | STRONG | **P1** |
| 2 | **Anthropic** | Sydney (emerging) | Sydney | ESB | **88.7** | **1** | APPLY | 20.2 | MAXIMUM | **P1** |
| 1 | **Anthropic** | SA Applied AI | London | FDE | **88.5** | **1** | APPLY NOW | 16.7 | MAXIMUM | **P1** |
| 5 | **Databricks** | EMEA Hub | London | ES | **88.3** | **1** | APPLY | 16.7 | Standard | **P1** |
| 7 | **Google DeepMind** | Applied AI | London | KDE | **87.6→T2** | **2** | APPLY | 16.7 | Limited | **P2** |
| 6 | **Databricks** | Sr. SWE | Aarhus | KDE | **86.9→T2** | **2** | WATCH | 22 | Limited | **P3** |
| 3 | **Cohere** | SA Public Sector | London | FDE | **85.4** | **1** | APPLY | 16.7 | NEW | **P1** |
| 12 | **Hugging Face** | DevRel | Remote EU | ESB | **85.4** | **1** | APPLY | N/A | Limited | **P2** |
| 10 | **Anthropic** | AI Engineer | Dublin | FDE | **85.3→T2** | **2** | WATCH | 18 | MAXIMUM | **P2** |
| 11 | **Red Hat AI** | GTM Enablement | Spain/EMEA | ES | **83.4** | **2** | APPLY | 18.2 | Limited | **P3** |
| 8 | **Datadog** | DevRel | Madrid | ESB | **82.1** | **2** | APPLY | 18.2 | NEW | **P3** |

---

## Top-Line Findings

### 9 of 12 targets score Tier 1 or strong Tier 2

The talent match confirms the global search hypothesis: these markets have high-fit roles, not just safe economics.

### Profile Distribution
| Profile | Count | Avg Score |
|---------|-------|-----------|
| `enablement_systems_builder` (ESB) | 4 | 86.7 |
| `forward_deployed_engineer` (FDE) | 4 | 86.7 |
| `enablement_strategy` (ES) | 2 | 85.9 |
| `customer_success_ai` (CSAI) | 1 | 88.9 |
| `knowledge_data_engineer` (KDE) | 2 | 87.3 |

**ESB and FDE are the dominant profiles** — your career maps best to "build the enablement system" and "architect the solution for the customer."

### Geographic Distribution by Tier
| Location | Tier 1 | Tier 2 | Total |
|----------|--------|--------|-------|
| **London** | 4 | 2 | **6** |
| **Paris** | 1 | 0 | **1** |
| **Sydney** | 1 | 0 | **1** |
| **Remote EU** | 1 | 0 | **1** |
| **Dublin** | 0 | 1 | **1** |
| **Spain/EMEA** | 0 | 2 | **2** |
| **Denmark** | 0 | 1 | **1** |

**London is the clear winner** — 6 targets including 4 Tier 1. This makes sense: UK CAPE 16.7 (undervalued) + AI company EMEA expansion wave (Anthropic, Databricks, Cohere, DeepMind, Mistral) = highest density of high-fit roles in a crash-resilient market.

### Crash Resilience × Fit Score Matrix

```
                    HIGH FIT (85+)                    MODERATE FIT (75-84)
              ┌──────────────────────────────┬──────────────────────────────┐
 LOW CAPE     │ ★ Anthropic London (88.5)    │   Red Hat Spain (83.4)       │
 (< 20)       │ ★ Cohere London (85.4)       │   Datadog Madrid (82.1)      │
 Most hedge   │ ★ Databricks London (88.3)   │                              │
              │ ★ DeepMind London (87.6)     │                              │
              │ ★ OpenAI London/Dublin (88.9) │                              │
              ├──────────────────────────────┼──────────────────────────────┤
 MED CAPE     │ ★ Anthropic Sydney (88.7)    │   Databricks Aarhus (86.9)   │
 (20-25)      │ ★ Mistral Paris/London (90.7)│                              │
 Good hedge   │ ★ Hugging Face EU (85.4)     │                              │
              ├──────────────────────────────┼──────────────────────────────┤
 HIGH CAPE    │   (US roles — avoid)         │   (US roles — avoid)         │
 (> 35)       │                              │                              │
              └──────────────────────────────┴──────────────────────────────┘
```

**SWEET SPOT**: Upper-left quadrant — high fit + low CAPE. That's London (Anthropic, Cohere, Databricks, OpenAI) and Sydney (Anthropic).

---

## Immediate Action Plan

### This Week (P0 + P1)
1. **Mistral** → Continue pipeline (already interviewing)
2. **Anthropic London SA** → Apply immediately — 4 SA roles open, MAXIMUM Palette context
3. **Cohere London SA** → Apply — research Command R+ first, build product fluency
4. **Anthropic Sydney** → Apply to London SA, flag Sydney interest in cover letter
5. **Databricks London** → Apply to EMEA enablement roles — $850M investment = job security
6. **OpenAI EU** → Reactivate recruiter — ask about London/Dublin deployment roles

### Next Week (P2)
7. **Google DeepMind** → Apply to Applied AI track
8. **Hugging Face** → Apply to DevRel EU roles
9. **Anthropic Dublin** → Monitor for SA/enablement roles (AI Engineer is too IC)

### Watch (P3)
10. **Red Hat AI Spain** → Apply if no Tier 1 traction by end of April
11. **Datadog Madrid** → Apply if no Tier 1 traction
12. **Databricks Aarhus** → Watch only (wrong trajectory)

### EU Search Patterns to Add to `role-profiles.yaml`
The `eu_search` section should be updated with:
```yaml
- { name: Anthropic, location: London, profile: forward_deployed_engineer }
- { name: Anthropic, location: Sydney, profile: enablement_systems_builder }
- { name: Cohere, location: London, profile: forward_deployed_engineer }
- { name: Databricks, location: London, profile: enablement_strategy }
- { name: "Google DeepMind", location: London, profile: knowledge_data_engineer }
- { name: Datadog, location: Madrid, profile: enablement_systems_builder }
- { name: "Hugging Face", location: "Remote EU", profile: enablement_systems_builder }
```

---

## Resume Generation Queue (Phase 2 — Next Step)

Based on the profile distribution, you need **3 resumes** to cover all 12 targets:

| Resume | Profile | Targets Covered | build_resume.py flag |
|--------|---------|----------------|---------------------|
| FDE Resume | `forward_deployed_engineer` | Anthropic London, Cohere London, Anthropic Dublin | `--profile forward_deployed_engineer` |
| ESB Resume | `enablement_systems_builder` | Mistral, Anthropic Sydney, Datadog Madrid, Hugging Face | `--profile technical_marketing_engineer` |
| ES Resume | `enablement_strategy` | Databricks London, Red Hat Spain | `--profile enablement_strategy` |

OpenAI (CSAI) and DeepMind/Databricks Aarhus (KDE) can use the FDE resume with minor positioning adjustments.

---

## Market Failure Probability Integration

| If US crashes (71% probability)... | Impact on This Pipeline |
|-------------------------------------|------------------------|
| US-based AI companies freeze hiring | **London/Sydney/EU offices are separate legal entities** — hiring continues for committed roles |
| Comp benchmarks compress | UK/AU/EU comps are already 20-40% below US — less room to compress |
| Visa sponsorship tightens | **UK/AU have active skilled worker visa pathways** (188/482 AU, Skilled Worker UK) |
| Runway pressure on startups | Anthropic ($2B+), Databricks ($62B), Google = well-funded. Cohere, Mistral = later-stage. Low runway risk. |
| AI spending shifts to efficiency | **Enablement roles become MORE valuable** in efficiency mode — your ES/ESB profiles benefit |

**Net assessment**: This pipeline is **crash-resilient by design**. The highest-fit targets (Anthropic, Databricks, Mistral, OpenAI, Google) are well-capitalized companies expanding into undervalued markets. Even in a bear case, these roles are likely to survive.
