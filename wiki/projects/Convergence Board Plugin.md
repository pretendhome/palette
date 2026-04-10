---
convergence:
  mode: converge
  route: execution
  confidence: 82
  known:
    - "2,370+ lines TypeScript, 900+ lines CSS"
    - "Two sidebar views: Decision Board + Bus Dashboard"
    - "CM6 StateField with block decorations, WidgetType badges"
    - "5 modals: VaultOverview, CommitConfirm, QuickSend, AssignTask, CreateActivityNote"
    - "Bus Dashboard: agent status, checkpoints, search, capture"
    - "Frontmatter-native via processFrontMatter with merge guard"
    - "Mobile parity: Platform.isMobile, 44px touch targets"
    - "Theme compatible: all CSS uses Obsidian variables"
    - "Clean TypeScript: 0 type errors"
    - "12 commands registered"
  missing:
    - "Application not yet submitted"
    - "No public standalone repo yet"
  blocked: []
  next_action: "Submit Obsidian engineering application"
  bus_query: "obsidian"
  updated: 2026-04-08T17:00:00Z
---

# Convergence Board Plugin

Obsidian plugin that turns any note into a live decision surface with explore -> converge -> commit workflow. Built for the Obsidian Plugin Competition.

## Thesis

Obsidian helps you accumulate and connect ideas. Convergence Board helps you resolve one.

## Technical Highlights

- **CM6**: StateField with `provide: EditorView.decorations.from(field)` for block decorations, WidgetType for inline badge + confidence bar
- **Obsidian API**: processFrontMatter, MetadataCache, EditorSuggest, 2 ItemViews, requestUrl, MarkdownPostProcessor, registerMarkdownCodeBlockProcessor, file-menu event, status bar, view state serialization
- **Bus layer**: requestUrl to local HTTP broker, agent status strip, checkpoint approve/reject, FTS5 search, message capture to frontmatter
- **Architecture**: file-over-app, deterministic core, Dataview compatible, uninstall clean, graceful offline for bus features

## Crew Contributions

| Agent | Contribution % | Key Idea |
|-------|---------------|----------|
| Claude | 38% | Synthesis, execution, vault health, CM6 field architecture |
| Kiro | 27% | Frontmatter-native, file-over-app, quality gates, code review |
| Codex | 23% | Product vision, naming, ecosystem positioning, pitch |
| Gemini | 7% | Feasibility, improvements list, bus relay |
| Mistral | 5% | Original scaffold, scoring |

## Links

- [[Job Search]]
- [[Palette]]
