# 公告披露监控数据查询

### 概述

本节记录了使用理杏仁开放平台进行 A 股上市公司公告披露监控的数据查询方法。公告披露监控是投资决策的重要环节，用于识别重大事项、风险提示、业绩变动等关键信息。

### 数据来源

- **平台**: 理杏仁开放平台 (https://www.lixinger.com/open/api)
- **数据范围**: A 股上市公司公告、股价、基本面数据
- **数据时间**: 实时更新，T 日晚间可获取 T 日公告

### API 接口

#### 1. 获取公告数据

**API**: `cn/company/announcement`

**用途**: 获取上市公司公告信息，包括公告标题、类型、披露时间等

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/announcement" \
  --params '{"stockCode": "300750", "startDate": "2026-03-01", "endDate": "2026-03-24"}' \
  --columns "date,linkText,linkType,types" \
  --limit 50
```

**参数说明**:
- `stockCode`: 股票代码（必填）
- `startDate`: 公告起始日期，格式 YYYY-MM-DD（必填）
- `endDate`: 公告结束日期，格式 YYYY-MM-DD（选填，默认上周一）
- `limit`: 返回最近数据的数量（选填）

**返回字段说明**:
- `date`: 公告日期
- `linkText`: 公告标题
- `linkType`: 链接类型（PDF 等）
- `types`: 公告类型数组（详见下方类型映射）

**公告类型映射**:
- `fs`: 财务报表
- `fsfc`: 业绩预告
- `o_d`: 经营数据
- `eac`: 权益分派
- `bm`: 董事会
- `sm`: 监事会
- `shm`: 股东大会
- `so`: 股权激励
- `ntsu`: 解禁
- `b`: 债券
- `c_b`: 可转换债券
- `eat`: 股权变更
- `c_rp`: 澄清及风险提示
- `irs`: 投资者关系
- `i_l`: 问询函
- `sa`: 配股
- `spo`: 增发
- `srp`: 回购
- `ipo`: IPO
- `other`: 其它

#### 2. 获取股价数据

**API**: `cn/company/candlestick`

**用途**: 获取 K 线数据，用于分析公告前后股价变化

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode": "300750", "startDate": "2026-02-01", "endDate": "2026-03-24", "type": "lxr_fc_rights"}' \
  --columns "date,open,close,high,low,volume,amount,change,to_r" \
  --limit 50
```

**参数说明**:
- `stockCode`: 股票代码（必填）
- `type`: 复权类型（选填，默认不复权）
  - `ex_rights`: 不复权
  - `lxr_fc_rights`: 理杏仁前复权
  - `fc_rights`: 前复权
  - `bc_rights`: 后复权
- `startDate`: 起始日期（选填）
- `endDate`: 结束日期（选填）
- `date`: 指定日期（选填）
- `limit`: 返回最近数据的数量（选填）

**返回字段说明**:
- `date`: 数据时间
- `open`: 开盘价
- `close`: 收盘价
- `high`: 最高价
- `low`: 最低价
- `volume`: 成交量
- `amount`: 成交金额
- `change`: 涨跌幅
- `to_r`: 换手率

#### 3. 获取基本面数据

**API**: `cn/company/fundamental/non_financial`

**用途**: 获取估值指标，用于分析公告对估值的影响

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["300750"], "date": "2026-03-23", "metricsList": ["pe_ttm", "pb", "ps_ttm", "dyr", "mc"]}' \
  --columns "date,stockCode,pe_ttm,pb,ps_ttm,dyr,mc" \
  --limit 10
```

**参数说明**:
- `stockCodes`: 股票代码数组（必填）
- `date`: 指定日期（选填，与 startDate 二选一）
- `startDate`: 起始日期（选填，与 date 二选一）
- `endDate`: 结束日期（选填）
- `metricsList`: 指标数组（必填）
  - `pe_ttm`: PE-TTM（滚动市盈率）
  - `pb`: PB（市净率）
  - `ps_ttm`: PS-TTM（滚动市销率）
  - `dyr`: 股息率
  - `mc`: 总市值
- `limit`: 返回最近数据的数量（选填）

### 分析框架

#### 公告分类

1. **业绩类**: 业绩预告、业绩快报、年报、季报
2. **重组类**: 并购重组、资产注入、股权转让
3. **风险类**: 风险提示、诉讼仲裁、违规处罚
4. **股权类**: 股东减持、股权质押、解禁
5. **其他类**: 停牌复牌、分红派息、股东大会

#### 关键指标

1. **公告重要性指标**:
   - 重要性评分（0-100）
   - 关键词匹配度
   - 历史平均影响

2. **情绪倾向指标**:
   - 利好词占比
   - 利空词占比
   - 情绪得分（-1 ~ +1）

3. **市场反应指标**:
   - 公告后涨跌幅
   - 公告后成交量变化
   - 公告后换手率变化

#### 监控要点

1. **触发监控**:
   - 业绩预告（预增/预减 >= 30%）
   - 重大重组（并购、资产注入、控制权变更）
   - 风险提示（诉讼、违规、ST 风险）
   - 股东减持（减持比例 >= 1%）
   - 股权质押（质押比例 >= 50%）
   - 违规处罚（证监会、交易所）
   - 停牌复牌（重大事项）

2. **A 股特殊注意**:
   - T+1 交易制度: 盘后公告次日才能交易
   - 涨跌停限制: 利好/利空公告可能连续涨跌停
   - 停牌影响: 重大事项停牌可能持续数月
   - 公告披露时间: 大部分在盘后披露（15:00-24:00）

### 使用示例

**示例: 宁德时代公告披露监控**

```bash
# 1. 获取公告数据
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/announcement" \
  --params '{"stockCode": "300750", "startDate": "2026-03-01", "endDate": "2026-03-24"}' \
  --columns "date,linkText,linkType,types" \
  --limit 50

# 2. 获取股价数据
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode": "300750", "startDate": "2026-03-01", "endDate": "2026-03-24", "type": "lxr_fc_rights"}' \
  --columns "date,open,close,high,low,volume,change,to_r" \
  --limit 20

# 3. 获取基本面数据
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["300750"], "startDate": "2026-03-01", "endDate": "2026-03-24", "metricsList": ["pe_ttm", "pb", "dyr", "mc"]}' \
  --columns "date,stockCode,pe_ttm,pb,dyr,mc" \
  --limit 20
```

### 注意事项

1. **数据时效性**: 公告数据 T 日晚间可获取，股价数据实时更新
2. **公告解读**: 需要结合公告标题和类型判断重要性和情绪倾向
3. **市场反应**: 公告发布后需观察 1-3 日的市场反应
4. **风险控制**: 关注风险提示、违规处罚等负面公告
5. **停牌风险**: 重大事项停牌期间无法交易，需提前评估

### 相关文件

- 分析报告: `analysis_20260324_disclosure_monitor.md`
- 技能文档: `.claude/skills/China-market_disclosure-notice-monitor/`

