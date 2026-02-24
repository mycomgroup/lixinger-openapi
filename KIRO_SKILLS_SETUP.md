# Kiro Skills 设置说明

## 已完成的设置

### 1. Skills 目录

已将 skills 目录链接到 Kiro 的 skills 目录：

```bash
.kiro/skills/
├── China-market -> /Users/fengzhi/Downloads/git/lixinger-openapi/skills/China-market
└── lixinger-data-query -> /Users/fengzhi/Downloads/git/lixinger-openapi/skills/lixinger-data-query
```

### 2. Steering 文件

已将 steering 文件添加到 Kiro：

```bash
.kiro/steering/
└── lixinger-skills.md  # 理杏仁金融分析技能包指南
```

**Steering 文件作用**：
- 自动加载到每次对话的上下文中
- 提供 56 个金融分析技能的完整说明
- 包含使用方式、示例场景、数据限制等信息
- 帮助 Kiro 自动选择合适的 skill 来回答问题

## 可用的 Skills

### 1. lixinger-data-query
理杏仁数据查询工具，提供 162 个 API 接口，覆盖 A股、港股、美股、宏观数据。

**使用方式**：
```
使用 lixinger-data-query skill 查询贵州茅台的分红数据
```

### 2. China-market Skills (56 个)

包括：
- dividend-corporate-action-tracker - 分红与配股跟踪
- shareholder-risk-check - 股东风险检查
- block-deal-monitor - 大宗交易监控
- hot-rank-sentiment-monitor - 市场热度监控
- financial-statement-analyzer - 财务报表分析
- ... 等 51 个其他 skills

**使用方式**：
```
使用 dividend-corporate-action-tracker skill 分析贵州茅台的分红历史
```

## 如何在 Kiro 中使用

### 方法 1: 直接调用 skill

在 Kiro 对话中，直接提及 skill 名称：

```
请使用 lixinger-data-query skill 查询贵州茅台的基本信息
```

### 方法 2: 让 Kiro 自动选择

描述你的需求，Kiro 会自动选择合适的 skill：

```
我想查询贵州茅台最近的分红数据
```

Kiro 会自动使用 `dividend-corporate-action-tracker` skill。

### 方法 3: 查看可用 skills

```
列出所有可用的 China-market skills
```

## 测试 Skills

### 测试 lixinger-data-query

```
使用 lixinger-data-query skill 查询贵州茅台（600519）的股票基本信息
```

### 测试 dividend-corporate-action-tracker

```
使用 dividend-corporate-action-tracker skill 分析贵州茅台的分红历史
```

### 测试 shareholder-risk-check

```
使用 shareholder-risk-check skill 检查贵州茅台的股东结构风险
```

## Skills 目录结构

```
skills/
├── lixinger-data-query/
│   ├── SKILL.md                    # Skill 主文档
│   ├── LLM_USAGE_GUIDE.md          # LLM 使用指南
│   ├── EXAMPLES.md                 # 查询示例
│   ├── scripts/
│   │   └── query_tool.py           # 查询工具
│   └── api_new/
│       └── api-docs/               # 162 个 API 文档
│
└── China-market/
    ├── dividend-corporate-action-tracker/
    │   ├── SKILL.md                # Skill 主文档
    │   └── references/
    │       ├── data-queries.md     # 数据获取指南（精简版）
    │       ├── methodology.md      # 方法论
    │       └── output-template.md  # 输出模板
    │
    ├── shareholder-risk-check/
    │   └── ...
    │
    └── ... (其他 54 个 skills)
```

## 注意事项

1. **数据获取**：所有 skills 都依赖 `lixinger-data-query` 的 `query_tool.py` 来获取数据
2. **Token 配置**：需要在项目根目录配置 `token.cfg` 文件
3. **Python 环境**：需要激活 `.venv` 虚拟环境
4. **数据限制**：理杏仁免费版有 API 调用次数限制

## 故障排除

### Skills 未被识别

如果 Kiro 无法识别 skills，检查：

1. 符号链接是否正确：
```bash
ls -la .kiro/skills/
```

2. SKILL.md 文件是否存在：
```bash
ls skills/lixinger-data-query/SKILL.md
ls skills/China-market/dividend-corporate-action-tracker/SKILL.md
```

3. 重启 Kiro

### 数据查询失败

如果数据查询失败，检查：

1. Token 是否配置：
```bash
cat token.cfg
```

2. Python 环境是否激活：
```bash
which python3
```

3. 依赖是否安装：
```bash
pip list | grep lixinger
```

## 相关文档

- **Skills 优化报告**: `DATA_QUERIES_CLEANUP_REPORT.md`
- **最终总结**: `FINAL_DATA_QUERIES_SUMMARY.md`
- **查询工具文档**: `skills/lixinger-data-query/SKILL.md`
- **LLM 使用指南**: `skills/lixinger-data-query/LLM_USAGE_GUIDE.md`

---

**设置时间**: 2026-02-23  
**设置者**: Kiro AI
