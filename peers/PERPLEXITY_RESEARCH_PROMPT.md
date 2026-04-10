# Perplexity Research: Local Multi-Agent Communication Hub

## Context

I have 6 AI agents running on my local machine, each with a different runtime:

| Agent | Runtime | MCP Support | Current Bus Access |
|-------|---------|-------------|-------------------|
| Claude Code | claude-code CLI | Yes (stdio) | Connected via MCP adapter |
| Mistral Le Chat | mistral-le-chat | Yes (stdio) | Connected via MCP adapter |
| Kiro | kiro-cli | MCP capable (not built) | No adapter |
| Codex | codex-cli | Tools + sandbox model | No adapter |
| Gemini | gemini-cli | Unknown | No adapter |
| Perplexity | API-only | No local process | No adapter |

I already have a working message bus: an HTTP + SQLite broker on localhost:7899 with governed message envelopes (risk gates, human checkpoints, persistent audit trail, FTS5 search, agent memory, agent skills). Two agents are connected via MCP adapters. The bus protocol is tested and solid.

**The problem**: I cannot get all 6 agents into one conversation. Each agent has a different runtime model. Building and maintaining per-agent MCP adapters is fragile — runtimes change, adapters break.

## What I Need Researched

### 1. Heterogeneous Agent Bridging Patterns (2026)
What are the current best practices for connecting agents with different runtime models to a single local communication bus? Specifically:

- **File-drop patterns**: Agents write JSON files to a watched directory, a daemon posts them to the bus. How are people implementing this? What are the atomic write / lock patterns to avoid corruption?
- **A2A protocol local mode**: Google's Agent2Agent protocol uses `/.well-known/agent.json` for discovery. Can A2A run purely locally (no cloud, no HTTPS) for heterogeneous agent coordination? Are there local-only A2A implementations?
- **claude-peers-mcp**: The louislva/claude-peers-mcp project does broker + MCP for Claude-to-Claude. Has anyone extended this pattern to non-Claude agents (Kiro, Codex, Gemini)?
- **Polling vs push**: For agents that can't run an MCP server (like API-only Perplexity), what's the lightest-weight polling integration?

### 2. Multi-Agent Communication Hubs with Web UI (2026)
I want a single HTML page (local, no cloud) where:
- I can see all messages across all agents
- I can send a message to any agent or broadcast to all
- I can see agent status, memory, and skills
- Voice notification via Rime TTS when a message arrives

What open-source projects exist for this? Specifically:
- **Agent dashboards**: Any local-first agent monitoring dashboards? (Not cloud-hosted like LangSmith)
- **Bus visualizers**: Any web UIs for SQLite-backed message buses?
- **ruflo, ClaudeSwarm, oh-my-claudecode**: These orchestration tools — do any provide a web dashboard for message monitoring?

### 3. File-Based Bus as Universal Bridge
The simplest pattern I can think of:
1. Shared directory `peers/dropbox/`
2. Each agent writes a JSON envelope file (UUID filename)
3. A watcher daemon reads new files and POSTs to the HTTP bus
4. Agent reads responses from the bus via polling or file write-back

Has anyone built this specific pattern? What are the failure modes? How do you handle:
- Partial writes (agent crashes mid-write)
- Ordering guarantees (files don't have timestamps as precise as DB inserts)
- Cleanup (who deletes processed files)
- Back-pressure (what if an agent floods the dropbox)

### 4. Kiro + Codex + Gemini CLI Communication
These three specific tools — Kiro CLI, OpenAI Codex CLI, and Google Gemini CLI:
- Do any of them support MCP natively as of April 2026?
- Do any of them have plugin/extension systems that could host a bus adapter?
- Do any of them support reading from stdin or a watched file for incoming messages?
- What's the lightest-weight way to inject a message into each of these tools?

### 5. Rime TTS as Notification Layer
Rime has an MCP server (`rime-mcp`) that exposes a `speak` tool. I want to use this as a notification layer:
- When a message arrives on the bus destined for the human, Rime reads it aloud
- This doesn't replace the bus — it's a voice notification on top

Has anyone combined Rime MCP with a message bus for agent notifications? What's the latency like? Is Arcana v3 fast enough for real-time notification (< 500ms)?

### 6. What I Should NOT Build
Given the pace of change in 2026:
- Which of these problems will be solved by MCP roadmap features in the next 3-6 months?
- Which agent runtimes (Kiro, Codex, Gemini) are likely to add native MCP or A2A support soon?
- Where should I invest effort vs. wait for the ecosystem to catch up?

## Constraints
- Everything must run locally (no cloud services for the bus itself)
- No API credits for the bus (agents may use their own APIs, but bus infra is zero-cost)
- Must work on Linux (Ubuntu)
- SQLite is the database (already in use)
- The existing bus protocol (governed envelopes, risk gates, human checkpoints) must be preserved
- Solution should take < 8 hours to build, not 2 days that falls apart

## Output Format
For each section, provide:
1. The best current solution (with GitHub link or docs link)
2. Whether it's proven in production or experimental
3. Estimated integration effort (hours)
4. Risk level (will it break when runtimes update?)
