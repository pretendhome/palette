"""Profile scanner — determines which profiles need enrichment."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import Any

from .config import STALE_THRESHOLD_DAYS


QUALITY_PRIORITY = {"high": 0, "medium": 1, "low": 2, "unvalidated": 3}


@dataclass
class EnrichmentTarget:
    person_id: str
    name: str
    github_handle: str
    reasons: list[str] = field(default_factory=list)
    priority: int = 99  # lower = higher priority


def scan_profiles(
    data: Any,
    *,
    source: str = "github",
    explicit_ids: list[str] | None = None,
) -> list[EnrichmentTarget]:
    """Scan people_library data and return ordered targets needing enrichment.

    Triggers (any of):
      1. Profile has ``github`` in ``platforms`` but no ``github_data`` section
      2. ``enrichment_date`` older than STALE_THRESHOLD_DAYS
      3. Explicitly requested via ``explicit_ids``

    Priority: explicit > high stale > missing data > medium > low.
    """
    profiles = data.get("profiles")
    if profiles is None:
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=STALE_THRESHOLD_DAYS)
    targets: list[EnrichmentTarget] = []

    for profile in profiles:
        pid = profile.get("id", "")
        name = profile.get("name", "")
        status = profile.get("status", "active")
        if status == "archived":
            continue

        # Resolve github handle
        platforms = profile.get("platforms") or {}
        gh_entry = platforms.get("github")
        if isinstance(gh_entry, dict):
            gh_handle = gh_entry.get("handle") or gh_entry.get("username", "")
        elif isinstance(gh_entry, str):
            gh_handle = gh_entry
        else:
            gh_handle = ""

        # When explicit_ids provided, only consider those profiles
        if explicit_ids and pid not in explicit_ids:
            continue

        if not gh_handle:
            if explicit_ids and pid in explicit_ids:
                # Explicitly requested but no handle — skip with note
                continue
            else:
                continue  # no github handle

        reasons: list[str] = []
        priority = 50

        # Trigger 3: explicit request (highest priority)
        if explicit_ids and pid in explicit_ids:
            reasons.append("explicitly requested")
            priority = 0

        # Trigger 1: has handle but no github_data
        if gh_handle and not profile.get("github_data"):
            reasons.append("missing github_data")
            if priority > 10:
                priority = 10

        # Trigger 2: stale enrichment_date
        enrich_date_str = profile.get("enrichment_date", "")
        if enrich_date_str:
            try:
                enrich_date = datetime.strptime(enrich_date_str, "%Y-%m-%d").replace(
                    tzinfo=timezone.utc
                )
                if enrich_date < cutoff:
                    reasons.append(
                        f"enrichment_date {enrich_date_str} older than {STALE_THRESHOLD_DAYS}d"
                    )
                    if priority > 20:
                        priority = 20
            except ValueError:
                pass

        if not reasons:
            continue

        # Adjust by signal quality
        quality = profile.get("signal_quality", "unvalidated")
        quality_offset = QUALITY_PRIORITY.get(quality, 3)
        priority += quality_offset

        targets.append(
            EnrichmentTarget(
                person_id=pid,
                name=name,
                github_handle=gh_handle,
                reasons=reasons,
                priority=priority,
            )
        )

    targets.sort(key=lambda t: t.priority)
    return targets
