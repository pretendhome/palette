# Palette Skill Packs

Skill packs inject validated domain knowledge into agent sessions. They bridge the gap between Palette's RIU taxonomy (which routes problems) and agent execution (which solves them).

## Format

Each skill pack is a markdown file at `palette/skills/<domain>/<skill-name>.md` with:

### Frontmatter (YAML)
- **id**: Skill identifier (e.g., `SKILL-001`)
- **name**: Human-readable name
- **domain**: Knowledge domain
- **for_agents**: Which Palette archetypes can use this skill (e.g., ["Theri", "Rex"])
- **triggers**: When this skill should be loaded (mapped to RIUs)
- **impressions**: Current impression count (follows Palette impressions system)
- **status**: UNVALIDATED / WORKING / PRODUCTION

### Body (Markdown)
Domain-specific knowledge, patterns, gotchas, and validated approaches. This content is injected into the agent's context when the skill is triggered.

## Rules

1. Skills are READ-ONLY context — they inform agent behavior but don't grant new capabilities.
2. Skills follow the impressions system: start at 0, earn trust through validated use.
3. Skills are loaded ONLY when relevant (not all skills all the time — context is precious).
4. A skill at PRODUCTION status (50+ impressions) can be trusted without spot-checking.
5. Skills should stay under 100 lines. If larger, split into sub-skills.
