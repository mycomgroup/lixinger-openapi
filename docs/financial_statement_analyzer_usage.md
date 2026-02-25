# 财报深度分析技能使用说明

## 功能概述

`financial-statement-analyzer` 是一个完整的上市公司财务报表深度分析工具，支持 A股、港股、美股所有上市公司的多维度财务分析。

## 主要功能

1. **三大报表完整获取**：自动获取资产负债表、利润表、现金流量表历史数据
2. **杜邦分析体系**：ROE 拆解为净利率 × 资产周转率 × 杠杆率
3. **现金流质量分析**：验证经营现金流与净利润的匹配程度
4. **财务造假风险识别**：存贷双高/商誉减值/应收账款高企/存货积压等风险预警
5. **成长能力分析**：营收/利润/资产同比增长率分析
6. **偿债能力分析**：流动比率/速动比率/资产负债率/现金比率分析
7. **运营效率分析**：应收账款周转天数/存货周转天数/总资产周转率分析
8. **综合评分与评级**：基于多维度指标给出 A+ 到 D 的综合评级

## 使用方式

### 步骤 1：查看技能说明

```bash
# A股
cat skills/China-market/financial-statement-analyzer/SKILL.md

# 港股
cat skills/HK-market/hk-financial-statement/SKILL.md

# 美股
cat skills/US-market/us-financial-statement-analyzer/SKILL.md
```

### 步骤 2：查看数据获取指南

```bash
# A股
cat skills/China-market/financial-statement-analyzer/references/data-queries.md

# 港股
cat skills/HK-market/hk-financial-statement/references/data-queries.md

# 美股
cat skills/US-market/us-financial-statement-analyzer/references/data-queries.md
```

### 步骤 3：获取财务数据

#### A股示例：分析贵州茅台

```bash
# 获取非财务指标（ROE、毛利率、净利率等）
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.fs.non_financial" \
  --params '{"stockCode": "600519", "metricsList": ["roe", "grossProfitMargin", "netProfitMargin", "debtToAssetRatio"]}' \
  --limit 20

# 获取财务报表数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "cn.company.fs" \
  --params '{"stockCode": "600519"}' \
  --limit 20
```

#### 港股示例：分析腾讯控股

```bash
# 获取港股财务数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "hk.company.fs.non_financial" \
  --params '{"stockCode": "00700", "metricsList": ["roe", "grossProfitMargin", "netProfitMargin"]}' \
  --limit 20
```

#### 美股示例：分析苹果公司

```bash
# 获取美股财务数据
python3 skills/lixinger-data-query/scripts/query_tool.py \
  --suffix "us.company.fs.non_financial" \
  --params '{"stockCode": "AAPL", "metricsList": ["roe", "grossProfitMargin", "netProfitMargin"]}' \
  --limit 20
```

### 步骤 4：进行财务分析

按照 `references/methodology.md` 中的方法论进行分析：

1. **杜邦分析**：
   - ROE = 净利率 × 资产周转率 × 杠杆率
   - 分析 ROE 变化的驱动因素

2. **盈利能力分析**：
   - 毛利率、净利率趋势
   - 与同行业对比

3. **偿债能力分析**：
   - 流动比率、速动比率
   - 资产负债率

4. **运营效率分析**：
   - 应收账款周转天数
   - 存货周转天数
   - 总资产周转率

5. **成长能力分析**：
   - 营收增长率
   - 净利润增长率

6. **风险识别**：
   - 存贷双高风险
   - 商誉减值风险
   - 应收账款风险
   - 存货积压风险

### 步骤 5：输出分析结果

按照 `references/output-template.md` 格式化输出结果。

## 分析指标说明

### 杜邦分析

**ROE（净资产收益率）** = 净利率 × 资产周转率 × 杠杆率

- **净利率** = 净利润 / 营业收入
- **资产周转率** = 营业收入 / 总资产
- **杠杆率** = 总资产 / 净资产

### 盈利能力指标

- **毛利率** = (营业收入 - 营业成本) / 营业收入
- **净利率** = 净利润 / 营业收入
- **ROE** = 净利润 / 净资产
- **ROA** = 净利润 / 总资产

### 偿债能力指标

- **流动比率** = 流动资产 / 流动负债
- **速动比率** = (流动资产 - 存货) / 流动负债
- **资产负债率** = 总负债 / 总资产
- **现金比率** = 货币资金 / 流动负债

### 运营效率指标

- **应收账款周转天数** = 365 / (营业收入 / 应收账款平均余额)
- **存货周转天数** = 365 / (营业成本 / 存货平均余额)
- **总资产周转率** = 营业收入 / 总资产平均余额

### 成长能力指标

- **营收增长率** = (本期营收 - 上期营收) / 上期营收
- **净利润增长率** = (本期净利润 - 上期净利润) / 上期净利润
- **总资产增长率** = (期末总资产 - 期初总资产) / 期初总资产

### 综合评级标准

- **A+**: 得分 ≥ 85，财务状况非常优秀
- **A**: 得分 ≥ 75，财务状况良好
- **B+**: 得分 ≥ 65，财务状况一般偏上
- **B**: 得分 ≥ 55，财务状况一般
- **C**: 得分 ≥ 45，财务状况较差
- **D**: 得分 < 45，财务状况糟糕，存在较高风险

### 风险类型说明

- **存贷双高风险**：货币资金远低于有息负债，存在财务造假嫌疑
- **商誉减值风险**：商誉占净资产比例过高，存在大额减值风险
- **应收账款风险**：应收账款占营收比例过高，回款能力弱
- **存货积压风险**：存货占流动资产比例过高，存在积压减值风险

## 注意事项

1. 数据来源为理杏仁（Lixinger）开放平台 API，需要配置 API Token
2. 返回数据中的金额单位均为亿元人民币（A股）、亿港元（港股）、亿美元（美股）
3. 财报数据更新频率为季度，年报数据通常在次年 4 月前披露
4. 建议结合多个维度进行分析，避免单一指标决策
5. 所有分析结果仅供参考，不构成投资建议

## 相关文档

- [技能列表](../.kiro/steering/lixinger-skills.md)
- [使用指南](./USAGE_GUIDE.md)
- [架构设计](./ARCHITECTURE.md)

---

**文档版本**: v2.0  
**更新时间**: 2026-02-24
