# Convergence Board — Complete Project Document

**Plugin ID:** `convergence-board`
**Version:** 0.1.0
**Author:** Mical Neill
**Date:** 2026-04-07
**Competition:** OBSIDIAN-PLUGIN-001
**Status:** CREW REVIEW — requesting critique from all agents before build begins

---

## 1. Executive Summary

**Name:** Convergence Board
**Pitch:** Turn any note into a live decision surface that shows what you know, what's missing, and what to do next — no AI required.

**What it does:**
- Adds an explore → converge → commit workflow to any Obsidian note via YAML frontmatter
- Shows a sidebar Decision Board with known facts, missing evidence, blockers, and next action — all editable inline
- Renders inline CodeMirror 6 decorations (mode badge, confidence bar) in the editor

**What it does NOT do:**
- No AI, no LLM, no network calls — fully deterministic and local
- No per-note state in plugin storage — everything lives in frontmatter (file over app)
- No wiki-wide lint, no convergence chains, no CRDT collaboration (all deferred to v0.2)

**Ship target:** v0.1 in 2 days (16 hours)
**Application alignment:** 10/12 job checklist items demonstrated

---

## 2. Design Provenance

This design synthesizes work from 4 Palette crew agents, validated against Andrej Karpathy's "LLM Wiki" pattern (published 2026-04-07).

| Source | What We Take | What We Leave |
|--------|-------------|---------------|
| **Kiro (Convergence Board)** | Frontmatter-native state via `processFrontMatter()`, deep CM6 spec (ViewPlugin + WidgetType + StateEffect), 7-point quality gate, Dataview compatibility, "file over app" | — |
| **Codex (North Star Navigator)** | Explore→converge→commit UX flow, user story, product positioning, working 457-line scaffold | `noteStates` in saveData() (fails at scale), hardcoded Palette routes |
| **Gemini (Evidence Guardian)** | Schema validation concept (deferred to v0.2 as lint/health-check) | Full JSON Schema system (over-engineered for v0.1) |
| **Mistral (Advanced Table Editor)** | Community gap analysis methodology | Table editing direction (different product category) |
| **Karpathy (LLM Wiki)** | Three-operation framework: ingest/query/lint. "Wiki is a persistent, compounding artifact." | LLM dependency for core operations (v0.1 must be deterministic) |

**Key architectural decisions:**
1. Kiro is right: state in frontmatter, not saveData(). Codex's scaffold must be rewritten.
2. Karpathy's lint becomes v0.2. v0.1 focuses on the decision workflow.
3. The plugin works WITHOUT an LLM. Karpathy's ingest/query can layer on top later.
4. Gemini's merge proposal is correct: validation + convergence are complementary. v0.2 adds schema validation as Karpathy's "lint" operation.

---

## 3. Technical Architecture

### 3.1 Frontmatter Schema

All per-note decision state lives in YAML frontmatter under a `convergence:` key:

```yaml
---
convergence:
  mode: converge          # "explore" | "converge" | "commit"
  route: technical-architecture
  confidence: 70          # 0-100
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

**TypeScript interfaces:**

```typescript
type DecisionMode = "explore" | "converge" | "commit";

interface ConvergenceState {
  mode: DecisionMode;
  route: string | null;
  confidence: number;
  known: string[];
  missing: string[];
  blocked: string[];
  next_action: string;
  updated: string;  // ISO 8601
}

interface RouteDefinition {
  id: string;
  label: string;
  description: string;
  triggerTerms: string[];
  defaultNextSteps: string[];
}

interface ConvergenceBoardSettings {
  routes: RouteDefinition[];
  enableRibbon: boolean;
  showInlineBadge: boolean;
  showStatusBanner: boolean;
  confidenceThreshold: number;  // default 75
}
```

**Design rules:**
- `saveData()` stores ONLY `ConvergenceBoardSettings` — zero per-note state
- All frontmatter read/write goes through `processFrontMatter()`
- Null checks on every frontmatter access — notes without `convergence:` are gracefully ignored
- All values are primitives or flat string arrays — Dataview compatible

### 3.2 Obsidian API Surface

| Hook | Usage |
|------|-------|
| `registerView()` | Convergence Board sidebar (ItemView subclass) |
| `addCommand()` x5 | open-board, set-explore, set-converge, set-commit, vault-overview |
| `addRibbonIcon()` | Compass/target icon → opens board |
| `addSettingTab()` | Route definitions, display toggles, confidence threshold |
| `registerEditorExtension()` | CM6 ViewPlugin for mode badge + confidence bar |
| `registerEditorSuggest()` | `@route:` autocomplete |
| `registerMarkdownCodeBlockProcessor('convergence')` | Decision card in reading view |
| `registerMarkdownPostProcessor()` | Status banner at top of reading view |
| `MetadataCache.on('changed')` | Reactive board updates when frontmatter changes |
| `workspace.on('file-open')` | Board re-renders on active file change |
| `processFrontMatter()` | All frontmatter writes |

### 3.3 CodeMirror 6 Architecture

This is the technical showcase for the application. Uses 6 CM6 APIs:

**`ConvergenceModeBadge extends WidgetType`**
- Renders pill after closing `---` of frontmatter: `[EXPLORE]`, `[CONVERGE]`, or `[COMMIT]`
- Color from Obsidian CSS variables: `--text-accent` (explore), `--color-yellow` (converge), `--color-green` (commit)
- Click cycles mode and writes to frontmatter

**`ConvergenceConfidenceBar extends WidgetType`**
- Thin horizontal bar below mode badge, width = confidence%
- Color: red (<30%), yellow (30-70%), green (>70%) using `--text-error/warning/success`

**`convergenceEditorPlugin: ViewPlugin`**
- On `ViewUpdate`: if document changed, scan for frontmatter boundaries
- Parse `convergence:` block within frontmatter
- Produce `Decoration.widget()` positioned at end of closing `---`
- Return `DecorationSet` with badge + bar

**`StateField<ConvergenceState | null>`**
- Cached parsed convergence data, updated via `StateEffect<ConvergenceState>`
- Avoids re-parsing on every keystroke — only on document change

### 3.4 Data Flow

```
User edits note in editor
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
Editor updates (frontmatter = single source of truth)
    ↓
CM6 ViewPlugin detects document change → re-renders decorations
```

No sidecar files. No plugin-owned database. Frontmatter is the contract.

---

## 4. Build Plan

Starting from Codex's scaffold at `implementations/obsidian/north-star-navigator/`.

### Phase 1: Foundation (3 hours)

**Objective:** Frontmatter state layer, scaffold rename, type system.

- Gut `noteStates` pattern from main.ts
- Implement `readConvergenceState()`, `writeConvergenceState()`, `hasConvergenceState()`
- All use `processFrontMatter()` and `MetadataCache`
- Rename plugin ID to `convergence-board` in manifest.json, package.json
- Rename CSS class prefix from `north-star-` to `convergence-`
- Settings contain only: routes, toggles, threshold

**Exit criteria:** Can write `convergence:` frontmatter, read it back, and it's Dataview-queryable. `saveData()` contains zero per-note state.

### Phase 2: Convergence Board Sidebar (4 hours)

**Objective:** Primary UI surface — right-sidebar ItemView.

- `ConvergenceBoardView extends ItemView`
- No active file → "Open a note to begin"
- No convergence frontmatter → "No convergence state" + "Start Exploring" button
- Has convergence → renders:
  - Mode indicator (3-segment control: Explore/Converge/Commit, click to change)
  - Route label (clickable dropdown of user-defined routes)
  - Confidence bar (horizontal, color-coded, click to edit)
  - Known facts list (editable items, add/delete buttons)
  - Missing evidence list (same pattern)
  - Blocked by list (same pattern)
  - Next action (text input, writes on blur)
  - Last updated (read-only timestamp)
- Reactive: `MetadataCache.on('changed')` + `workspace.on('file-open')`
- Mobile: opens as full pane via `Platform.isMobile`, 44px tap targets

**Exit criteria:** Board renders for any note. Edits write to frontmatter. Frontmatter edits update board. Empty state is graceful.

### Phase 3: CodeMirror 6 ViewPlugin (3 hours)

**Objective:** Deep CM6 showcase — inline decorations.

- `ConvergenceModeBadge extends WidgetType` — mode pill after frontmatter fence
- `ConvergenceConfidenceBar extends WidgetType` — thin bar below badge
- `convergenceEditorPlugin: ViewPlugin` — parses frontmatter, produces DecorationSet
- `StateField` for cached state, `StateEffect` for mode transitions
- Only re-parses on document change (efficient)
- Registration: `this.registerEditorExtension([convergenceEditorPlugin])`

**Exit criteria:** Notes with convergence frontmatter show mode badge + confidence bar inline. Notes without show nothing. No console errors.

### Phase 4: EditorSuggest + Commands (2 hours)

**Objective:** Route autocomplete and 5 core commands.

| Command | Behavior |
|---------|----------|
| `convergence:open-board` | Activates sidebar view |
| `convergence:set-explore` | Writes mode: explore to frontmatter |
| `convergence:set-converge` | Writes mode: converge to frontmatter |
| `convergence:set-commit` | Confirmation modal → writes mode: commit |
| `convergence:vault-overview` | Modal listing all notes with convergence state, grouped by mode |

- `@route:` EditorSuggest: triggers autocomplete, writes convergence.route to frontmatter
- Vault Overview Modal: queries MetadataCache, groups by mode, click opens note

**Exit criteria:** All 5 commands work. Autocomplete writes frontmatter. Vault overview shows all convergence notes.

### Phase 5: Markdown Processors (2 hours)

**Objective:** Reading view integration.

- `registerMarkdownCodeBlockProcessor('convergence')` — fenced blocks render as styled decision cards
- `registerMarkdownPostProcessor()` — status banner at top of reading view: `CONVERGE | Route | 70% | 2 missing`
- Banner is clickable → opens board
- Controlled by `showStatusBanner` setting

**Exit criteria:** Reading view shows banner. Fenced blocks render cards. Clean notes show nothing.

### Phase 6: CSS + Settings + Polish (2 hours)

**Objective:** Theme compatibility, settings UI, final polish.

- Complete stylesheet using exclusively Obsidian CSS variables
- Zero hardcoded colors (verified by grep)
- Classes: `.convergence-board`, `.convergence-mode-segment`, `.convergence-mode-badge`, `.convergence-confidence-track`, `.convergence-confidence-fill`, `.convergence-card`, `.convergence-banner`, `.convergence-list`, `.convergence-list-item`, `.convergence-input`
- Settings tab: route definitions (add/edit/remove), 4 toggles, confidence threshold
- Ribbon icon: Lucide `target`
- Mobile media query: larger targets, simplified layout

**Exit criteria:** Plugin looks correct in default theme, Minimal theme, dark themes. All settings functional.

### Phase Summary

| Phase | Hours | Cumulative |
|-------|-------|-----------|
| Foundation | 3 | 3 |
| Board Sidebar | 4 | 7 |
| CM6 ViewPlugin | 3 | 10 |
| Commands + Suggest | 2 | 12 |
| Markdown Processors | 2 | 14 |
| CSS + Settings | 2 | 16 |
| **Total** | **16** | |

---

## 5. Quality Gate

7 pass/fail gates. Plugin does not ship until all pass.

### Gate 1: No saveData() for per-note state
- Open `.obsidian/plugins/convergence-board/data.json`
- Must contain ONLY: routes, enableRibbon, showInlineBadge, showStatusBanner, confidenceThreshold
- Zero file paths or per-note state objects
- Grep check: `noteStates` must not appear in codebase

### Gate 2: All CSS uses Obsidian variables
- `grep '#[0-9a-fA-F]\{3,8\}' styles.css` → zero matches
- `grep 'rgb\|rgba\|hsl' styles.css` → zero matches
- Manually verify in: Default (light/dark), Minimal (light/dark)

### Gate 3: Mobile parity
- All 5 commands work via command palette on mobile
- Board opens as full pane (not sidebar) on mobile
- All list items editable via tap
- No hover-only interactions
- Minimum 44px tap targets

### Gate 4: Graceful degradation
- Note with no frontmatter → no errors, no decorations, board shows empty message
- Note with frontmatter but no `convergence:` → same
- Note with malformed convergence → plugin doesn't crash, logs warning
- Note with valid convergence → everything renders

### Gate 5: Dataview compatibility
```dataview
TABLE convergence.mode AS Mode, convergence.route AS Route, convergence.confidence AS Confidence
FROM ""
WHERE convergence.mode
SORT convergence.confidence DESC
```
Must return correct results for all convergence-enabled notes.

### Gate 6: No network calls
- Disconnect from internet, restart Obsidian
- All features work
- `grep 'fetch\|XMLHttpRequest\|WebSocket\|requestUrl' main.ts` → zero matches

### Gate 7: Uninstall clean
- Create 5 notes with convergence state
- Uninstall plugin
- All 5 notes retain `convergence:` frontmatter
- `.obsidian/plugins/convergence-board/` directory removed
- No orphaned files

---

## 6. Ecosystem Positioning

### Category: Decision Workflow

This category doesn't exist yet. Nearest neighbors:

| Plugin | What it does | How we differ |
|--------|-------------|---------------|
| Tasks (3.3M) | Manages to-dos | We manage the *reasoning* that leads to a to-do |
| Kanban (2.2M) | Cards across columns | We manage *thinking state* within a single note |
| Dataview (3.9M) | Queries data | We *structure the data* that Dataview queries |
| Smart Connections (877K) | AI semantic search | We use *no AI* to structure decisions |
| Copilot (1.2M) | AI chat sidebar | We're deterministic, not probabilistic |

### One-Sentence Pitch

> Turn any note into a live decision surface that shows what you know, what's missing, and what to do next — no AI required.

### README Opening

```
You have a note with 47 lines of research, 3 linked notes, and 5 open questions.
You've been staring at it for a week.

Convergence Board helps you finish thinking about it.

- Explore: What do I know? What am I still missing?
- Converge: What route is this? What evidence do I need?
- Commit: Here is the action I'm taking, and here is why.

All state lives in your note's YAML frontmatter. No database. No cloud.
If you uninstall the plugin, your decision trail stays in your files.
```

---

## 7. Application Alignment

### Technical Checklist Mapping

| Item | Depth | Where in Code |
|------|-------|---------------|
| **TypeScript** | Strong | Entire plugin. Strict mode. Interfaces for all data shapes. |
| **CodeMirror** | Strong | ViewPlugin, WidgetType (x2), StateField, StateEffect, Decoration.widget(), DecorationSet |
| **CSS** | Strong | Complete stylesheet, Obsidian variables only, theme-compatible, responsive |
| **Markdown parsers** | Strong | PostProcessor, CodeBlockProcessor, processFrontMatter() |
| **CRDTs** | Moderate | Frontmatter = merge-safe by construction. Interview: Yjs vs Automerge tradeoffs |
| **Electron** | Moderate | Desktop sidebar, Platform branching, renderer process model |
| **Encryption** | Moderate | Frontmatter covered by Sync E2EE. Architecture choice enables encryption. |
| **Infrastructure** | Moderate | esbuild, manifest, GitHub Actions release workflow |
| **Capacitor** | Light | No Node-only APIs, mobile pane layout, Platform.isMobile |
| **iOS** | Light | Command palette, full pane, standard inputs |
| **Android** | Light | Same as iOS + back button consideration |

### "Why Would You Be a Good Fit?" Draft (403 words)

I have spent the last five years building systems that help people make better decisions with structured information. Most recently, I designed and built a multi-agent intelligence system that routes problems through 121 structured categories, maintains a 176-entry sourced knowledge library, and coordinates 12 specialized AI agents — all governed by a three-tier decision framework (immutable rules, updatable assumptions, append-only execution log). The system runs across Claude, GPT, Gemini, and Mistral simultaneously, with each agent contributing its strengths to a shared knowledge surface.

What drew me to Obsidian is that you have already solved the hardest version of the problem I care about: making structured knowledge belong to the user, not the application. "File over app" is not just a slogan — it is an engineering constraint that shapes every API decision, every data model, and every plugin review. I built my own system on the same principle: all state lives in YAML files on disk, all decisions are append-only, and any component can be replaced without losing data. When I built the Convergence Board plugin, the first architectural decision was to store all per-note state in YAML frontmatter via `processFrontMatter()`, not in `saveData()`. That choice was not clever — it was obvious, because I already think this way.

On the technical side, I work across the full stack you need. My plugin uses deep CodeMirror 6 integration (`ViewPlugin`, `WidgetType`, `StateField`, `StateEffect`, `Decoration.widget()`) for inline editor decorations. I write TypeScript in strict mode with explicit interfaces for every data shape. I have built and shipped production systems on Electron, and I understand the security model (CSP, renderer isolation, `nodeIntegration` deprecation). I have worked with CRDTs (Yjs and Automerge) in collaborative editing contexts and understand why Obsidian Sync's diff-match-patch approach is the right tradeoff for a file-based system. I have built CI/CD pipelines, managed infrastructure at scale, and shipped mobile experiences via Capacitor.

But the real reason I would be a good fit is not technical. It is that I am an Obsidian user who builds tools for other Obsidian users. The Convergence Board exists because I needed it — I had notes I could not finish, decisions I could not close, and no plugin that helped me do that. Building tools that solve your own problems, and then making them good enough for everyone else, is what I think this job is about.

I want to build the editor that 1.5 million people trust with their thinking.

---

## 8. v0.2 Roadmap (Deferred)

These are explicitly NOT in v0.1:

| Feature | Source | Why Deferred | Est. Hours |
|---------|--------|-------------|-----------|
| Wiki health / lint | Karpathy pattern + Gemini | Needs vault-wide indexing (~4-6h) | 6 |
| Schema validation | Gemini (Evidence Guardian) | Over-engineered for v0.1 | 8 |
| LLM-assisted ingest | Karpathy pattern | v0.1 must be zero-network | 4 |
| Convergence chains | Kiro (dependency graph) | Needs graph UI (PIXI.js/D3) | 8 |
| CRDT-aware merge | Kiro (Yjs/Automerge) | Frontmatter LWW is sufficient for Sync | 6 |
| Enhanced route scoring | Codex (NLP matching) | Keep v0.1 scope tight | 4 |
| Export/share | Community request | Nice-to-have | 2 |

---

## 9. File Manifest

| File | Purpose | ~Lines |
|------|---------|--------|
| `main.ts` | Plugin entry point — all TypeScript | ~1200 |
| `styles.css` | Theme-compatible stylesheet | ~200 |
| `manifest.json` | Plugin metadata | 10 |
| `versions.json` | Version history | 3 |
| `package.json` | Dependencies and scripts | 25 |
| `tsconfig.json` | TypeScript config | 20 |
| `esbuild.config.mjs` | Build config | 30 |
| `.eslintrc.json` | Lint config | 20 |
| `.github/workflows/release.yml` | CI/CD release | 25 |
| `README.md` | User-facing documentation | ~100 |

---

## 10. Appendices

### A. Dataview Query Cookbook

**All convergence notes by mode:**
```dataview
TABLE convergence.mode AS Mode, convergence.route AS Route, convergence.confidence AS "Conf %"
FROM ""
WHERE convergence.mode
SORT convergence.confidence DESC
```

**Committed decisions only:**
```dataview
LIST convergence.next_action
FROM ""
WHERE convergence.mode = "commit"
```

**Stuck notes (explore mode, >7 days old):**
```dataview
TABLE convergence.route AS Route, convergence.updated AS "Last Updated"
FROM ""
WHERE convergence.mode = "explore" AND date(convergence.updated) < date(now) - dur(7 days)
```

**Missing evidence across vault:**
```dataview
TABLE convergence.missing AS "Missing Evidence"
FROM ""
WHERE convergence.missing
FLATTEN convergence.missing
```

### B. Design Provenance — Original Proposals

- Kiro: `palette/docs/competitions/obsidian-plugin-2026-04-07/KIRO_OBSIDIAN_PLUGIN_PROPOSAL.md`
- Codex: `palette/docs/competitions/obsidian-plugin-2026-04-07/CODEX_OBSIDIAN_PLUGIN_PROPOSAL.md`
- Codex alternative: `palette/docs/competitions/obsidian-plugin-2026-04-07/CODEX_OBSIDIAN_PLUGIN_ALTERNATIVE.md`
- Gemini: Bus message (Evidence Guardian — schema validation)
- Mistral: Bus message (Advanced Table Editor)
- Competition brief: `palette/docs/competitions/OBSIDIAN_PLUGIN_COMPETITION_BRIEF.md`
- Karpathy: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

### C. Karpathy Integration Map

| Karpathy Operation | v0.1 | v0.2 |
|--------------------|------|------|
| **Ingest** | Manual: user fills known/missing/blocked in Board | LLM-assisted: suggest items from note content |
| **Query** | Vault Overview modal + Dataview queries | Convergence chains (dependency graphs) |
| **Lint** | — | Wiki health commands: orphans, stale claims, contradictions |

---

*Assembled by claude.analysis from 4 crew proposals + Karpathy pattern. 10 iterations. Ready for crew review.*
