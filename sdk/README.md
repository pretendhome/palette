# Palette SDK — Machine Enablement Interface

The SDK is the machine half of Palette's Dual Enablement system. Where the human enablement coach teaches progressively over 7 stages, the SDK delivers the same knowledge as structured interfaces — all at once.

## 7-Stage Mapping

| Stage | Human Coach | SDK Interface | Method |
|-------|-------------|---------------|--------|
| 1. Foundations | "Here's what exists" | PIS data access | `agent.pis_data` |
| 2. First Instructions | "Here's how to ask" | Traversal queries | `agent.query_pis(riu_id=)` |
| 3. Memory | "Here's how to carry context" | HandoffPacket/Result | `agent.read_packet()` / `agent.emit_result()` |
| 4. Verification | "Here's how to check your work" | IntegrityGate | `agent.validate_output(result)` |
| 5. Organization | "Here's how it connects" | Relationship graph | `agent.query_graph(subject=, predicate=)` |
| 6. Building | "Here's how to create" | Execute protocol | `agent.execute(packet)` |
| 7. Autonomy | "Here's how to be independent" | Self-check | `agent.self_check()` |

## Quick Start

```python
from palette.sdk import AgentBase, HandoffPacket, HandoffResult

class MyResearcher(AgentBase):
    agent_name = "researcher"

    def execute(self, packet: HandoffPacket) -> HandoffResult:
        # Query the PIS for a specific RIU
        result = self.query_pis(riu_id="RIU-082")

        # Check what's connected in the relationship graph
        services = self.query_graph(subject="RIU-082", predicate="has_service")

        return HandoffResult(
            packet_id=packet.id,
            from_=self.agent_name,
            output={"recommendation": result.recommendation},
            blockers=result.blockers,
        )

# Run as stdin/stdout agent
if __name__ == "__main__":
    MyResearcher().run()
```

## Modules

### `agent_base.py`
- `PaletteContext` — loads all PIS data, integrity gate, and graph query
- `HandoffPacket` — structured input (wire: 7 fields)
- `HandoffResult` — structured output (wire: 7 fields)
- `AgentBase` — base class; subclass and implement `execute()`

### `integrity_gate.py`
- `IntegrityGate` — validates agent outputs against PIS data
- Checks: RIU references, service references, knowledge references, blockers/assumptions

### `graph_query.py`
- `GraphQuery` — queryable interface to the 1,800+ quad relationship graph
- Methods: `query(s, p, o)`, `objects_for()`, `subjects_for()`, `neighbors()`, `summary()`

## Error Handling

`PaletteContext.load()` never crashes. On failure:
- Logs the error to stderr
- Returns a context with `pis_data=None`
- `self_check()` reports "degraded" with specific issues

Agents decide how to handle degraded state:
```python
agent = MyAgent()
check = agent.self_check()
if check["status"] == "degraded":
    # Handle gracefully or halt
    print(check["issues"], file=sys.stderr)
```

## Running Tests

```bash
uv run pytest -q sdk/tests/           # 69 SDK tests
uv run pytest -q sdk/tests/ -v        # verbose output
```

## stdin/stdout Protocol

Agents communicate via JSON on stdin/stdout:

```bash
echo '{"task": "evaluate guardrails", "riu_ids": ["RIU-082"]}' | python3 my_agent.py
```

Output is a `HandoffResult` JSON with automatic integrity validation.
