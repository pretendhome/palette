# Mission Canvas — System Reflection and CX Sweep

Author: codex.implementation  
Date: 2026-03-28  
Purpose: reflect on the system after concrete implementation work, identify what should be redesigned if starting from the current state, and highlight the likely customer experience path.

---

## Executive View

Mission Canvas is now real enough to critique honestly.

That changes the conversation.

At the beginning, the temptation was to think about:
- endpoint contract
- UI wiring
- routing logic
- fetch_signals
- peer coordination

Those were necessary.
But now that the local runner works, the more important question is:

**What kind of product is this actually becoming for a user?**

My answer:

It is not primarily a chat product.
It is not primarily a prompt router.
It is not primarily a planning form.

It is a **decision-convergence system**.

If we started from that truth, I would design the system differently.

---

## What The System Is Good At Now

The current system already has several strong foundations:

1. **Local-first trust boundary**
- The architecture is appropriately biased toward local processing
- This is the right default for sensitive work

2. **Structured routing**
- The RIU / routing layer is materially better than ad hoc prompting
- The system now has a meaningful contract surface and ranking logic

3. **Policy visibility**
- One-way-door treatment, decision logging, and knowledge-gap surfacing are the right kinds of controls

4. **Voice-first interaction**
- This is a real differentiator if done well
- For a user with partial ideas, voice is a better front door than a blank structured form

5. **Glass-box orientation**
- The system is trying to expose why it did something, not just what it did
- That is the right product philosophy

These are not small wins.
They mean the system has a serious spine.

---

## What I Would Do Differently If Starting Now

## 1. I would design around project-state, not request-state

The current architecture still centers the individual request too much.

That means:
- objective
- context
- desired outcome
- constraints
- route
- brief

That is good for a single interaction.
It is weak for an actual implementation or long-running project.

If starting now, I would make the primary object:

`Project State`

Not:

`Current Request`

Project state would explicitly track:
- current objective
- known facts
- missing evidence
- open decisions
- blocked actions
- current route hypothesis
- confidence in that route
- owner-facing next decisions
- operator-facing next tasks

That one shift would make the whole product feel less like a smart form and more like an operating system for convergence.

---

## 2. I would separate three UX modes clearly

Right now, several interaction modes are mixed together:
- exploratory thinking
- structured routing
- execution guidance

Those are not the same user state.

If starting now, I would make three explicit modes:

1. **Explore**
- user is messy
- system helps extract signal
- no premature routing confidence

2. **Converge**
- system turns ambiguity into a stable decision frame
- identifies missing evidence, open decisions, and competing routes

3. **Commit**
- user has enough clarity to choose a route
- logs decision
- applies one-way-door policy if needed

This would dramatically improve the customer experience because right now the product risks moving from “I’m still figuring this out” to “here is your route” too quickly.

---

## 3. I would make the primary output a Decision Board, not just an Action Brief

The current Action Brief is useful, but it is still document-shaped.

If I were restarting from here, I would make the central output a persistent **Decision Board** with sections like:
- What we believe
- What we know
- What we do not know
- What is blocked
- What needs owner input
- What can execute now
- Which route is leading
- Which alternatives were rejected

Then the Action Brief becomes a derivative artifact, not the core product surface.

This would improve CX because users generally do not need “more text.”
They need:
- orientation
- confidence
- next step clarity

---

## 4. I would design the system to preserve ambiguity longer

The current system is improving, but routing still exerts pressure too early.

That can make the UX feel smarter than it really is.

In practice, users often begin with:
- mixed goals
- unstated constraints
- contradictory desires
- missing evidence

If the system routes too early, it gives a false sense of convergence.

If I were restarting now, I would introduce an explicit state like:

`status: needs_convergence`

and keep it visible longer.

Meaning:
- “Here are the top 3 plausible routes”
- “Here is why the system is not ready to collapse to one”
- “Here are the 2 inputs that would change the decision”

That would make the system more trustworthy.

---

## 5. I would make personas secondary and lenses primary

The current persona layer is helpful, but it is too broad.

“Business Owner” or “Game Builder” is not the deepest distinction that matters during real use.

The more useful distinction is:
- owner lens
- operator lens
- advisor lens
- evaluator lens

These lenses change the answer structure, not just the example wording.

This matters because customer experience is not only about what the user is working on.
It is also about **what kind of decision they are trying to make right now**.

If we had started from the concrete system we have now, I would have prioritized:
- response lensing
- decision role framing

before persona kits.

---

## 6. I would treat knowledge gaps as first-class UX objects

Right now, knowledge-gap detection exists, which is good.
But it still feels like a backend status, not a user experience primitive.

If starting now, I would make every knowledge gap visible as:
- what is missing
- why it matters
- who can resolve it
- whether it is evidence, retrieval, or decision-state missingness

There are really three different gap types:

1. **Retrieval gap**
- we do not have enough library coverage

2. **Evidence gap**
- the user has not supplied the facts

3. **Decision gap**
- the facts exist, but a human must choose

If the system does not distinguish those clearly, users will experience the same vague frustration:

“Why can’t it just tell me what to do?”

This is a major CX point.

---

## 7. I would design one-way-door UX much earlier

The technical policy exists, and the hardening work is going in the right direction.
But from a CX perspective, one-way-door handling should not feel like an exception bolt-on.

It should feel like a natural shift in interface mode:

- exploration mode
- recommendation mode
- gated decision mode

The user should feel:
- why the system paused
- what exactly is irreversible
- what approval means
- what will happen after approval

That is not only a safety feature.
It is a trust feature.

---

## 8. I would unify voice and structured refinement more deliberately

Voice is one of the strongest ideas in the system.
But the current pattern is still:
- speak
- translate
- edit form
- route

That works.
But if I were redesigning now, I would make the loop feel more conversational:

- user speaks
- system extracts and reflects back structure
- user confirms or corrects only the unstable parts
- system converges in place

In other words:

less “speech-to-form”
more “speech-to-convergence”

That would feel materially better.

---

## 9. I would design around recurring implementation rhythms

The Rossi bridge surfaced something important:
real projects repeat the same inquiries.

Examples:
- what is blocked
- what changed
- what is missing
- what decisions are waiting
- what is the next funding move

If I were starting now, I would design recurring views from day one:
- status
- gaps
- decisions
- risks
- evidence
- next actions

That is better CX than making the user restate those needs as fresh prompts forever.

---

## The Real CX Journey

If this system becomes good, I think the ideal customer experience looks like this:

1. User arrives messy
- voice or typed
- partial goal
- uncertain framing

2. System reflects structure back
- here is what I think you mean
- here is what is still unclear

3. System helps converge
- here are the likely routes
- here is missing evidence
- here is the owner decision vs operator task split

4. System stabilizes project state
- not just a one-off answer
- a persistent working map

5. System gates irreversible actions clearly
- no surprises
- no hidden transitions

6. System leaves an audit trail
- not because compliance asked
- because users need to trust their own path

That is the experience worth building.

---

## Product Risk If We Don’t Adjust

If we do not make these shifts, the likely failure mode is:

the system becomes a very sophisticated router with a good demo and weak staying power.

It will feel impressive in first contact, but users will drift away because it will not hold project-state or decision-state strongly enough to become indispensable.

That would be a waste, because the foundations are strong enough to do something more ambitious.

---

## Bottom Line

If I were starting now, I would:

1. center project-state over request-state
2. split UX into Explore / Converge / Commit
3. make Decision Board the primary output
4. preserve ambiguity longer
5. prioritize lenses over personas
6. elevate knowledge gaps into first-class UX
7. design one-way-door gating as a natural interface transition
8. make voice a convergence interface, not just a form-filling interface
9. build recurring implementation views early

The system we have is good enough to justify this level of redesign thinking.

That is a positive sign.
