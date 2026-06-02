#!/usr/bin/env bash
# Kiro Failsafe Check — run at session start to see if VPS reported errors
# Usage: bash scripts/kiro_failsafe_check.sh

BOLD='\033[1m'
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${BOLD}[kiro-failsafe] Checking VPS for error reports...${NC}"

MSGS=$(ssh root@srv1390882.hstgr.cloud 'curl -s -X POST http://127.0.0.1:7899/fetch -H "Content-Type: application/json" -d "{\"identity\":\"kiro.design\"}" 2>/dev/null')

COUNT=$(echo "$MSGS" | python3 -c "import json,sys;d=json.load(sys.stdin);print(len(d.get('messages',[])))" 2>/dev/null)

if [ "$COUNT" = "0" ] || [ -z "$COUNT" ]; then
  echo -e "  ${GREEN}✓${NC} No pending errors. System healthy."
else
  echo -e "  ${RED}⚠ $COUNT error(s) need attention:${NC}"
  echo "$MSGS" | python3 -c "
import json,sys
d=json.load(sys.stdin)
for m in d.get('messages',[]):
    print(f'  → {m[\"intent\"]}')
    print(f'    {m[\"created_at\"]}')
    content = m.get('payload',{}).get('content','')
    # Show first 3 lines of content
    for line in content.split('\n')[:3]:
        if line.strip(): print(f'    {line.strip()}')
    print()
"
fi
