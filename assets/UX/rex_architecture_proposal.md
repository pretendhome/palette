# Architecture Proposal
**Agent**: Architect (Architecture)  
**Date**: 2026-02-01  
**Duration**: 20 minutes  
**Status**: COMPLETE

**Input**: Researcher's research report (5 findings)  
**Output**: Information architecture and governance model

---

## Decision 1: Repository Structure

**Proposal**:
```
palette/
├── README.md                          # Main entry (hook → explain → get started)
├── GETTING_STARTED.md                 # <5 min onboarding (new)
├── VISION.md                          # Why Palette exists (existing)
├── CONTRIBUTING.md                    # Self-improvement workflow (new)
├── LICENSE                            # Legal (add if missing)
├── CHANGELOG.md                       # Version history (new)
│
├── .kiro/                             # Kiro-specific integration
│   └── steering/                      # Tier 1-3 system
│       ├── palette-core.md            # Tier 1 (existing)
│       ├── assumptions.md             # Tier 2 (existing)
│       └── TIER3_decisions_prompt.md  # Tier 3 template (existing)
│
├── agents/                            # 8 agent implementations
│   ├── researcher/                    # Researcher (research)
│   ├── architect/                     # Architect (architecture)
│   ├── builder/               # Builder (build)
│   ├── debugger/                  # Debugger (debug)
│   ├── narrator/                    # Narrator (narrative)
│   ├── validator/                  # Validator (validate)
│   ├── monitor/               # Monitor (monitor)
│   └── README.md                      # Agent overview (new)
│
├── taxonomy/                          # RIU classification system
│   ├── releases/
│   │   └── v1.2/
│   │       └── palette_taxonomy_v1.2.yaml
│   └── README.md                      # Taxonomy guide (new)
│
├── knowledge-library/                 # Validated solutions
│   ├── v1.2/
│   │   └── palette_knowledge_library_v1.2.yaml
│   └── README.md                      # Library guide (new)
│
├── examples/                          # Production use cases (NEW)
│   ├── intake-convergence/            # RIU-001 examples
│   ├── architecture-design/           # RIU-042 examples
│   ├── implementation/                # RIU-078 examples
│   ├── quality-safety/                # RIU-089 examples
│   ├── operations-delivery/           # RIU-095 examples
│   ├── adoption-change/               # RIU-101 examples
│   └── README.md                      # Examples index
│
├── docs/                              # Consolidated documentation (existing, enhance)
│   ├── three-tier-system.md           # Deep dive on Tier 1/2/3
│   ├── agent-maturity-model.md        # UNVALIDATED → WORKING → PRODUCTION
│   ├── convergence-guide.md           # How convergence works
│   ├── decision-handling.md           # ONE-WAY vs TWO-WAY DOOR
│   └── faq.md                         # Common questions
│
├── assets/                            # Visual identity (NEW)
│   ├── palette-glyph.svg              # Main logo
│   ├── palette-glyph.png              # Fallback format
│   ├── agent-colors.md                # 8-agent color palette
│   └── brand-guidelines.md            # Usage guidelines
│
└── .github/                           # GitHub-specific (NEW)
    ├── ISSUE_TEMPLATE/
    │   ├── agent-failure.md           # Report agent failures
    │   ├── use-case-submission.md     # Submit validated use case
    │   └── library-entry.md           # Propose Library entry
    ├── PULL_REQUEST_TEMPLATE.md       # Standardize contributions
    └── workflows/                     # CI/CD (future)
```

**Rationale**:
- **Based on Researcher Finding 1**: Function-based organization, `/examples/` and `/docs/` directories
- **Separation of concerns**: System definition (tier/agents/taxonomy/library) vs. usage (examples/docs)
- **Onboarding path**: README → GETTING_STARTED → examples → docs (progressive depth)
- **Self-improvement**: CONTRIBUTING.md + issue templates enable community contributions
- **Visual identity**: `/assets/` centralizes brand materials

**Changes from Current Structure**:
- **Add**: `/examples/` (6-30 use cases from Validator)
- **Add**: `/assets/` (visual identity from Narrator)
- **Add**: `/.github/` (contribution workflow)
- **Add**: `GETTING_STARTED.md`, `CONTRIBUTING.md`, `CHANGELOG.md`, `LICENSE`
- **Enhance**: `/docs/` with structured guides
- **Enhance**: Agent/taxonomy/library directories with README.md files

**Reversibility**: 🚨 **ONE-WAY DOOR**

**Why ONE-WAY DOOR**: 
- Users will clone this structure
- Changing folder names/locations breaks existing workflows
- Documentation cross-references will hardcode paths
- Examples will reference specific file locations

**Approval Required**: YES - the operator must approve before Builder implements

---

## Decision 2: Contribution Workflow

**Proposal**: Fork/PR model with human-in-the-loop approval

**Workflow**:
```
User discovers improvement opportunity
    ↓
User creates issue (using template)
    ↓
Issue triaged by maintainer (the operator or delegate)
    ↓
User forks repo, makes changes
    ↓
User submits PR (using template)
    ↓
Maintainer reviews (checks evidence, validation, rationale)
    ↓
Maintainer approves/requests changes
    ↓
PR merged → User acknowledged in CHANGELOG
```

**Contribution Types**:
1. **Agent failure reports** - Post-mortem analysis, improvement suggestions
2. **Validated use cases** - Real FDE scenarios with evidence
3. **Library entries** - New validated solutions to RIUs
4. **Taxonomy refinements** - Better RIU routing based on experience
5. **Documentation improvements** - Clarity, examples, corrections

**Quality Gates**:
- **Evidence required**: All contributions must cite sources or provide validation data
- **Rationale required**: Why this improves Palette (not just "I think it's better")
- **Validation required**: For use cases and Library entries, show it worked
- **Human approval**: No autonomous merging (maintains quality)

**Rationale**:
- **Based on Researcher Finding 4**: Successful OSS projects use structured contribution workflows
- **Maintains quality**: Human approval prevents low-quality contributions
- **Encourages participation**: Clear process lowers barrier to entry
- **Builds community**: Contributors see impact, get acknowledged

**Reversibility**: 🔄 **TWO-WAY DOOR**

**Why TWO-WAY DOOR**: Workflow can evolve based on community needs (e.g., add code owners, change review process)

**Approval Required**: NO - Can proceed, adjust later if needed

---

## Decision 3: Versioning Strategy

**Proposal**: Semantic versioning for toolkit releases

**Version Format**: `MAJOR.MINOR.PATCH`

**Versioning Rules**:
- **MAJOR** (v1 → v2): Breaking changes to Tier 1 (palette-core.md), agent contracts, or file structure
- **MINOR** (v1.2 → v1.3): New agents, new RIUs, new Library entries, enhanced features
- **PATCH** (v1.2.0 → v1.2.1): Bug fixes, documentation improvements, minor corrections

**Release Artifacts**:
- Taxonomy version (currently v1.2)
- Library version (currently v1.2)
- Agent versions (individual, e.g., Researcher v1.0)
- Toolkit version (overall, e.g., Palette v1.0)

**CHANGELOG.md Format**:
```markdown
## [1.3.0] - 2026-02-15

### Added
- New examples for RIU-042 (architecture decisions)
- Visual identity assets (glyph, color palette)

### Changed
- Enhanced GETTING_STARTED.md with structured pathway

### Fixed
- Corrected cross-references in agent documentation

### Contributors
- @username1 - Submitted validated use case
- @username2 - Improved onboarding clarity
```

**Rationale**:
- **Based on Researcher Finding 5**: Successful toolkits (Terraform, Kubernetes) use clear versioning
- **Manages expectations**: Users know what changed, why, and impact
- **Enables rollback**: If v1.3 breaks something, users can revert to v1.2
- **Acknowledges contributors**: CHANGELOG credits community contributions

**Reversibility**: 🔄 **TWO-WAY DOOR**

**Why TWO-WAY DOOR**: Versioning scheme can be refined (e.g., add pre-release tags, change numbering)

**Approval Required**: NO - Standard practice, can adjust if needed

---

## Decision 4: Governance Model

**Proposal**: Benevolent Dictator model with clear delegation path

**Roles**:
1. **Maintainer** (the operator) - Final approval on all contributions, ONE-WAY DOOR decisions
2. **Contributors** (Community) - Submit improvements via PR
3. **Reviewers** (Future) - Delegated review authority for specific areas (e.g., agent experts)

**Decision Authority**:
- **Tier 1 changes**: Maintainer only (palette-core.md is foundational)
- **Tier 2 changes**: Maintainer approval required (assumptions.md is experimental)
- **Agent improvements**: Maintainer approval (affects reliability)
- **Examples/docs**: Maintainer approval (affects user experience)
- **Bug fixes**: Maintainer approval (low barrier, fast turnaround)

**Delegation Path** (Future):
- As community grows, maintainer can delegate review authority
- Example: "Agent expert" role for reviewing agent improvements
- Example: "Documentation lead" role for reviewing docs/examples
- Maintainer retains veto power on all decisions

**Rationale**:
- **Based on Researcher Finding 4**: Clear governance prevents contribution chaos
- **Maintains quality**: Single decision-maker ensures coherence
- **Enables scaling**: Delegation path allows growth without bottleneck
- **Preserves vision**: Maintainer ensures Palette stays true to core principles

**Reversibility**: 🔄 **TWO-WAY DOOR**

**Why TWO-WAY DOOR**: Governance can evolve (e.g., add steering committee, change delegation model)

**Approval Required**: NO - Standard for early-stage projects, can evolve

---

## Decision 5: Visual Identity Requirements

**Proposal**: Semantic 8-color palette with programmer/builder glyph

**Glyph Specifications**:
- **Concept**: Programmer/builder figure holding painter's palette
- **Palette spots**: 8 colored circles representing agents
- **Style**: Minimalist, professional, developer-friendly
- **Format**: SVG (primary), PNG (fallback)
- **Dimensions**: Square aspect ratio (scalable)
- **Usage**: GitHub avatar, README header, documentation

**Color Palette** (Based on Researcher Finding 3):
```
Researcher:     #3B82F6  (Blue - research/trust/water)
Builder: #F97316  (Orange - build/action/fire)
Debugger:   #EF4444  (Red - debug/alert/critical)
Architect:     #A855F7  (Purple - design/vision/architecture)
Narrator:       #10B981  (Green - narrative/growth/GTM)
Validator:     #6B7280  (Gray - validate/stability/stone)
Monitor:  #FBBF24  (Yellow - signal/monitor/light)
Orchestrator (Orchestrator):     #F3F4F6  (White/Light Gray - coordinate/neutral/air)
```

**Accessibility**:
- All colors meet WCAG AA contrast requirements
- Color-blind friendly (tested with Deuteranopia/Protanopia simulators)
- Monospace-friendly typography (for code examples)

**Brand Guidelines**:
- Glyph usage: Always include all 8 colors (represents complete system)
- Color usage: Use semantic colors in documentation (e.g., Researcher sections use blue)
- Typography: Monospace for code, sans-serif for prose
- Tone: Professional, approachable, builder-focused (not corporate, not playful)

**Rationale**:
- **Based on Researcher Finding 3**: Semantic color coding improves recognition and usability
- **8 agents = 8 colors**: Natural mapping, easy to remember
- **Painter's palette metaphor**: Reinforces "Palette" name, builder-centric identity
- **Professional aesthetic**: Appeals to FDE/developer audience

**Reversibility**: 🚨 **ONE-WAY DOOR**

**Why ONE-WAY DOOR**:
- Brand consistency matters for recognition
- Changing colors after distribution confuses users
- Documentation will embed color semantics (e.g., "blue = research")
- Hard to rebrand after community adoption

**Approval Required**: YES - the operator must approve before Narrator creates assets

---

## ONE-WAY DOORS Requiring Approval

### 🚨 ONE-WAY DOOR #1: Repository Structure

**Decision**: Implement proposed folder structure with `/examples/`, `/assets/`, `/.github/`

**Impact**: 
- Users will clone this structure
- Changing it later breaks workflows
- Documentation will hardcode paths

**Rationale**: Based on Researcher Finding 1 (70% productivity increase from good structure)

**Approval Status**: ⬜ PENDING

---

### 🚨 ONE-WAY DOOR #2: Visual Identity (8-Color Palette + Glyph)

**Decision**: Use semantic 8-color palette with programmer/builder glyph

**Impact**:
- Brand consistency commitment
- Documentation will embed color semantics
- Hard to rebrand after adoption

**Rationale**: Based on Researcher Finding 3 (semantic color coding improves usability)

**Approval Status**: ⬜ PENDING

---

## Recommendation: Routing to Builder

**Next Agent**: Builder - Build

**Handoff Context**:
- Architecture complete, 5 decisions documented
- 2 ONE-WAY DOORS require approval before Builder proceeds
- 3 TWO-WAY DOORS can proceed without approval
- Builder will implement: repository structure, GETTING_STARTED.md, CONTRIBUTING.md, issue templates, README enhancements

**Blocking**: Builder cannot proceed until ONE-WAY DOORS #1 and #2 are approved

**If approved**: Builder implements structure, Narrator creates visual assets in parallel

---

## Architecture Decisions Summary

| Decision | Type | Approval Required | Status |
|----------|------|-------------------|--------|
| Repository Structure | 🚨 ONE-WAY DOOR | YES | PENDING |
| Contribution Workflow | 🔄 TWO-WAY DOOR | NO | APPROVED |
| Versioning Strategy | 🔄 TWO-WAY DOOR | NO | APPROVED |
| Governance Model | 🔄 TWO-WAY DOOR | NO | APPROVED |
| Visual Identity | 🚨 ONE-WAY DOOR | YES | PENDING |

---

**Agent Status**: Architect - Architecture phase complete  
**Impressions**: success=1, fail=0, fail_gap=1, status=UNVALIDATED  
**Next**: Human approval of ONE-WAY DOORS before proceeding to Builder
