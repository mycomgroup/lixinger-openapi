# 数据获取指南

使用 `query_tool.py` 获取 financial-statement-analyzer 所需的数据。

---

## 查询示例

### 查询Us.Index.Fundamental（仅供参考，China-market 建议使用中国数据）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "us/index/fundamental" \
  --params '{"date":"2026-02-24","stockCodes":[".INX"],"metricsList":["pe_ttm.mcw","pb.mcw","dyr.mcw","mc"]}' \
  --columns "date,stockCode,pe_ttm.mcw,pb.mcw,dyr.mcw,mc" \
  --limit 20
```

**注意**: 本 skill 为 China-market，建议优先使用中国公司和指数数据。

### 查询Cn.Company.Fs.Non Financial

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["600519"], "startDate": "2025-01-01", "endDate": "2026-02-24", "metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.ps.gp_m.t"]}' \
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

- `cn/company/fs/non_financial`: 中国公司财务报表
- `cn/company/fundamental/non_financial`: 中国公司基本面数据

### 查询中国公司财务报表

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes":["600519"],"startDate":"2021-01-01","endDate":"2026-02-27","metricsList":["q.ps.toi.t","q.ps.np.t","q.ps.gp_m.t","q.bs.ta.t","q.bs.tl.t"]}' \
  --columns "date,stockCode,q.ps.toi.t,q.ps.np.t,q.ps.gp_m.t" \
  --limit 20
```

### 查询估值数据（用于财务质量评估）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes":["600519"],"date":"2026-02-24","metricsList":["pe_ttm","pb"]}' \
  --columns "stockCode,name,pe_ttm,pb"
```

### 查询股东数据（用于股权结构分析）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/major-shareholders-shares-change" \
  --params '{"stockCode":"600519","startDate":"2023-01-01"}' \
  --columns "date,shareholderName,changeReason,changeAmount,sharesRatio"
```

### 查询质押数据（用于风险评估）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/pledge" \
  --params '{"stockCode":"600519","startDate":"2023-01-01"}' \
  --columns "date,pledgeRatio,pledgor,pledgee,pledgeShares"
```

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
