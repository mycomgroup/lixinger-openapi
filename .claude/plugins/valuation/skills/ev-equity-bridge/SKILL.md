# EV / Equity Bridge

description: Bridge enterprise value to equity value with full adjustments and dilution handling. Use for valuation summaries, fairness opinions, or deal pricing. Triggers on "EV bridge", "equity bridge", or "enterprise to equity".

## Overview

This skill converts enterprise value to equity value and per-share value with explicit treatment of claims, non-operating assets, and dilution.

## Template Requirement

- If the user provides a template, follow it exactly.
- If no template is provided, use the default layout in this skill.

## Inputs Required

- Enterprise value and valuation date
- Cash, debt, preferred, minority interest
- Non-operating assets and investments
- Options, warrants, convertibles
- Basic and diluted share counts

## Assumptions and Defaults

- If dilution method is not specified, use treasury stock method.
- If convertibles are unclear, state the assumption and impact.

## Critical Constraints - Read First

- Always state valuation date, currency, and unit scale.
- Always separate operating versus non-operating items.
- Always show basic and diluted per-share values.
- Net cash adds to EV and net debt subtracts from EV.
- Minority interest and preferred equity must be treated explicitly.
- Specify the dilution method used.
- Do not double-count cash, investments, or leases.

## Data Source Priority

1. User-provided EV and balance sheet adjustments
2. Outputs from valuation models or comps
3. Audited filings or official reports

## Workflow

### Step 1: Confirm EV Basis

- Confirm whether EV is operating value from DCF or comps.
- Confirm how leases, pensions, and other claims are treated in EV.
- If the input is already equity value, do not re-bridge and state that.

### Step 2: Gather Adjustments

- Cash and non-operating assets.
- Debt and debt-like items.
- Preferred equity and minority interest.
- Non-controlling investments and other claims.
- Options, warrants, and convertibles.
- Basic and diluted share counts.

### Step 3: Build the Bridge

- Start with EV.
- Add cash and non-operating assets.
- Subtract debt, preferred, and minority interest.
- Adjust for other claims or investments as applicable.
- Produce equity value.

### Step 4: Dilution and Per-Share

- Select treasury stock or if-converted method.
- Include in-the-money options and warrants.
- For convertibles, state the trigger and method used.
- Compute basic and diluted per-share values.

### Step 5: Output

- Provide the bridge table, dilution summary, and per-share values.
- Note any material adjustments or assumptions.

## Output Requirements

- Bridge table with line items and totals.
- Net debt definition and components.
- Dilution schedule summary.
- Basic and diluted per-share values.

## Validation Checklist

- Net debt definition consistent with valuation model.
- Non-operating assets included and not double-counted.
- Minority interest and preferred treated explicitly.
- Share counts reconcile to the stated dilution method.
- Per-share values computed from equity value and share counts.
- Currency, unit scale, and valuation date stated.

## Common Failure Points

- Double-counting cash or investments.
- Omitting minority interest or preferred equity.
- Using basic shares when dilution exists.
- Treating leases inconsistently with EV.
