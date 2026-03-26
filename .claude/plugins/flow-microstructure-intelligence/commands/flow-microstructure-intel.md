---
description: 生成资金结构与交易行为画像，判断趋势资金质量与拥挤/流动性脆弱风险
argument-hint: [market] [window]
---

你是 Flow-Microstructure Intelligence 插件执行器。

请按以下流程输出：

1. 读取并整合以下域信号（有则用，无则降级）：
   - A 股：fund flow / northbound / hsgt holdings / dragon-tiger / block deals / limit-up pool / intraday microstructure
   - 港股：southbound / foreign flow / ETF flow
   - 通用：factor crowding
2. 计算：
   - `source_quality_score`
   - `stability_score`
   - `structure_health_score`
   - `crowding_risk_score`
   - `fragility_risk_score`
   - `flow_quality_score`
3. 判别状态：
   - `SUSTAINABLE_TREND`
   - `NEUTRAL_TRANSITION`
   - `CROWDING_PULSE`
4. 写出标准文件：
   - `capital/owner_mix.json`
   - `capital/crowding_risk.json`
   - `capital/liquidity_fragility_curve.json`
   - `capital/flow_quality_summary.json`
5. 给出交易翻译：
   - 建议持有时长
   - 仓位上限
