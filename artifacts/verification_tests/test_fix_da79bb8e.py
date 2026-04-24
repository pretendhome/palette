
import sys
from pathlib import Path

def verify():
    path = Path('BUILDER_TEST_FILE.py')
    if not path.is_absolute():
        # Resolve against project root
        path = Path(__file__).parent.parent.parent / path
    
    if not path.exists():
        print("FAIL: File not found")
        return False
        
    with open(path, 'r') as f:
        content = f.read()
        if 'print(\'Verified\')' in content:
            print("PASS: Fixed code found in file.")
            return True
        else:
            print("FAIL: Fixed code NOT found in file.")
            return False

if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
