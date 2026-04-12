---
description: 对申万行业板块进行横截面估值、动量、景气度的综合分析，输出行业强弱排名与配置评分。
argument-hint: "[行业名称或代码] [--date YYYY-MM-DD] [--compare-industries 行业1,行业2]"
---

# 行业板块分析

对申万一级/二级行业做横截面估值扫描、动量分析与景气度评估，输出行业综合评分与配置建议。

## 执行步骤

1. **确认参数**：
   - `industry`：目标行业名称（如"电子"）或申万代码（如"360000"），留空则分析全量申万2021一级行业（31个）
   - `date`：分析基准日期，默认今日
   - `compare-industries`：可选，指定对比行业列表

2. 加载 `industry-board-analyzer` skill（`.claude/plugins/industry-concept-research/skills/industry-board-analyzer/SKILL.md`），执行：
   - **估值横截面**：PE-TTM / PB 的市值加权值及10年历史分位数
   - **动量分析**：近1M / 3M / 6M 涨跌幅计算（通过市值变化）
   - **股息率分析**：当前股息率与历史均值对比
   - **综合评分**：估值30% + 动量30% + 股息率10% + 景气30%

3. 按 `contracts/research-conclusion.schema.json` 输出结构化结论，必须包含：
   - 各行业综合得分排名表
   - 低估行业清单（PE分位 < 30%）
   - 高估行业清单（PE分位 > 70%）
   - 高股息行业清单（股息率 > 3%）
   - 置信度声明 + 数据缺口说明（如有）

4. 若数据获取失败，在 `data_gaps` 中标注，不允许无声略过。

## 独立调用接口

本 skill 支持被外部插件（`valuation`、`deep-research`）独立加载，最小输入：

```
{
  "industry_name": "电子",         # 或 industry_code: "360000"
  "as_of_date": "2026-03-27"      # 可选，默认今日
}
```

输出：`valuation_summary`（估值状态）、`momentum_signal`（超配/标配/低配）、`confidence`（置信度）

## 示例

```
/industry-board-analyzer
/industry-board-analyzer 电子
/industry-board-analyzer 电子 --date 2026-03-20
/industry-board-analyzer 电子 --compare-industries 半导体,消费电子,光学光电子
```
