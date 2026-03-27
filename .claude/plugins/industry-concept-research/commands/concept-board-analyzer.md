---
description: 分析 A 股概念主题板块的生命周期阶段（启动/扩散/拥挤/退潮），评估主题热度与持续性，识别拥挤度风险。
argument-hint: "[概念名称] [--mode lifecycle|heat|risk] [--horizon 2w|1m|3m]"
---

# 概念板块主题分析

判断主题概念板块当前所处的生命周期阶段，量化主题热度，评估拥挤度风险，为主题参与时机提供决策依据。

## 执行步骤

1. **确认参数**：
   - `concept`：概念板块名称（如"AI算力"、"人形机器人"）
   - `mode`：`lifecycle`（阶段判断）/ `heat`（热度评估）/ `risk`（拥挤度风险，联动 board-crowding-risk-monitor）/ 不填则全量执行
   - `horizon`：观测时间窗口，默认 `1m`

2. 加载 `concept-board-analyzer` skill（`.claude/plugins/industry-concept-research/skills/concept-board-analyzer/SKILL.md`），执行：
   - **生命周期阶段识别**：
     - 启动期：首板龙头出现，概念成员涨停数 < 3
     - 扩散期：成员涨停数持续扩大，资金持续净流入
     - 拥挤期：换手率突破历史80分位，新进资金边际减少
     - 退潮期：龙头股出现高位滞涨，涨停板封板率下降
   - **主题热度评分**：涨停家数 + 换手率变化 + 资金流 + 新闻热度（0-100分）
   - **概念 vs 行业区别判断**：识别是政策/事件主题驱动还是基本面改善
   - **与 board-crowding-risk-monitor 协同**：拥挤期自动触发拥挤度风险评估

3. 输出结构化结论，必须包含：
   - 当前生命周期阶段 + 阶段特征描述
   - 主题热度综合评分（0-100）
   - 参与建议（进入/持有/减仓/回避）
   - 主要风险（拥挤度风险 / 政策退出风险 / 基本面不及预期）
   - 失效条件（如板块龙头连续2日低开低走）
   - 监控指标（换手率分位、涨停板封板率、资金流变化）

4. 若主题热度评分 < 30 且处于退潮期，自动降级输出决策为 `WARNING`，不给出明确进入建议。

## 独立调用接口

本 skill 支持独立加载（不通过 Orchestrator）：

```
{
  "concept_name": "AI算力",
  "as_of_date": "2026-03-27",
  "mode": "lifecycle"   # lifecycle|heat|risk
}
```

输出：`lifecycle_stage`（阶段）、`heat_score`（热度评分 0-100）、`recommendation`（参与建议）

## 示例

```
/concept-board-analyzer AI算力
/concept-board-analyzer 人形机器人 --mode lifecycle
/concept-board-analyzer 低空经济 --mode risk --horizon 2w
/concept-board-analyzer 量子计算 --mode heat
```
