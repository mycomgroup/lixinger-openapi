本插件为 industry-concept-research 的子 skill，无独立安装步骤。

## 前置依赖

1. **理杏仁 OpenAPI Token**：确保 `token.cfg` 中已配置有效 token
2. **query_tool.py**：路径 `.claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py` 可用
3. **AKShare（可选）**：用于概念板块资金流数据；缺少时自动降级为三维简版评分

## 使用方式

1. **通过主 Orchestrator**：`/industry-concept-research {板块名称} --mode full`（会在阶段2自动调用）
2. **通过独立命令**：`/board-crowding-risk-monitor AI算力 --type concept`
3. **外部 skill 直接调用**：当 concept-board-analyzer 判断处于"拥挤期"时，自动加载本 skill
4. **外部插件直接加载**：`Load skill: .claude/plugins/industry-concept-research/skills/board-crowding-risk-monitor/SKILL.md`
