# Unified Product Thesis — Mission Canvas + Workspace

**Author**: codex.implementation
**Date**: 2026-03-29
**Status**: Proposal

## Thesis

Mission Canvas and Agentic Workspace are not two separate products.

They are one system with:
- one **engine**
- multiple **frontends**
- multiple **workspace configurations**

The engine is the existing Mission Canvas stack:
- routing
- knowledge retrieval
- governance
- project-state
- session-state
- one-way-door handling
- decision logging

What changes per user is:
- the domain lens
- the entry modality
- the first-run experience
- the persistent workspace state

So the product is not:
- a chat app
- a prompt router
- a website builder
- a general “AI OS”

The product is:

**a decision-and-artifact engine that turns messy user intent into persistent, useful structure**

That structure includes:
- decisions
- briefs
- plans
- trackers
- evidence packs
- next actions
- workspace state

## Product Architecture

### Engine

The engine should remain the unified backend:
- `missioncanvas-site/server.mjs`
- `openclaw_adapter_core.mjs`
- shared RIU routing
- shared knowledge systems
- shared governance layer
- shared project-state model

### Frontends

The system should support three first-class frontends:

1. **Web**
- best for visible convergence
- strong for boards, gaps, and review workflows

2. **CLI / Voice**
- best for fast, focused interaction
- strong for executive or operator flow

3. **Telegram / Mobile**
- best for ambient access and capture
- strong for “while moving” use

These are not separate products.
They are separate doors into the same engine.

### Workspace Configurations

Each real deployment should be a workspace configuration, not a forked codebase.

Examples:
- `rossi`
- `oil-investor`
- future client workspaces

Each workspace should carry:
- `project_state.yaml`
- domain config
- greeting / FRX config
- allowed modalities
- source/retrieval config
- identity and notification config

## Core Product Promise

The user promise should be:

**“Talk to your mission, and the system turns it into working artifacts and live state.”**

Not:
- “talk to a bot”
- “fill out a form”
- “build a site”

The experience should feel like:
- the system understands the mission
- the system accumulates orientation
- the system produces useful outputs quickly
- the system keeps track of what matters over time

## What Users Actually Buy

Users do not buy:
- agent orchestration
- RIU routing
- governance logic

They buy:
- reduced ambiguity
- reduced cognitive load
- saved work
- continuity
- confidence
- better decisions

The system should therefore optimize for:
- orientation
- persistence
- artifact quality
- easy re-entry

## What Makes The Product Feel Real

The system feels real when:
- it remembers the mission
- it knows what is blocked
- it knows what changed
- it produces an artifact, not just an answer
- it shows the user what to do next

The system feels fake when:
- every turn starts from scratch
- it only produces generic chat
- it routes too early
- it cannot explain why it paused
- it creates text with no persistent consequence

## Strategic Product Direction

### Near-Term

Build the unified engine around:
- project-state
- decision board
- artifact generation
- voice/text interoperability

### Mid-Term

Make workspace creation cheap:
- new workspace = config + state + domain pack
- not new repo
- not new engine

### Long-Term

The long-term product is a **mission workspace platform**:
- one engine
- many missions
- many frontends
- domain packs on top

## Product Rules

1. **Artifact first, site second**
- the system should first create persistent useful objects
- rendering them as a site or workspace comes after

2. **Project-state over request-state**
- continuity is part of the product, not a nice-to-have

3. **Voice is a front door, not the whole house**
- voice should help users enter and operate
- persistent visual structure still matters

4. **Governance is part of UX**
- one-way-door handling, knowledge gaps, and pauses should feel native

5. **A new client should mean a new workspace config, not a fork**

## Recommendation

Treat Mission Canvas as the engine.
Treat Workspace / Mission Control as a packaged experience on top of that engine.

Do not split the product story.
Unify it around:

**decision convergence + artifact creation + persistent workspace state**
