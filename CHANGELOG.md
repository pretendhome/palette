# Palette Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- **Lenses (Optional Context Overlays)** (`palette/lenses/`): Three pilot lenses that shape output framing without overriding agent routing or ONE-WAY DOOR gates. LENS-PM-001 (product decisions), LENS-ENG-001 (engineering execution), LENS-DEV-001 (developer delivery). All v0.1/pilot with built-in kill criteria after 20 evaluation runs. Integration plan at `palette/lenses/INTEGRATION_PLAN.md`.

---

## [2.0.0] - 2026-02-18

### Summary
**v2.0 (Agentic Runtime)**: Palette crosses from a markdown governance framework into a live, executable multi-agent system. First agents with real binaries, first phone interface, first self-improving eval loop.

### Added

- **Corythosaurus (Cory) — Intent Resolver**: New agent (`agents/corythosaurus/`) that acts as the front door of Palette. Maps raw user input to 111 RIUs via two-phase resolution (cluster classification → RIU matching). Single-question disambiguation, stateless per invocation, multi-turn state via HandoffPacket payload. Named for the hollow-crested hadrosaur evolved for two-way communication.

- **Orchestrator binary (Orch)**: Promoted from design-only placeholder to a running Go binary (`agents/orchestrator/orch`). Full agent roster management, capability-scored routing, keyword-rule routing table, Cory fallback for ambiguous inputs. Commands: `orch status`, `orch route`, `orch run`.

- **Argentavis (Argy) v2.0**: Complete rewrite of the research agent. HandoffPacket stdin → HandoffResult stdout protocol. Real API calls to Perplexity, Tavily, Exa with Claude synthesis layer. Query classification (factual/synthesis/academic/current_events). `_parse_json()` helper for Claude markdown-wrapped JSON responses. `decision_context` gate.

- **Telegram Bridge** (`bridges/telegram/`): Live phone interface to Palette via `@palette_ai_bot`. Long-polling bot with per-chat state, text and voice input (OpenAI Whisper transcription). Interview simulation modes: Josh Rutberg (VP Customer Outcomes, Bain background) and Avril (AI Outcomes Specialist, Singapore). Commands: `/interview josh`, `/interview avril`, `/feedback`, `/reset`.

- **MissionCanvas Eval Loop** (`/home/mical/fde/product/`): 100-payload evaluation suite with 6 scored dimensions (convergence, routing, actionability, safety, uncertainty, expansion). Hard pass threshold 24/30. Auto-prune (FIFO + TTL), PM decision note generation, status board, triage queue.

- **Auto-Recursive Feedback Agent** (`product/eval/generate_feedback_v1.mjs`): Claude-powered analysis agent that reads failure clusters, diagnoses root causes, and proposes specific fixes. `--auto-apply` flag patches `openclaw_adapter_core.mjs` directly. Wired into `run_cycle_v1.sh` as step 4. Skips cleanly on 100% pass rate.

- **MissionCanvas OWD Detection** (`missioncanvas-site/openclaw_adapter_core.mjs`): Expanded `OWD_TERMS` from 6 technical terms to 16 terms covering business-level irreversibility (vendor lock-in, decommissioning, multi-year contracts, removing human oversight). OWD recall improved from 20% → 100%.

### Fixed

- **Duplicate LIB IDs**: Renumbered 9 duplicate entries (LIB-089 through LIB-097) in `knowledge-library/v1.2/palette_knowledge_library_v1.2.yaml` to LIB-101 through LIB-109. All entries preserved, IDs now unique. Integrity validator passes clean.

- **server.mjs null response bug**: When `OPENCLAW_BASE_URL` is empty, `proxyToOpenClaw()` returns `null` instead of throwing, causing the server to send literal `"null"` as the response body. Fixed with null-coalescing fallback to `localRouteResponse()` in both the route handler and the stream handler.

- **`_parse_json()` robustness**: Added to both Cory and Argy to handle Claude returning markdown-wrapped JSON (both leading backtick and trailing text variants).

- **`datetime.utcnow()` deprecation**: Updated to `datetime.datetime.now(datetime.timezone.utc)` in Argy and Cory.

- **ANTHROPIC_API_KEY environment loading**: Documented and fixed `.bash_profile` vs `.bashrc` issue for non-interactive shell subprocesses.

### Infrastructure

- **pm2 process management**: MissionCanvas server now runs under pm2 (`pm2 start`), auto-restarts on crash, persists across sessions. `pm2 save` configured.

- **`agent.json` constraints typing**: Fixed `constraints` field to `map[string]bool` (numeric values caused silent Orch roster exclusion).

- **Orch routing rules**: Added `intent/clarify` rule (conversational inputs → Cory) and Cory fallback in `routeByCapability` when no candidates match.

- **`core/packet.go`**: Added `AgentCory AgentID = "corythosaurus"` constant.

---

## Framework Milestones

- **v1.0 (Foundation)**: Initial three-tier system only (Tier 1/2/3 governance backbone).
- **v1.1 (Mythfall Precedent)**: First implementation precedent for convergence briefing + multi-agent workflow in one engagement.
- **v1.2 (Rossi External Precedent)**: First real external customer implementation with artifact-heavy business-plan workflow and alignment-first execution.
- **v1.3 (Professionalization + OpenClaw Learnings)**: Structural hardening, governance refinements, and system mechanism improvements informed by comparative analysis.

---

## [1.3.1] - 2026-02-10

### Added
- **Company-RIU Mapping Library v1.0**: 127 funded AI companies mapped to Palette RIUs across 12 use cases
- **Business Plan Composite Agent**: Multi-agent workflow (Argy → Rex → Yuty → Anky) validated on Rossi project
- **Impression Sync Script**: `scripts/sync-impressions.py` aggregates agent performance from project logs
- **Git Hook Automation**: Post-commit hook auto-syncs impressions and pushes to GitHub
- **Windows Quick Start Guide**: Platform-agnostic setup instructions addressing Windows confusion
- **Agent Maturity Tracking**: Live status in `agents/README.md` with impression counts
- **Operational learnings integration**: Continued v1.3 hardening toward a reproducible framework handoff model per implementation

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

- **v1.0**: Foundation (three tiers only)
- **v1.1**: Mythfall precedent (convergence + multi-agent workflow)
- **v1.2**: Rossi precedent (external environment, alignment-first artifact workflow)
- **v1.3**: OpenClaw-informed structural/professionalization phase
- **v1.3.1** (2026-02-10): Incremental additions and tooling updates

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
