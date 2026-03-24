# CPE Web-Grounded Sourcing Playbook

目标：为 `competitive_positioning/` 四个 JSON 提供可复查、可追溯、尽量最新的证据输入，减少模型凭记忆补数字。

## 一条硬原则

先找来源，再写 JSON；先写事实，再写推断；先写 claims，再写 verdict。

## 来源优先级

`Tier 1`
- 公司官网、年报、业绩公告、投资者交流纪要、产品发布
- 监管与行业机构：欧盟委员会、交易所、行业协会、海关

`Tier 2`
- 结构化数据源：理杏仁、AkShare、SNE Research、乘联会口径转引

`Tier 3`
- Reuters、AP、主流财经媒体、专业行业媒体

规则：
- 高 severity claim 不应只依赖 `Tier 3`
- 估计值必须明确写成 estimate / inferred，不要伪装成披露值
- 所有时间敏感信息使用绝对日期，例如 `2024-10-29`

## 文件级构造方法

### market_map.json

适合填入的事实：
- 市场定义
- 细分市场
- 市场规模
- CAGR
- CR3 / CR5 / HHI

推荐来源：
- 公司年报中的业务拆分与管理层口径
- 行业协会销量口径
- 监管或海关数据
- 行业研究机构的集中度统计

填充规则：
- `estimated_market_size_bn_cny` 和 `estimated_cagr_pct` 如果没有可信来源，可保留 `null`
- `overall_concentration.notes` 写清楚口径，例如 “中国新能源乘用车，按批发销量”
- `data_sources` 至少覆盖 2 个不同来源类别

### peer_clusters.json

适合填入的事实：
- 谁是直接竞争者
- 为什么纳入
- 为什么排除

推荐判定维度：
- 同价格带
- 同技术路线
- 同地理市场
- 同价值链层级
- 同客户群

填充规则：
- `inclusion_reason` 需要可验证
- `excluded` 不是随手写，必须说清“不是同层竞争”还是“重叠太弱”
- 如果 peer 是未上市品牌，尽量写到映射的上市主体

### claims.json

适合填入的事实：
- 成本优势
- 技术优势
- 客户与品牌壁垒
- 海外与监管压力
- 资本效率与供应链约束

填充规则：
- 每条 high severity claim 至少 2 条 supporting evidence
- 至少 1 条 supporting evidence 来自 `Tier 1`
- `counter_evidence` 不应为空，除非该 claim 明显是低争议事实
- 遇到以下类型时默认降级为 `tentative`，除非有硬证据：
  - BOM 低多少
  - 自供率多少
  - 用户满意度排名
  - 海外销量目标与落地节奏

### verdict.json

适合填入的内容：
- position
- moat_strength
- moat_trend
- premium / discount view

填充规则：
- verdict 只能综合 claims，不单独引入新事实
- 关键风险必须在 claims 或 market_map 中找到来源
- 如果核心 claim 仍是 `tentative`，则 verdict `confidence` 不应偏高

## 推荐的来源字段

当前 contract 还没把来源字段做成硬约束，但生成时建议保留以下信息：

- `source`
- `source_url`
- `source_type`
- `as_of_date`
- `retrieved_at`
- `source_tier`
- `is_inferred`
- `note`

## 适用于比亚迪这类案例的高价值来源

- BYD 官方年报与新闻稿：销量、研发、海外布局、产品发布
- 欧盟委员会：关税、反补贴、价格承诺谈判进展
- 乘联会 / 中汽协：销量、出口、份额
- peer 年报：毛利率、研发、资本开支、海外收入

## 最小可用标准

四个 JSON 里，只要出现时间敏感数字，就至少回答下面四个问题：

1. 这个数是谁说的？
2. 原始日期是什么？
3. 是披露值、统计值，还是估算值？
4. 如果明天重跑，这个数有没有较大概率变化？
