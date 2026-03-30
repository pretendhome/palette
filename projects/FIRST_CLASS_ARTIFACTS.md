# First-Class Artifacts

**Author**: codex.implementation
**Date**: 2026-03-29
**Status**: Proposal

## Why This Matters

The system should not primarily be judged by the quality of its chat.

It should be judged by the quality of the persistent things it creates.

Those persistent things are the real product.

## First-Class Artifact Types

### 1. Decision Board

The live summary of:
- what we know
- what we believe
- what is missing
- what is blocked
- what needs input
- what can execute now

This is the primary orientation artifact.

### 2. Project State

The persistent machine-readable record of:
- mission
- facts
- gaps
- decisions
- blockers
- route hypotheses
- ownership

This is the substrate artifact.

### 3. Action Brief

A concise explanation of:
- the current route
- why it was selected
- what to do next
- what evidence supports it

This is the immediate execution artifact.

### 4. Evidence Pack

A structured bundle of:
- retrieved sources
- summaries
- citations
- unresolved evidence gaps

This is the trust artifact.

### 5. Plan

A time-bounded plan such as:
- 30-day plan
- weekly execution plan
- launch plan
- funding-readiness plan

This is the movement artifact.

### 6. Tracker

A persistent object for watching:
- blockers
- risks
- filings
- stakeholder actions
- document requests
- deadlines

This is the continuity artifact.

### 7. Brief / Memo

Short narrative outputs such as:
- board memo
- investor brief
- operator summary
- daily market brief
- weekly update

This is the communication artifact.

### 8. Draft Deliverable

A user-facing or external-facing output such as:
- email draft
- LP update
- regulatory response draft
- business plan section
- decision note

This is the labor-saving artifact.

### 9. Source Set

A reusable grouping of:
- uploaded docs
- live feeds
- approved sources
- workspace-specific knowledge inputs

This is the retrieval artifact.

### 10. Session Snapshot

A lightweight record of:
- what changed this turn
- what was created
- what was decided
- what remains unresolved

This is the re-entry artifact.

## Priority Order

If we need to narrow scope, prioritize:

1. Decision Board
2. Project State
3. Action Brief
4. Evidence Pack
5. Brief / Memo
6. Plan

Those six are enough to make the system feel valuable.

## Voice-to-Artifact Principle

The strongest experience pattern is:

1. user speaks or types
2. system interprets the request against workspace state
3. system produces one of the artifacts above
4. system saves it automatically
5. user can refine it conversationally

This means the first product loop is not:
- question -> answer

It is:
- intent -> artifact -> persisted state

## What Not To Make First-Class

Do not make these the primary user-facing unit:
- routes alone
- raw agent invocations
- taxonomies
- internal governance mechanics
- “persona kits”

Those are engine internals.
The user should feel the artifacts, not the machinery.

## Recommendation

Design every frontend around creation, inspection, and refinement of first-class artifacts.

If a conversation does not update state or produce a useful artifact, it should be treated as lower-value product behavior.
