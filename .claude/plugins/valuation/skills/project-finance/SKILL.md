# Project Finance Model

description: Build project finance models for infrastructure, energy, and PPP assets. Focuses on contract cash flows, debt sizing, DSCR, and completion risk. Use when asked for project finance modeling, DSCR analysis, or infrastructure valuation. Triggers on "project finance", "DSCR", "PPP model", or "infrastructure model".

## Overview

This skill builds a project cash flow model, sizes debt to DSCR covenants, and produces equity return outputs.

## Template Requirement

- If the user provides a template, follow it exactly.
- If no template is provided, use the default layout in this skill.

## Inputs Required

- Project scope, timeline, and capex schedule
- Contract terms: PPA, toll, availability, escalation, tenor
- Opex and maintenance assumptions
- Tax regime and depreciation schedule
- Financing terms: debt amount, tenor, rate, amortization

## Assumptions and Defaults

- If escalation is not provided, assume flat real pricing and state it.
- If tax regime is not provided, use the statutory rate or flag as unknown.
- If covenants are not provided, assume a minimum DSCR and state it.

## Critical Constraints - Read First

- Separate construction and operations phases.
- Compute DSCR on CFADS, not EBITDA.
- Debt sizing must respect minimum DSCR covenant.
- State whether debt service is sculpted or level.
- Validate covenants under a downside case.

## Data Source Priority

1. User-provided data
2. Contract documents or term sheets
3. Public benchmarks and industry sources

## Workflow

### Step 1: Gather Inputs

- Use `references/project-finance-model.md` for structure and definitions.
- Confirm revenue drivers and escalation mechanics.

### Step 2: Build Cash Flow

- Construct CFADS.
- Separate construction and operations cash flows.
- Apply contract indexation and volume assumptions.

### Step 3: Debt Sizing and Coverage

- Compute DSCR, LLCR, and PLCR.
- Test debt capacity against minimum DSCR covenant.
- Evaluate sculpted versus level debt service.

### Step 4: Returns and Sensitivity

- Compute equity IRR and NPV.
- Run sensitivities on price, volume, capex, and debt terms.

### Step 5: Output

- Provide debt sizing and coverage summaries.

## Output Requirements

- Project cash flow schedule
- DSCR, LLCR, and PLCR tables
- Debt sizing summary and covenant check
- Equity IRR and NPV summary
- Sensitivity summary

## Validation Checklist

- Construction and operations phases are separated.
- CFADS is used for DSCR calculation.
- Debt service schedule ties to cash flow.
- Minimum DSCR covenant is respected in base and downside.
- Currency and unit scale are consistent.

## Common Failure Points

- Using EBITDA instead of CFADS for DSCR.
- Mixing construction capex into operating cash flow.
- Ignoring debt sculpting or covenants.
