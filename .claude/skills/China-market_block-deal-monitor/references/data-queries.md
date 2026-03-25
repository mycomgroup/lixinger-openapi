# 大宗交易监控数据查询

### 概述

本节记录了使用理杏仁开放平台进行 A 股大宗交易监控的数据查询方法。大宗交易监控用于识别潜在建仓/派发信号、评估流动性风险和冲击成本。

### 数据来源

- **平台**: 理杏仁开放平台 (https://www.lixinger.com/open/api)
- **数据范围**: A 股上市公司大宗交易数据
- **数据时间**: 每日更新，T 日晚间可获取 T 日大宗交易数据

### API 接口

#### 1. 获取大宗交易数据（核心）

**API**: `cn/company/block-deal`

**用途**: 获取上市公司大宗交易信息，包括成交价、成交量、成交金额、折溢价率、买卖营业部等

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/block-deal" \
  --params '{"stockCode": "600196", "startDate": "2026-03-19"}' \
  --columns "date,stockCode,tradingPrice,tradingVolume,tradingAmount,discountRate,buyBranch,sellBranch" \
  --limit 20
```

**参数说明**:
- `stockCode`: 股票代码（选填，仅在请求 date range 数据时生效）
- `date`: 指定日期，格式 YYYY-MM-DD（选填）
- `startDate`: 起始日期，格式 YYYY-MM-DD（选填）
- `endDate`: 结束日期，格式 YYYY-MM-DD（选填，默认上周一）
- `limit`: 返回最近数据的数量（选填）

**返回字段说明**:
- `date`: 交易日期
- `stockCode`: 股票代码
- `tradingPrice`: 成交价（元）
- `tradingVolume`: 成交量（股）
- `tradingAmount`: 成交金额（元）
- `discountRate`: 折价率（负数为折价，正数为溢价）
- `buyBranch`: 买入营业部
- `sellBranch`: 卖出营业部

**注意事项**:
- ⚠️ 此 API 只接受单个 `stockCode`，不是数组
- 批量查询需要循环调用
- 建议使用 `startDate` 查询历史大宗交易记录

#### 2. 获取行业成分股

**API**: `cn/industry/constituents/sw_2021`

**用途**: 获取申万行业成分股列表，用于按行业筛选大宗交易

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/constituents/sw_2021" \
  --params '{"stockCodes":["370000"],"date":"2026-03-24"}' \
  --columns "stockCode,constituents" \
  --limit 1
```

**常用医药行业代码**:
- `370000`: 医药生物（申万一级）

**常用行业代码**:
- `110000`: 农林牧渔
- `210000`: 采掘
- `220000`: 化工
- `270000`: 电子
- `280000`: 汽车
- `330000`: 家用电器
- `340000`: 食品饮料
- `480000`: 银行
- `490000`: 非银金融
- `630000`: 电气设备
- `710000`: 计算机

#### 3. 获取 K 线数据（用于验证承接）

**API**: `cn/company/candlestick`

**用途**: 获取 K 线数据，用于分析大宗交易前后股价表现和承接情况

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode":"600196","type":"normal","startDate":"2026-03-17","endDate":"2026-03-24"}' \
  --columns "date,close,pctChg,volume,amount" \
  --limit 10
```

**返回字段说明**:
- `date`: 交易日期
- `open`: 开盘价
- `high`: 最高价
- `low`: 最低价
- `close`: 收盘价
- `volume`: 成交量（股）
- `amount`: 成交金额（元）
- `pctChg`: 涨跌幅（%）
- `turnover`: 换手率（%）
- `turnoverFree`: 自由流通股换手率（%）

#### 4. 获取股东增减持数据（用于交叉验证）

**API**: `cn/company/major-shareholders-shares-change`

**用途**: 获取股东增减持数据，用于验证大宗交易是否与减持窗口重合

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/major-shareholders-shares-change" \
  --params '{"stockCode": "600196", "startDate": "2025-01-01"}' \
  --columns "date,shareholderName,changeReason,changeAmount" \
  --limit 20
```

**返回字段说明**:
- `date`: 变动日期
- `shareholderName`: 股东名称
- `changeReason`: 变动原因（如：大宗交易、二级市场买卖、股权质押等）
- `changeAmount`: 变动数量（股），正值为增持，负值为减持

#### 5. 获取股东人数数据

**API**: `cn/company/shareholders-num`

**用途**: 获取股东人数变化，用于分析筹码集中度

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/shareholders-num" \
  --params '{"stockCode": "600196", "startDate": "2025-01-01"}' \
  --columns "date,stockCode,shareholdersNum" \
  --limit 20
```

**返回字段说明**:
- `date`: 报告期
- `stockCode`: 股票代码
- `shareholdersNum`: 股东人数

#### 6. 获取个股基本信息

**API**: `cn/company/base-info`

**用途**: 获取股票基本信息，用于了解公司基本情况

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/base-info" \
  --params '{"stockCodes":["600196"]}' \
  --columns "stockCode,stockName,industry" \
  --limit 1
```

**返回字段说明**:
- `stockCode`: 股票代码
- `stockName`: 股票名称
- `industry`: 所属行业
- `totalShares`: 总股本
- `floatShares`: 流通股本

#### 7. 获取限售解禁数据

**API**: `cn/company/share-lockup`

**用途**: 获取限售股解禁数据，用于判断大宗交易是否临近解禁窗口

**查询示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/share-lockup" \
  --params '{"stockCode": "600196", "startDate": "2026-01-01"}' \
  --columns "date,lockupType,lockupShares" \
  --limit 20
```

### 分析框架

#### 折溢价解读

| 折价率范围 | 解读 | 风险等级 |
|-----------|------|---------|
| 0% ~ -2% | 平价或微幅折价 | 低 |
| -2% ~ -5% | 常态折价 | 低 |
| -5% ~ -7% | 中度折价 | 中 |
| < -7% | 显著折价，可能存在抛压 | 高 |
| > 0% | 溢价成交，买方积极 | 需验证 |

#### 信号类型

1. **建仓型特征**（需要验证）
   - 折价温和（2-5%）+ 连续多日 + 成交均价稳定
   - 二级市场回撤浅、换手温和上升

2. **派发/抛压型特征**（风险更大）
   - 折价显著（>7%）+ 成交金额占比高 + 二级市场承接弱
   - 与解禁/减持窗口重合

3. **事件/结构型**（不直接解读为多空）
   - 股权激励/员工持股、协议转让、基金产品调仓等

#### 风险标签

- **流动性风险**: 日均成交偏低、冲击成本高
- **二次供给**: 后续仍可能继续折价成交
- **利好出尽**: 溢价成交但股价不跟随

### 批量查询示例

**示例: 查询医药行业多只股票的大宗交易**

```bash
# 查询医药行业成分股
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/constituents/sw_2021" \
  --params '{"stockCodes":["370000"],"date":"2026-03-24"}' \
  --columns "stockCode,constituents" \
  --limit 1

# 批量查询医药龙头股大宗交易
for code in 600276 000538 600196 300122 300142 603259 000661 300347 300759 002007; do
  echo "=== 查询 ${code} ==="
  python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
    --suffix "cn/company/block-deal" \
    --params '{"stockCode": "'"${code}"'", "startDate": "2026-03-19"}' \
    --columns "date,stockCode,tradingPrice,tradingVolume,tradingAmount,discountRate,buyBranch,sellBranch" \
    --limit 10
done
```

**示例: 查询后验证股价承接情况**

```bash
# 查询大宗交易数据
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/block-deal" \
  --params '{"stockCode": "002594", "startDate": "2026-03-20"}' \
  --columns "date,stockCode,tradingPrice,tradingVolume,tradingAmount,discountRate,buyBranch,sellBranch" \
  --limit 10

# 查询同期K线数据验证承接
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode":"002594","type":"normal","startDate":"2026-03-18","endDate":"2026-03-24"}' \
  --columns "date,close,pctChg,volume,amount" \
  --limit 10
```

### 注意事项

1. **API 限制**: 大宗交易 API 只接受单个 stockCode，批量查询需要循环调用
2. **数据时效性**: 大宗交易数据 T 日晚间可获取
3. **解读谨慎**: 大宗交易可能因协议转让、产品调仓、合规需求等原因发生，并非必然对应“建仓/派发”
4. **交叉验证**: 建议结合股东增减持、解禁数据、资金流向等进行综合判断
5. **连续性关注**: 连续多日同标的/同方向的大宗交易更有分析价值

### 相关文件

- 技能文档: `.claude/skills/China-market_block-deal-monitor/`
- 查询工具: `.claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py`
- API 文档: `.claude/skills/lixinger-data-query/api_new/api-docs/cn_company_block-deal.md`
