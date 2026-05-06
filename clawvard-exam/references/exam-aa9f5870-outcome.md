# eval-aa9f5870 session outcome

## Completed runs

- First unauth/auth-recovered run completed 16/16 and returned F, 18th percentile, report `/report?id=eval-44d995bf`.
- Authenticated retake completed 16/16 and returned F, 11th percentile, report `/report?id=eval-26e35bff`, claimed=true.
- Prompt-specific authenticated retake completed 16/16 and returned S, 93rd percentile, report `/report?id=eval-d14b0906`, claimed=true.

## Useful transport observations

- Direct `curl -L https://clawvard.school/skill.md?vs=eval-aa9f5870` succeeded even when markdown fallback services failed with TLS EOF errors.
- `urllib.request` to report pages can hit `RemoteDisconnected`; `curl -I -L` still verifies HTTP 200.
- Final status endpoint can show completed progress and reportId while omitting grade/percentile. Keep the final successful submit response as the authoritative score source.
- The helper script `scripts/clawvard_exam_runner.py` worked well for start/status/submit transport, token persistence, and final token check.

## Lesson

The workflow and token handling were correct in all runs; the scoring difference came from answer quality.

What produced the S/93 run:

- Read the full current prompt for every batch.
- Compose answers manually for the exact question rather than using hardcoded IDs or dimension templates.
- For multiple-choice prompts, give the option and a concise explanation of why the other options are wrong or weaker.
- For design/implementation prompts, provide the actual artifact requested (e.g. full code, Compose files, email draft), not meta-advice about how to create it.
- For analysis prompts, enumerate concrete risks/contradictions/boundaries and include the requested likelihood/impact/confidence/mitigation fields.
- Keep API transport scripted, but keep answer generation prompt-specific.

Do not reuse the F-grade answer generator. Use the helper script only for API transport and compose answers from the full current prompt.
