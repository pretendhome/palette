#!/usr/bin/env python3
"""palette demo sarah — Run the full BDB 3-moment demo flow.

Usage:
  palette demo sarah
  palette demo sarah --external   (use Perplexity for Moment 2)

Runs: PROTECT → RESEARCH → DECIDE with shared matter_id.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from scripts.palette_intents.infra import BOLD, CYAN, DIM, RESET, WHITE

MATTER_ID = "sarah-demo"

MOMENT_1_QUERY = "What's our exposure if the majority member was self-dealing through a related-party transaction?"
MOMENT_2_QUERY = "What fiduciary duty standards apply to LLC co-founders in Delaware?"
MOMENT_3_QUERY = "Given the fiduciary evidence, should Sarah pursue litigation or settle?"


def run_demo(use_external: bool = False):
    """Run the full Sarah demo: PROTECT → RESEARCH → DECIDE."""

    print()
    print(f"  {BOLD}{WHITE}{'═' * 60}{RESET}")
    print(f"  {BOLD}{WHITE}  SARAH'S MORNING — Palette OS Demo{RESET}")
    print(f"  {BOLD}{WHITE}{'═' * 60}{RESET}")
    print()
    print(f"  {DIM}Matter: {MATTER_ID}{RESET}")
    print(f"  {DIM}3 moments. 3 intents. 3 typed artifacts. Zero data leakage.{RESET}")
    print()

    # Moment 1: PROTECT
    print(f"  {CYAN}{'━' * 20} MOMENT 1: PROTECT {'━' * 20}{RESET}")
    from scripts.palette_intents.protect import run_protect
    gate, state1 = run_protect(MOMENT_1_QUERY, matter_id=MATTER_ID)

    print()
    input(f"  {DIM}[Press Enter for Moment 2...]{RESET}")
    print()

    # Moment 2: RESEARCH
    print(f"  {CYAN}{'━' * 20} MOMENT 2: RESEARCH {'━' * 19}{RESET}")
    from scripts.palette_intents.research import run_research
    brief, state2 = run_research(
        MOMENT_2_QUERY,
        matter_id=MATTER_ID,
        local_only=not use_external,
    )

    print()
    input(f"  {DIM}[Press Enter for Moment 3...]{RESET}")
    print()

    # Moment 3: DECIDE
    print(f"  {CYAN}{'━' * 20} MOMENT 3: DECIDE {'━' * 21}{RESET}")
    from scripts.palette_intents.decide import run_decide
    decision, state3 = run_decide(MOMENT_3_QUERY, matter_id=MATTER_ID)

    # Summary
    print()
    print(f"  {BOLD}{WHITE}{'═' * 60}{RESET}")
    print(f"  {BOLD}  DEMO COMPLETE{RESET}")
    print(f"  {DIM}  3 artifacts produced. Compounding chain visible.{RESET}")
    print(f"  {DIM}  Matter: {MATTER_ID}{RESET}")
    print(f"  {DIM}  PROTECT: {gate['action']} | RESEARCH: {brief['status']} | DECIDE: {decision['reversibility']}{RESET}")
    print(f"  {BOLD}{WHITE}{'═' * 60}{RESET}")
    print()


def main():
    parser = argparse.ArgumentParser(prog="palette demo")
    parser.add_argument("scenario", nargs="?", default="sarah", help="Demo scenario (default: sarah)")
    parser.add_argument("--external", "-e", action="store_true", help="Use Perplexity for research")
    args = parser.parse_args()

    if args.scenario != "sarah":
        print(f"Unknown demo scenario: {args.scenario}")
        print("Available: sarah")
        sys.exit(1)

    run_demo(use_external=args.external)


if __name__ == "__main__":
    main()
