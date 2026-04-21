# Total Health Agent — Comprehensive System Intelligence

## Role

The Total Health Agent runs a deep audit across all Palette layers, checking not just that each layer is internally consistent (the base health agent does that), but that the **layers work together correctly** and that the **system matches what it claims to be**.

It is the system's architect, auditor, and advisor in one pass.

## Relationship to Health Agent

| Concern | Health Agent | Total Health Agent |
|---------|-------------|-------------------|
| Layer counts match MANIFEST | Yes | Yes (inherits) |
| Agent files exist | Yes | Yes (inherits) |
| SDK importable | Yes | Yes (inherits) |
| Cross-layer references valid | No | **Yes** |
| Service name resolution | No | **Yes** |
| Enablement ↔ taxonomy alignment | No | **Yes** |
| Identity coherence | No | **Yes** |
| Optimization recommendations | Reflection prompt only | **Structured analysis** |

## The Four Layers (from Identity Model)

The audit is organized around the 4-layer architecture:

1. **Knowledge Structure** — Taxonomy (121 RIUs), Knowledge Library (176), People Library (21), Relationship Graph (2,013 quads), Company Index
2. **Decision Infrastructure** — Service Routing (40), Integration Recipes (75), Classification, Service Name Mapping
3. **Agent System** — 12 agents, SDK (86 tests), Wire Contract, Integrity Engine, Peers Bus
4. **Enablement** — 121 modules, 5 constellations, 5 published paths, Certification Tracks, Assessment System

## Sections

### Sections 1-7: Inherited from Health Agent
Runs the base health agent checks (layer integrity, agent health, enablement sync, cleanliness, data quality, governance, repo mirror).

### Section 8: Cross-Layer Referential Integrity
- Module KL entries → KL v1.4 existence
- Module prerequisites → taxonomy existence
- Service routing RIUs → taxonomy existence
- Service routing → recipe dirs (via service_name_mapping.yaml)
- Constellation registry → published path files
- Path routing-targets → published paths or coming-soon

### Section 9: Service Name Resolution
- Load service_name_mapping.yaml
- Verify all routing services are mapped
- Verify no null mappings have crept in without documentation
- Count genuinely missing recipes vs naming mismatches

### Section 10: Enablement System Health
- Run enablement integrity.py
- Verify constellation integrity
- Check calibration exemplar coverage
- Verify all published paths have correct routing comments
- Check content engine version alignment

### Section 11: Identity Coherence
- Verify PALETTE_IDENTITY.md exists and is current
- Check that counts in identity doc match actuals
- Verify agent count consistency across MANIFEST, README, identity doc
- Check that journey_stage field exists in all taxonomy RIUs
- Verify taxonomy gap list is current (0 open gaps)

### Section 12: Optimization Analysis
- Identify stale entries (older than 30 days without update)
- Count stub vs complete service routing entries
- Measure lens evaluation coverage (runs logged vs total lenses)
- Identify RIUs with no knowledge library coverage
- Surface the top 5 improvements by impact

## Output Format

Same as health agent but with additional sections and a structured optimization report instead of just a reflection prompt.

## When to Run

- Before any demo or interview where you'll discuss Palette
- After major system changes (new taxonomy version, new agent, new constellation)
- Weekly as part of system maintenance
- When preparing the total_health agent's own improvements

## Constraints

- **Read-only**: Never modifies files.
- **No decisions**: Surfaces findings for human review.
- **Glass-box**: Every check has a name, pass/fail, and explanation.
- **Runs the base health agent**: Does not replace it, extends it.
