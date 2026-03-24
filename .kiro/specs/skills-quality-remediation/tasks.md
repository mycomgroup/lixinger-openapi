# Implementation Plan

- [x] 1. 编写 Bug Condition 探索性测试（修复前执行）
  - **Property 1: Bug Condition** - Skill 文档可执行性验证
  - **CRITICAL**: 此测试 MUST FAIL on unfixed code — 失败即确认 bug 存在
  - **DO NOT attempt to fix the test or the code when it fails**
  - **GOAL**: 通过实际执行暴露 5 类 bug 的具体反例
  - **Scoped PBT Approach**: 针对每类 bug 构造最小可复现用例
  - 测试 1.1 — 不存在 API：执行 `python .claude/skills/lixinger-data-query/scripts/query_tool.py --suffix "cn/company/esg" --token $TOKEN`，预期返回 `Api was not found`
  - 测试 1.2 — 点号路径：执行 `--suffix "cn.industry.fundamental.sw_2021"`，预期返回 `Api was not found`
  - 测试 1.3 — 参数冲突：调用 `cn/index/constituents` 时传入 `indexCode` 参数，预期返回 `ValidationError: "stockCodes" is required`
  - 测试 1.4 — 跨市场污染：grep 检查 `US-market_us-dividend-aristocrat-calculator/references/data-queries.md` 是否含 `cn/` 路径，预期命中
  - 测试 1.5 — TODO 残留：grep 检查 `China-market_macro-liquidity-monitor/references/methodology.md` 是否含 `[TODO]`，预期命中
  - 运行测试，记录所有反例（counterexamples）
  - **EXPECTED OUTCOME**: 所有测试 FAIL（证明 bug 存在）
  - 任务完成条件：测试已编写、已运行、失败已记录
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.9_

- [x] 2. 编写 Preservation 保留性测试（修复前执行）
  - **Property 2: Preservation** - 已验证 Skill 不受影响
  - **IMPORTANT**: 遵循 observation-first 方法论 — 先在未修复代码上观察，再写断言
  - 观察：`China-market_single-stock-health-check/references/data-queries.md` 当前内容（记录 checksum 或关键行）
  - 观察：`China-market_financial-statement-analyzer` 相关文档当前内容
  - 观察：`analysis-market/analysis-best-practices.md` 中 `metricsList`、`.mcw` 后缀等规则当前内容
  - 观察：`US-market_us-financial-statement-analyzer` 等未污染美股 Skill 的当前内容
  - 编写属性测试：对所有 `NOT isBugCondition(X)` 的文档，修复前后内容应完全相同
  - 具体检查：`grep -r "cn\." .claude/skills/China-market_single-stock-health-check/` 应无命中（确认该 Skill 本身无点号路径）
  - 具体检查：`grep "stockCodes\|metricsList\|\.mcw" .claude/skills/analysis-market/analysis-best-practices.md` 应命中（确认规则存在）
  - 运行测试，确认在未修复代码上 PASS
  - **EXPECTED OUTCOME**: 所有测试 PASS（确认基线行为）
  - 任务完成条件：测试已编写、已运行、在未修复代码上通过
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 3. Layer 0 — 真值文档确认

  - [ ] 3.1 确认 api_new/api-docs/ 中存在的 API 路径清单
    - 文件命名规则：`{market}_{path_segment1}_{path_segment2}...md`，其中 `non_financial`、`sw_2021`、`mm_ha`、`tr_dri` 等带下划线的词是单个路径段，不拆分
    - 已确认以下文件存在（对应 API 路径）：
      - `cn_industry_fundamental_sw_2021.md` → `cn/industry/fundamental/sw_2021` ✓
      - `cn_industry.md` → `cn/industry` ✓
      - `cn_index_constituents.md` → `cn/index/constituents` ✓
      - `cn_company_fundamental_non_financial.md` → `cn/company/fundamental/non_financial` ✓
      - `cn_company_dividend.md` → `cn/company/dividend` ✓
      - `cn_company_majority-shareholders.md` → `cn/company/majority-shareholders` ✓
      - `cn_company_measures.md` → `cn/company/measures` ✓
      - `cn_company_inquiry.md` → `cn/company/inquiry` ✓
    - 已确认以下文件不存在（对应 API 不可用）：
      - `cn_company_esg.md` 不存在 → `cn/company/esg` 不可用 ✓
      - `cn_company_governance.md` 不存在 → `cn/company/governance` 不可用 ✓
      - `cn_company_violation.md` 不存在 → `cn/company/violation` 不可用 ✓
      - `cn_industry_candlestick.md` 不存在 → `cn/industry/candlestick` 不可用（需在任务 6.2 中一并处理）✓
    - 已确认 `cn_index_constituents.md` 中参数名为 `stockCodes`（非 `indexCode`）✓
    - 此子任务已完成，无需执行额外操作
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 3.2 确认 AkShare 替代接口可用性
    - 确认 `api_new/akshare_data/` 中存在 `stock_esg_rate_sina` 或等效 ESG 接口文档
    - 确认 `stock_board_industry_fund_flow_rank_em` 接口文档存在（行业资金流向替代）
    - 记录各替代接口的调用参数和返回字段
    - _Requirements: 2.1, 2.2_

- [ ] 4. Layer 1 — 修复点号路径格式

  - [x] 4.1 修复 `lixinger-data-query/SKILL.md` 中的点号路径
    - 文件：`.claude/skills/lixinger-data-query/SKILL.md`
    - 将 `--suffix "cn.company"` → `--suffix "cn/company"`
    - 将 `--suffix "cn.index.constituents"` → `--suffix "cn/index/constituents"`
    - 全文 grep 确认无残留点号路径（`cn\.[a-z]` 模式）
    - _Bug_Condition: X 包含点号格式路径（匹配正则 `cn\.[a-z]`）_
    - _Expected_Behavior: 所有 `--suffix` 参数值使用斜杠格式_
    - _Preservation: lixinger-data-query 其他章节内容不变_
    - _Requirements: 2.5_

  - [x] 4.2 修复 `lixinger-data-query/LLM_USAGE_GUIDE.md` 中的点号路径
    - 文件：`.claude/skills/lixinger-data-query/LLM_USAGE_GUIDE.md`
    - grep 扫描所有点号路径（`cn\.[a-z]`、`hk\.[a-z]`、`us\.[a-z]`）
    - 将所有命中项替换为对应斜杠格式
    - _Bug_Condition: X 包含点号格式路径_
    - _Expected_Behavior: 所有路径使用斜杠格式_
    - _Requirements: 2.5_

  - [x] 4.3 修复 `China-market_sector-valuation-heat-map/references/data-queries.md` 中的点号路径
    - 文件：`.claude/skills/China-market_sector-valuation-heat-map/references/data-queries.md`
    - `cn.industry.fundamental.sw_2021` → `cn/industry/fundamental/sw_2021`
    - `cn.industry` → `cn/industry`
    - `cn.industry.candlestick` → `cn/industry/candlestick`
    - `cn/industry.candlestick`（混合格式）→ `cn/industry/candlestick`
    - `cn/industry.fundamental.sw_2021`（混合格式）→ `cn/industry/fundamental/sw_2021`
    - 全文 grep 确认无残留点号路径
    - _Bug_Condition: X 包含点号格式路径_
    - _Expected_Behavior: 所有路径使用斜杠格式_
    - _Requirements: 2.2, 2.5_

  - [x] 4.4 全量扫描其他 Skill 文档中的点号路径
    - 执行：`grep -r "cn\.[a-z]\|hk\.[a-z]\|us\.[a-z]" .claude/skills/ --include="*.md" -l`
    - 对每个命中文件，逐一替换点号路径为斜杠格式
    - 记录修复的文件列表
    - _Bug_Condition: X 包含点号格式路径_
    - _Expected_Behavior: 全量 Skill 文档无点号路径_
    - _Requirements: 2.5_

- [ ] 5. Layer 2 — 修复参数定义冲突

  - [x] 5.1 修复 `analysis-market/SKILL.md` 中 `cn/index/constituents` 参数名
    - 文件：`.claude/skills/analysis-market/SKILL.md`
    - 定位"A股常用 API"速查表中 `cn/index/constituents` 行
    - 将必需参数 `indexCode` → `stockCodes`
    - 确认修改后与 `api_new/api-docs/cn_index_constituents.md` 真值一致
    - 确认 SKILL.md 其他内容（项目文件夹规范、三级优先级规则）未被修改
    - _Bug_Condition: X 中参数名与真值文档不一致（`indexCode` vs `stockCodes`）_
    - _Expected_Behavior: 参数名为 `stockCodes`，与真值文档一致_
    - _Preservation: SKILL.md 其他章节内容不变_
    - _Requirements: 2.3, 3.3, 3.5_

- [ ] 6. Layer 3 — 修复不存在的 API 引用

  - [x] 6.1 修复 `China-market_esg-screener/references/data-queries.md`
    - 文件：`.claude/skills/China-market_esg-screener/references/data-queries.md`
    - 替换 `cn/company/esg`：标注"理杏仁 API 不提供 ESG 评分，可使用 AkShare `stock_esg_rate_sina` 接口获取新浪 ESG 评级"
    - 替换 `cn/company/finance`：改为 `cn/company/fundamental/non_financial`（PE、PB、ROE 等）
    - 替换 `cn/company/governance`：改为 `cn/company/majority-shareholders`（前十大股东）和 `cn/company/nolimit-shareholders`（前十大流通股东）
    - 替换 `cn/company/violation`：改为 `cn/company/measures`（监管措施）和 `cn/company/inquiry`（问询函）
    - 验证所有替换后的 API 路径在 `api_new/api-docs/` 中存在
    - _Bug_Condition: X 包含未在 api_new/api-docs/ 中存在的 API 路径_
    - _Expected_Behavior: 所有 API 路径可在真值文档中找到，不可用维度明确标注替代方案_
    - _Requirements: 2.1_

  - [x] 6.2 修复 `China-market_sector-valuation-heat-map/references/data-queries.md` 中的猜测型占位符
    - 文件：`.claude/skills/China-market_sector-valuation-heat-map/references/data-queries.md`
    - 定位 `Need to check for money flow specific API` 占位符
    - 替换为：明确说明理杏仁 API 当前不提供行业资金流向数据，可使用 AkShare `stock_board_industry_fund_flow_rank_em` 接口作为替代，或通过成分股成交量/价格变化推算
    - _Bug_Condition: X 包含猜测型占位符（`Need to check`）_
    - _Expected_Behavior: 无猜测型占位符，替代方案明确_
    - _Requirements: 2.2_

- [ ] 7. Layer 4 — 修复跨市场污染

  - [x] 7.1 修复 `US-market_us-dividend-aristocrat-calculator/references/data-queries.md`
    - 文件：`.claude/skills/US-market_us-dividend-aristocrat-calculator/references/data-queries.md`
    - 删除以下 A 股查询示例整块代码：
      - `cn/company/fundamental/non_financial`（含 `600519`、`000858`、`300750`）
      - `cn/company/dividend`（含 `600519`）
      - `cn/index/candlestick`（含 `000001`）
      - `cn/industry`（A 股行业数据）
    - 补充美股查询示例：
      - `us/company/fundamental/non_financial`（含 `AAPL`、`JNJ`、`KO` 示例）
      - `us/company/dividend`（含 `AAPL` 示例）
    - 保留已有的 `us/index/fundamental` 查询（不修改）
    - 更新"本 Skill 常用 API"列表：移除所有 `cn/` 前缀条目，替换为 `us/` 前缀
    - 全文 grep 确认无残留 `cn/` 路径和 A 股代码（`600519`、`000858`、`300750`、`000001`）
    - _Bug_Condition: US-market_* Skill 包含 `cn/` 前缀路径或 A 股代码_
    - _Expected_Behavior: 仅含 `us/` 前缀路径和美股代码示例_
    - _Preservation: `us/index/fundamental` 等已有美股查询不变_
    - _Requirements: 2.4, 3.4_

- [ ] 8. Layer 5 — 补全 TODO/Draft 内容

  - [x] 8.1 补全 `China-market_macro-liquidity-monitor/references/methodology.md`
    - 文件：`.claude/skills/China-market_macro-liquidity-monitor/references/methodology.md`
    - 读取当前文件，定位所有 `[TODO]` 占位符
    - 补全指标计算公式（M2 同比增速、社融存量增速、DR007 利率等）
    - 补全阈值来源和边界条件（参考历史数据区间，注明数据来源）
    - 确认补全后文件不含任何 `[TODO]` 字符串
    - _Bug_Condition: stable/partial Skill 文档含 `[TODO]` 占位符_
    - _Expected_Behavior: 方法论文档包含完整公式、阈值和边界条件_
    - _Requirements: 2.9_

  - [x] 8.2 补全 `China-market_event-study/references/methodology.md`
    - 文件：`.claude/skills/China-market_event-study/references/methodology.md`
    - 读取当前文件，定位所有 `[TODO]` 占位符
    - 补全事件研究方法论：事件窗口定义、正常收益估计模型、超额收益计算公式
    - 确认补全后文件不含任何 `[TODO]` 字符串
    - _Requirements: 2.9_

  - [x] 8.3 补全 `US-market_us-peer-comparison-analyzer/references/methodology.md`
    - 文件：`.claude/skills/US-market_us-peer-comparison-analyzer/references/methodology.md`
    - 读取当前文件，定位所有 `[TODO]` 占位符
    - 补全同业比较方法论：可比公司筛选标准、估值倍数计算、排名评分逻辑
    - 确认补全后文件不含任何 `[TODO]` 字符串
    - _Requirements: 2.9_

  - [x] 8.4 补全 `US-market_us-tax-aware-rebalancing-planner/references/methodology.md`
    - 文件：`.claude/skills/US-market_us-tax-aware-rebalancing-planner/references/methodology.md`
    - 读取当前文件，定位所有 `[TODO]` 占位符
    - 补全税务感知再平衡方法论：税损收割规则、wash-sale 规则、再平衡触发阈值
    - 确认补全后文件不含任何 `[TODO]` 字符串
    - _Requirements: 2.9_

  - [x] 8.5 补全高频主入口 Skill 的输出模板（按模板家族批量处理）
    - 读取 `docs/SKILLS_QUALITY_REMEDIATION_DESIGN.md` 中定义的模板家族分类
    - 对每个含空模板骨架的 `output-template.md`，补全：结论摘要、关键数据表、风险说明、下一步建议四个标准章节
    - 优先处理高频使用的主入口 Skill（参考 `analysis-market/SKILLS_MAP.md` 中的使用频率）
    - 确认所有处理文件不含 `[TODO]` 字符串
    - _Requirements: 2.9_

- [ ] 9. 数据源扩展架构 — 补充 `lixinger-data-query/SKILL.md` 新数据源接入规范

  - [x] 9.1 在 `lixinger-data-query/SKILL.md` 中添加新数据源接入规范章节
    - 文件：`.claude/skills/lixinger-data-query/SKILL.md`
    - 在文件末尾添加"新数据源接入规范"章节，内容包含：
      - 目录约定：`api_new/{datasource}_data/` 命名规范
      - 文档格式要求：与 `akshare_data/` 保持一致（接口名、输入参数、返回字段、调用示例）
      - 更新 `API_KEYWORD_INDEX.md` 的步骤
      - 更新 `analysis-market/SKILL.md` 三级优先级规则的步骤
      - 优先级插入原则（数据质量高 → 理杏仁之后；补充性 → AkShare 之后）
    - 确认新增章节不影响现有章节内容
    - _Requirements: 3.5_

- [ ] 10. Checkpoint — 验证所有修复正确且无回归

  - [x] 10.1 验证 Bug Condition 探索性测试现在通过
    - **Property 1: Expected Behavior** - Skill 文档可执行性验证
    - **IMPORTANT**: 重新运行任务 1 中的 SAME 测试，不要编写新测试
    - 重新执行任务 1 中的 5 个测试用例
    - 测试 1.1：`cn/company/esg` 查询应返回明确的"不支持"说明（文档已更新）
    - 测试 1.2：点号路径 grep 应无命中（所有文档已修复）
    - 测试 1.3：`cn/index/constituents` 文档中参数名应为 `stockCodes`
    - 测试 1.4：`US-market_us-dividend-aristocrat-calculator/references/data-queries.md` 中无 `cn/` 路径
    - 测试 1.5：`China-market_macro-liquidity-monitor/references/methodology.md` 中无 `[TODO]`
    - **EXPECTED OUTCOME**: 所有测试 PASS（确认 bug 已修复）
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.9_

  - [x] 10.2 验证 Preservation 保留性测试仍然通过
    - **Property 2: Preservation** - 已验证 Skill 不受影响
    - **IMPORTANT**: 重新运行任务 2 中的 SAME 测试，不要编写新测试
    - 确认 `China-market_single-stock-health-check/references/data-queries.md` 内容未变
    - 确认 `analysis-market/analysis-best-practices.md` 中 `metricsList`、`.mcw` 规则未变
    - 确认 `US-market_us-financial-statement-analyzer` 等未污染美股 Skill 文档未被修改
    - 确认 `analysis-market/SKILL.md` 的项目文件夹规范和三级优先级规则未变（仅 `indexCode` → `stockCodes` 一处修改）
    - **EXPECTED OUTCOME**: 所有测试 PASS（确认无回归）
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

  - [x] 10.3 全量验证 — 确认无残留 bug
    - 执行全量 grep：`grep -r "cn\.[a-z]\|hk\.[a-z]\|us\.[a-z]" .claude/skills/ --include="*.md"` 应无命中
    - 执行全量 grep：`grep -r "\[TODO\]" .claude/skills/ --include="*.md"` 对 stable/partial Skill 应无命中
    - 执行全量 grep：`grep -r "cn/" .claude/skills/US-market_*/references/ --include="*.md"` 应无命中
    - 如有遗漏，补充修复后重新运行
    - 确认所有测试通过，如有疑问请询问用户
