# MEMORY

## Preferences

- 定时任务默认使用 **agent turn + isolated 模式** 执行。
- 收到相关任务时，按该模式优先实现，除非用户明确要求其他方式。
- 安装新的 skills 后，需要执行 git 提交并推送到 GitHub 仓库 `https://github.com/linkaka970105/skills` 以同步更新。
- 该仓库默认 git 身份为：`user.name=linkaka`、`user.email=linkaka970105@gmail.com`。
- 模型策略：默认优先 `openai-codex/gpt-5.3-codex`；当额度不足或不可用时，自动切换到 `edgefnglm/GLM-5`，并第一时间告知用户切换原因与目标模型。
- 回复偏好（跨会话生效）：若流程使用了 skills，需要在每次回复结尾追加“Skills 使用记录”；若未触发也写“Skills 使用记录：无”。该记录持续输出，直到用户明确说停止。
- AI 日报默认结构：
  1. Top 5 昨日重点
  2. 昨日发生了什么
  3. GitHub 热榜总览（全品类，不限 AI）
  4. GitHub 热榜 AI 专项（AI / Agent / LLM / Infra / Tools）
  5. 你该关注的 3 点
  用户提到“发日报/重发日报/整理日报”时，默认按此结构输出，除非用户明确要求更改。
