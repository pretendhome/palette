#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import os
import re
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REDACT_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]+"),
    re.compile(r"nexos-team-[A-Za-z0-9]+"),
    re.compile(r"\b\d{9,}\b"),  # coarse sender ids/chat ids
]


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso_z(ts: dt.datetime | None = None) -> str:
    value = ts or utc_now()
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ts_slug(ts: dt.datetime | None = None) -> str:
    value = ts or utc_now()
    return value.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")


def sanitize_text(text: str | None) -> str:
    if not text:
        return ""
    out = text
    for pattern in REDACT_PATTERNS:
        out = pattern.sub("<redacted>", out)
    return out


def atomic_write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", delete=False, dir=str(path.parent), encoding="utf-8") as tmp:
        tmp.write(content)
        tmp_path = Path(tmp.name)
    os.replace(tmp_path, path)


def yaml_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    if text == "" or re.search(r"[:#\n]", text) or text.strip() != text:
        return json.dumps(text)
    return text


def render_frontmatter(data: dict[str, Any]) -> str:
    lines: list[str] = ["---"]
    for key, value in data.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {yaml_scalar(item)}")
        elif isinstance(value, dict):
            lines.append(f"{key}:")
            for sub_key, sub_value in value.items():
                lines.append(f"  {sub_key}: {yaml_scalar(sub_value)}")
        else:
            lines.append(f"{key}: {yaml_scalar(value)}")
    lines.append("---")
    return "\n".join(lines)


@dataclass
class RelayPaths:
    base: Path
    events: Path
    sessions: Path
    inbox: Path
    outbox: Path
    archive: Path
    state: Path
    index: Path
    idempotency_log: Path


class TelegramRelayStore:
    """Per-implementation artifact store for Telegram <-> Palette relay."""

    def __init__(self, implementations_root: str | Path, impl_id: str):
        self.impl_id = impl_id
        base = Path(implementations_root) / impl_id / "telegram"
        self.paths = RelayPaths(
            base=base,
            events=base / "events",
            sessions=base / "sessions",
            inbox=base / "inbox",
            outbox=base / "outbox",
            archive=base / "archive",
            state=base / "STATE.md",
            index=base / "index",
            idempotency_log=base / "index" / "idempotency_seen.jsonl",
        )

    def ensure_layout(self) -> None:
        for path in [
            self.paths.base,
            self.paths.events,
            self.paths.sessions,
            self.paths.inbox,
            self.paths.outbox,
            self.paths.archive,
            self.paths.index,
        ]:
            path.mkdir(parents=True, exist_ok=True)
        if not self.paths.state.exists():
            self._write_state(
                status_lines=[
                    "- Relay: active",
                    "- Telegram bridge: enabled",
                    "- Direct shell from Telegram: disabled",
                ],
                queue_counts={"Inbox pending": 0, "Outbox pending": 0, "Failed": 0},
                last_processed={},
            )

    def _event_file(self, ts: dt.datetime | None = None) -> Path:
        value = ts or utc_now()
        return self.paths.events / f"{value.astimezone(dt.timezone.utc).strftime('%Y-%m-%d')}.jsonl"

    def _new_id(self, prefix: str) -> str:
        return f"{prefix}_{utc_now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

    def new_trace_id(self, source: str = "telegram") -> str:
        return f"{source}-{self.impl_id}-{utc_now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:4]}"

    def append_event(self, event: dict[str, Any]) -> dict[str, Any]:
        self.ensure_layout()
        payload = dict(event)
        payload.setdefault("event_id", self._new_id("evt"))
        payload.setdefault("impl_id", self.impl_id)
        payload.setdefault("ts", iso_z())
        payload.setdefault("status", "recorded")
        payload.setdefault("provenance", "relay")
        if "message_text" in payload:
            payload["message_text"] = sanitize_text(str(payload["message_text"]))
        path = self._event_file()
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=True) + "\n")
        payload["_artifact_path"] = str(path)
        return payload

    def has_seen_idempotency(self, idempotency_key: str) -> bool:
        if not self.paths.idempotency_log.exists():
            return False
        with open(self.paths.idempotency_log, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("idempotency_key") == idempotency_key:
                    return True
        return False

    def mark_idempotency_seen(self, idempotency_key: str, trace_id: str, source_event_id: str | None = None) -> None:
        self.ensure_layout()
        row = {
            "ts": iso_z(),
            "impl_id": self.impl_id,
            "idempotency_key": idempotency_key,
            "trace_id": trace_id,
            "source_event_id": source_event_id,
        }
        with open(self.paths.idempotency_log, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=True) + "\n")

    def write_session_summary(
        self,
        *,
        session_id: str,
        trace_id: str,
        started_at: str,
        ended_at: str,
        summary: str,
        event_ids: list[str],
        source: str = "telegram",
        status: str = "completed",
        provider_observed: str | None = None,
        models_observed: list[str] | None = None,
        decisions: list[str] | None = None,
        open_questions: list[str] | None = None,
        next_actions: list[str] | None = None,
        safety_notes: list[str] | None = None,
    ) -> Path:
        self.ensure_layout()
        frontmatter = {
            "session_id": session_id,
            "impl_id": self.impl_id,
            "trace_id": trace_id,
            "source": source,
            "started_at": started_at,
            "ended_at": ended_at,
            "status": status,
            "event_count": len(event_ids),
            "provider_observed": provider_observed or "",
            "models_observed": models_observed or [],
            "contains_live_system_calls": False,
            "contains_orch_dispatch": False,
            "review_required": False,
        }
        parts = [
            render_frontmatter(frontmatter),
            "## Summary",
            sanitize_text(summary.strip()),
            "",
            "## Decisions",
        ]
        for item in (decisions or ["No explicit decisions recorded."]):
            parts.append(f"- {sanitize_text(item)}")
        parts.extend(["", "## Open Questions"])
        for item in (open_questions or ["None recorded."]):
            parts.append(f"- {sanitize_text(item)}")
        parts.extend(["", "## Next Actions"])
        for item in (next_actions or ["None."]):
            parts.append(f"- {sanitize_text(item)}")
        parts.extend(["", "## Evidence"])
        for event_id in event_ids:
            parts.append(f"- {event_id}")
        parts.extend(["", "## Safety Notes"])
        for item in (safety_notes or ["No elevated actions executed."]):
            parts.append(f"- {sanitize_text(item)}")
        content = "\n".join(parts).rstrip() + "\n"
        path = self.paths.sessions / f"{ts_slug()}_session.md"
        atomic_write_text(path, content)
        return path

    def write_request(
        self,
        *,
        trace_id: str,
        intent: str,
        user_request: str,
        requested_by: str,
        requested_by_label: str,
        target_agent: str = "orch",
        source_event_ids: list[str] | None = None,
        related_session: str | None = None,
        idempotency_key: str | None = None,
        risk: str = "low",
        publish_to_github_requested: bool = False,
        publish_target_path: str | None = None,
        publish_commit_message: str | None = None,
    ) -> Path:
        self.ensure_layout()
        request_id = self._new_id("req")
        frontmatter = {
            "request_id": request_id,
            "trace_id": trace_id,
            "impl_id": self.impl_id,
            "source": "telegram",
            "requested_by": requested_by,
            "requested_by_label": requested_by_label,
            "target_agent": target_agent,
            "intent": intent,
            "status": "new",
            "priority": "normal",
            "risk": risk,
            "created_at": iso_z(),
            "approval_required": False,
            "idempotency_key": idempotency_key or "",
            "related_session": related_session or "",
            "source_event_ids": source_event_ids or [],
            "publish_to_github_requested": publish_to_github_requested,
            "publish_to_github_approved": False,
            "publish_target_path": publish_target_path or "",
            "publish_commit_message": publish_commit_message or "",
        }
        body = "\n".join(
            [
                render_frontmatter(frontmatter),
                "## User Request",
                sanitize_text(user_request.strip()),
                "",
                "## Constraints",
                "- Do not fabricate live system state.",
                "- Explicitly mark whether any downstream call was live or inferred.",
                "",
                "## Expected Output",
                "- Concise response with assumptions",
            ]
        ).rstrip() + "\n"
        path = self.paths.inbox / f"{ts_slug()}_req_{intent}.md"
        atomic_write_text(path, body)
        return path

    def write_response(
        self,
        *,
        request_id: str,
        trace_id: str,
        intent: str,
        response_text: str,
        destination: str = "telegram",
        source: str = "orch",
        delivery_target: str | None = None,
        live_call: bool = False,
        evidence: dict[str, Any] | None = None,
        status: str = "completed",
        publish_to_github_requested: bool = False,
        publish_to_github_approved: bool = False,
        publish_target_path: str | None = None,
    ) -> Path:
        self.ensure_layout()
        response_id = self._new_id("resp")
        frontmatter = {
            "response_id": response_id,
            "request_id": request_id,
            "trace_id": trace_id,
            "impl_id": self.impl_id,
            "source": source,
            "destination": destination,
            "intent": intent,
            "status": status,
            "created_at": iso_z(),
            "completed_at": iso_z(),
            "delivery_status": "pending" if destination == "telegram" else "n/a",
            "delivery_channel": destination,
            "delivery_target": delivery_target or "",
            "approval_required": False,
            "publish_to_github_requested": publish_to_github_requested,
            "publish_to_github_approved": publish_to_github_approved,
            "publish_target_path": publish_target_path or "",
            "provenance": {
                "kind": "palette-agent",
                "agent": source,
                "live_call": live_call,
            },
        }
        if evidence:
            frontmatter["provenance"]["evidence"] = json.dumps(evidence, ensure_ascii=True)
        body = "\n".join(
            [
                render_frontmatter(frontmatter),
                "## Response",
                sanitize_text(response_text.strip()),
            ]
        ).rstrip() + "\n"
        path = self.paths.outbox / f"{ts_slug()}_resp_{intent}.md"
        atomic_write_text(path, body)
        return path

    def update_state(
        self,
        *,
        status_lines: list[str],
        queue_counts: dict[str, int],
        last_processed: dict[str, str],
        notes: list[str] | None = None,
    ) -> Path:
        self.ensure_layout()
        return self._write_state(
            status_lines=status_lines,
            queue_counts=queue_counts,
            last_processed=last_processed,
            notes=notes,
        )

    def _write_state(
        self,
        *,
        status_lines: list[str],
        queue_counts: dict[str, int],
        last_processed: dict[str, str],
        notes: list[str] | None = None,
    ) -> Path:
        fm = render_frontmatter(
            {
                "impl_id": self.impl_id,
                "relay_version": "v1",
                "updated_at": iso_z(),
            }
        )
        lines = [fm, "## Current Status", *status_lines, "", "## Last Processed"]
        if last_processed:
            for k, v in last_processed.items():
                lines.append(f"- {k}: {sanitize_text(v)}")
        else:
            lines.append("- None yet.")
        lines.extend(["", "## Queues"])
        for k, v in queue_counts.items():
            lines.append(f"- {k}: {v}")
        lines.extend(["", "## Notes"])
        for note in (notes or ["Append-only events + MD summaries enabled."]):
            lines.append(f"- {sanitize_text(note)}")
        content = "\n".join(lines).rstrip() + "\n"
        atomic_write_text(self.paths.state, content)
        return self.paths.state
