# VC / Startup Model

description: Value high-growth and pre-profit companies using VC Method, First Chicago, ARR multiples, and unit economics. Use for early-stage valuation, growth equity, or SaaS benchmarking. Triggers on "startup valuation", "VC model", "First Chicago", or "ARR multiple".

## Overview

This skill builds scenario-driven valuations for early-stage companies with explicit assumptions on growth, burn, and exit outcomes.

## Template Requirement

- If the user provides a template, follow it exactly.
- If no template is provided, use the default layout in this skill.

## Inputs Required

- Revenue or ARR, growth, and retention
- CAC, LTV, payback period
- Burn rate and runway
- Exit multiple and target return
- Current cap table and dilution assumptions if available

## Assumptions and Defaults

- If exit multiple is not provided, use a peer range and state it.
- If target return is not provided, default to a typical VC hurdle and state it.
- If dilution is unclear, assume a conservative pool expansion and state it.

## Critical Constraints - Read First

- Show both pre-money and post-money valuation.
- State the exit year and the exit metric used.
- Separate operating burn from financing inflows.
- Use scenario weights for First Chicago outputs.

## Data Source Priority

1. User-provided company metrics and cap table
2. Management guidance and investor materials
3. Public SaaS or sector benchmarks

## Workflow

### Step 1: Gather Inputs

- Use `references/vc-startup-model.md` for structure and definitions.
- Confirm revenue basis, retention definitions, and cohort assumptions.

### Step 2: Build Valuations

- VC Method: exit value, target return, and present value.
- First Chicago: downside, base, upside scenarios with weights.
- Multiples: EV to ARR or P/S with peer ranges.

### Step 3: Output

- Provide valuation range and key drivers.
- Summarize dilution and ownership impacts.

## Output Requirements

- Pre-money and post-money valuation range
- Scenario table with weights and outcomes
- Key driver summary and sensitivities
- Dilution and ownership impact summary

## Validation Checklist

- Exit year and metric are stated.
- Scenario weights sum to 100 percent.
- Valuation range aligns with scenario outputs.
- Currency and unit scale are consistent.

## Common Failure Points

- Using public market multiples without scale or risk adjustments.
- Ignoring dilution and option pool expansion.
- Mixing ARR and revenue definitions across metrics.
