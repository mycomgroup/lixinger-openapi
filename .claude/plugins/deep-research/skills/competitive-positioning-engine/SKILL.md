# Competitive Positioning Engine (CPE) — Evidence-First MVP

description: 竞争格局引擎：定义比较空间、重构 peer clusters、沉淀 market map / claims / verdict 的结构化输出。当前执行口径为 evidence-first：先获取最新可验证证据，再做推断并产出结论；无可验证新数据时必须降级（`tentative`/`null`），不得用模型记忆补数。触发词：竞争格局、护城河、peer 比较、市场地位、竞争优势、CPE。

## 目标与范围（Phase 2 预备）

- 先把输出契约与 case 目录结构稳定跑通（evidence-first）
- 允许研究员手工校正 peer list 与 claims 证据
- 不追求一步自动评分，先保证"证据链结构正确、主张可追溯"
- 第一个真实行业样例：动力电池（宁德时代 300750）

## 当前执行口径（硬约束）

按 `web-grounded evidence-first` 执行。

核心不是多写观点，而是要求生成 `market_map.json / peer_clusters.json / claims.json / verdict.json` 时，先联网搜集并标注来源，再做推断。没有可验证来源的数字，宁可留空、降级为定性描述，或把 status 标为 `tentative`，不要伪装成已确认事实。

推荐执行顺序：

1. 先用本地结构化数据源补定量底座
   - 理杏仁：公司财务、估值、peer 年报对比
   - AkShare：补充销量、行情、宏观、部分行业数据
2. 再用网页搜索补半结构化与监管证据
   - 公司官网 / 年报 / 新闻稿 / 产品发布
   - 监管机构 / 行业协会 / 交易所 / 海关 / 欧盟委员会
   - 高质量行业媒体仅用于补背景，不作为唯一硬证据
3. 最后才生成四个 JSON
   - 事实层：带来源和日期
   - 推断层：明确 `is_inferred`
   - 结论层：写入 verdict

## 输出契约（对齐 references/cpe-output-contract.json）

四个文件构成一个完整 `competitive_positioning/` 目录：

### market_map.json
- 市场定义（scope、地理范围、价值链位置）
- 细分市场（id、规模、CAGR、集中度、关键玩家）
- 整体集中度（CR3/CR5/HHI）

### peer_clusters.json
- 按竞争层次分组的 peer 列表（中国一线 / 全球一线 / 细分专项）
- 每个 peer 的纳入理由、关键相似点、关键差异点
- 排除列表（含排除理由）

### claims.json
- 竞争主张列表，维度覆盖：scale / technology / cost / customer / brand / supply_chain / regulation / capital
- 每条主张：direction（advantage/disadvantage/neutral）、severity、supporting_evidence、counter_evidence、confidence、status
- status 取值：confirmed / tentative / disputed / stale

### verdict.json
- position（leader / challenger / niche / follower）
- moat_assessment（moat_type、moat_strength、moat_trend、rationale）
- premium_discount_view（direction、key_drivers、key_risks）
- confidence、key_uncertainties、summary

补充要求（当前即硬约束）：

- `market_map.json` 的集中度、市场规模、CAGR，优先来自行业协会/监管/公司年报；无可靠来源时允许为 `null`
- `peer_clusters.json` 的纳入理由必须基于可验证事实，例如销量排名、价格带重叠、地理市场重叠、技术路线重叠
- `claims.json` 的每条高 severity 主张，至少 2 条 supporting evidence，且至少 1 条来自官方或监管来源
- `verdict.json` 只能综合已被证据支持的 claims，不应直接引入未在 claims 中出现的新数字

## 真实样例：宁德时代（300750）动力电池

路径：`examples/catl_300750/`

核心结论（截至 2025-12-31）：
- position: leader，moat_strength: wide，moat_trend: **narrowing**
- 三重护城河：规模（全球 37% 份额）+ 技术（专利 19000+）+ 客户（覆盖全球前 20 大整车厂中 16 家）
- 三重压力：比亚迪国内追赶 + 欧美贸易壁垒 + 储能价格战
- 核心不确定性：固态电池技术路线切换窗口（2028-2032）

claims 覆盖 8 条主张（5 个 advantage、3 个 disadvantage），confidence 范围 0.62-0.88。

## 使用方式

### 手工创建新 case

1. 在 `research_cases/case_YYYYMMDD_company/competitive_positioning/` 下创建四个文件
2. 参考 `examples/catl_300750/` 的结构和字段
3. 用 `deep-research-qa` 做 QA（应检查证据来源、日期与降级标记是否完整）

### 联网取证工作流（必走）

生成四个文件时，按下面的取证顺序走：

#### 1. market_map.json

- 市场定义：优先看公司年报的业务分部口径，再看行业协会/监管口径
- 市场规模与集中度：优先用乘联会/中汽协/SNE Research/海关/欧盟委员会等来源
- `data_sources` 应写明来源名称、绝对日期、为何使用

#### 2. peer_clusters.json

- 先确定比较维度：价格带、技术路线、地理市场、价值链位置
- 再用销量榜、产品矩阵、海外布局、品牌定位去筛 peer
- `inclusion_reason` 不应只是常识判断，最好能落到一条可查事实

#### 3. claims.json

- 每条 claim 拆成事实片段，不要一口气塞进长句
- 数字型主张优先用结构化源或官方披露
- 监管型主张优先用官方公告
- 如果是分析推断，例如 “BOM 低 15-20%”，必须明确是研究估算，不要写成公司已披露事实

#### 4. verdict.json

- 只在 claims 足够覆盖后再写结论
- `moat_strength` 与 `moat_trend` 必须能回指到 claims
- `premium_discount_view` 里的 driver/risk 应来自 claims，不要额外发明结论

详见 `references/web-grounded-sourcing-playbook.md`。

### 与 FQE 集成

CPE 的 `verdict.json` 中的 `premium_discount_view` 应与 FQE 的 `verdict.json` 中的 `grade` 和 `scores` 联合解读：
- FQE grade A/B + CPE position leader → 支持估值溢价
- FQE grade C/D + CPE moat_trend narrowing → 估值折价信号

## 下一步（Phase 2 自动化方向）

- 从理杏仁 API 拉取 peer 财务数据，自动生成定量 claims（毛利率对比、ROE 对比等）
- 基于 market_map 的集中度数据自动触发竞争格局红旗
- QA 脚本加入 CPE 检查项（claims 是否有 supporting_evidence、verdict 字段完整性）
- QA 脚本新增来源质量检查：是否有官方/监管来源、是否写明绝对日期、是否把估算与事实混写
