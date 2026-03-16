#!/usr/bin/env python3
"""
Comprehensive Palette System Audit
Validates all components for OpenAI interview readiness
"""

import yaml
import json
import os
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any, Tuple

class PaletteAuditor:
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.issues = []
        self.warnings = []
        self.successes = []
        
    def log_issue(self, category: str, severity: str, message: str):
        self.issues.append({"category": category, "severity": severity, "message": message})
    
    def log_warning(self, category: str, message: str):
        self.warnings.append({"category": category, "message": message})
    
    def log_success(self, category: str, message: str):
        self.successes.append({"category": category, "message": message})
    
    def audit_steering_files(self) -> Dict[str, Any]:
        """Audit .kiro/steering files"""
        results = {"status": "CHECKING", "files": {}}
        
        steering_path = Path.home() / ".kiro" / "steering"
        required_files = ["palette-core.md", "assumptions.md"]
        
        for filename in required_files:
            filepath = steering_path / filename
            if filepath.exists():
                size = filepath.stat().st_size
                results["files"][filename] = {"exists": True, "size": size}
                self.log_success("steering", f"{filename} exists ({size} bytes)")
            else:
                results["files"][filename] = {"exists": False}
                self.log_issue("steering", "CRITICAL", f"Missing required file: {filename}")
        
        # Check for convergence success pattern
        conv_file = steering_path / "convergence-success-oreilly-enhancement.md"
        if conv_file.exists():
            results["files"]["convergence-pattern"] = {"exists": True}
            self.log_success("steering", "Convergence success pattern documented")
        
        results["status"] = "COMPLETE"
        return results
    
    def audit_decisions_md(self) -> Dict[str, Any]:
        """Audit decisions.md structure and content"""
        results = {"status": "CHECKING"}
        
        decisions_path = self.base_path / "decisions.md"
        if not decisions_path.exists():
            self.log_issue("decisions", "CRITICAL", "decisions.md does not exist")
            results["status"] = "MISSING"
            return results
        
        with open(decisions_path) as f:
            content = f.read()
            lines = content.split('\n')
        
        results["line_count"] = len(lines)
        results["size_bytes"] = len(content)
        
        # Check for required sections
        required_sections = [
            "Toolkit-Changing ONE-WAY DOOR Decisions",
            "RIU Taxonomy Integration Prompt",
            "Agent Assignment Rules"
        ]
        
        for section in required_sections:
            if section in content:
                self.log_success("decisions", f"Section present: {section}")
            else:
                self.log_warning("decisions", f"Section missing or renamed: {section}")
        
        # Check for agent maturity tracking
        if "impressions:" in content or "fail_gap:" in content:
            self.log_success("decisions", "Agent maturity tracking present")
        else:
            self.log_warning("decisions", "No agent maturity tracking found")
        
        results["status"] = "COMPLETE"
        return results
    
    def audit_knowledge_library(self) -> Dict[str, Any]:
        """Audit knowledge library structure and integrity"""
        results = {"status": "CHECKING"}
        
        lib_path = self.base_path / "knowledge-library" / "v1.4" / "palette_knowledge_library_v1.4.yaml"
        if not lib_path.exists():
            self.log_issue("knowledge_library", "CRITICAL", "Knowledge library v1.4 not found")
            results["status"] = "MISSING"
            return results
        
        try:
            with open(lib_path) as f:
                data = yaml.safe_load(f)
            
            # Count entries
            lib_questions = data.get("library_questions", [])
            gap_additions = data.get("gap_additions", [])
            context_specific = data.get("context_specific_questions", [])
            
            results["library_questions"] = len(lib_questions)
            results["gap_additions"] = len(gap_additions)
            results["context_specific"] = len(context_specific)
            results["total_entries"] = len(lib_questions) + len(gap_additions) + len(context_specific)
            
            self.log_success("knowledge_library", f"Total entries: {results['total_entries']}")
            
            # Validate structure of entries
            required_fields = ["id", "question", "answer", "problem_type", "difficulty", "tags", "journey_stage"]
            missing_fields = defaultdict(int)
            
            for entry in lib_questions:
                for field in required_fields:
                    if field not in entry:
                        missing_fields[field] += 1
            
            if missing_fields:
                for field, count in missing_fields.items():
                    self.log_issue("knowledge_library", "HIGH", f"{count} entries missing field: {field}")
            else:
                self.log_success("knowledge_library", "All entries have required fields")
            
            # Check for RIU references
            riu_refs = set()
            for entry in lib_questions:
                rius = entry.get("rius", [])
                riu_refs.update(rius)
            
            results["unique_riu_references"] = len(riu_refs)
            self.log_success("knowledge_library", f"References {len(riu_refs)} unique RIUs")
            
            results["status"] = "COMPLETE"
            
        except Exception as e:
            self.log_issue("knowledge_library", "CRITICAL", f"Failed to parse: {str(e)}")
            results["status"] = "ERROR"
            results["error"] = str(e)
        
        return results
    
    def audit_taxonomy(self) -> Dict[str, Any]:
        """Audit RIU taxonomy"""
        results = {"status": "CHECKING"}
        
        # Check for vnext (expected) and v1.3 (fallback)
        vnext_path = self.base_path / "taxonomy" / "releases" / "palette_taxonomy_vnext.yaml"
        v13_path = self.base_path / "taxonomy" / "releases" / "v1.3" / "palette_taxonomy_v1.3.yaml"
        
        taxonomy_path = None
        if vnext_path.exists():
            taxonomy_path = vnext_path
            results["version"] = "vnext"
        elif v13_path.exists():
            taxonomy_path = v13_path
            results["version"] = "v1.3"
            self.log_warning("taxonomy", "Using v1.3, vnext not found")
        else:
            self.log_issue("taxonomy", "CRITICAL", "No taxonomy file found")
            results["status"] = "MISSING"
            return results
        
        try:
            with open(taxonomy_path) as f:
                data = yaml.safe_load(f)
            
            rius = data.get("rius", [])
            results["riu_count"] = len(rius)
            
            # Check RIU structure
            required_riu_fields = ["riu_id", "name", "problem_pattern", "execution_intent", "workstreams"]
            missing_fields = defaultdict(int)
            
            for riu in rius:
                for field in required_riu_fields:
                    if field not in riu:
                        missing_fields[field] += 1
            
            if missing_fields:
                for field, count in missing_fields.items():
                    self.log_issue("taxonomy", "HIGH", f"{count} RIUs missing field: {field}")
            else:
                self.log_success("taxonomy", f"All {len(rius)} RIUs have required fields")
            
            # Check for agent archetypes
            archetypes = data.get("agent_archetypes", [])
            results["archetype_count"] = len(archetypes)
            self.log_success("taxonomy", f"{len(archetypes)} agent archetypes defined")
            
            results["status"] = "COMPLETE"
            
        except Exception as e:
            self.log_issue("taxonomy", "CRITICAL", f"Failed to parse: {str(e)}")
            results["status"] = "ERROR"
            results["error"] = str(e)
        
        return results
    
    def audit_relationship_graph(self) -> Dict[str, Any]:
        """Audit relationship graph integrity"""
        results = {"status": "CHECKING"}
        
        graph_path = self.base_path / "RELATIONSHIP_GRAPH.yaml"
        if not graph_path.exists():
            self.log_issue("relationship_graph", "HIGH", "Relationship graph not found")
            results["status"] = "MISSING"
            return results
        
        try:
            with open(graph_path) as f:
                data = yaml.safe_load(f)
            
            quads = data.get("quads", [])
            results["quad_count"] = len(quads)
            
            # Check for required quad fields
            required_fields = ["id", "subject", "predicate", "object"]
            invalid_quads = 0
            
            for quad in quads:
                for field in required_fields:
                    if field not in quad:
                        invalid_quads += 1
                        break
            
            if invalid_quads > 0:
                self.log_issue("relationship_graph", "HIGH", f"{invalid_quads} quads missing required fields")
            else:
                self.log_success("relationship_graph", f"All {len(quads)} quads valid")
            
            # Check for null values
            null_count = sum(1 for q in quads if q.get("object") is None or q.get("subject") is None)
            if null_count > 0:
                self.log_issue("relationship_graph", "HIGH", f"{null_count} quads have null values")
            else:
                self.log_success("relationship_graph", "No null values in graph")
            
            # Predicate distribution
            predicates = defaultdict(int)
            for quad in quads:
                predicates[quad.get("predicate", "UNKNOWN")] += 1
            
            results["predicate_distribution"] = dict(predicates)
            results["unique_predicates"] = len(predicates)
            
            self.log_success("relationship_graph", f"{len(predicates)} unique predicate types")
            
            results["status"] = "COMPLETE"
            
        except Exception as e:
            self.log_issue("relationship_graph", "CRITICAL", f"Failed to parse: {str(e)}")
            results["status"] = "ERROR"
            results["error"] = str(e)
        
        return results
    
    def audit_cross_references(self, lib_data: Dict, tax_data: Dict, graph_data: Dict) -> Dict[str, Any]:
        """Audit cross-references between components"""
        results = {"status": "CHECKING", "issues": []}
        
        # Extract RIU IDs from each source
        lib_rius = set()
        if lib_data.get("status") == "COMPLETE":
            lib_path = self.base_path / "knowledge-library" / "v1.4" / "palette_knowledge_library_v1.4.yaml"
            with open(lib_path) as f:
                data = yaml.safe_load(f)
                for entry in data.get("library_questions", []):
                    lib_rius.update(entry.get("rius", []))
        
        tax_rius = set()
        if tax_data.get("status") == "COMPLETE":
            tax_path = self.base_path / "taxonomy" / "releases" / "v1.3" / "palette_taxonomy_v1.3.yaml"
            if not tax_path.exists():
                tax_path = self.base_path / "taxonomy" / "releases" / "palette_taxonomy_vnext.yaml"
            with open(tax_path) as f:
                data = yaml.safe_load(f)
                for riu in data.get("rius", []):
                    tax_rius.add(riu.get("riu_id"))
        
        graph_rius = set()
        if graph_data.get("status") == "COMPLETE":
            graph_path = self.base_path / "RELATIONSHIP_GRAPH.yaml"
            with open(graph_path) as f:
                data = yaml.safe_load(f)
                for quad in data.get("quads", []):
                    subj = quad.get("subject", "")
                    obj = quad.get("object", "")
                    if subj.startswith("RIU-"):
                        graph_rius.add(subj)
                    if obj.startswith("RIU-"):
                        graph_rius.add(obj)
        
        # Check for orphaned references
        lib_only = lib_rius - tax_rius
        if lib_only:
            self.log_issue("cross_reference", "HIGH", f"Library references {len(lib_only)} RIUs not in taxonomy: {sorted(list(lib_only))[:5]}")
            results["issues"].append(f"lib_only: {len(lib_only)}")
        
        graph_only = graph_rius - tax_rius
        if graph_only:
            self.log_issue("cross_reference", "HIGH", f"Graph references {len(graph_only)} RIUs not in taxonomy: {sorted(list(graph_only))[:5]}")
            results["issues"].append(f"graph_only: {len(graph_only)}")
        
        if not lib_only and not graph_only:
            self.log_success("cross_reference", "All RIU references are valid")
        
        results["lib_rius"] = len(lib_rius)
        results["tax_rius"] = len(tax_rius)
        results["graph_rius"] = len(graph_rius)
        results["status"] = "COMPLETE"
        
        return results
    
    def audit_agent_definitions(self) -> Dict[str, Any]:
        """Audit agent definition files"""
        results = {"status": "CHECKING", "agents": {}}
        
        agents_path = self.base_path / "agents"
        if not agents_path.exists():
            self.log_warning("agents", "No agents directory found")
            results["status"] = "MISSING"
            return results
        
        # Find all agent directories
        agent_dirs = [d for d in agents_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        
        for agent_dir in agent_dirs:
            agent_name = agent_dir.name
            agent_info = {"path": str(agent_dir)}
            
            # Check for required files
            prompt_file = agent_dir / "prompt.md"
            config_file = agent_dir / "config.yaml"
            
            agent_info["has_prompt"] = prompt_file.exists()
            agent_info["has_config"] = config_file.exists()
            
            if prompt_file.exists() and config_file.exists():
                self.log_success("agents", f"{agent_name}: complete definition")
            elif prompt_file.exists():
                self.log_warning("agents", f"{agent_name}: missing config.yaml")
            elif config_file.exists():
                self.log_warning("agents", f"{agent_name}: missing prompt.md")
            else:
                self.log_warning("agents", f"{agent_name}: incomplete (no prompt or config)")
            
            results["agents"][agent_name] = agent_info
        
        results["agent_count"] = len(agent_dirs)
        results["status"] = "COMPLETE"
        
        return results
    
    def run_full_audit(self) -> Dict[str, Any]:
        """Run complete audit"""
        print("=" * 80)
        print("PALETTE SYSTEM COMPREHENSIVE AUDIT")
        print("=" * 80)
        print()
        
        audit_results = {}
        
        print("[1/7] Auditing steering files...")
        audit_results["steering"] = self.audit_steering_files()
        
        print("[2/7] Auditing decisions.md...")
        audit_results["decisions"] = self.audit_decisions_md()
        
        print("[3/7] Auditing knowledge library...")
        audit_results["knowledge_library"] = self.audit_knowledge_library()
        
        print("[4/7] Auditing taxonomy...")
        audit_results["taxonomy"] = self.audit_taxonomy()
        
        print("[5/7] Auditing relationship graph...")
        audit_results["relationship_graph"] = self.audit_relationship_graph()
        
        print("[6/7] Auditing cross-references...")
        audit_results["cross_references"] = self.audit_cross_references(
            audit_results["knowledge_library"],
            audit_results["taxonomy"],
            audit_results["relationship_graph"]
        )
        
        print("[7/7] Auditing agent definitions...")
        audit_results["agents"] = self.audit_agent_definitions()
        
        print()
        print("=" * 80)
        print("AUDIT SUMMARY")
        print("=" * 80)
        print()
        
        # Print issues by severity
        critical = [i for i in self.issues if i["severity"] == "CRITICAL"]
        high = [i for i in self.issues if i["severity"] == "HIGH"]
        
        print(f"✓ Successes: {len(self.successes)}")
        print(f"⚠ Warnings: {len(self.warnings)}")
        print(f"✗ Issues: {len(self.issues)} (Critical: {len(critical)}, High: {len(high)})")
        print()
        
        if critical:
            print("CRITICAL ISSUES:")
            for issue in critical:
                print(f"  [{issue['category']}] {issue['message']}")
            print()
        
        if high:
            print("HIGH PRIORITY ISSUES:")
            for issue in high:
                print(f"  [{issue['category']}] {issue['message']}")
            print()
        
        if self.warnings:
            print("WARNINGS:")
            for warning in self.warnings[:10]:  # Show first 10
                print(f"  [{warning['category']}] {warning['message']}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more")
            print()
        
        # Overall health assessment
        if len(critical) == 0 and len(high) == 0:
            health = "EXCELLENT"
        elif len(critical) == 0 and len(high) <= 2:
            health = "GOOD"
        elif len(critical) == 0:
            health = "FAIR"
        else:
            health = "NEEDS ATTENTION"
        
        print(f"OVERALL SYSTEM HEALTH: {health}")
        print()
        
        audit_results["summary"] = {
            "successes": len(self.successes),
            "warnings": len(self.warnings),
            "issues": len(self.issues),
            "critical_issues": len(critical),
            "high_issues": len(high),
            "health": health
        }
        
        return audit_results

if __name__ == "__main__":
    _root = os.environ.get("PALETTE_ROOT", os.path.join(os.path.expanduser("~"), "fde", "palette"))
    auditor = PaletteAuditor(_root)
    results = auditor.run_full_audit()

    # Save detailed results
    output_path = Path(_root) / "COMPREHENSIVE_AUDIT_2026-03-11.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"Detailed results saved to: {output_path}")
