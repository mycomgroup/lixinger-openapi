# 港股Skills数据查询文档状态

## 📊 完成状态

### ✅ 已完善 (7/12)

1. **hk-concentration-risk** - 港股集中度风险监控
   - ✅ 完整的data-queries.md
   - ✅ additional-data-sources.md（增强数据源）
   - 包含：组合数据、风险因子、相关性矩阵等

2. **hk-dividend-tracker** - 港股股息跟踪器
   - ✅ 完整的data-queries.md
   - 包含：分红历史、股息率、财务数据等

3. **hk-market-overview** - 港股市场概览
   - ✅ 完整的data-queries.md
   - 包含：指数数据、市场宽度、行业板块、资金流向等

4. **hk-southbound-flow** - 南向资金流向分析
   - ✅ 完整的data-queries.md
   - 包含：指数/个股/行业南向资金、持仓分析、资金流向计算等

5. **hk-valuation-analyzer** - 港股估值分析
   - ✅ 完整的data-queries.md
   - 包含：市场/行业/个股估值、DCF模型、相对估值、估值区间分析等

6. **hk-financial-statement** - 港股财务报表分析
   - ✅ 完整的data-queries.md
   - 包含：三大报表、财务比率计算、健康度评分、趋势分析等

7. **hk-sector-rotation** - 港股行业轮动
   - ✅ 完整的data-queries.md
   - 包含：相对强度、资金轮动、轮动信号、配置建议等

### ⏳ 待完善 (5/12)

8. **hk-market-breadth** - 港股市场宽度
   - 现有：基础data-queries.md
   - 需要：补充市场宽度指标

9. **hk-currency-risk** - 港股汇率风险监控
   - 现有：基础data-queries.md
   - 需要：补充汇率API、风险计算方法

10. **hk-etf-flow** - 港股ETF资金流向
   - 现有：基础data-queries.md
   - 需要：补充ETF相关API

8. **hk-financial-statement** - 港股财务报表分析
   - 现有：基础data-queries.md
   - 需要：补充财务报表API

9. **hk-foreign-flow** - 港股外资流向
   - 现有：基础data-queries.md
   - 需要：补充外资流向API

10. **hk-liquidity-risk** - 港股流动性风险
    - 现有：基础data-queries.md
    - 需要：补充流动性指标API

11. **hk-market-breadth** - 港股市场宽度
    - 现有：基础data-queries.md
    - 需要：补充市场宽度指标

12. **hk-sector-rotation** - 港股行业轮动
    - 现有：基础data-queries.md
    - 需要：补充行业轮动指标

---

## 🎯 完善建议

### 优先级1（核心功能）
1. **hk-market-breadth** - 市场宽度（市场分析）✅ 下一个
2. **hk-liquidity-risk** - 流动性风险（风险管理）
### 优先级2（风险管理）
3. **hk-currency-risk** - 汇率风险
4. **hk-liquidity-risk** - 流动性风险

### 优先级3（高级分析）
5. **hk-sector-rotation** - 行业轮动
6. **hk-market-breadth** - 市场宽度
7. **hk-foreign-flow** - 外资流向
8. **hk-etf-flow** - ETF资金流向

---

## 📋 完善模板

每个skill的data-queries.md应包含：

### 1. 核心数据需求
- 列出该skill需要的所有数据类型
- 说明数据用途

### 2. 数据查询示例
- 提供完整的query_tool.py命令
- 包含参数说明
- 标注核心API（⭐）

### 3. 计算方法
- 说明如何使用API数据进行计算
- 提供Python代码示例

### 4. 常用API列表
- 核心API（必需）
- 辅助API（可选）

### 5. 缺失数据说明
- 列出理杏仁API无法提供的数据
- 说明替代方案

### 6. 使用示例
- 提供完整的分析流程示例
- 包含多个API的组合使用

---

## 🔧 需要的港股API

### 已确认可用
- ✅ `hk.company` - 公司基本信息
- ✅ `hk.company.dividend` - 分红数据
- ✅ `hk.company.fundamental.non-financial` - 基本面数据
- ✅ `hk.company.fs.non-financial` - 财务报表
- ✅ `hk.company.candlestick` - K线数据
- ✅ `hk.company.industries` - 行业分类
- ✅ `hk.company.mutual-market` - 港股通数据
- ✅ `hk.index.fundamental` - 指数基本面
- ✅ `hk.index.constituents` - 指数成分股
- ✅ `hk.industry.fundamental.hsi` - 行业基本面

### 需要确认
- ⚠️ `hk.company.short-selling` - 卖空数据
- ⚠️ `hk.company.repurchase` - 回购数据
- ⚠️ `hk.index.mutual-market` - 指数互联互通
- ⚠️ `hk.industry.mutual-market.hsi` - 行业互联互通

### 可能缺失（需要外部数据）
- ❌ ETF持仓明细
- ❌ 外资持仓明细（非港股通）
- ❌ 期权数据
- ❌ 实时资金流向

---

## 📝 下一步行动

### 立即行动
1. 完善hk-market-overview（最常用）
2. 完善hk-southbound-flow（重要指标）
3. 完善hk-valuation-analyzer（核心分析）

### 短期计划
4. 完善所有风险管理相关skills
5. 为每个skill创建additional-data-sources.md
6. 添加更多使用示例

### 长期计划
7. 创建港股数据获取最佳实践文档
8. 建立港股API使用案例库
9. 开发自动化测试脚本

---

## 🤝 贡献指南

如需完善某个skill的data-queries.md：

1. 参考已完成的示例（hk-concentration-risk, hk-dividend-tracker）
2. 阅读该skill的SKILL.md了解功能需求
3. 查看理杏仁API文档确认可用数据
4. 编写完整的查询示例和计算方法
5. 标注缺失数据和替代方案

---

**更新日期**: 2026-02-24  
**完成进度**: 7/12 (58.3%)  
**下次更新**: hk-market-breadth
