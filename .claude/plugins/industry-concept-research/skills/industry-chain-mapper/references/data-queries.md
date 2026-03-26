# 数据获取指南 - industry-chain-mapper

使用理杏仁API获取产业链映射所需的数据。

---

## 核心API

### 1. 行业数据

**API路径**: `cn/industry`

**描述**: 获取A股行业分类数据，用于产业链映射

**参数**:
- `source`: 数据源（如 "sw" 代表申万）
- `level`: 行业层级（"one"/"two"/"three"）

**使用示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry" \
  --params '{"source": "sw", "level": "one"}' \
  --limit 20
```

**分析用途**:
- 产业链位置划分（上游/中游/下游）
- 行业分类与产业链映射
- 产业链关系建立

---

### 2. 公司营收结构

**API路径**: `cn/company/operation-revenue-constitution`

**描述**: 获取公司主营业务收入构成，用于分析产业链位置

**参数**:
- `stockCode`: 股票代码
- `startDate`: 开始日期

**使用示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/operation-revenue-constitution" \
  --params '{"stockCode": "002371", "startDate": "2025-01-01"}' \
  --limit 20
```

**分析用途**:
- 主营业务分析
- 产品结构分析
- 产业链位置判断
- 客户/供应商集中度分析

---

### 3. 公司财务数据

**API路径**: `cn/company/fs/non_financial`

**描述**: 获取公司财务指标，用于产业链业绩传导分析

**参数**:
- `stockCodes`: 股票代码数组（如 ["002371"]）
- `startDate`: 开始日期
- `endDate`: 结束日期
- `metricsList`: 指标列表

**指标格式**:
- 营业收入: `q.ps.toi.t`（季度累计值）
- 净利润: `q.ps.np.t`（季度累计值）
- 毛利率: `q.ps.gp_m.t`（季度累计值）

**使用示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["002371"], "startDate": "2024-01-01", "metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.ps.gp_m.t"]}' \
  --limit 10
```

**分析用途**:
- 毛利率变化分析（价格传导）
- 净利润增速分析（业绩传导）
- 营收增长分析（需求传导）

---

### 4. 行业估值数据

**API路径**: `cn/industry/fundamental/sw_2021`

**描述**: 获取行业估值数据，用于评估产业链估值水平

**参数**:
- `stockCodes`: 行业代码数组（如 ["270100"]）
- `date`: 日期
- `metricsList`: 指标列表

**指标格式**:
- PE-TTM: `pe_ttm.mcw`（市值加权）
- PB: `pb.mcw`（市值加权）
- 市值: `mc`

**使用示例**:
```bash
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"stockCodes": ["270100"], "date": "latest", "metricsList": ["pe_ttm.mcw", "pb.mcw", "mc"]}' \
  --limit 10
```

---

## 半导体产业链示例

### 产业链环节与代表公司

| 环节 | 申万行业代码 | 代表公司 | 股票代码 |
|------|--------------|----------|----------|
| 上游设备 | 270100 | 北方华创 | 002371 |
| 中游制造 | 270100 | 中芯国际 | 688981 |
| 下游设计 | 270100 | 韦尔股份 | 603501 |

### 数据获取命令

```bash
# 1. 获取半导体行业估值
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/industry/fundamental/sw_2021" \
  --params '{"stockCodes": ["270100"], "date": "latest", "metricsList": ["pe_ttm.mcw", "pb.mcw", "mc"]}'

# 2. 获取北方华创财务数据
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["002371"], "startDate": "2024-01-01", "metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.ps.gp_m.t"]}'

# 3. 获取北方华创营收结构
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/operation-revenue-constitution" \
  --params '{"stockCode": "002371", "startDate": "2025-01-01"}'

# 4. 获取中芯国际财务数据
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["688981"], "startDate": "2024-01-01", "metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.ps.gp_m.t"]}'

# 5. 获取韦尔股份财务数据
python3 .claude/plugins/query_data/lixinger-api-docs/scripts/query_tool.py \
  --suffix "cn/company/fs/non_financial" \
  --params '{"stockCodes": ["603501"], "startDate": "2024-01-01", "metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.ps.gp_m.t"]}'
```

---

## 数据组合分析框架

### 产业链位置映射

```python
# 1. 获取行业数据
industry_data = query_api("cn/industry", {"source": "sw", "level": "one"})

# 2. 根据行业分类映射产业链位置
# 上游：采掘、有色金属、钢铁、化工等
# 中游：机械设备、电气设备、电子等
# 下游：汽车、家电、食品饮料、医药等

# 3. 建立产业链关系
# 示例：半导体产业链
# 上游：设备（北方华创、中微公司）
# 中游：制造（中芯国际、华虹半导体）
# 下游：设计（韦尔股份、兆易创新）
```

### 价格传导分析

```python
# 1. 获取上游公司营收结构
upstream_company = query_api("cn/company/operation-revenue-constitution", 
                            {"stockCode": "002371", "startDate": "2024-01-01"})

# 2. 获取下游公司营收结构
downstream_company = query_api("cn/company/operation-revenue-constitution", 
                              {"stockCode": "603501", "startDate": "2024-01-01"})

# 3. 分析价格传导
# 上游价格变化 → 中游成本变化 → 下游价格变化
# 毛利率变化反映价格传导效果
```

### 业绩传导分析

```python
# 1. 获取上游公司财务数据
upstream_fundamental = query_api("cn/company/fs/non_financial", 
                                {"stockCodes": ["002371"], "startDate": "2024-01-01", 
                                 "metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.ps.gp_m.t"]})

# 2. 获取下游公司财务数据
downstream_fundamental = query_api("cn/company/fs/non_financial", 
                                  {"stockCodes": ["603501"], "startDate": "2024-01-01", 
                                   "metricsList": ["q.ps.toi.t", "q.ps.np.t", "q.ps.gp_m.t"]})

# 3. 分析业绩传导
# 上游业绩变化 → 中游业绩变化 → 下游业绩变化
# 净利润增速变化反映业绩传导效果
```

---

## 常用产业链示例

### 新能源车产业链

| 环节 | 代表公司 | 数据API |
|------|----------|---------|
| 上游锂矿 | 天齐锂业(002460) | cn/company/operation-revenue-constitution |
| 中游电池 | 宁德时代(300750) | cn/company/fs/non_financial |
| 下游整车 | 比亚迪(002594) | cn/company/operation-revenue-constitution |

### 半导体产业链

| 环节 | 代表公司 | 数据API |
|------|----------|---------|
| 上游设备 | 北方华创(002371) | cn/company/operation-revenue-constitution |
| 中游制造 | 中芯国际(688981) | cn/company/fs/non_financial |
| 下游设计 | 韦尔股份(603501) | cn/company/operation-revenue-constitution |

### 化工产业链

| 环节 | 代表公司 | 数据API |
|------|----------|---------|
| 上游原油 | 中国石油(601857) | cn/company/operation-revenue-constitution |
| 中游化工 | 万华化学(600309) | cn/company/fs/non_financial |
| 下游制品 | 金发科技(600143) | cn/company/operation-revenue-constitution |

---

## 注意事项

### 数据时效性
- 行业数据：季度更新
- 公司财务数据：季度更新（财报披露后）
- 估值数据：日频更新

### 数据口径差异
- 行业分类：申万、中信、证监会等不同标准
- 财务数据：合并报表 vs 母公司报表
- 营收结构：产品分类 vs 地区分类

### 常见陷阱
- 产业链关系可能随时间变化
- 公司业务转型可能改变产业链位置
- 数据缺失需要使用代理指标

---

## 交叉验证建议

| 验证维度 | 推荐工具 | 目的 |
|----------|----------|------|
| 资金验证 | `$fund-flow-monitor` | 产业链景气但资金↓ → 风险 |
| 板块验证 | `$industry-board-analyzer` | 确认产业链是否与板块联动 |
| 事件验证 | `$disclosure-notice-monitor` | 排除政策/事件影响 |
| 估值验证 | `$valuation-regime-detector` | 评估产业链估值合理性 |

---

## 查找更多 API

详细的 API 查找和使用方法，请参考：`.claude/plugins/query_data/lixinger-api-docs/SKILL.md`