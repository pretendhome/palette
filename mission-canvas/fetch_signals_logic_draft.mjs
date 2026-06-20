/**
 * fetch_signals Implementation (Draft v2 - Production Ready)
 * Purpose: Securely extract business signals with Tier 1 PII scrubbing.
 * Compliant with: RIU-081, RIU-011, and Crew Feedback (2026-03-29).
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const ALLOW_LIST_DIRS = [
  "/home/mical/fde/implementations/retail/retail-rossi-store/",
  "/home/mical/fde/implementations/retail/retail-rossi-store/data/"
];

const ALLOWED_EXTENSIONS = ['.pdf', '.csv', '.json', '.txt', '.md'];

// --- Helper: Path Validation ---
function validatePath(filePath) {
  // 1. Resolve realpath (Resolves symlinks + ..)
  let resolvedPath;
  try {
    resolvedPath = fs.realpathSync(filePath);
  } catch (err) {
    throw new Error(`FILE_NOT_FOUND: ${filePath}`);
  }

  // 2. Check Allowlist
  const isAllowed = ALLOW_LIST_DIRS.some(dir => resolvedPath.startsWith(path.resolve(dir)));
  if (!isAllowed) throw new Error("ACCESS_DENIED: Path outside allowlist (Symlink Bypass Blocked).");

  // 3. Reject Dotfiles in any part of the path
  const parts = resolvedPath.split(path.sep);
  if (parts.some(part => part.startsWith('.'))) throw new Error("ACCESS_DENIED: Dotfiles restricted.");

  // 4. Reject Directories
  if (fs.statSync(resolvedPath).isDirectory()) throw new Error("ACCESS_DENIED: Cannot parse directories.");

  // 5. Check Extension
  if (!ALLOWED_EXTENSIONS.includes(path.extname(resolvedPath))) throw new Error("ACCESS_DENIED: Invalid file type.");

  return resolvedPath;
}

// --- Helper: PII Generalization ---
function generalizeRevenue(amount) {
  const num = parseFloat(amount.replace(/[^0-9.]/g, ''));
  if (isNaN(num)) return "[UNKNOWN_REVENUE]";
  if (num < 25000) return "$0-25k";
  if (num < 50000) return "$25-50k";
  if (num < 100000) return "$50-100k";
  if (num < 250000) return "$100-250k";
  return "$250k+";
}

function generalizeHeadcount(count) {
  const num = parseInt(count, 10);
  if (isNaN(num)) return "[UNKNOWN_HEADCOUNT]";
  if (num <= 5) return "1-5";
  if (num <= 20) return "6-20";
  if (num <= 50) return "21-50";
  return "50+";
}

// --- Helper: Tier 1 PII Scrubbing ---
function scrubPII(rawText) {
  let scrubbed = rawText;
  
  // 1. STRIP (Immediate removal)
  scrubbed = scrubbed.replace(/[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g, '[STRIPPED_EMAIL]');
  scrubbed = scrubbed.replace(/\b\d{3}-\d{2}-\d{4}\b/g, '[STRIPPED_SSN]');
  scrubbed = scrubbed.replace(/\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g, '[STRIPPED_PHONE]');
  scrubbed = scrubbed.replace(/\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b/g, '[STRIPPED_CC]');
  // Bank account/routing: labeled fields only (avoids over-stripping arbitrary numbers)
  scrubbed = scrubbed.replace(/(Account|Routing|Bank)[#:\s]+\d{6,17}/gi, '$1 [STRIPPED_ACCOUNT]');
  // DOB patterns
  scrubbed = scrubbed.replace(/(DOB|Date of Birth|Birth ?Date|Born)[:\s]+\d{1,4}[-/]\d{1,2}[-/]\d{1,4}/gi, '$1: [STRIPPED_DOB]');
  // Names (Strip fields labeled name/owner/contact/applicant)
  scrubbed = scrubbed.replace(/(Name|Owner|Contact|Applicant|Person)[:\s]+[A-Z][a-z]+(\s+[A-Z][a-z]+)?/gi, '$1: [STRIPPED_NAME]');
  // Addresses (Simple pattern for number + street)
  scrubbed = scrubbed.replace(/\d+\s+[A-Z][a-z]+\s+(St|Ave|Rd|Blvd|Lane|Way|Dr|Ct|Pl|Circle)/g, '[STRIPPED_ADDRESS]');
  
  // 2. GENERALIZE
  scrubbed = scrubbed.replace(/(Total Income|Revenue|Gross Sales)[:\s]+\$?([0-9,.]+)/gi, (m, p1, p2) => `${p1}: ${generalizeRevenue(p2)}`);
  scrubbed = scrubbed.replace(/(Employee Count|Headcount|Staff)[:\s]+([0-9]+)/gi, (m, p1, p2) => `${p1}: ${generalizeHeadcount(p2)}`);

  return scrubbed;
}

// --- Core: File Parsing ---
async function parseFile(resolvedPath) {
  const ext = path.extname(resolvedPath);
  
  if (ext === '.pdf') {
    try {
      // Use system pdftotext with 10s timeout (DoS protection)
      // execFileSync avoids shell — prevents command injection via filenames
      const buffer = execFileSync('pdftotext', [resolvedPath, '-'], { timeout: 10000 });
      return buffer.toString('utf-8');
    } catch (err) {
      throw new Error(`PDF_PARSE_FAILED: ${err.message}`);
    }
  }

  if (ALLOWED_EXTENSIONS.includes(ext)) {
    return fs.readFileSync(resolvedPath, 'utf-8');
  }

  throw new Error("UNSUPPORTED_FORMAT");
}

// --- Logging ---
function logAccess(filePath, result) {
  const logEntry = `[${new Date().toISOString()}] ACCESS: ${filePath} | RESULT: ${result}\n`;
  fs.appendFileSync(path.join(path.dirname(fileURLToPath(import.meta.url)), 'file_access.log'), logEntry);
}

// --- Exported Function ---
export async function fetchSignals(filePath) {
  let validatedPath;
  try {
    validatedPath = validatePath(filePath);
    const rawContent = await parseFile(validatedPath);
    const scrubbedContent = scrubPII(rawContent);
    
    logAccess(validatedPath, "SUCCESS");

    // Kiro's Signal Schema - Expanded
    const signals = [];
    const text = scrubbedContent;

    // 1. Revenue
    if (text.includes("Total Income") || text.includes("Revenue")) {
      const match = text.match(/(Total Income|Revenue): (\$[0-9k+-]+)/);
      signals.push({ type: "revenue_bracket", value: match ? match[2] : "[DETECTED]", source_file: path.basename(validatedPath) });
    }
    // 2. Industry
    if (text.match(/Retail|Specialized|Shop|NAICS/i)) {
      signals.push({ type: "industry", value: "Retail", source_file: path.basename(validatedPath) });
    }
    // 3. Business Structure (PASS THROUGH)
    if (text.match(/LLC|Corp|Inc\.|Sole Prop/i)) {
      const match = text.match(/(LLC|Corp|Inc\.|Sole Prop)/i);
      signals.push({ type: "business_structure", value: match[0], source_file: path.basename(validatedPath) });
    }
    // 4. Grant Eligibility (PASS THROUGH)
    if (text.match(/Grant|Funding|SBA|Underwriter/i)) {
      signals.push({ type: "grant_eligible", value: true, source_file: path.basename(validatedPath) });
    }
    // 5. Growth Indicators
    if (text.match(/Expansion|New Location|Growth|Scale/i)) {
      signals.push({ type: "growth_indicator", value: "Positive", source_file: path.basename(validatedPath) });
    }

    return {
      signals,
      summary: `Extracted ${signals.length} signals (Structure, Revenue, Industry, Grants) from ${path.basename(validatedPath)}. PII Scrubbed.`,
      files_accessed: [path.basename(validatedPath)],
      pii_scrubbed: true
    };

  } catch (err) {
    logAccess(filePath, `FAILED: ${err.message}`);
    throw err;
  }
}
