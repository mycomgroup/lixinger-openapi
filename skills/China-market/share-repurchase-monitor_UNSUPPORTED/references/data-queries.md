# 数据获取指南

使用 `query_tool.py` 获取 share-repurchase-monitor_UNSUPPORTED 所需的数据。

---

## 查询示例

### 查询K线数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company.candlestick" --params '{"stockCode": "600519", "startDate": "2024-01-01", "endDate": "2024-12-31"}' --columns "date,close,volume"
```

### 查询股票基本信息

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py --suffix "cn.company" --params '{"stockCodes": ["600519"]}' --columns "stockCode,name,ipoDate"
```

---

## 参数说明

- `--suffix`: API 路径
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 查找更多 API

```bash
# 查看 API 列表
cat skills/lixinger-data-query/SKILL.md

# 搜索关键字
grep -r "关键字" skills/lixinger-data-query/api_new/api-docs/
```

**相关文档**: `skills/lixinger-data-query/SKILL.md`
