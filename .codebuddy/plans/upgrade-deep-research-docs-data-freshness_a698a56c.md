---
name: upgrade-deep-research-docs-data-freshness
overview: 升级 `.claude/plugins/deep-research` 文档，消除“模型补数/示例即事实”的歧义，明确必须优先抓取当下可验证数据并标注时间与来源。
todos:
  - id: audit-doc-gaps
    content: 使用 [subagent:code-explorer] 盘点 deep-research 文档冲突与遗漏
    status: completed
  - id: align-entry-docs
    content: 统一 README 与 commands，写明先采集最新数据再推断
    status: completed
    dependencies:
      - audit-doc-gaps
  - id: harden-skill-rules
    content: 修订 CPE/FQE/QA SKILL，固化来源、日期、降级约束
    status: completed
    dependencies:
      - align-entry-docs
  - id: update-playbook-examples
    content: 增强 sourcing playbook 与示例注释，声明示例不可当事实
    status: completed
    dependencies:
      - harden-skill-rules
  - id: final-consistency-check
    content: 使用 [subagent:code-explorer] 全量复核并输出检查清单
    status: completed
    dependencies:
      - update-playbook-examples
---

## User Requirements

- 升级 `.claude/plugins/deep-research` 内文档，解决“未优先获取当下可验证数据、直接用模型记忆/估算补全”的问题。
- 仅做文档与说明升级，不改执行脚本逻辑。
- 将“先采集最新可验证数据，再生成结构化结果，再推断结论”写成明确且统一的流程约束。
- 明确示例数据仅用于结构示意，不能直接当作当前事实复用。
- 明确时间敏感数字必须带 `as_of_date` 与来源；无可验证新数据时必须降级为 `tentative` 或 `null` 并说明缺口。

## Product Overview

- 本次交付是 deep-research 插件的“证据优先”文档规范升级，覆盖入口 README、命令说明、技能说明、取证手册与示例注释。
- 文档呈现上将统一增加“硬约束/流程顺序/降级规则”描述块，使使用者一眼看到先后顺序与不可越过的红线。

## Core Features

- 统一工作流：数据采集（结构化+网页）→ 结构化 JSON → QA → 结论输出。
- 统一证据规则：来源分级、日期标注、事实与推断分层、估算显式标记。
- 统一降级策略：缺少可验证新数据时，禁止伪造确定性数字，改为 `tentative`/`null`。
- 统一示例边界：样例仅示意字段与证据链写法，不代表实时事实。

## Tech Stack Selection

- 现有项目栈沿用：Markdown 文档体系（README/commands/SKILL/references）+ JSON 示例文件。
- 不引入新框架、不改 Python 执行逻辑，仅做文档层规范对齐。

## Implementation Approach

- 采用“入口到细则”的分层统一策略：先修入口文档与命令描述，再修技能规范与取证手册，最后修示例注释，确保全链路口径一致。
- 关键决策：复用已有 `web-grounded-sourcing-playbook` 与现有 CPE/FQE/QA 结构，不新增并行规范，避免双标准。
- 性能与可靠性：本次为文档改造，主要成本是多文件一致性校对；通过集中规则模板降低遗漏与回滚风险。

## Implementation Notes (Execution Details)

- 仅修改 `.claude/plugins/deep-research` 下文档与示例说明字段，控制影响面。
- 保持既有命令名、目录结构、契约字段语义不破坏，确保向后兼容。
- 对“实时性、来源、降级”三类规则使用同一措辞模板，避免 README/commands/SKILL 互相矛盾。
- 不新增与任务无关重构，不调整脚本参数与 QA 代码行为。

## Architecture Design

- 沿用现有文档架构链路：

1. 入口层：`README.md`、`commands/*.md`
2. 规范层：`skills/*/SKILL.md`
3. 取证细则层：`references/web-grounded-sourcing-playbook.md`
4. 示例层：`examples/catl_300750/*.json`

- 本次改动目标是让四层在“先证据后推断、时间戳与来源必填、缺失即降级”上完全一致。

## Directory Structure

## Directory Structure Summary

本次为现有 deep-research 插件的文档一致性升级，重点修订入口说明、命令语义、技能约束、取证手册与示例注释，确保“实时数据优先”可执行。

- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/deep-research/README.md`  # [MODIFY] 插件入口说明；统一声明 evidence-first 顺序、示例不可当实时事实、缺失数据降级策略。
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/deep-research/commands/competitive-positioning.md`  # [MODIFY] 命令描述；去除仅 scaffold 语义，明确先采集最新可验证数据再生成四个 JSON。
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/deep-research/commands/financial-quality.md`  # [MODIFY] 命令约束；强化 `as_of_date`、来源口径、无新数据时的输出边界。
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/deep-research/commands/deep-research-qa.md`  # [MODIFY] QA 命令说明；补充对来源完整性与时间敏感字段核验的使用指引。
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/deep-research/skills/competitive-positioning-engine/SKILL.md`  # [MODIFY] CPE 主规范；消除 manual-first 与 evidence-first 表述冲突，固化硬约束。
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/deep-research/skills/financial-quality-engine/SKILL.md`  # [MODIFY] FQE 规范；补齐实时数据优先与来源可回溯要求。
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/deep-research/skills/deep-research-qa/SKILL.md`  # [MODIFY] QA 规范；明确对 `as_of_date`/source/tentative 的检查期望与判定口径。
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/deep-research/skills/competitive-positioning-engine/references/web-grounded-sourcing-playbook.md`  # [MODIFY] 取证手册；把建议项升级为可执行硬规则与缺失处理流程。
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/deep-research/skills/competitive-positioning-engine/examples/catl_300750/market_map.json`  # [MODIFY] 示例注释；强化“仅示意、需按最新来源重取”提示。
- `/Users/fengzhi/Downloads/git/lixinger-openapi/.claude/plugins/deep-research/skills/competitive-positioning-engine/examples/catl_300750/claims.json`  # [MODIFY] 示例注释/字段说明；明确估算与披露值边界及降级示例。

## Agent Extensions

- **SubAgent: code-explorer**
- **Purpose**: 跨多文件快速检索 deep-research 文档中的口径冲突、遗漏字段与不一致措辞。
- **Expected outcome**: 产出可执行的修改清单，确保 README、commands、SKILL、playbook、示例注释规则一致。