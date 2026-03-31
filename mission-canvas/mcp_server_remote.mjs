// Mission Canvas MCP Server — Remote Mode
// Connects to a Mission Canvas server via HTTP API.
// All workspace data lives on the server — no local files needed.
//
// Run: node mcp_server_remote.mjs [workspace_id]
// Env: MC_SERVER=http://your-vps:8787  (required)
//      MC_WORKSPACE=oil-investor       (optional, default)
//
// Claude Desktop config:
// {
//   "mcpServers": {
//     "mission-canvas": {
//       "command": "node",
//       "args": ["mcp_server_remote.mjs", "oil-investor"],
//       "env": { "MC_SERVER": "http://your-vps:8787" }
//     }
//   }
// }

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

const MC_SERVER = process.env.MC_SERVER || 'http://localhost:8787';
const DEFAULT_WORKSPACE = process.argv[2] || process.env.MC_WORKSPACE || 'oil-investor';

// ── HTTP helper ──

async function api(endpoint, payload = {}) {
  const url = `${MC_SERVER}/v1/missioncanvas/${endpoint}`;
  const resp = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  return resp.json();
}

function text(str) {
  return { content: [{ type: 'text', text: str }] };
}

// ── Create MCP Server ──

const server = new McpServer({
  name: 'mission-canvas',
  version: '2.0.0',
  description: `Connected to ${MC_SERVER} — workspace: ${DEFAULT_WORKSPACE}`
});

// ── Tool: workspace_brief ──

server.tool(
  'workspace_brief',
  'Get the daily brief for a workspace — health score, blockers, next actions, coaching hints.',
  { workspace_id: z.string().optional().describe('Workspace ID (default: ' + DEFAULT_WORKSPACE + ')') },
  async ({ workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const result = await api('workspace-welcome', { workspace_id: wsId });

    if (result.status !== 'ok') return text(result.error || 'Failed to load brief.');

    const lines = [
      `# ${result.workspace_name || wsId} — Daily Brief`,
      '',
      `**Health**: ${result.health_score}/100 (${result.health_label})`,
      `**Target**: ${result.target_score}/100`,
      '',
      `_${result.objective || ''}_`,
    ];

    const nudges = result.nudges || [];
    if (nudges.length > 0) {
      lines.push('', '## Items needing attention', '');
      for (const n of nudges) {
        const who = n.is_yours ? '(on you)' : `(${n.who_resolves || '?'})`;
        lines.push(`- **${n.summary}** — ${n.age_string || '?'} ${who}`);
      }
    }

    if (result.daily_brief) {
      const db = result.daily_brief;
      if (db.action_brief_markdown) {
        lines.push('', '---', '', db.action_brief_markdown);
      }
    }

    return text(lines.join('\n'));
  }
);

// ── Tool: ask ──

server.tool(
  'ask',
  'Ask a question about the workspace — status, blockers, next actions, what changed, facts, decisions. Routes automatically.',
  {
    question: z.string().describe('Your question (e.g. "how are we doing", "what is blocking us", "what should I do next")'),
    workspace_id: z.string().optional()
  },
  async ({ question, workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const result = await api('route', {
      input: { objective: question },
      workspace_id: wsId
    });

    const chain = result.convergence_chain || {};
    const narration = chain.narration || '';
    const brief = result.action_brief_markdown || '';
    const error = result.error;

    if (error && typeof error === 'object' && error.message) {
      return text(`Error: ${error.message}`);
    }

    return text(narration || brief || JSON.stringify(result, null, 2).slice(0, 3000));
  }
);

// ── Tool: resolve_evidence ──

server.tool(
  'resolve_evidence',
  'Resolve a missing evidence gap by providing the answer. Improves health score and may unblock decisions.',
  {
    evidence_id: z.string().describe('Evidence ID (e.g. ME-001)'),
    resolution: z.string().describe('The answer or resolution'),
    workspace_id: z.string().optional()
  },
  async ({ evidence_id, resolution, workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const result = await api('resolve-evidence', {
      workspace_id: wsId,
      evidence_id,
      resolution
    });

    if (result.status === 'resolved') {
      const lines = [
        `**Resolved**: ${evidence_id}`,
        `**Health**: ${result.health_score}/100`,
        `**Remaining gaps**: ${result.remaining_gaps}`,
      ];
      if (result.unblocked && result.unblocked.length > 0) {
        lines.push(`**Unblocked**: ${result.unblocked.join(', ')}`);
      }
      return text(lines.join('\n'));
    }

    return text(result.error || 'Failed to resolve evidence.');
  }
);

// ── Tool: add_fact ──

server.tool(
  'add_fact',
  'Add a known fact to the workspace. Facts improve the health score and provide context for decisions.',
  {
    fact: z.string().describe('The fact to add'),
    source: z.string().describe('Source of the fact (e.g. "EIA report", "user-provided")'),
    workspace_id: z.string().optional()
  },
  async ({ fact, source, workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const result = await api('add-fact', {
      workspace_id: wsId,
      fact,
      source
    });

    if (result.status === 'added') {
      return text(`Got it. (${result.total_facts} facts, health: ${result.health_score}/100)\n_${fact}_`);
    }

    return text(result.error || 'Failed to add fact.');
  }
);

// ── Tool: verify_mastery ──

server.tool(
  'verify_mastery',
  'Verify understanding of a concept. Completes the learning loop — system stops teaching this concept once verified.',
  {
    concept_id: z.string().describe('Concept ID (e.g. OIL-002, one_way_door)'),
    answer: z.string().optional().describe('Your understanding in one sentence'),
    workspace_id: z.string().optional()
  },
  async ({ concept_id, answer, workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const result = await api('verify-mastery', {
      workspace_id: wsId,
      concept_id,
      answer: answer || ''
    });

    if (result.status === 'verified' || result.status === 'already_verified') {
      return text(`**${concept_id}**: ${result.status}. ${result.newly_verified ? 'Mastery recorded.' : 'Already verified.'}`);
    }

    return text(result.error || result.message || 'Verification failed.');
  }
);

// ── Tool: list_gaps ──

server.tool(
  'list_gaps',
  'List all missing evidence gaps. These are things the system needs to know but does not yet.',
  { workspace_id: z.string().optional() },
  async ({ workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    // Route through the chain — "what is blocking us" maps to blockers/gaps
    const result = await api('route', {
      input: { objective: 'what is blocking us?' },
      workspace_id: wsId
    });

    const chain = result.convergence_chain || {};
    return text(result.action_brief_markdown || chain.narration || 'No gaps found.');
  }
);

// ── Tool: list_decisions ──

server.tool(
  'list_decisions',
  'List all open decisions — which are blocked and which are ready to approve.',
  { workspace_id: z.string().optional() },
  async ({ workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const result = await api('route', {
      input: { objective: 'what decisions are pending?' },
      workspace_id: wsId
    });

    const chain = result.convergence_chain || {};
    return text(result.action_brief_markdown || chain.narration || 'No open decisions.');
  }
);

// ── Tool: workspace_health ──

server.tool(
  'workspace_health',
  'Get the health score breakdown — what contributes to the score and what would improve it fastest.',
  { workspace_id: z.string().optional() },
  async ({ workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const result = await api('workspace-welcome', { workspace_id: wsId });

    if (result.status !== 'ok') return text(result.error || 'Failed to load health.');

    const lines = [
      `# Health Score: ${result.health_score}/100 (${result.health_label})`,
      `Target: ${result.target_score}/100`,
      '',
      `_${result.objective || ''}_`,
    ];

    const nudges = result.nudges || [];
    if (nudges.length > 0) {
      lines.push('', '## What needs attention');
      for (const n of nudges) {
        const who = n.is_yours ? '(on you)' : `(${n.who_resolves || '?'})`;
        lines.push(`- **${n.summary}** — ${n.age_string || '?'} ${who}`);
      }
    }

    return text(lines.join('\n'));
  }
);

// ── Tool: update_profile ──

server.tool(
  'update_profile',
  'Push a sanitized profile to the workspace. This is the public-safe summary of the investor lens. PII is blocked server-side.',
  {
    profile: z.string().describe('Sanitized profile markdown (no PII — first name, city only, ranges not exact amounts)'),
    workspace_id: z.string().optional()
  },
  async ({ profile, workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const result = await api('update-profile', {
      workspace_id: wsId,
      profile
    });

    if (result.status === 'updated') {
      return text(`Profile updated for workspace "${wsId}".`);
    }
    if (result.status === 'blocked') {
      return text(`**Blocked**: ${result.message}\nViolations: ${(result.violations || []).join(', ')}\n\nRemove personal data and try again.`);
    }

    return text(result.error || result.message || 'Failed to update profile.');
  }
);

// ── Resource: workspace state summary ──

server.resource(
  'workspace://state',
  'workspace://state',
  async (uri) => {
    const result = await api('workspace-welcome', { workspace_id: DEFAULT_WORKSPACE });
    const summary = {
      workspace: DEFAULT_WORKSPACE,
      server: MC_SERVER,
      health_score: result.health_score,
      health_label: result.health_label,
      objective: result.objective,
      nudges: (result.nudges || []).length,
    };
    return { contents: [{ uri: uri.href, text: JSON.stringify(summary, null, 2), mimeType: 'application/json' }] };
  }
);

// ── Start ──

const transport = new StdioServerTransport();
await server.connect(transport);
