---
description: 分析目标行业的产业链上下游传导路径，判断价格、业绩、供需三层传导对行业景气度的影响。
argument-hint: "[行业名称] [--direction upstream|downstream|full] [--depth 1|2|3]"
---

# 产业链传导分析

绘制目标行业的产业链结构，分析上下游的价格/业绩/供需三层传导路径，识别景气度传导顺序与阶段位置。

## 执行步骤

1. **确认参数**：
   - `industry`：目标行业名称（如"半导体"、"新能源汽车"）
   - `direction`：分析方向，`upstream`（向上溯源）/ `downstream`（向下延伸）/ `full`（全链）
   - `depth`：传导层级深度，默认 2（上下游各2层）

2. 加载 `industry-chain-mapper` skill（`.claude/plugins/industry-concept-research/skills/industry-chain-mapper/SKILL.md`），执行：
   - **产业链结构绘制**：上游原材料 → 中游制造 → 下游应用的完整链条
   - **价格传导分析**：上游价格变动对中下游盈利的传导路径与时滞
   - **业绩传导分析**：景气改善/恶化从哪一环节最先反映，传导到目标行业需要多长时间
   - **供需传导分析**：需求扩张/收缩的产能利用率影响路径
   - **目标行业定位**：在产业链中是受益方、传导枢纽还是承压方

3. 输出结构化结论，必须包含：
   - 产业链结构图（文本格式）
   - 三层传导路径摘要（价格/业绩/供需）
   - 目标行业当前位置判断（受益/传导/承压）
   - 景气传导时滞估计
   - 关键上下游观测指标清单
   - 失效条件（如上游价格逆转、下游需求突变）

4. 协同说明：与 `industry-subsector-decomposer` 协同时，将行业链条中的各层环节传入做细分拆解。

## 独立调用接口

本 skill 可被 `valuation`、`deep-research` 独立加载，最小输入：

```
{
  "industry_name": "锂电池",
  "direction": "full",    # upstream|downstream|full
  "as_of_date": "2026-03-27"
}
```

输出：`chain_structure`（产业链结构）、`transmission_summary`（三层传导摘要）、`target_position`（目标行业定位）

## 示例

```
/industry-chain-mapper 半导体
/industry-chain-mapper 锂电池 --direction upstream
/industry-chain-mapper 新能源汽车 --direction full --depth 3
```
