# Naming Convention Audit
Date: 2026-03-02
Scope: `/home/mical/fde` and `/home/mical/fde/palette`

## 1) Repository Topology

- Local repo root: `/home/mical/fde`
- Nested working tree at `/home/mical/fde/palette` resolves to same git repo context.
- Remotes configured:
  - `origin` -> `git@github.com:pretendhome/pretendhome.git`
  - `palette` -> `git@github.com:pretendhome/palette.git`

### Branch/ref state observed
- Current branch: `main`
- HEAD: `e980fde`
- `origin/main`: `e980fde` (aligned with HEAD in local refs)
- `palette/main`: `d4ee09c` (diverged in local refs)
- Divergence count (local refs): `palette/main...HEAD` = `55 / 93` (left/right)

### Commit verification requested
- Commit `886b4e7` exists in repo history:
  - `886b4e7 Rename dinosaur agents to role-based names for external readability`

## 2) Engine Audit Results

Executed from `/home/mical/fde/palette`:

1. `python3 -m scripts.palette_intelligence_system.integrity --checks-only`
   - 8/8 consistency checks passing
   - Routing↔Recipe: `106/106`
   - Knowledge↔Taxonomy: `498/498`

2. `python3 -m scripts.palette_intelligence_system.audit_system`
   - Findings: `1` total
   - Severity: `0 critical, 0 high, 1 medium, 0 low`
   - Medium finding: missing people-signal coverage on a subset of both-classified RIUs

3. `python3 -m scripts.palette_intelligence_system.regression --check`
   - SLOs: `7 passing, 0 failing`
   - Regressions: `0`
   - Improvements: `44`

4. `python3 -m scripts.palette_intelligence_system.drift`
   - Drift clusters: `15` (`3 high, 9 medium, 3 low`)

5. `python3 -m scripts.palette_intelligence_system.para_decision`
   - Decision: `ship_with_risks`
   - Rationale: hard gates pass, medium/low risks remain

### Test runner status
- `pytest` binary unavailable in this environment
- `python3 -m pytest` also unavailable (`No module named pytest`)
- Unit tests not executable in current runtime without installing pytest.

## 3) Naming Convention Audit (Role-based names)

### Audit intent
Validate migration from dinosaur/codename labels to clear role names:
- resolver, researcher, architect, builder, debugger, narrator, validator, monitor, orchestrator

### Aggregate signal
- Legacy-name references found (excluding `.git`, archive, garbage):
  - `149 files`
  - `1345 total legacy-token hits`

This indicates migration is incomplete across active docs, prompts, and some runtime-facing text.

## 4) Findings (ordered by severity)

## HIGH

1. Broken/incorrect canonical path in main README
- File: `/home/mical/fde/palette/README.md:221`
- Issue: `agents/rex/` still listed, but active directory is `agents/architect/`.
- Impact: misleading onboarding and path breakage for users.

2. Core prompt still encodes legacy agent taxonomy
- File: `/home/mical/fde/palette/core/decisions-prompt.md:152`
- File: `/home/mical/fde/palette/core/decisions-prompt.md:158`
- Issue: maps to Argentavis/Therizinosaurus/Velociraptor/Rex/Yuty/Anky/Para names.
- Impact: core operating prompt is not aligned with the new contract; can reintroduce naming debt.

3. Runtime/CLI surfaces still emit legacy labels in active agent code
- File: `/home/mical/fde/palette/agents/resolver/resolver.py:542`
- File: `/home/mical/fde/palette/agents/architect/architect.py:35`
- File: `/home/mical/fde/palette/agents/builder/builder.py:35`
- File: `/home/mical/fde/palette/agents/debugger/debugger.py:40`
- File: `/home/mical/fde/palette/agents/narrator/narrator.py:34`
- File: `/home/mical/fde/palette/agents/validator/validator.py:34`
- File: `/home/mical/fde/palette/agents/monitor/monitor.py:34`
- Issue: class names/help text/banner strings still dinosaur/codename-heavy.
- Impact: operator confusion and inconsistent API/UX terminology.

## MEDIUM

1. Governance docs still route via old names
- File: `/home/mical/fde/palette/docs/PARA_DECISION_CONTRACT.md:17`
- File: `/home/mical/fde/palette/docs/PARA_DECISION_CONTRACT.md:20`
- Issue: routes to `Raptor/Rex/Argy` rather than role labels.

2. Architecture diagram remains mixed-name
- File: `/home/mical/fde/palette/docs/architecture/PIS_E2E_SYSTEM_GRAPH_2026-03-02.md:10`
- File: `/home/mical/fde/palette/docs/architecture/PIS_E2E_SYSTEM_GRAPH_2026-03-02.md:84`
- Issue: `Cory/Resolver`, `Raptor/Rex/Argy`, `Para` references remain.

3. Tooling scripts/docs still mention legacy invocation labels
- File: `/home/mical/fde/palette/scripts/setup-perplexity-mcp.sh:91`
- File: `/home/mical/fde/palette/scripts/sync-impressions.py:55`
- File: `/home/mical/fde/palette/skills/README.md:13`

## LOW

1. Historical/analysis artifacts preserve legacy labels
- `decisions.md`, `assets/UX/*`, `business-plan-creation/*`, older convergence briefs.
- Likely expected for historical traceability; should be explicitly marked as legacy references if retained.

2. Module path naming residue
- File: `/home/mical/fde/palette/agents/monitor/go.mod:1`
- Issue: module path still `.../agents/parasaurolophus`.
- Impact: low functional risk if internal, but inconsistent branding/identity.

## 5) Conclusion

- Structural engine health: strong (integrity/regression checks passing).
- Naming migration: **not yet coherent end-to-end**.
- Current status: production logic is healthy, but human-facing and prompt-facing naming consistency still has material debt.

## 6) Recommended Fix Order

1. Canonical docs + core prompt first
   - `README.md`, `core/decisions-prompt.md`, `docs/PARA_DECISION_CONTRACT.md`, architecture graph.
2. Runtime-facing agent strings and class names
   - Resolver/Architect/Builder/Debugger/Narrator/Validator/Monitor files.
3. Utility scripts and skill docs
   - setup/sync/skills docs.
4. Optional legacy freeze policy
   - keep historical files unchanged but prepend “legacy naming” note.

