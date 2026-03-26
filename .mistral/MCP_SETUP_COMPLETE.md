# Mistral Vibe MCP Setup Complete

## What Was Done

Configured Mistral Vibe runtime to connect to the Palette Peers message bus via MCP (Model Context Protocol).

## Configuration File

**Location:** `/home/mical/.vibe/config.toml`

## Changes Made

Added MCP server configuration to the `mcp_servers` array:

```toml
mcp_servers = [
  {
    name = "palette-peers",
    type = "stdio",
    command = "node",
    args = ["/home/mical/fde/palette/peers/adapters/generic/server.mjs", "mistral-vibe.builder"]
  }
]
```

## What This Does

When Mistral Vibe restarts, it will:
1. Spawn the MCP server as a subprocess using Node.js
2. Load the generic adapter: `/home/mical/fde/palette/peers/adapters/generic/server.mjs`
3. Use identity: `mistral-vibe.builder` (already configured in the adapter)
4. Connect to broker at: `http://127.0.0.1:7899`
5. Register on the Palette Peers message bus
6. Provide 8 new tools: `peers_send`, `peers_fetch`, `peers_list`, `peers_status`, `peers_checkpoints`, `peers_approve`, `peers_reject`, `peers_thread`

## Verification Steps After Restart

1. Run `peers_status` - should return broker health and peer count
2. Run `peers_list` - should show other connected peers (claude.analysis, kiro.design)
3. Run `peers_fetch` - should retrieve your pending task message

## Expected Task

After connection, you should receive task: **"write calibration exemplars for RIU-001 (Convergence Brief)"**

Task details are in: `/home/mical/fde/enablement/MISTRAL_TASK_001.md`

## Architecture

```
[Mistral Vibe Runtime] --stdio--> [MCP Server] --HTTP--> [Peers Broker :7899] --HTTP--> [Other Agents]
```

## Current Team Status

- Claude Code (claude.analysis): ✅ Live on MCP
- Kiro (kiro.design): ✅ Live on MCP  
- Codex (codex.implementation): ✅ Live on MCP
- Mistral Vibe (mistral-vibe.builder): 🟡 Configured, needs restart
- Perplexity (perplexity.research): ❌ Manual relay only

## Files Modified

- `/home/mical/.vibe/config.toml` - Added MCP server configuration

## Files Referenced

- `/home/mical/fde/palette/peers/adapters/generic/server.mjs` - MCP server (not modified)
- `/home/mical/fde/enablement/MISTRAL_ONBOARDING_MCP.md` - Onboarding guide
- `/home/mical/fde/enablement/MISTRAL_TASK_001.md` - Your pending task

## Restart Required

Mistral Vibe needs to restart to load the new MCP configuration and establish the connection.