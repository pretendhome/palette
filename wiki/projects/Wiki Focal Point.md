---
convergence:
  mode: converge
  route: execution
  confidence: 55
  known:
    - "Deterministic compiler exists and works (compile_wiki.py)"
    - "332 wiki pages generated from knowledge library"
    - "8/8 validation passes"
    - "Phase 1 build assigned to Kiro"
    - "Validation assigned to Codex"
    - "Health monitoring assigned to Claude"
  missing:
    - "Focal point UI not built"
    - "Real-time recompilation on knowledge library change"
    - "Search across wiki pages"
  blocked: []
  next_action: "Kiro delivers Phase 1 build, then validate with Codex"
  updated: 2026-04-07T12:00:00Z
---

# Wiki Focal Point

A deterministic compiler that transforms the Palette knowledge library into browsable wiki pages. The compiler is operational. The focal point UI is next.

## Current State

- **Compiler**: `compile_wiki.py` — transforms 176 knowledge entries into 332 wiki pages
- **Validator**: `validate_wiki.py` — 8/8 checks pass
- **Governance**: Proposed entries flow through voting pipeline before promotion

## Architecture

The wiki is generated state, not authored content. Source of truth is always the knowledge library YAML. The compiler is deterministic — same input always produces same output.

## Links

- [[Governance Model]]
- [[Knowledge Library]]
