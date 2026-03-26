# Stock Crawler Plugin

Website-first research crawling plugin for non-API, high-timeliness, and unstructured investment data.

## Quickstart

### 方式1: 使用已有配置直接抓取

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/stock-crawler
node src/index.js config/eastmoney-plugin.json
```

### 方式2: 交互式生成配置

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/stock-crawler
node src/template-pipeline-cli.js https://example.com ./output/example
# 然后基于生成的 pattern 创建 config/<site>.json
```

## 工作流程

1. **准备配置**: 选择已有配置或生成新配置
2. **提交任务**: 运行 `node src/index.js <config.json>`
3. **检查进度**: 查看 `output/<site>/logs/` 下的日志
4. **分析结果**: 查看生成的 Markdown 文件

## Scope and Fit

Best fit:

- website data that updates before APIs
- page-visible data that APIs do not provide
- paid API substitutes where the webpage still exposes useful information
- announcements, news, reports, and community content

Not ideal:

- standardized time series already covered by `query_data`
- workflows that require a full task scheduler inside the crawler core
- cases where you need one unified normalized schema before any analysis

## Architecture

**重构后的架构**

目录结构:
```
.claude/stock-crawler/          # Crawler 核心
├── src/
│   ├── index.js               # CLI 入口: node src/index.js <config>
│   ├── crawler-main.js        # 核心逻辑
│   ├── template-pipeline-cli.js  # 配置生成工具
│   └── ...
├── config/                    # 站点配置文件
│   ├── eastmoney-plugin.json
│   ├── xueqiu-plugin.json
│   └── ...
└── output/                    # 抓取输出目录

.claude/plugins/stock-crawler/  # Plugin 命令文档
├── commands/
│   ├── submit-crawl-task.md   # 任务提交流程
│   ├── check-crawl-progress.md
│   └── analyze-crawl-results.md
└── README.md
```

## Commands

| Command | Description |
|---------|-------------|
| `/submit-crawl-task` | 提交抓取任务（生成配置 + 运行 crawler） |
| `/check-crawl-progress [output_path]` | 检查抓取进度和日志 |
| `/analyze-crawl-results [output_dir]` | 分析生成的 Markdown 结果 |

## Configuration Generator

### 方式1: Template Pipeline（自动发现）

```bash
node src/template-pipeline-cli.js <site-url> [output-dir]
```

示例:
```bash
node src/template-pipeline-cli.js https://finance.eastmoney.com ./output/eastmoney
```

输出:
- `output/<site>/template-pipeline/links.txt` - 发现的链接
- `output/<site>/template-pipeline/url-patterns.json` - URL 模式分析
- `output/<site>/template-pipeline/classified-patterns.json` - 分类后的模式
- `output/<site>/template-pipeline/templates/*.json` - 生成的模板

### 方式2: 手动创建配置

复制 example.json 并修改:

```bash
cp config/example.json config/my-site.json
# 编辑 config/my-site.json
```

标准配置格式:
```json
{
  "name": "my-crawler",
  "site": "mysite",
  "description": "站点描述",
  "seedUrls": ["https://example.com/start"],
  "urlRules": {
    "include": [".*example\\.com/.*"],
    "exclude": [".*login.*"]
  },
  "crawler": {
    "headless": true,
    "timeout": 30000,
    "waitBetweenRequests": 1000,
    "maxRetries": 3
  },
  "output": {
    "directory": "./output/my-crawler",
    "format": "markdown"
  }
}
```

## Running Crawler

### 基本用法

```bash
# 使用已有配置
node src/index.js config/eastmoney-plugin.json

# 使用自定义配置
node src/index.js config/my-site.json
```

### CLI 参数

```bash
node src/index.js --help
```

### 环境变量

```bash
DEBUG=1 node src/index.js config/my-site.json  # 启用调试模式
```

## Output Directory Structure

```
output/<config-name>/
├── logs/
│   └── crawler-20260326_101530.log
├── pages-20260326_101530/
│   ├── a1b2c3d4.json
│   └── ...
├── links.txt
└── eastmoney-plugin_news_article_2026-03-26T10-16-02.md
```

## Available Configurations

查看所有可用配置:
```bash
ls -la config/
```

常用配置:
- `eastmoney-plugin.json` - 东方财富网（财经新闻、个股数据）
- `cninfo-plugin.json` - 巨潮资讯网（上市公司公告）
- `xueqiu-plugin.json` - 雪球（投资者社区）
- `lixinger-plugin.json` - 理杏仁（金融数据）

## Progress Checking

Preferred progress sources:

- `output/<config-name>/logs/crawler-*.log`
- `output/<config-name>/pages-*/`
- `output/<config-name>/links.txt`

Practical interpretation:

- growing `logs/` means the crawl is still active
- new Markdown file means a result is already analyzable
- changing `links.txt` indicates URL-level progress

## Analyze While Running

Do not wait for a full perfect end state before analysis.

Good pattern:

1. search or discover candidate links
2. crawl high-value pages
3. analyze Markdown immediately
4. resubmit refined tasks if needed

## Task Output Convention

### Running

```json
{
  "task_id": "stock_crawler_20260325_101530_eastmoney_news_article",
  "status": "running",
  "config": "config/eastmoney-plugin.json",
  "submitted_at": "2026-03-25T10:15:30+08:00",
  "artifacts_dir": "output/eastmoney-crawler/",
  "message": "Crawler started. Check logs for progress."
}
```

### Completed

```json
{
  "task_id": "stock_crawler_20260325_101530_eastmoney_news_article",
  "status": "succeeded",
  "config": "config/eastmoney-plugin.json",
  "artifacts_dir": "output/eastmoney-crawler/",
  "markdown_files": [
    "output/eastmoney-crawler/eastmoney-crawler_2026-03-25T10-16-02.md"
  ],
  "message": "Crawling completed successfully!"
}
```
