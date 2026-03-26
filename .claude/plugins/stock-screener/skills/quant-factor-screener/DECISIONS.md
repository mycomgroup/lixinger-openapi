# quant-factor-screener 设计决策

## 1. 核心定位

把量化因子策略收敛为“可复现的因子共振识别与解释层”，而不是宏大但不可验证的学术大杂烩。

它不是新的母策略，而是服务于现有母策略的解释层：
- 为 `high-dividend-strategy` 解释红利质量、现金牛复利与股东回报增强
- 为 `undervalued-stock-screener` 解释价值修复、龙头错杀与风格冲突

## 2. 候选池底座

统一先用 `.claude/skills/lixinger-screener` 收敛 Universe，再对入围股补查数据。原因是：
- 控制数据量
- 先排除明显不适合的股票
- 保留因子解释所需的重点样本

## 3. 因子范围

当前优先保留仓库内较容易验证的因子：
- 价值
- 质量
- 成长
- 股东回报增强项
- 动量
- 低波
- 规模

暂不把未验证的预期修正、复杂应计质量、拥挤度数据库等写成默认能力。

## 4. 接口选择

优先使用：
- `cn/company/fundamental/non_financial` 提供价值、规模、流动性基础指标
- `cn/company/fs/non_financial` 提供质量与成长指标
- `cn/company/candlestick` / `cn/index/candlestick` 提供动量、波动与基准
- `cn/company/industries` 提供行业归属
- `macro/interest-rates` 仅用于轻量解释利率环境，不用于重型择时

## 5. 输出策略

结果至少拆成：
- `高共振候选`
- `风格受益候选`
- `低估待启动候选`
- `因子冲突高风险候选`

重点不是“谁分高”，而是“为什么高、哪里冲突、哪些不能追”。

## 6. 协同边界

当前默认边界是：
- 不替代 `high-dividend-strategy` 的股东回报判断
- 不替代 `undervalued-stock-screener` 的低估原因分析
- 只负责把价值、质量、成长、股东回报和风格冲突解释清楚

## 7. 数据边界

当前不做的事情：
- 使用未验证字段名
- 伪精确宏观择时
- 把单一风格行情误写成长期因子有效性结论
- 把单一高股息或单一动量误写成完整多因子共振

## 8. 第一轮改造清单

按当前优先方向并入设计，后续优先回填以下位置：

1. `SKILL.md`
   - 固定 `cash-cow-compounder` 与 `leader-oversold-recovery` 两个解释层接口
   - 输出时显式标明服务的主线与对应母策略分类
2. `references/factor-methodology.md`
   - 固定 `价值 + 质量 + 成长 + 股东回报` 用于 `cash-cow-compounder`
   - 固定 `价值 + 质量 + 动量 / 低波冲突` 用于 `leader-oversold-recovery`
3. `references/output-template.md`
   - 新增 `主线归属`、`因子共振点`、`因子冲突点`、`不应越权替代的主判断`

本策略继续保持解释层边界：
- 不替代 `high-dividend-strategy`
- 不替代 `undervalued-stock-screener`
- 只解释为什么成立、哪里冲突、哪些结果不能追
