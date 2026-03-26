---
name: stock-screener-quality-improvement-plan
overview: 为 `.claude/plugins/stock-screener` 制定一轮质量提升方案，重点提升 6 个首批策略的差异化价值、文档可信度与可执行性，同时保持 `lixinger-screener` 作为通用筛选底座的定位不被扩张。
todos:
  - id: audit-gap
    content: 用[subagent:code-explorer]盘点全量文档缺口与校验点
    status: completed
  - id: rewrite-plugin-entry
    content: 重写 README 与 6 个 commands 入口规范
    status: completed
    dependencies:
      - audit-gap
  - id: upgrade-core-trio
    content: 用[skill:skill-creator]升级低估值、高股息、北交所策略包
    status: completed
    dependencies:
      - rewrite-plugin-entry
  - id: upgrade-remaining-trio
    content: 用[skill:skill-creator]升级小盘成长、量化因子、ESG 策略包
    status: completed
    dependencies:
      - rewrite-plugin-entry
  - id: sync-metadata-docs
    content: 统一修正安装、决策、元数据与索引
    status: completed
    dependencies:
      - upgrade-core-trio
      - upgrade-remaining-trio
---

## User Requirements

- 评估 `.claude/plugins/stock-screener` 当前内容的不足，先输出一份可执行的改进方案，不直接动手修改。
- 方案需要覆盖插件总说明、6 个策略 command、各自 skill 主文档与配套参考文档，重点提升内容可信度、实用性和差异化。
- 每个策略都要有独到判断和真实价值，不能继续停留在同模板改字的状态。
- 体系要保持可扩展，支持后续继续新增更多策略，不能把结构写死为固定 6 个。
- `lixinger-screener` 继续保持通用建池与基础筛选定位，不承载具体策略分析编排。

## Product Overview

- 本轮产出的是一套针对 stock-screener 插件的内容升级蓝图，统一 README、commands、SKILL、references、INSTALLATION、DECISIONS 与技能元数据。
- 改进后文档应更可信、结构更清晰，阅读时能快速看出每个策略的适用场景、筛选链路、输出重点与数据边界，整体呈现更整洁、层次更分明。

## Core Features

- 重建 6 个策略的差异化定位，明确各自的硬筛条件、软评分、核心风险和结论输出。
- 修正错误路径、不可移植绝对路径、缺失输入文件、可疑接口与字段示例，提升文档可复现性。
- 把输出模板收敛为“决策优先”格式，突出入选理由、失效条件、补充数据缺口，减少空泛大报告。
- 统一插件级扩展规则、安装说明、决策记录和发现入口文案，保证后续继续加策略时仍然可维护。

## Tech Stack Selection

- 内容载体沿用现有项目：Markdown 文档与 JSON 元数据。
- 候选池底座沿用仓库已有的 `.claude/skills/lixinger-screener/request/fetch-lixinger-screener.js`。
- 补充查询示例沿用 `.claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py`。
- 接口真实性以 `.claude/plugins/query_data/lixinger-api-docs/docs/*.md` 为校验源。
- Python 依赖基线以仓库根目录 `requirements.txt` 为准。

## Implementation Approach

本轮采用“先校准可信度，再重写策略价值，再统一发现入口”的方式推进，只改现有插件内容与元数据，不引入新脚本或新架构。整体按插件层、命令层、策略包层三层重构，优先处理当前证据最充分、最容易拉开差异的策略，再处理方法论与数据边界更复杂的策略。

### 关键技术决策

- 保持现有目录结构不变，只增强内容质量，避免引入新的组织模式。
- 所有策略统一遵循“候选池先行，入围股补查”的链路，避免把全市场逐股深拉写成默认方案。
- 每个策略都改成“适用场景、硬筛条件、二次判断、风险与失效条件、输出结论、数据缺口”六段式，保证统一但不模板化。
- 只保留已在仓库中可验证的 endpoint、参数与字段；做不到的能力显式降级为“可选外部补充”，不伪造能力。
- 输出模板从“大而全报告”收敛为“先结论、后证据”的决策格式，减少空转文字，提高真实使用价值。
- 升级优先级建议沿用当前仓库证据强弱顺序：低估值 → 高股息 → 北交所 → 小盘成长 → 量化因子 → ESG。

### Performance and Reliability

- 继续复用 `lixinger-screener` 做批量候选池，可把全市场深拉改为先批量筛选、再对少量入围股补查，显著减少接口调用与维护成本。
- 最大风险点是接口文档与示例字段漂移；缓解方式是逐条对照 `lixinger-api-docs/docs/`，不保留未被文档证实的字段名与列名。
- 保持命令名、技能名、目录名不变，控制影响面，避免破坏现有发现入口与引用关系。
- 不改 `lixinger-screener` 底座逻辑，也不改 `query_data` 实现，仅修正文档引用与使用边界。

## Implementation Notes

- `INSTALLATION.md` 当前普遍写成 `requirement.txt`，仓库实际文件是根目录 `requirements.txt`。
- `INSTALLATION.md` 当前普遍缺少 `.claude/` 前缀，真实查询脚本路径是 `.claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py`。
- 多份 `references/data-queries.md` 写入了作者本机绝对路径，需要统一改成仓库相对路径或中性占位。
- `high-dividend-strategy/references/data-queries.md` 引用了不存在的 `high-dividend-screen.json`，应替换为真实存在的输入方式或删除。
- `bse-selection-analyzer/references/data-queries.md` 使用了仓库 API 文档中未发现的 `cn/company/quote/daily`，应改为已存在的 `cn/company/candlestick` 或明确删去。
- `small-cap-growth-identifier`、`quant-factor-screener`、`esg-screener` 的示例中存在未在文档中检索到的字段或列名，应重写成文档已支持的指标表达，或改成“外部补充数据”说明。
- 低估值策略已有实测结果与经验沉淀，应把这些可验证经验从 `references/data-queries.md` 提升到 `SKILL.md` 和 command 主入口中，作为示范基线。

## Architecture Design

### 系统结构

- 插件层：`.claude/plugins/stock-screener/README.md` 定义总定位、扩展规则、数据分层与质量标准。
- 命令层：`commands/*.md` 负责用户入口、必问参数、默认流程与策略差异化唤起。
- 策略层：`skills/*/SKILL.md` 负责分析主链路，`references/*.md` 负责方法论、数据示例与输出模板。
- 校验层：`.claude/plugins/query_data/lixinger-api-docs/docs/*.md` 作为接口与字段真实性依据。
- 发现层：各 skill 的 `.claude-plugin/marketplace.json` 与全局 `.claude/plugins.json` 同步描述文案。

### 关系说明

用户输入 `/command` → 对应 `commands/*.md` → 对应 `skills/*/SKILL.md` → 引用 `references/*.md` → 数据路径优先走 `lixinger-screener`，按需补充 `query_data` 或外部来源。

## Directory Structure

### 总览

本轮不新增执行脚本，主要修改 stock-screener 插件内的文档与元数据，并同步全局索引。

### 插件层

- `.claude/plugins/stock-screener/README.md` [MODIFY] 插件总入口。重写策略矩阵、数据分层、扩展规则与统一质量标准，明确体系支持继续新增策略。
- `.claude/plugins/stock-screener/.claude-plugin/plugin.json` [MODIFY] 插件级描述元数据。同步新版定位与版本说明。
- `.claude/plugins.json` [MODIFY] 全局技能索引。同步 6 个策略的描述文案与发现入口信息。

### Commands 层

- `.claude/plugins/stock-screener/commands/undervalued-stock-screener.md` [MODIFY] 低估值入口。突出候选池模板、适用场景、必问项和风险导向。
- `.claude/plugins/stock-screener/commands/high-dividend-strategy.md` [MODIFY] 高股息入口。突出分红可持续性、总回报与红利陷阱排查。
- `.claude/plugins/stock-screener/commands/quant-factor-screener.md` [MODIFY] 量化因子入口。突出可复现因子输入、行业中性与输出限制。
- `.claude/plugins/stock-screener/commands/small-cap-growth-identifier.md` [MODIFY] 小盘成长入口。突出“被忽视的成长”与验证链路。
- `.claude/plugins/stock-screener/commands/bse-selection-analyzer.md` [MODIFY] 北交所入口。突出流动性优先与执行层风控。
- `.claude/plugins/stock-screener/commands/esg-screener.md` [MODIFY] ESG 入口。缩小到可实现的治理代理、争议排除与外部评级补充。

### 低估值策略包

- `.claude/plugins/stock-screener/skills/undervalued-stock-screener/.claude-plugin/marketplace.json` [MODIFY] 同步更准确的技能描述与发现文案。
- `.claude/plugins/stock-screener/skills/undervalued-stock-screener/SKILL.md` [MODIFY] 提升为示范级主文档，吸收已验证候选池模板、低估原因分析与风险失效条件。
- `.claude/plugins/stock-screener/skills/undervalued-stock-screener/INSTALLATION.md` [MODIFY] 修正依赖文件名、脚本路径与最小验证命令。
- `.claude/plugins/stock-screener/skills/undervalued-stock-screener/DECISIONS.md` [MODIFY] 去掉占位文本，记录真实数据路径与设计取舍。
- `.claude/plugins/stock-screener/skills/undervalued-stock-screener/references/screening-methodology.md` [MODIFY] 明确硬筛条件、相对估值原则与价值陷阱识别。
- `.claude/plugins/stock-screener/skills/undervalued-stock-screener/references/data-queries.md` [MODIFY] 移除绝对路径，保留实测命令与已验证参数文件经验。
- `.claude/plugins/stock-screener/skills/undervalued-stock-screener/references/output-template.md` [MODIFY] 改成决策优先模板，突出入选理由、失效场景与催化因素。

### 高股息策略包

- `.claude/plugins/stock-screener/skills/high-dividend-strategy/.claude-plugin/marketplace.json` [MODIFY] 同步新版策略价值主张。
- `.claude/plugins/stock-screener/skills/high-dividend-strategy/SKILL.md` [MODIFY] 强化分红可持续性、现金流覆盖、税后收益与总回报判断。
- `.claude/plugins/stock-screener/skills/high-dividend-strategy/INSTALLATION.md` [MODIFY] 修正统一安装与验证步骤。
- `.claude/plugins/stock-screener/skills/high-dividend-strategy/DECISIONS.md` [MODIFY] 写实记录数据边界与分红分析取舍。
- `.claude/plugins/stock-screener/skills/high-dividend-strategy/references/calculation-methodology.md` [MODIFY] 收敛为可执行计算链路，突出分红率、现金流覆盖与再投资假设。
- `.claude/plugins/stock-screener/skills/high-dividend-strategy/references/data-queries.md` [MODIFY] 删除不存在的 `high-dividend-screen.json` 引用，改成真实可复现示例。
- `.claude/plugins/stock-screener/skills/high-dividend-strategy/references/output-template.md` [MODIFY] 改成“收益质量优先”的输出模板，减少冗长市场综述。

### 量化因子策略包

- `.claude/plugins/stock-screener/skills/quant-factor-screener/.claude-plugin/marketplace.json` [MODIFY] 同步可复现多因子定位。
- `.claude/plugins/stock-screener/skills/quant-factor-screener/SKILL.md` [MODIFY] 从泛化叙述改为可复现输入、打分边界和结果解释。
- `.claude/plugins/stock-screener/skills/quant-factor-screener/INSTALLATION.md` [MODIFY] 修正统一安装与验证步骤。
- `.claude/plugins/stock-screener/skills/quant-factor-screener/DECISIONS.md` [MODIFY] 记录因子选择、行业中性和可得数据取舍。
- `.claude/plugins/stock-screener/skills/quant-factor-screener/references/factor-methodology.md` [MODIFY] 缩小到仓库可支撑的因子定义，避免伪精确宏观叙事。
- `.claude/plugins/stock-screener/skills/quant-factor-screener/references/data-queries.md` [MODIFY] 重写为与 API 文档一致的字段与列名。
- `.claude/plugins/stock-screener/skills/quant-factor-screener/references/output-template.md` [MODIFY] 改成因子暴露、排名原因、风险回撤三段式输出。

### 小盘成长策略包

- `.claude/plugins/stock-screener/skills/small-cap-growth-identifier/.claude-plugin/marketplace.json` [MODIFY] 同步“被忽视成长”型技能描述。
- `.claude/plugins/stock-screener/skills/small-cap-growth-identifier/SKILL.md` [MODIFY] 强化成长真实性、验证链路与被市场忽视原因。
- `.claude/plugins/stock-screener/skills/small-cap-growth-identifier/INSTALLATION.md` [MODIFY] 修正统一安装与验证步骤。
- `.claude/plugins/stock-screener/skills/small-cap-growth-identifier/DECISIONS.md` [MODIFY] 去掉模板占位，明确小盘成长的数据边界。
- `.claude/plugins/stock-screener/skills/small-cap-growth-identifier/references/small-cap-screening-criteria.md` [MODIFY] 收敛为“成长质量＋治理约束＋流动性”标准。
- `.claude/plugins/stock-screener/skills/small-cap-growth-identifier/references/data-queries.md` [MODIFY] 替换未被 API 文档证实的字段名与列名。
- `.claude/plugins/stock-screener/skills/small-cap-growth-identifier/references/output-template.md` [MODIFY] 改成“成长驱动、忽视原因、验证证据、风险清单”模板。

### 北交所策略包

- `.claude/plugins/stock-screener/skills/bse-selection-analyzer/.claude-plugin/marketplace.json` [MODIFY] 同步“可交易性优先”的技能描述。
- `.claude/plugins/stock-screener/skills/bse-selection-analyzer/SKILL.md` [MODIFY] 强化流动性门槛、执行约束、仓位建议与退出条件。
- `.claude/plugins/stock-screener/skills/bse-selection-analyzer/INSTALLATION.md` [MODIFY] 修正统一安装与验证步骤。
- `.claude/plugins/stock-screener/skills/bse-selection-analyzer/DECISIONS.md` [MODIFY] 记录北交所数据缺口、交易性优先级与方法取舍。
- `.claude/plugins/stock-screener/skills/bse-selection-analyzer/references/methodology.md` [MODIFY] 从提纲式文档升级为可执行方法论。
- `.claude/plugins/stock-screener/skills/bse-selection-analyzer/references/data-queries.md` [MODIFY] 删除或替换未在文档中发现的 `cn/company/quote/daily` 示例。
- `.claude/plugins/stock-screener/skills/bse-selection-analyzer/references/output-template.md` [MODIFY] 改成“可交易性、候选理由、执行风险”优先输出。

### ESG 策略包

- `.claude/plugins/stock-screener/skills/esg-screener/.claude-plugin/marketplace.json` [MODIFY] 同步缩边后的技能定位。
- `.claude/plugins/stock-screener/skills/esg-screener/SKILL.md` [MODIFY] 从全量 ESG 评分叙述收敛为治理代理、争议排除、外部评级补充的可执行流程。
- `.claude/plugins/stock-screener/skills/esg-screener/INSTALLATION.md` [MODIFY] 修正统一安装与验证步骤。
- `.claude/plugins/stock-screener/skills/esg-screener/DECISIONS.md` [MODIFY] 记录理杏仁无独立 ESG 评分接口这一核心边界。
- `.claude/plugins/stock-screener/skills/esg-screener/references/esg-framework.md` [MODIFY] 重写为“可得代理指标＋外部数据补充”的务实框架。
- `.claude/plugins/stock-screener/skills/esg-screener/references/data-queries.md` [MODIFY] 校正未被文档证实的字段与列名，并明确哪些能力依赖外部源。
- `.claude/plugins/stock-screener/skills/esg-screener/references/output-template.md` [MODIFY] 收敛为“排除结果、治理代理、争议监控、数据局限”模板。

## Agent Extensions

### SubAgent

- `code-explorer`
- Purpose: 跨多个目录检索模板化内容、错误路径、缺失文件引用、接口示例与索引同步点。
- Expected outcome: 形成经过仓库验证的改写清单、差异矩阵与最终影响文件范围。

### Skill

- `skill-creator`
- Purpose: 以更新现有 skill 的方式重构 6 套策略文档结构、价值主张和使用规范。
- Expected outcome: 产出统一但不模板化的 SKILL、command、reference 改写标准，并提升每个策略的独特价值与可执行性。