# 港股估值分析 - 数据获取指南

本文档说明如何使用 `query_tool.py` 获取港股估值分析所需的数据。

---

## 核心数据需求

### 1. 市场整体估值数据
- 恒生指数估值指标（PE、PB、PS、PCF、股息率）
- 估值历史分位数
- 市场市值数据
- 成交量成交额

### 2. 行业估值数据
- 各行业估值指标
- 行业估值历史分位数
- 行业市值分布
- 行业估值排名

### 3. 个股估值数据
- 个股估值指标
- 个股财务数据
- 个股历史估值
- 同行业对比数据

### 4. 历史数据
- 长期估值历史（10年）
- 估值分位数计算
- 估值趋势分析

---

## 数据查询示例

### 1. 获取恒生指数估值数据 ⭐ 核心

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI"], "date": "2024-12-31", "metricsList": ["pe_ttm.mcw", "pe_ttm.y10.mcw.cvpos", "pb.mcw", "pb.y10.mcw.cvpos", "ps_ttm.mcw", "ps_ttm.y10.mcw.cvpos", "dyr.mcw", "dyr.y10.mcw.cvpos", "mc", "cp", "cpc"]}' \
  --columns "date,pe_ttm.mcw,pe_ttm.y10.mcw.cvpos,pb.mcw,pb.y10.mcw.cvpos,ps_ttm.mcw,ps_ttm.y10.mcw.cvpos,dyr.mcw,dyr.y10.mcw.cvpos,mc,cp,cpc"
```

**用途**: 获取恒生指数的核心估值指标及历史分位数

**关键指标**:
- `pe_ttm.mcw`: PE-TTM（市值加权）
- `pe_ttm.y10.mcw.cvpos`: PE-TTM 10年历史分位数
- `pb.mcw`: PB（市值加权）
- `pb.y10.mcw.cvpos`: PB 10年历史分位数
- `ps_ttm.mcw`: PS-TTM（市值加权）
- `dyr.mcw`: 股息率（市值加权）
- `mc`: 市值
- `cp`: 收盘点位
- `cpc`: 涨跌幅

**估值分位数说明**:
- `cvpos`: 当前值分位数（0-100%）
- 分位数 < 30%: 估值偏低
- 分位数 30-70%: 估值适中
- 分位数 > 70%: 估值偏高

### 2. 获取多个指数估值对比

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI", "HSCEI", "HSCCI", "HSTECH"], "date": "2024-12-31", "metricsList": ["pe_ttm.mcw", "pe_ttm.y10.mcw.cvpos", "pb.mcw", "dyr.mcw"]}' \
  --columns "date,pe_ttm.mcw,pe_ttm.y10.mcw.cvpos,pb.mcw,dyr.mcw"
```

**用途**: 对比恒生指数、国企指数、红筹指数、科技指数的估值水平

### 3. 获取恒生指数历史估值数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI"], "startDate": "2020-01-01", "endDate": "2024-12-31", "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw", "mc"]}' \
  --columns "date,pe_ttm.mcw,pb.mcw,dyr.mcw,mc" \
  --limit 1000
```

**用途**: 获取历史估值数据，用于趋势分析和分位数计算

### 4. 获取行业估值数据 ⭐ 核心

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"stockCodes": ["H50", "H5010", "H5020", "H5030", "H5040"], "date": "2024-12-31", "metricsList": ["pe_ttm.mcw", "pe_ttm.y10.mcw.cvpos", "pb.mcw", "pb.y10.mcw.cvpos", "dyr.mcw", "mc"]}' \
  --columns "date,pe_ttm.mcw,pe_ttm.y10.mcw.cvpos,pb.mcw,pb.y10.mcw.cvpos,dyr.mcw,mc"
```

**用途**: 获取各行业的估值指标和历史分位数

**行业代码示例**:
- H50: 能源业
- H5010: 原材料业
- H5020: 工业
- H5030: 非必需消费品
- H5040: 必需消费品

### 5. 获取所有行业估值（用于排名）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"date": "2024-12-31", "metricsList": ["pe_ttm.mcw", "pe_ttm.y10.mcw.cvpos", "pb.mcw", "dyr.mcw", "mc"]}' \
  --columns "industryCode,date,pe_ttm.mcw,pe_ttm.y10.mcw.cvpos,pb.mcw,dyr.mcw,mc" \
  --limit 50
```

**用途**: 获取所有行业估值，用于行业估值排名和对比

### 6. 获取行业列表

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry" \
  --params '{}' \
  --columns "industryCode,industryName,industryLevel"
```

**用途**: 获取行业分类信息，用于行业名称映射

### 7. 获取个股估值数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"stockCodes": ["00700"], "date": "2024-12-31", "metricsList": ["pe", "pe.y10.cvpos", "pb", "pb.y10.cvpos", "ps", "dyr", "mc", "roe", "roa"]}' \
  --columns "date,stockCode,pe,pe.y10.cvpos,pb,pb.y10.cvpos,ps,dyr,mc,roe,roa"
```

**用途**: 获取个股的估值指标和历史分位数

**关键指标**:
- `pe`: 市盈率
- `pe.y10.cvpos`: PE 10年历史分位数
- `pb`: 市净率
- `ps`: 市销率
- `dyr`: 股息率
- `mc`: 市值
- `roe`: 净资产收益率
- `roa`: 总资产收益率

### 8. 获取个股历史估值

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"stockCodes": ["00700"], "startDate": "2020-01-01", "endDate": "2024-12-31", "metricsList": ["pe", "pb", "ps", "dyr", "mc"]}' \
  --columns "date,pe,pb,ps,dyr,mc" \
  --limit 1000
```

**用途**: 获取个股历史估值数据，用于估值区间分析

### 9. 获取个股财务数据（用于DCF估值）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fs/non_financial" \
  --params '{"stockCodes": ["00700"], "startDate": "2020-01-01", "endDate": "2024-12-31", "metricsList": ["fcf", "np", "revenue", "totalAssets", "totalLiabilities"]}' \
  --columns "date,fcf,np,revenue,totalAssets,totalLiabilities" \
  --limit 20
```

**用途**: 获取财务数据，用于DCF现金流折现估值

**关键指标**:
- `fcf`: 自由现金流
- `np`: 净利润
- `revenue`: 营业收入
- `totalAssets`: 总资产
- `totalLiabilities`: 总负债

### 10. 获取同行业股票列表（用于相对估值）

```bash
# 步骤1: 获取目标股票的行业
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company.industries" \
  --params '{"stockCodes": ["00700"]}' \
  --columns "industryCode,industryName"

# 步骤2: 获取同行业所有股票
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company" \
  --params '{}' \
  --columns "stockCode,name,market" \
  --limit 1000

# 步骤3: 获取同行业股票的估值（需要筛选）
```

**用途**: 获取同行业股票，用于相对估值对比

---

## 估值分析计算

### 1. 计算估值评分
```python
# 基于历史分位数计算估值评分
def calculate_valuation_score(pe_percentile, pb_percentile, ps_percentile, dyr_percentile):
    """
    估值评分：0-100分
    分位数越低，估值越低，评分越高（投资价值越大）
    """
    # PE、PB、PS分位数越低越好（反向计分）
    pe_score = (100 - pe_percentile) * 0.35
    pb_score = (100 - pb_percentile) * 0.30
    ps_score = (100 - ps_percentile) * 0.20
    
    # 股息率分位数越高越好（正向计分）
    dyr_score = dyr_percentile * 0.15
    
    total_score = pe_score + pb_score + ps_score + dyr_score
    
    return round(total_score, 1)

# 使用示例
pe_percentile = 35  # PE历史分位数35%
pb_percentile = 40  # PB历史分位数40%
ps_percentile = 45  # PS历史分位数45%
dyr_percentile = 65  # 股息率历史分位数65%

score = calculate_valuation_score(pe_percentile, pb_percentile, ps_percentile, dyr_percentile)
print(f"估值评分: {score}/100")
```

### 2. DCF估值模型（简化版）
```python
def dcf_valuation(fcf_list, growth_rate=0.05, discount_rate=0.10, terminal_growth=0.03):
    """
    DCF现金流折现估值
    
    参数:
    - fcf_list: 历史自由现金流列表
    - growth_rate: 预期增长率
    - discount_rate: 折现率
    - terminal_growth: 永续增长率
    """
    # 计算平均FCF
    avg_fcf = sum(fcf_list) / len(fcf_list)
    
    # 预测未来5年FCF
    future_fcf = []
    for i in range(1, 6):
        fcf = avg_fcf * ((1 + growth_rate) ** i)
        future_fcf.append(fcf)
    
    # 计算现值
    pv_fcf = []
    for i, fcf in enumerate(future_fcf, 1):
        pv = fcf / ((1 + discount_rate) ** i)
        pv_fcf.append(pv)
    
    # 计算终值
    terminal_value = future_fcf[-1] * (1 + terminal_growth) / (discount_rate - terminal_growth)
    pv_terminal = terminal_value / ((1 + discount_rate) ** 5)
    
    # 企业价值
    enterprise_value = sum(pv_fcf) + pv_terminal
    
    return enterprise_value

# 使用示例
fcf_history = [50000, 55000, 60000, 65000, 70000]  # 百万港币
enterprise_value = dcf_valuation(fcf_history)
print(f"企业价值: {enterprise_value:.2f} 百万港币")
```

### 3. 相对估值分析
```python
def relative_valuation(target_pe, target_growth, industry_avg_pe, industry_avg_growth):
    """
    PEG相对估值分析
    
    PEG = PE / 增长率
    PEG < 1: 低估
    PEG = 1: 合理
    PEG > 1: 高估
    """
    target_peg = target_pe / (target_growth * 100)
    industry_peg = industry_avg_pe / (industry_avg_growth * 100)
    
    # 计算相对估值
    relative_discount = (target_peg - industry_peg) / industry_peg * 100
    
    return {
        'target_peg': round(target_peg, 2),
        'industry_peg': round(industry_peg, 2),
        'relative_discount': round(relative_discount, 1)
    }

# 使用示例
result = relative_valuation(
    target_pe=18.5,
    target_growth=0.15,  # 15%增长
    industry_avg_pe=22.0,
    industry_avg_growth=0.12  # 12%增长
)
print(f"目标PEG: {result['target_peg']}")
print(f"行业PEG: {result['industry_peg']}")
print(f"相对折价: {result['relative_discount']}%")
```

### 4. 估值区间分析
```python
def valuation_range(historical_pe, current_price):
    """
    基于历史PE计算估值区间
    """
    pe_min = min(historical_pe)
    pe_max = max(historical_pe)
    pe_median = sorted(historical_pe)[len(historical_pe)//2]
    pe_q1 = sorted(historical_pe)[len(historical_pe)//4]
    pe_q3 = sorted(historical_pe)[len(historical_pe)*3//4]
    
    # 计算当前EPS
    current_pe = historical_pe[-1]
    current_eps = current_price / current_pe
    
    # 计算估值区间
    price_min = current_eps * pe_min
    price_q1 = current_eps * pe_q1
    price_median = current_eps * pe_median
    price_q3 = current_eps * pe_q3
    price_max = current_eps * pe_max
    
    return {
        'min': round(price_min, 2),
        'q1': round(price_q1, 2),
        'median': round(price_median, 2),
        'q3': round(price_q3, 2),
        'max': round(price_max, 2),
        'current': current_price
    }
```

---

## 完整估值分析流程

### 步骤1: 获取市场整体估值
```bash
# 获取恒生指数估值及分位数
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI"], "date": "2024-12-31", "metricsList": ["pe_ttm.mcw", "pe_ttm.y10.mcw.cvpos", "pb.mcw", "pb.y10.mcw.cvpos", "dyr.mcw", "dyr.y10.mcw.cvpos"]}' \
  --columns "date,pe_ttm.mcw,pe_ttm.y10.mcw.cvpos,pb.mcw,pb.y10.mcw.cvpos,dyr.mcw,dyr.y10.mcw.cvpos"
```

### 步骤2: 获取行业估值排名
```bash
# 获取所有行业估值
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"date": "2024-12-31", "metricsList": ["pe_ttm.mcw", "pe_ttm.y10.mcw.cvpos", "pb.mcw", "dyr.mcw"]}' \
  --columns "industryCode,pe_ttm.mcw,pe_ttm.y10.mcw.cvpos,pb.mcw,dyr.mcw" \
  --limit 50
```

### 步骤3: 获取个股估值分析
```bash
# 获取个股估值指标
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"stockCodes": ["00700"], "date": "2024-12-31", "metricsList": ["pe", "pe.y10.cvpos", "pb", "pb.y10.cvpos", "dyr", "mc", "roe"]}' \
  --columns "date,pe,pe.y10.cvpos,pb,pb.y10.cvpos,dyr,mc,roe"
```

### 步骤4: 获取财务数据（DCF估值）
```bash
# 获取历史FCF数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fs/non_financial" \
  --params '{"stockCodes": ["00700"], "startDate": "2020-01-01", "endDate": "2024-12-31", "metricsList": ["fcf", "np", "revenue"]}' \
  --columns "date,fcf,np,revenue" \
  --limit 20
```

---

## 参数说明

- `--suffix`: API 路径
- `--params`: JSON 格式参数
  - `stockCodes`: 股票/指数/行业代码数组
  - `date`: 指定日期
  - `startDate/endDate`: 日期范围
  - `metricsList`: 指标列表
- `--columns`: 指定返回字段（推荐使用）
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

### 核心 API ⭐
- `hk/index/fundamental` - 港股指数估值（最重要）
- `hk.industry.fundamental.hsi` - 港股行业估值（最重要）
- `hk/company/fundamental/non_financial` - 港股个股估值（最重要）

### 辅助 API
- `hk/company/fs/non_financial` - 港股财务报表（DCF估值）
- `hk.industry` - 行业分类信息
- `hk/company` - 港股公司信息
- `hk/company.industries` - 个股行业归属
- `hk/company/dividend` - 分红数据（DDM估值）

---

## 数据更新频率

- **估值数据**: 每日更新
- **财务数据**: 季度更新
- **历史数据**: 10年以上
- **分位数**: 实时计算

---

## 缺失数据说明

以下数据理杏仁API无法直接提供，需要通过计算或外部数据源补充：

### 1. PCF（市现率）数据
- **问题**: API未提供PCF指标
- **替代方案**: 使用PE、PB、PS进行估值分析

### 2. EV/EBITDA数据
- **问题**: API未提供企业价值倍数
- **替代方案**: 通过财务数据自行计算

### 3. 分析师目标价
- **问题**: API未提供分析师预测数据
- **替代方案**: 使用DCF、DDM等模型自行估值

### 4. 增长率预测
- **问题**: API未提供未来增长率预测
- **替代方案**: 基于历史数据推算或使用行业平均

### 5. 折现率参数
- **问题**: API未提供WACC等折现率
- **替代方案**: 使用市场平均或自行计算

---

## 使用示例

### 示例1: 市场整体估值分析

```bash
# 1. 获取恒生指数估值
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI"], "date": "2024-12-31", "metricsList": ["pe_ttm.mcw", "pe_ttm.y10.mcw.cvpos", "pb.mcw", "pb.y10.mcw.cvpos", "dyr.mcw", "dyr.y10.mcw.cvpos"]}' \
  --columns "date,pe_ttm.mcw,pe_ttm.y10.mcw.cvpos,pb.mcw,pb.y10.mcw.cvpos,dyr.mcw,dyr.y10.mcw.cvpos"

# 2. 计算估值评分（需要脚本处理）
# 输出示例：
# 恒生指数估值水平:
# PE (TTM): 12.5x (历史分位数: 35%)
# PB (MRQ): 1.2x (历史分位数: 40%)
# 股息率: 3.2% (历史分位数: 65%)
# 估值评分: 65/100 (适中偏低)
```

### 示例2: 行业估值对比

```bash
# 1. 获取所有行业估值
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"date": "2024-12-31", "metricsList": ["pe_ttm.mcw", "pe_ttm.y10.mcw.cvpos", "pb.mcw"]}' \
  --columns "industryCode,pe_ttm.mcw,pe_ttm.y10.mcw.cvpos,pb.mcw" \
  --limit 50

# 2. 获取行业名称
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry" \
  --params '{}' \
  --columns "industryCode,industryName"

# 3. 排序并输出TOP10低估行业（需要脚本处理）
```

### 示例3: 个股DCF估值

```bash
# 1. 获取历史FCF数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fs/non_financial" \
  --params '{"stockCodes": ["00700"], "startDate": "2020-01-01", "endDate": "2024-12-31", "metricsList": ["fcf", "np"]}' \
  --columns "date,fcf,np" \
  --limit 20

# 2. 获取当前市值
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"stockCodes": ["00700"], "date": "2024-12-31", "metricsList": ["mc"]}' \
  --columns "mc"

# 3. 计算DCF估值（需要脚本处理）
# 4. 对比当前市值，计算溢价/折价
```

---

## 查找更多 API

```bash
# 查看完整 API 列表
cat skills/lixinger-data-query/SKILL.md

# 搜索估值相关 API
grep -r "fundamental" skills/lixinger-data-query/api_new/api-docs/

# 查看具体 API 文档
cat skills/lixinger-data-query/api_new/api-docs/hk_index_fundamental.md
cat skills/lixinger-data-query/api_new/api-docs/hk_industry_fundamental_hsi.md
cat skills/lixinger-data-query/api_new/api-docs/hk_company_fundamental_non-financial.md
```

---

## 相关文档

- **API 文档**: `skills/lixinger-data-query/SKILL.md`
- **使用指南**: `skills/lixinger-data-query/LLM_USAGE_GUIDE.md`
- **Skill 说明**: `../SKILL.md`

---

**更新日期**: 2026-02-24  
**版本**: v1.0.0
