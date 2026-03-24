# Risk Gates v1

**Version**: 1.0.0
**Status**: ACCEPTED (2026-03-23)

---

## Purpose

The risk gates layer sits between the broker (transport) and the agents (execution). It classifies messages by risk and enforces governance rules. This is the policy layer — separate from the broker core.

## Gate Classification

When a message enters the broker, the risk gate evaluates it:

```
Message arrives
    │
    ▼
┌─────────────────┐
│ Risk Gate Check  │
│                  │
│ risk_level?      │
│ message_type?    │
│ from_agent tier? │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
  PASS      HOLD
  (deliver)  (waiting_human)
```

## Rules

### Rule 1: Critical risk requires human checkpoint
```
IF risk_level == "critical"
THEN state = "waiting_human"
     DO NOT deliver to recipient execution queue
     NOTIFY human via checkpoint mechanism
```

### Rule 2: One-way-door messages cannot auto-execute
```
IF message_type == "one_way_door"
THEN requires_ack = true (forced)
     state MUST pass through "waiting_human" before "executed"
```

### Rule 3: Unvalidated peers cannot request execution
```
IF from_agent.trust_tier == "UNVALIDATED"
AND message_type == "execution_request"
THEN REJECT with reason "unvalidated peers cannot request execution"
```

### Rule 4: High risk forces acknowledgment
```
IF risk_level == "high"
THEN requires_ack = true (forced)
```

### Rule 5: Expired messages are dead
```
IF created_at + ttl_seconds < now()
AND ttl_seconds > 0
THEN state = "expired"
     DO NOT deliver
     RETAIN in database for audit
```

## Human Checkpoint Mechanism

When a message is held at `waiting_human`:

1. Broker stores the message with `state: "waiting_human"`
2. Broker exposes it via `GET /checkpoints` (pending human decisions)
3. Human reviews via CLI: `palette-peers checkpoints`
4. Human approves or rejects: `palette-peers approve <message_id>` / `palette-peers reject <message_id> --reason "..."`
5. On approve: state transitions to `approved`, message delivered to recipient
6. On reject: state transitions to `rejected`, originating agent notified

## Audit Trail

Every risk gate evaluation is logged:

```json
{
  "message_id": "uuid",
  "gate_result": "pass | hold | reject",
  "rule_triggered": "rule_name | null",
  "evaluated_at": "ISO8601",
  "resolved_at": "ISO8601 | null",
  "resolved_by": "human | system | expired"
}
```

This log is append-only and stored in the same SQLite database as messages.

## Integration with Palette Decision Model

| Palette Concept | Peers Implementation |
|----------------|---------------------|
| 🚨 ONE-WAY DOOR | `message_type: "one_way_door"` + `risk_level: "critical"` |
| 🔄 TWO-WAY DOOR | `message_type: "execution_request"` carrying canonical `handoff_packet` + `risk_level: "low"` |
| Convergence Brief | `message_type: "proposal"` with semantic blueprint in payload |
| ASSUMPTION label | `message_type: "advisory"` + `risk_level: "medium"` |
| ⚠️ KNOWLEDGE GAP | `message_type: "human_checkpoint"` + research retrieval plan in payload |
