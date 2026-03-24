# 数据获取指南

使用 `query_tool.py` 获取 concept-board-analyzer 所需的数据。

---

## 概念板块分析所需数据

### 1. 概念板块列表
**数据源**: AKShare `stock_board_concept_name_em`
**用途**: 获取所有概念板块代码和名称
**查询方式**: Python直接调用

```python
import akshare as ak
df = ak.stock_board_concept_name_em()
print(df)
```

### 2. 板块行情数据
**数据源**: AKShare `stock_board_concept_hist_em`
**用途**: 获取板块历史行情（涨跌幅、成交额、换手率等）
**查询方式**: Python直接调用

```python
import akshare as ak
df = ak.stock_board_concept_hist_em(
    symbol="半导体",  # 板块名称
    period="daily",
    start_date="20260101",
    end_date="20260324",
    adjust=""
)
print(df)
```

### 3. 板块实时行情
**数据源**: AKShare `stock_board_concept_spot_em`
**用途**: 获取板块实时数据（最新价、涨跌幅、成交额等）
**查询方式**: Python直接调用

```python
import akshare as ak
df = ak.stock_board_concept_spot_em(symbol="半导体")
print(df)
```

### 4. 板块成分股
**数据源**: AKShare `stock_board_concept_cons_em`
**用途**: 获取板块成分股列表
**查询方式**: Python直接调用

```python
import akshare as ak
df = ak.stock_board_concept_cons_em(symbol="半导体")
print(df)
```

### 5. 板块资金流数据
**数据源**: AKShare `stock_concept_fund_flow_hist`
**用途**: 获取板块历史资金流向（主力净流入、超大单净流入等）
**查询方式**: Python直接调用

```python
import akshare as ak
df = ak.stock_concept_fund_flow_hist(symbol="半导体")
print(df)
```

### 6. 概念板块资金流排名
**数据源**: AKShare `stock_fund_flow_concept`
**用途**: 获取概念板块资金流排名（即时/3日/5日/10日）
**查询方式**: Python直接调用

```python
import akshare as ak
df = ak.stock_fund_flow_concept(symbol="即时")  # 可选: "即时", "3日排行", "5日排行", "10日排行"
print(df)
```

### 7. 板块热度数据
**数据源**: 东方财富、同花顺
**用途**: 获取板块搜索指数、关注度、新闻数量等
**查询方式**: 需要爬取或使用第三方API

---

## 理杏仁 API 查询（辅助数据）

### 查询板块内个股基本面数据

```bash
# 查询半导体板块成分股的PE、PB等基本面数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company" \
  --params '{"stockCodes": ["002049", "603986", "600584"]}' \
  --columns "stockCode,name,pe_ttm,pb,marketCap"
```

### 查询板块内个股财务数据

```bash
# 查询个股财务数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCode": "002049", "startDate": "2025-01-01", "endDate": "2026-03-24"}' \
  --columns "date,revenue,netProfit,roe"
```

---

## 参数说明

- `--suffix`: API 路径
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 数据获取顺序

1. **获取板块列表**: 确认板块名称和代码
2. **获取板块行情**: 分析板块涨跌幅、成交额、换手率
3. **获取板块成分股**: 了解板块构成
4. **获取资金流向**: 分析主力资金动向
5. **获取板块热度**: 评估市场关注度
6. **获取个股数据**: 分析龙头股和成分股表现

---

## 注意事项

1. **AKShare接口需要网络访问**: 部分接口可能因网络问题无法访问
2. **数据更新频率**: 
   - 实时数据：盘中实时更新
   - 资金流数据：T日晚间更新
   - 热度数据：可能延迟1天
3. **板块名称**: 使用中文名称，如"半导体"、"人工智能"、"新能源"等
4. **数据格式**: AKShare返回pandas DataFrame格式

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：
- AKShare接口: `../../lixinger-data-query/api_new/akshare_data/`
- 理杏仁API: `../../lixinger-data-query/api_new/api-docs/`
