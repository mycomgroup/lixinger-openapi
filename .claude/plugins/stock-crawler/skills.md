---
description: stock-crawler 数据分析处理技能
description-en: Data analysis skill for stock-crawler outputs
---

# Stock Crawler Analyzer Skill

用于分析 stock-crawler 抓取结果的数据处理技能。提供从 page 目录发现、Markdown 文件收集到内容深度分析的全套工具。

## 核心功能

### 1. 目录发现 (discoverPageDirectories)

自动发现并扫描 output 目录下的所有 page 目录。

**输入:**
- `basePath`: 基础路径（如 `.claude/stock-crawler/output/lixinger-crawler`）
- `siteName`: 可选，站点名称过滤

**输出:**
```javascript
[
  {
    "site": "lixinger-crawler",
    "pageDir": "pages-20260325-201203",
    "fullPath": ".../output/lixinger-crawler/pages-20260325-201203",
    "createdAt": "2026-03-25T20:12:03Z",
    "fileCount": 156
  }
]
```

### 2. 文件收集 (collectMarkdownFiles)

递归收集 page 目录中的所有 Markdown 文件。

**输入:**
- `pageDir`: page 目录路径
- `excludePatterns`: 排除模式数组（如 `["*_index.md", "*summary.md"]`）

**输出:**
```javascript
[
  {
    "path": ".../A股_PB_市场估值_模型_analytics.md",
    "filename": "A股_PB_市场估值_模型_analytics.md",
    "size": 1988,
    "modifiedAt": "2026-03-25T20:22:10Z",
    "category": "A股_PB_市场估值_模型_analytics"  // 子目录名
  }
]
```

### 3. 内容分析 (analyzeMarkdownContent)

深度分析 Markdown 文件内容，提取结构化信息。

**输入:**
- `filePath`: Markdown 文件路径
- `analysisType`: 分析类型（'basic' | 'entities' | 'full'）

**输出:**
```javascript
{
  "metadata": {
    "title": "A股市净率估值模型分析",
    "wordCount": 1250,
    "lineCount": 45,
    "hasTable": true,
    "hasCode": false
  },
  "entities": {
    "stockCodes": ["000001", "600000"],
    "companies": ["平安银行", "浦发银行"],
    "industries": ["银行", "金融"]
  },
  "structure": {
    "headings": ["# 标题", "## 市场概况"],
    "tables": 2,
    "links": 5
  },
  "summary": "文本内容摘要..."
}
```

### 4. 批量分析 (batchAnalyze)

批量分析整个 page 目录，生成综合报告。

**输入:**
- `pageDir`: page 目录路径
- `options`: 配置选项

**输出:**
```javascript
{
  "overview": {
    "totalFiles": 156,
    "totalSize": 5242880,
    "timeRange": {
      "start": "2026-03-25T20:12:03Z",
      "end": "2026-03-25T20:54:12Z"
    }
  },
  "contentStats": {
    "totalWords": 1250000,
    "avgWordsPerFile": 8012,
    "filesWithTables": 45,
    "filesWithImages": 12
  },
  "entitySummary": {
    "uniqueStocks": 89,
    "uniqueCompanies": 156,
    "uniqueIndustries": 28
  },
  "themes": [
    {"name": "估值分析", "count": 23, "files": [...]},
    {"name": "财报数据", "count": 18, "files": [...]}
  ],
  "quality": {
    "emptyFiles": 2,
    "duplicateTitles": 3,
    "errors": []
  }
}
```

## 使用方法

### 基本用法

```javascript
// 发现所有 page 目录
const pageDirs = await skill.discoverPageDirectories(
  '.claude/stock-crawler/output/lixinger-crawler'
);

// 收集最新 page 目录的 Markdown 文件
const latestDir = pageDirs[0];
const files = await skill.collectMarkdownFiles(latestDir.fullPath);

// 批量分析
const report = await skill.batchAnalyze(latestDir.fullPath);
console.log(report);
```

### 高级用法

```javascript
// 按类别分析
const categoryReport = await skill.analyzeByCategory(
  latestDir.fullPath,
  ['analytics', '百科', '财报']
);

// 提取时间序列数据
const timeSeries = await skill.extractTimeSeries(latestDir.fullPath);

// 搜索特定内容
const searchResults = await skill.searchInPages(
  latestDir.fullPath,
  '市盈率',
  { caseSensitive: false }
);

// 生成对比报告（对比两个 page 目录）
const diffReport = await skill.comparePageDirs(
  'pages-20260325-201203',
  'pages-20260324-180530'
);
```

## 数据分析模块

### 实体提取器 (EntityExtractor)

- **股票代码**: 识别 A 股、港股、美股代码格式
- **公司名称**: 匹配已知的上市公司名称
- **行业标签**: 识别行业分类关键词
- **时间日期**: 提取报告期、公告日等

### 主题聚类 (ThemeCluster)

- 基于标题和内容的关键词聚类
- 使用 TF-IDF 识别文档主题
- 生成主题-文档映射关系

### 质量检查器 (QualityChecker)

- 检测空文件或极小文件（< 100 字节）
- 识别重复内容（基于标题或内容哈希）
- 检查格式错误（缺少标题、断链等）
- 验证数据完整性

### 统计生成器 (StatsGenerator)

- 文件数量和时间分布
- 内容长度统计
- 结构元素统计（表格、代码块、图片）
- 实体出现频率

## 报告格式

### 标准分析报告

```markdown
# Stock Crawler 分析报告

## 概览
- 站点: lixinger-crawler
- Page 目录: pages-20260325-201203
- 文件总数: 156
- 分析时间: 2026-03-26T10:30:00Z

## 内容统计
- 总字数: 1,250,000
- 平均文件大小: 8.5 KB
- 包含表格的文件: 45 (28.8%)
- 时间跨度: 2026-03-25 20:12 ~ 20:54

## 主题分布
1. 估值分析 (23 文件)
2. 财报数据 (18 文件)
3. 市场概况 (15 文件)
...

## 提取的实体
- 涉及股票: 89 只
- 公司数量: 156 家
- 行业分布: 28 个行业

## 质量检查
- ⚠️ 空文件: 2 个
- ⚠️ 重复标题: 3 个
- ✅ 格式正确: 151 个

## 建议
1. 清理空文件并重新抓取
2. 合并重复内容
3. 重点关注"估值分析"主题，数据最丰富
```

## 集成方式

### 作为 Skill 使用

```yaml
# 在 agent 配置中引用
skills:
  - stock-crawler-analyzer
```

### 作为模块导入

```javascript
import { StockCrawlerAnalyzer } from './skills/stock-crawler-analyzer';

const analyzer = new StockCrawlerAnalyzer({
  outputBasePath: '.claude/stock-crawler/output'
});

const report = await analyzer.analyze('lixinger-crawler');
```

## 配置选项

```javascript
{
  // 文件收集
  "excludePatterns": ["*_index.md", "*summary.md", ".*"],
  "includeSubdirs": true,
  "maxFileSize": 10485760,  // 10MB
  
  // 内容分析
  "analysisDepth": "full",  // 'basic' | 'standard' | 'full'
  "extractEntities": true,
  "detectLanguage": true,
  
  // 主题聚类
  "clusterThemes": true,
  "minClusterSize": 3,
  "maxClusters": 20,
  
  // 质量检查
  "checkQuality": true,
  "minFileSize": 100,
  "detectDuplicates": true,
  
  // 报告生成
  "reportFormat": "markdown",  // 'markdown' | 'json' | 'both'
  "includeRawData": false,
  "saveReport": true
}
```

## 注意事项

1. **性能考虑**: 大量文件（>1000）时，建议使用分批处理
2. **内存管理**: 大文件分析时注意内存使用，可设置 `maxFileSize` 限制
3. **并发控制**: 默认并发数为 5，可通过配置调整
4. **缓存机制**: 分析结果会自动缓存，避免重复计算

## 故障排查

### 找不到 page 目录
- 确认 output 路径正确
- 检查是否有抓取任务已完成并生成 pages-* 目录

### 文件读取失败
- 检查文件权限
- 确认文件编码为 UTF-8
- 查看是否有损坏的文件

### 分析结果为空
- 确认 Markdown 文件有实际内容
- 检查 `excludePatterns` 是否过于严格
- 验证文件是否被正确识别为 Markdown

## 版本历史

- **v1.0**: 初始版本，支持基础的目录发现和文件收集
- **v1.1**: 增加内容分析和实体提取
- **v1.2**: 添加主题聚类和质量检查
- **v1.3**: 支持批量分析和对比功能

## 相关资源

- [stock-crawler README](../README.md)
- [analyze-crawl-results 命令](./commands/analyze-crawl-results.md)
- [Crawler 核心文档](../../../stock-crawler/README.md)
