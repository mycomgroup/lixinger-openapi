# Regime Lab Plugin

Regime Lab 用于将多市场（CN/HK/US，可扩展 EU/JP）与行业层信号统一为可消费的 `regime_state` 先验。

## Commands

- `/regime-lab-market [market] [date]`
- `/regime-lab-industry [market] [industry_scope]`
- `/regime-lab-cross-market [markets]`
- `/regime-lab-drift-watch [market] [horizon]`

## MVP 执行层

从仓库根目录运行：

```bash
python .claude/plugins/regime-lab/skills/regime-lab-core/scripts/regime_lab_mvp.py \
  --input .claude/plugins/regime-lab/skills/regime-lab-core/examples/sample_features.json \
  --outdir .claude/plugins/regime-lab/outputs/sample
```

输出：
- `regime/posterior.json`
- `regime/driver_attribution.json`
- `regime/invalidators.json`
- `regime/industry_regime_map.jsonl`

> 说明：`industry_regime_map.parquet` 在存在 `pyarrow` 时会自动写出，否则保持 JSONL。

## 合约

- `contracts/posterior.schema.json`
- `contracts/driver_attribution.schema.json`
- `contracts/invalidators.schema.json`

## 设计文档

详见：
- `.claude/plugins/regime-lab-technical-design.md`
- `.claude/plugins/SKILLS_TO_PLUGINS_DEEP_DIVE.md`
