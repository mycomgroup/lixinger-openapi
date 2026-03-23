# Resource Valuation

description: Value oil, gas, and mining assets using reserves, rNPV, and unit economics. Use for resource company valuation, IPO prep, or asset-level appraisal. Triggers on "resource valuation", "oil gas valuation", "mining valuation", or "rNPV".

## Overview

This skill builds asset-level cash flows based on reserves and production profiles, then computes NPV and rNPV with commodity price sensitivity.

## Template Requirement

- If the user provides a template, follow it exactly.
- If no template is provided, use the default layout in this skill.

## Inputs Required

- Reserves by class and recovery rates
- Production profile and decline curves
- Commodity price deck and differentials
- Capex, opex, and sustaining costs
- Tax and royalty regime
- Decommissioning or abandonment costs

## Assumptions and Defaults

- If price deck is not provided, use a standard benchmark deck and state it.
- If success probabilities are not provided, assume proved is 100 percent and state it.
- If discount rate is not provided, request it or state a placeholder and impact.

## Critical Constraints - Read First

- Separate proved, probable, and possible reserves.
- Apply royalties, taxes, and abandonment costs consistently.
- State whether prices and costs are real or nominal.
- Use rNPV when technical or commercial risks are material.

## Data Source Priority

1. User-provided reserve reports and technical data
2. Operator guidance and official filings
3. Public benchmarks for price decks and costs

## Workflow

### Step 1: Gather Inputs

- Use `references/resource-valuation.md` for structure and definitions.
- Confirm reserve classes and production profiles.

### Step 2: Build Cash Flow

- Forecast production, revenue, and operating costs.
- Apply royalties, taxes, and abandonment costs.
- Compute NPV and rNPV if probabilities apply.

### Step 3: Benchmark Metrics

- Compute NPV per boe or per ton.
- Compute EV to reserves and EV to production.

### Step 4: Output

- Provide asset-level NPV and rNPV with sensitivity ranges.

## Output Requirements

- NPV and rNPV summary
- Unit value metrics
- Sensitivity on prices and costs
- Clear statement of price deck and discount rate

## Validation Checklist

- Reserve classes are separated and labeled.
- Price deck and cost basis are stated.
- Taxes, royalties, and abandonment are applied.
- Currency and unit scale are consistent.

## Common Failure Points

- Mixing reserve classes or double-counting production.
- Omitting abandonment costs.
- Using inconsistent price decks across assets.
