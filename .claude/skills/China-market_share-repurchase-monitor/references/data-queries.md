# 数据获取指南

使用 `query_tool.py` 获取 share-repurchase-monitor 所需的数据。

---

## 查询示例

### 查询K线数据

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py --suffix "cn/company/candlestick" --params '{"stockCode": "600519", "type": "normal", "startDate": "2026-01-01", "endDate": "2026-02-24"}' --columns "date,close,volume"
```

### 查询股票基本信息

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py --suffix "cn/company" --params '{"stockCodes": ["600519"]}' --columns "stockCode,name,ipoDate"
```

### 查询港股回购数据（推荐用于港股分析）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py --suffix "hk/company/repurchase" --params '{"stockCode": "00700", "startDate": "2026-01-01", "endDate": "2026-02-24"}' --columns "methodOfRepurchase,highestPrice,lowestPrice,avgPrice,num,totalPaid"
```

### 查询A股回购公告（通过公告API过滤获取）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py --suffix "cn/company/announcement" --params '{"stockCode": "600519", "startDate": "2026-01-01", "endDate": "2026-02-24"}' --columns "date,linkText,linkUrl,types" --row-filter '{"types": {"contains": "srp"}}'
```

---

## 参数说明

- `--suffix`: API 路径
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 可用API参考

### 港股回购专用API
- **路径**: `hk/company/repurchase`
- **说明**: 获取港股具体回购交易数据，包括回购方式、价格、数量等详细信息
- **关键字段**: methodOfRepurchase, highestPrice, lowestPrice, avgPrice, num, totalPaid

### A股回购信息获取方式
- **路径**: `cn/company/announcement` 
- **说明**: 通过公告API获取，需要过滤 types 字段包含 "srp" (回购) 的公告
- **关键字段**: date (公告日期), linkText (公告标题), linkUrl (公告链接), types (公告类型)

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

