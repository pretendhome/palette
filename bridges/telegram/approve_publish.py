#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from relay_consumer import parse_frontmatter_md
from relay_store import TelegramRelayStore, atomic_write_text, iso_z


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Approve or revoke GitHub publish metadata on relay outbox artifacts")
    parser.add_argument("--impl-id", required=True)
    parser.add_argument("--artifact", required=True, help="Path to outbox artifact")
    parser.add_argument("--approve", action="store_true", help="Set publish_to_github_approved=true")
    parser.add_argument("--revoke", action="store_true", help="Set publish_to_github_approved=false")
    parser.add_argument("--approved-by", default="manual", help="Approver label (default: manual)")
    parser.add_argument("--implementations-root", default="/home/mical/fde/implementations")
    args = parser.parse_args()

    if args.approve == args.revoke:
        parser.error("Choose exactly one of --approve or --revoke")

    artifact = Path(args.artifact)
    if not artifact.exists():
        parser.error(f"Artifact not found: {artifact}")

    store = TelegramRelayStore(args.implementations_root, args.impl_id)
    fm, body = parse_frontmatter_md(artifact)
    trace_id = str(fm.get("trace_id", "")) or store.new_trace_id("approve")

    requested = str(fm.get("publish_to_github_requested", "false")).lower() == "true" or fm.get("publish_to_github_requested") is True
    if not requested:
        parser.error("Artifact does not request GitHub publish (`publish_to_github_requested` is false)")

    approved = args.approve
    fm["publish_to_github_approved"] = approved
    fm["publish_approved_by"] = args.approved_by
    fm["publish_approved_at"] = iso_z() if approved else ""

    patch_top_level_frontmatter(
        artifact,
        {
            "publish_to_github_approved": approved,
            "publish_approved_by": args.approved_by,
            "publish_approved_at": iso_z() if approved else "",
        },
    )

    store.append_event(
        {
            "trace_id": trace_id,
            "source": "relay-approve",
            "direction": "internal",
            "status": "publish_approval_updated",
            "artifact_path": str(artifact),
            "publish_to_github_approved": approved,
            "publish_approved_by": args.approved_by,
            "provenance": "approve_publish",
        }
    )

    state = "approved" if approved else "revoked"
    print(f"{artifact.name}: publish approval {state} by {args.approved_by}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
