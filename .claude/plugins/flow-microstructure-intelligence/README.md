# Flow-Microstructure Intelligence Plugin

Flow-Microstructure Intelligence（资金结构与交易行为引擎）用于回答：

- 当前行情是**真实配置资金推动**，还是**短期交易拥挤 + 流动性幻觉**？

插件统一聚合资金来源、持仓稳定性、成交结构、拥挤度，输出：

- `capital/owner_mix.json`
- `capital/crowding_risk.json`
- `capital/liquidity_fragility_curve.json`

## Command

- `/flow-microstructure-intel [market] [window]`

## MVP 执行

```bash
python .claude/plugins/flow-microstructure-intelligence/skills/flow-microstructure-core/scripts/flow_microstructure_mvp.py \
  --input .claude/plugins/flow-microstructure-intelligence/skills/flow-microstructure-core/examples/sample_features.json \
  --outdir .claude/plugins/flow-microstructure-intelligence/outputs/sample
```

## 输出文件

- `capital/owner_mix.json`
- `capital/crowding_risk.json`
- `capital/liquidity_fragility_curve.json`
- `capital/flow_quality_summary.json`

## 合约

- `contracts/owner_mix.schema.json`
- `contracts/crowding_risk.schema.json`
- `contracts/liquidity_fragility_curve.schema.json`
