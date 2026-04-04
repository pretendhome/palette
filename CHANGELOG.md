# Palette Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [3.0.0] — 2026-04-04

### Added — Wiki Focal Point (Phases 1-3)

- **Wiki Compiler** (`scripts/compile_wiki.py`): Deterministic Python compiler reads 6 YAML data layers and generates 332 browsable markdown pages with provenance headers, cross-references, agent backlinks, and indexes. 8/8 validation checks pass.
- **Wiki Validator** (`scripts/validate_wiki.py`): 8-check validation suite — orientation test, coverage check, broken backlinks, orphan detection, adversarial test, deterministic rebuild, dual-experience test, source cross-check.
- **Governance Model v1** (`docs/WIKI_GOVERNANCE_MODEL_v1.md`): 527-line governance document. Three tiers (Obviously Right / Two-Way Door / One-Way Door). Unanimous consensus with veto escalation. Gradient descent resolution for disagreements. Trust-weighted voting. Precedent accumulation. 10 edge case scenarios. Sunset clause after 20 proposals.
- **Governance Pipeline**: `file_proposal.py`, `record_vote.py`, `promote_proposal.py`, `bridge_feedback_to_proposals.py` — full proposal lifecycle from filing through voting to promotion or rejection.
- **Voting Roster** (`wiki/proposed/VOTING_ROSTER.yaml`): Machine-readable canonical roster. 3 binding agents (WORKING), 2 advisory (UNVALIDATED).
- **Approval Queue** (`wiki/proposed/APPROVAL_QUEUE.md`): Auto-generated human-readable queue of pending proposals.
- **Workspace KL Governance**: Lighter W1/W2/W3 tiers for workspace-specific knowledge with promotion path to canonical KL.

### Changed

- **Knowledge Library**: 168 → 170 entries. LIB-178 (crack spread) and LIB-179 (hallucination detection) promoted through governance pipeline.
- **Sources**: 466 → 547. 25 broken URLs fixed (8 internal://, 17 file:// to dead paths).
- **Wiki pages**: 329 → 332. Path files now have frontmatter. Agent pages have source_file/hash and Protocol sections.
- **Compiler**: "Why It Matters" duplication fixed (90/168 → 0). Evidence links render local paths as inline code. URL scheme validation warns on internal/file URLs. Proposed entries compiled with PROPOSED banner. proposed/ directory preserved across recompiles.
- **Validator**: Source cross-check added (check #8). Governance artifacts excluded. Path frontmatter handled in dual-experience test.
- **Health checks**: Section 8 (Governance Pipeline) added to health_check.py. Section 13 added to total_health_check.py.
- **palette-core.md**: Added "The system is strongest when its partners are most different from each other, because complementary coverage creates the safety to be bold."

### Fixed

- 25 broken source URLs in knowledge library (old Myth-Fall-Game paths → current locations)
- 90/168 "Why It Matters" sections duplicating Definition opening
- 14 path files missing frontmatter
- 12 agent pages missing source_file field
- 6 thin KL entries enriched (LIB-076 through LIB-080, LIB-177)
- PROP-ID counter checking archive to prevent duplicates
- Compiler preserving proposed/ directory across recompiles
- validate_palette_state.py skipping ARCHIVED implementations
- Orchestrator guard in .kiro/steering/assumptions.md
- Stale counts across 11+ living documents (167→170 entries, 466→547 sources)

### Added — Governance Research & Design

- `docs/WIKI_FOCAL_POINT_PROPOSAL.md` — 17 iterations, 3 peer reviews
- `docs/WIKI_COMPILER_SPEC.md` — Page template, field specs, rendering rules
- `docs/WIKI_DESIGN_RATIONALE.md` — Design context
- `docs/WIKI_PHASE_2_SCOPE.md` — 5 iterations, 11 work items
- `docs/WIKI_PHASE_3_PLAN.md` — Implementation plan
- `docs/WIKI_PROPOSED_GOVERNANCE_RESEARCH.md` — 5 governance patterns researched
- `docs/WIKI_BRIDGE_REVIEW_KIRO.md` — Kiro's review of Claude's bridge design

---

## [Previous — Unreleased]

### Added

- **Voice Summary Engine** (`mission-canvas/openclaw_adapter_core.mjs`): `makeVoiceSummary()` generates conversational voice-friendly responses from structured route data. Translates routing → natural language with one-way door warnings, knowledge support counts, and alternative suggestions.

- **Resolver Service** (`mission-canvas/resolver_service.py`): LLM-based intent classification service that maps natural language input to grounded prompts with RIU routing, confidence scoring, and suggested agent assignment. Integrated into both server.mjs and joseph_bridge.py.

- **Market Stress Module** (`mission-canvas/market_stress.py`): CAPE + Buffett Indicator + P/S ratio composite crash probability model, callable from Joseph bridge via `/stress` command.

- **Known Marketing Workspace** (`mission-canvas/workspaces/known-marketing/`): Full workspace for dating app marketing strategy — config, knowledge library, voice brand playbook, wire contract spec. First external client workspace demonstrating the workspace engine.

- **Kiro Steering Files** (`mission-canvas/.kiro/steering/`): Product, structure, and tech steering documents for Mission Canvas, generated by Kiro autonomous agent.

- **LENS-MKT-002** (`lenses/releases/v0/LENS-MKT-002_known_dating_marketing.yaml`): Marketing lens for dating app domain, created for Known workspace.

- **Voxtral WebGPU Test Suite** (`mission-canvas/test_voxtral_integration.mjs`): Verification tests for Voxtral WebGPU speech-to-text integration — fallback mechanism, endpoint compatibility, priority order, browser capability detection.

- **Lenses (Optional Context Overlays)** (`palette/lenses/`): Three pilot lenses that shape output framing without overriding agent routing or ONE-WAY DOOR gates. LENS-PM-001 (product decisions), LENS-ENG-001 (engineering execution), LENS-DEV-001 (developer delivery). All v0.1/pilot with built-in kill criteria after 20 evaluation runs. Integration plan at `palette/lenses/INTEGRATION_PLAN.md`.

### Changed

- **Joseph Bridge** (`mission-canvas/joseph_bridge.py`): Added `/stress` command, resolver intent classification integration, expanded monitor patterns, and improved research routing logic.

- **Server.mjs** (`mission-canvas/server.mjs`): Integrated resolver service for LLM-based intent classification before local routing. Added `callResolver()` with 15s timeout and graceful fallback.

- **Index.html** (`mission-canvas/index.html`): Voxtral WebGPU speech-to-text integration with intelligent fallback system (Voxtral → native SpeechRecognition → server Whisper).

- **Workspace Coaching** (`mission-canvas/workspace_coaching.mjs`): Enhanced coaching signals and workspace integration improvements.

---

## [2.0.0] - 2026-03-16

### Summary
**v2.0 (SDK Hardening + Dual Enablement)**: Completes the machine enablement half of the Dual Enablement loop. The SDK — which provides any agent instant access to Palette's full intelligence system — gains production-grade error handling, a 58-test suite, and a system-wide health agent. V2 graduation: the SDK is verified, tested, and ready for agent adoption.

### Added

- **SDK Test Suite** (`sdk/tests/`): 58 unit and integration tests covering all 3 SDK modules (agent_base, integrity_gate, graph_query). Tests cover: PaletteContext loading (healthy + degraded), HandoffPacket/HandoffResult serialization round-trips, IntegrityGate validation (RIU/LIB/service references, assumption detection, gap enforcement), GraphQuery SPO queries, stdin/stdout agent protocol, self_check() health status, and full integration with real PIS data.

- **Health Agent** (`agents/health/`): 6-section system integrity checklist (58 checks) covering layer integrity, agent health, enablement sync, cleanliness, data quality, and governance. Ends every run with a structured reflection prompt for continuous improvement. Runnable as `python3 agents/health/health_check.py`.

- **Business Plan Creation agent.json** (`agents/business-plan-creation/agent.json`): Added missing agent manifest for the multi-agent business plan workflow (validated on Rossi project, 82/100 quality score).

### Changed

- **SDK Error Handling**: `PaletteContext.load()` now catches exceptions and returns a degraded context (pis_data=None) with error logged to stderr, instead of crashing. Agents can check `self_check()` and decide whether to proceed or halt.

- **GraphQuery.from_yaml() Visibility**: Failed YAML loads now log to stderr with the specific error, instead of returning None silently.

- **IntegrityGate Defensive Guards**: All 4 check methods now guard against None data and None results. Passing None PIS data returns an explicit warning instead of crashing with AttributeError.

- **Health Check Accuracy**: Fixed knowledge library entry counting (was matching sub-entries inside YAML string literals). Fixed taxonomy counting key. Added word-boundary matching for personal name detection to eliminate false positives (e.g., "reliability" no longer matches a substring of a personal name). Self-matching patterns constructed dynamically.

- **Health Check Scope**: Operational code scan now excludes content/documentation directories (docs, research, assets, knowledge-library, taxonomy, lenses, bridges, buy-vs-build) where names and paths are legitimate. Hardcoded path check excludes bridges (VPS deployment).

### Fixed

- **Hardcoded paths in operational code**: Replaced absolute `/home/*/fde/palette/` paths with portable relative paths or `PALETTE_ROOT` environment variable lookups in `agents/researcher/researcher.md`, `agents/debugger/README.md`, `agents/business-plan-creation/QUICK_START.md`, `scripts/comprehensive_palette_audit.py`, `scripts/lens_eval_runner.py`.

### Metrics

- Health check: 51/62 → 57/58 passing (1 pre-existing data quality warning: terminology drift in service naming)
- SDK tests: 0 → 58 passing
- Coordination tests: 21/21 (no regression)
- Integrity checks: 8/8 (no regression)
- Regression SLOs: all passing (no regression)

---

## [2.0.0] - 2026-02-18

### Summary
**v2.0 (Agentic Runtime)**: Palette crosses from a markdown governance framework into a live, executable multi-agent system. First agents with real binaries, first phone interface, first self-improving eval loop.

### Added

- **Resolver — Intent Resolver**: New agent (`agents/resolver/`) that acts as the front door of Palette. Maps raw user input to 111 RIUs via two-phase resolution (cluster classification → RIU matching). Single-question disambiguation, stateless per invocation, multi-turn state via HandoffPacket payload. Named for the hollow-crested hadrosaur evolved for two-way communication.

- **Orchestrator binary (Orchestrator)**: Promoted from design-only placeholder to a running Go binary (`agents/orchestrator/orch`). Full agent roster management, capability-scored routing, keyword-rule routing table, Resolver fallback for ambiguous inputs. Commands: `orch status`, `orch route`, `orch run`.

- **Researcher v2.0**: Complete rewrite of the research agent. HandoffPacket stdin → HandoffResult stdout protocol. Real API calls to Perplexity, Tavily, Exa with Claude synthesis layer. Query classification (factual/synthesis/academic/current_events). `_parse_json()` helper for Claude markdown-wrapped JSON responses. `decision_context` gate.

- **Telegram Bridge** (`bridges/telegram/`): Live phone interface to Palette via `@palette_ai_bot`. Long-polling bot with per-chat state, text and voice input (OpenAI Whisper transcription). Interview simulation modes: Josh Rutberg (VP Customer Outcomes, Bain background) and Avril (AI Outcomes Specialist, Singapore). Commands: `/interview josh`, `/interview avril`, `/feedback`, `/reset`.

- **MissionCanvas Eval Loop** (`/home/mical/fde/product/`): 100-payload evaluation suite with 6 scored dimensions (convergence, routing, actionability, safety, uncertainty, expansion). Hard pass threshold 24/30. Auto-prune (FIFO + TTL), PM decision note generation, status board, triage queue.

- **Auto-Recursive Feedback Agent** (`product/eval/generate_feedback_v1.mjs`): Claude-powered analysis agent that reads failure clusters, diagnoses root causes, and proposes specific fixes. `--auto-apply` flag patches `openclaw_adapter_core.mjs` directly. Wired into `run_cycle_v1.sh` as step 4. Skips cleanly on 100% pass rate.

- **MissionCanvas OWD Detection** (`missioncanvas-site/openclaw_adapter_core.mjs`): Expanded `OWD_TERMS` from 6 technical terms to 16 terms covering business-level irreversibility (vendor lock-in, decommissioning, multi-year contracts, removing human oversight). OWD recall improved from 20% → 100%.

### Fixed

- **Duplicate LIB IDs**: Renumbered 9 duplicate entries (LIB-089 through LIB-097) in `knowledge-library/v1.2/palette_knowledge_library_v1.2.yaml` to LIB-101 through LIB-109. All entries preserved, IDs now unique. Integrity validator passes clean.

- **server.mjs null response bug**: When `OPENCLAW_BASE_URL` is empty, `proxyToOpenClaw()` returns `null` instead of throwing, causing the server to send literal `"null"` as the response body. Fixed with null-coalescing fallback to `localRouteResponse()` in both the route handler and the stream handler.

- **`_parse_json()` robustness**: Added to both Resolver and Researcher to handle Claude returning markdown-wrapped JSON (both leading backtick and trailing text variants).

- **`datetime.utcnow()` deprecation**: Updated to `datetime.datetime.now(datetime.timezone.utc)` in Researcher and Resolver.

- **ANTHROPIC_API_KEY environment loading**: Documented and fixed `.bash_profile` vs `.bashrc` issue for non-interactive shell subprocesses.

### Infrastructure

- **pm2 process management**: MissionCanvas server now runs under pm2 (`pm2 start`), auto-restarts on crash, persists across sessions. `pm2 save` configured.

- **`agent.json` constraints typing**: Fixed `constraints` field to `map[string]bool` (numeric values caused silent Orchestrator roster exclusion).

- **Orchestrator routing rules**: Added `intent/clarify` rule (conversational inputs → Resolver) and Resolver fallback in `routeByCapability` when no candidates match.

- **`core/packet.go`**: Added `AgentResolver AgentID = "resolver"` constant.

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
- **Business Plan Composite Agent**: Multi-agent workflow (Researcher → Architect → Narrator → Validator) validated on Rossi project
- **Impression Sync Script**: `scripts/sync-impressions.py` aggregates agent performance from project logs
- **Git Hook Automation**: Post-commit hook auto-syncs impressions and pushes to GitHub
- **Windows Quick Start Guide**: Platform-agnostic setup instructions addressing Windows confusion
- **Agent Maturity Tracking**: Live status in `agents/README.md` with impression counts
- **Operational learnings integration**: Continued v1.3 hardening toward a reproducible framework handoff model per implementation

### Changed
- **Narrator promoted to WORKING tier**: First agent to reach Tier 2 (10 consecutive successes on rossi-mission)
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
  - Expanded Validator role: multi-layered evaluation, LM-as-Judge
  - LIB-093: Agent Quality Evaluation Methods
  - Artifact-focused validation (JSON rubrics, not opinions)

### Changed
- Tier 2 section numbering (Agent Communication Protocol now Section 7)
- Validator description (added validation methods)
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
- 7 agent implementations (Researcher, Architect, Builder, Debugger, Narrator, Validator, Monitor)
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
- Project maintainer

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
