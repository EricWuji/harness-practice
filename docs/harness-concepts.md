# Harness核心概念与分层约束

## Types → Config → Repo → Service → Runtime → UI

该链路表示**单向依赖**：

- `Types`：领域类型、接口、事件模型；不依赖其他层。
- `Config`：系统配置与装配参数；可依赖 `Types`。
- `Repo`：数据访问与持久化；可依赖 `Types`/`Config`。
- `Service`：业务编排与策略实现；可依赖 `Types`/`Config`/`Repo`。
- `Runtime`：运行时与任务调度；可依赖 `Types`/`Config`/`Repo`/`Service`。
- `UI`：展示层与交互层；可依赖全部下层。

禁止反向依赖，例如：

- `Repo` 依赖 `Service`
- `Types` 依赖 `UI`

## 渐进式披露（Progressive Disclosure）

在本仓库中，`AGENTS.md` 只放“入口规则”，再指向 `docs/` 的专题文档，意义是：

1. Agent先读取最小必要信息，避免一次性加载全部上下文。
2. 当任务涉及某主题（比如分层依赖）时，再按链接进入对应文档。
3. 降低提示噪声，提升执行稳定性与可维护性。

建议索引：

- 场景说明：`docs/scenario.md`
- Agent流程：`docs/agent-workflow.md`
- Prompt治理：`docs/prompt-policy.md`
- 分层依赖：`docs/harness-concepts.md`
