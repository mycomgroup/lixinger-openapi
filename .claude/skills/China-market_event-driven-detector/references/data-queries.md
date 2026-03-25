# 数据获取指南

使用 `query_tool.py` 获取 event-driven-detector 所需的数据。

---

## 事件驱动分析所需数据

### 1. 并购重组类事件

| 数据用途 | API 路径 | 说明 |
|---------|---------|------|
| 公告信息 | `cn/company/announcement` | 获取重大资产重组、并购公告 |
| 公司概况 | `cn/company/profile` | 了解公司主营业务、控股股东 |
| 财务数据 | `cn/company/fs/non_financial` | 评估标的公司盈利能力 |
| 基本面数据 | `cn/company/fundamental/non_financial` | PE、PB、市值等估值指标 |

### 2. 回购增持类事件

| 数据用途 | API 路径 | 说明 |
|---------|---------|------|
| 大股东增减持 | `cn/company/major-shareholders-shares-change` | 大股东增持/减持数据 |
| 高管增减持 | `cn/company/senior-executive-shares-change` | 董监高增减持数据 |
| 前十大股东 | `cn/company/majority-shareholders` | 股东持股变化 |
| 股东人数 | `cn/company/shareholders-num` | 筹码集中度变化 |

### 3. 指数调整类事件

| 数据用途 | API 路径 | 说明 |
|---------|---------|------|
| 指数成分股 | `cn/index/constituents` | 获取沪深300、中证500等成分股 |
| 成分股权重 | `cn/index/constituent-weightings` | 被动资金配置权重 |
| 指数基本面 | `cn/index/fundamental` | 指数整体估值水平 |
| 跟踪基金 | `cn/index/tracking-fund` | 估算被动资金规模 |

### 4. 解禁减持类事件

| 数据用途 | API 路径 | 说明 |
|---------|---------|------|
| 股本变动 | `cn/company/equity-change` | 限售股解禁数据 |
| 流通股东 | `cn/company/nolimit-shareholders` | 前十大流通股东 |
| 大宗交易 | `cn/company/block-deal` | 大宗交易减持情况 |

### 5. 国企改革/资产注入类事件

| 数据用途 | API 路径 | 说明 |
|---------|---------|------|
| 公司概况 | `cn/company/profile` | 控股股东、实控人信息 |
| 行业信息 | `cn/company/industries` | 同业竞争分析 |
| 财务数据 | `cn/company/fs/non_financial` | 资产注入前后的财务对比 |

---

## 查询示例

### 查询公司公告（并购重组筛选）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/announcement" \
  --params '{"stockCodes": ["600519"], "startDate": "2025-01-01", "endDate": "2025-12-31"}' \
  --columns "stockCode,title,publishDate,announcementType" \
  --row-filter '{"announcementType": {"contains": "重组"}}' \
  --limit 20
```

### 查询大股东增减持数据

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/major-shareholders-shares-change" \
  --params '{"stockCodes": ["000858", "300750"], "startDate": "2025-01-01"}' \
  --columns "stockCode,shareholderName,changeType,changeNum,changeRatio,avgPrice" \
  --limit 30
```

### 查询指数成分股（用于判断指数调整影响）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/constituents" \
  --params '{"date": "2025-12-31", "stockCodes": ["000300"]}' \
  --flatten "constituents" \
  --columns "stockCode,name,weight" \
  --limit 50
```

### 查询股本变动（解禁数据）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/equity-change" \
  --params '{"stockCodes": ["600519"], "startDate": "2025-01-01"}' \
  --columns "stockCode,changeDate,changeType,changeReason,beforeNum,afterNum" \
  --limit 30
```

### 查询高管增减持

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/senior-executive-shares-change" \
  --params '{"stockCodes": ["000858"], "startDate": "2025-01-01"}' \
  --columns "stockCode,executiveName,changeType,changeNum,avgPrice" \
  --limit 20
```

### 查询大宗交易

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/block-deal" \
  --params '{"stockCodes": ["600519"], "startDate": "2025-01-01"}' \
  --columns "stockCode,tradeDate,volume,price,discountRate,buyerName,sellerName" \
  --limit 30
```

---

## 参数说明

- `--suffix`: API 路径（参考上方数据用途表格）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--flatten`: 展开嵌套数组（如指数成分股）
- `--limit`: 限制返回行数

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`
