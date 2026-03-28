# Tasks: Valuation Plugin Improvements

## Task List

- [ ] 1. 数据源 Commands 改为 LLM 指令模式（P1）
  - [ ] 1.1 重写 `finnhub-quote.md`：移除脚本引用，改为 LLM 指令风格，包含环境变量、API endpoint、期望返回字段
  - [ ] 1.2 重写 `fmp-quote.md`：移除脚本引用，改为 LLM 指令风格
  - [ ] 1.3 重写 `alphavantage-quote.md`：移除脚本引用，改为 LLM 指令风格
  - [ ] 1.4 重写 `tiingo-eod.md`：移除脚本引用，改为 LLM 指令风格
  - [ ] 1.5 重写 `eulerpool-income-statement.md`：移除脚本引用，改为 LLM 指令风格
  - [ ] 1.6 重写 `massive-agg-bars.md`：移除脚本引用，改为 LLM 指令风格
  - [ ] 1.7 重写 `test-data-sources.md`：改为 LLM 指令风格，描述通过 query_data plugin 验证各 provider 可达性

- [ ] 2. 补充单元测试（P1）
  - [ ] 2.1 新增 `test_auto_valuation.py` 文件，配置 pytest fixture 加载 `sample_input.json`
  - [ ] 2.2 实现 `test_dcf_basic`：验证 PV 计算（含 mid-year）与手算一致，误差 < 0.01%
  - [ ] 2.3 实现 `test_nwc_delta`：验证 NWC 使用变化量，稳定增长场景下 FCF 高于旧逻辑
  - [ ] 2.4 实现 `test_terminal_value_share`：验证 terminal_share > 0.75 时触发 warning
  - [ ] 2.5 实现 `test_comps_ev_vs_equity`：验证 ev_ebitda 走 EV bridge，pe 不走
  - [ ] 2.6 实现 `test_normalize_inputs_qoe`：验证 QoE 调整后 normalized_ebit 正确
  - [ ] 2.7 实现 `test_irr_high_growth`：验证 IRR > 100% 场景正常返回数值
  - [ ] 2.8 实现 `test_safe_ratio_near_zero`：验证 denominator 为 1e-11 时返回 None

- [ ] 3. industry-models.md 文档与代码对齐（P1）
  - [ ] 3.1 在 `industry-models.md` 中新增"实现状态"表格，标注已实现模型（✅）和 LLM 辅助模型（🔲）

- [ ] 4. model-weighting.md 补全扩展场景（P2）
  - [ ] 4.1 在 `model-weighting.md` 中新增 SOTP、REITs、Pre-revenue、银行、地产开发商、受监管公用事业六个场景的权重方案
  - [ ] 4.2 新增优先级规则：`industry_model` 字段存在时 `calc_industry_model` 输出权重优先

- [ ] 5. A 类 Skills 补充 Examples（P2）
  - [ ] 5.1 为 `scenario-modeling` 新增 `examples/sample_input.json` 和 `examples/sample_output.json`
  - [ ] 5.2 为 `ev-equity-bridge` 新增 `examples/sample_input.json` 和 `examples/sample_output.json`
  - [ ] 5.3 为 `resource-valuation` 新增 `examples/sample_input.json` 和 `examples/sample_output.json`
  - [ ] 5.4 为 `project-finance` 新增 `examples/sample_input.json` 和 `examples/sample_output.json`
  - [ ] 5.5 为 `quality-control` 新增 `examples/sample_input.json` 和 `examples/sample_output.json`

- [ ] 6. B 类 Skills 新增独立脚本（P2）
  - [ ] 6.1 新增 `peer-analysis/scripts/build_comps.py`：实现 peer list 输入、multiples 计算、summary stats（median/P25/P75）、implied range 输出
  - [ ] 6.2 新增 `vc-startup-model/scripts/vc_model.py`：实现 VC Method（pre/post money）和 First Chicago（场景加权）计算

- [ ] 7. cn-data-source 补充结构化路由（P2）
  - [ ] 7.1 在 `cn-data-source/SKILL.md` 中新增"Provider 路由决策树"章节（三层判断：理杏仁 → AkShare → query_data → 数据缺口）
  - [ ] 7.2 新增 `cn-data-source/references/field-provider-map.md`，列出高频估值字段的推荐 provider 和查询入口

- [ ] 8. 路径引用统一与基础设施（P2）
  - [ ] 8.1 在 `.gitignore` 中新增 valuation plugin 输出目录条目
  - [ ] 8.2 新增 `.claude/plugins/valuation/ENV_SETUP.md`，说明 6 个数据源的环境变量配置和 A 股默认路径

- [ ] 9. 端到端回归验证脚本（P3）
  - [ ] 9.1 新增 `company-valuation/scripts/validate_sample.py`：读取 sample_input.json，运行核心计算，与 valuation_summary.json 关键字段做 diff（容差 ±1%）
  - [ ] 9.2 将 `validate_sample.py` 追加到 `regression_tests/run_tests.sh`

- [ ] 10. calc_industry_model 扩展（P3）
  - [ ] 10.1 在 `auto_valuation.py` 中新增 `calc_reit_model`：实现 P/FFO 估值和 NAV 估值
  - [ ] 10.2 在 `auto_valuation.py` 中新增 `calc_saas_model`：实现 EV/ARR 估值
  - [ ] 10.3 更新 `calc_industry_model` dispatch 逻辑，新增 `reit` 和 `saas` 路由
  - [ ] 10.4 更新 `industry-models.md`，将 P/FFO 和 EV/ARR 状态从 🔲 更新为 ✅
