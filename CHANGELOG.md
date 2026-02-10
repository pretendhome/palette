# Palette Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

---

## [1.3.1] - 2026-02-10

### Added
- **Company-RIU Mapping Library v1.0**: 127 funded AI companies mapped to Palette RIUs across 12 use cases
- **Business Plan Composite Agent**: Multi-agent workflow (Argy → Rex → Yuty → Anky) validated on Rossi project
- **Impression Sync Script**: `scripts/sync-impressions.py` aggregates agent performance from project logs
- **Git Hook Automation**: Post-commit hook auto-syncs impressions and pushes to GitHub
- **Windows Quick Start Guide**: Platform-agnostic setup instructions addressing Windows confusion
- **Agent Maturity Tracking**: Live status in `agents/README.md` with impression counts

### Changed
- **Yutyrannus promoted to WORKING tier**: First agent to reach Tier 2 (10 consecutive successes on rossi-mission)
- **Updated palette.zip**: Now 462KB, includes v1.3.1 features, Windows-friendly with clear setup guide
- **Agents README**: Shows real-time impression counts, maturity status, and projects contributing

### Fixed
- **Platform confusion**: Clarified Palette is markdown files (works on Windows/macOS/Linux, no installation)
- **Impression rollup**: Projects now automatically sync to global agent maturity on commit

---

## [1.3.0] - 2026-02-05

### Added
- **Security formalization** (Tier 2 Section 6)
  - Agent identity, least privilege, guardrails, policy enforcement
  - RIU-105: Agent Security & Access Control
  - LIB-089: Least Privilege for Agents
  - LIB-090: Guardrails & Policy Enforcement
  - LIB-091: Agent Identity & Authentication

- **Decision classification** (Library)
  - LIB-092: Decision Classification Framework
  - Formalizes ONE-WAY DOOR / TWO-WAY DOOR as reusable pattern

- **Validation methods** (Tier 2 + Library)
  - Expanded Anky role: multi-layered evaluation, LM-as-Judge
  - LIB-093: Agent Quality Evaluation Methods
  - Artifact-focused validation (JSON rubrics, not opinions)

### Changed
- Tier 2 section numbering (Agent Communication Protocol now Section 7)
- Ankylosaurus description (added validation methods)
- Taxonomy: 104 → 105 RIUs
- Library: 76 → 81 questions

### Rationale
- Addresses enterprise security requirements (Google "Intro to Agents" research)
- Elevates decision classification as Palette's unique differentiator
- Strengthens maturity model with concrete evaluation methods
- Maintains Tier 1 immutability (security in Tier 2, not Tier 1)

---

## [1.0.0] - 2026-01-31

### Added
- Initial release of Palette toolkit
- Three-tier system (Tier 1: palette-core.md, Tier 2: assumptions.md, Tier 3: decisions template)
- 7 agent implementations (Argy, Rex, Theri, Raptor, Yuty, Anky, Para)
- Taxonomy v1.2 (104 RIUs)
- Knowledge Library v1.2 (86 questions)
- Interactive onboarding (type "start")
- Demo guide with live agent switching
- Shareable ZIP package (298 KB)

### Status
- All agents at v1.0 UNVALIDATED (0 impressions)
- Ready for first real executions

---

## Version History

- **v1.0.0** (2026-01-31): Initial release
- **v1.2** (Taxonomy/Library): Current artifact versions

---

## Contributors

Thank you to everyone who has contributed to Palette!

### Maintainer
- Mical - Creator and maintainer

### Contributors
(Contributors will be listed here as they submit validated improvements)

---

## How to Contribute

See `CONTRIBUTING.md` for guidelines on submitting:
- Agent failure reports
- Validated use cases
- Library entries
- Taxonomy refinements
- Documentation improvements
