"""Round-trip YAML editing using ruamel.yaml for parsing, text insertion for saving."""
from __future__ import annotations

import io
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML

from .config import VALIDATION_SCRIPT

yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 4096  # prevent unwanted line wrapping


def load_people_library(path: Path) -> tuple[Any, bytes]:
    """Load people library YAML (multi-document: metadata + profiles).

    Returns (merged dict with both 'metadata' and 'profiles' keys, raw_bytes for backup).
    """
    raw = path.read_bytes()
    docs = list(yaml.load_all(path))
    # Merge all documents into a single dict
    merged: dict = {}
    for doc in docs:
        if doc is not None:
            merged.update(doc)
    return merged, raw


def find_profile(data: Any, person_id: str) -> Any | None:
    """Locate a profile by its ``id`` field inside the ``profiles`` list."""
    profiles = data.get("profiles")
    if profiles is None:
        return None
    for profile in profiles:
        if profile.get("id") == person_id:
            return profile
    return None


def update_profile_field(profile: Any, field_path: str, value: Any) -> Any | None:
    """Set a nested field on a profile.  ``field_path`` uses dot-notation.

    Returns the previous value (or None).
    """
    parts = field_path.split(".")
    target = profile
    for part in parts[:-1]:
        child = target.get(part)
        if child is None:
            from ruamel.yaml.comments import CommentedMap
            child = CommentedMap()
            target[part] = child
        target = child
    prev = target.get(parts[-1])
    target[parts[-1]] = value
    return prev


def _render_yaml_block(key: str, value: Any, indent: int = 4) -> str:
    """Render a single key: value pair as a YAML string with given indentation."""
    y = YAML()
    y.default_flow_style = False
    y.width = 4096
    buf = io.StringIO()
    y.dump({key: value}, buf)
    raw = buf.getvalue().rstrip("\n")
    # Remove trailing newline doc markers
    if raw.endswith("\n..."):
        raw = raw[:-4].rstrip("\n")
    # Indent each line
    prefix = " " * indent
    lines = raw.split("\n")
    return "\n".join(prefix + line for line in lines)


def _find_profile_line_range(text: str, person_id: str) -> tuple[int, int] | None:
    """Find the line range (start, end_exclusive) for a profile in the YAML text.

    Returns (first_line_of_profile, first_line_of_next_item_or_EOF).
    """
    lines = text.split("\n")
    profile_start = None
    # Pattern: list item with id field, e.g. "  - id: "PERSON-019""
    id_pattern = re.compile(r"^\s+-\s+id:\s+\"?" + re.escape(person_id) + r"\"?\s*$")
    next_item_pattern = re.compile(r"^\s+-\s+id:\s+\"?PERSON-")

    for i, line in enumerate(lines):
        if profile_start is None:
            if id_pattern.match(line):
                profile_start = i
        elif next_item_pattern.match(line):
            return (profile_start, i)

    if profile_start is not None:
        return (profile_start, len(lines))
    return None


def insert_field_into_profile(
    path: Path, person_id: str, field_name: str, value: Any
) -> bool:
    """Insert or replace a field in a profile by text manipulation.

    Preserves all comments, formatting, and multi-document structure.
    """
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")

    rng = _find_profile_line_range(text, person_id)
    if rng is None:
        print(f"[yaml_updater] profile {person_id} not found in {path}")
        return False

    start, end = rng

    # Determine the base indentation from the profile's id line
    id_line = lines[start]
    base_indent = len(id_line) - len(id_line.lstrip())
    # Fields inside the profile item are indented by base + 2 (after the "- ")
    field_indent = base_indent + 2

    # Check if field already exists in this profile range
    field_pattern = re.compile(
        r"^" + " " * field_indent + re.escape(field_name) + r":"
    )
    existing_start = None
    existing_end = None
    for i in range(start + 1, end):
        if field_pattern.match(lines[i]):
            existing_start = i
            # Find end of this field (next field at same indent or end of profile)
            for j in range(i + 1, end):
                stripped = lines[j]
                if not stripped.strip():
                    continue
                line_indent = len(stripped) - len(stripped.lstrip())
                if line_indent <= field_indent and not stripped.strip().startswith("-"):
                    existing_end = j
                    break
                elif line_indent == field_indent and stripped.strip().startswith("-"):
                    # This is a list item at field level — still part of field
                    continue
            if existing_end is None:
                existing_end = end
            break

    # Render the new field block
    rendered = _render_yaml_block(field_name, value, indent=field_indent)

    if existing_start is not None:
        # Replace existing field
        lines[existing_start:existing_end] = [rendered]
    else:
        # Insert before the end of the profile (before next profile or blank+comment)
        insert_at = end
        # Walk backwards from end to find a good insertion point (after last real field)
        for i in range(end - 1, start, -1):
            stripped = lines[i].strip()
            if stripped and not stripped.startswith("#"):
                insert_at = i + 1
                break
        lines.insert(insert_at, "")
        lines.insert(insert_at + 1, rendered)

    path.write_text("\n".join(lines), encoding="utf-8")
    return True


def save_people_library(data: Any, path: Path, *, backup: bool = True) -> None:
    """Apply pending field updates via text insertion, preserving original file.

    This function is called after in-memory updates. It iterates profiles
    that have a ``github_data`` field and inserts them into the file.
    """
    if backup:
        bak = path.with_suffix(path.suffix + ".bak")
        shutil.copy2(path, bak)

    profiles = data.get("profiles")
    if not profiles:
        return

    for profile in profiles:
        pid = profile.get("id", "")
        gh_data = profile.get("github_data")
        if gh_data is not None:
            insert_field_into_profile(path, pid, "github_data", dict(gh_data))

        # Also update enrichment_date if it was changed
        enrich_date = profile.get("enrichment_date")
        if enrich_date:
            insert_field_into_profile(path, pid, "enrichment_date", enrich_date)

    # Validate the result is still parseable
    list(yaml.load_all(path))


def run_validation(*, strict: bool = False) -> bool:
    """Run ``validate_palette_state.py`` and return True if it passes."""
    if not VALIDATION_SCRIPT.exists():
        print(f"[yaml_updater] validation script not found: {VALIDATION_SCRIPT}")
        return True  # non-fatal — script is optional
    cmd = [sys.executable, str(VALIDATION_SCRIPT)]
    if strict:
        cmd.append("--strict")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[yaml_updater] validation FAILED:\n{result.stdout}\n{result.stderr}")
        return False
    print(f"[yaml_updater] validation passed")
    return True
