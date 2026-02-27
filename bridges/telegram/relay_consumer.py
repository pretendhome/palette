#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

from relay_store import TelegramRelayStore


FM_BOUNDARY = "---"


def parse_frontmatter_md(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith(FM_BOUNDARY):
        raise ValueError(f"Missing frontmatter in {path}")
    parts = text.split(FM_BOUNDARY, 2)
    if len(parts) < 3:
        raise ValueError(f"Malformed frontmatter in {path}")
    fm_text = parts[1].strip("\n")
    body = parts[2].lstrip("\n")
    data: dict[str, Any] = {}
    current_key: str | None = None
    for raw_line in fm_text.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if re.match(r"^\s+-\s+", line):
            if current_key is None:
                continue
            data.setdefault(current_key, [])
            data[current_key].append(_parse_scalar(re.sub(r"^\s+-\s+", "", line)))
            continue
        if line.endswith(":") and ":" not in line[:-1]:
            current_key = line[:-1].strip()
            data[current_key] = []
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            current_key = key.strip()
            data[current_key] = _parse_scalar(value.strip())
    return data, body


def _parse_scalar(value: str) -> Any:
    if value in {"true", "false"}:
        return value == "true"
    if value == "null":
        return None
    if value.startswith('"') and value.endswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value.strip('"')
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


def extract_section(body: str, heading: str) -> str:
    marker = f"## {heading}"
    if marker not in body:
        return ""
    tail = body.split(marker, 1)[1].lstrip("\n")
    next_match = re.search(r"^##\s+", tail, flags=re.MULTILINE)
    if next_match:
        tail = tail[: next_match.start()]
    return tail.strip()


def build_stub_response(intent: str, user_request: str) -> str:
    if intent == "orch_summary_request":
        return (
            "Accepted relay request for `orch_summary_request`.\n\n"
            "V1 consumer mode is active, so no live Orch call was executed. "
            "A downstream Palette/Orch worker should read this request and produce a reviewed summary.\n\n"
            f"Captured request: {user_request[:500]}"
        )
    if intent in {"status_request", "daily_update"}:
        label = "daily_update" if intent == "daily_update" else "status_request"
        return (
            f"Accepted relay `{label}`.\n\n"
            "V1 consumer is a safe stub: it recorded your request and generated this placeholder response. "
            "No runtime/system status was queried."
        )
    if intent == "update_request":
        return (
            "Accepted relay `update_request`.\n\n"
            "V1 consumer does not mutate repo files. The request is archived and ready for a higher-trust worker "
            "to review and generate an approved markdown update."
        )
    if intent == "triage_request":
        return (
            "Accepted relay `triage_request`.\n\n"
            "V1 consumer recorded the request. A future worker can classify and route it to Orch/Argy/Rex/Theri."
        )
    return (
        f"Accepted relay request for `{intent}`, but no handler exists in v1 consumer. "
        "Request has been recorded and should be reviewed manually."
    )


def orch_adapter_enabled() -> bool:
    return os.environ.get("PALETTE_RELAY_ORCH_ENABLED", "0").strip().lower() in {"1", "true", "yes", "on"}


def orch_binary_path() -> str:
    return os.environ.get(
        "PALETTE_RELAY_ORCH_BIN",
        "/home/mical/fde/palette/agents/orchestrator/orch",
    )


def orch_mode() -> str:
    mode = os.environ.get("PALETTE_RELAY_ORCH_MODE", "plan").strip().lower()
    return mode if mode in {"route", "plan"} else "plan"


def orch_timeout_sec() -> int:
    raw = os.environ.get("PALETTE_RELAY_ORCH_TIMEOUT_SEC", "25").strip()
    try:
        return max(3, min(120, int(raw)))
    except ValueError:
        return 25


def invoke_orch(task: str, trace_id: str) -> tuple[bool, str, dict[str, Any]]:
    cmd = [orch_binary_path(), orch_mode(), "--trace-id", trace_id, task]
    timeout = orch_timeout_sec()
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()
    evidence = {
        "orch_cmd": cmd,
        "exit_code": proc.returncode,
        "timeout_sec": timeout,
        "stdout_preview": stdout[:2000],
        "stderr_preview": stderr[:2000],
    }
    ok = proc.returncode == 0
    if ok:
        response = (
            f"Live Orch handoff executed via `orch {orch_mode()}`.\n\n"
            f"Task: {task}\n\n"
            "### Orch Output\n"
            f"{stdout or '(no stdout)'}"
        )
        if stderr:
            response += f"\n\n### Orch Stderr\n{stderr}"
        return True, response, evidence
    response = (
        f"Orch handoff attempted via `orch {orch_mode()}` but failed (exit {proc.returncode}).\n\n"
        f"Task: {task}\n\n"
        f"### stderr\n{stderr or '(empty)'}"
    )
    if stdout:
        response += f"\n\n### stdout\n{stdout}"
    return False, response, evidence


def build_orch_task(
    *,
    impl_id: str,
    intent: str,
    user_request: str,
    request_id: str,
    trace_id: str,
    publish_requested: bool = False,
    publish_target_path: str = "",
) -> str:
    """
    Build a structured Orch task string from relay metadata.
    Keep it plaintext (CLI-friendly) but more constrained than raw Telegram text.
    """
    base = [
        f"impl={impl_id}",
        f"intent={intent}",
        f"request_id={request_id}",
        f"trace_id={trace_id}",
        "source=telegram-relay",
        "goal=produce concise routing/plan guidance for downstream Palette processing",
        "constraints=no direct execution unless explicitly requested outside this relay; prefer routing/plan",
        f"user_request={user_request.strip()}",
    ]

    if impl_id == "retail-rossi-store" and intent == "orch_summary_request":
        base.extend(
            [
                "domain=rossi mission project funding/business-plan support",
                "desired_output=one short routing/plan summary for Rossi funding blockers follow-up",
                "safety=do not fabricate live repo/system state; route if live data required",
            ]
        )
    elif impl_id == "retail-rossi-store" and intent in {"status_request", "daily_update"}:
        base.extend(
            [
                "domain=rossi mission project status/fundability tracking",
                "desired_output=route or plan for a concise status artifact update",
                "safety=no live repo/system claims without explicit evidence",
            ]
        )
    elif impl_id == "retail-rossi-store" and intent == "update_request":
        base.extend(
            [
                "domain=rossi mission project update drafting",
                "desired_output=route/plan for generating a publishable markdown update artifact",
                f"publish_requested={'true' if publish_requested else 'false'}",
                f"publish_target_path={publish_target_path or 'none'}",
                "safety=do not publish or commit directly from orch routing step",
            ]
        )

    return " | ".join(base)


def summarize_orch_output_for_telegram(stdout: str, *, mode: str) -> str:
    """
    Create a compact user-facing summary from Orch stdout while keeping full output in provenance.
    """
    text = (stdout or "").strip()
    if not text:
        return f"Orch `{mode}` completed, but returned no stdout."

    route_match = re.search(r"^\s*Route:\s+(.+)$", text, flags=re.MULTILINE)
    confidence_match = re.search(r"^\s*Confidence:\s+(.+)$", text, flags=re.MULTILINE)
    steps_match = re.search(r"^\s*Steps:\s+(.+)$", text, flags=re.MULTILINE)
    trace_match = re.search(r"^\s*Trace:\s+(.+)$", text, flags=re.MULTILINE)
    reason_match = re.search(r"^\s*Reason:\s+(.+)$", text, flags=re.MULTILINE)

    lines = [
        f"Live Orch handoff executed via `orch {mode}`.",
        "",
        "## Orch Summary",
    ]
    if route_match:
        lines.append(f"- Route: {route_match.group(1).strip()}")
    if confidence_match:
        lines.append(f"- Confidence/Maturity: {confidence_match.group(1).strip()}")
    if steps_match:
        lines.append(f"- Planned steps: {steps_match.group(1).strip()}")
    if reason_match:
        lines.append(f"- Routing reason: {reason_match.group(1).strip()}")
    if trace_match:
        lines.append(f"- Orch trace: {trace_match.group(1).strip()}")
    if len(lines) == 3:
        preview = "\n".join(text.splitlines()[:10]).strip()
        lines.append(f"- Output preview: {preview[:600]}")
    lines.extend(
        [
            "",
            "Full Orch stdout/stderr is preserved in relay provenance evidence for audit.",
        ]
    )
    return "\n".join(lines)


def archive_request_file(store: TelegramRelayStore, req_path: Path, status: str) -> Path:
    archive_dir = store.paths.archive / status
    archive_dir.mkdir(parents=True, exist_ok=True)
    dest = archive_dir / req_path.name
    shutil.move(str(req_path), str(dest))
    return dest


def process_request_file(store: TelegramRelayStore, req_path: Path) -> tuple[str, str]:
    fm, body = parse_frontmatter_md(req_path)
    request_id = str(fm.get("request_id", ""))
    trace_id = str(fm.get("trace_id", ""))
    intent = str(fm.get("intent", "unknown"))
    publish_requested = bool(fm.get("publish_to_github_requested", False))
    publish_approved = bool(fm.get("publish_to_github_approved", False))
    publish_target_path = str(fm.get("publish_target_path", ""))
    requested_by = str(fm.get("requested_by", "")).strip()
    source_event_ids = fm.get("source_event_ids") if isinstance(fm.get("source_event_ids"), list) else []
    user_request = extract_section(body, "User Request")

    if not request_id or not trace_id:
        archive_path = archive_request_file(store, req_path, "failed")
        store.append_event(
            {
                "trace_id": trace_id or store.new_trace_id("relay"),
                "source": "relay-consumer",
                "direction": "internal",
                "status": "failed",
                "error_code": "invalid_request_artifact",
                "artifact_path": str(archive_path),
                "provenance": "relay-consumer",
            }
        )
        return ("failed", str(archive_path))

    store.append_event(
        {
            "trace_id": trace_id,
            "source": "relay-consumer",
            "direction": "internal",
            "status": "processing",
            "request_id": request_id,
            "intent": intent,
            "artifact_path": str(req_path),
            "provenance": "relay-consumer",
        }
    )

    live_call = False
    evidence: dict[str, Any] = {"request_artifact": str(req_path)}
    response_text = build_stub_response(intent, user_request)
    structured_task = build_orch_task(
        impl_id=store.impl_id,
        intent=intent,
        user_request=user_request,
        request_id=request_id,
        trace_id=trace_id,
        publish_requested=publish_requested,
        publish_target_path=publish_target_path,
    )
    evidence["structured_task"] = structured_task
    if intent == "orch_summary_request" and orch_adapter_enabled():
        try:
            orch_task = structured_task
            live_call, orch_text, orch_evidence = invoke_orch(orch_task, trace_id)
            response_text = orch_text
            stdout_preview = str(orch_evidence.get("stdout_preview", ""))
            if live_call and orch_mode() in {"plan", "route"} and stdout_preview:
                response_text = summarize_orch_output_for_telegram(stdout_preview, mode=orch_mode())
            evidence.update(orch_evidence)
            evidence["orch_task"] = orch_task
            store.append_event(
                {
                    "trace_id": trace_id,
                    "source": "relay-consumer",
                    "direction": "internal",
                    "status": "orch_handoff_completed" if live_call else "orch_handoff_failed",
                    "request_id": request_id,
                    "intent": intent,
                    "provenance": "relay-consumer",
                }
            )
        except subprocess.TimeoutExpired as e:
            live_call = False
            response_text = (
                f"Orch handoff attempted via `orch {orch_mode()}` but timed out after {orch_timeout_sec()}s.\n\n"
                f"Task: {user_request}"
            )
            orch_task = build_orch_task(
                impl_id=store.impl_id,
                intent=intent,
                user_request=user_request,
                request_id=request_id,
                trace_id=trace_id,
                publish_requested=publish_requested,
                publish_target_path=publish_target_path,
            )
            evidence.update(
                {
                    "orch_cmd": [orch_binary_path(), orch_mode(), "--trace-id", trace_id, orch_task],
                    "orch_task": orch_task,
                    "timeout_sec": orch_timeout_sec(),
                    "error": "timeout",
                }
            )
            store.append_event(
                {
                    "trace_id": trace_id,
                    "source": "relay-consumer",
                    "direction": "internal",
                    "status": "orch_handoff_timeout",
                    "request_id": request_id,
                    "intent": intent,
                    "provenance": "relay-consumer",
                }
            )
    if publish_requested:
        response_text += (
            "\n\nGitHub publish was requested in metadata, but v1 consumer will not publish. "
            f"Approved={publish_approved}. Target={publish_target_path or 'unset'}."
        )
    outbox_path = store.write_response(
        request_id=request_id,
        trace_id=trace_id,
        intent=intent,
        response_text=response_text,
        destination="telegram",
        source="relay-consumer",
        delivery_target=requested_by,
        live_call=live_call,
        evidence=evidence,
        publish_to_github_requested=publish_requested,
        publish_to_github_approved=publish_approved,
        publish_target_path=publish_target_path,
    )

    archived_path = archive_request_file(store, req_path, "processed")
    store.append_event(
        {
            "trace_id": trace_id,
            "source": "relay-consumer",
            "direction": "internal",
            "status": "completed",
            "request_id": request_id,
            "intent": intent,
            "artifact_path": str(outbox_path),
            "archive_path": str(archived_path),
            "source_event_ids": source_event_ids,
            "provenance": "relay-consumer",
        }
    )
    return ("completed", str(outbox_path))


def refresh_state(store: TelegramRelayStore) -> None:
    inbox_pending = len(list(store.paths.inbox.glob("*.md")))
    outbox_pending = len(list(store.paths.outbox.glob("*.md")))
    failed = len(list((store.paths.archive / "failed").glob("*.md"))) if (store.paths.archive / "failed").exists() else 0

    last_processed: dict[str, str] = {}
    processed_dir = store.paths.archive / "processed"
    if processed_dir.exists():
        latest = sorted(processed_dir.glob("*.md"))
        if latest:
            last_processed["Request Artifact"] = latest[-1].name
    outbox = sorted(store.paths.outbox.glob("*.md"))
    if outbox:
        last_processed["Response Artifact"] = outbox[-1].name

    store.update_state(
        status_lines=[
            "- Relay: active",
            "- Telegram bridge: pilot hook enabled",
            "- Relay consumer: stub + optional Orch handoff (`PALETTE_RELAY_ORCH_ENABLED=1`)",
            "- Direct shell from Telegram: disabled",
            "- Repo mutation: approval required",
        ],
        queue_counts={"Inbox pending": inbox_pending, "Outbox pending": outbox_pending, "Failed": failed},
        last_processed=last_processed,
        notes=[
            "Consumer writes stub outbox responses by default.",
            "Optional live Orch handoff is disabled by default and uses `orch plan|route` only.",
        ],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Process Telegram relay inbox artifacts (safe stub v1)")
    parser.add_argument("--impl-id", required=True, help="Implementation id under implementations/")
    parser.add_argument(
        "--implementations-root",
        default="/home/mical/fde/implementations",
        help="Implementations root path",
    )
    parser.add_argument("--once", action="store_true", help="Process current inbox and exit")
    parser.add_argument("--watch", action="store_true", help="Poll inbox for new requests until stopped")
    parser.add_argument("--poll-sec", type=float, default=5.0, help="Poll interval seconds for --watch (default: 5)")
    parser.add_argument("--max-iterations", type=int, default=0, help="Stop after N watch iterations (0 = infinite)")
    args = parser.parse_args()

    store = TelegramRelayStore(args.implementations_root, args.impl_id)
    store.ensure_layout()
    def run_pass() -> int:
        inbox_files = sorted(store.paths.inbox.glob("*.md"))
        if not inbox_files:
            refresh_state(store)
            print("No inbox requests found.")
            return 0
        for req_path in inbox_files:
            status, ref = process_request_file(store, req_path)
            print(f"{req_path.name}: {status} -> {ref}")
        refresh_state(store)
        return len(inbox_files)

    if args.watch:
        import time
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
