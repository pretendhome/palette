# Palette Grounding Use Cases

**Purpose**: Keep the traversal function and all system decisions anchored to real people with real needs. Every architectural choice should be testable against at least one of these.

**Date**: 2026-02-25

---

## UC-1: Rossi Mission — Small Business, Zero Tech

**Who**: Small business owner, no technical experience
**Channel**: Telegram chatbot (must be conversational, no dashboards)
**Core need**: "What do I do next?" — actionable next step, not options
**Key constraint**: Interface must be super easy to understand. No jargon. No choices that require technical knowledge to evaluate.
**Unique requirement**: Ideas and decisions must be logged and integrated back. The system must reinforce that the user IS the expert on what should be done — they just don't know how. The tool handles "how," the user owns "what."
**Tests traversal by**: Can Palette take a vague business goal, resolve it to an RIU, route to a service, and return a single clear next step in plain language?

---

## UC-2: La Scuola / Alpha — Claudia Canu, Expert Outside Her Domain

**Who**: PhD, 17 years program management and teaching experience. Tasked with designing an AI-integrated high school curriculum.
**Core need**: Bridge between what she knows deeply (pedagogy, program design) and what she doesn't (AI tooling, technical implementation) — in a way that makes her MORE confident, not less.
**Key constraints**:
- Output must be good out of the box — she won't feel comfortable changing it AND she knows exactly what quality looks like for the educational outcome
- Must produce deliverables consumable by other school leadership who themselves don't understand the tech
- Needs a specific voice for the high school design
**Unique requirement**: The system must respect her expertise. It's not teaching her — it's extending her reach into domains she hasn't worked in. Confidence-building, not skill-building.
**Tests traversal by**: Can Palette take a domain-expert's goal, route through knowledge + service options, and produce implementation-ready output that the expert trusts without needing to validate the technical parts?

---

## UC-3: Mythgall Game — Adam, Teenager Builder

**Who**: Teenager, making and playing games since age 8, cannot code
**Core need**: Bridge between what he can imagine and what he can build. Step-by-step instructions. All dirty work handled.
**Key constraints**:
- Must be spoonfed — every step explicit
- Must connect imagination to implementation without requiring coding knowledge
- Step-by-step, not overview
**Unique requirement**: The tool IS the bridge. It doesn't explain options — it picks the right path and walks him through it.
**Tests traversal by**: Can Palette resolve "I want X in my game" to specific tooling + integration recipe + sequential build instructions, without ever asking the user to make a technical decision?

---

## UC-4: Energy Executive (In Development)

**Who**: Real executive in the energy sector
**Core need**: Tool built backwards from the executive lens (LENS-EXEC-001), catered to his specific needs
**Status**: Demo target for Friday. Will validate whether role lens + traversal can produce exec-ready output for a specific industry context.
**Tests traversal by**: Can the executive lens shape traversal output into decision-ready briefings for a non-tech industry vertical?

---

## UC-5: Elia Canu — Dating Startup (In Development)

**Who**: Startup founder, identifies client needs and proactively finds matches on the web, sets up communication, coaches through the process
**Core need**: Client identification → outreach → coaching pipeline
**Status**: Early. Interesting because it tests Palette's ability to support a human-in-the-loop matching and communication workflow.

---

## How to use this file

When evaluating any architectural decision for the traversal function, routing, or lenses:
1. Would this work for Rossi? (zero tech, needs one clear answer)
2. Would this work for Claudia? (deep expertise, needs confidence not education)
3. Would this work for Adam? (pure imagination, needs every step spelled out)

If the answer is "no" for any of them, the design needs adjustment.
