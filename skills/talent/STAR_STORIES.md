# STAR Story Bank — Base File
**Updated**: 2026-03-27
**Purpose**: Single source of truth for behavioral interview stories. Role-specific preps in `implementations/talent/` pull from this file.

**How to use**: Each story has a 90-second version (default), an extended version (when asked for depth), and tagging for when to deploy it. The commit-based stories at the end are for proving you ship — use them when interviewers want concrete recent evidence.

---

## STORY 1: Ask Pathfinder — The GTM Chatbot
**Era**: AWS (ERA-4)
**Theme**: Technical content creation + cross-functional unification
**Tags**: `technical_content`, `sales_enablement`, `adoption`, `engineering_interface`, `knowledge_architecture`
**When to use**: "Tell me about yourself", "Give an example of enabling sales teams", "Technical content that drove adoption", "Tell me about unclear ownership"

### 90-Second Version
"At AWS I joined a three-person team building an internal sales chatbot called Ask Pathfinder. My first move was diagnostic — I built a quality scoring prompt and ran it against the tool's own traces. What it showed was that retrieval was lazily routing to the same small set of documents.

The fix required two things: restructuring the taxonomy from industry-based to function-based, so learnings could transfer across domains, and creating parent-child artifact relationships so one solution's approach could inform another.

But the real blocker wasn't technical — a parallel team had better data and worse algorithms, and they were competing instead of collaborating. I used the audit results as neutral evidence, got both teams in a room, gave each a win they could claim, and unified the effort.

Result: 25% reduction in seller prep time, two to three hours saved per seller per week, and the tool now serves over 12,000 sellers monthly."

### Extended Version — KB Architecture Detail
"The system I designed was a full knowledge base architecture with three layers:

**Content ingestion**: AWS public content, partner content, and internal curated mappings get transformed into summarized units with structured metadata — type, subType, and curated keywords.

**Metadata layer**: Every content unit gets a type (blog, solution, whitepaper, workshop, reference), a subType for fine-grained ranking, and what I called pf_metaKeywords — manually curated keyword sets that improve semantic similarity scoring. This is human-designed signal injection, not automated tagging. The metadata isn't decoration — it's a first-class retrieval control mechanism.

**Use-case ontology**: Instead of indexing documents, we indexed problems users are trying to solve. I built a master taxonomy across 15 verticals — customer support, sales, finance, insurance, supply chain, engineering, healthcare, manufacturing, energy, telecom, media, retail, autonomous vehicles, data/AI, and cross-domain horizontals — with over 100 specific use cases. A seller searching for 'how do I help a bank detect fraud' hits the right content because the ontology maps to the intent, not just the keywords.

The design principle: cross-domain patterns exist. Detection, classification, generation, optimization — these are the same functional patterns applied across industries. By organizing around function instead of industry, a solution from manufacturing anomaly detection could inform healthcare diagnostic support."

---

## STORY 2: POI Knowledge Graph
**Era**: Alexa Automotive (ERA-2)
**Theme**: Data engineering at scale + multilingual systems
**Tags**: `data_engineering`, `entity_resolution`, `scale`, `multilingual`, `knowledge_graphs`
**When to use**: "Walk me through a system you built", "Tell me about working with data at scale", "How do you handle conflicting data?", "Most technically complex project"

### 90-Second Version
"At Alexa Automotive I designed the knowledge architecture for a 25-billion-node POI Knowledge Graph. We were ingesting data from 47 providers — map vendors, restaurant aggregators, government databases — each with different schemas, quality bars, and update cadences. The same restaurant might appear in 6 feeds with conflicting names, addresses, and hours.

My approach was vector-based entity resolution: reduce each entity to an ID plus an embedding capturing its identity, then do nearest-neighbor matching with per-locale tunable thresholds. This replaced a brittle rule-based system that needed constant manual tuning.

I also designed the category taxonomy normalizing 47 different provider categorization schemes into one consistent hierarchy, and led the Italy launch leveraging my Italian fluency. The architecture proved generalizable — new locales onboard via configuration, not rebuild."

### Extended Version — Entity Resolution Detail
"The deeper challenge was conflicting data. Provider A says a restaurant closes at 10pm, Provider B says 11pm. Different names for the same place across languages. Six different category schemes for the same entity type.

I solved this with three design decisions:
1. **Field-level provenance** — not entity-level. Know exactly which source contributed each field, so conflicts are traceable.
2. **Asymmetric merge thresholds** — high confidence auto-merge, low confidence goes to human review queue. This prevented false merges (entity disappearance) without flooding the review queue.
3. **Source-priority rules with recency weighting** — when sources conflict on the same field, the system applies both a source quality ranking and a freshness signal.

I also managed two annotation teams (~30 people) producing training data for the entity resolution models and ground truth for quality evaluation. The workflow was: annotation guidelines → labeling → inter-annotator agreement measurement → disagreement review → guideline revision → retrain."

---

## STORY 3: Data Leadership Forum
**Era**: AWS (ERA-4)
**Theme**: Executive engagement + thought leadership
**Tags**: `executive_engagement`, `thought_leadership`, `content_strategy`, `community_building`
**When to use**: "How do you build credibility with senior audiences?", "Content for executive buyers", "How do you influence without authority?"

### 90-Second Version
"At AWS I created and ran the Data Leadership Forum — a technical community of 291 senior data leaders and 98 CxOs. The insight was that C-level buyers don't want product demos, they want to understand the decision architecture: what to build, what to buy, what to evaluate, and what to skip.

So I designed the forum around decision frameworks, not feature lists. We'd bring in real architecture patterns, real failure modes, and real cost models. No slides — just working sessions where leaders could stress-test their AI strategies against each other.

That's the difference between marketing content and technical marketing content. One tells you what a product does. The other helps you decide whether to bet on it."

---

## STORY 4: Taxonomy Restructuring
**Era**: AWS (ERA-4) — inside Ask Pathfinder
**Theme**: Design decision with business impact
**Tags**: `technical_depth`, `knowledge_architecture`, `design_decisions`, `simplifying_complexity`
**When to use**: "Tell me about a design decision", "How do you structure knowledge?", "Explain X to a non-technical audience", "Most impactful technical choice"

### 90-Second Version
"Inside Ask Pathfinder, I found that AWS's internal knowledge was organized by industry — law, healthcare, financial services. That made sense historically, but in an LLM context it's the wrong organizing principle. What matters is function: document processing, code generation, data extraction.

I had a migrations team with an elegant recursive commit-checking system — incredibly rigorous. And a legal document processing team that was purely semantic. By reclassifying both under 'document processing' and creating parent-child relationships between their artifacts, the rigor of one approach could improve the other. Accuracy improved significantly.

This is the kind of technical story that works in a whitepaper or a sales deck: take a complex architecture decision, show why it matters for the customer's outcome, and make the insight transferable."

---

## STORY 5: Mistral Partnership at AWS
**Era**: AWS (ERA-4)
**Theme**: Partner management + model deployment narrative
**Tags**: `partner_management`, `model_deployment`, `trust_building`, `translation`
**When to use**: "Why Mistral?", "Tell me about your AI experience", "How would you ramp up at an AI company?"

### 90-Second Version
"At AWS, I organized enterprise enablement programs featuring Mistral and other frontier AI partners — xAI, Stability AI, Luma AI, TwelveLabs. My job was to translate what these models could do technically into enablement content and deployment narratives that AWS's 140,000-person partner ecosystem could act on.

For Mistral specifically, that meant curating technical content for enterprise audiences, running enablement sessions on model selection and deployment architecture, and helping sellers articulate why Mistral's models mattered for specific customer use cases.

What I learned is that adoption isn't a model problem — it's a translation problem. The best model in the world doesn't get deployed if the sales team can't explain why it matters."

---

## STORY 6: Structured Attribution Pipeline
**Era**: Amazon AGI (ERA-3)
**Theme**: AI evaluation + hallucination detection
**Tags**: `ai_evaluation`, `hallucination_detection`, `training_data`, `quality_control`, `rl_pipelines`
**When to use**: "How do you evaluate AI quality?", "Tell me about working with ML teams", "How do you handle AI errors?"

### 90-Second Version
"At Amazon AGI, I designed a structured attribution pipeline for evaluating AI output quality. The core idea: decompose every AI output into individual claims, link each claim to a source document, and score the link strength. No link or weak link equals a potential hallucination.

This turned subjective 'does this look right?' evaluation into measurable 'what percentage of claims are traceable to sources?' The key insight was that hallucination is a knowledge coverage problem, not just a model problem. When we filled knowledge gaps in the source material, hallucination rates dropped more than when we tuned the model.

I also managed annotation teams producing labeled judgments that fed RL training loops. When model quality degraded, the first question was always: is this a data quality issue or a model issue? Most of the time, it was data — annotator disagreement or guideline ambiguity. That taught me that the quality of your training data sets the ceiling for your model's quality."

---

## STORY 7: Multilingual Communication
**Era**: Pre-Amazon (Paris years)
**Theme**: Cultural fit + communication range
**Tags**: `cultural_fit`, `communication`, `international`, `linguistics`, `teaching`
**When to use**: "Why Paris?", "How do you communicate with diverse audiences?", "Tell me about your background", "What makes you different?"

### 90-Second Version
"Before Amazon, I spent eight years in Paris — teaching at Sciences Po and Université Paris Ouest Nanterre, interpreting at international conferences, and designing domain-specific lexicons for the publishing industry.

Comparative linguistics teaches you one thing above all: the same concept expressed differently changes whether people understand it, believe it, and act on it. That's true whether you're teaching a class in French or writing a whitepaper about LLM fine-tuning.

I'm fluent in French and Italian, I hold an EU passport, and my family has deep roots in France. Paris isn't a relocation for me — it's a homecoming."

---

## STORY 8: Palette — Builder Credibility
**Era**: Independent (ERA-5)
**Theme**: Hands-on AI/ML building
**Tags**: `builder_credibility`, `hands_on`, `agent_design`, `multi_agent`, `governance`
**When to use**: "Personal projects?", "Technical depth?", "Hands-on AI experience?", "What have you built recently?"
**Note**: USE SPARINGLY. Lead with AWS stories. Deploy this when asked for technical depth or proof of building.

### 90-Second Version
"On my own time, I built Palette — an open-source multi-agent intelligence system with 12 specialized agents that route any AI decision to the right combination of internal knowledge and external services.

The system has 121 classified problem types, a 176-entry knowledge library with evidence tiers, a 2,013-quad relationship graph, and 69 working service integrations. It is a production Python codebase with 146 passing tests and a 12-section automated health audit that runs 103 checks across taxonomy, knowledge, agents, governance, enablement, and identity coherence.

I built it because I wanted to understand, at a deep level, how these models actually work in production — not just in demos. That hands-on builder experience is what makes me credible when creating technical content or advising customers on deployment."

### Extended Version — System Architecture
"Palette has three tightly coupled layers that share one ontology:

**Decision intelligence**: 121 classified problem types (RIUs), a 176-entry knowledge library with 466 citations, service routing across 40 routed RIUs, and 75 working integrations with auth, rate limits, and code examples. It classifies the problem, checks what it already knows, and routes to the right tool.

**Machine enablement**: 12 agents with bounded roles communicating through a wire contract — 7 fields in, 7 fields out — with an integrity engine that validates outputs before they ship. An SDK gives agents a shared base class, pre-emit validation, and a queryable relationship graph.

**Human enablement**: 121 hand-crafted curriculum modules, 14 published learning paths organized into 5 constellations, portfolio-based assessment with AI + human calibration, and 5 certification tracks. The same ontology the agents use to route decisions is what the curriculum teaches humans to understand.

The governance layer is three tiers: immutable core rules, an experimental buffer for testable assumptions, and an append-only execution log. Every RIU is classified for reversibility — two-way, one-way, or mixed — and the system blocks on one-way doors rather than just warning."

---

## STORY 9: Live MCP Verification
**Era**: Independent (ERA-5) — recent
**Theme**: Technical rigor + safety judgment
**Tags**: `technical_rigor`, `launch_readiness`, `safety`, `verification`, `mcp`
**When to use**: "What have you built recently?", "How do you verify quality?", "How technical are you day to day?"

### 90-Second Version
"Recently I worked on a live multi-agent system that uses MCP for governed coordination between different assistants. I didn't treat it like a demo. I started by checking the live broker and the peer registration, then I exercised real send and receive behavior, validated the human-checkpoint path, and confirmed delegated execution through the bus.

What made it useful was what came after the happy path. The transport worked, but I also found that the trust model and the runtime behavior were not perfectly aligned. The system's approval semantics and trust defaults were weaker than the policy language implied.

That is the kind of work I like doing: verify the system live, then look for where the operational reality diverges from the intended safety story."

---

## STORY 10: Low Adoption Rescue
**Era**: AWS (ERA-4)
**Theme**: Diagnosing and fixing adoption failure
**Tags**: `adoption`, `diagnosis`, `behavior_change`, `enablement`
**When to use**: "How do you handle low adoption?", "Tell me about a time something wasn't working", "How do you turn around a struggling initiative?"

### 90-Second Version
"At AWS I had a prospecting community that was hesitant to use a new AI-powered IDE tool. Usage was low and the team was pushing for more training sessions. My instinct said the problem wasn't awareness — they knew about the tool. The problem was that no one had shown them value in their specific workflow.

So instead of more training, I designed a five-minute exercise: use the tool to find sales spiffs they were missing. It was narrow, concrete, and immediately valuable. Within minutes, sellers were finding money they hadn't known about.

Once the value became real in their own workflow, adoption increased quickly and spread naturally to adjacent use cases. The lesson: proof creates pull. You don't convince people to use a tool — you show them one thing it does that they can't ignore."

---

## COMMIT-BASED STAR ANSWERS
**Source**: Palette git history
**When to use**: When interviewers want concrete, recent evidence of shipping, quality discipline, and governance.

### COMMIT-STAR 1: Built integrity layer for trust at scale
**Commit**: `358628d`
- **Situation**: Data and routing layers were growing, but trust was low because consistency wasn't provable.
- **Task**: Build a structural integrity system that validates cross-layer correctness.
- **Action**: Implemented a cross-layer integrity engine to check taxonomy, routing, recipes, knowledge, and signals together.
- **Result**: Created a repeatable trust gate that turned ad hoc validation into systematic validation.

### COMMIT-STAR 2: Added drift/regression controls
**Commit**: `78785f4`
- **Situation**: System quality could degrade over time via naming drift and ambiguous matching.
- **Task**: Add operational controls so quality stayed stable after launch.
- **Action**: Added override registry, terminology drift detection, and regression/SLO monitoring.
- **Result**: Moved from one-time audit to continuous quality enforcement.

### COMMIT-STAR 3: Closed a real data-link failure
**Commit**: `1e50914`
- **Situation**: Audit exposed broken service-to-recipe linkage that could cause wrong routing outcomes.
- **Task**: Fix the broken link and improve audit execution cadence.
- **Action**: Corrected routing linkage; added audit artifacts and batch execution scripts.
- **Result**: Restored routing integrity and improved repeatability of audits.

### COMMIT-STAR 4: Completed integration coverage
**Commit**: `9a3721e`
- **Situation**: High-value workflows were blocked by missing integration recipes.
- **Task**: Close coverage gaps fast enough to make audits actionable.
- **Action**: Added/updated a large set of integration recipes and normalized service coverage.
- **Result**: Raised practical completeness, enabling more RIUs to resolve to usable actions.

### COMMIT-STAR 5: Finished tail-end defects
**Commit**: `0e0847d`
- **Situation**: Main architecture was in place, but edge-case integrity failures remained.
- **Task**: Remove remaining audit blockers without destabilizing the system.
- **Action**: Fixed final audit issues in both engine logic and supporting knowledge mappings.
- **Result**: Tightened reliability and reduced risk of post-launch surprises.

### COMMIT-STAR 6: Defined explicit decision policy
**Commit**: `3e311b8`
- **Situation**: Teams needed consistent go/no-go behavior when risk was present.
- **Task**: Encode clear decision semantics and enforce them operationally.
- **Action**: Added Para decision contract (ship / ship_with_risks / block), architecture docs, and test hardening.
- **Result**: Improved decision consistency and auditability across workflows.

### COMMIT-STAR 7: Reduced system friction
**Commit**: `d4ee09c`
- **Situation**: Scattered docs/scripts increased onboarding and maintenance cost.
- **Task**: Improve maintainability without breaking active flows.
- **Action**: Reorganized core docs, normalized script paths, and decluttered root structure.
- **Result**: Faster navigation, clearer ownership boundaries, and easier contributor ramp-up.

### COMMIT-STAR 8: Improved executive communication layer
**Commit**: `4223168`
- **Situation**: Technical progress existed, but messaging wasn't aligned for stakeholders.
- **Task**: Present system capability in a way decision-makers can quickly evaluate.
- **Action**: Rewrote README with up-to-date metrics and clearer value framing.
- **Result**: Better narrative clarity for interviews, demos, and stakeholder alignment.

---

## BEHAVIORAL ROUTING TABLE

Use this to quickly find the right story for a given question type:

| Question Pattern | Primary Story | Backup Story |
|---|---|---|
| "Tell me about yourself" | STORY 1 (Pathfinder) | STORY 7 (Multilingual) |
| "Technical depth" | STORY 2 (POI Graph) | STORY 8 (Palette) extended |
| "Design decision" | STORY 4 (Taxonomy) | STORY 2 (Entity Resolution) |
| "Executive audience" | STORY 3 (Forum) | STORY 5 (Partner) |
| "Low adoption" | STORY 10 (Rescue) | STORY 1 (Pathfinder) |
| "Cross-functional conflict" | STORY 1 (Pathfinder) | STORY 2 (POI Graph) |
| "AI evaluation / quality" | STORY 6 (Attribution) | STORY 9 (MCP Verification) |
| "Why this company?" | STORY 5 (Partner) | STORY 7 (Multilingual) |
| "Recent hands-on work" | STORY 9 (MCP) | COMMIT-STARs 1-3 |
| "Failure / setback" | STORY 10 (Rescue) | STORY 2 (Italy launch) |
| "Influence without authority" | STORY 1 (Pathfinder) | STORY 3 (Forum) |
| "Builder credibility" | STORY 8 (Palette) | COMMIT-STARs |
| "Background / what makes you different" | STORY 7 (Multilingual) | STORY 1 (Pathfinder) |
| "Governance / safety" | STORY 8 (Palette) extended | STORY 9 (MCP) |
| "Scaling knowledge" | STORY 4 (Taxonomy) | STORY 2 (POI Graph) |

---

## 30-SECOND META ANSWERS

**"What do your stories show?"**
They show my operating style: diagnose before building, structure knowledge for machines and humans, unify competing teams with evidence, and measure behavior change — not activity.

**"What do your commits show?"**
They show how I ship: build trust infrastructure first, instrument drift and regression, fix real defects quickly, encode clear decision policy, and keep the system understandable to both builders and business stakeholders.

**"What's the thread across your career?"**
The same problem keeps appearing: unstructured knowledge that machines and humans both need to navigate. I've been solving it for 15 years — from multilingual lexicons to knowledge graphs to AI routing systems. The tools changed. The problem didn't.

---

*Source files: experience-inventory.yaml, BEHAVIORAL_STORIES.md (Mistral), COMMIT_BASED_STAR_ANSWERS (Lumen), OPENAI_ONSITE_MASTER_QA.md*
