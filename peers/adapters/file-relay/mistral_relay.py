#!/usr/bin/env python3
"""
Palette Peers — File Relay for Mistral Vibe

Bridges Mistral (Le Chat) into the Palette Peers message bus via filesystem.
Mistral writes markdown files to OUTBOX; this relay posts them to the broker.
Broker messages for Mistral get written as markdown to INBOX.

Usage:
    python3 mistral_relay.py                    # run once (fetch + send)
    python3 mistral_relay.py --watch            # poll every 30s
    python3 mistral_relay.py --watch --interval 10  # poll every 10s
"""

import argparse
import json
import os
import re
import shutil
import sys
import time
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

BROKER_BASE = "http://127.0.0.1:7899"
IDENTITY = "mistral-vibe.builder"
AGENT_NAME = "mistral-vibe"
RUNTIME = "file-relay"
CAPABILITIES = ["content_generation", "exercise_design", "documentation"]
ROLE = "builder"
TRUST_TIER = "WORKING"

# Paths
ENABLEMENT_DIR = Path(__file__).resolve().parents[4] / "enablement"
INBOX = ENABLEMENT_DIR / "MISTRAL_INBOX"
OUTBOX = ENABLEMENT_DIR / "MISTRAL_OUTBOX"
SENT = OUTBOX / "sent"
RELAY_LOG = INBOX / ".relay_log"
SEEN_IDS = INBOX / ".seen_ids"


def broker_post(path, body):
    """POST JSON to the broker."""
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        f"{BROKER_BASE}{path}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e)}


def broker_get(path):
    """GET from the broker."""
    try:
        with urllib.request.urlopen(f"{BROKER_BASE}{path}", timeout=10) as resp:
            return json.loads(resp.read())
    except Exception as e:
        return {"error": str(e)}


def log(msg):
    """Print and append to relay log."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    line = f"[{ts}] {msg}"
    print(line)
    with open(RELAY_LOG, "a") as f:
        f.write(line + "\n")


def register():
    """Register Mistral on the broker."""
    result = broker_post("/register", {
        "identity": IDENTITY,
        "agent_name": AGENT_NAME,
        "runtime": RUNTIME,
        # File-relay may run as short-lived polling cycles, so a process PID is not
        # a stable liveness signal for peer visibility on the bus.
        "pid": None,
        "cwd": str(ENABLEMENT_DIR),
        "git_root": str(ENABLEMENT_DIR),
        "capabilities": CAPABILITIES,
        "palette_role": ROLE,
        "trust_tier": TRUST_TIER,
        "version": "1.0.0",
    })
    if "error" in result:
        log(f"Registration failed: {result['error']}")
        return False
    log(f"Registered as {IDENTITY}")
    return True


def heartbeat():
    """Send heartbeat to broker."""
    broker_post("/heartbeat", {"identity": IDENTITY})


def load_seen_ids():
    """Load set of already-processed message IDs (for broadcast dedup)."""
    if SEEN_IDS.exists():
        return set(SEEN_IDS.read_text().strip().splitlines())
    return set()


def save_seen_id(msg_id):
    """Append a message ID to the seen set."""
    with open(SEEN_IDS, "a") as f:
        f.write(msg_id + "\n")


def fetch_messages():
    """Fetch pending messages for Mistral and write them to INBOX."""
    result = broker_post("/fetch", {"identity": IDENTITY})
    messages = result.get("messages", [])
    if not messages:
        return 0

    seen = load_seen_ids()
    for msg in messages:
        msg_id = msg.get("message_id", "unknown")
        if msg_id in seen:
            continue
        from_agent = msg.get("from_agent", "unknown")
        intent = msg.get("intent", "no intent")
        msg_type = msg.get("message_type", "unknown")
        risk = msg.get("risk_level", "none")
        thread = msg.get("thread_id", "")
        created = msg.get("created_at", "")
        payload = msg.get("payload", {})

        # Format payload as readable text
        if isinstance(payload, dict):
            payload_lines = []
            for k, v in payload.items():
                if isinstance(v, (list, dict)):
                    payload_lines.append(f"**{k}**:")
                    payload_lines.append(f"```\n{json.dumps(v, indent=2)}\n```")
                else:
                    payload_lines.append(f"**{k}**: {v}")
            payload_text = "\n".join(payload_lines)
        else:
            payload_text = str(payload)

        # Write to INBOX
        safe_from = from_agent.replace(".", "-")
        ts = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        filename = f"{ts}_{safe_from}_{msg_id[:8]}.md"
        filepath = INBOX / filename

        content = f"""# Message from {from_agent}

**Type**: {msg_type}
**Intent**: {intent}
**Risk**: {risk}
**Message ID**: {msg_id}
**Thread**: {thread or "none"}
**Created**: {created}

---

{payload_text}
"""
        filepath.write_text(content)
        save_seen_id(msg_id)
        log(f"INBOX <- {from_agent}: {intent} ({filename})")

    return len(messages)


def parse_outbox_file(filepath):
    """Parse a markdown file with YAML-like frontmatter into a bus message."""
    text = filepath.read_text()

    # Extract frontmatter between --- delimiters
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not fm_match:
        return None, "No frontmatter found (expected --- delimiters)"

    frontmatter_text = fm_match.group(1)
    body = fm_match.group(2).strip()

    # Parse simple key: value frontmatter (no full YAML parser needed)
    meta = {}
    for line in frontmatter_text.strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip('"').strip("'")

    # Validate required fields
    to_agent = meta.get("to")
    if not to_agent:
        return None, "Missing 'to' field in frontmatter"

    intent = meta.get("intent", "Message from Mistral Vibe")
    msg_type = meta.get("type", "informational")
    risk = meta.get("risk", "none")
    thread_id = meta.get("thread") or None
    in_reply_to = meta.get("in_reply_to") or None

    envelope = {
        "protocol_version": "1.0.0",
        "message_id": str(uuid.uuid4()),
        "thread_id": thread_id,
        "in_reply_to": in_reply_to,
        "from_agent": IDENTITY,
        "to_agent": to_agent,
        "message_type": msg_type,
        "intent": intent,
        "risk_level": risk,
        "requires_ack": False,
        "payload": {"content": body},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "ttl_seconds": 604800,
    }
    return envelope, None


def parse_adhoc_file(filepath):
    """Parse an ad-hoc Mistral file (MISTRAL_TO_*.md, MISTRAL_REPLY*.md) into a bus message.
    These files don't have frontmatter — just plain content. We wrap them as
    informational messages to claude.analysis."""
    text = filepath.read_text().strip()
    if not text:
        return None, "Empty file"

    # Guess intent from filename
    name = filepath.stem
    if "reply" in name.lower():
        intent = "Reply from Mistral Vibe"
    elif "to_claude" in name.lower():
        intent = "Message from Mistral Vibe to Claude"
    elif "to_codex" in name.lower():
        intent = "Message from Mistral Vibe to Codex"
    else:
        intent = f"Message from Mistral Vibe ({name})"

    # Guess recipient
    to_agent = "claude.analysis"
    if "codex" in name.lower():
        to_agent = "codex.implementation"
    elif "kiro" in name.lower():
        to_agent = "kiro.design"

    envelope = {
        "protocol_version": "1.0.0",
        "message_id": str(uuid.uuid4()),
        "thread_id": None,
        "in_reply_to": None,
        "from_agent": IDENTITY,
        "to_agent": to_agent,
        "message_type": "informational",
        "intent": intent,
        "risk_level": "none",
        "requires_ack": False,
        "payload": {"content": text},
        "created_at": datetime.now(timezone.utc).isoformat(),
        "ttl_seconds": 604800,
    }
    return envelope, None


def send_outbox():
    """Process outbox files and ad-hoc Mistral files, send to broker."""
    sent_count = 0

    # 1. Check formal OUTBOX (frontmatter format)
    for filepath in sorted(OUTBOX.glob("*.md")):
        if filepath.name.startswith("."):
            continue

        envelope, error = parse_outbox_file(filepath)
        if error:
            log(f"OUTBOX SKIP {filepath.name}: {error}")
            continue

        result = broker_post("/send", envelope)
        if result.get("ok"):
            log(f"OUTBOX -> {envelope['to_agent']}: {envelope['intent']} ({filepath.name})")
            # Move to sent/
            shutil.move(str(filepath), str(SENT / filepath.name))
            sent_count += 1
        else:
            log(f"OUTBOX FAIL {filepath.name}: {json.dumps(result)}")

    # 2. Check ad-hoc files (MISTRAL_TO_*.md, MISTRAL_REPLY*.md)
    adhoc_patterns = ["MISTRAL_TO_*.md", "MISTRAL_REPLY*.md"]
    for pattern in adhoc_patterns:
        for filepath in sorted(ENABLEMENT_DIR.glob(pattern)):
            # Skip if already processed (check relay log)
            if RELAY_LOG.exists():
                log_content = RELAY_LOG.read_text()
                if filepath.name in log_content:
                    continue

            envelope, error = parse_adhoc_file(filepath)
            if error:
                log(f"ADHOC SKIP {filepath.name}: {error}")
                continue

            result = broker_post("/send", envelope)
            if result.get("ok"):
                log(f"ADHOC -> {envelope['to_agent']}: {envelope['intent']} ({filepath.name})")
                sent_count += 1
            else:
                log(f"ADHOC FAIL {filepath.name}: {json.dumps(result)}")

    return sent_count


def run_once():
    """Single fetch + send cycle."""
    register()
    heartbeat()
    fetched = fetch_messages()
    sent = send_outbox()
    log(f"Cycle complete: {fetched} fetched, {sent} sent")
    return fetched, sent


def run_watch(interval):
    """Polling loop."""
    log(f"Watch mode started (interval: {interval}s)")
    register()
    cycle = 0
    try:
        while True:
            cycle += 1
            fetched = fetch_messages()
            sent = send_outbox()
            if fetched or sent:
                log(f"Cycle {cycle}: {fetched} fetched, {sent} sent")
            heartbeat()
            time.sleep(interval)
    except KeyboardInterrupt:
        log("Watch mode stopped (Ctrl-C)")


def main():
    parser = argparse.ArgumentParser(
        description="Palette Peers file relay for Mistral Vibe"
    )
    parser.add_argument(
        "--watch", action="store_true", help="Poll continuously"
    )
    parser.add_argument(
        "--interval", type=int, default=30, help="Poll interval in seconds (default: 30)"
    )
    args = parser.parse_args()

    # Ensure directories exist
    INBOX.mkdir(parents=True, exist_ok=True)
    OUTBOX.mkdir(parents=True, exist_ok=True)
    SENT.mkdir(parents=True, exist_ok=True)

    if args.watch:
        run_watch(args.interval)
    else:
        run_once()


if __name__ == "__main__":
    main()
