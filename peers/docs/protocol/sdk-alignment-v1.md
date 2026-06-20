# Peers / SDK Alignment v1

## Purpose

Prevent `palette/peers` from drifting into a second task wire contract.

## Rule

`palette/peers` is a transport envelope.
It is not a replacement for the canonical Palette agent contract.

The canonical intra-agent work unit remains:

- `HandoffPacket`: `id`, `from`, `to`, `task`, `riu_ids`, `payload`, `trace_id`
- `HandoffResult`: `packet_id`, `from`, `status`, `output`, `blockers`, `artifacts`, `next_agent`

Source of truth:

- [packet.schema.json](/home/mical/fde/palette/core/schema/packet.schema.json)
- [result.schema.json](/home/mical/fde/palette/core/schema/result.schema.json)
- [agent_base.py](/home/mical/fde/palette/sdk/agent_base.py)

## Mapping

When a peer wants another peer to perform work:

- Outer envelope uses `message_type: "execution_request"`
- `payload.handoff_packet` carries the canonical `HandoffPacket`
- Any transport-specific review criteria remain alongside it, for example `acceptance_criteria`

Example:

```json
{
  "message_type": "execution_request",
  "payload": {
    "handoff_packet": {
      "id": "uuid-v4",
      "from": "claude.analysis",
      "to": "perplexity.research",
      "task": "Research MCP support",
      "riu_ids": ["RIU-024"],
      "payload": {
        "context": "Palette peers compatibility study"
      },
      "trace_id": "trace-123"
    },
    "acceptance_criteria": "Structured findings with confidence notes"
  }
}
```

## Compatibility

The broker still accepts the older `execution_request` payload shape with top-level:

- `task`
- `context`
- `artifacts`
- `constraints`

That support is transitional. New adapters should emit `payload.handoff_packet`.
