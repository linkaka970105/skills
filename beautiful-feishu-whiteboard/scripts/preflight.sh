#!/usr/bin/env bash
# Preflight check for the beautiful-feishu-whiteboard skill.
# Verifies the tools needed to render an SVG and write it into Feishu as an editable whiteboard.
set -u
ok=1
echo "▶ Checking prerequisites for beautiful-feishu-whiteboard…"
echo

# Node ≥ 20
if command -v node >/dev/null 2>&1; then
  echo "  ✓ Node $(node -v)"
else
  echo "  ✗ Node.js not found — install Node ≥ 20  (https://nodejs.org)"
  ok=0
fi

# lark-cli  (npm: @larksuite/cli)  — auth + writing to Feishu
if command -v lark-cli >/dev/null 2>&1; then
  echo "  ✓ lark-cli ($(lark-cli --version 2>/dev/null | head -1))"
  status_json="$(lark-cli auth status --json --verify 2>/dev/null || true)"
  if printf '%s' "$status_json" | python3 -c 'import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get("identities",{}).get("user",{}).get("available") else 1)' 2>/dev/null; then
    echo "  ✓ lark-cli user identity is authenticated"
  else
    echo "  ✗ lark-cli user identity is missing. This skill writes boards with --as user. Run:"
    echo "        lark-cli config init     # first-time setup, scan the QR"
    echo "        lark-cli auth login      # authorize your Feishu/Lark account"
    ok=0
  fi
else
  echo "  ✗ lark-cli not found. Install and authenticate:"
  echo "        npm install -g @larksuite/cli"
  echo "        lark-cli config init     # scan the QR"
  echo "        lark-cli auth login"
  ok=0
fi

# whiteboard-cli  (run via npx, auto-downloads)
if npx -y @larksuite/whiteboard-cli@^0.2.11 -v >/dev/null 2>&1; then
  echo "  ✓ @larksuite/whiteboard-cli reachable via npx"
else
  echo "  ! could not reach @larksuite/whiteboard-cli via npx (needs network on first run)"
fi

echo
if [ "$ok" = 1 ]; then
  echo "✅ Ready. You also need a Feishu/Lark account — boards are written to your own tenant."
else
  echo "❌ Missing prerequisites above. Install them, then re-run this check."
  exit 1
fi
