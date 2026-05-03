# AGENTS.md

## 项目目标

这个仓库用于 **Harness + AI Agent 工程化协作练习**。默认假设：

- 需求、设计、代码、测试、文档大部分由 AI 生成；

- 人类主要负责设定边界、审批变更、处理例外。

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

## 练习场景（必须遵守）

我们要构建一个"**智能工单分流与SLA预警系统**"：

- 输入：来自邮件/IM/表单的客户问题；

- 输出：自动分类（账单/故障/咨询）、优先级（P1-P4）、建议处理人、SLA风险预警；

- 约束：必须可追溯、可回滚、可审计，且每次Agent改动都要有测试与评审记录。

## Agent协作原则

1. 先写计划，再改代码（Plan → Execute → Verify）。
2. 所有变更必须附带：
   - 变更摘要
   - 风险评估
   - 回滚方案
3. 默认新增或更新测试；如果不加测试，必须在PR描述中写明原因。
4. 涉及提示词（prompt）或策略规则变更时，必须更新 `docs/prompt-policy.md`。

## 分层依赖原则

必须遵守：`Types → Config → Repo → Service → Runtime → UI`。

- 只允许从左到右单向依赖；
- 禁止右侧层反向依赖左侧层。

CI 将执行 `scripts/check_layering.py` 进行自动检查。

## 目录约定

- `docs/`：业务背景、架构、流程、运行手册。

- `.github/workflows/`：CI流程，至少包含 lint / test / agent-policy 检查。

## 提交规范

提交信息建议采用：

- `docs: ...`

- `ci: ...`

- `feat: ...`

- `fix: ...`

## Definition of Done

一次任务完成至少满足：

- 文档更新（场景或流程有变化时）

- CI通过

- 可复现的本地验证命令
