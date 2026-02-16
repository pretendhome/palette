#!/usr/bin/env python3
"""Palette integrity checks to prevent drift across docs, taxonomy, and library."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PALETTE = ROOT / "palette"

ERRORS: list[str] = []
WARNINGS: list[str] = []
STRICT = "--strict" in sys.argv


def expect_file(path: Path) -> None:
    if not path.exists():
        ERRORS.append(f"Missing required file: {path.relative_to(ROOT)}")


def check_outdated_paths() -> None:
    files = [
        PALETTE / ".kiro/steering/TIER3_decisions_prompt.md",
        PALETTE / ".kiro/steering/palette-core-v1.0-archived.md",
        PALETTE / "README.md",
        PALETTE / "PROJECT_STRUCTURE.md",
    ]
    bad_patterns = [r"/projects/<", r"~/projects/<", r"/fde/projects/"]
    for file in files:
        if not file.exists():
            continue
        text = file.read_text(encoding="utf-8", errors="ignore")
        for pattern in bad_patterns:
            if re.search(pattern, text):
                ERRORS.append(
                    f"Outdated path reference '{pattern}' found in {file.relative_to(ROOT)}"
                )


def check_taxonomy_counts() -> None:
    tax = PALETTE / "taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml"
    if not tax.exists():
        ERRORS.append("Missing taxonomy v1.3 snapshot")
        return
    text = tax.read_text(encoding="utf-8", errors="ignore")
    riu_count = len(re.findall(r"^\s*- riu_id:\s+", text, flags=re.MULTILINE))
    stat_match = re.search(r"^\s*total_rius:\s*(\d+)\s*$", text, flags=re.MULTILINE)
    if not stat_match:
        ERRORS.append("taxonomy_statistics.total_rius not found in taxonomy v1.3")
        return
    declared = int(stat_match.group(1))
    if riu_count != declared:
        ERRORS.append(
            f"Taxonomy RIU count mismatch: declared={declared}, actual={riu_count}"
        )


def check_library_ids() -> None:
    lib = PALETTE / "knowledge-library/v1.2/palette_knowledge_library_v1.2.yaml"
    if not lib.exists():
        ERRORS.append("Missing knowledge library file")
        return
    text = lib.read_text(encoding="utf-8", errors="ignore")
    ids = re.findall(r"^\s*- id:\s*(LIB-\d+)\s*$", text, flags=re.MULTILINE)
    if not ids:
        ERRORS.append("No LIB IDs found in knowledge library")
        return
    seen = set()
    dupes = sorted({x for x in ids if x in seen or seen.add(x)})
    if dupes:
        msg = f"Duplicate LIB IDs detected: {', '.join(dupes[:10])}"
        if STRICT:
            ERRORS.append(msg)
        else:
            WARNINGS.append(msg)


def check_orchestrator_guard() -> None:
    assumptions = PALETTE / ".kiro/steering/assumptions.md"
    agents_readme = PALETTE / "agents/README.md"
    for file, pattern in [
        (assumptions, r"DESIGN-ONLY PLACEHOLDER"),
        (agents_readme, r"\| \*\*Orchestrator\*\* \| DESIGN ONLY"),
    ]:
        if not file.exists():
            ERRORS.append(f"Missing file for Orchestrator guard: {file.relative_to(ROOT)}")
            continue
        text = file.read_text(encoding="utf-8", errors="ignore")
        if not re.search(pattern, text):
            ERRORS.append(f"Orchestrator guard missing in {file.relative_to(ROOT)}")



def check_implementation_modules() -> None:
    impl_root = ROOT / "implementations"
    if not impl_root.exists():
        return
    required = [
        ".kiro/steering/palette/TIER1_palette_core.md",
        ".kiro/steering/palette/TIER2_assumptions.md",
        ".kiro/steering/palette/TIER3_decisions_prompt.md",
        "fde/decisions.md",
    ]
    for impl in sorted(p for p in impl_root.iterdir() if p.is_dir() and not p.name.startswith("_")):
        for rel in required:
            path = impl / rel
            if not path.exists():
                WARNINGS.append(f"Implementation module missing: {path.relative_to(ROOT)}")


def main() -> int:
    expect_file(PALETTE / ".kiro/steering/TIER3_decisions_prompt.md")
    expect_file(PALETTE / ".kiro/steering/assumptions.md")
    expect_file(PALETTE / "taxonomy/releases/v1.3/palette_taxonomy_v1.3.yaml")
    expect_file(PALETTE / "knowledge-library/v1.2/palette_knowledge_library_v1.2.yaml")

    check_outdated_paths()
    check_taxonomy_counts()
    check_library_ids()
    check_orchestrator_guard()
    check_implementation_modules()

    if WARNINGS:
        print("WARNINGS:")
        for w in WARNINGS:
            print(f"- {w}")

    if ERRORS:
        print("ERRORS:")
        for e in ERRORS:
            print(f"- {e}")
        return 1

    print("Palette integrity checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
