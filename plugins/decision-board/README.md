# Decision Board

Turn any note into a lightweight decision surface — what needs deciding, what's unclear, and what happens next.

## The problem

You have a note with research, links, and half-finished thoughts. You've been staring at it for a week. You don't need more information. You need to finish thinking about it.

## What this plugin does

Decision Board adds a small sidebar panel that helps you close a note:

- **What do you know?** — list the facts you've gathered
- **What's still unclear?** — name the gaps explicitly
- **What happens next?** — write the next action
- **Mark as decided** — record the decision when you're ready

All state lives in your note's YAML frontmatter. If you uninstall the plugin, your data stays in your files.

## Frontmatter

```yaml
---
status: thinking
next_action: "Evaluate Supabase vs PlanetScale"
known:
  - "Stack is Node + TypeScript"
  - "Budget is $500/mo"
missing:
  - "Migration downtime estimate"
  - "Team sign-off"
updated: 2026-04-08T20:00:00Z
---
```

Works with Dataview:

```dataview
TABLE status, next_action FROM "" WHERE status
```

## Commands

- **Open Decision Board** — open the sidebar
- **Cycle status** — Open → Thinking → Decided
- **Mark as Decided** — record a decision (with confirmation)
- **All Decisions** — see every decision note in your vault

## Installation

1. Open Settings → Community Plugins → Browse
2. Search "Decision Board"
3. Install and enable

## Design principles

- **File over app** — all state in frontmatter, nothing in plugin storage
- **No network calls** — fully local, fully offline
- **No methodology** — helps you finish thinking without imposing a framework
- **Theme compatible** — works with any Obsidian theme
- **Mobile ready** — all commands work on iOS and Android
