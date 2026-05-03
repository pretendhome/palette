# Palette — Claude Code Project Instructions

## What This Is
Palette is a multi-agent intelligence system that routes any AI/ML decision to the right combination of internal knowledge and external services. It is NOT a wrapper around one LLM — it orchestrates 12 specialized agents, 121 problem-solution taxonomies (RIUs), 176 knowledge entries, 69 integration recipes, and 40+ external service routes.

## Quick Orientation
- **MANIFEST.yaml** — single source of truth for all current versions and paths. Read this first.
- **docs/CLAUDE_OPERATIONAL_RUNBOOK.md** — fast orientation, common operations, grep patterns.
- **core/palette-core.md** — Tier 1 immutable rules. Never violate these.
- **decisions.md** — Tier 3 execution log. Append decisions here, never delete.

## Two Operating Modes

### Mode 1: Palette-Native Work
**When**: Building the system itself, adding knowledge, evaluating services, doing buy-vs-build analysis, designing agents, updating taxonomy.

**Cadence** (MUST follow):
1. Classify the problem → find the RIU in `taxonomy/releases/v1.3/`
2. Check the knowledge library → `knowledge-library/v1.4/`
3. Check service routing → is this `internal_only` or `both`?
4. Route to the right agent role (see Agent Role Selection in Runbook)
5. Log material decisions in `decisions.md`

### Mode 2: Skill Execution
**When**: Applying a validated skill to a real problem — writing a resume, prepping for an interview, planning a trip, designing a learning program.

**Cadence**:
1. Load the relevant skill from `skills/<domain>/`
2. Follow the skill's methodology
3. The skill was BUILT using the Palette protocol; executing it doesn't require re-routing through RIUs every time
4. Log ONE-WAY DOOR decisions in `decisions.md`

**Active Skills**: retail-ai, talent, education, travel, enablement, lenses (see `skills/README.md`)

## Architecture (6 Layers)
1. **Core** (`core/`) — Governance tiers, immutable rules, assumptions
2. **Taxonomy** (`taxonomy/releases/v1.3/`) — 121 RIUs mapping problems to solution categories
3. **Knowledge Library** (`knowledge-library/v1.4/`) — 176 sourced, cited entries
4. **Agents** (`agents/`) — 12 specialized agents with maturity tracking
5. **Buy-vs-Build** (`buy-vs-build/`) — Service routing, people signals, 69 integration recipes
6. **Skills** (`skills/`) — Validated domain frameworks applied through implementations

## Agents
| Agent | Purpose | Implementation |
|-------|---------|---------------|
| resolver | Intent classification, maps input to RIU | Design spec |
| researcher | Research with Perplexity Sonar API as primary backend | Python (`researcher.py`) |
| architect | System design and tradeoff evaluation | Design spec |
| builder | Implementation within bounded spec | Design spec |
| debugger | Failure diagnosis and minimal repair | Design spec |
| narrator | GTM/narrative, evidence-based only | Design spec |
| validator | Plan assessment, GO/NO-GO verdicts | Design spec |
| monitor | Signal monitoring and anomaly detection | Go + Python |
| orchestrator | Workflow routing between agents | Go |
| business-plan-creation | Multi-agent business plan workflow | Design spec |
| health | System integrity checklist (8 sections) | Python (`health_check.py`) |
| total-health | Cross-layer audit (13 sections) | Python (`total_health_check.py`) |

## Repository Structure — Sandbox vs Production

| Repo | Visibility | Purpose |
|------|-----------|---------|
| `pretendhome/pretendhome` | **PRIVATE** | Sandbox — build, experiment, iterate |
| `pretendhome/palette` | **PUBLIC** | Production toolkit — shared with the world |
| `pretendhome/enablement` | **PUBLIC** | Production curriculum — shared with the world |

**Sandbox (pretendhome, PRIVATE)** contains `palette/` and `enablement/` as subtrees, plus private directories that never leave the sandbox:
- `implementations/` — where skills meet reality (talent, retail, education, travel)
- `archive/` — closed work
- `backups/` — snapshots

**Production (palette, PUBLIC)** is the toolkit — reusable frameworks, agents, knowledge, skills, voice tools, mission canvas engine. This is what gets shared with interviewers, the NSA team, collaborators, and the world.

**The rule: subtree push = deploy to production.** Everything in `palette/` goes public on push. Before pushing, verify no private content leaked in.

Skills live in palette. Implementations live in pretendhome. Learnings flow back into skill updates. Reusable toolkit parts move to palette when ready.

### External Repos Governed by Palette
- **`~/learning-architecture`** (`github.com:lingua-viva/learning-architecture.git`) — Claudia Canu Fautré's public learning design portfolio. Changes governed by Palette education + talent skills. See its `CLAUDE.md` for the connection protocol. Pull both repos before making cross-repo changes.

## Key Conventions
- **Glass-box architecture**: Every decision must be traceable. No black boxes.
- **Convergence protocol**: Agents must converge toward a decision, not cycle indefinitely.
- **Semantic blueprints**: Every non-trivial task starts with goal/roles/capabilities/constraints/non-goals.
- **ONE-WAY DOOR classification**: Irreversible decisions require human review.
- **Evidence bar**: Tier 1 sources (Google/Anthropic/OpenAI/AWS/Meta), Tier 2 (NIST/EU/peer-reviewed), Tier 3 (>500-star GitHub).
- **Privacy**: Never commit personally identifiable child data. Use anonymized avatars (e.g., ARON).
## Running Tests
```bash
uv run pytest -q scripts/palette_intelligence_system/test_*.py
```

## Running Integrity Checks
```bash
uv run python scripts/palette_intelligence_system/integrity.py
```

## Push Protocol
```bash
git push origin main                                    # always
git subtree push --prefix=palette palette main          # only if palette/ files changed
```

## Do NOT
- Modify `core/palette-core.md` without explicit human approval (Tier 1, immutable)
- Delete entries from `decisions.md` — append only
- Skip the MANIFEST when looking for current versions
- Fabricate sources or claims — evidence-based only
- Commit personally identifiable information about children
- Use API credits — authenticate via Claude.ai subscription account only
