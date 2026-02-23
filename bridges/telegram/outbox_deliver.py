#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import time
from pathlib import Path

import httpx

from relay_consumer import parse_frontmatter_md
from relay_store import TelegramRelayStore, atomic_write_text, iso_z, sanitize_text


def parse_chat_id(delivery_target: str) -> int:
    target = delivery_target.strip()
    if target.startswith("telegram:"):
        target = target.split(":", 1)[1]
    return int(target)


def tg_send(bot_token: str, chat_id: int, text: str) -> dict:
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    with httpx.Client(timeout=30.0) as client:
        return client.post(url, json={"chat_id": chat_id, "text": text}).json()


def _scalar_text(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "" or re.search(r"[:#\n]", text) or text.strip() != text:
        return json.dumps(text)
    return text


def patch_top_level_frontmatter(path: Path, updates: dict) -> None:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        raise ValueError(f"Missing frontmatter: {path}")
    parts = raw.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"Malformed frontmatter: {path}")
    fm_lines = parts[1].splitlines()
    body = parts[2].lstrip("\n")

    remaining = dict(updates)
    out_lines: list[str] = []
    for line in fm_lines:
        if not line.strip():
            out_lines.append(line)
            continue
        if line.startswith(" ") or line.startswith("\t"):
            out_lines.append(line)
            continue
        if ":" not in line:
            out_lines.append(line)
            continue
        key = line.split(":", 1)[0].strip()
        if key in remaining:
            out_lines.append(f"{key}: {_scalar_text(remaining.pop(key))}")
        else:
            out_lines.append(line)
    for key, value in remaining.items():
        out_lines.append(f"{key}: {_scalar_text(value)}")

    patched = "---\n" + "\n".join(out_lines).rstrip() + "\n---\n" + body
    if not patched.endswith("\n"):
        patched += "\n"
    atomic_write_text(path, patched)


def make_delivery_text(fm: dict, body: str) -> str:
    intent = str(fm.get("intent", "unknown"))
    trace_id = str(fm.get("trace_id", ""))
    content = body.strip()
    if content.startswith("## Response"):
        content = content[len("## Response") :].lstrip()
    text = f"[relay:{intent}] {content}"
    if trace_id:
        text += f"\n\ntrace: {trace_id}"
    return sanitize_text(text)


def deliver_one(store: TelegramRelayStore, path: Path, bot_token: str, *, dry_run: bool = False) -> tuple[str, str]:
    fm, body = parse_frontmatter_md(path)
    trace_id = str(fm.get("trace_id", "")) or store.new_trace_id("deliver")
    delivery_channel = str(fm.get("delivery_channel", "")).strip()
    delivery_target = str(fm.get("delivery_target", "")).strip()
    delivery_status = str(fm.get("delivery_status", "")).strip()

    if delivery_channel != "telegram":
        return ("skipped", f"delivery_channel={delivery_channel!r}")
    if delivery_status != "pending":
        return ("skipped", f"delivery_status={delivery_status!r}")
    if not delivery_target:
        return ("failed", "missing delivery_target")

    text = make_delivery_text(fm, body)
    if dry_run:
        result = {"ok": True, "result": {"message_id": 0}}
    else:
        result = tg_send(bot_token, parse_chat_id(delivery_target), text)

    if not result.get("ok"):
        patch_top_level_frontmatter(
            path,
            {
                "delivery_status": "failed",
                "delivery_error": json.dumps(result, ensure_ascii=True)[:1000],
            },
        )
        store.append_event(
            {
                "trace_id": trace_id,
                "source": "outbox-deliver",
                "direction": "outbound",
                "status": "delivery_failed",
                "artifact_path": str(path),
                "delivery_target": delivery_target,
                "provenance": "outbox_deliver",
            }
        )
        return ("failed", "telegram send failed")

    patch_top_level_frontmatter(
        path,
        {
            "delivery_status": "sent" if not dry_run else "dry_run_sent",
            "delivery_sent_at": iso_z(),
            "delivery_message_id": int(result.get("result", {}).get("message_id", 0)),
        },
    )
    store.append_event(
        {
            "trace_id": trace_id,
            "source": "outbox-deliver",
            "direction": "outbound",
            "status": "delivery_sent" if not dry_run else "delivery_dry_run",
            "artifact_path": str(path),
            "delivery_target": delivery_target,
            "provenance": "outbox_deliver",
        }
    )
    return ("sent" if not dry_run else "dry-run", str(path))


def main() -> int:
    parser = argparse.ArgumentParser(description="Deliver relay outbox responses back to Telegram")
    parser.add_argument("--impl-id", required=True)
    parser.add_argument("--artifact", help="Specific outbox artifact")
    parser.add_argument("--implementations-root", default="/home/mical/fde/implementations")
    parser.add_argument("--bot-token-env", default="ROSSI_BOT_TOKEN", help="Env var containing Telegram bot token")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--watch", action="store_true", help="Poll for new pending outbox artifacts until stopped")
    parser.add_argument("--poll-sec", type=float, default=5.0, help="Poll interval seconds for --watch (default: 5)")
    parser.add_argument("--max-iterations", type=int, default=0, help="Stop after N watch iterations (0 = infinite)")
    args = parser.parse_args()

    token = os.environ.get(args.bot_token_env, "")
    if not token and not args.dry_run:
        parser.error(f"{args.bot_token_env} not set (or use --dry-run)")

    store = TelegramRelayStore(args.implementations_root, args.impl_id)
    store.ensure_layout()
    def run_pass() -> int:
        if args.artifact:
            candidates = [Path(args.artifact)]
        else:
            candidates = sorted(store.paths.outbox.glob("*.md"))
        if not candidates:
            print("No outbox artifacts found.")
            return 0
        for path in candidates:
            status, detail = deliver_one(store, path, token, dry_run=args.dry_run)
            print(f"{path.name}: {status} -> {detail}")
            if not args.once and not args.watch:
                time.sleep(0.1)
        return len(candidates)

    if args.watch:
        iterations = 0
        try:
            while True:
                run_pass()
                iterations += 1
                if args.max_iterations and iterations >= args.max_iterations:
                    break
                time.sleep(max(0.2, args.poll_sec))
        except KeyboardInterrupt:
            print("Stopped watch loop.")
        return 0

    run_pass()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
