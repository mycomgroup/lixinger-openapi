# 数据查询指南

本文档说明如何使用 `query_tool.py` 获取 ETF 配置分析所需的数据。

## 核心数据查询

### 1. 指数基本面数据（估值分析）

获取主要指数的PE、PB估值数据，用于判断市场估值水平和配置时机。

```bash
# 查询沪深300、中证500、创业板指的估值数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"date": "2024-12-31", "stockCodes": ["000300", "000905", "399006"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "pe_ttm.y10.mcw.cvpos", "pb.y10.mcw.cvpos", "mc"]}' \
  --limit 10
```

**参数说明**：
- `date`: 查询日期（YYYY-MM-DD 格式）
- `stockCodes`: 指数代码数组
  - `000300`: 沪深300指数
  - `000905`: 中证500指数
  - `399006`: 创业板指数
  - `000016`: 上证50指数
  - `399005`: 中小板指数
- `metricsList`: 指标列表（必须参数）
  - `pe_ttm.mcw`: 市盈率（市值加权）
  - `pb.mcw`: 市净率（市值加权）
  - `pe_ttm.y10.mcw.cvpos`: PE 10年历史分位数
  - `pb.y10.mcw.cvpos`: PB 10年历史分位数
  - `mc`: 市值

**推荐字段组合**：
- 估值分析：`["pe_ttm.mcw", "pb.mcw", "pe_ttm.y10.mcw.cvpos", "pb.y10.mcw.cvpos"]`
- 市值分析：`["mc", "cmc", "ecmc"]`
- 收益分析：`["dyr", "cp", "cpc"]`

### 2. 指数历史估值数据（时间序列）

获取指数的历史估值数据，用于分析估值趋势和历史分位数。

```bash
# 查询沪深300近1年的估值历史
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"startDate": "2024-01-01", "endDate": "2024-12-31", "stockCodes": ["000300"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "pe_ttm.y10.mcw.cvpos"]}' \
  --limit 365
```

**参数说明**：
- `startDate`: 开始日期（YYYY-MM-DD 格式）
- `endDate`: 结束日期（YYYY-MM-DD 格式，时间间隔不超过10年）
- `stockCodes`: 只能传入一个指数代码（使用时间范围时的限制）
- `metricsList`: 指标列表

**注意**：使用 `startDate` 时，`stockCodes` 只能包含一个指数代码。

### 3. 行业指数数据（行业配置）

获取行业指数的估值数据，用于行业ETF配置分析。

```bash
# 查询主要行业指数估值
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"date": "2024-12-31", "stockCodes": ["000807", "000808", "000809"], "metricsList": ["pe_ttm.mcw", "pb.mcw", "pe_ttm.y5.mcw.cvpos"]}' \
  --limit 10
```

**常用行业指数代码**：
- `000807`: 食品饮料
- `000808`: 医药生物
- `000809`: 电子
- `000810`: 计算机
- `000811`: 传媒
- `000812`: 通信
- `000813`: 银行
- `000814`: 非银金融

### 4. 指数成分股数据（持仓分析）

获取指数成分股列表，用于分析ETF持仓结构。

```bash
# 查询沪深300成分股
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/constituents" \
  --params '{"stockCode": "000300", "type": "normal", "date": "2024-12-31"}' \
  --columns "stockCode,stockName,weight" \
  --limit 300
```

**参数说明**：
- `indexCode`: 指数代码（注意：这里是 `indexCode` 不是 `stockCodes`）
- `date`: 查询日期

**推荐字段**：
- `stockCode`: 股票代码
- `stockName`: 股票名称
- `weight`: 权重

### 5. 指数K线数据（收益分析）

获取指数的历史价格数据，用于计算收益率和波动率。

```bash
# 查询沪深300近1年K线数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode": "000300", "type": "normal", "startDate": "2024-01-01", "endDate": "2024-12-31"}' \
  --columns "date,open,high,low,close,volume,amount" \
  --limit 365
```

**参数说明**：
- `indexCode`: 指数代码
- `startDate`: 开始日期
- `endDate`: 结束日期

**推荐字段**：
- `date`: 日期
- `open`: 开盘价
- `high`: 最高价
- `low`: 最低价
- `close`: 收盘价
- `volume`: 成交量
- `amount`: 成交额

## 数据获取流程

1. **确定查询参数**：根据分析需求确定指数代码、日期范围等参数
2. **选择合适的 API**：
   - 估值数据：使用 `cn/index/fundamental`（必须包含 `metricsList` 参数）
   - 成分股数据：使用 `cn/index/constituents`
   - K线数据：使用 `cn/index/candlestick`
3. **指定返回字段**：使用 `--columns` 参数指定需要的字段（可选，但推荐使用）
4. **执行查询**：运行 `query_tool.py` 获取数据
5. **数据分析**：对返回的 CSV 数据进行分析

## ETF配置分析方法

### 估值分位数分析
1. 获取指数的PE/PB历史分位数
2. 分位数 < 30%：低估，增加配置
3. 分位数 30-70%：合理，标准配置
4. 分位数 > 70%：高估，减少配置

### 风险收益分析
1. 获取指数历史K线数据
2. 计算年化收益率：`(期末价格/期初价格)^(252/天数) - 1`
3. 计算年化波动率：`std(日收益率) × √252`
4. 计算夏普比率：`(年化收益率 - 无风险利率) / 年化波动率`

### 相关性分析
1. 获取多个指数的历史收益率
2. 计算相关性矩阵
3. 选择相关性低的指数构建分散化组合

## 注意事项

1. **日期格式**：所有日期参数使用 YYYY-MM-DD 格式
2. **metricsList 必须参数**：使用 `cn/index/fundamental` API 时，`metricsList` 是必须参数
3. **stockCodes 限制**：使用 `startDate` 时，`stockCodes` 只能包含一个指数代码
4. **时间间隔**：startDate 和 endDate 的时间间隔不超过10年
5. **指数代码格式**：A股指数代码为6位数字，如 "000300"
6. **字段过滤**：建议使用 `--columns` 参数只返回需要的字段
7. **数据限制**：使用 `--limit` 参数限制返回行数
8. **API 文档**：详细的 API 文档位于 `skills/lixinger-data-query/api_new/api-docs/cn_index_fundamental.md`

## 常用指数代码速查

### 宽基指数
- `000001`: 上证指数
- `000016`: 上证50
- `000300`: 沪深300
- `000905`: 中证500
- `000852`: 中证1000
- `399001`: 深证成指
- `399005`: 中小板指
- `399006`: 创业板指
- `399303`: 国证2000

### 风格指数
- `000919`: 300价值
- `000920`: 300成长
- `000922`: 中证红利
- `000991`: 全指医药
- `000993`: 全指信息

## 相关文档

- **API 列表**：`skills/lixinger-data-query/SKILL.md`
- **使用指南**：`skills/lixinger-data-query/LLM_USAGE_GUIDE.md`
- **查询示例**：`skills/lixinger-data-query/EXAMPLES.md`
- **指数基本面 API 文档**：`skills/lixinger-data-query/api_new/api-docs/cn_index_fundamental.md`
- **指数成分股 API 文档**：`skills/lixinger-data-query/api_new/api-docs/cn_index_constituent.md`
- **指数K线 API 文档**：`skills/lixinger-data-query/api_new/api-docs/cn_index_k-line.md`
