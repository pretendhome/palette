#!/usr/bin/env python3
"""Self-contained integration tests for Palette Peers broker."""
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def new_iso():
    return datetime.now(timezone.utc).isoformat()

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent
PORT = int(os.environ.get("PALETTE_PEERS_TEST_PORT", "17899"))
BASE = f"http://127.0.0.1:{PORT}"


def post(path, data):
    req = urllib.request.Request(
        f"{BASE}{path}",
        json.dumps(data).encode(),
        {"Content-Type": "application/json"},
    )
    try:
        return json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as exc:
        return json.loads(exc.read())


def get(path):
    return json.loads(urllib.request.urlopen(f"{BASE}{path}").read())


def load_fixture(name):
    with open(FIXTURES / name, encoding="utf-8") as handle:
        return json.load(handle)["envelope"]


def check(name, ok, detail=""):
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name} {detail}".rstrip())
    return 1 if ok else 0


def wait_for_broker():
    deadline = time.time() + 10
    last_error = None
    while time.time() < deadline:
        try:
            data = get("/health")
            if data.get("status") == "ok":
                return
        except Exception as exc:  # noqa: BLE001
            last_error = exc
        time.sleep(0.2)
    raise RuntimeError(f"broker did not become healthy: {last_error}")


def register_peers():
    peers = [
        {
            "identity": "kiro.design",
            "agent_name": "kiro",
            "runtime": "kiro-cli",
            "pid": 1,
            "capabilities": ["architecture"],
            "trust_tier": "WORKING",
            "version": "1.0.0",
        },
        {
            "identity": "claude.analysis",
            "agent_name": "claude",
            "runtime": "claude",
            "pid": 2,
            "capabilities": ["debugging"],
            "trust_tier": "WORKING",
            "version": "1.0.0",
        },
        {
            "identity": "codex.implementation",
            "agent_name": "codex",
            "runtime": "codex",
            "pid": 3,
            "capabilities": ["code_generation"],
            "trust_tier": "UNVALIDATED",
            "version": "1.0.0",
        },
        {
            "identity": "perplexity.research",
            "agent_name": "perplexity",
            "runtime": "api",
            "capabilities": ["deep_research"],
            "trust_tier": "WORKING",
            "version": "1.0.0",
        },
    ]
    for peer in peers:
        result = post("/register", peer)
        if not result.get("ok"):
            raise RuntimeError(f"failed to register peer: {peer['identity']} {result}")


def main():
    passed = 0
    total = 0

    with tempfile.TemporaryDirectory(prefix="palette-peers-") as temp_dir:
        db_path = os.path.join(temp_dir, "palette-peers.db")
        env = os.environ.copy()
        env["PALETTE_PEERS_PORT"] = str(PORT)
        env["PALETTE_PEERS_DB"] = db_path
        broker = subprocess.Popen(
            ["node", "broker/index.mjs"],
            cwd=ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            wait_for_broker()
            register_peers()

            total += 1
            d = post("/send", load_fixture("informational.json"))
            passed += check("Informational (pass)", d.get("gate") == "pass", f"gate={d.get('gate')}")

            total += 1
            d = post("/send", load_fixture("one_way_door.json"))
            passed += check(
                "One-Way-Door (hold)",
                d.get("gate") == "hold" and d.get("state") == "waiting_human",
                f"gate={d.get('gate')} state={d.get('state')}",
            )

            total += 1
            d = post("/send", load_fixture("execution_request.json"))
            passed += check("Exec WORKING (pass)", d.get("gate") == "pass", f"gate={d.get('gate')}")

            total += 1
            d = post("/send", load_fixture("rejected_unvalidated.json"))
            passed += check(
                "Exec UNVALIDATED (reject)",
                d.get("gate") == "reject",
                f"gate={d.get('gate')} reason={d.get('reason')}",
            )

            total += 1
            d = get("/checkpoints")
            pending = len(d.get("checkpoints", []))
            passed += check("Checkpoints (1 pending)", pending == 1, f"pending={pending}")

            total += 1
            d = post("/approve", {"message_id": "f1e2d3c4-b5a6-4978-8d7c-6e5f4a3b2c1d"})
            approved = d.get("ok") and d.get("state") == "approved"
            fetched = post("/fetch", {"identity": "kiro.design"}).get("messages", [])
            passed += check(
                "Approve+Fetch",
                approved and len(fetched) >= 1,
                f"approved={approved} fetched={len(fetched)} types={[m['message_type'] for m in fetched]}",
            )

            total += 1
            d = post(
                "/send",
                {
                    "protocol_version": "1.0.0",
                    "message_id": "d4e5f6a7-b8c9-4d0e-8f1a-2b3c4d5e6f7a",
                    "thread_id": None,
                    "in_reply_to": None,
                    "from_agent": "claude.analysis",
                    "to_agent": "future.peer",
                    "message_type": "informational",
                    "intent": "Queue message for a peer that has not registered yet",
                    "risk_level": "none",
                    "requires_ack": False,
                    "payload": {"content": "store-and-forward smoke test"},
                    "created_at": new_iso(),
                    "ttl_seconds": 3600,
                },
            )
            store_and_forward_sent = d.get("gate") == "pass"
            register_result = post(
                "/register",
                {
                    "identity": "future.peer",
                    "agent_name": "future",
                    "runtime": "test",
                    "trust_tier": "WORKING",
                    "version": "1.0.0",
                },
            )
            future_msgs = post("/fetch", {"identity": "future.peer"}).get("messages", [])
            passed += check(
                "Unregistered recipient store-and-forward",
                store_and_forward_sent and register_result.get("ok") and len(future_msgs) == 1,
                f"sent={store_and_forward_sent} registered={register_result.get('ok')} fetched={len(future_msgs)}",
            )

            # --- Test 8: TTL expiry ---
            total += 1
            expired_id = "e8f9a0b1-c2d3-4e5f-6a7b-8c9d0e1f2a3b"
            # Send a message with 1-second TTL, using a timestamp 10 seconds in the past
            past_time = "2020-01-01T00:00:00.000Z"
            d = post(
                "/send",
                {
                    "protocol_version": "1.0.0",
                    "message_id": expired_id,
                    "thread_id": None,
                    "in_reply_to": None,
                    "from_agent": "kiro.design",
                    "to_agent": "claude.analysis",
                    "message_type": "informational",
                    "intent": "This message should expire before delivery",
                    "risk_level": "none",
                    "requires_ack": False,
                    "payload": {"content": "should be expired"},
                    "created_at": past_time,
                    "ttl_seconds": 1,
                },
            )
            ttl_sent = d.get("gate") == "pass"
            # Fetch should NOT return the expired message
            fetched_msgs = post("/fetch", {"identity": "claude.analysis"}).get("messages", [])
            expired_in_result = any(m.get("message_id") == expired_id for m in fetched_msgs)
            passed += check(
                "TTL expiry (not delivered)",
                ttl_sent and not expired_in_result,
                f"sent={ttl_sent} expired_in_result={expired_in_result} fetched={len(fetched_msgs)}",
            )

            # --- Test 9: Ack flow ---
            total += 1
            ack_msg_id = "f9a0b1c2-d3e4-4f5a-6b7c-8d9e0f1a2b3c"
            d = post(
                "/send",
                {
                    "protocol_version": "1.0.0",
                    "message_id": ack_msg_id,
                    "thread_id": None,
                    "in_reply_to": None,
                    "from_agent": "kiro.design",
                    "to_agent": "perplexity.research",
                    "message_type": "informational",
                    "intent": "Message to test ack flow",
                    "risk_level": "none",
                    "requires_ack": True,
                    "payload": {"content": "please ack this"},
                    "created_at": new_iso(),
                    "ttl_seconds": 3600,
                },
            )
            ack_sent = d.get("gate") == "pass"
            # Fetch to deliver it
            post("/fetch", {"identity": "perplexity.research"})
            # Send ack
            ack_result = post("/ack", {"message_id": ack_msg_id})
            ack_ok = ack_result.get("ok", False)
            passed += check(
                "Ack flow",
                ack_sent and ack_ok,
                f"sent={ack_sent} acked={ack_ok}",
            )

            # --- Test 10: Thread retrieval ---
            total += 1
            thread_uuid = "11111111-2222-4333-a444-555555555555"
            msg1_id = "a1111111-b222-4c33-d444-e55555555551"
            msg2_id = "a1111111-b222-4c33-d444-e55555555552"
            for mid, from_a, to_a, intent in [
                (msg1_id, "kiro.design", "claude.analysis", "Thread msg 1"),
                (msg2_id, "claude.analysis", "kiro.design", "Thread msg 2 reply"),
            ]:
                post(
                    "/send",
                    {
                        "protocol_version": "1.0.0",
                        "message_id": mid,
                        "thread_id": thread_uuid,
                        "in_reply_to": msg1_id if mid == msg2_id else None,
                        "from_agent": from_a,
                        "to_agent": to_a,
                        "message_type": "informational",
                        "intent": intent,
                        "risk_level": "none",
                        "requires_ack": False,
                        "payload": {"content": intent},
                        "created_at": new_iso(),
                        "ttl_seconds": 3600,
                    },
                )
            thread_result = post("/thread", {"thread_id": thread_uuid})
            thread_msgs = thread_result.get("messages", [])
            passed += check(
                "Thread retrieval (2 messages)",
                len(thread_msgs) == 2,
                f"thread_msgs={len(thread_msgs)}",
            )

            # --- Test 11: Reject held message ---
            total += 1
            reject_msg_id = "b2222222-c333-4d44-e555-f66666666666"
            post(
                "/send",
                {
                    "protocol_version": "1.0.0",
                    "message_id": reject_msg_id,
                    "thread_id": None,
                    "in_reply_to": None,
                    "from_agent": "kiro.design",
                    "to_agent": "claude.analysis",
                    "message_type": "one_way_door",
                    "intent": "Test rejection flow",
                    "risk_level": "critical",
                    "requires_ack": True,
                    "payload": {
                        "decision": "Test reject",
                        "rationale": "Testing",
                        "impact": "None",
                        "rollback_cost": "None",
                        "state": "proposed",
                    },
                    "created_at": new_iso(),
                    "ttl_seconds": 0,
                },
            )
            reject_result = post("/reject", {"message_id": reject_msg_id, "reason": "test rejection"})
            rejected_ok = reject_result.get("ok") and reject_result.get("state") == "rejected"
            # Verify rejected message is NOT fetchable
            fetch_after_reject = post("/fetch", {"identity": "claude.analysis"}).get("messages", [])
            rejected_in_fetch = any(m.get("message_id") == reject_msg_id for m in fetch_after_reject)
            passed += check(
                "Reject flow (not delivered)",
                rejected_ok and not rejected_in_fetch,
                f"rejected={rejected_ok} in_fetch={rejected_in_fetch}",
            )

            print(f"\n{passed}/{total} passed")
            return 0 if passed == total else 1
        finally:
            broker.terminate()
            try:
                broker.wait(timeout=5)
            except subprocess.TimeoutExpired:
                broker.kill()
                broker.wait(timeout=5)
            stderr = broker.stderr.read().strip()
            if stderr:
                print("\n[broker stderr]")
                print(stderr)


if __name__ == "__main__":
    sys.exit(main())
