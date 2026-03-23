# Scenario Modeling

description: Design base, upside, and downside scenarios and run sensitivity analysis on valuation drivers with strict output rules. Use when asked for sensitivity tables, scenario valuation, or risk ranges. Triggers on "scenario analysis", "sensitivity", or "stress test".

## Overview

This skill builds scenario cases and sensitivity tables that are fully linked to valuation drivers and consistent with the base model.

## Template Requirement

- If the user provides a template, follow it exactly.
- If no template is provided, use the default layout in this skill.

## Inputs Required

- Base model assumptions and outputs
- Key drivers to stress or scenario shift
- Valuation date, currency, and period basis

## Assumptions and Defaults

- If driver ranges are not provided, use `references/assumptions-catalog.md`.
- If sensitivity grid size is not provided, default to 5 by 5.
- Base case is taken from the primary valuation model unless specified.

## Critical Constraints - Read First

- Always produce Base, Upside, and Downside scenarios.
- The Base case must match the primary valuation assumptions.
- Each scenario must list explicit drivers and values.
- Provide at least one DCF sensitivity and one multiple sensitivity.
- Sensitivity tables must be fully calculated, no placeholders.
- Use consistent units, currency, and period basis across outputs.

## Data Source Priority

1. User-provided base model assumptions and outputs
2. Outputs from `company-valuation` or other core models
3. Reference ranges from `references/assumptions-catalog.md`

## Workflow

### Step 1: Align the Base Case

- Confirm valuation date, currency, and period basis.
- Pull base assumptions from the primary valuation model.
- Lock base metrics before defining scenarios.

### Step 2: Define Scenario Drivers

- Use `references/assumptions-catalog.md` for default ranges.
- Select 4 to 6 key drivers such as growth, margin, capex, working capital, WACC, terminal growth, or exit multiple.
- State base, upside, and downside values for each driver.
- Ensure drivers are internally consistent.

### Step 3: Build Scenario Valuations

- Recompute valuation outputs for each scenario.
- Show EV, equity value, and per-share values for each case.
- Document which models were used for each scenario.

### Step 4: Build Sensitivity Tables

- Use `references/scenario-sensitivity.md` for driver pairs.
- DCF sensitivity must include WACC versus terminal growth or exit multiple.
- Multiple sensitivity must include a valuation multiple versus an operating metric.
- Use at least a 5 by 5 grid unless the user requests otherwise.

### Step 5: Summarize Results

- Present scenario valuation ranges and the main drivers.
- Highlight breakpoints where conclusions change.

## Output Requirements

- Scenario assumptions table with base, upside, and downside values.
- Scenario valuation table with EV, equity, and per-share values.
- DCF sensitivity table.
- Multiple sensitivity table.
- Summary of the top drivers and their elasticity.

## Validation Checklist

- Base case equals the primary valuation inputs.
- Upside valuation exceeds base and downside is below base.
- Sensitivity tables show monotonic directional movement.
- Units, currency, and period basis are consistent.
- Scenario driver values are realistic and non-contradictory.

## Common Failure Points

- Base case drift from the primary valuation.
- Sensitivity grids not linked to model drivers.
- Scenario assumptions that cannot coexist.
