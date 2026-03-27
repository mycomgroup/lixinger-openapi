---
description: 监控目标行业/概念板块的拥挤度状态，计算综合拥挤度评分，识别脆弱触发器，给出降仓/观察/回避建议。
argument-hint: "[行业名称或概念名称] [--type industry|concept] [--alert-threshold 70|80|90]"
---

# 板块拥挤度监控

对目标行业/概念板块计算综合拥挤度评分（换手率分位 + 成交占比 + 估值分位 + 资金集中度），识别脆弱触发器（量价背离/成交萎缩/龙头破位），给出明确的降仓/观察/回避操作建议。

## 执行步骤

1. **确认参数**：
   - `subject`：目标行业名称（如"电子"）或概念名称（如"AI算力"）
   - `type`：`industry`（行业板块）/ `concept`（概念板块，使用 AKShare 数据）
   - `alert-threshold`：拥挤度告警阈值，默认 80（即评分 > 80 时触发告警）

2. 加载 `board-crowding-risk-monitor` skill（`.claude/plugins/industry-concept-research/skills/board-crowding-risk-monitor/SKILL.md`），执行：
   - **拥挤度评分（0-100）**：
     - 换手率5日均值的10年历史分位数（权重30%）
     - 行业成交额占全A成交额比例的历史分位（权重25%）
     - PE-TTM 10年历史分位数（权重25%）
     - 北向/融资资金集中度变化（权重20%）
   - **脆弱触发器识别**：
     - 量价背离：成交量萎缩但价格仍维持高位
     - 成交萎缩：近5日成交额较高峰下降 > 30%
     - 龙头破位：板块龙头股收盘价跌破20日均线
   - **风险等级**：低（<60）/ 中（60-80）/ 高（>80）/ 极高（>90）

3. 输出结构化结论，必须包含：
   - 拥挤度仪表盘（总分 + 四维子指标分值）
   - 风险等级（低/中/高/极高）
   - 脆弱触发器清单（已触发 / 未触发 / 临近触发）
   - 操作建议：
     - 低（<60）：可正常参与
     - 中（60-80）：建议控制仓位，关注止盈时机
     - 高（>80）：建议减仓或不加仓
     - 极高（>90）：建议回避或清仓
   - 失效条件（如拥挤度快速回落 + 龙头股放量上涨则重新评估）
   - 监控指标（换手率、封板率、资金流变化）

4. **与 concept-board-analyzer 协同**：当概念板块处于"拥挤期"时，自动触发此命令；输出结果回传给 concept-board-analyzer 更新参与建议。

## 独立调用接口

本 skill 支持独立调用，为 `concept-board-analyzer`、`industry-board-analyzer` 提供风险刹车：

```
{
  "subject_name": "AI算力",
  "subject_type": "concept",    # industry | concept
  "as_of_date": "2026-03-27"
}
```

输出：`crowding_score`（拥挤度0-100）、`risk_level`（风险等级）、`fragility_triggers`（脆弱触发器）、`recommendation`（操作建议）

## 示例

```
/board-crowding-risk-monitor 电子
/board-crowding-risk-monitor AI算力 --type concept
/board-crowding-risk-monitor 新能源 --alert-threshold 70
/board-crowding-risk-monitor 人形机器人 --type concept --alert-threshold 80
```
