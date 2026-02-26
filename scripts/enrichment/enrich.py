#!/usr/bin/env python3
"""Palette Enrichment Pipeline — CLI entry point.

Usage:
  python3 scripts/enrichment/enrich.py --source github              # all eligible
  python3 scripts/enrichment/enrich.py --source github --profile PERSON-019
  python3 scripts/enrichment/enrich.py --source github --dry-run     # preview only
  python3 scripts/enrichment/enrich.py --scan-only                   # list targets

HandoffPacket (stdin JSON):
  {"task": "enrich profiles", "payload": {"source": "github", "profile_ids": ["PERSON-019"]}}
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
from datetime import datetime, timezone

from .config import PEOPLE_LIBRARY_PATH, github_token
from .audit_log import log_entry
from .yaml_updater import (
    load_people_library,
    find_profile,
    update_profile_field,
    save_people_library,
    run_validation,
)
from .github_intel import fetch_github_profile, profile_to_yaml_dict
from .profile_scanner import scan_profiles
from .crossref_regenerator import regenerate_crossref


def _run_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S") + "-" + uuid.uuid4().hex[:6]


def _parse_handoff(raw: str) -> dict | None:
    """Parse a HandoffPacket from stdin JSON."""
    try:
        packet = json.loads(raw)
        if packet.get("task") == "enrich profiles":
            return packet.get("payload", {})
    except (json.JSONDecodeError, AttributeError):
        pass
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Palette Enrichment Pipeline")
    parser.add_argument(
        "--source",
        choices=["github"],
        default="github",
        help="Enrichment source (default: github)",
    )
    parser.add_argument(
        "--profile",
        action="append",
        dest="profiles",
        help="Specific profile ID(s) to enrich (e.g. PERSON-019)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview targets without making changes",
    )
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="List enrichment targets and exit",
    )
    args = parser.parse_args(argv)

    # Check for HandoffPacket on stdin
    if not sys.stdin.isatty():
        stdin_raw = sys.stdin.read().strip()
        if stdin_raw:
            payload = _parse_handoff(stdin_raw)
            if payload:
                args.source = payload.get("source", args.source)
                if payload.get("profile_ids"):
                    args.profiles = payload["profile_ids"]

    run_id = _run_id()
    print(f"[enrich] run={run_id} source={args.source} dry_run={args.dry_run}")

    # Verify token (not needed for --scan-only or --dry-run)
    if args.source == "github" and not github_token() and not args.scan_only and not args.dry_run:
        print("[enrich] ERROR: GITHUB_TOKEN env var not set")
        log_entry(action="pipeline_start", error="GITHUB_TOKEN not set", pipeline_run_id=run_id)
        return 1

    # Load people library
    try:
        data, _raw_backup = load_people_library(PEOPLE_LIBRARY_PATH)
    except Exception as exc:
        print(f"[enrich] ERROR loading people library: {exc}")
        log_entry(action="pipeline_start", error=str(exc), pipeline_run_id=run_id)
        return 1

    # Scan for targets
    targets = scan_profiles(data, source=args.source, explicit_ids=args.profiles)

    if not targets:
        print("[enrich] No profiles need enrichment.")
        log_entry(action="pipeline_complete", source=args.source, pipeline_run_id=run_id)
        return 0

    print(f"[enrich] Found {len(targets)} target(s):")
    for t in targets:
        print(f"  {t.person_id} ({t.name}) @{t.github_handle} — {', '.join(t.reasons)} [pri={t.priority}]")

    if args.scan_only:
        return 0

    if args.dry_run:
        print("[enrich] Dry run — no changes made.")
        log_entry(
            action="dry_run",
            source=args.source,
            new_values={"targets": [t.person_id for t in targets]},
            pipeline_run_id=run_id,
        )
        return 0

    # Enrich each target
    log_entry(
        action="pipeline_start",
        source=args.source,
        new_values={"target_count": len(targets)},
        pipeline_run_id=run_id,
    )

    modified = 0
    errors = 0
    total_api_calls = 0

    for target in targets:
        print(f"\n[enrich] Fetching GitHub data for {target.person_id} (@{target.github_handle})...")
        try:
            gh_profile = fetch_github_profile(target.github_handle)
        except RuntimeError as exc:
            # Rate limit or network failure — stop pipeline
            print(f"[enrich] FATAL: {exc}")
            log_entry(
                action="fetch_error",
                person_id=target.person_id,
                source=args.source,
                error=str(exc),
                pipeline_run_id=run_id,
            )
            errors += 1
            break

        total_api_calls += gh_profile.api_calls

        if gh_profile.error:
            print(f"[enrich] SKIP {target.person_id}: {gh_profile.error}")
            log_entry(
                action="fetch_skip",
                person_id=target.person_id,
                source=args.source,
                error=gh_profile.error,
                api_calls=gh_profile.api_calls,
                pipeline_run_id=run_id,
            )
            continue

        # Transform to YAML-embeddable dict
        gh_data = profile_to_yaml_dict(gh_profile)

        # Apply update
        profile = find_profile(data, target.person_id)
        if profile is None:
            print(f"[enrich] WARNING: profile {target.person_id} not found in data — skipping")
            continue

        prev = update_profile_field(profile, "github_data", gh_data)
        # Update enrichment_date
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        update_profile_field(profile, "enrichment_date", today)

        log_entry(
            action="profile_enriched",
            person_id=target.person_id,
            source=args.source,
            fields_changed=["github_data", "enrichment_date"],
            previous_values={"github_data": prev} if prev else {},
            new_values={"github_data": gh_data},
            api_calls=gh_profile.api_calls,
            pipeline_run_id=run_id,
        )

        print(f"[enrich] Updated {target.person_id}: "
              f"{gh_profile.followers} followers, "
              f"{gh_profile.public_repos} repos, "
              f"{len(gh_profile.top_repos)} top repos, "
              f"{gh_profile.recent_commits_30d} recent commits")
        modified += 1

    # Save if any profiles modified
    if modified > 0:
        print(f"\n[enrich] Saving people library ({modified} profile(s) updated)...")
        save_people_library(data, PEOPLE_LIBRARY_PATH)

        print("[enrich] Regenerating crossref...")
        crossref_summary = regenerate_crossref(data)
        print(f"[enrich] Crossref: {crossref_summary['total_tools']} tools total, "
              f"{crossref_summary['added_count']} added, "
              f"{crossref_summary['updated_count']} updated")

        print("[enrich] Running validation...")
        valid = run_validation()
        if not valid:
            print("[enrich] WARNING: validation failed — check output above")

    # Summary
    print(f"\n{'='*60}")
    print(f"[enrich] DONE  run={run_id}")
    print(f"  targets:    {len(targets)}")
    print(f"  modified:   {modified}")
    print(f"  errors:     {errors}")
    print(f"  api_calls:  {total_api_calls}")
    print(f"{'='*60}")

    log_entry(
        action="pipeline_complete",
        source=args.source,
        new_values={
            "targets": len(targets),
            "modified": modified,
            "errors": errors,
            "api_calls": total_api_calls,
        },
        pipeline_run_id=run_id,
    )

    if errors > 0:
        return 2  # partial
    return 0


if __name__ == "__main__":
    sys.exit(main())
