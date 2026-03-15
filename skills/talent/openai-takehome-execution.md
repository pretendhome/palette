---
id: SKILL-INT-001
name: OpenAI Takehome Execution
domain: Talent
for_agents: [Architect, Builder, Validator, Narrator, Researcher, Monitor]
triggers: [RIU-001, RIU-014, RIU-020, RIU-062]
impressions: 0
status: UNVALIDATED
validated_on: pending
---

# OpenAI Takehome Execution

Use for high-stakes interview assignments, especially technical-success, deployment, or case-study style work.

## What The Grader Likely Rewards

- Exact prompt coverage
- Customer reality, not abstract AI talk
- Technical credibility with explicit tradeoffs
- Safety, evaluation, and operational controls
- Reviewer-friendly structure
- A clear thesis that names the core tension in the problem

## What To Avoid

- Generic transformation language
- Unbacked claims
- Architecture with no adoption plan
- Adoption plan with no technical substance
- Hard-to-grade output shape

## Default Submission Shape

- Executive summary
- Governing thesis
- Main recommendation with tradeoffs
- Technical workflow or architecture detail
- Evaluation and monitoring plan
- Rollout and adoption plan
- What I would do next with more time
- Assumptions and open questions
- README or reviewer instructions for any artifact

## Useful HYDRA Imports

Take these ideas from benchmark-agent design only where they improve reviewer trust:

- Evaluator-first thinking: the grading lens and validation loop matter more than generating more drafts.
- Prompt classification up front: identify the assessment family quickly so the workflow fits the test.
- Adversarial review: create reviewer challenges designed to break your own answer before submission.
- Ensemble disagreement: if two strong drafts disagree, inspect the disagreement zone first.
- Rubber duck check: explain the recommendation simply; if the explanation is muddy, the submission is muddy.
- Anti-fragile perturbation: change one major assumption and see what collapses.

## Agent-Specific Guidance

**Researcher**
- Prioritize official OpenAI material first.
- Use Perplexity for current process signals and market reality.
- Separate facts from inference.
- Identify the likely prompt family early so the team does not overbuild the wrong response format.

**Architect**
- Compare at least 2 response shapes before choosing.
- Optimize for scoreability, not cleverness.
- Flag one-way doors early.
- Produce a thesis, not just a structure.
- The thesis should name the central tension or asymmetry driving the whole answer.

**Builder**
- Build only against the approved shape.
- Make artifacts runnable and easy to inspect.
- Include verification steps.

**Narrator**
- Reduce grader effort.
- Design the grader's first 60 seconds, not just the final polish.
- Make requirement coverage obvious.
- Check voice: this should read like a strong internal operator memo, not a candidate performing for approval.
- Cut any sentence that sounds inflated.
- Run a rubber-duck pass on the core recommendation.

**Validator**
- Check requirement coverage first.
- Fail anything with hidden assumptions in core recommendations.
- Treat missing metrics or missing risk controls as material gaps.
- Produce adversarial reviewer questions, not just checklist validation.

**Debugger**
- Triage only concrete failures found by Validator or Monitor.
- Fix the narrowest issue first.
- If a fix implies architecture drift, stop and route back to Architect for re-approval.
- After fixes, return to Validator rather than self-certifying readiness.

**Monitor**
- Track unresolved assumptions, missing artifacts, failing checks, and time remaining.
- Start tracking by phase-1, not just at the end.
- Emit `block` if the package is not defensible yet.
- Watch for process bloat: if workflow effort starts exceeding deliverable complexity, trigger compressed mode review.

**Orchestrator**
- Manage phase transitions and loop-backs.
- Trigger compressed mode when deadline or prompt shape makes the full workflow too heavy.
- Keep the workflow from becoming the deliverable.

## Submission Test

Before shipment, ask:
- Could a Technical Success lead hand this to a customer tomorrow?
- Could a technical reviewer challenge any major claim and get a coherent answer?
- Can a grader find every explicit requirement in under 2 minutes?

## Defense Rehearsal

- Prepare 5-7 likely grader questions from your weakest assumptions and strongest claims.
- Prepare one question that attacks your thesis directly.
- Prepare one answer that begins with "I don't know yet, but here is how I would find out."
- Rehearse 60-second answers, not 5-minute monologues.
- Add one rubber-duck explanation: explain the entire recommendation as if to a smart new teammate.

## Compressed Mode

Use compressed mode when the deadline is under 6 hours, the prompt is tightly bounded, or the output format is obvious.

- Merge convergence, research, and architecture into one short block.
- Start building by hour 2.
- Skip remediation unless a critical or high-severity issue appears.
