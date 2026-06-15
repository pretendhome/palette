// data_boundary.mjs — Hard PII enforcement for Mission Canvas
// Classification: TIER 1 (IMMUTABLE)
// This module validates ALL text before it enters workspace state.
// Import and call validateText() before any write to project_state.yaml.

// ── PII Detection Patterns ──────────────────────────────────────────────────

const PII_PATTERNS = [
  // SSN
  { name: 'ssn', pattern: /\b\d{3}-\d{2}-\d{4}\b/g, severity: 'critical' },
  // Credit card (13-19 digits, with optional separators)
  { name: 'credit_card', pattern: /\b(?:\d[ -]*?){13,19}\b/g, severity: 'critical' },
  // Email
  { name: 'email', pattern: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, severity: 'high' },
  // Phone (US/UK formats)
  { name: 'phone', pattern: /\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b/g, severity: 'high' },
  { name: 'phone_uk', pattern: /\b(?:\+?44[-.\s]?)?\d{4}[-.\s]?\d{6}\b/g, severity: 'high' },
  // Street address (number + street name)
  { name: 'street_address', pattern: /\b\d{1,5}\s+(?:North|South|East|West|N\.?|S\.?|E\.?|W\.?)?\s*\w+\s+(?:Street|St\.?|Avenue|Ave\.?|Boulevard|Blvd\.?|Drive|Dr\.?|Lane|Ln\.?|Road|Rd\.?|Court|Ct\.?|Place|Pl\.?|Way|Circle|Cir\.?)\b/gi, severity: 'high' },
  // Bank account / routing (9-digit routing, 8-17 digit account)
  { name: 'routing_number', pattern: /\brouting[:\s#]*\d{9}\b/gi, severity: 'critical' },
  { name: 'account_number', pattern: /\baccount[:\s#]*\d{8,17}\b/gi, severity: 'critical' },
  // Passport
  { name: 'passport', pattern: /\bpassport[:\s#]*[A-Z0-9]{6,12}\b/gi, severity: 'critical' },
  // Tax ID / EIN
  { name: 'tax_id', pattern: /\b\d{2}-\d{7}\b/g, severity: 'critical' },
  // Date of birth patterns
  { name: 'dob', pattern: /\b(?:dob|date of birth|born)[:\s]*\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}\b/gi, severity: 'high' },
  // Exact large dollar amounts (more than $9,999 — force ranges instead)
  { name: 'exact_dollar_large', pattern: /\$\d{1,3}(?:,\d{3}){1,4}(?:\.\d{2})?\b/g, severity: 'medium' },
  { name: 'exact_dollar_large_plain', pattern: /\b\d{5,12}\s*(?:dollars|usd)\b/gi, severity: 'medium' },
  // Local file paths (user's machine)
  { name: 'file_path_unix', pattern: /(?:\/(?:home|Users|root)\/[^\s,;'"]+)/g, severity: 'medium' },
  { name: 'file_path_windows', pattern: /[A-Z]:\\(?:Users|Documents|Desktop)\\[^\s,;'"]+/g, severity: 'medium' },
];

const BLOCK_SIGNALS = [
  'privileged',
  'confidential',
  'secret',
  'nda',
  'trade secret',
  'proprietary',
  'internal only',
  'off the record',
  'not for sharing',
  'client',
  'patient',
  'matter',
];

const EXTERNAL_REDACTION_PATTERNS = [
  ...PII_PATTERNS,
  { name: 'medical_record', pattern: /\b(?:MRN|medical record)[#:\s]*\d{6,12}\b/gi, severity: 'critical' },
  { name: 'case_number', pattern: /\b\d{1,2}[-:]\w{2,4}[-:]\d{4,8}\b/g, severity: 'high' },
  { name: 'client_reference', pattern: /\b(?:client|patient|matter|case|file|docket)\s*(?:#|number|no\.?|:)\s*\S+\b/gi, severity: 'high' },
  { name: 'titled_person_name', pattern: /\b(?:Mr|Mrs|Ms|Dr|Prof|Judge|Justice|Attorney|Counsel|Director|CEO|CFO|CTO)\.\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}\b/g, severity: 'high' },
];

// ── Validation ──────────────────────────────────────────────────────────────

/**
 * Validate text for PII. Returns { ok, violations } where violations is an
 * array of { name, severity, matches }.
 *
 * @param {string} text - Text to validate
 * @param {object} options
 * @param {boolean} options.allowDollarAmounts - Allow exact dollar amounts (for market data)
 * @param {boolean} options.allowFilePaths - Allow file paths (should be false for VPS)
 * @param {string} options.context - Where this text is going ('vps', 'local', 'log')
 */
export function validateText(text, options = {}) {
  if (!text || typeof text !== 'string') return { ok: true, violations: [] };

  const context = options.context || 'vps';
  const allowDollars = options.allowDollarAmounts || false;
  const allowPaths = options.allowFilePaths || false;

  const violations = [];

  for (const rule of PII_PATTERNS) {
    // Skip dollar amount check if allowed (for market data facts)
    if (allowDollars && (rule.name === 'exact_dollar_large' || rule.name === 'exact_dollar_large_plain')) {
      continue;
    }
    // Skip file path check if allowed (for local-only context)
    if (allowPaths && (rule.name === 'file_path_unix' || rule.name === 'file_path_windows')) {
      continue;
    }

    const matches = text.match(rule.pattern);
    if (matches) {
      violations.push({
        name: rule.name,
        severity: rule.severity,
        count: matches.length,
        // Redact the actual matches in the violation report
        samples: matches.slice(0, 2).map(m => m.slice(0, 4) + '***'),
      });
    }
  }

  const hasCritical = violations.some(v => v.severity === 'critical');
  const hasHigh = violations.some(v => v.severity === 'high');

  return {
    ok: violations.length === 0,
    blocked: hasCritical || hasHigh,
    violations,
    summary: violations.length === 0
      ? 'clean'
      : `${violations.length} PII pattern(s) detected: ${violations.map(v => v.name).join(', ')}`,
  };
}


function hasBlockSignal(text) {
  const lower = String(text || '').toLowerCase();
  return BLOCK_SIGNALS.find((signal) => {
    if (signal.includes(' ')) return lower.includes(signal);
    return new RegExp(`\\b${signal.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'i').test(lower);
  }) || null;
}

/**
 * Sanitize text before it leaves the machine for an external model/API.
 * Critical block signals stop the outbound call; PII patterns are redacted.
 */
export function sanitizeForExternal(text, options = {}) {
  if (!text || typeof text !== 'string') {
    return { ok: true, blocked: false, text, redactions: [], reason: null };
  }

  if (options.classification?.blocks_external) {
    return {
      ok: false,
      blocked: true,
      text: '',
      redactions: [],
      reason: 'classification_blocks_external',
    };
  }

  const signal = hasBlockSignal(text);
  if (signal) {
    return {
      ok: false,
      blocked: true,
      text: '',
      redactions: [],
      reason: `block_signal:${signal}`,
    };
  }

  let sanitized = text;
  const redactions = [];
  for (const rule of EXTERNAL_REDACTION_PATTERNS) {
    sanitized = sanitized.replace(rule.pattern, () => {
      redactions.push({ name: rule.name, severity: rule.severity });
      return `[REDACTED:${rule.name}]`;
    });
  }

  return {
    ok: true,
    blocked: false,
    text: sanitized,
    redactions,
    reason: redactions.length ? 'redacted' : null,
  };
}

/**
 * Recursively sanitize strings inside an outbound payload.
 */
export function sanitizePayloadForExternal(value, options = {}) {
  if (typeof value === 'string') {
    const result = sanitizeForExternal(value, options);
    return { ...result, value: result.text };
  }
  if (Array.isArray(value)) {
    const out = [];
    const redactions = [];
    for (const item of value) {
      const result = sanitizePayloadForExternal(item, options);
      if (result.blocked) return result;
      out.push(result.value);
      redactions.push(...result.redactions);
    }
    return { ok: true, blocked: false, value: out, text: out, redactions, reason: redactions.length ? 'redacted' : null };
  }
  if (value && typeof value === 'object') {
    const out = {};
    const redactions = [];
    for (const [key, item] of Object.entries(value)) {
      const result = sanitizePayloadForExternal(item, options);
      if (result.blocked) return result;
      out[key] = result.value;
      redactions.push(...result.redactions);
    }
    return { ok: true, blocked: false, value: out, text: out, redactions, reason: redactions.length ? 'redacted' : null };
  }
  return { ok: true, blocked: false, value, text: value, redactions: [], reason: null };
}

/**
 * Scrub PII from text — replaces matches with [REDACTED].
 * Use this for logging, NOT for user-facing responses (tell the user to rephrase instead).
 */
export function scrubText(text) {
  if (!text || typeof text !== 'string') return text;
  let scrubbed = text;
  for (const rule of PII_PATTERNS) {
    scrubbed = scrubbed.replace(rule.pattern, `[REDACTED:${rule.name}]`);
  }
  return scrubbed;
}

/**
 * Validate a fact before it enters the workspace.
 * Returns { ok, fact, error } — if not ok, the fact is blocked.
 * Dollar amounts in market data are ALLOWED (WTI at $97/bbl is public data).
 */
export function validateFact(fact, source) {
  // Market data sources get a pass on dollar amounts
  const isMarketData = /\b(eia|opec|fed|bloomberg|reuters|wsj|perplexity|market|bbl|barrel|spread|wti|brent|henry hub)\b/i.test(source || '');

  const result = validateText(fact, {
    context: 'vps',
    allowDollarAmounts: isMarketData,
    allowFilePaths: false,
  });

  if (result.blocked) {
    return {
      ok: false,
      error: `Blocked: ${result.summary}. Personal data cannot be stored on the server. Use ranges instead of exact amounts, and never include names, emails, phone numbers, or addresses.`,
      violations: result.violations,
    };
  }

  // Warn on medium severity but allow
  if (!result.ok) {
    return {
      ok: true,
      warning: result.summary,
      fact,
    };
  }

  return { ok: true, fact };
}

/**
 * Validate a workspace profile before storage.
 * Stricter than facts — no dollar amounts allowed at all.
 */
export function validateProfile(text) {
  return validateText(text, {
    context: 'vps',
    allowDollarAmounts: false,
    allowFilePaths: false,
  });
}
