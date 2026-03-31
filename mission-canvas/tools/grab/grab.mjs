#!/usr/bin/env node
/**
 * grab — fetch any URL and extract clean self-contained HTML
 *
 * Usage:
 *   node grab.mjs <url> [css-selector]
 *   node grab.mjs https://example.com
 *   node grab.mjs https://example.com "main .hero"
 *
 * Iterations:
 *   1. Basic fetch + clean HTML (strip scripts, tracking, cookie banners)
 *   2. CSS resolution and inlining (all styles in one block)
 *   3. Asset handling (images as absolute URLs or data URIs)
 *   4. Selector-scoped extraction (grab just a component)
 *   5. Quality pass (edge cases, error handling, size limits, tested)
 */

import { parse as parseHTML } from 'node-html-parser';
import { URL } from 'node:url';
import { writeFileSync } from 'node:fs';

const MAX_HTML_SIZE = 5 * 1024 * 1024; // 5MB
const FETCH_TIMEOUT = 15000;
const MAX_CSS_FETCHES = 20;
const MAX_CSS_TOTAL_SIZE = 500 * 1024; // 500KB max inlined CSS
const MAX_IMAGE_INLINE_SIZE = 100 * 1024; // 100KB for data URI inlining

// ── Iteration 1: Basic fetch + clean ──

const STRIP_TAGS = ['script', 'noscript', 'iframe', 'object', 'embed', 'applet'];
const STRIP_SELECTORS = [
  '[class*="cookie"]', '[id*="cookie"]',
  '[class*="consent"]', '[id*="consent"]',
  '[class*="gdpr"]', '[id*="gdpr"]',
  '[class*="tracking"]',
  '[class*="analytics"]',
  '[data-nosnippet]',
  '[aria-label*="cookie"]',
  '.cc-banner', '.cc-window',
  '#onetrust-banner-sdk',
  '.qc-cmp-ui-container',
];
const STRIP_ATTRS = ['onclick', 'onload', 'onerror', 'onmouseover', 'onfocus', 'onblur',
  'data-ga', 'data-analytics', 'data-track', 'data-gtm'];

async function fetchWithTimeout(url, timeout = FETCH_TIMEOUT) {
  // Use curl as fetcher for reliability across environments
  const { execSync } = await import('node:child_process');
  try {
    const text = execSync(
      `curl -sL --max-time ${Math.ceil(timeout/1000)} -H "User-Agent: Mozilla/5.0 (compatible; PaletteGrab/1.0)" ${JSON.stringify(url)}`,
      { encoding: 'utf-8', maxBuffer: MAX_HTML_SIZE, timeout }
    );
    if (text.length > MAX_HTML_SIZE) throw new Error(`Response too large: ${(text.length / 1024 / 1024).toFixed(1)}MB`);
    if (!text.trim()) throw new Error('Empty response');
    return text;
  } catch (err) {
    throw new Error(err.message || 'Fetch failed');
  }
}

function cleanHTML(root) {
  // Strip dangerous/unwanted tags
  for (const tag of STRIP_TAGS) {
    root.querySelectorAll(tag).forEach(el => el.remove());
  }
  // Strip cookie/consent/tracking elements
  for (const sel of STRIP_SELECTORS) {
    try { root.querySelectorAll(sel).forEach(el => el.remove()); } catch { /* selector may not parse */ }
  }
  // Strip event handler attributes
  root.querySelectorAll('*').forEach(el => {
    for (const attr of STRIP_ATTRS) {
      el.removeAttribute(attr);
    }
    // Strip inline event handlers (on*)
    const attrs = el.rawAttributes || {};
    for (const attr of Object.keys(attrs)) {
      if (attr.startsWith('on')) {
        el.removeAttribute(attr);
      }
    }
  });
  // Strip comments
  // node-html-parser doesn't expose comments easily, so we do a regex pass later

  // Remove empty container elements (leftover from script/tracking removal)
  let changed = true;
  while (changed) {
    changed = false;
    root.querySelectorAll('div, span, p').forEach(el => {
      const text = el.text?.trim() || '';
      const children = el.childNodes?.length || 0;
      if (!text && children === 0) {
        el.remove();
        changed = true;
      }
    });
  }
}

// ── Iteration 2: CSS resolution and inlining ──

async function resolveCSS(root, baseUrl) {
  const linkEls = root.querySelectorAll('link[rel="stylesheet"], link[type="text/css"]');
  const cssTexts = [];
  let fetched = 0;
  let totalCSSSize = 0;

  for (const link of linkEls) {
    if (fetched >= MAX_CSS_FETCHES || totalCSSSize >= MAX_CSS_TOTAL_SIZE) break;
    const href = link.getAttribute('href');
    if (!href) continue;
    try {
      const cssUrl = new URL(href, baseUrl).href;
      const { execSync } = await import('node:child_process');
      const css_raw = execSync(
        `curl -sL --max-time 5 -H "User-Agent: Mozilla/5.0 (compatible; PaletteGrab/1.0)" ${JSON.stringify(cssUrl)}`,
        { encoding: 'utf-8', maxBuffer: 2 * 1024 * 1024, timeout: 6000 }
      );
      if (css_raw) {
        let css = css_raw;
        // Resolve relative URLs in CSS (url(...))
        css = css.replace(/url\(["']?(?!data:)(?!https?:)([^"')]+)["']?\)/g, (match, path) => {
          try { return `url(${new URL(path, cssUrl).href})`; } catch { return match; }
        });
        cssTexts.push(`/* ${cssUrl} */\n${css}`);
        totalCSSSize += css.length;
        fetched++;
      }
    } catch { /* skip unreachable stylesheets */ }
    link.remove();
  }

  // Collect inline <style> blocks
  root.querySelectorAll('style').forEach(el => {
    cssTexts.push(el.innerHTML);
    el.remove();
  });

  return cssTexts.join('\n\n');
}

// ── Iteration 3: Asset handling ──

function resolveAssetURLs(root, baseUrl) {
  // Images: make URLs absolute, remove tracking pixels
  root.querySelectorAll('img').forEach(el => {
    const src = el.getAttribute('src');
    // Remove likely tracking pixels (1x1, spacer gifs, beacon images)
    const w = parseInt(el.getAttribute('width') || '999', 10);
    const h = parseInt(el.getAttribute('height') || '999', 10);
    if ((w <= 1 || h <= 1 || w === 0 || h === 0) ||
        (src && /\b(pixel|beacon|track|spacer|s\.gif|blank\.gif|clear\.gif)\b/i.test(src))) {
      el.remove();
      return;
    }
    if (src && !src.startsWith('data:') && !src.startsWith('http')) {
      try { el.setAttribute('src', new URL(src, baseUrl).href); } catch { /* leave as-is */ }
    }
    const srcset = el.getAttribute('srcset');
    if (srcset) {
      const resolved = srcset.split(',').map(entry => {
        const parts = entry.trim().split(/\s+/);
        if (parts[0] && !parts[0].startsWith('data:') && !parts[0].startsWith('http')) {
          try { parts[0] = new URL(parts[0], baseUrl).href; } catch { /* leave */ }
        }
        return parts.join(' ');
      }).join(', ');
      el.setAttribute('srcset', resolved);
    }
  });

  // Background images in inline styles
  root.querySelectorAll('[style]').forEach(el => {
    const style = el.getAttribute('style');
    if (style && style.includes('url(')) {
      const resolved = style.replace(/url\(["']?(?!data:)(?!https?:)([^"')]+)["']?\)/g, (match, path) => {
        try { return `url(${new URL(path, baseUrl).href})`; } catch { return match; }
      });
      el.setAttribute('style', resolved);
    }
  });

  // Favicons, icons
  root.querySelectorAll('link[rel*="icon"]').forEach(el => {
    const href = el.getAttribute('href');
    if (href && !href.startsWith('data:') && !href.startsWith('http')) {
      try { el.setAttribute('href', new URL(href, baseUrl).href); } catch { /* leave */ }
    }
  });
}

// ── Iteration 4: Selector-scoped extraction ──

function extractBySelector(root, selector) {
  const matches = root.querySelectorAll(selector);
  if (matches.length === 0) return null;
  // Return all matches wrapped in a div
  const wrapper = parseHTML('<div class="grab-extracted"></div>');
  for (const el of matches) {
    wrapper.firstChild.appendChild(el);
  }
  return wrapper.firstChild;
}

// ── Iteration 5: Assembly + quality ──

function assembleCleanHTML(title, css, bodyContent, baseUrl) {
  const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>${escapeHTML(title)}</title>
<base href="${escapeHTML(baseUrl)}"/>
<style>
${css}
</style>
</head>
<body>
${bodyContent}
</body>
</html>`;
  // Strip HTML comments
  return html.replace(/<!--[\s\S]*?-->/g, '');
}

function escapeHTML(str) {
  return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// ── Main grab function ──

export async function grab(url, selector = null) {
  // Validate URL
  let parsedUrl;
  try {
    parsedUrl = new URL(url);
    if (!['http:', 'https:'].includes(parsedUrl.protocol)) {
      return { ok: false, error: `Unsupported protocol: ${parsedUrl.protocol}` };
    }
  } catch {
    return { ok: false, error: `Invalid URL: ${url}` };
  }

  // Fetch
  let rawHTML;
  try {
    rawHTML = await fetchWithTimeout(url);
  } catch (err) {
    return { ok: false, error: `Fetch failed: ${err.message}` };
  }

  // Parse
  const root = parseHTML(rawHTML, { comment: false });

  // Clean (Iteration 1)
  cleanHTML(root);

  // Resolve CSS (Iteration 2)
  const css = await resolveCSS(root, url);

  // Resolve assets (Iteration 3)
  resolveAssetURLs(root, url);

  // Extract title
  const titleEl = root.querySelector('title');
  const title = titleEl ? titleEl.text : parsedUrl.hostname;

  // Scope extraction (Iteration 4)
  let bodyContent;
  if (selector) {
    const scoped = extractBySelector(root, selector);
    if (!scoped) {
      return { ok: false, error: `Selector "${selector}" matched 0 elements` };
    }
    bodyContent = scoped.innerHTML;
  } else {
    const body = root.querySelector('body');
    bodyContent = body ? body.innerHTML : root.innerHTML;
  }

  // Assemble (Iteration 5)
  const html = assembleCleanHTML(title, css, bodyContent, url);

  return {
    ok: true,
    url,
    selector: selector || null,
    title,
    html,
    stats: {
      original_size: rawHTML.length,
      clean_size: html.length,
      reduction: `${Math.round((1 - html.length / rawHTML.length) * 100)}%`,
      css_inlined: css.length > 0,
    }
  };
}

// ── CLI ──

if (process.argv[1] && process.argv[1].includes('grab')) {
  const url = process.argv[2];
  const selector = process.argv[3] || null;

  if (!url) {
    console.error('Usage: node grab.mjs <url> [css-selector]');
    process.exit(1);
  }

  console.error(`Grabbing ${url}${selector ? ` (selector: ${selector})` : ''}...`);
  const result = await grab(url, selector);

  if (!result.ok) {
    console.error(`Error: ${result.error}`);
    process.exit(1);
  }

  console.error(`Done. ${result.stats.original_size} → ${result.stats.clean_size} (${result.stats.reduction} reduction)`);

  // Write to stdout for piping, or to file
  const outFile = process.argv[4];
  if (outFile) {
    writeFileSync(outFile, result.html);
    console.error(`Written to ${outFile}`);
  } else {
    process.stdout.write(result.html);
  }
}
