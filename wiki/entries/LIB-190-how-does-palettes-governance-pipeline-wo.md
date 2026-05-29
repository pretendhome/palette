---
source_file: knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml
source_id: LIB-190
source_hash: sha256:74553aedcd9bbe3a
compiled_at: 2026-05-27T22:42:24Z
compiler_version: 1.0.0
type: knowledge_entry
evidence_tier: 2
tags: [foundation, governance, knowledge-entry, knowledge-evolution, quality-gates, voting]
related: [RIU-001, RIU-062]
handled_by: [architect, debugger, researcher]
journey_stage: foundation
DO_NOT_EDIT: This file is auto-generated. Edit the source YAML and recompile.
---

# How does Palette's governance pipeline work and what are the four scripts?

The governance pipeline is a four-stage workflow that controls what enters the knowledge library. It prevents memory pollution by requiring structured review before any new knowledge is canonicalized.

## Definition

The governance pipeline is a four-stage workflow that controls what enters the knowledge library. It prevents memory pollution by requiring structured review before any new knowledge is canonicalized.

**The four scripts**:
1. **file_proposal.py** (377 lines): Accepts a proposal, assigns a unique ID (PROP-YYYY-MM-DD-NNN), validates tier/type/content structure, writes YAML + rendered markdown, generates approval queue, posts to peers bus.
2. **record_vote.py** (199 lines): Records agent votes (approve/object/object-with-alternative). Checks binding vs advisory status. Evaluates unanimous consent. Any binding objection blocks.
3. **promote_proposal.py** (196 lines): Takes approved proposals, generates next LIB-ID, appends to knowledge library YAML, archives proposal, recompiles wiki.
4. **bridge_feedback_to_proposals.py** (124 lines): Reads external feedback (palette_feedback.yaml from implementations), converts to governance proposals. Closes the feedback loop.

**Key properties**: Proposals expire after 14 days (no zombie proposals). Evidence tiers filter source quality. Voting roster defines binding vs advisory agents with quorum minimum.

 **The pattern**: This is the same propose → confirm → graduate pattern that Mozilla CQ independently built for shared agent learning. Our version adds evidence tiers and multi-agent voting.

## Evidence

- **Tier 2 (entry-level)**: Palette Governance Pipeline Scripts (`scripts/file_proposal.py`)
- **Tier 2 (entry-level)**: [Mozilla CQ — Shared agent learning with 5-tool pattern](https://github.com/mozilla-ai/cq)

Evidence tier shown is the entry-level minimum. Individual source tiers are not yet classified.

## Related

- [RIU-001](../rius/RIU-001.md)
- [RIU-062](../rius/RIU-062.md)

## Handled By

- [Architect](../agents/architect.md)
- [Debugger](../agents/debugger.md)
- [Researcher](../agents/researcher.md)

## Learning Path

- [RIU-001](../paths/RIU-001-convergence-brief.md) — hands-on exercise

## Provenance

Source: `knowledge-library/v1.4/palette_knowledge_library_v1.4.yaml`, entry LIB-190.
Evidence tier: 2.
Journey stage: foundation.
