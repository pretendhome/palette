#!/usr/bin/env bash
set -euo pipefail

# Continuous PIS strict-audit runner.
# Stop with: Ctrl+C
#
# Optional env vars:
#   INTERVAL=2
#   BACKLOG_PATH=/tmp/pis_backlog.json
#   LOG_DIR=/tmp/pis-audit-runs

INTERVAL="${INTERVAL:-2}"
BACKLOG_PATH="${BACKLOG_PATH:-/tmp/pis_backlog.json}"
LOG_DIR="${LOG_DIR:-/tmp/pis-audit-runs}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PALETTE_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"

cd "${PALETTE_DIR}"
python3 -m scripts.pis.run_audit_batch \
  --infinite \
  --interval "${INTERVAL}" \
  --backlog-path "${BACKLOG_PATH}" \
  --log-dir "${LOG_DIR}"
