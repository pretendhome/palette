"""Regenerate people_library_company_signals from people_library (merge, not replace)."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

from .config import PEOPLE_LIBRARY_PATH, CROSSREF_PATH

yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 4096


def _extract_tools_from_profiles(data: Any) -> dict[str, list[dict]]:
    """Scan people_library for all notable_recommendations.tools.

    Returns {tool_name: [{id, name, reason/note, signal_strength}]}.
    """
    tools_map: dict[str, list[dict]] = {}
    profiles = data.get("profiles")
    if profiles is None:
        return tools_map

    for profile in profiles:
        if profile.get("status") == "archived":
            continue
        pid = profile.get("id", "")
        pname = profile.get("name", "")
        recs = profile.get("notable_recommendations")
        if not recs:
            continue
        tools = recs.get("tools")
        if not tools:
            continue
        for tool in tools:
            tool_name = tool.get("name", "")
            if not tool_name:
                continue
            entry: dict[str, str] = {"id": pid, "name": pname}
            if tool.get("reason"):
                entry["reason"] = tool["reason"]
            if tool.get("note"):
                entry["note"] = tool["note"]
            tools_map.setdefault(tool_name, []).append(entry)

    return tools_map


def regenerate_crossref(
    people_data: Any,
    *,
    crossref_path: Path | None = None,
    dry_run: bool = False,
) -> dict[str, Any]:
    """Merge-regenerate the company signals crossref.

    Strategy: scan people_library for all tools → for each tool, update
    the recommender list in the existing crossref.  Preserve human-curated
    fields (riu_primary, riu_secondary, palette_action, taxonomy_gap).
    New tools get added with palette_action=evaluate.

    Returns summary dict.
    """
    crossref_path = crossref_path or CROSSREF_PATH

    # Load existing crossref (may be multi-document)
    if crossref_path.exists():
        docs = list(yaml.load_all(crossref_path))
        existing: dict = {}
        for doc in docs:
            if doc is not None:
                existing.update(doc)
    else:
        existing = {"metadata": {}, "signals": []}

    existing_signals = existing.get("signals") or []

    # Index existing signals by tool name
    existing_by_tool: dict[str, Any] = {}
    for sig in existing_signals:
        tool_name = sig.get("tool", "")
        if tool_name:
            existing_by_tool[tool_name] = sig

    # Extract fresh tools from people_library
    fresh_tools = _extract_tools_from_profiles(people_data)

    added: list[str] = []
    updated: list[str] = []

    for tool_name, recommenders in fresh_tools.items():
        if tool_name in existing_by_tool:
            # Update recommenders list only — preserve curated fields
            sig = existing_by_tool[tool_name]
            old_recs = {r.get("id") for r in (sig.get("recommenders") or [])}
            new_recs = [r for r in recommenders if r["id"] not in old_recs]
            if new_recs:
                sig.setdefault("recommenders", []).extend(new_recs)
                updated.append(tool_name)
                # Update signal tier based on recommender count
                count = len(sig.get("recommenders", []))
                if count >= 3:
                    sig["signal_tier"] = 1
                    sig["aggregate_signal_strength"] = "high"
                elif count >= 2:
                    sig["signal_tier"] = 2
                    sig["aggregate_signal_strength"] = "medium"
        else:
            # New tool — add with defaults
            new_signal = {
                "tool": tool_name,
                "signal_tier": 3 if len(recommenders) < 2 else 2,
                "aggregate_signal_strength": "medium" if len(recommenders) >= 2 else "low",
                "recommenders": recommenders,
                "company_library_status": "needs_entry",
                "palette_action": "evaluate",
                "taxonomy_gap": False,
            }
            existing_signals.append(new_signal)
            added.append(tool_name)

    # Update metadata
    meta = existing.get("metadata") or {}
    meta["total_tools_tracked"] = len(existing_signals)
    tier_counts = {1: 0, 2: 0, 3: 0}
    for sig in existing_signals:
        tier = sig.get("signal_tier", 3)
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
    meta["tier_1_tools"] = tier_counts[1]
    meta["tier_2_tools"] = tier_counts[2]
    meta["tier_3_tools"] = tier_counts[3]
    existing["metadata"] = meta
    existing["signals"] = existing_signals

    summary = {
        "total_tools": len(existing_signals),
        "added": added,
        "updated": updated,
        "added_count": len(added),
        "updated_count": len(updated),
    }

    if not dry_run:
        import shutil
        from ruamel.yaml.comments import CommentedMap

        if crossref_path.exists():
            shutil.copy2(crossref_path, crossref_path.with_suffix(".yaml.bak"))

        # Write as multi-doc (metadata | signals) to match original format
        doc1 = CommentedMap()
        doc2 = CommentedMap()
        for key in existing:
            if key == "signals":
                doc2[key] = existing[key]
            else:
                doc1[key] = existing[key]

        with open(crossref_path, "w", encoding="utf-8") as f:
            yaml.dump(doc1, f)
            f.write("\n---\n\n")
            yaml.dump(doc2, f)
        # Re-parse to validate
        list(yaml.load_all(crossref_path))

    return summary
