# 港股财务报表分析 - 数据获取指南

本文档说明如何使用 `query_tool.py` 获取港股财务报表分析所需的数据。

---

## 核心数据需求

### 1. 财务报表数据
- 损益表（利润表）
- 资产负债表
- 现金流量表
- 所有者权益变动表

### 2. 财务比率数据
- 盈利能力指标
- 偿债能力指标
- 运营效率指标
- 成长性指标

### 3. 基本面数据
- 估值指标（PE、PB、PS）
- ROE、ROA等回报率
- 股息率
- 市值数据

### 4. 历史趋势数据
- 多年度财务数据
- 季度财务数据
- 同比环比增长率

---

## 数据查询示例

### 1. 获取最新财务报表数据 ⭐ 核心

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fs/non_financial" \
  --params '{"stockCodes": ["00700"], "date": "latest", "metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.ps.gp_m.t", "q.ps.np_s_r.t", "q.ps.beps.t"]}' \
  --columns "date,q.ps.toi.t,q.ps.np.t,q.ps.gp_m.t,q.ps.np_s_r.t,q.ps.beps.t"
```

**用途**: 获取最新季度的核心财务数据（利润表）

**关键指标**:
- `q.ps.toi.t`: 营业总收入（季度累积）
- `q.ps.np.t`: 净利润（季度累积）
- `q.ps.gp_m.t`: 毛利率
- `q.ps.np_s_r.t`: 净利率
- `q.ps.beps.t`: 基本每股收益

**注意**: HK fs API 仅支持利润表数据。资产负债表和现金流数据请使用 `hk/company/fundamental/non_financial` API

### 2. 获取损益表（利润表）数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fs/non_financial" \
  --params '{"stockCodes": ["00700"], "date": "2026-02-24", "metricsList": ["q.ps.toi.t", "q.ps.oc.t", "q.ps.gp.t", "q.ps.gp_m.t", "q.ps.se.t", "q.ps.ae.t", "q.ps.fe.t", "q.ps.rade.t", "q.ps.tp.t", "q.ps.np.t", "q.ps.npatoshopc.t", "q.ps.beps.t"]}' \
  --columns "date,q.ps.toi.t,q.ps.oc.t,q.ps.gp.t,q.ps.gp_m.t,q.ps.se.t,q.ps.ae.t,q.ps.fe.t,q.ps.rade.t,q.ps.tp.t,q.ps.np.t,q.ps.npatoshopc.t,q.ps.beps.t"
```

**用途**: 获取完整的损益表数据

**关键指标**:
- `q.ps.toi.t`: 营业总收入
- `q.ps.oc.t`: 营业成本
- `q.ps.gp.t`: 毛利
- `q.ps.gp_m.t`: 毛利率
- `q.ps.se.t`: 销售费用
- `q.ps.ae.t`: 管理费用
- `q.ps.fe.t`: 财务费用
- `q.ps.rade.t`: 研发费用
- `q.ps.tp.t`: 利润总额
- `q.ps.np.t`: 净利润
- `q.ps.npatoshopc.t`: 归母净利润
- `q.ps.beps.t`: 基本每股收益

### 3. 获取资产负债表数据（使用 fundamental API）

**注意**: HK fs API 不支持资产负债表数据，需使用 fundamental API

```bash
# 资产负债表数据不在 fs API 中，建议查看公司年报或使用其他数据源
# 或者使用 hk/company/fundamental/non_financial 获取部分财务指标
```

**说明**: 港股 fs API 仅提供利润表数据，资产负债表和现金流数据需要：
1. 查阅港交所披露易的原始财报
2. 使用 `hk/company/fundamental/non_financial` 获取部分财务比率

### 4. 获取现金流量表数据（使用 fundamental API）

**注意**: HK fs API 不支持现金流量表数据，需使用 fundamental API

```bash
# 现金流量表数据不在 fs API 中，建议查看公司年报或使用其他数据源
# 或者使用 hk/company/fundamental/non_financial 获取部分现金流指标
```

**说明**: 港股 fs API 仅提供利润表数据，现金流数据需要：
1. 查阅港交所披露易的原始财报
2. 使用 `hk/company/fundamental/non_financial` 获取部分现金流比率

### 5. 获取历史财务数据（多年度）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fs/non_financial" \
  --params '{"stockCodes": ["00700"], "startDate": "2020-01-01", "endDate": "2026-02-24", "metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.ps.gp_m.t", "q.ps.np_s_r.t"]}' \
  --columns "date,q.ps.toi.t,q.ps.np.t,q.ps.gp_m.t,q.ps.np_s_r.t" \
  --limit 20
```

**用途**: 获取多年度财务数据（利润表），用于趋势分析

**注意**: 仅包含利润表数据。资产负债表和现金流数据不在此API中

### 6. 获取同比环比增长数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fs/non_financial" \
  --params '{"stockCodes": ["00700"], "date": "2026-02-24", "metricsList": ["q.ps.toi.t", "q.ps.toi.t_y2y", "q.ps.toi.t_c2c", "q.ps.np.t", "q.ps.np.t_y2y", "q.ps.np.t_c2c"]}' \
  --columns "date,q.ps.toi.t,q.ps.toi.t_y2y,q.ps.toi.t_c2c,q.ps.np.t,q.ps.np.t_y2y,q.ps.np.t_c2c"
```

**用途**: 获取同比环比增长率数据

**关键指标**:
- `t_y2y`: 同比增长率
- `t_c2c`: 环比增长率

### 7. 获取单季度数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fs/non_financial" \
  --params '{"stockCodes": ["00700"], "date": "2026-02-24", "metricsList": ["q.ps.toi.c", "q.ps.np.c", "q.ps.gp_m.c", "q.ps.np_s_r.c"]}' \
  --columns "date,q.ps.toi.c,q.ps.np.c,q.ps.gp_m.c,q.ps.np_s_r.c"
```

**用途**: 获取单季度数据（非累积）

**指标说明**:
- `.t`: 累积值（年初至今）
- `.c`: 单季值（仅当季）
- `.ttm`: TTM值（过去12个月）

### 8. 获取TTM数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fs/non_financial" \
  --params '{"stockCodes": ["00700"], "date": "2026-02-24", "metricsList": ["q.ps.toi.ttm", "q.ps.np.ttm", "q.ps.gp_m.ttm", "q.ps.np_s_r.ttm"]}' \
  --columns "date,q.ps.toi.ttm,q.ps.np.ttm,q.ps.gp_m.ttm,q.ps.np_s_r.ttm"
```

**用途**: 获取TTM（过去12个月）数据，用于估值分析

**注意**: 仅包含利润表TTM数据。现金流TTM数据不在此API中

### 9. 获取基本面数据（配合财务分析）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"stockCodes": ["00700"], "date": "2026-02-24", "metricsList": ["pe_ttm", "pb", "ps_ttm", "dyr", "mc"]}' \
  --limit 20
```

**说明**: `hk/company/fundamental/non_financial` 不支持 `roe_ttm` 和 `roa_ttm` 指标，如需财务指标请使用 `hk/company/fs/non_financial` API

**用途**: 获取估值和回报率指标

### 10. 获取公司基本信息

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company" \
  --params '{"stockCodes": ["00700"]}' \
  --columns "stockCode,name,market,fsTableType,ipoDate,areaCode"
```

**用途**: 获取公司基本信息

**关键字段**:
- `fsTableType`: 财报类型（non_financial/bank/security/insurance）
- `ipoDate`: 上市日期
- `areaCode`: 地区代码

---

## 财务比率计算

### 1. 盈利能力比率计算
```python
def calculate_profitability_ratios(financial_data):
    """
    计算盈利能力比率
    """
    revenue = financial_data['q.ps.toi.t']  # 营业收入
    cost = financial_data['q.ps.oc.t']  # 营业成本
    net_profit = financial_data['q.ps.np.t']  # 净利润
    total_assets = financial_data['q.bs.ta.t']  # 总资产
    equity = financial_data['q.bs.se.t']  # 股东权益
    
    # 毛利率
    gross_margin = (revenue - cost) / revenue * 100
    
    # 净利率
    net_margin = net_profit / revenue * 100
    
    # ROE（净资产收益率）
    roe = net_profit / equity * 100
    
    # ROA（总资产收益率）
    roa = net_profit / total_assets * 100
    
    return {
        'gross_margin': round(gross_margin, 2),
        'net_margin': round(net_margin, 2),
        'roe': round(roe, 2),
        'roa': round(roa, 2)
    }

# 使用示例
ratios = calculate_profitability_ratios({
    'q.ps.toi.t': 154063000000,  # 1540.63亿港元
    'q.ps.oc.t': 84395000000,    # 843.95亿港元
    'q.ps.np.t': 42312000000,    # 423.12亿港元
    'q.bs.ta.t': 1245678000000,  # 12456.78亿港元
    'q.bs.se.t': 788889000000    # 7888.89亿港元
})
print(f"毛利率: {ratios['gross_margin']}%")
print(f"净利率: {ratios['net_margin']}%")
print(f"ROE: {ratios['roe']}%")
print(f"ROA: {ratios['roa']}%")
```

### 2. 偿债能力比率计算
```python
def calculate_solvency_ratios(financial_data):
    """
    计算偿债能力比率
    """
    current_assets = financial_data['q.bs.ca.t']  # 流动资产
    current_liabilities = financial_data['q.bs.cl.t']  # 流动负债
    inventory = financial_data['q.bs.inv.t']  # 存货
    total_assets = financial_data['q.bs.ta.t']  # 总资产
    total_liabilities = financial_data['q.bs.tl.t']  # 总负债
    equity = financial_data['q.bs.se.t']  # 股东权益
    
    # 流动比率
    current_ratio = current_assets / current_liabilities
    
    # 速动比率
    quick_ratio = (current_assets - inventory) / current_liabilities
    
    # 资产负债率
    debt_to_asset_ratio = total_liabilities / total_assets * 100
    
    # 债务权益比
    debt_to_equity_ratio = total_liabilities / equity
    
    return {
        'current_ratio': round(current_ratio, 2),
        'quick_ratio': round(quick_ratio, 2),
        'debt_to_asset_ratio': round(debt_to_asset_ratio, 2),
        'debt_to_equity_ratio': round(debt_to_equity_ratio, 2)
    }
```

### 3. 运营效率比率计算
```python
def calculate_efficiency_ratios(financial_data):
    """
    计算运营效率比率
    """
    revenue = financial_data['q.ps.toi.ttm']  # 营业收入（TTM）
    cost = financial_data['q.ps.oc.ttm']  # 营业成本（TTM）
    total_assets = financial_data['q.bs.ta.t']  # 总资产
    inventory = financial_data['q.bs.inv.t']  # 存货
    receivables = financial_data['q.bs.ar.t']  # 应收账款
    payables = financial_data['q.bs.ap.t']  # 应付账款
    
    # 总资产周转率
    asset_turnover = revenue / total_assets
    
    # 存货周转率
    inventory_turnover = cost / inventory
    
    # 应收账款周转率
    receivables_turnover = revenue / receivables
    
    # 应付账款周转率
    payables_turnover = cost / payables
    
    # 现金转换周期（天）
    days_inventory = 365 / inventory_turnover
    days_receivables = 365 / receivables_turnover
    days_payables = 365 / payables_turnover
    cash_conversion_cycle = days_inventory + days_receivables - days_payables
    
    return {
        'asset_turnover': round(asset_turnover, 2),
        'inventory_turnover': round(inventory_turnover, 2),
        'receivables_turnover': round(receivables_turnover, 2),
        'cash_conversion_cycle': round(cash_conversion_cycle, 1)
    }
```

### 4. 财务健康度评分
```python
def calculate_financial_health_score(ratios):
    """
    计算财务健康度评分（0-100分）
    """
    score = 0
    
    # 盈利能力评分（40分）
    if ratios['roe'] >= 20:
        score += 20
    elif ratios['roe'] >= 15:
        score += 15
    elif ratios['roe'] >= 10:
        score += 10
    
    if ratios['net_margin'] >= 20:
        score += 20
    elif ratios['net_margin'] >= 15:
        score += 15
    elif ratios['net_margin'] >= 10:
        score += 10
    
    # 偿债能力评分（30分）
    if ratios['current_ratio'] >= 2.0:
        score += 15
    elif ratios['current_ratio'] >= 1.5:
        score += 10
    elif ratios['current_ratio'] >= 1.0:
        score += 5
    
    if ratios['debt_to_asset_ratio'] <= 40:
        score += 15
    elif ratios['debt_to_asset_ratio'] <= 60:
        score += 10
    elif ratios['debt_to_asset_ratio'] <= 80:
        score += 5
    
    # 运营效率评分（30分）
    if ratios['asset_turnover'] >= 1.0:
        score += 15
    elif ratios['asset_turnover'] >= 0.5:
        score += 10
    elif ratios['asset_turnover'] >= 0.3:
        score += 5
    
    if ratios['cash_conversion_cycle'] <= 30:
        score += 15
    elif ratios['cash_conversion_cycle'] <= 60:
        score += 10
    elif ratios['cash_conversion_cycle'] <= 90:
        score += 5
    
    # 评级
    if score >= 85:
        rating = 'A'
        level = '优秀'
    elif score >= 70:
        rating = 'B'
        level = '良好'
    elif score >= 55:
        rating = 'C'
        level = '适中'
    else:
        rating = 'D'
        level = '较差'
    
    return {
        'score': score,
        'rating': rating,
        'level': level
    }
```

---

## 完整财务分析流程

### 步骤1: 获取最新财务报表
```bash
# 获取最新季度完整财务数据（利润表）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fs/non_financial" \
  --params '{"stockCodes": ["00700"], "date": "latest", "metricsList": ["q.ps.toi.t", "q.ps.oc.t", "q.ps.np.t", "q.ps.gp_m.t", "q.ps.np_s_r.t"]}' \
  --columns "date,q.ps.toi.t,q.ps.oc.t,q.ps.np.t,q.ps.gp_m.t,q.ps.np_s_r.t"
```

**注意**: HK fs API 仅支持利润表数据。资产负债表和现金流数据需使用其他API或查阅原始财报

### 步骤2: 获取历史趋势数据
```bash
# 获取近5年财务数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fs/non_financial" \
  --params '{"stockCodes": ["00700"], "startDate": "2020-01-01", "endDate": "2026-02-24", "metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.ps.toi.t_y2y", "q.ps.np.t_y2y"]}' \
  --columns "date,q.ps.toi.t,q.ps.np.t,q.ps.toi.t_y2y,q.ps.np.t_y2y" \
  --limit 20
```

### 步骤3: 获取估值数据
```bash
# 获取估值指标
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"stockCodes": ["00700"], "date": "2026-02-24", "metricsList": ["pe_ttm", "pb", "dyr", "mc"]}' \
  --limit 20
```

**说明**: `hk/company/fundamental/non_financial` 不支持 `roe_ttm` 和 `roa_ttm` 指标，如需财务指标请使用 `hk/company/fs/non_financial` API

### 步骤4: 计算财务比率（需要脚本处理）
```python
# 使用上述计算函数处理数据
# 输出财务比率分析报告
```

---

## 参数说明

### metricsList 格式
```
[granularity].[tableName].[fieldName].[expressionCalculateType]
```

**granularity（时间粒度）**:
- `y`: 年度
- `hy`: 半年度
- `q`: 季度

**tableName（报表类型）**:
- `ps`: 利润表（Profit Statement）
- `bs`: 资产负债表（Balance Sheet）
- `cf`: 现金流量表（Cash Flow）

**expressionCalculateType（计算类型）**:
- `t`: 累积值/当期值
- `t_o`: 原始值
- `t_y2y`: 同比增长率
- `t_c2c`: 环比增长率
- `c`: 单季值/半年值
- `c_o`: 单季原始值
- `c_y2y`: 单季同比
- `c_c2c`: 单季环比
- `ttm`: TTM值（过去12个月）
- `ttm_y2y`: TTM同比

---

## 本 Skill 常用 API

### 核心 API ⭐
- `hk/company/fs/non_financial` - 港股财务报表（最重要）
- `hk/company/fundamental/non_financial` - 港股基本面数据

### 辅助 API
- `hk/company` - 港股公司信息
- `hk/company.industries` - 港股行业分类
- `hk/company/dividend` - 分红数据

---

## 数据更新频率

- **年报数据**: 年度更新（通常3-4月披露）
- **中报数据**: 半年度更新（通常8-9月披露）
- **季报数据**: 季度更新
- **财报披露**: 有延迟，通常在季度结束后1-2个月

---

## 缺失数据说明

以下数据理杏仁API无法直接提供，需要通过计算或外部数据源补充：

### 1. 详细科目数据
- **问题**: 部分细分科目可能不全
- **替代方案**: 使用主要科目进行分析

### 2. 附注信息
- **问题**: 财报附注、审计意见详情
- **替代方案**: 查阅港交所披露易原始报表

### 3. 分部数据
- **问题**: 业务分部、地区分部详细数据
- **替代方案**: 查阅公司年报

### 4. 关联交易
- **问题**: 关联方交易明细
- **替代方案**: 查阅公司公告

### 5. 或有事项
- **问题**: 或有负债、担保等信息
- **替代方案**: 查阅财报附注

---

## 使用示例

### 示例1: 生成财务报表概览

```bash
# 1. 获取最新财务数据（利润表指标）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fs/non_financial" \
  --params '{"stockCodes": ["00700"], "date": "latest", "metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.ps.beps.t", "q.ps.gp.t", "q.ps.oc.t"]}' \
  --columns "date,q.ps.toi.t,q.ps.np.t,q.ps.beps.t,q.ps.gp.t,q.ps.oc.t"

# 注意：hk/company/fs/non_financial 仅支持利润表（q.ps.*）指标
# 资产负债表和现金流量表数据需查看原始财报或使用 hk/company/fundamental/non_financial

# 2. 格式化输出（需要脚本处理）
# 输出示例：
# 腾讯控股(00700) 财务报表 (2024Q3):
# 营业收入: 1540.63亿港元
# 净利润: 423.12亿港元
# 每股收益: 4.42港元
# 总资产: 12456.78亿港元
# 总负债: 4567.89亿港元
# 股东权益: 7888.89亿港元
```

### 示例2: 财务比率分析

```bash
# 1. 获取财务数据（利润表指标）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fs/non_financial" \
  --params '{"stockCodes": ["00700"], "date": "2026-02-24", "metricsList": ["q.ps.toi.ttm", "q.ps.oc.ttm", "q.ps.np.ttm", "q.ps.gp.ttm", "q.ps.np_s_r.ttm"]}' \
  --columns "date,q.ps.toi.ttm,q.ps.oc.ttm,q.ps.np.ttm,q.ps.gp.ttm,q.ps.np_s_r.ttm"

# 注意：hk/company/fs/non_financial 仅支持利润表（q.ps.*）指标
# 资产负债表（q.bs.*）和现金流量表（q.cf.*）数据需查看原始财报

# 2. 计算财务比率（需要脚本处理）
# 3. 输出比率分析报告
```

### 示例3: 财务趋势分析

```bash
# 获取5年财务趋势
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fs/non_financial" \
  --params '{"stockCodes": ["00700"], "startDate": "2020-01-01", "endDate": "2026-02-24", "metricsList": ["q.ps.toi.t", "q.ps.toi.t_y2y", "q.ps.np.t", "q.ps.np.t_y2y", "q.ps.gp_m.t", "q.ps.np_s_r.t"]}' \
  --columns "date,q.ps.toi.t,q.ps.toi.t_y2y,q.ps.np.t,q.ps.np.t_y2y,q.ps.gp_m.t,q.ps.np_s_r.t" \
  --limit 20
```

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`

## 相关文档

- **API 文档**: `../../lixinger-data-query/SKILL.md`
- **使用指南**: `../../lixinger-data-query/LLM_USAGE_GUIDE.md`
- **Skill 说明**: `../SKILL.md`

---

**更新日期**: 2026-02-24  
**版本**: v1.0.0
