// Mission Canvas MCP Server
// Exposes workspace tools to any MCP client (Claude Desktop, Claude Code, Cursor, etc.)
// Run: node mcp_server.mjs [workspace_id]
// Default workspace: oil-investor

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  detectProjectQuery,
  handleProjectQuery,
  loadWorkspace,
  updateProjectState,
  invalidateIndex,
  generateNudges,
  formatNudgesAsWelcome,
  calculateHealthScore,
  generateDailyBrief,
  getISODate,
  lookupWorkspaceKnowledge
} from './convergence_chain.mjs';

import {
  buildCoachingResponse,
  loadLearnerLens,
  saveLearnerLens,
  verifyMastery
} from './workspace_coaching.mjs';

import {
  generateKLCandidate,
  generateDecisionRecord,
  generateDecisionCoaching,
  generateMasterySignal,
  persistFeedback,
  getPendingFeedback,
  markFeedbackIngested
} from './flywheel_feedback.mjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const WORKSPACES_DIR = path.join(__dirname, 'workspaces');

// Default workspace from CLI arg or env
const DEFAULT_WORKSPACE = process.argv[2] || process.env.MC_WORKSPACE || 'oil-investor';

// Workspace cache (same pattern as server.mjs)
const workspaceCache = new Map();
function getWorkspace(workspaceId) {
  if (!workspaceId) return null;
  if (workspaceCache.has(workspaceId)) return workspaceCache.get(workspaceId);
  const ws = loadWorkspace(WORKSPACES_DIR, workspaceId);
  if (ws) workspaceCache.set(workspaceId, ws);
  return ws;
}

// Flatten nested config for functions that expect { user_name, domain, project_name, ... }
function flatConfig(config) {
  const ws = config.workspace || {};
  return {
    user_name: ws.user_name || 'there',
    domain: ws.domain || 'general',
    project_name: ws.name || ws.id || 'your project',
    user_role: ws.user_role || 'owner',
    ...config
  };
}

function getLearnerLens(workspace, workspaceId) {
  if (!workspace._learnerLensCache) {
    workspace._learnerLensCache = loadLearnerLens(WORKSPACES_DIR, workspaceId);
  }
  return workspace._learnerLensCache;
}

// ── Create MCP Server ──

const server = new McpServer({
  name: 'mission-canvas',
  version: '1.0.0'
});

// ── Tool: workspace_brief ──

server.tool(
  'workspace_brief',
  'Get the daily brief for a workspace — health score, blockers, next actions, coaching hints. This is the "how are we doing" view.',
  { workspace_id: z.string().optional().describe('Workspace ID (default: oil-investor)') },
  async ({ workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const ws = getWorkspace(wsId);
    if (!ws) return { content: [{ type: 'text', text: `Workspace "${wsId}" not found.` }] };

    const cfg = flatConfig(ws.config);
    const brief = generateDailyBrief(ws.projectState, cfg);
    const health = calculateHealthScore(ws.projectState);
    const nudges = generateNudges(ws.projectState, {
      nudge_threshold_days: (ws.config.frx || {}).nudge_threshold_days || 14,
      max_nudges: 5,
      user_role: cfg.user_role
    });
    const nudgeText = nudges.length > 0 ? formatNudgesAsWelcome(nudges, cfg) : '';

    const lines = [
      `# ${(ws.config.workspace || {}).name || wsId} — Daily Brief`,
      '',
      `**Health**: ${health.score}/100 (${health.label})`,
      '',
      brief.action_brief_markdown || brief.narration || '',
    ];
    if (nudgeText) {
      lines.push('', '---', '', '## Nudges', nudgeText);
    }

    return { content: [{ type: 'text', text: lines.join('\n') }] };
  }
);

// ── Tool: ask ──

server.tool(
  'ask',
  'Ask a question about the workspace — status, blockers, next actions, what changed, facts, decisions. The system routes to the right answer automatically.',
  {
    question: z.string().describe('Your question (e.g. "how are we doing", "what is blocking us", "what should I do next")'),
    workspace_id: z.string().optional().describe('Workspace ID (default: oil-investor)')
  },
  async ({ question, workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const ws = getWorkspace(wsId);
    if (!ws) return { content: [{ type: 'text', text: `Workspace "${wsId}" not found.` }] };

    // Try project-state query first
    const queryDetection = detectProjectQuery(question);
    if (queryDetection.detected) {
      if (ws.knowledgeLibrary) ws.projectState._workspaceKL = ws.knowledgeLibrary;
      ws.projectState._learnerLens = getLearnerLens(ws, wsId);
      const result = handleProjectQuery(queryDetection.type, ws.projectState, ws.config);

      // Persist learner_lens if coaching signals fired
      if (result.convergence_chain?.coaching_signals) {
        ws._learnerLensCache = ws.projectState._learnerLens;
        saveLearnerLens(WORKSPACES_DIR, wsId, ws._learnerLensCache);
        for (const signal of result.convergence_chain.coaching_signals) {
          persistFeedback(WORKSPACES_DIR, wsId, {
            id: `CS-${signal.concept_id}-${Date.now()}`,
            type: 'concept_exposure',
            concept_id: signal.concept_id,
            term: signal.term,
            depth: signal.depth,
            workspace_id: wsId,
            detected_at: signal.detected_at,
            status: 'candidate',
            source_type: 'chain_narration'
          });
        }
      }

      return { content: [{ type: 'text', text: result.action_brief_markdown || result.convergence_chain?.narration || 'No data.' }] };
    }

    // Try coaching intercept for explanatory questions
    const coachingResult = buildCoachingResponse({
      objective: question,
      workspace: ws,
      workspaceId: wsId,
      workspacesDir: WORKSPACES_DIR
    });
    if (coachingResult) {
      return { content: [{ type: 'text', text: coachingResult.action_brief_markdown || coachingResult.coaching?.answer || 'No coaching available.' }] };
    }

    // Try knowledge library lookup
    if (ws.knowledgeLibrary && ws.knowledgeLibrary.length > 0) {
      const results = lookupWorkspaceKnowledge(ws.knowledgeLibrary, question, 3);
      if (results.length > 0) {
        const text = results.map(r => `**${r.question}**\n${r.answer}`).join('\n\n---\n\n');
        return { content: [{ type: 'text', text }] };
      }
    }

    // Last resort: if question looks like "what should I do / focus / priority / next" → return brief + nudges
    if (/focus|priorit|first|next|start|begin|do now/i.test(question)) {
      const cfg = flatConfig(ws.config);
      const brief = generateDailyBrief(ws.projectState, cfg);
      const health = calculateHealthScore(ws.projectState);
      const nudges = generateNudges(ws.projectState, {
        nudge_threshold_days: (ws.config.frx || {}).nudge_threshold_days || 14,
        max_nudges: 5,
        user_role: cfg.user_role
      });
      const nudgeText = nudges.length > 0 ? formatNudgesAsWelcome(nudges, cfg) : '';
      const lines = [
        `# Here's your priority view`,
        '',
        `**Health**: ${health.score}/100 (${health.label})`,
        '',
        brief.action_brief_markdown || brief.narration || '',
      ];
      if (nudgeText) lines.push('', '---', '', '## What needs your attention', nudgeText);
      return { content: [{ type: 'text', text: lines.join('\n') }] };
    }

    return { content: [{ type: 'text', text: `I don't have a specific answer for "${question}" in this workspace. Try: "how are we doing", "what's blocking us", "what should I do next", or ask about a specific concept.` }] };
  }
);

// ── Tool: resolve_evidence ──

server.tool(
  'resolve_evidence',
  'Resolve a missing evidence gap by providing the answer. This improves the health score and may unblock decisions.',
  {
    evidence_id: z.string().describe('Evidence ID to resolve (e.g. ME-001, ME-003)'),
    resolution: z.string().describe('The answer or resolution for this evidence gap'),
    workspace_id: z.string().optional()
  },
  async ({ evidence_id, resolution, workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const ws = getWorkspace(wsId);
    if (!ws) return { content: [{ type: 'text', text: `Workspace "${wsId}" not found.` }] };

    const ps = ws.projectState.project_state || ws.projectState;
    if (!ps.missing_evidence) ps.missing_evidence = [];
    const idx = ps.missing_evidence.findIndex(e => e.id === evidence_id);
    if (idx === -1) {
      const available = ps.missing_evidence.map(e => `${e.id}: ${e.what || e.summary || 'no description'}`).join('\n');
      return { content: [{ type: 'text', text: `Evidence "${evidence_id}" not found.\n\nAvailable gaps:\n${available || 'None'}` }] };
    }

    const evidence = ps.missing_evidence.splice(idx, 1)[0];
    if (!ps.known_facts) ps.known_facts = [];
    ps.known_facts.push({
      id: `KF-AUTO-${Date.now().toString(36).slice(-4)}`,
      fact: evidence.what || evidence.summary || evidence_id,
      source: resolution
    });

    // Unblock dependencies
    const unblocked = [];
    if (ps.open_decisions) {
      for (const od of ps.open_decisions) {
        if (od.blocked_by && od.blocked_by.includes(evidence_id)) {
          od.blocked_by = od.blocked_by.filter(b => b !== evidence_id);
          if (od.blocked_by.length === 0) { delete od.blocked_by; unblocked.push(od.id); }
        }
      }
    }

    updateProjectState(WORKSPACES_DIR, wsId, ws.projectState);
    invalidateIndex(ws.projectState);
    workspaceCache.delete(wsId);

    // Flywheel: generate Palette KL candidate
    const wsConfig = ws.config?.workspace || {};
    const klCandidate = generateKLCandidate(evidence, resolution, wsId, wsConfig.domain);
    persistFeedback(WORKSPACES_DIR, wsId, klCandidate);

    const health = calculateHealthScore(ws.projectState);
    const lines = [
      `**Resolved**: ${evidence_id} — ${evidence.what || evidence.summary}`,
      `**Health**: ${health.score}/100 (${health.label})`,
      `**Remaining gaps**: ${ps.missing_evidence.length}`,
    ];
    if (unblocked.length > 0) lines.push(`**Unblocked**: ${unblocked.join(', ')}`);
    lines.push(`\n_Knowledge candidate ${klCandidate.id} staged for Palette._`);

    return { content: [{ type: 'text', text: lines.join('\n') }] };
  }
);

// ── Tool: approve_decision ──

server.tool(
  'approve_decision',
  'Approve a one-way-door decision. These are consequential, hard-to-reverse decisions that require explicit approval. The system will ask you to articulate WHY you made this choice.',
  {
    decision_id: z.string().describe('Decision ID to approve (e.g. OD-001)'),
    reason: z.string().describe('Why you are approving this decision'),
    workspace_id: z.string().optional()
  },
  async ({ decision_id, reason, workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const ws = getWorkspace(wsId);
    if (!ws) return { content: [{ type: 'text', text: `Workspace "${wsId}" not found.` }] };

    const ps = ws.projectState.project_state || ws.projectState;
    if (!ps.open_decisions) ps.open_decisions = [];
    const decision = ps.open_decisions.find(d => d.id === decision_id);
    if (!decision) {
      const available = ps.open_decisions.map(d => `${d.id}: ${d.decision}`).join('\n');
      return { content: [{ type: 'text', text: `Decision "${decision_id}" not found.\n\nOpen decisions:\n${available || 'None'}` }] };
    }

    // Check if blocked
    if (decision.blocked_by && decision.blocked_by.length > 0) {
      return { content: [{ type: 'text', text: `Decision "${decision_id}" is blocked by: ${decision.blocked_by.join(', ')}. Resolve those evidence gaps first.` }] };
    }

    // Approve: move to resolved
    decision.status = 'resolved';
    decision.resolved_at = getISODate();
    decision.resolution = reason;
    if (!ps.resolved_decisions) ps.resolved_decisions = [];
    ps.resolved_decisions.push(decision);
    ps.open_decisions = ps.open_decisions.filter(d => d.id !== decision_id);

    // Unblock actions
    const unblocked = [];
    if (ps.blocked_actions) {
      for (const ba of ps.blocked_actions) {
        if (ba.blocked_by && ba.blocked_by.includes(decision_id)) {
          ba.blocked_by = ba.blocked_by.filter(b => b !== decision_id);
          if (ba.blocked_by.length === 0) unblocked.push(ba.id || ba.action);
        }
      }
      ps.blocked_actions = ps.blocked_actions.filter(ba => !ba.blocked_by || ba.blocked_by.length > 0);
    }

    // Add known fact
    if (!ps.known_facts) ps.known_facts = [];
    ps.known_facts.push({
      id: `KF-AUTO-${Date.now().toString(36).slice(-4)}`,
      fact: `Decision approved: ${decision.decision}`,
      source: reason
    });

    updateProjectState(WORKSPACES_DIR, wsId, ws.projectState);
    invalidateIndex(ws.projectState);
    workspaceCache.delete(wsId);

    // Flywheel: decision record + coaching verification
    const approval = { reason };
    const decisionRecord = generateDecisionRecord(decision, approval, wsId);
    persistFeedback(WORKSPACES_DIR, wsId, decisionRecord);
    const coaching = generateDecisionCoaching(decision, approval);

    const health = calculateHealthScore(ws.projectState);
    const lines = [
      `**Approved**: ${decision.decision}`,
      `**Reason**: ${reason}`,
      `**Health**: ${health.score}/100 (${health.label})`,
    ];
    if (unblocked.length > 0) lines.push(`**Unblocked actions**: ${unblocked.join(', ')}`);
    lines.push('', '---', '', '**Coaching verification**:', coaching.answer, '', `_${coaching.verification_prompt}_`);

    return { content: [{ type: 'text', text: lines.join('\n') }] };
  }
);

// ── Tool: verify_mastery ──

server.tool(
  'verify_mastery',
  'Verify that you understand a concept. This completes the learning loop — the system stops teaching you about this concept once verified.',
  {
    concept_id: z.string().describe('Concept ID to verify (e.g. OIL-002, one_way_door)'),
    answer: z.string().optional().describe('Your understanding of the concept in one sentence'),
    workspace_id: z.string().optional()
  },
  async ({ concept_id, answer, workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const result = verifyMastery(WORKSPACES_DIR, wsId, concept_id, answer);

    if (!result.ok) {
      return { content: [{ type: 'text', text: `Cannot verify: ${result.message}` }] };
    }

    // Flywheel: mastery signal
    if (result.newly_verified) {
      const learnerLens = loadLearnerLens(WORKSPACES_DIR, wsId);
      const masterySignal = generateMasterySignal(concept_id, learnerLens, wsId);
      persistFeedback(WORKSPACES_DIR, wsId, masterySignal);
    }

    return { content: [{ type: 'text', text: `**${concept_id}**: ${result.status}. ${result.newly_verified ? 'Mastery recorded — the system will stop teaching this concept.' : 'Already verified.'}` }] };
  }
);

// ── Tool: list_gaps ──

server.tool(
  'list_gaps',
  'List all missing evidence gaps in the workspace. These are things the system needs to know but does not yet.',
  { workspace_id: z.string().optional() },
  async ({ workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const ws = getWorkspace(wsId);
    if (!ws) return { content: [{ type: 'text', text: `Workspace "${wsId}" not found.` }] };

    const ps = ws.projectState.project_state || ws.projectState;
    const gaps = ps.missing_evidence || [];
    if (gaps.length === 0) {
      return { content: [{ type: 'text', text: 'No missing evidence gaps. All clear.' }] };
    }

    const lines = gaps.map(g => {
      const priority = g.priority ? ` [${g.priority}]` : '';
      const blockedBy = g.blocked_by ? ` (blocked by: ${g.blocked_by})` : '';
      return `- **${g.id}**${priority}: ${g.what || g.summary || 'no description'}${blockedBy}`;
    });

    return { content: [{ type: 'text', text: `## Missing Evidence (${gaps.length} gaps)\n\n${lines.join('\n')}` }] };
  }
);

// ── Tool: list_decisions ──

server.tool(
  'list_decisions',
  'List all open decisions in the workspace, including which ones are blocked and which are ready to approve.',
  { workspace_id: z.string().optional() },
  async ({ workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const ws = getWorkspace(wsId);
    if (!ws) return { content: [{ type: 'text', text: `Workspace "${wsId}" not found.` }] };

    const ps = ws.projectState.project_state || ws.projectState;
    const decisions = ps.open_decisions || [];
    if (decisions.length === 0) {
      return { content: [{ type: 'text', text: 'No open decisions. All resolved.' }] };
    }

    const lines = decisions.map(d => {
      const blocked = d.blocked_by && d.blocked_by.length > 0;
      const status = blocked ? `🔒 blocked by ${d.blocked_by.join(', ')}` : '✅ ready to approve';
      const owd = d.one_way_door ? ' ⚠️ ONE-WAY DOOR' : '';
      return `- **${d.id}**${owd}: ${d.decision}\n  ${status}`;
    });

    return { content: [{ type: 'text', text: `## Open Decisions (${decisions.length})\n\n${lines.join('\n\n')}` }] };
  }
);

// ── Tool: workspace_health ──

server.tool(
  'workspace_health',
  'Get the current health score breakdown — what is contributing to the score and what would improve it fastest.',
  { workspace_id: z.string().optional() },
  async ({ workspace_id }) => {
    const wsId = workspace_id || DEFAULT_WORKSPACE;
    const ws = getWorkspace(wsId);
    if (!ws) return { content: [{ type: 'text', text: `Workspace "${wsId}" not found.` }] };

    const health = calculateHealthScore(ws.projectState);
    const ps = ws.projectState.project_state || ws.projectState;

    const lines = [
      `# Health Score: ${health.score}/100 (${health.label})`,
      '',
      `| Component | Count | Impact |`,
      `|-----------|-------|--------|`,
      `| Known facts | ${(ps.known_facts || []).length} | +1 each |`,
      `| Resolved decisions | ${(ps.resolved_decisions || []).length} | +3 each |`,
      `| Missing evidence | ${(ps.missing_evidence || []).length} | -5 each |`,
      `| Open decisions | ${(ps.open_decisions || []).length} | -3 each |`,
      `| Blocked actions | ${(ps.blocked_actions || []).length} | -2 each |`,
    ];

    // Suggest fastest improvement
    const suggestions = [];
    const criticalGaps = (ps.missing_evidence || []).filter(e => e.priority === 'critical');
    if (criticalGaps.length > 0) {
      suggestions.push(`Resolve critical gap **${criticalGaps[0].id}** (${criticalGaps[0].what}) for biggest impact`);
    }
    const readyDecisions = (ps.open_decisions || []).filter(d => !d.blocked_by || d.blocked_by.length === 0);
    if (readyDecisions.length > 0) {
      suggestions.push(`Approve ready decision **${readyDecisions[0].id}** (${readyDecisions[0].decision})`);
    }
    if (suggestions.length > 0) {
      lines.push('', '## Fastest Improvements', ...suggestions.map(s => `- ${s}`));
    }

    return { content: [{ type: 'text', text: lines.join('\n') }] };
  }
);

// ── Resource: workspace_state ──

server.resource(
  'workspace://state',
  'workspace://state',
  async (uri) => {
    const ws = getWorkspace(DEFAULT_WORKSPACE);
    if (!ws) return { contents: [{ uri: uri.href, text: 'Workspace not found', mimeType: 'text/plain' }] };

    const ps = ws.projectState.project_state || ws.projectState;
    const summary = {
      workspace: DEFAULT_WORKSPACE,
      health: calculateHealthScore(ws.projectState),
      missing_evidence: (ps.missing_evidence || []).length,
      open_decisions: (ps.open_decisions || []).length,
      blocked_actions: (ps.blocked_actions || []).length,
      known_facts: (ps.known_facts || []).length,
      resolved_decisions: (ps.resolved_decisions || []).length,
      knowledge_library_entries: (ws.knowledgeLibrary || []).length
    };

    return { contents: [{ uri: uri.href, text: JSON.stringify(summary, null, 2), mimeType: 'application/json' }] };
  }
);

// ── Start ──

const transport = new StdioServerTransport();
await server.connect(transport);
