---
id: SKILL-TAL-005
name: Enablement Assessment Execution
domain: Talent
for_agents: [Architect, Builder, Validator, Narrator, Researcher]
triggers: [RIU-001, RIU-014, RIU-020, RIU-062]
impressions: 0
status: UNVALIDATED
validated_on: pending
parent: SKILL-INT-001
specializes: openai-takehome-execution.md
last_updated: 2026-04-20
revision: 15
revision_notes: "Kiro 15-iteration refinement — quick classifier, knowledge map template, instrumentation examples, fill checklist, grader empathy gate, defense Q7-Q8, rehearsal method, submission packaging, compressed time budget, swap test, artifact signal table, post-submission protocol"
---

# Enablement Assessment Execution

Specialized execution skill for technical enablement interview assessments — take-homes, case studies, system design exercises, role-plays. Inherits the generic takehome protocol from `openai-takehome-execution.md` and adds enablement-specific module library, classification, and artifact patterns.

The parent skill handles generic assessment structure (thesis, shape selection, defense rehearsal, compressed mode). This skill handles what to build and how to assemble it when the domain is enablement.

## When to Use

The assessment prompt involves any of: designing enablement programs, creating enablement materials for a product change, diagnosing adoption failures, prioritizing enablement motions, auditing existing enablement, or role-playing as an enablement lead. If the prompt is a generic case study or deployment plan with no enablement angle, use the parent skill instead.

**Do NOT use this skill for**: pure engineering take-homes (system design + coding), product management exercises, sales strategy assessments, or general business case studies. Those have different grader lenses and different artifact expectations.

## Assessment Family Classification

Read the prompt. Classify within 15 minutes. The family determines the response shape and which modules to load.

### Quick Classification (under 60 seconds)
Ask one question: **What is the prompt asking me to CREATE?**
- A system/program → Family 1
- Materials for a specific product change → Family 2
- A diagnosis of what went wrong → Family 3
- A prioritized plan with tradeoffs → Family 4
- A critique of something that exists → Family 5
- A live performance of how I'd operate → Family 6
- None of the above → Family 0

### Family 1: System Design (most common)
**Trigger phrases**: "Design a program", "Build an onboarding/everboarding system", "Create a learning path", "How would you structure enablement for..."
**Response shape**: Architecture blueprint + role-specific paths + measurement framework + one concrete artifact.
**Modules**: A + B + C + D
**Grader lens**: Can this person design a system, not just describe one?

### Family 2: Product-to-Enablement Translation
**Trigger phrases**: "Here's a new feature, create enablement materials", "This launched last week, what do the field teams need?", "Translate this release into training."
**Response shape**: Audience analysis + tiered content plan + one fully-built deliverable + rollout sequence.
**Modules**: B + C + D + E
**Grader lens**: Can this person turn complexity into field-ready output fast?

### Family 3: Diagnosis and Fix
**Trigger phrases**: "Adoption stalled", "Implementations are failing", "Escalations spiked", "What's broken?"
**Response shape**: Root cause analysis + evidence-based diagnosis + fix proposal + measurement plan to verify the fix worked.
**Modules**: B + C + D
**Grader lens**: Can this person diagnose without hand-waving? Do they measure the fix?

### Family 4: Prioritization / Strategy
**Trigger phrases**: "You can only build one motion", "What would you do first?", "Given limited resources...", "First 90 days."
**Response shape**: Decision framework + recommendation with explicit tradeoffs + what you'd cut and why + measurement criteria for the bet.
**Modules**: A + C
**Grader lens**: Does this person make real tradeoffs or try to do everything?

### Family 5: Audit / Critique
**Trigger phrases**: "Here's our existing enablement", "What would you change?", "Review this program."
**Response shape**: Structured assessment against enablement principles + severity-ranked findings + concrete fixes + measurement plan.
**Modules**: A + C + D
**Grader lens**: Can this person see structural problems, not just cosmetic ones?

### Family 6: Role-Play / Walk-Through
**Trigger phrases**: "Walk us through your first 90 days", "Role-play: you're the enablement lead", "Present as if you're already on the team."
**Response shape**: Phased action plan with discovery/build/scale arcs + explicit what-I'd-learn-before-deciding gates + collaborative framing.
**Modules**: A + B + C
**Grader lens**: Does this person listen before prescribing? Can they think on their feet?

### Family Overlap Rule
When families overlap (e.g., "walk us through your first 90 days" is both Family 4 prioritization AND Family 6 role-play), use the higher-numbered family's response shape (more interactive) but pull modules from both.

### Family 0: Unclassified
If the prompt doesn't match any family, fall back to the parent skill's generic takehome protocol. Use the enablement module library where applicable but don't force the classification.

## Module Library

Self-contained, domain-portable components. Each module works for any enablement company — fill in the company-specific product surface, role names, and business metrics at assembly time.

### Module A: Enablement System Architecture
The structural backbone. Three layers that every enablement system needs:

**Layer 1 — Onboarding**: Time-to-productive for new hires. Role-specific tracks (not one path fits all). Progressive depth: vocabulary → concepts → application → independent operation. Milestone gates, not calendar gates.

**Layer 2 — Everboarding**: How the field stays current as the product evolves. Product-change-to-enablement pipeline with defined SLAs. Content lifecycle: draft → technical review → role adaptation → field release → usage measurement → retirement. Frequency cadence matched to product release velocity.

**Layer 3 — Measurement**: Covered in Module C. The architecture must include measurement as a layer, not an afterthought.

**Role-specific paths**: Every enablement system must distinguish audiences. Common enablement roles: Solutions Architects/Engineers (deep technical), Customer Success/Outcomes (value realization + adoption), Support (troubleshooting + escalation), Partners (subset of SA track, external-facing). Map each role to the depth they need per product domain. A knowledge map (Module B) drives this.

**Content engine pattern**: Spec (what to teach) → Template (how to teach it) → Creator mode (how to produce it at scale). This separates curriculum design from content production. Example: Spec says "SAs must explain connector permissions to CISOs." Template defines the format: 5-minute talk track + one-pager + objection guide. Creator mode: any enablement team member can produce a new connector guide by filling the template — no curriculum designer needed per artifact.

### Module B: Role-Specific Knowledge Map
A matrix of technical domains × roles × required depth. This is the enablement curriculum in compressed form.

Build the map from the company's product surface area. For each technical domain, define what each role needs to know and at what depth (configure, explain to customers, troubleshoot, architect solutions). The map makes role-specificity concrete — it's the difference between "we'll train the field" and "SAs need to configure connectors; CSMs need to explain the value; Support needs to debug sync failures."

**Template** (fill at assembly time):

| Technical Domain | SA Depth | CSM/AIOM Depth | Support Depth | Partner Depth |
|-----------------|----------|----------------|---------------|---------------|
| [Domain 1] | configure + explain | explain + value story | troubleshoot | explain (subset) |
| [Domain 2] | ... | ... | ... | ... |

Depth levels: **aware** (knows it exists) → **explain** (can describe to customer) → **configure** (can set up) → **troubleshoot** (can diagnose failures) → **architect** (can design solutions using it)

The knowledge map also reveals coverage gaps: domains where no enablement exists yet, roles that are under-served, and depth mismatches (e.g., Support is trained at explain-depth but needs troubleshoot-depth).

### Module C: Measurement Framework
Three layers, each necessary but insufficient alone:

| Layer | Measures | Proves |
|-------|----------|--------|
| **Activity** | Content views, session attendance, completion rates, tool adoption | People showed up (necessary, not sufficient) |
| **Behavior** | Time-to-ramp, repeat-question reduction, escalation deflection, field confidence scores, content retrieval patterns | Enablement changed what people DO |
| **Outcome** | Business metrics: churn reduction, expansion rate, time-to-value, NPS, implementation velocity | Enablement connects to business results |

The key insight: most enablement orgs stop at activity metrics. The measurement framework must bridge to behavior and outcome. Include the instrumentation plan — how you'd actually collect each metric, not just name it.

**Instrumentation examples** (adapt to company):
- Activity: LMS completion data, content view analytics, session attendance logs
- Behavior: support ticket analysis (repeat-question rate), field confidence surveys (quarterly), time-from-hire-to-first-solo-customer-call, content retrieval patterns from internal search
- Outcome: correlate enablement cohorts with deal velocity, churn rate by SA tenure, expansion attach rate by team, implementation time-to-value by quarter

### Module D: Day-1 Artifacts
The submission must include at least one concrete deliverable that demonstrates what enablement output actually looks like. Not a plan for an artifact — the artifact itself.

**Artifact patterns** (choose based on the company's domain):
- **Readiness Guide**: Role-specific guide for a technical topic. Dense spoken paragraph + visual one-pager + decision tree. Format: HTML or Markdown, scannable in 2 minutes.
- **Troubleshooting Decision Tree**: "When X happens, check Y, then Z." Interactive or static. Shows you understand the product's failure modes.
- **Product-Change Enablement Package**: A complete package for one feature: what changed, who cares, what to say, what to demo, what to watch for. Shows the pipeline in action.
- **Onboarding Checkpoint**: One milestone from an onboarding track with assessment criteria, practice exercise, and pass/fail rubric.
- **Coaching Rubric**: Structured scoring tool for managers to evaluate field readiness on a specific skill.

**The "application IS the proof" pattern**: The artifact itself demonstrates the enablement capability. An SA Readiness Guide that is well-structured, technically accurate, and field-ready IS the proof that you can build enablement systems. The artifact does double duty: submission content AND capability demonstration.

**Artifact-to-family mapping** (default selection, override with judgment):
| Family | Best artifact pattern |
|--------|----------------------|
| F1 (System Design) | Readiness Guide or Onboarding Checkpoint |
| F2 (Product Translation) | Product-Change Enablement Package |
| F3 (Diagnosis) | Troubleshooting Decision Tree |
| F4 (Prioritization) | Coaching Rubric |
| F5 (Audit) | Matched to the weakest finding |
| F6 (Role-Play) | Skip artifact — focus on live demonstration |

**1 vs 2 artifacts rule**: Default to 1. Only build 2 if (a) time budget allows AND (b) the second demonstrates a different capability than the first. Two similar artifacts = wasted time.

### Module E: Interactive/Demo Component
A working tool that shows enablement thinking in action. HTML preferred (single-file, no dependencies, opens in a browser).

**Patterns**:
- Pipeline simulator: product change → audience analysis → content plan → deliverable
- Knowledge assessment tool: quiz format that demonstrates progressive depth
- Readiness dashboard mockup: what the measurement framework would look like in production
- Role-specific drill tool: timed practice with scoring

The Sierra voice workbench and Stripe invisible-learning-system are reference implementations. The tool should be functional, not decorative — a reviewer should be able to use it, not just look at it.

## Execution Protocol

### Phase 0: Classify (15 minutes)
1. Read the prompt twice. Identify the assessment family.
2. Map to modules. Note which modules apply and which to skip.
3. Identify the company-specific fill: product domains, role names, business metrics.
   - Product domains: list the 4-6 technical areas the field must know (e.g., connectors, graph, agents, governance)
   - Role names: what does this company call its post-sales roles? (SA, CSM, AIOM, Support, Partner)
   - Business metrics: what does the company measure? (churn, expansion, NRR, time-to-value, CSAT)
   - Product stage: is this a new product area (need onboarding) or evolving area (need everboarding)?
4. Set a time budget. Default: 6-8 hours total. Adjust based on stated constraints.

### Phase 1: Architecture (1 hour)
1. Draft the response structure: thesis → system design → role-specific detail → measurement → artifact.
2. Write the thesis. One sentence: what enablement must do for THIS company at THIS stage. Name the central tension. **Swap test**: replace the company name with a competitor. If the thesis still works, it's too generic — rewrite until it's specific to this company's product stage, org structure, or strategic moment.
3. Select which Day-1 artifact(s) to build. Choose the artifact that best demonstrates the thesis.
4. Check every section against "so what?" — if a section doesn't help the grader decide yes/no, cut it.

### Phase 2: Build (3-4 hours)
1. Write the system design using Module A as backbone. Fill with company-specific product depth from Module B.
2. Build 1-2 Day-1 artifacts (Module D). These take the most time and have the most impact.
3. Add the measurement framework (Module C) — connect every metric to the company's business outcomes.
4. If applicable, build the interactive component (Module E).
5. Add the "why me" bridge: connect personal evidence to the system you designed. Scale numbers, behavior-change proof, prior art.

### Phase 3: Quality Gate (1 hour)
- [ ] **Requirement coverage**: Every explicit requirement in the prompt is addressed.
- [ ] **Product depth**: Would an insider say "this person knows our product"?
- [ ] **Role specificity**: Are distinct audiences treated distinctly, not generically?
- [ ] **Measurement**: Is there a KPI framework tied to the company's business metrics?
- [ ] **Concrete artifacts**: At least one thing that IS enablement output, not a plan for it.
- [ ] **Thesis present**: The central tension is named and the system resolves it.
- [ ] **60-second test**: The core idea is explainable in 60 seconds.
- [ ] **Adversarial questions**: The 3 most likely pushback points are pre-answered or acknowledged.
- [ ] **Grader empathy**: Can the grader assess this in under 15 minutes? Is there a clear executive summary at the top? Are artifacts clearly labeled and immediately openable?

### Phase 4: Walk-Through Prep (1 hour)
Build three versions:

**60-second version**: "Here's the problem, here's my system, here's the proof it works." For when they say "give us the overview."

**5-minute version**: Thesis → strongest artifact → system architecture → measurement → what I'd do next. For a structured presentation slot.

**15-minute version**: Full walk-through with 3 collaborative decision points. "I chose X over Y because Z — what do you think?" Leave 5 minutes for discussion.

**30+ minute slots**: Expand the collaborative section, not the presentation. Co-builder interviewers want discussion time, not longer slides. If the slot is 30 minutes, use 12-15 for presentation and 15-18 for collaborative discussion.

**Time budget template** (adjust to actual slot):
- 0:00-2:00 — "Here's what I built and why" (thesis + artifact lead)
- 2:00-7:00 — Walk through the system (strongest piece first, not chronological)
- 7:00-10:00 — Measurement and evidence
- 10:00-12:00 — What I'd do differently with more time / what I'd learn first
- 12:00-15:00 — "Three things I'd love your input on" (collaborative)

## Defense Protocol

### Prepare for these questions:
1. "How would you measure whether this actually works?" → Module C, outcome layer.
2. "This is ambitious — what would you cut if you had half the time?" → Name the cut. Don't hedge.
3. "How does this scale beyond the first team?" → Content engine pattern from Module A.
4. "What assumptions are you making that could be wrong?" → Name 2-3. Show how you'd validate.
5. "How is this different from what we already have?" → This requires product research. If unknown, say "I'd need to understand your current state — here's what I'd look for in the first two weeks."
6. "Walk me through the artifact you built." → Know it cold. Every design decision, every tradeoff.
7. "How is this different from just building a training library?" → "A training library is content. This is a system — it has intake (product changes trigger enablement), role-specific routing (different audiences get different depth), measurement (behavior change, not completion), and a feedback loop (field questions surface gaps). The library is one component, not the system."
8. "What would you do if the product team ships faster than enablement can keep up?" → "That's the everboarding problem. The content engine pattern separates curriculum design from production — templates let anyone produce a guide, not just the enablement team. And I'd instrument which product areas generate the most field questions to prioritize."

### Anti-Conservatism Protocol
Inherited from the parent interview-prep skill, non-negotiable for enablement assessments:
- Lead with the strongest piece in the first 10 seconds. Not the safest.
- If you haven't said something substantive by second 10, you're hedging.
- The tell: words like "framework," "alignment," or "holistic" without concrete referent.
- The override: one proof point, not three. One claim. One question back.
- Practice the opener 5x timed before the walk-through.

**Rehearsal method**: Record yourself on your phone. Play it back. If the first 10 seconds sound like a preamble ("So what I did was, I started by thinking about..."), re-record. The opener should sound like a claim: "The biggest enablement gap is X. Here's the system I built to close it." No warm-up.

## Agent-Specific Guidance

**Researcher**: Map the company's product surface before anything else. The knowledge map (Module B) is only as good as the product understanding underneath it. Prioritize official docs, engineering blogs, and recent release announcements. Identify the business metrics the company reports (churn, expansion, NRR, time-to-value).

**Architect**: Compare at least 2 response shapes before committing. The thesis must name the central tension — "enablement for [company] is really about [X]." If the thesis sounds generic, it IS generic. Check: would this thesis work for a different company? If yes, it's too weak.

**Builder**: Build the Day-1 artifact first, then the system around it. The artifact is the highest-signal component. Make it runnable (HTML) or immediately usable (Markdown with clear structure). Include verification: can a reviewer open this artifact and use it without explanation?

**Narrator**: The walk-through IS the submission. Structure for the grader's first 60 seconds, not for completeness. The grader should know within one minute: what you built, why, and whether it's credible.

**Validator**: Check requirement coverage first. Then check product depth — surface-level product references fail. Then check whether the measurement framework actually connects to the company's stated business metrics. Produce 3 adversarial questions the grader would ask.

## Calibration

Match output to 1.5x what they asked for, not 5x. If they say "spend 2-3 hours," produce 3-4 hours of visible work. If they give a page limit, respect it for the main document and include artifacts as appendices. Over-delivery should feel like depth, not volume.

## Submission Packaging

**Default format** (unless they specify otherwise):
1. **Main document** (PDF or Google Doc): Executive summary (1 paragraph) → system design → measurement → evidence bridge. Under 8 pages.
2. **Artifact(s)** (HTML files or links): Attached separately or linked. Each artifact should open and be usable without reading the main document.
3. **README** (if multiple files): One paragraph explaining what's in the submission and the recommended reading order.

**Naming convention**: `[YourName]_[Company]_[Role]_[Component].ext` — e.g., `Neill_Glean_TechEnablement_SystemDesign.pdf`, `Neill_Glean_TechEnablement_SA_Guide.html`

**Never submit**: raw Markdown (looks unfinished), a single massive document with artifacts inline (hard to navigate), or files that require installation to open.

## Artifact Creation Toolkit

When the skill calls for a concrete artifact (Module D or E), choose from these validated creation patterns. Each has been used in a real application and produced a passing submission.

### Pattern 1: HTML Readiness Guide (recommended default)
**What**: Single-file HTML that teaches one technical topic to one role. Includes talk tracks, objection handling, visual architecture, and checklists.
**When**: Any assessment that asks for enablement materials. Works for Families 1, 2, 3, 5.
**Reference**: `implementations/talent/applications/active/glean-technical-enablement/artifacts/sa-context-platform-guide.html`
**Creation**: Hand-coded. Dark mode, Inter + IBM Plex Mono fonts, badge system for role/time/audience, card layout, talk-track blocks with SAY/OBJECTION/RESPONSE styling. Single file, no dependencies beyond Google Fonts CDN.
**Build time**: 2-3 hours for a complete guide.
**Why it wins**: Opens in any browser. Looks professional. Demonstrates both technical depth AND enablement design thinking. The artifact IS the proof.

### Pattern 2: Interactive Learning Specimen (Stripe pattern)
**What**: Single-file HTML that demonstrates one enablement principle through an interactive experience. User selects a scenario, the tool generates a learning path or coaching response.
**When**: Assessments that ask you to demonstrate instructional design or AI-augmented learning.
**References**:
- `stripe-learning-architect/invisible-learning-system.html` (725 lines — behavior architecture: cue → artifact → coaching → evidence)
- `stripe-learning-architect/stripe-coach.html` (386 lines — operating principles coach with structured coaching output)
- `stripe-learning-architect/enablement-demo.html` (190 lines — intake form → learning path generator)
**Creation**: Hand-coded. Sophisticated visual design with gradient backgrounds, responsive grids. Interactive state management in vanilla JS.
**Build time**: 2-4 hours depending on complexity.
**Why it wins**: The reviewer can USE it, not just read it. Shows you think in terms of user experience, not just content.

### Pattern 3: Evaluation Workbench (Sierra pattern)
**What**: Single-file HTML tool for evaluating quality across multiple dimensions. Used for voice quality, but the pattern works for any multi-criteria evaluation.
**When**: Assessments where you need to demonstrate measurement or evaluation methodology.
**Reference**: `palette/voice/workbench/index.html` (868 lines — voice persona evaluation with audio, scoring rubrics, recommendation engine)
**Creation**: Hand-coded. Audio integration, live recommendation engine, dimension scoring.
**Build time**: 4-6 hours. Higher complexity.
**Why it wins**: Shows you can design evaluation systems, not just describe them.

### Pattern 4: Portfolio Page (YAML → HTML generator)
**What**: YAML configuration → generated HTML portfolio page with hero section, project showcases, philosophy, timeline.
**When**: When you need to present a body of work rather than a single artifact.
**Reference**: `enablement/portfolio/generate.py` (433 lines). Templates: oka, dashboard, obsidian, enablement, custom.
**Creation**: Write YAML config → run `python3 generate.py topics/[topic].yaml` → get HTML.
**Build time**: 30-60 minutes (config + generation + review).
**Why it wins**: Fast. Professional. Reusable across applications.

### Pattern 5: Slide Deck (Python → PPTX)
**What**: Programmatically generated PowerPoint with brand-aware styling.
**When**: Assessments that explicitly ask for a presentation or deck.
**Reference**: `archive/talent-closed-2026-04-09/talent-openai-deployment-mgr/takehome/generate_deck_v2.py`
**Creation**: Python script using `python-pptx`. Brand color palettes, styled text boxes, multi-slide structure.
**Build time**: 1-2 hours for script + generation.
**Why it wins**: Professional deck without manual PowerPoint work. Shows automation thinking.

### Pattern 6: Interactive Dashboard (Streamlit)
**What**: Live data visualization dashboard showing metrics, usage patterns, or adoption data.
**When**: Assessments where you need to demonstrate measurement, visibility, or operational intelligence.
**Reference**: `archive/talent-closed-2026-04-09/talent-openai-deployment-mgr/takehome/dashboard/app.py`
**Creation**: Python Streamlit app with Plotly charts. Can export to static HTML.
**Build time**: 2-4 hours. Requires Streamlit + Plotly.
**Why it wins**: Interactive data visualization. Can simulate real operational metrics.

### Pattern 7: Interview/Assessment Drill Tool (HTML)
**What**: Timed practice tool with questions, scoring, and feedback. Dark mode, 2-column layout.
**When**: If the assessment asks you to build a learning or practice tool.
**References**: `meta-product-ops-contract/meta-interview-bot.html`, `glean-technical-enablement/prep-bot/glean-kelley-recruiter-prep.html`
**Creation**: Hand-coded HTML/JS. Timer, question bank, scoring, vocabulary detection.
**Build time**: 2-3 hours.

### Artifact Selection Rule
When time is limited, default to **Pattern 1** (HTML Readiness Guide). It has the best effort-to-impact ratio: professional, demonstrates enablement thinking, opens anywhere, and can be built in 2-3 hours. Only use Patterns 2-7 when the assessment specifically calls for something they provide (interactivity, evaluation, presentation, data viz).

**What each pattern signals to the grader**:
| Pattern | Signal |
|---------|--------|
| 1 (Readiness Guide) | "I can produce field-ready content that's immediately usable" |
| 2 (Interactive Learning) | "I think about learning as an experience, not a document" |
| 3 (Evaluation Workbench) | "I can design measurement systems, not just describe them" |
| 4 (Portfolio Page) | "I can present a body of work coherently" |
| 5 (Slide Deck) | "I can communicate to executives" |
| 6 (Dashboard) | "I can make data visible and actionable" |
| 7 (Drill Tool) | "I can build practice environments that accelerate ramp" |

## Compressed Mode

## Post-Submission Protocol

Between submitting and the walk-through discussion:
1. **Re-read your submission cold** — as if you're the grader seeing it for the first time. Note what's unclear.
2. **Identify your 3 weakest points** — the grader will find them. Prepare honest answers for each.
3. **Prepare 2 "what I'd do differently" items** — shows self-awareness and iteration thinking.
4. **Rehearse the opener** — 60-second version, out loud, timed. Record and play back.
5. **Prepare 3 questions for the panel** — collaborative, not performative. "I made a choice about X — how does that match what you're seeing internally?"

## Compressed Mode

Use when: deadline under 4 hours, prompt is bounded, or the assessment is one of the simpler families (3, 4, or 5).

**Compressed time budget (4 hours total)**:
| Phase | Time | What to cut |
|-------|------|-------------|
| Classify + Architecture | 30 min | Merge into one pass. Thesis + module selection + artifact choice in one sitting. |
| Build | 2.5 hrs | One artifact only. Skip Module E. System design can be shorter (2 pages, not 5). |
| Quality Gate | 15 min | Checklist only — requirement coverage, product depth, thesis present, 60-second test. |
| Walk-Through Prep | 15 min | 60-second and 5-minute versions only. Skip 15-minute version. |
| Buffer | 30 min | For unexpected issues, final polish, submission packaging. |
