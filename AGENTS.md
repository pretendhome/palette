# Palette — Codex Project Instructions

## Overview
Palette is a multi-agent intelligence system for AI/ML decision routing. It combines 12 specialized agents, a 121-unit problem taxonomy, 176 knowledge entries, and 70 integration recipes to route any AI decision to the right combination of internal knowledge and external services.

## Two Operating Modes

### Mode 1: Palette-Native Work (building the system)
Follow the full routing protocol:
1. Classify → find the RIU in `taxonomy/releases/v1.3/`
2. Check knowledge → `knowledge-library/v1.4/`
3. Check service routing → `buy-vs-build/service-routing/v1.0/`
4. Route to agent role (resolver, researcher, architect, builder, etc.)
5. Log decisions in `decisions.md`

### Mode 2: Skill Execution (applying the system)
Load the skill from `skills/<domain>/` and follow its methodology.
Active skills: retail-ai, talent, education, travel.
Skills encode the Palette protocol — you don't need to re-route through RIUs during execution.

## Project Structure
```
palette/
├── MANIFEST.yaml     # START HERE — single source of truth for all versions and paths
├── CLAUDE.md         # Claude Code instructions
├── AGENTS.md         # Codex instructions (this file)
├── .kiro/            # Kiro instructions
├── agents/           # 12 specialized agents
├── core/             # Governance (Tier 1 immutable, Tier 2 assumptions, Tier 3 decisions)
├── taxonomy/         # 121 RIUs — problem-to-solution routing
├── knowledge-library/# 176 sourced, cited entries
├── buy-vs-build/     # Service routing, people signals, 70 integration recipes
├── scripts/          # Integrity checks, audit, query engine
├── skills/           # Validated domain frameworks (retail-ai, talent, education, travel)
├── docs/             # Architecture guides, audit reports
├── bridges/          # External integrations (Telegram)
└── lenses/           # Optional context overlays
```

## Key Implementation: Research Agent
`agents/researcher/researcher.py` — the most complete agent implementation:
- **Primary backend**: Perplexity Sonar API (sonar-pro / sonar-reasoning)
- **Fallback chain**: Perplexity → Tavily → Exa
- **Synthesis**: Claude (structured JSON with confidence scores, gaps, sources)
- **Query routing**: Classifies as factual/current_events/academic/synthesis
- **Local-first**: Checks knowledge library before any external API call

## Active Skills
| Domain | What It Does | Validated On |
|--------|-------------|-------------|
| retail-ai | Enterprise AI strategy for small businesses | Gap Inc. (2026-02) |
| talent | Interview prep + application system | OpenAI, Perplexity, Glean |
| education | Adaptive learning for special needs | ARON pilot, La Scuola (2026-03) |
| travel | Multi-leg family route planning | Neill Summer 2026 (9 bookings) |

## Conventions
- Evidence-based only — every claim needs a source
- Glass-box — every decision traceable, no black boxes
- Convergence — progress toward decisions, don't cycle
- ONE-WAY DOOR gates — irreversible decisions need human review
- Privacy — never commit personally identifiable child data; use anonymized avatars
- Append-only decision log — never delete from `decisions.md`

## Testing
```bash
uv run pytest -q scripts/palette_intelligence_system/test_*.py
```

## Push Protocol
```bash
git push origin main
git subtree push --prefix=palette palette main
```
