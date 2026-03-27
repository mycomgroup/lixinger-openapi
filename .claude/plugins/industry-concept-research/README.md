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
- `monitoring-checklist.schema.json`：统一监控清单结构（指标、阈值、触发动作）
- `data-gap-report.schema.json`：统一缺数与降级声明（缺口来源、降级方法、置信度影响）
- `inter-plugin-interface.schema.json`：跨插件复用接口声明（输出可消费项、独立调用约定）
- `qc-rules.schema.json`：输出 QA 自检规则（三档决策、完整性、矛盾检测）

## 输出与质量门禁

Orchestrator 强制输出三档决策：

- `CONCLUSION`：置信度 >= 60%，关键字段齐全
- `WARNING`：置信度 30%-60% 或存在重要数据缺口
- `REFUSE`：置信度 < 30% 或核心模块不可用

并附带：

- `skill_outputs[]` 中间产物（证据链）
- `data_gaps` 缺口声明（不可静默降级）
- `qc_status / errors / warnings` 自检结果

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