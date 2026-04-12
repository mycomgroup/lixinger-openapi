# Industry & Concept Research Plugin

面向 A 股“行业板块 + 概念板块”研究的一体化插件，提供统一编排入口与可复用的模块化分析能力。

## 核心目标

将研究流程沉淀为可审计、可复评、可复用的标准闭环：

1. 横截面扫描（行业/概念强弱）
2. 轮动归因（驱动与持续性）
3. 产业链验证（景气传导）
4. 政策映射（催化与扰动）
5. 研报校验（一致预期与分歧）
6. 拥挤度与风险刹车（脆弱触发器）


## 行业口径说明

- **分类版本**：统一使用申万行业分类 `sw_2021`。
- **一级行业总数**：31 个（一级行业口径）。
- **口径更新时间**：2026-04-10。
- **边界说明**：
  - 本插件行业分析默认仅覆盖申万2021一级行业，不混用中信/Wind/GICS 口径。
  - 如需二级/三级下钻，仍基于同一 `sw_2021` 体系展开。
  - 若外部数据源出现分类变更，需在输出中显式披露并触发口径复核。

## 目录结构

- `commands/`：命令层（统一入口 + 各模块命令）
- `skills/`：能力层（10 个可独立调用 skill）
- `contracts/`：统一输出契约（JSON Schema）
- `plugin.json`：插件元数据、能力边界、复用声明
- `ARCHITECTURE.md`：架构与流程设计
- `ROADMAP_INDUSTRY_DETAIL_SKILLS.md`：能力规划与阶段状态

## Commands

### Orchestrator

- `/industry-concept-research [topic] [window] [mode=quick|full|detailed]`

### Core skills（既有）

- `/industry-board-analyzer [scope] [window]`
- `/sector-rotation-detector [scope] [window]`
- `/industry-chain-mapper [chain_theme]`
- `/concept-board-analyzer [concept_theme]`
- `/policy-sensitivity-brief [policy_theme]`
- `/limit-up-down-linkage-detector [window] [scope]`
- `/industry-report-analyzer [industry_or_topic] [window]`

### P0 skills（已落地）

- `/industry-subsector-decomposer [industry] [window]`
- `/sector-factor-attributor [industry] [window]`
- `/board-crowding-risk-monitor [industry_or_concept] [window]`

## Skills 索引

- `industry-board-analyzer`
- `sector-rotation-detector`
- `industry-chain-mapper`
- `concept-board-analyzer`
- `policy-sensitivity-brief`
- `limit-up-down-linkage-detector`
- `industry-report-analyzer`
- `industry-subsector-decomposer`
- `sector-factor-attributor`
- `board-crowding-risk-monitor`

> 每个 `SKILL.md` 均包含“§ 独立调用接口”，可被外部插件直接加载。

## Contracts（统一输出 Schema）

- `research-conclusion.schema.json`：统一研究结论结构（结论、证据链、置信度、风险、失效条件）
- `monitoring-checklist.schema.json`：统一监控清单结构（checklist 元信息 + indicators[] 嵌套指标条目）
- `data-gap-report.schema.json`：统一缺数与降级声明（缺口来源、降级方法、置信度影响）
- `inter-plugin-interface.schema.json`：跨插件复用接口声明（输出可消费项、独立调用约定）
- `qc-rules.schema.json`：输出 QA 自检规则（三档决策、完整性、矛盾检测）


## 契约版本变更说明（monitoring_checklist）

- **生效版本**：`industry-concept-research` `v2.1.0`（2026-04-10）。
- **唯一权威结构**：`monitoring_checklist` 采用 `checklist + indicators[]` 嵌套结构；不再接受历史扁平条目（如 `indicator/current_value/alert_threshold/review_date` 直接挂在数组元素上）。
- **兼容窗口**：旧格式仅在 `v2.0.x` 视为兼容输入，`2026-06-30` 后废弃；`2026-07-01` 起按新契约严格校验。
- **迁移方法**：
  1. 将旧条目按研究主题聚合为 checklist 对象，补齐 `checklist_id/research_subject/as_of_date/review_date`；
  2. 原 flat 字段迁移到 `indicators[]`：`indicator -> indicator_name`，其余字段映射为 `current_value/alert_threshold`；
  3. 新增必填：`category` 与 `alert_direction`（可按指标语义补全）；
  4. 建议直接复用 `contracts/monitoring-checklist.schema.json`，避免局部定义漂移。

## 输出与质量门禁

Orchestrator 强制输出三档决策：

- `CONCLUSION`：置信度 >= 60%，关键字段齐全
- `WARNING`：置信度 30%-60% 或存在重要数据缺口
- `REFUSE`：置信度 < 30% 或核心模块不可用

并附带：

- `skill_outputs[]` 中间产物（证据链）
- `data_gaps` 缺口声明（不可静默降级）
- `qc_status / errors / warnings` 自检结果

置信度折损统一使用 `confidence_impact` 正数编码，并按以下规则聚合：

- `overall_confidence_impact = min(1, sum(data_gaps[].confidence_impact))`
- `final_confidence = clamp(raw_confidence × (1 - overall_confidence_impact), 0, 1)`

示例：

- **单个 gap**：`raw_confidence=0.80`，`data_gaps=[{confidence_impact:0.20}]`  
  则 `overall_confidence_impact=0.20`，`final_confidence=0.80×(1-0.20)=0.64`。
- **多个 gap**：`raw_confidence=0.75`，`data_gaps=[0.15,0.30,0.70]`（累计 1.15）  
  则 `overall_confidence_impact=min(1,1.15)=1`，`final_confidence=0.75×(1-1)=0`（累计超过 1 时按 1 截断）。

## 异常处理与 Fail-safe

- 模块缺数：允许降级，但必须在 `data_gaps` 显式披露
- 关键依赖不可用：触发 `WARNING` 或 `REFUSE`，禁止强行给高置信结论
- 结论冲突：触发 QA 矛盾检测并下调决策等级
- 数据时效异常：标记时效风险并要求复评时间点

## 复用边界

插件输出可被以下外部插件消费：

- `valuation`
- `regime-lab`
- `deep-research`

具体复用模式与接口字段见 `plugin.json` 与 `contracts/inter-plugin-interface.schema.json`。
