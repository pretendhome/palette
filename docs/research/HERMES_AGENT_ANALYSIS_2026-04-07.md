# Kiro Analysis: Hermes Agent — What Palette Can Learn

**Author**: kiro.design
**Date**: 2026-04-07
**Source**: [github.com/nousresearch/hermes-agent](https://github.com/nousresearch/hermes-agent)
**Stats**: 33K stars, 4.2K forks, 3,472 commits, MIT license, v0.7.0 (Apr 3 2026)
**Built by**: Nous Research (formerly OpenClaw → rebranded to Hermes Agent)

---

## What Hermes Agent Is

A self-improving AI agent with a closed learning loop. Single Python codebase (~50K+ lines) that runs as CLI, messaging gateway (Telegram/Discord/Slack/WhatsApp/Signal/14 platforms), cron scheduler, ACP server (VS Code/Zed/JetBrains), and batch runner. Provider-agnostic (OpenRouter, OpenAI, Anthropic, Gemini, local models). Runs on a $5 VPS or serverless.

The core differentiator: it learns from experience. It creates skills from completed tasks, improves them during use, nudges itself to persist knowledge, searches past conversations, and builds a user model across sessions.

---

## Architecture Overview

Three-layer system:

1. **AIAgent** (`run_agent.py`, ~9,200 lines) — core conversation loop with prompt building, provider resolution, tool dispatch
2. **Entry points** — CLI, Gateway (14 platform adapters), ACP (IDE integration), Cron, Batch Runner
3. **Tool system** — 47 tools across 20 toolsets, 6 terminal backends (local, Docker, SSH, Modal, Daytona, Singularity)

Key subsystems: Skills (procedural memory), Memory (MEMORY.md + USER.md), Session Search (SQLite + FTS5), Cron (scheduled agent tasks), Gateway (multi-platform messaging), Plugin system.

---

## 7 Things Palette Should Steal

### 1. SKILLS SYSTEM (HIGH PRIORITY)

**What Hermes does**: When the agent completes a complex task (5+ tool calls), it saves the approach as a reusable "skill" — a SKILL.md file with trigger conditions, procedure, pitfalls, and verification steps. Skills use progressive disclosure (Level 0: list names, Level 1: full content, Level 2: reference files) to minimize token usage.

**What Palette lacks**: Our agents have no procedural memory. Every session starts from zero. Kiro's `KIRO_READ_THIS_FIRST.md` is a manual version of this, but it's not structured, not progressive, and not auto-generated from successful task completions.

**What to build**: A skill system for Palette agents. When an agent completes a complex task successfully (e.g., "rewire voice_interface.py to use peers bus"), it should auto-generate a skill file with the procedure, pitfalls discovered, and verification steps. Store in `~/.kiro/skills/` (or per-agent equivalent). Load via progressive disclosure — agent sees skill names in system prompt, loads full content only when relevant.

**Palette-specific twist**: Our skills should be governed. New skills enter as UNVALIDATED. After 10 successful uses, promote to WORKING. This maps directly to our agent maturity model in assumptions.md.

### 2. BOUNDED PERSISTENT MEMORY (HIGH PRIORITY)

**What Hermes does**: Two files — MEMORY.md (2,200 chars, agent's notes) and USER.md (1,375 chars, user profile). Injected into system prompt as frozen snapshot at session start. Agent manages its own memory via add/replace/remove actions. Character limits force curation — when full, the agent must consolidate or replace entries.

**What Palette lacks**: We have no persistent memory across sessions. assumptions.md says "No persistent memory across engagements/projects" and "No historical logging beyond what is required for toolkit integrity." This was a deliberate design choice for statelessness, but it means every session starts cold.

**What to build**: A bounded memory system for each agent. Not unlimited — Hermes's insight is that bounded memory forces curation, which produces higher-quality recall. 2,200 chars (~800 tokens) is enough for 8-15 critical facts. This is cheap enough to inject into every system prompt without blowing context.

**Palette-specific twist**: Memory should be per-workspace, not global. The oil-investor workspace needs different memory than the rossi workspace. This maps to our existing workspace config pattern.

### 3. SESSION SEARCH (MEDIUM PRIORITY)

**What Hermes does**: All sessions stored in SQLite with FTS5 full-text search. Agent can search past conversations to find "did we discuss X last week?" Uses Gemini Flash for summarization of search results.

**What Palette lacks**: Our peers bus messages are ephemeral (consumed on read). Session summaries exist as steering files but aren't searchable. When Claude's bus message was consumed before he could read it, we lost the content permanently.

**What to build**: Persist all bus messages to SQLite with FTS5. The broker already has the data — it just needs a write-through to a persistent store. Then add a `bus_search` tool that agents can use to find past messages. This solves the "consumed message" problem that bit us during the governance project.

### 4. CRON / SCHEDULED TASKS (MEDIUM PRIORITY)

**What Hermes does**: First-class scheduled agent tasks. Jobs store in JSON, support cron expressions, can attach skills and scripts, and deliver results to any platform. Not shell cron — agent cron. The agent runs a full conversation loop on schedule.

**What Palette lacks**: No scheduled tasks. The wiki validator, semantic audit, and health checks all run manually. The expiry check for governance proposals (`--check-expiry`) has no cron job.

**What to build**: A simple cron system for Palette. Start with 3 jobs:
- Daily: `validate_wiki.py` + `file_proposal.py --check-expiry`
- Weekly: semantic audit (stale counts, orphan detection)
- On-commit: `compile_wiki.py` + health checks

This doesn't need Hermes's full complexity. A systemd timer or cron job that runs Python scripts and posts results to the bus is enough for v1.

### 5. MULTI-PLATFORM GATEWAY (MEDIUM PRIORITY)

**What Hermes does**: One gateway process serves 14 messaging platforms. Telegram, Discord, Slack, WhatsApp, Signal, Matrix, email, SMS, Home Assistant, webhook. Cross-platform conversation continuity. Voice memo transcription.

**What Palette has**: Telegram bridge (rossi_bridge.py, joseph_bridge.py), peers bus (HTTP broker), voice bridge (terminal_voice_bridge.mjs). But these are separate, disconnected systems.

**What to build**: Not the full 14-platform gateway — that's over-engineered for our needs. But a unified gateway that routes messages from Telegram, CLI voice, and the peers bus through one process would eliminate the current fragmentation. The Mission Canvas server at port 8787 is already close to this — it just needs the Telegram adapter wired in alongside the HTTP API.

### 6. PROGRESSIVE DISCLOSURE FOR CONTEXT (LOW PRIORITY)

**What Hermes does**: Skills use 3-level progressive disclosure. Level 0 is just names and descriptions (~3K tokens for all skills). Level 1 is full content (loaded on demand). Level 2 is reference files within a skill. The agent only loads what it needs.

**What Palette lacks**: Our steering files are all-or-nothing. palette-core.md (13KB) is loaded in full every session. assumptions.md (10KB) is loaded in full. That's ~23KB of context before the agent does anything.

**What to build**: A progressive disclosure layer for steering files. Level 0: one-line summaries of each steering file (~500 tokens). Level 1: full file loaded on demand via `#filename` (which Kiro already supports). This would free up ~20K tokens of context window for actual work.

### 7. SECURITY SCANNING FOR SKILLS/PLUGINS (LOW PRIORITY)

**What Hermes does**: All hub-installed skills go through a security scanner that checks for data exfiltration, prompt injection, destructive commands, and supply-chain signals. Trust levels: builtin → official → trusted → community.

**What Palette has**: Our governance model has tier-based trust (Tier 1/2/3) but no automated security scanning of proposals or code contributions.

**What to build**: Not urgent, but when we open the wiki governance pipeline to external contributors, we'll need automated scanning of proposed KL entries for prompt injection, hallucinated sources, and contradictions with existing entries. The governance model already has the trust tiers — we just need the scanner.

---

## 3 Things Palette Does Better Than Hermes

### 1. Multi-agent governance

Hermes is a single-agent system. One agent, one memory, one skill set. Palette has 5 agents with different cognitive styles, a proposal/vote/promote governance pipeline, and a wire contract for inter-agent communication. Hermes has no equivalent of our peers bus, no voting, no multi-perspective convergence.

### 2. Deterministic knowledge routing

Hermes uses LLM inference for everything — routing, skill selection, memory management. Palette has deterministic taxonomy routing (121 RIUs), structured KL lookup, and convergence chain traversal that work without any LLM calls. Our system is more reliable and auditable for the same class of problems.

### 3. Decision governance (OWD)

Hermes has command approval (dangerous command detection) but no concept of one-way door decisions, no confirmation gates for irreversible actions, no decision logging with rationale. Palette's OWD system is more sophisticated and more important for production use.

---

## 3 Things That Are Interesting But Not Actionable Yet

### 1. RL Training / Tinker-Atropos integration
Hermes has a full environment framework for evaluation and reinforcement learning training. Generates ShareGPT-format trajectories from agent interactions. This is research infrastructure — interesting for training custom models but not relevant to Palette's current needs.

### 2. ACP (Agent Communication Protocol) for IDE integration
Hermes exposes itself as an editor-native agent over stdio/JSON-RPC for VS Code, Zed, and JetBrains. This is a distribution channel, not a capability. Interesting if we ever want Palette to live inside an IDE.

### 3. Profile isolation
Each Hermes profile gets its own HERMES_HOME, config, memory, sessions, and gateway PID. Multiple profiles run concurrently. This maps to our workspace concept but at the agent level rather than the project level.

---

## Priority Recommendation

| Item | Priority | Effort | Impact on Palette |
|------|----------|--------|-------------------|
| Skills system (procedural memory) | HIGH | 2-3 days | Agents stop re-learning the same workflows |
| Bounded persistent memory | HIGH | 1-2 days | Sessions start warm instead of cold |
| Session search (bus persistence) | MEDIUM | 1 day | No more lost bus messages |
| Cron / scheduled tasks | MEDIUM | 0.5 day | Automated health checks, expiry enforcement |
| Unified gateway | MEDIUM | 2-3 days | Telegram + voice + bus through one process |
| Progressive disclosure | LOW | 1 day | Free up ~20K tokens of context window |
| Security scanning | LOW | 2-3 days | Needed when governance opens to external contributors |

**Start with**: Skills system + bounded memory. These two changes would make the biggest difference in agent effectiveness. Every other agent system (Hermes, Claude Code, Codex) has some form of persistent procedural memory. We're the only multi-agent system that starts every session from scratch.

---

## The Deeper Insight

Hermes is a single-agent system that compensates for having one perspective by learning aggressively from experience. Palette is a multi-agent system that compensates for lack of memory by having multiple perspectives.

The ideal system has both: multiple agents with different cognitive styles AND persistent memory that compounds across sessions. That's the synthesis. Hermes shows us the memory architecture. We already have the multi-agent architecture. Combining them is the next evolution of Palette.

---

*Analysis by kiro.design. No implementation — observation only, as requested.*

References:
[1] Hermes Agent GitHub - https://github.com/nousresearch/hermes-agent
[2] Hermes Agent Docs - https://hermes-agent.nousresearch.com/docs/
