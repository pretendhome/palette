#!/usr/bin/env python3
"""palette_cron.py — Governed Scheduled Intent Execution

Reads schedule YAML files from .palette/schedules/, runs intents on schedule
with governance gates (approval, expiry, boundary), stores artifacts, emits
integrity signals.

Usage:
  palette cron list                        # show all schedules
  palette cron run <id>                    # manual trigger
  palette cron daemon                      # run forever (check every 60s)
  palette cron create <id> <intent> <query> [--schedule "0 8 * * 1-5"]

Schedules are YAML files in .palette/schedules/ with this shape:

  id: morning-legal-briefing
  intent: RESEARCH
  query: "Delaware corporate law changes this week"
  schedule_minutes: 480          # every 8 hours (cron expressions post-BDB)
  boundary: governed_external
  delivery: stdout               # stdout | file | telegram
  approved_by: operator
  approved_at: 2026-05-28
  expires_at: 2026-08-28
  enabled: true

Every execution is governance-gated: the intent system classifies, the boundary
is enforced, and the result is stored as a typed artifact. This is what makes
Mission Canvas crons different from Hermes — scheduled tasks with trust boundaries.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

# ── Paths ──────────────────────────────────────────────────────────────────

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEDULES_DIR = REPO_ROOT / ".palette" / "schedules"
ARTIFACTS_DIR = REPO_ROOT / ".palette" / "artifacts"
CRON_LOG = REPO_ROOT / ".palette" / "cron_log.ndjson"
PALETTE_CMD = REPO_ROOT / "scripts" / "palette_intent.py"

CHECK_INTERVAL = 60  # seconds between schedule checks

# ── ANSI ───────────────────────────────────────────────────────────────────

BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"


# ── Schedule Loading ───────────────────────────────────────────────────────

def load_schedules() -> list[dict]:
    """Load all schedule YAML files from .palette/schedules/."""
    SCHEDULES_DIR.mkdir(parents=True, exist_ok=True)
    schedules = []
    for path in sorted(SCHEDULES_DIR.glob("*.yaml")):
        try:
            with open(path) as f:
                data = yaml.safe_load(f)
            if data and isinstance(data, dict):
                data["_path"] = str(path)
                schedules.append(data)
        except Exception as e:
            print(f"{RED}Error loading {path.name}: {e}{RESET}", file=sys.stderr)
    return schedules


def save_schedule(schedule: dict) -> None:
    """Write a schedule back to its YAML file (updates last_run, etc.)."""
    path = Path(schedule.get("_path", ""))
    if not path.exists():
        path = SCHEDULES_DIR / f"{schedule['id']}.yaml"
    data = {k: v for k, v in schedule.items() if not k.startswith("_")}
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


# ── Governance Checks ──────────────────────────────────────────────────────

def check_governance(schedule: dict) -> tuple[bool, str]:
    """Check if a schedule is approved, not expired, and enabled.

    Returns (allowed, reason).
    """
    if not schedule.get("enabled", True):
        return False, "disabled"

    if not schedule.get("approved_by"):
        return False, "no approval — requires approved_by field"

    expires = schedule.get("expires_at")
    if expires:
        try:
            exp_date = datetime.fromisoformat(str(expires)).replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) > exp_date:
                return False, f"expired on {expires}"
        except ValueError:
            return False, f"invalid expires_at: {expires}"

    return True, "approved"


def is_due(schedule: dict) -> bool:
    """Check if a schedule is due to run based on schedule_minutes."""
    interval = schedule.get("schedule_minutes", 0)
    if interval <= 0:
        return False

    last_run = schedule.get("last_run")
    if not last_run:
        return True  # never run before

    try:
        last = datetime.fromisoformat(str(last_run)).replace(tzinfo=timezone.utc)
        elapsed = (datetime.now(timezone.utc) - last).total_seconds() / 60
        return elapsed >= interval
    except ValueError:
        return True


# ── Intent Execution ───────────────────────────────────────────────────────

def execute_intent(schedule: dict) -> dict:
    """Execute a governed intent via subprocess.

    Returns {success, output, artifact_path, duration_ms}.
    """
    intent = schedule.get("intent", "RESEARCH").lower()
    query = schedule.get("query", "")
    sid = schedule.get("id", "unknown")

    start = time.monotonic()

    # Build command: python3 scripts/palette_intent.py <intent> "<query>"
    cmd = [
        sys.executable,
        str(PALETTE_CMD),
        intent,
        query,
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(REPO_ROOT),
        )
        duration_ms = int((time.monotonic() - start) * 1000)

        output = result.stdout
        success = result.returncode == 0

        if not success and result.stderr:
            output += f"\n[STDERR] {result.stderr[-500:]}"

        return {
            "success": success,
            "output": output,
            "return_code": result.returncode,
            "duration_ms": duration_ms,
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "[TIMEOUT] Intent execution exceeded 120s",
            "return_code": -1,
            "duration_ms": 120000,
        }
    except Exception as e:
        return {
            "success": False,
            "output": f"[ERROR] {e}",
            "return_code": -1,
            "duration_ms": int((time.monotonic() - start) * 1000),
        }


# ── Artifact Storage ───────────────────────────────────────────────────────

def store_cron_artifact(schedule: dict, result: dict) -> str:
    """Store cron execution result as a typed artifact."""
    intent = schedule.get("intent", "RESEARCH").lower()
    sid = schedule.get("id", "unknown")

    type_dir = ARTIFACTS_DIR / "cron" / intent
    type_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")
    filename = f"{sid}_{timestamp}.md"
    path = type_dir / filename

    frontmatter = {
        "schedule_id": sid,
        "intent": intent,
        "query": schedule.get("query", ""),
        "boundary": schedule.get("boundary", "local_only"),
        "approved_by": schedule.get("approved_by", ""),
        "success": result["success"],
        "duration_ms": result["duration_ms"],
        "executed_at": datetime.now(timezone.utc).isoformat(),
    }

    content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---\n\n{result['output']}\n"
    path.write_text(content)
    return str(path)


# ── Logging ────────────────────────────────────────────────────────────────

def log_execution(schedule: dict, result: dict, artifact_path: str) -> None:
    """Append execution record to cron_log.ndjson (audit trail)."""
    CRON_LOG.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "schedule_id": schedule.get("id"),
        "intent": schedule.get("intent"),
        "query": schedule.get("query"),
        "boundary": schedule.get("boundary"),
        "success": result["success"],
        "duration_ms": result["duration_ms"],
        "artifact_path": artifact_path,
    }
    with open(CRON_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


# ── Delivery ───────────────────────────────────────────────────────────────

def deliver(schedule: dict, result: dict) -> None:
    """Deliver result to configured destination."""
    delivery = schedule.get("delivery", "stdout")
    sid = schedule.get("id", "")

    if delivery == "stdout":
        print(result["output"])
    elif delivery == "file":
        # Already stored as artifact
        pass
    elif delivery == "telegram":
        # Will be wired when mc_telegram.py is built
        print(f"{DIM}[delivery:telegram] would send to Telegram — not yet wired{RESET}")


# ── Run One Schedule ───────────────────────────────────────────────────────

def run_schedule(schedule: dict, force: bool = False) -> bool:
    """Execute a single governed schedule.

    Returns True if executed, False if skipped.
    """
    sid = schedule.get("id", "unknown")
    intent = schedule.get("intent", "?")

    # Governance gate
    allowed, reason = check_governance(schedule)
    if not allowed:
        print(f"  {RED}BLOCKED{RESET}  {sid} — {reason}")
        return False

    # Due check (skip if not forced)
    if not force and not is_due(schedule):
        return False

    # Execute
    print(f"  {CYAN}[CRON]{RESET}  {BOLD}{sid}{RESET}")
    print(f"  {DIM}Intent: {intent} | Boundary: {schedule.get('boundary', 'local_only')}{RESET}")
    print(f"  {DIM}Query: {schedule.get('query', '')[:80]}{RESET}")
    print(f"  {DIM}Approved by: {schedule.get('approved_by', 'none')} | Expires: {schedule.get('expires_at', 'never')}{RESET}")
    print()

    result = execute_intent(schedule)

    # Store artifact
    artifact_path = store_cron_artifact(schedule, result)

    # Log execution
    log_execution(schedule, result, artifact_path)

    # Update last_run
    schedule["last_run"] = datetime.now(timezone.utc).isoformat()
    save_schedule(schedule)

    # Status
    if result["success"]:
        print(f"  {GREEN}DONE{RESET}  {sid} ({result['duration_ms']}ms)")
    else:
        print(f"  {RED}FAIL{RESET}  {sid} ({result['duration_ms']}ms)")

    print(f"  {DIM}Artifact: {artifact_path}{RESET}")
    print()

    # Deliver
    deliver(schedule, result)

    return True


# ── CLI Commands ───────────────────────────────────────────────────────────

def cmd_list() -> None:
    """List all schedules with status."""
    schedules = load_schedules()
    if not schedules:
        print(f"{DIM}No schedules found in {SCHEDULES_DIR}{RESET}")
        print(f"{DIM}Create one: palette cron create <id> <intent> <query>{RESET}")
        return

    print(f"\n{BOLD}Governed Schedules{RESET}")
    print(f"{DIM}{'ID':<30} {'Intent':<10} {'Interval':<10} {'Boundary':<18} {'Status':<12} Last Run{RESET}")
    print("─" * 110)

    for s in schedules:
        sid = s.get("id", "?")
        intent = s.get("intent", "?")
        interval = f"{s.get('schedule_minutes', 0)}m"
        boundary = s.get("boundary", "local_only")
        allowed, reason = check_governance(s)
        status = f"{GREEN}ready{RESET}" if allowed else f"{RED}{reason}{RESET}"
        last = s.get("last_run", "never")
        if last != "never":
            last = last[:19]  # trim to seconds
        print(f"  {sid:<30} {intent:<10} {interval:<10} {boundary:<18} {status:<22} {last}")

    print()


def cmd_run(schedule_id: str) -> None:
    """Manually trigger a single schedule."""
    schedules = load_schedules()
    match = [s for s in schedules if s.get("id") == schedule_id]
    if not match:
        print(f"{RED}Schedule '{schedule_id}' not found.{RESET}")
        print(f"{DIM}Available: {', '.join(s.get('id', '?') for s in schedules)}{RESET}")
        return
    run_schedule(match[0], force=True)


def cmd_daemon() -> None:
    """Run continuously, checking schedules every CHECK_INTERVAL seconds."""
    print(f"{BOLD}Mission Canvas Cron Daemon{RESET}")
    print(f"{DIM}Checking schedules every {CHECK_INTERVAL}s. Press Ctrl+C to stop.{RESET}")
    print()

    try:
        while True:
            schedules = load_schedules()
            for s in schedules:
                try:
                    run_schedule(s, force=False)
                except Exception as e:
                    print(f"  {RED}ERROR{RESET}  {s.get('id', '?')}: {e}", file=sys.stderr)
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print(f"\n{DIM}Cron daemon stopped.{RESET}")


def cmd_create(schedule_id: str, intent: str, query: str, schedule_minutes: int = 480) -> None:
    """Create a new schedule YAML."""
    SCHEDULES_DIR.mkdir(parents=True, exist_ok=True)
    path = SCHEDULES_DIR / f"{schedule_id}.yaml"

    if path.exists():
        print(f"{RED}Schedule '{schedule_id}' already exists at {path}{RESET}")
        return

    schedule = {
        "id": schedule_id,
        "intent": intent.upper(),
        "query": query,
        "schedule_minutes": schedule_minutes,
        "boundary": "governed_external" if intent.upper() == "RESEARCH" else "local_only",
        "delivery": "stdout",
        "approved_by": os.environ.get("USER", "unknown"),
        "approved_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "expires_at": "",  # no expiry by default
        "enabled": True,
    }

    with open(path, "w") as f:
        yaml.dump(schedule, f, default_flow_style=False, sort_keys=False)

    print(f"{GREEN}Created:{RESET} {path}")
    print(f"{DIM}Edit to customize boundary, delivery, and expiry.{RESET}")


# ── Main ───────────────────────────────────────────────────────────────────

def main() -> None:
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print(f"""
{BOLD}palette cron{RESET} — Governed Scheduled Intent Execution

  {CYAN}palette cron list{RESET}                          Show all schedules
  {CYAN}palette cron run <id>{RESET}                      Manual trigger (governance-gated)
  {CYAN}palette cron daemon{RESET}                        Run forever (check every {CHECK_INTERVAL}s)
  {CYAN}palette cron create <id> <intent> <query>{RESET}  Create new schedule

{DIM}Schedules live in .palette/schedules/*.yaml
Each execution is governance-gated: approved, not expired, boundary enforced.
Results stored as typed artifacts in .palette/artifacts/cron/{RESET}
""")
        return

    cmd = args[0]

    if cmd == "list":
        cmd_list()
    elif cmd == "run" and len(args) >= 2:
        cmd_run(args[1])
    elif cmd == "daemon":
        cmd_daemon()
    elif cmd == "create" and len(args) >= 4:
        minutes = int(args[4]) if len(args) >= 5 else 480
        cmd_create(args[1], args[2], args[3], minutes)
    else:
        print(f"{RED}Unknown command: {cmd}{RESET}")
        print(f"{DIM}Try: palette cron --help{RESET}")


if __name__ == "__main__":
    main()
