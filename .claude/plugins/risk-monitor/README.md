# Risk Monitor Plugin

面向“选股后排雷 + 持仓后事件跟踪”的风险插件。

## 当前阶段目标

1. **旧能力迁移（不整合）**：将 9 个既有风险 skill 原样迁移到 `skills/legacy/`。
2. **新引擎重开发**：在 `skills/risk-signal-engine/` 内建立独立规则引擎规范与可扩展规则目录。
3. **事件相关覆盖**：支持公告/新闻/异动触发的持仓后增量重算。

## 目录

- `skills/legacy/`：旧 skill 原样迁移区（仅迁移，不改造）
- `skills/risk-signal-engine/`：新规则引擎（重开发）
- `skills/risk-monitor-orchestrator/`：编排层（后续接入）
- `templates/`：能力矩阵、规则 schema、排雷输出模板
- `commands/`：命令入口

## 迁移清单（9个）

- equity-pledge-risk-monitor
- shareholder-risk-check
- shareholder-structure-monitor
- goodwill-risk-monitor
- st-delist-risk-scanner
- ipo-lockup-risk-monitor
- margin-risk-monitor
- limit-up-limit-down-risk-checker
- liquidity-impact-estimator

## 开发策略

- 在迁移完成前，不对 `skills/legacy/*` 做逻辑改造。
- 新逻辑仅放在 `risk-signal-engine`，通过规则文件迭代。
- 输出必须是"问题发现导向"，而非仅指标转述。
- 路径规范详见 `templates/path-conventions.md`。
- 事件源定义详见 `templates/event-source-dictionary.json`。

## 覆盖率统计口径

能力矩阵中的 `gap_status` 统一按以下判定：

- `match`：新引擎在输入要素、核心规则与输出结论上与 legacy 能力单元等价，且无已知关键缺口。
- `partial`：已覆盖 legacy 的主干场景，但至少存在一个关键子能力（阈值分层、事件链路、输出字段或风控分支）未落地。
- `missing`：当前无可执行规则，或规则无法对应该 legacy 能力单元的核心判定逻辑。
- `enhanced`：完整覆盖 legacy 能力单元，并新增可验证增强（如跨维度联动、更多事件触发、解释性输出或更高精度阈值体系）。


## Event Source Dictionary

### 规范事件源枚举

| canonical_source | 中文别名 | 命令层可用 | Schema 可用 |
|---|---|---|---|
| announcement | 公告 | ✓ | ✓ |
| news | 新闻 | ✓ | ✓ |
| market_anomaly | 交易异动 | ✓ | ✓ |
| filing_update | 文件更新/备案更新 | ✗ | ✓ |
| manual | 手动触发 | ✗ | ✓ |

### 层级关系

- **命令层 subset**：`announcement`, `news`, `market_anomaly` → 用于 `/risk-monitor-event-update`
- **Schema 全集**：以上 5 个 → 用于规则定义 `event_triggers[].source`

### 中文→英文映射

| 中文 | 英文 |
|---|---|
| 公告 | announcement |
| 新闻 | news |
| 异动 | market_anomaly |
| 文件更新 | filing_update |
| 手动触发 | manual |


## 最小编排模块运行示例

可执行入口：`orchestrator/runner.py`

### 1) 运行一次 scan

```bash
python3 .claude/plugins/risk-monitor/orchestrator/runner.py scan \
  --watchlist '["600519","000858"]' \
  --as-of-date 2026-04-12 \
  --mode hybrid
```

输入参数（等价 JSON）

```json
{
  "command": "scan",
  "watchlist": ["600519", "000858"],
  "as_of_date": "2026-04-12",
  "mode": "hybrid",
  "event_window": "24h",
  "event_sources": ["announcement", "market_anomaly", "news"]
}
```

输出片段（示例）

```json
{
  "routes": [
    "skills/legacy/*",
    "skills/risk-signal-engine/rules/*"
  ],
  "alerts": [
    {
      "security": "600519",
      "action": "observe",
      "severity": "medium",
      "thesis": "Legacy branch executed for 600519 @ 2026-04-12",
      "evidence": ["legacy skill loaded: equity-pledge-risk-monitor"],
      "invalidation": "连续两个观察窗口无新增风险信号",
      "branch": "legacy"
    }
  ]
}
```

### 2) 运行一次 event-update

```bash
python3 .claude/plugins/risk-monitor/orchestrator/runner.py event-update \
  --watchlist '600519,000858' \
  --mode engine_only \
  --event-window 3d \
  --event-sources announcement,news
```

输入参数（等价 JSON）

```json
{
  "command": "event-update",
  "watchlist": ["600519", "000858"],
  "as_of_date": "2026-04-12",
  "mode": "engine_only",
  "event_window": "3d",
  "event_sources": ["announcement", "news"]
}
```

输出片段（示例）

```json
{
  "routes": ["skills/risk-signal-engine/rules/*"],
  "alerts": [
    {
      "security": "000858",
      "action": "deweight",
      "severity": "high",
      "thesis": "Engine branch evaluated for 000858 @ 2026-04-12",
      "evidence": ["engine rule matched: equity-pledge-risk-monitor"],
      "invalidation": "触发规则回落至低风险区间",
      "branch": "engine"
    }
  ]
}
```
