# Researcher Auto-Enrichment Spec
## Knowledge Library Growth Through Governed Research

**Date**: 2026-04-21
**Status**: SPEC — build Thursday/Friday after interview gauntlet
**Owner**: Claude (spec), operator (build)
**Principle**: The smallest system that can be trusted in production.

---

## The Problem

Every time the researcher completes a deep research task, it produces findings with claims, evidence, sources, and confidence scores. Those findings get returned to the requesting agent and then disappear. The knowledge library stays static at 176 entries unless someone manually proposes additions.

Meanwhile, the governance pipeline (file_proposal → record_vote → promote_proposal) is fully operational but starved of input. Bridge_feedback creates gap signals from bus messages, but no agent automatically proposes substantive knowledge entries from research output.

The result: the system gets smarter during a session but forgets between sessions. This is the Hermes procedural memory gap applied to knowledge, not just skills.

## The Solution

After the researcher completes any task, it evaluates its findings against the existing knowledge library and automatically files high-quality findings as Tier 1 proposals through the existing governance pipeline. No new infrastructure — just connecting the researcher's output to the governance pipeline's input.

## Architecture

```
Task arrives
  → Resolver classifies (unchanged, local, fast)
  → Researcher runs (Perplexity Sonar / Tavily / Exa — unchanged)
  → Researcher produces HandoffResult with findings[]
  → NEW: Auto-enrichment filter runs on findings[]
    → For each finding:
      1. Check: does this claim already exist in the knowledge library?
      2. Check: is the confidence above threshold (75)?
      3. Check: does it have at least one verifiable source?
      4. If all three pass → format as KL proposal
    → File proposals via existing file_proposal.py
    → Log what was proposed and what was filtered out
  → HandoffResult continues to requesting agent (unchanged)
```

## What Changes

| Component | Change | Risk |
|-----------|--------|------|
| `researcher.py` | Add post-completion hook that calls auto-enrichment filter | LOW — additive, doesn't change core research flow |
| New: `auto_enrich.py` | Filter + formatter that evaluates findings and files proposals | LOW — standalone module, no dependencies on core agents |
| `file_proposal.py` | No change — already accepts proposals programmatically | NONE |
| Knowledge library | Grows through governed proposals — no direct writes | NONE |
| Governance pipeline | Receives more proposals — existing voting/promotion flow handles quality gate | NONE |

## What Does NOT Change

- Resolver: untouched
- Orchestrator: untouched
- Knowledge library: never written to directly — only through governance
- Governance model: no new tiers, no new rules
- Human approval: still required for promotion to library
- Existing research flow: findings still returned to requesting agent exactly as before

## The Auto-Enrichment Filter (`auto_enrich.py`)

### Input
```python
findings: list[dict]  # from researcher HandoffResult.output.findings
# Each finding: {claim, evidence, source, confidence}
```

### Filter Rules

1. **Deduplication**: Check each claim against existing KL entries using keyword overlap + semantic similarity (simple TF-IDF, not vector DB — keep it light). If >80% overlap with an existing entry, skip. If 50-80% overlap, flag as "possible update to existing entry" rather than new entry.

2. **Confidence threshold**: Only propose findings with confidence >= 75. Below that, the researcher itself wasn't sure — don't pollute the pipeline with uncertain claims.

3. **Source requirement**: At least one source with a URL that was actually fetched (not just a search snippet). The knowledge library standard is sourced citations — unsourced claims don't qualify.

4. **Recency filter**: For current-events or product-specific findings, include a `valid_until` date (default: 90 days). This prevents the library from accumulating stale product claims. The governance pipeline can extend or retire entries during review.

5. **Rate limit**: Maximum 5 proposals per research task. If more than 5 findings pass the filter, take the top 5 by confidence. This prevents a single deep research task from flooding the governance pipeline.

### Output Format

Each proposal follows the existing governance schema:

```yaml
proposal_id: "AUTO-{timestamp}-{index}"
type: "addition"
source_agent: "researcher"
source_task: "{task_id from HandoffPacket}"
title: "{claim, compressed to <80 chars}"
content:
  question: "{the claim as a question the KL would answer}"
  answer: "{the evidence, with inline citations}"
  sources:
    - url: "{source URL}"
      title: "{source title}"
      retrieved_at: "{ISO timestamp}"
      reliability: "{tier 1/2/3 per Palette evidence bar}"
  confidence: {0-100}
  valid_until: "{ISO date, default 90 days from now}"
  evidence_tier: "{derived from source reliability}"
  tags: ["{RIU IDs from the original task classification}"]
filed_at: "{ISO timestamp}"
auto_generated: true
status: "proposed"
```

### Filing

Call `file_proposal.py` with the formatted proposal. The existing script:
- Saves to `wiki/proposed/`
- Notifies the bus (best-effort)
- Tracks resubmission limits (max 3 per topic)
- Checks expiry (14-day review window)

No changes needed to `file_proposal.py`.

## Integration Point in researcher.py

After the researcher produces its HandoffResult (around line 400-500 in the current code), add:

```python
# Auto-enrichment: propose high-confidence findings to knowledge library
if findings and len(findings) > 0:
    try:
        from auto_enrich import evaluate_and_propose
        proposed, filtered = evaluate_and_propose(
            findings=result.output.get("findings", []),
            task_id=packet.id if packet else "unknown",
            source_rius=matched_rius,  # from the original classification
            kl_path=KNOWLEDGE_LIBRARY_PATH,
        )
        result.output["auto_enrichment"] = {
            "proposed": len(proposed),
            "filtered": len(filtered),
            "proposal_ids": [p["proposal_id"] for p in proposed],
        }
        # Log to stderr for human visibility
        if proposed:
            print(f"[auto-enrich] Filed {len(proposed)} KL proposals, filtered {len(filtered)}", file=sys.stderr)
    except Exception as e:
        # Auto-enrichment is best-effort — never block research output
        print(f"[auto-enrich] Failed (non-blocking): {e}", file=sys.stderr)
```

Key design decision: **best-effort, never blocking**. If auto-enrichment fails for any reason, the research output is still delivered unchanged. The enrichment is a side effect, not a dependency.

## Governance Flow (Existing — No Changes)

```
auto_enrich.py files proposal
  → wiki/proposed/{proposal_id}.yaml
  → bus notification (best-effort)
  → Agents see proposals in their feeds
  → Voting: binding agents (Kiro, Codex, Claude) vote
  → Quorum reached → promote_proposal.py
  → Entry added to knowledge library with full provenance
  → Wiki recompiled
```

## Measurement

Track in the health agent (new checks for Section 8 or new Section 15):

| Metric | What It Measures |
|--------|-----------------|
| Proposals filed (auto) | Volume of auto-enrichment activity |
| Proposals promoted | Quality of auto-generated proposals (should trend up as filter improves) |
| Proposals rejected | Filter calibration signal (if too many rejected, raise confidence threshold) |
| Proposals expired | Review cadence signal (if many expire, review process is too slow) |
| KL growth rate | Entries/week from auto-enrichment vs manual |
| Dedup hit rate | How often findings already exist in KL (high = library is comprehensive) |

## Perplexity Competition Angle

For the Billion Dollar Build pitch, this is the demo:

1. "Watch: I ask the system a question about enterprise AI governance"
2. Researcher runs → Perplexity Agent API does multi-step research → findings returned
3. "Now watch what happens next: the system automatically proposed 3 new knowledge entries from that research"
4. "Those proposals go through a governance pipeline where multiple agents vote on quality"
5. "The ones that pass become permanent institutional knowledge — cited, sourced, governed"
6. "The system gets smarter every time someone uses it. That's the moat."

The pitch is: **self-improving enterprise knowledge that compounds with use, with governance that prevents pollution.**

## Build Plan (Thursday/Friday)

| Step | Time | What |
|------|------|------|
| 1 | 1 hour | Write `auto_enrich.py` — filter + formatter + filing |
| 2 | 30 min | Add integration hook to `researcher.py` (the try/except block above) |
| 3 | 30 min | Write 5 test cases: dedup, confidence filter, source requirement, rate limit, format validation |
| 4 | 30 min | Run one real research task end-to-end, verify proposals appear in `wiki/proposed/` |
| 5 | 30 min | Add health check metrics (proposals filed, promoted, rejected) |
| 6 | 30 min | Update MANIFEST.yaml with auto-enrichment section |

**Total: ~3.5 hours.** All additive. No existing code modified except the one hook in researcher.py.

## What This Enables Next

Once auto-enrichment is working:

1. **Perplexity competition demo** — live demo of self-improving knowledge
2. **Perficient live build** — build a domain-specific version in 2.5 hours (healthcare or BFSI knowledge auto-enrichment)
3. **Skills auto-save** (Hermes fix #2) — same pattern applied to procedural memory instead of knowledge: after an agent completes a complex task, auto-save the procedure as a skill proposal through governance
4. **Glean enablement** — if you get the role, this IS the content-operations pipeline: product changes → research → auto-proposed enablement entries → governed review → published to field

## Open Questions (for crew review)

1. Should the confidence threshold be 75 or higher? Too low = noise. Too high = misses useful findings.
2. Should deduplication use simple keyword overlap or the existing signal-matching from the taxonomy? Signal-matching is more accurate but adds dependency on the resolver.
3. Should auto-enrichment run on every research task or only on `depth: deep` tasks? Running on every task means more proposals but also more noise from quick lookups.
4. Should there be an opt-out flag on the HandoffPacket? ("Don't auto-enrich this research" for sensitive or ephemeral tasks.)
5. Should the rate limit be 5 per task or 5 per hour? Per-task is simpler. Per-hour prevents a burst of deep research tasks from flooding the pipeline.

---

*Spec written 2026-04-21. Build target: Thursday April 24 or Friday April 25, after Capital Group tech interview (Wed 2:30pm) and Glean Stage 1 (Wed 10:30am). The interview gauntlet comes first.*
