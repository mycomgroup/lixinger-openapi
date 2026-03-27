---
description: 对行业涨跌幅做三维因子归因（估值扩张/EPS预期上修/风险溢价变化），评估风格因子暴露，解释行业行情的本质驱动。
argument-hint: "[行业名称] [--period 1m|3m|6m] [--benchmark 沪深300]"
---

# 板块因子归因

对目标行业的阶段性涨跌幅做三维归因分解：估值扩张贡献 + EPS 预期上修贡献 + 风险溢价变化贡献，并评估行业的风格因子暴露（大小盘、成长价值、质量红利），回答"行业为什么涨/跌"。

## 执行步骤

1. **确认参数**：
   - `industry`：目标行业名称（如"电子"、"食品饮料"）
   - `period`：归因区间，默认 `3m`（近3个月）
   - `benchmark`：基准指数，默认"沪深300"

2. 加载 `sector-factor-attributor` skill（`.claude/plugins/industry-concept-research/skills/sector-factor-attributor/SKILL.md`），执行：
   - **三维收益拆解**：
     - 估值扩张贡献：PE/PB 变化产生的涨幅（纯情绪驱动）
     - EPS/盈利预期上修贡献：盈利增长驱动的涨幅（基本面驱动）
     - 风险溢价变化贡献：折现率变化产生的涨幅（宏观/流动性驱动）
   - **风格因子暴露**：大盘/小盘、成长/价值、质量/红利的因子暴露评估
   - **归因质量评估**：数据完整性驱动的归因置信度
   - **降级策略**：缺盈利预期数据时，使用"半归因"（估值 + 风险溢价两维）

3. 输出结构化结论，必须包含：
   - 三维归因拆解表（各驱动贡献比例）
   - 风格因子暴露矩阵
   - 归因质量评估（FULL / PARTIAL / INDICATIVE）
   - 对 `sector-rotation-detector` 的增强解释（为什么行业值得超配/低配的因子层面证据）
   - 置信度说明（缺盈利数据时自动降为 PARTIAL 归因并标注）

4. 协同说明：与 `sector-rotation-detector` 协同使用时，提供行业轮动信号的"为什么"解释，增强配置逻辑说服力。

## 独立调用接口

本 skill 支持独立调用，最小输入：

```
{
  "industry_name": "电子",
  "period": "3m",            # 归因区间
  "as_of_date": "2026-03-27"
}
```

输出：`attribution_breakdown`（三维归因表）、`style_exposure`（风格因子）、`attribution_quality`（归因质量）

## 示例

```
/sector-factor-attributor 电子
/sector-factor-attributor 食品饮料 --period 6m
/sector-factor-attributor 银行 --period 1m --benchmark 中证500
```
