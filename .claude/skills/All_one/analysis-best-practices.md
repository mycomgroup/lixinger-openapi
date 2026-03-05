# API 调用快速指南

帮助 AI 一次性正确调用理杏仁 API，避免常见错误。

---

## ⚡ 调用前必查清单

### 1. 查找合适的 API（必须！）
```bash
# 方法 1：使用中文关键词索引（推荐）
grep -i "分红" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "市盈率\|PE" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "ROE\|净资产收益率" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md

# 方法 2：直接搜索 API 文档
grep -r "分红" .claude/skills/lixinger-data-query/api_new/api-docs/
```

### 2. 查看 API 文档（必须！）
```bash
# 找到 API 后，查看详细文档
cat .claude/skills/lixinger-data-query/api_new/api-docs/{api_name}.md
```

### 2. 检查关键格式
- ✅ API 路径使用斜杠：`cn/company/dividend`
- ❌ 不要用点号：`cn.company.dividend`
- ✅ 使用最近日期：`2026-02-25`
- ❌ 不要用过时日期：`2024-12-31`
- ✅ 参数用单引号：`--params '{"key": "value"}'`
- ❌ 不要转义引号：`--params \'{"key": "value"}\'`

### 3. 使用 --columns 过滤字段
```bash
# 节省 30-40% token
--columns "date,stockCode,pe_ttm,pb,dyr"
```

---

## 🔍 如何快速找到需要的 API

### 常用中文关键词搜索

```bash
# 财务指标
grep -i "分红\|股息" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "市盈率\|PE" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "市净率\|PB" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "ROE\|净资产收益率" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "营业收入\|营收" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "净利润" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md

# 交易数据
grep -i "K线\|行情\|股价" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "成交量\|成交额" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md

# 资金流向
grep -i "融资融券\|两融" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "大宗交易" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "龙虎榜" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "陆股通\|港股通\|北向资金\|南向资金" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md

# 公司事件
grep -i "公告\|披露" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "配股" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "增减持" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "股权质押" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md

# 持股数据
grep -i "股东" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "基金持股\|机构持仓" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md

# 指数和行业
grep -i "指数\|成分股" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "行业\|板块" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md

# 宏观数据
grep -i "GDP\|CPI\|PPI" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "货币供应\|M0\|M1\|M2" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
grep -i "汇率\|外汇" .claude/skills/lixinger-data-query/api_new/API_KEYWORD_INDEX.md
```

### 查找流程

1. **使用中文关键词搜索索引**（找到 API 路径）
2. **查看 API 文档**（确认参数和字段）
3. **构造查询命令**（使用正确的参数）

---

## 🚨 最常见的 10 个错误

### 错误 1：API 路径格式错误
```bash
❌ --suffix "cn.company.dividend"
✅ --suffix "cn/company/dividend"
```

### 错误 2：缺少必需参数 metricsList
```bash
❌ --params '{"stockCodes": ["600519"], "date": "2026-02-24"}'
✅ --params '{"stockCodes": ["600519"], "date": "2026-02-24", "metricsList": ["pe_ttm", "pb"]}'
```
**适用 API**：`fundamental/non_financial`, `fs/non_financial`, `index/fundamental`

### 错误 3：指标缺少 .mcw 后缀
```bash
❌ --params '{"metricsList": ["pe_ttm", "pb", "dyr"]}'  # 指数 API
✅ --params '{"metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw"]}'
```
**适用 API**：`cn/index/fundamental`, `hk/index/fundamental`, `us/index/fundamental`

### 错误 4：参数名称单复数错误
```bash
❌ --params '{"stockCodes": ["00700"]}'  # hk/company/dividend
✅ --params '{"stockCode": "00700"}'     # 单数

❌ --params '{"stockCode": "000001"}'    # cn/index/candlestick
✅ --params '{"stockCodes": ["000001"]}' # 复数
```
**规则**：查看 API 文档确认参数名

### 错误 5：使用不支持的指标
```bash
# 港股 fundamental API
❌ "metricsList": ["pe", "ps", "roe", "roa"]
✅ "metricsList": ["pe_ttm", "ps_ttm", "pb", "dyr"]

# A股 fs API（仅支持利润表和部分资产负债表）
❌ "metricsList": ["q.cf.cfo.t", "q.bs.te.t"]
✅ "metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.bs.ta.t"]
```

### 错误 6：缺少 source 参数
```bash
❌ --params '{"level": "one"}'
✅ --params '{"source": "sw", "level": "one"}'  # cn/industry
✅ --params '{"source": "hsi"}'                  # hk/industry
```

### 错误 7：缺少 type 参数
```bash
❌ --params '{"stockCode": "00700", "startDate": "2026-01-01"}'
✅ --params '{"stockCode": "00700", "type": "normal", "startDate": "2026-01-01"}'
```
**适用 API**：`candlestick` (K线数据)

### 错误 8：批量查询限制
```bash
# 某些 API 使用 startDate 时只能查询一个代码
❌ --params '{"stockCodes": ["000300", "000905"], "startDate": "2026-01-01"}'

✅ 使用循环：
for code in 000300 000905; do
  python3 query_tool.py --params "{\"stockCodes\": [\"${code}\"], \"startDate\": \"2026-01-01\"}" ...
done
```
**适用 API**：`cn/index/fundamental`, `hk/industry/fundamental/hsi`

### 错误 9：日期过时
```bash
❌ "date": "2024-12-31"  # 现在是 2026 年
✅ "date": "2026-02-25"
✅ "startDate": "2026-02-01"
```

### 错误 10：命令格式错误
```bash
❌ --params \'{"source": "sw"}\'  # 转义单引号
✅ --params '{"source": "sw"}'

❌ for code in ["600519", "601318"]; do  # Python 语法
✅ for code in 600519 601318; do         # bash 语法
```

---

## 📋 API 特殊规则速查

### A股 API
- `cn/company/fs/non_financial`：仅支持 `q.ps.*` (利润表) 和 `q.bs.ta.t` (总资产)
- `cn/index/fundamental`：指标需要 `.mcw` 后缀
- `cn/index/candlestick`：需要 `type` 参数（`normal` 或 `forward`）
- `cn/industry`：需要 `source` 参数（`sw` 申万行业）

### 港股 API
- `hk/company/dividend`：参数名为 `stockCode`（单数）
- `hk/company/fs/non_financial`：仅支持 `q.ps.*` (利润表)
- `hk/company/fundamental/non_financial`：不支持 `roe`, `roa`，使用 `pe_ttm`, `ps_ttm`
- `hk/index/fundamental`：指标需要 `.mcw` 后缀，不支持 `dyr`（需要 `dyr.mcw`）
- `hk/industry/fundamental/hsi`：参数名为 `stockCodes`（复数），不支持 `cp`, `cpc`

### 美股 API
- `us/index/fundamental`：指标需要 `.mcw` 后缀

### 宏观数据 API
- 所有宏观 API 需要 `areaCode` 和 `metricsList` 参数
- 示例：`{"areaCode": "cn", "metricsList": ["m.m0.t", "m.m1.t"]}`

---

## 🎯 标准调用模板

### 基本查询
```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/dividend" \
  --params '{"stockCode": "600519", "startDate": "2026-01-01"}' \
  --columns "date,dividendPerShare,dividendYield" \
  --limit 20
```

### 批量查询（循环）
```bash
for code in 600519 601318 600036; do
  python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
    --suffix "cn/company/dividend" \
    --params "{\"stockCode\": \"${code}\", \"startDate\": \"2026-01-01\"}" \
    --columns "date,dividendPerShare" \
    --limit 10
done
```

### 指数基本面查询
```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/index/fundamental" \
  --params '{"stockCodes": ["000300"], "date": "2026-02-25", "metricsList": ["pe_ttm.mcw", "pb.mcw", "dyr.mcw"]}' \
  --columns "date,stockCode,pe_ttm.mcw,pb.mcw,dyr.mcw"
```

### 财务数据查询
```bash
python3 .claude/skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["600519"], "date": "2025-09-30", "metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.ps.gp_m.t"]}' \
  --columns "date,stockCode,q.ps.toi.t,q.ps.np.t,q.ps.gp_m.t"
```

---

## 🔍 遇到错误时的诊断流程

1. **ValidationError: "xxx" is required**
   → 检查是否缺少必需参数（metricsList, source, type, stockCodes, areaCode）

2. **ValidationError: (xxx) are invalid metrics**
   → 检查指标是否支持，是否需要 .mcw 后缀

3. **Api was not found**
   → 检查 API 路径格式（使用斜杠而非点号）

4. **"stockCodes" must contain 1 items**
   → 使用循环分别查询每个代码

5. **数据为空**
   → 检查日期是否过时，使用 startDate 而非 date

---

## 💡 效率提升技巧

1. **使用 --columns 过滤字段**（节省 30-40% token）
2. **使用 --limit 限制行数**（避免返回过多数据）
3. **使用 --row-filter 过滤数据**（在查询时直接过滤）
4. **批量操作使用循环**（避免手动执行多次）

---

**最后更新**：2026-02-26  
**测试覆盖**：381 个命令，100% 通过率
