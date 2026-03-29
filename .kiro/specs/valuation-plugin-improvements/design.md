# Design Document: Valuation Plugin Improvements

## Overview

本文档描述 Valuation Plugin 的系统性改进方案，涵盖单元测试补充、文档与代码对齐、无脚本 skills 可执行层建设、以及端到端回归验证等方面。P0 级代码 bug（NWC 变化量、mid-year convention、IRR 范围、浮点比较）已在 `auto_valuation.py` 中直接修复，本文档聚焦 P1~P3 的设计层面改进。

数据源 commands 改写（原 Requirement 1）和 cn-data-source 结构化路由（原 Requirement 7）已从范围中移除。

改进目标：提升插件的可靠性（测试覆盖）、可维护性（文档与代码对齐）、可执行性（补全脚本）、以及可发现性（补全文档与示例）。

## Architecture

```
Skills Layer
  company-valuation/
    scripts/
      auto_valuation.py        (已有，P0 bug 已修复)
      test_auto_valuation.py   (新增，Req 1)
      validate_sample.py       (新增，Req 7)
    references/
      industry-models.md       (更新，Req 2 + Req 8)
      model-weighting.md       (更新，Req 3)
    examples/                  (已有)

  peer-analysis/
    scripts/
      build_comps.py           (新增，Req 5)

  vc-startup-model/
    scripts/
      vc_model.py              (新增，Req 5)

  scenario-modeling/
    examples/                  (新增，Req 4)

  ev-equity-bridge/
    examples/                  (新增，Req 4)

  resource-valuation/
    examples/                  (新增，Req 4)

  project-finance/
    examples/                  (新增，Req 4)

  quality-control/
    examples/                  (新增，Req 4)

Plugin Root
  ENV_SETUP.md                 (新增，Req 6)

Repo Root
  .gitignore                   (更新，Req 6)
  regression_tests/run_tests.sh (更新，Req 7)
```

## Components and Interfaces

### Component 1: 单元测试（test_auto_valuation.py）

**Purpose**: 为 `auto_valuation.py` 这个精度敏感的计算引擎提供测试覆盖。

**文件路径**: `.claude/plugins/valuation/skills/company-valuation/scripts/test_auto_valuation.py`

**测试结构**:

```python
class TestDCFCalculation:
    def test_dcf_basic(self): ...           # PV 计算含 mid-year 与手算一致
    def test_nwc_delta(self): ...           # NWC 用变化量而非余额
    def test_terminal_value_share(self): ...  # terminal_share > 0.75 触发 warning

class TestCompsValuation:
    def test_comps_ev_vs_equity(self): ...  # ev_ebitda 走 EV bridge，pe 不走

class TestInputNormalization:
    def test_normalize_inputs_qoe(self): ...  # QoE 调整后 normalized_ebit 正确

class TestEdgeCases:
    def test_irr_high_growth(self): ...     # IRR > 100% 场景正常返回
    def test_safe_ratio_near_zero(self): ...  # denominator 为 1e-11 返回 None
```

**Responsibilities**:
- 覆盖 DCF 核心计算路径（含 mid-year convention）
- 覆盖 NWC 变化量逻辑
- 覆盖 comps EV bridge 路径分叉
- 覆盖边界条件（IRR 上限、浮点安全除法）

---

### Component 2: industry-models.md 实现状态标注

**Purpose**: 消除文档列出模型与代码实际实现之间的歧义。

**文件路径**: `.claude/plugins/valuation/skills/company-valuation/references/industry-models.md`

**新增实现状态表**:

```markdown
## 实现状态

| 模型 | 状态 | 执行方式 |
|---|---|---|
| FCFF DCF | ✅ 已实现 | auto_valuation.py / calc_dcf |
| Comps (EV/EBITDA, P/E 等) | ✅ 已实现 | auto_valuation.py / calc_comps |
| Financials (P/B + ROE, DDM) | ✅ 已实现 | auto_valuation.py / calc_financials_model |
| Resource (NAV/rNPV) | ✅ 已实现 | auto_valuation.py / calc_resource_model |
| Project Finance | ✅ 已实现 | auto_valuation.py / calc_project_finance_model |
| EV/ARR, P/User (SaaS/平台) | 🔲 LLM 辅助 | vc-startup-model skill |
| RNAV (地产开发商) | 🔲 LLM 辅助 | 待实现 |
| P/FFO (REITs) | 🔲 LLM 辅助 | 待实现 |
| RAB DCF (受监管公用事业) | 🔲 LLM 辅助 | 待实现 |
```

Req 8 完成后，P/FFO 和 EV/ARR 状态更新为 ✅。

---

### Component 3: model-weighting.md 扩展

**Purpose**: 补全缺失的行业场景权重指导。

**文件路径**: `.claude/plugins/valuation/skills/company-valuation/references/model-weighting.md`

**新增内容**:

```markdown
## 扩展场景

| 场景 | 权重方案 |
|---|---|
| SOTP（集团/多业务） | 各业务线独立估值后加总，不做跨业务线权重混合 |
| REITs | 70% P/FFO，30% NAV（资产重置价值） |
| Pre-revenue / 早期 | 100% VC Method 或 First Chicago，不使用 DCF |
| 银行 | 70% P/B + ROE，30% Residual Income；不使用 EV 类指标 |
| 地产开发商 | 80% RNAV，20% P/E（基于结转利润） |
| 受监管公用事业 | 70% RAB DCF，30% EV/EBITDA |

## 优先级规则
当 `industry_model` 字段存在时，`calc_industry_model` 的输出权重优先于默认 DCF/comps 权重。
```

---

### Component 4: A 类 Skills 补充 Examples

**Purpose**: 为已有 `auto_valuation.py` 函数支撑的 skills 补充可执行示例。

**受影响 Skills**:

| Skill | 对应函数 | 补充内容 |
|---|---|---|
| `scenario-modeling` | `calc_scenarios` | `examples/sample_input.json` + `examples/sample_output.json` |
| `ev-equity-bridge` | `ev_to_equity` | `examples/sample_input.json` + `examples/sample_output.json` |
| `resource-valuation` | `calc_resource_model` | `examples/sample_input.json` + `examples/sample_output.json` |
| `project-finance` | `calc_project_finance_model` | `examples/sample_input.json` + `examples/sample_output.json` |
| `quality-control` | `run_additional_qc` | `examples/sample_input.json` + `examples/sample_output.json` |

示例 JSON 字段必须与 `auto_valuation.py` 实际接口一致，可从 `company-valuation/examples/sample_input.json` 中裁剪对应字段。

---

### Component 5: B 类 Skills 新增脚本

**Purpose**: 为 `peer-analysis` 和 `vc-startup-model` 补充独立计算脚本。

#### build_comps.py

**文件路径**: `.claude/plugins/valuation/skills/peer-analysis/scripts/build_comps.py`

```python
def build_comps(
    peers: list[dict],          # [{ticker, ev, ebitda, net_income, book_value, ...}]
    target: dict,               # {ebitda, net_income, book_value, ...}
    multiples: list[str],       # e.g. ["ev_ebitda", "pe", "pb"]
    period_basis: str = "LTM"   # "LTM" or "NTM"
) -> dict:
    # 返回: multiples_table, summary_stats, implied_range
```

- 分母为负数或 abs < 1e-10 时，该倍数标记为 N/M，排除出统计
- summary_stats 包含 median、p25、p75、count（仅计 valid 条目）
- implied_range 用 p25~p75 区间乘以 target 对应指标

#### vc_model.py

**文件路径**: `.claude/plugins/valuation/skills/vc-startup-model/scripts/vc_model.py`

```python
def calc_vc_method(
    revenue_or_arr: float,
    growth_rate: float,
    exit_multiple: float,
    target_return: float,
    dilution: float,
    exit_year: int
) -> dict:
    # 返回: pre_money, post_money, ownership_impact

def calc_first_chicago(
    scenarios: list[dict],  # [{name, prob, exit_value}]
    target_return: float,
    dilution: float
) -> dict:
    # 场景概率之和必须等于 1，否则抛出 ValueError
    # 返回: scenario_table, weighted_pre_money, weighted_post_money
```

---

### Component 6: 基础设施

**ENV_SETUP.md**

**文件路径**: `.claude/plugins/valuation/ENV_SETUP.md`

列出 6 个数据源环境变量（名称、用途、获取方式）和 A 股默认路径说明。

**.gitignore 追加**

```gitignore
# Valuation plugin outputs
.claude/plugins/valuation/skills/*/outputs/
.claude/plugins/valuation/skills/*/examples/*/output_*.json
```

---

### Component 7: 端到端回归验证脚本

**文件路径**: `.claude/plugins/valuation/skills/company-valuation/scripts/validate_sample.py`

```python
def validate_sample(
    input_path: str = "examples/sample_input.json",
    expected_path: str = "examples/valuation_summary.json",
    tolerance: float = 0.01   # ±1%
) -> ValidationResult:
    # 验证字段: enterprise_value, equity_value, terminal_share, implied_terminal_ev_ebitda
    # 容差内 → exit 0；超出容差 → 输出 diff，exit 1
```

---

### Component 8: calc_industry_model 扩展

**Purpose**: 为 REITs 和 SaaS 补充脚本支持。

```python
def calc_reit_model(inputs: dict, issues: Issues) -> dict:
    # 输入: ffo, pffo_low, pffo_high, asset_value, liabilities, shares
    # 输出: equity_value_low, equity_value_high, nav_per_share

def calc_saas_model(inputs: dict, issues: Issues) -> dict:
    # 输入: arr, ev_arr_low, ev_arr_high
    # 输出: ev_low, ev_high

# calc_industry_model dispatch 新增:
if model_type in {"reit", "reits"}:
    return calc_reit_model(inputs, issues)
if model_type in {"saas", "arr"}:
    return calc_saas_model(inputs, issues)
```

## Data Models

### build_comps 输出结构

```python
{
  "multiples_table": [
    {"ticker": str, "ev_ebitda": float | None, "pe": float | None, "period_basis": str}
  ],
  "summary_stats": {
    "ev_ebitda": {"median": float, "p25": float, "p75": float, "count": int}
  },
  "implied_range": {"low": float, "mid": float, "high": float}
}
```

### vc_model 输出结构

```python
{
  "pre_money": float,
  "post_money": float,
  "scenario_table": [
    {"name": str, "prob": float, "exit_value": float, "pv": float}
  ],
  "ownership_impact": {"pre_dilution": float, "post_dilution": float}
}
```

### ValidationResult 结构

```python
{
  "passed": bool,
  "diffs": [
    {"field": str, "expected": float, "actual": float, "delta_pct": float, "within_tolerance": bool}
  ],
  "summary": str
}
```

## Error Handling

- `build_comps.py`：分母为零或负数 → 标记 N/M，不抛异常
- `vc_model.py`：场景概率之和 ≠ 1 → 抛出 `ValueError`
- `validate_sample.py`：关键字段缺失 → 标记 MISSING，整体 FAILED，exit 1
- 单元测试：fixture 文件缺失 → 跳过并输出 warning，不阻断其他测试

## Testing Strategy

**运行单元测试**:
```bash
python -m pytest .claude/plugins/valuation/skills/company-valuation/scripts/test_auto_valuation.py -v
```

**运行回归验证**:
```bash
python .claude/plugins/valuation/skills/company-valuation/scripts/validate_sample.py
```

| 测试用例 | 验证目标 | 类型 |
|---|---|---|
| `test_dcf_basic` | PV 计算（含 mid-year）与手算一致 | 精度验证 |
| `test_nwc_delta` | NWC 用变化量，FCF 在稳定增长时高于旧逻辑 | 逻辑验证 |
| `test_terminal_value_share` | terminal_share > 0.75 触发 warning | 边界验证 |
| `test_comps_ev_vs_equity` | ev_ebitda 走 EV bridge，pe 不走 | 路径验证 |
| `test_normalize_inputs_qoe` | QoE 调整后 normalized_ebit 正确 | 计算验证 |
| `test_irr_high_growth` | IRR > 100% 场景正常返回 | 边界验证 |
| `test_safe_ratio_near_zero` | denominator 为 1e-11 返回 None | 安全验证 |

## Security Considerations

- API Key 不硬编码，统一通过环境变量读取
- `ENV_SETUP.md` 只说明变量名和获取方式，不包含实际 key 值
- `.gitignore` 补充输出目录，防止含敏感数据的输出文件被意外提交

## Dependencies

| 依赖 | 用途 | 状态 |
|---|---|---|
| pytest | 单元测试运行 | 需确认已安装 |
| auto_valuation.py | 核心计算引擎 | 已有 |
| sample_input.json | 测试 fixture | 已有 |
| valuation_summary.json | 回归基准 | 已有 |
