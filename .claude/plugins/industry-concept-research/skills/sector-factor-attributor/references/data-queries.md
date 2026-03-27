# 数据获取指南 — sector-factor-attributor

使用 `query_tool.py` 获取板块因子归因所需数据。

---

## API 清单

### 1. 获取区间起止日行业估值快照（计算估值变化）

#### 1.1 归因起始日

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"date": "2025-12-27", "stockCodes": ["360000"], "metricsList": ["pe_ttm.mcw","pb.mcw","mc"]}' \
  --columns "stockCode,date,pe_ttm.mcw,pb.mcw,mc" \
  --limit 1
```

**用途**：获取归因区间起始日的 PE、PB、市值，用于计算估值扩张幅度。

#### 1.2 归因结束日

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"date": "2026-03-27", "stockCodes": ["360000"], "metricsList": ["pe_ttm.mcw","pb.mcw","mc"]}' \
  --columns "stockCode,date,pe_ttm.mcw,pb.mcw,mc" \
  --limit 1
```

**注意**：替换 `stockCodes` 为目标行业代码；`date` 参数支持单个或多个代码。

---

### 2. 获取行业 PE 历史序列（用于估值分位判断）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"startDate": "2025-09-27", "endDate": "2026-03-27", "stockCodes": ["360000"], "metricsList": ["pe_ttm.mcw","pe_ttm.y10.mcw.cvpos","pb.mcw","mc"]}' \
  --columns "stockCode,date,pe_ttm.mcw,pe_ttm.y10.mcw.cvpos,pb.mcw,mc" \
  --limit 130
```

**用途**：获取近6个月的 PE/PB 历史序列，用于：
- 计算区间估值变化（归因的估值维度）
- 绘制估值走势
- 判断当前估值处于历史什么分位（`pe_ttm.y10.mcw.cvpos`）

**注意**：`startDate` 模式下 `stockCodes` 只支持1个代码。

---

### 3. 获取行业财务数据（盈利维度，可选）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fs/sw_2021/hybrid" \
  --params '{"date": "2025-09-30", "stockCodes": ["490000"], "metricsList": ["q.ps.np.t","q.ps.np.t_y2y","q.ps.oi.t","q.ps.oi.t_y2y"]}' \
  --columns "stockCode,q.ps.np.t,q.ps.np.t_y2y,q.ps.oi.t,q.ps.oi.t_y2y" \
  --limit 1
```

**用途**：获取行业净利润同比增速（`q.ps.np.t_y2y`），用于盈利贡献归因。

**重要注意**：此 API 目前仅对部分行业（如非银金融 490000）返回数据，多数行业暂无数据。
- 若不可得：触发降级，使用 PARTIAL 归因（两维：估值 + 残差）
- 在 `data_gaps` 中标注：`missing_field: "eps_data", fallback_method: "PARTIAL_ATTRIBUTION"`

---

### 4. 基准指数数据（沪深300对比）

```bash
# 沪深300 申万代码（用于超额收益计算）
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"date": "2026-03-27", "stockCodes": ["000300.SH"], "metricsList": ["pe_ttm.mcw","mc"]}' \
  --columns "stockCode,date,pe_ttm.mcw,mc" \
  --limit 1
```

**注意**：若基准数据不可得，省略超额收益分析，仅做绝对收益归因。

---

### 5. 行业成分股数据（用于风格因子暴露评估）

```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/constituents/sw_2021" \
  --params '{"stockCodes": ["360000"]}' \
  --columns "stockCode,name,mc" \
  --limit 30
```

**用途**：获取行业成分股列表和市值，用于评估：
- 大盘/小盘风格：Top10成分股市值是否集中（大市值行业 vs 分散小盘）
- 龙头效应评估

---

## 估值扩张归因计算公式

```python
# 总收益率
R_total = (mc_end - mc_start) / mc_start

# 估值扩张贡献（PE变化产生的收益）
valuation_contribution = (pe_end / pe_start - 1)
# 近似：如果EPS不变，PE扩张即是估值驱动的全部收益

# 盈利贡献（EPS增速产生的收益）
earnings_contribution = eps_growth_rate   # 使用净利润同比增速近似

# 残差（风险溢价 + 其他）
residual = R_total - valuation_contribution - earnings_contribution

# 归因比例
valuation_pct = valuation_contribution / R_total
earnings_pct = earnings_contribution / R_total
residual_pct = residual / R_total
```

---

## 风格因子判断参考

| 风格因子 | 数据来源 | 判断方式 |
|---------|---------|---------|
| 大/小盘 | 行业成分股 mc 分布 | Top10成分股市值 > 5000亿 = 大盘 |
| 成长/价值 | PE vs PB 分位 + 净利润增速 | PE分位高 + 高增速 = 成长 |
| 质量/红利 | 股息率 + ROE | 股息率 > 3% = 高红利特征 |
| 动量 | 近3M/6M涨跌幅排名分位 | 排名前30% = 高动量 |

---

## 数据源对比

| API | 用途 | 可用性 | 备注 |
|-----|------|-------|------|
| cn/industry/fundamental/sw_2021（date） | 估值快照 | 高 | 核心数据源 |
| cn/industry/fundamental/sw_2021（startDate） | 估值历史序列 | 高 | 每次一个code |
| cn/industry/fs/sw_2021/hybrid | 盈利数据 | 低 | 多数行业无数据 |
| cn/industry/constituents/sw_2021 | 成分股 | 中 | 用于风格评估 |

---

## 查找更多 API

详细的 API 发现方法，参考：`.claude/plugins/query_data/lixinger-api-docs/SKILL.md`
