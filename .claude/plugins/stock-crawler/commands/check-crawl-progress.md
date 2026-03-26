---
description: 查看 stock-crawler 离线抓取任务的进度
argument-hint: "[output_path]"
---

检查 `stock-crawler` 抓取任务的进度。

## 检查位置

### 1. 日志文件
```
output/<config-name>/logs/crawler-<timestamp>.log
```

### 2. 页面输出
```
output/<config-name>/pages-<timestamp>/
```

### 3. 链接文件
```
output/<config-name>/links.txt
```

### 4. Markdown 结果
```
output/<config-name>/*.md
```

## 使用示例

**检查特定配置的进度:**
```bash
cd /Users/fengzhi/Downloads/git/lixinger-openapi/.claude/stock-crawler
tail -f output/eastmoney-crawler/logs/crawler-*.log
```

**查看已生成的文件:**
```bash
ls -lah output/eastmoney-crawler/
ls -lah output/eastmoney-crawler/pages-*/
```

**统计链接数量:**
```bash
wc -l output/eastmoney-crawler/links.txt
```

## 进度报告

当用户询问进度时，报告以下内容：

1. **运行状态**: 
   - 日志文件是否还在增长
   - 是否有新的 Markdown 文件生成
   - 进程是否还在运行

2. **已完成内容**:
   - 已抓取的页面数（pages-*/ 目录中的文件数）
   - 已生成的 Markdown 文件
   - 已发现的链接数

3. **建议**:
   - 如果还在运行: "请稍后再检查"
   - 如果已完成: "可以分析结果了"
   - 如果出错: "查看日志中的错误信息"

## 示例输出

```
进度报告:
========
配置: eastmoney-plugin.json
输出目录: output/eastmoney-crawler/

状态: 运行中 ⏳
- 最新日志: logs/crawler-20260326_101530.log (正在写入)
- 已抓取页面: 23 个 (pages-20260326_101530/)
- 已发现链接: 156 个 (links.txt)
- Markdown 文件: 2 个

建议: 任务仍在进行中，请稍后再次检查
```
