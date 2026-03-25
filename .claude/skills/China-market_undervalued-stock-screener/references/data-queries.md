# 数据查询指南（低估值股票筛选）

## 概述

本文档记录了使用理杏仁开放平台进行 A 股低估值股票筛选的数据查询方法。

## 数据来源

- **平台**: 理杏仁开放平台 (https://www.lixinger.com/open/api)
- **数据范围**: 沪深 300 指数成分股
- **数据时间**: 2025 年 9 月 30 日（财务数据）、2025 年 12 月 31 日（估值数据）

## 查询工具

使用 `query_tool.py` 进行数据查询，位于 `.claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py`

## API 接口

### 1. 获取指数成分股

**API**: `cn/index/constituents`

**用途**: 获取沪深 300 指数成分股列表

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/constituents" \
  --params '{"date": "latest", "stockCodes": ["000300"]}' \
  --flatten "constituents" \
  --columns "stockCode" \
  --limit 300
```

### 2. 获取基本面数据

**API**: `cn/company/fundamental/non_financial`

**用途**: 获取股票的估值指标（PE、PB、市值、股息率等）

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"date": "2025-12-31", "stockCodes": ["600519", "000858"], "metricsList": ["pe_ttm", "pb", "mc", "dyr"]}' \
  --columns "stockCode,pe_ttm,pb,mc,dyr" \
  --limit 100
```

**指标说明**:
- `pe_ttm`: 滚动市盈率（TTM）
- `pb`: 市净率
- `mc`: 总市值
- `dyr`: 股息率

### 3. 获取财务数据

**API**: `cn/company/fs/non_financial`

**用途**: 获取股票的财务指标（ROE、营收、净利润等）

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"date": "2025-09-30", "stockCodes": ["600519"], "metricsList": ["q.ps.toi.t", "q.ps.toi.t_y2y", "q.ps.np.t", "q.ps.np.t_y2y", "q.ps.gp_m.t", "q.bs.ta.t", "q.bs.tl.t", "q.ps.wroe.t"]}' \
  --columns "stockCode,q.ps.toi.t,q.ps.toi.t_y2y,q.ps.np.t,q.ps.np.t_y2y,q.ps.gp_m.t,q.bs.ta.t,q.bs.tl.t,q.ps.wroe.t" \
  --limit 100
```

**指标说明**:
- `q.ps.toi.t`: 营业收入（累计值）
- `q.ps.toi.t_y2y`: 营业收入同比增长率
- `q.ps.np.t`: 净利润（累计值）
- `q.ps.np.t_y2y`: 净利润同比增长率
- `q.ps.gp_m.t`: 毛利率
- `q.bs.ta.t`: 总资产
- `q.bs.tl.t`: 总负债
- `q.ps.wroe.t`: 加权 ROE

## 筛选条件

### 低估值股票筛选标准

1. **估值指标**:
   - PE (TTM) < 15
   - PB < 2

2. **盈利能力**:
   - ROE > 5%
   - 毛利率 > 0%

3. **成长性**:
   - 营收增长率 > -10%
   - 净利润增长率 > -10%

4. **财务健康**:
   - 资产负债率 < 80%

## 注意事项

1. **API 限制**: 每次查询最多只能获取 100 只股票的数据
2. **数据时间**: 财务数据为季度数据，估值数据为日度数据
3. **行业差异**: 不同行业的估值中枢不同，需在行业内比较
4. **风险提示**: 低估值不等于投资机会，需结合基本面分析

## 相关文件

- 筛选结果: `undervalued_stocks_relaxed.csv`
- 筛选报告: `undervalued_stocks_report.md`
- 沪深 300 成分股: `hs300_all.csv`

