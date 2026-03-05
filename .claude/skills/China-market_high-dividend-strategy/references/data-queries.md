# 数据获取指南

使用 `query_tool.py` 获取 high-dividend-strategy 所需的数据。

---

## 设计说明：补齐“可执行上下文”（关键）

### 背景 / 痛点

- 业务 `SKILL.md` 主要描述**分析逻辑**（该算什么），但缺少**可直接复制执行的取数命令**（去哪查、怎么查）。
- 结果是：一旦触发高股息分析模式，模型容易在“找接口 / 猜参数 / 二次查文档”上浪费回合与 token，影响稳定性与可复现性。

### 目标（本 Skill 的最小闭环）

在本 `references/data-queries.md` 内，提供至少两类“复制即用”的命令片段：

1. **入口数据（范围）**：获取中证红利指数（`000922`）成分股列表 → 得到 `stockCode` 列表  
2. **核心数据（分红）**：对 `stockCode` 拉取近 5 年现金分红明细 → 支撑股息率 / 分红持续性等分析

### 非目标

- 不在此文档中实现完整的打分、回测、组合构建流水线（属于分析层）。
- 不改动 `query_tool.py` 的能力边界（这里只给“可执行上下文”与最小可跑示例）。

### 验收标准

- 只阅读本文件，不依赖其他文档，也能在 1 分钟内跑通：
  - 查询 `000922` 成分股 `stockCode` 列表
  - 对任意一个 `stockCode` 查询近 5 年分红明细

## 查询示例

### 查询 Cn.Index.Constituents（中证红利 000922 成分股）

**API 路径**: `cn/index/constituents`

**必需参数**:
- `date`: 信息日期（可用 `"latest"`）
- `stockCodes`: 指数代码数组（如 `["000922"]`）

**注意**:
- 返回数据包含嵌套数组 `constituents`，建议使用 `--flatten "constituents"` 直接展开成“成分股行”。

**查询示例**（输出成分股代码到 CSV 文件，供后续批量查询使用）:

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/constituents" \
  --params '{"date": "latest", "stockCodes": ["000922"]}' \
  --flatten "constituents" \
  --columns "stockCode,market,areaCode" \
  --limit 500 \
  --format csv > csi_dividend_000922_constituents.csv
```

### 查询 Cn.Company.Dividend

**API 路径**: `cn/company/dividend`

**必需参数**: 
- `stockCode`: 股票代码（单个）
- `startDate`: 起始日期（YYYY-MM-DD）
- `endDate`: 结束日期（YYYY-MM-DD，可选；默认上周一）

**参数限制**:
- ⚠️ 此 API 只接受单个 `stockCode`（不是数组）
- 建议使用 `startDate` 查询历史分红记录

**查询示例**:

```bash
# 示例 1: 查询单个股票近 5 年历史分红（推荐）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "600519", "startDate": "2021-01-01", "endDate": "2026-02-24"}' \
  --columns "date,dividend,dividendAmount,annualNetProfitDividendRatio,exDate" \
  --limit 20

# 示例 2: 批量查询中证红利(000922)成分股的分红数据（需要循环）
# 依赖上一步生成的 csi_dividend_000922_constituents.csv；先用 head 控制请求量，确认没问题后再去掉。
tail -n +2 csi_dividend_000922_constituents.csv | cut -d, -f1 | head -n 10 | while read -r code; do
  python3 skills/lixinger-data-query/scripts/query_tool.py \
    --suffix "cn/company/dividend" \
    --params "{\"stockCode\": \"${code}\", \"startDate\": \"2021-01-01\", \"endDate\": \"2026-02-24\"}" \
    --columns "date,dividend,dividendAmount,annualNetProfitDividendRatio,exDate" \
    --limit 200 \
    --format csv > "dividend_${code}.csv"
done
```

**常用字段**:
- `date`: 公告日期
- `dividend`: 每股现金分红（元）
- `dividendAmount`: 分红金额
- `annualNetProfitDividendRatio`: 年度净利润分红比例
- `exDate`: 除权除息日
- `registerDate`: 股权登记日
- `paymentDate`: 分红到账日
- `fsEndDate`: 财报期末

**常见错误**:

❌ **错误**: 使用 stockCodes 数组
```bash
--params '{"stockCodes": ["600519", "000858"], "startDate": "2021-01-01"}'
```
✅ **正确**: 使用单个 stockCode
```bash
--params '{"stockCode": "600519", "startDate": "2021-01-01"}'
```

---

## 参数说明

- `--suffix`: API 路径（使用斜杠格式，如 `cn/company/dividend`）
- `--params`: JSON 格式参数（注意内层使用双引号）
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件（JSON 格式，如 `'{"dividend": {">": 1}}'`）
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

- `cn/index/constituents`: 指数成分股（用于确定分析范围）
- `cn/company/dividend`: 分红数据
- `cn/company/fundamental/non_financial`: 基本面数据（需要 metricsList）

### 查询估值与财务指标（用于筛选高股息股票）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fundamental/non_financial" \
  --params '{"stockCodes":["600519","601398","601857"],"date":"2026-02-24","metricsList":["dyr","pe_ttm","pb"]}' \
  --columns "stockCode,name,dyr,pe_ttm,pb"
```

### 查询财务报表（用于分析分红可持续性）

```bash
# 查询利润表和现金流量表关键指标
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes":["600519"],"startDate":"2021-01-01","endDate":"2026-02-27","metricsList":["q.ps.np.t","q.ps.gp_m.t","q.ps.op_m.t"]}' \
  --columns "date,stockCode,q.ps.np.t,q.ps.gp_m.t,q.ps.op_m.t"
```

### 查询行业分布（用于分散化分析）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/industry" \
  --params '{"source":"sw","level":"one","date":"2026-02-27"}' \
  --columns "industryCode,industryName,pe_ttm,pb,dyr"
```

### 查询宏观利率环境（用于评估高股息吸引力）

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "macro/money-supply" \
  --params '{"areaCode":"cn","startDate":"2023-01-01","endDate":"2026-02-27","metricsList":["m.m0.t","m.m1.t","m.m2.t"]}' \
  --columns "date,m.m0.t,m.m1.t,m.m2.t"
```

---

## 查找更多 API

```bash
# 查看完整 API 列表
cat skills/lixinger-data-query/SKILL.md

# 搜索关键字
grep -r "关键字" skills/lixinger-data-query/api_new/api-docs/

# 查看具体 API 文档
cat skills/lixinger-data-query/api_new/api-docs/{api_name}.md
```

**相关文档**: `skills/lixinger-data-query/SKILL.md`
