# Company Valuation

description: Build a full multi-model valuation for a single company with strict execution rules. Includes intrinsic valuation, relative comps, industry-specific checks, EV and equity bridge, scenario analysis, and QA. Use when asked to value a company, produce a valuation report, or cross-check valuation methods. Triggers on "company valuation", "multi-model valuation", "valuation report", or "DCF valuation".

## Overview

This is the master valuation workflow. It must call `peer-analysis`, `scenario-modeling`, `quality-control`, and `ev-equity-bridge` unless the user explicitly narrows the scope.

## Computation Engine (Auto Valuation)

To move beyond a process-only workflow, use the execution layer:

- Script: `scripts/auto_valuation.py`
- Input schema: `references/input-schema.md`
- Example input: `examples/sample_input.json`
- Resource example: `examples/sample_input_resource.json`
- Project finance example: `examples/sample_input_project_finance.json`
- Outputs: `outputs/valuation_summary.json` and `outputs/valuation_report.md`
- Industry models supported: `financials`, `resource`, `project_finance` via `industry_model` block
- Industry model formulas: `references/industry-models.md`

Run:
`python scripts/auto_valuation.py --input examples/sample_input.json --outdir outputs`

## Template Requirement

- If the user provides a template, follow it exactly.
- If no template is provided, use `references/output-template.md`.
- Do not invent a new layout when a template exists.

## Inputs Required

- Valuation date, currency, and unit scale
- Period basis: LTM or NTM
- Financials: revenue, EBITDA, EBIT, net income
- Balance sheet: cash, debt, preferred, minority interest
- Market data: price, shares, dilution details
- Cost of capital inputs or guidance
- Industry classification and business model
- Optional normalization inputs: one-offs, QoE/accounting adjustments, restricted cash, lease liabilities, maintenance capex, cash-flow support, and dilution bridge items

## Assumptions and Defaults

- If valuation date is not provided, use the latest available close and state it.
- If currency is not provided, use the reporting currency.
- If period basis is not provided, default to LTM.
- If model weights are not provided, use `references/model-weighting.md`.

## Critical Constraints - Read First

- Always include at least one intrinsic model and one relative model.
- Always state valuation date, currency, and unit scale in the output.
- Never mix LTM and NTM within a single model table.
- Use a single EV definition and net debt policy across the entire analysis.
- Always produce an EV to equity bridge and reconcile to diluted shares.
- Always run `quality-control` before final output.
- If any input is missing, state the assumption and its impact.
- Terminal growth must be less than WACC.
- Terminal value should not dominate without justification, flag if it exceeds 75 percent of EV.
- If a denominator is negative or near zero, mark as N/M and exclude from stats.
- Model weights must sum to 100 percent and be justified.
- Do not hardcode results that should be driven by assumptions.

## Data Source Priority

1. User-provided data
2. **A股公司**：先调用 `cn-data-source` skill 发现可用 provider、查询入口与来源说明，再按本次估值提取最小字段集
3. MCP sources if available
4. Audited filings or official reports
5. Public market data for current prices or shares

### A股数据获取规则

当股票代码为6位数字（如 600519、300750、000858）时：
- 优先通过 `cn-data-source` 确定最合适的 provider 与查询命令
- 仅将本次估值所需的最小字段整理为 `references/input-schema.md` 所需结构
- 数据单位从元换算为百万元后再传入估值模型
- 如混用多个 provider，为实际使用字段保留 `source_map` 或 `source_notes`
- 无风险利率使用中国10年期国债收益率，ERP 使用 6%~8%

## Workflow

### Step 1: Clarify Requirements

- Confirm company, currency, valuation date, and unit scale.
- Confirm desired output format and template usage.
- Confirm whether any industry-specific model is required.

### Step 2: Gather Inputs

- LTM or NTM financials: revenue, EBITDA, EBIT, net income.
- Balance sheet: cash, debt, net debt, equity.
- Cash flow: operating cash flow, capex, working capital.
- Market data: share price, shares outstanding, market cap.
- Cost of capital inputs: risk-free rate, beta, equity risk premium, tax rate.
- Business model and industry classification.

### Step 3: Normalize and Validate

- Align fiscal periods, currency, and unit scale across all inputs.
- If multiple providers are mixed, preserve per-field provenance via `source_map` or equivalent source notes.
- Normalize for one-offs and accounting anomalies.
- For A股非金融公司，优先形成 `reported -> normalized` 桥表，再进入估值。
- QoE/accounting adjustments 优先覆盖政府补助、公允价值变动、资产处置收益、减值、信用减值、存货跌价等非核心项目。
- If operating cash flow is available, cross-check normalized earnings with cash conversion.
- Confirm net debt vs net cash and document adjustments, including restricted cash and lease liabilities where relevant.
- Verify share count and dilution details, including options, RSUs, converts, and buybacks if material.

### Step 4: Model Selection Rules

- Profitable, stable cash flows: FCFF DCF as anchor.
- Financial institutions: residual income or DDM, plus P/B.
- Asset-heavy or cyclical: mid-cycle DCF plus P/B or NAV.
- High-growth but unprofitable: scenario DCF plus P/S or EV to ARR.
- Conglomerate: SOTP as industry-specific model.

### Step 5: Intrinsic Valuation

- Use `references/valuation-formulas.md`.
- Use `references/valuation-models.md`.
- Use 5 to 10 year projections unless clearly stable.
- Apply mid-year convention if not otherwise specified.
- For A股非金融公司，优先用 normalized EBIT / owner earnings / normalized net debt 进入估值。
- Use perpetuity and exit multiple as cross-checks.
- Show implied terminal multiple from DCF assumptions.

### Step 6: Relative Valuation

- Call `peer-analysis` for the peer set and multiple ranges.
- Use at least 3 core multiples relevant to the industry.
- Report median and quartile bands.

### Step 7: Industry-Specific Model

- Select a model from `references/valuation-models.md`.
- Include only if it materially explains industry economics.

### Step 8: Scenario and Sensitivity

- Call `scenario-modeling` for base, upside, and downside cases.
- Require at least one DCF sensitivity and one multiple sensitivity.
- Ensure base case aligns with intrinsic assumptions.

### Step 9: EV and Equity Bridge

- Call `ev-equity-bridge`.
- Include minority interest, preferred equity, options, and converts.

### Step 10: Model Weighting and Conclusion

- Use `references/model-weighting.md` if no user guidance is provided.
- Explain weights and how they reflect model reliability.
- Produce a weighted valuation range and midpoint.

### Step 11: Quality Control

- Call `quality-control`.
- Resolve all material issues or flag them in output.

### Step 12: Produce Output

- Use `references/output-template.md`.
- Include model rationale, assumptions, sensitivity tables, and QA notes.

## Output Requirements

- Valuation range with midpoint and weightings.
- Model result table for each method used.
- Peer multiples table with median and quartiles.
- EV and equity bridge table.
- Scenario table with base, upside, and downside.
- QA checklist summary and issue log.
- Explicit list of key assumptions and data sources.

## Validation Checklist

- LTM or NTM consistent everywhere.
- Currency and unit scale consistent.
- WACC is greater than terminal growth.
- Terminal value share flagged if it exceeds 75 percent.
- EV and equity bridge reconciles with diluted shares.
- Comps table uses consistent peer criteria and EV definition.
- Implied multiples are within a reasonable industry range.
- Scenario hierarchy is logical with upside above base and downside below.
- Weights sum to 100 percent and are explained.

## Common Failure Points

- Mixing LTM with NTM in a single table.
- Using book values for WACC weights.
- Omitting non-operating assets in the bridge.
- Terminal value dominating without justification.
- Peer set too small or misclassified.
- Weighting that contradicts the stated model confidence.
