# Palette FDPM Niche Brief (v1)

Date: 2026-02-18
Owner: MissionCanvas / Palette
Purpose: pick a defensible niche based on current AI company focus signals and open role signals.

## Executive Thesis
Palette should not compete on base models. Palette should become the AI enablement control plane for overwhelmed operators: a trusted filter that discovers, evaluates, routes, and governs external agents/tools while keeping outcomes tied to business decisions.

Positioning line:
- "We do not ask customers to pick the best AI stack. Palette continuously does that for them and ships only decision-grade actions."

## Market Signals: What leading AI companies appear focused on now
These are inferred from current role mix and product messaging.

1. Deployment-heavy enterprise motions are growing.
- OpenAI is hiring Technical Success / Solutions Architect roles explicitly for "safe and effective deployment" and strategic partner solution design.
- Anthropic Applied AI roles emphasize end-to-end enterprise delivery from SOW to production and measurable outcomes.
- Fireworks and Sendbird are both hiring Forward Deployed Product Managers.

2. Agentic workflows are becoming productized in enterprise stacks.
- Glean emphasizes agent creation, orchestration, and model choice in enterprise workflows.
- Databricks is shipping assistant "Agent mode" for multi-step data engineering workflows.

3. Infrastructure and enterprise GTM are heavily staffed.
- Fireworks roles include infra, performance optimization, enterprise solutions architects, and FDPM.
- Cohere messaging centers on secure enterprise AI solutions.

## What they seem less focused on (opportunity zone)
1. Cross-vendor AI change management as a product category.
- Most companies optimize for their own stack adoption and ecosystem outcomes.
- Few are explicitly owning "continuous tool churn management" for the customer across many providers.

2. Independent decision-governance + agent brokerage for AI enablement teams.
- Strong products exist for in-product assistants, model hosting, or enterprise search/agents.
- Fewer products are purpose-built to answer: "given this objective/risk posture/timebox, which external AI agents should run now, with what human gates?"

3. One-way-door aware execution planning for non-technical operators.
- Market tools often focus on model quality and workflow automation.
- There is still whitespace in reversible decision design, safety gates, and audit-ready action briefs for business owners and transformation teams.

## Recommended Niche
## "AI Enablement Command Layer"
A neutral control layer for AI operators that:
- Continuously scans/ingests the AI vendor landscape.
- Matches objective -> best-fit agent/tool portfolio for that moment.
- Enforces convergence checks, one-way-door approvals, and decision logging.
- Produces action briefs and operating artifacts, not just chat answers.

Initial ICP:
- AI enablement leads and transformation owners in mid-market/enterprise teams with tool sprawl.

Beachhead Use Cases:
1. "Tool Sprawl Triage": from 50-200 tools to a monthly recommended operating stack.
2. "Decision-Grade Planning": objective -> routed plan -> action brief -> audit log.
3. "Pilot-to-Production Guardrails": phase gates, risk checks, and measurable outcome tracking.

## Why this fits Palette specifically
- Palette already has role separation (research/architecture/build/validate/narrative/monitor) and routing behavior.
- MissionCanvas already supports convergence + one-way-door checks + decision logs.
- Your personal edge is AI enablement operations, not base-model research.

## Competitive Frame
Not:
- Base model provider
- Generic chatbot
- Single-vendor workflow lock-in

Yes:
- Orchestration + governance + operator UX for AI decision execution.

## Workflow Recommendation (run this through Palette/ORCH)
Use your own platform in 4 loops.

### Loop 1: Landscape Sensing (Argy-led)
Input:
- AI company matrix (providers, vertical players, orchestration products, infra vendors)
- Hiring signal scrape (FDPM/FDE/Solutions/Applied AI roles)

Output artifacts:
- `market_focus_map_v1.md`
- `role_signal_heatmap_v1.csv`
- `focus_vs_whitespace_matrix_v1.md`

Gate:
- Anky validates source quality and inference confidence.

### Loop 2: Niche Selection (Rex-led)
Input:
- Loop 1 artifacts

Output artifacts:
- `niche_options_v1.md` (3 options)
- `tradeoff_matrix_v1.md`
- `one_way_doors_v1.md`

Gate:
- One-way-door checkpoint: choose one wedge only.

### Loop 3: Offer Design (Theri + Yuty)
Input:
- Selected niche

Output artifacts:
- `offer_stack_v1.md` (core product, service wrapper, pricing hypothesis)
- `operator_narrative_v1.md` (problem -> promise -> proof)
- `pilot_design_v1.md` (2-3 pilot designs)

Gate:
- Validate each offer includes measurable 30/60/90 day outcomes.

### Loop 4: GTM Execution Plan (Para + Anky)
Input:
- Offer artifacts

Output artifacts:
- `30_day_execution_plan_v1.md`
- `founder_pipeline_v1.csv` (first 25 targets)
- `experiment_backlog_v1.md`

Gate:
- Weekly scorecard live: pipeline, pilot starts, pilot conversion, time-to-value.

## Concrete 30-Day Plan
Week 1:
- Finalize niche statement and exclusion list (what Palette will not do).
- Build first AI company matrix dashboard view.

Week 2:
- Create one "AI Enablement Diagnostic" artifact template and run internally.
- Ship one demo flow: objective -> route -> action brief -> log.

Week 3:
- Pilot with 3 design partners (tool-sprawl-heavy teams).
- Capture before/after metrics on decision cycle time.

Week 4:
- Package offer v1 and publish a category POV memo.
- Decide continue/pivot based on pilot metrics.

## Success Metrics (first 90 days)
Primary:
- Time-to-decision reduction (%).
- Number of AI tools rationalized per customer.
- Pilot-to-paid conversion.

Secondary:
- Decision log completeness rate.
- One-way-door gate compliance.
- User confidence score in recommended stack.

## Risks
1. Category education burden: "filter layer" may need strong proof.
2. Perceived overlap with existing agent platforms.
3. Data freshness requirements for vendor/agent tracking.

Mitigations:
- Lead with measurable cost/time reduction.
- Show neutral, multi-vendor routing and governance differentiator.
- Maintain explicit model/provider abstraction in architecture.

## Suggested next MissionCanvas prompt (for immediate use)
"We are Palette. Objective: define and launch a niche category called AI Enablement Command Layer for organizations overloaded by AI tool sprawl. Build a 30-day execution plan with one-way-door gates, pilot design, measurable outcomes, and decision-log checkpoints. Constraints: do not build our own base model, remain vendor-neutral, prioritize speed to pilot revenue."

## Product Development Exercise Format (PM + Design Team)
Context:
- Team profile: startup, early-career designers/engineers with strong daily AI usage intuition.
- PM role: clear decision voice, sets quality bar and scope discipline.
- Team role: generate novel interaction patterns, edge-case coverage, and practical UX details.

Operating principle:
- Do not optimize only for frequent known intents.
- Keep a small regression suite, but bias learning toward long-tail and unfamiliar use cases.
- Measure expansion capability: how well we handle new problem shapes.

## Route Payload Program (for self-improving routing)
Definition:
- Route payload = structured JSON input to MissionCanvas route API used as a repeatable test case.

### Payload Taxonomy (v1)
Create payloads across these categories:
1. Core regression:
- Common business planning, grant planning, launch planning.
- Purpose: prevent breaking known baseline quality.
2. Long-tail novelty:
- Rare industries, unusual goals, sparse context.
- Purpose: discover blind spots and expansion opportunities.
3. Ambiguous intents:
- Vague objectives, missing outcomes, conflicting constraints.
- Purpose: test convergence and clarification behavior.
4. Cross-domain blends:
- Mixed objectives (e.g., education + compliance + GTM).
- Purpose: test routing under multi-goal tension.
5. One-way-door risk cases:
- Irreversible decisions, legal exposure, security tradeoffs.
- Purpose: validate gate behavior and escalation quality.
6. Adversarial/constraint-stress:
- Unrealistic timelines, contradictory instructions.
- Purpose: ensure safe refusal, decomposition, or re-scope behavior.

### 100-Payload Starter Mix (v1)
- 20 Core regression
- 35 Long-tail novelty
- 15 Ambiguous intents
- 15 Cross-domain blends
- 10 One-way-door risk cases
- 5 Adversarial/constraint-stress

Rationale:
- 80% of test inventory explores beyond known high-frequency intents.
- 20% protects core reliability.

### Evaluation Rubric (per payload, 1-5 scale each)
1. Convergence quality:
- Did output clarify objective/context/outcome/constraints adequately?
2. Routing fitness:
- Did selected RIU/agent map fit the problem type?
3. Actionability:
- Are next artifacts/actions concrete and executable?
4. Safety/governance:
- Were one-way-door risks detected and gated when needed?
5. Uncertainty honesty:
- Did system acknowledge missing info and avoid overconfident hallucination?
6. Expansion signal:
- Did system show useful behavior for a problem it has likely not seen before?

Aggregate metrics:
- Hard pass rate (>= 24/30 rubric score)
- One-way-door gate precision/recall
- Clarification-needed rate
- Novelty handling score (long-tail categories only)

### Self-Improvement Loop (weekly)
1. Generate/refresh payload set:
- Keep 20 fixed core payloads.
- Rotate 20-30 long-tail payloads weekly.
2. Run route and collect artifacts:
- Route output, action brief, decision log, gate behavior.
3. Independent evaluation:
- Use external reviewers or blinded internal eval panel.
4. Failure clustering:
- Group by failure type (convergence, routing, actionability, safety).
5. Targeted changes:
- Update translation heuristics, routing policy, prompt templates.
6. Re-run with holdout:
- Validate improvements on unseen payload subset.
7. Promote changes:
- Only ship if core regression stable and novelty score improves.

## PM-Driven Iteration Plan (3 rounds minimum)
This is the explicit \"design team writes -> PM critiques -> team revises\" cycle.

### Iteration 1: Problem Framing + Initial System Design
Design team delivers:
- `payload_taxonomy_v1.md`
- `payload_set_v1.jsonl` (first 100 payloads)
- `rubric_v1.md`
- `eval_runner_spec_v1.md`

PM review focus:
- Are we overweighting known frequent intents?
- Are long-tail and unfamiliar cases sufficiently represented?
- Are one-way-door cases explicit and auditable?

PM comments required:
- Keep/kill list for payload categories.
- Coverage gaps and overfitted clusters.
- Decision on v1 scoring thresholds.

Exit criteria:
- Payload distribution approved.
- Rubric approved.
- First evaluation run authorized.

### Iteration 2: Evaluation Results + Failure Analysis
Design team delivers:
- `eval_results_v1.csv`
- `failure_clusters_v1.md`
- `improvement_proposals_v1.md` (top 5 changes by impact)

PM review focus:
- Which failures are structural vs surface-level?
- Are improvements increasing expansion capability, not just pass-rate gaming?
- Did any change harm core regression reliability?

PM comments required:
- Prioritized remediation queue.
- Any blocked changes due to one-way-door risk.
- Updated target metrics for next round.

Exit criteria:
- Top 3 fixes selected.
- Holdout test plan approved.

### Iteration 3: Revised System + Holdout Validation
Design team delivers:
- `payload_set_v2.jsonl` (core stable + refreshed long-tail)
- `eval_results_v2_holdout.csv`
- `delta_report_v1_to_v2.md`
- `ship_recommendation_v1.md`

PM review focus:
- Did novelty handling improve on holdout?
- Did one-way-door gate quality improve or degrade?
- Is this enough to run live pilots?

PM comments required:
- Ship / iterate / pivot decision.
- Next 30-day product learning agenda.
- Specific hypotheses for Iteration 4.

Exit criteria:
- Decision memo published.
- Pilot instrumentation backlog created.

## Optional Iteration 4 Trigger
Run Iteration 4 if either is true:
- Hard pass rate < target on long-tail categories.
- Safety/gate precision drops after changes.

Iteration 4 scope:
- Architecture-level routing policy adjustments.
- Additional evaluator calibration.
- New payload category for emergent use cases from live pilots.

## Practical File Structure (recommended)
- `product/payloads/core_regression_v1.jsonl`
- `product/payloads/long_tail_v1.jsonl`
- `product/payloads/one_way_door_v1.jsonl`
- `product/eval/rubric_v1.md`
- `product/eval/results/`
- `product/eval/failure_clusters/`
- `product/pm_reviews/iteration_1.md`
- `product/pm_reviews/iteration_2.md`
- `product/pm_reviews/iteration_3.md`

## Immediate Next Action
Start Iteration 1 this week with one constraint:
- At least 60% of payloads must be outside current known implementation patterns.
- That forces discovery over comfort-zone optimization.

## Source Links
- OpenAI Solutions Architect, ChatGPT Ecosystem (Technical Success / safe deployment): https://openai.com/careers/solutions-architect-chatgpt-ecosystem-san-francisco/
- OpenAI Product Manager, Search (search/API/factual access focus): https://openai.com/careers/product-manager-search/
- Anthropic Technical Deployment Lead, Applied AI (Fortune 500, SOW-to-production): https://job-boards.greenhouse.io/anthropic/jobs/5017903008
- Fireworks careers (FDPM + infra-heavy role mix): https://fireworks.ai/careers
- Fireworks FDPM role (customer-to-roadmap bridge): https://job-boards.greenhouse.io/fireworksai/jobs/4008626009
- Sendbird careers (FDPM/FDE + AI Agent product roles): https://sendbird.com/careers
- Glean product overview (enterprise agents + orchestration + model choice messaging): https://www.glean.com/product/overview
- Cohere careers (secure enterprise AI positioning): https://cohere.com/careers
- Scale AI FDE role examples (forward deployed enterprise delivery): https://scale.com/careers/4597399005
