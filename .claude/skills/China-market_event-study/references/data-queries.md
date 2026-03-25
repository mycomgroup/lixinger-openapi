# 数据获取指南

使用 `query_tool.py` 获取 event-study 所需的数据。

---

## 事件研究数据需求

事件研究分析需要以下数据：

1. **事件日期数据**：确定事件发生的具体日期（如公告日期、业绩发布日期等）
2. **标的K线数据**：计算事件窗内的收益率和波动
3. **基准指数数据**：计算超额收益（标的收益率 - 基准收益率）
4. **基本面数据**：分析事件前后的估值变化

---

## 查询示例

### 1. 查询公司公告（确定事件日期）

```bash
# 查询宁德时代2024-2025年的公告，筛选包含"报告"的公告
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/announcement" \
  --params '{"stockCode": "300750", "startDate": "2024-01-01", "endDate": "2025-03-24", "limit": 200}' \
  --columns "date,linkText,types" \
  --row-filter '{"linkText": {"contains": "报告"}}'
```

**返回字段说明**：
- `date`: 公告日期
- `linkText`: 公告标题
- `types`: 公告类型（`fs_full` 表示完整财务报告）

---

### 2. 查询标的K线数据（计算事件窗收益率）

```bash
# 查询宁德时代K线数据（前复权），用于计算事件窗[-20, +20]的收益率
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/candlestick" \
  --params '{"stockCode": "300750", "startDate": "2025-02-01", "endDate": "2025-04-30", "type": "lxr_fc_rights"}' \
  --columns "date,stockCode,close,change,volume,amount,to_r" \
  --limit 50
```

**返回字段说明**：
- `date`: 交易日期
- `close`: 收盘价
- `change`: 涨跌幅
- `volume`: 成交量
- `amount`: 成交金额
- `to_r`: 换手率

**复权类型选项**：
- `lxr_fc_rights`: 理杏仁前复权（推荐）
- `fc_rights`: 前复权
- `bc_rights`: 后复权
- `ex_rights`: 不复权

---

### 3. 查询基准指数K线数据（计算超额收益）

```bash
# 查询沪深300指数K线数据
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/index/candlestick" \
  --params '{"stockCode": "000300", "startDate": "2025-02-01", "endDate": "2025-04-30", "type": "normal"}' \
  --columns "date,close,change" \
  --limit 50
```

**常用基准指数代码**：
- `000300`: 沪深300指数
- `000905`: 中证500指数
- `000016`: 上证50指数
- `399006`: 创业板指

---

### 4. 查询基本面数据（分析估值变化）

```bash
# 查询宁德时代基本面数据
python3 plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes": ["300750"], "date": "2025-03-15", "metricsList": ["pe_ttm", "pb", "dyr", "mc", "to_r"]}' \
  --columns "date,stockCode,pe_ttm,pb,dyr,mc,to_r"
```

**常用估值指标**：
- `pe_ttm`: PE-TTM（市盈率）
- `pb`: PB（市净率）
- `dyr`: 股息率
- `mc`: 总市值
- `to_r`: 换手率

**估值分位数指标**（用于判断估值历史位置）：
- `pe_ttm.y5.cvpos`: PE-TTM 5年分位点
- `pb.y5.cvpos`: PB 5年分位点

---

## 参数说明

- `--suffix`: API 路径（参考下方可用 API 列表）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

| API 后缀 | 说明 | 使用场景 |
|---------|------|----------|
| `cn/company/announcement` | 公告信息 | 确定事件日期 |
| `cn/company/candlestick` | K线数据 | 计算事件窗收益率 |
| `cn/index/candlestick` | 指数K线数据 | 计算超额收益 |
| `cn/company/fundamental/non_financial` | 基本面数据 | 分析估值变化 |
| `cn/company/fs/non_financial` | 财务数据 | 分析财务指标变化 |

---

## 事件研究分析流程

1. **确定事件日期**
   - 查询公告数据，找到目标事件（如业绩报告、并购公告等）
   - 记录事件日期 `event_date`

2. **计算事件窗时间范围**
   - 事件窗：`[event_date - N, event_date + M]`（如 [-20, +20] 交易日）
   - 查询标的和基准的K线数据

3. **计算收益率指标**
   - 标的日收益率：`r_stock = change`
   - 基准日收益率：`r_benchmark = change`
   - 超额收益率：`AR = r_stock - r_benchmark`
   - 累计超额收益率：`CAR = Σ AR`

4. **分析估值变化**
   - 查询事件前后的基本面数据
   - 对比PE、PB等估值指标的变化

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`../../lixinger-data-query/SKILL.md`
