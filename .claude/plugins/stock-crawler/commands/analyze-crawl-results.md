---
description: 分析 stock-crawler 已产出的 Markdown 抓取结果
description-en: Analyze stock-crawler markdown outputs from page directories
argument-hint: "[output_dir or site_name]"
---

分析 `stock-crawler` 已抓取并生成的 Markdown 文件，支持从 page 目录批量读取和分析。

## 工作流程

1. **定位 Page 目录**
   - 如果参数是站点名称（如 `lixinger-crawler`），自动查找 `output/<site>/pages-*/`
   - 如果参数是完整路径，直接使用该路径
   - 扫描所有 `pages-<timestamp>/` 子目录

2. **收集 Markdown 文件**
   - 遍历 page 目录及其子目录
   - 收集所有 `.md` 文件（不包括 `_index.md` 等元数据文件）
   - 记录文件路径、大小、修改时间

3. **执行分析**
   - 读取每个 Markdown 文件内容
   - 提取关键信息：标题、日期、实体、主题
   - 统计：文件数量、总字数、平均文件大小
   - 识别重复主题和异常内容

4. **生成报告**
   - 汇总统计信息
   - 列出所有抓取的文档
   - 识别数据质量问题
   - 建议后续操作

## 参数格式

```
# 按站点名称分析
/analyze-crawl-results lixinger-crawler

# 按完整路径分析  
/analyze-crawl-results .claude/stock-crawler/output/lixinger-crawler/pages-20260325-201203

# 分析最新的一次抓取
/analyze-crawl-results .claude/stock-crawler/output/lixinger-crawler
```

## 分析维度

### 基础统计
- 文件总数
- 总字符数 / 总词数
- 平均文件大小
- 时间范围（最早/最晚）

### 内容分析
- 标题提取与去重
- 实体识别（股票代码、公司名称）
- 主题聚类
- 关键词频率

### 质量检查
- 空文件或超小文件
- 重复内容
- 抓取失败的标记
- 格式异常

### 数据洞察
- 热门主题排行
- 时间分布
- 数据来源统计
- 内容类型分布

## 输出示例

```json
{
  "scan_summary": {
    "site": "lixinger-crawler",
    "page_dir": "pages-20260325-201203",
    "total_files": 156,
    "total_chars": 1250000,
    "time_range": {
      "earliest": "2026-03-25T20:12:03Z",
      "latest": "2026-03-25T20:54:12Z"
    }
  },
  "content_analysis": {
    "titles": [...],
    "entities": [...],
    "themes": [...]
  },
  "quality_issues": [...],
  "recommendations": [...]
}
```

## 实现说明

底层调用技能：`stock-crawler-analyzer`

分析流程:
1. 使用 `discoverPageDirectories()` 查找所有 page 目录
2. 使用 `collectMarkdownFiles()` 收集所有 md 文件
3. 使用 `analyzeMarkdownContent()` 分析内容
4. 生成结构化报告

## 注意事项

- 大型站点可能有数百个文件，分析需要时间
- 建议先查看 `pages-*/` 目录结构了解数据分布
- 可配合 `/check-crawl-progress` 确认抓取完成度
- 如需深度分析特定文件，使用技能 `stock-crawler-analyzer` 的专项功能

## 相关命令

- `/submit-crawl-task` - 提交新的抓取任务
- `/check-crawl-progress` - 检查抓取进度
- `/skills stock-crawler-analyzer` - 使用数据分析技能
