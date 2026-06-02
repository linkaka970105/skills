# WeChat MP rich extraction for deep-reading summaries

Use this when summarizing `mp.weixin.qq.com/s/...` articles and generic Markdown extraction fails or returns incomplete content.

## Reliable extraction path

1. Try existing web extraction first. If it fails with TLS EOF, CAPTCHA, or empty content, fetch the origin through the configured proxy using `socks5h` so DNS is proxied too.
2. Save HTML and check two signals:
   - `wappoc_appmsgcaptcha` absent.
   - `id="js_content"` present.
3. Extract metadata and article body from `js_content`.
   - Title: `id="activity-name"` or `var msg_title`.
   - Account: `id="js_name"`.
   - Body: the `div id="js_content"` block, stripping scripts/styles/svg and converting closing block tags to newlines.
4. Inspect embedded images in `js_content`.
   - WeChat articles often store comparison tables, architecture diagrams, or summary graphics as `mmbiz.qpic.cn` images.
   - Extract `data-src` / `src`, download via the same proxy when needed, and use vision/OCR on images that look like tables or diagrams.
5. Merge image/table facts into the final synthesis instead of treating them as decoration.

## Why this matters

In one Agent scheduling article, the text extraction captured the narrative, but the key OpenClaw vs Hermes Agent vs MSE comparison was embedded as an image table. OCR preserved rows including storage HA, service HA, performance, session isolation, notification delivery, Prompt versioning, observability, and workflow dependency orchestration. Missing that image would have produced a weaker summary.

## Summary integration checklist

- Did you capture the article title and source account?
- Did you verify the page is not a WeChat CAPTCHA or environment-error page?
- Did you parse `js_content`, not random script boilerplate?
- Did you enumerate and inspect inline images?
- Did you include table rows/columns when the image contains a comparison table?
- Did you label product-marketing claims as the article’s framing rather than neutral fact?
