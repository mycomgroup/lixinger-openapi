---
description: 对申万行业做一级→二级→三级的细分拆解，识别细分强弱分层，定位 Alpha 来源，输出"下一阶段优先子方向"。
argument-hint: "[行业名称] [--level two|three] [--date YYYY-MM-DD]"
---

# 行业细分拆解

从申万一级行业下钻到二级/三级，识别各细分行业的相对强弱，分解 Alpha 来源（行业 Beta vs 细分 Alpha），输出下一阶段值得重点关注的优先子方向。

## 执行步骤

1. **确认参数**：
   - `industry`：目标申万一级行业名称（如"电子"、"医药生物"）
   - `level`：下钻层级，`two`（到二级行业）/ `three`（到三级行业，数据更细但可能不完整）
   - `date`：分析基准日期，默认今日

2. 加载 `industry-subsector-decomposer` skill（`.claude/plugins/industry-concept-research/skills/industry-subsector-decomposer/SKILL.md`），执行：
   - **层级拆解**：一级 → 二级（可选三级）行业列表获取
   - **细分强弱排名**：各细分行业近1M/3M 涨跌幅 + 估值分位数排名
   - **贡献度分解**：识别哪些细分行业贡献了一级行业大部分涨跌幅
   - **强弱分层**：领涨层 / 跟涨层 / 掉队层 三层划分
   - **Alpha 来源识别**：超出一级行业 Beta 的细分 Alpha 来源

3. 输出结构化结论，必须包含：
   - 细分行业排名表（涨跌幅 + 估值分位数 + 强弱层）
   - 贡献度分解（各细分行业对一级行业涨跌幅的贡献比例）
   - 强弱分层结果（领涨/跟涨/掉队）
   - Alpha 来源判断
   - 下一阶段优先子方向（Top 2-3）+ 选择理由
   - 置信度说明（数据覆盖不完整时降级）

4. 与 `industry-chain-mapper` 协同：如需了解领涨细分行业在产业链中的位置，可联动分析。

## 独立调用接口

本 skill 支持独立调用，最小输入：

```
{
  "industry_name": "电子",
  "level": "two",           # two | three
  "as_of_date": "2026-03-27"
}
```

输出：`subsector_ranking`（细分排名表）、`alpha_source`（Alpha来源）、`priority_subsectors`（优先子方向）

## 示例

```
/industry-subsector-decomposer 电子
/industry-subsector-decomposer 医药生物 --level three
/industry-subsector-decomposer 新能源 --level two --date 2026-03-20
```
