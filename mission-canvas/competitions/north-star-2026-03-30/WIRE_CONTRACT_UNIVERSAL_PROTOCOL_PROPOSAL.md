# Proposal: Wire Contract as Universal Communication Protocol

**Author**: kiro.design
**Date**: 2026-03-30
**Status**: PROPOSAL — requesting team feedback
**Scope**: Palette, Mission Canvas, Enablement, UX

---

## The Insight

We have three communication protocols in the system today:

1. **Wire Contract** (Palette SDK) — 7 fields in, 7 fields out. Agent-to-agent.
2. **Peer Envelope** (Peers Bus) — 12 fields. Agent-to-agent over HTTP.
3. **Ad-hoc JSON** (Canvas endpoints) — Different shape per endpoint. System-to-UX.

The coaching system we built today added a fourth implicit protocol: coaching_signals flowing from Canvas to UX with their own shape (concept_id, term, depth, explanation).

Mical asked: can the wire contract also carry Enablement ↔ UX communication?

The answer is yes — and the implications are bigger than coaching.

---

## The Wire Contract Today

From `palette/sdk/agent_base.py`:

```
HandoffPacket (7 fields in):
  id        — unique identifier
  from      — sender identity
  to        — recipient identity
  task      — what needs to be done
  riu_ids   — which problem types are involved
  payload   — domain-specific content (freeform)
  trace_id  — links related messages

HandoffResult (7 fields out):
  packet_id — links back to the input
  from      — who produced this result
  status    — success | failure | blocked
  output    — domain-specific result (freeform)
  blockers  — what prevented success (glass-box)
  artifacts — what was created
  next_agent — who should act next
```

The key design property: **everything domain-specific lives in `payload` and `output`. Everything structural is fixed.** This means the contract can carry ANY content without schema changes.

---

## What Enablement ↔ UX Communication Looks Like

### Teaching Moment (Enablement → UX)

When the system wants to teach the user something:

```json
{
  "id": "cm-OIL-002-1711835400",
  "from": "enablement.coaching",
  "to": "ux.workspace",
  "task": "teach_concept",
  "riu_ids": [],
  "payload": {
    "concept_id": "OIL-002",
    "term": "crack spread",
    "depth": "full",
    "explanation": "The 3-2-1 crack spread is the industry standard benchmark for refining margins.",
    "sources": [{"title": "EIA Refinery Reports", "url": "https://..."}],
    "stage": "orient",
    "suggested_followup": "Want me to explain how to read it yourself?"
  },
  "trace_id": "session-oil-investor-2026-03-30"
}
```

### Teaching Result (UX → Enablement)

When the user responds to coaching:

```json
{
  "packet_id": "cm-OIL-002-1711835400",
  "from": "ux.workspace",
  "status": "success",
  "output": {
    "user_action": "acknowledged",
    "time_spent_ms": 3200,
    "followup_requested": false
  },
  "blockers": [],
  "artifacts": [],
  "next_agent": "enablement.coaching"
}
```

### Mastery Verification (UX → Enablement)

```json
{
  "id": "mv-OIL-002-1711835500",
  "from": "ux.workspace",
  "to": "enablement.coaching",
  "task": "verify_mastery",
  "riu_ids": [],
  "payload": {
    "concept_id": "OIL-002",
    "user_answer": "It's the margin refiners earn — 3 barrels crude in, 2 gasoline and 1 diesel out.",
    "verification_type": "teach_back"
  },
  "trace_id": "session-oil-investor-2026-03-30"
}
```

### Verification Result (Enablement → UX)

```json
{
  "packet_id": "mv-OIL-002-1711835500",
  "from": "enablement.coaching",
  "status": "success",
  "output": {
    "mastery_confirmed": true,
    "new_stage": "verify",
    "feedback": "That's exactly right. You won't see this explanation again."
  },
  "blockers": [],
  "artifacts": ["learner_lens.yaml"],
  "next_agent": ""
}
```

It fits perfectly. No schema changes needed.

---

## Why This Matters

### 1. One Protocol, Three Systems

Today:
- Palette agents speak wire contract
- Canvas endpoints speak ad-hoc JSON
- Coaching speaks coaching_signals
- Peers bus speaks peer envelope

If we unify on the wire contract:
- Palette agents speak wire contract
- Canvas speaks wire contract (wrapped in HTTP)
- Coaching speaks wire contract
- Peers bus speaks wire contract (peer envelope becomes a transport wrapper around wire packets)

One protocol to learn. One protocol to debug. One protocol to trace.

### 2. Coaching Becomes Traceable

Every teaching moment is a HandoffPacket. Every verification is a HandoffResult. The trace_id links them to the session. You can reconstruct the entire learning journey from wire messages:

```
Packet: teach OIL-002 (depth: full)
  → Result: acknowledged (3.2s)
Packet: teach OIL-002 (depth: brief)
  → Result: acknowledged (0.8s)
Packet: verify OIL-002
  → Result: mastery confirmed
```

This is the same traceability we have for agent handoffs. Now we have it for learning.

### 3. Flywheel Feedback Is Native

Claude's flywheel_feedback system generates KL candidates, decision records, and mastery signals. Today these are custom objects. If they were wire packets, the Palette enrichment pipeline could consume them using the same `from_wire()` method it uses for agent results. No special parsing.

### 4. MCP Distribution Gets Simpler

The MCP tools we're building for Palette-as-a-service need to communicate coaching signals to the client. If coaching speaks wire contract, the MCP tool just returns a HandoffResult. The client (Claude Desktop, Cursor, etc.) renders it however it wants. We don't need a separate coaching API shape for MCP.

### 5. The UX Becomes an Agent

This is the deep insight. If the UX speaks wire contract, it IS an agent. It has an identity (`ux.workspace`), it sends packets (user actions), it receives results (system responses). The boundary between "agent" and "user interface" dissolves.

This means:
- The workspace selector is a routing decision (which agent context to load)
- A button click is a HandoffPacket (task: "resolve_evidence", payload: {evidence_id: "ME-001"})
- A coaching hint is a HandoffResult (output: {explanation: "..."})
- The convergence chain response is a HandoffResult (output: {narration: "...", health_score: 85})

The UX doesn't need custom endpoint shapes. It sends packets, receives results.

---

## What Changes

### Phase 1: Coaching on Wire (Low Risk)

Map the existing coaching_signals to wire format. No functional change — just reshape the data.

**Current** (in convergence_chain response):
```json
{
  "coaching_signals": [
    {"concept_id": "OIL-002", "term": "crack spread", "depth": "full", "explanation": "..."}
  ]
}
```

**Proposed** (same data, wire shape):
```json
{
  "coaching_packets": [
    {
      "id": "cm-OIL-002-...",
      "from": "enablement.coaching",
      "to": "ux.workspace",
      "task": "teach_concept",
      "riu_ids": [],
      "payload": {"concept_id": "OIL-002", "term": "crack spread", "depth": "full", "explanation": "..."},
      "trace_id": "session-..."
    }
  ]
}
```

The UX renders it the same way. But now it's a wire packet that can be traced, logged, and consumed by the enrichment pipeline.

### Phase 2: Mutations on Wire (Medium Risk)

Map Canvas mutation endpoints to wire format. Each endpoint becomes a packet type:

| Current Endpoint | Wire Task |
|---|---|
| POST /resolve-evidence | `resolve_evidence` |
| POST /add-fact | `add_fact` |
| POST /confirm-one-way-door | `confirm_owd` |
| POST /verify-mastery | `verify_mastery` |
| POST /coaching-check | `check_coaching_depth` |

The HTTP endpoints stay (backward compatibility). But internally, they deserialize to HandoffPacket, process, and return HandoffResult.

### Phase 3: Full Wire UX (Higher Risk, Future)

The UX sends all interactions as wire packets. The server is a packet router. This is the "UX as agent" vision. Defer to V2.

---

## What Does NOT Change

- The wire contract schema (7 in, 7 out) — no modifications
- The peer envelope — it wraps wire packets for bus transport, stays as-is
- The HTTP endpoints — they stay for backward compatibility
- The convergence chain engine — it produces results, the wire wrapping happens at the server layer

---

## Risks

1. **Over-engineering**: If we wrap everything in wire packets just for consistency, we add overhead without value. The wire format should only be used where traceability or cross-system communication matters.

2. **Payload bloat**: Wire packets have 7 fields of overhead. For a simple coaching signal, that's more metadata than content. Mitigation: only use wire format for signals that need tracing. Keep inline hints as plain text.

3. **Two serialization paths**: During migration, some responses will have both `coaching_signals` (old) and `coaching_packets` (new). Need a clean deprecation path.

---

## The Contract Question Answered

Mical asked: can the wire contract carry Enablement ↔ UX communication?

**Yes.** The wire contract is domain-agnostic by design. The `payload` and `output` fields carry any content. The structural fields (id, from, to, task, status, blockers, artifacts) provide exactly the traceability and routing that coaching needs.

The deeper answer: the wire contract should be the universal protocol for the entire system. Not because everything needs to be an agent — but because everything benefits from the same traceability, the same routing, and the same glass-box visibility.

**Palette knows what to do. Canvas does it. Enablement teaches how. The wire contract is how they talk to each other.**

---

## Recommended Next Step

Phase 1 only. Reshape coaching_signals to wire format in the convergence chain response. Verify that:
1. The UX still renders correctly
2. The enrichment pipeline can consume wire-shaped coaching events
3. The trace_id links coaching to the session

If Phase 1 works, Phase 2 follows naturally. If it doesn't, we learn why and adjust.

This is a 🔄 TWO-WAY DOOR — we can always revert to the current coaching_signals shape.

---

**End of proposal.**
