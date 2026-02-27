#!/usr/bin/env python3
"""Validate implementation structure consistency.

Discovery: uses .palette-meta.yaml as the marker for Palette implementations.
Folders without .palette-meta.yaml are silently skipped.

Severity tiers:
  ERROR — required for any Palette implementation (blocks PASS)
  WARN  — recommended for mature implementations (informational)
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

# Required for ALL implementations (missing = ERROR)
REQUIRED_PATHS = [
    ".palette-meta.yaml",
    "STATUS.md",
    "fde/decisions.md",
]

# Recommended for mature implementations (missing = WARN)
RECOMMENDED_PATHS = [
    "LEARNINGS.md",
    "fde/kgdrs",
    ".kiro/steering",
    "workflows/WEEKLY_ACTION_BOARD.md",
]

REQUIRED_META_FIELDS = [
    "name",
    "slug",
    "domain",
    "type",
    "status",
]

RECOMMENDED_META_FIELDS = [
    "palette_agents_used",
    "outcomes",
]

RECOMMENDED_DECISIONS_SECTION = "## A) Implementation ONE-WAY DOOR Decisions"


def find_implementations(root: Path) -> list[Path]:
    """Discover implementations by scanning for .palette-meta.yaml."""
    out: list[Path] = []
    for domain in sorted(root.iterdir()):
        if not domain.is_dir() or domain.name.startswith(("_", ".")):
            continue
        for impl in sorted(domain.iterdir()):
            if not impl.is_dir():
                continue
            if (impl / ".palette-meta.yaml").exists():
                out.append(impl)
    return out


def validate_impl(impl: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    # --- Entrypoint (ERROR) ---
    if not ((impl / "README.md").exists() or (impl / "CONVERGENCE_BRIEF.md").exists()):
        errors.append("missing entrypoint: need README.md or CONVERGENCE_BRIEF.md")

    # --- Required paths (ERROR) ---
    for rel in REQUIRED_PATHS:
        if not (impl / rel).exists():
            errors.append(f"missing required: {rel}")

    # --- Recommended paths (WARN) ---
    for rel in RECOMMENDED_PATHS:
        if not (impl / rel).exists():
            warnings.append(f"missing recommended: {rel}")

    # --- Runbook (WARN — flexible location) ---
    if not ((impl / "RUNBOOK.md").exists() or (impl / "telegram" / "RUNBOOK.md").exists()):
        warnings.append("missing recommended: RUNBOOK.md (or telegram/RUNBOOK.md)")

    # --- Metadata validation ---
    meta_path = impl / ".palette-meta.yaml"
    if meta_path.exists():
        try:
            meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
            if not isinstance(meta, dict):
                errors.append(".palette-meta.yaml is not a mapping")
                meta = {}
            for key in REQUIRED_META_FIELDS:
                if key not in meta:
                    errors.append(f".palette-meta.yaml missing field: {key}")
            for key in RECOMMENDED_META_FIELDS:
                if key not in meta:
                    warnings.append(f".palette-meta.yaml missing recommended field: {key}")
        except Exception as exc:  # noqa: BLE001
            errors.append(f".palette-meta.yaml parse failed: {exc}")

    # --- Decisions section (WARN) ---
    decisions_path = impl / "fde/decisions.md"
    if decisions_path.exists():
        try:
            decisions = decisions_path.read_text(encoding="utf-8")
            if RECOMMENDED_DECISIONS_SECTION not in decisions:
                warnings.append(
                    f"fde/decisions.md missing recommended section "
                    f"'{RECOMMENDED_DECISIONS_SECTION}'"
                )
        except Exception as exc:  # noqa: BLE001
            warnings.append(f"could not read fde/decisions.md: {exc}")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate implementation structure consistency."
    )
    parser.add_argument(
        "--implementations-root",
        default="implementations",
        help="Path to implementations root (default: implementations/)",
    )
    parser.add_argument(
        "--impl",
        action="append",
        default=[],
        help="Specific implementation path(s). If omitted, validates all.",
    )
    parser.add_argument(
        "--fail-on-warnings",
        action="store_true",
        help="Treat warnings as failures.",
    )
    args = parser.parse_args()

    root = Path(args.implementations_root)
    if args.impl:
        impls = [Path(p) for p in args.impl]
    else:
        impls = find_implementations(root)

    if not impls:
        print("No implementations found.")
        return 1

    total_errors = 0
    total_warnings = 0
    passed = 0
    for impl in impls:
        errors, warnings = validate_impl(impl)
        status = "PASS" if not errors else "FAIL"
        if not errors:
            passed += 1
        print(f"[{status}] {impl.name}")
        for msg in errors:
            print(f"  ERROR: {msg}")
        for msg in warnings:
            print(f"  WARN:  {msg}")
        total_errors += len(errors)
        total_warnings += len(warnings)

    print(
        f"\n{passed}/{len(impls)} passed, "
        f"{total_errors} error(s), {total_warnings} warning(s)"
    )
    if total_errors:
        return 1
    if args.fail_on_warnings and total_warnings:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
