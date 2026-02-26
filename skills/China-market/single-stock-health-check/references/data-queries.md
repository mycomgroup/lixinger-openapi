# 数据获取指南

使用 `query_tool.py` 获取 single-stock-health-check 所需的数据。

---

## 查询示例

### 查询公司概况

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/profile" \
  --params '{"stockCodes":["600519"]}'
```

### 查询估值与交易指标

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes":["600519"],"startDate":"2023-01-01","endDate":"2026-02-23","metricsList":["pe_ttm","pb","ps_ttm","ev_ebitda_r","sp","ta","to_r"]}'
```

### 查询财报核心指标

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes":["600519"],"startDate":"2023-01-01","endDate":"2026-02-23","metricsList":["q.ps.toi.t","q.ps.np.t","q.cf.cfo.t","q.bs.ta.t","q.bs.te.t","q.ps.gp_m.t"]}'
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

- `cn/company/profile`
- `cn/company`
- `cn/company/fundamental/non_financial`
- `cn/company/fs/non_financial`
- `cn/company/operating-data`
- `cn/company/operation-revenue-constitution`
- `cn/company/majority-shareholders`
- `cn/company/major-shareholders-shares-change`
- `cn/company/senior-executive-shares-change`
- `cn/company/shareholders-num`
- `cn/company/pledge`
- `cn/company/announcement`
- `cn/company/trading-abnormal`
- `cn/company/allotment`
- `cn/company/dividend`
- `cn/company/candlestick`
- `cn/company/margin-trading-and-securities-lending`
- `cn/company/mutual-market`
- `cn/company/hot/tr_dri`
- `cn/company/block-deal`
- `cn/company/industries`
- `cn/company/indices`

---

## 查找更多 API

```bash
# 查看完整 API 列表
cat skills/lixinger-data-query/SKILL.md

# 搜索关键字
grep -r "关键字" skills/lixinger-data-query/api_new/api-docs/

# 查看具体 API 文档
cat skills/lixinger-data-query/api_new/api-docs/{api_name}.md
```

**相关文档**: `skills/lixinger-data-query/SKILL.md`
