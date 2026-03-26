---
description: 提交一个 stock-crawler 离线抓取任务
argument-hint: "[site] [target] [url-or-keyword]"
---

使用重构后的 `stock-crawler` 提交离线抓取任务。

## 工作流程

### 方式1: 交互式生成配置并提交（推荐）

如果这是新站点或需要生成新的配置：

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/stock-crawler
node src/index.js <config-file>
```

**步骤**:
1. 用户指定站点名称和种子 URL
2. 系统自动生成配置文件 `.claude/stock-crawler/config/<site-name>.json`
3. 运行 `node src/index.js config/<site-name>.json` 开始抓取

### 方式2: 使用已有配置直接抓取

如果配置文件已存在：

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/stock-crawler
node src/index.js config/eastmoney-plugin.json
```

## 可用配置

运行以下命令查看所有可用配置:
```bash
ls -la /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/stock-crawler/config/
```

常用配置:
- `eastmoney-plugin.json` - 东方财富网
- `cninfo-plugin.json` - 巨潮资讯网
- `xueqiu-plugin.json` - 雪球
- `lixinger-plugin.json` - 理杏仁

## 配置生成

如需交互式生成新的站点配置文件：

```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/stock-crawler
node src/template-pipeline-cli.js <site-url> [output-dir]
```

示例:
```bash
node src/template-pipeline-cli.js https://finance.eastmoney.com ./output/eastmoney
```

该工具会:
1. 爬取站点发现链接
2. 分析 URL 模式并分类
3. 生成 pattern 报告和模板
4. 输出到 `output/<site>/template-pipeline/`

然后手动创建配置文件:
```bash
# 基于模板创建标准配置
cp config/example.json config/my-site.json
# 编辑 my-site.json 填写站点信息
```

## 任务提交示例

**场景1: 抓取单篇新闻**
```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/stock-crawler
# 修改 eastmoney-plugin.json 的 seedUrls 为目标 URL
node src/index.js config/eastmoney-plugin.json
```

**场景2: 搜索并抓取**
```bash
# 1. 先生成搜索配置
cat > config/temp-search.json << 'EOF'
{
  "name": "temp-search",
  "seedUrls": ["https://search.eastmoney.com/?keyword=宁德时代"],
  "urlRules": {
    "include": [".*search.*eastmoney\\.com.*", ".*finance\\.eastmoney\\.com/a/.*"],
    "exclude": [".*login.*"]
  },
  "crawler": {
    "headless": true,
    "timeout": 30000,
    "waitBetweenRequests": 1000,
    "maxRetries": 3
  },
  "output": {
    "directory": "./output/temp-search",
    "format": "markdown"
  }
}
EOF

# 2. 运行抓取
node src/index.js config/temp-search.json
```

**场景3: 链接发现**
```bash
# 修改配置增加 linkDiscovery 选项
# 然后运行
node src/index.js config/eastmoney-plugin.json
```

## 输出目录结构

抓取完成后输出到:
```
output/<config-name>/
├── logs/                      # 日志文件
│   └── crawler-<timestamp>.log
├── pages-<timestamp>/         # 原始页面数据
│   ├── <url-hash>.json
│   └── ...
├── links.txt                  # 发现的链接
└── *.md                       # 生成的 Markdown 文件
```

## 后续步骤

1. **检查进度**: 查看 `output/<site>/logs/crawler-*.log`
2. **查看结果**: 查看 `output/<site>/` 下的 Markdown 文件
3. **分析内容**: 使用 `/analyze-crawl-results [output_dir]` 分析结果

## 手动配置模板

标准配置格式:
```json
{
  "name": "my-crawler",
  "site": "mysite",
  "description": "站点描述",
  "seedUrls": [
    "https://example.com/start"
  ],
  "urlRules": {
    "include": [
      ".*example\\.com/.*"
    ],
    "exclude": [
      ".*login.*",
      ".*logout.*"
    ]
  },
  "targets": {
    "article": {
      "parser": "article-parser",
      "urlPattern": ".*/article/.*",
      "description": "文章页面"
    }
  },
  "login": {
    "required": false
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

配置文件生成后，直接运行:
```bash
node src/index.js config/my-crawler.json
```
