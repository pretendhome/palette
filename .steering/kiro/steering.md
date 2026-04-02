# Palette — Kiro Steering File

## Project Identity
**Palette** is a multi-agent intelligence system that routes AI/ML decisions to the optimal combination of internal knowledge and external services.

## Start Here
1. `MANIFEST.yaml` — all current versions and file paths
2. `CLAUDE_OPERATIONAL_RUNBOOK.md` — common operations and grep patterns
3. `core/palette-core.md` — immutable governance rules (Tier 1)

## Two Operating Modes

### Mode 1: Palette-Native Work
When building or modifying the system itself, follow the routing protocol:
1. Find the RIU → `taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml`
2. Check knowledge → `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`
3. Check service routing → `buy-vs-build/service-routing/v1.0/`
4. Route to agent → `agents/{role}/{role}.md`
5. Log decisions → `decisions.md`

### Mode 2: Skill Execution
When applying a skill to a real problem, load from `skills/<domain>/` and follow the skill's methodology. Active skills: retail-ai, talent, education, travel.

## Architecture
- **12 agents**: resolver, researcher, architect, builder, debugger, narrator, validator, monitor, orchestrator, business-plan-creation, health, total-health
- **121 RIUs**: problem-to-solution taxonomy
- **167 knowledge entries**: sourced, cited, tiered by evidence quality
- **69 integration recipes**: external service configurations
- **6 skill domains**: retail-ai, talent, education, travel, enablement, lenses

## Key Implementation
The researcher agent (`agents/researcher/researcher.py`):
- Routes queries to Perplexity Sonar API (sonar-pro / sonar-reasoning)
- Falls back to Tavily and Exa
- Synthesizes via Claude with structured JSON output
- Checks local knowledge library before external calls

## Governance
- **Tier 1** (`core/palette-core.md`): Immutable — convergence, glass-box, semantic blueprints
- **Tier 2** (`core/assumptions.md`): Updatable with evidence
- **Tier 3** (`decisions.md`): Append-only execution log

## Constraints
- Never modify Tier 1 without human approval
- Never delete from decisions.md
- All claims require sourced evidence
- No black boxes — every decision traceable
- Never commit personally identifiable child data — use anonymized avatars (e.g., ARON)
