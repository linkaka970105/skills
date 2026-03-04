#!/usr/bin/env bash
set -euo pipefail

URL="${1:-}"
if [[ -z "$URL" ]]; then
  echo "Usage: fetch_markdown.sh <url>" >&2
  exit 2
fi

if [[ ! "$URL" =~ ^https?:// ]]; then
  echo "Error: URL must start with http:// or https://" >&2
  exit 2
fi

fetch_with_prefix() {
  local prefix="$1"
  local target="https://${prefix}/${URL}"

  local code
  code=$(curl -L --max-time 25 -A "Mozilla/5.0" -sS -o /tmp/wmf_out.txt -w "%{http_code}" "$target" || echo "000")

  if [[ "$code" =~ ^2 ]]; then
    # Heuristic: consider useful if non-trivial size and not obvious error page
    if [[ $(wc -c < /tmp/wmf_out.txt) -gt 200 ]] && ! grep -qiE "(error|not found|access denied|captcha)" /tmp/wmf_out.txt; then
      echo "SOURCE: ${prefix}"
      cat /tmp/wmf_out.txt
      return 0
    fi
  fi
  return 1
}

# 1) markdown.new
if fetch_with_prefix "markdown.new"; then
  exit 0
fi

# 2) defuddle.md
if fetch_with_prefix "defuddle.md"; then
  exit 0
fi

# 3) r.jina.ai
if fetch_with_prefix "r.jina.ai/http"; then
  exit 0
fi

# 4) Scrapling fallback
if command -v scrapling >/dev/null 2>&1; then
  if scrapling "$URL" >/tmp/wmf_scrapling.txt 2>/tmp/wmf_scrapling_err.txt; then
    if [[ -s /tmp/wmf_scrapling.txt ]]; then
      echo "SOURCE: scrapling-cli"
      cat /tmp/wmf_scrapling.txt
      exit 0
    fi
  fi
fi

if command -v python3 >/dev/null 2>&1; then
  if python3 - <<'PY' "$URL" >/tmp/wmf_scrapling.txt 2>/tmp/wmf_scrapling_err.txt
import sys
url = sys.argv[1]
try:
    from scrapling.fetchers import Fetcher
    f = Fetcher(auto_match=False)
    page = f.get(url, timeout=25000)
    text = page.markdown if hasattr(page, 'markdown') else page.text
    if text:
        print(text)
        raise SystemExit(0)
except Exception:
    pass
raise SystemExit(1)
PY
  then
    if [[ -s /tmp/wmf_scrapling.txt ]]; then
      echo "SOURCE: scrapling-python"
      cat /tmp/wmf_scrapling.txt
      exit 0
    fi
  fi
fi

echo "All methods failed for: $URL" >&2
echo "Tried: markdown.new -> defuddle.md -> r.jina.ai -> Scrapling" >&2
exit 1
