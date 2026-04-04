#!/usr/bin/env python3
"""
file_proposal.py — File a governance proposal into wiki/proposed/

Usage:
    python3 scripts/file_proposal.py proposal.yaml
    python3 scripts/file_proposal.py --from-feedback oil-investor CS-OIL-001
    python3 scripts/file_proposal.py --interactive
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone, date
from pathlib import Path

import yaml

PALETTE_ROOT = Path(__file__).resolve().parent.parent
PROPOSED_DIR = PALETTE_ROOT / "wiki" / "proposed"
ARCHIVE_DIR = PROPOSED_DIR / "archive"
ROSTER_PATH = PROPOSED_DIR / "VOTING_ROSTER.yaml"
QUEUE_PATH = PROPOSED_DIR / "APPROVAL_QUEUE.md"
KL_PATH = PALETTE_ROOT / "knowledge-library" / "v1.4" / "palette_knowledge_library_v1.4.yaml"
TAXONOMY_PATH = PALETTE_ROOT / "taxonomy" / "releases" / "v1.3" / "palette_taxonomy_v1.3.yaml"

REQUIRED_FIELDS = ["proposed_by", "tier", "type", "content", "rationale", "source_of_insight"]

BUS_URL = "http://127.0.0.1:7899/send"


def notify_bus(from_agent, intent, content_text, requires_ack=False):
    """Best-effort bus notification. Does not fail if bus is unavailable."""
    try:
        import json
        import urllib.request
        import uuid
        msg = {
            "protocol_version": "1.0.0",
            "message_id": str(uuid.uuid4()),
            "thread_id": None,
            "in_reply_to": None,
            "from_agent": from_agent,
            "to_agent": "all",
            "message_type": "informational",
            "intent": intent,
            "risk_level": "none",
            "requires_ack": requires_ack,
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
        pass  # Bus notification is best-effort
VALID_TYPES = {"new", "modify", "remap", "retag", "fix"}
VALID_TIERS = {1, 2, 3}


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def today_str():
    return date.today().isoformat()


def next_prop_id():
    today = today_str()
    # Check both proposed/ and archive/ for existing IDs
    existing = list(PROPOSED_DIR.glob("PROP-*.yaml"))
    if ARCHIVE_DIR.exists():
        existing += list(ARCHIVE_DIR.glob("PROP-*.yaml"))
    today_count = sum(1 for f in existing if today in f.name)
    return f"PROP-{today}-{today_count + 1:03d}"


def load_roster():
    if not ROSTER_PATH.exists():
        return {"roster": [], "quorum_minimum": 2}
    with open(ROSTER_PATH) as f:
        return yaml.safe_load(f)


def load_taxonomy_rius():
    with open(TAXONOMY_PATH) as f:
        tax = yaml.safe_load(f)
    return {r["riu_id"] for r in tax.get("rius", [])}


def load_kl_ids():
    with open(KL_PATH) as f:
        kl = yaml.safe_load(f)
    ids = set()
    for section in ["library_questions", "gap_additions", "context_specific_questions"]:
        for e in kl.get(section, []):
            ids.add(e["id"])
    return ids


def validate_proposal(prop):
    errors = []
    for f in REQUIRED_FIELDS:
        if f not in prop:
            errors.append(f"Missing required field: {f}")

    if prop.get("tier") not in VALID_TIERS:
        errors.append(f"Invalid tier: {prop.get('tier')}. Must be 1, 2, or 3.")

    if prop.get("type") not in VALID_TYPES:
        errors.append(f"Invalid type: {prop.get('type')}. Must be one of {VALID_TYPES}.")

    content = prop.get("content", {})
    if prop.get("tier", 0) >= 2:
        if not content.get("question"):
            errors.append("Tier 2+ requires content.question")
        if not content.get("answer") or len(content.get("answer", "")) < 100:
            errors.append("Tier 2+ requires content.answer > 100 words")
        if not content.get("sources"):
            errors.append("Tier 2+ requires at least one source with URL")
        else:
            for s in content["sources"]:
                if not s.get("url"):
                    errors.append(f"Source missing URL: {s.get('title','untitled')}")
        if not content.get("related_rius"):
            errors.append("Tier 2+ requires at least one related_rius")
        else:
            valid_rius = load_taxonomy_rius()
            for riu in content["related_rius"]:
                if riu not in valid_rius:
                    errors.append(f"Invalid RIU: {riu} not in taxonomy")
        if not content.get("evidence_tier_justification"):
            errors.append("Tier 2+ requires evidence_tier_justification")

    if not prop.get("contradiction_check"):
        errors.append("Missing contradiction_check section")

    return errors


def render_proposed_page(prop):
    prop_id = prop["id"]
    votes = prop.get("votes", [])
    binding = sum(1 for v in votes if v.get("binding", True) and v.get("vote") == "approve")
    total_binding = len([a for a in load_roster().get("roster", []) if a.get("binding")])
    expires = "14 days from filing"

    lines = [
        "---",
        "STATUS: PROPOSED — NOT YET IN CANONICAL KNOWLEDGE LIBRARY",
        f"proposed_by: {prop['proposed_by']}",
        f"votes: {binding}/{total_binding} binding approve",
        f"expires: {expires}",
        f"DO_NOT_EDIT: This file is auto-generated from {prop_id}.yaml",
        "---",
        "",
        f"# {prop.get('content', {}).get('question', prop_id)}",
        "",
        f"**Proposal ID**: {prop_id}",
        f"**Tier**: {prop['tier']}",
        f"**Type**: {prop['type']}",
        f"**Proposed by**: {prop['proposed_by']}",
        f"**Rationale**: {prop.get('rationale', '')}",
        "",
        "## Proposed Content",
        "",
        prop.get("content", {}).get("answer", ""),
        "",
    ]

    sources = prop.get("content", {}).get("sources", [])
    if sources:
        lines.append("## Evidence")
        lines.append("")
        for s in sources:
            lines.append(f"- [{s.get('title','')}]({s.get('url','')})")
        lines.append("")

    lines.append("## Votes")
    lines.append("")
    if votes:
        for v in votes:
            binding_str = "binding" if v.get("binding", True) else "advisory"
            lines.append(f"- **{v['agent_id']}** ({binding_str}): {v['vote']} — {v.get('reasoning','')}")
    else:
        lines.append("*No votes yet.*")
    lines.append("")

    return "\n".join(lines)


def generate_approval_queue():
    proposals = sorted(PROPOSED_DIR.glob("PROP-*.yaml"))
    if not proposals:
        content = "<!-- DO NOT EDIT — auto-generated by wiki governance pipeline -->\n\n# Approval Queue\n\nNo pending proposals.\n"
        QUEUE_PATH.write_text(content)
        return

    lines = [
        "<!-- DO NOT EDIT — auto-generated by wiki governance pipeline -->",
        "",
        "# Approval Queue",
        "",
        f"{len(proposals)} pending proposal(s).",
        "",
    ]

    roster = load_roster()
    total_binding = len([a for a in roster.get("roster", []) if a.get("binding")])

    for pf in proposals:
        with open(pf) as f:
            prop = yaml.safe_load(f)
        prop_id = prop.get("id", pf.stem)
        votes = prop.get("votes", [])
        approves = [v for v in votes if v.get("vote") == "approve" and v.get("binding", True)]
        objects = [v for v in votes if v.get("vote") in ("object", "object-with-alternative") and v.get("binding", True)]
        pending = total_binding - len(approves) - len(objects)
        question = prop.get("content", {}).get("question", "No question")[:80]

        lines.append(f"### {prop_id}")
        lines.append(f"- **Question**: {question}")
        lines.append(f"- **Tier**: {prop.get('tier')}")
        lines.append(f"- **Proposed by**: {prop.get('proposed_by')}")
        lines.append(f"- **Votes**: {len(approves)}/{total_binding} approve, {len(objects)} object, {pending} pending")
        if objects:
            for o in objects:
                lines.append(f"- **Objection**: {o.get('agent_id')} — {o.get('reasoning','')[:100]}")
        status = prop.get("status", "open")
        lines.append(f"- **Status**: {status}")
        lines.append("")

    QUEUE_PATH.write_text("\n".join(lines))


def file_proposal(prop_path=None, prop_data=None):
    if prop_path:
        with open(prop_path) as f:
            prop = yaml.safe_load(f)
    elif prop_data:
        prop = prop_data
    else:
        raise ValueError("Need prop_path or prop_data")

    # Assign ID and timestamp
    prop_id = next_prop_id()
    prop["id"] = prop_id
    prop["proposed_at"] = utc_now()
    prop["status"] = "open"
    prop.setdefault("votes", [])
    # Set expiry date (14 days from filing per governance model)
    from datetime import timedelta
    prop["expires"] = (datetime.now(timezone.utc) + timedelta(days=14)).strftime("%Y-%m-%d")

    # Check resubmission limit (max 3 attempts per topic per governance model)
    resubmission_of = prop.get("resubmission_of")
    if resubmission_of:
        # Count archived proposals with same resubmission chain
        chain_count = 0
        if ARCHIVE_DIR.exists():
            for af in ARCHIVE_DIR.glob("PROP-*.yaml"):
                with open(af) as f:
                    archived = yaml.safe_load(f)
                if (archived.get("resubmission_of") == resubmission_of or
                        archived.get("id") == resubmission_of):
                    chain_count += 1
        if chain_count >= 3:
            print(f"REJECTED: Topic has been submitted {chain_count} times (max 3). "
                  f"Original: {resubmission_of}")
            return None
        prop["resubmission_count"] = chain_count + 1

    # Validate
    errors = validate_proposal(prop)
    if errors:
        print(f"VALIDATION FAILED for {prop_id}:")
        for e in errors:
            print(f"  - {e}")
        return None

    # Ensure directories
    PROPOSED_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    # Write proposal YAML
    yaml_path = PROPOSED_DIR / f"{prop_id}.yaml"
    with open(yaml_path, "w") as f:
        yaml.dump(prop, f, default_flow_style=False, allow_unicode=True, width=120, sort_keys=False)

    # Write rendered page
    md_path = PROPOSED_DIR / f"{prop_id}.md"
    md_path.write_text(render_proposed_page(prop))

    # Regenerate queue
    generate_approval_queue()

    print(f"FILED: {prop_id}")
    print(f"  YAML: {yaml_path}")
    print(f"  Page: {md_path}")
    print(f"  Queue: {QUEUE_PATH}")

    # Notify bus — vote request
    question = prop.get("content", {}).get("question", prop_id)[:80]
    notify_bus(
        prop.get("proposed_by", "governance.pipeline"),
        f"NEW PROPOSAL: {prop_id} — {question}. Vote required.",
        f"New proposal filed: {prop_id}\nQuestion: {question}\n"
        f"Tier: {prop.get('tier')}\nType: {prop.get('type')}\n"
        f"Review and vote: wiki/proposed/{prop_id}.yaml",
        requires_ack=True,
    )

    return prop_id


def check_expiry():
    """Expire proposals past their 14-day deadline."""
    today = date.today().isoformat()
    proposals = sorted(PROPOSED_DIR.glob("PROP-*.yaml"))
    expired = 0
    for pf in proposals:
        with open(pf) as f:
            prop = yaml.safe_load(f)
        expires = prop.get("expires", "")
        status = prop.get("status", "open")
        if expires and expires < today and status in ("open", "voting"):
            prop["status"] = "expired"
            prop["resolution"] = f"Auto-expired on {today} (filed {prop.get('proposed_at', '?')})"
            # Archive
            ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
            archive_path = ARCHIVE_DIR / pf.name
            with open(archive_path, "w") as f:
                yaml.dump(prop, f, default_flow_style=False, allow_unicode=True, width=120, sort_keys=False)
            pf.unlink()
            md_path = PROPOSED_DIR / f"{pf.stem}.md"
            if md_path.exists():
                md_path.unlink()
            expired += 1
            print(f"EXPIRED: {pf.stem} (was {status}, expires {expires})")
    if expired:
        generate_approval_queue()
    print(f"{expired} proposal(s) expired. {len(proposals) - expired} remaining.")


def main():
    parser = argparse.ArgumentParser(description="File a governance proposal")
    parser.add_argument("proposal", nargs="?", help="Path to proposal YAML file")
    parser.add_argument("--regenerate-queue", action="store_true", help="Just regenerate APPROVAL_QUEUE.md")
    parser.add_argument("--check-expiry", action="store_true", help="Expire proposals past their 14-day deadline")
    args = parser.parse_args()

    if args.check_expiry:
        check_expiry()
        return 0

    if args.regenerate_queue:
        generate_approval_queue()
        print(f"Queue regenerated: {QUEUE_PATH}")
        return 0

    if not args.proposal:
        parser.print_help()
        return 1

    result = file_proposal(prop_path=args.proposal)
    return 0 if result else 1


if __name__ == "__main__":
    sys.exit(main())
