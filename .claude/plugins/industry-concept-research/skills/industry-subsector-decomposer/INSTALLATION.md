本插件为 industry-concept-research 的子 skill，无独立安装步骤。

## 前置依赖

1. **理杏仁 OpenAPI Token**：确保 `token.cfg` 中已配置有效 token
2. **query_tool.py**：路径 `.claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py` 可用

## 使用方式

通过以下任一方式调用：

1. **通过主 Orchestrator**：`/industry-concept-research {行业名称} --mode detailed`
2. **通过独立命令**：`/industry-subsector-decomposer {行业名称} --level two`
3. **外部插件直接加载**：`Load skill: .claude/plugins/industry-concept-research/skills/industry-subsector-decomposer/SKILL.md`
