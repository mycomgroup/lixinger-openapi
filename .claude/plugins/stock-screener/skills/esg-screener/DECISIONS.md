# esg-screener 设计决策

## 1. 核心定位

把 ESG 策略收缩为“治理与风险代理筛选”，避免伪装成仓库当前无法支撑的完整 ESG 评分系统。

## 2. 候选池底座

统一先用 `.claude/skills/lixinger-screener` 做候选池与基础排除，原因是：
- 先控制范围
- 先排除明显财务与交易性不合格样本
- 把治理和争议补查留给少量入围股

## 3. 代理框架

默认优先看：
- 股东结构
- 分红与资本配置稳定性
- 审计意见、监管措施、问询函
- 外部 ESG 评级变化（仅作参考）

这比编造一个无法核验的 E/S/G 综合分更可信。

## 4. 接口选择

优先使用：
- `cn/company/majority-shareholders`
- `cn/company/nolimit-shareholders`
- `cn/company/measures`
- `cn/company/inquiry`
- `cn/company/fs/non_financial` 与 `fundamental/non_financial` 做财务与分红侧辅助

## 5. 输出策略

结果至少拆成：
- `治理改善机会`
- `稳健治理候选`
- `监管风险预警`
- `高收益但高治理风险`

并且必须说明哪些结论来自外部评级，哪些来自仓库内代理数据。

## 6. 数据边界

当前不做的事情：
- 伪造完整 ESG 评分
- 把未验证的环境、社会指标写成已实装能力
- 忽略外部依赖和数据缺口
