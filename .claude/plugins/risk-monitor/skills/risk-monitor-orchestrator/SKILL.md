---
name: risk-monitor-orchestrator
description: 风险监控编排器。用于在“旧能力迁移不整合”阶段控制执行模式（legacy_only / hybrid / engine_only），并管理选股后排雷与持仓后事件增量处理流程。
---

# Risk Monitor Orchestrator

## 执行模式

- `legacy_only`：仅调用 `skills/legacy/*`（当前默认）
- `hybrid`：旧能力 + 新引擎并行输出对照
- `engine_only`：仅新引擎

## 处理流程

1. 接收股票池与时间窗口
2. 判断是否为事件触发（公告/新闻/异动）
3. 按模式执行
4. 生成统一排雷报告

## 当前阶段策略

- 先确保 legacy 迁移可用。
- 新引擎在不影响 legacy 的前提下独立迭代。

