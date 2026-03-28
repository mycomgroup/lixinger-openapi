# Valuation Plugin 改进设计

> 本文档覆盖分析报告中尚未修复的设计层面问题（P1~P3 及结构性问题）。
> P0 代码 bug（NWC 变化量、mid-year convention、IRR 范围、浮点比较）已在 `auto_valuation.py` 中直接修复。

---

## 一、数据源 Commands 清理（P1）

### 问题

7 个 command（`finnhub-quote`、`fmp-quote`、`alphavantage-quote`、`tiingo-eod`、`eulerpool-income-statement`、`massive-agg-bars`、`test-data-sources`）引用了 `tools/data_sources/test_data_sources.py`，该路径在插件目录下不存在，命令无法执行。

### 设计方案

**方案 A（推荐）：改为 LLM 执行模式**

将这些 command 改为纯 LLM 指令风格，不依赖本地脚本。每个 command 描述：
- 需要的环境变量
- 调用的 API endpoint 和参数
- 期望的返回字段

Claude 直接通过 `query_data` plugin 的现有工具执行，无需本地脚本。

**方案 B：补充脚本**

在 `.claude/plugins/valuation/tools/data_sources/` 下创建 `test_data_sources.py`，实现各 provider 的 smoke test。

结构：
```
tools/
  data_sources/
    test_data_sources.py   # CLI: --source [finnhub|fmp|...] --symbol AAPL
    providers/
      finnhub.py
      fmp.py
      alphavantage.py
      tiingo.py
      eulerpool.py
      massive.py
```

**决策建议**：优先方案 A。这些 command 的实际使用场景是"在估值流程中补充数据"，而非独立运行脚本。改为 LLM 指令风格与 `cn-data-source` 的设计哲学一致，维护成本更低。

---

## 二、单元测试（P1）

### 问题

`auto_valuation.py` 约 1500 行，是精度敏感的计算引擎，但没有任何测试。

### 设计方案

在 `skills/company-valuation/scripts/` 下新增 `test_auto_valuation.py`，覆盖以下核心路径：

**必须覆盖（P1）**

| 测试用例 | 验证目标 |
|---|---|
| `test_dcf_basic` | 给定已知 FCF 序列，验证 PV 计算（含 mid-year）与手算一致 |
| `test_nwc_delta` | 验证 NWC 用变化量而非余额，FCF 在稳定增长时高于旧逻辑 |
| `test_terminal_value_share` | terminal_share > 0.75 时触发 warning |
| `test_comps_ev_vs_equity` | `ev_ebitda` 走 EV bridge，`pe` 不走 EV bridge |
| `test_normalize_inputs_qoe` | QoE 调整后 normalized_ebit 正确 |
| `test_irr_high_growth` | IRR > 100% 的场景能正常返回（验证搜索上限扩展） |
| `test_safe_ratio_near_zero` | denominator 为 1e-11 时返回 None |

**运行方式**

```bash
python -m pytest skills/company-valuation/scripts/test_auto_valuation.py -v
```

**参考 sample input**

使用 `skills/company-valuation/examples/` 下已有的 `sample_input.json` 作为 fixture，验证输出与 `valuation_summary.json` 的关键字段一致（回归测试）。

---

## 三、industry-models 文档与代码对齐（P1）

### 问题

`industry-models.md` 列出了 RAB DCF、EV/ARR、P/User、RNAV、P/FFO 等模型，但 `calc_industry_model` 只实现了 `financials`、`resource`、`project_finance` 三种。

### 设计方案

**短期（文档对齐代码）**：在 `industry-models.md` 中明确标注哪些模型已有脚本支持，哪些是"LLM 辅助执行"。

```markdown
## 实现状态

| 模型 | 状态 | 执行方式 |
|---|---|---|
| FCFF DCF | ✅ 已实现 | auto_valuation.py |
| Comps (EV/EBITDA, P/E 等) | ✅ 已实现 | auto_valuation.py |
| Financials (P/B + ROE, DDM) | ✅ 已实现 | calc_financials_model |
| Resource (NAV/rNPV) | ✅ 已实现 | calc_resource_model |
| Project Finance | ✅ 已实现 | calc_project_finance_model |
| EV/ARR, P/User (SaaS/平台) | 🔲 LLM 辅助 | vc-startup-model skill |
| RNAV (地产开发商) | 🔲 LLM 辅助 | 待实现 |
| P/FFO (REITs) | 🔲 LLM 辅助 | 待实现 |
| RAB DCF (受监管公用事业) | 🔲 LLM 辅助 | 待实现 |
```

**中期（扩展 calc_industry_model）**：按需补充 `calc_reit_model`、`calc_saas_model`，接入 `calc_industry_model` 的 dispatch。

优先级建议：REITs（P/FFO）> SaaS（EV/ARR）> RNAV > RAB DCF。

---

## 四、model-weighting.md 补全（P2）

### 问题

只覆盖 4 种场景，缺少 SOTP、REITs、pre-revenue 等。

### 设计方案

扩展 `model-weighting.md`，补充以下场景：

```markdown
## 扩展场景

- **SOTP（集团/多业务）**：各业务线独立估值后加总，不做跨业务线权重混合
- **REITs**：70% P/FFO，30% NAV（资产重置价值）
- **Pre-revenue / 早期**：100% VC Method 或 First Chicago，不使用 DCF
- **银行**：70% P/B + ROE，30% Residual Income；不使用 EV 类指标
- **地产开发商**：80% RNAV，20% P/E（基于结转利润）
- **受监管公用事业**：70% RAB DCF，30% EV/EBITDA
```

同时在 `model-weighting.md` 中增加一条规则：
> 当 `industry_model` 字段存在时，`calc_industry_model` 的输出权重优先于默认 DCF/comps 权重。

---

## 五、无脚本 Skills 的可执行层设计（P2）

### 问题

`peer-analysis`、`scenario-modeling`、`quality-control`、`ev-equity-bridge`、`resource-valuation`、`project-finance`、`vc-startup-model` 只有 SKILL.md，没有脚本或示例。

### 设计方案

分两类处理：

**A 类：已有 auto_valuation.py 函数支撑，补 examples 即可**

这些 skill 的计算逻辑已在 `auto_valuation.py` 中实现，只需补充 `examples/` 目录：

| Skill | 对应函数 | 需补充内容 |
|---|---|---|
| `scenario-modeling` | `calc_scenarios` | `sample_input.json` + `sample_output.json` |
| `ev-equity-bridge` | `ev_to_equity` | `sample_input.json` + `sample_output.json` |
| `resource-valuation` | `calc_resource_model` | `sample_input.json` + `sample_output.json` |
| `project-finance` | `calc_project_finance_model` | `sample_input.json` + `sample_output.json` |
| `quality-control` | `run_additional_qc` | `sample_input.json` + `sample_output.json` |

**B 类：需要独立脚本**

| Skill | 设计 |
|---|---|
| `peer-analysis` | 新增 `scripts/build_comps.py`，接受 peer list JSON，输出 multiples table 和 summary stats |
| `vc-startup-model` | 新增 `scripts/vc_model.py`，实现 VC Method + First Chicago 计算 |

`vc_model.py` 最小接口：
```python
# 输入：revenue/ARR, growth, exit_multiple, target_return, dilution
# 输出：pre_money, post_money, scenario_table, ownership_impact
```

---

## 六、cn-data-source 结构化路由（P2）

### 问题

`cn-data-source` SKILL.md 描述了"四件事"但没有可执行逻辑，完全依赖 Claude 自由发挥。

### 设计方案

不引入复杂路由脚本，而是在 SKILL.md 中补充一个**决策树**，让 Claude 有明确的执行路径：

```markdown
## Provider 路由决策树

1. 目标字段是否在理杏仁覆盖范围？
   - 是 → 使用 lixinger query_tool.py
   - 否 → 继续

2. 是否是现金流/宏观字段？
   - 是 → 使用 AkShare
   - 否 → 继续

3. 是否是美股/港股数据？
   - 是 → 按 query_data plugin 的 provider 文档选择
   - 否 → 标记为"数据缺口"，在 source_notes 中说明
```

同时在 `references/` 下补充 `field-provider-map.md`，列出高频字段的推荐 provider，避免每次重新判断。

---

## 七、路径引用统一（P2）

### 问题

`data-source-docs.md` command 中引用的脚本路径与实际路径不一致。

### 设计方案

统一约定：所有 command 中的路径引用使用**相对于仓库根目录**的路径，并在 README 中说明。

检查清单（需逐一核对）：
- `commands/data-source-docs.md` → 确认 `refresh_summary.py` 实际路径
- `commands/finnhub-quote.md` 等 → 按方案一改为 LLM 指令风格后路径问题自然消除

---

## 八、输出目录与 .gitignore（P2）

### 问题

运行后生成的输出文件可能被意外提交。

### 设计方案

在 `.gitignore` 中补充：

```gitignore
# Valuation plugin outputs
.claude/plugins/valuation/skills/*/outputs/
.claude/plugins/valuation/skills/*/examples/*/output_*.json
```

在 README 中说明：
> 运行时输出默认写入 `--outdir` 指定目录，建议使用项目根目录下的 `outputs/` 或临时目录，不要写入插件目录内。

---

## 九、API Key 配置文档（P2）

### 问题

6 个数据源依赖环境变量，但没有统一说明。

### 设计方案

在 `.claude/plugins/valuation/` 下新增 `ENV_SETUP.md`：

```markdown
# 环境变量配置

## 必需（使用对应 command 时）

| 变量名 | 用途 | 获取方式 |
|---|---|---|
| FINNHUB_API_KEY | finnhub-quote | finnhub.io 注册 |
| FMP_API_KEY | fmp-quote | financialmodelingprep.com |
| ALPHAVANTAGE_API_KEY | alphavantage-quote | alphavantage.co |
| TIINGO_API_KEY | tiingo-eod | tiingo.com |
| EULERPOOL_API_KEY | eulerpool-income-statement | eulerpool.com |
| MASSIVE_API_KEY | massive-agg-bars | 内部申请 |

## A 股默认路径（无需额外配置）

理杏仁 token 通过 `.claude/plugins/query_data/lixinger-api-docs/token.cfg` 读取。
AkShare 无需 API key。
```

---

## 十、端到端回归验证（P3）

### 问题

没有自动化验证脚本，代码改动可能无声地破坏计算结果。

### 设计方案

新增 `skills/company-valuation/scripts/validate_sample.py`：

```python
# 用法：python validate_sample.py
# 读取 examples/sample_input.json，运行 auto_valuation.py，
# 与 examples/valuation_summary.json 的关键字段做 diff
# 关键字段：enterprise_value, equity_value, terminal_share, implied_terminal_ev_ebitda
# 容差：±1%（浮点误差）
```

集成到 CI 或 regression_tests：

```bash
# regression_tests/run_tests.sh 中追加
python .claude/plugins/valuation/skills/company-valuation/scripts/validate_sample.py
```

---

## 实施优先级汇总

| 优先级 | 项目 | 工作量 |
|---|---|---|
| P1 | 数据源 commands 改为 LLM 指令风格 | 小（改 7 个 md 文件） |
| P1 | 补充单元测试 | 中（新增 ~200 行测试） |
| P1 | industry-models 文档标注实现状态 | 小（改 1 个 md 文件） |
| P2 | model-weighting 补全扩展场景 | 小 |
| P2 | A 类 skills 补 examples | 小（补 JSON 示例） |
| P2 | peer-analysis / vc-startup-model 补脚本 | 中 |
| P2 | cn-data-source 补决策树和 field-provider-map | 小 |
| P2 | 路径引用统一 + .gitignore + ENV_SETUP.md | 小 |
| P3 | 端到端回归验证脚本 | 小 |
| P3 | calc_industry_model 扩展（REITs、SaaS） | 大 |
