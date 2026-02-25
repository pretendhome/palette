#!/usr/bin/env python3
"""
Manual-first lens evaluation runner for Palette lenses.

Purpose:
- list fixtures from the lens fixture pack
- print fixture details for a run
- append a markdown scoring template (baseline + lens variants) to a results file

This is intentionally lightweight and Telegram-friendly:
you run the prompt manually, collect outputs, then fill in scores/notes.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path("/home/mical/fde")
DEFAULT_FIXTURES = REPO_ROOT / "palette/lenses/fixtures/LENS_EVAL_FIXTURES_v0.yaml"
DEFAULT_RESULTS_DIR = REPO_ROOT / "palette/lenses/results"
DEFAULT_SPEC = REPO_ROOT / "palette/lenses/LENS_EVAL_HARNESS_SPEC_2026-02-25.md"


def load_fixture_pack(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Fixture pack not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or "fixtures" not in data:
        raise ValueError(f"Invalid fixture pack schema: {path}")
    return data


def fixture_index(fixture_pack: dict[str, Any]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for fx in fixture_pack.get("fixtures", []):
        if isinstance(fx, dict) and fx.get("id"):
            out[str(fx["id"])] = fx
    return out


def fmt_list(values: list[Any]) -> str:
    if not values:
        return "(none)"
    return ", ".join(str(v) for v in values)


def print_fixture_summary(fx: dict[str, Any], scoring_dimensions: list[str]) -> None:
    intended = fx.get("intended_lenses", {}) or {}
    primary = intended.get("primary", []) or []
    comparison = intended.get("comparison", []) or []

    print(f"Fixture: {fx.get('id')} — {fx.get('title')}")
    print("-" * 72)
    print("Prompt:")
    print(str(fx.get("prompt", "")).rstrip())
    print()
    print(f"Primary lens(es):    {fmt_list(primary)}")
    print(f"Comparison lens(es): {fmt_list(comparison)}")
    print(f"Expected shape:      {fmt_list(fx.get('expected_output_shape', []) or [])}")
    print(f"Failure patterns:    {fmt_list(fx.get('failure_patterns', []) or [])}")
    print(f"Scoring dimensions:  {fmt_list(scoring_dimensions)}")


def build_result_template(
    fx: dict[str, Any],
    scoring_dimensions: list[str],
    run_labels: list[str],
    notes: str | None = None,
) -> str:
    ts = dt.datetime.now().isoformat(timespec="seconds")
    lines: list[str] = []
    lines.append(f"## {fx.get('id')} — {fx.get('title')}")
    lines.append("")
    lines.append(f"- `generated_at`: {ts}")
    lines.append(f"- `fixture_id`: {fx.get('id')}")
    lines.append(f"- `harness_spec`: `{DEFAULT_SPEC}`")
    if notes:
        lines.append(f"- `notes`: {notes}")
    lines.append("")
    lines.append("### Prompt")
    lines.append("")
    lines.append("```text")
    lines.append(str(fx.get("prompt", "")).rstrip())
    lines.append("```")
    lines.append("")
    lines.append("### Intended Lenses")
    lines.append("")
    intended = fx.get("intended_lenses", {}) or {}
    lines.append(f"- Primary: {fmt_list(intended.get('primary', []) or [])}")
    lines.append(f"- Comparison: {fmt_list(intended.get('comparison', []) or [])}")
    lines.append("")
    lines.append("### Runs")
    lines.append("")

    for label in run_labels:
        lines.append(f"#### Run: `{label}`")
        lines.append("")
        lines.append("**Output**")
        lines.append("")
        lines.append("```text")
        lines.append("PASTE OUTPUT HERE")
        lines.append("```")
        lines.append("")
        lines.append("**Scores (1-5)**")
        for dim in scoring_dimensions:
            lines.append(f"- {dim}: ")
        lines.append("")
        lines.append("**What worked**")
        lines.append("- ")
        lines.append("")
        lines.append("**What was weak / missing**")
        lines.append("- ")
        lines.append("")
        lines.append("**Failure patterns observed**")
        lines.append("- ")
        lines.append("")
        lines.append("**Reviewer notes**")
        lines.append("- ")
        lines.append("")

    lines.append("### Comparison Summary")
    lines.append("")
    lines.append("- Winner (if any): ")
    lines.append("- Why: ")
    lines.append("- Promotion signal: ")
    lines.append("- Follow-up action: ")
    lines.append("")
    return "\n".join(lines)


def append_result(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header_needed = not path.exists()
    with path.open("a", encoding="utf-8") as f:
        if header_needed:
            f.write("# Lens Eval Results Log\n\n")
            f.write(f"- Created: {dt.datetime.now().isoformat(timespec='seconds')}\n\n")
        f.write(content)
        if not content.endswith("\n"):
            f.write("\n")


def default_results_path() -> Path:
    stamp = dt.date.today().isoformat()
    return DEFAULT_RESULTS_DIR / f"LENS_EVAL_RESULTS_{stamp}.md"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Manual-first lens evaluation runner")
    p.add_argument(
        "--fixtures",
        type=Path,
        default=DEFAULT_FIXTURES,
        help=f"Path to fixture pack YAML (default: {DEFAULT_FIXTURES})",
    )
    p.add_argument("--list", action="store_true", help="List available fixtures")
    p.add_argument("--fixture", help="Fixture ID to inspect or template (e.g., FIX-001)")
    p.add_argument(
        "--print-only",
        action="store_true",
        help="Print fixture details and exit (no template append)",
    )
    p.add_argument(
        "--template",
        action="store_true",
        help="Append a markdown result template for the fixture",
    )
    p.add_argument(
        "--runs",
        default="baseline",
        help="Comma-separated run labels for template (default: baseline). Example: baseline,LENS-PM-001,LENS-EXEC-001",
    )
    p.add_argument(
        "--results-file",
        type=Path,
        default=default_results_path(),
        help="Markdown results log path",
    )
    p.add_argument(
        "--notes",
        default=None,
        help="Optional run notes added to template header",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()

    try:
        pack = load_fixture_pack(args.fixtures)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    fixtures = fixture_index(pack)
    scoring_dimensions = [str(x) for x in (pack.get("scoring_dimensions", []) or [])]

    if args.list or (not args.fixture and not args.template):
        print(f"Fixture pack: {pack.get('fixture_pack_id', '(unknown)')}")
        print(f"Fixtures: {len(fixtures)}")
        print("-" * 72)
        for fid in sorted(fixtures):
            title = fixtures[fid].get("title", "")
            intended = fixtures[fid].get("intended_lenses", {}) or {}
            primary = fmt_list((intended.get("primary", []) or []))
            print(f"{fid}: {title}")
            print(f"  primary: {primary}")
        if not args.fixture and not args.template:
            print("\nTip: use --fixture FIX-001 --print-only or --template")
        return 0 if not args.fixture else 1

    fx = fixtures.get(str(args.fixture))
    if not fx:
        print(f"ERROR: Fixture not found: {args.fixture}", file=sys.stderr)
        print(f"Available: {', '.join(sorted(fixtures.keys()))}", file=sys.stderr)
        return 1

    print_fixture_summary(fx, scoring_dimensions)

    if args.print_only and not args.template:
        return 0

    if args.template:
        run_labels = [x.strip() for x in args.runs.split(",") if x.strip()]
        if not run_labels:
            run_labels = ["baseline"]
        content = build_result_template(fx, scoring_dimensions, run_labels, args.notes)
        append_result(args.results_file, content)
        print()
        print(f"Appended template to: {args.results_file}")
        print(f"Run labels: {', '.join(run_labels)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

