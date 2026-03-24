# 商誉风险监控数据查询

### 概述

本节记录了使用理杏仁开放平台进行 A 股上市公司商誉风险监控的数据查询方法。商誉减值是 A 股重要的业绩地雷，商誉风险监控是风险管理的关键环节。

### 数据来源

- **平台**: 理杏仁开放平台 (https://www.lixinger.com/open/api)
- **数据范围**: A 股上市公司商誉、财务、估值、股东等数据
- **数据时间**: 季度数据（一季报、半年报、三季报、年报）

### 分析框架

商誉风险监控包括以下核心模块：

1. **商誉规模评估**: 商誉余额、商誉占净资产比例、商誉占市值比例
2. **业绩承诺监控**: 业绩承诺完成率、累计完成率、业绩缺口
3. **商誉减值风险评估**: 减值风险等级、潜在减值金额、减值影响分析
4. **并购标的质量评估**: 并购溢价率、并购 PE、标的盈利能力
5. **商誉变化监控**: 商誉增加额、商誉减值额、减值比例

### API 接口

#### 1. 获取商誉数据（核心）

**API**: `cn/company/fs/non_financial`

**用途**: 获取股票的商誉数据，用于商誉规模评估

**查询示例**:
```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["002594"], "startDate": "2021-01-01", "endDate": "2026-03-24", "metricsList": ["q.bs.goodwill.t", "q.bs.tse.t", "q.bs.ta.t", "q.bs.intangible.t", "q.ps.np.t"]}' \
  --columns "date,stockCode,q.bs.goodwill.t,q.bs.tse.t,q.bs.ta.t,q.bs.intangible.t,q.ps.np.t" \
  --limit 100
```

**商誉指标说明**:
- `q.bs.goodwill.t`: 商誉（账面价值）
- `q.bs.tse.t`: 股东权益（净资产）
- `q.bs.ta.t`: 总资产
- `q.bs.intangible.t`: 无形资产
- `q.ps.np.t`: 净利润

#### 2. 获取估值数据

**API**: `cn/company/fundamental/non_financial`

**用途**: 获取市值数据，用于计算商誉占市值比例

**查询示例**:
```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["002594"], "date": "2026-03-24", "metricsList": ["mc", "pe_ttm", "pb"]}' \
  --columns "stockCode,name,mc,pe_ttm,pb"
```

**估值指标说明**:
- `mc`: 总市值
- `pe_ttm`: PE-TTM（滚动市盈率）
- `pb`: PB（市净率）

#### 3. 获取财务报表数据

**API**: `cn/company/fs/non_financial`

**用途**: 获取财务数据，用于评估公司盈利能力和商誉减值风险

**查询示例**:
```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["002594"], "startDate": "2021-01-01", "endDate": "2026-03-24", "metricsList": ["q.ps.toi.t", "q.ps.toi.t_y2y", "q.ps.np.t", "q.ps.np.t_y2y", "q.ps.gp_m.t", "q.ps.wroe.t"]}' \
  --columns "date,stockCode,q.ps.toi.t,q.ps.toi.t_y2y,q.ps.np.t,q.ps.np.t_y2y,q.ps.gp_m.t,q.ps.wroe.t" \
  --limit 100
```

**财务指标说明**:
- `q.ps.toi.t`: 营业收入（累计值）
- `q.ps.toi.t_y2y`: 营业收入同比增长率
- `q.ps.np.t`: 净利润（累计值）
- `q.ps.np.t_y2y`: 净利润同比增长率
- `q.ps.gp_m.t`: 毛利率
- `q.ps.wroe.t`: 加权 ROE

#### 4. 获取公告数据

**API**: `cn/company/announcement`

**用途**: 获取公司公告，用于识别并购重组、业绩承诺、商誉减值等信息

**查询示例**:
```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/announcement" \
  --params '{"stockCode": "002594", "startDate": "2025-01-01", "endDate": "2026-03-24"}' \
  --columns "date,linkText,linkType,types" \
  --limit 50
```

**公告类型关注**:
- `fs`: 财务报表
- `fsfc`: 业绩预告
- `c_rp`: 澄清及风险提示
- `spo`: 增发
- `bm`: 董事会决议

#### 5. 获取股东数据

**API**: `cn/company/major-shareholders-shares-change`

**用途**: 获取股东增减持数据，用于评估股东对公司商誉风险的态度

**查询示例**:
```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/major-shareholders-shares-change" \
  --params '{"stockCode": "002594", "startDate": "2023-01-01"}' \
  --columns "date,shareholderName,changeReason,changeAmount,sharesRatio"
```

### 核心指标计算公式

#### 商誉规模指标

| 指标 | 公式 | 风险阈值 |
|------|------|----------|
| 商誉占净资产比例 | 商誉 / 净资产 × 100% | >= 50%（高风险） |
| 商誉占市值比例 | 商誉 / 市值 × 100% | >= 30%（高风险） |
| 商誉占总资产比例 | 商誉 / 总资产 × 100% | >= 20%（关注） |

#### 业绩承诺指标

| 指标 | 公式 | 风险阈值 |
|------|------|----------|
| 业绩承诺完成率 | 实际净利润 / 承诺净利润 × 100% | <= 80%（高风险） |
| 业绩缺口 | 承诺净利润 - 实际净利润 | 正数（风险） |

#### 商誉减值风险指标

| 指标 | 公式 | 说明 |
|------|------|------|
| 潜在减值金额 | 商誉 × 减值比例估计 | 基于历史减值比例 |
| 减值对EPS影响 | 潜在减值 / 总股本 | 元/股 |
| 减值对净资产影响 | 潜在减值 / 净资产 × 100% | 百分比 |

### 风险等级分类

#### 高风险（建议回避）

1. **商誉占净资产 >= 50%** 且 **业绩承诺完成率 <= 80%**
2. **商誉占市值 >= 30%** 且 **股价年跌幅 >= 30%**
3. **历史减值次数 >= 2次** 且 **累计减值金额 >= 商誉余额 × 50%**

#### 中风险（谨慎关注）

1. **商誉占净资产 30%-50%** 且 **业绩承诺完成率 80%-90%**
2. **商誉占市值 20%-30%** 且 **标的业绩下滑 >= 20%**
3. **承诺期最后一年** 且 **并购溢价率 >= 300%**

#### 低风险（常规监控）

1. **商誉占净资产 < 30%**
2. **业绩承诺完成率 > 90%**
3. **标的业绩稳定增长**

### 完整查询流程示例

**示例: 商誉风险监控完整数据查询**

```bash
# 1. 获取商誉数据（5年数据）
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["002594"], "startDate": "2021-01-01", "endDate": "2026-03-24", "metricsList": ["q.bs.goodwill.t", "q.bs.tse.t", "q.bs.ta.t", "q.bs.intangible.t", "q.ps.np.t"]}' \
  --columns "date,stockCode,q.bs.goodwill.t,q.bs.tse.t,q.bs.ta.t,q.bs.intangible.t,q.ps.np.t" \
  --limit 100

# 2. 获取估值数据
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["002594"], "date": "2026-03-24", "metricsList": ["mc", "pe_ttm", "pb"]}' \
  --columns "stockCode,name,mc,pe_ttm,pb"

# 3. 获取财务数据
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["002594"], "startDate": "2021-01-01", "endDate": "2026-03-24", "metricsList": ["q.ps.toi.t", "q.ps.toi.t_y2y", "q.ps.np.t", "q.ps.np.t_y2y", "q.ps.gp_m.t", "q.ps.wroe.t"]}' \
  --columns "date,stockCode,q.ps.toi.t,q.ps.toi.t_y2y,q.ps.np.t,q.ps.np.t_y2y,q.ps.gp_m.t,q.ps.wroe.t" \
  --limit 100

# 4. 获取公告数据
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/announcement" \
  --params '{"stockCode": "002594", "startDate": "2025-01-01", "endDate": "2026-03-24"}' \
  --columns "date,linkText,linkType,types" \
  --limit 50

# 5. 获取股东数据
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/major-shareholders-shares-change" \
  --params '{"stockCode": "002594", "startDate": "2023-01-01"}' \
  --columns "date,shareholderName,changeReason,changeAmount,sharesRatio" \
  --limit 50
```

### 注意事项

1. **数据时间**: 财务数据为季度数据，商誉数据在年报中披露最完整
2. **商誉减值时点**: 商誉减值通常在年报中计提，四季度业绩预告时预警
3. **业绩承诺期**: 业绩承诺期通常 3 年，承诺期结束后风险上升
4. **行业差异**: 传媒、计算机、医药等行业并购多，商誉风险较大
5. **A 股特殊性**: 商誉不摊销，仅在减值时一次性计提，减值不可转回

### A股特殊注意

1. **T+1交易制度**: 商誉减值公告后无法当日卖出，需要提前预警
2. **涨跌停限制**: 商誉大额减值可能导致连续跌停，无法卖出
3. **停牌影响**: 重大事项停牌可能持续数月，风险累积
4. **业绩承诺补偿**: 业绩未完成时原股东补偿，但补偿往往不足
5. **监管趋严**: 减值测试要求提高，商誉减值问询增加

### 相关文件

- 技能文档: `.claude/skills/China-market_goodwill-risk-monitor/`
- 方法论文档: `.claude/skills/China-market_goodwill-risk-monitor/references/methodology.md`
- 输出模板: `.claude/skills/China-market_goodwill-risk-monitor/references/output-template.md`
- 查询工具: `.claude/skills/lixinger-data-query/scripts/query_tool.py`

