# Requirements: Valuation Plugin Improvements

## Introduction

本文档定义 Valuation Plugin 改进的功能需求，基于设计文档推导而来。改进目标是消除无效脚本引用、补充测试覆盖、对齐文档与代码、完善可执行层，并提供端到端回归验证能力。

---

## Requirements

### Requirement 1: 数据源 Commands 改为 LLM 指令模式（P1）

**User Story**: 作为使用 Valuation Plugin 的用户，我希望数据源 commands 能够正常执行，而不是因为引用不存在的脚本路径而失败。

#### Acceptance Criteria

1.1 `finnhub-quote.md` 不再引用 `tools/data_sources/test_data_sources.py`，改为描述通过 query_data plugin 执行的 LLM 指令。

1.2 `fmp-quote.md` 不再引用本地脚本，改为 LLM 指令风格，包含所需环境变量、API endpoint 和期望返回字段。

1.3 `alphavantage-quote.md` 不再引用本地脚本，改为 LLM 指令风格。

1.4 `tiingo-eod.md` 不再引用本地脚本，改为 LLM 指令风格。

1.5 `eulerpool-income-statement.md` 不再引用本地脚本，改为 LLM 指令风格。

1.6 `massive-agg-bars.md` 不再引用本地脚本，改为 LLM 指令风格。

1.7 `test-data-sources.md` 改为 LLM 指令风格，描述如何通过 query_data plugin 验证各 provider 可达性。

1.8 每个改写后的 command 必须包含：所需环境变量名称、API endpoint 说明、期望返回字段列表。

---

### Requirement 2: 单元测试覆盖（P1）

**User Story**: 作为维护 `auto_valuation.py` 的开发者，我希望有自动化测试来验证核心计算逻辑的正确性，防止改动引入静默错误。

#### Acceptance Criteria

2.1 在 `.claude/plugins/valuation/skills/company-valuation/scripts/` 下新增 `test_auto_valuation.py`。

2.2 `test_dcf_basic`：给定已知 FCF 序列和 WACC，验证 PV 计算结果（含 mid-year convention）与手工计算值一致，误差在 0.01% 以内。

2.3 `test_nwc_delta`：验证 NWC 计算使用变化量（delta）而非余额，在稳定增长场景下 FCF 高于使用余额的旧逻辑。

2.4 `test_terminal_value_share`：当 terminal value 占总 EV 比例超过 75% 时，函数触发 warning（通过 `warnings.warn` 或日志输出）。

2.5 `test_comps_ev_vs_equity`：`ev_ebitda` 倍数估值经过 EV-to-equity bridge 转换，`pe` 倍数估值不经过 EV bridge 直接得到 equity value。

2.6 `test_normalize_inputs_qoe`：给定 QoE（Quality of Earnings）调整项，`normalized_ebit` 等于原始 EBIT 加上调整项之和。

2.7 `test_irr_high_growth`：在高增长场景（预期 IRR > 100%）下，IRR 计算函数能正常返回数值而不报错或返回 None。

2.8 `test_safe_ratio_near_zero`：当除数为 1e-11（接近零）时，`safe_ratio` 函数返回 None 而非抛出异常或返回 inf。

2.9 测试可通过 `python -m pytest skills/company-valuation/scripts/test_auto_valuation.py -v` 运行，所有用例通过。

---

### Requirement 3: industry-models.md 文档与代码对齐（P1）

**User Story**: 作为使用 Valuation Plugin 的分析师，我希望 `industry-models.md` 清楚标注哪些模型有脚本支持、哪些需要 LLM 辅助执行，避免误用未实现的模型。

#### Acceptance Criteria

3.1 `industry-models.md` 新增"实现状态"表格，列出每个模型的状态（✅ 已实现 / 🔲 LLM 辅助）和执行方式。

3.2 已实现模型（FCFF DCF、Comps、Financials、Resource、Project Finance）标注为 ✅，并注明对应函数名。

3.3 未实现模型（EV/ARR、P/User、RNAV、P/FFO、RAB DCF）标注为 🔲 LLM 辅助，并注明对应 skill 或"待实现"。

3.4 文档中不再出现未标注实现状态的模型条目。

---

### Requirement 4: model-weighting.md 补全扩展场景（P2）

**User Story**: 作为使用 Valuation Plugin 的分析师，我希望 `model-weighting.md` 覆盖更多行业场景，在处理 REITs、银行、地产开发商等特殊行业时有明确的权重指导。

#### Acceptance Criteria

4.1 `model-weighting.md` 新增 SOTP（集团/多业务）场景：各业务线独立估值后加总，不做跨业务线权重混合。

4.2 新增 REITs 场景：70% P/FFO，30% NAV。

4.3 新增 Pre-revenue / 早期场景：100% VC Method 或 First Chicago，不使用 DCF。

4.4 新增银行场景：70% P/B + ROE，30% Residual Income；明确说明不使用 EV 类指标。

4.5 新增地产开发商场景：80% RNAV，20% P/E（基于结转利润）。

4.6 新增受监管公用事业场景：70% RAB DCF，30% EV/EBITDA。

4.7 新增优先级规则：当 `industry_model` 字段存在时，`calc_industry_model` 的输出权重优先于默认 DCF/comps 权重。

---

### Requirement 5: A 类 Skills 补充 Examples（P2）

**User Story**: 作为使用 Valuation Plugin 的用户，我希望每个 skill 都有可参考的输入输出示例，方便理解如何调用和预期结果格式。

#### Acceptance Criteria

5.1 `scenario-modeling` skill 下新增 `examples/sample_input.json` 和 `examples/sample_output.json`，示例对应 `calc_scenarios` 函数的输入输出。

5.2 `ev-equity-bridge` skill 下新增 `examples/sample_input.json` 和 `examples/sample_output.json`，示例对应 `ev_to_equity` 函数的输入输出。

5.3 `resource-valuation` skill 下新增 `examples/sample_input.json` 和 `examples/sample_output.json`，示例对应 `calc_resource_model` 函数的输入输出。

5.4 `project-finance` skill 下新增 `examples/sample_input.json` 和 `examples/sample_output.json`，示例对应 `calc_project_finance_model` 函数的输入输出。

5.5 `quality-control` skill 下新增 `examples/sample_input.json` 和 `examples/sample_output.json`，示例对应 `run_additional_qc` 函数的输入输出。

5.6 所有示例 JSON 文件格式合法，字段与 `auto_valuation.py` 实际接口一致。

---

### Requirement 6: B 类 Skills 新增独立脚本（P2）

**User Story**: 作为使用 Valuation Plugin 的分析师，我希望 `peer-analysis` 和 `vc-startup-model` 有可执行脚本，能够直接运行计算而不完全依赖 LLM 自由发挥。

#### Acceptance Criteria

6.1 在 `.claude/plugins/valuation/skills/peer-analysis/scripts/` 下新增 `build_comps.py`。

6.2 `build_comps.py` 接受 peer list JSON 和 target company metrics 作为输入，输出 multiples table、summary stats（median、P25、P75）和 implied valuation range。

6.3 `build_comps.py` 支持 LTM 和 NTM 两种 period basis，默认 LTM。

6.4 当某个 peer 的倍数分母为负数或接近零时，该倍数标记为 N/M 并从统计中排除。

6.5 在 `.claude/plugins/valuation/skills/vc-startup-model/scripts/` 下新增 `vc_model.py`。

6.6 `vc_model.py` 实现 VC Method：给定 revenue/ARR、growth、exit_multiple、target_return、dilution，计算 pre_money 和 post_money。

6.7 `vc_model.py` 实现 First Chicago：给定多个场景（name、prob、exit_value），计算加权 pre_money 和 post_money，场景概率之和必须等于 1。

6.8 `vc_model.py` 输出包含 scenario_table 和 ownership_impact。

---

### Requirement 7: cn-data-source 补充结构化路由（P2）

**User Story**: 作为使用 cn-data-source skill 的用户，我希望有明确的 provider 路由决策树，减少每次选择 provider 时的不确定性。

#### Acceptance Criteria

7.1 `cn-data-source/SKILL.md` 新增"Provider 路由决策树"章节，包含三层判断逻辑：理杏仁覆盖 → AkShare → query_data plugin → 数据缺口。

7.2 在 `.claude/plugins/valuation/skills/cn-data-source/references/` 下新增 `field-provider-map.md`，列出高频估值字段（revenue、ebitda、ebit、net_income、capex、nwc、cash、debt、current_price）的推荐 provider。

7.3 `field-provider-map.md` 对每个字段注明：provider 名称、查询入口、字段名/API 后缀、注意事项。

---

### Requirement 8: 路径引用统一与基础设施（P2）

**User Story**: 作为维护 Valuation Plugin 的开发者，我希望所有路径引用统一、输出目录不被意外提交、API key 配置有文档说明。

#### Acceptance Criteria

8.1 所有 command 文件中的路径引用使用相对于仓库根目录的路径（在 Requirement 1 完成后，数据源 commands 的路径问题自然消除）。

8.2 `.gitignore` 新增以下条目：
```
.claude/plugins/valuation/skills/*/outputs/
.claude/plugins/valuation/skills/*/examples/*/output_*.json
```

8.3 在 `.claude/plugins/valuation/` 下新增 `ENV_SETUP.md`，列出 6 个数据源的环境变量名称（`FINNHUB_API_KEY`、`FMP_API_KEY`、`ALPHAVANTAGE_API_KEY`、`TIINGO_API_KEY`、`EULERPOOL_API_KEY`、`MASSIVE_API_KEY`）、用途和获取方式。

8.4 `ENV_SETUP.md` 说明 A 股默认路径（理杏仁 token 通过 `token.cfg` 读取，AkShare 无需 API key）。

---

### Requirement 9: 端到端回归验证脚本（P3）

**User Story**: 作为维护 `auto_valuation.py` 的开发者，我希望有自动化脚本验证代码改动不会静默破坏计算结果，可集成到 CI 流程。

#### Acceptance Criteria

9.1 在 `.claude/plugins/valuation/skills/company-valuation/scripts/` 下新增 `validate_sample.py`。

9.2 脚本读取 `examples/sample_input.json`，运行 `auto_valuation.py` 的核心计算流程，与 `examples/valuation_summary.json` 的关键字段做对比。

9.3 验证字段包括：`enterprise_value`、`equity_value`、`terminal_share`、`implied_terminal_ev_ebitda`。

9.4 容差为 ±1%（浮点误差范围）。

9.5 所有字段在容差内时，脚本以 exit code 0 退出；任意字段超出容差时，输出详细 diff 并以非零 exit code 退出。

9.6 脚本可追加到 `regression_tests/run_tests.sh` 中作为回归测试的一部分运行。

---

### Requirement 10: calc_industry_model 扩展（P3）

**User Story**: 作为使用 Valuation Plugin 的分析师，我希望 REITs 和 SaaS 公司的行业特定模型有脚本支持，不完全依赖 LLM 辅助执行。

#### Acceptance Criteria

10.1 在 `auto_valuation.py` 中新增 `calc_reit_model` 函数，实现 P/FFO 估值：给定 FFO、P/FFO 倍数范围，输出 equity value range。

10.2 `calc_reit_model` 同时支持 NAV 估值：给定资产重置价值和负债，输出 NAV per share。

10.3 在 `auto_valuation.py` 中新增 `calc_saas_model` 函数，实现 EV/ARR 估值：给定 ARR、EV/ARR 倍数范围，输出 EV range。

10.4 `calc_industry_model` 的 dispatch 逻辑新增对 `reit` 和 `saas` 类型的路由，分别调用 `calc_reit_model` 和 `calc_saas_model`。

10.5 `industry-models.md` 中 P/FFO（REITs）和 EV/ARR（SaaS）的状态从 🔲 LLM 辅助更新为 ✅ 已实现。
