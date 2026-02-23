#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from relay_store import TelegramRelayStore


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize per-implementation Telegram relay folders")
    parser.add_argument("--impl-id", required=True, help="Implementation folder name under implementations/")
    parser.add_argument(
        "--implementations-root",
        default="/home/mical/fde/implementations",
        help="Path to implementations root (default: /home/mical/fde/implementations)",
    )
    args = parser.parse_args()

    root = Path(args.implementations_root)
    if not root.exists():
        parser.error(f"implementations root not found: {root}")

    store = TelegramRelayStore(root, args.impl_id)
    store.ensure_layout()
    store.update_state(
        status_lines=[
            "- Relay: active",
            "- Telegram bridge: pending integration hook",
            "- Direct shell from Telegram: disabled",
            "- Repo mutation: approval required",
        ],
        queue_counts={"Inbox pending": 0, "Outbox pending": 0, "Failed": 0},
        last_processed={},
        notes=[
            "Scaffold initialized by relay_scaffold.py",
            "Next: wire bridge to append events and create request artifacts for allowlisted intents",
        ],
    )

    print(f"Initialized relay scaffold: {store.paths.base}")
    for p in [store.paths.events, store.paths.sessions, store.paths.inbox, store.paths.outbox, store.paths.archive]:
        print(f"- {p}")
    print(f"- {store.paths.state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

