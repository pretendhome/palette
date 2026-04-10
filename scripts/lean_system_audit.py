#!/usr/bin/env python3
"""
Lean System Architecture Audit
Identifies agentic friction, communication bottlenecks, token bloat, and context coherence issues.
Modeled after the comprehensive_palette_audit.py integrity engine.
"""

import os
import re
import yaml
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any

class LeanSystemAuditor:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.issues = []
        self.warnings = []
        self.successes = []

    def log(self, category: str, severity: str, message: str):
        entry = {"category": category, "message": message}
        if severity == "SUCCESS":
            self.successes.append(entry)
        elif severity == "WARNING":
            self.warnings.append(entry)
        else:
            entry["severity"] = severity
            self.issues.append(entry)

    def audit_agent_capabilities(self) -> Dict[str, Any]:
        """Check for role overlap and redundant capabilities in server.mjs"""
        server_path = self.base_path / "peers/adapters/generic/server.mjs"
        if not server_path.exists():
            # Fallback path if generic doesn't have it
            server_path = self.base_path / "adapters/generic/server.mjs"
            if not server_path.exists():
                self.log("capabilities", "CRITICAL", f"server.mjs not found at {server_path}")
                return {"status": "MISSING"}

        try:
            content = server_path.read_text(encoding="utf-8")
            # Extract AGENT_CONFIGS block
            match = re.search(r"const AGENT_CONFIGS = ({.*?});", content, re.DOTALL)
            if not match:
                self.log("capabilities", "HIGH", "AGENT_CONFIGS not found in server.mjs")
                return {"status": "NOT_FOUND"}

            # Rough extraction of capabilities for each agent using regex
            agent_matches = re.finditer(r"'([^']+)':\s*{[^}]*capabilities:\s*\[(.*?)\]", match.group(1))
            
            capabilities_map = {}
            for m in agent_matches:
                agent = m.group(1)
                caps = [c.strip(" '\"") for c in m.group(2).split(",") if c.strip()]
                capabilities_map[agent] = set(caps)

            # Check for overlaps
            agents = list(capabilities_map.keys())
            for i in range(len(agents)):
                for j in range(i + 1, len(agents)):
                    agent1 = agents[i]
                    agent2 = agents[j]
                    overlap = capabilities_map[agent1].intersection(capabilities_map[agent2])
                    if len(overlap) > 0:
                        if len(overlap) >= 3:
                            self.log("capabilities", "HIGH", f"High capability overlap ({len(overlap)}) between {agent1} and {agent2}: {overlap}")
                        else:
                            self.log("capabilities", "WARNING", f"Capability overlap between {agent1} and {agent2}: {overlap}")

            if len(self.issues) == 0:
                self.log("capabilities", "SUCCESS", "Agent capabilities are well-partitioned with minimal overlap")

            return {"status": "COMPLETE", "agent_count": len(agents)}
            
        except Exception as e:
            self.log("capabilities", "CRITICAL", f"Failed to parse server.mjs: {str(e)}")
            return {"status": "ERROR"}

    def audit_context_bloat(self) -> Dict[str, Any]:
        """Audit prompt sizes and steering files for token bloat"""
        agents_dir = self.base_path / "agents"
        if not agents_dir.exists():
            self.log("context", "HIGH", "agents/ directory not found")
            return {"status": "MISSING"}

        bloat_threshold_bytes = 4000 # ~1000 tokens as a rough limit for lean prompts
        prompt_sizes = {}

        for prompt_file in agents_dir.glob("*/prompt.md"):
            agent_name = prompt_file.parent.name
            size = prompt_file.stat().st_size
            prompt_sizes[agent_name] = size

            if size > bloat_threshold_bytes:
                self.log("context", "WARNING", f"Agent '{agent_name}' prompt.md is {size} bytes, potentially causing token bloat")
            else:
                self.log("context", "SUCCESS", f"Agent '{agent_name}' prompt.md is lean ({size} bytes)")

        return {"status": "COMPLETE", "analyzed_prompts": len(prompt_sizes)}

    def audit_graph_redundancy(self) -> Dict[str, Any]:
        """Check for redundant or circular paths in RELATIONSHIP_GRAPH.yaml"""
        graph_path = self.base_path / "RELATIONSHIP_GRAPH.yaml"
        if not graph_path.exists():
            self.log("graph", "HIGH", "RELATIONSHIP_GRAPH.yaml not found")
            return {"status": "MISSING"}

        try:
            with open(graph_path) as f:
                data = yaml.safe_load(f)

            quads = data.get("quads", [])
            edges = defaultdict(list)
            
            for quad in quads:
                subj = quad.get("subject")
                obj = quad.get("object")
                if subj and obj:
                    edges[subj].append(obj)

            # Simple cycle detection (depth 2)
            cycles = 0
            for node, neighbors in edges.items():
                for neighbor in neighbors:
                    if node in edges.get(neighbor, []):
                        self.log("graph", "WARNING", f"Redundant/Circular edge detected between {node} and {neighbor}")
                        cycles += 1

            if cycles == 0:
                self.log("graph", "SUCCESS", "No immediate cycles detected in relationship graph")

            return {"status": "COMPLETE", "cycles_found": cycles}

        except Exception as e:
            self.log("graph", "CRITICAL", f"Failed to parse graph: {str(e)}")
            return {"status": "ERROR"}

    def run(self):
        print("================================================================")
        print("TO GET LEAN: MULTI-AGENT ARCHITECTURE COHERENCE AUDIT")
        print("================================================================")
        
        self.audit_agent_capabilities()
        self.audit_context_bloat()
        self.audit_graph_redundancy()

        print("\n[ CRITICAL / HIGH ISSUES ]")
        for i in self.issues:
            print(f"[{i['category'].upper()}] {i['severity']}: {i['message']}")
        
        print("\n[ WARNINGS (FRICTION POINTS) ]")
        for w in self.warnings:
            print(f"[{w['category'].upper()}] {w['message']}")

        print("\n[ SUCCESSES (LEAN PRACTICES) ]")
        for s in self.successes[:5]:
            print(f"[{s['category'].upper()}] {s['message']}")
        if len(self.successes) > 5:
            print(f"... and {len(self.successes)-5} more lean practices confirmed.")

        print("\nAudit complete.")

if __name__ == "__main__":
    palette_root = os.environ.get("PALETTE_ROOT", os.path.join(os.path.expanduser("~"), "fde", "palette"))
    auditor = LeanSystemAuditor(palette_root)
    auditor.run()
