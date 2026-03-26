---
description: 直接运行 stock-crawler 抓取任务（本地执行 npm run crawl）
argument-hint: "[config-name]"
---

直接运行本地 stock-crawler 抓取任务，执行 `npm run crawl config/<config-name>.json`。

工作流程：

1. 检查配置文件是否存在 `config/<config-name>.json`
2. 在 stock-crawler 目录下执行 `npm run crawl config/<config-name>.json`
3. 监控执行输出并返回结果

支持的配置文件：
- `lixinger` - 理杏仁数据抓取
- `eastmoney-plugin` - 东方财富数据抓取
- `cninfo-plugin` - 巨潮资讯数据抓取
- `xueqiu-plugin` - 雪球数据抓取
- 其他 config/ 目录下的配置文件

示例：
`/run-crawl-task lixinger`
