# /risk-monitor-event-update [watchlist]

持仓后事件驱动增量更新（公告/新闻/异动触发）。

## 输入

- `watchlist`
- `event_window`（如近24h/3d）
- `event_sources`（announcement, news, market_anomaly）

## 行为

1. 识别新增事件
2. 定位触发规则
3. 增量重算受影响股票
4. 输出新增/升级/解除告警

