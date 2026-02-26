#!/usr/bin/env python3
"""PIS Query Engine — CLI for traversing Palette Intelligence System data.

Traverses all four PIS data layers (taxonomy, classification, service routing,
integration recipes) and answers structured queries.

Usage:
  python -m scripts.pis.query_engine traverse RIU-082
  python -m scripts.pis.query_engine coverage
  python -m scripts.pis.query_engine cost RIU-061 RIU-082 RIU-521 RIU-524
  python -m scripts.pis.query_engine gaps
  python -m scripts.pis.query_engine stack "observability"
  python -m scripts.pis.query_engine check

Recipe Matching Heuristic:
  Service names in routing (e.g., "AWS Bedrock Guardrails") don't match recipe
  directory names (e.g., "bedrock-guardrails"). Matching uses three strategies:
  1. Normalize both to lowercase alphanumeric and compare
  2. Parse "# RIUs served:" comments from recipe headers for reverse RIU lookup
  3. Check if normalized recipe service_name is a substring of normalized routing name
  Strategy 2 is the key fix: it catches cases like RIU-522 → OpenRouter recipe,
  where the routing lists "OpenRouter (built-in)" but the recipe header explicitly
  declares "RIUs served: RIU-522".
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml


# Recipes that are intentionally present as reusable integration building blocks
# even if they are not yet referenced by a service-routing entry.
ALLOWED_ORPHAN_RECIPES: Set[str] = {
    "githubapi",
}


# ── Data Layer Paths ──────────────────────────────────────────────

def _find_repo_root() -> Path:
    """Find repo root by looking for palette/ directory."""
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "palette").is_dir():
            return parent
    raise RuntimeError("Could not find repo root (no palette/ directory found)")


REPO_ROOT = _find_repo_root()
TAXONOMY_PATH = REPO_ROOT / "palette" / "taxonomy" / "releases" / "v1.3" / "palette_taxonomy_v1.3.yaml"
CLASSIFICATION_PATH = REPO_ROOT / "palette" / "company-library" / "service-routing" / "v1.0" / "riu_classification_v1.0.yaml"
ROUTING_PATH = REPO_ROOT / "palette" / "company-library" / "service-routing" / "v1.0" / "service_routing_v1.0.yaml"
INTEGRATIONS_DIR = REPO_ROOT / "palette" / "company-library" / "integrations"


# ── Normalization ──────────────────────────────────────────────────

def normalize_name(name: str) -> str:
    """Normalize a service name for fuzzy matching.

    Strips everything except lowercase alphanumeric characters.
    "AWS Bedrock Guardrails" → "awsbedrockguardrails"
    "OpenRouter" → "openrouter"
    """
    return re.sub(r"[^a-z0-9]", "", name.lower())


# ── Data Loading ──────────────────────────────────────────────────

class PISData:
    """All four PIS data layers, loaded and cross-indexed."""

    def __init__(self):
        self.taxonomy: Dict[str, Dict[str, Any]] = {}        # riu_id → raw entry
        self.classification: Dict[str, Dict[str, Any]] = {}   # riu_id → raw entry
        self.routing: Dict[str, Dict[str, Any]] = {}          # riu_id → raw entry
        self.recipes: Dict[str, Dict[str, Any]] = {}          # normalized_name → raw entry + _path
        self.recipe_riu_index: Dict[str, List[str]] = {}      # riu_id → [normalized_recipe_name, ...]
        self.load_errors: List[str] = []

    def load_all(self):
        """Load all four data layers with error isolation."""
        self._load_taxonomy()
        self._load_classification()
        self._load_routing()
        self._load_recipes()

    def _load_taxonomy(self):
        if not TAXONOMY_PATH.exists():
            self.load_errors.append(f"Taxonomy file not found: {TAXONOMY_PATH}")
            return
        try:
            with open(TAXONOMY_PATH) as f:
                data = yaml.safe_load(f)
            for entry in data.get("rius", []):
                riu_id = entry.get("riu_id", "")
                if riu_id:
                    self.taxonomy[riu_id] = entry
        except Exception as e:
            self.load_errors.append(f"Taxonomy load failed: {e}")

    def _load_classification(self):
        if not CLASSIFICATION_PATH.exists():
            self.load_errors.append(f"Classification file not found: {CLASSIFICATION_PATH}")
            return
        try:
            with open(CLASSIFICATION_PATH) as f:
                for doc in yaml.safe_load_all(f):
                    if not isinstance(doc, dict):
                        continue
                    for entry in doc.get("rius", []):
                        riu_id = entry.get("riu_id", "")
                        if riu_id:
                            self.classification[riu_id] = entry
        except Exception as e:
            self.load_errors.append(f"Classification load failed: {e}")

    def _load_routing(self):
        if not ROUTING_PATH.exists():
            self.load_errors.append(f"Routing file not found: {ROUTING_PATH}")
            return
        try:
            with open(ROUTING_PATH) as f:
                for doc in yaml.safe_load_all(f):
                    if not isinstance(doc, dict):
                        continue
                    for entry in doc.get("routing_entries", []):
                        riu_id = entry.get("riu_id", "")
                        if riu_id:
                            self.routing[riu_id] = entry
        except Exception as e:
            self.load_errors.append(f"Routing load failed: {e}")

    def _load_recipes(self):
        if not INTEGRATIONS_DIR.exists():
            self.load_errors.append(f"Integrations directory not found: {INTEGRATIONS_DIR}")
            return
        for subdir in sorted(INTEGRATIONS_DIR.iterdir()):
            if not subdir.is_dir():
                continue
            recipe_path = subdir / "recipe.yaml"
            if not recipe_path.exists():
                continue
            try:
                # Parse RIU references from comment header
                served_rius = self._parse_rius_served(recipe_path)

                with open(recipe_path) as f:
                    data = yaml.safe_load(f)
                if not isinstance(data, dict):
                    continue
                data["_path"] = str(recipe_path)
                data["_dir_name"] = subdir.name
                data["_served_rius"] = served_rius

                norm = normalize_name(data.get("service_name", ""))
                if norm:
                    self.recipes[norm] = data
                    # Build reverse index: RIU → recipes that serve it
                    for riu_id in served_rius:
                        self.recipe_riu_index.setdefault(riu_id, []).append(norm)
            except Exception as e:
                self.load_errors.append(f"Recipe load failed ({recipe_path}): {e}")

    @staticmethod
    def _parse_rius_served(recipe_path: Path) -> List[str]:
        """Extract RIU IDs from the '# RIUs served:' comment in recipe headers."""
        rius = []
        try:
            with open(recipe_path) as f:
                for line in f:
                    if not line.startswith("#"):
                        break
                    if "RIUs served:" in line or "rius served:" in line.lower():
                        rius = re.findall(r"RIU-\d+", line)
                        break
        except Exception:
            pass
        return rius

    def find_recipe_for_service(self, service_name: str, riu_id: str = "",
                               allow_riu_fallback: bool = True) -> Optional[Dict[str, Any]]:
        """Find the best matching recipe for a service name and optional RIU context.

        Matching strategies (in priority order):
        1. Exact normalized name match (e.g., "OpenRouter" → openrouter recipe)
        2. Substring match (normalized recipe name in normalized service name, or vice versa)
        3. Reverse RIU index — only when strategies 1 and 2 fail AND allow_riu_fallback
           is True. If a recipe declares it serves this RIU, return it as a fallback.
           This catches cases like RIU-522 where the service is "Helicone" (no recipe)
           but the OpenRouter recipe declares "RIUs served: RIU-522".

        Set allow_riu_fallback=False for display contexts (traverse output) where
        you only want to show recipes that directly match the service name.
        """
        norm = normalize_name(service_name)

        # Strategy 1: Exact normalized match
        if norm in self.recipes:
            return self.recipes[norm]

        # Strategy 2: Substring match
        for recipe_name, recipe_data in self.recipes.items():
            if len(recipe_name) >= 4 and len(norm) >= 4:
                if recipe_name in norm or norm in recipe_name:
                    return recipe_data

        # Strategy 3: Reverse RIU index (fallback only)
        if allow_riu_fallback and riu_id and riu_id in self.recipe_riu_index:
            recipe_names = self.recipe_riu_index[riu_id]
            if recipe_names:
                return self.recipes.get(recipe_names[0])

        return None


# ── Commands ──────────────────────────────────────────────────────

def cmd_traverse(pis: PISData, riu_id: str) -> int:
    """Traverse a single RIU across all four data layers."""
    tax = pis.taxonomy.get(riu_id)
    if not tax:
        print(f"ERROR: {riu_id} not found in taxonomy", file=sys.stderr)
        return 1

    name = tax.get("name", "UNNAMED")
    problem = tax.get("problem_pattern", "") or tax.get("problem_statement", "")
    workstreams = tax.get("workstreams", [])
    agents = tax.get("agent_types", [])

    print(f"{riu_id}: {name}")

    # Classification
    cls = pis.classification.get(riu_id)
    cls_type = cls.get("classification", "MISSING") if cls else "MISSING"
    print(f"Classification: {cls_type}")

    if problem:
        print(f"Problem: {problem}")

    if workstreams:
        print(f"Workstreams: {', '.join(workstreams)}")

    # Service routing
    routing = pis.routing.get(riu_id)
    if routing and routing.get("services"):
        print("Service Routing:")
        for i, svc in enumerate(routing["services"], 1):
            svc_name = svc.get("name", "UNNAMED")
            print(f"  {i}. {svc_name} (PIS Score: {_compute_pis_score(svc, pis, riu_id)})")
            cost_est = svc.get("cost_estimate", "")
            if cost_est:
                print(f"     - Cost: {cost_est}")
            # For display: only show recipe if it directly matches this service name
            # (not via RIU index fallback, which would show the wrong recipe)
            recipe = pis.find_recipe_for_service(svc_name, riu_id, allow_riu_fallback=False)
            if recipe:
                rel_path = _relative_recipe_path(recipe)
                print(f"     - Recipe: {rel_path}")
                free_tier = recipe.get("free_tier", {})
                if isinstance(free_tier, dict):
                    avail = free_tier.get("availability", "")
                    if avail:
                        print(f"     - Free tier: {avail}")
            else:
                print("     - Recipe: NOT FOUND")
    elif cls_type == "both":
        print("Service Routing: MISSING (expected for 'both' classification)")
    else:
        print("Service Routing: N/A (internal_only)")

    if agents:
        print(f"Palette Agents: {', '.join(agents)}")

    return 0


def cmd_coverage(pis: PISData) -> int:
    """Report coverage across all four data layers."""
    total_rius = len(pis.taxonomy)
    total_classified = len(pis.classification)
    both_ids = [rid for rid, c in pis.classification.items() if c.get("classification") == "both"]
    both_count = len(both_ids)

    routed_count = sum(1 for rid in both_ids if rid in pis.routing)

    full_entries = 0
    stub_entries = 0
    for rid in both_ids:
        r = pis.routing.get(rid)
        if not r:
            continue
        services = r.get("services", [])
        if services and any(s.get("cost_estimate") for s in services):
            full_entries += 1
        else:
            stub_entries += 1

    # Recipes matched to both RIUs (using improved matching)
    recipes_matched = 0
    for rid in both_ids:
        r = pis.routing.get(rid)
        if not r:
            continue
        for svc in r.get("services", []):
            if pis.find_recipe_for_service(svc.get("name", ""), rid):
                recipes_matched += 1
                break

    # Full traversal: every RIU has all applicable layers
    full_traversal = 0
    for riu_id in pis.taxonomy:
        cls = pis.classification.get(riu_id)
        if not cls:
            continue
        if cls.get("classification") == "internal_only":
            full_traversal += 1
        elif cls.get("classification") == "both" and riu_id in pis.routing:
            full_traversal += 1

    print("Layer Coverage Report")
    print("\u2500" * 21)
    print(f"Taxonomy:          {total_rius}/{total_rius} (100.0%)")
    print(f"Classification:    {total_classified}/{total_rius} ({100*total_classified/max(total_rius,1):.1f}%)")
    print(f"Service Routing:    {routed_count}/{both_count}  both RIUs have routing entries ({full_entries} full, {stub_entries} stubs)")
    print(f"Integration Recipes: {recipes_matched}/{both_count} both RIUs have matching recipes")
    print(f"Full traversal:     {full_traversal}/{total_rius} RIUs have complete data across all applicable layers")
    return 0


def cmd_cost(pis: PISData, riu_ids: List[str]) -> int:
    """Extract cost data for specified RIUs from recipes and routing."""
    found_any = False

    for riu_id in riu_ids:
        tax = pis.taxonomy.get(riu_id)
        if not tax:
            print(f"WARNING: {riu_id} not found in taxonomy")
            continue

        routing = pis.routing.get(riu_id)
        if not routing or not routing.get("services"):
            print(f"\n{riu_id}: {tax.get('name', '')}")
            print("  No service routing data")
            continue

        found_any = True
        print(f"\n{riu_id}: {tax.get('name', '')}")

        for svc in routing["services"]:
            svc_name = svc.get("name", "UNNAMED")
            # For cost display: only show recipe cost if it directly matches this service
            # (not via RIU index fallback, which would show the wrong service's costs)
            recipe = pis.find_recipe_for_service(svc_name, riu_id, allow_riu_fallback=False)

            print(f"  {svc_name}:")
            if recipe and recipe.get("cost_per_unit"):
                for key, val in recipe["cost_per_unit"].items():
                    print(f"    - {key}: {val}")
                free_tier = recipe.get("free_tier", {})
                if isinstance(free_tier, dict):
                    avail = free_tier.get("availability", "")
                    if avail:
                        print(f"    - Free tier: {avail}")
            elif svc.get("cost_estimate"):
                print(f"    - {svc['cost_estimate']}")
            else:
                print("    - Cost data not available")

    if not found_any:
        print("No cost data found for any specified RIUs")
        return 1
    return 0


def cmd_gaps(pis: PISData) -> int:
    """Find 'both' RIUs that have no matching recipe for any of their services."""
    both_ids = sorted(
        rid for rid, c in pis.classification.items()
        if c.get("classification") == "both"
    )
    gaps = []

    for rid in both_ids:
        routing = pis.routing.get(rid)
        if not routing or not routing.get("services"):
            gaps.append((rid, ["No routing entry"]))
            continue

        has_recipe = False
        for svc in routing["services"]:
            if pis.find_recipe_for_service(svc.get("name", ""), rid):
                has_recipe = True
                break

        if not has_recipe:
            svc_names = [s.get("name", "?") for s in routing["services"]]
            gaps.append((rid, svc_names))

    if gaps:
        print(f"Found {len(gaps)} 'both' RIUs missing recipes:\n")
        for rid, names in gaps:
            tax = pis.taxonomy.get(rid)
            label = tax.get("name", "UNKNOWN") if tax else "UNKNOWN"
            print(f"{rid}: {label}")
            print(f"  No recipe for: {', '.join(names)}")
    else:
        print("No gaps found \u2014 all 'both' RIUs have matching recipes")
    return 0


def cmd_stack(pis: PISData, keyword: str) -> int:
    """Find RIUs matching a keyword and recommend tools."""
    kw = keyword.lower()
    matches = []

    for riu_id, tax in pis.taxonomy.items():
        haystack = " ".join([
            tax.get("name", ""),
            tax.get("problem_pattern", ""),
            tax.get("execution_intent", ""),
            " ".join(tax.get("workstreams", [])),
            " ".join(tax.get("tags", [])),
        ]).lower()
        if kw in haystack:
            matches.append(riu_id)

    if not matches:
        print(f"No RIUs found matching '{keyword}'")
        return 1

    print(f"Found {len(matches)} RIUs matching '{keyword}':\n")
    for riu_id in sorted(matches):
        tax = pis.taxonomy[riu_id]
        cls = pis.classification.get(riu_id)
        routing = pis.routing.get(riu_id)

        print(f"{riu_id}: {tax.get('name', '')}")
        if cls:
            print(f"  Classification: {cls.get('classification', '?')}")
        if routing and routing.get("services"):
            print("  Recommended tools:")
            for svc in routing["services"][:3]:
                score = _compute_pis_score(svc, pis, riu_id)
                print(f"    - {svc.get('name', '?')} (Score: {score})")
        print()
    return 0


def cmd_check(pis: PISData) -> int:
    """Validate cross-layer consistency across all four data layers."""
    results: List[Tuple[str, bool, List[str]]] = []

    # Check 1: Every taxonomy RIU has a classification
    missing = [rid for rid in pis.taxonomy if rid not in pis.classification]
    results.append(("Every RIU in taxonomy has a classification entry", len(missing) == 0, missing[:5]))

    # Check 2: Every "both" RIU has a routing entry
    both_ids = [rid for rid, c in pis.classification.items() if c.get("classification") == "both"]
    missing_routing = [rid for rid in both_ids if rid not in pis.routing]
    results.append(("Every 'both' RIU has a service routing entry", len(missing_routing) == 0, missing_routing[:5]))

    # Check 3: Every service in routing has a matching recipe
    unmatched = []
    for rid, entry in pis.routing.items():
        for svc in entry.get("services", []):
            svc_name = svc.get("name", "")
            if not pis.find_recipe_for_service(svc_name, rid):
                unmatched.append(f"{rid}:{svc_name}")
    results.append(("Every service in routing has a matching recipe (or is flagged)", len(unmatched) == 0, unmatched[:5]))

    # Check 4: No orphaned recipes (or explicitly flagged standalone recipes)
    routed_names: Set[str] = set()
    for entry in pis.routing.values():
        for svc in entry.get("services", []):
            routed_names.add(normalize_name(svc.get("name", "")))
    # Also include names reachable via RIU index
    for rid_list in pis.recipe_riu_index.values():
        for rn in rid_list:
            routed_names.add(rn)
    orphaned = [name for name in pis.recipes if name not in routed_names]
    unflagged_orphans = [name for name in orphaned if name not in ALLOWED_ORPHAN_RECIPES]
    flagged_orphans = [name for name in orphaned if name in ALLOWED_ORPHAN_RECIPES]
    orphan_details = []
    if unflagged_orphans:
        orphan_details.extend(unflagged_orphans[:5])
    elif flagged_orphans:
        orphan_details.extend([f"{name} (flagged standalone)" for name in flagged_orphans[:5]])
    results.append(("No orphaned recipes (recipe exists but RIU not classified as 'both', or is flagged)", len(unflagged_orphans) == 0, orphan_details))

    # Check 5: Agent names in taxonomy match known agent list
    known_agents = {
        "ARK:Argentavis", "ARK:Yutyrannus", "ARK:Tyrannosaurus",
        "ARK:Therizinosaurus", "ARK:Ankylosaurus", "ARK:Velociraptor",
        "ARK:Parasaurolophus", "ARK:Corythosaurus", "ARK:Orchestrator",
        "Human:Delivery",
    }
    unknown = set()
    for tax in pis.taxonomy.values():
        for agent in tax.get("agent_types", []):
            if agent not in known_agents:
                unknown.add(agent)
    results.append(("Agent names in taxonomy match known agent list", len(unknown) == 0, list(unknown)[:5]))

    # Check 6: No data load errors
    results.append(("No data load errors", len(pis.load_errors) == 0, pis.load_errors[:5]))

    # Print summary
    print("Cross-Layer Consistency Check")
    print("\u2500" * 29)
    passed = 0
    for desc, ok, details in results:
        status = "[PASS]" if ok else "[FAIL]"
        print(f"{status} {desc}")
        if not ok and details:
            for d in details:
                print(f"       {d}")
        if ok:
            passed += 1

    print(f"\nSummary: {passed}/{len(results)} checks passed")
    return 0 if passed == len(results) else 1


# ── Helpers ──────────────────────────────────────────────────────

def _compute_pis_score(svc: Dict[str, Any], pis: PISData, riu_id: str) -> int:
    """Compute a PIS confidence score for a service recommendation.

    Scoring components (0-100):
      - Has cost_estimate: +25
      - Has recipe: +30
      - signal_strength high=25, medium=15, low=5
      - integration_status integrated=20, available=15, evaluate=10, recipe_needed=5
    """
    score = 0
    if svc.get("cost_estimate"):
        score += 25
    if pis.find_recipe_for_service(svc.get("name", ""), riu_id):
        score += 30
    strength = svc.get("signal_strength", "")
    score += {"high": 25, "medium": 15, "low": 5}.get(str(strength), 0)
    status = svc.get("integration_status", "")
    score += {"integrated": 20, "available": 15, "evaluate": 10, "recipe_needed": 5}.get(status, 0)
    return min(score, 100)


def _relative_recipe_path(recipe: Dict[str, Any]) -> str:
    """Return recipe path relative to repo root."""
    full = recipe.get("_path", "")
    if not full:
        return "UNKNOWN"
    try:
        return str(Path(full).relative_to(REPO_ROOT))
    except ValueError:
        return full


# ── CLI ──────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="PIS Query Engine — traverse Palette Intelligence System data"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("traverse", help="Full traversal of a single RIU")
    p.add_argument("riu_id", help="RIU ID (e.g., RIU-082)")

    sub.add_parser("coverage", help="Layer coverage report")

    p = sub.add_parser("cost", help="Cost data for specified RIUs")
    p.add_argument("riu_ids", nargs="+", help="One or more RIU IDs")

    sub.add_parser("gaps", help="Find 'both' RIUs missing recipes")

    p = sub.add_parser("stack", help="Find RIUs by keyword and recommend tools")
    p.add_argument("keyword", help="Search keyword")

    sub.add_parser("check", help="Cross-layer consistency validation")

    args = parser.parse_args()

    pis = PISData()
    pis.load_all()

    dispatch = {
        "traverse": lambda: cmd_traverse(pis, args.riu_id),
        "coverage": lambda: cmd_coverage(pis),
        "cost": lambda: cmd_cost(pis, args.riu_ids),
        "gaps": lambda: cmd_gaps(pis),
        "stack": lambda: cmd_stack(pis, args.keyword),
        "check": lambda: cmd_check(pis),
    }
    return dispatch[args.command]()


if __name__ == "__main__":
    sys.exit(main())
