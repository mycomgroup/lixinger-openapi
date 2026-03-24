# cn-data-source

description: 从理杏仁开放平台获取A股公司数据，为 company-valuation、peer-analysis、scenario-modeling 等估值技能提供标准化输入。当目标公司是A股（股票代码为6位数字）时，优先调用此技能获取数据，再传入估值流程。

## 数据工具

使用项目根目录的 `query_tool.py`：

```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "<API后缀>" \
  --params '<JSON参数>' \
  --columns "<字段列表>"
```

token 从项目根目录 `token.cfg` 自动读取，无需额外配置。

---

## Step 1：获取公司基本信息

```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,name,fsTableType,ipoDate,exchange"
```

返回字段：公司名称、财报类型（non_financial/bank/insurance/security）、上市日期、交易所。

---

## Step 2：获取财务数据（利润表 + 资产负债表）

获取最近5年年度数据，用于 LTM 计算和趋势分析：

```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.fs.non_financial" \
  --params '{
    "stockCodes": ["600519"],
    "startDate": "2020-12-31",
    "endDate": "2024-12-31",
    "metricsList": [
      "y.ps.toi.t",
      "y.ps.ebit.t",
      "y.ps.ebitda.t",
      "y.ps.npatoshopc.t",
      "y.ps.gp_m.t",
      "y.ps.np_s_r.t",
      "y.ps.wroe.t",
      "y.ps.beps.t",
      "y.ps.toi.t_y2y",
      "y.ps.npatoshopc.t_y2y",
      "y.bs.ta.t",
      "y.bs.tl.t"
    ]
  }' \
  --columns "date,y.ps.toi.t,y.ps.ebit.t,y.ps.ebitda.t,y.ps.npatoshopc.t,y.ps.gp_m.t,y.ps.np_s_r.t,y.ps.wroe.t,y.ps.beps.t,y.ps.toi.t_y2y,y.ps.npatoshopc.t_y2y,y.bs.ta.t,y.bs.tl.t"
```

> 注意：`cn.company.fs.non_financial` 的现金流量表字段（如 `y.cf.*`）和部分资产负债表字段（如 `y.bs.te.t` 股东权益）不可用。如需现金流数据，使用 AkShare 的 `stock_financial_report_sina` 接口。

关键字段映射（对应 valuation 输入）：

| 理杏仁字段 | valuation 输入 | 说明 |
|-----------|---------------|------|
| y.ps.toi.t | revenue | 营业总收入（年度累计，单位：元） |
| y.ps.ebitda.t | ebitda | EBITDA（单位：元） |
| y.ps.ebit.t | ebit | EBIT（单位：元） |
| y.ps.npatoshopc.t | net_income | 归母净利润（单位：元） |
| y.bs.ta.t | total_assets | 总资产（单位：元） |
| y.bs.tl.t | total_liabilities | 总负债（单位：元） |
| y.bs.ta.t - y.bs.tl.t | equity（估算） | 净资产（单位：元） |

---

## Step 3：获取市场数据（估值 + 股本）

```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.fundamental.non_financial" \
  --params '{
    "stockCodes": ["600519"],
    "date": "latest"
  }' \
  --columns "date,stockCode,sp,mc,cmc,pe_ttm,d_pe_ttm,pb,ps_ttm,dyr,ev_ebit_r,ev_ebitda_r,pe_ttm.y5.cvpos,pb.y5.cvpos"
```

关键字段映射：

| 理杏仁字段 | valuation 输入 | 说明 |
|-----------|---------------|------|
| sp | price | 最新股价（元） |
| mc | market_cap | 总市值（元） |
| pe_ttm | pe_ttm | PE-TTM |
| pb | pb | PB |
| dyr | dividend_yield | 股息率 |
| ev_ebitda_r | ev_ebitda | EV/EBITDA |

股本数量 = mc / sp（总股本，单位：股）

---

## Step 4：获取分红数据（用于 DDM / 股息率分析）

```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.dividend" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "date,stockCode,dividendPerShare,dividendYield,payoutRatio"
```

---

## Step 5：获取同行业可比公司（用于 peer-analysis）

先获取目标公司所属行业：

```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.industries" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,industryCode,industryName"
```

再获取同行业公司的估值数据：

```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.industry.fundamental.sw_2021" \
  --params '{"industryCode": "<行业代码>", "date": "latest"}' \
  --columns "stockCode,name,pe_ttm,pb,ps_ttm,mc,dyr"
```

---

## Step 6：获取无风险利率（用于 WACC）

理杏仁不提供10年期国债收益率，使用 AkShare：

```python
import akshare as ak
df = ak.bond_zh_us_rate(start_date='20260101')
rf = df['中国国债收益率10年'].dropna().iloc[-1]
print(f"中国10年期国债收益率: {rf}%")
```

或使用理杏仁的 LPR 作为参考：

```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro.interest-rates" \
  --params '{"areaCode": "cn", "startDate": "2026-01-01", "endDate": "2026-03-20", "metricsList": ["lpr_y1","lpr_y5"]}' \
  --columns "date,lpr_y1,lpr_y5" --limit 1
```

---

## 数据组装为 valuation 输入

执行完上述查询后，将数据整理为以下结构传入 `company-valuation` skill：

```json
{
  "meta": {
    "company": "贵州茅台",
    "valuation_date": "<最新交易日>",
    "currency": "CNY",
    "unit_scale": "millions",
    "listing_market": "A"
  },
  "basis": "LTM",
  "financials": {
    "revenue": "<y.ps.toi.t / 1,000,000>",
    "ebitda": "<y.ps.ebitda.t / 1,000,000>",
    "ebit": "<y.ps.ebit.t / 1,000,000>",
    "net_income": "<y.ps.npatoshopc.t / 1,000,000>",
    "depreciation_amortization": "<如能获取则填入>"
  },
  "balance_sheet": {
    "cash": "<现金类科目 / 1,000,000>",
    "debt": "<(短债 + 长债) / 1,000,000>",
    "minority_interest": "<少数股东权益 / 1,000,000>",
    "preferred": 0,
    "non_operating_assets": "<联营投资/其他非经营资产，如适用>"
  },
  "shares": {
    "basic": "<mc / sp>",
    "diluted": "<若无更好数据，可先与 basic 相同>"
  },
  "adjustments": {
    "one_off_items": {
      "ebit": "<非经常性 EBIT 调整>",
      "net_income": "<非经常性净利润调整>"
    },
    "restricted_cash": "<受限现金，如有>",
    "lease_liabilities": "<租赁负债，如有>",
    "maintenance_capex": "<维护性资本开支，如能估算>"
  },
  "assumptions": {
    "cost_of_capital": {
      "risk_free_rate": "<cn_10y 最新值>",
      "equity_risk_premium": 0.06,
      "beta": "<行业或回归 beta>",
      "cost_of_debt": "<税前债务成本>",
      "target_debt_weight": "<目标资本结构债务占比>"
    }
  },
  "market": {
    "current_price": "<sp>",
    "price_date": "<最新交易日>",
    "listing_market": "A",
    "accounting_standard": "PRC GAAP",
    "trading_currency": "CNY"
  }
}
```

---

## A股特殊注意事项

- 单位：理杏仁财务数据默认单位为**元**，传入 valuation 时需换算为百万元（÷1,000,000）
- 货币：A股报告货币为 CNY
- 财报类型：银行/保险/证券公司使用 `cn.company.fs.financial` 而非 `non_financial`，EBITDA 不适用
- 股本：理杏仁不直接返回股本数，用 `mc / sp` 计算总股本；如无摊薄信息，先令 `diluted = basic` 并在报告中说明
- 标准化：优先输出 `reported -> normalized` 桥表，至少覆盖非经常项、受限现金、租赁负债、维护性 Capex
- 无风险利率：使用中国10年期国债收益率，而非美国国债
- ERP：A股市场风险溢价建议使用 6%~8%（高于成熟市场）
- 财年：A股财年为自然年，12月31日为年报日期
