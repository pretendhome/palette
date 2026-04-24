#!/usr/bin/env python3
"""
Builder Agent v2.0 - The Automated Remediation Closer
Status: WORKING (Tier 2)

This engine applies surgical fixes proposed by Debugger v2.1. It validates
against disk reality (drift detection) and ensures syntax integrity.
"""

import json
import sys
import uuid
import ast
import urllib.request
import traceback
import shutil
from datetime import datetime, timezone
from pathlib import Path

# Bus Configuration
BROKER_BASE = "http://127.0.0.1:7899"
IDENTITY = "builder.engine"

class BuilderEngine:
    def __init__(self):
        self.version = "2.1"
        self.agent_type = "Builder"
        self.agent_dir = Path(__file__).parent
        self.palette_root = self.agent_dir.parent.parent
        self.buffer_path = self.agent_dir / "builder_buffer.json"
        self.ledger_path = self.palette_root / "decisions.md"
        self.patch_dir = self.palette_root / "artifacts" / "patches"
        self.patch_dir.mkdir(parents=True, exist_ok=True)
        self.fix_counts = {} # RIU-031
        self.processed_ids = set() # (Imp #14) Message deduplication
        self._is_registered = False

    def _register(self):
        if self._is_registered: return True
        payload = {
            "identity": IDENTITY, "agent_name": "builder", "runtime": "python-script",
            "capabilities": ["implementation", "code_patching", "test_generation"],
            "palette_role": "builder", "trust_tier": "WORKING", "version": self.version,
            "cwd": str(self.palette_root)
        }
        try:
            req = urllib.request.Request(f"{BROKER_BASE}/register",
                data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=5): self._is_registered = True
            return True
        except Exception: return False

    def verify_proof_of_origin(self, msg):
        """(Imp #10) Confirms request originates from authorized peer."""
        from_agent = str(msg.get('from_agent', '')).lower()
        return any(x in from_agent for x in ["debugger", "orchestrator", "human", "architect"])

    def validate_spec(self, fix_proposal):
        """Ensures the proposal is complete and valid (RIU-540)."""
        mode = fix_proposal.get('mode', 'replace_line')
        required = ["file"]
        if mode in ['replace_line', 'insert_after']:
            required += ["line", "fixed"]
        elif mode == 'replace_block':
            required += ["start_line", "end_line", "fixed"]
            # Imp #3 requires current_block for drift detection
            if 'current_block' not in fix_proposal:
                return False, "Incomplete spec: missing 'current_block' for replace_block"
        elif mode == 'delete_line':
            required += ["line", "current"]
        elif mode == 'create_file':
            required += ["fixed"] # content
            
        for r in required:
            if r not in fix_proposal or fix_proposal[r] is None:
                return False, f"Incomplete spec: missing '{r}'"
        return True, None

    def apply_patch(self, fix_proposal):
        """Surgically applies the fix to the filesystem (RIU-028)."""
        file_path = Path(fix_proposal['file'])
        if not file_path.is_absolute():
            file_path = self.palette_root / file_path

        # (Imp #4) Path Traversal Prevention
        try:
            file_path.resolve().relative_to(self.palette_root.resolve())
        except ValueError:
            return False, f"Security Violation: Path {file_path} escapes palette_root"

        mode = fix_proposal.get('mode', 'replace_line')
        dry_run = fix_proposal.get('dry_run', False)

        if mode == 'create_file':
            if file_path.exists():
                return False, f"File already exists: {file_path}"
            if not dry_run:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                content = fix_proposal['fixed']
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            return True, None

        if not file_path.exists():
            return False, f"File not found: {file_path}"

        # (Imp #5) Automatic Backups
        backup_path = file_path.with_suffix(file_path.suffix + '.bak')
        if not dry_run:
            shutil.copy2(file_path, backup_path)

        print(f"[Builder v{self.version}] Reading {file_path.name}...")
        # (Imp #6) UTF-8 Enforcement
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if mode == 'replace_line':
            line_idx = int(fix_proposal['line']) - 1
            if line_idx >= len(lines):
                return False, f"Line {line_idx+1} out of bounds"
            
            actual_current = lines[line_idx].strip()
            expected_current = str(fix_proposal['current']).strip()
            if actual_current != expected_current:
                return False, f"Drift Detected! Expected '{expected_current}', found '{actual_current}'"

            print(f"  ✓ Applying line replacement at line {line_idx+1}...")
            original_line = lines[line_idx]
            indent = original_line[:len(original_line) - len(original_line.lstrip())]
            lines[line_idx] = indent + fix_proposal['fixed'].strip() + "\n"

        elif mode == 'replace_block':
            start_idx = int(fix_proposal['start_line']) - 1
            end_idx = int(fix_proposal['end_line'])
            
            # (Imp #3) Block Drift Detection
            actual_block = "".join(lines[start_idx:end_idx]).strip()
            expected_block = str(fix_proposal['current_block']).strip()
            # Loose comparison for block drift
            if expected_block not in actual_block and actual_block not in expected_block:
                return False, f"Block Drift Detected!"
                
            print(f"  ✓ Applying block replacement (lines {start_idx+1}-{end_idx})...")
            # (Imp #8) Block Indentation Preservation
            first_line = lines[start_idx]
            indent = first_line[:len(first_line) - len(first_line.lstrip())]
            new_content = [indent + line + "\n" for line in fix_proposal['fixed'].strip().splitlines()]
            lines[start_idx:end_idx] = new_content

        elif mode == 'insert_after':
            line_idx = int(fix_proposal['line'])
            print(f"  ✓ Inserting after line {line_idx}...")
            # (Imp #7) Insert Indentation Preservation
            indent = ""
            if line_idx > 0 and line_idx <= len(lines):
                prev_line = lines[line_idx-1]
                indent = prev_line[:len(prev_line) - len(prev_line.lstrip())]
            lines.insert(line_idx, indent + fix_proposal['fixed'].strip() + "\n")
            
        elif mode == 'delete_line':
            line_idx = int(fix_proposal['line']) - 1
            if line_idx >= len(lines):
                return False, f"Line {line_idx+1} out of bounds"
            actual_current = lines[line_idx].rstrip()
            expected_current = str(fix_proposal['current']).rstrip()
            if actual_current != expected_current:
                return False, f"Drift Detected!"
            print(f"  ✓ Deleting line {line_idx+1}...")
            del lines[line_idx]

        # (Imp #16) Prepend mode
        elif mode == 'prepend_to_file':
            print(f"  ✓ Prepending to file...")
            lines.insert(0, fix_proposal['fixed'].strip() + "\n")

        # (Imp #17) Append mode
        elif mode == 'append_to_file':
            print(f"  ✓ Appending to file...")
            if lines and not lines[-1].endswith("\n"): lines[-1] += "\n"
            lines.append(fix_proposal['fixed'].strip() + "\n")

        content = "".join(lines)
        if file_path.suffix == ".py":
            try:
                # (Imp #18) Advanced Syntax Check: Compile to byte code
                compile(content, str(file_path), 'exec')
            except SyntaxError as e:
                # Restore backup on failure
                if not dry_run: shutil.copy2(backup_path, file_path)
                return False, f"Patch rejected: Syntax Error would be introduced: {e}"

        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # (Imp #13) Generate Patch Artifact
            patch_file = self.patch_dir / f"patch_{uuid.uuid4().hex[:8]}.txt"
            with open(patch_file, 'w', encoding='utf-8') as f:
                f.write(f"Applied mode {mode} to {file_path.name}\n")
        
        return True, None

    def generate_verification_test(self, fix_proposal):
        """(Imp #13) Creates a REAL test to verify the fix actually applied."""
        test_dir = self.palette_root / "artifacts" / "verification_tests"
        test_dir.mkdir(parents=True, exist_ok=True)
        test_id = str(uuid.uuid4())[:8]
        test_file = test_dir / f"test_fix_{test_id}.py"
        
        file_path = str(fix_proposal['file'])
        expected_code = str(fix_proposal['fixed']).replace("'", "\\'")
        
        # Real verification logic: Read file and check for fixed content
        content = f"""
import sys
from pathlib import Path

def verify():
    path = Path('{file_path}')
    if not path.is_absolute():
        # Resolve against project root
        path = Path(__file__).parent.parent.parent / path
    
    if not path.exists():
        print("FAIL: File not found")
        return False
        
    with open(path, 'r') as f:
        content = f.read()
        if '{expected_code}' in content:
            print("PASS: Fixed code found in file.")
            return True
        else:
            print("FAIL: Fixed code NOT found in file.")
            return False

if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
"""
        with open(test_file, 'w') as f: f.write(content)
        return str(test_file)

    def detect_bus_deadlock(self):
        """(Imp #11) Flags if broker is up but unresponsive."""
        try:
            req = urllib.request.Request(f"{BROKER_BASE}/health")
            with urllib.request.urlopen(req, timeout=1) as resp:
                 if resp.status == 200: return False
        except Exception: return True
        return True

    def handle_fix_request(self, fix_proposal, thread_id=None, in_reply_to=None, sender_msg=None):
        try:
            print(f"\n[Builder v{self.version}] Processing Fix Proposal...")

            # (Imp #10) Origin Verification
            if sender_msg and not self.verify_proof_of_origin(sender_msg):
                print(f"  🛑 SECURITY ALERT: Unauthorized source: {sender_msg.get('from_agent')}")
                return False

            if self.detect_bus_deadlock():
                 print(f"  ⚠️  BUS DEADLOCK WARNING: Broker unresponsive.")

            # 1. Validate
            valid, err = self.validate_spec(fix_proposal)
            if not valid: return self._fail("validation", err, thread_id, in_reply_to)

            # 2. Architecture Boundary Check
            if str(fix_proposal.get('blast_radius')).lower() == "high":
                return self._fail("architecture_boundary", "High blast radius requires Architect review", thread_id, in_reply_to, target="architect")

            # 3. Circuit Breaker (RIU-031)
            task_id = fix_proposal.get('file', 'unknown') + str(fix_proposal.get('line', 0))
            count = self.fix_counts.get(task_id, 0) + 1
            self.fix_counts[task_id] = count

            # (Imp #12) Maturity Gate
            limit = 3
            if sender_msg and "unvalidated" in str(sender_msg.get('trust_tier', '')).lower():
                 limit = 2
            
            if count > limit: return self._fail("circuit_breaker", "Max attempts reached", thread_id, in_reply_to)

            # 4. Apply
            success, err = self.apply_patch(fix_proposal)
            if not success: return self._fail("apply", err, thread_id, in_reply_to)

            # (Imp #14) Dry Run mode
            if fix_proposal.get('dry_run'):
                 print("  ✓ Dry-run completed successfully.")
                 return True

            # 5. Test
            test_path = self.generate_verification_test(fix_proposal)
            print(f"  ✓ Verification test generated: {Path(test_path).name}")

            # 6. Route back to Validator (RIU-121)
            self._send_to_bus({
                "to_agent": "validator.engine", "message_type": "execution_request",
                "intent": f"Verify Fix: {fix_proposal['file']}", "risk_level": "low",
                "payload": {
                    "handoff_packet": {
                        "id": f"verify-{uuid.uuid4().hex[:8]}", "from": IDENTITY,
                        "to": "validator.engine", "task": "Verify applied patch"
                    },
                    "test_file": test_path, "fix_proposal": fix_proposal
                },
                "thread_id": thread_id, "in_reply_to": in_reply_to
            })
            self._log(fix_proposal, True)
            return True
        except Exception as e:
             # (Imp #9) Self-Debug Harness
             trace = traceback.format_exc()
             print(f"  💥 SELF-DEBUG ALERT: Builder Engine encountered internal error:\n{trace}")
             return False

    def listen_for_work(self, interval_sec=5):
        """Active loop that polls the bus for work (uses /fetch for delivery)."""
        print(f"[Builder v{self.version}] Active Agent Loop Started.")
        self._register()
        import time
        while True:
            try:
                # 1. Fetch new messages (marks as delivered at broker)
                req = urllib.request.Request(f"{BROKER_BASE}/fetch",
                    data=json.dumps({"identity": IDENTITY}).encode(), headers={'Content-Type': 'application/json'})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    messages = json.loads(resp.read().decode()).get('messages', [])
                    for msg in messages:
                        m_id = msg['message_id']
                        if m_id in self.processed_ids: continue
                        
                        if msg['message_type'] in ['proposal', 'execution_request']:
                            payload = msg.get('payload', {})
                            if 'handoff_result' in payload:
                                self.handle_fix_request(
                                    payload['handoff_result']['output'].get('fix_proposal', {}),
                                    thread_id=msg.get('thread_id'),
                                    in_reply_to=m_id
                                )
                                self.processed_ids.add(m_id)
            except Exception as e: print(f"  ⚠️  Bus fetch failed: {e}")
            time.sleep(interval_sec)

    def _fail(self, phase, reason, tid, reply_to, target="debugger.engine"):
        print(f"  ❌ Build Failure ({phase}): {reason}")
        # Build failure evidence -> Debugger/Architect
        ev_id = str(uuid.uuid4())
        ev_path = self.palette_root / "artifacts" / "validation" / f"BUILD-EVIDENCE-{ev_id[:8]}.json"
        with open(ev_path, 'w') as f:
            json.dump({"task": "build_fix", "error": f"{phase} failed: {reason}", 
                       "timestamp": datetime.now(timezone.utc).isoformat()}, f)
        
        self._send_to_bus({
            "to_agent": target, "message_type": "execution_request",
            "intent": f"Remediate Build Failure: {phase}", "risk_level": "medium",
            "payload": {"evidence_file": str(ev_path)}, "thread_id": tid, "in_reply_to": reply_to
        })
        self._log({"phase": phase, "reason": reason}, False)
        return False

    def _send_to_bus(self, envelope_partial):
        self._register()
        envelope = {
            "protocol_version": "1.0.0", "message_id": str(uuid.uuid4()),
            "from_agent": IDENTITY, "created_at": datetime.now(timezone.utc).isoformat() + "Z",
            "requires_ack": True, "ttl_seconds": 3600, **envelope_partial
        }
        try:
            req = urllib.request.Request(f"{BROKER_BASE}/send",
                data=json.dumps(envelope).encode(), headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=5): return True
        except Exception: return False

    def _log(self, spec, success):
        entry = f"\n---\n### Agent Execution: Builder v2.0\n**Time**: {datetime.now()}\n" \
                f"**File**: {spec.get('file')}\n**Outcome**: {'PASS' if success else 'FAIL'}\n"
        try:
            with open(self.ledger_path, 'a') as f: f.write(entry)
        except Exception: pass

if __name__ == "__main__":
    print("Builder Engine v2.0. Use test_builder_v2.py to run.")
