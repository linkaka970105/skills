---
name: deep-reading-synthesis
description: Deep-read and distill articles, WeChat MP posts, reports, and long-form web content into high-density Chinese or English summaries that preserve concrete facts, numbers, causal logic, examples, and actionable takeaways. Use when the user asks to “吃透” an article, extract article essence, summarize a URL with hard details, produce TL;DR/core skeleton/new insights/actions, or avoid vague high-level summaries.
---

# Deep Reading Synthesis

## Role

Act as an extremely efficient, detail-first **deep reading and information refinement expert**. Help the user quickly eat through an article while preserving the valuable underlying logic, hard details, and core evidence.

## Core standard

Strictly follow **拒绝空话、保留细节**. Optimize for reading compression without detail loss. Do not write broad filler like “作者分析了行业现状”. Directly extract the actual status data, claims, numbers, examples, named products, causal links, tradeoffs, methods, and operating logic.

## Workflow

1. **Acquire the full source before summarizing.**
   - For normal URLs, use extraction tools or Markdown fallbacks.
   - For WeChat MP articles, if generic extraction fails, use the WeChat extraction pattern in `references/wechat-mp-rich-extraction.md`.
   - If the article contains embedded images, charts, or tables, inspect them before finalizing. Many WeChat posts put critical comparison tables in images.
2. **Separate article claims from your judgment.**
   - Mark the article’s stated thesis and evidence first.
   - Add your own brief judgment only after the requested structure, and label it as judgment.
3. **Preserve hard details.**
   - Keep concrete numbers, product names, architecture choices, failure modes, capability lists, URLs only when useful, named people/orgs, and exact categories.
   - Preserve “because X, therefore Y” logic instead of flattening it into themes.
4. **Compress aggressively but not vaguely.**
   - Prefer 3–5 core points.
   - Each point should have: claim → evidence/details → underlying logic or quote.
5. **Check completeness before final.**
   - Did you cover title/source/date if available?
   - Did you capture all tables/images with substantive content?
   - Did you avoid unsupported embellishment?

## Canonical output contract

When the user asks for article essence in Chinese, follow this structure strictly unless they supply a different format:

```markdown
### 1. 一句话核心主旨 (TL;DR)
- 用最精炼语言说明这篇文章核心解决了什么问题，或者传达了什么最颠覆的观点（不超过50字）。

### 2. 核心骨架与高密细节 (The Core & Details)
请梳理出文章的 3-5 个核心要点。每一个要点下，必须包含以下“硬核细节”：

#### 要点一：...
- **核心观点**：作者在这里提出了什么具体主张？
- **硬核论据/细节**：作者用了什么具体的事实、案例、数据、实验或对比来支撑这个观点？必须保留具体数字、专有名词、关键行动步骤，不要模糊带过。
- **底层逻辑/金句**：作者看问题的方法论是什么？有没有含金量极高的原话或逻辑推导？

### 3. 关键概念/新认知解释 (New Insights)
- 文章中是否有提及任何新名词、新概念、独特的行业术语，或者反直觉的观点？列出来并做简要大白话解释。

### 4. 核心落地行动点/启示 (Actionable Takeaways)
- 基于文章内容，列出读者可以直接复用、落地、或者用于指导实践的行动建议或思考模型（1-3条）。
```

Keep this as the default prompt contract. Adapt only when the user explicitly asks for another format. Keep their headings unless there is a strong reason not to.

## Quality bar

Good:
- “OpenClaw 把任务配置和运行记录存在本地文件；机器挂或磁盘坏会丢。Hermes Agent 的任务记录要去会话里找；OpenClaw 有记录但缺分页和搜索。”

Bad:
- “作者指出开源方案存在可观测和高可用问题。”

Good:
- “任务隔离：不同任务隔离会话，同一任务每次执行共享记忆；调度隔离每次新起会话，作者认为可能撑爆会话，不推荐。”

Bad:
- “文章介绍了多种会话管理方式。”

## Pitfalls

- Do not summarize from the browser CAPTCHA/error page.
- Do not ignore figures. If a table is an image, OCR/vision it and merge its contents into the synthesis.
- Do not over-credit advertorials. If the piece is product marketing, say so briefly while still extracting the real technical thesis.
- Do not invent numbers that are not in the source. If the article is vague, say it is vague.

## References

- `references/wechat-mp-rich-extraction.md` — WeChat MP extraction notes for article text plus embedded image/table capture.
