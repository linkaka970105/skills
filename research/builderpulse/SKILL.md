---
name: builderpulse
description: Fetch and summarize BuilderPulse daily opportunity briefs from https://github.com/BuilderPulse/BuilderPulse. Use when the user asks for BuilderPulse, indie hacker daily reports, daily startup/build opportunities, micro-SaaS idea briefings, or scheduled BuilderPulse digests in Chinese or English.
---

# BuilderPulse

Use this skill to retrieve BuilderPulse's latest daily opportunity brief and turn it into a concise founder-oriented digest.

## Source

- Repository: `https://github.com/BuilderPulse/BuilderPulse`
- Reports: `zh/YYYY/YYYY-MM-DD.md` and `en/YYYY/YYYY-MM-DD.md`
- License: BuilderPulse report content is CC BY-NC 4.0. Do not repackage it for commercial redistribution without permission. Personal/internal summaries are fine.

## Quick workflow

1. Run `scripts/fetch_latest.py` to fetch the latest report.
2. Prefer `--lang zh` unless the user asks for English.
3. Summarize in the user's language.
4. Include the source date and GitHub/raw links.
5. Keep the digest actionable rather than dumping the full report.

Example:

```bash
python ~/.hermes/skills/research/builderpulse/scripts/fetch_latest.py --lang zh --max-chars 12000
```

The script uses curl first and tries common local proxies (`socks5h://127.0.0.1:1089`, `http://127.0.0.1:7897`) because GitHub access in this environment often needs proxy routing. Override with `BUILDERPULSE_PROXY` if needed.

## Digest format

For a daily report, produce:

```markdown
**BuilderPulse 日报｜YYYY-MM-DD**

**今日建议**
- <one concrete build idea>

**为什么现在值得做**
- <2-3 bullets on timing and pain>

**Top 信号**
1. <signal + metric/source>
2. <signal + metric/source>
3. <signal + metric/source>

**两小时 MVP**
- <what to build first>

**咔咔视角**
- <one blunt/opinionated founder take>

来源：<GitHub report link>
```

## Cron guidance

When creating a scheduled BuilderPulse daily job:

- Default schedule: `30 9 * * *` local time, unless the user specifies another time.
- Deliver to the origin chat when created from chat.
- Use agent mode, not script-only, so the report can be summarized and translated.
- Enable only the toolsets needed: `terminal`, `file`, `web`, `skills` if available.
- Prompt must be self-contained and mention this skill name.

Suggested cron prompt:

```text
Load the `builderpulse` skill. Fetch the latest Chinese BuilderPulse report from https://github.com/BuilderPulse/BuilderPulse using the bundled script or GitHub raw files. If today's report is not published yet, use the newest available report and state its date. Produce a concise Chinese daily digest with: 今日建议, 为什么现在值得做, Top 3 信号, 两小时 MVP, 咔咔视角, and source link. Do not dump the full report. Respect CC BY-NC 4.0: this is an internal personal summary, not a commercial republication.
```

## Pitfalls

- The GitHub repository is a content archive, not a native Hermes/Claude skill. This local skill wraps it into a usable workflow.
- Do not assume today's calendar date has a report; fetch the newest available file from the repo.
- Avoid sending the entire Markdown report to chat. The raw files are long; summarize.
- If GitHub is slow or unreachable, retry with proxy-aware curl/Python environment or fall back to the last cached copy if one exists.
