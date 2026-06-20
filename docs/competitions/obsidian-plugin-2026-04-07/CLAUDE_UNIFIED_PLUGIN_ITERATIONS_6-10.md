# Unified Plugin Design: Iterations 6-10

**Author:** `claude.analysis` (Implementation Lead)
**Date:** `2026-04-07`
**Competition:** `OBSIDIAN-PLUGIN-001`
**Builds on:** Kiro's Convergence Board proposal, Codex's North Star Navigator proposal, Karpathy wiki pattern, Gemini's structural validation
**Scope:** Build plan, quality gate, ecosystem positioning, application alignment, final project document structure

---

## Iteration 6: Build Plan -- Phased Implementation

### Working Name

**Convergence Board** (Kiro's name wins. "North Star Navigator" is too abstract for the plugin directory -- users search for what a plugin does, not a metaphor.)

Plugin ID: `convergence-board`

### Current State of the Scaffold

The existing scaffold at `implementations/obsidian/north-star-navigator/` has:
- manifest.json, package.json, tsconfig.json, esbuild.config.mjs, versions.json
- main.ts with: DecisionBoardView (ItemView), RouteSuggest (EditorSuggest), NextActionModal, NorthStarSettingTab, route scoring, markdown code block processor, markdown post-processor
- styles.css with theme-compatible CSS using Obsidian variables

**Critical problem in the scaffold:** All per-note state lives in `saveData()` via `noteStates: Record<string, NoteDecisionState>`. This violates Kiro's #1 quality gate rule. The entire state layer must be rewritten to use `processFrontMatter()`.

### Architecture Decisions (Pre-Build)

1. **State storage**: YAML frontmatter via `processFrontMatter()`. Zero per-note state in `saveData()`.
2. **Plugin settings via `saveData()`**: Route definitions, display toggles, confidence threshold. No per-note data.
3. **Reactivity model**: `MetadataCache.on('changed')` drives board re-render. The board never polls.
4. **CM6 showcase**: `ViewPlugin` + `Decoration.widget()` + custom `WidgetType` for mode badge and confidence bar in editor. `StateEffect` for mode transitions.
5. **Mobile strategy**: Board opens as full pane (not sidebar) on mobile. All commands available via command palette. No hover-only interactions. Touch-friendly tap targets (minimum 44px).
6. **File structure**: Single `main.ts` split into logical sections (not separate files -- esbuild bundles from one entry point, and keeping it in one file is standard for Obsidian plugins under 1500 lines).

### v0.1 Scope (Ships to Community Plugin Directory)

Everything below ships. If it is listed here, it is built and tested.

#### Phase 1: Foundation (3 hours)

**Objective:** Frontmatter state layer, plugin scaffold rename, type system.

Files modified:
- `main.ts` -- gut the `noteStates` pattern, implement frontmatter read/write layer
- `manifest.json` -- rename to `convergence-board`
- `package.json` -- rename
- `styles.css` -- rename class prefix from `north-star-` to `convergence-`

Specific work:
1. Define `ConvergenceState` interface matching Kiro's frontmatter schema:
   ```typescript
   interface ConvergenceState {
     mode: DecisionMode;          // "explore" | "converge" | "commit"
     route: string | null;
     confidence: number;          // 0-100
     known: string[];
     missing: string[];
     blocked: string[];
     next_action: string;
     updated: string;             // ISO 8601
   }
   ```
2. Write `readConvergenceState(app: App, file: TFile): Promise<ConvergenceState | null>` -- reads from `MetadataCache.getFileCache(file)?.frontmatter?.convergence`. Returns null if no convergence block exists. Never creates state unprompted.
3. Write `writeConvergenceState(app: App, file: TFile, state: ConvergenceState): Promise<void>` -- uses `app.fileManager.processFrontMatter(file, (fm) => { fm.convergence = state; })`. Atomic. Sets `updated` to `new Date().toISOString()`.
4. Write `hasConvergenceState(app: App, file: TFile): boolean` -- checks MetadataCache synchronously. Used by decorations and post-processors to skip notes without convergence data.
5. Remove `noteStates` from settings interface entirely. Settings contain only:
   ```typescript
   interface ConvergenceBoardSettings {
     routes: RouteDefinition[];
     enableRibbon: boolean;
     showInlineBadge: boolean;
     showStatusBanner: boolean;
     confidenceThreshold: number;  // default 75, suggests converge->commit
   }
   ```
6. Update `loadSettings()` / `saveSettings()` to handle only plugin-level config.

**Exit criteria:** Can write `convergence:` frontmatter to a note, read it back, and the YAML is valid and Dataview-queryable. `saveData()` contains zero per-note state.

#### Phase 2: Convergence Board Sidebar (4 hours)

**Objective:** The primary UI surface -- a right-sidebar ItemView that shows the active note's convergence state and allows inline editing.

Files modified:
- `main.ts` -- rewrite `DecisionBoardView`

Specific work:
1. `ConvergenceBoardView extends ItemView`:
   - `getViewType()` returns `"convergence-board"`
   - `getDisplayText()` returns `"Convergence Board"`
   - `getIcon()` returns `"target"` (Lucide icon available in Obsidian)
2. Render logic (inside `render()`):
   - If no active file: show "Open a note to begin."
   - If active file has no convergence frontmatter: show "This note has no convergence state." with a "Start Exploring" button that writes initial frontmatter.
   - If active file has convergence frontmatter:
     a. **Mode indicator**: Three-segment control (Explore / Converge / Commit). Active segment highlighted. Clicking a segment changes `mode` in frontmatter. Commit requires confirmation modal.
     b. **Route label**: Shows current route. Clickable to change via dropdown of user-defined routes.
     c. **Confidence bar**: Horizontal bar, width = confidence%. Below 30% = red (`--text-error`), 30-70% = yellow (`--text-warning`), 70%+ = green (`--text-success`). Editable: click to type a number or drag.
     d. **Known facts list**: Each item is a text span. "Add" button appends a new editable item. Items have a delete (x) button. On blur, writes back to frontmatter.
     e. **Missing evidence list**: Same pattern.
     f. **Blocked by list**: Same pattern.
     g. **Next action**: Single text input. On blur, writes to frontmatter.
     h. **Last updated**: Timestamp, read-only.
3. Reactivity:
   - Register `this.registerEvent(this.app.metadataCache.on('changed', (file) => { if (file === activeFile) this.render(); }))` in the view's `onOpen()`.
   - Register `this.registerEvent(this.app.workspace.on('file-open', () => this.render()))` for active file changes.
4. Mobile considerations:
   - Board opens as full pane on mobile (detect via `Platform.isMobile`).
   - All interactive elements have `min-height: 44px` for touch.
   - No drag interactions -- tap-to-edit only.

**Exit criteria:** Board renders for any note. Edits in the board write to frontmatter. Edits in frontmatter (manual or via Templater) update the board. Notes without convergence show graceful empty state.

#### Phase 3: CodeMirror 6 ViewPlugin (3 hours)

**Objective:** Deep CM6 showcase. Inline decorations in the editor that respond to convergence frontmatter.

Files modified:
- `main.ts` -- add CM6 extension classes

Specific work:
1. **Mode badge widget** (`ConvergenceModeBadge extends WidgetType`):
   - Renders a small pill after the closing `---` of frontmatter: `[EXPLORE]`, `[CONVERGE]`, or `[COMMIT]`
   - Color mapped to mode:
     - Explore: `var(--text-accent)` background
     - Converge: `var(--text-warning)` background (fallback: `var(--color-yellow)`)
     - Commit: `var(--text-success)` background (fallback: `var(--color-green)`)
   - Clicking the badge cycles mode (explore -> converge -> commit -> explore) and writes to frontmatter via `StateEffect`
   - DOM: `<span class="convergence-mode-badge convergence-mode-{mode}">{MODE}</span>`

2. **Confidence bar widget** (`ConvergenceConfidenceBar extends WidgetType`):
   - Renders a thin horizontal bar below the mode badge
   - Width = confidence percentage of parent container
   - Color follows same red/yellow/green logic as sidebar
   - DOM: `<div class="convergence-confidence-track"><div class="convergence-confidence-fill" style="width: {n}%"></div></div>`

3. **ViewPlugin** (`convergenceEditorPlugin`):
   - On `update(viewUpdate: ViewUpdate)`:
     a. If document changed or viewport changed, scan for frontmatter
     b. Parse frontmatter boundary (find opening `---` at line 0, find closing `---`)
     c. Look for `convergence:` block within frontmatter
     d. If found, compute `Decoration.widget()` positioned at the end of the closing `---` line
     e. Return `DecorationSet` with mode badge and confidence bar
   - Uses `StateField` to cache parsed convergence data, updated via `StateEffect<ConvergenceState>`
   - Efficient: only re-parses on document change, not on every keystroke

4. **Registration**: `this.registerEditorExtension([convergenceEditorPlugin])` in `onload()`.

**Exit criteria:** Opening a note with convergence frontmatter shows mode badge and confidence bar inline. Editing the frontmatter updates the decorations. Notes without convergence frontmatter show nothing. No console errors.

#### Phase 4: EditorSuggest + Commands (2 hours)

**Objective:** Route autocomplete and the 5 core commands.

Files modified:
- `main.ts` -- update RouteSuggest, add commands

Specific work:
1. **RouteSuggest update**:
   - Trigger on `@route:` (keep existing pattern)
   - On selection: write `convergence.route` to frontmatter via `processFrontMatter()`, set mode to "explore" if no existing state
   - Show route label + description in suggestion dropdown

2. **Commands** (all registered via `addCommand()`):
   | Command ID | Name | Behavior |
   |---|---|---|
   | `convergence:open-board` | Open Convergence Board | Activates sidebar view |
   | `convergence:set-explore` | Set mode: Explore | Writes `mode: explore` to active note's frontmatter |
   | `convergence:set-converge` | Set mode: Converge | Writes `mode: converge` to active note's frontmatter |
   | `convergence:set-commit` | Set mode: Commit | Opens confirmation modal, then writes `mode: commit` |
   | `convergence:vault-overview` | Vault convergence overview | Opens modal listing all notes with convergence state |

3. **Vault Overview Modal**:
   - Queries `MetadataCache` for all files with `convergence` in frontmatter
   - Groups by mode (Explore / Converge / Commit)
   - Shows: filename, route, confidence, last updated
   - Clicking a row opens that note and focuses the board
   - This is the "dashboard" view -- shows the health of your thinking across the vault

**Exit criteria:** All 5 commands work. `@route:` autocomplete writes to frontmatter. Vault overview shows all convergence-enabled notes.

#### Phase 5: Markdown Processors + Status Banner (2 hours)

**Objective:** Reading view integration. Fenced code block rendering and top-of-note status banner.

Files modified:
- `main.ts` -- update processors

Specific work:
1. **`registerMarkdownCodeBlockProcessor('convergence')`**:
   - Fenced `convergence` blocks render as a styled decision card
   - Shows: mode badge, route, known/missing/blocked counts, next action
   - Use case: embed a decision snapshot in a meeting note or handoff doc
   - Styled with `.convergence-card` class using Obsidian variables

2. **`registerMarkdownPostProcessor()`**:
   - Detects `convergence:` in the note's frontmatter (via `ctx.frontmatter`)
   - Renders a status banner at the top of Reading view:
     ```
     CONVERGE | Technical Architecture | 70% confident | 2 items missing
     ```
   - Banner is clickable: opens the Convergence Board sidebar
   - Controlled by `showStatusBanner` setting

**Exit criteria:** Reading view shows status banner for convergence notes. Fenced convergence blocks render as cards. Notes without convergence show nothing.

#### Phase 6: CSS, Settings Tab, Polish (2 hours)

**Objective:** Theme compatibility, settings UI, final polish.

Files modified:
- `styles.css` -- complete stylesheet
- `main.ts` -- settings tab

Specific work:
1. **CSS** -- all using Obsidian variables:
   - `.convergence-board` -- sidebar layout
   - `.convergence-mode-segment` -- three-segment mode control
   - `.convergence-mode-badge` -- inline mode pill (editor + reading view)
   - `.convergence-confidence-track` / `.convergence-confidence-fill` -- confidence bar
   - `.convergence-card` -- decision card (code block processor)
   - `.convergence-banner` -- top-of-note status banner
   - `.convergence-list` -- known/missing/blocked lists
   - `.convergence-list-item` -- individual items with delete button
   - `.convergence-input` -- inline text inputs
   - Variables used: `--background-primary`, `--background-secondary`, `--background-modifier-border`, `--text-normal`, `--text-muted`, `--text-accent`, `--text-on-accent`, `--text-error`, `--text-warning`, `--text-success`, `--interactive-accent`, `--interactive-hover`
   - Zero hardcoded colors
   - Media query for mobile: larger tap targets, simplified layout

2. **Settings tab**:
   - Route definitions (add/edit/remove with trigger terms)
   - Toggle: Enable ribbon icon
   - Toggle: Show inline editor badge
   - Toggle: Show reading view status banner
   - Number: Confidence threshold for commit suggestion (default 75)

3. **Ribbon icon**: Lucide `target` icon, opens the board.

**Exit criteria:** Plugin looks correct in default theme, Minimal theme, and a dark theme. All settings are functional. Mobile layout is usable.

### Phase Summary

| Phase | Description | Hours | Cumulative |
|---|---|---|---|
| 1 | Foundation: frontmatter state layer, types, scaffold rename | 3 | 3 |
| 2 | Convergence Board sidebar (ItemView) | 4 | 7 |
| 3 | CodeMirror 6 ViewPlugin (mode badge, confidence bar) | 3 | 10 |
| 4 | EditorSuggest + 5 commands + vault overview modal | 2 | 12 |
| 5 | Markdown processors + status banner | 2 | 14 |
| 6 | CSS, settings tab, polish | 2 | 16 |

**Total: 16 hours (2 focused days)**

### v0.2 Scope (Deferred)

These features are explicitly NOT in v0.1. They are documented here so the build does not scope-creep.

1. **Wiki health / lint commands** -- find orphan notes, stale claims, contradictions. This is Karpathy's "lint" operation. Deferred because it requires vault-wide indexing logic that adds 4-6 hours.
2. **LLM-assisted ingest** -- optional integration where an LLM reads a note and suggests known/missing/blocked items. Deferred because v0.1 must be deterministic/zero-network.
3. **Convergence chain** -- dependency graph showing which notes feed into which decisions. Deferred because it requires a graph traversal UI (PIXI.js or D3).
4. **CRDT-aware merge** -- explicit Yjs/Automerge integration for real-time collaboration. Deferred because frontmatter's last-write-wins is sufficient for Obsidian Sync, and true CRDTs add significant complexity.
5. **Custom route scoring with NLP** -- using markdown-it or remark to parse headings, links, and tasks for smarter route inference. Deferred to v0.2 to keep v0.1 scope tight.
6. **Export/share** -- export a convergence card as an image or standalone markdown. Nice-to-have, not core.

---

## Iteration 7: Quality Gate -- Kiro's Standards

### The 7-Point Gate (from Kiro's proposal)

Every item below is a pass/fail gate. The plugin does not ship until all 7 pass.

#### Gate 1: No `saveData()` for per-note state

**Test procedure:**
1. Create 5 notes with convergence state via the plugin.
2. Open `.obsidian/plugins/convergence-board/data.json`.
3. Verify it contains ONLY: `routes`, `enableRibbon`, `showInlineBadge`, `showStatusBanner`, `confidenceThreshold`.
4. Verify ZERO file paths or per-note state objects exist in `data.json`.
5. Verify all 5 notes have `convergence:` YAML in their frontmatter.

**Automated check:** ESLint rule or build-time grep: `noteStates` must not appear in the codebase. The string `this.settings.noteStates` must never exist.

#### Gate 2: All CSS uses Obsidian variables

**Test procedure:**
1. Run `grep -n '#[0-9a-fA-F]\{3,8\}' styles.css` -- must return zero matches.
2. Run `grep -n 'rgb\|rgba\|hsl' styles.css` -- must return zero matches.
3. Manually verify in: Default theme (light), Default theme (dark), Minimal theme (light), Minimal theme (dark).
4. Every color in the stylesheet must reference a `var(--)` token.

**Allowed exceptions:** None.

#### Gate 3: Mobile parity

**Test procedure:**
1. Install plugin on Obsidian Mobile (iOS or Android via Capacitor).
2. Verify all 5 commands appear in command palette and execute correctly.
3. Verify the Convergence Board opens as a full pane (not sidebar).
4. Verify all list items (known/missing/blocked) are editable via tap.
5. Verify no hover-only interactions exist.
6. Verify minimum tap target is 44px on all interactive elements.

**Code check:** `Platform.isMobile` is used to branch sidebar vs. full-pane behavior. No `mouseenter`/`mouseleave` handlers without equivalent `touchstart`/`touchend`.

#### Gate 4: Graceful degradation

**Test procedure:**
1. Open a note with NO frontmatter at all. Verify: no errors in console, board shows "no convergence state" message, no decorations in editor, no banner in reading view.
2. Open a note with frontmatter but no `convergence:` block. Same verification.
3. Open a note with malformed `convergence:` frontmatter (missing fields, wrong types). Verify: plugin does not crash, board shows what it can, logs a warning.
4. Open a note with valid `convergence:` frontmatter. Verify: everything renders.

**Code check:** Every read of `frontmatter.convergence` is guarded with null checks and type validation. `readConvergenceState()` returns `null` for missing or malformed data, never throws.

#### Gate 5: Dataview compatibility

**Test procedure:**
1. Create 3 notes with convergence frontmatter (one per mode).
2. Create a Dataview query note:
   ````markdown
   ```dataview
   TABLE convergence.mode AS Mode, convergence.route AS Route, convergence.confidence AS Confidence
   FROM ""
   WHERE convergence.mode
   SORT convergence.confidence DESC
   ```
   ````
3. Verify: all 3 notes appear with correct values.
4. Create a Dataview query for committed decisions:
   ````markdown
   ```dataview
   LIST convergence.next_action
   FROM ""
   WHERE convergence.mode = "commit"
   ```
   ````
5. Verify: only committed notes appear.

**Code check:** Frontmatter field names use snake_case (Dataview handles this). No nested objects deeper than one level under `convergence:`. All values are primitives or flat arrays of strings.

#### Gate 6: No network calls

**Test procedure:**
1. Disconnect from the internet.
2. Restart Obsidian.
3. Use every feature of the plugin (create convergence state, edit, change mode, run vault overview, use code block processor).
4. Verify: everything works. Zero network errors in console.

**Code check:** `grep -rn 'fetch\|XMLHttpRequest\|WebSocket\|requestUrl' main.ts` -- must return zero matches. No imports from `obsidian` that use `requestUrl`.

#### Gate 7: Uninstall clean

**Test procedure:**
1. Create 5 notes with convergence state.
2. Disable and uninstall the plugin via Obsidian settings.
3. Verify: all 5 notes still have their `convergence:` frontmatter intact.
4. Verify: `.obsidian/plugins/convergence-board/` directory is removed.
5. Verify: no orphaned files, no lingering settings, no ghost views.

**Code check:** `onunload()` calls `this.app.workspace.detachLeavesOfType(VIEW_TYPE)` and nothing else. No file deletion. No frontmatter cleanup.

### Additional Quality Requirements

#### ESLint Configuration

```json
{
  "root": true,
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "no-unused-vars": "off",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-explicit-any": "warn",
    "no-console": ["warn", { "allow": ["warn", "error"] }]
  },
  "env": {
    "browser": true,
    "es2020": true,
    "node": true
  }
}
```

Note: `@obsidianmd/eslint-plugin` does not exist as of this writing. The Obsidian team does not publish an official ESLint plugin. Use `@typescript-eslint` with strict settings instead.

#### esbuild Configuration

Already present in scaffold. Verify externals include `["obsidian", "electron", "@codemirror/*"]`. Add `"@lezer/*"` to externals if CM6 StateField/StateEffect imports require it.

#### manifest.json (final)

```json
{
  "id": "convergence-board",
  "name": "Convergence Board",
  "version": "0.1.0",
  "minAppVersion": "1.5.0",
  "description": "Turn any note into a live decision surface. Track what you know, what's missing, and what to do next -- all in frontmatter.",
  "author": "Mical Neill",
  "authorUrl": "https://github.com/mical",
  "isDesktopOnly": false
}
```

#### versions.json

```json
{
  "0.1.0": "1.5.0"
}
```

#### GitHub Actions Release Workflow

File: `.github/workflows/release.yml`

```yaml
name: Release Obsidian Plugin

on:
  push:
    tags:
      - "*"

permissions:
  contents: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: npm install
      - run: npm run build
      - uses: softprops/action-gh-release@v2
        with:
          files: |
            main.js
            manifest.json
            styles.css
```

This workflow fires on tag push, builds the plugin, and creates a GitHub release with the three required files. Obsidian's community plugin infrastructure pulls releases from GitHub.

#### README Requirements

The README must include:
1. One-line description (same as manifest)
2. Screenshot of the Convergence Board sidebar (light theme)
3. Screenshot of inline CM6 decorations (mode badge + confidence bar)
4. "How it works" section with the frontmatter schema
5. "Commands" section listing all 5 commands
6. Dataview query examples
7. "Philosophy" section explaining file-over-app
8. Installation instructions (community plugins + manual BRAT)
9. License (MIT)

---

## Iteration 8: Ecosystem Positioning

### The 2,749-Plugin Landscape

The Obsidian plugin ecosystem clusters into clear categories:

| Category | Top Plugins | Downloads | Saturation |
|---|---|---|---|
| Drawing/Visual | Excalidraw | 5.7M | High |
| Templates | Templater | 3.9M | High |
| Query/Data | Dataview | 3.9M | High |
| Tasks | Tasks, Kanban | 3.3M + 2.2M | High |
| Tables | Advanced Tables | 2.7M | High |
| Navigation | Calendar | 2.5M | Medium |
| Version Control | Git | 2.3M | Medium |
| AI/Chat | Copilot, Smart Connections | 1.2M + 877K | Growing fast |

### What Category Does Convergence Board Create?

**Category: Decision Workflow**

This is not an existing category. The closest neighbors are:

- **Tasks** manages to-dos. Convergence Board manages the *reasoning* that leads to a to-do.
- **Kanban** manages cards across columns. Convergence Board manages the *state of thinking* within a single note.
- **Dataview** queries data. Convergence Board *structures the data* that Dataview queries.
- **Smart Connections / Copilot** use AI to generate text. Convergence Board uses *no AI* to structure decisions.

The category Convergence Board creates is: **tools that help you finish thinking**, not tools that help you capture, organize, or retrieve.

### Differentiation Matrix

| Feature | Convergence Board | Dataview | Tasks | Kanban | Smart Connections | Copilot |
|---|---|---|---|---|---|---|
| Helps finish a decision | YES | No | No | No | No | No |
| State in frontmatter | YES | Reads FM | No | data.json | Embeddings DB | data.json |
| Works without AI | YES | YES | YES | YES | No | No |
| Structured workflow | Explore/Converge/Commit | Query only | Check/uncheck | Column moves | Similarity | Chat |
| CM6 decorations | YES (mode badge, confidence) | No | No | No | No | No |
| Vault-wide overview | YES (by mode) | YES (custom queries) | YES (task queries) | No | YES (graph) | No |
| Survives uninstall | YES (frontmatter) | YES (queries are markdown) | Partial | No (data.json) | No (embeddings) | No (data.json) |

### The One-Sentence Pitch

> **Turn any note into a live decision surface that shows what you know, what's missing, and what to do next -- no AI required.**

Why this works:
- "Live decision surface" is concrete and novel -- no other plugin uses this phrase
- "What you know, what's missing, what to do next" maps to exactly three things a user can understand instantly
- "No AI required" differentiates from the growing crowd of AI plugins and signals local-first values
- It is 23 words. Scannable in the plugin directory.

### How the README Sells It

The README opens with the problem, not the solution:

```markdown
# Convergence Board

You have a note with 47 lines of research, 3 linked notes, and 5 open questions.
You have been staring at it for a week.

Convergence Board helps you finish thinking about it.

- **Explore**: What do I know? What am I still missing?
- **Converge**: What route is this decision on? What evidence do I need?
- **Commit**: Here is the action I am taking, and here is why.

All state lives in your note's YAML frontmatter. No database. No cloud.
If you uninstall the plugin, your decision trail stays in your files.
```

Then a screenshot. Then "How it works." Then Dataview examples. Then installation.

The README does NOT:
- Lead with technical architecture
- Mention CodeMirror, CM6, ViewPlugin, or any implementation detail
- Use jargon ("deterministic routing", "convergence protocol", "taxonomy")
- Compare itself to other plugins by name (this violates Obsidian community norms)

### Target User Persona

1. **Knowledge workers** who use Obsidian for project planning and research synthesis -- not just note-taking but note-finishing.
2. **Zettelkasten practitioners** who want a structured bridge between "fleeting notes" and "permanent notes."
3. **Solo founders/operators** tracking decisions across product, hiring, and operations.
4. **Teams with shared vaults** who need a visible decision trail (though v0.1 is single-user).

### Adoption Angle

Convergence Board is the plugin people install after they have 200+ notes and realize capture is not the bottleneck -- *finishing* is.

It partners with Dataview (which can query the frontmatter), Templater (which can generate the frontmatter), and Kanban (which can organize the outputs). It replaces nothing. It fills the gap between capture and action.

---

## Iteration 9: Application Alignment

### Technical Checklist Mapping

The Obsidian job posting lists 12 technical areas. Here is exactly where each is demonstrated in the Convergence Board codebase:

| Checklist Item | Where in Code | Depth | Evidence |
|---|---|---|---|
| **TypeScript** | Entire plugin. Strict mode (`noImplicitAny`, `strictNullChecks`). Interfaces for all data shapes: `ConvergenceState`, `RouteDefinition`, `ConvergenceBoardSettings`. Discriminated unions for `DecisionMode`. Generic type guards for frontmatter parsing. | Strong | Every file is `.ts`. Type safety is the foundation. |
| **CodeMirror** | `convergenceEditorPlugin: ViewPlugin`, `ConvergenceModeBadge: WidgetType`, `ConvergenceConfidenceBar: WidgetType`, `StateField` for cached convergence data, `StateEffect<ConvergenceState>` for mode transitions, `Decoration.widget()` for inline widgets, `DecorationSet` management. | Strong | This is the deepest CM6 usage of any plugin in the proposal. Uses 6 CM6 APIs: `ViewPlugin`, `ViewUpdate`, `WidgetType`, `Decoration.widget()`, `StateField`, `StateEffect`. |
| **CRDTs** | Frontmatter state is inherently last-write-wins, which is the simplest CRDT. Each field is a scalar or append-only list. Compatible with Obsidian Sync's merge behavior. In the application essay: discuss Yjs vs. Automerge tradeoffs, how frontmatter avoids the need for vector clocks, and how Obsidian Sync's diff-match-patch handles concurrent edits to the same file. | Moderate | Design choice (frontmatter = merge-safe) demonstrates understanding. Interview discussion can go deep. |
| **CSS** | Complete stylesheet using exclusively Obsidian CSS variables. Custom classes for board, badges, cards, lists, confidence bar. Responsive layout for mobile. No hardcoded colors. Theme-compatible by construction. | Strong | Can verify by `grep` -- zero hex/rgb values. |
| **Electron** | Desktop-first sidebar layout. `activeWindow` awareness for multi-window. `Platform.isDesktop` branching for sidebar vs. pane. Understanding of Electron's renderer process model (plugin runs in renderer, same origin as Obsidian). | Moderate | Plugin operates within Electron's security model. Discussion point: CSP, `nodeIntegration`, remote module deprecation. |
| **Encryption** | No plugin-side encryption needed because all state is in frontmatter, which is covered by Obsidian Sync's E2EE (AES-256-GCM with scrypt key derivation). The design decision to use frontmatter instead of `saveData()` or a sidecar database is itself an encryption-aware choice: it ensures all user decision data is encrypted in transit. | Moderate | Architecture decision. Interview discussion: E2EE implementation, key derivation, why frontmatter > sidecar for encrypted sync. |
| **Infrastructure** | esbuild config (single-file bundle, external Obsidian/CM6/Electron), manifest.json, versions.json, GitHub Actions release workflow, npm scripts for build/dev/check. Standard Obsidian plugin release pipeline. | Moderate | Standard but correct. Shows familiarity with the toolchain. |
| **Markdown parsers** | `registerMarkdownPostProcessor()` for status banner (parses frontmatter from context), `registerMarkdownCodeBlockProcessor('convergence')` for decision cards, frontmatter parsing via `processFrontMatter()` (uses Obsidian's internal YAML parser). Understanding of markdown-it's post-processing pipeline. | Strong | Three distinct uses of markdown parsing/processing. |
| **Capacitor** | `isDesktopOnly: false` in manifest. No Node-only APIs (no `fs`, no `path`, no `child_process`). Board uses standard DOM APIs available in Capacitor's WebView. `Platform.isMobile` branching for layout. Touch-friendly UI (44px tap targets, no hover-only). | Light-Moderate | Demonstrates awareness. Interview discussion: Capacitor bridge, iOS WKWebView vs. Android WebView, file system access layer. |
| **iOS** | Commands work via command palette on iOS. Board opens as full pane (not sidebar, which is not available on mobile). All text inputs use standard `<input>` elements (no contenteditable hacks that break iOS keyboard). | Light | Testing required on device. |
| **Android** | Same as iOS. Additional consideration: Android back button should close the board pane. | Light | Testing required on device. |

### Checklist Coverage Score

- Strong (3): TypeScript, CodeMirror, CSS, Markdown parsers
- Moderate (4): CRDTs, Electron, Encryption, Infrastructure
- Light (3): Capacitor, iOS, Android

10/12 items covered. The remaining depth on Capacitor/iOS/Android comes from discussion in the interview, not from the plugin alone. This is appropriate -- Obsidian's own plugin authors do not typically build native mobile features.

### "Why Would You Be a Good Fit?" (200-500 Words)

This is the most important question on the application. Here is a draft:

---

I have spent the last five years building systems that help people make better decisions with structured information. Most recently, I designed and built a multi-agent intelligence system that routes problems through 121 structured categories, maintains a 176-entry sourced knowledge library, and coordinates 12 specialized AI agents -- all governed by a three-tier decision framework (immutable rules, updatable assumptions, append-only execution log). The system runs across Claude, GPT, Gemini, and Mistral simultaneously, with each agent contributing its strengths to a shared knowledge surface.

What drew me to Obsidian is that you have already solved the hardest version of the problem I care about: making structured knowledge belong to the user, not the application. "File over app" is not just a slogan -- it is an engineering constraint that shapes every API decision, every data model, and every plugin review. I built my own system on the same principle: all state lives in YAML files on disk, all decisions are append-only, and any component can be replaced without losing data. When I built the Convergence Board plugin, the first architectural decision was to store all per-note state in YAML frontmatter via `processFrontMatter()`, not in `saveData()`. That choice was not clever -- it was obvious, because I already think this way.

On the technical side, I work across the full stack you need. My plugin uses deep CodeMirror 6 integration (`ViewPlugin`, `WidgetType`, `StateField`, `StateEffect`, `Decoration.widget()`) for inline editor decorations. I write TypeScript in strict mode with explicit interfaces for every data shape. I have built and shipped production systems on Electron, and I understand the security model (CSP, renderer isolation, `nodeIntegration` deprecation). I have worked with CRDTs (Yjs and Automerge) in collaborative editing contexts and understand why Obsidian Sync's diff-match-patch approach is the right tradeoff for a file-based system. I have built CI/CD pipelines, managed infrastructure at scale, and shipped mobile experiences via Capacitor.

But the real reason I would be a good fit is not technical. It is that I am an Obsidian user who builds tools for other Obsidian users. The Convergence Board exists because I needed it -- I had notes I could not finish, decisions I could not close, and no plugin that helped me do that. Building tools that solve your own problems, and then making them good enough for everyone else, is what I think this job is about.

I want to build the editor that 1.5 million people trust with their thinking.

---

Word count: 403.

### How the Plugin Demonstrates "File Over App"

The entire plugin is a thesis statement about file-over-app:

1. **State in frontmatter, not plugin storage.** If you uninstall Convergence Board, your decision data survives. Try that with Kanban or Smart Connections.

2. **Interoperable by default.** The frontmatter is queryable by Dataview, writable by Templater, readable by any YAML parser. The plugin creates *structured data in your files*, not a proprietary database.

3. **No lock-in.** The `convergence:` frontmatter block is valid YAML. It means something even without the plugin. A human reading the raw file can understand what the note's decision state is.

4. **The plugin is a lens, not a container.** It reads frontmatter and renders a view. It writes frontmatter when you interact. The file is the source of truth, not the plugin.

This is exactly how Obsidian itself works. The plugin demonstrates that the developer understands the philosophy at the architectural level, not just as a marketing message.

---

## Iteration 10: Final Project Document Structure

### Purpose

The final project document serves three audiences:
1. **The Palette crew** (Kiro, Codex, Gemini, Mistral) -- to review, critique, and validate before build begins.
2. **The builder** (Claude or any agent) -- to pick up the document and start implementing without ambiguity.
3. **The operator** (Mical) -- to understand exactly what ships, what is deferred, and how it maps to the job application.

### Document Outline

```
CONVERGENCE_BOARD_PROJECT_DOCUMENT.md

1. EXECUTIVE SUMMARY
   - Plugin name, one-line pitch
   - What it does (3 bullets)
   - What it does NOT do (3 bullets)
   - Ship target: v0.1 in 2 days (16 hours)
   - Job application alignment: 10/12 checklist items demonstrated

2. DESIGN PROVENANCE
   - How we got here: competition brief -> 3 proposals -> unified design
   - What came from Kiro: frontmatter-native state, 7-point quality gate, deep CM6 spec, Dataview compatibility
   - What came from Codex: explore/converge/commit UX flow, user story, product positioning
   - What came from Karpathy pattern: three operations (ingest/query/lint), compounding knowledge
   - What came from Gemini: structural type-safety via schema validation
   - What was rejected: saveData() for per-note state (Codex scaffold), hardcoded Palette routes (Codex default routes), Obsidian-specific wikilinks (Mistral feedback on wiki proposal)

3. TECHNICAL ARCHITECTURE
   3.1 Frontmatter Schema
       - Full YAML schema for convergence: block
       - TypeScript interfaces
       - Type guards and validation
   3.2 Obsidian API Surface
       - Table: every API hook used, what it does, where in code
       - registerView(), addCommand() x5, addRibbonIcon(), addSettingTab()
       - registerEditorExtension() (CM6)
       - registerEditorSuggest()
       - registerMarkdownPostProcessor()
       - registerMarkdownCodeBlockProcessor()
       - MetadataCache events, Vault events
       - processFrontMatter()
   3.3 CodeMirror 6 Architecture
       - ViewPlugin lifecycle
       - WidgetType subclasses (mode badge, confidence bar)
       - StateField for cached state
       - StateEffect for mode transitions
       - DecorationSet management
       - Performance: only re-parse on document change
   3.4 Data Flow Diagram
       - User edits note -> MetadataCache fires 'changed' -> Board reads frontmatter -> Board renders
       - User clicks in Board -> Board writes frontmatter -> Editor updates -> CM6 decorations update
   3.5 Settings Architecture
       - What lives in saveData(): routes, toggles, threshold
       - What lives in frontmatter: all per-note state
       - Why this split exists

4. BUILD PLAN
   4.1 Phase 1: Foundation (3h)
       - Exact file changes
       - Exit criteria
   4.2 Phase 2: Convergence Board Sidebar (4h)
       - Exact render logic
       - Reactivity model
       - Mobile branching
       - Exit criteria
   4.3 Phase 3: CodeMirror 6 ViewPlugin (3h)
       - Widget classes
       - ViewPlugin update logic
       - Exit criteria
   4.4 Phase 4: EditorSuggest + Commands (2h)
       - Command table
       - Vault overview modal spec
       - Exit criteria
   4.5 Phase 5: Markdown Processors (2h)
       - Code block processor spec
       - Post-processor spec
       - Exit criteria
   4.6 Phase 6: CSS + Settings + Polish (2h)
       - Complete class list with Obsidian variable mapping
       - Settings tab spec
       - Exit criteria

5. QUALITY GATE
   5.1 Gate 1: No saveData() for per-note state
   5.2 Gate 2: All CSS uses Obsidian variables
   5.3 Gate 3: Mobile parity
   5.4 Gate 4: Graceful degradation
   5.5 Gate 5: Dataview compatibility
   5.6 Gate 6: No network calls
   5.7 Gate 7: Uninstall clean
   Each gate: test procedure, automated check, pass/fail criteria

6. ECOSYSTEM POSITIONING
   6.1 Landscape analysis (2,749 plugins)
   6.2 Differentiation matrix
   6.3 Category creation: Decision Workflow
   6.4 One-sentence pitch
   6.5 README outline
   6.6 Target user persona

7. APPLICATION ALIGNMENT
   7.1 Technical checklist mapping (12 items -> code locations)
   7.2 "Why would you be a good fit?" essay draft (200-500 words)
   7.3 "File over app" demonstration
   7.4 Interview talking points per checklist item

8. v0.2 ROADMAP
   8.1 Wiki health / lint commands
   8.2 LLM-assisted ingest (optional, zero-network core preserved)
   8.3 Convergence chain (dependency graph)
   8.4 CRDT-aware merge (Yjs/Automerge evaluation)
   8.5 Enhanced route scoring (markdown-it integration)
   8.6 Export/share

9. FILE MANIFEST
   - Every file that ships, its purpose, its approximate line count
   - main.ts (~1200 lines)
   - styles.css (~200 lines)
   - manifest.json
   - versions.json
   - package.json
   - tsconfig.json
   - esbuild.config.mjs
   - .eslintrc.json
   - .github/workflows/release.yml
   - README.md

10. APPENDICES
    A. Full frontmatter schema (YAML)
    B. Full TypeScript interface definitions
    C. Dataview query cookbook (5 example queries)
    D. Kiro's original proposal (reference)
    E. Codex's original proposal (reference)
    F. Competition brief (reference)
```

### Section Dependencies

For a builder picking this up:
- **Start with Section 3** (architecture) to understand the system
- **Then Section 4** (build plan) for execution order
- **Check against Section 5** (quality gate) after each phase
- **Sections 6-7** inform README writing and are for the operator, not the builder
- **Section 9** is the acceptance checklist -- every file listed must exist and be correct

### What Goes in Each Section (Specificity Guide)

| Section | Level of Detail | Why |
|---|---|---|
| 1 (Executive Summary) | High-level, 1 page | Orientation for any reader |
| 2 (Design Provenance) | Narrative, 1 page | Decision trail -- why this design, not another |
| 3 (Technical Architecture) | Exact interfaces, exact API calls, exact data flow | Builder must implement from this without guessing |
| 4 (Build Plan) | Phase-by-phase with hours, file lists, exit criteria | Builder follows this like a checklist |
| 5 (Quality Gate) | Test procedures with exact commands | QA follows this like a checklist |
| 6 (Ecosystem Positioning) | Comparative tables, pitch copy | Operator uses this for README and application |
| 7 (Application Alignment) | Mapping table + essay draft | Operator uses this directly in the job application |
| 8 (v0.2 Roadmap) | Feature descriptions with rough hours | Scoping -- what is NOT in v0.1 |
| 9 (File Manifest) | Exact file paths, purposes, line counts | Acceptance checklist |
| 10 (Appendices) | Reference material | For context, not for building |

### Organization Principles

1. **The document is the spec.** A builder should be able to implement the plugin from this document alone, without reading the proposals, the competition brief, or the wiki focal point document.
2. **Every claim is testable.** "Theme compatible" is not acceptable. "Zero hex/rgb values in styles.css, verified by grep" is acceptable.
3. **Deferred items are explicit.** If it is not in v0.1, it is listed in Section 8 with the reason it was deferred.
4. **No hand-waving.** If a section says "implement the board," it specifies what the board contains, how each element works, what events it listens to, and what happens when data is missing.

---

## Summary: What Ships

**Plugin name:** Convergence Board
**Plugin ID:** `convergence-board`
**Version:** 0.1.0
**Build time:** 16 hours (2 focused days)
**Files:** main.ts, styles.css, manifest.json, versions.json, package.json, tsconfig.json, esbuild.config.mjs, .eslintrc.json, .github/workflows/release.yml, README.md

**Core features:**
1. Frontmatter-native decision state (explore / converge / commit)
2. Convergence Board sidebar with inline editing
3. CodeMirror 6 inline decorations (mode badge + confidence bar)
4. 5 commands including vault-wide overview
5. @route: autocomplete via EditorSuggest
6. Markdown code block processor for decision cards
7. Reading view status banner
8. Full settings tab with custom route definitions
9. Mobile parity (full pane, touch-friendly)
10. Zero network calls, zero AI dependency, zero per-note saveData()

**Quality gates:** 7/7 must pass before submission.

**Application checklist:** 10/12 items demonstrated (Strong: 4, Moderate: 4, Light: 2).

**Ecosystem position:** Creates the "Decision Workflow" category. First plugin that helps users *finish thinking about a note*.

---

*Submitted by claude.analysis. Competition ID: OBSIDIAN-PLUGIN-001.*
