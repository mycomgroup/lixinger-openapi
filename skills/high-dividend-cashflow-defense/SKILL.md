---
name: high-dividend-cashflow-defense
description: Build a defensive stock-screening and analysis workflow to distinguish real cash-generating high-dividend companies from dividend traps using dividend/distribution history, cash flow statements, balance sheets, and valuation analysis. Use when users ask questions like “高股息里谁是现金牛”, “分红陷阱怎么排除”, “做防御增强组合”, or need a scoring/ranking model with explainable rules.
---

# High Dividend Cashflow Defense

Use this skill to design and execute a **defensive enhancement model** for high-dividend equities.

## Quick Workflow

1. Define universe and data window.
2. Compute core indicators from:
   - dividend/distribution history
   - cash flow statement
   - balance sheet
   - valuation metrics
3. Score each company on **Cash Dividend Quality**, **Balance Sheet Resilience**, and **Valuation Margin**.
4. Tag names as `True Cash Cow`, `Watchlist`, or `Dividend Trap`.
5. Output ranking + risk notes + rebalancing triggers.

If no exact data is available, clearly state assumptions and provide a proxy method.

## Metric Framework

Read `references/metric-framework.md` before doing full analysis.

Use the following pillars:

- **P1 分红可持续性 (30%)**
- **P2 现金流质量 (35%)**
- **P3 资产负债表韧性 (20%)**
- **P4 估值与安全边际 (15%)**

Default total score range: `0-100`.

## Decision Rules (Default)

Classify with both score and hard constraints:

- `True Cash Cow`:
  - Total score `>= 75`
  - `FCF/Dividends >= 1.2`
  - Last-3Y CFO positive in at least 2 years
  - Net debt/EBITDA not deteriorating sharply
- `Watchlist`:
  - Total score `55-74`
  - No hard red flag triggered
- `Dividend Trap` (any one trigger is enough):
  - Dividend yield is in top quantile but `FCF/Dividends < 0.8`
  - CFO positive but FCF persistently negative due to capex stress
  - Rising short-term debt + declining cash ratio + payout not adjusted
  - Dividend maintained mainly by asset sales/new debt/equity financing

Always report which hard trigger caused a `Dividend Trap` tag.

## Output Template

Use this structure in responses:

1. **结论摘要**: top candidates and avoided traps.
2. **评分表**: ticker, dividend yield, P1-P4 score, total score, final label.
3. **关键证据**:
   - dividend history consistency
   - cash conversion and FCF coverage
   - debt maturity and liquidity pressure
   - valuation percentile vs own history/peers
4. **风险与失效条件**: what could break thesis.
5. **调仓规则**: downgrade/exit conditions.

## Defensive Portfolio Construction Rules

When user asks for a model portfolio:

- Prefer sector diversification and avoid single-sector yield concentration.
- Cap single name weight (e.g., `<= 10%`).
- Blend high-yield and medium-yield/high-quality names.
- Penalize firms with unstable financing structure even if current yield is high.
- Rebalance quarterly; add event-driven review for dividend cuts, refinancing shocks, or regulatory changes.

## Communication Rules

- Explain **why yield is sustainable or fake** in plain language.
- Avoid using yield alone as a buy signal.
- If data is stale or partial, call it out explicitly.
- Give scenario analysis (base/bull/bear) when uncertainty is high.
