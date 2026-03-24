# Competitive Positioning Engine (CPE) — Scaffold

description: 竞争格局引擎骨架：定义比较空间、重构 peer clusters、沉淀 market map / profit pool / claims 的结构化输出契约。当前为骨架版本，优先把对象模型与中间产物 JSON 定下来，后续再按 Phase 2 补齐行业数据与推断规则。

## 目标与范围（Phase 2 预备）

- 先把输出契约与 case 目录结构跑通
- 允许研究员手工校正 peer list 与 claims 证据
- 不追求一步自动评分，先保证“证据链结构正确”

## 最小输出（骨架）

- `market_map.json`：市场定义、细分、关键玩家、集中度（可为空但字段齐全）
- `peer_clusters.json`：peer 列表、排除列表、聚类理由
- `claims.json`：竞争主张列表（dimension/claim/supporting_evidence/confidence/status）
- `verdict.json`：position、premium/discount view、confidence

