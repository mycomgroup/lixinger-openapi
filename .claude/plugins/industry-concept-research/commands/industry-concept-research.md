---
description: 行业与概念研究统一 Orchestrator。根据研究主题和模式自动编排所有分析模块，输出带置信度评级、QA 自检状态、失效条件和监控清单的结构化研究结论。
argument-hint: "[研究主题] [--mode quick|full|detailed] [--horizon 1m|3m|6m|12m]"
---

# 行业与概念研究统一 Orchestrator

面向 A 股行业板块与概念板块的一体化研究入口，支持三种模式：

| 模式 | 适用场景 | 调用模块 | 预计耗时 |
|------|---------|---------|---------|
| `quick` | T+0 快速复盘、盘中判断 | 横截面扫描 + 联动识别 | 最短 |
| `full` | 深度行业研究、建仓决策 | 全10模块完整流程 | 较长 |
| `detailed` | 细分行业下钻、因子归因 | full + 细分拆解 + 因子归因 | 最长 |

---

## 执行流程

### 阶段 0：解析输入

确认以下参数：
1. **研究主题**：行业名称（如"电子"）或概念名称（如"AI算力"）
2. **模式**：`quick` / `full` / `detailed`（默认 `full`）
3. **时间窗口**：`1m` / `3m` / `6m` / `12m`（默认 `6m`）
4. **主体类型**：自动判断为 `INDUSTRY_BOARD`（对应申万行业代码）或 `CONCEPT_BOARD`（主题概念）

### 阶段 1：快速横截面（所有模式均执行）

**Step 1 — 行业板块横截面扫描**

加载 `industry-board-analyzer` skill（`.claude/plugins/industry-concept-research/skills/industry-board-analyzer/SKILL.md`）：
- 获取当日所有申万一级行业估值分位数（PE/PB 10年分位）
- 计算近 1M/3M 涨跌幅排名
- 生成综合评分（估值30%+动量30%+股息10%+景气30%）
- 产出 `skill_outputs[industry-board-analyzer]`：行业强弱排名 + 目标行业估值状态

若主体为 `CONCEPT_BOARD`，同步执行：

**Step 2 — 概念板块生命周期判断**

加载 `concept-board-analyzer` skill（`.claude/plugins/industry-concept-research/skills/concept-board-analyzer/SKILL.md`）：
- 判断概念主题所处阶段：启动 / 扩散 / 拥挤 / 退潮
- 评估主题热度（涨停家数 + 换手率 + 资金流综合打分）
- 产出 `skill_outputs[concept-board-analyzer]`：阶段判断 + 热度评分

**Step 3 — 涨跌停联动检测（快速信号）**

加载 `limit-up-down-linkage-detector` skill（`.claude/plugins/industry-concept-research/skills/limit-up-down-linkage-detector/SKILL.md`）：
- 识别近期涨停板块扩散路径
- 判断资金主线与跟风盘分布
- 产出 `skill_outputs[limit-up-down-linkage-detector]`：联动信号摘要

> **quick 模式在此结束**，直接进入阶段 4 执行 QA 自检并输出结论。

---

### 阶段 2：轮动归因（full/detailed 模式）

**Step 4 — 宏观驱动行业轮动分析**

加载 `sector-rotation-detector` skill（`.claude/plugins/industry-concept-research/skills/sector-rotation-detector/SKILL.md`）：
- 评估五大宏观支柱（货币/通胀/增长/就业/政策）
- 判断经济周期阶段（复苏/扩张/滞胀/衰退）
- 生成行业超配/标配/低配信号（含基准概率）
- 产出 `skill_outputs[sector-rotation-detector]`：轮动信号表 + 经济周期判断

**Step 5 — 板块拥挤度风险监控**

加载 `board-crowding-risk-monitor` skill（`.claude/plugins/industry-concept-research/skills/board-crowding-risk-monitor/SKILL.md`）：
- 计算拥挤度综合评分（换手分位 + 成交占比 + 估值分位 + 资金集中度）
- 识别脆弱触发器（量价背离 / 成交萎缩 / 龙头破位）
- 产出 `skill_outputs[board-crowding-risk-monitor]`：拥挤度仪表盘 + 风险提示

---

### 阶段 3：结构验证（full/detailed 模式）

**Step 6 — 产业链传导分析**

加载 `industry-chain-mapper` skill（`.claude/plugins/industry-concept-research/skills/industry-chain-mapper/SKILL.md`）：
- 绘制上下游传导路径（价格/业绩/供需三层传导）
- 识别景气传导顺序与时滞
- 判断目标行业在产业链中的位置（受益 / 传导 / 承压）
- 产出 `skill_outputs[industry-chain-mapper]`：传导路径图 + 景气传导判断

**Step 7 — 政策敏感度评估**

加载 `policy-sensitivity-brief` skill（`.claude/plugins/industry-concept-research/skills/policy-sensitivity-brief/SKILL.md`）：
- 梳理近期相关政策（顶层定调 → 部委细则 → 地方执行 → 市场响应）
- 评估政策力度评分（0-10分）与行业敏感度矩阵
- 推演三种情景（超预期 / 符合预期 / 低于预期）
- 产出 `skill_outputs[policy-sensitivity-brief]`：政策力度评分 + 情景概率

**Step 8 — 研报观点校验**

加载 `industry-report-analyzer` skill（`.claude/plugins/industry-concept-research/skills/industry-report-analyzer/SKILL.md`）：
- 汇总卖方主流观点与目标价
- 评估多空分歧程度
- 识别卖方共识与逆向机会
- 产出 `skill_outputs[industry-report-analyzer]`：研报共识摘要 + 分歧度评分

---

### 阶段 4：深度下钻（仅 detailed 模式）

**Step 9 — 行业细分拆解**

加载 `industry-subsector-decomposer` skill（`.claude/plugins/industry-concept-research/skills/industry-subsector-decomposer/SKILL.md`）：
- 申万一级 → 二级 → 三级下钻，识别细分强弱分层
- 分解 Alpha 来源（行业 Beta vs 细分 Alpha）
- 输出"下一阶段优先子方向"
- 产出 `skill_outputs[industry-subsector-decomposer]`：细分排名表 + 优先子方向

**Step 10 — 板块因子归因**

加载 `sector-factor-attributor` skill（`.claude/plugins/industry-concept-research/skills/sector-factor-attributor/SKILL.md`）：
- 三维归因：估值扩张 + EPS预期上修 + 风险溢价变化
- 风格因子暴露：大小盘 / 成长价值 / 质量红利
- 产出 `skill_outputs[sector-factor-attributor]`：归因拆解表 + 归因置信度

---

### 阶段 5：QA 自检 + 结论生成

**Step 11 — 置信度计算**

按 `contracts/qc-rules.schema.json` 的 `confidence_calculation_rules` 计算综合置信度：

```
raw_confidence = Σ(skill_weight[i] × skill_confidence[i])
overall_confidence_impact = min(1, Σ(data_gap.confidence_impact))
confidence = clamp(raw_confidence × (1 - overall_confidence_impact), 0, 1)

skill_confidence: COMPLETED=1.0, DEGRADED=0.6, FAILED=0（影响权重）, SKIPPED=0（不影响权重）
```

说明：
- `data_gap.confidence_impact` 统一使用**非负折损**（禁止负数编码）。
- 若累计折损超过 1，按 `overall_confidence_impact = 1` 截断处理。
- 最终 `confidence` 必须截断在 `[0,1]`。

各 skill 权重：`industry-board-analyzer`=25%、`sector-rotation-detector`=20%、`industry-chain-mapper`=15%、`concept-board-analyzer`=10%、`policy-sensitivity-brief`=10%、`limit-up-down-linkage-detector`=8%、`industry-report-analyzer`=7%、`board-crowding-risk-monitor`=5%

**Step 12 — 输出决策判断（三档）**

| 决策 | 条件 |
|------|------|
| `CONCLUSION` | confidence ≥ 0.6 且 至少 3 个 skill COMPLETED/DEGRADED 且所有必填字段齐全 |
| `WARNING` | confidence 0.3-0.6，或存在 POOR 级别数据缺口，或超过 2 个 skill DEGRADED |
| `REFUSE` | confidence < 0.3，或核心 skill（industry-board-analyzer 且 sector-rotation-detector）全部 FAILED |

**Step 13 — QA 字段自检**

按 `contracts/qc-rules.schema.json` 的 `required_field_rules` 和 `consistency_rules` 执行：
- 检查所有 required 字段完整性（RF-001 ~ RF-005）
- 检查跨字段一致性（CS-001 ~ CS-004）
- 将检验结果填入 `qc_status.passed / errors / warnings`

**Step 14 — 生成结构化输出**

按 `contracts/research-conclusion.schema.json` 输出完整结论，必须包含：

```json
{
  "as_of_date": "YYYY-MM-DD",
  "research_subject": "电子",
  "subject_type": "INDUSTRY_BOARD",
  "output_decision": "CONCLUSION|WARNING|REFUSE",
  "confidence": 0.0~1.0,
  "summary": "一句话结论",
  "drivers": [...],
  "risks": [...],
  "invalidation_conditions": [...],
  "skill_outputs": [...],
  "monitoring_checklist": [
    {
      "checklist_id": "电子-20260410",
      "research_subject": "电子",
      "as_of_date": "YYYY-MM-DD",
      "review_date": "YYYY-MM-DD",
      "review_frequency": "WEEKLY",
      "indicators": [
        {
          "indicator_name": "PE-TTM 10年分位数",
          "category": "VALUATION",
          "current_value": "58%",
          "alert_threshold": ">60%",
          "alert_direction": "ABOVE",
          "observable_trigger": "估值分位连续3日高于60%",
          "action_on_trigger": "DOWNGRADE_CONCLUSION"
        }
      ]
    }
  ],
  "data_gaps": [...],
  "qc_status": { "passed": true|false, "errors": [...], "warnings": [...] }
}
```

---

## Fail-Safe 规则

| 场景 | 处理方式 |
|------|---------|
| 单个 skill 数据查询超时/报错 | 标记为 `DEGRADED`，继续执行其余 skill，置信度扣减 |
| 理杏仁 API 不可用 | 降级为仅分析可获取字段，在 `data_gaps` 中显式标注 |
| AKShare 数据缺失 | 跳过资金流相关分析，降级但不中断 |
| 核心 skill 全部 FAILED | 触发 `REFUSE`，说明原因，给出数据补充建议 |
| 置信度 < 0.3 | 强制 `REFUSE`，禁止输出超配/低配等方向性结论 |
| 数据陈旧（>T+2）| 在 `data_gaps` 中标注 `missing_reason: DATA_STALE`，降低置信度 |

**原则：降级不静默。所有降级必须在 `data_gaps` 中显式记录，用户必须能看到局限性。**

---

## 示例调用

```
/industry-concept-research 电子
/industry-concept-research 电子 --mode quick
/industry-concept-research AI算力 --mode full --horizon 3m
/industry-concept-research 新能源 --mode detailed --horizon 12m
/industry-concept-research 食品饮料 --mode full
```
