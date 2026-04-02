# Mission Canvas — Tech Stack

## Runtime
- Node.js 22+ (ESM modules, .mjs files)
- No build step — runs directly with `node server.mjs`
- Dependencies: js-yaml, node-html-parser, ajv, @modelcontextprotocol/sdk

## Code Style
- ESM imports (`import { x } from './file.mjs'`)
- No TypeScript — plain JavaScript
- Functions exported individually (`export function name()`)
- Error handling: return structured objects `{ ok: false, error: '...' }`, don't throw
- Async where needed, sync for file I/O in hot paths (cached on workspace load)

## Testing
- Test files: `stress_test_*.mjs` and `test_*.mjs`
- Run with: `node <test-file>.mjs` (server must be running on port 8787)
- Tests connect to localhost:8787 — they don't start their own server
- All tests must pass before committing

## Data
- YAML for config and state (js-yaml for parsing)
- JSON for API responses and exported data
- Workspace state: `workspaces/<id>/config.yaml` + `project_state.yaml`
- Schema validation: `config_schema.json`, `project_state_schema.json`

## Server
- Plain Node.js HTTP server (no Express, no framework)
- Port 8787
- CORS enabled
- NDJSON streaming for `/talk-stream`
- All endpoints under `/v1/missioncanvas/`
