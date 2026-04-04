#!/usr/bin/env python3
"""
record_vote.py — Record a vote on a governance proposal

Usage:
    python3 scripts/record_vote.py PROP-2026-04-03-001 approve kiro.design "Meets all criteria"
    python3 scripts/record_vote.py PROP-2026-04-03-001 object claude.analysis "Source not verifiable"
    python3 scripts/record_vote.py PROP-2026-04-03-001 object-with-alternative codex.implementation "Better approach" --alternative alt.yaml
"""
import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

PALETTE_ROOT = Path(__file__).resolve().parent.parent
PROPOSED_DIR = PALETTE_ROOT / "wiki" / "proposed"
ARCHIVE_DIR = PROPOSED_DIR / "archive"
ROSTER_PATH = PROPOSED_DIR / "VOTING_ROSTER.yaml"

VALID_VOTES = {"approve", "object", "object-with-alternative"}

BUS_URL = "http://127.0.0.1:7899/send"


def notify_bus(from_agent, intent, content_text):
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
            "from_agent": from_agent,
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


def load_roster():
    with open(ROSTER_PATH) as f:
        return yaml.safe_load(f)


def get_agent_status(roster, agent_id):
    for a in roster.get("roster", []):
        if a["agent_id"] == agent_id:
            return {"binding": True, "trust_tier": a.get("trust_tier", "WORKING")}
    for a in roster.get("advisory_agents", []):
        if a["agent_id"] == agent_id:
            return {"binding": False, "trust_tier": a.get("trust_tier", "UNVALIDATED")}
    return None


def check_unanimous(prop, roster):
    binding_agents = {a["agent_id"] for a in roster.get("roster", []) if a.get("binding")}
    quorum_min = roster.get("quorum_minimum", 2)
    votes = prop.get("votes", [])

    binding_approves = set()
    binding_objects = set()
    binding_voted = set()

    for v in votes:
        if not v.get("binding", True):
            continue
        aid = v["agent_id"]
        binding_voted.add(aid)
        if v["vote"] == "approve":
            binding_approves.add(aid)
        elif v["vote"] in ("object", "object-with-alternative"):
            binding_objects.add(aid)

    # Any objection blocks
    if binding_objects:
        return "objected", binding_objects

    # Check unanimous among those who voted
    if len(binding_approves) >= quorum_min and binding_approves == binding_voted:
        # Check if all roster agents voted or timed out
        not_voted = binding_agents - binding_voted
        if not not_voted:
            return "unanimous", binding_approves
        # Abstain-timeout rule: if remaining are unanimous and quorum met, OK
        if len(binding_approves) >= quorum_min:
            return "unanimous_with_abstain", binding_approves

    return "pending", binding_approves


def record_vote(prop_id, vote, agent_id, reasoning, alternative_path=None):
    prop_path = PROPOSED_DIR / f"{prop_id}.yaml"
    if not prop_path.exists():
        print(f"ERROR: Proposal {prop_id} not found at {prop_path}")
        return False

    if vote not in VALID_VOTES:
        print(f"ERROR: Invalid vote '{vote}'. Must be one of {VALID_VOTES}")
        return False

    if vote in ("object", "object-with-alternative") and not reasoning:
        print("ERROR: object votes require reasoning")
        return False

    roster = load_roster()
    agent_status = get_agent_status(roster, agent_id)
    if not agent_status:
        print(f"ERROR: {agent_id} not on voting roster")
        return False

    with open(prop_path) as f:
        prop = yaml.safe_load(f)

    # Check for duplicate vote
    existing = [v for v in prop.get("votes", []) if v["agent_id"] == agent_id]
    if existing:
        print(f"WARNING: {agent_id} already voted. Replacing previous vote.")
        prop["votes"] = [v for v in prop["votes"] if v["agent_id"] != agent_id]

    vote_entry = {
        "agent_id": agent_id,
        "trust_tier": agent_status["trust_tier"],
        "vote": vote,
        "reasoning": reasoning,
        "binding": agent_status["binding"],
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    if vote == "object-with-alternative" and alternative_path:
        with open(alternative_path) as f:
            vote_entry["alternative"] = yaml.safe_load(f)

    prop.setdefault("votes", []).append(vote_entry)

    # Check outcome
    outcome, agents = check_unanimous(prop, roster)

    if outcome == "objected":
        prop["status"] = "objected"
        print(f"OBJECTION by {agents}. Proposal escalated.")
        notify_bus(agent_id, f"OBJECTION on {prop_id} by {agent_id}",
                   f"{prop_id} objected by {agent_id}: {reasoning[:200]}")
    elif outcome in ("unanimous", "unanimous_with_abstain"):
        prop["status"] = "approved"
        print(f"UNANIMOUS APPROVAL ({len(agents)} binding votes). Ready for promotion.")
        notify_bus(agent_id, f"APPROVED: {prop_id} — unanimous ({len(agents)} binding votes). Ready for promotion.",
                   f"{prop_id} approved unanimously. Ready for: python3 scripts/promote_proposal.py {prop_id}")
    else:
        prop["status"] = "voting"
        print(f"Vote recorded. Status: voting ({len(agents)} approve so far)")

    with open(prop_path, "w") as f:
        yaml.dump(prop, f, default_flow_style=False, allow_unicode=True, width=120, sort_keys=False)

    # Regenerate rendered page and queue
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from file_proposal import render_proposed_page, generate_approval_queue
    md_path = PROPOSED_DIR / f"{prop_id}.md"
    md_path.write_text(render_proposed_page(prop))
    generate_approval_queue()

    return True


def main():
    parser = argparse.ArgumentParser(description="Record a vote on a proposal")
    parser.add_argument("prop_id", help="Proposal ID (e.g., PROP-2026-04-03-001)")
    parser.add_argument("vote", choices=VALID_VOTES, help="Vote type")
    parser.add_argument("agent_id", help="Voting agent identity")
    parser.add_argument("reasoning", help="Written reasoning for the vote")
    parser.add_argument("--alternative", help="Path to alternative proposal YAML (for object-with-alternative)")
    args = parser.parse_args()

    ok = record_vote(args.prop_id, args.vote, args.agent_id, args.reasoning, args.alternative)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
