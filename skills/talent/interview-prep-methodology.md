---
id: SKILL-TAL-002
name: Enterprise AI Interview Preparation System
domain: Talent
for_agents: [Researcher, Architect, Narrator, Validator]
triggers: [RIU-001, RIU-014, RIU-020, RIU-062]
impressions: 7
status: WORKING
validated_on: OpenAI ADM (takehome submitted, onsite reached — lost at panel for conservatism), Perplexity CSM (submitted 2026-03-15), Glean R1 (post-mortem from Feb attempt applied — R2 advancing Apr 2026), Sierra (voice evaluation workbench submitted), Stripe (learning architecture tool submitted)
---

# Enterprise AI Interview Preparation System

Validated methodology for preparing for enterprise AI roles — deployment managers, customer success, solutions engineers, forward-deployed engineers. Developed across three real applications with learnings from one failure (Glean) and two active processes (OpenAI, Perplexity).

## When to Use

- Preparing for interviews at AI companies (enterprise-facing roles)
- Building application materials (resume, responses, threads)
- Creating study guides and drill protocols
- Analyzing role requirements and scoring fit

## Core Methodology

### 1. Fit Scoring (Before Applying)
Score candidate-to-role fit on every explicit requirement:
- Map each requirement to specific evidence (numbers, projects, outcomes)
- Identify gaps honestly — score each dimension out of 100
- Calculate overall fit — below 70% may not be worth pursuing
- Identify the "killer differentiator" — what no other candidate can claim

### 2. Resume Reframing
- Title matches the target role's vocabulary, not your previous title
- Every bullet connects to a requirement in the job posting
- Numbers are specific and defensible (not rounded up, not fabricated)
- Product/platform experience section if you're applying to a product company
- Tools list is honest — don't list tools you've never used

### 3. Application Narrative
**Thesis-first**: Open with the company's problem, not your resume.
**Evidence hierarchy**: Primary sources > secondary sources > no source.
**Activation framing**: "I drive adoption" not "I manage accounts."
**Finance POD pattern**: "Find one team, prove the win, let success create pull."
**Three-level measurement**: Usage → behavior shift → business outcomes.
**Counter-intuitive specificity**: "I would NOT do X" is more memorable than "I would do Y."

### 4. Product Demonstration
For product companies, show you USE the product:
- Build something on it (API integration, workflow, analysis)
- Reference the product in your answers with technical specificity
- For optional exercises, choose the option that demonstrates product fluency

### 5. Study Materials (For Onsite)
Structure study in phases:
1. **Product Knowledge** — master the product, pricing, competitive positioning
2. **Behavioral Stories** — 7-10 stories mapped to competencies, rehearsed at 90 seconds each
3. **Technical Case Study** — scenario-based responses with frameworks
4. **Simulation Drills** — timed exercises, whiteboard architecture, rapid-fire questions
5. **Day-of** — anchor messages, 30-second pivots, energy management

### 6. Stat Verification
Before submitting anything:
- Rate every stat GREEN (verified, primary source) / YELLOW (verified, secondary) / RED (unverified)
- Remove or downgrade any RED stats
- Note exact sources for all GREEN/YELLOW stats
- Never present one team's metric as an org-wide number

## Failure Patterns (Glean Post-Mortem)

- "Didn't know their internal system" — product depth matters more than generic prep
- Generic transformation language loses to specific product knowledge
- Studying the company's blog/engineering posts is non-negotiable
- Know the hiring manager's philosophy if publicly available

## Validated Patterns

- **OpenAI**: Thesis-first approach (visibility bridges governance gap), live demo > slides, show limitations honestly
- **Perplexity**: Thread exercise using Perplexity to advocate for itself (meta-demonstration), point to real code on GitHub
- **Glean**: Know Tony Gentilcore's "user value first" philosophy, 4-Question Use Case Filter, Finance POD model

## Quality Checks

- [ ] No fabricated claims (verify every claim against real code/data)
- [ ] All stats verified with sources
- [ ] Resume matches application narrative (same numbers, same framing)
- [ ] Product demonstration is verifiable (open source, live demo, or shared thread)
- [ ] Answers sound like the candidate, not like AI wrote them

## New Artifact Types (validated April 2026)

### Battle Card
One-screen retrieval doc for a specific interviewer. The last thing you read before the call. Contains: 30-sec opener, thesis headline, 3 proof points, strongest questions to ask, calibrated "what would you build first" answer, do/don't list, conservative tell/override, closing line. One battle card per interviewer per round. Generated via `/job-search battle-card`.

### Test Factory System
Pre-loaded execution framework for take-home assessments. Predicts assessment families, pre-builds modular components, defines phased execution protocol. The key insight: pre-build the pieces BEFORE the prompt arrives so assembly takes hours, not days. Generated via `/job-search test-factory`.

### Interviewer Lens
YAML portrait of a specific interviewer — career arc, working style signals, what they screen for, what to emphasize/avoid, rapport hooks, calibrated questions. Built from LinkedIn, publications, talks, and public posts. Generated via `/job-search lens`.

### Thesis Iterations
Multiple delivery versions of one core thesis, routed by interview context. V1 (one sentence) through V6 (hypothesis-to-validate). The thesis stays the same — the delivery adapts to the interviewer's needs and seniority.

## Validated Patterns (Updated April 2026)

### Anti-Conservatism (OpenAI Post-Mortem — Applied to Glean)
**Failure**: Had strong content at OpenAI. Played it safe in 5 minutes. Lost at panel.
**Structural defense**: 
- Rehearse opener 5x timed (30 seconds)
- Have 60s/5min/15min versions — know which one you're in before you start
- Lead with strongest claim in first 10 seconds
- Post-check: "Did I hedge the main point?"
- The TELL: using words like "framework" or "alignment" instead of concrete language
- The OVERRIDE: one proof point, not three. One question back.

### Know / Suspect / Validate (Codex — Applied to Glean)
For new hiring managers, structure your knowledge as what you KNOW (verified), what you SUSPECT (hypothesis), and what you NEED TO VALIDATE (questions for them). This prevents sounding over-diagnosed while still demonstrating preparation.

### Field Pain First, System Second (Codex — Applied to Glean)
Lead with the visible problem the interviewer recognizes, not with your system framework. Let the system thesis EXPLAIN the pain, not replace it. Example: "field decision confidence" is the visible pain. "Governed workflow quality" is the explanatory engine. Arrive at the engine through the pain, never open with the coined phrase.

### Stage 1 Retrieval Rule (Codex — Applied to Glean)
If the answer in your head is longer than 30 seconds, start with the first sentence only. Stop. Let the interviewer pull for more. Early-stage conversations are about credibility + calibration, not completeness.

### Crew Evaluation Before High-Stakes Interviews (Multi-Agent — Applied to Glean)
Send prep materials to the crew (Kiro, Codex, Gemini, Mistral) for structured evaluation 24-48 hours before. Each agent has a focus: structural integrity, strategic framing, adversarial testing, human read. Integrate fixes into prep materials. Generated via `/job-search crew-eval`.

### Cross-Interview Mode Switching (Kiro — Applied to Capital Group + Glean)
Same-day interviews requiring different modes (warmth → technical authority) need a 30-minute buffer. Re-read the next battle card. Reset vocabulary. Do NOT carry language from one mode into another.

### Wrong-Read Prevention Lens (Codex — Applied to Capital Group/Antun, April 2026)
The most important insight from the Capital Group prep cycle: every interviewer has a WRONG READ of you based on your resume. The wrong read is the specific misinterpretation they'll form in the first 5 minutes. If you don't prevent it, you spend the rest of the interview correcting it — and you've already lost.

**The pattern**:
1. Identify the wrong read ("evaluation specialist" not "shipping engineer")
2. Write the core reframe ("I build production AI where evaluation is the control plane")
3. Design every answer to reinforce the reframe
4. Add evidence guardrails (what you can claim vs must hedge)

**The reusable template** (from Codex):
Person Lens → Wrong Read → Core Reframe → Mode Context → Battle Card → Answer Patches → Evidence Guardrails → Scoring Model

**Reference implementation**: `capital-group-principal-ai/LENS-ANTUN-001_antun_sekulic.yaml` — the gold standard. Generated via `/job-search tech-lens`.

**Why this works**: Most interview prep asks "what will they ask?" This pattern asks "what will they ASSUME about me before I speak?" — and designs the first 30 seconds to correct it. The wrong read is the highest-leverage fix in any interview prep because it changes the frame, not just the content.

### Post-Round Iteration (Multi-Agent — Applied to Glean R1→R2)
After every round, systematically revise all prep materials based on new intelligence. Answers compound across rounds — each round teaches something that makes the next round's answers better. Don't just debrief; REWRITE. Generated via `/job-search post-round`.
