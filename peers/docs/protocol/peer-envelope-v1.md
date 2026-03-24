# Peer Envelope v1 Protocol

**Version**: 1.0.0
**Status**: DRAFT → ACCEPTED (2026-03-23)
**Schema version field**: Required in every message (`protocol_version: "1.0.0"`)

---

## Envelope Schema

Every message on the Palette Peers bus uses this envelope:

```json
{
  "protocol_version": "1.0.0",
  "message_id": "uuid-v4",
  "thread_id": "uuid-v4 | null",
  "in_reply_to": "message_id | null",
  "from_agent": "agent_identity",
  "to_agent": "agent_identity",
  "message_type": "informational | advisory | proposal | execution_request | one_way_door | ack | human_checkpoint",
  "intent": "free-text summary of purpose",
  "risk_level": "none | low | medium | high | critical",
  "requires_ack": true,
  "payload": {},
  "created_at": "ISO8601",
  "ttl_seconds": 3600
}
```

## Field Definitions

### Identity Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `protocol_version` | string | yes | Semantic version of this protocol |
| `message_id` | uuid | yes | Unique identifier for this message |
| `thread_id` | uuid | no | Groups related messages into a conversation thread |
| `in_reply_to` | uuid | no | The `message_id` this message responds to |

### Routing Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `from_agent` | string | yes | Sender identity (e.g., `kiro.design`) |
| `to_agent` | string | yes | Recipient identity (e.g., `claude.analysis`) |

### Classification Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message_type` | enum | yes | See Message Types below |
| `intent` | string | yes | Human-readable purpose (1-2 sentences) |
| `risk_level` | enum | yes | See Risk Levels below |
| `requires_ack` | boolean | yes | Whether sender expects acknowledgment |

### Payload

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `payload` | object | yes | Message-type-specific content (see below) |

### Lifecycle

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `created_at` | ISO8601 | yes | When the message was created |
| `ttl_seconds` | integer | no | Time-to-live. Default: 3600 (1 hour). 0 = no expiry. |

---

## Message Types

### `informational`
Status updates, context sharing. No action required.
```json
{ "payload": { "content": "string" } }
```

### `advisory`
Recommendations or observations. Recipient may act or ignore.
```json
{ "payload": { "content": "string", "evidence": ["string"] } }
```

### `proposal`
A proposed action or decision. Expects a reply (accept/reject/modify).
```json
{
  "payload": {
    "content": "string",
    "proposed_action": "string",
    "alternatives": ["string"],
    "reversibility": "two_way_door | one_way_door"
  }
}
```

### `execution_request`
Request for a specific agent to perform work. Requires ack.
The canonical form embeds a Palette `HandoffPacket` so the peers bus does not create a second task wire contract.
```json
{
  "payload": {
    "handoff_packet": {
      "id": "uuid-v4",
      "from": "agent_identity",
      "to": "agent_identity",
      "task": "string",
      "riu_ids": ["RIU-123"],
      "payload": {},
      "trace_id": "string"
    },
    "acceptance_criteria": "string"
  }
}
```

Legacy compatibility:
- Older payloads with top-level `task`, `context`, `artifacts`, and `constraints` are still accepted during migration.
- New adapters should emit `payload.handoff_packet` using the canonical schema from [packet.schema.json](/home/mical/fde/palette/core/schema/packet.schema.json).

### `one_way_door`
A decision that is irreversible or high-cost to undo. **Cannot auto-execute.** Must transition through human checkpoint.
```json
{
  "payload": {
    "decision": "string",
    "rationale": "string",
    "impact": "string",
    "rollback_cost": "string",
    "state": "draft | proposed | waiting_human | approved | rejected | executed"
  }
}
```

### `ack`
Acknowledgment of a received message.
```json
{
  "payload": {
    "acked_message_id": "uuid",
    "status": "received | accepted | rejected | deferred",
    "reason": "string | null"
  }
}
```

### `human_checkpoint`
Explicit request for human review before proceeding.
```json
{
  "payload": {
    "decision_context": "string",
    "options": ["string"],
    "recommendation": "string | null",
    "blocking": true
  }
}
```

---

## Risk Levels

| Level | Meaning | Protocol Behavior |
|-------|---------|-------------------|
| `none` | No risk | Normal delivery |
| `low` | Easily reversible | Normal delivery |
| `medium` | Reversible with effort | Delivery + log |
| `high` | Difficult to reverse | Delivery + log + requires_ack forced true |
| `critical` | Irreversible | Delivery + log + human_checkpoint required before execution |

When `risk_level` is `critical`, the broker MUST NOT deliver to the recipient's execution queue. It MUST hold the message in `waiting_human` state until a human checkpoint clears it.

---

## State Machine: One-Way Door Messages

```
draft ──> proposed ──> waiting_human ──> approved ──> executed
                              │
                              └──> rejected
```

- `draft`: Agent is composing the decision
- `proposed`: Sent to the bus, visible to all relevant peers
- `waiting_human`: Blocked until human approves or rejects
- `approved`: Human cleared it, execution may proceed
- `rejected`: Human rejected it, originating agent must acknowledge
- `executed`: Action was taken (terminal state)

---

## Validation Rules

1. `protocol_version` MUST be present and MUST match a supported version
2. `message_id` MUST be a valid UUID v4
3. `from_agent` MUST match a registered peer identity, except reserved local operator identities such as `human.operator` and `system.broker`
4. `to_agent` MAY target an unregistered identity for store-and-forward delivery
5. `message_type` MUST be one of the defined enum values
6. `risk_level: critical` MUST have `message_type: one_way_door` or `human_checkpoint`
7. `one_way_door` messages MUST include `state` in payload
8. `ack` messages MUST include `acked_message_id` referencing an existing message
9. `ttl_seconds` of 0 means the message never expires
10. Expired messages (created_at + ttl_seconds < now) SHOULD be marked dead but NOT deleted

---

## Wire Format

JSON over HTTP POST. Content-Type: application/json. All timestamps ISO8601 UTC.
