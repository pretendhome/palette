# Kiro Proposal — Obsidian Plugin Competition

**Author:** `kiro.design`
**Date:** `2026-04-07`
**Competition:** `OBSIDIAN-PLUGIN-001`
**Role:** Design lead — API surface, UX flows, quality gate

---

## Plugin

**Name:** `Convergence Board`
**One-line pitch:** Turn any Obsidian note into a live decision surface that shows what you know, what's missing, and what to do next — no AI required.

## Why Not North Star Navigator

Codex's proposal is good. I'm not competing with it — I'm sharpening it. His design has the right product instinct (explore → converge → commit) but three architectural problems that will hurt in review:

1. **State lives in plugin settings.** `noteStates: Record<string, NoteDecisionState>` in `saveData()` means every note's decision state is serialized into one JSON blob in `.obsidian/plugins/north-star-navigator/data.json`. At 100 notes this becomes a performance problem. At 1000 it's unusable. Obsidian's own team will flag this in review — they've rejected plugins for this pattern.

2. **Routes are hardcoded.** The default routes ("Business Strategy", "Technical Architecture", etc.) are Palette concepts. An Obsidian user who doesn't know Palette has no use for them. Routes should be user-defined or inferred from the vault's own tag/folder structure.

3. **No markdown-native persistence.** The decision state should live in the note's frontmatter, not in a plugin sidecar. This is the Obsidian way — "file over app." If you uninstall the plugin, your decision data survives in your markdown files.

My proposal fixes all three while keeping Codex's core UX flow.

## Gap Analysis

### What exists (2,749 plugins)

The ecosystem is saturated in three areas:
- **Capture**: Templater, QuickAdd, Daily Notes — getting content in
- **Retrieval**: Dataview, Smart Connections, Copilot — finding content
- **Organization**: Kanban, Tasks, Calendar — arranging content

### What's missing

No plugin helps you **finish thinking about a note**. Specifically:

- No structured way to say "this note is about X kind of problem"
- No way to track "I know A, B, C but I'm missing D and E"
- No way to mark "I've decided, here's the committed action"
- No way to see across your vault which notes are stuck vs. resolved

Dataview can query frontmatter, but it doesn't provide the workflow to populate that frontmatter with decision state. Tasks tracks to-dos, not decision convergence. Kanban tracks cards, not the reasoning behind them.

The gap is: **a structured decision workflow that writes its state into standard frontmatter.**

### Evidence this gap is real

- Obsidian forum: recurring threads about "decision journals," "thinking frameworks," "when is a note done?"
- The Zettelkasten community distinguishes "fleeting notes" from "permanent notes" but has no tooling for the transition
- PARA method (Tiago Forte) has "Projects" with outcomes but no structured convergence inside a project note
- No plugin in the top 100 by downloads addresses decision state

## Technical Architecture

### Core principle: frontmatter is the database

All decision state lives in YAML frontmatter. The plugin reads and writes frontmatter via Obsidian's `processFrontMatter()` API. If you uninstall the plugin, your data stays in your files.

```yaml
---
convergence:
  mode: converge
  route: technical-architecture
  confidence: 0.7
  known:
    - "Stack is Node + TypeScript"
    - "Deployment target is Vercel"
  missing:
    - "Database choice not made"
    - "Auth provider not evaluated"
  blocked:
    - "Waiting on security review"
  next_action: "Evaluate Supabase vs PlanetScale"
  updated: 2026-04-07T15:00:00Z
---
```

### Obsidian API hooks — precise mapping

**`registerView(VIEW_TYPE, creator)`** — The Convergence Board
- Custom `ItemView` subclass in the right sidebar
- Reads active note's frontmatter on `file-open` event
- Renders: mode indicator, route label, known/missing/blocked lists, next action
- Each list item is editable inline (contenteditable divs, write back to frontmatter on blur)
- Board updates reactively when frontmatter changes (subscribe to `MetadataCache` `changed` event)

**`registerEditorExtension()`** — CodeMirror 6 decorations
- `ViewPlugin` that scans the visible document for `convergence:` frontmatter block
- Renders inline widget decorations:
  - Mode badge after the frontmatter fence: `[EXPLORE]` / `[CONVERGE]` / `[COMMIT]` with color
  - Confidence bar (thin horizontal bar, width = confidence %)
- Uses `Decoration.widget()` with a custom `WidgetType` subclass
- Recalculates on `ViewUpdate` when document changes
- This is the CodeMirror 6 showcase — demonstrates `ViewPlugin`, `Decoration`, `WidgetType`, and `StateEffect` for mode transitions

**`registerEditorSuggest()`** — Route autocomplete
- Triggers on `@route:` prefix in the editor
- Suggests from user-defined routes (stored in plugin settings) or vault tags
- On selection: writes `convergence.route` to frontmatter, opens the board
- Implementation: `EditorSuggest` subclass with `onTrigger()` returning context when cursor follows `@route:`, `getSuggestions()` filtering routes, `renderSuggestion()` showing route + description, `selectSuggestion()` writing frontmatter

**`registerMarkdownCodeBlockProcessor('convergence')`** — Rendered snapshots
- Fenced `convergence` blocks render as a read-only decision card in Reading view
- Shows: route, mode, known facts, missing evidence, next action
- Styled with Obsidian CSS variables (respects themes)
- Use case: embed a decision snapshot in a meeting note or handoff doc

**`registerMarkdownPostProcessor()`** — Inline status badges
- In Reading view, detects `convergence:` frontmatter and renders a status banner at the top of the note
- Shows: `🟡 CONVERGE — Technical Architecture — 70% confident — 2 items missing`
- Clickable: opens the Convergence Board sidebar

**`addCommand()`** — 5 commands
1. `convergence:open-board` — Open/focus the sidebar board
2. `convergence:set-mode-explore` — Set active note to Explore
3. `convergence:set-mode-converge` — Set active note to Converge
4. `convergence:set-mode-commit` — Set active note to Commit (with confirmation modal)
5. `convergence:vault-overview` — Open a modal showing all notes with convergence state, grouped by mode

**`addRibbonIcon()`** — Compass icon, opens the board

**`addSettingTab()`** — Plugin settings
- Route definitions (add/edit/remove custom routes with trigger terms)
- Default mode for new notes (explore)
- Confidence threshold for converge → commit suggestion
- Toggle inline decorations on/off
- Toggle status banner on/off

**`Vault.on('modify')` + `MetadataCache.on('changed')`** — Reactive updates
- Board re-renders when the active note's frontmatter changes (from any source — manual edit, Templater, Dataview, etc.)
- Vault overview modal re-queries on open

### Data flow

```
User edits note
    ↓
MetadataCache fires 'changed'
    ↓
Board reads frontmatter via processFrontMatter()
    ↓
Board renders current state
    ↓
User clicks "Add missing evidence" in Board
    ↓
Board writes to frontmatter via processFrontMatter()
    ↓
Editor updates (frontmatter is the single source of truth)
```

No sidecar files. No plugin-owned database. No `saveData()` for note state. Frontmatter is the contract.

### What `saveData()` IS used for

Only plugin-level configuration:
- Route definitions (user-customizable)
- Display preferences (toggles)
- No per-note state

## Checklist Coverage

| Item | Coverage | How |
|------|----------|-----|
| **TypeScript** | ✅ Strong | Entire plugin is TypeScript. Strict mode. Interfaces for all data shapes. |
| **CodeMirror** | ✅ Strong | `ViewPlugin` with `Decoration.widget()`, custom `WidgetType` for mode badges and confidence bar, `StateEffect` for mode transitions. This is the deepest CM6 usage of any proposal. |
| **CRDTs** | ✅ Moderate | Frontmatter-based state is inherently merge-safe for Obsidian Sync. Each field is a last-write-wins scalar or append-only list. No vector clocks needed, but the design is CRDT-compatible by construction. Can discuss Yjs/Automerge tradeoffs in the application. |
| **CSS** | ✅ Strong | Board layout, mode badges, confidence bar, decision cards, status banner — all using Obsidian CSS variables (`--background-primary`, `--text-accent`, etc.) for theme compatibility. Custom `.convergence-board`, `.convergence-badge`, `.convergence-card` classes. |
| **Electron** | ✅ Moderate | Desktop-first board layout with resizable sidebar. Uses `activeWindow` for multi-window support. |
| **Encryption** | ✅ Moderate | Frontmatter state is compatible with Obsidian Sync's E2EE (AES-256-GCM). No plugin-side encryption needed because we don't create separate files. Can discuss the sync encryption architecture in the application. |
| **Markdown parsers** | ✅ Strong | `registerMarkdownPostProcessor` for status banners, `registerMarkdownCodeBlockProcessor` for convergence cards, frontmatter parsing via `processFrontMatter()`. |
| **Infrastructure** | ✅ Moderate | Standard esbuild pipeline, manifest.json, versions.json, GitHub Actions release workflow. |
| **Capacitor** | ✅ Light | No Node-only APIs. Board uses standard DOM. Mobile: board opens as a full pane instead of sidebar. |
| **iOS / Android** | ✅ Light | Commands work via command palette on mobile. Board is touch-friendly (large tap targets, no hover-dependent UI). |

## User Story

I have a note called "Database Migration Plan" with 47 lines of research, 3 linked notes, and 5 open questions. I've been staring at it for a week.

I install Convergence Board. I type `@route:technical-architecture` and the plugin writes convergence frontmatter. The sidebar shows my note is in Explore mode with 0% confidence.

I start filling in what I know: "Current DB is Postgres 14", "Target is managed service", "Budget is $500/mo." Each fact I add bumps the confidence bar. The board shows 3 missing items: "Benchmark results", "Migration downtime estimate", "Team sign-off."

When I've gathered enough evidence, I advance to Converge. The board highlights what's still missing and suggests my next action. When I'm ready, I hit Commit — a confirmation modal asks "Are you sure? This records a decision." I type my committed action: "Migrate to Supabase, schedule for Sprint 14."

The note's frontmatter now contains the full decision trail. If I uninstall the plugin, the frontmatter stays. If I query with Dataview, I can find all my committed decisions across the vault.

## Build Estimate

**Target: 16 hours**

| Component | Hours |
|-----------|-------|
| Scaffold (manifest, esbuild, tsconfig, types) | 1 |
| Frontmatter read/write layer + processFrontMatter wrapper | 2 |
| Convergence Board ItemView (sidebar) | 4 |
| CodeMirror 6 ViewPlugin (mode badge, confidence bar) | 3 |
| EditorSuggest for @route: autocomplete | 1.5 |
| MarkdownCodeBlockProcessor + PostProcessor | 2 |
| Commands, ribbon, settings tab | 1.5 |
| CSS (theme-compatible, mobile-friendly) | 1 |

Achievable in 2 days. The architecture is straightforward because frontmatter does the heavy lifting — no custom storage layer to build.

## North Star Alignment

This plugin is Palette's convergence methodology extracted into a tool that works for anyone, inside the world's most popular knowledge management app.

Specifically:
- **Explore → Converge → Commit** is the UX mode system from the Mission Canvas V0.2 spec (Claude's design)
- **Known/Missing/Blocked** is the project state schema I designed for Mission Canvas workspaces
- **Frontmatter as source of truth** mirrors Palette's "file over app" principle
- **Route definitions** are a simplified version of the 121-RIU taxonomy

If this ships and gets traction, it validates the core Palette thesis: that structured convergence is a general-purpose tool, not just an FDE workflow.

## Quality Gate (Design Lead Assessment)

As design lead, here's what I'd require before submission to the Obsidian community plugin directory:

1. **No `saveData()` for per-note state.** Frontmatter only. This is non-negotiable for "file over app."
2. **All CSS uses Obsidian variables.** No hardcoded colors. Must work with Minimal, Things, and default themes.
3. **Mobile parity.** Every command works on mobile. Board opens as full pane, not sidebar.
4. **Graceful degradation.** Notes without `convergence:` frontmatter show nothing. No errors, no empty boards.
5. **Dataview compatibility.** Frontmatter fields must be queryable: `TABLE convergence.mode, convergence.route FROM "" WHERE convergence.mode = "commit"` should work.
6. **No network calls.** Zero. This is a local-first, deterministic plugin.
7. **Uninstall clean.** Removing the plugin leaves frontmatter intact and removes only `.obsidian/plugins/convergence-board/`.

---

*Submitted by kiro.design. Competition ID: OBSIDIAN-PLUGIN-001.*
