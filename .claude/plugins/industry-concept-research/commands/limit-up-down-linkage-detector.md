---
description: 追踪 A 股近期涨跌停联动路径，识别资金主线、板块扩散顺序与主力意图，判断行情持续性。
argument-hint: "[起始板块或龙头股] [--date YYYY-MM-DD] [--lookback 3d|5d|10d]"
---

# 涨跌停联动探测

分析 A 股近期涨跌停板的联动扩散路径，识别行情主线、跟风盘分布与资金主力意图，辅助判断板块行情是否具有持续性。

## 执行步骤

1. **确认参数**：
   - `start_subject`：可选，起始板块名称或龙头股代码（如"AI算力"、"300059"）；不填则分析全市场涨停联动
   - `date`：分析基准日期，默认今日
   - `lookback`：回溯窗口，默认 `5d`（5个交易日）

2. 加载 `limit-up-down-linkage-detector` skill（`.claude/plugins/industry-concept-research/skills/limit-up-down-linkage-detector/SKILL.md`），执行：
   - **联动路径识别**：首板 → 二板 → 跟风板的扩散顺序
   - **资金主线判断**：识别真正有资金堆积的主线板块（vs 跟风炒作板块）
   - **主力意图分析**：尾盘炸板 / 早盘封板 / 高开低走 / 量价背离等信号
   - **板块扩散阶段**：初期（1-2个板块涨停）/ 扩散期（3-5个板块）/ 高潮期（5+板块）/ 衰退期
   - **联动强度评分**：涨停股数量 + 封板率 + 资金净流入 + 板块覆盖广度

3. 输出结构化结论，必须包含：
   - 联动路径图（首板 → 跟风板的时序）
   - 资金主线识别（核心板块 + 跟风板块区分）
   - 当前扩散阶段判断
   - 联动强度评分（0-100）
   - 持续性判断（强 / 中 / 弱）
   - 关键风险（高位炸板 / 尾盘出货 / 量价背离）

4. **快速信号模式**：当由 Orchestrator（quick 模式）调用时，只输出关键联动摘要，省略详细扩散路径。

## 独立调用接口

本 skill 支持独立调用，最小输入：

```
{
  "as_of_date": "2026-03-27",
  "lookback_days": 5,           # 默认5日
  "start_concept": "AI算力"    # 可选
}
```

输出：`linkage_path`（联动路径）、`main_theme`（资金主线）、`continuation_signal`（持续性信号）

## 示例

```
/limit-up-down-linkage-detector
/limit-up-down-linkage-detector AI算力
/limit-up-down-linkage-detector 300059 --date 2026-03-25
/limit-up-down-linkage-detector --lookback 10d
```
