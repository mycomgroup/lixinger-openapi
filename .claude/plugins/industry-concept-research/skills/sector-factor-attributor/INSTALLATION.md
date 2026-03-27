本插件为 industry-concept-research 的子 skill，无独立安装步骤。

## 前置依赖

1. **理杏仁 OpenAPI Token**：确保 `token.cfg` 中已配置有效 token
2. **query_tool.py**：路径 `.claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py` 可用

## 数据可得性说明

- **估值数据（必需）**：理杏仁 API 完全支持，PE/PB 历史序列可直接获取
- **盈利数据（可选）**：`cn/industry/fs/sw_2021/hybrid` 仅对部分行业有数据，多数行业会触发 PARTIAL 归因

## 使用方式

1. **通过主 Orchestrator**：`/industry-concept-research {行业名称} --mode detailed`
2. **通过独立命令**：`/sector-factor-attributor {行业名称} --period 3m`
3. **外部插件直接加载**：`Load skill: .claude/plugins/industry-concept-research/skills/sector-factor-attributor/SKILL.md`
