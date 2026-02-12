# Palette Core Documentation

This document defines the immutable physics of Palette — the foundational patterns that govern all agent engagements.

## Engagement Memory

Every Palette engagement MUST maintain a MEMORY.md file at the engagement root directory. This is the canonical source of truth for facts that persist across sessions.

### MEMORY.md Structure

MEMORY.md contains ONLY verified, canonical facts. It is curated, not appended — outdated entries are updated or removed.

Required sections:
- **Canonical Numbers**: All quantitative values that appear in multiple documents (budget, team size, ROI projections, timelines). When a number changes, MEMORY.md updates FIRST, then documents follow.
- **Key Decisions**: Summary of ONE-WAY DOOR and TWO-WAY DOOR decisions with status. This mirrors decisions.md but in quick-reference format.
- **Active Agents**: Which Palette agents have contributed, what phase the engagement is in.
- **Known Gaps**: What has been flagged but not yet addressed.

Rules:
- Every agent MUST read MEMORY.md before producing output.
- Every agent that produces quantitative output MUST check its numbers against MEMORY.md canonical numbers.
- If an agent's work changes a canonical number, it MUST flag this as a MEMORY UPDATE and explain why the number changed.
- MEMORY.md should stay under 200 lines. If it grows beyond this, archive older entries to decisions.md or a separate reference file.

### Daily Engagement Logs

Long-running engagements SHOULD maintain daily logs at `memory/YYYY-MM-DD.md` within the engagement directory. These are append-only operational records.

Each daily log entry includes:
- Agent that acted
- What was produced or changed
- Any canonical number changes (cross-reference MEMORY.md)
- Blockers encountered
- Next expected action

Daily logs are operational context — they help resume work after session breaks. Unlike MEMORY.md (curated truth), daily logs are raw chronological records.

---

## Context Compaction Protocol

When an engagement session approaches context limits (operator judgment or system warning), execute the COMPACT protocol before context is lost:

### COMPACT Steps

1. **Flush to MEMORY.md**: Update MEMORY.md with any canonical facts from the current session that aren't yet recorded.
2. **Flush to daily log**: Write a daily log entry summarizing what was accomplished in this session.
3. **Update decisions.md**: Log any decisions made in this session that haven't been recorded.
4. **Write continuation note**: At the bottom of the daily log, write a "NEXT SESSION STARTS HERE" block with:
   - Current phase and step
   - What was in progress when compaction triggered
   - What the next action should be
   - Any context that won't survive in artifacts alone (e.g., "the user prefers conservative estimates" or "we decided to skip the vendor analysis")
5. **Summarize artifacts**: List all files created or modified in this session with one-line descriptions.

### Compaction Ownership

Yuty (narrative coherence agent) owns the COMPACT protocol. When another agent is active and compaction is needed, Yuty runs compaction before handing back to the active agent.

### Prevention

Before starting a session on a long engagement, agents SHOULD:
- Read MEMORY.md first (canonical state)
- Read the most recent daily log (operational context)
- Read decisions.md (decision history)
- Only then read specific phase artifacts as needed

This reduces context consumption by avoiding re-reading completed artifacts that are already summarized in MEMORY.md.

---

## Agent Loading Protocol

When loading a Palette agent into a session, context is assembled from 4 layers (in order):

1. **CORE** — `palette-core.md` (immutable Palette physics — never changes between engagements)
2. **AGENT** — Agent archetype definition (e.g., `agents/argentavis/argentavis.md` — defines who this agent is, what it can/cannot do)
3. **ENGAGEMENT** — Engagement-specific context:
   - `MEMORY.md` (canonical facts)
   - `decisions.md` (decision history)
   - `workflow.yaml` (phase structure, if exists)
   - Latest daily log (operational context)
4. **USER** — User preferences and profile (communication style, domain expertise, constraints)

### Loading Rules

- Layers 1 and 2 are STABLE — they change only when Palette or the agent definition is updated.
- Layers 3 and 4 are ENGAGEMENT-SPECIFIC — they change with every engagement.
- When switching engagements, only layers 3 and 4 need to change.
- When switching agents within an engagement, only layer 2 changes.
- This separation reduces context waste and makes agent/engagement switching clean.
