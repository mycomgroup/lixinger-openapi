# Quality Control

description: Perform valuation quality checks, data validation, and assumption sanity review with strict sign-off rules. Use when asked to review valuation outputs or validate modeling logic. Triggers on "valuation review", "quality check", or "audit valuation".

## Overview

This is a strict audit workflow. It does not change assumptions or rebuild models unless the user explicitly asks.

## Template Requirement

- If the user provides a template, follow it exactly.
- If no template is provided, use the default layout in this skill.

## Inputs Required

- Valuation outputs and key assumptions
- Model type and period basis
- Data sources or source notes if available
- Comps tables and scenario outputs if used

## Assumptions and Defaults

- If inputs are missing, list them and mark impact as unknown.
- QC does not revise assumptions unless explicitly requested.

## Critical Constraints - Read First

- Do not sign off if any Critical issue exists.
- Do not change assumptions without user approval.
- Always state valuation date, currency, and unit scale.
- LTM or NTM basis must be explicit and consistent.
- Use `references/data-requirements.md` and `references/risk-checks.md`.
- If any required input is missing, list it and explain impact.

## Data Source Priority

1. User-provided models, outputs, and assumptions
2. Source notes or data provenance provided with the model
3. Audited filings or official reports for cross-checks

## Workflow

### Step 1: Intake and Scope

- Identify all models used and the primary valuation outputs.
- Confirm valuation date, currency, and unit scale.
- Identify the data sources used for key inputs.

### Step 2: Data Integrity Checks

- Validate historical financials and period alignment.
- Check net debt components and reconcile to sources.
- Verify share counts and dilution schedules.
- If a three-statement model is used, confirm that the balance sheet and cash flow tie.

### Step 3: Assumption Sanity Checks

- Verify WACC is greater than terminal growth.
- Test margins, capex, and working capital against history and peers.
- Flag terminal value dominance if it exceeds 75 percent of EV.

### Step 4: Method Integrity Checks

- DCF: confirm unlevered FCF definition and discounting convention.
- Comps: confirm peer set consistency, LTM or NTM basis, and EV definition.
- Asset-based: confirm revaluation logic and non-operating adjustments.
- SOTP: confirm each segment uses consistent dates and metrics.

### Step 5: Output Review

- Confirm the EV to equity bridge reconciles to diluted shares.
- Validate model weights and the weighted valuation range.
- Ensure scenario outputs match the base case assumptions.

## Output Requirements

- QA summary with Pass, Pass with Issues, or Fail.
- Issue log with severity, location, description, impact, and fix.
- List of missing inputs and assumptions.
- Sign-off statement with limitations.

## Validation Checklist

- LTM or NTM basis is consistent everywhere.
- Currency and unit scale are consistent.
- EV and equity bridge reconciles to diluted shares.
- WACC is greater than terminal growth.
- Terminal value share flagged if above 75 percent.
- DCF uses unlevered FCF and correct discount period.
- Comps use consistent peers and EV definition.
- Scenario tables match base case assumptions.
- Net debt definition matches sources.
- Share count reconciles to dilution method.
- Model weights sum to 100 percent.
- Output ranges tie to model outputs.

## Severity Definitions

- Critical: Output is materially wrong or irreconcilable.
- Warning: Model runs but has significant risk or inconsistency.
- Info: Formatting or documentation improvements.

## Common Failure Points

- Mixing LTM and NTM.
- Inconsistent net debt or EV definition.
- Terminal value dominance without explanation.
- Missing dilution in per-share values.
