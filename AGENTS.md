# AGENTS.md

## 项目目标

这个仓库用于 **Harness + AI Agent 工程化协作练习**。

## 渐进式披露（必须遵守）

先读本文件，再按任务进入对应文档，避免一次性加载过多上下文：

- 场景说明：`docs/scenario.md`
- Agent工作流：`docs/agent-workflow.md`
- Prompt策略治理：`docs/prompt-policy.md`
- Harness分层概念与依赖规则：`docs/harness-concepts.md`

含义：

- `AGENTS.md` 提供入口规则；
- `docs/*.md` 提供主题细则；
- Agent只在需要时读取主题文档（Progressive Disclosure）。

## 分层依赖原则

必须遵守：`Types → Config → Repo → Service → Runtime → UI`。

- 只允许从左到右单向依赖；
- 禁止右侧层反向依赖左侧层。

CI 将执行 `scripts/check_layering.py` 进行自动检查。
