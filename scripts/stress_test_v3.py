import os
import subprocess
import yaml
import json
import time
from pathlib import Path

PALETTE_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PALETTE_ROOT / "scripts"
PROPOSED_DIR = PALETTE_ROOT / "wiki" / "proposed"
KL_PATH = PALETTE_ROOT / "knowledge-library" / "v1.4" / "palette_knowledge_library_v1.4.yaml"

def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return result

def test_phase_1_filing(count=100):
    print(f"--- Phase 1: Filing {count} Proposals ---")
    start_time = time.time()
    props = []
    # Using a slightly longer answer to pass the >100 char limit
    answer = "This is a comprehensive stress test answer that is guaranteed to be over one hundred characters long. We need to ensure that the governance pipeline can handle a high volume of concurrent requests without breaking the internal state machines or the rendered wiki pages."
    
    for i in range(count):
        prop = {
            "proposed_by": "gemini.specialist",
            "tier": 2,
            "type": "new",
            "content": {
                "question": f"Stress test question {i}?",
                "answer": answer + f" Index: {i}",
                "sources": [{"title": "Test Source", "url": "https://example.com"}],
                "related_rius": ["RIU-001"],
                "evidence_tier": 3,
                "evidence_tier_justification": "Automated stress test justification"
            },
            "rationale": f"Stress testing the pipeline at index {i}",
            "source_of_insight": "Automated stress test v3",
            "contradiction_check": {"checked_against": [], "conflicts_found": "none"}
        }
        path = f"/tmp/stress_prop_{i}.yaml"
        with open(path, "w") as f:
            yaml.dump(prop, f)
        
        res = run_cmd(f"python3 {SCRIPTS_DIR}/file_proposal.py {path}")
        if res.returncode == 0:
            try:
                prop_id = res.stdout.split("FILED: ")[1].split("\n")[0].strip()
                props.append(prop_id)
            except IndexError:
                print(f"FAILED to parse prop_id for {i}: {res.stdout}")
        else:
            print(f"FAILED to file prop {i}: {res.stdout} {res.stderr}")
    
    elapsed = time.time() - start_time
    print(f"Filed {len(props)} proposals in {elapsed:.2f}s")
    return props

def test_phase_2_voting(props):
    print(f"--- Phase 2: Voting on {len(props)} Proposals ---")
    agents = ["kiro.design", "claude.analysis", "codex.implementation"]
    start_time = time.time()
    for prop_id in props:
        for agent in agents:
            # We need reasoning for non-approve votes, but record_vote says 'object' votes require reasoning. 
            # I'll provide it for all.
            res = run_cmd(f"python3 {SCRIPTS_DIR}/record_vote.py {prop_id} approve {agent} 'Stress test approval'")
            if res.returncode != 0:
                print(f"FAILED to vote on {prop_id} by {agent}: {res.stderr}")
    
    elapsed = time.time() - start_time
    print(f"Recorded {len(props) * len(agents)} votes in {elapsed:.2f}s")

def test_phase_3_promotion(props):
    print(f"--- Phase 3: Promoting {len(props)} Proposals ---")
    start_time = time.time()
    success_count = 0
    for prop_id in props:
        res = run_cmd(f"python3 {SCRIPTS_DIR}/promote_proposal.py {prop_id}")
        if res.returncode == 0:
            success_count += 1
        else:
            print(f"FAILED to promote {prop_id}: {res.stderr}")
    
    elapsed = time.time() - start_time
    print(f"Promoted {success_count} proposals in {elapsed:.2f}s")

def main():
    # Setup: Backup KL
    print("Backing up environment...")
    run_cmd(f"cp {KL_PATH} {KL_PATH}.bak")
    
    try:
        props = test_phase_1_filing(100)
        test_phase_2_voting(props)
        test_phase_3_promotion(props)
        
        print("\n--- Final Integrity Check ---")
        res = run_cmd(f"cd {PALETTE_ROOT} && export PYTHONPATH=$PYTHONPATH:. && python3 -m scripts.palette_intelligence_system.integrity --checks-only")
        print(res.stdout)
        
    finally:
        # Cleanup
        print("Restoring environment...")
        run_cmd(f"mv {KL_PATH}.bak {KL_PATH}")
        # Manual cleanup of tmp files
        for i in range(100):
            try: os.remove(f"/tmp/stress_prop_{i}.yaml")
            except: pass

if __name__ == "__main__":
    main()
