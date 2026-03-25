# 数据获取指南

使用 `query_tool.py` 获取 tech-hype-vs-fundamentals 所需的数据。

---

## 查询示例

### 查询Cn.Company.Fundamental.Non Financial - 基本面数据

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["688001", "688012", "300750", "000001", "000858"], "metricsList": ["pe_ttm", "pb", "ps_ttm", "peg", "roe", "roic", "gross_margin", "net_margin", "fo_cfo_yoy", "free_cash_flow", "rd_exp", "sb_exp", "total_mv"]}' \
  --columns "date,stockCode,pe_ttm,pb,ps_ttm,peg,roe,roic,gross_margin,net_margin,fo_cfo_yoy,free_cash_flow,rd_exp,sb_exp,total_mv" \
  --limit 50
```

### 查询Cn.Company.Fundamental.Non Financial - 研发及股份支付详情

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["688001", "688012", "300750"], "metricsList": ["rd_exp", "rd_exp_revenue", "sb_exp", "sb_exp_revenue", "capitalized_rd", "rd_to_total_exp"]}' \
  --columns "date,stockCode,rd_exp,rd_exp_revenue,sb_exp,sb_exp_revenue,capitalized_rd,rd_to_total_exp" \
  --limit 20
```

### 查询Cn.Company.Fundamental.Non Financial - 国产替代相关指标

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["688001", "688012", "300750"], "metricsList": ["domestic_substitution_ratio", "import_substitution_progress", "policy_support_score", "technical_barrier_score", "self_reliance_index"]}' \
  --columns "date,stockCode,domestic_substitution_ratio,import_substitution_progress,policy_support_score,technical_barrier_score,self_reliance_index" \
  --limit 20
```

### 查询Cn.Index.Fundamental - 科技板块指数估值

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"date": "2026-03-24", "stockCodes": ["399006", "399007", "883873", "883871"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "ps_ttm.mcw", "dividend_yield.mcw", "total_mv"]}' \
  --columns "date,stockCode,pe_ttm.mcw,pb.mcw,ps_ttm.mcw,dividend_yield.mcw,total_mv" \
  --limit 20
```

### 查询Cn.Company.Financial.Non Financial - 利润表数据（用于增长分析）

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/financial/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["688001", "688012", "300750", "000001", "000858"], "metricsList": ["revenue", "revenue_yoy", "net_profit", "net_profit_yoy", "gross_profit", "operating_profit"]}' \
  --columns "date,stockCode,revenue,revenue_yoy,net_profit,net_profit_yoy,gross_profit,operating_profit" \
  --limit 50
```

### 查询Cn.Company.Financial.Non Financial - 现金流量表数据

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/financial/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["688001", "688012", "300750"], "metricsList": ["operating_cash_flow", "investing_cash_flow", "financing_cash_flow", "free_cash_flow", "free_cash_flow_yoy"]}' \
  --columns "date,stockCode,operating_cash_flow,investing_cash_flow,financing_cash_flow,free_cash_flow,free_cash_flow_yoy" \
  --limit 20
```

### 查询Cn.Company.Financial.Non Financial - 资产负债表数据

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/financial/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["688001", "688012", "300750"], "metricsList": ["total_assets", "total_liabilities", "shareholder_equity", "debt_to_equity", "current_ratio", "quick_ratio"]}' \
  --columns "date,stockCode,total_assets,total_liabilities,shareholder_equity,debt_to_equity,current_ratio,quick_ratio" \
  --limit 20
```

### 查询Cn.Company.Financial.Non Financial - 每股指标

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/financial/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["688001", "688012", "300750", "000001", "000858"], "metricsList": ["eps", "eps_yoy", "bps", "bps_yoy", "cfps", "cfps_yoy"]}' \
  --columns "date,stockCode,eps,eps_yoy,bps,bps_yoy,cfps,cfps_yoy" \
  --limit 50
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

- `cn/company/fundamental/non_financial` - 非金融公司基本面指标
- `cn/company/financial/non_financial` - 非金融公司财务报表数据
- `cn/index/fundamental` - 指数基本面数据

---

## 关键指标说明

### 估值指标
- PE_TTM: 市盈率（滚动十二个月）
- PB: 市净率
- PS_TTM: 市销率（滚动十二个月）
- PEG: 市盈率增长比

### 盈利能力指标
- ROE: 净资产收益率
- ROIC: 投入资本回报率
- Gross Margin: 毛利率
- Net Margin: 净利率

### 成长指标
- Revenue YoY: 营收同比增长
- Net Profit YoY: 净利润同比增长
- Operating Cash Flow YoY: 经营现金流同比增长
- Free Cash Flow YoY: 自由现金流同比增长

### 研发及股份支付
- RD Exp: 研发费用
- RD Exp Revenue: 研发费用占营收比例
- SB Exp: 股份支付费用
- SB Exp Revenue: 股份支付费用占营收比例
- Capitalized RD: 资本化研发费用
- RD To Total Exp: 研发费用占总费用比例

### 国产替代/自主可控指标
- Domestic Substitution Ratio: 国产替代比例
- Import Substitution Progress: 进口替代进度
- Policy Support Score: 政策支持力度评分
- Technical Barrier Score: 技术壁垒评分
- Self Reliance Index: 自主可控指数

### 财务健康指标
- Debt to Equity: 资产负债率
- Current Ratio: 流动比率
- Quick Ratio: 速动比率
- Free Cash Flow: 自由现金流

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`