#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════════╗
# ║  PALETTE OS — Governance Mirror                             ║
# ║  Shows real-time routing decisions as user interacts with   ║
# ║  https://missioncanvas.ai                                   ║
# ╚══════════════════════════════════════════════════════════════╝

BOLD='\033[1m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
DIM='\033[2m'
NC='\033[0m'

clear
echo -e "${BOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BOLD}║  ${GREEN}PALETTE OS${NC}${BOLD} — Governance Mirror                             ║${NC}"
echo -e "${BOLD}║  ${DIM}Watching: https://missioncanvas.ai${NC}${BOLD}                        ║${NC}"
echo -e "${BOLD}║  ${DIM}Every query → classify → route → respond${NC}${BOLD}                  ║${NC}"
echo -e "${BOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${DIM}  Waiting for queries...${NC}"
echo ""

ssh root@srv1390882.hstgr.cloud "tail -f /tmp/hub.log" 2>/dev/null | while IFS= read -r line; do
  if [[ "$line" == *"━━━ INTENT:"* ]]; then
    echo ""
    echo -e "${BOLD}${CYAN}$line${NC}"
  elif [[ "$line" == *"CLASSIFY:"* ]]; then
    echo -e "  ${GREEN}$line${NC}"
  elif [[ "$line" == *"ROUTE: LOCAL"* ]]; then
    echo -e "  ${YELLOW}$line${NC}"
  elif [[ "$line" == *"ROUTE: EXTERNAL"* ]]; then
    echo -e "  ${MAGENTA}$line${NC}"
  elif [[ "$line" == *"QUERY:"* ]]; then
    echo -e "  ${DIM}$line${NC}"
  elif [[ "$line" == *"resolver"* || "$line" == *"researcher"* ]]; then
    echo -e "  ${DIM}$line${NC}"
  fi
done
