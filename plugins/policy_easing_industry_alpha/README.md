# policy_easing_industry_alpha

面向“政策宽松到行业超额收益传导链”的研究型插件。

## 目标

识别宽信用周期中可能出现“先涨估值，后涨盈利（pattern_A）”的行业，并给出可解释证据链。

## 当前实现状态（MVP Scaffold）

- [x] 插件元信息与配置骨架
- [x] 特征工程模块接口（macro/flow/research/valuation_earnings）
- [x] 宽信用阶段识别接口
- [x] 行业收益拆解接口
- [x] 模式识别与行业排序接口
- [x] 统一 pipeline 入口（`run_detection.py`）
- [ ] 真实数据源接入
- [ ] 回测与监控

## 快速开始

```bash
python -m plugins.policy_easing_industry_alpha.pipelines.run_detection \
  --asof-date 2026-03-31 \
  --top-n 5
```

## 输出说明

当前输出为示例结构，遵循 `data_contract/schema.md`，便于后续替换为真实数据与模型。
