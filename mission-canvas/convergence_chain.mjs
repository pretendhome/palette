// Convergence Chain Engine — Phase 1 of V0.3
// The reasoning layer that turns inert project state into dependency-aware answers.
//
// Five components:
//   1. detectProjectQuery  — recognizes project-state questions before RIU routing
//   2. traceChain          — walks the dependency graph from any node
//   3. narrateChain        — produces natural language from a dependency chain
//   4. generateNudges      — finds stale blockers on session start
//   5. annotateWithCoaching — PASSIVE coaching: fires automatically during narration,
//                             detects domain concepts in text, tracks learner depth,
//                             injects inline hints on first encounter.
//                             Data store: learner_lens.yaml (shared with workspace_coaching.mjs)
//
// All deterministic. No LLM. Graph traversal over structured YAML.
//
// Assumptions:
//   - Date fields (created_at, last_updated, identified_at, resolved_at) are strings in ISO format (e.g., "2026-03-29")
//   - Node IDs (e.g., ME-001, OD-001) are unique within their category (missing_evidence, open_decisions, blocked_actions)
//   - Priority levels: critical > moderate > low (used for sorting)
//   - Status values: resolved, unresolved for missing_evidence; resolved, open for open_decisions
//   - The project_state.yaml file must conform to the schema defined in project_state_schema.json
//   - Circular dependencies are detected and handled gracefully (returns error without crashing)

import { readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { load as loadYAML, dump as dumpYAML } from 'js-yaml';
import Ajv from 'ajv';
import { readFileSync as readFile } from 'node:fs';
import { loadLearnerLens, saveLearnerLens } from './workspace_coaching.mjs';

const ajv = new Ajv();
const projectStateSchema = JSON.parse(readFile('./project_state_schema.json', 'utf-8'));
const validateProjectState = ajv.compile(projectStateSchema);

let validateConfig = null;
try {
  const configSchema = JSON.parse(readFile('./config_schema.json', 'utf-8'));
  validateConfig = ajv.compile(configSchema);
} catch { /* config schema not found — skip validation */ }

// ── 1. State-Aware Query Detector ──────────────────────────────────────────

const QUERY_PATTERNS = [
  {
    type: 'status',
    patterns: [
      /how are we doing/i,
      /how('s| is) (the |my |our )?progress/i,
      /what('s| is) (the |our |my )?status/i,
      /where (do we|are we) stand/i,
      /give me (a |the )?status/i,
      /^status$/i,
      /overall (status|health|progress)/i,
      /fundability/i,
      /health score/i,
    ]
  },
  {
    type: 'blockers',
    patterns: [
      /what('?s| is) blocking/i,
      /what('?s| is) (the |our )?block/i,
      /why.*(block|stuck)/i,
      /what are the gaps/i,
      /what('?s| is) missing/i,
      /what evidence (do we|is) (need|missing)/i,
      /^gaps$/i,
      /^blockers$/i,
      /stuck/i,
      /why can('?t| not)/i,
    ]
  },
  {
    type: 'next_action',
    patterns: [
      /what should (i|we) do (next|now)/i,
      /what('s| is) (the )?next (step|action|move)/i,
      /what can (i|we) do/i,
      /where should (i|we) (start|focus|begin)/i,
      /what('s| is) (the )?(most important|highest priority)/i,
      /^next$/i,
      /^priorities$/i,
      /what needs to happen/i,
    ]
  },
  {
    type: 'what_changed',
    patterns: [
      /what changed/i,
      /what('s| is) (new|different)/i,
      /any (updates|changes|news)/i,
      /what happened/i,
      /catch me up/i,
      /bring me up to (speed|date)/i,
    ]
  },
  {
    type: 'known_facts',
    patterns: [
      /what do (we|i) know/i,
      /what are the facts/i,
      /known facts/i,
      /what('s| is) confirmed/i,
      /^facts$/i,
    ]
  },
  {
    type: 'decisions',
    patterns: [
      /what decisions/i,
      /what('s| is) pending/i,
      /open decisions/i,
      /what needs deciding/i,
      /^decisions$/i,
      /show.*(the )?decisions/i,
      /pending decisions/i,
    ]
  }
];

/**
 * Detect if input is a project-state query that should short-circuit RIU routing.
 * @param {string} text - The user's input text (objective field)
 * @returns {{ detected: boolean, type: string|null, confidence: string }}
 */
export function detectProjectQuery(text) {
  if (!text || typeof text !== 'string') {
    return { detected: false, type: null, confidence: 'none' };
  }

  const trimmed = text.trim();

  for (const group of QUERY_PATTERNS) {
    for (const pattern of group.patterns) {
      if (pattern.test(trimmed)) {
        return { detected: true, type: group.type, confidence: 'high' };
      }
    }
  }

  return { detected: false, type: null, confidence: 'none' };
}

// ── 2. Dependency Chain Traverser ──────────────────────────────────────────

// Cache for buildIndex to avoid rebuilding the index for the same projectState
const indexCache = new WeakMap();

/** Invalidate cached index after project state mutation. */
export function invalidateIndex(projectState) {
  indexCache.delete(projectState);
}

/**
 * Build a lookup index from project state for fast node resolution.
 */
function buildIndex(projectState) {
  // Check if we already have an index for this projectState
  if (indexCache.has(projectState)) {
    return indexCache.get(projectState);
  }

  const ps = projectState.project_state || projectState;
  const index = new Map();

  for (const me of (ps.missing_evidence || [])) {
    index.set(me.id, { ...me, node_type: 'missing_evidence' });
  }
  for (const od of (ps.open_decisions || [])) {
    index.set(od.id, { ...od, node_type: 'open_decision' });
  }
  for (const ba of (ps.blocked_actions || [])) {
    index.set(ba.id, { ...ba, node_type: 'blocked_action' });
  }

  // Cache the index for future use
  indexCache.set(projectState, index);
  return index;
}

/**
 * Get current date in YYYY-MM-DD format.
 */
export function getISODate() {
  return new Date().toISOString().slice(0, 10);
}

/**
 * Compute age in days from an ISO date string.
 */
function ageDays(isoDate) {
  if (!isoDate) return null;
  const then = new Date(isoDate);
  const now = new Date();
  return Math.floor((now - then) / (1000 * 60 * 60 * 24));
}

/**
 * Compute age as a human-readable string.
 */
function ageString(days) {
  if (days === null) return 'unknown duration';
  if (days === 0) return 'just now';
  if (days < 7) return `${days} day${days === 1 ? '' : 's'}`;
  const weeks = Math.floor(days / 7);
  return `${weeks} week${weeks === 1 ? '' : 's'}`;
}

/**
 * Trace the full dependency chain from a given node ID.
 * Returns a tree of what this node unblocks (forward links).
 *
 * @param {string} nodeId - The ID of the node to trace from (e.g., "ME-001")
 * @param {object} projectState - Full project state YAML object
 * @param {Set} [visited] - Internal cycle detection
 * @returns {{ node: object, age_days: number, age_string: string, who_resolves: string, unblocks: Array }}
 */
export function traceChain(nodeId, projectState, visited = new Set()) {
  const index = typeof projectState._index !== 'undefined'
    ? projectState._index
    : buildIndex(projectState);

  const node = index.get(nodeId);
  if (!node) {
    const availableNodes = Array.from(index.keys()).join(', ');
    return { 
      node_id: nodeId, 
      node_type: 'unknown', 
      error: `Node not found: ${nodeId}. Available nodes: ${availableNodes}` 
    };
  }

  if (visited.has(nodeId)) {
    return { node_id: nodeId, node_type: node.node_type, error: 'Circular dependency' };
  }
  visited.add(nodeId);

  const age = ageDays(node.identified_at);
  const unblockIds = node.unblocks || [];

  const chain = {
    node_id: nodeId,
    node_type: node.node_type,
    summary: node.what || node.decision || node.action || nodeId,
    status: node.status || 'unknown',
    priority: node.priority || null,
    who_resolves: node.who_resolves || node.who_decides || null,
    age_days: age,
    age_string: ageString(age),
    identified_at: node.identified_at || null,
    unblocks: []
  };

  for (const childId of unblockIds) {
    // Resolve both node IDs and descriptive strings
    if (index.has(childId)) {
      chain.unblocks.push(traceChain(childId, projectState, new Set(visited)));
    } else {
      // Descriptive string like "fundability_improvement"
      chain.unblocks.push({
        node_id: childId,
        node_type: 'goal',
        summary: childId.replace(/_/g, ' '),
        unblocks: []
      });
    }
  }

  return chain;
}

/**
 * Trace all chains from all critical blockers.
 * Returns the full dependency forest.
 */
export function traceAllChains(projectState) {
  const ps = projectState.project_state || projectState;
  const index = buildIndex(projectState);
  // Cache index on the object for reuse
  const stateWithIndex = { ...projectState, _index: index };

  const chains = [];

  // Start from missing evidence (the leaves of the dependency tree)
  for (const me of (ps.missing_evidence || [])) {
    if (me.status === 'resolved') continue;
    if ((me.unblocks || []).length > 0) {
      chains.push(traceChain(me.id, stateWithIndex));
    }
  }

  // Also trace from missing evidence that blocks nothing (standalone gaps)
  for (const me of (ps.missing_evidence || [])) {
    if (me.status === 'resolved') continue;
    if ((me.unblocks || []).length === 0 && !chains.find(c => c.node_id === me.id)) {
      chains.push(traceChain(me.id, stateWithIndex));
    }
  }

  return chains;
}

// ── 3. Chain Narrator ──────────────────────────────────────────────────────

/**
 * Narrate a single dependency chain as human-readable text.
 */
function narrateSingleChain(chain, depth = 0) {
  const indent = '  '.repeat(depth);
  const lines = [];

  const ageNote = chain.age_string ? ` (${chain.age_string})` : '';
  const whoNote = chain.who_resolves ? ` — ${chain.who_resolves}` : '';
  const priorityNote = chain.priority ? ` [${chain.priority.toUpperCase()}]` : '';

  if (depth === 0) {
    lines.push(`${chain.summary}${priorityNote}${ageNote}${whoNote}`);
  } else {
    lines.push(`${indent}→ unblocks: ${chain.summary}${whoNote}`);
  }

  for (const child of (chain.unblocks || [])) {
    lines.push(...narrateSingleChain(child, depth + 1));
  }

  return lines;
}

/**
 * Produce a full narration for a project-state query response.
 *
 * @param {string} queryType - From detectProjectQuery: 'status', 'blockers', 'next_action', etc.
 * @param {object} projectState - Full project state YAML
 * @param {string} [userRole='owner'] - 'owner' or 'operator'
 * @returns {{ type: string, title: string, narration: string, data: object }}
 */
export function narrateChain(queryType, projectState, userRole = 'owner') {
  const ps = projectState.project_state || projectState;

  switch (queryType) {
    case 'status':
      return narrateStatus(ps, userRole);
    case 'blockers':
      return narrateBlockers(ps, userRole);
    case 'next_action':
      return narrateNextAction(ps, userRole);
    case 'what_changed':
      return narrateWhatChanged(ps);
    case 'known_facts':
      return narrateKnownFacts(ps);
    case 'decisions':
      return narrateDecisions(ps, userRole);
    default:
      return { type: queryType, title: 'Unknown Query', narration: 'Query type not recognized.', data: {} };
  }
}

function narrateStatus(ps, userRole) {
  const health = calculateHealthScore({ project_state: ps });
  const score = health.score;
  const label = health.label;
  const target = ps.target_score || 100;
  const objective = ps.objective || 'No objective set';

  const unresolvedEvidence = (ps.missing_evidence || []).filter(m => m.status !== 'resolved');
  const criticalGaps = unresolvedEvidence.filter(m => m.priority === 'critical');
  const openDecisions = (ps.open_decisions || []).filter(d => d.status !== 'resolved');
  const blockedActions = ps.blocked_actions || [];

  const chains = traceAllChains({ project_state: ps });
  const criticalChains = chains.filter(c => c.priority === 'critical');

  const lines = [
    `## ${ps.name || 'Project'} — Status`,
    '',
    `**Health Score**: ${score}/100 (${label}) — target: ${target}`,
    `**Objective**: ${objective}`,
    '',
  ];

  if (criticalGaps.length > 0) {
    lines.push(`**Critical Gaps**: ${criticalGaps.length}`);
    for (const gap of criticalGaps) {
      const age = ageDays(gap.identified_at);
      const ageStr = ageString(age);
      lines.push(`- **${gap.id}**: ${gap.what} — ${ageStr} outstanding, ${gap.who_resolves} must resolve`);
    }
    lines.push('');
  }

  if (criticalChains.length > 0) {
    lines.push('**Dependency Chain** (what the top blocker unlocks):');
    for (const chain of criticalChains) {
      lines.push(...narrateSingleChain(chain).map(l => `  ${l}`));
    }
    lines.push('');
  }

  if (openDecisions.length > 0) {
    lines.push(`**Open Decisions**: ${openDecisions.length}`);
    for (const d of openDecisions) {
      const blockedNote = (d.blocked_by || []).length > 0
        ? ` (blocked by ${d.blocked_by.join(', ')})`
        : '';
      lines.push(`- ${d.id}: ${d.decision}${blockedNote}`);
    }
    lines.push('');
  }

  if (blockedActions.length > 0) {
    lines.push(`**Blocked Actions**: ${blockedActions.length}`);
    for (const ba of blockedActions) {
      const blockers = Array.isArray(ba.blocked_by) ? ba.blocked_by.join(', ') : ba.blocked_by;
      lines.push(`- ${ba.action} — blocked by: ${blockers}`);
    }
    lines.push('');
  }

  // Bottom-line summary
  const topBlocker = criticalGaps[0];
  if (topBlocker) {
    const age = ageDays(topBlocker.identified_at);
    const roleRef = topBlocker.who_resolves === userRole ? 'you' : topBlocker.who_resolves;
    lines.push(`**Bottom line**: The #1 blocker is ${topBlocker.what}. It's been ${ageString(age)} and ${roleRef} need${roleRef === 'you' ? '' : 's'} to resolve it. Once done, it unblocks ${(topBlocker.unblocks || []).length} downstream item${(topBlocker.unblocks || []).length === 1 ? '' : 's'}.`);
  }

  return {
    type: 'status',
    title: `${ps.name || 'Project'} — Status`,
    narration: lines.join('\n'),
    data: {
      health_score: score,
      health_label: label,
      target_score: target,
      critical_gaps: criticalGaps.length,
      open_decisions: openDecisions.length,
      blocked_actions: blockedActions.length,
      chains: criticalChains
    }
  };
}

function narrateBlockers(ps, userRole) {
  const chains = traceAllChains({ project_state: ps });
  const unresolvedEvidence = (ps.missing_evidence || []).filter(m => m.status !== 'resolved');

  const lines = [
    `## Blockers & Evidence Gaps`,
    '',
    `**${unresolvedEvidence.length} evidence gap${unresolvedEvidence.length === 1 ? '' : 's'}** identified:`,
    '',
  ];

  // Sort by priority: critical first
  const sorted = [...unresolvedEvidence].sort((a, b) => {
    const order = { critical: 0, moderate: 1, low: 2 };
    return (order[a.priority] ?? 3) - (order[b.priority] ?? 3);
  });

  for (const gap of sorted) {
    const age = ageDays(gap.identified_at);
    const roleRef = gap.who_resolves === userRole ? 'you' : gap.who_resolves;
    const unblockCount = (gap.unblocks || []).length;
    lines.push(`### ${gap.id}: ${gap.what}`);
    lines.push(`- **Priority**: ${(gap.priority || 'unknown').toUpperCase()}`);
    lines.push(`- **Age**: ${ageString(age)}`);
    lines.push(`- **Who resolves**: ${roleRef}`);
    lines.push(`- **Why it matters**: ${gap.why}`);
    if (unblockCount > 0) {
      lines.push(`- **Unblocks**: ${gap.unblocks.join(', ')} (${unblockCount} item${unblockCount === 1 ? '' : 's'})`);
    }
    lines.push('');
  }

  // Blocked actions
  const blocked = ps.blocked_actions || [];
  if (blocked.length > 0) {
    lines.push('### Blocked Actions');
    for (const ba of blocked) {
      const blockers = Array.isArray(ba.blocked_by) ? ba.blocked_by.join(', ') : ba.blocked_by;
      lines.push(`- **${ba.action}** — needs: ${blockers}`);
    }
    lines.push('');
  }

  return {
    type: 'blockers',
    title: 'Blockers & Evidence Gaps',
    narration: lines.join('\n'),
    data: { gaps: sorted, blocked, chains }
  };
}

function narrateNextAction(ps, userRole) {
  const unresolvedEvidence = (ps.missing_evidence || []).filter(m => m.status !== 'resolved');

  // Filter to items this user can resolve
  const myItems = unresolvedEvidence.filter(m => m.who_resolves === userRole);
  const otherItems = unresolvedEvidence.filter(m => m.who_resolves !== userRole);

  // Sort by priority then age
  const sorted = [...myItems].sort((a, b) => {
    const order = { critical: 0, moderate: 1, low: 2 };
    const pDiff = (order[a.priority] ?? 3) - (order[b.priority] ?? 3);
    if (pDiff !== 0) return pDiff;
    return (ageDays(b.identified_at) ?? 0) - (ageDays(a.identified_at) ?? 0);
  });

  const openDecisions = (ps.open_decisions || [])
    .filter(d => d.status !== 'resolved' && d.who_decides === userRole && (d.blocked_by || []).length === 0);

  const lines = [
    `## What You Should Do Next`,
    '',
  ];

  if (sorted.length > 0) {
    lines.push(`**Evidence you need to supply** (${sorted.length} item${sorted.length === 1 ? '' : 's'}):`, '');
    for (let i = 0; i < sorted.length; i++) {
      const item = sorted[i];
      const age = ageDays(item.identified_at);
      lines.push(`${i + 1}. **${item.what}** [${(item.priority || '').toUpperCase()}] — ${ageString(age)}`);
      if (item.detail) lines.push(`   ${item.detail}`);
      if ((item.unblocks || []).length > 0) {
        lines.push(`   Unblocks: ${item.unblocks.join(', ')}`);
      }
    }
    lines.push('');
  }

  if (openDecisions.length > 0) {
    lines.push(`**Decisions ready for you** (${openDecisions.length}):`, '');
    for (const d of openDecisions) {
      lines.push(`- **${d.decision}**`);
      if (d.options && d.options.length > 0) {
        for (const opt of d.options) lines.push(`  - ${opt}`);
      }
    }
    lines.push('');
  }

  if (otherItems.length > 0) {
    lines.push(`**Waiting on others** (${otherItems.length}):`, '');
    for (const item of otherItems) {
      lines.push(`- ${item.what} — ${item.who_resolves}`);
    }
    lines.push('');
  }

  if (sorted.length === 0 && openDecisions.length === 0) {
    lines.push('No action items assigned to you right now. Check back with your operator.');
  }

  return {
    type: 'next_action',
    title: 'Next Actions',
    narration: lines.join('\n'),
    data: { my_evidence: sorted, my_decisions: openDecisions, waiting_on_others: otherItems }
  };
}

function narrateWhatChanged(ps) {
  // In V0.3, "what changed" compares against last session snapshot.
  // For now, return a summary of current state as a re-entry brief.
  const lastUpdated = ps.last_updated || 'unknown';
  const unresolvedEvidence = (ps.missing_evidence || []).filter(m => m.status !== 'resolved');
  const resolvedDecisions = ps.resolved_decisions || [];

  const lines = [
    `## What Changed Brief`,
    '',
    `**Last updated**: ${lastUpdated}`,
    '',
    `**Current state**:`,
    `- Health: ${calculateHealthScore({ project_state: ps }).score}/${ps.target_score || 100} (${calculateHealthScore({ project_state: ps }).label})`,
    `- Unresolved evidence gaps: ${unresolvedEvidence.length}`,
    `- Resolved decisions: ${resolvedDecisions.length}`,
    `- Known facts: ${(ps.known_facts || []).length}`,
    '',
    '*Note: Session-to-session diffing will be available when artifact persistence is enabled (Phase 7).*'
  ];

  return {
    type: 'what_changed',
    title: 'What Changed Brief',
    narration: lines.join('\n'),
    data: { last_updated: lastUpdated }
  };
}

function narrateKnownFacts(ps) {
  const facts = ps.known_facts || [];
  const lines = [
    `## Known Facts (${facts.length})`,
    '',
  ];

  for (const f of facts) {
    lines.push(`- **${f.id}**: ${f.fact}`);
    if (f.source) lines.push(`  Source: ${f.source}`);
  }

  return {
    type: 'known_facts',
    title: `Known Facts (${facts.length})`,
    narration: lines.join('\n'),
    data: { facts }
  };
}

function narrateDecisions(ps, userRole) {
  const openDecisions = (ps.open_decisions || []).filter(d => d.status !== 'resolved');
  const resolvedDecisions = ps.resolved_decisions || [];

  const lines = [
    `## Decisions`,
    '',
    `**${openDecisions.length} open**, ${resolvedDecisions.length} resolved`,
    '',
  ];

  if (openDecisions.length > 0) {
    lines.push('### Open');
    for (const d of openDecisions) {
      const blockedNote = (d.blocked_by || []).length > 0
        ? ` ⚠ blocked by: ${d.blocked_by.join(', ')}`
        : ' ✓ ready to decide';
      const roleRef = d.who_decides === userRole ? 'you' : d.who_decides;
      lines.push(`- **${d.id}**: ${d.decision}`);
      lines.push(`  Who decides: ${roleRef}${blockedNote}`);
      if (d.impact) lines.push(`  Impact: ${d.impact}`);
      if (d.options && d.options.length > 0) {
        for (const opt of d.options) lines.push(`    - ${opt}`);
      }
    }
    lines.push('');
  }

  if (resolvedDecisions.length > 0) {
    lines.push('### Resolved');
    for (const d of resolvedDecisions) {
      lines.push(`- **${d.id}**: ${d.decision} → ${d.resolution} (${d.resolved_at})`);
    }
  }

  return {
    type: 'decisions',
    title: 'Decisions',
    narration: lines.join('\n'),
    data: { open: openDecisions, resolved: resolvedDecisions }
  };
}

// ── 4. Proactive Nudge Generator ───────────────────────────────────────────

/**
 * Generate proactive nudges for stale blockers.
 * Called on session start to surface what needs attention.
 *
 * @param {object} projectState - Full project state YAML
 * @param {{ nudge_threshold_days?: number, max_nudges?: number, user_role?: string }} config
 * @returns {Array<{ id: string, summary: string, age_days: number, age_string: string, who_resolves: string, priority: string, urgency: string }>}
 */
export function generateNudges(projectState, config = {}) {
  const ps = projectState.project_state || projectState;
  const threshold = config.nudge_threshold_days || 14;
  const maxNudges = config.max_nudges || 3;
  const userRole = config.user_role || 'owner';

  const unresolvedEvidence = (ps.missing_evidence || []).filter(m => m.status !== 'resolved');
  const nudges = [];

  for (const me of unresolvedEvidence) {
    const age = ageDays(me.identified_at);
    if (age === null) continue;

    // Critical gaps bypass the age threshold but get a special urgency
    const isNewCritical = me.priority === 'critical' && age < threshold;
    if (age < threshold && !isNewCritical) continue;

    const urgency = isNewCritical ? 'immediate'
                  : age > 42 ? 'critical'    // 6+ weeks
                  : age > 28 ? 'high'        // 4+ weeks
                  : age > 14 ? 'moderate'     // 2+ weeks
                  : 'low';

    nudges.push({
      id: me.id,
      summary: me.what,
      age_days: age,
      age_string: ageString(age),
      who_resolves: me.who_resolves,
      priority: me.priority || 'unknown',
      urgency,
      unblocks_count: (me.unblocks || []).length,
      is_yours: me.who_resolves === userRole
    });
  }

  // Sort: critical priority first, then by age (oldest first)
  // Use ?? instead of || because 0 is falsy in JS
  nudges.sort((a, b) => {
    const pOrder = { critical: 0, high: 1, moderate: 2, low: 3 };
    const pDiff = (pOrder[a.priority] ?? 4) - (pOrder[b.priority] ?? 4);
    if (pDiff !== 0) return pDiff;
    return b.age_days - a.age_days;
  });

  return nudges.slice(0, maxNudges);
}

/**
 * Format nudges as a welcome message.
 */
export function formatNudgesAsWelcome(nudges, config = {}) {
  const userName = config.user_name || 'there';
  const projectName = config.project_name || 'your project';

  if (nudges.length === 0) {
    return `Good to see you, ${userName}. No stale blockers on ${projectName}.`;
  }

  const lines = [];
  const topNudge = nudges[0];

  if (nudges.length === 1) {
    lines.push(`${userName}, heads up: **${topNudge.summary}** has been outstanding for ${topNudge.age_string}.`);
    if (topNudge.is_yours) {
      lines.push(`This is on you. It unblocks ${topNudge.unblocks_count} downstream item${topNudge.unblocks_count === 1 ? '' : 's'}.`);
    }
  } else {
    lines.push(`${userName}, ${nudges.length} items need attention on ${projectName}:`);
    lines.push('');
    for (let i = 0; i < nudges.length; i++) {
      const n = nudges[i];
      const yours = n.is_yours ? ' (on you)' : ` (${n.who_resolves})`;
      lines.push(`${i + 1}. **${n.summary}** — ${n.age_string}${yours}`);
    }
    lines.push('');
    lines.push(`The #1 priority is **${topNudge.summary}** — ${topNudge.age_string} and counting.`);
  }

  return lines.join('\n');
}

// ── 5. Workspace Loader ────────────────────────────────────────────────────

/**
 * Load a workspace config and project state from disk.
 *
 * @param {string} workspacesDir - Path to workspaces/ directory
 * @param {string} workspaceId - Workspace ID (directory name)
 * @returns {{ config: object, projectState: object }|null}
 */
export function loadWorkspace(workspacesDir, workspaceId) {
  // Guard against path traversal
  if (!workspaceId || !/^[a-z0-9_-]+$/i.test(workspaceId)) return null;

  const configPath = `${workspacesDir}/${workspaceId}/config.yaml`;
  const statePath = `${workspacesDir}/${workspaceId}/project_state.yaml`;

  let config = null;
  let projectState = null;

  try {
    const configRaw = readFileSync(configPath, 'utf-8');
    config = loadYAML(configRaw);
    if (validateConfig && !validateConfig(config)) {
      console.warn(`[config] ${workspaceId}: schema warnings:`, validateConfig.errors.map(e => `${e.instancePath} ${e.message}`).join('; '));
    }
  } catch (e) {
    console.error(`Error loading workspace config at ${configPath}: ${e.message}`);
    return null; // workspace doesn't exist
  }

  try {
    const stateRaw = readFileSync(statePath, 'utf-8');
    projectState = loadYAML(stateRaw);
    const valid = validateProjectState(projectState);
    if (!valid) {
      console.error('Invalid project_state.yaml:', validateProjectState.errors);
      projectState = { project_state: {} };
    }
  } catch (e) {
    console.error('Error loading project state:', e.message);
    projectState = { project_state: {} };
  }

  // Load workspace-specific knowledge library if present
  let knowledgeLibrary = [];
  try {
    const wsDir = `${workspacesDir}/${workspaceId}`;
    const files = readdirSync(wsDir).filter(f => f.includes('knowledge_library') && f.endsWith('.yaml'));
    for (const file of files) {
      const klRaw = readFileSync(`${wsDir}/${file}`, 'utf-8');
      const klData = loadYAML(klRaw);
      const entries = klData.library_questions || klData.entries || [];
      knowledgeLibrary.push(...entries);
    }
    if (knowledgeLibrary.length > 0) {
      console.log(`[workspace] ${workspaceId}: loaded ${knowledgeLibrary.length} domain KL entries`);
    }
  } catch { /* no KL file — that's fine */ }

  return { config, projectState, knowledgeLibrary };
}

// ── 6. Full Query Handler ──────────────────────────────────────────────────

/**
 * Handle a project-state query end-to-end.
 * This is the main entry point called from server.mjs when detectProjectQuery returns true.
 *
 * @param {string} queryType - From detectProjectQuery
 * @param {object} projectState - Loaded project state
 * @param {object} config - Workspace config
 * @returns {object} - Full response object compatible with the route response shape
 */
export function handleProjectQuery(queryType, projectState, config) {
  const ps = projectState.project_state || projectState;
  const wsConfig = config.workspace || config;
  const userRole = wsConfig.user_role || 'owner';

  const result = narrateChain(queryType, projectState, userRole);
  const nudges = generateNudges(projectState, {
    nudge_threshold_days: (config.frx || {}).nudge_threshold_days || 14,
    max_nudges: (config.frx || {}).max_nudges || 3,
    user_role: userRole
  });

  const health = calculateHealthScore(projectState);

  // Coaching trigger: detect concepts that may need teaching
  // Uses learner_lens (unified store) — loaded by caller, passed via _learnerLens
  const workspaceKL = projectState._workspaceKL || [];
  const learnerLens = projectState._learnerLens || null;
  const coaching = annotateWithCoaching(result.narration, projectState, workspaceKL, learnerLens);
  // Store updated learnerLens back for caller to persist
  if (coaching.learnerLens) projectState._learnerLens = coaching.learnerLens;

  return {
    source: 'convergence_chain',
    status: 'ok',
    convergence_chain: {
      query_type: queryType,
      title: result.title,
      narration: coaching.narration,
      data: result.data,
      health_score: health.score,
      health_label: health.label,
      nudges: nudges.length > 0 ? nudges : undefined,
      coaching_signals: coaching.coaching_signals.length > 0 ? coaching.coaching_signals : undefined,
      coaching_packets: coaching.coaching_packets?.length > 0 ? coaching.coaching_packets : undefined
    },
    action_brief_markdown: coaching.narration,
    mode: 'converge',
    convergence_score: 100,
    convergence_gaps: [],
    suggested_questions: getSuggestedFollowUps(queryType)
  };
}

function getSuggestedFollowUps(queryType) {
  const followUps = {
    status: ['What\'s blocking us?', 'What should I do next?', 'Show me the decisions.'],
    blockers: ['What should I do next?', 'Show me the facts.', 'What decisions are pending?'],
    next_action: ['How are we doing overall?', 'What\'s blocking us?', 'Show me the decisions.'],
    what_changed: ['How are we doing?', 'What\'s blocking us?', 'What should I do next?'],
    known_facts: ['What\'s missing?', 'What decisions are open?', 'How are we doing?'],
    decisions: ['What\'s blocking us?', 'What should I do next?', 'How are we doing?']
  };
  return followUps[queryType] || ['How are we doing?', 'What\'s blocking us?', 'What should I do next?'];
}

/**
 * Calculate health score from actual project state composition.
 *
 * Formula:
 *   Base: 100
 *   - 8 per critical unresolved evidence gap
 *   - 4 per moderate unresolved evidence gap
 *   - 2 per low unresolved evidence gap
 *   - 5 per open decision with unresolved blockers
 *   - 2 per open decision without blockers (pending human choice)
 *   - 3 per blocked action
 *   + 1 per known fact (capped at +10)
 *   + 2 per resolved decision (capped at +10)
 *   Floor: 0, Ceiling: 100
 *
 * @param {object} projectState - Full project state object
 * @returns {{ score: number, label: string }}
 */
export function calculateHealthScore(projectState) {
  const ps = projectState.project_state || projectState;
  const target = ps.target_score || 95;

  let score = 100;

  const unresolved = (ps.missing_evidence || []).filter(m => m.status !== 'resolved');
  for (const me of unresolved) {
    if (me.priority === 'critical') score -= 8;
    else if (me.priority === 'moderate') score -= 4;
    else score -= 2;
  }

  for (const od of (ps.open_decisions || []).filter(d => d.status !== 'resolved')) {
    if (od.blocked_by && od.blocked_by.length > 0) score -= 5;
    else score -= 2;
  }

  score -= (ps.blocked_actions || []).length * 3;

  score += Math.min(10, (ps.known_facts || []).length);
  score += Math.min(10, (ps.resolved_decisions || []).length * 2);

  score = Math.max(0, Math.min(100, score));

  let label;
  if (score >= target) label = 'ON TRACK';
  else if (score >= 70) label = 'CONDITIONAL FAIL';
  else label = 'NEEDS ATTENTION';

  return { score, label };
}

/**
 * Look up workspace-specific knowledge library entries by matching query text against tags and questions.
 *
 * @param {Array} knowledgeLibrary - Array of KL entries from workspace
 * @param {string} queryText - The user's query text
 * @param {number} maxResults - Maximum entries to return
 * @returns {Array} - Matched KL entries, ranked by relevance
 */
export function lookupWorkspaceKnowledge(knowledgeLibrary, queryText, maxResults = 5) {
  if (!knowledgeLibrary || knowledgeLibrary.length === 0 || !queryText) return [];

  const words = queryText.toLowerCase().split(/\s+/).filter(w => w.length > 2);
  const scored = [];

  for (const entry of knowledgeLibrary) {
    let score = 0;
    const questionLower = (entry.question || '').toLowerCase();
    const tagsLower = (entry.tags || []).map(t => t.toLowerCase());
    const answerLower = (entry.answer || '').toLowerCase().slice(0, 500);

    for (const word of words) {
      if (questionLower.includes(word)) score += 3;
      if (tagsLower.some(t => t.includes(word) || word.includes(t))) score += 2;
      if (answerLower.includes(word)) score += 1;
    }

    if (score > 0) scored.push({ entry, score });
  }

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, maxResults).map(s => s.entry);
}

/**
 * Persist an updated project state to disk.
 *
 * @param {string} workspacesDir - Path to workspaces/ directory
 * @param {string} workspaceId - Workspace ID
 * @param {object} updatedState - The full state object to save
 * @returns {boolean} - Success or failure
 */
export function updateProjectState(workspacesDir, workspaceId, updatedState) {
  if (!workspaceId || !/^[a-z0-9_-]+$/i.test(workspaceId)) return false;

  const statePath = `${workspacesDir}/${workspaceId}/project_state.yaml`;

  try {
    const valid = validateProjectState(updatedState);
    if (!valid) {
      console.error('Validation failed for project state update:', validateProjectState.errors);
      // We still try to save if it's not a total disaster, or we could strict-fail.
      // For now, let's log and proceed but maybe Phase 8 should be stricter.
    }

    const yaml = dumpYAML(updatedState, {
      indent: 2,
      lineWidth: -1, // don't wrap long strings
      noRefs: true
    });

    writeFileSync(statePath, yaml, 'utf-8');
    return true;
  } catch (e) {
    console.error(`Error saving project state to ${statePath}:`, e.message);
    return false;
  }
}

// ── Daily Brief Generator ──
// Produces a voice-first daily brief artifact from project state.
// Follows 10 voice UX rules from Perplexity research (GAP 5):
//   - Rule of Three (max 3 items per spoken list)
//   - Lead with delta, not absolute
//   - Speak company names, not tickers
//   - Round aggressively in speech
//   - End every brief with a choice

const PRIORITY_ORDER = { critical: 0, moderate: 1, low: 2 };

export function generateDailyBrief(projectState, config = {}) {
  const ps = projectState.project_state || projectState;
  const now = getISODate();
  const userName = config.user_name || 'there';

  const domain = config.domain || 'general';

  const sections = [];

  // ── Section 1: Health & Objective (always first) ──
  const healthCalc = calculateHealthScore(projectState);
  const health = healthCalc.score;
  const label = healthCalc.label;
  const target = ps.target_score || 95;
  const objective = ps.objective || '';

  let healthLine = `Portfolio health: ${health} out of 100`;
  if (health < target) {
    healthLine += ` — ${target - health} points below your target of ${target}`;
  }
  healthLine += `. Status: ${label}.`;

  sections.push({
    id: 'health_snapshot',
    title: 'HEALTH SNAPSHOT',
    voice: healthLine,
    detail: { health_score: health, health_label: label, target_score: target, objective }
  });

  // ── Section 2: Commodity Snapshot (extract price facts) ──
  const facts = ps.known_facts || [];
  const priceFacts = facts.filter(f =>
    /\$/i.test(f.fact) && /(wti|brent|henry hub|crack spread|propane)/i.test(f.fact)
  );

  if (priceFacts.length > 0) {
    // Voice: top 3 price facts, rounded
    const voiceItems = priceFacts.slice(0, 3).map(f => {
      // Extract the key number and context
      const match = f.fact.match(/\$[\d,.]+/);
      const price = match ? match[0] : '';
      // Shorten the fact for voice
      const shortFact = f.fact.split('—')[0].trim();
      return shortFact;
    });

    let voice = voiceItems.join('. ') + '.';
    if (priceFacts.length > 3) {
      voice += ` Plus ${priceFacts.length - 3} more data points — want the full list?`;
    }

    sections.push({
      id: 'commodity_snapshot',
      title: 'COMMODITY SNAPSHOT',
      voice,
      detail: { facts: priceFacts.map(f => ({ id: f.id, fact: f.fact, source: f.source })) }
    });
  }

  // ── Section 3: Top Blockers (critical missing evidence) ──
  const unresolved = (ps.missing_evidence || []).filter(m => m.status !== 'resolved');
  const criticals = unresolved.filter(m => m.priority === 'critical');
  const moderates = unresolved.filter(m => m.priority === 'moderate');

  if (criticals.length > 0) {
    const top3 = criticals.slice(0, 3);
    const voiceItems = top3.map(m => m.what);
    let voice = `You have ${criticals.length} critical gap${criticals.length > 1 ? 's' : ''} blocking progress. `;
    voice += `Top ${Math.min(3, criticals.length)}: ${voiceItems.join('; ')}.`;
    if (moderates.length > 0) {
      voice += ` Plus ${moderates.length} moderate gap${moderates.length > 1 ? 's' : ''}.`;
    }

    sections.push({
      id: 'top_blockers',
      title: 'TOP BLOCKERS',
      voice,
      detail: {
        critical: criticals.map(m => ({ id: m.id, what: m.what, who_resolves: m.who_resolves, unblocks: m.unblocks })),
        moderate: moderates.map(m => ({ id: m.id, what: m.what }))
      }
    });
  }

  // ── Section 4: Open Decisions ──
  const openDecisions = (ps.open_decisions || []).filter(d => d.status !== 'resolved');
  if (openDecisions.length > 0) {
    const blocked = openDecisions.filter(d => d.blocked_by && d.blocked_by.length > 0);
    const ready = openDecisions.filter(d => !d.blocked_by || d.blocked_by.length === 0);

    let voice = `${openDecisions.length} open decision${openDecisions.length > 1 ? 's' : ''}. `;
    if (ready.length > 0) {
      const top = ready.slice(0, 2);
      voice += `${ready.length} ready for your call: ${top.map(d => d.decision.split('?')[0].trim()).join('; ')}.`;
      if (ready.length > 2) voice += ` Plus ${ready.length - 2} more.`;
    }
    if (blocked.length > 0) {
      voice += ` ${blocked.length} blocked — waiting on evidence.`;
    }

    sections.push({
      id: 'open_decisions',
      title: 'OPEN DECISIONS',
      voice,
      detail: {
        ready: ready.map(d => ({ id: d.id, decision: d.decision, options: d.options, impact: d.impact })),
        blocked: blocked.map(d => ({ id: d.id, decision: d.decision, blocked_by: d.blocked_by }))
      }
    });
  }

  // ── Section 5: Blocked Actions ──
  const blockedActions = ps.blocked_actions || [];
  if (blockedActions.length > 0) {
    const top3 = blockedActions.slice(0, 3);
    let voice = `${blockedActions.length} action${blockedActions.length > 1 ? 's' : ''} blocked: `;
    voice += top3.map(ba => ba.action).join('; ') + '.';

    sections.push({
      id: 'blocked_actions',
      title: 'BLOCKED ACTIONS',
      voice,
      detail: blockedActions.map(ba => ({ id: ba.id, action: ba.action, blocked_by: ba.blocked_by, impact: ba.impact }))
    });
  }

  // ── Section 6: Proactive Flags (known unknowns, top 3) ──
  const unknowns = ps.known_unknowns || [];
  if (unknowns.length > 0) {
    const top3 = unknowns.slice(0, 3);
    let voice = `${unknowns.length} risk factor${unknowns.length > 1 ? 's' : ''} on your radar. Top three: `;
    voice += top3.join('; ') + '.';
    if (unknowns.length > 3) {
      voice += ` Plus ${unknowns.length - 3} more.`;
    }

    sections.push({
      id: 'proactive_flags',
      title: 'PROACTIVE FLAGS',
      voice,
      detail: unknowns
    });
  }

  // ── Section 7: Resolved Since Last Brief ──
  const resolved = ps.resolved_decisions || [];
  if (resolved.length > 0) {
    const recent = resolved.filter(r => r.resolved_at >= (config.last_brief_date || '2000-01-01'));
    if (recent.length > 0) {
      const voice = `${recent.length} decision${recent.length > 1 ? 's' : ''} resolved: ${recent.slice(0, 3).map(r => r.decision).join('; ')}.`;
      sections.push({
        id: 'recently_resolved',
        title: 'RECENTLY RESOLVED',
        voice,
        detail: recent
      });
    }
  }

  // ── Closing: Always end with a choice ──
  const closingChoices = [];
  if (openDecisions.some(d => !d.blocked_by || d.blocked_by.length === 0)) {
    closingChoices.push('tackle an open decision');
  }
  if (criticals.length > 0) {
    closingChoices.push('resolve a critical gap');
  }
  closingChoices.push('dig into the numbers');

  const closingVoice = `What would you like to do? ${closingChoices.slice(0, 3).join(', ')}?`;

  // ── Compose full brief ──
  const fullVoice = sections.map(s => s.voice).join('\n\n') + '\n\n' + closingVoice;

  // Markdown version for artifact file
  const markdown = composeBriefMarkdown(sections, {
    userName, now, objective, closingVoice,
    health, label, target
  });

  return {
    generated_at: now,
    artifact_type: 'daily_brief',
    sections,
    closing: { voice: closingVoice, choices: closingChoices },
    voice_script: fullVoice,
    markdown,
    meta: {
      total_facts: facts.length,
      critical_gaps: criticals.length,
      moderate_gaps: moderates.length,
      open_decisions: openDecisions.length,
      blocked_actions: blockedActions.length,
      known_unknowns: unknowns.length
    }
  };
}

function composeBriefMarkdown(sections, ctx) {
  const lines = [];
  lines.push(`# Daily Brief — ${ctx.now}`);
  lines.push(`**${ctx.userName}** | Health: ${ctx.health}/${ctx.target} (${ctx.label})`);
  if (ctx.objective) lines.push(`> ${ctx.objective}`);
  lines.push('');

  for (const section of sections) {
    lines.push(`## ${section.title}`);
    lines.push(section.voice);

    // Add structured detail for non-voice consumption
    if (section.id === 'commodity_snapshot' && section.detail.facts) {
      lines.push('');
      for (const f of section.detail.facts) {
        lines.push(`- **${f.id}**: ${f.fact} _(${f.source})_`);
      }
    }
    if (section.id === 'top_blockers' && section.detail.critical) {
      lines.push('');
      for (const m of section.detail.critical) {
        lines.push(`- **${m.id}** [CRITICAL]: ${m.what} → unblocks: ${(m.unblocks || []).join(', ')}`);
      }
    }
    if (section.id === 'open_decisions') {
      if (section.detail.ready?.length) {
        lines.push('');
        lines.push('**Ready for decision:**');
        for (const d of section.detail.ready) {
          lines.push(`- **${d.id}**: ${d.decision}`);
          if (d.options?.length) {
            for (const opt of d.options) lines.push(`  - ${opt}`);
          }
        }
      }
    }
    lines.push('');
  }

  lines.push(`---`);
  lines.push(`*Generated ${ctx.now} by Mission Canvas convergence engine*`);

  return lines.join('\n');
}


// ── COACHING TRIGGER SYSTEM ──────────────────────────────────────────────────
// Contract between Canvas (execution) and Enablement (teaching).
// Canvas detects domain concepts during narration and checks learner state.
// Enablement methodology: expose → explain → verify → internalize.

/**
 * Detect domain concepts in text that may need coaching.
 * Returns concepts found with their IDs and context.
 */
export function detectCoachingOpportunities(text, workspaceKL) {
  if (!text || !workspaceKL || !workspaceKL.length) return [];

  const opportunities = [];
  const textLower = text.toLowerCase();

  for (const entry of workspaceKL) {
    const terms = extractKeyTerms(entry);
    for (const term of terms) {
      if (textLower.includes(term.toLowerCase())) {
        opportunities.push({
          concept_id: entry.id,
          term,
          question: entry.question || entry.title || term,
          source_entry: entry.id
        });
        break; // one match per KL entry is enough
      }
    }
  }

  return opportunities;
}

function extractKeyTerms(klEntry) {
  const terms = [];
  // Pull key phrases from the KL entry question/title
  const text = (klEntry.question || klEntry.title || '').toLowerCase();
  // Extract noun phrases >3 chars that aren't stop words
  const stops = new Set(['what','how','when','where','which','does','should','could','would','about','between','their','there','this','that','with','from','have','been','will','more','than','into','also','each','they','your','most','some']);
  const words = text.replace(/[^a-z0-9\s-]/g, '').split(/\s+/).filter(w => w.length > 3 && !stops.has(w));
  // Use bigrams as terms (more specific than single words)
  for (let i = 0; i < words.length - 1; i++) {
    terms.push(words[i] + ' ' + words[i + 1]);
  }
  // Also add individual distinctive words
  for (const w of words) {
    if (w.length > 5) terms.push(w);
  }
  return [...new Set(terms)];
}

/**
 * Check learner state for a concept — returns coaching depth.
 * Depth: 'full' (first encounter), 'brief' (seen before), 'none' (mastered).
 * Reads from learner_lens concept_progress (unified store).
 */
export function getCoachingDepth(conceptId, learnerLens) {
  if (!learnerLens) return 'full';
  const state = learnerLens.learner_lens?.state;
  if (!state) return 'full';
  // Check verified concepts list first
  if (Array.isArray(state.verified_concepts) && state.verified_concepts.includes(conceptId)) return 'none';
  // Check concept_progress for exposure count (times_taught maps to exposures)
  const progress = (state.concept_progress || []).find(p => p.concept_id === conceptId);
  if (!progress) return 'full';
  const exposures = progress.times_taught || 0;
  if (exposures >= 3) return 'none';
  if (exposures >= 1) return 'brief';
  return 'full';
}

/**
 * Record that a concept was shown to the learner.
 * Writes to learner_lens concept_progress (unified store).
 */
export function recordConceptExposure(conceptId, learnerLens) {
  if (!learnerLens || !learnerLens.learner_lens) return;
  const state = learnerLens.learner_lens.state;
  if (!state) return;
  if (!Array.isArray(state.concept_progress)) state.concept_progress = [];
  if (!Array.isArray(state.taught_concepts)) state.taught_concepts = [];
  const existing = state.concept_progress.find(p => p.concept_id === conceptId);
  if (existing) {
    existing.times_taught = (existing.times_taught || 0) + 1;
    existing.last_taught_at = getISODate();
  } else {
    state.concept_progress.push({
      concept_id: conceptId,
      concept_label: conceptId,
      source_type: 'chain_narration',
      stage: 'orient',
      times_taught: 1,
      last_taught_at: getISODate()
    });
  }
  if (!state.taught_concepts.includes(conceptId)) {
    state.taught_concepts.push(conceptId);
  }
}

/**
 * Generate coaching annotations for a narration.
 * Detects domain concepts, checks learner state, injects one inline hint
 * for the most important new concept, and returns coaching_signals for UI.
 * Only one 💡 hint per narration to avoid clutter.
 * Signals capped at 5 to keep response size reasonable.
 *
 * Uses learner_lens.yaml (unified store) via cache-on-load:
 *   - learnerLens is passed in from the caller (cached at workspace load time)
 *   - mutations are written back; caller persists to disk only when signals fire
 */
export function annotateWithCoaching(narration, projectState, workspaceKL, learnerLens) {
  const opportunities = detectCoachingOpportunities(narration, workspaceKL || []);
  // If no learnerLens provided, create a minimal in-memory one (backward compat)
  if (!learnerLens || !learnerLens.learner_lens) {
    learnerLens = { learner_lens: { identity: {}, goals: [], state: { taught_concepts: [], verified_concepts: [], concept_progress: [], stage_counts: { orient: 0, retain: 0, verify: 0 } }, teaching_moments: [] } };
  }

  const signals = [];
  let annotated = narration;

  for (const opp of opportunities) {
    const depth = getCoachingDepth(opp.concept_id, learnerLens);
    if (depth === 'none') continue;

    // Find the KL entry for this concept to get the answer
    const klEntry = (workspaceKL || []).find(e => e.id === opp.concept_id);
    const answer = klEntry ? (klEntry.answer || klEntry.answer_preview || '') : '';
    // Extract first sentence as a brief explanation
    const firstSentence = answer.split(/[.!?]\s/)[0];

    if (depth === 'full' && firstSentence && !annotated.includes(`💡`)) {
      // First encounter: add a coaching block after the first mention
      const hint = `\n\n💡 **${opp.term}**: ${firstSentence}.\n`;
      // Insert after the line containing the term
      const lines = annotated.split('\n');
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].toLowerCase().includes(opp.term.toLowerCase())) {
          lines.splice(i + 1, 0, hint);
          annotated = lines.join('\n');
          break;
        }
      }
    }

    signals.push({
      concept_id: opp.concept_id,
      term: opp.term,
      depth,
      question: opp.question,
      detected_at: getISODate(),
      ...(depth === 'full' && firstSentence ? { explanation: firstSentence } : {})
    });

    recordConceptExposure(opp.concept_id, learnerLens);
  }

  // Wire-format coaching packets (Phase 1: universal protocol)
  const traceId = projectState?.project_state?.id || 'unknown';
  const coaching_packets = signals.map(s => ({
    id: `cm-${s.concept_id}-${Date.now()}`,
    from: 'enablement.coaching',
    to: 'ux.workspace',
    task: 'teach_concept',
    riu_ids: [],
    payload: s,
    trace_id: traceId
  }));

  return { narration: annotated, coaching_signals: signals.slice(0, 5), coaching_packets: coaching_packets.slice(0, 5), learnerLens };
}
