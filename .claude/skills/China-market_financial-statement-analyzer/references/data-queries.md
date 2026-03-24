# 财务报表深度分析数据查询

### 概述

本节记录了使用理杏仁开放平台进行 A 股上市公司财务报表深度分析的数据查询方法。财务报表分析是评估公司盈利能力、财务健康状况、盈利质量和运营效率的重要工具。

### 数据来源

- **平台**: 理杏仁开放平台 (https://www.lixinger.com/open/api)
- **数据范围**: A 股上市公司财务报表、基本面、股东、质押等数据
- **数据时间**: 季度数据（一季报、半年报、三季报、年报）

### 分析框架

财务报表分析包括以下核心模块：

1. **杜邦分析**: 5 因子分解 ROE（税负系数、利息负担系数、营业利润率、资产周转率、权益乘数）
2. **盈利质量评估**: 应计比率、现金转化率、收入确认质量、非经常性项目依赖
3. **财务健康评分**: Altman Z 值、Piotroski F 值、Beneish M 值
4. **营运资本分析**: 现金转化周期（DSO + DIO - DPO）
5. **资产负债表风险评估**: 商誉、关联交易、在建工程等
6. **业务分部分析**: 各分部营收、利润率、资本密集度
7. **同行基准比较**: 与竞争对手的关键指标对比

### API 接口

#### 1. 获取财务报表数据（核心）

**API**: `cn/company/fs/non_financial`

**用途**: 获取股票的财务指标，包括利润表、资产负债表、现金流量表数据

**查询示例**:
```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["002594"], "startDate": "2021-01-01", "endDate": "2026-03-24", "metricsList": ["q.ps.toi.t", "q.ps.toi.t_y2y", "q.ps.np.t", "q.ps.np.t_y2y", "q.ps.gp_m.t", "q.bs.ta.t", "q.bs.tl.t", "q.ps.wroe.t", "q.ps.ebit.t", "q.bs.re.t", "q.ps.toi.t_qoq", "q.ps.np.t_qoq"]}' \
  --columns "date,stockCode,q.ps.toi.t,q.ps.toi.t_y2y,q.ps.np.t,q.ps.np.t_y2y,q.ps.gp_m.t,q.bs.ta.t,q.bs.tl.t,q.ps.wroe.t" \
  --limit 100
```

**杜邦分析指标说明**:
- `q.ps.toi.t`: 营业收入（累计值）
- `q.ps.toi.t_y2y`: 营业收入同比增长率
- `q.ps.np.t`: 净利润（累计值）
- `q.ps.np.t_y2y`: 净利润同比增长率
- `q.ps.gp_m.t`: 毛利率
- `q.bs.ta.t`: 总资产
- `q.bs.tl.t`: 总负债
- `q.ps.wroe.t`: 加权 ROE
- `q.ps.ebit.t`: EBIT（息税前利润）
- `q.bs.re.t`: 留存收益
- `q.ps.toi.t_qoq`: 营业收入环比增长率
- `q.ps.np.t_qoq`: 净利润环比增长率

#### 2. 获取估值数据

**API**: `cn/company/fundamental/non_financial`

**用途**: 获取估值指标，用于财务质量评估和同行比较

**查询示例**:
```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["002594"], "date": "2026-03-24", "metricsList": ["pe_ttm", "pb", "ps_ttm", "dyr", "mc", "ev_ebitda"]}' \
  --columns "stockCode,name,pe_ttm,pb,ps_ttm,dyr,mc,ev_ebitda"
```

**估值指标说明**:
- `pe_ttm`: PE-TTM（滚动市盈率）
- `pb`: PB（市净率）
- `ps_ttm`: PS-TTM（滚动市销率）
- `dyr`: 股息率
- `mc`: 总市值
- `ev_ebitda`: EV/EBITDA

#### 3. 获取股东数据

**API**: `cn/company/major-shareholders-shares-change`

**用途**: 获取股东增减持数据，用于股权结构分析

**查询示例**:
```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/major-shareholders-shares-change" \
  --params '{"stockCode": "002594", "startDate": "2023-01-01"}' \
  --columns "date,shareholderName,changeReason,changeAmount,sharesRatio"
```

#### 4. 获取质押数据

**API**: `cn/company/pledge`

**用途**: 获取股权质押数据，用于风险评估

**查询示例**:
```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/pledge" \
  --params '{"stockCode": "002594", "startDate": "2023-01-01"}' \
  --columns "date,pledgeRatio,pledgor,pledgee,pledgeShares"
```

#### 5. 获取现金流量表数据

**API**: `cn/company/fs/non_financial`

**用途**: 获取现金流量表数据，用于盈利质量评估

**查询示例**:
```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["002594"], "startDate": "2021-01-01", "endDate": "2026-03-24", "metricsList": ["q.cfs.nocf.t", "q.cfs.icf.t", "q.cfs.fcf.t", "q.cfs.nocf.t_y2y"]}' \
  --columns "date,stockCode,q.cfs.nocf.t,q.cfs.icf.t,q.cfs.fcf.t,q.cfs.nocf.t_y2y" \
  --limit 100
```

**现金流量指标说明**:
- `q.cfs.nocf.t`: 经营活动产生的现金流量净额
- `q.cfs.icf.t`: 投资活动产生的现金流量净额
- `q.cfs.fcf.t`: 筹资活动产生的现金流量净额
- `q.cfs.nocf.t_y2y`: 经营现金流同比增长率

#### 6. 获取资产负债表明细

**API**: `cn/company/fs/non_financial`

**用途**: 获取资产负债表明细数据，用于营运资本分析

**查询示例**:
```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["002594"], "startDate": "2021-01-01", "endDate": "2026-03-24", "metricsList": ["q.bs.ar.t", "q.bs.inv.t", "q.bs.ap.t", "q.bs.cash.t", "q.bs.goodwill.t", "q.bs.intangible.t", "q.bs.construction_in_progress.t", "q.bs.other_receivables.t"]}' \
  --columns "date,stockCode,q.bs.ar.t,q.bs.inv.t,q.bs.ap.t,q.bs.cash.t,q.bs.goodwill.t" \
  --limit 100
```

**资产负债表指标说明**:
- `q.bs.ar.t`: 应收账款
- `q.bs.inv.t`: 存货
- `q.bs.ap.t`: 应付账款
- `q.bs.cash.t`: 货币资金
- `q.bs.goodwill.t`: 商誉
- `q.bs.intangible.t`: 无形资产
- `q.bs.construction_in_progress.t`: 在建工程
- `q.bs.other_receivables.t`: 其他应收款

### 完整查询流程示例

**示例: 比亚迪（002594）财务报表分析数据查询**

```bash
# 1. 获取财务报表数据（5年数据）
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["002594"], "startDate": "2021-01-01", "endDate": "2026-03-24", "metricsList": ["q.ps.toi.t", "q.ps.toi.t_y2y", "q.ps.np.t", "q.ps.np.t_y2y", "q.ps.gp_m.t", "q.bs.ta.t", "q.bs.tl.t", "q.ps.wroe.t", "q.ps.ebit.t", "q.bs.re.t"]}' \
  --columns "date,stockCode,q.ps.toi.t,q.ps.toi.t_y2y,q.ps.np.t,q.ps.np.t_y2y,q.ps.gp_m.t,q.bs.ta.t,q.bs.tl.t,q.ps.wroe.t,q.ps.ebit.t,q.bs.re.t" \
  --limit 100

# 2. 获取现金流量表数据
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["002594"], "startDate": "2021-01-01", "endDate": "2026-03-24", "metricsList": ["q.cfs.nocf.t", "q.cfs.icf.t", "q.cfs.fcf.t", "q.cfs.nocf.t_y2y"]}' \
  --columns "date,stockCode,q.cfs.nocf.t,q.cfs.icf.t,q.cfs.fcf.t,q.cfs.nocf.t_y2y" \
  --limit 100

# 3. 获取资产负债表明细
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["002594"], "startDate": "2021-01-01", "endDate": "2026-03-24", "metricsList": ["q.bs.ar.t", "q.bs.inv.t", "q.bs.ap.t", "q.bs.cash.t", "q.bs.goodwill.t", "q.bs.intangible.t", "q.bs.construction_in_progress.t", "q.bs.other_receivables.t"]}' \
  --columns "date,stockCode,q.bs.ar.t,q.bs.inv.t,q.bs.ap.t,q.bs.cash.t,q.bs.goodwill.t,q.bs.intangible.t,q.bs.construction_in_progress.t,q.bs.other_receivables.t" \
  --limit 100

# 4. 获取估值数据
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["002594"], "date": "2026-03-24", "metricsList": ["pe_ttm", "pb", "ps_ttm", "dyr", "mc", "ev_ebitda"]}' \
  --columns "stockCode,name,pe_ttm,pb,ps_ttm,dyr,mc,ev_ebitda"

# 5. 获取股东数据
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/major-shareholders-shares-change" \
  --params '{"stockCode": "002594", "startDate": "2023-01-01"}' \
  --columns "date,shareholderName,changeReason,changeAmount,sharesRatio" \
  --limit 50

# 6. 获取质押数据
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/pledge" \
  --params '{"stockCode": "002594", "startDate": "2023-01-01"}' \
  --columns "date,pledgeRatio,pledgor,pledgee,shareholderName" \
  --limit 50
```

### 关键指标计算公式

#### 杜邦分析（5因子分解）

```
ROE = 税负系数 × 利息负担系数 × 营业利润率 × 资产周转率 × 权益乘数
```

| 组成部分 | 公式 | 揭示内容 |
|---------|------|---------|
| 税负系数 | 净利润 / 税前利润 | 税收效率 |
| 利息负担系数 | 税前利润 / EBIT | 债务成本影响 |
| 营业利润率 | EBIT / 营业收入 | 运营效率 |
| 资产周转率 | 营业收入 / 总资产 | 资产利用效率 |
| 权益乘数 | 总资产 / 股东权益 | 财务杠杆 |

#### 财务健康评分

| 模型 | 用途 | 组成部分 |
|------|------|---------|
| Altman Z值 | 破产预测 | 营运资本、留存收益、EBIT、市值、营收——均相对于总资产 |
| Piotroski F值 | 财务实力 | 9个二元信号，涵盖盈利能力、杠杆和效率 |
| Beneish M值 | 盈利操纵检测 | 8个变量，衡量财务数据中的异常 |

#### 营运资本分析

| 指标 | 公式 | 揭示内容 |
|------|------|---------|
| 应收账款周转天数（DSO） | (应收账款 / 营业收入) × 365 | 收款效率 |
| 存货周转天数（DIO） | (存货 / 营业成本) × 365 | 存货管理 |
| 应付账款周转天数（DPO） | (应付账款 / 营业成本) × 365 | 付款实践 |
| 现金转化周期 | DSO + DIO − DPO | 营运资本效率 |

### 盈利质量评估标准

| 测试 | 衡量内容 | 红灯阈值 |
|------|---------|---------|
| 应计比率 | 非现金盈利占比 | > 总资产的10% |
| 现金转化率 | 经营现金流 / 净利润 | 持续 < 0.8 |
| 收入确认 | 收入增长 vs 应收账款增长 | 应收增速超过收入 |
| 合同负债/预收 | 合同负债趋势 | 下降（提前确认收入） |
| 非经常性项目 | 一次性收益/费用频率 | "非经常性"项目每年出现 |
| 政府补助依赖 | 政府补助占净利润比例 | > 30%（利润可持续性存疑） |

### 资产负债表风险评估

| 风险领域 | 检查内容 |
|---------|---------|
| 商誉/无形资产 | 相对净资产的规模；减值风险（A股并购商誉减值是常见雷区） |
| 关联交易 | 与控股股东及关联方的交易规模和定价公允性 |
| 应收票据及应收账款 | 商业承兑汇票的信用风险 |
| 在建工程 | 长期不结转固定资产的项目（可能的费用资本化） |
| 其他应收款 | 对关联方的资金占用 |
| 股份支付 | 稀释影响 |
| 有息负债到期结构 | 短期偿债压力 vs 现金/再融资能力 |
| 股权质押 | 大股东股权质押比例 |

### 注意事项

1. **数据时间**: 财务数据为季度数据，需要按年报、半年报、季报分别分析
2. **扣非净利润**: 关注扣除非经常性损益后的净利润，这是评估 A 股公司持续经营能力的更可靠指标
3. **A 股特有陷阱**: 关联交易转移利润、政府补助撑利润、在建工程长期不转固、商业承兑汇票坏账风险
4. **趋势比绝对值重要**: 下降的毛利率比低但稳定的毛利率更令人担忧
5. **读附注**: 财务报表中最重要的信息往往在附注中

### 相关文件

- 分析报告: `analysis_20260324_byd_financial.md`
- 技能文档: `.claude/skills/China-market_financial-statement-analyzer/`
- 查询工具: `.claude/skills/lixinger-data-query/scripts/query_tool.py`

