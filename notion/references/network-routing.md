# Notion API Network Routing Troubleshooting

Use this when Notion API calls fail before an HTTP response, especially errors like:

- `curl: (35) ... unexpected eof while reading`
- `SSL_connect: connection reset by peer`
- Python `RemoteDisconnected('Remote end closed connection without response')`
- HTTP status shown as `000`

## Diagnosis pattern

1. Do not assume the API key or Notion sharing is wrong when the failure is TLS EOF/reset and no HTTP body is returned.
2. Test the request with explicit routing and without leaking the token:

```bash
set -a
source ~/.hermes/.env
set +a

DB_ID="<database_id>"
curl --noproxy '*' \
  --resolve api.notion.com:443:208.103.161.2 \
  -sS -o /tmp/notion_db_smoke.json \
  -w 'http=%{http_code} remote=%{remote_ip} ssl=%{ssl_verify_result} version=%{http_version}\n' \
  -H "Authorization: Bearer $NOTION_API_KEY" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  "https://api.notion.com/v1/databases/$DB_ID"
```

A successful smoke test should print `http=200` and a usable remote IP. In the May 2026 environment, `api.notion.com` routed via `208.103.161.1` reset TLS while `208.103.161.2` succeeded.

## Short-term workaround

For curl-based Notion operations from this environment, add:

```bash
--noproxy '*' --resolve api.notion.com:443:208.103.161.2
```

This bypasses local proxy routing and pins the working Notion edge IP while preserving TLS SNI/hostname verification.

## Longer-term fix

Fix the local proxy/DNS routing for `api.notion.com`, or add a local DNS/hosts rule pointing `api.notion.com` to a working edge. Avoid saving a blanket rule that Notion is broken: this is a routing issue, not a Notion credential or API issue.

## Safety

Never print `NOTION_API_KEY`. Redact Authorization headers in verbose curl output before sharing logs.
