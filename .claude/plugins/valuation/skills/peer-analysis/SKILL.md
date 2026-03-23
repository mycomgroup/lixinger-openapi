# Peer Analysis

description: Build a comparable company set, normalize multiples, and summarize valuation ranges with strict consistency checks. Use when asked for comps, peer set selection, or market multiple benchmarking. Triggers on "peer analysis", "comps", "comparable companies", or "relative valuation".

## Overview

This skill produces a defensible peer set and a clean multiples package with clear period labeling, consistent EV definitions, and documented adjustments.

## Template Requirement

- If the user provides a template, follow it exactly.
- If no template is provided, use the default layout in this skill.

## Inputs Required

- Target company or industry
- Valuation date and period basis
- Peer candidates or screening criteria
- Market data: price, shares, debt, cash
- Financial metrics for multiples

## Assumptions and Defaults

- If no peer list is provided, derive peers using `references/peer-selection.md`.
- If period basis is not provided, default to LTM.
- If price date is not provided, use the latest available close and state it.

## Critical Constraints - Read First

- Minimum 5 peers unless the industry is too narrow, and explain if fewer.
- Use a single basis, LTM or NTM, across any given table.
- Use a single EV definition and net debt policy across all peers.
- Use the same valuation date for market data, or state any mismatch.
- If a denominator is negative or near zero, mark as N/M and exclude from stats.
- Adjust for one-offs that materially distort multiples and document them.
- Provide median, P25, and P75 for each multiple, not just averages.

## Data Source Priority

1. User-provided peer list or data
2. MCP sources if available
3. Audited filings or official reports
4. Public market data for prices and shares

## Workflow

### Step 1: Scope and Criteria

- Confirm target company, valuation date, and period basis.
- Define peer screen: industry, business model, revenue mix, size, growth, margin profile, geography, and regulation.
- Decide if the company should be treated as financials or non-financials.

### Step 2: Build the Peer List

- Use `references/peer-selection.md`.
- Start with 8 to 12 candidates, then narrow to 5 to 10 final peers.
- Document exclusions and the rationale for each exclusion.

### Step 3: Collect and Normalize Data

- Gather price, shares, market cap, debt, cash, minority interest, and preferred equity.
- Align currency and unit scale across all peers.
- Normalize fiscal year and LTM or NTM basis.
- Adjust for one-offs, leases, and SBC if material and consistent.

### Step 4: Compute EV and Multiples

- EV = Market Cap + Net Debt + Preferred + Minority - Non-operating assets.
- Use a single net debt definition and cash treatment across peers.
- Select multiples using `references/industry-mapping.md`.
- Clearly label every metric as LTM or NTM.

### Step 5: Summarize and Apply

- Produce the comps table and summary statistics.
- Apply selected multiple ranges to target metrics.
- Present the implied valuation range with method notes.

## Output Requirements

- Peer list table with ticker, business description, size, growth, margin, and geography.
- Market data table with price date, shares, market cap, and net debt.
- Multiples table with LTM or NTM labels and currency units.
- Summary stats table with median, P25, P75, and count.
- Exclusion list with rationale and any data gaps.

## Validation Checklist

- LTM or NTM is consistent across each table.
- EV definition and net debt policy are consistent.
- Currency and unit scale are consistent.
- Price date and shares date are stated.
- N/M items are excluded from stats.
- Outliers are flagged with rationale.
- Implied range uses target metrics from the same period basis.

## Common Failure Points

- Mixing LTM and NTM within the same table.
- Using inconsistent EV or net debt across peers.
- Averaging ratios when denominators are negative.
- Applying multiples to target metrics from a different period.
