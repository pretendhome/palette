#!/usr/bin/env python3
"""Run PIS audit_system repeatedly.

Examples:
  python3 -m scripts.pis.run_audit_batch --count 20
  python3 -m scripts.pis.run_audit_batch --count 50 --interval 1
  python3 -m scripts.pis.run_audit_batch --infinite --interval 2
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def _utc_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch runner for PIS strict audit")
    parser.add_argument("--count", type=int, default=1, help="Number of runs (ignored with --infinite)")
    parser.add_argument("--infinite", action="store_true", help="Run forever until interrupted")
    parser.add_argument("--interval", type=float, default=0.5, help="Sleep seconds between runs")
    parser.add_argument(
        "--workdir",
        default=str(Path.home() / "fde" / "palette"),
        help="Directory where scripts.pis.audit_system is available",
    )
    parser.add_argument(
        "--backlog-path",
        default="/tmp/pis_backlog.json",
        help="Path for backlog JSON output",
    )
    parser.add_argument(
        "--log-dir",
        default="/tmp/pis-audit-runs",
        help="Directory for per-run stdout/stderr logs",
    )
    args = parser.parse_args()

    workdir = Path(args.workdir)
    log_dir = Path(args.log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    run_total = 0
    failures = 0
    start = time.time()

    print(f"Batch audit start: workdir={workdir}")
    print(f"Logs: {log_dir}")
    print(f"Backlog: {args.backlog_path}")

    try:
        while args.infinite or run_total < args.count:
            run_total += 1
            stamp = _utc_stamp()
            out_path = log_dir / f"run_{run_total:04d}_{stamp}.out"
            err_path = log_dir / f"run_{run_total:04d}_{stamp}.err"

            cmd = [
                sys.executable,
                "-m",
                "scripts.pis.audit_system",
                "--strict",
                "--emit-backlog-json",
                args.backlog_path,
            ]

            result = subprocess.run(
                cmd,
                cwd=workdir,
                capture_output=True,
                text=True,
            )
            out_path.write_text(result.stdout, encoding="utf-8")
            err_path.write_text(result.stderr, encoding="utf-8")

            if result.returncode != 0:
                failures += 1

            print(
                f"[{run_total}] exit={result.returncode} "
                f"log={out_path.name} backlog={args.backlog_path}"
            )

            if args.interval > 0:
                time.sleep(args.interval)

    except KeyboardInterrupt:
        print("\nInterrupted by user.")

    elapsed = time.time() - start
    print(
        f"Done: runs={run_total}, nonzero_exits={failures}, "
        f"elapsed_s={elapsed:.1f}, log_dir={log_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
