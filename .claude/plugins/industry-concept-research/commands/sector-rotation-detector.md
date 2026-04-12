---
description: 基于宏观经济周期和五大宏观支柱，判断 A 股各行业未来 6-12 个月的配置方向（超配/标配/低配）及置信度。
argument-hint: "[--horizon 6m|12m] [--risk-pref conservative|balanced|aggressive] [--industries 行业1,行业2]"
---

# 行业轮动信号探测

分析宏观经济指标与经济周期位置，生成 A 股行业超配 / 标配 / 低配信号，为资产配置决策提供宏观依据。

## 执行步骤

1. **确认参数**：
   - `horizon`：预测时间窗口，默认 `6m`（6个月）
   - `risk-pref`：风险偏好，`conservative`（小幅偏离）/ `balanced`（显著超配低配）/ `aggressive`（集中押注）
   - `industries`：可选，指定分析的行业子集；不填则覆盖全量申万2021一级行业（31个）

2. 加载 `sector-rotation-detector` skill（`.claude/plugins/industry-concept-research/skills/sector-rotation-detector/SKILL.md`），执行：
   - **五大宏观支柱评估**：货币政策 + 通胀 + 经济增长 + 就业消费 + 政策导向
   - **经济周期定位**：复苏 / 扩张 / 滞胀/过热 / 衰退 四阶段判断
   - **行业信号生成**：对每个行业给出超配/标配/低配 + **基准概率**（置信度）
   - **失效触发识别**：为每个观点定义具体可观测的失效条件

3. 按 `contracts/research-conclusion.schema.json` 输出结构化结论，必须包含：
   - 宏观仪表盘（五大支柱当前状态与方向）
   - 经济周期判断（阶段 + 位置）
   - 全行业信号表（信号 + 逻辑 + 基准概率）
   - 超配行业深度分析（Top 3-5）
   - 低配行业深度分析（Bottom 3-5）
   - 情景分析（失效触发条件矩阵）

4. **置信度强制**：所有行业信号必须附带基准概率（0-1），低于 0.3 的信号标记为 REFUSE，不给出方向性建议。

## 独立调用接口

本 skill 可被 `regime-lab` 独立加载，作为行业层面的轮动验证：

```
{
  "as_of_date": "2026-03-27",
  "horizon": "6m",                  # 可选
  "target_industries": ["电子","银行"]  # 可选，不填则全量分析
}
```

输出：`rotation_signals[]`（行业信号表）、`cycle_phase`（经济周期）、`confidence`

## 示例

```
/sector-rotation-detector
/sector-rotation-detector --horizon 12m
/sector-rotation-detector --risk-pref aggressive
/sector-rotation-detector --industries 电子,银行,新能源 --horizon 6m
```
