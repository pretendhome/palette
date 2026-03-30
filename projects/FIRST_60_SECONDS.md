# First 60 Seconds

**Author**: codex.implementation
**Date**: 2026-03-29
**Status**: Proposal

## Goal

In the first 60 seconds, the user should feel:
- recognized
- oriented
- helped
- already in motion

The system should not spend the first minute explaining itself.
It should spend the first minute proving usefulness.

## Shared Experience Pattern

Whether the user enters through:
- web
- CLI voice
- Telegram

the same product logic should happen:

1. identify workspace
2. load state
3. surface context
4. invite action
5. produce first artifact fast

## State 1: Launch

The user starts the system:
- `./start.sh rossi`
- `./start.sh oil-investor`
- opens the workspace URL
- opens Telegram thread

Visible meaning:
- the system is loading *their mission*, not just opening a generic app

## State 2: Recognition

The system should immediately identify:
- workspace name
- user name or role
- current project state
- relevant context for today

Example:

“Mission Canvas active for Rossi.
Fundability status is 79, with 2 critical evidence gaps and 1 open revenue decision.”

Or:

“Mission Control active for [Investor Name].
WTI context loaded, 3 portfolio-relevant regulatory items detected, and 1 unresolved decision from yesterday is still open.”

## State 3: Offer Orientation

The system should not ask a blank “How can I help?”
It should provide structured orientation first.

Example:

“Right now the most useful things I can do are:
1. show what is blocked
2. brief you on what changed
3. draft the next artifact
4. help you decide the next move”

This reduces blank-screen paralysis.

## State 4: First User Input

The user should be able to respond naturally:
- “What changed?”
- “What’s blocking us?”
- “Draft the update.”
- “Summarize these files.”
- “Help me decide.”

No setup wizard.
No mode tutorial.
No taxonomy explanation.

## State 5: First Artifact

Within the first minute, the system should create one persistent useful object:
- a brief
- an evidence pack
- a blocker summary
- a plan
- a stakeholder update

This is the “aha” moment.

The user should feel:
- I said one thing
- it knew my context
- it made something useful
- it saved it

## State 6: Persistence Is Visible

The system should say or show:
- what it created
- where it lives
- how it changed workspace state

Example:

“Created: Today’s funding blocker brief.
Saved to your workspace.
Decision Board updated with 2 unresolved gaps.”

This is essential.
If persistence is invisible, the product feels like chat again.

## State 7: Easy Next Step

After the first artifact, the system should offer the next move:
- refine
- send
- save
- compare
- gather more evidence

Example:

“Next, I can:
1. turn this into a one-page memo
2. gather the missing evidence
3. draft the owner-facing decision note”

## Failure Handling

If voice fails:
- fall back to text immediately
- do not dramatize it

Example:

“Mic not available. Text input is active and your workspace is ready.”

If knowledge is missing:
- surface the gap clearly
- say why it matters
- suggest the fastest resolution path

## Product Rule

The first 60 seconds should create:
- orientation
- one artifact
- one visible state update

If any frontend cannot do that, it is not ready.
