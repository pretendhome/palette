#!/usr/bin/env python3
"""
System Health Checks for Monitor Agent
Lightweight passive checks for Palette system integrity
"""

import yaml
from pathlib import Path
from typing import Dict, List, Tuple

class SystemHealthMonitor:
    """Lightweight system health checks for continuous monitoring"""
    
    def __init__(self, base_path: str = None):
        self.base_path = Path(base_path) if base_path else Path.home() / "fde" / "palette"
        self.steering_path = Path.home() / ".kiro" / "steering"
        
    def check_critical_files(self) -> Tuple[bool, List[str]]:
        """Check if critical files exist and are loadable"""
        issues = []
        
        # Critical files that must exist
        critical = {
            "palette-core.md": self.steering_path / "palette-core.md",
            "assumptions.md": self.steering_path / "assumptions.md",
            "decisions.md": self.base_path / "decisions.md",
            "knowledge_library": self.base_path / "knowledge-library" / "v1.4" / "palette_knowledge_library_v1.4.yaml",
            "taxonomy": self.base_path / "taxonomy" / "releases" / "v1.3" / "palette_taxonomy_v1.3.yaml",
        }
        
        for name, path in critical.items():
            if not path.exists():
                issues.append(f"CRITICAL: {name} not found at {path}")
        
        return len(issues) == 0, issues
    
    def check_yaml_loadable(self) -> Tuple[bool, List[str]]:
        """Check if YAML files can be loaded"""
        issues = []
        
        yaml_files = {
            "knowledge_library": self.base_path / "knowledge-library" / "v1.4" / "palette_knowledge_library_v1.4.yaml",
            "taxonomy": self.base_path / "taxonomy" / "releases" / "v1.3" / "palette_taxonomy_v1.3.yaml",
        }
        
        for name, path in yaml_files.items():
            if path.exists():
                try:
                    with open(path) as f:
                        yaml.safe_load(f)
                except Exception as e:
                    issues.append(f"CRITICAL: {name} cannot be loaded: {str(e)[:50]}")
        
        return len(issues) == 0, issues
    
    def quick_health_check(self) -> Dict:
        """Run quick health check (< 1 second)"""
        files_ok, file_issues = self.check_critical_files()
        yaml_ok, yaml_issues = self.check_yaml_loadable()
        
        all_issues = file_issues + yaml_issues
        
        return {
            "status": "HEALTHY" if not all_issues else "DEGRADED",
            "critical_issues": all_issues,
            "checks_passed": files_ok and yaml_ok,
            "timestamp": None  # Monitor will add timestamp
        }

def emit_health_signal(health_status: Dict) -> str:
    """Format health status as monitor signal"""
    if health_status["checks_passed"]:
        return """✅ SYSTEM HEALTH: NORMAL

All critical files present and loadable.
Status: HEALTHY
"""
    else:
        issues_text = "\n".join(f"  - {issue}" for issue in health_status["critical_issues"])
        return f"""⚠️ SIGNAL DETECTED: SYSTEM HEALTH DEGRADED

Status: {health_status["status"]}
Critical issues detected:
{issues_text}

Routing recommendation:
- For immediate attention → Human
- For diagnosis → Debugger
"""

if __name__ == "__main__":
    monitor = SystemHealthMonitor()
    health = monitor.quick_health_check()
    print(emit_health_signal(health))
