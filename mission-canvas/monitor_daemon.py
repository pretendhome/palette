#!/usr/bin/env python3
"""
monitor_daemon.py — Mission Canvas Monitor Daemon
Reads workspace monitor definitions, runs Perplexity searches on schedule,
writes alerts, and pushes notifications to Telegram.

Setup:
  export PERPLEXITY_API_KEY="pplx-xxx"
  export JOSEPH_BOT_TOKEN="your-telegram-bot-token"
  export TELEGRAM_CHAT_ID="123456789"       # Joseph's chat ID
  export MC_WORKSPACE="oil-investor"
  python3 monitor_daemon.py

The daemon runs in a loop, checking each monitor's schedule.
Without PERPLEXITY_API_KEY, it exits with instructions.
"""
from __future__ import annotations

import os
import sys
import time
import json
import datetime
import hashlib
from pathlib import Path

import httpx
import yaml

# ── Config ──────────────────────────────────────────────────────────────────

PERPLEXITY_KEY = os.environ.get("PERPLEXITY_API_KEY", "")
BOT_TOKEN      = os.environ.get("JOSEPH_BOT_TOKEN", "")
CHAT_ID        = os.environ.get("TELEGRAM_CHAT_ID", "")
MC_WORKSPACE   = os.environ.get("MC_WORKSPACE", "oil-investor")
WORKSPACES_DIR = os.environ.get("MC_WORKSPACES_DIR",
                                os.path.join(os.path.dirname(__file__), "workspaces"))
CHECK_INTERVAL = 60  # seconds between schedule checks

PERPLEXITY_URL = "https://api.perplexity.ai/chat/completions"
PERPLEXITY_MODEL = "sonar"
TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


# ── Perplexity API ──────────────────────────────────────────────────────────

def perplexity_search(query: str, system_prompt: str = "") -> dict:
    """Call Perplexity Sonar API and return content + citations."""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": query})

    with httpx.Client(timeout=60.0) as client:
        resp = client.post(
            PERPLEXITY_URL,
            headers={
                "Authorization": f"Bearer {PERPLEXITY_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": PERPLEXITY_MODEL,
                "messages": messages,
                "return_citations": True,
            },
        )
        resp.raise_for_status()
        data = resp.json()

    content = data["choices"][0]["message"]["content"]
    citations = data.get("citations", [])
    return {"content": content, "citations": citations}


# ── Telegram ────────────────────────────────────────────────────────────────

def tg_send(chat_id: str, text: str) -> None:
    """Send a message to Telegram, chunking if needed."""
    if not BOT_TOKEN or not chat_id:
        print(f"[monitor] would notify Telegram: {text[:100]}...", flush=True)
        return
    chunk_size = 4000
    with httpx.Client(timeout=15.0) as client:
        for i in range(0, len(text), chunk_size):
            client.post(
                f"{TELEGRAM_URL}/sendMessage",
                json={
                    "chat_id": chat_id,
                    "text": text[i : i + chunk_size],
                    "parse_mode": "Markdown",
                },
            )
            if i + chunk_size < len(text):
                time.sleep(0.3)


# ── YAML helpers ────────────────────────────────────────────────────────────

def load_yaml(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f) or {}


def save_yaml(path: Path, data: dict) -> None:
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


# ── Monitor execution ──────────────────────────────────────────────────────

def should_run(monitor: dict) -> bool:
    """Check if enough time has passed since last run."""
    last_run = monitor.get("last_run")
    if not last_run:
        return True
    schedule = monitor.get("schedule_minutes", 120)
    if isinstance(last_run, str):
        last_dt = datetime.datetime.fromisoformat(last_run)
    else:
        last_dt = last_run
    elapsed = (datetime.datetime.now() - last_dt).total_seconds() / 60
    return elapsed >= schedule


def run_monitor(monitor: dict, workspace_dir: Path) -> list[dict]:
    """Execute a single monitor: search, filter, create alerts."""
    monitor_id = monitor["id"]
    name = monitor["name"]
    queries = monitor.get("search_queries", [])
    system_prompt = monitor.get("system_prompt", "")
    max_alerts = monitor.get("context", {}).get("max_alerts_per_run", 3)

    print(f"[monitor] running '{name}' ({len(queries)} queries)...", flush=True)

    # Combine all queries into one focused search
    combined_query = (
        f"Provide a brief intelligence update on the following topics. "
        f"Only include developments from the last 24 hours that are materially significant. "
        f"Format as numbered items with specific data points.\n\n"
        + "\n".join(f"- {q}" for q in queries)
    )

    try:
        result = perplexity_search(combined_query, system_prompt)
    except Exception as e:
        print(f"[monitor] Perplexity error for '{name}': {e}", flush=True)
        return []

    content = result["content"]
    citations = result.get("citations", [])

    if not content or len(content.strip()) < 20:
        print(f"[monitor] '{name}' — no significant results", flush=True)
        return []

    # Create alert
    now = datetime.datetime.now()
    alert_id = f"alert-{now.strftime('%Y%m%d-%H%M%S')}-{monitor_id}"

    alert = {
        "alert": {
            "id": alert_id,
            "monitor_id": monitor_id,
            "monitor_name": name,
            "timestamp": now.isoformat(),
            "content": content,
            "citations": citations[:5],
            "source": "perplexity-sonar",
        }
    }

    # Write alert to file
    alerts_dir = workspace_dir / "alerts"
    alerts_dir.mkdir(exist_ok=True)
    alert_path = alerts_dir / f"{alert_id}.yaml"
    save_yaml(alert_path, alert)
    print(f"[monitor] wrote alert: {alert_path.name}", flush=True)

    return [alert]


def notify_alerts(alerts: list[dict], chat_id: str) -> None:
    """Send alert notifications to Telegram."""
    for alert_data in alerts:
        a = alert_data["alert"]
        # Format for Telegram
        lines = [
            f"🔔 *{a['monitor_name']}*",
            f"_{datetime.datetime.fromisoformat(a['timestamp']).strftime('%H:%M %b %d')}_",
            "",
            a["content"][:3000],
        ]
        citations = a.get("citations", [])
        if citations:
            lines.append("")
            lines.append("*Sources:*")
            for i, c in enumerate(citations[:3], 1):
                if isinstance(c, str):
                    lines.append(f"{i}. {c}")
                elif isinstance(c, dict):
                    lines.append(f"{i}. {c.get('url', c.get('title', 'source'))}")
        tg_send(chat_id, "\n".join(lines))


# ── Main loop ───────────────────────────────────────────────────────────────

def run_once(workspace_id: str, chat_id: str) -> int:
    """Run one cycle of all monitors. Returns number of alerts generated."""
    ws_dir = Path(WORKSPACES_DIR) / workspace_id
    monitors_dir = ws_dir / "monitors"

    if not monitors_dir.exists():
        print(f"[monitor] no monitors/ dir in {workspace_id}", flush=True)
        return 0

    total_alerts = 0

    for monitor_file in sorted(monitors_dir.glob("*.yaml")):
        try:
            data = load_yaml(monitor_file)
            monitor = data.get("monitor", {})

            if not monitor.get("enabled", True):
                continue

            if not should_run(monitor):
                next_run = monitor.get("schedule_minutes", 120)
                print(f"[monitor] '{monitor['id']}' — next run in {next_run}m, skipping", flush=True)
                continue

            alerts = run_monitor(monitor, ws_dir)

            # Update monitor state
            monitor["last_run"] = datetime.datetime.now().isoformat()
            monitor["last_alert_count"] = len(alerts)
            monitor["total_alerts"] = monitor.get("total_alerts", 0) + len(alerts)
            data["monitor"] = monitor
            save_yaml(monitor_file, data)

            if alerts:
                notify_alerts(alerts, chat_id)
                total_alerts += len(alerts)

        except Exception as e:
            print(f"[monitor] error processing {monitor_file.name}: {e}", flush=True)

    return total_alerts


def main():
    if not PERPLEXITY_KEY:
        print("[monitor] PERPLEXITY_API_KEY not set.", flush=True)
        print("[monitor] export PERPLEXITY_API_KEY='pplx-xxx' to enable monitoring.", flush=True)
        sys.exit(1)

    workspace_id = MC_WORKSPACE
    chat_id = CHAT_ID

    print(f"[monitor] starting — workspace={workspace_id}", flush=True)
    print(f"[monitor] Telegram chat_id={'set' if chat_id else 'NOT SET (will log only)'}", flush=True)
    print(f"[monitor] checking every {CHECK_INTERVAL}s", flush=True)

    # Run once immediately
    count = run_once(workspace_id, chat_id)
    print(f"[monitor] initial run: {count} alerts", flush=True)

    # Then loop
    while True:
        try:
            time.sleep(CHECK_INTERVAL)
            run_once(workspace_id, chat_id)
        except KeyboardInterrupt:
            print("\n[monitor] stopped.", flush=True)
            break
        except Exception as e:
            print(f"[monitor] loop error: {e}", flush=True)
            time.sleep(30)


if __name__ == "__main__":
    main()
