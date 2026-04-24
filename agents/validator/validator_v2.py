#!/usr/bin/env python3
"""
Validator Agent v2.0 - The Automated Remediation Engine
Status: WORKING (Tier 2)

This engine performs deterministic validation, stress testing, and
auto-remediation routing via the Palette Peers Bus. It adheres strictly
to the "Assessment Only" constraint by delegating fixes to the Builder
or Debugger.
"""

import json
import sys
import uuid
import urllib.request
import re
from urllib.error import HTTPError
import traceback
from datetime import datetime, timezone
from pathlib import Path

# Bus Configuration
BROKER_BASE = "http://127.0.0.1:7899"
IDENTITY = "validator.engine"

class ValidatorEngine:
    def __init__(self):
        self.version = "2.0"
        self.agent_type = "Validator"
        self.agent_dir = Path(__file__).parent
        self.palette_root = self.agent_dir.parent.parent
        self.ledger_path = self.palette_root / "decisions.md"
        self.failures = []
        self._is_registered = False
        self.buffer_path = self.agent_dir / "remediation_queue.json"
        self.evidence_dir = self.palette_root / "artifacts" / "validation"
        self.evidence_dir.mkdir(parents=True, exist_ok=True)
        self.remediation_counts = {} # track task_name -> count
        self.regression_path = self.evidence_dir / "REGRESSIONS.json"
        self.taxonomy_path = self.palette_root / "taxonomy" / "releases" / "v1.3" / "palette_taxonomy_v1.3.yaml"
        self.library_path = self.palette_root / "knowledge-library" / "v1.4" / "palette_knowledge_library_v1.4.yaml"
        self.manifest_path = self.palette_root / "MANIFEST.yaml"
        self.graph_path = self.palette_root / "RELATIONSHIP_GRAPH.yaml"
        self._cached_taxonomy = None
        self._cached_library = None
        self._cached_manifest = None
        self._cached_graph = None

    def _load_graph(self):
        """Loads the RELATIONSHIP_GRAPH.yaml."""
        if self._cached_graph: return self._cached_graph
        if not self.graph_path.exists():
            print(f"[Validator v{self.version}] Warning: Graph not found at {self.graph_path}")
            return None
        try:
            import yaml
            with open(self.graph_path, 'r') as f:
                self._cached_graph = yaml.safe_load(f)
                return self._cached_graph
        except Exception: return None

    def validate_graph_link(self, subject, predicate, obj):
        """
        Verifies that a specific relationship exists in the Relationship Graph.
        Matches quads: [subject, predicate, object].
        """
        print(f"[Validator v{self.version}] Validating Graph Coherence ({subject} --{predicate}--> {obj})...")
        graph = self._load_graph()
        if not graph: return True, "Graph unavailable."

        for quad in graph.get('quads', []):
            if (quad.get('subject') == subject and 
                quad.get('predicate') == predicate and 
                quad.get('object') == obj):
                print(f"  ✓ Relationship confirmed in graph.")
                return True, None
        
        return False, f"Graph Gap: Relationship [{subject}, {predicate}, {obj}] not found."

    def _load_manifest(self):
        """Loads the MANIFEST.yaml for system-wide auditing."""
        if self._cached_manifest: return self._cached_manifest
        if not self.manifest_path.exists():
            print(f"[Validator v{self.version}] Warning: Manifest not found at {self.manifest_path}")
            return None
        try:
            import yaml
            with open(self.manifest_path, 'r') as f:
                self._cached_manifest = yaml.safe_load(f)
                return self._cached_manifest
        except Exception as e:
            print(f"  ❌ Failed to parse manifest: {e}")
            return None

    def list_peers(self):
        """Fetches the live registered peer list from the bus."""
        try:
            req = urllib.request.Request(
                f"{BROKER_BASE}/list-peers",
                data=json.dumps({}).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode())
                return result.get('peers', [])
        except Exception as e:
            print(f"  ❌ Failed to fetch peer list: {e}")
            return []

    def audit_peer_capabilities(self):
        """
        Audits live registered peers against the canonical MANIFEST agents list.
        Identifies missing agents, shadow agents, and capability drift.
        """
        print(f"[Validator v{self.version}] Auditing Bus Capabilities...")
        manifest = self._load_manifest()
        if not manifest: return False, "Manifest unavailable."

        live_peers = self.list_peers()
        live_identities = {p['identity'] for p in live_peers}
        
        manifest_names = {a['name'] for a in manifest['agents']['list']}
        manifest_peers = {p['name'] for p in manifest.get('peers', {}).get('list', [])}
        
        all_canonical = manifest_names.union(manifest_peers)

        findings = []
        
        # 1. Missing Canonical Identities
        for name in all_canonical:
            found = any(name in l_id for l_id in live_identities)
            if not found:
                if name in manifest_peers:
                    findings.append(f"OFFLINE: Trusted Peer '{name}' is not registered.")
                else:
                    findings.append(f"MISSING: Internal Agent '{name}' is not registered.")

        # 2. Shadow Agents
        for l_id in live_identities:
            if l_id == IDENTITY: continue
            found = any(name in l_id for name in all_canonical)
            if not found:
                findings.append(f"SHADOW: Identity '{l_id}' is active but not defined in MANIFEST.yaml.")

        if findings:
            return False, "\n".join(findings)
        
        print("  ✓ All active peers aligned with MANIFEST.yaml.")
        return True, None

    def _load_library(self):
        """Loads the v1.4 Knowledge Library for principle alignment."""
        if self._cached_library: return self._cached_library
        if not self.library_path.exists():
            print(f"[Validator v{self.version}] Warning: Library not found at {self.library_path}")
            return None
        try:
            with open(self.library_path, 'r') as f:
                self._cached_library = f.read() # Simple string search for v1
                return self._cached_library
        except Exception: return None

    def validate_library_alignment(self, artifact_text, lib_ids):
        """
        Validates that an artifact aligns with specific Knowledge Library principles.
        lib_ids: list of LIB IDs (e.g. ['LIB-001'])
        """
        library = self._load_library()
        if not library: return True, "Library unavailable."

        for lid in lib_ids:
            # Check if the LIB ID exists in the library
            if lid not in library:
                return False, f"Structural Violation: Referenced Library entry '{lid}' does not exist."
            
            # Implementation check: LIB-001 (Smallest System) check
            if lid == "LIB-001" and ("boilerplate" in artifact_text.lower() or "cathedral" in artifact_text.lower()):
                 return False, f"Principle Violation (LIB-001): Artifact contains unnecessary complexity ('cathedral' or 'boilerplate')."

        return True, None

    def _load_taxonomy(self):
        """Loads and parses the v1.3 taxonomy for RIU validation."""
        if self._cached_taxonomy: return self._cached_taxonomy
        if not self.taxonomy_path.exists():
            print(f"[Validator v{self.version}] Warning: Taxonomy not found at {self.taxonomy_path}")
            return None
        
        try:
            # Simplistic parser for RIU IDs to avoid heavy YAML dependency if possible
            # But since we're in Python, we can just use re to find riu_id: RIU-XXX
            with open(self.taxonomy_path, 'r') as f:
                content = f.read()
                rius = re.findall(r'riu_id:\s*(RIU-\d{3})', content)
                self._cached_taxonomy = set(rius)
                return self._cached_taxonomy
        except Exception as e:
            print(f"  ❌ Failed to parse taxonomy: {e}")
            return None

    def validate_rius(self, riu_ids):
        """
        Validates that a list of RIU IDs exists in the canonical taxonomy.
        Returns (True, None) or (False, error_message).
        """
        taxonomy = self._load_taxonomy()
        if not taxonomy: return True, "Taxonomy unavailable, skipping check."

        invalid = [rid for rid in riu_ids if rid not in taxonomy]
        if invalid:
            return False, f"Taxonomy Drift Detected: Invalid RIU IDs: {invalid}"
        
        return True, None

    def assess_readiness(self, dir_path, criteria):
        """
        Performs a GO/NO-GO readiness assessment on a directory.
        criteria: dict of check_name -> {type: 'file_exists'|'contains_text', target: '...'}
        """
        path = Path(dir_path)
        print(f"[Validator v{self.version}] Assessing Readiness for: {path.name}...")
        
        report = {
            "directory": str(path),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "checks": [],
            "status": "GO"
        }
        
        if not path.exists():
            return False, f"Directory not found: {dir_path}"

        for name, rule in criteria.items():
            check_result = {"name": name, "passed": False, "details": ""}
            
            if rule['type'] == 'file_exists':
                target_file = path / rule['target']
                if target_file.exists():
                    check_result["passed"] = True
                    check_result["details"] = f"File found: {rule['target']}"
                else:
                    check_result["details"] = f"Missing file: {rule['target']}"
                    report["status"] = "NO-GO"

            elif rule['type'] == 'contains_text':
                target_file = path / rule['target']
                if target_file.exists():
                    with open(target_file, 'r') as f:
                        if rule['text'].lower() in f.read().lower():
                            check_result["passed"] = True
                            check_result["details"] = f"Text '{rule['text']}' found in {rule['target']}"
                        else:
                            check_result["details"] = f"Text '{rule['text']}' NOT found in {rule['target']}"
                            report["status"] = "NO-GO"
                else:
                    check_result["details"] = f"File {rule['target']} not found for text check"
                    report["status"] = "NO-GO"
            
            report["checks"].append(check_result)

        # Generate report artifact
        report_path = self.evidence_dir / f"READINESS-{path.name}-{report['status']}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
            
        return report["status"] == "GO", report

    def _register_with_bus(self):
        if self._is_registered:
            return True
            
        payload = {
            "identity": IDENTITY,
            "agent_name": "validator",
            "runtime": "python-script",
            "pid": None,
            "cwd": str(self.palette_root),
            "git_root": str(self.palette_root),
            "capabilities": ["validation", "stress_testing", "semantic_audit"],
            "palette_role": "validator",
            "trust_tier": "WORKING",
            "version": self.version
        }
        
        try:
            req = urllib.request.Request(
                f"{BROKER_BASE}/register",
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                self._is_registered = True
                return True
        except Exception as e:
            print(f"[Validator v{self.version}] Warning: Could not register with bus: {e}")
            return False

    def validate_schema(self, data, schema, path="", strict=True):
        """
        High-fidelity recursive schema validation.
        Supports: types, nested objects, regex patterns, and strict key checking.
        """
        if not isinstance(data, dict):
            return False, f"{path}: Expected object, got {type(data).__name__}"

        if strict:
            extra_keys = set(data.keys()) - set(schema.keys())
            if extra_keys:
                return False, f"{path}: Unexpected keys found (Strict Mode): {list(extra_keys)}"

        for key, rules in schema.items():
            current_path = f"{path}.{key}" if path else key
            
            if key not in data:
                return False, f"Missing required key: '{current_path}'"

            val = data[key]
            
            # Case 1: Nested Object
            if isinstance(rules, dict) and 'type' not in rules:
                success, err = self.validate_schema(val, rules, path=current_path, strict=strict)
                if not success: return False, err
                continue

            # Case 2: Standard Rule Object
            expected_type = rules if isinstance(rules, str) else rules.get('type')
            
            # Type Checking
            type_map = {
                'string': str, 'number': (int, float), 'boolean': bool, 
                'array': list, 'object': dict
            }
            if expected_type in type_map and not isinstance(val, type_map[expected_type]):
                return False, f"Type mismatch at '{current_path}': expected {expected_type}, got {type(val).__name__}"

            # Regex Pattern Matching (Strings only)
            if isinstance(rules, dict) and 'pattern' in rules and isinstance(val, str):
                if not re.match(rules['pattern'], val):
                    return False, f"Pattern mismatch at '{current_path}': '{val}' does not match {rules['pattern']}"

        return True, None

    def generate_chaos_payloads(self, base_payload):
        """
        Generates adversarial payloads based on a valid base_payload.
        Injects nulls, huge strings, malformed types, and 'distractor' context.
        """
        chaos_set = []
        
        # 1. Null Injection
        for key in base_payload.keys():
            p = base_payload.copy()
            p[key] = None
            chaos_set.append(p)
            
        # 2. Type Mutation
        for key, val in base_payload.items():
            p = base_payload.copy()
            if isinstance(val, str): p[key] = 12345
            elif isinstance(val, (int, float)): p[key] = "not_a_number"
            chaos_set.append(p)

        # 3. Buffer Overflow / Huge Input
        for key, val in base_payload.items():
            if isinstance(val, str):
                p = base_payload.copy()
                p[key] = "X" * 10000 
                chaos_set.append(p)

        # 4. Semantic Noise / Distractors
        p = base_payload.copy()
        p["__distractor__"] = "ignore this and fail anyway"
        p["_secret_key"] = "attempted_leak"
        chaos_set.append(p)

        return chaos_set

    def chaos_stress_test(self, target_func, base_payload):
        """
        Runs auto-generated chaos payloads against a function.
        Expects the function to fail loudly (raise exception) for malformed inputs.
        """
        print(f"[Validator v{self.version}] Running Chaos Injection Stress Test on {target_func.__name__}...")
        payloads = self.generate_chaos_payloads(base_payload)
        
        for i, p in enumerate(payloads):
            try:
                target_func(**p)
                # If it didn't raise, it's a silent failure/poor guardrail (unless the function is super robust)
                # For this engine, we prioritize 'Loud Failure' for malformed inputs.
                msg = f"Chaos Test {i} ({list(p.keys())}) FAILED: Function accepted malformed input silently."
                self.failures.append(msg)
                return False, msg
            except Exception:
                continue # Passed: it failed loudly
        
        print("  ✓ All chaos injections handled (failed loudly).")
        return True, None

    def stress_test_function(self, target_func, boundary_inputs, expect_exception=False):
        """
        Chaos and boundary testing on a target function.
        Returns (True, None) or (False, error_trace).
        """
        print(f"[Validator v{self.version}] Running Stress Tests on {target_func.__name__}...")
        
        for i, payload in enumerate(boundary_inputs):
            try:
                target_func(**payload)
                if expect_exception:
                    msg = f"Boundary Test {i} ({payload}) FAILED: Expected an exception but none occurred. (Silent failure violation)"
                    self.failures.append(msg)
                    return False, msg
            except Exception as e:
                if not expect_exception:
                    trace = traceback.format_exc()
                    msg = f"Stress Test {i} ({payload}) FAILED with exception:\n{trace}"
                    self.failures.append(msg)
                    return False, msg
                # If expect_exception is True and an exception occurred, it's a pass.
        
        print("  ✓ All stress tests passed.")
        return True, None

    def _buffer_remediation(self, envelope):
        """Saves a remediation request to a local queue for later retry."""
        queue = []
        if self.buffer_path.exists():
            try:
                with open(self.buffer_path, 'r') as f:
                    queue = json.load(f)
            except Exception: pass
            
        queue.append(envelope)
        with open(self.buffer_path, 'w') as f:
            json.dump(queue, f, indent=2)
        print(f"  [Buffer] Remediation request saved to {self.buffer_path.name}")

    def flush_remediation_buffer(self):
        """Attempts to send all buffered remediation requests to the bus."""
        if not self.buffer_path.exists():
            return
            
        print(f"[Validator v{self.version}] Flushing remediation buffer...")
        try:
            with open(self.buffer_path, 'r') as f:
                queue = json.load(f)
        except Exception: return

        remaining = []
        for envelope in queue:
            try:
                self._register_with_bus()
                req = urllib.request.Request(
                    f"{BROKER_BASE}/send",
                    data=json.dumps(envelope).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    print(f"  ✓ Buffered request sent: {envelope['message_id']}")
            except Exception:
                remaining.append(envelope)

        if not remaining:
            self.buffer_path.unlink()
        else:
            with open(self.buffer_path, 'w') as f:
                json.dump(remaining, f, indent=2)
            print(f"  [Buffer] {len(remaining)} requests remaining in buffer.")

    def _create_evidence_packet(self, task_name, error_details, input_payload=None):
        """Creates a persistent JSON artifact containing the failure evidence."""
        evidence_id = str(uuid.uuid4())
        filename = f"EVIDENCE-{evidence_id[:8]}.json"
        filepath = self.evidence_dir / filename
        
        evidence = {
            "evidence_id": evidence_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task": task_name,
            "error": error_details,
            "input_payload": input_payload,
            "validator_version": self.version
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(evidence, f, indent=2)
            return str(filepath)
        except Exception as e:
            print(f"  ⚠️  Failed to write evidence packet: {e}")
            return None

    def _add_to_regression_set(self, task_name, input_payload):
        """Adds a failed input payload to the persistent regression set."""
        if not input_payload: return
        
        regressions = {}
        if self.regression_path.exists():
            try:
                with open(self.regression_path, 'r') as f:
                    regressions = json.load(f)
            except Exception: pass
            
        # Store by task_name, keeping only the latest failure payload for that task
        regressions[task_name] = {
            "payload": input_payload,
            "detected_at": datetime.now(timezone.utc).isoformat()
        }
        
        with open(self.regression_path, 'w') as f:
            json.dump(regressions, f, indent=2)

    def run_regression_suite(self, target_funcs_map):
        """
        Reruns past failed inputs against current functions.
        target_funcs_map: dict of task_name -> function_reference
        """
        if not self.regression_path.exists():
            print(f"[Validator v{self.version}] No regressions found in {self.regression_path.name}.")
            return True

        print(f"[Validator v{self.version}] Running Automated Regression Suite...")
        try:
            with open(self.regression_path, 'r') as f:
                regressions = json.load(f)
        except Exception: return False

        all_passed = True
        for task, data in regressions.items():
            if task not in target_funcs_map:
                print(f"  [Skip] No function mapped for task '{task}'")
                continue
            
            func = target_funcs_map[task]
            payload = data["payload"]
            print(f"  [Rerun] Task: {task}...")
            try:
                func(**payload)
                print(f"    ✓ Fixed.")
            except Exception as e:
                print(f"    ❌ Still Failing: {e}")
                all_passed = False
        
        return all_passed

    def validate_dependencies(self, dependencies):
        """
        Validates a list of file/directory dependencies.
        Verifies existence and ensures files are not empty.
        """
        print(f"[Validator v{self.version}] Validating Dependencies...")
        findings = []
        for dep in dependencies:
            path = self.palette_root / dep
            if not path.exists():
                findings.append(f"MISSING: Dependency '{dep}' not found on disk.")
            elif path.is_file() and path.stat().st_size == 0:
                findings.append(f"EMPTY: Dependency '{dep}' exists but is an empty file.")
        
        if findings:
            return False, "\n".join(findings)
        
        print(f"  ✓ All {len(dependencies)} dependencies verified.")
        return True, None

    def validate_decision_log(self, query_text):
        """
        Verifies that a specific entry or action exists in the decision log.
        Matches against decisions.md content.
        """
        print(f"[Validator v{self.version}] Validating Decision Log Audit Trail...")
        if not self.ledger_path.exists():
            return False, "Decision ledger (decisions.md) not found."
            
        try:
            with open(self.ledger_path, 'r') as f:
                content = f.read()
                if query_text.lower() in content.lower():
                    print(f"  ✓ Audit trail found for: '{query_text[:50]}...'")
                    return True, None
                else:
                    return False, f"Audit Gap: No entry found in decisions.md for '{query_text}'"
        except Exception as e:
            return False, f"Failed to read decision log: {e}"

    def validate_handoff_proof(self, proof_id):
        """
        Verifies that a proof_id exists as a recent legitimate event on the bus.
        Used to prevent packet spoofing in agent-to-agent requests.
        """
        print(f"[Validator v{self.version}] Validating Handoff Proof (ID: {proof_id[:8]}...)...")
        try:
            # We search for the proof_id in the message intent or payload
            # Wrap in double quotes for FTS5 exact phrase match
            req = urllib.request.Request(
                f"{BROKER_BASE}/search",
                data=json.dumps({"query": f'"{proof_id}"', "limit": 1}).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode())
                if result.get('count', 0) > 0:
                    print(f"  ✓ Proof of handoff confirmed on bus.")
                    return True, None
                else:
                    return False, f"Spoof Warning: No legitimate event found on bus for proof_id '{proof_id}'."
        except HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"  ❌ Proof validation failed: {e} - Body: {error_body}")
            return False, f"Proof validation failed: {e} - {error_body}"
        except Exception as e:
            return False, f"Proof validation failed: {e}"

    def validate_policy(self, artifact_text, policies):
        """
        Performs static analysis on artifact text against system policies.
        policies: dict of policy_name -> {pattern: 'regex', message: 'error if found'}
        """
        print(f"[Validator v{self.version}] Enforcing Architectural Policies...")
        findings = []
        for name, rule in policies.items():
            if re.search(rule['pattern'], artifact_text, re.MULTILINE):
                findings.append(f"POLICY VIOLATION: {name} - {rule['message']}")
        
        if findings:
            return False, "\n".join(findings)
        
        print(f"  ✓ All {len(policies)} policies enforced.")
        return True, None

    def validate_evidence_artifact(self, artifact_path):
        """
        Validates the soundness and technical depth of a validation evidence artifact.
        Ensures it is not empty, well-formed, and contains substantive error details.
        """
        print(f"[Validator v{self.version}] Validating Evidence Soundness...")
        path = Path(artifact_path)
        if not path.exists():
            return False, f"Artifact not found: {artifact_path}"
        
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            
            # 1. Structural Check
            required = ["evidence_id", "timestamp", "task", "error"]
            for req in required:
                if req not in data:
                    return False, f"Evidence Malformed: Missing required field '{req}'"
            
            # 2. Depth Check
            err = str(data["error"])
            if len(err) < 20:
                return False, f"Evidence Too Shallow: Error details are only {len(err)} chars. Expected substantive trace."
            
            # 3. Technical Token Check
            technical_tokens = ["error", "exception", "failed", "failure", "traceback", "mismatch", "missing", "invalid", "null", "none"]
            if not any(t in err.lower() for t in technical_tokens):
                 return False, "Evidence Unclear: Error details lack technical markers (error, exception, etc)."

            print(f"  ✓ Evidence artifact '{path.name}' is sound and substantive.")
            return True, None
        except Exception as e:
            return False, f"Failed to validate evidence: {e}"

    def validate_environment(self):
        """
        Audits the runtime environment for stability.
        Checks: Disk space, service reachability.
        """
        print(f"[Validator v{self.version}] Auditing Runtime Environment...")
        findings = []
        
        # 1. Disk Space Check (Minimum 100MB free)
        import shutil
        usage = shutil.disk_usage(self.palette_root)
        free_mb = usage.free / (1024 * 1024)
        if free_mb < 100:
            findings.append(f"CRITICAL: Low disk space on {self.palette_root.name} ({free_mb:.2f}MB free).")

        # 2. Service Reachability
        services = {
            "Peers Broker": BROKER_BASE + "/health",
        }
        for name, url in services.items():
            try:
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=2) as response:
                    if response.status != 200:
                         findings.append(f"DOWN: Service '{name}' returned status {response.status}")
            except Exception as e:
                findings.append(f"UNREACHABLE: Service '{name}' failed with error: {e}")

        if findings:
            return False, "\n".join(findings)

        print(f"  ✓ Environment is stable ({free_mb:.2f}MB free, all core services up).")
        return True, None

    def auto_remediate(self, task_name, error_details, target_agent="debugger.engine", input_payload=None, risk_level="medium"):
        """
        The Auto-Remediation Loop.
        Uses the Palette Peers Bus to send an execution_request to the appropriate agent.
        Trips a circuit breaker (RIU-031) after 3 attempts for the same task.
        High/Critical risk forces human gating (one_way_door).
        """
        self._add_to_regression_set(task_name, input_payload)
        
        count = self.remediation_counts.get(task_name, 0) + 1
        self.remediation_counts[task_name] = count
        
        # Determine msg_type and target based on risk and circuit breaker
        is_hitl = risk_level in ["high", "critical"]
        
        if count > 3:
            print(f"\n[Validator v{self.version}] 🛑 CIRCUIT BREAKER TRIPPED for '{task_name}' ({count} attempts).")
            print("  Escalating to human.operator for manual intervention.")
            target_agent = "human.operator"
            intent = f"CRITICAL: Remediation Loop Detected - {task_name}"
            actual_risk = "critical"
            msg_type = "one_way_door"
        elif is_hitl:
            print(f"\n[Validator v{self.version}] ⚠️  HIGH RISK FAILURE detected for '{task_name}'.")
            print(f"  Routing one_way_door to {target_agent} (Awaiting Human Approval).")
            intent = f"High-Risk Remediation: {task_name}"
            actual_risk = risk_level
            msg_type = "one_way_door"
        else:
            print(f"\n[Validator v{self.version}] 🚨 Validation Failed (Attempt {count}/3). Initiating Auto-Remediation Loop...")
            print(f"  Routing failure to: {target_agent}")
            intent = f"Auto-Remediation Request: {task_name}"
            actual_risk = risk_level
            msg_type = "execution_request"
        
        self._register_with_bus()
        
        evidence_path = self._create_evidence_packet(task_name, error_details, input_payload)
        if evidence_path:
            print(f"  ✓ Evidence packet created: {Path(evidence_path).name}")

        msg_id = str(uuid.uuid4())
        
        # Build the HandoffPacket payload
        payload = {
            "handoff_packet": {
                "id": f"auto-remediation-{msg_id[:8]}",
                "from": IDENTITY,
                "to": target_agent,
                "task": f"Fix validation failure in {task_name}"
            },
            "attempt_number": count,
            "error_details": error_details,
            "evidence_file": evidence_path,
            "instructions": "Validator identified a critical failure. Assessment only: fix the issue and reply when complete."
        }
        
        if msg_type == "one_way_door":
            payload["state"] = "waiting_human" # Required for one_way_door
            if count > 3:
                payload["instructions"] = f"Automated remediation failed 3 times. Manual intervention required. See evidence: {evidence_path}"
            else:
                payload["instructions"] = f"HIGH RISK: This remediation requires human review before {target_agent} proceeds. See evidence: {evidence_path}"

        envelope = {
            "protocol_version": "1.0.0",
            "message_id": msg_id,
            "thread_id": None,
            "in_reply_to": None,
            "from_agent": IDENTITY,
            "to_agent": target_agent,
            "message_type": msg_type,
            "intent": intent,
            "risk_level": actual_risk,
            "requires_ack": True,
            "payload": payload,
            "created_at": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
            "ttl_seconds": 3600,
        }
        
        try:
            req = urllib.request.Request(
                f"{BROKER_BASE}/send",
                data=json.dumps(envelope).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                result = json.loads(response.read().decode())
                print(f"  ✓ Remediation request sent to bus. Message ID: {msg_id}")
                self._log_execution(task_name, False, f"Remediation routed to {target_agent}")
                return msg_id
        except HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"  ❌ Failed to send remediation request: {e} - Body: {error_body}")
            self._buffer_remediation(envelope)
            self._log_execution(task_name, False, f"Remediation buffered (HTTP Error)")
            return None
        except Exception as e:
            print(f"  ❌ Failed to send remediation request: {e}")
            self._buffer_remediation(envelope)
            self._log_execution(task_name, False, f"Remediation buffered (Exception)")
            return None

    def wait_for_remediation(self, message_id, timeout_sec=10):
        """
        Polls the bus for a response (ack or reply) to a specific message_id.
        Returns the response payload if found, or None if timed out.
        """
        print(f"[Validator v{self.version}] Waiting for remediation feedback (ID: {message_id[:8]}...)...")
        start_time = datetime.now().timestamp()
        
        while (datetime.now().timestamp() - start_time) < timeout_sec:
            try:
                req = urllib.request.Request(
                    f"{BROKER_BASE}/peek",
                    data=json.dumps({"identity": IDENTITY}).encode('utf-8'),
                    headers={'Content-Type': 'application/json'}
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    result = json.loads(response.read().decode())
                    messages = result.get('messages', [])
                    for msg in messages:
                        if msg.get('in_reply_to') == message_id:
                            print(f"  ✓ Feedback received from {msg['from_agent']}.")
                            return msg['payload']
            except Exception as e:
                print(f"  ⚠️  Bus peek failed: {e}")
            
            sys.stdout.write(".")
            sys.stdout.flush()
            time.sleep(1)
        
        print("\n  ❌ Timed out waiting for remediation feedback.")
        return None

    def verify_fix(self, task_name, test_func, test_args):
        """
        Closes the loop: Reruns the failing test to verify the fix.
        If passed, clears the remediation count for that task.
        """
        print(f"[Validator v{self.version}] Verifying Fix for '{task_name}'...")
        try:
            if isinstance(test_args, dict):
                test_func(**test_args)
            else:
                test_func(*test_args)
            
            print(f"  ✅ FIX VERIFIED for '{task_name}'. Resetting circuit breaker.")
            if task_name in self.remediation_counts:
                del self.remediation_counts[task_name]
            self._log_execution(task_name, True, "Fix verified successfully.")
            return True
        except Exception as e:
            print(f"  ❌ Fix verification FAILED: {e}")
            return False

    def _log_execution(self, task_name, success, notes=""):
        """Log execution to decisions.md"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"""
---
### Agent Execution: Validator v2.0 (Automated)

**Timestamp**: {timestamp}
**Agent**: {IDENTITY}
**Task**: {task_name}
**Outcome**: {'SUCCESS' if success else 'FAILURE (Remediation Triggered)'}
**Notes**: {notes}
"""
        try:
            with open(self.ledger_path, 'a') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"[Validator v{self.version}] Could not log to decisions.md: {e}")

if __name__ == "__main__":
    print("This module is the Validator Engine. Import it to use or run tests via test_validator_v2.py")
