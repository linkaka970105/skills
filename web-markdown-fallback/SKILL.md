---
name: web-markdown-fallback
description: Fetch web content as Markdown with prefix fallbacks. Use when user asks to search/read webpage content quickly or scrape pages that are hard to parse directly. Try markdown.new/, then defuddle.md/, then r.jina.ai/ as URL prefixes; if those fail, fall back to Scrapling-based extraction.
---

# Web Markdown Fallback

Use this skill to quickly get readable page content.

## Workflow

1. Accept a full URL (`https://...`).
2. Run:
   ```bash
   bash skills/web-markdown-fallback/scripts/fetch_markdown.sh "<URL>"
   ```
3. Return the best extracted Markdown/text result.
4. If all attempts fail, report which fallback layers failed.

## Notes

- Prefix order is fixed: `markdown.new/` → `defuddle.md/` → `r.jina.ai/`.
- Keep the original scheme in the prefixed URL (e.g. `https://markdown.new/https://example.com`).
- Use Scrapling only as final fallback.
