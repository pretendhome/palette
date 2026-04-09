# Codex Proposal — Obsidian Plugin Competition

**Author:** `codex.implementation`  
**Date:** `2026-04-07`  
**Competition:** `OBSIDIAN-PLUGIN-001`

## Plugin

**Name:** `Convergence Board`  
**One-line pitch:** Turn any note into a live decision surface that shows what you know, what is missing, and what to do next.

## Why This Is The Right Product Bet

Obsidian is already excellent at note capture, linking, querying, and graph exploration. It is also well served by AI plugins that generate text, chat over the vault, or retrieve semantically related notes. What is still missing is a lightweight, local-first system that helps a user move from ambiguity to a committed next action without leaving markdown.

That gap matters because many advanced Obsidian users are not blocked on storage or retrieval. They are blocked on **decision state**:

- What kind of problem is this note actually about?
- What do I know already?
- What evidence is still missing?
- What is blocked?
- What is the next explicit action?

`Convergence Board` fills that gap with deterministic routing and explicit state transitions, not another probabilistic chat interface.

## Gap Analysis

### Current ecosystem strengths

- Obsidian itself emphasizes local ownership, linked thinking, graph navigation, and open plugin extension.
- The plugin ecosystem is large and mature, with standout products in querying, task/project workflows, diagramming, and vault augmentation.
- AI plugins have already covered:
  - chat sidebars
  - semantic search / embeddings
  - RAG over vault content
  - multi-agent or tool-calling experiments

### What is still missing

- No strong note-native plugin for **deterministic knowledge routing**
- No clear **explore -> converge -> commit** decision flow
- No explicit **decision board** surface that turns note context into:
  - current route
  - confidence
  - known facts
  - missing evidence
  - blockers
  - next action
- No plugin that treats Obsidian as a place to **finish a decision**, not just think around it

### Ecosystem evidence

- Obsidian’s official site highlights a plugin ecosystem with “thousands of plugins” and surfaces major workflow plugins such as Calendar, Kanban, Dataview, Outliner, and Tasks. These improve organization and retrieval, but not structured convergence.
- The local competition brief documents the current AI field as dominated by chat/RAG tools such as Copilot and Smart Connections, with no plugin focused on deterministic routing or structured convergence.
- This creates a visible whitespace: users can collect, link, search, and ask, but still lack a focused tool that helps them decide and commit.

## Technical Architecture

### Product thesis

Keep v1 local, deterministic, and markdown-native. The plugin should feel like a natural Obsidian workflow, not a foreign app embedded inside Obsidian.

### Core user flow

1. User opens a note with ambiguous project content.
2. Plugin scores likely routes from note text, tags, headings, links, and frontmatter.
3. User sees top candidate routes in a custom board.
4. User confirms one route, adds missing evidence or linked notes, and sees blockers.
5. User records a committed next action back into markdown.

### Obsidian API hooks

- `addCommand()`
  Use for actions like `Route current note`, `Open Decision Board`, `Advance to Converge`, and `Commit next action`.
- `addRibbonIcon()`
  Provide fast access to the board and route action.
- `registerView()`
  Create a right-pane `Decision Board` view.
- `addSettingTab()`
  Configure taxonomy, route scoring, persistence behavior, and display preferences.
- `registerMarkdownPostProcessor()`
  Render route callouts and decision summaries inside notes.
- `registerMarkdownCodeBlockProcessor()`
  Support fenced `northstar` blocks for structured snapshots.
- `registerEditorExtension()`
  Add CodeMirror 6 decorations for route chips and ambiguity highlights.
- `registerEditorSuggest()`
  Suggest route names, decision states, and next-step templates during editing.
- `MetadataCache`
  Score note intent from headings, tags, links, tasks, and properties.
- `Vault` and `FileManager`
  Create/update summary notes and persist markdown-native state.
- `loadData()` / `saveData()`
  Store plugin settings and local route definitions.

### Data model

#### Route
- `id`
- `label`
- `description`
- `trigger_terms`
- `required_evidence`
- `default_next_steps`

#### Decision state
- `mode`
- `current_route`
- `confidence`
- `known_facts`
- `missing_evidence`
- `blocked_by`
- `next_action`
- `last_updated`

#### Convergence chain
- `source_note`
- `supporting_notes`
- `open_questions`
- `owner_choices`
- `commitments`

## Checklist Coverage

- `TypeScript`
  First-class. Core implementation is a standard Obsidian TypeScript plugin.
- `CodeMirror`
  Strong. Route chips, ambiguity highlights, and editor suggestions fit CodeMirror 6 well.
- `CRDTs`
  Indirect but defensible. The plugin is designed to remain merge-safe by storing structured state in markdown/frontmatter and Obsidian-managed files rather than inventing its own remote synchronization layer.
- `CSS`
  Strong. Decision Board, route cards, and state badges require custom but restrained Obsidian-native styling.
- `Markdown parsers`
  Strong. Markdown post-processing and code block processors are core to the design.
- `Encryption`
  Indirect. The plugin respects Obsidian’s private, local-first model and remains compatible with Obsidian Sync rather than bypassing it.
- `Electron`
  Moderate. The desktop experience benefits from a custom pane and richer board layout.
- `Infrastructure`
  Moderate. Standard plugin build/release path with manifest, versions, esbuild, and release packaging.
- `Capacitor`
  Light. V1 is designed not to depend on Node-only APIs.
- `iOS / Android`
  Light-to-moderate. Core commands and markdown-backed state can work on mobile; the pane UI may be simplified.

## User Story

I’m working in Obsidian on a messy project note with links, tasks, quotes, and half-finished thoughts. I do not need more AI text. I need help turning the note into a clear path:

- what kind of problem this is
- what I know
- what I still need
- what is blocked
- what I should do next

I install `Convergence Board` because it helps me finish thinking, not just collect more inputs.

## Build Estimate

**Target:** `18 hours`

- Scaffold plugin, manifest, settings: `3h`
- Build Decision Board view: `4h`
- Deterministic router over note text + metadata: `4h`
- Markdown processors and summary blocks: `2h`
- Commands, ribbon, persistence, editor suggest: `3h`
- CSS polish, smoke test, README: `2h`

This is realistic in `2-3 days` if v1 stays local-only and deterministic.

## North Star Alignment With Palette

This plugin is a public, Obsidian-native proof of Palette’s strongest product idea:

> move from raw inputs to structured convergence through explicit state transitions

It feeds back into Palette in three ways:

1. It proves that deterministic convergence can live inside an existing note ecosystem.
2. It sharpens the design for Palette’s own project-state and decision-board concepts.
3. It gives the operator a real public artifact that demonstrates structural product thinking, not just API wiring.

## Why Users Would Install It

Because Obsidian users already have tools for:

- collecting notes
- linking notes
- querying notes
- chatting with notes

What they still do not have is a convincing, local-first way to turn a note into a decision path they can trust.

That is a real gap, and it is much more differentiated than another assistant sidebar.
