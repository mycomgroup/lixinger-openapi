# 理杏仁金融分析技能包使用指南

## 快速开始

### 1. 环境配置

#### 配置理杏仁 Token

在项目根目录创建 `token.cfg` 文件：

```bash
echo "your_lixinger_token_here" > token.cfg
chmod 600 token.cfg
```

获取 Token：访问 [理杏仁开放平台](https://open.lixinger.com/) 注册并获取 API Token。

#### 无需安装依赖

`query_tool.py` 是完全独立的工具，直接运行即可，无需虚拟环境或安装依赖。

---

## 2. 使用方式

### 方式一：使用分析技能（推荐）

优先使用专业的分析技能，它们提供完整的分析方法论。

#### 步骤 1：查看技能说明

```bash
cat skills/China-market/dividend-corporate-action-tracker/SKILL.md
```

#### 步骤 2：查看数据获取指南

```bash
cat skills/China-market/dividend-corporate-action-tracker/references/data-queries.md
```

#### 步骤 3：使用 query_tool.py 获取数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare,dividendYield" \
  --limit 20
```

#### 步骤 4：按照方法论进行分析

查看 `references/methodology.md` 了解分析方法。

#### 步骤 5：按照模板输出结果

查看 `references/output-template.md` 了解输出格式。

### 方式二：直接查询数据

当找不到合适的分析技能时，使用原始数据查询工具。

#### 查询股票基本信息

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,name,listDate"
```

#### 查询财务数据

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.fs.non_financial" \
  --params '{"stockCode": "600519", "metricsList": ["roe", "grossProfitMargin"]}' \
  --limit 10
```

#### 查询历史行情

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.candlestick" \
  --params '{"stockCode": "600519", "startDate": "2024-01-01", "endDate": "2024-12-31"}' \
  --columns "date,open,high,low,close,volume"
```

---

## 3. 使用示例

### 示例 1：A股分红数据分析

**场景**：分析贵州茅台的分红历史

```bash
# 1. 查看技能说明
cat skills/China-market/dividend-corporate-action-tracker/SKILL.md

# 2. 获取分红数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.dividend" \
  --params '{"stockCode": "600519"}' \
  --columns "date,dividendPerShare,dividendYield,payoutRatio" \
  --limit 20

# 3. 分析分红趋势
# - 查看分红金额变化
# - 计算股息率
# - 评估分红稳定性
```

### 示例 2：港股市场概览

**场景**：分析恒生指数估值水平

```bash
# 获取恒生指数估值数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk.index.fundamental" \
  --params '{"indexCode": "HSI", "date": "2024-12-31"}' \
  --columns "date,pe,pb,roe,dividendYield"

# 分析估值水平
# - 对比历史分位数
# - 评估投资价值
```

### 示例 3：美股估值分析

**场景**：分析标普500指数估值

```bash
# 获取标普500指数估值数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "us.index.fundamental" \
  --params '{"indexCode": "SPX", "date": "2024-12-31"}' \
  --columns "date,pe,pb,roe,dividendYield"

# 分析估值水平
# - 对比历史均值
# - 评估市场风险
```

### 示例 4：财务报表深度分析

**场景**：分析宁德时代的财务状况

```bash
# 1. 查看技能说明
cat skills/China-market/financial-statement-analyzer/SKILL.md

# 2. 获取财务数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.fs.non_financial" \
  --params '{"stockCode": "300750", "metricsList": ["roe", "grossProfitMargin", "netProfitMargin", "debtToAssetRatio"]}' \
  --limit 20

# 3. 进行杜邦分析
# - ROE = 净利率 × 资产周转率 × 杠杆率
# - 分析盈利能力变化趋势
```

### 示例 5：量化因子选股

**场景**：使用多因子模型筛选股票

```bash
# 1. 查看技能说明
cat skills/China-market/quant-factor-screener/SKILL.md

# 2. 获取因子数据
# 价值因子：PE、PB
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.fundamental.non_financial" \
  --params '{"stockCodes": ["600519", "000858", "002304"]}' \
  --columns "stockCode,pe,pb,ps,pcf"

# 成长因子：营收增长率、净利润增长率
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.fs.non_financial" \
  --params '{"stockCodes": ["600519", "000858", "002304"]}' \
  --columns "stockCode,revenueGrowthRate,netProfitGrowthRate"

# 3. 计算因子得分并排名
```

---

## 4. 高级用法

### 字段过滤

使用 `--columns` 参数只返回需要的字段，节省 30-40% token：

```bash
# 只返回股票代码、名称、上市日期
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company" \
  --params '{"stockCodes": ["600519"]}' \
  --columns "stockCode,name,listDate"
```

### 数据筛选

使用 `--row-filter` 参数过滤数据行：

```bash
# 筛选 ROE > 15% 的数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.fs.non_financial" \
  --params '{"stockCode": "600519"}' \
  --row-filter "roe>15"
```

### 数组展开

使用 `--flatten` 参数展开嵌套数组：

```bash
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company" \
  --params '{"stockCodes": ["600519"]}' \
  --flatten
```

### 限制返回行数

使用 `--limit` 参数限制返回行数：

```bash
# 只返回最近 10 条数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.fs.non_financial" \
  --params '{"stockCode": "600519"}' \
  --limit 10
```

---

## 5. 技能选择指南

### 如何选择合适的技能？

#### 步骤 1：确定分析目标

- 个股分析？行业分析？市场分析？
- 基本面分析？技术面分析？资金面分析？
- 风险监控？投资决策？组合管理？

#### 步骤 2：确定市场

- A股市场：使用 `skills/China-market/` 下的技能
- 港股市场：使用 `skills/HK-market/` 下的技能
- 美股市场：使用 `skills/US-market/` 下的技能

#### 步骤 3：查找技能

查看 `.kiro/steering/lixinger-skills.md` 获取完整技能列表。

#### 步骤 4：查看技能文档

```bash
# 查看技能说明
cat skills/{market}/{skill-name}/SKILL.md

# 查看数据获取指南
cat skills/{market}/{skill-name}/references/data-queries.md
```

### 常见分析场景与技能对应

| 分析场景 | 推荐技能 | 市场 |
|---------|---------|------|
| 财务报表分析 | financial-statement-analyzer | A股/港股/美股 |
| 分红分析 | dividend-corporate-action-tracker | A股 |
| 估值分析 | valuation-regime-detector | A股/港股/美股 |
| 资金流向分析 | fund-flow-monitor | A股 |
| 北向资金分析 | northbound-flow-analyzer | A股 |
| 龙虎榜分析 | dragon-tiger-list-analyzer | A股 |
| 大宗交易分析 | block-deal-monitor | A股 |
| 行业分析 | industry-board-analyzer | A股 |
| 组合健康检查 | portfolio-health-check | A股/港股/美股 |
| 量化选股 | quant-factor-screener | A股/港股/美股 |

---

## 6. 常见问题

### Q1: 如何获取理杏仁 Token？

访问 [理杏仁开放平台](https://open.lixinger.com/)，注册账号后在个人中心获取 API Token。

### Q2: Token 如何配置？

在项目根目录创建 `token.cfg` 文件，将 Token 写入文件即可。

### Q3: 是否需要安装依赖？

不需要。`query_tool.py` 是完全独立的工具，直接运行即可。

### Q4: 如何查看所有可用的 API 接口？

查看 `../.claude/skills/lixinger-data-query/SKILL.md` 文件，包含所有 162 个 API 接口的列表。

### Q5: 如何查看某个 API 的详细文档？

查看 `../.claude/skills/lixinger-data-query/api_new/api-docs/` 目录下的对应文档。

### Q6: 数据更新频率是多少？

- 实时行情：实时更新
- 日线数据：每日收盘后更新
- 财务数据：季报/年报发布后更新
- 宏观数据：官方发布后更新

### Q7: API 调用有频率限制吗？

有。具体限制请查看理杏仁开放平台的服务条款。

### Q8: 如何优化查询性能？

1. 使用 `--columns` 参数只返回需要的字段
2. 使用 `--limit` 参数限制返回行数
3. 使用 `--row-filter` 参数过滤数据
4. 在应用层实现缓存

---

## 7. 最佳实践

### 数据查询最佳实践

1. **明确需求**：先确定需要哪些字段，避免返回无用数据
2. **字段过滤**：使用 `--columns` 参数，节省 token
3. **数据限制**：使用 `--limit` 参数，避免返回过多数据
4. **缓存策略**：对不常变化的数据进行缓存
5. **错误处理**：处理 API 调用失败的情况

### 分析流程最佳实践

1. **查看文档**：先查看技能的 SKILL.md 和 data-queries.md
2. **获取数据**：使用 query_tool.py 获取所需数据
3. **数据验证**：检查数据的完整性和准确性
4. **分析计算**：按照 methodology.md 进行分析
5. **结果输出**：按照 output-template.md 格式化输出

### 安全最佳实践

1. **Token 保护**：不要将 token.cfg 提交到版本控制系统
2. **权限控制**：设置 token.cfg 文件权限为 600
3. **数据合规**：遵守理杏仁服务条款，不转售数据
4. **频率控制**：注意 API 调用频率限制

---

## 8. 参考资料

- [理杏仁开放平台](https://open.lixinger.com/)
- [理杏仁 API 文档](https://open.lixinger.com/doc)
- [项目架构文档](./ARCHITECTURE.md)
- [技能列表](../.kiro/steering/lixinger-skills.md)

---

**文档版本**: v1.0  
**更新时间**: 2026-02-24
