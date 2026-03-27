# earnings-expectation-gap

面向“业绩预告季预期差延续”主题的可执行插件原型。

## 能力

- 计算单标的 `surprise_fy0`、`undertraded_score`、`continuation_score`
- 根据阈值筛选“超预期但资金未充分交易”的候选
- 按 5D/10D/20D 维度输出延续概率与等级

## 快速使用

### 1) 单标的打分

```bash
python3 .claude/plugins/earnings-expectation-gap/scripts/score_earnings_expectation_gap.py \
  --symbol 000001.SZ \
  --guidance-mid 12.8 \
  --cons-fy0 10.0 \
  --open-day-ret 0.021 \
  --gap-ret 0.010 \
  --net-main-inflow-ratio 0.0012 \
  --net-xl-inflow-ratio 0.0003 \
  --turnover-pct-rank 0.42 \
  --lhb-net-buy-ratio 0.001 \
  --lhb-concentration 0.28 \
  --revision-up-diffusion 0.35 \
  --valuation-percentile 0.61
```

### 2) 批量筛选

```bash
python3 .claude/plugins/earnings-expectation-gap/scripts/rank_candidates.py \
  --input /tmp/earnings_candidates.csv \
  --min-surprise 0.15 \
  --min-undertraded 0.65 \
  --topk 20
```

输入 CSV 字段见 `schemas/earnings_event_record.schema.json`。
