---
name: lightweight-data-source-architecture
overview: 将现有偏重 canonical 映射的多数据源设计，收敛为更轻量的接入方案：新 provider 只需 docs + API key + 最多一个命令；`cn-data-source` 降级为发现/路由/溯源层，避免维护大而脆弱的全量映射。
todos:
  - id: trace-call-chain
    content: 用 [subagent:code-explorer] 复核数据源调用链与影响文件
    status: completed
  - id: rewrite-architecture-doc
    content: 用 [skill:skill-creator] 重写轻量数据源方案文档
    status: completed
    dependencies:
      - trace-call-chain
  - id: refactor-skill-contracts
    content: 用 [skill:skill-creator] 调整 cn-data-source 与 data-source-docs 定位
    status: completed
    dependencies:
      - rewrite-architecture-doc
  - id: align-command-and-executor
    content: 同步 valuation 命令与 lixinger-data-query 为按需取数模式
    status: completed
    dependencies:
      - refactor-skill-contracts
  - id: add-provider-template
    content: 新增 Provider 接入模板并校验全文案一致性
    status: completed
    dependencies:
      - refactor-skill-contracts
---

## User Requirements

需要把现有数据源方案收缩成更轻量、低维护的模式。新增一个数据源时，最好只需要补三类内容：提供商文档、本地可读取的鉴权信息、最多一个查询命令或薄脚本；不希望每接一个数据源都维护一套完整字段映射。

## Product Overview

`cn-data-source` 应从“统一标准化装配器”调整为“数据源发现、路由与溯源入口”。它负责根据当前任务找到合适的数据源、给出可执行查询方式、保留来源说明；不强制对所有 provider 预先做完整统一映射。

文档效果应更清晰：新增 provider 时按固定模板补最少信息即可，阅读路径从“先找数据源、再执行查询、最后按当前任务提取需要字段”展开，避免厚重的全局规则。

## Core Features

- 以“Provider Pack”方式接入新数据源，只要求文档、鉴权说明、一个命令示例
- `cn-data-source` 只做发现、选择、调用建议与来源记录，不承诺完整标准输入
- 估值场景改为“按本次任务提取最小字段集”，不维护大而全的全局映射表
- 复用现有 provider 文档缓存能力，优先从摘要和本地文档定位可用接口
- 保留轻量溯源信息，说明字段或结果来自哪个 provider、哪个接口、哪个日期

## Tech Stack Selection

- 继续复用现有技能文档体系：`SKILL.md`、命令文档、设计文档
- 继续复用现有执行层：`.claude/skills/lixinger-data-query`
- 继续复用现有 provider 摘要层：`.claude/plugins/valuation/skills/data-source-docs`
- 保持 `company-valuation` 主脚本与输入主结构稳定，首阶段不引入新运行时框架

## Implementation Approach

采用“轻量 Provider Pack + 按任务临时提取”的方案，替代当前偏重的 registry、domain priority、全局 canonical 映射思路。高层流程是：先用 `data-source-docs` 和 provider 文档发现可用源，再由 `cn-data-source` 给出最合适的查询入口与来源说明，最后在具体任务里只提取本次真正需要的字段。

关键决策：

- 不维护完整 provider 到 canonical 的预映射，降低 provider 增长后的脆弱性
- 不把 `cn-data-source` 继续扩成完整标准化编排层，避免职责过重
- 不改 `auto_valuation.py`，把变化限制在文档与 skill 契约层
- 把“稳定性”放在 provider 接入模板和任务级提取规则上，而不是全局字段表

性能与可靠性：

- provider 发现优先读取 `data-source-docs` 缓存摘要，再回落到原始文档，搜索复杂度约为 O(P)，P 为 provider 数量；当前规模下开销很小
- 避免预先维护大映射表，可减少错误扩散面和后续修订成本
- 鉴权信息继续留在本地配置，不进入摘要、文档或示例输出

## Implementation Notes

- 首阶段不要改 `company-valuation/scripts/auto_valuation.py`
- 首阶段不要重写 `.claude/skills/lixinger-data-query/scripts/query_tool.py`
- 保留 `data-source-docs` “不做跨 provider 标准化”的既有原则
- 新 provider 只要求最小接入信息：文档位置、鉴权读取方式、一个查询示例、适用范围说明
- `source_map` 与 `source_notes` 保留为轻量溯源能力，不再当作全量治理中心
- 更新命令文案时，避免再承诺“自动整理完整标准输入”，改成“按当前任务抽取最小所需字段”

## Architecture Design

当前更合适的结构是四层轻耦合：

1. Provider 文档与摘要层  
`data-source-docs` 负责保存和读取 provider 最小摘要，帮助快速发现可用接口。

2. 执行层  
`.claude/skills/lixinger-data-query` 继续作为默认查询执行入口；对新 provider，只要求能落一个命令示例或薄脚本。

3. 路由与溯源层  
`cn-data-source` 负责识别当前任务需要什么、选择哪个 provider、更适合走哪条查询路径，并记录来源。

4. 任务消费层  
`cn-company-valuation` 等任务只在本次运行中提取所需字段，避免把一次性提取规则固化成全局映射资产。

这与现有仓库最一致，也能把改动集中在文档和 skill 约定层。

## Directory Structure

## Directory Structure Summary

本次方案以“收缩职责、统一接入模板、减少全局映射”为目标，主要改动现有设计文档、skill 文案和命令说明；仅新增一个 provider 接入模板文件，避免脚本层大改。

- `docs/DATA_SOURCE_ARCHITECTURE_DESIGN.md` [MODIFY]  
目的：把现有偏重的多 provider 架构改成更轻的 Provider Pack 方案。
功能：删除或降级 registry、domain priority、全局 canonical 装配叙述；改写为“docs + auth + one command + task-local extraction”。
要求：明确非目标，强调不做完整映射、不改估值主脚本。

- `.claude/plugins/valuation/skills/cn-data-source/SKILL.md` [MODIFY]  
目的：重定义 `cn-data-source` 的职责。
功能：从“标准化输入提供者”改为“数据源发现、路由、查询建议、溯源入口”。
要求：补充新 provider 最小接入规范，移除重映射导向表述。

- `.claude/plugins/valuation/skills/data-source-docs/SKILL.md` [MODIFY]  
目的：把现有轻量摘要能力正式纳入接入主流程。
功能：强调缓存摘要优先、原始文档回退、只提供最小接入信息。
要求：保持“不做跨 provider 标准化”的约束不变。

- `.claude/plugins/valuation/commands/cn-company-valuation.md` [MODIFY]  
目的：修正文案与执行假设。
功能：不再假设 `cn-data-source` 自动产出完整标准输入，而是说明先发现 provider，再按本次估值提取最小字段集。
要求：保持用户命令入口不变，减少行为预期偏差。

- `.claude/skills/lixinger-data-query/SKILL.md` [MODIFY]  
目的：明确它是当前默认执行中枢，而不是全局标准化层。
功能：增加“新 provider 可挂载文档与单命令示例”的说明。
要求：不改现有查询方式，只补充接入边界和定位。

- `.claude/plugins/valuation/skills/data-source-docs/references/provider-onboarding-template.md` [NEW]  
目的：提供统一、可复制的最小接入模板。
功能：规定每个 provider 需要填写的最少信息：文档来源、鉴权方式、一个命令示例、适用数据范围、注意事项。
要求：模板足够短，能直接复制后填写，避免新建 provider 时再发明结构。

## Key Code Structures

本轮不建议新增接口层代码结构；优先通过文档契约与模板收敛行为，降低实现面和回归风险。

## Agent Extensions

### SubAgent

- **code-explorer**
- Purpose: 复核 `valuation` 相关 skill、命令与文档之间的调用链和受影响文件，确保轻量化改法不遗漏引用点。
- Expected outcome: 得到准确的修改边界，避免只改设计文档而遗漏 `cn-company-valuation` 等实际入口说明。

### Skill

- **skill-creator**
- Purpose: 按现有 skill 规范重写 `cn-data-source`、`data-source-docs`、`lixinger-data-query` 的职责描述与接入模板。
- Expected outcome: 形成一致、可复用、低歧义的技能文案，使后续新增 provider 时只需按模板补最少内容。