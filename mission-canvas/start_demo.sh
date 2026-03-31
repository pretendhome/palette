#!/bin/bash
# start_demo.sh — Start all Mission Canvas services for demo
#
# Usage:
#   ./start_demo.sh                    # minimal (server + bridge)
#   ./start_demo.sh --with-monitors    # adds monitor daemon
#   ./start_demo.sh --tunnel           # also starts cloudflared tunnel
#
# Required env vars:
#   JOSEPH_BOT_TOKEN    — Telegram bot token for @joseph_palette_bot
#
# Optional env vars:
#   PERPLEXITY_API_KEY  — enables research + live monitors
#   TELEGRAM_CHAT_ID    — Joseph's chat ID (for monitor push alerts)
#   MC_WORKSPACE        — workspace ID (default: oil-investor)
#   MC_SERVER           — server URL (default: http://localhost:8787)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Mission Canvas Demo Launcher${NC}"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check required vars
if [ -z "$JOSEPH_BOT_TOKEN" ]; then
    echo -e "${RED}ERROR: JOSEPH_BOT_TOKEN not set${NC}"
    echo "  export JOSEPH_BOT_TOKEN=\"8748740444:AAE7mncPmZFZs45xxVgKAF1xMoFvDOxOBjQ\""
    exit 1
fi

MC_WORKSPACE="${MC_WORKSPACE:-oil-investor}"
MC_SERVER="${MC_SERVER:-http://localhost:8787}"

echo -e "Workspace:  ${GREEN}$MC_WORKSPACE${NC}"
echo -e "Server:     ${GREEN}$MC_SERVER${NC}"
echo -e "Perplexity: ${PERPLEXITY_API_KEY:+${GREEN}ENABLED${NC}}${PERPLEXITY_API_KEY:-${YELLOW}DISABLED${NC}}"
echo ""

# Kill any existing processes
echo "Stopping any existing processes..."
pkill -f "node server.mjs" 2>/dev/null || true
pkill -f "python3 joseph_bridge.py" 2>/dev/null || true
pkill -f "python3 monitor_daemon.py" 2>/dev/null || true
sleep 1

# Start server
echo -e "Starting server.mjs..."
node server.mjs > /tmp/mc-server.log 2>&1 &
SERVER_PID=$!
sleep 2

# Check server started
if ! curl -s http://localhost:8787/v1/missioncanvas/health > /dev/null 2>&1; then
    echo -e "${RED}Server failed to start. Check /tmp/mc-server.log${NC}"
    exit 1
fi
echo -e "  ${GREEN}✓ Server running${NC} (PID $SERVER_PID)"

# Start Telegram bridge
echo -e "Starting joseph_bridge.py..."
MC_SERVER="$MC_SERVER" MC_WORKSPACE="$MC_WORKSPACE" \
  JOSEPH_BOT_TOKEN="$JOSEPH_BOT_TOKEN" \
  PERPLEXITY_API_KEY="${PERPLEXITY_API_KEY:-}" \
  python3 joseph_bridge.py > /tmp/mc-bridge.log 2>&1 &
BRIDGE_PID=$!
sleep 1
echo -e "  ${GREEN}✓ Telegram bridge running${NC} (PID $BRIDGE_PID)"

# Start monitors if requested
if [[ "$1" == "--with-monitors" || "$2" == "--with-monitors" ]]; then
    if [ -z "$PERPLEXITY_API_KEY" ]; then
        echo -e "  ${YELLOW}⚠ Monitors need PERPLEXITY_API_KEY — skipping${NC}"
    else
        echo -e "Starting monitor_daemon.py..."
        PERPLEXITY_API_KEY="$PERPLEXITY_API_KEY" \
          JOSEPH_BOT_TOKEN="$JOSEPH_BOT_TOKEN" \
          TELEGRAM_CHAT_ID="${TELEGRAM_CHAT_ID:-}" \
          MC_WORKSPACE="$MC_WORKSPACE" \
          python3 monitor_daemon.py > /tmp/mc-monitors.log 2>&1 &
        MONITOR_PID=$!
        echo -e "  ${GREEN}✓ Monitor daemon running${NC} (PID $MONITOR_PID)"
    fi
fi

# Start tunnel if requested
if [[ "$1" == "--tunnel" || "$2" == "--tunnel" ]]; then
    if command -v cloudflared &> /dev/null; then
        echo -e "Starting cloudflared tunnel..."
        cloudflared tunnel --url http://localhost:8787 > /tmp/mc-tunnel.log 2>&1 &
        sleep 3
        TUNNEL_URL=$(grep -oP 'https://[a-z0-9-]+\.trycloudflare\.com' /tmp/mc-tunnel.log | head -1)
        echo -e "  ${GREEN}✓ Tunnel: $TUNNEL_URL${NC}"
    else
        echo -e "  ${YELLOW}⚠ cloudflared not installed — install: sudo snap install cloudflared${NC}"
    fi
fi

echo ""
echo -e "${GREEN}━━━ Demo Ready ━━━${NC}"
echo ""
echo "Web UI:     http://localhost:8787/oil-investor"
echo "Telegram:   @joseph_palette_bot"
echo "Logs:       /tmp/mc-server.log, /tmp/mc-bridge.log"
echo ""
echo "To stop:    kill $SERVER_PID $BRIDGE_PID ${MONITOR_PID:+$MONITOR_PID}"
echo "Or:         pkill -f 'node server.mjs'; pkill -f joseph_bridge"
echo ""
echo "━━━ Quick test commands for Joseph ━━━"
echo "  /start          — see what's available"
echo "  /brief          — today's executive brief"
echo "  /alerts         — recent market + AI alerts"
echo "  /research Is Anthropic a good AI investment?"
echo "  Should I trim upstream positions?"
echo ""

# Wait for Ctrl+C
trap "echo 'Stopping...'; kill $SERVER_PID $BRIDGE_PID ${MONITOR_PID:+$MONITOR_PID} 2>/dev/null; exit 0" INT
wait
