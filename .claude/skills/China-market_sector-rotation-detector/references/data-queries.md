# 数据获取指南

使用 `query_tool.py` 获取 sector-rotation-detector 所需的数据。

---

## 查询示例

### 查询Macro.Money Supply (货币政策)

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/money-supply" \
  --params '{"areaCode": "cn", "startDate": "2025-02-01", "endDate": "2026-02-24", "metricsList": ["m.m0.t", "m.m1.t", "m.m2.t"]}' \
  --columns "date,m0,m1,m2" \
  --limit 20
```

### 查询Macro.Price Index (通胀)

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/price-index" \
  --params '{"areaCode": "cn", "startDate": "2021-01-01", "endDate": "2026-02-23", "metricsList": ["m.cpi.t", "m.ppi.t"]}' \
  --columns "date,m.cpi.t,m.ppi.t" \
  --limit 80
```

### 查询Cn.Industry (行业分类)

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/industry" \
  --params '{"source": "sw", "level": "one"}' \
  --limit 20
```

### 查询Macro.Gdp (经济增长)

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/gdp" \
  --params '{"areaCode": "cn", "startDate": "2025-01-01", "endDate": "2026-02-24", "metricsList": ["q.gdp.t", "q.gdp.t_y2y"]}' \
  --limit 20
```

### 查询Cn.Index.Fundamental (指数估值)

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"date": "2026-02-24", "stockCodes": ["000001"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc"]}' \
  --columns "date,stockCode,pe_ttm.mcw,pb.mcw,dyr.mcw,mc" \
  --limit 20
```

### 查询Macro.Interest Rates (货币政策 - 利率)

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/interest-rates" \
  --params '{"areaCode": "cn", "startDate": "2025-02-01", "endDate": "2026-02-24", "metricsList": ["m.lpr1y.t", "m.lpr5y.t", "m.mlf.t", "m.shibor3m.t"]}' \
  --columns "date,lpr1y,lpr5y,mlf,shibor3m" \
  --limit 20
```

### 查诡Macro.Required Reserves (货币政策 - 存款准备金率)

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/required-reserves" \
  --params '{"areaCode": "cn", "startDate": "2025-02-01", "endDate": "2026-02-24", "metricsList": ["m.rrr.t"]}' \
  --columns "date,rrr" \
  --limit 20
```

### 查询Macro.Social Financing (货币政策 - 社会融资)

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/social-financing" \
  --params '{"areaCode": "cn", "startDate": "2025-02-01", "endDate": "2026-02-24", "metricsList": ["m.sfin.t", "m.sfin.t_y2y"]}' \
  --columns "date,sfin,sfin_yoy" \
  --limit 20
```

### 查询Macro.Investment in Fixed Assets (经济增长 - 固定资产投资)

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/investment-in-fixed-assets" \
  --params '{"areaCode": "cn", "startDate": "2025-01-01", "endDate": "2026-02-24", "metricsList": ["m.fai.t", "m.fai.t_y2y"]}' \
  --columns "date,fai,fai_yoy" \
  --limit 20
```

### 查询Macro.Domestic Trade (经济增长 - 社会消费品零售总额)

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/domestic-trade" \
  --params '{"areaCode": "cn", "startDate": "2025-01-01", "endDate": "2026-02-24", "metricsList": ["m.retail.t", "m.retail.t_y2y"]}' \
  --columns "date,retail,retail_yoy" \
  --limit 20
```

### 查询Macro.Industrialization (经济增长 - 工业增加值)

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/industrialization" \
  --params '{"areaCode": "cn", "startDate": "2025-01-01", "endDate": "2026-02-24", "metricsList": ["m.industr.val.t", "m.industr.val.t_y2y"]}' \
  --columns "date,industr_val,industr_val_yoy" \
  --limit 20
```

### 查询Macro.PMI (就业与消费 - PMI指数)

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/pmi" \
  --params '{"areaCode": "cn", "startDate": "2025-02-01", "endDate": "2026-02-24", "metricsList": ["m.pmi.manufacturing.t", "m.pmi.nonmanufacturing.t"]}' \
  --columns "date,pmi_manufacturing,pmi_nonmanufacturing" \
  --limit 20
```

### 查询Macro.Unemployment Rate (就业与消费 - 城镇调查失业率)

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/unemployment-rate" \
  --params '{"areaCode": "cn", "startDate": "2025-01-01", "endDate": "2026-02-24", "metricsList": ["m.urban.unemployment.t"]}' \
  --columns "date,urban_unemployment" \
  --limit 20
```

### 查询Macro.RMB Loans (货币政策 - 人民币贷款)

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/rmb-loans" \
  --params '{"areaCode": "cn", "startDate": "2025-02-01", "endDate": "2026-02-24", "metricsList": ["m.rmb.loans.t", "m.rmb.loans.t_y2y"]}' \
  --columns "date,rmb_loans,rmb_loans_yoy" \
  --limit 20
```

### 查询Macbo.Real Estate (房地产数据 - 作为领先指标)

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/real-estate" \
  --params '{"areaCode": "cn", "startDate": "2025-01-01", "endDate": "2026-02-24", "metricsList": ["m.land.sale.area.t", "m.land.sale.amount.t"]}' \
  --columns "date,land_sale_area,land_sale_amount" \
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

### 货币政策支柱
- `macro/money-supply`
- `macro/interest-rates`
- `macro/required-reserves`
- `macro/social-financing`
- `macro/rmb-loans`

### 通胀支柱
- `macro/price-index`

### 经济增长支柱
- `macro/gdp`
- `macro/investment-in-fixed-assets`
- `macro/domestic-trade`
- `macro/industrialization`

### 就业与消费支柱
- `macro/pmi`
- `macro/unemployment-rate`

### 政策导向支柱
- 需要结合政策文件和新闻分析，可参考中央经济工作会议、国务院政策等

### 行业分析
- `cn/industry`
- `cn/index/fundamental`

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

## 重要提示

1. 社会融资规模增速是A股最重要的领先指标，通常领先经济和股市3-6个月
2. 信用脉冲（社融增量的变化率）是判断拐点的核心工具
3. 房地产周期的连锁效应：地产→建材→家居→家电→银行是A股最重要的行业联动体系
4. 政策权重极高：中国经济的政策驱动性远强于西方市场