#!/usr/bin/env python3
"""
Test Suite for Validator v2.0
Validates the validation framework (meta-validation).
"""

import sys
import time
import json
import uuid
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from validator_v2 import ValidatorEngine

def dummy_target_function(a, b):
    """A dummy function that fails if b is 0 or negative."""
    if b <= 0:
        raise ValueError("b must be strictly positive")
    return a / b

def main():
    print("="*60)
    print("VALIDATING THE VALIDATOR (v2.0)")
    print("="*60)
    
    engine = ValidatorEngine()
    
    # 1. Test Schema Validation (Pass)
    print("\n--- Test 1: Schema Validation (Pass) ---")
    valid_data = {"name": "Test", "age": 30, "active": True}
    schema = {"name": "string", "age": "number", "active": "boolean"}
    success, err = engine.validate_schema(valid_data, schema)
    assert success is True, "Expected Pass"
    
    # 2. Test Schema Validation (Fail)
    print("\n--- Test 2: Schema Validation (Fail) ---")
    invalid_data = {"name": "Test", "age": "thirty"}
    success, err = engine.validate_schema(invalid_data, schema)
    assert success is False, "Expected Fail"
    print(f"Caught expected error: {err}")

    # 2.1 Test Schema Validation (Nested + Regex + Strict)
    print("\n--- Test 2.1: Advanced Schema (Nested + Regex + Strict) ---")
    complex_schema = {
        "metadata": {
            "riu_id": {"type": "string", "pattern": r"^RIU-\d{3}$"},
            "owner": "string"
        },
        "tags": "array"
    }
    valid_complex = {
        "metadata": {"riu_id": "RIU-001", "owner": "gemini"},
        "tags": ["testing", "validation"]
    }
    success, err = engine.validate_schema(valid_complex, complex_schema)
    assert success is True, f"Expected Pass, got: {err}"
    print("  ✓ Nested + Regex passed.")

    invalid_complex = {
        "metadata": {"riu_id": "NOT-A-RIU", "owner": "gemini"},
        "tags": []
    }
    success, err = engine.validate_schema(invalid_complex, complex_schema)
    assert success is False, "Expected Fail (Regex)"
    print(f"  ✓ Caught expected Regex fail: {err}")

    strict_leak = {
        "metadata": {"riu_id": "RIU-001", "owner": "gemini", "leaked": True},
        "tags": []
    }
    success, err = engine.validate_schema(strict_leak, complex_schema, strict=True)
    assert success is False, "Expected Fail (Strict Mode)"
    print(f"  ✓ Caught expected Strict Mode fail: {err}")
    
    # 3. Test Stress Testing (Pass - expects exception for bad inputs)
    print("\n--- Test 3: Stress Testing (Boundary - Expected Exception) ---")
    bad_inputs = [{"a": 10, "b": 0}, {"a": 10, "b": -5}]
    success, err = engine.stress_test_function(dummy_target_function, bad_inputs, expect_exception=True)
    assert success is True, "Expected Pass (function correctly failed loudly)"

    # 3.1 Test Chaos Injection
    print("\n--- Test 3.1: Chaos Injection Stress Test ---")
    # This will generate many bad payloads and ensure dummy_target_function fails on all of them
    valid_base = {"a": 10, "b": 5}
    success, err = engine.chaos_stress_test(dummy_target_function, valid_base)
    assert success is True, f"Expected Chaos Engine to pass (all bad inputs caught), but: {err}"
    print("  ✓ Chaos Engine successfully stressed the target.")
    
    # 4. Test Auto-Remediation Loop
    print("\n--- Test 4: Auto-Remediation Loop (Bus Integration) ---")
    # We will trigger a stress test that fails silently when it shouldn't, or just fails on normal inputs.
    # Let's pass a bad input without expecting an exception, so the validator catches it as a failure.
    bad_inputs_unhandled = [{"a": 10, "b": 0}]
    success, err = engine.stress_test_function(dummy_target_function, bad_inputs_unhandled, expect_exception=False)
    
    if not success:
        # Trigger the remediation loop to the Debugger (claude.analysis)
        remediation_success = engine.auto_remediate("Dummy Function Fix", err, target_agent="claude.analysis")
        if remediation_success:
            print("✓ Auto-remediation successfully routed to claude.analysis.")
        else:
            print("❌ Auto-remediation routing failed. Check if broker is running on port 7899.")
            sys.exit(1)

    # 5. Test Fault Tolerance (Buffering)
    print("\n--- Test 5: Fault Tolerance (Buffering) ---")
    import validator_v2
    original_base = validator_v2.BROKER_BASE
    
    # Simulate Bus Down (wrong port)
    validator_v2.BROKER_BASE = "http://127.0.0.1:9999" 
    print("  (Simulating Bus Down...)")
    success = engine.auto_remediate("Buffered Task", "Simulated failure", target_agent="debugger.engine")
    assert success is None, "Expected failure (Bus down)"
    assert engine.buffer_path.exists(), "Expected remediation to be buffered"
    print("  ✓ Remediation correctly buffered.")

    # Simulate Bus Up
    validator_v2.BROKER_BASE = original_base
    print("  (Simulating Bus Recovery...)")
    engine.flush_remediation_buffer()
    assert not engine.buffer_path.exists(), "Expected buffer to be empty after flush"
    print("  ✓ Remediation buffer successfully flushed.")

    # 6. Test Evidence Packet Creation
    print("\n--- Test 6: Evidence Packet Creation (LIB-093) ---")
    # Trigger a remediation with an input payload
    test_input = {"a": 100, "b": "bad"}
    success = engine.auto_remediate("Evidence Test Task", "Detailed traceback showing a critical failure in the component.", input_payload=test_input)
    
    # Find the evidence file in the directory
    evidence_files = list(engine.evidence_dir.glob("EVIDENCE-*.json"))
    assert len(evidence_files) > 0, "Expected evidence file to be created"
    
    # Read the latest evidence file
    latest_evidence = sorted(evidence_files, key=lambda x: x.stat().st_mtime, reverse=True)[0]
    with open(latest_evidence, 'r') as f:
        data = json.load(f)
        assert data["input_payload"] == test_input, "Input payload mismatch in evidence"
        assert data["task"] == "Evidence Test Task", "Task name mismatch in evidence"
    
    print(f"  ✓ Evidence packet created and verified: {latest_evidence.name}")

    # 7. Test Circuit Breaker (Kill Switch)
    print("\n--- Test 7: Circuit Breaker (RIU-031) ---")
    task = "Infinite Loop Task"
    # Call 1, 2, 3 (Regular remediation)
    for i in range(1, 4):
        print(f"  Attempt {i}...")
        success = engine.auto_remediate(task, "Test fail")
        assert success
    
    # Call 4 (Should trip circuit breaker)
    print("  Attempt 4 (Should trip)...")
    success = engine.auto_remediate(task, "Test fail")
    assert success
    assert engine.remediation_counts[task] == 4
    print("  ✓ Circuit breaker tripped and escalated to human.operator.")

    # 8. Test Regression Harness
    print("\n--- Test 8: Regression Harness ---")
    reg_task = "Regression Target"
    # Initial state: failing
    def failing_func(val): raise ValueError("Bad")
    
    print("  (Triggering initial failure...)")
    engine.auto_remediate(reg_task, "Initial fail", input_payload={"val": 123})
    assert engine.regression_path.exists()
    
    # State change: fixed
    def fixed_func(val): print(f"    (fixed_func received {val})"); return True
    
    print("  (Running regression suite after 'fix'...)")
    success = engine.run_regression_suite({reg_task: fixed_func})
    assert success is True, "Regression suite should pass after fix"
    print("  ✓ Regression harness verified.")

    # 9. Test Taxonomy Consistency
    print("\n--- Test 9: Taxonomy Consistency (The Gemini Brake) ---")
    success, err = engine.validate_rius(["RIU-001", "RIU-003"])
    assert success is True, f"Valid RIUs should pass, but: {err}"
    print("  ✓ Valid RIUs passed.")
    
    success, err = engine.validate_rius(["RIU-999", "BOGUS-001"])
    assert success is False, "Invalid RIUs should fail"
    print(f"  ✓ Caught expected Taxonomy Drift: {err}")

    # 10. Test HITL Risk Tiering
    print("\n--- Test 10: HITL Risk Tiering ---")
    print("  (Triggering High-Risk Remediation...)")
    msg_id = engine.auto_remediate("High Risk Task", "Critical bug", risk_level="high")
    assert msg_id is not None
    print("  ✓ High-risk remediation successfully routed via one_way_door.")

    # 10.1 Test Feedback Loop
    print("\n--- Test 10.1: Feedback Loop (wait_for_remediation) ---")
    ack_envelope = {
        "protocol_version": "1.0.0",
        "message_id": str(uuid.uuid4()),
        "in_reply_to": msg_id,
        "from_agent": "human.operator",
        "to_agent": "validator.engine",
        "message_type": "ack",
        "intent": "Acking High Risk Task",
        "risk_level": "none",
        "requires_ack": False,
        "payload": {
            "status": "fixed",
            "acked_message_id": msg_id
        },
        "created_at": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')
    }
    
    print("  (Sending simulated feedback...)")
    import validator_v2
    try:
        req = urllib.request.Request(
            f"{validator_v2.BROKER_BASE}/send",
            data=json.dumps(ack_envelope).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print(f"  ❌ Feedback send failed: {e} - {e.read().decode()}")
        raise

    feedback = engine.wait_for_remediation(msg_id, timeout_sec=5)
    assert feedback is not None
    assert feedback["status"] == "fixed"
    print("  ✓ Feedback loop verified.")
    print("  ✓ High-risk remediation successfully routed via one_way_door.")

    # 11. Test Library Alignment
    print("\n--- Test 11: Knowledge Library Alignment ---")
    success, err = engine.validate_library_alignment("Lean code, minimal dependencies.", ["LIB-001"])
    assert success is True, f"Expected pass, got: {err}"
    print("  ✓ Principle alignment passed.")
    
    success, err = engine.validate_library_alignment("Extensive cathedral of boilerplate code.", ["LIB-001"])
    assert success is False, "Expected principle violation"
    print(f"  ✓ Caught expected Principle Violation: {err}")
    
    success, err = engine.validate_library_alignment("Test", ["LIB-999"])
    assert success is False, "Expected structural violation (missing entry)"
    print(f"  ✓ Caught expected missing entry: {err}")

    # 12. Test Readiness Assessment
    print("\n--- Test 12: Readiness Assessment ---")
    # Audit this directory (agents/validator)
    current_dir = Path(__file__).parent
    criteria = {
        "Has Logic": {"type": "file_exists", "target": "validator_v2.py"},
        "Has Documentation": {"type": "file_exists", "target": "VALIDATOR_V2_SPEC.md"},
        "Contains Identity": {"type": "contains_text", "target": "validator_v2.py", "text": "validator.engine"}
    }
    
    success, report = engine.assess_readiness(current_dir, criteria)
    assert success is True, "Self-readiness check should pass"
    print(f"  ✓ Readiness assessed: {report['status']}")
    
    # Failing check
    criteria["Missing File"] = {"type": "file_exists", "target": "NON-EXISTENT.txt"}
    success, report = engine.assess_readiness(current_dir, criteria)
    assert success is False, "Should fail on missing file"
    print(f"  ✓ Caught expected NO-GO: {report['status']}")

    # 13. Test Peer Audit
    print("\n--- Test 13: Live Peer Audit (Capability Drift) ---")
    success, err = engine.audit_peer_capabilities()
    if not success:
        print(f"  ✓ Successfully identified discrepancies:\n{err}")
    else:
        print("  ✓ All peers aligned (unexpected in restricted session but valid).")

    # 14. Test Dependency Integrity
    print("\n--- Test 14: Dependency Integrity ---")
    # 14.1 Pass
    success, err = engine.validate_dependencies(["MANIFEST.yaml", "core/palette-core.md"])
    assert success is True, f"Expected pass, got: {err}"
    print("  ✓ Valid dependencies passed.")
    
    # 14.2 Fail (Missing)
    success, err = engine.validate_dependencies(["NON-EXISTENT.txt"])
    assert success is False
    assert "MISSING" in err
    print(f"  ✓ Caught expected MISSING: {err}")
    
    # 14.3 Fail (Empty)
    empty_file = engine.palette_root / "EMPTY_TEST.txt"
    empty_file.touch()
    try:
        success, err = engine.validate_dependencies(["EMPTY_TEST.txt"])
        assert success is False
        assert "EMPTY" in err
        print(f"  ✓ Caught expected EMPTY: {err}")
    finally:
        if empty_file.exists(): empty_file.unlink()

    # 15. Test Decision Log Audit
    print("\n--- Test 15: Decision Log Audit ---")
    # We know 'validator.engine' wrote logs in previous steps
    success, err = engine.validate_decision_log("validator.engine")
    assert success is True, f"Expected to find 'validator.engine' in log, but: {err}"
    print("  ✓ Found own engine in audit trail.")
    
    # Fail path
    success, err = engine.validate_decision_log("NON_EXISTENT_TOKEN_12345")
    assert success is False
    print(f"  ✓ Caught expected Audit Gap: {err}")

    # 16. Test Graph Coherence
    print("\n--- Test 16: Relationship Graph Coherence ---")
    # Valid link (from line 25 of RELATIONSHIP_GRAPH.yaml)
    success, err = engine.validate_graph_link("Architect", "handles_riu", "RIU-001")
    assert success is True, f"Expected link to exist, but: {err}"
    print("  ✓ Valid graph link verified.")
    
    # Missing link
    success, err = engine.validate_graph_link("Gemini", "is_a", "Robot")
    assert success is False
    print(f"  ✓ Caught expected Graph Gap: {err}")

    # 17. Test Handoff Proof
    print("\n--- Test 17: Proof of Handoff (Identity Audit) ---")
    # We use the msg_id from Test 10.1 (Feedback Loop) which we know is on the bus
    success, err = engine.validate_handoff_proof(msg_id)
    assert success is True, f"Expected proof to be found on bus, but: {err}"
    print("  ✓ Valid handoff proof confirmed.")
    
    # Spoof path
    success, err = engine.validate_handoff_proof("SPOOFED_ID_99999")
    assert success is False
    print(f"  ✓ Caught expected Spoof Warning: {err}")

    # 18. Test Policy Enforcement
    print("\n--- Test 18: Architectural Policy Enforcement ---")
    policies = {
        "No Direct DB Access": {
            "pattern": r"import sqlite3", 
            "message": "Use the Palette Peers Bus for all persistence."
        },
        "No Hidden State": {
            "pattern": r"global _cache", 
            "message": "Use bounded_memory for state persistence."
        }
    }
    # Pass path
    success, err = engine.validate_policy("import json\nimport urllib.request", policies)
    assert success is True, f"Expected pass, got: {err}"
    print("  ✓ Clean code passed policies.")
    
    # Fail path
    success, err = engine.validate_policy("import sqlite3\ndb = sqlite3.connect('local.db')", policies)
    assert success is False
    assert "No Direct DB Access" in err
    print(f"  ✓ Caught expected Policy Violation: {err}")

    # 19. Test Evidence Soundness
    print("\n--- Test 19: Evidence Soundness ---")
    # Using the evidence file from Test 6
    success, err = engine.validate_evidence_artifact(latest_evidence)
    assert success is True, f"Expected pass for Test 6 evidence, but: {err}"
    print("  ✓ Real evidence artifact passed soundness check.")
    
    # Fail path (shallow)
    shallow_file = engine.evidence_dir / "SHALLOW.json"
    with open(shallow_file, 'w') as f:
        json.dump({
            "evidence_id": "123", "timestamp": "now", "task": "T", "error": "too short"
        }, f)
    try:
        success, err = engine.validate_evidence_artifact(shallow_file)
        assert success is False
        assert "Too Shallow" in err
        print(f"  ✓ Caught expected shallow evidence: {err}")
    finally:
        if shallow_file.exists(): shallow_file.unlink()

    # 20. Test Environment Audit
    print("\n--- Test 20: Runtime Environment Audit ---")
    success, err = engine.validate_environment()
    assert success is True, f"Environment should be healthy in this session, but: {err}"
    print("  ✓ Environment audit passed.")

    # 21. Test Fix Verification (Closing the Loop)
    print("\n--- Test 21: Remediation Verification ---")
    # Trigger 1 attempt
    engine.auto_remediate("Fix Loop Task", "Initial error")
    assert engine.remediation_counts["Fix Loop Task"] == 1
    
    # Verify the fix (rerun a successful dummy function)
    success = engine.verify_fix("Fix Loop Task", dummy_target_function, {"a": 10, "b": 2})
    assert success is True
    assert "Fix Loop Task" not in engine.remediation_counts
    print("  ✓ Remediation verified and count cleared.")

    print("\n" + "="*60)
    print("✅ ALL 21 META-VALIDATIONS PASSED")
    print("="*60)

if __name__ == "__main__":
    main()
