# Valuation Plugin

Valuation modeling skills for intrinsic valuation, comps, scenario analysis, and QA.

Architecture reference:
`skills/company-valuation/references/auto_valuation_architecture.md` (valuation system architecture)

## Quickstart

1. Choose a command, for example `/company-valuation [company]`.
2. Provide valuation date, currency, and period basis (LTM or NTM).
3. Share key inputs: revenue, EBITDA, net income, cash, debt, shares.
4. Review outputs: valuation range, comps table, scenario table, and QA log.

## Execution Layer (Auto Valuation)

To run an automated valuation using normalized inputs:

- Script: `skills/company-valuation/scripts/auto_valuation.py`
- Input schema: `skills/company-valuation/references/input-schema.md`
- Example input: `skills/company-valuation/examples/sample_input.json`
- Resource example: `skills/company-valuation/examples/sample_input_resource.json`
- Project finance example: `skills/company-valuation/examples/sample_input_project_finance.json`
- Industry models: `financials`, `resource`, `project_finance` via `industry_model`
- Industry model formulas: `skills/company-valuation/references/industry-models.md`

Example:
`python skills/company-valuation/scripts/auto_valuation.py --input skills/company-valuation/examples/sample_input.json --outdir skills/company-valuation/outputs`

## Input Expectations

- Valuation date, currency, and unit scale
- Period basis: LTM or NTM
- Financials: revenue, EBITDA, EBIT, net income
- Balance sheet: cash, debt, preferred, minority interest
- Market data: price, shares outstanding, dilution info

## Data Source Priority

1. User-provided data
2. MCP sources if available
3. Audited filings or official reports
4. Public market data for current prices or shares

## Scope and Fit

Best fit:
- Public companies with reliable financials
- Sectors where standard multiples and DCF inputs are observable
- Projects with contracted cash flows and clear debt terms

Not ideal:
- Pre-revenue companies without credible monetization signals
- Markets with opaque reporting or extreme accounting volatility
- Situations where inputs are missing and cannot be reasonably estimated

## Commands

| Command | Description |
|---------|-------------|
| `/company-valuation [company]` | Multi-model valuation pack |
| `/peer-analysis [company or industry]` | Comparable company analysis |
| `/scenario-modeling [company]` | Scenario and sensitivity analysis |
| `/quality-control [company or valuation]` | Valuation QA checks |
| `/project-finance [project]` | Project finance model with DSCR |
| `/resource-valuation [asset or company]` | Resource valuation using rNPV |
| `/vc-startup-model [company]` | Startup/VC valuation |
| `/ev-equity-bridge [company]` | EV to equity bridge |
| `/finnhub-quote [symbol]` | Finnhub quote (non-MCP) |
| `/fmp-quote [symbol]` | Financial Modeling Prep quote (non-MCP) |
| `/alphavantage-quote [symbol]` | Alpha Vantage Global Quote (non-MCP) |
| `/tiingo-eod [symbol]` | Tiingo daily prices (non-MCP) |
| `/eulerpool-income-statement [optional]` | Eulerpool superinvestors list (non-MCP) |
| `/massive-agg-bars [optional]` | Massive reference ticker types (non-MCP) |
| `/test-data-sources [symbol]` | Smoke test all non-MCP sources |

## Skills

### Core Valuation
| Skill | Description |
|-------|-------------|
| **company-valuation** | Full valuation workflow |
| **peer-analysis** | Comparable company analysis |
| **scenario-modeling** | Scenario and sensitivity analysis |
| **quality-control** | QA and risk checks |
| **ev-equity-bridge** | EV to equity bridge |

### Specialized Models
| Skill | Description |
|-------|-------------|
| **project-finance** | Project finance modeling |
| **resource-valuation** | Resource and mining valuation |
| **vc-startup-model** | Startup and VC valuation |

### Data Source Utilities
| Skill | Description |
|-------|-------------|
| **data-source-docs** | Cached provider summaries for data sources |
