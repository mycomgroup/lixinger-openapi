# 数据获取指南

使用 `query_tool.py` 获取 shareholder-risk-check 所需的数据。

---

## 查询示例

### 查询大股东增减持数据

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/major-shareholders-shares-change" \
  --params '{"date": "2026-02-24"}' \
  --limit 20
```

### 查询股东人数变化

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/shareholders-num" \
  --params '{"stockCode": "600519", "startDate": "2025-01-01"}' \
  --limit 20
```

### 查询前十大股东持股信息

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/majority-shareholders" \
  --params '{"stockCode": "600519", "date": "2026-02-24"}' \
  --limit 10
```

### 查询股权质押数据

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/pledge" \
  --params '{"stockCode": "600519", "startDate": "2025-01-01"}' \
  --limit 20
```

### 查询高管增减持数据

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/senior-executive-shares-change" \
  --params '{"stockCode": "600519", "startDate": "2025-01-01"}' \
  --limit 20
```

### 查询前十大流通股东持股信息

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/nolimit-shareholders" \
  --params '{"stockCode": "600519", "date": "2026-02-24"}' \
  --limit 10
```

---

## 参数说明

- `--suffix`: API 路径（参考下方可用 API 列表）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

- `cn/company/major-shareholders-shares-change` - 大股东增减持数据
- `cn/company/shareholders-num` - 股东人数变化
- `cn/company/majority-shareholders` - 前十大股东持股信息
- `cn/company/pledge` - 股权质押数据
- `cn/company/senior-executive-shares-change` - 高管增减持数据
- `cn/company/nolimit-shareholders` - 前十大流通股东持股信息

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../../plugins/query_data/lixinger-api-docs/SKILL.md`