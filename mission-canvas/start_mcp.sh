#!/usr/bin/env bash
# Launch Mission Canvas MCP server
# Usage: ./start_mcp.sh [workspace_id]
# Default: oil-investor
cd "$(dirname "$0")"
exec node mcp_server.mjs "${1:-oil-investor}"
