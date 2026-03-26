---
name: priority-strategy-integration-technical-design
overview: 为 `shareholder-yield-enhancer`、`cash-cow-compounder`、`leader-oversold-recovery`、`soe-rerating` 这 4 个优先方向整理一份技术设计文档，明确如何并入现有母策略、各自的数据与判断信号、输出结构和后续文档落点。
todos:
  - id: audit-parent-strategies
    content: 使用 [subagent:code-explorer] 复核四个母策略承接关系与引用链
    status: completed
  - id: draft-integration-design
    content: 起草 PRIORITY_STRATEGY_INTEGRATION_DESIGN.md 并写清四方向并入方案
    status: completed
    dependencies:
      - audit-parent-strategies
  - id: update-doc-indexes
    content: 更新 README.md 与 STRATEGY_DESIGN_CHECKLIST.md 增加设计文档入口
    status: completed
    dependencies:
      - draft-integration-design
  - id: verify-consistency
    content: 校验术语、链接、数据边界与输出契约一致性
    status: completed
    dependencies:
      - update-doc-indexes
---

## User Requirements

- 为 `shareholder-yield-enhancer`、`cash-cow-compounder`、`leader-oversold-recovery`、`soe-rerating` 输出一份技术设计文档。
- 文档重点是说明这 4 个方向如何直接并入现有母策略，而不是重新拆成独立策略或单独命令。
- 设计内容需围绕当前已经确定的承接关系展开：四个方向分别并入 `high-dividend-strategy`、`undervalued-stock-screener`、`quant-factor-screener`、`esg-screener` 的既有框架。

## Product Overview

- 交付物应是一份位于 `stock-screener` 插件内的结构化设计文档，集中说明四个高优先方向的目标边界、母策略分工、协同链路、验证信号与后续演进。
- 文档呈现应清晰分层，读者能快速从总体承接图进入单方向设计、统一输出要求和文件落点，不需要来回翻查多份零散说明。

## Core Features

- 明确四个方向的并入对象、职责边界、优先级与“不单建策略”的约束。
- 统一描述硬筛选、策略强化、异常发现、机会归类四层分析链路在四个方向中的落法。
- 汇总每个方向的关键验证信号、数据补查需求、失效条件与风险提示。
- 定义统一输出契约、文档引用关系与后续更新入口，保证现有文档体系可继续扩展。

## 技术栈选择

- 文档载体：复用仓库现有 Markdown 文档体系。
- 文档位置：沿用 `.claude/plugins/stock-screener/` 根目录治理文档结构。
- 参考基础：已存在的 `README.md`、`STRATEGY_DESIGN_CHECKLIST.md`，以及四个母策略的 `SKILL.md`、`DECISIONS.md`、`references/*.md`。

## 实现方案

- 采用“新增一份并入设计总文档 + 小范围回写索引文档”的方式完成，不扩散为多份新策略文档。
- 新文档只负责当前四个高优先方向的集成设计：说明目标边界、承接映射、统一执行链路、数据需求、输出契约、文件落点与演进原则；各母策略的执行细节继续以现有 `skills/*` 文档为准。
- 关键决策：
- 不新建新的 `skills/` 或 `commands/` 目录，严格遵循现有“先并入四个母策略”的原则。
- 只引用仓库内已验证过的数据入口、OpenAPI 后缀、指标字段和数据边界，避免把未验证能力写进设计文档。
- `quant-factor-screener` 保持解释增强层定位，`esg-screener` 保持治理验证层定位，避免职责重叠。
- 性能与可靠性：
- 本次无运行时代码改动，主要风险是文档漂移与口径不一致；通过“总文档引用现有 source docs”降低重复维护成本。
- 设计文档应继续强调“先建候选池，再对入围股补查”，避免把工作流写成全市场逐股深拉；补查成本随入围股数量线性增长，风险可控。
- 避免技术债：
- 不复制各 skill 中的大段方法论，只抽取并入所需的差异化逻辑和协同边界。
- 对公告、治理改善、外部评级等仓库内不能直接证实的部分，统一标记为外部补充或待验证。

## 实施说明

- `README.md` 与 `STRATEGY_DESIGN_CHECKLIST.md` 当前已存在未提交修改，回写时应采用最小增量补充，避免覆盖已有编辑内容。
- 新文档中的术语、分类名、输出段落名，应与现有四个母策略文档保持一致，优先复用已落地表述。
- 除非发现索引断链或明显矛盾，否则不额外改动 `commands/` 与 `skills/*` 文件，控制影响面。

## 架构设计

- 根文档层：
- `README.md` 负责插件定位、策略索引、扩展原则。
- `STRATEGY_DESIGN_CHECKLIST.md` 负责策略立项门槛与优先级清单。
- 集成设计层：
- 新增一份并入设计文档，作为“四个优先方向如何落到现有母策略”的总说明。
- 执行细节层：
- `skills/high-dividend-strategy/`
- `skills/undervalued-stock-screener/`
- `skills/quant-factor-screener/`
- `skills/esg-screener/`
这些目录继续承载具体方法论、数据查询与输出模板。

## Directory Structure

### Directory Structure Summary

本次改动以新增总设计文档为主，并对现有两份根文档做轻量索引补充，保持现有 skill 文档体系不扩散。

```text
.claude/plugins/stock-screener/
├── PRIORITY_STRATEGY_INTEGRATION_DESIGN.md   # [NEW]
├── README.md                                 # [MODIFY]
└── STRATEGY_DESIGN_CHECKLIST.md              # [MODIFY]
```

- `/.claude/plugins/stock-screener/PRIORITY_STRATEGY_INTEGRATION_DESIGN.md`  [NEW]  
用途：作为四个高优先方向并入现有母策略的技术设计总文档。
功能：写清目标边界、母策略承接映射、统一四层分析链路、分方向验证信号、数据需求、输出契约、风险边界、文件落点与后续演进。
要求：所有映射、接口、字段、分类名称必须引用现有已验证文档；无法验证的能力要显式标注边界。

- `/.claude/plugins/stock-screener/README.md`  [MODIFY]  
用途：插件总入口与策略索引。
功能：补充新设计文档入口，并确保根层策略映射与新文档保持一致。
要求：只做增量补链，不重写现有大段内容，避免与当前未提交修改冲突。

- `/.claude/plugins/stock-screener/STRATEGY_DESIGN_CHECKLIST.md`  [MODIFY]  
用途：策略设计池与立项检查清单。
功能：补充对新设计文档的引用，并把“第一优先级并入现有母策略”的结论与设计文档建立双向关系。
要求：继续保持 checklist 属性，不把完整技术设计重复堆进本文件。

## Agent Extensions

### SubAgent

- **code-explorer**
- Purpose: 在落笔前复核 `stock-screener` 下四个母策略、根文档、引用路径与现有边界描述。
- Expected outcome: 输出准确的受影响文件清单、承接关系与可引用事实，确保设计文档与现有文档体系一致。