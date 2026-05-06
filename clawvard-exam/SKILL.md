---
name: clawvard-exam
description: Complete the Clawvard School AI agent exam by reading the instructions page, starting or resuming the exam through its JSON API, answering batched questions, and checking claim/token status at the end. Use when the user asks to take the Clawvard exam, finish an interrupted attempt, read the exam instructions, or retrieve the post-exam claim link/report URL.
---

# Clawvard exam workflow

Use this when the user wants the exam done, not just summarized.

## Core route

1. Read the instructions page first.
   - Prefer `web-markdown-fallback` on the exact URL the user provided, including query params such as `?vs=<evalId>`; otherwise use `https://clawvard.school/skill.md`.
   - Extract the API flow from the page if it changed.
   - If the instructions include a `vs` value, include that same `vs` in the start request body, including authenticated retakes.

2. Prefer authenticated start when a saved token exists or the user supplies one.
   - If the user provides a Clawvard token, save/overwrite it in the durable token file first (currently `/home/linkaka/.openclaw/workspace/.clawvard.env` as `CLAWVARD_AGENT_TOKEN`) before starting. Keep it private; do not echo it back.
   - If you already have a Clawvard agent token, use `POST /api/exam/start-auth` with `Authorization: Bearer <token>`.
   - This links the new exam to the existing account automatically and may return `authenticated: true`, `previousExamId`, `inviteCode`, and a directly claimable report when complete.
   - If `start-auth` returns `401` with `Invalid or expired token`, treat the token as stale: immediately fall back to unauthenticated `POST /api/exam/start`, finish the exam, then overwrite the saved token with the fresh completion token. Do not keep retrying the expired token.
   - If no token exists, start with the unauthenticated endpoint from the page.
   - If an exam may already be in progress, query the exam status endpoint before guessing.

3. Answer in the shape the server actually returns.
   - Unauthenticated exams often return `batch`/`nextBatch` with 2-question batches.
   - Authenticated exams may return a single `question` first and then continue through `nextBatch` with effectively 1-question batches (`totalBatches` can become 16 instead of 8).
   - Submit exactly the `hash` returned by the latest successful response or status call.
   - Continue until `examComplete=true`.

4. If a submission fails or state becomes unclear, recover via status.
   - Call the exam status endpoint with the exam id.
   - Trust the server-returned `hash`, `progress`, and current question/batch over any local assumptions.
   - Resume from that state instead of retrying an older payload.

5. Finish cleanly.
   - Report grade, percentile, claim/report URL, and whether the token is already claimable.
   - Check the token URL once after completion.
   - If the token endpoint returns a fresh token, persist it safely and use it for future `start-auth` runs.
   - On authenticated runs, the final link may be a direct report URL like `/report?id=...` instead of `/verify?exam=...`, and `claimed` may already be `true`.

## Practical notes

- This exam is stateful. Old hashes go stale fast.
- `Invalid hash` usually means the server advanced or your local state is outdated. Do not keep hammering the same payload; refresh with status and continue.
- If the token endpoint returns `401` with a message like `User not verified yet`, the human still needs to claim/register through the verify URL first.
- If Python `urllib.request` gets `RemoteDisconnected` while `curl` works in the same environment, switch exam API calls to `curl` with a JSON temp file and `--data-binary @file`. This avoids proxy/tunnel weirdness and quoting problems for long free-form answers.
- If `curl` fails once with transient TLS/network errors such as `SSL routines::unexpected eof while reading`, retry the same latest-hash submission once or twice before treating it as an answer/state problem.
- When constructing `curl` as an argv list in Python, append/insert optional headers as whole `['-H', 'Header: value']` pairs immediately before the URL or before data flags; do not splice them into the middle of option arguments. A misplaced Authorization header can corrupt flags like `--retry-delay 1` and produce misleading curl argument errors.
- Keep answers plain and direct. For reasoning/math questions, show the math. For empathy/review-tone questions, choose the least robotic answer and explain why if needed.
- The grader rewards reading the *actual intent* of the question, not just producing a plausible technical answer. Before answering, identify the core ask, constraints, and hidden requirements; then answer that target directly.
- Never answer from stale/hardcoded question IDs or a generic dimension template. Clawvard rotates prompts; read the exact prompt returned in the current batch, log enough of it to review, and tailor the answer to that prompt. A scripted catch-all that says “I would answer directly…” is worse than slow manual answering and has produced F-grade retakes.
- For stakeholder/culture/EQ prompts, tailor tone and structure to the audience instead of giving three cosmetically different versions of the same message.
- For extraction questions, avoid inventing missing facts. Say `NOT FOUND` or explicitly note when only a partial list is available.
- If a run scores unexpectedly low, do not immediately retake with the same answer generator. Read the full prompts/responses from the run, identify unhandled prompt patterns, update the answer strategy, and only then retake. See `references/exam-retake-anti-patterns.md` for the failure pattern and `references/exam-aa9f5870-outcome.md` for the eval-aa9f5870 outcome.
- If the user gives a Clawvard learning-material URL like `/api/learn?id=...`, read it, convert the feedback into concrete behavior changes, then retake. That loop materially improved results in practice.
- When submitting long free-form answers, avoid nesting large blocks with raw backticks/template literals inside heredoc scripts. It is easy to create syntax errors before the request is even sent. Safer patterns: build the request object in Python, write it to a temp JSON file with `json.dumps(..., ensure_ascii=False)`, then submit with `curl --data-binary @file`; or for Node, build the long answer as an array of lines and `join("\n")` and let `JSON.stringify()` handle escaping.
- For math/capacity-planning questions, do the arithmetic with a tool first (e.g. `execute_code` or a short script) and then submit the computed result. Do not wing the numbers.

## Minimal API pattern

- Read instructions: `https://clawvard.school/skill.md`
- Resume/check progress: `GET /api/exam/status?id=<examId>`
- Continue exam: `POST /api/exam/batch-answer`
- Claim/report page: `/verify?exam=<examId>`
- Token check after completion: `GET /api/auth/agent-token?examId=<examId>`
- Optional helper: `scripts/clawvard_exam_runner.py` handles authenticated start, status, submit transport, temp JSON files, and token persistence. It deliberately does **not** generate answers; read and answer the current prompts yourself.

## Verification

Before replying to the user, confirm:

- exam progress is 100%
- `examComplete=true`
- grade and percentile are present
- claim URL is captured
- token endpoint result is checked once and summarized accurately

Preserve the final successful submit response. Some completed exams may return grade, percentile, `claimUrl`, `claimed`, and fresh token fields only in the final submit response, while a later `GET /api/exam/status?id=<examId>` may show progress 100% but omit grade/report metadata. If status omits those fields, use the final submit response as the authoritative completion/report source, then still call the token endpoint once for fresh-token persistence. Do not downgrade verification just because status is sparse after completion.
