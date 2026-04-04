#!/usr/bin/env python3
"""
bridge_feedback_to_proposals.py — Convert workspace feedback into governance proposals

Reads palette_feedback.yaml from workspaces, converts eligible entries
into governance proposals, and files them via file_proposal.py.

Usage:
    python3 scripts/bridge_feedback_to_proposals.py
    python3 scripts/bridge_feedback_to_proposals.py --workspace oil-investor
    python3 scripts/bridge_feedback_to_proposals.py --dry-run
"""
import argparse
import sys
from pathlib import Path

import yaml

PALETTE_ROOT = Path(__file__).resolve().parent.parent
FDE_ROOT = PALETTE_ROOT.parent
MISSIONCANVAS_ROOT = PALETTE_ROOT / "mission-canvas"
WORKSPACES_DIR = MISSIONCANVAS_ROOT / "workspaces"

sys.path.insert(0, str(PALETTE_ROOT / "scripts"))
from file_proposal import file_proposal


def load_feedback(workspace_dir):
    fb_path = workspace_dir / "palette_feedback.yaml"
    if not fb_path.exists():
        return []
    with open(fb_path) as f:
        data = yaml.safe_load(f)
    return data.get("feedback", [])


def concept_to_proposal(entry, workspace_id):
    """Convert a concept_exposure feedback entry to a Tier 2 proposal."""
    term = entry.get("term", "")
    question = entry.get("question", f"What is {term} and why does it matter?")
    concept_id = entry.get("concept_id", "")

    return {
        "proposed_by": "enrichment.bridge",
        "tier": 1,
        "type": "fix",
        "target": "LIB-NEW",
        "content": {
            "question": question,
            "answer": f"GAP SIGNAL: The concept '{term}' was detected during convergence chain "
                      f"narration in the {workspace_id} workspace but has no canonical KL entry. "
                      f"This is a gap signal filed by the enrichment bridge — it requires a domain "
                      f"expert or agent to enrich with substantive, sourced content (>100 words, "
                      f"at least one verifiable source) before it can be promoted to Tier 2 and "
                      f"enter the voting pipeline. The concept appeared in context: "
                      f"{entry.get('context', 'no context captured')}. "
                      f"Related workspace: {workspace_id}. Concept ID: {concept_id}.",
            "sources": [{"title": f"Workspace feedback: {workspace_id}", "url": f"workspaces/{workspace_id}/palette_feedback.yaml", "accessed": "2026-04-03"}],
            "related_rius": ["RIU-400"],
            "evidence_tier": 4,
            "evidence_tier_justification": "Auto-generated gap signal from workspace feedback. Not yet enriched.",
            "tags": [workspace_id, term.lower().replace(" ", "-"), "gap-signal"],
        },
        "rationale": f"Knowledge gap detected: '{term}' appeared in {workspace_id} workspace narration but has no canonical KL entry.",
        "source_of_insight": f"workspace feedback ({workspace_id}, entry {entry.get('id', 'unknown')})",
        "contradiction_check": {
            "checked_against": [],
            "conflicts_found": "none (new entry, no existing content to contradict)"
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Bridge workspace feedback to governance proposals")
    parser.add_argument("--workspace", help="Specific workspace to process")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--max", type=int, default=5, help="Max proposals to file per run")
    args = parser.parse_args()

    if args.workspace:
        workspaces = [WORKSPACES_DIR / args.workspace]
    else:
        workspaces = [d for d in WORKSPACES_DIR.iterdir() if d.is_dir()]

    filed = 0
    for ws_dir in workspaces:
        ws_id = ws_dir.name
        feedback = load_feedback(ws_dir)
        candidates = [e for e in feedback if e.get("type") == "concept_exposure" and e.get("status") == "candidate"]

        if not candidates:
            continue

        print(f"\n{ws_id}: {len(candidates)} candidate concept exposures")

        for entry in candidates[:args.max - filed]:
            prop = concept_to_proposal(entry, ws_id)
            if args.dry_run:
                print(f"  DRY RUN: would file proposal for '{entry.get('term', '?')}'")
            else:
                prop_id = file_proposal(prop_data=prop)
                if prop_id:
                    entry["status"] = "proposed"
                    entry["proposal_id"] = prop_id
                    filed += 1

            if filed >= args.max:
                break

        if not args.dry_run and filed > 0:
            # Save updated feedback with status changes
            fb_path = ws_dir / "palette_feedback.yaml"
            with open(fb_path) as f:
                data = yaml.safe_load(f)
            data["feedback"] = feedback
            with open(fb_path, "w") as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, width=120, sort_keys=False)

    print(f"\nTotal filed: {filed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
