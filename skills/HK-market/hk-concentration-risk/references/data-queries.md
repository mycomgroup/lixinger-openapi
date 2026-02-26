# 港股集中度风险监控 - 数据获取指南

本文档说明如何使用 `query_tool.py` 获取港股集中度风险监控所需的数据。

---

## 核心数据需求

### 1. 持仓组合数据
- 个股持仓信息
- 行业分布
- 地域分布
- 权重配置

### 2. 市场数据
- 股票价格
- 市值数据
- 行业分类
- 指数成分

### 3. 风险数据
- 相关性矩阵
- 波动率数据
- 风险因子暴露

---

## 数据查询示例

### 1. 获取港股公司基本信息

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company" \
  --params '{"stockCodes": ["00700", "09988", "00005", "00011"]}' \
  --columns "stockCode,name,market,areaCode,fsTableType,ipoDate" \
  --limit 100
```

**用途**: 获取持仓股票的基本信息，用于分类和分组

### 2. 获取港股指数成分股

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/constituents" \
  --params '{"indexCode": "HSI"}' \
  --columns "stockCode,name,weight" \
  --limit 100
```

**用途**: 获取指数成分股权重，用于基准对比

### 3. 获取港股行业分类

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/industries" \
  --params '{"stockCode": "00700"}' \
  --columns "industryCode,industryName,industryLevel"
```

**用途**: 获取股票行业分类，用于行业集中度分析

### 4. 获取港股基本面数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/fundamental/non_financial" \
  --params '{"stockCodes": ["00700"], "date": "2026-02-24", "metricsList": ["mc", "pe_ttm", "pb", "dyr"]}' \
  --columns "date,stockCode,mc,pe_ttm,pb,dyr" \
  --limit 20
```

**注意**: `roe` 不在 `hk/company/fundamental/non_financial` API 支持的指标中，已替换为 `dyr`（股息率）

**用途**: 获取市值等基本面数据，用于权重计算

### 5. 获取港股通持仓数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/mutual-market" \
  --params '{"stockCode": "00700", "startDate": "2026-01-01", "endDate": "2026-02-24"}' \
  --columns "date,shareholdings,shareholdingsRatio" \
  --limit 100
```

**用途**: 获取港股通持仓，用于资金流向分析

### 6. 获取港股指数基本面

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/index/fundamental" \
  --params '{"stockCodes": ["HSI"], "date": "2026-02-24", "metricsList": ["mc", "pe_ttm.mcw", "pb.mcw"]}' \
  --columns "date,mc,pe_ttm.mcw,pb.mcw"
```

**用途**: 获取市场整体估值，用于基准对比

### 7. 获取港股行业基本面

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/industry/fundamental/hsi" \
  --params '{"stockCodes": ["H50"], "date": "2026-02-24", "metricsList": ["mc", "pe_ttm.mcw"]}' \
  --columns "date,mc,pe_ttm.mcw"
```

**注意**: 参数名为 `stockCodes`（复数），值为行业代码如 "H50"

**用途**: 获取行业估值数据，用于行业集中度分析

---

## 集中度计算所需数据

### 个股集中度指标
```bash
# 获取持仓股票列表和权重（需要从组合管理系统获取）
# 计算：
# - 最大持仓权重
# - 前十大持仓权重
# - HHI指数 = Σ(权重²)
# - 有效持仓数 = 1 / HHI
```

### 行业集中度指标
```bash
# 1. 获取每只股票的行业分类
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk/company/industries" \
  --params '{"stockCode": "00700"}' \
  --columns "industryCode,industryName,industryLevel"

# 2. 按行业汇总权重
# 3. 计算行业HHI和有效行业数
```

### 风险因子集中度
```bash
# 需要额外的风险模型数据（见增强数据文件）
# - 市场风险因子
# - 风格风险因子
# - 行业风险因子
```

---

## 参数说明

- `--suffix`: API 路径（参考下方可用 API 列表）
- `--params`: JSON 格式参数
- `--columns`: 指定返回字段（推荐使用，节省 30-40% token）
- `--row-filter`: 过滤条件
- `--limit`: 限制返回行数

---

## 本 Skill 常用 API

### 核心 API
- `hk/company` - 港股公司基本信息
- `hk/company/fundamental/non_financial` - 港股基本面数据
- `hk/company.industries` - 港股行业分类
- `hk/index/constituents` - 港股指数成分股
- `hk/index/fundamental` - 港股指数基本面
- `hk.industry.fundamental.hsi` - 港股行业基本面

### 辅助 API
- `hk/company.mutual-market` - 港股通持仓
- `hk/company/candlestick` - 港股K线数据
- `hk/index.candlestick` - 港股指数K线

---

## 数据更新频率

- **实时数据**: 持仓和价格（需要实时系统）
- **日度数据**: 基本面、市值、行业分类
- **周度数据**: 集中度指标计算
- **月度数据**: 风险报告生成

---

## 缺失数据说明

以下数据需要从其他数据源补充（见 `additional-data-sources.md`）：

1. **组合持仓数据**: 需要从组合管理系统获取
2. **风险因子数据**: 需要风险模型提供
3. **相关性矩阵**: 需要历史价格计算
4. **波动率数据**: 需要历史价格计算
5. **VaR计算**: 需要历史收益率数据

---

## 查找更多 API

```bash
# 查看完整 API 列表
cat skills/lixinger-data-query/SKILL.md

# 搜索港股相关 API
grep -r "hk\." skills/lixinger-data-query/api_new/api-docs/

# 查看具体 API 文档
cat skills/lixinger-data-query/api_new/api-docs/hk_company.md
```

---

## 相关文档

- **API 文档**: `skills/lixinger-data-query/SKILL.md`
- **增强数据**: `additional-data-sources.md`
- **使用指南**: `skills/lixinger-data-query/LLM_USAGE_GUIDE.md`
