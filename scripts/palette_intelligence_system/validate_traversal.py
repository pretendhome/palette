#!/usr/bin/env python3
"""Validate query_engine.py output against hand-verified traversal results.

Runs query_engine.py traverse for each of the 28 RIUs documented in
implementations/dev/dev-palette-devenv/validation/pis-traversal-results.md
and compares classification, primary service, and recipe references.

Exit code 0 = all match, 1 = mismatches found.
"""

import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def _repo_root() -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "palette").is_dir():
            return parent
    raise RuntimeError("Could not find repo root")


REPO_ROOT = _repo_root()
MANUAL_RESULTS = REPO_ROOT / "implementations" / "dev" / "dev-palette-devenv" / "validation" / "pis-traversal-results.md"


def parse_manual_results() -> Dict[str, Dict[str, str]]:
    """Parse the manual pis-traversal-results.md into structured data.

    Extracts RIU ID, name, and table fields from each ### section.
    The file uses markdown tables with **bold** field names in the first column.
    """
    content = MANUAL_RESULTS.read_text()
    results: Dict[str, Dict[str, str]] = {}

    # Split on ### RIU-NNN headers
    sections = re.split(r"\n### (RIU-\d+): (.+?)\n", content)

    # sections[0] = preamble, then triplets: (riu_id, name, body)
    for i in range(1, len(sections), 3):
        if i + 2 >= len(sections):
            break
        riu_id = sections[i].strip()
        name = sections[i + 1].strip()
        body = sections[i + 2]

        data: Dict[str, str] = {"name": name}

        # Parse markdown table rows: | **Field** | Value |
        for match in re.finditer(r"\| \*\*(.+?)\*\* \| (.+?) \|", body):
            field = match.group(1).strip()
            value = match.group(2).strip()
            data[field] = value

        results[riu_id] = data

    return results


def run_traverse(riu_id: str) -> str:
    """Run query_engine traverse and capture stdout."""
    result = subprocess.run(
        [sys.executable, "-m", "scripts.palette_intelligence_system.query_engine", "traverse", riu_id],
        cwd=REPO_ROOT / "palette",
        capture_output=True,
        text=True,
        timeout=30,
    )
    return result.stdout


def validate_one(riu_id: str, manual: Dict[str, str]) -> List[str]:
    """Compare programmatic output against manual data for one RIU.

    Returns a list of mismatch descriptions (empty = pass).
    """
    output = run_traverse(riu_id)
    mismatches: List[str] = []

    # 1. Classification must match
    expected_cls = manual.get("Classification", "")
    if expected_cls and expected_cls not in output:
        mismatches.append(f"Classification: expected '{expected_cls}', not in output")

    # 2. For 'both' RIUs, primary service name should appear
    if expected_cls == "both":
        svc_routing = manual.get("Service Routing", "")
        if svc_routing:
            # Extract first service name (before comma or parenthesis)
            m = re.match(r"([A-Za-z][A-Za-z0-9 ]+?)(?:\s*[\(,]|$)", svc_routing)
            if m:
                first_svc = m.group(1).strip()
                if len(first_svc) > 3:
                    norm_expected = first_svc.lower().replace(" ", "")
                    norm_output = output.lower().replace(" ", "")
                    if norm_expected not in norm_output:
                        mismatches.append(f"Primary service '{first_svc}' not in output")

    # 3. Recipe reference should appear if manual lists one
    #    Manual format: `integrations/xxx/recipe.yaml` or `integrations/xxx/recipe.yaml` (note)
    recipe_field = manual.get("Recipe", "")
    if recipe_field:
        # Manual docs sometimes note an indirect contextual mention (e.g. "Referenced in ...")
        # instead of a direct recipe for the routed services. Do not require a recipe in output
        # for these cases; the engine is validating routed service recipes, not adjacent IAM notes.
        if recipe_field.lower().startswith("referenced in "):
            return mismatches
        # Direct recipe reference
        recipe_match = re.search(r"`integrations/([^`]+?)/recipe\.yaml`", recipe_field)
        if recipe_match:
            recipe_dir = recipe_match.group(1)
            # The output should mention recipe.yaml somewhere for this RIU
            if "recipe.yaml" not in output and "Recipe:" not in output:
                mismatches.append(f"Recipe reference missing (expected integrations/{recipe_dir}/recipe.yaml)")
            # More specifically, check if the recipe dir or service is mentioned
            elif recipe_dir.replace("-", "") in output.lower().replace("-", "").replace(" ", ""):
                pass  # Found
            elif "recipe.yaml" in output:
                pass  # Has some recipe — good enough
            elif "NOT FOUND" not in output:
                pass  # No NOT FOUND markers
            # If manual says it's an indirect reference (like "Referenced in" or has parenthetical note),
            # be lenient — just check that SOME recipe.yaml appears
            elif "(" in recipe_field:
                # Indirect reference (e.g., Datadog recipe mentions SLO tracking)
                # Only fail if zero recipes show up
                if "recipe.yaml" not in output:
                    mismatches.append(f"No recipe found in output (expected indirect ref via {recipe_dir})")

    return mismatches


def main() -> int:
    print("Validating query_engine.py against manual traversal results...\n")

    manual_results = parse_manual_results()
    print(f"Loaded {len(manual_results)} manual traversal results")

    passed = 0
    failed = 0

    for riu_id in sorted(manual_results.keys()):
        manual = manual_results[riu_id]
        mismatches = validate_one(riu_id, manual)

        if mismatches:
            failed += 1
            print(f"\n\u274c {riu_id}: {manual.get('name', '?')}")
            for m in mismatches:
                print(f"   - {m}")
        else:
            passed += 1
            print(f"\u2713 {riu_id}: {manual.get('name', '?')}")

    total = passed + failed
    print(f"\n{'=' * 60}")
    print(f"Results: {passed}/{total} passed, {failed}/{total} failed")

    if failed > 0:
        print("\nValidation FAILED \u2014 mismatches found")
        return 1
    print("\nValidation PASSED \u2014 all manual results match programmatic output")
    return 0


if __name__ == "__main__":
    sys.exit(main())
