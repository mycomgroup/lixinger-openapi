# Event Alpha Factory Plugin

面向“事件冲击 → 定价偏差 → 跟踪验证”的事件驱动中间层插件。

## 插件定位

本插件不替代上游 `event-driven-detector` / `event-study` 等能力，而是统一完成：

1. 事件标准化分类（taxonomy）
2. 历史同类事件反应分布对比（abnormal return panel）
3. 事件后 1D/5D/20D 验证清单生成（playbook）

目标是把“公告摘要”升级为“可交易且可验证”的结构化输出。

## 目录

- `events/event_taxonomy.json`：事件分类与映射规则
- `events/post_event_playbook.json`：1D/5D/20D 验证模板
- `schemas/abnormal_return_panel.schema.json`：异常收益面板字段契约
- `scripts/score_event_alpha.py`：计算 `EventAlphaScore`
- `scripts/generate_post_event_checklist.py`：生成验证清单

## Quickstart

```bash
python3 .claude/plugins/event-alpha-factory/scripts/score_event_alpha.py \
  --surprise 0.9 --persistence 0.7 --tradability 0.8 --confounder 0.2

python3 .claude/plugins/event-alpha-factory/scripts/generate_post_event_checklist.py \
  --playbook .claude/plugins/event-alpha-factory/events/post_event_playbook.json \
  --event-type earnings_beat
```

## 输出契约（核心）

- `normalized_event_type`
- `event_alpha_score`
- `percentile_1d/5d/20d`
- `post_event_checklist`
- `tracking_tasks`

## 评分公式（v1）

`EventAlphaScore = 0.35*SurpriseStrength + 0.30*PersistenceProb + 0.20*Tradability - 0.15*ConfounderPenalty`

## 建议接入技能

- `*_event-driven-detector`
- `*_event-study`
- `US-market_us-earnings-reaction-analyzer`
- `China-market_disclosure-notice-monitor`
- `China-market_ipo-newlist-monitor`
- `China-market_ipo-lockup-risk-monitor`
- `China-market_share-repurchase-monitor`
- `*_insider-trading-analyzer`
