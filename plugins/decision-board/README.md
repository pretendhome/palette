# Decision Board

An Obsidian plugin that turns any note into a lightweight decision surface — what you know, what's unclear, what happens next.

## What it does

Add `status: open` to any note's frontmatter and Decision Board tracks your thinking:

- **Status**: open / thinking / decided
- **Known**: what you know so far
- **Missing**: what's still unclear
- **Next action**: what happens next

All state lives in YAML frontmatter via `processFrontMatter()`. Zero plugin-owned databases. Notes remain plain markdown files.

## Vault Overview

The real power: open the **All Decisions** modal to see every decision across your vault, grouped by status, with stale items (>7 days) flagged. It answers: *across everything I'm working on, where am I stuck?*

## API surfaces demonstrated

425 lines, 14 distinct Obsidian API integrations:

| Surface | Usage |
|---------|-------|
| `ItemView` | Sidebar with three render states |
| `StateField` + `provide` | CM6 block decorations |
| `WidgetType` | Custom status badge widget |
| `registerMarkdownPostProcessor` | Reading view status banner |
| `registerMarkdownCodeBlockProcessor` | `decision` code blocks |
| `Modal` | Vault overview + confirmation dialogs |
| `PluginSettingTab` | 4 toggle settings |
| `addCommand` | 4 commands |
| `addRibbonIcon` | Sidebar toggle |
| `addStatusBarItem` | Status indicator |
| `processFrontMatter` | Frontmatter read/write |
| `MetadataCache` | Vault-wide decision scanning |
| `Platform.isMobile` | Mobile layout branching |
| `debounce` | Throttled status bar updates |

## Install

```bash
npm install --legacy-peer-deps
npm run build
```

Copy `main.js`, `manifest.json`, and `styles.css` to your vault's `.obsidian/plugins/decision-board/` directory.

## Design principles

- **File over app**: all state in frontmatter, queryable by Dataview
- **Zero network calls**: works fully offline
- **Theme compatible**: zero hardcoded colors, all CSS variables
- **Mobile parity**: 44px touch targets, full-pane layout on mobile
- **Uninstall clean**: removing the plugin leaves only your frontmatter
