# Palette Project Structure Standard

**Version**: 1.0  
**Status**: Canonical  
**Last Updated**: 2026-02-07

---

## Core Principle

**Palette is the toolkit. Projects use the toolkit.**

- Palette: `/home/mical/fde/palette/` (versioned, canonical, toolkit development)
- Projects: `/home/mical/fde/projects/<client-name>/` (project execution)
- Learnings flow: Projects → Palette (promote patterns that work)

---

## Standard Project Structure

```
/home/mical/fde/projects/<client-name>/
├── .kiro/steering/              # Project-specific steering (required)
│   ├── product.md               # Product purpose, users, goals
│   ├── tech.md                  # Tech stack, frameworks, constraints
│   └── structure.md             # File organization, naming conventions
│
├── decisions.md                 # Project decision log (Tier 3)
├── README.md                    # Project overview
│
├── artifacts/                   # Agent outputs by phase (required)
│   ├── research/                # Argy outputs
│   ├── architecture/            # Rex outputs
│   ├── implementation/          # Theri outputs
│   ├── validation/              # Anky outputs
│   ├── narrative/               # Yuty outputs
│   └── monitoring/              # Para outputs
│
└── [project-specific]           # Project code/docs
    ├── src/
    ├── docs/
    └── ...
```

---

## Agent Output Organization

| Agent | Directory | Purpose |
|-------|-----------|---------|
| Argy (Argentavis) | `artifacts/research/` | Market research, competitive analysis, context gathering |
| Rex (Tyrannosaurus) | `artifacts/architecture/` | System design, architecture proposals, tradeoff analysis |
| Theri (Therizinosaurus) | `artifacts/implementation/` | Code, configs, build artifacts |
| Raptor (Velociraptor) | `artifacts/implementation/` | Debug reports, root cause analysis |
| Anky (Ankylosaurus) | `artifacts/validation/` | Quality reports, compliance checks, validation |
| Yuty (Yutyrannus) | `artifacts/narrative/` | Demos, docs, customer communication |
| Para (Parasaurolophus) | `artifacts/monitoring/` | Monitoring configs, alerts, health checks |

---

## Learning Flow

**Projects → Palette**:
1. Agent succeeds consistently → Promote maturity tier
2. New pattern discovered → Add to knowledge library
3. New problem type → Add RIU to taxonomy
4. Steering pattern works → Document in examples

**Palette → Projects**:
1. Reference taxonomy for problem classification
2. Use Palette agents for execution
3. Follow decision framework (ONE-WAY vs TWO-WAY DOOR)
4. Inherit convergence principles

---

## Implementation Status

**Rossi Mission**: ✓ Standardized (local only, no remote configured)  
**Myth Fall Game**: ✓ Standardized and pushed to GitHub

---

## Version History

- **v1.0** (2026-02-07): Initial standard, applied to rossi-mission and myth-fall-game
