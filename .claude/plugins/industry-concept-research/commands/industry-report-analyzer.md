---
description: 综合分析卖方研报对目标行业的观点，汇总评级分布、目标价区间、多空分歧，识别共识与逆向机会。
argument-hint: "[行业名称] [--period 1m|3m|6m] [--focus consensus|divergence|catalyst]"
---

# 行业研报综合分析

汇总卖方机构对目标行业的研究报告，提炼评级分布、核心逻辑、多空分歧，识别研报共识背后的隐藏机会与风险。

## 执行步骤

1. **确认参数**：
   - `industry`：目标行业名称（如"电子"、"医药"）
   - `period`：研报覆盖时间范围，默认 `3m`（近3个月）
   - `focus`：分析重点，`consensus`（共识观点）/ `divergence`（多空分歧）/ `catalyst`（催化剂识别）/ 不填则全量

2. 加载 `industry-report-analyzer` skill（`.claude/plugins/industry-concept-research/skills/industry-report-analyzer/SKILL.md`），执行：
   - **评级分布统计**：强烈推荐 / 推荐 / 中性 / 回避 的比例分布
   - **目标价区间汇总**：隐含最高/最低/中值涨跌幅
   - **核心逻辑梳理**：多方主要逻辑 + 空方主要顾虑
   - **分歧度评估**：分歧度高（评级分散、目标价区间大）/ 低（高度一致）
   - **催化剂识别**：研报中提及频率最高的未来潜在催化剂
   - **逆向信号识别**：当分歧度极低（共识过于集中）时，标记为潜在逆向机会

3. 输出结构化结论，必须包含：
   - 研报综合评级（多家机构加权）
   - 评级分布图（各评级占比）
   - 目标价隐含涨幅区间
   - 多方核心逻辑（Top 3）
   - 空方核心顾虑（Top 3）
   - 分歧度评分（0-100，越高分歧越大）
   - 最重要的催化剂（未来1-3个月）
   - 置信度说明（研报数量少于3份时降级为 WARNING）

4. **数据降级说明**：若无法获取最新研报数据，标注为缺口并仅基于历史研报趋势给出参考性分析。

## 独立调用接口

本 skill 支持独立调用，最小输入：

```
{
  "industry_name": "电子",
  "period": "3m",        # 研报覆盖范围
  "as_of_date": "2026-03-27"
}
```

输出：`consensus_rating`（综合评级）、`divergence_score`（分歧度0-100）、`top_catalysts`（主要催化剂）

## 示例

```
/industry-report-analyzer 电子
/industry-report-analyzer 医药 --period 6m
/industry-report-analyzer 新能源 --focus divergence
/industry-report-analyzer 银行 --focus catalyst --period 1m
```
