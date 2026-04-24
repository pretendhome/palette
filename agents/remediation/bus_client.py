"""
Shared bus client for the remediation loop agents.
Single source of truth for agent identities and bus communication.
"""
import json
import uuid
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BROKER_BASE = "http://127.0.0.1:7899"

# Canonical identity registry — the ONLY place agent routing is defined
AGENTS = {
    "validator": "validator.engine",
    "debugger":  "debugger.engine",
    "builder":   "builder.engine",
    "human":     "human.operator",
}

PALETTE_ROOT = Path(__file__).parent.parent.parent


def _post(path, body):
    req = urllib.request.Request(
        f"{BROKER_BASE}{path}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode())


def register(identity, capabilities, role):
    return _post("/register", {
        "identity": identity, "agent_name": identity.split(".")[0],
        "runtime": "python-script", "capabilities": capabilities,
        "palette_role": role, "trust_tier": "WORKING",
        "cwd": str(PALETTE_ROOT),
    })


def send(from_id, to_id, message_type, intent, payload,
         risk="none", thread_id=None, in_reply_to=None):
    msg_id = str(uuid.uuid4())
    envelope = {
        "protocol_version": "1.0.0", "message_id": msg_id,
        "thread_id": thread_id, "in_reply_to": in_reply_to,
        "from_agent": from_id, "to_agent": to_id,
        "message_type": message_type, "intent": intent,
        "risk_level": risk, "requires_ack": True,
        "payload": payload,
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "ttl_seconds": 3600,
    }
    result = _post("/send", envelope)
    return msg_id, result


def fetch(identity):
    return _post("/fetch", {"identity": identity})


def peek(identity):
    return _post("/peek", {"identity": identity})


def health():
    req = urllib.request.Request(f"{BROKER_BASE}/health")
    with urllib.request.urlopen(req, timeout=5) as resp:
        return json.loads(resp.read().decode())
