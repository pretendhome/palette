# Codex Alternative Proposal — Obsidian Plugin Competition

**Author:** `codex.implementation`  
**Date:** `2026-04-07`  
**Competition:** `OBSIDIAN-PLUGIN-001`

## Plugin

**Name:** `Decision Ledger`  
**One-line pitch:** A local-first plugin that turns Obsidian into an auditable decision journal with proposals, objections, approvals, and committed outcomes.

## Why This Exists

`Convergence Board` is the better first bet for broad adoption because it starts earlier in the user workflow. This alternative is narrower but sharper: it focuses on the last mile of decision-making.

Many Obsidian users already document plans, meeting notes, and options, but they do not have a strong markdown-native way to answer:

- what was proposed
- what objections were raised
- what was approved
- what changed
- what is now binding

`Decision Ledger` is an answer to that gap.

## Gap Analysis

The ecosystem has strong planning, PKM, task, and AI retrieval tools. It has weak support for **governed decision history** inside markdown.

This proposal fills a niche for:

- solo operators who want durable reasoning trails
- teams using shared Obsidian vaults
- founders tracking decisions across product, hiring, and operations

It is less broad than `Convergence Board`, but very differentiated and highly legible.

## Architecture

- `registerView()` for a `Decision Ledger` pane
- `addCommand()` for `Create proposal`, `Record objection`, `Approve decision`, `Archive outcome`
- `registerMarkdownCodeBlockProcessor()` for fenced `proposal`, `vote`, and `decision` blocks
- `registerMarkdownPostProcessor()` for rendering decision status cards inline
- `MetadataCache` for indexing proposal tags and cross-note references
- `Vault` / `FileManager` for writing durable markdown-native records
- `loadData()` / `saveData()` for templates, workflow labels, and archive preferences

## Checklist Coverage

- `TypeScript`: strong
- `CodeMirror`: moderate, mainly for structured insertions and suggestions
- `CRDTs`: moderate discussion point via sync-safe markdown state
- `CSS`: strong, pane and decision cards
- `Markdown parsers`: strong
- `Encryption`: indirect, same local-first story
- `Electron`: moderate
- `Infrastructure`: moderate
- `Capacitor`: light
- `iOS / Android`: moderate for read/write, lighter for pane ergonomics

## User Story

I use Obsidian for project and research work, but I keep losing the actual decision trail. I can find notes, but I cannot quickly answer what we committed to and why. `Decision Ledger` gives me a durable record of proposals, objections, approvals, and outcomes directly in the vault.

## Build Estimate

**Target:** `14-16 hours`

This is slightly easier to build than `Convergence Board`, but it is also narrower and probably less exciting to a broad Obsidian audience.

## North Star Alignment

Strong fit with Palette governance and proposal/vote/promote logic. This plugin would show that the operator can translate governance machinery into a product artifact that ordinary users can understand.

## Recommendation

Build `Convergence Board` first. Keep `Decision Ledger` as the fallback if we want a tighter, more governance-forward concept.
