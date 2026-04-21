# Answer Backbone — Topic-Indexed Experience Library

**Purpose**: This file is for Claude Code (and other agents) to use as a backbone when building CHEATSHEET.md files. It is NOT a user-facing document. It solves the problem of overlapping answers by organizing experiences BY TOPIC rather than by story, so each cheatsheet section can draw from a different experience without double-dipping.

**How to use**: When building a cheatsheet for a new role, scan the JD for topics. For each topic, find the matching section below, pick the strongest experience that hasn't been used in another section yet, and write the spoken answer from the details here. Every number is GREEN-verified unless marked YELLOW.

**Rule**: Never use the same experience in two cheatsheet sections. If "Foursquare/TripAdvisor provider swap" is used for SQL, use a DIFFERENT experience for Dashboards. This library exists to make that possible.

---

## TOPIC: SQL / DATA ANALYSIS

### Experience A: Foursquare/TripAdvisor Provider Swap (ERA-2, Alexa)
- **Context**: Deciding whether to replace Foursquare/Factual with TripAdvisor as POI data source. Decision stuck — nobody understood true dependency across 47 feeds, 2 APIs, and a large scraped-data pipeline.
- **What I did**: Dug into SQL, decomposed composite provider-ID field to measure actual source-level dependency. Built two metrics: unique contribution (Foursquare in 27% of records but only 2% truly uniquely dependent) and provider differentiation (flags quality issues when one source diverges sharply from the rest).
- **Result**: TripAdvisor added 7% net-new coverage with richer metadata (kid-friendly beaches, dog beaches, vegan, accessibility). Analysis gave team confidence to make the switch. Turned metrics into a dashboard for ongoing supplier and quality decisions.
- **Numbers**: 47 feeds, 2 APIs, 27% appearance rate, 2% true dependency, 7% net-new coverage
- **Best for**: SQL depth, data-driven decision making, turning ambiguity into actionable analysis

### Experience B: Ask Pathfinder Quality Scoring (ERA-4, AWS)
- **Context**: Five competing chatbot tools, no shared quality baseline. Needed to evaluate which pieces were strongest.
- **What I did**: Built a quality-scoring prompt and ran it against the tool's own traces. Analyzed retrieval patterns to diagnose lazy routing to the same small set of documents.
- **Result**: Data analysis drove the consolidation decision. Evidence-based, not opinion-based.
- **Best for**: Using data to diagnose operational bottlenecks, data-informed decision making

### Experience C: Adoption/KPI Instrumentation (ERA-4, AWS)
- **Context**: Needed to measure whether enablement sessions and tooling were actually changing behavior, not just generating activity.
- **What I did**: Built KPI instrumentation tracking usage, behavior change, and feature adoption. Tracked retrieval quality and discovery patterns.
- **Numbers**: +17% engagement, +50% satisfaction, +67% feature adoption, 250+ sessions/year, 20,000+ users
- **Best for**: Metrics design, proving ROI, adoption measurement

### Experience D: Entity Resolution Thresholds (ERA-2, Alexa)
- **Context**: 47 providers describing same real-world entities differently. Same restaurant in 6 feeds with conflicting names, addresses, hours.
- **What I did**: Vector-based entity resolution with per-locale tunable thresholds. Asymmetric merge: high confidence auto-merge, low confidence to human review queue. Source-priority rules with recency weighting.
- **Numbers**: 25 billion nodes, 47 providers, 13 locales, ~30 annotators
- **Best for**: Conflicting data, entity resolution, quality at scale

---

## TOPIC: DASHBOARDS / REPORTING / VISUALIZATION

### Experience A: Provider Dependency Dashboard (ERA-2, Alexa)
- **Context**: Provider swap analysis needed to be visible to engineering, data ops, and product simultaneously.
- **What I did**: Built dashboard showing real-time source coverage, unique dependency percentages, and quality divergence flags across the full 47-provider merge build. Teams used it for ongoing supplier and quality decisions.
- **Best for**: Dashboard that drives decisions, cross-team visibility
- **NOTE**: If the Foursquare/TripAdvisor story is already used for SQL, use a different dashboard experience.

### Experience B: Ask Pathfinder KPI Dashboard (ERA-4, AWS)
- **Context**: Ask Pathfinder scaled to 12,000 users/month. Needed to prove the taxonomy restructure was working and track ongoing retrieval quality.
- **What I did**: Built KPI instrumentation and adoption tracking — retrieval quality, discovery patterns, usage metrics. Tracked whether the taxonomy change actually improved how sellers found content.
- **Numbers**: 12,000+ users/month, 25% reduction in prep time, 67% increase in sales-play coverage
- **Best for**: Adoption dashboards, proving structural improvements with data

### Experience C: OpenAI Takehome Visibility Dashboard (ERA-5, Independent)
- **Context**: OpenAI AI Deployment Manager takehome. Needed to demonstrate visibility bridge between developers and leadership.
- **What I did**: Built Streamlit visibility dashboard with simulated Codex usage data. Governing thesis: "visibility bridges the gap between developers and leadership."
- **Best for**: Prototype dashboards, demonstrating dashboard thinking in interviews

### Experience D: Data Leadership Forum Metrics (ERA-4, AWS)
- **Context**: Needed to track engagement and value of executive community.
- **What I did**: Tracked community growth, engagement patterns, and content effectiveness for 291 data leaders and 98 CxOs.
- **Numbers**: 291 senior data leaders, 98 CxOs
- **Best for**: Executive-level reporting, community metrics

---

## TOPIC: PROGRAM EXECUTION / MULTI-WORKSTREAM

### Experience A: Ask Pathfinder Consolidation (ERA-4, AWS)
- **Context**: Five different teams building overlapping sales-assist tools. Fragmented capability, no shared quality baseline.
- **What I did**: Joined three-person team, built quality-scoring prompt to evaluate traces across tools, used analysis to bring teams together. Preserved strongest pieces from each group (UX, answer quality, data ownership). Gave each team a win they could claim.
- **Result**: Consolidated into one tool. 25% reduction in seller prep time, ~3 hours saved per seller per week, scaled to 12,000 monthly users.
- **Best for**: 0-to-1 execution, unifying competing efforts, cross-functional program management

### Experience B: Alexa 47 Providers / 13 Locales (ERA-2)
- **Context**: 47 data providers across 13 locales. Challenge was consistency, mapping, and quality across distributed systems.
- **What I did**: Made the problem legible through structure, data, and coordination. Designed canonical schema, taxonomy normalizing 47 provider categorization schemes, entity resolution strategy, source-priority rules.
- **Result**: Architecture proved generalizable — new locales onboard via config, not rebuild. Led Italy launch leveraging Italian fluency.
- **Best for**: Scale, distributed systems, messy data, operational coordination

### Experience C: Amazon Kaizen / Continuous Improvement (ERA-1)
- **Context**: Operational metrics and customer behavior in retail/fulfillment.
- **What I did**: Led continuous improvement work grounded in operational metrics. Find the real bottleneck, quantify it, change the system, measure whether behavior actually improves.
- **Best for**: Continuous improvement, metrics-driven ops, operational discipline

### Experience D: Enablement Program Scale (ERA-4, AWS)
- **Context**: 250+ enablement sessions per year across a 140,000-person partner ecosystem.
- **What I did**: Managed multiple workstreams simultaneously — content development, session delivery, partner coordination, measurement, and tooling.
- **Numbers**: 250+ sessions/year, 20,000+ users, 140,000-person ecosystem
- **Best for**: Managing multiple parallel workstreams at scale

---

## TOPIC: AI AGENTS / AI-ASSISTED WORKFLOWS

### Experience A: Palette Multi-Agent System (ERA-5)
- **Context**: Built from scratch to understand how AI models work in production.
- **What I did**: 12 specialized agents with taxonomy-driven routing, wire contracts (7 fields in, 7 out), integrity gates on every output. Resolver classifies intent, researcher retrieves evidence, builder executes, validator checks output.
- **Numbers**: 121 taxonomy nodes, 176 knowledge entries, 2,013-quad relationship graph, 12 agents, 75 integration recipes, 149 tests, 103 health checks
- **Best for**: AI agent design, orchestration, governance, repeatable AI systems

### Experience B: AWS Frontier AI Partner Enablement (ERA-4)
- **Context**: Translating frontier AI model capabilities into enterprise deployment narratives.
- **What I did**: Organized enablement programs for Mistral, xAI, Stability AI, Luma AI, TwelveLabs. Translated model capabilities into actionable content for 140,000-person ecosystem.
- **Numbers**: 5 frontier AI partners, 140,000-person ecosystem, 5x YoY revenue growth
- **Best for**: AI tool adoption, translating AI capabilities for enterprise users

### Experience C: Low Adoption Rescue (ERA-4, AWS)
- **Context**: Prospecting community hesitant to use new AI-powered IDE tool. Usage was low, team pushing for more training.
- **What I did**: Diagnosed: problem wasn't awareness, it was that no one had seen value in their specific workflow. Designed five-minute exercise: use the tool to find sales spiffs they were missing. Within minutes, sellers finding money they didn't know about.
- **Result**: Adoption increased quickly, spread naturally to adjacent use cases.
- **Best for**: Practical AI tool adoption, proof-creates-pull pattern

### Experience D: MCP Governed Coordination (ERA-5)
- **Context**: Live multi-agent system using MCP for governed coordination.
- **What I did**: Verified live broker, peer registration, send/receive, human-checkpoint path, delegated execution. Found trust defaults and approval semantics weaker in practice than safety story implied.
- **Best for**: Technical verification, safety judgment, launch readiness

---

## TOPIC: RISK / QUALITY / COMPLIANCE

### Experience A: AGI Structured Attribution Pipeline (ERA-3)
- **Context**: Evaluating AI output quality — needed to move from subjective "does this look right?" to measurable.
- **What I did**: Decomposed AI outputs into discrete claims, linked each claim to source passages, scored support strength (fully supported, partially supported, unsupported). Treated low annotator agreement as signal that rubric was unclear. Used risk tiers: low-stakes → probabilistic inference, high-stakes → verified evidence required.
- **Key insight**: Hallucination is a knowledge coverage problem, not just a model problem. Filling knowledge gaps reduced hallucination rates more than model tuning.
- **Best for**: AI quality evaluation, structured quality frameworks, risk tiering

### Experience B: Alexa Data Quality at Scale (ERA-2)
- **Context**: Data quality issues across 47 providers would cascade into customer experience if not caught.
- **What I did**: Designed quality gates, validation rules, coverage metrics, automated anomaly detection. Field-level provenance (not entity-level) so conflicts are traceable.
- **Best for**: Data quality at scale, cascading risk, ingestion-time validation

### Experience C: Palette Governance Tiers (ERA-5)
- **Context**: Multi-agent system needed clear governance so agents know what they're allowed to do without asking.
- **What I did**: Three tiers: immutable core rules, experimental buffer for testable assumptions, append-only execution log. Every RIU classified for reversibility (two-way, one-way, mixed). System blocks on one-way doors.
- **Best for**: Governance, compliance, decision classification, one-way door protocol

### Experience D: Annotation Quality / Inter-Rater Reliability (ERA-3, AGI)
- **Context**: ~30 annotators producing labeled judgments feeding RL training loops. When model quality degraded, first question: data issue or model issue?
- **What I did**: Measured inter-annotator agreement (Cohen's kappa). Used disagreement analysis to refine rubrics. Versioned datasets with lineage tracking.
- **Key insight**: Most quality issues traced to data (annotator disagreement, guideline ambiguity), not model.
- **Best for**: Training data quality, annotation management, RL pipelines

---

## TOPIC: CROSS-FUNCTIONAL COORDINATION / STAKEHOLDER MANAGEMENT

### Experience A: Ask Pathfinder Team Unification (ERA-4, AWS)
- **Context**: Five competing teams, none with full authority over the others. Political tension.
- **What I did**: Used quality audit results as neutral evidence. Got both teams in a room, gave each a win they could claim, unified the effort.
- **Best for**: Influence without authority, unifying competing teams, evidence-based alignment

### Experience B: Alexa Cross-Org Coordination (ERA-2)
- **Context**: 47 providers across 13 locales, multiple internal teams (engineering, science, data ops, product).
- **What I did**: Made the problem legible through structure and data so teams could execute against it instead of fighting same issues every sprint. Partnered with engineering and science on pipelines, vector search, relevance tuning.
- **Best for**: Cross-team coordination at scale, translating between technical and non-technical groups

### Experience C: Data Leadership Forum (ERA-4, AWS)
- **Context**: 291 data leaders and 98 CxOs needed a space to stress-test AI strategies, not receive product demos.
- **What I did**: Designed forum around decision frameworks, not feature lists. Real architecture patterns, real failure modes, real cost models.
- **Numbers**: 291 leaders, 98 CxOs
- **Best for**: Executive engagement, building trust with senior audiences, thought leadership

### Experience D: AWS Partner Ecosystem (ERA-4)
- **Context**: 140,000-person partner ecosystem with 5 frontier AI partners.
- **What I did**: Translated model capabilities into enterprise deployment narratives. Curated technical content, ran enablement sessions, helped sellers articulate value for specific customer use cases.
- **Numbers**: 140,000-person ecosystem, 5x YoY revenue growth
- **Best for**: Partner management, ecosystem coordination, technical translation

---

## TOPIC: KNOWLEDGE ARCHITECTURE / TAXONOMY / ONTOLOGY

### Experience A: Ask Pathfinder 3-Layer KB (ERA-4, AWS)
- **Context**: Internal knowledge organized by industry. Wrong organizing principle for LLM retrieval.
- **What I did**: Designed 3-layer architecture: content ingestion, metadata layer (type/subType/pf_metaKeywords as human-designed signals), use-case ontology spanning 15 verticals and 100+ use cases. Reclassified from industry-based to function-based.
- **Key insight**: Cross-domain patterns exist. Detection, classification, generation, optimization are the same functional patterns across industries.
- **Numbers**: 15 verticals, 100+ use cases, 12,000+ users/month
- **Best for**: Knowledge architecture, taxonomy design, retrieval system design

### Experience B: POI Category Taxonomy (ERA-2, Alexa)
- **Context**: 47 different provider categorization schemes for the same entity types.
- **What I did**: Designed hierarchical ontology accommodating granular (200+) and coarse (10) taxonomies into one consistent hierarchy.
- **Numbers**: 47 provider schemes unified, 25 billion nodes
- **Best for**: Ontology design, unifying conflicting classification schemes

### Experience C: Palette Taxonomy as Routing Layer (ERA-5)
- **Context**: Needed a way to classify any AI/ML problem and route it to the right knowledge, services, and agents.
- **What I did**: 121-node taxonomy where classification IS routing. Classify the problem → know what knowledge, services, and agents to apply. Evidence tiers for source quality. Fail-closed validation.
- **Numbers**: 121 nodes, 176 knowledge entries, 75 integration recipes
- **Best for**: Taxonomy-driven routing, problem classification, knowledge governance

---

## TOPIC: ADOPTION / ENABLEMENT / BEHAVIOR CHANGE

### Experience A: Ask Pathfinder Adoption (ERA-4, AWS)
- **Context**: Built tool, needed to drive actual behavior change among 12,000+ sellers.
- **What I did**: Tracked usage → behavior shift → business outcomes (three-level measurement). Not vanity metrics.
- **Numbers**: 25% reduction in prep time, 67% sales-play coverage increase, 50% CSAT increase
- **Best for**: Proving adoption with metrics, three-level measurement

### Experience B: Low Adoption Rescue — AI IDE Tool (ERA-4, AWS)
- **Context**: New AI tool, low adoption, team pushing more training. Problem wasn't awareness.
- **What I did**: Designed five-minute exercise showing immediate value in their specific workflow (finding sales spiffs they were missing). Proof created pull.
- **Result**: Adoption increased quickly, spread naturally to adjacent use cases.
- **Best for**: Fixing low adoption, proof-creates-pull, narrow-then-expand pattern

### Experience C: Enablement at Scale (ERA-4, AWS)
- **Context**: 140,000-person partner ecosystem needing AI enablement.
- **What I did**: 250+ sessions/year reaching 20,000+ users. Content organized by problem solved, not product described.
- **Numbers**: 250+ sessions, 20,000+ users, +17% engagement, +67% feature adoption
- **Best for**: Enablement at enterprise scale, content strategy

---

## TOPIC: BUILDER CREDIBILITY / TECHNICAL DEPTH (HANDS-ON)

### Experience A: Palette Full System (ERA-5)
- **Full system**: 12 agents, 121 taxonomy nodes, 176 knowledge entries, 2,013-quad graph, 75 integrations, 149 tests, 103 health checks, Python SDK (86 tests), Go wire contracts, Telegram bridge
- **Best for**: Proving you build, not just advise. Use sparingly — lead with Amazon stories.

### Experience B: MCP Governed Coordination (ERA-5)
- **What I did**: Verified live multi-agent broker, exercised send/receive, validated human-checkpoint path. Found trust defaults weaker than policy language implied.
- **Best for**: Recent hands-on work, technical rigor, safety judgment

### Experience C: POI Knowledge Graph Architecture (ERA-2, Alexa)
- **What I did**: Designed knowledge architecture for 25-billion-node graph. Spark ETL, vector-based entity resolution, knowledge graph with typed relationships, NLU → graph traversal → ranking pipeline.
- **Best for**: System architecture, data engineering at scale, production systems

---

## STAT QUICK REFERENCE (ALL GREEN)

| Stat | Source |
|------|--------|
| 12,000+ sellers/month (Pathfinder) | Internal AWS metrics |
| 25% reduction in seller prep time | Internal measurement |
| 2-3 hours saved per seller per week | Internal measurement |
| 67% increase in sales-play coverage | Internal measurement |
| 50% increase in high-CSAT indicators | Internal measurement |
| 250+ sessions/year | Program records |
| 20,000+ users reached/year | Program records |
| 291+ senior data leaders (Forum) | Forum records |
| 98+ CxOs (Forum) | Forum records |
| +17% engagement | Program KPIs |
| +67% feature adoption | Program KPIs |
| 5x YoY revenue growth (partners) | Partner metrics |
| 47 data providers (Alexa) | Internal Alexa data |
| 13 locales (Alexa) | Internal Alexa data |
| 25 billion nodes (POI graph) | YELLOW — verify exact count |
| 27% Foursquare appearance rate | Analysis results |
| 2% true unique dependency | Analysis results |
| 7% TripAdvisor net-new coverage | Analysis results |
| 121 taxonomy nodes (Palette) | GitHub repo |
| 176 knowledge entries (Palette) | GitHub repo |
| 12 agents (Palette) | GitHub repo |
| 2,013-quad relationship graph | GitHub repo |
| 75 integration recipes (Palette) | GitHub repo |
| 149 tests (Palette) | GitHub repo |
| 140,000-person partner ecosystem | AWS org data |

---

*Built 2026-04-14. Source: experience-inventory.yaml, STAR_STORIES.md, iBusiness/Meta/Mistral/OpenAI/Gap prep materials.*
