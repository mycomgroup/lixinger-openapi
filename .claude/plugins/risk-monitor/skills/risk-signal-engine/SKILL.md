---
name: risk-signal-engine
description: 可扩展风险信号引擎。用于重开发规则体系，支持单维风险、跨维风险、持仓后事件触发、风险升级与解除条件管理。当用户需要新增/修改风险规则、构建规则驱动排雷能力、或做事件触发风控时使用。
---

# Risk Signal Engine

## 执行目标

- 从规则文件中计算“可解释风险信号”。
- 输出告警必须包含：问题定义、证据链、触发逻辑、置信度、失效条件。
- 支持 `batch` 和 `event` 两种模式。

## 规则来源

- 规则 schema：`../../templates/rules-schema.json`
- 样例规则：`rules/`

## 核心约束

1. 不直接修改 `skills/legacy/` 中迁移过来的旧 skill。
2. 新增逻辑必须以规则文件方式落地。
3. 输出必须满足“问题发现导向”要求。
4. 持仓后事件必须能触发增量重算（公告、新闻、交易异动）。

## 开发顺序

1. 按 `rules-schema.json` 编写/校验规则。
2. 运行规则 lint（后续脚本接入）。
3. 按 `post-selection-risk-clearance-output-template.md` 生成输出。

