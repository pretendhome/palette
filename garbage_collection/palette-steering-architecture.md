# Palette Hierarchical Steering Architecture

## What This Document Is

This explains how we structure AI-assisted development across multiple projects using a **hierarchical steering system**. The goal is to have one global source of truth that cascades into project-specific guidance — so every project inherits core principles while maintaining its own decision history and context.

---

## The Problem We're Solving

When working with AI agents (like Kiro/Claude) on multiple projects:

1. **Consistency**: We want the same core principles everywhere — reversibility, decision tracking, convergence
2. **Isolation**: Each project needs its own decision log and context — they shouldn't bleed into each other
3. **Simplicity for Engineers**: An engineer on a game project shouldn't need to understand the full toolkit architecture — they need guidance specific to their work
4. **Restartability**: Anyone should be able to pick up any project from `decisions.md` alone

---

## The Three-Layer Architecture

```
LAYER 1: GLOBAL (Immutable Core)
────────────────────────────────
~/.kiro/steering/
├── palette-core.md          ← Universal principles (never changes per project)
└── assumptions.md           ← Experimental patterns being tested globally

LAYER 2: VERTICAL (Project-Type Templates)
──────────────────────────────────────────
~/.kiro/steering/verticals/
├── game-dev/
│   ├── game-core.md         ← Game development principles
│   └── game-assumptions.md  ← Game-specific agent patterns
├── data-pipeline/
│   └── pipeline-core.md     ← Data engineering principles
└── web-app/
    └── webapp-core.md       ← Web application principles

LAYER 3: PROJECT (Instance-Specific)
────────────────────────────────────
~/projects/blox-game/
├── steering/
│   ├── game-core.md         ← Copied/inherited from verticals/game-dev/
│   ├── decisions.md         ← THIS PROJECT's decisions (append-only)
│   └── adam-prompts.md      ← Engineer-specific Kiro prompts
└── repo/
    └── [actual code]
```

---

## Authority Cascade (What Wins on Conflict)

```
1. palette-core.md         ← ALWAYS WINS (immutable)
   ↓
2. verticals/game-dev/     ← Wins over project-specific
   ↓
3. projects/blox-game/     ← Working surface (most specific)
```

**Example**: If `palette-core.md` says "never make one-way door decisions without confirmation" and a project-level prompt says "proceed autonomously" — the core wins. One-way doors always require confirmation.

---

## What Lives Where

### Layer 1: `palette-core.md` (Global)

This file contains principles that are **always true, for every project**:

- **Convergence**: How we align intent → capabilities → solution
- **Decision Classification**: One-way doors vs two-way doors
- **Glass-Box Operation**: Decisions must be transparent and traceable
- **Semantic Blueprint**: Every engagement needs Goal, Roles, Capabilities, Constraints, Non-goals
- **Failure Handling**: How to respond when things break
- **Operating Priorities**: Safety > Trust > Alignment > Progress > Elegance

**You should rarely edit this file.** When you do, it affects everything.

### Layer 2: `verticals/game-dev/game-core.md` (Project-Type)

This file contains principles specific to **game development projects**:

- Server-authoritative architecture requirements
- Real-time networking constraints (sub-100ms latency)
- Cost-per-user thinking
- Asset optimization targets (<10MB initial load)
- Anti-cheat baseline expectations
- Godot/Socket.io/Vultr stack assumptions (if standardized)

**Edit this when you learn something that applies to ALL game projects.**

### Layer 3: `projects/blox-game/decisions.md` (Project Instance)

This file is the **single source of truth for this specific project**:

- Semantic Blueprint (current state)
- Selected RIUs and why
- One-way door decisions with rationale
- Artifacts created/updated
- Open questions
- Post-mortems when things fail

**This is append-only.** Never delete or rewrite history. Always add a new block.

---

## How an Engineer (Adam) Experiences This

Adam doesn't need to understand Palette internals. He gets:

### 1. `game-core.md` — The Rules

A simplified document that tells him:
- What "done" looks like for this project
- How decisions are classified (reversible vs not)
- When to pause and ask vs proceed autonomously
- What artifacts he's responsible for

### 2. `adam-prompts.md` — The Playbook

Specific Kiro prompts for each phase of work:
- "Initialize project structure"
- "Create game server with Socket.io"
- "Implement core combat mechanics"
- etc.

### 3. `decisions.md` — The History

The append-only log that tells him:
- What was already decided
- What RIUs are active
- What's blocked/open
- What to do next

**Adam's workflow:**
1. Read `decisions.md` to see current state
2. Execute the next step using appropriate Kiro prompt
3. Validate the output
4. Append progress to `decisions.md`

---

## Why This Matters

### For the Operator (You)

- **One global truth**: `palette-core.md` is your bible — maintain it once, apply everywhere
- **Reusable verticals**: Build `game-dev/` once, use for every game project
- **Project isolation**: Each project has its own `decisions.md` — no cross-contamination
- **Handoff-safe**: Anyone can restart any project from its `decisions.md`

### For the Engineer (Adam)

- **Clear scope**: He knows exactly what applies to him
- **No cognitive overload**: He doesn't need to understand Palette toolkit internals
- **Traceable decisions**: He can always see why something was decided
- **Agentic-first**: Prompts are designed for AI-assisted execution

### For the System

- **Restartable**: Delete everything except `decisions.md` and steering files — you can rebuild
- **Debuggable**: Every one-way door has recorded reasoning
- **Evolvable**: Promote patterns from project → vertical → core as they prove reliable

---

## Quick Reference: What Goes Where

| Question | Answer |
|----------|--------|
| "Should this principle apply to ALL projects?" | → `palette-core.md` |
| "Should this apply to all GAME projects?" | → `verticals/game-dev/game-core.md` |
| "Is this specific to THIS game?" | → `projects/blox-game/decisions.md` |
| "Is this a prompt for Adam to execute?" | → `projects/blox-game/adam-prompts.md` |
| "Is this experimental and might change?" | → `assumptions.md` (global) or project-level |

---

## Setting Up a New Project

```bash
# 1. Create project structure
mkdir -p ~/projects/new-game/steering
mkdir -p ~/projects/new-game/repo

# 2. Copy vertical template
cp ~/.kiro/steering/verticals/game-dev/game-core.md ~/projects/new-game/steering/

# 3. Initialize decisions.md with first engagement update
# (Palette will generate this)

# 4. Create engineer prompts (if applicable)
touch ~/projects/new-game/steering/engineer-prompts.md

# 5. Initialize git repo
cd ~/projects/new-game/repo
git init
```

---

## The Golden Rules

1. **`palette-core.md` is immutable during execution** — change it between projects, not during
2. **`decisions.md` is append-only** — never rewrite history
3. **One-way doors require confirmation** — always, no exceptions
4. **Vertical templates are reusable** — don't put project-specific stuff there
5. **Engineers get simplified views** — they don't need the full toolkit
6. **Everything must be restartable** — if you can't rebuild from `decisions.md`, something is missing

---

## Example: Blox Fruits Game Project

```
~/projects/blox-game/
├── steering/
│   ├── game-core.md           ← From verticals/game-dev/ + project customizations
│   ├── decisions.md           ← All decisions for THIS game
│   └── adam-prompts.md        ← Kiro prompts for Adam
│
└── repo/
    ├── client/                ← Adam owns (Godot project)
    ├── server/                ← Shared (Node.js + Socket.io)
    ├── shared/                ← Shared (protocols, types)
    ├── deployment/            ← Operator owns (Docker, CI/CD)
    └── docs/                  ← Shared
```

**Authority for this project:**
1. `~/.kiro/steering/palette-core.md` — wins on conflict
2. `~/projects/blox-game/steering/game-core.md` — game-specific rules
3. `~/projects/blox-game/steering/decisions.md` — project history and state

---

## Summary

This architecture gives you:

- **Global consistency** through `palette-core.md`
- **Domain expertise** through vertical templates
- **Project isolation** through per-project `decisions.md`
- **Engineer simplicity** through curated steering files
- **Full restartability** through append-only decision logs

The system scales from one project to many, and from one engineer to a team — without losing the core principles that make AI-assisted development reliable.
