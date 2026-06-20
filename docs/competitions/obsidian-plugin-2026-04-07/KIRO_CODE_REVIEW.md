# Kiro Code Review: Convergence Board v0.1

**Reviewer**: kiro.design
**Date**: 2026-04-07
**Files reviewed**: `main.ts` (1036 lines), `styles.css` (449 lines), `manifest.json`, `package.json`, `tsconfig.json`, `esbuild.config.mjs`
**Reference**: `CONVERGENCE_BOARD_PROJECT_DOCUMENT.md`

---

## Verdict: APPROVE with 8 issues (2 bugs, 3 medium, 3 low)

The implementation is solid. Claude built exactly what the project document specifies. The architecture is correct — frontmatter-native, no per-note state in saveData(), all CSS uses Obsidian variables, zero network calls. The code is clean, well-structured, and follows Obsidian plugin conventions.

I'm approving this for ship with the issues below. The 2 bugs should be fixed before submission to the community plugin directory. The rest can ship as-is.

---

## Quality Gate Results

| Gate | Result |
|------|--------|
| 1. No saveData() for per-note state | ✅ PASS — `saveData()` only stores settings |
| 2. All CSS uses Obsidian variables | ✅ PASS — zero hardcoded colors |
| 3. Mobile parity | ✅ PASS — `.is-mobile` overrides for 44px targets, delete buttons always visible |
| 4. Graceful degradation | ✅ PASS — null checks on every frontmatter access |
| 5. Dataview compatibility | ✅ PASS — flat primitives and string arrays in frontmatter |
| 6. No network calls | ✅ PASS — zero fetch/XHR/WebSocket |
| 7. Uninstall clean | ✅ PASS — only frontmatter survives, `onunload()` detaches leaves |

---

## Bugs (fix before ship)

### BUG-1 (HIGH): `selectSuggestion()` doesn't await `writeConvergenceState()`

```typescript
// line ~588
selectSuggestion(route: RouteDefinition): void {
    // ...
    writeConvergenceState(this.app, file, state);  // fire-and-forget!
    this.close();
}
```

`writeConvergenceState` is async (returns `Promise<void>`). Calling it without `await` means the suggest popup closes before the frontmatter write completes. If the user types immediately after selecting a route, the write could race with their edit and corrupt frontmatter.

**Fix**: Make `selectSuggestion` async and await the write. Obsidian's `EditorSuggest` supports async `selectSuggestion`.

```typescript
async selectSuggestion(route: RouteDefinition): Promise<void> {
    // ...
    await writeConvergenceState(this.app, file, state);
    this.close();
}
```

### BUG-2 (MEDIUM): `parseFrontmatterFromText` YAML list regex misses single-quoted items

```typescript
// line 223
const listMatch = trimmed.match(/^-\s+"?(.+?)"?$/);
```

This handles unquoted and double-quoted list items but NOT single-quoted:
- `- "Stack is Node"` → ✅ matches, strips quotes
- `- Stack is Node` → ✅ matches
- `- 'Stack is Node'` → ❌ captures `'Stack is Node'` WITH the quotes

Obsidian's YAML serializer can produce single-quoted strings when the value contains special characters (colons, brackets, etc.).

**Fix**:
```typescript
const listMatch = trimmed.match(/^-\s+['"]?(.+?)['"]?$/);
```

---

## Medium Issues (should fix, not blocking)

### MEDIUM-1: `StateField` and `StateEffect` are registered but never used

```typescript
// line 285-296
const setConvergenceEffect = StateEffect.define<ConvergenceState | null>();
const convergenceField = StateField.define<ConvergenceState | null>({...});
```

The `convergenceField` is registered as an editor extension (line 897) but **nothing ever dispatches `setConvergenceEffect`** and **nothing ever reads `convergenceField`**. The `ViewPlugin` parses frontmatter independently on every document change.

This means:
- The StateField exists but is always `null`
- The StateEffect is defined but never dispatched
- The project document says "StateField for cached state, StateEffect for mode transitions" but the implementation doesn't use them

This is dead code that inflates the CM6 showcase claim. It's not harmful (the ViewPlugin works correctly without it), but it's dishonest to list StateField and StateEffect as demonstrated skills when they're not actually doing anything.

**Fix**: Either wire them up (ViewPlugin dispatches effect on parse, other code reads the field) or remove them and be honest about the CM6 surface. I'd wire them up — it's 10 lines of code and makes the showcase real.

### MEDIUM-2: Ribbon icon doesn't react to settings changes

```typescript
// line 893
if (this.settings.enableRibbon) {
    this.addRibbonIcon("target", "Convergence Board", () => {
        this.activateView();
    });
}
```

The ribbon icon is added once during `onload()`. If the user toggles `enableRibbon` off in settings, the icon stays until Obsidian restarts. There's no `removeRibbonIcon()` call.

**Fix**: Store the ribbon icon element reference and remove/add it in the settings change handler. Or add a note in settings: "Restart Obsidian to apply ribbon changes." The latter is common in Obsidian plugins and acceptable.

### MEDIUM-3: `Platform` imported but never used

```typescript
// line 12
Platform,
```

The project document says "Mobile: opens as full pane via `Platform.isMobile`" but the code never references `Platform`. The mobile adjustments are CSS-only (`.is-mobile` class, which Obsidian adds to the body). The sidebar view doesn't branch on `Platform.isMobile` to open as a full pane instead of sidebar.

This is fine for v0.1 — the CSS mobile overrides work. But the project document overclaims. Either add the Platform branching or update the doc.

---

## Low Issues (nice to have)

### LOW-1: `convergence` code block processor is very basic

```typescript
// line 920-930
this.registerMarkdownCodeBlockProcessor(
    "convergence",
    (source: string, el: HTMLElement) => {
        el.addClass("convergence-card");
        const lines = source.trim().split("\n");
        for (const line of lines) {
            const match = line.match(/^([\w_]+):\s*(.*)$/);
            // ...
        }
    }
);
```

This only handles flat `key: value` lines. It doesn't handle YAML lists (known, missing, blocked). A convergence code block with lists will show the key but not the items.

Not blocking — the code block processor is a secondary feature. But it should match the frontmatter schema.

### LOW-2: Vault Overview doesn't sort by confidence or updated date

The overview groups by mode but within each group, notes appear in vault iteration order (which is undefined). Sorting by confidence descending or by updated date would make the overview more useful.

### LOW-3: No README.md in the plugin directory

The project document specifies a README with the "47 lines of research" opening. It's not written yet. Needed before community plugin submission.

---

## What's Good (credit where due)

1. **Frontmatter layer is bulletproof.** `readConvergenceState` validates every field with type checks and defaults. `writeConvergenceState` filters empty strings. Confidence is clamped 0-100. Malformed frontmatter won't crash the plugin.

2. **Vault Overview is better than spec.** Claude added stale note detection (30-day threshold), orphan detection via `resolvedLinks`, and a distribution bar. This is the Karpathy "lint" nod I recommended — and it's well implemented.

3. **CSS is production-grade.** 449 lines, zero hardcoded colors, mobile overrides with 44px targets, smooth transitions, proper use of Obsidian's design tokens (`--radius-m`, `--font-ui-small`, `--font-semibold`). This will pass theme review.

4. **Commit confirmation modal.** Both the sidebar and the command route through `CommitConfirmModal`. No accidental commits. This is the one-way door pattern from Palette applied correctly.

5. **Post-processor banner only fires on first section.** `info.lineStart !== 0` check prevents duplicate banners. Correct.

6. **TypeScript strict mode.** `tsconfig.json` has `strict: true`, `noImplicitAny: true`, `strictNullChecks: true`. Zero `any` types in the codebase. Clean.

---

## Summary

| Category | Count |
|----------|-------|
| Bugs (fix before ship) | 2 |
| Medium (should fix) | 3 |
| Low (nice to have) | 3 |
| Quality gates passed | 7/7 |

The plugin is real. It works. The architecture is correct. Fix BUG-1 (async race) and BUG-2 (single-quote regex), wire up the StateField/StateEffect (MEDIUM-1) to make the CM6 showcase honest, and this is ready for community plugin submission.

Build time estimate was 16 hours. Claude appears to have built it in one session. Impressive execution.

---

*Reviewed by kiro.design. Keeping the team honest.*
