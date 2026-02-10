#!/usr/bin/env python3
"""
Sync agent impressions from project decision logs to global agent maturity tracker.

Usage: python3 sync-impressions.py [--dry-run]
"""
import re
import sys
from pathlib import Path
from collections import defaultdict

# Paths
SCRIPT_DIR = Path(__file__).parent
PALETTE_ROOT = SCRIPT_DIR.parent
FDE_ROOT = PALETTE_ROOT.parent
PROJECTS_DIR = FDE_ROOT / "projects"
AGENTS_README = PALETTE_ROOT / "agents" / "README.md"

# Agent name mappings
AGENT_NAMES = {
    "argentavis": "Argentavis",
    "argy": "Argentavis",
    "tyrannosaurus": "Tyrannosaurus",
    "rex": "Tyrannosaurus",
    "therizinosaurus": "Therizinosaurus",
    "theri": "Therizinosaurus",
    "velociraptor": "Velociraptor",
    "raptor": "Velociraptor",
    "yutyrannus": "Yutyrannus",
    "yuty": "Yutyrannus",
    "ankylosaurus": "Ankylosaurus",
    "anky": "Ankylosaurus",
    "parasaurolophus": "Parasaurolophus",
    "para": "Parasaurolophus",
}

def parse_impressions(file_path):
    """Extract agent impressions from a decision log."""
    impressions = defaultdict(lambda: {"success": 0, "fail": 0, "projects": []})
    
    content = file_path.read_text()
    project_name = file_path.parent.name
    
    # Pattern: **Impressions**: X success, Y fail
    pattern = r'\*\*Impressions\*\*:\s*(\d+)\s*success,\s*(\d+)\s*fail'
    
    # Find agent name before impressions (look backwards from match)
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        if '**Impressions**:' in line:
            match = re.search(pattern, line)
            if match:
                success = int(match.group(1))
                fail = int(match.group(2))
                
                # Look backwards for agent name (### AgentName or **Agent**: name)
                agent = None
                for j in range(i-1, max(0, i-20), -1):
                    # Check for ### Argentavis (Argy) or ### Tyrannosaurus Rex (Rex) format
                    header_match = re.search(r'###\s+(\w+)(?:\s+\w+)?\s*\(', lines[j])
                    if header_match:
                        agent_key = header_match.group(1).lower()
                        if agent_key in AGENT_NAMES:
                            agent = AGENT_NAMES[agent_key]
                            break
                
                if agent and (success > 0 or fail > 0):
                    impressions[agent]["success"] += success
                    impressions[agent]["fail"] += fail
                    impressions[agent]["projects"].append(f"{project_name} ({success})")
    
    return impressions

def aggregate_impressions():
    """Scan all project decision logs and aggregate impressions."""
    totals = defaultdict(lambda: {"success": 0, "fail": 0, "projects": []})
    
    # Find all decisions.md and execution_summary.md files
    files_found = []
    for pattern in ["*/decisions.md", "*/*/execution_summary.md"]:
        for file_path in PROJECTS_DIR.glob(pattern):
            files_found.append(file_path)
            print(f"  Parsing {file_path.relative_to(FDE_ROOT)}...")
            impressions = parse_impressions(file_path)
            for agent, data in impressions.items():
                totals[agent]["success"] += data["success"]
                totals[agent]["fail"] += data["fail"]
                totals[agent]["projects"].extend(data["projects"])
    
    if not files_found:
        print(f"  WARNING: No decision logs found in {PROJECTS_DIR}")
    
    return totals

def calculate_status(success, fail):
    """Determine agent maturity tier."""
    if success >= 50 and (fail / max(success, 1)) < 0.05:
        return "PRODUCTION"
    elif success >= 10 and (fail / max(success, 1)) < 0.05:
        return "WORKING"
    else:
        return "UNVALIDATED"

def calculate_next_tier(status, success, fail):
    """Calculate impressions needed for next tier."""
    if status == "PRODUCTION":
        return "MAX TIER"
    elif status == "WORKING":
        needed = 50 - success
        return f"PRODUCTION ({needed} more)"
    else:
        needed = 10 - success
        return f"WORKING ({needed} more)"

def generate_table(totals):
    """Generate markdown table for agents/README.md."""
    lines = [
        "## Current Status (as of 2026-02-10)",
        "",
        "| Agent | Status | Impressions | Next Tier | Projects |",
        "|-------|--------|-------------|-----------|----------|",
    ]
    
    # Sort by success count (descending)
    sorted_agents = sorted(totals.items(), key=lambda x: x[1]["success"], reverse=True)
    
    for agent, data in sorted_agents:
        success = data["success"]
        fail = data["fail"]
        status = calculate_status(success, fail)
        next_tier = calculate_next_tier(status, success, fail)
        projects = ", ".join(data["projects"]) if data["projects"] else "-"
        
        lines.append(
            f"| **{agent}** | {status} | {success} success, {fail} fail | {next_tier} | {projects} |"
        )
    
    # Add agents with no impressions
    all_agents = ["Argentavis", "Tyrannosaurus", "Therizinosaurus", "Velociraptor", 
                  "Yutyrannus", "Ankylosaurus", "Parasaurolophus", "Orchestrator"]
    for agent in all_agents:
        if agent not in totals:
            if agent == "Orchestrator":
                lines.append(f"| **{agent}** | DESIGN ONLY | - | - | - |")
            else:
                lines.append(f"| **{agent}** | UNVALIDATED | 0 impressions | WORKING (10 more) | - |")
    
    lines.extend([
        "",
        "See individual agent directories for implementation details.",
    ])
    
    return "\n".join(lines)

def update_readme(table, dry_run=False):
    """Update agents/README.md with new status table."""
    content = AGENTS_README.read_text()
    
    # Find and replace the status section
    pattern = r'## Current Status.*?(?=\n##|\Z)'
    new_content = re.sub(pattern, table, content, flags=re.DOTALL)
    
    if dry_run:
        print("DRY RUN - Would update agents/README.md:")
        print(table)
    else:
        AGENTS_README.write_text(new_content)
        print(f"✅ Updated {AGENTS_README}")

def main():
    dry_run = "--dry-run" in sys.argv
    
    print("Scanning project decision logs...")
    totals = aggregate_impressions()
    
    print(f"\nFound impressions for {len(totals)} agents:")
    for agent, data in sorted(totals.items(), key=lambda x: x[1]["success"], reverse=True):
        print(f"  {agent}: {data['success']} success, {data['fail']} fail")
    
    print("\nGenerating status table...")
    table = generate_table(totals)
    
    print("\nUpdating agents/README.md...")
    update_readme(table, dry_run)
    
    if not dry_run:
        print("\n✅ Sync complete. Review changes and commit.")

if __name__ == "__main__":
    main()
