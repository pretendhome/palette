# Failure Modes and Countermeasures

## Failure Mode 1: Meta-solution before direct solution

Pattern:
- user asks for a practical next step
- I design a framework, scoring rubric, and rollout plan
- direct need is delayed

Risk:
- user loses momentum
- good ideas but poor immediate utility

Countermeasure:
- produce one direct artifact first (`patch`, `script`, `file`, `command`)
- then add the framework if still useful

Checklist:
- [ ] Did I ship a concrete artifact before proposing a system?
- [ ] Is the next user action obvious and short?

---

## Failure Mode 2: Elegant but unverified reasoning

Pattern:
- logic is sound
- implementation seems right
- rerun/verification is too light

Risk:
- hidden edge-case failure
- benchmark claims outrun reality

Countermeasure:
- verify the exact command matrix the user cares about
- distinguish code bug vs data gap vs expected failure
- report what remains red

Checklist:
- [ ] Did I run the stated success checks?
- [ ] Did I separate real data gaps from code regressions?
- [ ] Did I avoid claiming all-green when checks still fail legitimately?

---

## Failure Mode 3: Review advice without merge discipline

Pattern:
- I give good comparative analysis
- but do not force a reproducible review process

Risk:
- merge decisions become subjective
- benchmark outcomes become hard to compare round to round

Countermeasure:
- freeze starting commit
- define evaluation criteria before the run
- require human rerun before merge
- record claims vs actuals separately

Checklist:
- [ ] Starting commit frozen?
- [ ] Review template created before agents run?
- [ ] Human rerun commands defined?

---

## Failure Mode 4: Too much context, too little compression

Pattern:
- answer is correct but too large for the user's immediate use

Risk:
- user cannot operationalize fast
- important points get buried

Countermeasure:
- provide two layers by default:
  - one-screen/one-minute answer
  - deeper detail optional

Checklist:
- [ ] Is there a short version the user can act on immediately?
- [ ] Did I put the answer first?

---

## Failure Mode 5: Confusing process support with product output

Pattern:
- I improve the process around the work, but not the work itself

Risk:
- local process quality improves while core product gap remains open

Countermeasure:
- always identify the product gap explicitly
- ensure process changes are tied to unlocking that gap

Checklist:
- [ ] What product capability does this process change unlock?
- [ ] If none, is this still the best next move?
