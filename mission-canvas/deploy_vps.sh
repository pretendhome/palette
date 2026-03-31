#!/bin/bash
# deploy_vps.sh — Deploy Mission Canvas to Hostinger VPS
#
# Usage:
#   ./deploy_vps.sh                 # deploy files
#   ./deploy_vps.sh --start         # deploy + start services
#
# Prerequisites:
#   - SSH access to root@srv1390882.hstgr.cloud
#   - Set env vars on VPS or pass them here

set -e

VPS="root@srv1390882.hstgr.cloud"
VPS_DIR="/root/fde/missioncanvas-site"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Deploying Mission Canvas to $VPS:$VPS_DIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Files to deploy
FILES=(
    server.mjs
    convergence_chain.mjs
    workspace_coaching.mjs
    joseph_bridge.py
    monitor_daemon.py
    mcp_server.mjs
    start_demo.sh
    start_mcp.sh
    setup.html
    setup.js
    package.json
)

# Create remote directory structure
ssh "$VPS" "mkdir -p $VPS_DIR/workspaces"

# Sync core files
for f in "${FILES[@]}"; do
    echo "  → $f"
    scp "$SCRIPT_DIR/$f" "$VPS:$VPS_DIR/$f"
done

# Sync workspace data
echo "  → workspaces/oil-investor/"
rsync -avz --exclude='sessions/' \
    "$SCRIPT_DIR/workspaces/oil-investor/" \
    "$VPS:$VPS_DIR/workspaces/oil-investor/"

# Install dependencies on VPS
echo "Installing dependencies on VPS..."
ssh "$VPS" "cd $VPS_DIR && npm install 2>/dev/null; pip3 install httpx pyyaml 2>/dev/null"

# Create systemd service files
echo "Creating systemd services..."
ssh "$VPS" "cat > /etc/systemd/system/missioncanvas.service << 'UNIT'
[Unit]
Description=Mission Canvas Server
After=network.target

[Service]
Type=simple
WorkingDirectory=$VPS_DIR
ExecStart=/usr/bin/node server.mjs
Restart=always
RestartSec=5
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
UNIT"

ssh "$VPS" "cat > /etc/systemd/system/joseph-bridge.service << 'UNIT'
[Unit]
Description=Joseph Telegram Bridge
After=missioncanvas.service
Requires=missioncanvas.service

[Service]
Type=simple
WorkingDirectory=$VPS_DIR
ExecStart=/usr/bin/python3 joseph_bridge.py
Restart=always
RestartSec=5
EnvironmentFile=$VPS_DIR/joseph.env

[Install]
WantedBy=multi-user.target
UNIT"

ssh "$VPS" "cat > /etc/systemd/system/mc-monitors.service << 'UNIT'
[Unit]
Description=Mission Canvas Monitor Daemon
After=missioncanvas.service
Requires=missioncanvas.service

[Service]
Type=simple
WorkingDirectory=$VPS_DIR
ExecStart=/usr/bin/python3 monitor_daemon.py
Restart=always
RestartSec=30
EnvironmentFile=$VPS_DIR/joseph.env

[Install]
WantedBy=multi-user.target
UNIT"

# Create env file template
ssh "$VPS" "cat > $VPS_DIR/joseph.env << 'ENV'
JOSEPH_BOT_TOKEN=<your-telegram-bot-token>
MC_SERVER=http://localhost:8787
MC_WORKSPACE=oil-investor
# PERPLEXITY_API_KEY=pplx-xxx
# TELEGRAM_CHAT_ID=
ENV"

echo ""
echo "━━━ Deployed ━━━"
echo ""
echo "To start services on VPS:"
echo "  ssh $VPS"
echo "  systemctl daemon-reload"
echo "  systemctl enable --now missioncanvas joseph-bridge"
echo "  # Optional: systemctl enable --now mc-monitors"
echo ""
echo "To check status:"
echo "  ssh $VPS 'systemctl status missioncanvas joseph-bridge mc-monitors'"
echo ""

if [[ "$1" == "--start" ]]; then
    echo "Starting services..."
    ssh "$VPS" "systemctl daemon-reload && systemctl restart missioncanvas joseph-bridge"
    echo "Done. Check with: ssh $VPS 'systemctl status missioncanvas joseph-bridge'"
fi
