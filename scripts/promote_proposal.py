#!/usr/bin/env python3
"""
promote_proposal.py — Promote an approved proposal to canonical KL

Usage:
    python3 scripts/promote_proposal.py PROP-2026-04-03-001
    python3 scripts/promote_proposal.py PROP-2026-04-03-001 --dry-run
"""
import argparse
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

PALETTE_ROOT = Path(__file__).resolve().parent.parent
PROPOSED_DIR = PALETTE_ROOT / "wiki" / "proposed"
ARCHIVE_DIR = PROPOSED_DIR / "archive"
KL_PATH = PALETTE_ROOT / "knowledge-library" / "v1.4" / "palette_knowledge_library_v1.4.yaml"

BUS_URL = "http://127.0.0.1:7899/send"


def notify_bus(intent, content_text):
    """Best-effort bus notification."""
    try:
        import json
        import urllib.request
        import uuid
        msg = {
            "protocol_version": "1.0.0",
            "message_id": str(uuid.uuid4()),
            "thread_id": None,
            "in_reply_to": None,
            "from_agent": "governance.pipeline",
            "to_agent": "all",
            "message_type": "informational",
            "intent": intent,
            "risk_level": "none",
            "requires_ack": False,
            "payload": {"content": content_text},
            "created_at": datetime.now(timezone.utc).isoformat(),
            "ttl_seconds": 0,
        }
        req = urllib.request.Request(
            BUS_URL,
            data=json.dumps(msg).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass


def next_lib_id(kl):
    max_id = 0
    for section in ["library_questions", "gap_additions", "context_specific_questions"]:
        for e in kl.get(section, []):
            eid = e.get("id", "")
            if eid.startswith("LIB-"):
                try:
                    num = int(eid.split("-")[1])
                    max_id = max(max_id, num)
                except ValueError:
                    pass
    return f"LIB-{max_id + 1:03d}"


def promote(prop_id, dry_run=False):
    prop_path = PROPOSED_DIR / f"{prop_id}.yaml"
    if not prop_path.exists():
        print(f"ERROR: {prop_id} not found")
        return False

    with open(prop_path) as f:
        prop = yaml.safe_load(f)

    if prop.get("status") != "approved":
        print(f"ERROR: {prop_id} status is '{prop.get('status')}', not 'approved'")
        return False

    content = prop.get("content", {})
    with open(KL_PATH) as f:
        kl = yaml.safe_load(f)

    # Determine target ID
    target = prop.get("target", "LIB-NEW")
    if target == "LIB-NEW":
        target = next_lib_id(kl)

    # Build KL entry — honor all canonical fields from proposal, default where missing
    entry = {
        "id": target,
        "question": content.get("question", ""),
        "answer": content.get("answer", ""),
        "sources": content.get("sources", []),
        "related_rius": content.get("related_rius", []),
        "evidence_tier": content.get("evidence_tier", 3),
        "tags": content.get("tags", []),
        "journey_stage": content.get("journey_stage", "foundation"),
        "difficulty": content.get("difficulty", "medium"),
    }
    # Preserve optional canonical fields if present in proposal
    for optional in ("problem_type", "industries"):
        if content.get(optional):
            entry[optional] = content[optional]

    print(f"PROMOTING {prop_id} as {target}")
    print(f"  Question: {entry['question'][:80]}")
    print(f"  Sources: {len(entry['sources'])}")
    print(f"  RIUs: {entry['related_rius']}")

    if dry_run:
        print("DRY RUN — no changes made")
        return True

    # Append to the correct KL section (default: gap_additions)
    target_section = prop.get("target_section", "gap_additions")
    if target_section not in ("library_questions", "gap_additions", "context_specific_questions"):
        target_section = "gap_additions"
    kl.setdefault(target_section, []).append(entry)

    with open(KL_PATH, "w") as f:
        yaml.dump(kl, f, default_flow_style=False, allow_unicode=True, width=120, sort_keys=False)

    # Update proposal status
    prop["status"] = "promoted"
    prop["promoted_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    prop["promoted_as"] = target

    # Archive
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archive_path = ARCHIVE_DIR / f"{prop_id}.yaml"
    with open(archive_path, "w") as f:
        yaml.dump(prop, f, default_flow_style=False, allow_unicode=True, width=120, sort_keys=False)

    # Remove from proposed/
    prop_path.unlink()
    md_path = PROPOSED_DIR / f"{prop_id}.md"
    if md_path.exists():
        md_path.unlink()

    # Recompile and validate
    print("Recompiling wiki...")
    result = subprocess.run(
        [sys.executable, str(PALETTE_ROOT / "scripts" / "compile_wiki.py")],
        capture_output=True, text=True
    )
    print(result.stdout.split("\n")[-2] if result.stdout else "compile done")

    print("Validating...")
    result = subprocess.run(
        [sys.executable, str(PALETTE_ROOT / "scripts" / "validate_wiki.py")],
        capture_output=True, text=True
    )
    if "Overall: PASS" in result.stdout:
        print("VALIDATION: PASS")
    else:
        print("VALIDATION: FAIL — check output")
        print(result.stdout[-500:])

    # Regenerate queue
    sys.path.insert(0, str(PALETTE_ROOT / "scripts"))
    from file_proposal import generate_approval_queue
    generate_approval_queue()

    print(f"\nPROMOTED: {prop_id} → {target}")
    print(f"  Archived: {archive_path}")

    # Notify bus
    question = content.get("question", prop_id)[:80]
    notify_bus(
        f"PROMOTED: {prop_id} → {target} — {question}",
        f"Proposal {prop_id} promoted to canonical KL as {target}.\n"
        f"Question: {question}\nArchived: {archive_path}",
    )

    return True


def main():
    parser = argparse.ArgumentParser(description="Promote an approved proposal to canonical KL")
    parser.add_argument("prop_id", help="Proposal ID")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without changing anything")
    args = parser.parse_args()

    ok = promote(args.prop_id, dry_run=args.dry_run)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
