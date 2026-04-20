---
name: flow2api-generate
description: Generate images or videos through the local Flow2API service, list available Flow2API models, and troubleshoot local Flow2API generation. Use when a Hermes user asks to create images, make videos, use Google Flow, Veo, Gemini image generation, or inspect the local Flow2API service.
version: 1.0.0
author: local
prerequisites:
  commands: [python3, docker]
metadata:
  hermes:
    tags: [Media, Image, Video, Flow2API, Gemini, Veo]
---

# Flow2API Generate

Use the local Flow2API service at `http://127.0.0.1:38000` for image and video generation.

## Current Local Setup

- Service container: `flow2api`
- Service URL: `http://127.0.0.1:38000`
- Captcha mode: `personal`
- Default image model: `gemini-3.1-flash-image-landscape`
- Gemini 3.0 Pro image models are available, including: `gemini-3.0-pro-image-landscape`, `gemini-3.0-pro-image-portrait`, `gemini-3.0-pro-image-square`, `gemini-3.0-pro-image-four-three`, `gemini-3.0-pro-image-three-four`
- Video models include: `veo_3_1_t2v_fast_landscape`, `veo_3_1_i2v_s_fast_fl_landscape`, `veo_3_1_r2v_fast_portrait`
- API key source: prefer `FLOW2API_API_KEY`; otherwise read `/home/linkaka/flow2api/data/flow.db`; fallback to local default

Do not reveal Flow cookies, ST/AT tokens, captcha provider keys, or full API keys in chat. Mask secrets in status reports.

## Commands

Check service:

```bash
python3 /home/linkaka/.hermes/skills/media/flow2api-generate/scripts/flow2api_client.py status
```

List models:

```bash
python3 /home/linkaka/.hermes/skills/media/flow2api-generate/scripts/flow2api_client.py models --limit 20
```

Dry-run an image request without consuming credits:

```bash
python3 /home/linkaka/.hermes/skills/media/flow2api-generate/scripts/flow2api_client.py generate \
  --prompt "一只可爱的猫咪在花园里玩耍" \
  --dry-run
```

Generate an image:

```bash
python3 /home/linkaka/.hermes/skills/media/flow2api-generate/scripts/flow2api_client.py generate \
  --model gemini-3.1-flash-image-landscape \
  --prompt "一只可爱的猫咪在花园里玩耍" \
  --timeout 900
```

Generate a video:

```bash
python3 /home/linkaka/.hermes/skills/media/flow2api-generate/scripts/flow2api_client.py generate \
  --model veo_3_1_t2v_fast_landscape \
  --prompt "一只小猫在草地上追逐蝴蝶，电影感镜头，阳光柔和，镜头平滑推进" \
  --timeout 1800
```

Generate from reference images:

```bash
python3 /home/linkaka/.hermes/skills/media/flow2api-generate/scripts/flow2api_client.py generate \
  --model gemini-3.1-flash-image-landscape \
  --prompt "将这张图片变成水彩画风格" \
  --image /absolute/path/reference.jpg \
  --timeout 900
```

## Workflow

1. Run `status` before real generation unless the service was checked in the same session.
2. Use `--dry-run` for prompt/payload checks and debugging that should not consume Flow credits.
3. For normal image requests, use `gemini-3.1-flash-image-landscape` unless the user asks for portrait, square, video, or a specific model.
4. If the user explicitly asks for a `3.0 pro` model, honor that request by selecting the matching `gemini-3.0-pro-image-*` variant for the desired aspect ratio. For text-heavy educational posters, labeled diagrams, or infographic-style outputs, prefer `gemini-3.0-pro-image-four-three` unless the user asks for another shape.
5. For video requests, use a video model and set `--timeout 1800` or higher.
6. Return the JSON `primary_url`, elapsed time, model, and concise status. Do not paste full streamed logs unless asked.
7. If the user wants the generated image delivered in chat, do not stop at the remote `primary_url`. Download the image to a stable local path first, then send/embed the local file directly in the chat surface. Avoid replying with only an expiring URL unless the user explicitly asks for a link.
8. Some **2K image variants** may return a local cached URL like `http://127.0.0.1:38000/tmp/..._2K.jpg` instead of a public `storage.googleapis.com` URL. If the user needs a stable copy, save it immediately to a non-temporary local path. If the user explicitly needs an external link, prefer a non-2K image variant.

## Troubleshooting

- Service unreachable: run `docker ps --filter name=flow2api` and `docker logs --tail 120 flow2api`.
- Captcha errors: keep `personal` mode first; this local setup was tested faster than `yescaptcha`.
- `PUBLIC_ERROR_UNUSUAL_ACTIVITY` / `reCAPTCHA evaluation failed`: this can be intermittent. If the service is otherwise healthy, retry the same generation once before deeper debugging; a second attempt may succeed.
- 2K outputs may return a local cached URL like `http://127.0.0.1:38000/tmp/..._2K.jpg` instead of a Google storage URL. That is expected in this setup.
- Network errors: verify the container still uses host networking and proxy settings point to `127.0.0.1:8889`.
- Invalid API key: set `FLOW2API_API_KEY` or inspect the local DB without printing the full value.

For deployment notes, see `references/service.md`.
