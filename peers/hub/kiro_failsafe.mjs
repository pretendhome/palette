/**
 * Kiro Failsafe Agent — Error Recovery via Peers Bus
 * 
 * When the hub encounters an error it can't recover from, it broadcasts
 * to kiro.design via the peers bus. Next time Kiro is online, it picks
 * up the error, diagnoses it, and applies a fix.
 * 
 * This module provides:
 * 1. reportToKiro(error, context) — called from hub error handlers
 * 2. checkKiroResponses() — called at hub startup to apply pending fixes
 * 3. Error classification (transient vs structural vs config)
 */

import { readFile, writeFile, appendFile } from 'node:fs/promises';
import { join } from 'node:path';

const BUS_URL = process.env.PALETTE_BUS_URL || 'http://127.0.0.1:7899';
const KIRO_IDENTITY = 'kiro.design';
const HUB_IDENTITY = 'hub.voice';
const ERROR_LOG = join(import.meta.dirname || '.', '../../.palette/error_log.ndjson');

// ── Error Classification ────────────────────────────────────────────────────
const ERROR_CLASSES = {
  TRANSIENT: 'transient',       // Rate limits, timeouts, network blips — retry
  CONFIG: 'config',             // Missing key, wrong endpoint — needs human/kiro
  STRUCTURAL: 'structural',     // Code bug, schema mismatch — needs kiro
  PROVIDER: 'provider',         // Provider down, model unavailable — wait or switch
};

function classifyError(error, context) {
  const msg = (error?.message || error || '').toLowerCase();
  
  if (msg.includes('rate') || msg.includes('429') || msg.includes('timeout') || msg.includes('econnreset')) {
    return ERROR_CLASSES.TRANSIENT;
  }
  if (msg.includes('api_key') || msg.includes('unauthorized') || msg.includes('401') || msg.includes('403')) {
    return ERROR_CLASSES.CONFIG;
  }
  if (msg.includes('enoent') || msg.includes('spawn') || msg.includes('not found') || msg.includes('syntax')) {
    return ERROR_CLASSES.STRUCTURAL;
  }
  if (msg.includes('502') || msg.includes('503') || msg.includes('service unavailable')) {
    return ERROR_CLASSES.PROVIDER;
  }
  return ERROR_CLASSES.STRUCTURAL; // Default: assume needs intervention
}

// ── Circuit Breaker ─────────────────────────────────────────────────────────
// Don't spam the bus with the same error repeatedly
const recentErrors = new Map(); // key → { count, lastSent }
const COOLDOWN_MS = 60_000;     // Don't re-report same error within 1 min
const MAX_REPORTS = 5;          // Max 5 reports per error class per hour

function shouldReport(errorKey) {
  const now = Date.now();
  const entry = recentErrors.get(errorKey);
  
  if (!entry) {
    recentErrors.set(errorKey, { count: 1, lastSent: now, firstSeen: now });
    return true;
  }
  
  // Reset hourly
  if (now - entry.firstSeen > 3_600_000) {
    recentErrors.set(errorKey, { count: 1, lastSent: now, firstSeen: now });
    return true;
  }
  
  // Cooldown
  if (now - entry.lastSent < COOLDOWN_MS) return false;
  
  // Max reports
  if (entry.count >= MAX_REPORTS) return false;
  
  entry.count++;
  entry.lastSent = now;
  return true;
}

// ── Report to Kiro ──────────────────────────────────────────────────────────
export async function reportToKiro(error, context = {}) {
  const errorClass = classifyError(error, context);
  const errorMsg = error?.message || error?.toString() || String(error);
  const errorKey = `${errorClass}:${context.agent || 'unknown'}:${errorMsg.slice(0, 50)}`;
  
  // Don't report transient errors — just log them
  if (errorClass === ERROR_CLASSES.TRANSIENT) {
    await logError({ errorClass, errorMsg, context, action: 'ignored_transient' });
    return;
  }
  
  // Circuit breaker
  if (!shouldReport(errorKey)) {
    return;
  }
  
  // Log locally
  await logError({ errorClass, errorMsg, context, action: 'reported_to_kiro' });
  
  // Send to bus
  try {
    const message = {
      protocol_version: '1.0.0',
      message_id: crypto.randomUUID(),
      from_agent: HUB_IDENTITY,
      to_agent: KIRO_IDENTITY,
      message_type: 'advisory',
      intent: `FAILSAFE: ${errorClass} error in ${context.agent || 'hub'} — ${context.intent || 'unknown intent'}`,
      risk_level: errorClass === ERROR_CLASSES.STRUCTURAL ? 'medium' : 'low',
      requires_ack: errorClass === ERROR_CLASSES.STRUCTURAL,
      created_at: new Date().toISOString(),
      payload: {
        content: formatErrorReport(errorClass, errorMsg, context),
      },
    };
    
    const resp = await fetch(`${BUS_URL}/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(message),
    });
    
    if (!resp.ok) {
      console.error(`[kiro-failsafe] Bus send failed: ${resp.status}`);
    } else {
      console.log(`[kiro-failsafe] Reported ${errorClass} error to kiro.design`);
    }
  } catch (e) {
    // Bus is down — just log locally
    console.error(`[kiro-failsafe] Cannot reach bus: ${e.message}`);
  }
}

// ── Format Error Report ─────────────────────────────────────────────────────
function formatErrorReport(errorClass, errorMsg, context) {
  return `# Failsafe Error Report

**Class**: ${errorClass}
**Time**: ${new Date().toISOString()}
**Agent**: ${context.agent || 'unknown'}
**Intent**: ${context.intent || 'unknown'}
**Model**: ${context.model || 'unknown'}
**Provider**: ${context.provider || 'unknown'}

## Error
\`\`\`
${errorMsg}
\`\`\`

## Context
- Query: "${(context.query || '').slice(0, 100)}"
- Mode: ${context.mode || 'unknown'}
- Pipeline step: ${context.step || 'unknown'}

## Suggested Action
${getSuggestedAction(errorClass, errorMsg, context)}

## What Kiro Should Do
1. Read the error and context
2. Diagnose root cause
3. Apply fix (SSH to VPS, edit config, restart service)
4. Send ACK back on the bus confirming fix
`;
}

// ── Suggested Actions ───────────────────────────────────────────────────────
function getSuggestedAction(errorClass, errorMsg, context) {
  switch (errorClass) {
    case ERROR_CLASSES.CONFIG:
      return `Check API key for ${context.provider || 'provider'}. Verify .env file on VPS. Key may be expired or rate-limited.`;
    case ERROR_CLASSES.STRUCTURAL:
      if (errorMsg.includes('spawn')) return `Binary not found on VPS. Install the missing tool or fix the provider path.`;
      if (errorMsg.includes('syntax')) return `Code syntax error introduced. Check recent VPS patches. May need to revert.`;
      return `Structural issue. Check hub server.mjs on VPS for recent changes. May need code fix.`;
    case ERROR_CLASSES.PROVIDER:
      return `Provider ${context.provider || 'unknown'} appears down. Check status page. Consider routing to fallback model.`;
    default:
      return `Unknown error class. Manual investigation needed.`;
  }
}

// ── Local Error Log ─────────────────────────────────────────────────────────
async function logError(entry) {
  try {
    const line = JSON.stringify({ ...entry, timestamp: new Date().toISOString() }) + '\n';
    await appendFile(ERROR_LOG, line).catch(() => {});
  } catch {}
}

// ── Check for Kiro Responses (run at startup) ───────────────────────────────
export async function checkKiroResponses() {
  try {
    const resp = await fetch(`${BUS_URL}/fetch`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ identity: HUB_IDENTITY }),
    });
    if (!resp.ok) return;
    
    const data = await resp.json();
    const kiroMessages = (data.messages || []).filter(m => m.from_agent === KIRO_IDENTITY);
    
    if (kiroMessages.length > 0) {
      console.log(`[kiro-failsafe] ${kiroMessages.length} response(s) from kiro.design:`);
      for (const msg of kiroMessages) {
        console.log(`  → ${msg.intent}`);
        // Future: auto-apply fixes from Kiro responses
      }
    }
  } catch {
    // Bus not available at startup — that's fine
  }
}

// ── Auto-Recovery Attempts ──────────────────────────────────────────────────
// Before reporting to Kiro, try simple auto-recovery
export function attemptAutoRecovery(error, context) {
  const errorClass = classifyError(error, context);
  
  switch (errorClass) {
    case ERROR_CLASSES.TRANSIENT:
      // Retry with backoff — handled by caller
      return { action: 'retry', delay: 2000 };
      
    case ERROR_CLASSES.PROVIDER:
      // Try fallback model
      if (context.agent === 'perplexity' || context.agent === 'reasoning') {
        return { action: 'fallback', agent: 'mistral', reason: 'Perplexity unavailable, falling back to Mistral' };
      }
      if (context.agent === 'mistral') {
        return { action: 'fallback', agent: 'kimi', reason: 'Mistral unavailable, falling back to Groq' };
      }
      if (context.agent === 'claude') {
        return { action: 'fallback', agent: 'perplexity', reason: 'Claude unavailable, falling back to Perplexity' };
      }
      return { action: 'report', reason: 'No fallback available' };
      
    case ERROR_CLASSES.CONFIG:
    case ERROR_CLASSES.STRUCTURAL:
      // Can't auto-recover — report to Kiro
      return { action: 'report', reason: `${errorClass} error requires intervention` };
      
    default:
      return { action: 'report', reason: 'Unknown error' };
  }
}

export default { reportToKiro, checkKiroResponses, attemptAutoRecovery, classifyError, ERROR_CLASSES };
