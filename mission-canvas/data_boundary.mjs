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
