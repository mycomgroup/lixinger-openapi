# 行业与概念板块研究插件架构设计

## 1. 目标与定位

`industry-concept-research` 用于把行业与概念研究能力统一为可复用、可审计、可降级的研究流水线。

目标：

- 统一入口编排（Orchestrator）
- 模块独立可调用（10 skills）
- 输出结构统一（contracts）
- 质量门禁可执行（QA 三档决策）
- 异常处理可追踪（fail-safe + data_gaps）


## 行业口径说明

- **分类版本**：申万行业分类 `sw_2021`。
- **一级行业总数**：31 个。
- **口径更新时间**：2026-04-10。
- **边界说明**：
  - L1/L2 层涉及行业横截面、轮动、归因时，默认行业宇宙为申万2021一级行业。
  - 二级/三级行业分析仅作为同口径下钻扩展，不与其他行业标准混算。
  - 若数据源口径漂移（行业合并/拆分/命名调整），必须通过 `data_gaps` 披露并下调置信度。

## 2. 分层架构

### L0：命令编排层（commands）

- 主入口：`/industry-concept-research`
- 支持 `quick | full | detailed` 三种模式
- 职责：路由技能、聚合证据、执行 QA、给出最终决策

### L1：分析模块层（skills）

既有 7 项：

1. `industry-board-analyzer`
2. `sector-rotation-detector`
3. `industry-chain-mapper`
4. `concept-board-analyzer`
5. `policy-sensitivity-brief`
6. `limit-up-down-linkage-detector`
7. `industry-report-analyzer`

P0 新增 3 项（已落地）：

8. `industry-subsector-decomposer`
9. `sector-factor-attributor`
10. `board-crowding-risk-monitor`

> 每个 skill 均提供“§ 独立调用接口”，可直接被外部插件加载。

### L2：数据层

- 理杏仁 OpenAPI（`query_tool.py`）
- AKShare（概念与交易结构补充）

### L3：契约与输出层（contracts）

- `research-conclusion.schema.json`
- `monitoring-checklist.schema.json`
- `data-gap-report.schema.json`
- `inter-plugin-interface.schema.json`
- `qc-rules.schema.json`

用于保证跨 skill、跨插件输出口径一致。

## 3. Orchestrator 执行流程

1. 输入标准化（主题、范围、窗口、模式）
2. 横截面扫描（行业/概念）
3. 轮动归因与结构验证
4. 产业链与政策映射
5. 研报一致预期校验
6. 细分拆解 / 因子归因 / 拥挤度监控（按模式）
7. 统一聚合并产出 `skill_outputs[]`
8. 执行 QA 自检规则
9. 输出 `CONCLUSION | WARNING | REFUSE`

## 4. QA 闭环与三档决策

依据 `qc-rules.schema.json`：

- `CONCLUSION`：置信度 >= 0.60 且关键字段完整
- `WARNING`：置信度 0.30-0.60 或存在显著缺口
- `REFUSE`：置信度 < 0.30 或核心模块不可用

输出必须包含：

- 证据链：`skill_outputs[]`
- 缺口声明：`data_gaps`
- 质量状态：`qc_status/errors/warnings`
- 监控清单：`monitoring_checklist`（`checklist_id/research_subject/... + indicators[]` 嵌套结构）

## 5. Fail-safe 机制

### 5.1 模块级降级

- 非核心模块缺数：允许降级执行
- 核心模块缺数：下调决策到 `WARNING` 或 `REFUSE`

### 5.2 缺口强制披露

任何降级都必须写入 `data_gaps`：

- 缺失字段
- 缺失原因
- fallback 方法
- 对置信度影响

### 5.3 冲突与异常

- 若不同 skill 结论冲突，触发一致性规则并降权
- 若数据时效超阈值，标记时效风险并设置复评点

## 6. 复用与边界

跨插件复用通过 `inter-plugin-interface.schema.json` 与 `plugin.json` 声明：

- 外部消费者：`valuation`、`regime-lab`、`deep-research`
- 复用模式：信号注入、风险门控、监控转发、主题联动、结论摘要消费

边界约束：

- 本插件不做个股尽调与自动交易执行
- 仅提供结构化研究判断与监控框架

## 7. 演进方向

- 维持 contracts 先行，避免输出口径漂移
- 持续扩展 P1/P2 技能，但必须遵守同一 QA 与 fail-safe 规范
- 优先提升数据可得性与降级质量，而非扩展无契约的新能力