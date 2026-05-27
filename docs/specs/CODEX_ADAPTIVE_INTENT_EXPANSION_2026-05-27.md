# Codex Adaptive Intent Expansion - 2026-05-27

## Position

The adaptive intent framework is the right next abstraction.

Palette should not expose 131 RIUs to users. It should expose a small set of felt experiences that absorb the RIUs underneath. A user should not think, "I need RIU-701." They should think, "I need to research," "I need to protect privilege," "I need to decide," "I need to build," "I need to explain," or "I need to learn."

The RIUs remain the semantic spine. Intents become the experience layer. The model cascade becomes the execution layer. Governance is the boundary layer. Memory is the compounding layer.

The clean product grammar is:

```text
User intent -> RIU classification -> trust boundary -> model cascade -> artifact -> memory update
```

The intent is what the user feels.
The RIU is what Palette knows.
The trust boundary is what Palette protects.
The model cascade is how Palette thinks.
The artifact is what the user gets.
The memory update is why tomorrow is better.

## Fifteen Iterations

### Iteration 1 - Intent As Verb

Start with verbs, not domains. Humans enter through verbs:

- protect
- understand
- decide
- research
- create
- fix
- teach
- persuade
- monitor
- reflect

The domain comes second. "Protect a legal matter" and "protect a patient record" share an intent shape even though their rules differ.

### Iteration 2 - Intent As Situation

A user often cannot name the verb. They can name the situation:

- "I just got a new client."
- "Something broke."
- "I need to make a call."
- "I need to explain this."
- "I need to know what changed."
- "I need to not leak anything."

Palette should accept situation language and infer the intent.

### Iteration 3 - Intent As Trust State

Every intent has a default trust state:

- `local_only`: privileged, PHI, strategy, credentials, internal data
- `governed_external`: public research, market data, legal precedent, open documentation
- `human_checkpoint`: irreversible action, advice boundary, compliance exposure
- `open_creation`: low-risk drafting, ideation, templates

This makes intent routing safer than model routing.

### Iteration 4 - Intent As Artifact

Every intent should produce a recognizable artifact:

- protect -> gate decision
- research -> evidence brief
- decide -> decision record
- create -> artifact draft/build
- diagnose -> root-cause note and fix
- teach -> learning path or session plan
- evaluate -> scorecard
- communicate -> audience-ready message
- monitor -> signal packet
- reflect -> lesson/proposal

If an intent does not produce an artifact, it is probably just a chat mode.

### Iteration 5 - Intent As Emotional Relief

The real product is not "multi-model routing." It is relief:

- "I can use AI without leaking the client."
- "I do not have to start from scratch."
- "I know what kind of problem this is."
- "I have a record of why we decided."
- "I can show someone else how we got here."

Each intent should relieve a professional anxiety.

### Iteration 6 - Intent As RIU Envelope

An intent is a container for many RIUs. Example:

- `PROTECT` absorbs RIU-700 privilege, HIPAA, compliance, one-way-door, PII, access-control, security review.
- `RESEARCH` absorbs legal precedent, market scan, vendor scan, clinical literature, regulatory updates.
- `DECIDE` absorbs buy-vs-build, strategy choice, vendor selection, investment decision, treatment plan, settlement posture.

The user sees one intent. Palette sees the RIU.

### Iteration 7 - Intent As Model Cascade

Each intent has a default cascade, not a fixed pipeline:

- `PROTECT`: local classifier -> sanitizer -> governance gate -> audit log
- `RESEARCH`: local retrieval -> Perplexity -> local validation -> synthesis
- `DECIDE`: local retrieval -> options -> critique -> human checkpoint -> decision log
- `CREATE`: spec -> build -> test -> review -> store
- `TEACH`: learner model -> explanation -> check -> adapt -> assess

Palette can skip steps when not needed.

### Iteration 8 - Intent As Branching Surface

The best intents are allowed to discover they are wrong:

- `RESEARCH` can become `DECIDE` when evidence is enough.
- `DECIDE` can become `RESEARCH` when evidence is thin.
- `CREATE` can become `DIAGNOSE` when tests fail.
- `COMMUNICATE` can become `CONVERGE` when audience disagreement reveals a real decision.
- `TEACH` can become `CREATE` when the learner needs to build.

This is where Palette feels alive.

### Iteration 9 - Intent As Voice Primitive

In voice, the intent should be spoken naturally:

- "Protect this."
- "Research this publicly."
- "Help me decide."
- "Turn this into a client update."
- "Teach me what I am missing."
- "Stress test this."
- "Remember this."
- "What changed since yesterday?"

Voice should not expose RIUs, model names, or architecture by default.

### Iteration 10 - Intent As Boundary Contract

Each intent should make one visible promise:

- `PROTECT`: nothing sensitive leaves.
- `RESEARCH`: only safe public query leaves.
- `DECIDE`: no irreversible action without checkpoint.
- `CREATE`: artifact matches spec.
- `DIAGNOSE`: fix matches root cause.
- `TEACH`: learner state updates.
- `COMMUNICATE`: audience and purpose are explicit.
- `REFLECT`: lesson becomes reusable memory.

These are user-facing contracts.

### Iteration 11 - Intent As Founder Fit

The founder lens says Palette should not become a generic agent builder. It should become a system for translating messy human work into structured judgment.

That favors intents that:

- classify ambiguity
- preserve context
- create reusable artifacts
- help humans improve
- protect trust boundaries
- translate between domains

It disfavors flashy intents that only show model variety.

### Iteration 12 - Intent As Product Navigation

The eventual UI could be organized around a command palette:

```text
Protect...
Research...
Decide...
Create...
Fix...
Teach...
Explain...
Monitor...
Reflect...
```

Each command opens a guided experience, not a blank chat box.

### Iteration 13 - Intent As Market Wedge

For BDB, only three intents need to be visible:

- `PROTECT`: Sarah's privileged strategy stays local.
- `RESEARCH`: Sarah's public legal research uses Perplexity safely.
- `REFLECT/COMPOUND`: Sarah's later work connects to prior decisions.

Everything else can be in the product thesis.

### Iteration 14 - Intent As Governance Index

Each intent should have governance defaults:

| Intent | Default Boundary | Human Checkpoint |
|---|---|---|
| PROTECT | local_only | if user tries to override |
| RESEARCH | governed_external | if query contains sensitive terms |
| DECIDE | local_first | one-way-door decisions |
| CREATE | governed | publication/deployment |
| DIAGNOSE | local_first | production mutation |
| TEACH | local/governed | learner record updates |
| COMMUNICATE | governed | external send |
| MONITOR | governed | alerts/actions |
| REFLECT | local | promotion to source of truth |

This is where the OS becomes trustworthy.

### Iteration 15 - Intent As Memory Shape

Every intent stores a different memory object:

- `PROTECT` stores gate decisions.
- `RESEARCH` stores evidence packets.
- `DECIDE` stores rationale.
- `CREATE` stores artifact lineage.
- `DIAGNOSE` stores failure patterns.
- `TEACH` stores learner state.
- `COMMUNICATE` stores audience framing.
- `MONITOR` stores signal history.
- `REFLECT` stores lessons and proposals.

This is the missing piece: intents are not just how Palette acts. They determine what Palette remembers.

## Proposed Core Intents

I would not cut to five. Five will be too cramped. I would use nine user-facing core intents plus three hidden OS sub-intents.

### User-Facing Core

1. `PROTECT`
2. `RESEARCH`
3. `DECIDE`
4. `CREATE`
5. `FIX`
6. `TEACH`
7. `EXPLAIN`
8. `MONITOR`
9. `REFLECT`

### Hidden OS Sub-Intents

1. `CHECKPOINT`
2. `STORE`
3. `TRANSLATE`

`TRANSLATE` is hidden because it happens inside everything. It is the founder's superpower, but the user often experiences it as "make this make sense to them."

## Intent Catalog

### 1. PROTECT

Core promise: keep sensitive context inside the right boundary.

Default cascade:

```text
classify -> scan -> gate -> explain boundary -> log
```

Likely RIU families:

- RIU-700 privilege risk
- client strategy
- PHI / HIPAA
- PII exposure
- one-way-door decision
- access control
- policy compliance
- confidential business data

Use cases:

- Can I ask this question to Perplexity?
- Can I paste this document into Claude?
- Is this prompt privileged?
- Does this medical note contain PHI?
- Does this contract excerpt reveal client identity?
- Can this support ticket be sent to an external model?
- Should this negotiation strategy stay local?
- Is this board memo safe to summarize externally?
- Can we use cloud AI for this HR situation?
- Does this query need a human checkpoint?
- Did an agent try to use restricted context?
- What did we block today and why?

Best experience:

The user gets a plain answer:

```text
Safe for public research.
Client-specific strategy removed.
External query: "Delaware LLC fiduciary duty standards for co-founders."
Original matter details stayed local.
```

### 2. RESEARCH

Core promise: gather current evidence without losing the local frame.

Default cascade:

```text
classify -> retrieve local -> identify gap -> shape external query -> Perplexity -> validate -> evidence brief -> store
```

Likely RIU families:

- legal precedent
- clinical literature
- market scan
- competitor scan
- vendor evaluation
- regulatory update
- technology landscape
- company/person research
- public source enrichment

Use cases:

- What are the key Delaware LLC fiduciary cases?
- What changed in HIPAA AI rules this year?
- What are the best current local models for legal drafting?
- Which vendors support on-prem inference?
- What are Harvey and Legora doing now?
- What are the risks of using public AI for privileged material?
- What are the recent clinical guidelines for this treatment category?
- What are competitors saying about agent governance?
- What changed in Apple/NVIDIA/Qualcomm local inference?
- What case law supports this argument?
- What evidence should go into this pitch?
- What public facts can we safely bring into this private matter?

Best experience:

Palette should show three layers:

```text
Already known locally
New public evidence
How this changes the matter
```

### 3. DECIDE

Core promise: turn ambiguity into a judgment with rationale.

Default cascade:

```text
classify -> retrieve -> options -> evidence -> critique -> checkpoint -> decision record
```

Likely RIU families:

- buy vs build
- one-way/two-way door
- vendor choice
- settlement posture
- treatment plan
- investment decision
- roadmap prioritization
- policy decision
- hiring decision

Use cases:

- Should Sarah settle or litigate?
- Should we use local-only models for this workflow?
- Should Palette show four models in the BDB demo?
- Should a firm deploy Harvey, Legora, or Palette?
- Should a doctor order further tests or proceed?
- Should an executive approve a vendor?
- Should a founder apply now or wait?
- Should a team ship with known limitations?
- Should this be a two-way-door experiment?
- Should we add Mistral to the critical path?
- Should we publish this claim?
- Should this proposal become source of truth?

Best experience:

The output is a decision memo:

```text
Recommendation
Why
Evidence
Counterargument
Reversibility
Checkpoint required?
What would change my mind
```

### 4. CREATE

Core promise: turn intent into an artifact.

Default cascade:

```text
classify artifact -> retrieve patterns -> spec -> draft/build -> review -> test -> store
```

Likely RIU families:

- code implementation
- legal brief
- client memo
- curriculum module
- pitch deck
- business plan
- workflow
- bot/agent creation
- landing page
- demo script

Use cases:

- Write a client update.
- Draft a legal research memo.
- Build a CLI command.
- Create a voice bot for Joseph.
- Generate a demo script.
- Build a landing page.
- Create a learning module.
- Draft an investor pitch.
- Build a compliance checklist.
- Create a due diligence questionnaire.
- Write a settlement analysis template.
- Turn a decision into a reusable playbook.

Best experience:

Palette should ask for:

```text
Audience
Output format
Trust boundary
Source material
Definition of done
```

Then build through checkpoints.

### 5. FIX

Core promise: find the failure, repair it, and remember the lesson.

Default cascade:

```text
reproduce -> isolate -> retrieve similar failures -> root cause -> minimal fix -> verify -> lesson
```

Likely RIU families:

- bug diagnosis
- demo failure
- routing regression
- health check failure
- PII leakage
- bad retrieval
- stale manifest
- broken test
- incident response
- operational cleanup

Use cases:

- Why did `--json --external` crash?
- Why did a privileged query route externally?
- Why is the demo too slow?
- Why did the model classify nonsense confidently?
- Why did the bus message not arrive?
- Why is the manifest stale?
- Why did a cache result show `[CLIENT]`?
- Why are tests passing but the demo failing?
- Why did Mistral not run?
- Why did health report subtree mismatch?
- Why did the landing page not deploy?
- Why did the legal query use the wrong RIU?

Best experience:

Palette should produce:

```text
Failure
Repro
Root cause
Smallest fix
Tests
Lesson to store
```

### 6. TEACH

Core promise: increase someone's capability, not just answer them.

Default cascade:

```text
assess learner -> retrieve curriculum -> explain -> check understanding -> adapt -> practice -> store learner state
```

Likely RIU families:

- learning path
- onboarding
- capability building
- role-based explanation
- misconception detection
- adaptive session
- assessment
- enablement module

Use cases:

- Teach a lawyer how to use Palette safely.
- Teach a founder why local-first matters.
- Teach a junior engineer how the bus works.
- Teach a clinician the boundary between PHI and public research.
- Teach a salesperson the product story.
- Teach a new agent the BDB context.
- Teach a user the difference between research and strategy.
- Teach the team how to read a health check.
- Teach a learner through ARON-style adaptation.
- Teach a client what was decided and why.

Best experience:

The system should not just say "here is the answer." It should say:

```text
Here is the frame.
Here is the mistake people make.
Try this.
Show me your version.
Here is the next step.
```

### 7. EXPLAIN

Core promise: make a complex judgment legible to a specific audience.

Default cascade:

```text
classify audience -> retrieve context -> frame -> draft -> critique audience reaction -> refine -> store framing
```

Likely RIU families:

- stakeholder update
- client communication
- pitch
- status report
- board memo
- legal explanation
- technical explanation
- translation across domains

Use cases:

- Explain Palette to a judge in two minutes.
- Explain privilege risk to a solo attorney.
- Explain a routing decision to a compliance officer.
- Explain a failed test to an engineer.
- Explain a treatment choice to a patient.
- Explain a vendor choice to a CFO.
- Explain the BDB thesis to a nontechnical friend.
- Explain why Mistral should be cut from the main demo.
- Explain legal precedent to a startup founder.
- Explain a roadmap tradeoff to investors.

Best experience:

Palette should produce versions:

```text
Plain English
Expert version
Executive version
Skeptic version
One-sentence version
```

### 8. MONITOR

Core promise: watch the world or the system and tell me only what matters.

Default cascade:

```text
define signal -> set threshold -> scan -> filter -> alert -> store signal -> recommend next intent
```

Likely RIU families:

- external reality service
- market movement
- governance drift
- health regression
- competitor update
- legal/regulatory change
- task progress
- signal/noise classification

Use cases:

- Tell me if Harvey changes its local deployment story.
- Watch for new privilege/AI rulings.
- Watch for HIPAA AI guidance.
- Monitor Palette health failures.
- Monitor bus messages for blocked tasks.
- Monitor waitlist signups from legal domains.
- Monitor demo latency.
- Monitor whether gap signals exceed threshold.
- Monitor model API availability before recording.
- Monitor public competitor claims.
- Monitor stale governance proposals.
- Monitor legal vertical content gaps.

Best experience:

The output should be a `SignalPacket`:

```text
What changed
Why it matters
Affected RIUs
Confidence
Recommended next intent
```

### 9. REFLECT

Core promise: turn experience into reusable memory.

Default cascade:

```text
retrieve session -> identify patterns -> compare outcomes -> extract lessons -> propose KL/RIU updates -> human review -> store
```

Likely RIU families:

- session reflection
- auto enrichment
- health review
- postmortem
- case review
- learning review
- decision audit
- strategy update

Use cases:

- What did we learn from today's BDB sprint?
- Which demo queries failed or surprised us?
- What should become a KL entry?
- What RIU is missing?
- Which model route was too risky?
- Which claims are overclaims?
- What did Sarah's matter teach the system?
- What did the user's feedback reveal?
- What should be cut from the next script?
- What should be promoted to source of truth?
- What has Palette learned about itself this week?

Best experience:

This is the system's memory ceremony:

```text
What happened
What pattern emerged
What should change
What stays provisional
What gets promoted
```

## Expanded Experience Use Cases By Domain

### Legal

- Protect privilege before any model call.
- Split a mixed query into public law and client strategy.
- Research case law.
- Draft client update.
- Create settlement risk memo.
- Generate opposing counsel argument map.
- Compare claims to elements.
- Create deposition prep plan.
- Monitor new rulings.
- Reflect after matter milestone.
- Build privilege log.
- Review contract clause.
- Red-team legal memo.
- Explain legal risk to founder client.
- Decide whether a query can go external.

### Healthcare

- Strip PHI before public literature research.
- Retrieve clinical guidelines locally.
- Compare treatment options.
- Flag contraindications.
- Generate patient-friendly explanation.
- Prepare clinician handoff.
- Monitor new guideline updates.
- Audit AI use for HIPAA logs.
- Reflect on care pathway decisions.
- Teach a patient or junior clinician.
- Create follow-up checklist.
- Evaluate risk of external inference.
- Decide whether human approval is mandatory.

### Finance / Compliance

- Audit a process against a regulation.
- Research current rule changes.
- Evaluate a deal.
- Create investment memo.
- Monitor market or competitor signals.
- Generate risk register.
- Explain exposure to board.
- Decide GO/NO-GO.
- Draft compliance evidence packet.
- Reflect after audit.
- Compare vendor controls.
- Protect client financial data.

### Education / Enablement

- Assess learner state.
- Build adaptive session.
- Translate concept across domains.
- Create practice exercise.
- Diagnose misconception.
- Teach a workflow.
- Create onboarding path.
- Reflect on learner progress.
- Adapt for accessibility.
- Generate assessment rubric.
- Explain AI safety by role.
- Build "first useful artifact" for learner.

### Software / FDE

- Architect from messy request.
- Implement scoped patch.
- Debug failing workflow.
- Review code for regressions.
- Write tests.
- Monitor health.
- Reflect on sprint.
- Explain system to stakeholder.
- Create runbook.
- Protect secrets before commit.
- Decide build vs buy.
- Translate strategy into executable work.

### Founder / Executive

- Decide priority.
- Prepare investor pitch.
- Build demo narrative.
- Monitor market timing.
- Evaluate hires.
- Report progress.
- Negotiate partnership.
- Reflect on operating pattern.
- Create thesis memo.
- Explain category.
- Diagnose team drift.
- Protect confidential strategy.

## RIU Mapping Strategy

I would add an `intent_affinity` layer over RIUs, not bake intents into the RIU IDs.

Example schema:

```yaml
riu_id: RIU-701
primary_intent: RESEARCH
secondary_intents: [DECIDE, EXPLAIN, REFLECT]
guard_intents: [PROTECT]
default_boundary: governed_external
default_artifact: evidence_brief
memory_object: EvidencePacket
```

This keeps the taxonomy stable while allowing the product experience to evolve.

## Experience Objects

Each intent should create one of these objects:

| Intent | Object |
|---|---|
| PROTECT | GateDecision |
| RESEARCH | EvidenceBrief |
| DECIDE | DecisionRecord |
| CREATE | ArtifactLineage |
| FIX | FailureLesson |
| TEACH | LearnerState |
| EXPLAIN | FramingRecord |
| MONITOR | SignalPacket |
| REFLECT | ImprovementProposal |

These objects become the memory substrate. Chat logs disappear. Objects compound.

## The Big Creative Leap

Palette should eventually feel like this:

```text
User: I need to work this case.
Palette: This is MATTER WORK. I will protect privilege by default.

User: What does the law say?
Palette: This is RESEARCH. I can safely use public sources.

User: What should we do?
Palette: This is DECIDE. I will stay local and use the morning's research.

User: Write the client update.
Palette: This is EXPLAIN + CREATE. I will use the decision record, not expose the matter externally.

User: What did we learn?
Palette: This is REFLECT. I will update the matter memory and propose reusable knowledge.
```

The same system works for a clinician, founder, teacher, engineer, analyst, or consultant because the intent shape is stable and the RIUs/domain packs change underneath.

## Recommended Cut For Crew Vote

Do not vote on 30 intents. Vote on this:

### Keep As Core

- PROTECT
- RESEARCH
- DECIDE
- CREATE
- FIX
- TEACH
- EXPLAIN
- MONITOR
- REFLECT

### Keep As Hidden OS Primitives

- CHECKPOINT
- STORE
- TRANSLATE

### Treat As Domain Bundles, Not Core Intents

- Matter Work
- Clinical Decision
- Compliance Audit
- Deal Analysis
- Learning Design
- Client Intake
- Incident Response
- Negotiate
- Pitch
- Report
- Hire
- Debug
- Implement
- Architect

These are experience templates composed from the core intents.

## BDB Demo Fit

Sarah's morning becomes:

1. `PROTECT + DECIDE`
   - privileged strategy
   - local only
   - GateDecision + DecisionRecord

2. `RESEARCH`
   - public Delaware law
   - Perplexity governed external
   - EvidenceBrief

3. `DECIDE + REFLECT`
   - strategy based on prior research
   - local only
   - DecisionRecord linked to EvidenceBrief

This is cleaner than saying four models worked the case. The user story becomes:

```text
Palette knew when Sarah was protecting,
when Sarah was researching,
and when Sarah was deciding.
That is why each model saw only what it was allowed to see.
```

## Closing Thought

The magic is not "adaptive intents."

The magic is that Palette lets a professional move naturally through work without manually choosing:

- which model,
- which memory,
- which policy,
- which prior decision,
- which trust boundary,
- which artifact shape,
- or which next step.

The user brings intention.
Palette brings structure.
The models bring capability.
The memory brings continuity.
The checkpoints bring trust.

That is the experience layer.



## Second Pass - Recipes Change The Shape

The recipe layer adds the missing middle between intent and execution.

The first pass said:

```text
User intent -> RIU classification -> trust boundary -> model cascade -> artifact -> memory update
```

The more complete version is:

```text
User intent
-> situation/lens detection
-> RIU classification
-> trust boundary
-> integrity card
-> recipe selection
-> model/tool cascade
-> artifact
-> memory object
-> integrity signal
```

The `integrity card` is important. Palette should not choose a recipe from vibes. It should ask the integrity engine what is actually known about the RIU:

- Is the RIU classified?
- Is it internal-only or both?
- Does the knowledge library cover it?
- Does service routing exist?
- Do recipes exist for the candidate services?
- Are there people signals?
- Is the completeness score full, partial, weak, or bare?

That means intent does not only route the user. Intent also asks the system whether it is strong enough to act.

## Iterations 16-30

### Iteration 16 - Intent As Recipe Selector

Recipes should not be user-facing primary navigation.

A user should say:

```text
Research this.
Protect this.
Help me decide.
Create the memo.
Fix the failure.
```

Palette should silently resolve:

```text
intent=RESEARCH
riu=RIU-701 Legal Precedent Research
boundary=governed_external
integrity=partial/full
recipe=Perplexity legal-public-research recipe
artifact=EvidenceBrief
```

The recipe is the executable procedure. The intent is the felt job.

### Iteration 17 - Intent As Recipe Composer

The best workflows will not use one recipe. They will compose recipes.

Example:

```text
Matter Work = PROTECT + RESEARCH + DECIDE + EXPLAIN + REFLECT
```

Each step can invoke a different recipe:

- `PROTECT`: Microsoft Presidio/local regex sanitizer recipe, if available
- `RESEARCH`: Perplexity/Tavily public research recipe
- `DECIDE`: internal DecisionRecord recipe
- `EXPLAIN`: client memo recipe
- `REFLECT`: improvement proposal / KL proposal recipe

The domain bundle is not itself a core intent. It is a recipe chain over core intents.

### Iteration 18 - Intent As Integrity Probe

Before Palette executes an intent, it should check whether the underlying RIU layer is healthy enough.

The integrity engine already gives the needed pattern:

```text
RIU -> classification -> knowledge -> routing -> recipes -> people signals -> gaps/actions
```

Intent execution should inherit that:

```text
If RIU completeness is full: execute normally.
If RIU completeness is partial: execute, but expose limitations.
If RIU completeness is weak: ask for confirmation or narrow scope.
If RIU completeness is bare: route to RESEARCH or REFLECT before acting.
```

This prevents Palette from pretending maturity it does not have.

### Iteration 19 - Intent As Lens Adapter

Lenses are role/context adapters. They should not compete with intents.

The same intent changes shape by lens:

| Intent | Legal Lens | Healthcare Lens | Founder Lens | FDE Lens |
|---|---|---|---|---|
| PROTECT | privilege | PHI | strategy/confidentiality | secrets/access |
| RESEARCH | precedent | literature/guidelines | market/investor | docs/API/prior art |
| DECIDE | settlement posture | care pathway | priority/fundraising | architecture tradeoff |
| CREATE | memo/brief | patient explanation | pitch/demo | patch/spec/tool |
| DIAGNOSE | case flaw | workflow breakdown | operating drift | bug/regression |
| EXPLAIN | client/judge | patient/clinician | investor/team | stakeholder/dev |
| REFLECT | matter lessons | pathway audit | founder pattern | postmortem/KL |

The lens modifies vocabulary, risk defaults, examples, and artifact templates.
The intent remains the same.

### Iteration 20 - Intent As RIU Affinity, Not RIU Ownership

An RIU should not belong permanently to one intent. It should have affinities.

Example:

```yaml
riu_id: RIU-701
name: Legal Precedent Research
primary_intent: RESEARCH
secondary_intents: [DECIDE, EXPLAIN, REFLECT]
guard_intents: [PROTECT]
recipe_candidates: [perplexity, tavily]
default_artifact: EvidenceBrief
```

This is cleaner than adding intent-specific RIUs. It preserves the taxonomy while giving the product a user-friendly surface.

### Iteration 21 - Intent As Boundary Escalation

Some intents are natural guardrails for other intents.

`PROTECT` is not just a mode. It is a guard intent. It can interrupt anything.

Examples:

- `RESEARCH` becomes `PROTECT -> RESEARCH` when user includes client facts.
- `CREATE` becomes `PROTECT -> CREATE` when source material contains private data.
- `EXPLAIN` becomes `PROTECT -> EXPLAIN` before external send.
- `MONITOR` becomes `PROTECT -> MONITOR` if alerts include sensitive traces.

This is the difference between a workflow app and a governed OS.

### Iteration 22 - Intent As Artifact Contract

Every intent should have a strict artifact contract. This is where recipes and integrity meet.

| Intent | Artifact | Must Include |
|---|---|---|
| PROTECT | GateDecision | boundary, sanitized query, blocked material, rationale |
| RESEARCH | EvidenceBrief | local knowns, external findings, citations, confidence |
| DECIDE | DecisionRecord | recommendation, evidence, counterargument, reversibility |
| CREATE | ArtifactLineage | spec, source material, build output, review/test result |
| DIAGNOSE | FailureLesson | repro, root cause, patch, verification, stored lesson |
| TEACH | LearnerState | level, misconception, exercise, assessment, next step |
| EXPLAIN | FramingRecord | audience, purpose, version, risk, final message |
| MONITOR | SignalPacket | change, affected RIUs, confidence, recommended next intent |
| REFLECT | ImprovementProposal | pattern, proposed update, evidence, governance status |

The artifact contract should drive recipe requirements.

### Iteration 23 - Intent As Recipe Completion Signal

Recipes should report completion back into the integrity engine.

If an intent invokes a recipe and the recipe succeeds, Palette learns:

- this RIU has a working execution path
- this recipe is not orphaned
- this artifact contract can be produced
- this lens/domain path is viable

If a recipe fails, Palette learns:

- the RIU may need a better recipe
- service routing may be stale
- the recipe may need an override
- the knowledge entry may overclaim maturity

The integrity engine should eventually score not only static coverage, but observed recipe performance.

### Iteration 24 - Intent As Trust Boundary Before Model Boundary

The user should never choose the model first.

The system should choose:

```text
intent -> trust boundary -> allowed execution class -> model/tool
```

That means:

- local-only intent paths cannot call Perplexity just because research would be useful
- governed-external paths must use sanitized external queries
- open-creation paths can use broader model help
- human-checkpoint paths can prepare but not commit

This is the practical answer to the legal/privacy market wedge.

### Iteration 25 - Intent As Memory Write Policy

Memory should be shaped by intent because each intent knows what kind of memory is valuable.

`RESEARCH` should not store a vague chat transcript. It should store an EvidenceBrief.

`DECIDE` should not store "we talked about settlement." It should store a DecisionRecord with reversibility and change-my-mind criteria.

`DIAGNOSE` should not store "bug fixed." It should store a FailureLesson.

This is how Palette compounds without turning memory into a junk drawer.

### Iteration 26 - Intent As Demo Simplicity

BDB should not show all nine intents.

The thesis can name the full system. The demo should show three moves:

```text
PROTECT: Palette keeps privileged strategy local.
RESEARCH: Palette safely brings in public legal evidence.
DECIDE: Palette connects evidence to the matter without leaking it.
```

Then the compounding moment:

```text
REFLECT: Palette remembers what was decided and what should improve.
```

This proves the whole architecture without teaching the audience the whole architecture.

### Iteration 27 - Intent As Domain Pack Interface

Domain packs should be bundles of:

- lens defaults
- RIU affinity overrides
- recipe chains
- artifact templates
- risk vocabulary
- example situations

Example:

```yaml
domain_pack: legal_matter_work
default_guard_intent: PROTECT
visible_intents: [PROTECT, RESEARCH, DECIDE, EXPLAIN, REFLECT]
critical_rius: [RIU-700, RIU-701, RIU-708, RIU-709]
recipes:
  research: public_precedent_research
  explain: client_update
  reflect: matter_lesson_proposal
```

This lets Palette support verticals without multiplying core intents.

### Iteration 28 - Intent As Anti-Overclaim Discipline

Every intent should be honest about maturity.

If the RIU is internal-only, Palette should not pretend a service recipe exists.

If the RIU is `both` but recipe coverage is missing, Palette can say:

```text
I can produce the internal artifact.
External service routing is known, but the integration recipe is not validated yet.
```

This is not a weakness. This is the product earning trust.

### Iteration 29 - Intent As Operating System Primitive

The final primitive is not:

```text
agent
tool
model
recipe
RIU
```

The final primitive is:

```text
intentful governed work
```

That work has:

- a human purpose
- a semantic classification
- a trust boundary
- an integrity state
- an execution recipe
- an artifact contract
- a memory write
- a governance trail

This is the real OS claim.

### Iteration 30 - Intent As The Interface Between Human And System Learning

Humans learn through intents:

- "When do I protect?"
- "When do I research?"
- "When am I deciding?"
- "When should I explain?"
- "When should I reflect?"

The system learns through the same intents:

- which RIUs recur
- which recipes work
- which trust boundaries are triggered
- which artifacts create value
- which knowledge gaps repeat
- which domain packs are worth strengthening

That symmetry is the precious part. Palette is not only helping the user do work. It is learning the structure of the user's work in the same grammar the user can understand.

## RIU Family Fit

This is a provisional mapping. The exact RIU IDs should be generated from taxonomy metadata later, but the shape is clear.

| RIU Family | Best Intent Fit | Notes |
|---|---|---|
| RIU-001 to RIU-011 intake, convergence, scope, contracts | DECIDE / CREATE | These are the skeleton of professional judgment and delivery. |
| RIU-012 compliance and PII | PROTECT | Also guard intent for RESEARCH, CREATE, EXPLAIN, MONITOR. |
| RIU-013 to RIU-020 data/source/baseline | RESEARCH / DECIDE | Often preparatory evidence before a decision or build. |
| RIU-021 to RIU-035 eval, schema, cache, ranking, generation | DIAGNOSE / CREATE / DECIDE | These are engineering and quality recipes under the hood. |
| RIU-060 to RIU-077 architecture/design | DECIDE / CREATE | Best surfaced as architecture decisions or build specs. |
| RIU-080 to RIU-088 implementation/tooling | CREATE / DIAGNOSE | User says build or fix; Palette sees implementation RIUs. |
| RIU-089 to RIU-105 quality, safety, ops, adoption | DIAGNOSE / MONITOR / TEACH / REFLECT | These often become health checks, lessons, or enablement paths. |
| RIU-120 to RIU-140 reliability and delivery | DIAGNOSE / MONITOR | Strong Specialist/debugger territory. |
| RIU-200 to RIU-290 narrative/demo/customer value | EXPLAIN / CREATE / DECIDE | This is where GTM becomes artifact work, not generic copy. |
| RIU-320 to RIU-400 integration/content audit | CREATE / REFLECT / MONITOR | Recipes and integrity signals matter heavily here. |
| RIU-500 multimodal workflows | CREATE / RESEARCH / DECIDE | Tool choice depends on artifact and service routing. |
| RIU-510 agentic systems | CREATE / DECIDE / DIAGNOSE | Architecture plus runtime repair. |
| RIU-520 LLMOps | MONITOR / DIAGNOSE / DECIDE | Cost, cache, observability, routing, scaling. |
| RIU-530 governance | PROTECT / DECIDE / MONITOR | Guard layer and audit layer. |
| RIU-540 agent-specific patterns | CREATE / DIAGNOSE / REFLECT | Builds and improves agents. |
| RIU-550 no-code app generation | CREATE | Usually recipe-led external tool choice. |
| RIU-600 enterprise adoption | DECIDE / TEACH / EXPLAIN / REFLECT | Human enablement and operating model. |
| RIU-700 legal vertical | PROTECT / RESEARCH / DECIDE / EXPLAIN / REFLECT | BDB's strongest proof cluster. |

## Recipe Fit

Recipes should be evaluated against intents, not only against services.

Current integrity checks answer:

```text
Does this routed service have a recipe?
```

The next check should answer:

```text
Can this recipe fulfill the artifact contract for this intent?
```

A service recipe can be technically present but intent-incomplete.

Example:

- A Perplexity recipe may support `RESEARCH`.
- It does not automatically support `DECIDE`.
- It can feed a DecisionRecord only if the DECIDE intent has a synthesis/checkpoint recipe after research.

That suggests a second registry:

```yaml
intent_recipe_affinity:
  RESEARCH:
    required_outputs: [EvidenceBrief]
    acceptable_recipe_types: [web_research, literature_search, market_scan]
  PROTECT:
    required_outputs: [GateDecision]
    acceptable_recipe_types: [pii_scan, privilege_scan, sanitizer, policy_gate]
  DECIDE:
    required_outputs: [DecisionRecord]
    acceptable_recipe_types: [option_generation, critique, reversibility_check]
```

This would let the integrity engine find a new class of gap:

```text
RIU has service recipe coverage, but no intent-complete recipe chain.
```

That is the real maturity signal.

## Perfect-State Architecture

In perfect state, Palette has four registries layered over the same ontology.

### 1. RIU Registry

What kind of problem is this?

```yaml
riu_id: RIU-701
name: Legal Precedent Research
classification: both
reversibility: two_way
```

### 2. Intent Affinity Registry

How should the user experience this problem?

```yaml
riu_id: RIU-701
primary_intent: RESEARCH
secondary_intents: [DECIDE, EXPLAIN, REFLECT]
guard_intents: [PROTECT]
default_artifact: EvidenceBrief
memory_object: EvidenceBrief
```

### 3. Recipe Affinity Registry

How can Palette execute it?

```yaml
riu_id: RIU-701
intent: RESEARCH
recipe_chain:
  - local_knowledge_retrieval
  - public_query_sanitizer
  - perplexity_public_research
  - evidence_validation
  - evidence_brief_writer
```

### 4. Lens/Domain Registry

How should this feel in context?

```yaml
domain_pack: legal
lens: solo_attorney
riu_id: RIU-701
surface_language: "What does the law say?"
blocked_language: "What should I tell my client to do?" # requires DECIDE + PROTECT
artifact_template: legal_evidence_brief
```

These registries make the system legible:

```text
RIU tells Palette what the work is.
Intent tells the user what they are doing.
Recipe tells the machine how to do it.
Lens tells the product how it should feel.
```

## Core Intent Reconsideration

After adding recipes, the nine-intent set still mostly holds, but one change is worth making.

`FIX` should probably be named `DIAGNOSE` in the canonical system, with "Fix" as the plain-language command.

Reason:

- `FIX` implies mutation.
- `DIAGNOSE` implies root cause first.
- The Specialist loop already thinks in isolate/diagnose/propose/verify/close.
- Many professional contexts need diagnosis without immediate repair.

So the final naming should be:

| User Command | Canonical Intent |
|---|---|
| Fix this | DIAGNOSE |
| Debug this | DIAGNOSE |
| What broke? | DIAGNOSE |

The perfect-state core becomes:

1. `PROTECT`
2. `RESEARCH`
3. `DECIDE`
4. `CREATE`
5. `DIAGNOSE`
6. `TEACH`
7. `EXPLAIN`
8. `MONITOR`
9. `REFLECT`

And three hidden primitives:

1. `CHECKPOINT`
2. `STORE`
3. `TRANSLATE`

## Product Law

Palette should obey this law:

```text
No intent may execute through a recipe chain that cannot produce its artifact contract.
No recipe may call a tool outside the trust boundary selected by the intent and RIU.
No memory write may occur without an object type tied to the intent.
No source-of-truth update may occur without governance.
```

This law binds the whole architecture.

## Final Synthesis

The perfect state is not a list of intents.

It is a grammar:

```text
Human says what they are trying to do.
Palette infers the intent.
Palette classifies the RIU.
Palette checks the trust boundary.
Palette asks integrity whether the path is mature.
Palette selects or composes recipes.
Palette produces the right artifact.
Palette stores the right memory object.
Palette improves the RIU/recipe/lens map over time.
```

That is why recipes matter. They make the intent layer executable. They also keep the intent layer honest.

Without intents, recipes are buried infrastructure.
Without recipes, intents are beautiful product language.
Together, they become governed work.


## Third Pass - What The World Has Been Trying To Do With AI

The next lens is experiential.

People do not come to AI saying, "I need a transformer-backed probabilistic synthesis engine." They come with pressure:

- I have too much information.
- I need to make a decision.
- I need to not get in trouble.
- I need to turn vague thoughts into something real.
- I need to explain this to someone who does not think like me.
- I need to learn enough to act.
- I need to know what changed.
- I need to fix what broke.
- I need this work to matter again tomorrow.

Most AI products answer with a chat box. Palette should answer with an intentful path.

The training distribution of modern AI use is full of repeated human patterns. People ask models to write emails, summarize documents, compare options, debug code, generate strategy, make study plans, create presentations, analyze contracts, role-play conversations, research markets, draft policies, and explain hard ideas. Underneath all that variety are a few recurring jobs.

Palette's intents are powerful because they name those jobs in a way that a system can govern.

## The Common AI Failure Patterns

### 1. The Blank Box Problem

The user arrives with pressure but no structure. The chat box asks, "What do you want?" The user gives a half-shaped request. The model responds with a half-shaped answer.

Palette improvement:

```text
Half-shaped request -> inferred intent -> RIU -> artifact contract
```

Instead of asking the user to prompt better, Palette should infer the work shape:

- "I have a meeting with a client tomorrow" becomes `EXPLAIN + DECIDE`.
- "I do not know if I can paste this" becomes `PROTECT`.
- "What are we missing?" becomes `RESEARCH + DECIDE`.
- "This stopped working" becomes `DIAGNOSE`.
- "Make this useful for the team" becomes `CREATE + TEACH`.

The user should not have to know the right prompt genre. Palette supplies the genre.

### 2. The Confident Mush Problem

Generic AI often produces plausible synthesis without telling the user which parts are known, inferred, guessed, stale, or unsafe.

Palette improvement:

```text
Intent -> evidence posture -> artifact fields
```

A `RESEARCH` artifact separates:

- already known locally
- newly found externally
- contradictory
- unvalidated
- decision-relevant

A `DECIDE` artifact separates:

- recommendation
- reason
- counterargument
- reversibility
- what would change the answer

This turns AI from prose into judgment support.

### 3. The Privacy Cliff

Users casually paste sensitive material because the product gives no structural warning at the point of action.

Palette improvement:

```text
PROTECT as interrupt, not feature
```

`PROTECT` should be the intent that can preempt every other intent. The user starts with `RESEARCH`, but Palette notices privileged matter facts and inserts:

```text
PROTECT -> sanitize -> RESEARCH
```

This is the market wedge. Most tools make privacy a setting. Palette makes it a workflow primitive.

### 4. The Everything-Is-A-Draft Problem

AI tools overproduce drafts. Users then become editors of generic material instead of operators of structured work.

Palette improvement:

```text
CREATE requires source, audience, boundary, definition of done
```

`CREATE` should not mean "generate content." It should mean "turn intent into an artifact with lineage."

The minimum artifact lineage:

- what the user asked for
- what RIU/domain shaped it
- what sources were allowed
- what boundary applied
- what recipe ran
- what review happened
- what changed between versions

That makes creation trustworthy and repeatable.

### 5. The Decision Laundering Problem

People use AI to make a recommendation sound rational after they have already chosen. The model helps launder preference into prose.

Palette improvement:

```text
DECIDE requires counterargument and reversibility
```

A Palette decision cannot be just "I recommend X." It should always carry:

- options considered
- rejected options
- strongest counterargument
- reversibility
- checkpoint required
- change-my-mind trigger

This protects humans from using AI as a confidence machine.

### 6. The Lost Context Problem

Every AI session starts over. The user teaches the model the same project, same constraints, same preferences, same history.

Palette improvement:

```text
Intent-shaped memory objects
```

Memory should not be global chat residue. It should be typed:

- GateDecision
- EvidenceBrief
- DecisionRecord
- ArtifactLineage
- FailureLesson
- LearnerState
- FramingRecord
- SignalPacket
- ImprovementProposal

The next session retrieves the object that matches the new intent.

### 7. The Tool Choice Burden

Users are increasingly forced to decide which AI model or tool to use: Claude, ChatGPT, Gemini, Perplexity, local model, Cursor, Runway, NotebookLM, etc.

Palette improvement:

```text
Intent -> RIU -> trust boundary -> service routing -> recipe
```

The user should choose the work, not the vendor.

- `RESEARCH` with public facts can route to Perplexity.
- `PROTECT` with privileged material stays local.
- `CREATE` for code can route to builder/Codex patterns.
- `EXPLAIN` for audience framing can route to narrative templates.
- `MONITOR` for external change can route through ERS.

Tool choice becomes a consequence of governed classification.

### 8. The One-Off Magic Problem

A user gets one excellent AI output, then cannot reproduce it. The prompt was ad hoc, the context was accidental, and no process was captured.

Palette improvement:

```text
Successful intent run -> recipe candidate -> memory -> integrity signal
```

When a run works, Palette should ask:

- Was this just a result, or a reusable recipe?
- Which RIU did it serve?
- Which artifact contract did it satisfy?
- Which lens/domain should inherit it?
- Should it become a recipe, KL entry, or domain-pack example?

That is how random success becomes system capability.

### 9. The Learning Plateau

People use AI to get answers but do not get better. The work is outsourced, not absorbed.

Palette improvement:

```text
TEACH as optional overlay on any intent
```

`TEACH` should often be a companion, not a standalone destination.

- `RESEARCH + TEACH`: show how the evidence was evaluated.
- `DECIDE + TEACH`: explain the judgment pattern.
- `CREATE + TEACH`: turn the artifact into a reusable method.
- `DIAGNOSE + TEACH`: explain the failure pattern.
- `PROTECT + TEACH`: show why something was blocked.

This is how Palette becomes enablement, not just automation.

### 10. The No-Afterlife Problem

AI work often dies after the answer. No lesson, no update, no compounding.

Palette improvement:

```text
REFLECT as closing ceremony
```

Every meaningful session should have a lightweight REFLECT opportunity:

```text
What should Palette remember?
What should become reusable?
What was wrong or missing?
What should be promoted only after review?
```

The user should feel that good work leaves the system stronger.

## Perfect-State User Experiences

### The Lawyer

Old AI experience:

```text
Can I paste this client email into Claude? Maybe not. I will anonymize it manually. Now I need case law. I will open Perplexity. Now I need to connect it back to the facts. I hope I did not leak anything.
```

Palette experience:

```text
User: I need to work this client matter.
Palette: This is legal matter work. I will protect privilege by default.

User: What does the law say about fiduciary duties here?
Palette: I separated public law from client facts. Public research can go external. Client strategy stays local.

User: What should we do?
Palette: This is a decision. I will use the public evidence brief and the private matter record locally. No external call.

User: Draft the client update.
Palette: This is explain plus create. I will use the decision record and produce a client-safe version.

User: What should we remember?
Palette: I found one reusable matter pattern and one proposed knowledge update.
```

The magic is not that Palette can answer legal questions. The magic is that it knows when the work changes from protection to research to decision to explanation.

### The Doctor Or Clinician

Old AI experience:

```text
Summarize this case. Search guidelines. Explain to patient. Do not include PHI. Did I include PHI? Is the advice current? Is this medical advice? I need to check everything myself.
```

Palette experience:

```text
PROTECT: PHI stays local.
RESEARCH: public guideline search uses sanitized clinical category.
DECIDE: care pathway remains clinician-supervised and checkpointed.
EXPLAIN: patient-friendly explanation avoids unsupported certainty.
REFLECT: care pathway lesson is stored without patient identity.
```

Palette should not replace clinical judgment. It should keep the work in the right lane.

### The Founder

Old AI experience:

```text
Help me with strategy. Make a pitch. Research competitors. Write a roadmap. What should I do next? Everything blends into motivational business prose.
```

Palette experience:

```text
RESEARCH: external market signal.
DECIDE: priority and tradeoff.
CREATE: pitch/demo/script.
EXPLAIN: investor or customer framing.
MONITOR: market movement.
REFLECT: founder operating pattern.
```

The founder does not need more ideas. The founder needs pressure turned into sequenced judgment.

### The Engineer

Old AI experience:

```text
Here is an error. It suggests five possible fixes. I try one. It breaks something else. The model forgets what we tested.
```

Palette experience:

```text
DIAGNOSE: reproduce, isolate, retrieve similar failures, root cause.
CREATE: patch only after diagnosis.
MONITOR: health/regression check.
REFLECT: FailureLesson stored.
```

The important distinction: `CREATE` should not start until `DIAGNOSE` earns the right to patch.

### The Teacher Or Enablement Lead

Old AI experience:

```text
Make a lesson plan. Make it simpler. Make a quiz. Explain it again. The learner's actual misconception is weakly tracked.
```

Palette experience:

```text
TEACH: assess learner state.
EXPLAIN: adapt framing.
CREATE: practice artifact.
DIAGNOSE: identify misconception.
REFLECT: update learner state and module gap.
```

Teaching is not content generation. It is stateful capability change.

### The Executive

Old AI experience:

```text
Summarize this report. What are the risks? Write a board update. Which option is best? The answer sounds polished but I cannot audit the reasoning.
```

Palette experience:

```text
RESEARCH: current facts and evidence.
DECIDE: recommendation with reversibility.
EXPLAIN: board-ready framing.
PROTECT: confidential strategy boundary.
MONITOR: signal thresholds.
REFLECT: decision audit.
```

Palette should make executive work less performative and more inspectable.

## The Deeper Intent Set: Human Anxieties

The nine intents are verbs. Underneath them are anxieties.

| Anxiety | Intent That Relieves It | Product Promise |
|---|---|---|
| I might leak something | PROTECT | The boundary is handled before action. |
| I do not know what is true | RESEARCH | Evidence is separated from inference. |
| I do not know what to do | DECIDE | Options become judgment with rationale. |
| I need something real | CREATE | Intent becomes artifact. |
| Something is wrong | DIAGNOSE | Failure becomes cause, fix, lesson. |
| I do not understand | TEACH | Answer becomes capability. |
| They will not understand | EXPLAIN | Judgment becomes audience-fit language. |
| I need to know what changed | MONITOR | Signal is separated from noise. |
| I do not want to lose the lesson | REFLECT | Experience becomes memory. |

This may be the best user-facing way to test the intents. If an intent does not relieve a real anxiety, it is probably not core.

## The Hidden Superpower: Transitions

The best part of the intent model is not the intents. It is the transitions.

Most AI products are bad at recognizing when the job changed.

Palette should be excellent at transitions:

```text
RESEARCH -> DECIDE
when evidence is sufficient and the user asks "so what?"

DECIDE -> RESEARCH
when the decision lacks evidence.

CREATE -> DIAGNOSE
when the artifact fails review or tests.

EXPLAIN -> DECIDE
when audience framing exposes unresolved tradeoff.

PROTECT -> RESEARCH
when sensitive material can be safely converted into a public query.

MONITOR -> ALERT_HUMAN / DECIDE
when a signal crosses threshold.

TEACH -> CREATE
when the learner needs practice, not more explanation.

REFLECT -> CREATE
when a lesson should become a recipe, template, or KL proposal.
```

This is where Palette can feel unlike a chatbot. It can notice the work changing.

## Intent Transition Matrix

| From | To | Trigger |
|---|---|---|
| PROTECT | RESEARCH | Sanitized public query is available. |
| PROTECT | DECIDE | Sensitive facts require local judgment. |
| RESEARCH | DECIDE | Evidence crosses sufficiency threshold. |
| RESEARCH | MONITOR | Evidence is inconclusive but watchable. |
| RESEARCH | REFLECT | Knowledge gap recurs. |
| DECIDE | RESEARCH | Key assumption is unsupported. |
| DECIDE | EXPLAIN | Decision needs stakeholder communication. |
| DECIDE | CREATE | Decision implies an artifact or implementation. |
| CREATE | DIAGNOSE | Output fails test, review, or expectation. |
| CREATE | TEACH | Artifact should become reusable learning. |
| DIAGNOSE | CREATE | Root cause has a bounded fix. |
| DIAGNOSE | REFLECT | Failure pattern should be stored. |
| TEACH | DIAGNOSE | Learner misconception repeats. |
| TEACH | CREATE | Learner needs exercise or scaffold. |
| EXPLAIN | DECIDE | Messaging reveals unresolved choice. |
| EXPLAIN | PROTECT | Message risks disclosure. |
| MONITOR | RESEARCH | Signal needs validation. |
| MONITOR | DECIDE | Signal requires action. |
| REFLECT | CREATE | Lesson should become recipe/template. |
| REFLECT | PROTECT | Memory promotion risks source-of-truth or privacy boundary. |

The transition matrix may be more important than the command palette.

## Recipe Chains For Common Work

### Legal Matter Work

```yaml
experience: legal_matter_work
chain:
  - intent: PROTECT
    artifact: GateDecision
    recipe_chain: [local_privilege_scan, public_query_sanitizer]
  - intent: RESEARCH
    artifact: EvidenceBrief
    recipe_chain: [local_legal_knowledge_retrieval, perplexity_public_research, evidence_validation]
  - intent: DECIDE
    artifact: DecisionRecord
    recipe_chain: [matter_context_retrieval, options, counterargument, reversibility_check]
  - intent: EXPLAIN
    artifact: FramingRecord
    recipe_chain: [audience_selection, client_update_draft, disclosure_check]
  - intent: REFLECT
    artifact: ImprovementProposal
    recipe_chain: [matter_lesson_extract, kl_gap_proposal]
```

### AI Adoption Work

```yaml
experience: ai_adoption_work
chain:
  - intent: RESEARCH
    artifact: EvidenceBrief
    recipe_chain: [current_tool_landscape, people_signal_lookup, service_routing_check]
  - intent: DECIDE
    artifact: DecisionRecord
    recipe_chain: [buy_vs_build, risk_register, one_way_door_check]
  - intent: CREATE
    artifact: ArtifactLineage
    recipe_chain: [workflow_spec, integration_recipe, pilot_plan]
  - intent: TEACH
    artifact: LearnerState
    recipe_chain: [role_lens, five_minute_recipe, practice_task]
  - intent: MONITOR
    artifact: SignalPacket
    recipe_chain: [usage_signal, failure_signal, adoption_signal]
  - intent: REFLECT
    artifact: ImprovementProposal
    recipe_chain: [roi_lesson, recipe_update, kl_proposal]
```

### Software Remediation Work

```yaml
experience: software_remediation_work
chain:
  - intent: DIAGNOSE
    artifact: FailureLesson
    recipe_chain: [reproduce, isolate, root_cause, minimal_fix_spec]
  - intent: CREATE
    artifact: ArtifactLineage
    recipe_chain: [patch, focused_test, review]
  - intent: MONITOR
    artifact: SignalPacket
    recipe_chain: [health_check, regression_check]
  - intent: REFLECT
    artifact: ImprovementProposal
    recipe_chain: [failure_pattern, test_gap, memory_update]
```

## The Product Should Feel Like A Professional Partner, Not A Prompt Lab

A prompt lab says:

```text
Try asking better.
```

Palette says:

```text
I know what kind of work this is.
I know what must stay protected.
I know what evidence is missing.
I know which recipe can execute it.
I know what artifact should come out.
I know what should be remembered.
```

This is the leap.

## What To Build First In The Intent Layer

The first implementation should not try to automate all nine intents. It should build the spine that every intent uses.

### Slice 1 - Intent Resolver

Input:

```text
raw user utterance + optional lens/domain
```

Output:

```yaml
primary_intent: RESEARCH
secondary_intents: [DECIDE]
guard_intents: [PROTECT]
confidence: medium
situation: legal_public_research_from_private_matter
```

### Slice 2 - Intent Affinity Registry

A YAML registry mapping RIUs to:

- primary intent
- secondary intents
- guard intents
- default artifact
- memory object
- default boundary

### Slice 3 - Artifact Contract Registry

A YAML registry defining required fields for:

- GateDecision
- EvidenceBrief
- DecisionRecord
- ArtifactLineage
- FailureLesson
- LearnerState
- FramingRecord
- SignalPacket
- ImprovementProposal

### Slice 4 - Recipe Chain Registry

A YAML registry mapping:

```text
intent + RIU + boundary -> recipe chain
```

### Slice 5 - Integrity Hook

Before execution, call existing integrity logic:

```text
RIU completeness -> execution posture
```

Postures:

- `execute`
- `execute_with_limitations`
- `narrow_or_confirm`
- `research_or_reflect_first`
- `blocked_by_boundary`

### Slice 6 - BDB Legal Demo Path

Only wire:

```text
PROTECT -> RESEARCH -> DECIDE -> REFLECT
```

for:

```text
RIU-700 privilege risk
RIU-701 legal precedent research
RIU-708 settlement analysis
RIU-709 fiduciary duty analysis
```

That is enough to show the OS.

## The Final Creative Claim

The world has spent the last few years learning how to talk to models.

Palette should make that era feel primitive.

The next interface is not better prompting. It is governed intent.

A good AI system should not merely answer the sentence you typed. It should understand the professional act you are attempting, protect the boundaries around it, choose the right recipe, produce the right artifact, and remember the right lesson.

That is the shift:

```text
from prompts to intents
from chats to artifacts
from tools to recipes
from memory to typed experience
from automation to governed judgment
```

This is what Palette can be.
