#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/7] Ensure .env.production exists"
if [[ ! -f .env.production ]]; then
  cp .env.production.example .env.production
  echo "  Created .env.production from template"
else
  echo "  Found existing .env.production"
fi

echo "[2/7] Validate required env values"
set -a
source .env.production
set +a

missing=0
for v in OPENCLAW_BASE_URL OPENCLAW_UPSTREAM_MODE OPENCLAW_AGENT_ID ALLOW_ORIGIN; do
  if [[ -z "${!v:-}" || "${!v}" == *"CHANGE_ME"* || "${!v}" == *"<"* ]]; then
    echo "  Missing or placeholder: $v"
    missing=1
  fi
done
if [[ -z "${OPENCLAW_API_KEY:-}" || "${OPENCLAW_API_KEY}" == *"CHANGE_ME"* || "${OPENCLAW_API_KEY}" == *"<"* ]]; then
  echo "  Missing or placeholder: OPENCLAW_API_KEY"
  missing=1
fi
if [[ "${OPENCLAW_UPSTREAM_MODE:-}" != "missioncanvas" && "${OPENCLAW_UPSTREAM_MODE:-}" != "responses" && "${OPENCLAW_UPSTREAM_MODE:-}" != "chatcompletions" ]]; then
  echo "  OPENCLAW_UPSTREAM_MODE must be missioncanvas|responses|chatcompletions"
  missing=1
fi
if [[ "$missing" -ne 0 ]]; then
  echo "\nFill .env.production values first, then rerun."
  exit 2
fi

echo "[3/7] Static contract check"
node adapter_contract_check.mjs

echo "[4/7] Start adapter (background)"
node server.mjs > /tmp/missioncanvas_server.log 2>&1 &
SERVER_PID=$!
sleep 2

cleanup() {
  if kill -0 "$SERVER_PID" >/dev/null 2>&1; then
    kill "$SERVER_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

echo "[5/7] Health checks"
curl -fsS http://localhost:${PORT:-8787}/v1/missioncanvas/health | sed -n '1,120p'
curl -fsS http://localhost:${PORT:-8787}/v1/missioncanvas/capabilities | sed -n '1,120p'

echo "[6/7] Run Rossi pilot (online)"
node scripts/run_rossi_pilot.mjs --api-base http://localhost:${PORT:-8787}

echo "[7/7] Completed"
echo "- Adapter log: /tmp/missioncanvas_server.log"
echo "- Pilot outputs: $ROOT_DIR/pilot-output"
