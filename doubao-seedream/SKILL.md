---
name: doubao-seedream
description: 使用 Doubao Seedream 5.0 直接生图。适用于用户明确要求生成图片、海报、封面、插画、视觉素材时。
---

# Doubao Seedream 生图技能

当用户要求你生成图片时，优先使用以下配置：

- base URL: `https://ark.cn-beijing.volces.com/api/v3/images/generations`
- model: `doubao-seedream-5-0-260128`
- 鉴权：从 `/home/linkaka/.openclaw/openclaw.json` 中读取 `models.providers.doubao-seedream.apiKey`

## 执行规则

1. 先把用户需求整理成清晰英文 prompt；若用户要求中文风格文案可中英混合，但生图 prompt 默认优先英文。
2. 使用 `exec` 调用图片生成接口。
3. 默认尺寸使用 `1920x1920`，因为该模型要求图片尺寸至少 `3686400` 像素。
4. 成功后返回图片 URL；如果用户要，你也可以附上所用 prompt。
5. 如果失败：
   - 先检查是否是模型名错误、尺寸过小、或权限问题。
   - 再明确告诉用户失败原因，并询问是否需要改 prompt / 改尺寸 / 改模型重试。

## 建议请求格式

```bash
curl -sS 'https://ark.cn-beijing.volces.com/api/v3/images/generations' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <API_KEY>' \
  -d '{
    "model":"doubao-seedream-5-0-260128",
    "prompt":"<PROMPT>",
    "size":"1920x1920"
  }'
```

## 输出要求

- 简洁告诉用户：已生成 / 失败原因
- 给出图片 URL
- 如合适，补一句可以继续二改（换风格、比例、元素、文案）
