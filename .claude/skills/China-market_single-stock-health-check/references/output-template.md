# 个股体检输出模板

结构化的一页诊断卡片模板，参考 stock-analyzer 的 JSON 输出格式。

---

## 输出格式

### 方式 1：一页卡片（默认）

```markdown
# 【个股体检报告】股票名称（代码）

**生成时间**：YYYY-MM-DD HH:MM:SS  
**数据截至**：YYYY-MM-DD  
**分析师**：AI 综合研究与风控分析师

---

## 📊 健康评分

**总分**：XX/100 分（评级：X）  
**红灯数量**：X 个

### 维度得分

| 维度 | 得分 | 权重 | 加权得分 | 状态 |
|------|------|------|----------|------|
| 基本面与财务质量 | XX/10 | 20% | XX | ✅/⚠️/🚨 |
| 估值与分位 | XX/10 | 15% | XX | ✅/⚠️/🚨 |
| 业务质量分析 | XX/10 | 10% | XX | ✅/⚠️/🚨 |
| 股东与股权结构 | XX/10 | 10% | XX | ✅/⚠️/🚨 |
| 机构持仓分析 | XX/10 | 10% | XX | ✅/⚠️/🚨 |
| 治理与公告事件 | XX/10 | 10% | XX | ✅/⚠️/🚨 |
| 监管风险评估 | XX/10 | 10% | XX | ✅/⚠️/🚨 |
| 交易与流动性 | XX/10 | 5% | XX | ✅/⚠️/🚨 |
| 资金与持股 | XX/10 | 5% | XX | ✅/⚠️/🚨 |
| 行业定位与对比 | XX/10 | 5% | XX | ✅/⚠️/🚨 |

**状态说明**：✅ 健康 | ⚠️ 需关注 | 🚨 红灯警示

---

## 🎯 核心结论

1. **盈利能力**：[简洁判断，引用具体数据]
2. **估值水平**：[简洁判断，引用具体数据]
3. **业务质量**：[简洁判断，引用具体数据]
4. **股权结构**：[简洁判断，引用具体数据]
5. **综合建议**：[买入/持有/观望/规避，附理由]

---

## 🚨 红灯警示

### 高风险项（需立即关注）

1. **[维度名称]**：[具体问题描述]
   - 数据：[具体数值]
   - 风险：[风险说明]
   - 建议：[应对措施]

2. **[维度名称]**：[具体问题描述]
   - 数据：[具体数值]
   - 风险：[风险说明]
   - 建议：[应对措施]

### 中等风险项（需持续监控）

1. **[维度名称]**：[具体问题描述]
2. **[维度名称]**：[具体问题描述]

---

## 📋 详细分析

### 1. 基本面与财务质量（XX/20 分）

**盈利能力**：
- ROE：XX%（近 3 年平均）
- 毛利率：XX%
- 净利率：XX%
- 评价：[优秀/良好/一般/较差]

**成长性**：
- 营收 3 年 CAGR：XX%
- 净利润 3 年 CAGR：XX%
- 评价：[高成长/稳健/低增长/负增长]

**现金流质量**：
- 经营现金流/净利润：XX
- 自由现金流：[连续为正/偶有为负/连续为负]
- 评价：[优秀/良好/一般/较差]

---

### 2. 估值与分位（XX/15 分）

**当前估值**：
- PE-TTM：XX（历史分位：XX%）
- PB：XX（历史分位：XX%）
- PS-TTM：XX
- PEG：XX

**估值判断**：
- 相对历史：[低估/合理/高估]
- 相对行业：[低估/合理/高估]
- 综合评价：[值得买入/可以持有/建议观望]

---

### 3. 业务质量分析（XX/10 分）

**客户集中度**：
- 前五大客户占比：XX%
- 客户稳定性：[稳定/有变化/频繁变化]
- 风险评估：[低/中/高]

**供应商集中度**：
- 前五大供应商占比：XX%
- 供应链风险：[低/中/高]

**综合评价**：[业务分散/适度集中/高度集中]

---

### 4. 股东与股权结构（XX/10 分）

**股权集中度**：
- 第一大股东持股：XX%
- 前十大股东持股：XX%
- 评价：[稳定/可接受/风险]

**股权质押**：
- 质押比例：XX%
- 风险等级：[无/低/中/高]

**增减持**：
- 近 1 年大股东增减持：[净增持/无变化/净减持] XX%
- 近 1 年高管增减持：[净增持/无变化/净减持] XX%

---

### 5. 机构持仓分析（XX/10 分）

**公募基金持股**：
- 持股比例（占流通股）：XX%
- 持仓基金数量：XX 只
- 近 1 年变化：[增加/稳定/减少] XX%

**机构认可度**：
- 评价：[高度认可/认可/一般/较少]
- 趋势：[积极/稳定/谨慎/撤离]

---

### 6. 治理与公告事件（XX/10 分）

**信息披露**：
- 定期报告及时性：[按时/延迟]
- 公告完整性：[完整/有补充/有更正]

**分红与回购**：
- 近 3 年平均分红率：XX%
- 近 1 年回购：[有/无]
- 评价：[慷慨/良好/一般/吝啬]

---

### 7. 监管风险评估（XX/10 分）

**问询函**：
- 近 1 年数量：XX 次
- 主要类型：[定期报告审核/重大资产重组/其他]
- 风险等级：[无/低/中/高]

**监管措施**：
- 近 3 年记录：[无/监管工作函/监管警示/通报批评/公开谴责]
- 风险等级：[无/低/中/高]

**综合评价**：[合规良好/需关注/有风险/高风险]

---

### 8. 交易与流动性（XX/5 分）

**流动性**：
- 日均成交额（近 3 个月）：XX 亿
- 评价：[优秀/良好/一般/较差]

**波动性**：
- 近 1 年涨跌停次数：XX 次
- 评价：[稳定/正常/波动大]

---

### 9. 资金与持股（XX/5 分）

**北向资金**：
- 持股比例：XX%
- 近 1 年变化：[增加/稳定/减少]

**融资融券**：
- 融资余额/流通市值：XX%
- 活跃度：[活跃/一般]

**市场热度**：
- 关注度：[高/中/低]

---

### 10. 行业定位与对比（XX/5 分）

**行业信息**：
- 所属行业：[行业名称]
- 行业地位：[龙头/领先/中游/尾部]

**同业对比**：
- 市值排名：第 XX 名
- ROE 排名：第 XX 名
- 评价：[优秀/良好/一般]

---

## 📌 监控清单

### 需持续跟踪的指标

1. **财务指标**：
   - [ ] 季度营收增长率
   - [ ] 季度净利润增长率
   - [ ] 经营现金流

2. **估值指标**：
   - [ ] PE/PB 分位变化
   - [ ] 相对行业估值

3. **股东变化**：
   - [ ] 大股东增减持
   - [ ] 股权质押比例

4. **机构持仓**：
   - [ ] 基金持股变化
   - [ ] 北向资金变化

5. **公告事件**：
   - [ ] 定期报告
   - [ ] 重大事项公告
   - [ ] 问询函/监管措施

---

## 💡 建议与下一步

### 投资建议

**综合评级**：[强烈买入/买入/持有/观望/规避]

**理由**：
1. [核心优势 1]
2. [核心优势 2]
3. [主要风险 1]
4. [主要风险 2]

### 进一步尽调

1. **深度财务分析**：使用 `financial-statement-analyzer` 进行详细财报分析
2. **同业对比**：使用 `peer-comparison-analyzer` 对比竞争对手
3. **事件跟踪**：使用 `disclosure-notice-monitor` 监控公告
4. **资金流向**：使用 `fund-flow-monitor` 分析资金动向

### 需要的补充数据

1. [数据类型 1]：[说明为什么需要]
2. [数据类型 2]：[说明为什么需要]

---

## 📎 附录

### 数据来源

- 财务数据：理杏仁 API（`cn/company/fs/non_financial`, `cn/company/fundamental/non_financial`）
- 估值数据：理杏仁 API（`cn/company/fundamental/non_financial`）
- 股东数据：理杏仁 API（`cn/company/majority-shareholders`, `cn/company/pledge`）
- 机构持仓：理杏仁 API（`cn/company/fund-shareholders`）
- 监管数据：理杏仁 API（`cn/company/inquiry`, `cn/company/measures`）
- 交易数据：理杏仁 API（`cn/company/candlestick`, `cn/company/mutual-market`）

### 免责声明

本报告仅供信息参考与教育目的，不构成投资建议。投资有风险，决策需谨慎。

---

**报告生成工具**：single-stock-health-check skill  
**版本**：v2.0  
**最后更新**：2026-02-26
```

---

## 方式 2：简要要点

```markdown
# 【个股体检】股票名称（代码）

**健康评分**：XX/100 分（评级：X）| **红灯**：X 个

## 核心结论

1. **盈利能力**：ROE XX%，[优秀/良好/一般/较差]
2. **估值水平**：PE XX（分位 XX%），[低估/合理/高估]
3. **业务质量**：客户集中度 XX%，[分散/适中/集中]
4. **股权结构**：质押比例 XX%，[无风险/低风险/中等风险/高风险]
5. **机构持仓**：基金持股 XX%，[高度认可/认可/一般/较少]
6. **监管风险**：近 1 年问询 XX 次，[无风险/低风险/中等风险/高风险]

## 红灯警示

- 🚨 [问题 1]
- 🚨 [问题 2]
- ⚠️ [问题 3]

## 投资建议

**评级**：[强烈买入/买入/持有/观望/规避]  
**理由**：[简要说明]
```

---

## 方式 3：JSON 格式（参考 stock-analyzer）

```json
{
  "metadata": {
    "stockCode": "600519",
    "stockName": "贵州茅台",
    "market": "cn",
    "timestamp": "2026-02-26T10:30:00+08:00",
    "dataDate": "2026-02-25",
    "analyst": "AI 综合研究与风控分析师"
  },
  "healthScore": {
    "total": 85,
    "rating": "B",
    "redFlags": 1,
    "dimensions": {
      "fundamental": {"score": 8.5, "weight": 0.20, "weighted": 1.70, "status": "healthy"},
      "valuation": {"score": 7.0, "weight": 0.15, "weighted": 1.05, "status": "healthy"},
      "businessQuality": {"score": 6.0, "weight": 0.10, "weighted": 0.60, "status": "warning"},
      "shareholding": {"score": 8.0, "weight": 0.10, "weighted": 0.80, "status": "healthy"},
      "institutional": {"score": 9.0, "weight": 0.10, "weighted": 0.90, "status": "healthy"},
      "governance": {"score": 8.0, "weight": 0.10, "weighted": 0.80, "status": "healthy"},
      "regulatory": {"score": 10.0, "weight": 0.10, "weighted": 1.00, "status": "healthy"},
      "liquidity": {"score": 4.0, "weight": 0.05, "weighted": 0.20, "status": "healthy"},
      "capitalFlow": {"score": 7.0, "weight": 0.05, "weighted": 0.35, "status": "healthy"},
      "industry": {"score": 9.0, "weight": 0.05, "weighted": 0.45, "status": "healthy"}
    }
  },
  "coreConclusions": [
    "盈利能力优秀：ROE 25.3%，毛利率 91.2%，净利率 52.1%",
    "估值合理偏低：PE 18.5（历史分位 35%），PB 6.2（历史分位 32%）",
    "客户集中度适中：前五大客户占比 42%，需关注",
    "股权结构稳定：无质押，大股东持股 61.5%",
    "综合建议：买入，基本面优秀，估值合理，长期持有价值高"
  ],
  "redFlags": [
    {
      "dimension": "businessQuality",
      "severity": "warning",
      "issue": "客户集中度偏高",
      "data": "前五大客户占比 42%",
      "risk": "客户流失风险",
      "suggestion": "关注客户稳定性，分散客户结构"
    }
  ],
  "detailedAnalysis": {
    "fundamental": {
      "profitability": {
        "roe": 25.3,
        "grossMargin": 91.2,
        "netMargin": 52.1,
        "rating": "excellent"
      },
      "growth": {
        "revenueCagr3y": 18.5,
        "netProfitCagr3y": 17.2,
        "rating": "good"
      },
      "cashFlow": {
        "ocfToNetProfit": 1.15,
        "freeCashFlow": "positive",
        "rating": "excellent"
      }
    },
    "valuation": {
      "current": {
        "pe": 18.5,
        "pb": 6.2,
        "ps": 9.8,
        "peg": 1.08
      },
      "percentile": {
        "pe": 35,
        "pb": 32
      },
      "assessment": "undervalued"
    },
    "businessQuality": {
      "customerConcentration": {
        "top5Ratio": 42,
        "stability": "stable",
        "risk": "medium"
      },
      "supplierConcentration": {
        "top5Ratio": 28,
        "risk": "low"
      }
    },
    "shareholding": {
      "concentration": {
        "top1": 61.5,
        "top10": 78.2
      },
      "pledge": {
        "ratio": 0,
        "risk": "none"
      },
      "changes": {
        "majorShareholders": 0.5,
        "executives": 0.2
      }
    },
    "institutional": {
      "fundHolding": {
        "ratio": 8.5,
        "fundCount": 1250,
        "change1y": 1.2,
        "trend": "positive"
      }
    },
    "governance": {
      "disclosure": {
        "timeliness": "onTime",
        "completeness": "complete"
      },
      "dividend": {
        "payoutRatio3y": 55,
        "buyback1y": false
      }
    },
    "regulatory": {
      "inquiry": {
        "count1y": 0,
        "risk": "none"
      },
      "measures": {
        "count3y": 0,
        "risk": "none"
      }
    },
    "liquidity": {
      "avgTurnover3m": 2.5,
      "limitUpDown1y": 0,
      "rating": "good"
    },
    "capitalFlow": {
      "northbound": {
        "ratio": 6.2,
        "change1y": 0.8
      },
      "marginTrading": {
        "ratio": 3.5
      }
    },
    "industry": {
      "name": "白酒",
      "position": "leader",
      "marketCapRank": 1,
      "roeRank": 1
    }
  },
  "monitoringList": [
    "季度营收增长率",
    "季度净利润增长率",
    "PE/PB 分位变化",
    "基金持股变化",
    "客户集中度变化"
  ],
  "recommendation": {
    "rating": "buy",
    "reasons": [
      "基本面优秀，ROE 持续高于 20%",
      "估值合理，PE 处于历史低位",
      "机构持仓稳定，北向资金持续流入",
      "无监管风险，信息披露规范"
    ],
    "risks": [
      "客户集中度偏高，需关注客户稳定性"
    ]
  },
  "nextSteps": {
    "furtherAnalysis": [
      "使用 financial-statement-analyzer 进行详细财报分析",
      "使用 peer-comparison-analyzer 对比竞争对手"
    ],
    "additionalData": []
  }
}
```

---

## 输出选择建议

- **一页卡片**：适合快速查看，信息全面但简洁
- **简要要点**：适合快速决策，只看核心结论
- **JSON 格式**：适合程序化处理，便于集成到其他系统

---

**最后更新**：2026-02-26
