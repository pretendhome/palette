#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import time
from dataclasses import dataclass
from pathlib import Path

from relay_store import TelegramRelayStore


@dataclass
class PruneDecision:
    path: Path
    reason: str
    age_days: float


def file_age_days(path: Path, now: float) -> float:
    return max(0.0, (now - path.stat().st_mtime) / 86400.0)


def collect_files(path: Path, pattern: str = "*.md") -> list[Path]:
    if not path.exists():
        return []
    return sorted([p for p in path.glob(pattern) if p.is_file()], key=lambda p: p.stat().st_mtime, reverse=True)


def decide_prune(
    files: list[Path],
    *,
    keep_latest: int,
    max_age_days: int,
    now: float,
) -> list[PruneDecision]:
    decisions: list[PruneDecision] = []
    for idx, path in enumerate(files):
        age = file_age_days(path, now)
        if idx < keep_latest:
            continue
        if age >= max_age_days:
            decisions.append(PruneDecision(path=path, reason=f"age>={max_age_days}d and beyond keep_latest={keep_latest}", age_days=age))
    return decisions


def delete_files(decisions: list[PruneDecision]) -> int:
    deleted = 0
    for d in decisions:
        try:
            d.path.unlink(missing_ok=True)
            deleted += 1
        except OSError:
            continue
    return deleted


def summarize_bucket(label: str, files: list[Path], decisions: list[PruneDecision]) -> None:
    print(f"[{label}] total={len(files)} prune_candidates={len(decisions)}")
    for d in decisions[:10]:
        print(f"  - {d.path.name} ({d.age_days:.1f}d) :: {d.reason}")
    if len(decisions) > 10:
        print(f"  - ... {len(decisions)-10} more")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prune old Telegram relay artifacts (safe retention helper)")
    parser.add_argument("--impl-id", required=True)
    parser.add_argument("--implementations-root", default="/home/mical/fde/implementations")
    parser.add_argument("--apply", action="store_true", help="Actually delete files (default is dry-run)")
    parser.add_argument("--outbox-keep-latest", type=int, default=50)
    parser.add_argument("--outbox-max-age-days", type=int, default=14)
    parser.add_argument("--processed-keep-latest", type=int, default=200)
    parser.add_argument("--processed-max-age-days", type=int, default=60)
    parser.add_argument("--failed-keep-latest", type=int, default=200)
    parser.add_argument("--failed-max-age-days", type=int, default=90)
    parser.add_argument("--sessions-keep-latest", type=int, default=100)
    parser.add_argument("--sessions-max-age-days", type=int, default=30)
    parser.add_argument("--events-max-age-days", type=int, default=30, help="Delete whole daily .jsonl files older than this (except latest 7)")
    parser.add_argument("--events-keep-latest-days", type=int, default=7)
    args = parser.parse_args()

    store = TelegramRelayStore(args.implementations_root, args.impl_id)
    store.ensure_layout()
    now = time.time()

    # Buckets (md files)
    outbox_files = collect_files(store.paths.outbox, "*.md")
    processed_files = collect_files(store.paths.archive / "processed", "*.md")
    failed_files = collect_files(store.paths.archive / "failed", "*.md")
    session_files = collect_files(store.paths.sessions, "*.md")

    outbox_prune = decide_prune(outbox_files, keep_latest=args.outbox_keep_latest, max_age_days=args.outbox_max_age_days, now=now)
    processed_prune = decide_prune(processed_files, keep_latest=args.processed_keep_latest, max_age_days=args.processed_max_age_days, now=now)
    failed_prune = decide_prune(failed_files, keep_latest=args.failed_keep_latest, max_age_days=args.failed_max_age_days, now=now)
    sessions_prune = decide_prune(session_files, keep_latest=args.sessions_keep_latest, max_age_days=args.sessions_max_age_days, now=now)

    # Events (.jsonl) by day files
    event_files = collect_files(store.paths.events, "*.jsonl")
    event_prune: list[PruneDecision] = []
    for idx, path in enumerate(event_files):
        age = file_age_days(path, now)
        if idx < args.events_keep_latest_days:
            continue
        if age >= args.events_max_age_days:
            event_prune.append(PruneDecision(path=path, reason=f"daily event log older than {args.events_max_age_days}d beyond latest {args.events_keep_latest_days}", age_days=age))

    print(f"Relay retention scan: {args.impl_id}")
    print(f"Mode: {'APPLY' if args.apply else 'DRY-RUN'}")
    print("")
    summarize_bucket("outbox", outbox_files, outbox_prune)
    summarize_bucket("archive/processed", processed_files, processed_prune)
    summarize_bucket("archive/failed", failed_files, failed_prune)
    summarize_bucket("sessions", session_files, sessions_prune)
    summarize_bucket("events", event_files, event_prune)

    all_decisions = outbox_prune + processed_prune + failed_prune + sessions_prune + event_prune
    print("")
    print(f"Total prune candidates: {len(all_decisions)}")

    if not args.apply:
        print("No files deleted (dry-run). Re-run with --apply to prune.")
        return 0

    deleted = delete_files(all_decisions)
    print(f"Deleted files: {deleted}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

