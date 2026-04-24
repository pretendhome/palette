#!/usr/bin/env python3
"""
Integration test: Remediation Loop Wire Test

Proves the loop works end-to-end:
  Validator → Debugger → Builder → Validator

Does NOT test agent domain logic (that's what the 91 unit tests do).
Tests ONLY that messages route to the correct agent identity on the bus.
"""
import sys
import json
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from bus_client import AGENTS, BROKER_BASE, health, peek, send, register

TIMEOUT = 10  # seconds to wait for message delivery


def bus_post(path, body):
    req = urllib.request.Request(
        f"{BROKER_BASE}{path}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode())


def has_pending(identity, from_agent=None):
    """Check if identity has pending messages, optionally from a specific sender."""
    data = peek(identity)
    msgs = data.get("messages", [])
    if from_agent:
        return any(m["from_agent"] == from_agent for m in msgs)
    return len(msgs) > 0


def drain(identity):
    """Consume all pending messages for an identity."""
    try:
        bus_post("/fetch", {"identity": identity})
    except Exception:
        pass


def main():
    print("=" * 60)
    print("REMEDIATION LOOP — WIRE INTEGRATION TEST")
    print("=" * 60)

    # Preflight
    h = health()
    assert h["status"] == "ok", f"Broker not healthy: {h}"
    print(f"\n✓ Broker healthy ({h['peers']} peers)")

    # Register all three agents
    for name, identity in AGENTS.items():
        if name == "human":
            continue
        try:
            register(identity, ["test"], "test")
        except Exception:
            pass
    print("✓ All agents registered")

    # Drain any stale messages
    for name, identity in AGENTS.items():
        if name != "human":
            drain(identity)
    print("✓ Inboxes drained")

    # === TEST 1: Validator → Debugger ===
    print("\n--- Test 1: Validator → Debugger wire ---")
    msg_id, result = send(
        AGENTS["validator"], AGENTS["debugger"],
        "execution_request",
        "WIRE TEST: Validator failure routed to Debugger",
        {"handoff_packet": {"id": "wire-test-1", "from": AGENTS["validator"],
                            "to": AGENTS["debugger"], "task": "diagnose test failure"}},
    )
    assert result.get("ok"), f"Send failed: {result}"
    assert has_pending(AGENTS["debugger"], from_agent=AGENTS["validator"]), \
        f"Message not found at {AGENTS['debugger']}"
    print(f"  ✓ Message {msg_id[:8]} arrived at debugger.engine")
    drain(AGENTS["debugger"])

    # === TEST 2: Debugger → Builder ===
    print("\n--- Test 2: Debugger → Builder wire ---")
    msg_id, result = send(
        AGENTS["debugger"], AGENTS["builder"],
        "proposal",
        "WIRE TEST: Debugger fix proposal routed to Builder",
        {"handoff_result": {"status": "fix_proposed", "next_agent": "builder",
                            "output": {"fix_proposal": {"file": "test.py", "line": 1,
                                                        "current": "x = 1", "fixed": "x = 2"}}}},
    )
    assert result.get("ok"), f"Send failed: {result}"
    assert has_pending(AGENTS["builder"], from_agent=AGENTS["debugger"]), \
        f"Message not found at {AGENTS['builder']}"
    print(f"  ✓ Message {msg_id[:8]} arrived at builder.engine")
    drain(AGENTS["builder"])

    # === TEST 3: Builder → Validator ===
    print("\n--- Test 3: Builder → Validator wire ---")
    msg_id, result = send(
        AGENTS["builder"], AGENTS["validator"],
        "execution_request",
        "WIRE TEST: Builder verification routed to Validator",
        {"handoff_packet": {"id": "wire-test-3", "from": AGENTS["builder"],
                            "to": AGENTS["validator"], "task": "verify applied patch"}},
    )
    assert result.get("ok"), f"Send failed: {result}"
    assert has_pending(AGENTS["validator"], from_agent=AGENTS["builder"]), \
        f"Message not found at {AGENTS['validator']}"
    print(f"  ✓ Message {msg_id[:8]} arrived at validator.engine")
    drain(AGENTS["validator"])

    # === TEST 4: Escalation → Human ===
    print("\n--- Test 4: Escalation → Human wire ---")
    msg_id, result = send(
        AGENTS["validator"], AGENTS["human"],
        "human_checkpoint",
        "WIRE TEST: Circuit breaker escalation to human",
        {"handoff_packet": {"id": "wire-test-4", "from": AGENTS["validator"],
                            "to": AGENTS["human"], "task": "manual review required"}},
        risk="high",
    )
    assert result.get("ok"), f"Send failed: {result}"
    assert has_pending(AGENTS["human"], from_agent=AGENTS["validator"]), \
        f"Message not found at {AGENTS['human']}"
    print(f"  ✓ Message {msg_id[:8]} arrived at human.operator")
    drain(AGENTS["human"])

    # === TEST 5: Full loop routing (no agent logic, just wire) ===
    print("\n--- Test 5: Full loop wire (V→D→B→V) ---")
    # V→D
    send(AGENTS["validator"], AGENTS["debugger"], "execution_request",
         "Loop step 1", {"handoff_packet": {"id": "loop", "from": "v", "to": "d", "task": "t"}})
    assert has_pending(AGENTS["debugger"])
    drain(AGENTS["debugger"])
    # D→B
    send(AGENTS["debugger"], AGENTS["builder"], "proposal",
         "Loop step 2", {"handoff_result": {"status": "fix_proposed", "next_agent": "builder", "output": {}}})
    assert has_pending(AGENTS["builder"])
    drain(AGENTS["builder"])
    # B→V
    send(AGENTS["builder"], AGENTS["validator"], "execution_request",
         "Loop step 3", {"handoff_packet": {"id": "loop", "from": "b", "to": "v", "task": "verify"}})
    assert has_pending(AGENTS["validator"])
    drain(AGENTS["validator"])
    print("  ✓ Full loop: validator → debugger → builder → validator — all wires connected")

    # === TEST 6: Identity registry is canonical ===
    print("\n--- Test 6: Identity registry check ---")
    assert AGENTS["validator"] == "validator.engine"
    assert AGENTS["debugger"] == "debugger.engine"
    assert AGENTS["builder"] == "builder.engine"
    assert AGENTS["human"] == "human.operator"
    print("  ✓ All identities match canonical registry")

    print("\n" + "=" * 60)
    print("✅ ALL 6 WIRE TESTS PASSED — LOOP IS CLOSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
