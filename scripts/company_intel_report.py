#!/usr/bin/env python3
"""Generate a lightweight company intelligence report from company-RIU mapping."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "company-library/v1.0/palette_company_riu_mapping_v1.0.yaml"
OUT = ROOT / "company-library/v1.0/company_intel_report.md"


def parse_blocks(text: str):
    use_case = None
    current_riu = None
    data = {}

    for line in text.splitlines():
        uc_match = re.match(r"^\s{2}([a-z0-9_]+):\s*$", line)
        if uc_match and not line.strip().startswith("metadata"):
            use_case = uc_match.group(1)
            data.setdefault(use_case, {})
            current_riu = None
            continue

        riu_match = re.match(r"^\s{6}- riu_id:\s*(RIU-\d+)\s*$", line)
        if riu_match and use_case:
            current_riu = riu_match.group(1)
            data[use_case].setdefault(current_riu, [])
            continue

        name_match = re.match(r"^\s{10}- name:\s*\"(.+)\"\s*$", line)
        if name_match and use_case and current_riu:
            data[use_case][current_riu].append(name_match.group(1))

    return data


def main() -> int:
    if not SRC.exists():
        print(f"Missing source: {SRC}")
        return 1

    text = SRC.read_text(encoding="utf-8", errors="ignore")
    data = parse_blocks(text)

    lines = [
        "# Company Intelligence Report",
        "",
        "Generated from `palette_company_riu_mapping_v1.0.yaml`.",
        "",
        "## Who Is Doing What (By Use Case / RIU)",
        "",
    ]

    for use_case, riu_map in sorted(data.items()):
        lines.append(f"### {use_case}")
        if not riu_map:
            lines.append("- No RIU entries parsed.")
            lines.append("")
            continue

        for riu_id, companies in sorted(riu_map.items()):
            if companies:
                preview = ", ".join(companies[:5])
                lines.append(f"- {riu_id}: {len(companies)} mapped companies. Top examples: {preview}")
            else:
                lines.append(f"- {riu_id}: 0 mapped companies (gap)")
        lines.append("")

    lines.extend(
        [
            "## Build-vs-Buy Guidance",
            "",
            "Use this default policy:",
            "- Prefer **pattern adoption** (internal implementation via RIUs/agents) when feasible.",
            "- Use **tool integration** only when time/risk constraints justify external dependency.",
            "- Reassess decisions quarterly against implementation outcomes.",
            "",
            "## Next Actions",
            "",
            "1. Tag top 3 RIUs per active implementation and align company signals.",
            "2. Run a build-vs-buy scorecard for each shortlisted tool/company.",
            "3. Log ONE-WAY DOOR integration decisions in implementation `fde/decisions.md`.",
        ]
    )

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
