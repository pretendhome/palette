# Adaptive Intent Framework
## Palette's Heuristic Experience Layer
**Date**: 2026-05-27
**Status**: DRAFT — exhaustive list, pending crew merge
**Tag**: BDB-INTENTS

---

## The Concept

Palette is an OS. An OS needs more than a kernel — it needs **designed experiences** that guide professionals through governed workflows where each step uses the right model for the right reason.

These experiences are **intents** — not features, not agents, not tools. An intent is a defined entry point into a governed flow where:

1. Each step has a **purpose** and a **model assignment**
2. Between every step, **Palette checks**: did the classification hold? Should governance shift? Has the problem morphed?
3. The sequence can **branch, loop back, or switch intents** based on what Palette learns at each checkpoint
4. Every step routes through the **taxonomy** and **knowledge library** — Palette is a participant, not just an orchestrator

This is different from linear agent workflows (like the calvinfo plan → worktree → implement pattern). Those are fixed sequences. Palette's intents are **adaptive** — a CONVERGE can discover it needs to CREATE, a DIAGNOSE can discover the problem is actually a RESEARCH gap. The intents aren't silos. They're entry points into a governed flow that Palette steers.

### Why This Is the Moat

Nobody is doing adaptive, governed, multi-model intent sequences with an ontology in the middle. The closest comparisons:
- **CrewAI/LangGraph**: fixed agent graphs, no taxonomy, no governance checkpoints
- **Codex/calvinfo**: linear plan → build → review, manual model choice, no adaptation
- **Harvey/Legora**: single-model legal workflows, no multi-model orchestration
- **Redis**: memory infrastructure, no experience layer

Palette's intents are the **experience layer** on top of the OS — the thing that makes it feel like a product, not a framework.

### The Palette Checkpoint

Between every model call, Palette runs:
1. **Classification check**: Is this still the right RIU? Has the problem type changed?
2. **Knowledge check**: Did we learn something that changes the retrieval?
3. **Governance check**: Should the trust boundary shift? (e.g., query became privileged mid-flow)
4. **Intent check**: Should we branch to a different intent? (e.g., CONVERGE → CREATE)
5. **Compounding check**: Connect to prior decisions in the session

The checkpoint is what makes the system adaptive. Without it, you have a pipeline. With it, you have an OS.

---

## Exhaustive Intent List — By Lens

### Lens 1: The Professional Role

**What would each type of professional need as their primary workflows?**

#### INTENT-01: CONVERGE
*"I need to understand this problem from multiple angles and reach a judgment."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What kind of problem is this? | Taxonomy (local) | RIU assigned, governance tier set |
| 2. Retrieve | What do we already know? | KL + prior decisions (local) | Compounding signal |
| 3. Reason | What's the initial analysis? | Ollama (on-device) | Did local reasoning surface new questions? |
| 4. Research | What's missing from our knowledge? | Perplexity (governed) | Sanitization verified, gap identified |
| 5. Synthesize | How does research connect to context? | Claude (governed) | Did synthesis change the classification? |
| 6. Critique | What are we missing? What's the counter? | Mistral (governed) or Ollama (local) | Did critique reveal a new problem type? |
| 7. Store | Log everything, link decisions, propose improvements | Local | Gap signals filed, compounding updated |

*Who needs this*: Lawyers (case analysis), doctors (treatment planning), consultants (strategic recommendations), executives (investment decisions)
*Exits to*: CREATE (if convergence reveals something to build), RESEARCH (if gaps are too large), DIAGNOSE (if a flaw is found)

---

#### INTENT-02: CREATE
*"I need to build something new based on what I know."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What kind of artifact? | Taxonomy (local) | RIU assigned, scope defined |
| 2. Retrieve | What prior art exists? | KL + prior decisions (local) | Existing patterns found? |
| 3. Spec | Define what we're building | Claude (governed) | Spec reviewed against KL |
| 4. Build | Create the artifact | Kiro/Codex (governed) | Build matches spec? |
| 5. Review | Cross-check for quality | Codex (governed) | Overclaims? Missing pieces? |
| 6. Test | Verify it works | Automated + Gemini (governed) | Tests pass? Regressions? |
| 7. Critique | What would a critic say? | Mistral (governed) | Fundamental flaws? |
| 8. Rebuild | Incorporate feedback | Kiro/Claude (governed) | Better than V1? |
| 9. Store | Log artifact with provenance | Local | Decision trail complete |

*Who needs this*: Developers (code), founders (business plans), educators (curriculum), lawyers (briefs), marketers (campaigns)
*Exits to*: DIAGNOSE (if tests fail), CONVERGE (if scope is unclear), ITERATE (for V2+)

---

#### INTENT-03: DIAGNOSE
*"Something is broken and I need to fix it."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What kind of failure? | Taxonomy (local) | RIU assigned, severity assessed |
| 2. Isolate | Define the failure boundary | Gemini (governed) | Reproduction confirmed? |
| 3. Retrieve | What do we know about this failure class? | KL + prior decisions (local) | Similar past failures? |
| 4. Diagnose | Root cause (5 whys) | Local reasoning + Claude | Root cause found? Or need more data? |
| 5. Propose | Minimal fix specification | Claude (governed) | Fix matches root cause? |
| 6. Build | Implement the fix | Kiro/Codex (governed) | Fix is minimal? No scope creep? |
| 7. Verify | Confirm fix works | Automated tests + Gemini | Regression? New failures? |
| 8. Close | Memorialize the lesson | Local | KL proposal filed if pattern is new |

*Who needs this*: Developers (bugs), lawyers (case problems), doctors (differential diagnosis), support teams (escalations)
*Exits to*: CREATE (if fix requires new capability), CONVERGE (if root cause is strategic not technical)

---

#### INTENT-04: RESEARCH
*"I need to know everything about this before deciding."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What domain? What's the question shape? | Taxonomy (local) | RIU assigned, scope bounded |
| 2. Retrieve | What do we already know locally? | KL (local) | How much is already known? |
| 3. Gap analysis | What's missing? | Local reasoning | Specific gaps identified |
| 4. Parallel search | Multiple targeted queries | Perplexity × N (governed) | Each query shaped by taxonomy context |
| 5. Validate | Cross-reference results against KL | Local | Contradictions? Confirmations? |
| 6. Synthesize | Combine into coherent brief | Claude (governed) | Brief grounded in evidence? |
| 7. Store | File as new knowledge proposals | Local | KL entries proposed, evidence tiers assigned |

*Who needs this*: Lawyers (precedent research), analysts (market research), doctors (literature review), academics (systematic review)
*Exits to*: CONVERGE (if research reveals a decision needed), CREATE (if research reveals something to build)

---

#### INTENT-05: TEACH
*"I need someone to understand this — or I need to learn this myself."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What's the topic? What's the learner level? | Taxonomy (local) | RIU maps to curriculum module |
| 2. Retrieve | Get the enablement module + scaffolding | KL + enablement (local) | Module exists? Or gap? |
| 3. Present | Deliver content adapted to level | Claude/Voice (governed) | Level appropriate? |
| 4. Check | Verify understanding | Interactive Q&A | Comprehension confirmed? |
| 5. Adjust | Adapt based on response | Local reasoning | Misconception detected? Loop back? |
| 6. Apply | Guided practice exercise | Local + governed tools | Application successful? |
| 7. Assess | Verify competency | Structured assessment | Mastery threshold met? |
| 8. Store | Update learner state | Local | Competency record updated |

*Who needs this*: New hires (onboarding), students (education), professionals (upskilling), clients (product training)
*Exits to*: CREATE (if learner needs to build to learn), RESEARCH (if learner has questions beyond the module)

---

#### INTENT-06: EVALUATE
*"I need to assess quality, risk, or readiness."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What's being evaluated? Against what standard? | Taxonomy (local) | Evaluation criteria from KL |
| 2. Retrieve | Get the rubric/standard/checklist | KL (local) | Standard exists? Or create one? |
| 3. Analyze | Systematic assessment | Claude (governed) | Each criterion scored |
| 4. Evidence | Gather supporting data | Perplexity + local | Evidence mapped to criteria |
| 5. Compare | Benchmark against alternatives | Mistral (governed) | Relative positioning clear? |
| 6. Judge | GO/NO-GO verdict | Local reasoning | ONE-WAY DOOR check |
| 7. Store | Log evaluation with rationale | Local | Decision trail with evidence |

*Who needs this*: VCs (deal evaluation), lawyers (case merit), doctors (treatment options), managers (vendor selection), founders (build vs buy)
*Exits to*: CONVERGE (if evaluation reveals complexity), DIAGNOSE (if evaluation reveals a problem)

---

#### INTENT-07: PLAN
*"I need to break this into steps and assign work."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What kind of plan? | Taxonomy (local) | RIU assigned, scope bounded |
| 2. Retrieve | What prior plans exist for this type? | KL + prior decisions (local) | Templates? Precedents? |
| 3. Decompose | Break into workstreams/tasks | Claude (governed) | Decomposition complete? Dependencies? |
| 4. Assign | Match tasks to capabilities | Local reasoning | Right model/person for each task? |
| 5. Risk | Identify ONE-WAY DOOR decisions | Mistral (governed) | High-risk items flagged |
| 6. Sequence | Order by dependencies + priority | Local | Critical path identified |
| 7. Store | Log plan with assignments | Local | Plan traceable to RIU classification |

*Who needs this*: Project managers, founders, team leads, consultants
*Exits to*: CREATE (for each task), EVALUATE (for readiness checks)

---

#### INTENT-08: COMMUNICATE
*"I need to explain this to a specific audience."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What's the message? Who's the audience? | Taxonomy (local) | Audience lens identified |
| 2. Retrieve | What context does the audience need? | KL + person lens (local) | Audience profile loaded |
| 3. Frame | Shape the message for the audience | Claude (governed) | Framing matches audience? |
| 4. Draft | Create the communication artifact | Claude/Kiro (governed) | Artifact appropriate for medium? |
| 5. Critique | How would the audience react? | Mistral (governed) | Objections anticipated? |
| 6. Refine | Incorporate critique | Claude (governed) | Stronger than V1? |
| 7. Store | Log communication with audience context | Local | Decision trail includes framing rationale |

*Who needs this*: Executives (board presentations), lawyers (client updates), sales (proposals), educators (parent communications)
*Exits to*: CONVERGE (if communication reveals misalignment)

---

### Lens 2: Industry-Specific Intents

#### INTENT-09: PRIVILEGE CHECK (Legal)
*"Does this action expose privileged material?"*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What type of communication/action? | RIU-700 (local) | Privilege risk level assessed |
| 2. Scan | Detect privileged elements | Sanitizer (local) | PII/privilege markers found? |
| 3. Gate | Block or allow external routing | Governance (local) | BLOCK if privileged, ALLOW if public |
| 4. Store | Log the gate decision | Local | Audit trail for compliance |

*Fast path — designed to be < 1 second. Runs as a sub-intent inside any other intent.*

---

#### INTENT-10: MATTER WORK (Legal)
*"I'm working a legal matter — research, strategy, documents."*

Compound intent: sequences PRIVILEGE CHECK → RESEARCH → CONVERGE → CREATE, with matter context persistent throughout. Every step checks privilege before any external call.

---

#### INTENT-11: CLINICAL DECISION (Healthcare)
*"I need to make a treatment/diagnosis decision with evidence."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What clinical domain? | Taxonomy (local) | HIPAA governance activated |
| 2. Retrieve | Clinical guidelines + prior cases | KL (local) | Evidence-based guidance found? |
| 3. Research | Latest literature | Perplexity (governed, PHI stripped) | New evidence? Contradictions? |
| 4. Reason | Differential diagnosis / treatment options | Local + Claude (governed) | Options ranked by evidence tier |
| 5. Risk | Side effects, contraindications, interactions | Mistral (governed) | Risks flagged |
| 6. Decide | Treatment recommendation | Local (human-in-the-loop) | ONE-WAY DOOR: human approves |
| 7. Store | Clinical decision record | Local (HIPAA compliant) | Audit-ready documentation |

---

#### INTENT-12: COMPLIANCE AUDIT (Finance/Legal/Healthcare)
*"I need to verify we meet regulatory requirements."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | Which regulations apply? | Taxonomy (local) | Regulatory domain identified |
| 2. Retrieve | Applicable requirements | KL (local) | Requirements mapped |
| 3. Research | Current regulatory state | Perplexity (governed) | Recent changes? New guidance? |
| 4. Assess | Gap analysis against requirements | Claude (governed) | Gaps identified |
| 5. Risk | Exposure if gaps not closed | Mistral (governed) | Severity ranked |
| 6. Plan | Remediation roadmap | Local | Actions assigned |
| 7. Store | Audit record with evidence | Local | Compliance artifact |

---

#### INTENT-13: DEAL ANALYSIS (Finance/VC)
*"I need to evaluate an investment or transaction."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What kind of deal? | Taxonomy (local) | Deal type + jurisdiction |
| 2. Retrieve | Comparable deals, precedents | KL (local) | Comps found? |
| 3. Research | Market data, company intel | Perplexity (governed) | Current data gathered |
| 4. Model | Financial analysis | Local reasoning + Claude | Numbers grounded? |
| 5. Risk | What could go wrong? | Mistral (governed) | Downside scenarios |
| 6. Decide | GO/NO-GO with rationale | Local (human-in-the-loop) | ONE-WAY DOOR |
| 7. Store | Decision record with evidence trail | Local | Investment memo |

---

#### INTENT-14: LEARNING DESIGN (Education)
*"I need to create a learning experience for a specific learner."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What domain? What learner profile? | Taxonomy (local) | Learner level assessed |
| 2. Retrieve | Existing curriculum, ARON patterns | KL + enablement (local) | Prior modules found? |
| 3. Design | Learning objectives + structure | Claude (governed) | Objectives measurable? |
| 4. Build | Create content + exercises | Kiro/Claude (governed) | Content matches objectives? |
| 5. Adapt | Personalize for learner differences | Local reasoning | Accommodations built in? |
| 6. Store | Curriculum artifact with assessment rubric | Local | Reusable module |

---

#### INTENT-15: CLIENT INTAKE (Professional Services)
*"A new client or engagement is starting."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What kind of engagement? | Taxonomy (local) | Engagement type + risk tier |
| 2. Check | Conflicts, compliance requirements | Local (PRIVILEGE CHECK sub-intent) | Clear to proceed? |
| 3. Scope | Define deliverables, boundaries, non-goals | Claude (governed) | Scope documented |
| 4. Setup | Create workspace, assign governance tier | Local | Matter file / project file created |
| 5. Store | Engagement record | Local | Intake complete, ready to work |

---

#### INTENT-16: PITCH / PROPOSAL (Sales/Founders)
*"I need to persuade someone to act."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What's the ask? Who's the audience? | Taxonomy (local) | Audience lens loaded |
| 2. Retrieve | Prior pitches, audience research | KL + person lens (local) | What resonated before? |
| 3. Research | Audience's recent context | Perplexity (governed) | Current situation understood? |
| 4. Frame | Core argument + evidence | Claude (governed) | Argument grounded? |
| 5. Critique | How would they push back? | Mistral (governed) | Objections pre-empted |
| 6. Build | Create the artifact (deck, doc, email) | Kiro/Claude (governed) | Artifact matches medium? |
| 7. Rehearse | Practice delivery | Voice Hub (local) | Timing, clarity, confidence |
| 8. Store | Pitch record with outcome tracking | Local | Win/loss feeds future pitches |

---

#### INTENT-17: INCIDENT RESPONSE (Operations/Security)
*"Something went wrong in production. Fix it now."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What kind of incident? Severity? | Taxonomy (local) | Triage: P0/P1/P2 |
| 2. Contain | Stop the bleeding | Local + automated | Damage contained? |
| 3. Diagnose | Root cause (fast) | Gemini/Claude (governed) | Cause identified? |
| 4. Fix | Implement remediation | Kiro/Codex (governed) | Fix deployed? |
| 5. Verify | Confirm resolution | Automated tests | System stable? |
| 6. Post-mortem | What happened, why, how to prevent | Claude + Mistral (governed) | Lessons extracted |
| 7. Store | Incident record + KL proposal | Local | Pattern captured for future |

---

#### INTENT-18: NEGOTIATE (Legal/Business)
*"I need to reach an agreement with another party."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What kind of negotiation? | Taxonomy (local) | Stakes assessed, BATNA identified |
| 2. Retrieve | Prior negotiations, precedents | KL (local) | Comparable outcomes? |
| 3. Prepare | Position, interests, reservation point | Claude (governed) | Strategy grounded? |
| 4. Anticipate | Other party's likely positions | Mistral (governed) | Counter-arguments mapped |
| 5. Simulate | Role-play the negotiation | Voice Hub + Mistral | Practice under pressure |
| 6. Debrief | After each round, update strategy | Local | Position adjusted based on new info |
| 7. Store | Negotiation record with outcome | Local | Pattern feeds future negotiations |

---

#### INTENT-19: MONITOR
*"I need to watch for changes and alert when something matters."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What to watch? What triggers action? | Taxonomy (local) | Watchlist defined |
| 2. Configure | Set thresholds and check intervals | Local | Triggers validated |
| 3. Scan | Periodic check against sources | Perplexity (governed) + local | Signal detected? |
| 4. Filter | Is this signal above threshold? | Local reasoning | Noise vs signal |
| 5. Alert | Notify with context | Bus + Voice/Telegram | Alert delivered with action suggestion |
| 6. Store | Signal record | Local | Pattern accumulates over time |

*Already partially built: Joseph bot monitors, tech disruption theses*

---

#### INTENT-20: REFLECT
*"I need to look back at what happened and extract lessons."*

| Step | Purpose | Model | Palette Checkpoint |
|---|---|---|---|
| 1. Classify | What period/project/engagement? | Taxonomy (local) | Scope of reflection |
| 2. Retrieve | Decision trail, outcomes, gap signals | KL + session log (local) | Full history loaded |
| 3. Analyze | What worked, what didn't, why | Claude (governed) | Patterns identified |
| 4. Compare | Against initial goals/expectations | Local | Expectation vs reality |
| 5. Extract | Reusable lessons | Local | New KL entries proposed |
| 6. Improve | Update taxonomy, knowledge, agent maturity | Local (human-reviewed) | System gets better |

*This is the meta-intent — the one that makes all others improve over time.*

---

### Lens 3: Software Development (Adam's world)

#### INTENT-21: ARCHITECT
*"I need to design a system before building it."*

Steps: Classify problem → Retrieve patterns → Research state of art → Design (Claude) → Review tradeoffs (Mistral) → Document → Store

#### INTENT-22: IMPLEMENT
*"I have a spec. Build it."*

Steps: Load spec → Retrieve relevant code/patterns → Build (Kiro/Codex) → Test → Review → Fix → Ship

#### INTENT-23: DEBUG
*"This code is broken. Find the bug and fix it."*

Steps: Reproduce → Isolate → Diagnose (5 whys) → Fix (minimal) → Test → Regression check → Close

*(Similar to DIAGNOSE but code-specific)*

---

### Lens 4: Education (Claudia/ARON world)

#### INTENT-24: ASSESS LEARNER
*"I need to understand where this learner is."*

Steps: Classify domain → Present diagnostic → Evaluate responses → Map to competency framework → Identify gaps → Recommend path

#### INTENT-25: ADAPT SESSION
*"The learner is stuck/ahead/off-track. Adjust."*

Steps: Detect signal (stuck/skip/ahead) → Classify cause → Retrieve alternative approach → Present adapted content → Verify adjustment worked

*(Built from ARON's A→B→A session structure)*

---

### Lens 5: Founder/Executive

#### INTENT-26: DECIDE
*"I have a decision to make and I need to make it well."*

Steps: Classify decision type → Check: ONE-WAY or TWO-WAY door? → Gather evidence → Model options → Critique each → Decide → Store with rationale

#### INTENT-27: REPORT
*"I need to update stakeholders on status."*

Steps: Classify audience → Retrieve recent decisions/progress → Synthesize → Frame for audience → Draft → Critique → Deliver

#### INTENT-28: HIRE
*"I need to evaluate a candidate or build a job description."*

Steps: Classify role → Retrieve job framework → Research market comp → Design evaluation criteria → Build materials (JD, scorecard) → Store

---

### Lens 6: Cross-Cutting

#### INTENT-29: TRANSLATE
*"I need to move this knowledge from one domain/language/audience to another."*

Steps: Classify source domain + target domain → Retrieve both frameworks → Map concepts → Adapt language → Verify fidelity → Store translated artifact

*(This is comparative linguistics as a product feature — your core skill)*

#### INTENT-30: COMPOUND
*"I need to review what the system has learned and make it stronger."*

Steps: Read all gap signals → Cluster by RIU → Identify highest-priority gaps → Propose new KL entries → Propose new RIU nodes → Run auto_enrich → Update health → Store improvement record

*(This is auto_enrich elevated to an intent — the system improving itself as a first-class workflow)*

---

## Proposed Merge Categories

Before the crew review, here's my initial grouping of which intents likely merge:

| Core Intent | Absorbs | Rationale |
|---|---|---|
| **CONVERGE** | DECIDE, DEAL ANALYSIS | All are "reach a judgment from multiple inputs" |
| **CREATE** | IMPLEMENT, ARCHITECT | All are "build an artifact from a spec" |
| **DIAGNOSE** | DEBUG, INCIDENT RESPONSE | All are "find what's broken and fix it" |
| **RESEARCH** | MONITOR (partially) | Both are "gather knowledge from sources" |
| **TEACH** | ASSESS LEARNER, ADAPT SESSION, LEARNING DESIGN | All are "help someone learn" |
| **EVALUATE** | COMPLIANCE AUDIT | Both are "assess against a standard" |
| **COMMUNICATE** | PITCH, REPORT, NEGOTIATE | All are "persuade or inform an audience" |
| **REFLECT** | COMPOUND | Both are "look back and improve" |

That gives us **8 core intents** from 30 candidates. Could compress to 6-7 with further merging. The crew should decide.

---

## Sub-Intents (Always Available)

Some intents run as **sub-intents** inside any other intent:

- **PRIVILEGE CHECK** — fast-path, < 1 second, runs before any external call
- **STORE** — every intent ends with governed storage + compounding
- **PALETTE CHECKPOINT** — the adaptive check between every step

These aren't user-facing intents. They're OS primitives.

---

## What Makes This a Moat

1. **The sequences are governed, not hardcoded.** Palette checkpoints between every step can redirect the flow.
2. **The taxonomy is in the middle.** Every step routes through classification — the ontology shapes what each model sees.
3. **The intents are adaptive.** CONVERGE can become CREATE. DIAGNOSE can become RESEARCH. The OS steers.
4. **The system improves with use.** REFLECT/COMPOUND reads gap signals and proposes improvements. Each run makes the next run better.
5. **Nobody else has this.** Linear agent workflows exist (calvinfo, CrewAI). Fixed legal workflows exist (Harvey, Legora). Adaptive, governed, multi-model intent sequences with ontology checkpoints do not exist anywhere.

---

*Exhaustive list by claude.analysis. 30 intents across 6 lenses (professional role, industry, software development, education, founder/executive, cross-cutting). Pending crew merge to 5-7 core intents. 2026-05-27.*
