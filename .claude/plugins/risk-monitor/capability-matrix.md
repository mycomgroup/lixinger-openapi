# 能力对照矩阵（当前覆盖现状）

> 基于 `templates/capability-matrix-template.md`，按 9 个 legacy 风险维度填写当前 engine 覆盖。

| capability_id | risk_dimension | capability_unit | legacy_skill_path | engine_rules | gap_status | owner | target_milestone |
|---|---|---|---|---|---|---|---|
| CAP-001 | equity-pledge-risk-monitor | 控股股东高质押+平仓线预警 | `.claude/plugins/risk-monitor/skills/legacy/equity-pledge-risk-monitor` | equity-pledge-risk-monitor.json<br>equity-pledge-risk-monitor-concentration.json<br>equity-pledge-risk-monitor-margin-call.json | partial | risk-team | Sprint-1 |
| CAP-002 | shareholder-risk-check | 减持/冻结/质押综合股东风险检查 | `.claude/plugins/risk-monitor/skills/legacy/shareholder-risk-check` | shareholder-risk-check.json<br>shareholder-risk-check-equity-freeze.json<br>shareholder-risk-check-reduction-plan.json | partial | risk-team | Sprint-1 |
| CAP-003 | shareholder-structure-monitor | 股东结构稳定性与筹码集中度监控 | `.claude/plugins/risk-monitor/skills/legacy/shareholder-structure-monitor` | shareholder-structure-monitor.json<br>shareholder-structure-monitor-ownership-instability.json<br>shareholder-structure-monitor-related-party-rise.json | partial | risk-team | Sprint-2 |
| CAP-004 | goodwill-risk-monitor | 商誉减值与并购后遗症风险监控 | `.claude/plugins/risk-monitor/skills/legacy/goodwill-risk-monitor` | goodwill-risk-monitor.json<br>goodwill-risk-monitor-auditor-change.json<br>goodwill-risk-monitor-impairment-probability.json | partial | risk-team | Sprint-2 |
| CAP-005 | st-delist-risk-scanner | ST/退市触发条件扫描 | `.claude/plugins/risk-monitor/skills/legacy/st-delist-risk-scanner` | st-delist-risk-scanner.json<br>st-delist-risk-scanner-compliance-trigger.json<br>st-delist-risk-scanner-financial-trigger.json | match | risk-team | Sprint-1 |
| CAP-006 | ipo-lockup-risk-monitor | 解禁供给冲击与减持压力预警 | `.claude/plugins/risk-monitor/skills/legacy/ipo-lockup-risk-monitor` | ipo-lockup-risk-monitor.json<br>ipo-lockup-risk-monitor-near-term-unlock.json<br>ipo-lockup-risk-monitor-vc-exit-pressure.json | partial | risk-team | Sprint-1 |
| CAP-007 | margin-risk-monitor | 两融杠杆拥挤与踩踏风险监控 | `.claude/plugins/risk-monitor/skills/legacy/margin-risk-monitor` | margin-risk-monitor.json<br>margin-risk-monitor-crowded-long.json<br>margin-risk-monitor-financing-broker-divergence.json | partial | risk-team | Sprint-2 |
| CAP-008 | limit-up-limit-down-risk-checker | 涨跌停板流动性锁死风险检查 | `.claude/plugins/risk-monitor/skills/legacy/limit-up-limit-down-risk-checker` | limit-up-limit-down-risk-checker.json<br>limit-up-limit-down-risk-checker-board-failure.json<br>limit-up-limit-down-risk-checker-liquidation-chain.json | match | risk-team | Sprint-1 |
| CAP-009 | liquidity-impact-estimator | 交易冲击成本与流动性缺口评估 | `.claude/plugins/risk-monitor/skills/legacy/liquidity-impact-estimator` | liquidity-impact-estimator.json<br>liquidity-impact-estimator-auction-gap.json<br>liquidity-impact-estimator-depth-slippage.json | partial | risk-team | Sprint-2 |

## 覆盖统计（9 维度）
- match: 2
- partial: 7
- missing: 0
- enhanced: 0
