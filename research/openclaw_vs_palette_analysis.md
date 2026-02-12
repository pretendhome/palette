# OpenClaw vs Palette — Deep Comparison & Learnings

**Date**: 2026-02-12
**Purpose**: Identify what Palette can learn from OpenClaw's architecture, patterns, and design philosophy. No changes yet — research only.
**Source**: https://github.com/openclaw/openclaw (188k+ stars, MIT licensed)

---

## 1. WHAT OPENCLAW IS

OpenClaw is a **local-first personal AI assistant** that runs as a self-hosted Gateway (WebSocket control plane) connecting to messaging platforms (WhatsApp, Telegram, Slack, Discord, iMessage, etc.) while maintaining privacy and control.

- **188k+ GitHub stars** — one of the most popular open-source AI agent projects
- TypeScript monorepo, Node 22+, pnpm workspaces
- Supports Claude (recommended), OpenAI, local models via LiteLLM
- Multi-platform: macOS app, iOS/Android nodes, Linux/Windows CLI
- Voice-capable (ElevenLabs TTS, always-on wake word)
- Browser control via CDP (Chrome DevTools Protocol)

**Core philosophy**: One agent per person, running locally, always available across every messaging channel.

---

## 2. WHAT PALETTE IS (for comparison context)

Palette is a **three-tier decision framework for human-AI collaboration** designed around convergence-first execution, empirical agent trust, and glass-box reasoning.

- Internal toolkit (not public), 2.5 years development from AWS Solutions Engineering
- 8 cognitive agent archetypes with bounded responsibilities
- 115 RIUs (Reusable Implementation Units) as a routing taxonomy
- 99 knowledge library entries as validated Q&A
- Impressions system for agent maturity (UNVALIDATED → WORKING → PRODUCTION)
- Decision classification (ONE-WAY DOOR / TWO-WAY DOOR)

**Core philosophy**: Agents must earn trust empirically. Convergence before execution. Every decision is traceable.

---

## 3. ARCHITECTURAL COMPARISON

| Dimension | OpenClaw | Palette |
|-----------|----------|---------|
| **Primary purpose** | Personal AI assistant (always-on, multi-channel) | Decision framework for complex AI engagements |
| **Architecture** | Gateway + Agent Runtime + Channels + Nodes | 3-tier prompt architecture + agent archetypes |
| **Execution model** | Single agent loop with tool use | Multi-agent handoffs with quality gates |
| **Agent identity** | One "brain" per agent (workspace + state + sessions) | Cognitive archetypes with bounded permissions |
| **Multi-agent** | Routing by channel/sender to isolated agents | Sequential handoffs between specialized archetypes |
| **Memory** | File-based (daily logs + MEMORY.md) + vector search | Stateless across sessions; decisions.md for persistence |
| **Context mgmt** | Compaction (auto-summarize) + session pruning | Manual; relies on artifact documentation |
| **Trust model** | Sandbox + tool policies + elevated mode | Impressions system (empirical trust earned over time) |
| **Orchestration** | Lobster DSL (typed pipelines with approval gates) | Manual phase gates with ONE-WAY DOOR classification |
| **Skills/Tools** | SKILL.md files, hot-reloadable, ClawHub registry | RIUs (inert execution materials, no runtime) |
| **Channels** | 12+ messaging platforms, voice, browser, canvas | Human-in-the-loop via conversation |
| **Deployment** | npm install, Docker, Nix, VPS | Prompt files loaded into AI session |
| **Eval/Quality** | No formal evaluation framework visible | Anky validator, fixtures, LM-as-Judge rubrics |
| **State** | JSONL session files, SQLite memory index | Append-only decisions.md |

---

## 4. KEY DIFFERENCES (Philosophy)

### 4.1 Autonomy-First vs Convergence-First

**OpenClaw**: Agents act autonomously by default. Safety comes from sandboxing and tool policies (mechanical constraints). The agent decides when to act and when to ask.

**Palette**: Agents cannot act until convergence is established. Safety comes from decision classification and empirical trust (behavioral constraints). The human decides when the agent may act.

**Learning**: These are complementary, not competing. Palette's convergence-first approach is correct for *high-stakes decisions*. OpenClaw's autonomy-first is correct for *routine operations*. Palette could benefit from defining a "routine operations" tier where agents with PRODUCTION status can act autonomously on TWO-WAY DOOR decisions.

### 4.2 Runtime vs Framework

**OpenClaw**: A running system — Gateway process, WebSocket connections, persistent sessions, real tool execution.

**Palette**: A cognitive framework — prompt files, decision patterns, quality gates. No runtime. Agents are "loaded" into whatever AI system is being used.

**Learning**: Palette's lack of runtime is both its strength (platform-agnostic) and its weakness (no persistent state, no automation, no scheduled tasks). OpenClaw demonstrates what a runtime layer adds: memory persistence, session management, scheduled automation, multi-channel access.

### 4.3 Single-Agent-Per-Person vs Multi-Agent-Per-Task

**OpenClaw**: One agent "brain" per person, with sub-agents for parallel background work. The agent is a generalist that uses skills/tools to specialize.

**Palette**: Multiple specialist agents per engagement. Argy researches, Rex architects, Theri builds, Anky validates. Each has bounded permissions and disallowed actions.

**Learning**: OpenClaw's model scales to personal use. Palette's model scales to enterprise engagements. But OpenClaw's sub-agent pattern (spawn background workers with restricted tools) is directly applicable to how Palette could implement the Orchestrator archetype.

---

## 5. SPECIFIC LEARNINGS FOR PALETTE

### 5.1 Memory Architecture (HIGH PRIORITY)

**What OpenClaw does**:
- `MEMORY.md` — curated long-term facts, preferences, decisions
- `memory/YYYY-MM-DD.md` — daily append-only operational log
- Vector search over all memory files (semantic + BM25 hybrid retrieval)
- Auto-flush before context compaction (saves durable notes before summarizing)
- Memory loaded into system prompt at session start

**What Palette does**:
- `decisions.md` — append-only decision log (ONE-WAY/TWO-WAY doors)
- Stateless across sessions — "if it matters, document it explicitly"
- No search, no indexing, no automatic memory

**Gap**: Palette's statelessness is principled (avoids stale context) but costly (restartability requires re-reading all artifacts). OpenClaw's two-tier memory (daily log + curated long-term) is a practical middle ground.

**Recommendation**:
- Add a `MEMORY.md` pattern to Palette engagements — curated facts that survive sessions
- Add daily logs per engagement (not per agent) — operational context
- Consider vector indexing over engagement artifacts for faster restartability
- Keep decisions.md as the authoritative decision record (Palette's strength)

### 5.2 Context Compaction (HIGH PRIORITY)

**What OpenClaw does**:
- Auto-compaction when approaching context window limits
- Summarizes older messages, preserves recent ones
- Summary persists in JSONL session history
- Manual `/compact` with optional focus instructions
- Separate from "pruning" (in-memory trimming of old tool results)

**What Palette does**:
- Nothing. When context fills up, the engagement effectively restarts.
- Restartability depends on artifact quality, not context management.

**Gap**: Palette's complex multi-phase engagements (like the MQ x Tie One drop package or the GAP AI strategy) routinely hit context limits. The current workaround is "start a new session, re-read artifacts."

**Recommendation**:
- Define a compaction protocol for Palette engagements: what to summarize, what to preserve, what to write to artifacts before compaction
- Add a "COMPACT" step to Yuty's responsibilities — Yuty already does narrative coherence
- Document the pattern in an RIU (e.g., "Context Compaction for Long Engagements")

### 5.3 Lobster-Style Workflow DSL (MEDIUM PRIORITY)

**What OpenClaw does**:
- Lobster: typed workflow runtime with YAML-defined pipelines
- Steps chain via stdin/stdout (JSON pipes)
- Approval gates as first-class citizens (`approval: required`)
- Resumable state via `resumeToken`
- Deterministic, auditable, replayable

**What Palette does**:
- Manual phase gates documented in decisions.md
- ONE-WAY DOOR decisions require human confirmation (conceptually similar to approval gates)
- No formal workflow definition language
- Multi-agent sequences are described in prose (e.g., "Argy → Rex → Theri → Yuty → Anky")

**Gap**: Palette's workflows are implicit — they exist in the operator's head and in prose descriptions. Lobster shows that making workflows explicit as data enables determinism, auditability, and resumability.

**Recommendation**:
- Define a lightweight workflow format for Palette composite agents (YAML)
- Include: phases, agent assignments, quality gates, ONE-WAY DOOR checkpoints, artifact dependencies
- This would make the Business Plan Creation agent and the MQ Drop Package agent reproducible without re-describing the workflow each time
- Could become RIU-607: "Workflow Definition for Multi-Agent Engagements"

### 5.4 Skills System (MEDIUM PRIORITY)

**What OpenClaw does**:
- Skills are directories with a `SKILL.md` file (YAML frontmatter + instructions)
- Three tiers: bundled, managed (shared), workspace (per-agent)
- Hot-reloadable, gated by OS/binary/env requirements
- ClawHub registry for community sharing
- Skills teach agents HOW to use tools, not what tools are

**What Palette does**:
- RIUs define WHAT to do (problem → execution pattern → artifacts)
- Knowledge library entries define HOW to answer questions
- Agent archetypes define WHO does what
- No equivalent of "loadable skill packs" that modify agent behavior at runtime

**Gap**: Palette's RIUs are taxonomic (routing) while OpenClaw's skills are behavioral (runtime). When Palette's Theri agent builds a Shopify page, there's no "Shopify skill" that gives Theri specific Shopify knowledge — it relies on the underlying LLM's training data.

**Recommendation**:
- Consider a "skill pack" layer that sits between RIUs and agent execution
- Skill packs would inject domain-specific context (e.g., "Shopify Flows", "python-pptx", "AWS CDK")
- This maps to Palette's existing knowledge library but makes it loadable/injectable rather than static
- Start lightweight: skill = markdown file with domain context, loaded when RIU triggers

### 5.5 Bootstrap Files Pattern (MEDIUM PRIORITY)

**What OpenClaw does**:
- 6 bootstrap files define agent behavior: AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, USER.md, BOOTSTRAP.md
- Injected into system prompt at session start
- Clear separation of concerns:
  - AGENTS.md = operating directives + memory
  - SOUL.md = persona, ethics, communication style
  - TOOLS.md = tool usage guidance
  - IDENTITY.md = agent identity markers
  - USER.md = user profile
  - BOOTSTRAP.md = first-run setup (removed after)

**What Palette does**:
- 3 tiers: palette-core.md (physics), assumptions.md (agents), decisions.md (log)
- Agent archetypes loaded as single markdown files
- User context via convergence brief

**Gap**: OpenClaw's separation is cleaner for runtime injection. Palette conflates "who the agent is" (archetype) with "what the agent knows" (tier context) with "what the user needs" (engagement context).

**Recommendation**:
- Consider splitting Palette's agent loading into:
  - CORE.md (palette-core.md — immutable)
  - AGENT.md (archetype definition — e.g., argentavis.md)
  - ENGAGEMENT.md (convergence brief + decisions — engagement-specific)
  - USER.md (user preferences and profile)
- This makes agent loading more composable and engagement switching cleaner

### 5.6 Sub-Agent Spawning (MEDIUM PRIORITY)

**What OpenClaw does**:
- `sessions_spawn` creates isolated background workers
- Sub-agents get reduced system prompt (task-focused)
- Configurable concurrency (default 8)
- Restricted tool access (deny list)
- Results announced back to parent session
- Management commands: list, stop, log, send

**What Palette does**:
- Orchestrator archetype (DESIGN ONLY — not implemented)
- Multi-agent workflows are sequential, not parallel
- No formal sub-agent spawning mechanism

**Gap**: Palette's Argy research tasks are prime candidates for parallel sub-agent execution (e.g., the 6 research documents for the MQ drop ran sequentially when they could have been parallel).

**Recommendation**:
- When implementing the Orchestrator, use OpenClaw's sub-agent pattern:
  - Spawn with task description + restricted tools
  - Reduced context (task-focused, not full engagement)
  - Announce results back with structured output
  - Configurable concurrency limits
- This is the highest-value operational improvement for Palette

### 5.7 Session Management (LOW PRIORITY)

**What OpenClaw does**:
- Session keys for conversation isolation
- JSONL transcript persistence
- Configurable reset policies (daily, idle timeout, manual)
- DM scoping (per-peer, per-channel, shared)

**What Palette does**:
- No session management — operates within whatever AI platform provides
- Each conversation is effectively a new session

**Gap**: Less relevant for Palette's current design (framework, not runtime). But if Palette ever becomes a runtime, OpenClaw's session model is well-designed.

### 5.8 Channel Abstraction (LOW PRIORITY for now)

**What OpenClaw does**:
- Unified agent across 12+ messaging channels
- Per-channel routing, activation modes, chunking policies
- Group chat support with mention gating

**What Palette does**:
- Single-channel (whatever AI interface is being used — Claude Code, Kiro, etc.)

**Gap**: Not a current priority, but demonstrates where agentic AI is heading — agents that live across all your communication surfaces, not just a dev tool.

---

## 6. WHAT PALETTE DOES BETTER THAN OPENCLAW

Not everything flows one direction. Palette has significant advantages:

### 6.1 Decision Classification
OpenClaw has no equivalent of ONE-WAY DOOR / TWO-WAY DOOR. It uses sandbox/tool-policy (mechanical safety) but doesn't classify decision reversibility. Palette's decision framework is more sophisticated for enterprise use.

### 6.2 Empirical Trust (Impressions System)
OpenClaw grants full trust immediately (constrained by sandboxing). Palette requires agents to earn trust through measured performance. This is more appropriate for enterprise contexts where reliability matters more than speed.

### 6.3 Agent Specialization with Boundaries
OpenClaw agents are generalists that use skills to specialize. Palette agents have hard boundaries — Argy CANNOT make decisions, Anky CANNOT implement fixes. This prevents role confusion and scope creep in complex engagements.

### 6.4 Formal Evaluation
Palette has Anky (multi-layered validation: deterministic → LM-as-Judge → human feedback), fixtures for agent testing, and structured quality gates. OpenClaw has no visible formal evaluation framework.

### 6.5 Knowledge Taxonomy
Palette's RIU taxonomy is a unique asset — 115 validated execution patterns that route problems to solutions. OpenClaw has nothing comparable. Skills teach tool usage; RIUs teach problem-solving.

### 6.6 Restartability
Palette's decisions.md + artifact approach means anyone can pick up where work left off. OpenClaw's memory system is personal and implicit — harder for a different person (or agent) to resume.

### 6.7 Glass-Box Reasoning
Palette's requirement that every material decision is traceable and inspectable is more rigorous than OpenClaw's approach, where the agent's reasoning is mostly in the conversation stream.

---

## 7. PRIORITY IMPLEMENTATION ROADMAP

If implementing learnings from OpenClaw, here's the suggested order:

| Priority | Learning | Effort | Impact | New RIU? |
|----------|---------|--------|--------|----------|
| **P0** | Memory architecture (MEMORY.md + daily logs) | Low | High | No — pattern for engagements |
| **P0** | Context compaction protocol | Low | High | Yes — RIU-607 |
| **P1** | Workflow DSL for composite agents | Medium | High | Yes — RIU-608 |
| **P1** | Sub-agent spawning for Orchestrator | Medium | High | Orchestrator promotion |
| **P2** | Skill packs (injectable domain context) | Medium | Medium | Library enhancement |
| **P2** | Bootstrap file separation | Low | Medium | No — structural refactor |
| **P3** | Session management patterns | High | Low (for now) | Future consideration |
| **P3** | Channel abstraction | High | Low (for now) | Future consideration |

---

## 8. SYNTHESIS: WHAT "THE FUTURE OF AGENTIC AI" MEANS

OpenClaw represents the **consumer/prosumer** future of agentic AI:
- Always-on, multi-channel, voice-capable
- Local-first, privacy-preserving
- Skills marketplace (ClawHub)
- One agent per person, running 24/7

Palette represents the **enterprise/professional** future:
- Convergence-first, glass-box, auditable
- Empirical trust, bounded agents
- Knowledge taxonomy, formal evaluation
- Multi-agent collaboration with quality gates

**The convergence point** is where Palette's rigor meets OpenClaw's runtime capabilities:
- Agents that earn trust AND can run autonomously once earned
- Workflows that are typed, resumable AND have decision classification
- Memory that is persistent AND curated with quality gates
- Skills that are injectable AND validated through the impressions system

The most powerful system would combine:
1. OpenClaw's runtime layer (Gateway, sessions, memory, channels)
2. Palette's decision framework (convergence, ONE-WAY DOORS, glass-box)
3. OpenClaw's workflow engine (Lobster DSL with approval gates)
4. Palette's quality system (Anky validation, impressions, fixtures)
5. OpenClaw's skill loading (hot-reload, gated, registry)
6. Palette's knowledge taxonomy (RIUs as routing table for skills)

---

## 9. RAW NOTES

### OpenClaw Source Structure (key directories)
```
src/
├── agents/          # Agent runtime and lifecycle
├── gateway/         # WebSocket control plane
├── channels/        # Messaging platform adapters
├── memory/          # Memory indexing and search
├── sessions/        # Session management
├── routing/         # Message routing logic
├── security/        # Sandboxing, tool policies
├── browser/         # CDP browser control
├── canvas-host/     # Visual workspace (A2UI)
├── hooks/           # Lifecycle hooks
├── plugins/         # Plugin SDK and system
├── providers/       # LLM provider adapters
├── tts/             # Text-to-speech
├── cli/             # CLI commands
├── commands/        # Chat slash commands
└── skills/          # Skills loading and management
```

### OpenClaw Key Config Files
```
~/.openclaw/
├── openclaw.json          # Main configuration
├── workspace/             # Agent workspace root
│   ├── AGENTS.md          # Operating directives
│   ├── SOUL.md            # Persona definition
│   ├── TOOLS.md           # Tool guidance
│   ├── IDENTITY.md        # Agent identity
│   ├── USER.md            # User profile
│   ├── MEMORY.md          # Long-term curated memory
│   ├── memory/            # Daily memory logs
│   │   └── YYYY-MM-DD.md
│   └── skills/            # Workspace skills
│       └── <skill>/
│           └── SKILL.md
├── skills/                # Managed (shared) skills
├── agents/                # Agent state directories
│   └── <agentId>/
│       └── sessions/
│           └── sessions.json
└── memory/
    └── <agentId>.sqlite   # Vector index
```

### Key Documentation URLs
- Agent Runtime: https://docs.openclaw.ai/concepts/agent.md
- Multi-Agent: https://docs.openclaw.ai/concepts/multi-agent.md
- Memory: https://docs.openclaw.ai/concepts/memory.md
- Skills: https://docs.openclaw.ai/tools/skills.md
- Lobster (Workflows): https://docs.openclaw.ai/tools/lobster.md
- Sub-Agents: https://docs.openclaw.ai/tools/subagents.md
- Session Management: https://docs.openclaw.ai/concepts/session.md
- System Prompt: https://docs.openclaw.ai/concepts/system-prompt.md
- Security Layers: https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated.md
- Full docs index: https://docs.openclaw.ai/llms.txt
