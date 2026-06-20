# Mythfall Convergence Brief

Date: 2026-05-18
Status: Fresh convergence pass
Owner: Michael / Codex working session

## Session Context

The March OpenAI take-home handoff is stale and should be ignored for Mythfall planning.
This brief starts a new May convergence pass on the best way forward to build Mythfall.

User-provided direction so far:

- It is May, so old March handoff files are not authoritative for this work.
- Start a full convergence brief on the best way forward to build Mythfall.
- Begin with Codex as the first working partner.
- Save the answers and push them to the repo or otherwise preserve them.

Local background references found in Palette:

- `wiki/entries/LIB-081-how-do-i-choose-between-client-server-an.md`
- `wiki/entries/LIB-082-what-can-a-small-team-under-20-people-re.md`
- `wiki/entries/LIB-084-what-game-engine-should-i-choose-for-web.md`

These references are treated as background only, not final authority.

## Working Recommendation

Build Mythfall as a tight 4-player co-op vertical slice first, not as a broad game platform.
Use Godot 4.6.x, GDScript, stylized 2.5D/3D or top-down/isometric presentation, authoritative server networking, and a tiny repeatable mission loop.

The core validation question is:

> Can Mythfall feel fun with four players in one 10-minute mythic run?

Everything else is secondary until that answer is yes.

## Technical Direction

Use Godot 4.6.x as the client baseline. Prefer GDScript if browser export remains a serious launch path because Godot 4 C# web export remains constrained.

Use authoritative client-server multiplayer instead of peer-to-peer.

Rationale:

- P2P has attractive hosting cost but higher product risk.
- NAT traversal failures and host advantage can damage early player trust.
- Authoritative server behavior is easier to test, observe, patch, and reason about.
- Mythfall needs reliable first-play multiplayer more than theoretical zero hosting cost.

Server options to evaluate during the spike:

1. Node/TypeScript authoritative WebSocket server with explicit game-state messages.
2. Colyseus if room management, matchmaking, and state sync are worth the dependency.

Do not overcommit to a networking framework before the first playable multiplayer moment exists.

## First Playable Scope

The first playable Mythfall should contain:

- 4 players max
- One arena or compact dungeon
- One enemy faction
- Three player roles/classes
- One shared objective
- One boss or finale event
- 8-12 minute session length
- Temporary run rewards only
- No account system unless required for playtest logistics

## Success Criteria

The first milestone is a proof milestone, not a content milestone.

- Four players can join the same session from separate machines.
- Players can move, attack, take damage, revive, and complete one objective.
- Server remains authoritative over health, enemy state, objective state, and match result.
- A new tester understands what to do within 60 seconds without explanation.
- At least 3 of 5 testers ask to replay after one run.
- The build can be deployed and relaunched without manual machine-specific setup.

## Non-Goals

For the first convergence phase:

- No MMO architecture.
- No open world.
- No permanent economy.
- No procedural world generator.
- No PvP.
- No account marketplace.
- No cinematic story system.
- No large asset pipeline.
- No final engine or networking abstraction before the vertical slice proves fun.

## One-Way Door Decisions

These decisions should not be locked until enough evidence exists:

- Engine choice after the first production month.
- Web-first versus desktop-first launch target.
- Authoritative-server protocol shape.
- Art perspective: top-down, isometric, or third-person.
- Whether Mythfall is session-based roguelite or persistent campaign co-op.

Default recommendation:

> Treat Mythfall as a session-based co-op roguelite until proven wrong.

This gives a small team replayability without requiring huge authored content.

## Immediate Next Steps

1. Define the one-sentence game promise:
   "Mythfall is a 4-player co-op mythic action roguelite where players combine class powers to survive short cursed expeditions."

2. Build a disposable network spike:
   Godot client connects to a local authoritative server; four players move in one room; the server owns or validates core state.

3. Build the combat toy:
   One class, one enemy, one attack, one dodge/block/skill, health, death, and revive.

4. Combine the network spike and combat toy:
   Four players fight synchronized enemies in one room.

5. Decide whether to formalize Colyseus, custom WebSocket, or another backend only after the first multiplayer moment exists.

## Current Decision

Do not start by designing the whole Mythfall architecture.
Start by forcing the smallest multiplayer moment to exist.
The architecture should serve that moment, not precede it.
