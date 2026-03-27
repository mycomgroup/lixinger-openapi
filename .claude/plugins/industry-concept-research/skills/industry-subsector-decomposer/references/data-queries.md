# 数据获取指南 — industry-subsector-decomposer

使用 `query_tool.py` 获取行业细分拆解所需数据。

---

## API 清单

### 1. 获取申万二级行业列表

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry" \
  --params '{"source": "sw", "level": "two"}' \
  --columns "stockCode,name" \
  --limit 200
```

**用途**：获取所有申万二级行业代码和名称，从中筛选属于目标一级行业的细分列表。

---

### 2. 获取申万三级行业列表（可选）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry" \
  --params '{"source": "sw", "level": "three"}' \
  --columns "stockCode,name" \
  --limit 500
```

**用途**：获取申万三级行业代码，覆盖更细粒度的细分行业。

---

### 3. 获取细分行业当日基本面数据（批量快照）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"date": "2026-03-27", "stockCodes": ["360000","361000","362000","363000","364000"], "metricsList": ["pe_ttm.mcw","pe_ttm.y10.mcw.cvpos","pb.mcw","mc","to_r","ta"]}' \
  --columns "stockCode,pe_ttm.mcw,pe_ttm.y10.mcw.cvpos,pb.mcw,mc,to_r,ta" \
  --limit 50
```

**用途**：批量获取多个细分行业的当日估值与成交数据。

**注意**：
- `stockCodes` 需替换为目标一级行业下的实际细分行业代码列表
- 使用 `date` 参数时支持批量查询
- `pe_ttm.y10.mcw.cvpos`：PE 10年历史分位数（0-1，越低越低估）

---

### 4. 获取细分行业历史市值（计算涨跌幅）

**4.1 近1个月起始市值**

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"date": "2026-02-27", "stockCodes": ["361000"], "metricsList": ["mc"]}' \
  --columns "stockCode,date,mc" \
  --limit 1
```

**4.2 近3个月起始市值**

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"date": "2025-12-27", "stockCodes": ["361000"], "metricsList": ["mc"]}' \
  --columns "stockCode,date,mc" \
  --limit 1
```

**注意**：使用 `date` 参数（非 startDate）时，每次只能查一个代码。若批量计算多个细分行业涨跌幅，需循环查询：

```bash
for code in 361000 362000 363000 364000; do
  python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
    --suffix "cn/industry/fundamental/sw_2021" \
    --params "{\"date\": \"2026-02-27\", \"stockCodes\": [\"$code\"], \"metricsList\": [\"mc\"]}" \
    --columns "stockCode,mc" \
    --limit 1
done
```

---

### 5. 获取行业成分股（用于辅助验证龙头）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/constituents/sw_2021" \
  --params '{"stockCodes": ["361000"]}' \
  --columns "stockCode,name,mc" \
  --limit 20
```

**用途**：获取特定细分行业的成分股列表，识别龙头公司（市值最大的Top 3）。

---

## 涨跌幅计算公式

```python
# 细分行业近1个月涨跌幅
perf_1m = (mc_today - mc_1m_ago) / mc_1m_ago * 100

# 细分行业近3个月涨跌幅
perf_3m = (mc_today - mc_3m_ago) / mc_3m_ago * 100

# 一级行业总市值（用于计算贡献度）
total_mc = sum([mc for each subsector])

# 贡献度
contribution = perf_subsector × (mc_subsector / total_mc)
```

---

## 申万行业代码参考（电子行业细分示例）

| 行业名称 | 申万代码 | 层级 |
|---------|---------|------|
| 电子 | 360000 | 一级 |
| 半导体 | 361000 | 二级 |
| 消费电子 | 362000 | 二级 |
| 元件 | 363000 | 二级 |
| 光学光电子 | 364000 | 二级 |
| 其他电子 | 365000 | 二级 |

> 实际查询时，先通过 API 1 获取完整二级行业列表，再筛选目标一级行业下的细分。

---

## 数据源对比

| API | 数据内容 | 批量支持 | 备注 |
|-----|---------|---------|------|
| cn/industry（level=two） | 二级行业代码列表 | 全量一次返回 | 核心索引数据 |
| cn/industry（level=three） | 三级行业代码列表 | 全量一次返回 | 覆盖细粒度 |
| cn/industry/fundamental/sw_2021（date参数） | PE/PB/市值/换手率 | 支持批量codes | 核心数据源 |
| cn/industry/constituents/sw_2021 | 成分股列表 | 单行业查询 | 用于龙头识别 |

---

## 注意事项

1. `date` 参数支持多个 `stockCodes` 同时查询，效率更高
2. 涨跌幅计算需要历史某日的市值数据，历史查询每次只支持1个 code
3. 申万三级行业数据可能部分缺失，覆盖比例需在输出中说明
4. 行业代码与实际业务分类需核对，避免错误归类

---

## 查找更多 API

详细的 API 发现方法，参考：`.claude/plugins/query_data/lixinger-api-docs/SKILL.md`
