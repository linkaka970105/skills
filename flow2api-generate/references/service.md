# Flow2API Local Service Notes

## Runtime

- Base URL: `http://127.0.0.1:38000`
- Container: `flow2api`
- Image: `flow2api:headed`
- Restart policy: `unless-stopped`
- Docker daemon: systemd enabled
- Config file: `/home/linkaka/flow2api/config/setting.toml`
- Database: `/home/linkaka/flow2api/data/flow.db`

## Working Mode

The known working captcha path is `personal` with a headed Chromium/Xvfb browser inside the container:

- `ALLOW_DOCKER_HEADED_CAPTCHA=true`
- `DISPLAY=:99`
- `XVFB_SCREEN=1440x900x24`
- `PERSONAL_BROWSER_HEADLESS=0`
- Browser/request proxy: `http://127.0.0.1:8889`

## Performance Notes

Last local comparison:

- `yescaptcha`: average total about 40.0 seconds, captcha about 11.4 seconds
- `personal`: average total about 32.4 seconds, captcha about 3.4 seconds

Recommendation: use `personal` unless the user explicitly requests a provider comparison.

## API Shape

OpenAI-compatible endpoint:

- `GET /v1/models`
- `POST /v1/chat/completions`

The client script streams `/v1/chat/completions`, extracts result URLs from markdown links or plain URLs, and prints JSON.
