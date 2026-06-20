# COMPETITION BRIEF: Obsidian Plugin — North Star Project

**Competition ID**: OBSIDIAN-PLUGIN-001
**Posted**: 2026-04-07
**Deadline**: 2026-04-08 19:00 UTC
**Bus Message ID**: 90af308c-d3ae-4847-a81c-ba50bd6f7f06

---

## Context

Obsidian (obsidian.md) is hiring their 4th engineer. The operator is applying.

**Company Profile**:
- Founded March 2020 by Shida Li (CTO) and Erica Xu (COO), University of Waterloo
- CEO: Steph Ango (kepano) — joined from community (created Minimal theme)
- Fully bootstrapped. Zero investors. No stock options. ~$25M ARR, ~$350M est valuation
- ~18 people, only 3 engineers (hiring 4th)
- 1.5M MAU, 10,000+ organizations (Amazon, Meta, Capital One, UK Government)
- Philosophy: "File over app," local-first, no telemetry, user sovereignty

**Application Requirements**:
- Senior/staff-level, 8+ years experience
- Technical checklist: Android, Ansible, Capacitor, CodeMirror, CRDTs, CSS, Electron, Encryption, Infrastructure, iOS, Markdown parsers, TypeScript
- Must be an Obsidian user
- "Why would you be a good fit?" — 200-500 words (most important question)
- **Obsidian-related projects** (plugins, themes, tools, blog posts) — THIS IS WHAT WE'RE BUILDING

## Tech Stack

- **Desktop**: Electron (Chromium-based), custom UI (no React/Angular/Vue)
- **Mobile**: Capacitor (Ionic) for iOS and Android
- **Editor**: CodeMirror 6 — heavily customized for markdown live preview
- **Language**: TypeScript (primary)
- **Markdown**: markdown-it / remark parsers
- **Graph**: PIXI.js / WebGL + D3.js force simulation
- **Sync**: AES-256-GCM E2EE, scrypt key derivation, diff-match-patch for 3-way merge
- **Build**: esbuild for plugins
- **Presentations**: Reveal.js
- **PDF**: PDF.js
- **Math**: MathJax 3
- **Diagrams**: Mermaid.js

## Plugin API

Plugins are TypeScript compiled to a single `main.js` via esbuild.

**Core interfaces**:
- `App` — global entry point
- `Vault` — file CRUD operations
- `Workspace` — UI layout, pane management
- `MetadataCache` — cached markdown metadata (links, headings, tags, frontmatter)
- `FileManager` — high-level file operations

**Registration hooks**:
- `addRibbonIcon()` — left sidebar icons
- `addStatusBarItem()` — status bar elements
- `addCommand()` — global/editor commands with hotkeys
- `addSettingTab()` — custom settings panels
- `registerView()` — custom view types (new panes)
- `registerExtensions()` — custom file extension handlers
- `registerEditorExtension()` — CodeMirror 6 extensions
- `registerEditorSuggest()` — editor autocomplete
- `registerMarkdownPostProcessor()` — post-process rendered markdown
- `registerMarkdownCodeBlockProcessor()` — custom code block languages

**Lifecycle**: `onload()`, `onunload()`, `onUserEnable()`, `onExternalSettingsChange()`
**Data**: `loadData()` / `saveData()` for JSON settings

## Ecosystem Analysis (2,749 Plugins)

### Top Downloads
1. Excalidraw (5.7M) — drawing/diagramming
2. Templater (3.9M) — dynamic templates with JS
3. Dataview (3.9M) — SQL-like queries over vault
4. Tasks (3.3M) — task management
5. Advanced Tables (2.7M) — spreadsheet-like tables
6. Calendar (2.5M) — daily notes navigation
7. Git (2.3M) — version control
8. Style Settings (2.2M) — theme customization
9. Kanban (2.2M) — markdown-backed boards
10. Copilot (1.2M) — AI writing assistant

### AI Plugin Landscape
- **Smart Connections** (877K) — local-first embeddings, semantic linking, vault chat via RAG
- **Copilot** (1.2M) — chat sidebar, multi-provider (OpenAI, Anthropic, Google, Ollama)
- **SystemSculpt** — approval workflows, semantic search, governed actions
- **Obsilo Agent** — 55+ tools, hybrid search, MCP connectors, multi-agent workflows
- **YOLO** — agent mode with tool-calling, persistent memory
- **Sonar** — fully local semantic search with Llama.cpp

### What's MISSING
- **No deterministic knowledge routing** — all AI plugins are probabilistic (LLM-dependent)
- **No structured convergence** — no explore → converge → commit workflow
- **No taxonomy-based routing** — no plugin maps intent to structured problem categories
- **No wiki governance** — no proposal/vote/promote lifecycle for knowledge
- **No convergence chain** — no dependency graph traversal for project state
- **No voice-to-structured-data** — Whisper plugin does transcription, not intent parsing

## Competition Rules

Each agent submits a PROPOSAL with:

1. **Plugin name** and one-line pitch
2. **Gap analysis** — what gap it fills, with evidence from the ecosystem
3. **Technical architecture** — specific Obsidian API hooks, views, CodeMirror extensions
4. **Checklist coverage** — which job-posting items it demonstrates:
   - [ ] TypeScript
   - [ ] CodeMirror
   - [ ] CRDTs
   - [ ] CSS
   - [ ] Electron
   - [ ] Encryption
   - [ ] Markdown parsers
   - [ ] Infrastructure
   - [ ] Capacitor
   - [ ] iOS / Android
5. **User story** — why an Obsidian user would install this
6. **Build estimate** — hours
7. **North star alignment** — how this feeds back into Palette

## Agent Roles

| Agent | Role | What We Expect |
|-------|------|----------------|
| **Kiro** (kiro.design) | Design lead | Most technically precise proposal. API surface, UX flows, quality gate. |
| **Codex** (codex.implementation) | Product strategy | Most compelling to actual Obsidian users. Market fit, adoption angle. |
| **Claude** (claude.analysis) | Implementation lead | Full proposal + will build the winner. Deepest architecture. |
| **Gemini** (gemini.specialist) | Research specialist | Competitive analysis, feasibility. Identify riskiest assumptions. |
| **Mistral** (mistral-vibe.builder) | Builder | Alternative approach. Surprise us. |

## Judging Criteria

1. **Real gap?** — Does it fill a genuine hole in the 2,749-plugin ecosystem?
2. **Community downloads?** — Would actual Obsidian users install this?
3. **Skill showcase?** — Does it demonstrate the operator's fit for the engineering role?
4. **Buildable?** — Can it ship in 2-3 days?
5. **Palette flywheel?** — Does it feed back into the system?

## Deadline

**2026-04-08 19:00 UTC**

Post proposals to the Peers bus addressed to `human.operator`.

The winner gets built and shipped to the Obsidian community plugin directory.

---

*Posted by the Operator. Competition ID: OBSIDIAN-PLUGIN-001.*
