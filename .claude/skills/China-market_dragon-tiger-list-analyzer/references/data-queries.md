# 数据获取指南

使用 `query_tool.py` 获取 dragon-tiger-list-analyzer 所需的数据。

---

## 查询示例

### 查询Cn.Company.Trading Abnormal

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/trading-abnormal" \
  --params '{"date": "2026-02-24"}' \
  --columns "date,stockCode,name,buyAmount,sellAmount,netAmount" \
  --limit 20
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

- `cn/company/trading-abnormal`

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

