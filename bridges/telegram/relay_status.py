#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from relay_consumer import parse_frontmatter_md
from relay_store import TelegramRelayStore


def latest_files(path: Path, pattern: str = "*.md", limit: int = 3) -> list[Path]:
    return sorted(path.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)[:limit]


def read_event_tail(events_dir: Path, n: int = 5) -> list[dict[str, Any]]:
    files = sorted(events_dir.glob("*.jsonl"))
    if not files:
        return []
    rows: list[dict[str, Any]] = []
    for file in reversed(files[-3:]):
        try:
            with open(file, "r", encoding="utf-8") as f:
                lines = [ln for ln in f.read().splitlines() if ln.strip()]
        except OSError:
            continue
        for ln in reversed(lines):
            try:
                rows.append(json.loads(ln))
            except json.JSONDecodeError:
                continue
            if len(rows) >= n:
                return rows
    return rows


def summarize_artifact(path: Path) -> str:
    try:
        fm, _ = parse_frontmatter_md(path)
    except Exception:
        return f"{path.name} (unreadable)"
    bits = [path.name]
    if "intent" in fm:
        bits.append(f"intent={fm.get('intent')}")
    if "status" in fm:
        bits.append(f"status={fm.get('status')}")
    if "delivery_status" in fm:
        bits.append(f"delivery={fm.get('delivery_status')}")
    if "publish_to_github_approved" in fm:
        bits.append(f"publish_approved={fm.get('publish_to_github_approved')}")
    return " | ".join(bits)


def systemd_status(service_name: str) -> str:
    try:
        proc = subprocess.run(
            ["systemctl", "is-active", service_name],
            capture_output=True,
            text=True,
            check=False,
            timeout=3,
        )
        state = (proc.stdout or proc.stderr).strip() or "unknown"
        return state
    except Exception:
        return "unavailable"


def main() -> int:
    parser = argparse.ArgumentParser(description="Show Telegram relay pipeline status for an implementation")
    parser.add_argument("--impl-id", required=True)
    parser.add_argument("--implementations-root", default="/home/mical/fde/implementations")
    parser.add_argument("--check-systemd", action="store_true", help="Check Rossi systemd service active state")
    args = parser.parse_args()

    store = TelegramRelayStore(args.implementations_root, args.impl_id)
    store.ensure_layout()
    base = store.paths.base

    inbox = sorted(store.paths.inbox.glob("*.md"))
    outbox = sorted(store.paths.outbox.glob("*.md"))
    archived_processed = sorted((store.paths.archive / "processed").glob("*.md")) if (store.paths.archive / "processed").exists() else []
    archived_failed = sorted((store.paths.archive / "failed").glob("*.md")) if (store.paths.archive / "failed").exists() else []

    print(f"Relay Status: {args.impl_id}")
    print(f"Path: {base}")
    print("")
    print("Queues")
    print(f"- Inbox pending: {len(inbox)}")
    print(f"- Outbox pending/retained: {len(outbox)}")
    print(f"- Archive processed: {len(archived_processed)}")
    print(f"- Archive failed: {len(archived_failed)}")

    print("")
    print("Latest Artifacts")
    for label, path in [
        ("Inbox", store.paths.inbox),
        ("Outbox", store.paths.outbox),
        ("Processed", store.paths.archive / "processed"),
        ("Failed", store.paths.archive / "failed"),
        ("Sessions", store.paths.sessions),
    ]:
        print(f"- {label}:")
        files = latest_files(path) if path.exists() else []
        if not files:
            print("  - none")
            continue
        for f in files:
            print(f"  - {summarize_artifact(f)}")

    print("")
    print("Recent Events")
    rows = read_event_tail(store.paths.events, n=8)
    if not rows:
        print("- none")
    else:
        for row in rows:
            print(
                "- {ts} | {source} | {status} | {intent}".format(
                    ts=row.get("ts", ""),
                    source=row.get("source", ""),
                    status=row.get("status", ""),
                    intent=row.get("intent", row.get("direction", "")),
                )
            )

    if args.check_systemd and args.impl_id == "retail-rossi-store":
        print("")
        print("systemd")
        print(f"- rossi-relay-consumer.service: {systemd_status('rossi-relay-consumer.service')}")
        print(f"- rossi-outbox-deliver.service: {systemd_status('rossi-outbox-deliver.service')}")

    print("")
    print("Files")
    print(f"- STATE.md: {store.paths.state}")
    print(f"- Events dir: {store.paths.events}")
    print(f"- Inbox dir: {store.paths.inbox}")
    print(f"- Outbox dir: {store.paths.outbox}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

