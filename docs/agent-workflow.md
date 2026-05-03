# Harness练习工作流（AI主导）

## 1. 端到端流程

1. 需求录入（Issue / Spec）
2. Agent生成设计草案与任务拆分
3. Agent生成代码与测试
4. CI自动验证
5. 人工Review与审批
6. 部署到练习环境
7. 观察指标与回收反馈

## 2. 在Harness中的Pipeline建议

- Stage A: `plan`（读取需求、输出计划）

- Stage B: `build`（生成实现）

- Stage C: `verify`（lint/test/policy）

- Stage D: `human-approval`（人工关卡）

- Stage E: `release`（合并或部署）

## 3. 人工介入点（必须）

- 规则策略变更（分类规则、SLA阈值）

- 涉及客户可见文案

- 数据权限或安全相关变更

## 4. 失败处理

- CI失败：禁止进入审批关卡；

- 线上异常：执行回滚并冻结相应Agent策略版本；

- 误分类激增：切换到上一稳定模型/提示词。
