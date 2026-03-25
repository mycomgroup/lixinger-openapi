# 数据获取指南

使用 `query_tool.py` 获取 quant-factor-screener 所需的数据。

---

## 查询示例

### 查询Cn.Company.Fundamental.Non Financial (价值、质量、成长因子基础数据)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["000001", "600519", "000858", "300750"], "metricsList": ["pe_ttm", "pb", "pcf_ttm", "ev_ebitda_r", "roe", "debt_to_assets", "ocf_to_net_profit", "rev_yoy_3", "profit_yoy_3", "gross_margin_yoy_3"]}' \
  --columns "date,stockCode,pe_ttm,pb,pcf_ttm,ev_ebitda_r,roe,debt_to_assets,ocf_to_net_profit,rev_yoy_3,profit_yoy_3,gross_margin_yoy_3" \
  --limit 100
```

### 查询市值数据 (规模因子)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["000001", "600519", "000858", "300750"], "metricsList": ["mc", "cmc", "ecmc"]}' \
  --columns "date,stockCode,mc,cmc,ecmc" \
  --limit 100
```

### 查询价格和波动率数据 (动量、低波动因子)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"date": "2025-12-31", "stockCodes": ["000001", "600519", "000858", "300750"], "limit": 250}' \
  --columns "date,stockCode,open,high,low,close,volume,turnover_rate" \
  --limit 1000
```

### 查询指数数据 (用于Beta计算和市场环境判断)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"date": "2025-12-31", "stockCodes": ["000300", "000905"], "limit": 250}' \
  --columns "date,stockCode,open,high,low,close,volume" \
  --limit 100
```

### 查询基本面统计数据 (用于行业中性化处理)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["000001", "600519", "000858", "300750"], "metricsList": ["pe_ttm.y1.cvpos", "pb.y1.cvpos", "roe.y1.cvpos"]}' \
  --columns "date,stockCode,pe_ttm.y1.cvpos,pb.y1.cvpos,roe.y1.cvpos" \
  --limit 100
```

### 查询宏观经济数据 (因子择时判断)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "macro/gdp" \
  --params '{"startDate": "2024-01-01", "endDate": "2025-12-31"}' \
  --columns "date,period,gdp" \
  --limit 100
```

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "macro/cpi" \
  --params '{"startDate": "2024-01-01", "endDate": "2025-12-31"}' \
  --columns "date,month,cpi_yoy" \
  --limit 100
```

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "macro/interest-rates" \
  --params '{"startDate": "2024-01-01", "endDate": "2025-12-31"}' \
  --columns "date,rate_type,rate_value" \
  --limit 100
```

### 查询行业分类数据 (行业中性化必需)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/industries" \
  --params '{"date": "2025-12-31", "stockCodes": ["000001", "600519", "000858", "300750"]}' \
  --columns "date,stockCode,industry_name,industry_code" \
  --limit 100
```

### 查询换手率数据 (A股特有动量因子)

```bash
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["000001", "600519", "000858", "300750"], "metricsList": ["to_r", "to_r.avgv"]}' \
  --columns "date,stockCode,to_r,to_r.avgv" \
  --limit 100
```

---

## 参数说明

- `--suffix`: API 路径（参考下方可用 API 列表）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

## 本 Skill 常用 API

### 价值因子所需数据
- `cn/company/fundamental/non_financial` - PE-TTM, PB, PCF-TTM, EV/EBITDA

### 质量因子所需数据  
- `cn/company/fundamental/non_financial` - ROE, 资产负债率, 经营现金流/净利润

### 成长因子所需数据
- `cn/company/fundamental/non_financial` - 营收增速, 净利润增速, 毛利率增速

### 规模因子所需数据
- `cn/company/fundamental/non_financial` - 总市值, 流通市值, 自由流通市值

### 动量因子所需数据
- `cn/company/candlestick` - 日线价格数据（计算12-1月动量）
- `cn/company/fundamental/non_financial` - 换手率（A股特有因子）

### 低波动因子所需数据
- `cn/company/candlestick` - 日线价格数据（计算波动率、Beta、下行偏差）

### 行业中性化所需数据
- `cn/company/industries` - 行业分类信息

### 因子择时所需数据
- `macro/gdp` - GDP增速判断经济周期
- `macro/cpi` - CPI通胀水平
- `macro/interest-rates` - 利率环境

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

## 数据字段说明

### 估值指标 (Value因子)
- `pe_ttm`: 市盈率（TTM）
- `pb`: 市净率  
- `pcf_ttm`: 市现率（TTM）
- `ev_ebitda_r`: EV/EBITDA
- `ey`: 收益率

### 盈利能力指标 (Quality因子)
- `roe`: 净资产收益率
- `roic`: 投入资本回报率
- `net_profit_margin`: 净利润率
- `gross_profit_rate`: 毛利率

### 财务健康指标 (Quality因子)
- `debt_to_assets`: 资产负债率
- `current_ratio`: 流动比率
- `quick_ratio`: 速动比率

### 现金流指标 (Quality因子)
- `ocf_to_net_profit`: 经营现金流净利润比
- `ocf_to_revenue`: 经营现金流/营业收入
- `free_cash_flow`: 自由现金流

### 成长指标 (Growth因子)
- `rev_yoy_3`: 营业收入同比增长（3年平均）
- `profit_yoy_3`: 净利润同比增长（3年平均） 
- `gross_margin_yoy_3`: 毛利率同比增长（3年平均）
- `eps_yoy_3`: 每股收益同比增长（3年平均）

### 规模指标 (Size因子)
- `mc`: 总市值
- `cmc`: 流通市值
- `ecmc`: 自由流通市值

### 动量指标 (Momentum因子)
- `close`: 收盘价（用于计算价格动量）
- `turnover_rate`: 换手率（A股特有动量因子）
- `volume`: 成交量

### 风险指标 (Low Volatility因子)
- 需要通过收盘价数据计算：
  - 日收益率标准差（已实现波动率）
  - 相对基准的Beta
  - 下行偏差（仅负收益的半偏差）

## 使用建议

1. **优先使用非金融数据**：因子模型通常排除金融股，使用 `cn/company/fundamental/non_financial` 接口
2. **选择合适的日期**：使用最近一个季度末或月末数据确保基本面数据完整
3. **控制返回量**：使用 `--limit` 参数控制返回股票数量，避免数据过大
4. **只取必要字段**：使用 `--columns` 只返回所需因子计算的字段，节省token
5. **考虑复权**：价格数据建议使用后复权价格计算动量因子
6. **处理缺失数据**：因子计算前需要处理缺失值和异常值（去极值处理）