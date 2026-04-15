---
id: SKILL-TAL-003
name: "Talent Skill — Unified Methodology"
domain: Talent
for_agents: [Researcher, Architect, Narrator, Validator, Builder]
status: WORKING
validated_on: "OpenAI ADM, Perplexity CSM/FDE, Glean (post-mortem), Gap Inc, Mistral TME, Anthropic, iBusiness, FriendliAI, Claudia Canu Fautré (UNESCO P-4, Babbel, Duolingo, IBO)"
supersedes: [SKILL-TAL-001, SKILL-TAL-002]
---

# Talent Skill — Unified Methodology

End-to-end system from opportunity discovery to offer — all organized through **role profiles**. Every phase inherits from `profile_id`. Learnings compound: each interview for a profile type makes the next one better. Consolidates learnings from 18 implementations and 8+ real applications.

## Quick Start

When a new role comes in:
0. **Classify** (2 min) → assign `profile_id` from `role-profiles.yaml` → Phase 0
1. **Score fit** (5 min) → use profile's `fit_lens` → Phase 1
2. **Build resume** (15 min) → `build_resume.py --profile <profile_id>` → Phase 2
3. **Write application** (30 min) → query inventory using profile's `lead_eras` → Phase 3
4. **Prep for interview** (2-8 hours) → use profile's `interview_playbook` + `accumulated_learnings` → Phase 4
5. **Day-of review** (30 min) → fill glance sheet with profile's `anchor_messages` → Phase 5
6. **Post-mortem** (15 min) → feed learnings back into profile → Phase 6

## Source Data

Five source files work together:
- **`experience-inventory.yaml`** — structured career data (ERAs, stats, stories). Never write from scratch — query the inventory.
- **`role-profiles.yaml`** — 6 role profiles with search patterns, fit lenses, interview playbooks, and accumulated learnings.
- **`STAR_STORIES.md`** — 10 behavioral stories with 90-second and extended versions, plus a routing table mapping question types to stories.
- **`ANSWER_BACKBONE.md`** — topic-indexed experience library for building cheatsheet answers. Organized by interview topic (SQL, dashboards, AI agents, etc.), each with multiple experiences and verified numbers. Use this to assign different experiences to different cheatsheet sections — never reuse the same story in two sections. Built from the inventory and stories above.
- **`build_resume.py`** — parameterized resume builder. Each profile selects different headline, summary, bullet variants, and Palette framing.

Additional local source layer for job-search strategy:
- **`/home/mical/fde/implementations/talent/nsa/index.yaml`** — query map into the local Never Search Alone corpus
- **`/home/mical/fde/implementations/talent/nsa/CMF_SYNTHESIS_2026-04-03.md`** — Mical's current candidate-market-fit thesis
- **`/home/mical/fde/implementations/talent/nsa/MNOOKIN_TWO_PAGER_MICAL.md`** — Mical's wants / anti-wants / self-discovery

## NSA Pre-Filter

Before investing in a role, check whether it fits the local NSA evidence:
1. Does it align with the current CMF zones?
2. Does it avoid the anti-target environments identified in the CMF synthesis?
3. Is the narrative consistent with the Mnookin two-pager, or is it another one-off story?
4. If not, stop before resume tailoring and re-evaluate the target.

## Role Profiles

Every opportunity gets a `profile_id` before any work starts. The profile drives everything downstream.

| Profile ID | Display Name | Lead ERA | Example Companies |
|---|---|---|---|
| `forward_deployed_engineer` | Forward Deployed Engineer | ERA-2 + ERA-4 | Perplexity, Google Cloud, Dust, FriendliAI |
| `enablement_strategy` | Enablement Strategy & Adoption | ERA-4 | Gap, TaskRabbit, Databricks |
| `enablement_systems_builder` | Enablement Systems Builder | ERA-4 | Mistral, Lenovo, Cognition, Anthropic Education, LangChain |
| `customer_success_ai` | Customer Success & AI Deployment | ERA-4 + ERA-3 | OpenAI, Glean, Perplexity CSM |
| `knowledge_data_engineer` | Knowledge & Data Engineer | ERA-2 | iBusiness, Gusto, Airbnb, Leonardo SpA |
| `certification_architect` | Certification & Education Architect | ERA-4 + ERA-5 | Anthropic |

---

## Phase 0: Discovery & Classification (ongoing)

### Weekly Sweep
Run a market sweep weekly. For each opportunity:
1. Match against `role-profiles.yaml > profiles > [profile] > search_patterns`
2. Assign `profile_id`
3. Score fit using the profile's `fit_lens` (Phase 1)
4. Add to pipeline tracker with profile, fit tier, and deadline

### Search Patterns
Each profile defines `titles` and `keywords` to search for. EU opportunities use the `eu_search` section.

### Company Signals Cross-Reference (NEW)
Every sweep MUST cross-reference Palette's company intelligence:

**Source**: `buy-vs-build/people-library/v1.1/people_library_company_signals_v1.1.yaml` (43 tracked tools/companies)

**Why**: These are companies Palette already has deep intelligence on — funding stage, product positioning, signal tier, People Library connections. Applying to a tracked company means you can speak to their product, competitive position, and market signal with specificity no other candidate has.

**Sweep step**: For each company in the signals file:
1. Check their careers page for roles matching any `role-profiles.yaml` search pattern
2. Flag any role at a Tier 1 signal company (Anthropic, Lovable, Gamma, Wispr, Cursor, Perplexity, NotebookLM/Google) as priority
3. Note the Palette context advantage in the pipeline tracker (e.g., "tracked in People Library — Anton Osika cluster", "integrated in Palette routing", "service routing covers their product")
4. For People Library connections (21 profiles), check if the person is a hiring manager or can be a warm intro

**Company list** (33 unique companies, grouped by Palette context):
- **Integrated**: Anthropic (Claude), Perplexity, Gamma
- **Evaluated/Tracked**: Lovable, Cursor, Vercel, Wispr Flow, NotebookLM (Google)
- **Monitored**: Runway AI, Superhuman, Leonardo AI, xAI, Julius AI, Granola, HappyRobot, Krea, Higgsfield AI, OpenAI (Sora), Google DeepMind, Canva, Opus Clip, Easygen, Topaz Labs, Epidemic Sound, Overlap, Happenstance, Willow, Genre.ai, Freepik, ByteDance (Seedance/CapCut), Kuaishou (Kling)

### Pipeline Tracker
Every opportunity gets one row:
```
| Company | Role | profile_id | Fit Score | Tier | Status | Deadline | Palette Context | Next Action |
```

### Validated Pattern
- Sweep weekly, apply daily for Tier 1
- EU opportunities are tracked separately with language advantage notes
- New role types that don't fit existing profiles → evaluate whether to create a new profile
- Company signals companies get priority review — deep context is a competitive advantage

---

## Phase 1: Fit Assessment (5 min)

Use the profile's `fit_lens` from `role-profiles.yaml`. Score every explicit requirement 0-100 against evidence in the experience inventory. **Output must include `profile_id`.**

| Score | Action |
|-------|--------|
| 85-100 (Tier 1) | Full prep, lead with strongest match |
| 75-84 (Tier 2) | Apply, targeted prep on gaps |
| 65-74 (Tier 3) | Apply only if warm lead or unique angle |
| <65 | Pass |

### Scoring Rules
- Map each requirement to a specific ERA, system, or metric from the inventory
- Requirements with no evidence = 0 for that dimension
- Identify the **killer differentiator** — what no other candidate can claim
- Identify the **biggest gap** — be honest about what you'd need to learn
- Calculate weighted average (must-haves weighted 2x vs nice-to-haves)

### Validated Pattern (Glean Learnings)
Research depth scales with domain familiarity:
- **Unfamiliar domain** (e.g., retail at Gap): 8+ docs, 150KB, deep research
- **Familiar domain** (e.g., AI SaaS at Glean): 5 docs, 80KB, streamlined
- Don't over-research familiar domains. Invest research time where knowledge gaps exist.

### Multi-Method Validation (Career-Ops + UNESCO Learnings)
For high-stakes or ambiguous-fit roles, run the score through multiple methods and look for consensus:
1. **Palette fit lens** (profile-specific weighted scoring)
2. **6-Block Deep Evaluation** (JD line-by-line gap analysis, level check, comp research — see `job-search-command.md`)
3. **Reviewer Lens** (simulate the actual evaluator's perspective — what vocabulary do they expect? what screening criteria do they use?)

If all three agree on PASS — don't apply, even if it's emotionally appealing. If they disagree, investigate why. The most pessimistic score is usually the most honest.

**Structural factors** that can't be fixed by application quality:
- Geographic quotas (UN system)
- Internal candidate preference (many orgs fill 60%+ internally)
- Hard-gate requirements (e.g., "7 years in X" where you have 0)
- Seniority mismatch

**Validated on UNESCO P-4 (April 2026)**: Three methods scored 64-72. All agreed: reach application. The candidate's instinct to doubt was correct. The right move: submit (materials already built, low marginal cost) but redirect primary energy to higher-fit roles (Babbel 8/10, IBO 9/10 when open). The problem wasn't the candidate — it was the specific role's requirements vs. her actual strengths.

---

## Phase 2: Resume Generation (15 min)

### Process
1. Identify role type from `experience-inventory.yaml > positioning` profiles
2. Select headline, summary frame, and emphasis areas
3. Pull era bullets matching the role type (each era has role-specific bullet variants)
4. Select Palette framing (knowledge engineer vs enablement vs TME)
5. Run `build_resume.py` with the assembled content
6. Stat-check: every number must be GREEN or YELLOW (see inventory stats section)

### Role Positioning (Validated)
The same career, framed differently:
- **Knowledge/Data Engineer**: Lead with POI Knowledge Graph + data pipelines. Palette = knowledge graph + retrieval
- **Certification/Enablement Architect**: Lead with Ask Pathfinder + enablement metrics. Palette = curriculum + assessment
- **Technical Marketing Engineer**: Lead with Ask Pathfinder as knowledge-to-adoption translation. Palette = use sparingly
- **Forward Deployed Engineer**: Lead with Ask Pathfinder + customer delivery. Palette = builder credibility

### Validated Pattern (Glean Learnings)
**Enabler vs Executor positioning**: Same proof points (Palette, Ask Pathfinder) work for both strategic roles (governance, adoption) and tactical roles (build, ship). Only the framing changes. Proof points are reusable assets.

---

## Phase 3: Application Narrative (30 min)

### Answer Construction Protocol
1. Read the question carefully — what are they actually asking?
2. Query `experience-inventory.yaml` for the best-fit ERA and system
3. **Lead with the strongest system match**, not the most recent work
4. Structure: System → Problem → What I did → Outcome → Connection to their role
5. Each answer should feature a DIFFERENT era (no repetition across answers)

### Narrative Rules (Validated)
- **Thesis-first**: Open with the company's problem, not your resume
- **Evidence hierarchy**: GREEN stats > YELLOW stats > qualitative claims
- **Activation framing**: "I drive adoption" not "I manage accounts"
- **Counter-intuitive specificity**: "I would NOT do X" is more memorable than "I would do Y"
- **Finance POD pattern**: "Find one team, prove the win, let success create pull"
- **Three-level measurement**: Usage → behavior shift → business outcomes
- **Honest about tradeoffs**: Every approach has problems you encountered and solved

### Question-to-ERA Routing

| Question Type | Best Lead ERA | Why |
|---|---|---|
| "Walk me through a system..." | ERA-2 (Alexa POI Graph) | Biggest scale, full pipeline story |
| "Retrieval/indexing approach..." | ERA-2 + ERA-4 + ERA-5 | Three different approaches, shows range |
| "LLM enrichment / RAG..." | ERA-3 (AGI) + ERA-5 (Palette) | Hallucination detection + RAG pipeline |
| "Training data operations..." | ERA-2 + ERA-3 | Annotation teams, RL loops |
| "Knowledge graphs / ontologies..." | ERA-2 (POI) + ERA-5 (Palette) | 25B nodes, 2,013 quads |
| "Scale / distributed systems..." | ERA-2 (Spark, 47 sources) | Production scale evidence |
| "Adoption / enablement..." | ERA-4 (Ask Pathfinder) | 12K users, measurable impact |
| "Leadership / executive..." | ERA-4 (Data Forum) | 291 leaders, 98 CxOs |
| "Why this company?" | Research-dependent | Use company-specific framing |

---

## Phase 4: Interview Preparation (2-8 hours)

### Profile-Driven Prep
Before building materials, read `role-profiles.yaml > [profile_id] > interview_playbook` and `accumulated_learnings`. The playbook defines which documents to build, anchor messages to internalize, and common questions with ERA routing. The accumulated learnings are hard-won patterns from previous interviews of this type — they compound over time.

### Modular Materials (Validated Pattern)
Build 5-6 focused documents, NOT 1-2 monolithic ones (Glean learning: modular > monolithic).

| Document | Purpose | Time |
|---|---|---|
| **Fit Analysis** | Score each requirement, identify gaps | 30 min |
| **Company Research Brief** | Product, market, competitive, culture | 30-60 min |
| **Interview Cheatsheet** | Actual spoken answers — dense paragraphs per topic (see CHEATSHEET.md format in `job-search-command.md`) | 30 min |
| **Company Prep** | Coaching context: what they're testing, risks, mitigations, questions to ask (COMPANY_PREP.md) | 15 min |
| **Behavioral Stories** | 5-7 stories from story bank, tailored to role | 30 min |
| **Simulation Drills** | 4 rounds of practice scenarios | 60-120 min |
| **Day-of Protocol** | Energy management, anchor messages, pivots | 15 min |

### Experience Assignment (before writing Cheatsheet + Company Prep)
Before writing any answers, build an internal assignment table using `ANSWER_BACKBONE.md`:
1. List the major topics from the JD
2. For each topic, pick the strongest experience from ANSWER_BACKBONE.md
3. Once assigned, that experience is off-limits for other sections
4. Verify: no experience appears in two sections

This step is what prevents double-dipping (e.g., the same Foursquare/TripAdvisor story appearing in both SQL and Dashboards). The cheatsheet and company prep are always generated as a pair — cheatsheet has the spoken answers, company prep has the coaching context.

### Story Bank Protocol
1. Select 5-7 stories from `experience-inventory.yaml > stories` matching the role
2. For each story, verify all stats are GREEN
3. Rehearse at 90 seconds each — time yourself
4. Map each story to 2-3 likely questions
5. Prepare one "extended version" for the lead story (if asked for depth)

### Simulation Drill Protocol (4 rounds)
From Gap interview prep (most rigorous):

**Round 1: Core Strategy** (20 min)
- "Tell me about yourself" → Lead story
- "Why this company?" → Thesis-first
- "Walk me through a system you built" → Best ERA match

**Round 2: Execution & Adoption** (20 min)
- "How would you approach [specific scenario]?" → Framework answer
- "Give me an example of driving adoption" → Metrics story
- "How do you measure success?" → Three-level measurement

**Round 3: Technical Depth** (20 min)
- "Explain [technical concept] to me" → Simple first, then add layers
- "What was the hardest design decision?" → Tradeoff answer
- "How would you apply this here?" → Map to their context

**Round 4: Edge Cases & Culture** (20 min)
- "Tell me about a failure" → What you learned, not excuses
- "How do you handle disagreement?" → Neutral evidence story (Ask Pathfinder teams)
- "Questions for us?" → 3-5 prepared, at least 1 showing product knowledge

### Answer Shape (Validated)
Every answer follows: **Principle → Application → Metric/Signal → Tradeoff/Risk**

### Interviewer Lens (from Gap prep)
When you know the interviewer, build a YAML lens:
```yaml
interviewer:
  name: "..."
  role: "..."
  philosophy: "..."  # from LinkedIn, talks, blog posts
  likely_priorities: [...]
  answer_shape_preferences: "..."
```

### Product Demonstration (Validated)
For product companies, show you USE the product:
- Build something on it (API, workflow, analysis)
- Reference with technical specificity
- Choose optional exercises showing product fluency
- Meta-demonstration: use the product to advocate for itself (Perplexity pattern)

---

## Phase 5: Day-of Protocol (30 min before)

### One-Page Glance Sheet
Fill in before every interview:

```
ROLE: ___
INTERVIEWER: ___
MY THESIS: [One sentence — their problem, my solution]

TOP 3 NUMBERS:
1. ___
2. ___
3. ___

LEAD STORY: [Which story, 90-sec version]
PIVOT STORY: [Backup if conversation shifts]

KILLER DIFFERENTIATOR: ___
BIGGEST GAP: ___ (and how I'd address it)

3 QUESTIONS TO ASK:
1. ___
2. ___
3. ___

ENERGY ANCHORS:
- I built real systems at real scale
- My background in comparative linguistics IS the differentiator
- Evidence-based, honest about tradeoffs
```

### 30-Second Pivots
If the conversation goes off-script, these pivots bring it back:
- "That connects to something I built..." → bridge to lead story
- "The way I'd think about that..." → bridge to framework answer
- "What I've seen work in practice..." → bridge to evidence

---

## Phase 6: Post-Mortem (15 min after)

After every interview (pass or fail), capture AND update the profile:

```markdown
# Post-Mortem: [Company] [Role]
# profile_id: ___

## What worked
- ...

## What didn't work
- ...

## Questions I wasn't prepared for
- ...

## Patterns to extract → ADD TO role-profiles.yaml > [profile_id] > accumulated_learnings
- ...

## Anti-patterns to record → ADD TO role-profiles.yaml > [profile_id] > anti_patterns
- ...

## Updates to experience inventory
- New stat verified: ...
- New story validated: ...
- Positioning adjustment: ...
```

### Learnings Feedback Loop
**This is what makes the system compound.** After every post-mortem:
1. Add new patterns to `role-profiles.yaml > [profile_id] > accumulated_learnings > patterns`
2. Add new anti-patterns to `accumulated_learnings > anti_patterns`
3. Update `common_questions` if new question types appeared
4. Update `anchor_messages` if better framing was discovered
5. Update `story_bank` mapping if a different story worked better
6. If the profile's `advance_bar` was too low or high, adjust it

The next interview for this profile type starts with ALL previous learnings loaded.

### Failure Patterns (Validated — Glean Post-Mortem)
- Didn't know their internal system — product depth matters more than generic prep
- Generic transformation language — specifics win
- Didn't study company blog/engineering posts — non-negotiable
- Didn't know hiring manager's philosophy — research LinkedIn, talks, blog posts

---

## Takehome Execution (Compressed)

For high-stakes timed assignments, use the takehome protocol:

### Default Shape
Executive summary → Governing thesis → Main recommendation with tradeoffs → Technical workflow → Evaluation plan → Rollout plan → Next steps → Assumptions

### Time Budget
- **<6 hours**: Compressed mode — merge research/architecture, start building by hour 2
- **6-24 hours**: Full mode — research → architecture → build → review
- **>24 hours**: Full mode + iteration — build draft, sleep, review fresh

### Quality Checks
- Exact prompt coverage with customer reality
- Technical credibility with explicit tradeoffs
- Reviewer-friendly structure (make grading easy)
- Clear governing thesis naming core tension
- Runnable artifacts where possible

---

## Quality Gates (All Phases)

- [ ] No fabricated claims — verify every claim against real code/data
- [ ] All stats GREEN or YELLOW (check inventory)
- [ ] Resume matches narrative matches interview answers (same numbers, same framing)
- [ ] Product demonstration is verifiable
- [ ] Answers sound like the candidate, not like AI wrote them
- [ ] Each answer features a different ERA — no repetition
- [ ] Honest about gaps — score them, name them, explain how you'd close them
