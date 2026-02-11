# Verification Notes (2026-02-11)

## Scope
This note documents check logic updates made to improve physical coherence, genericity (all countries), and auditability without country-specific exceptions.

## Check Logic Changes

### Q1
- `Q1_NO_FALSE_PHASE2_WITHOUT_LOW_PRICE`
  - Rule enforced in code: a year cannot be `is_phase2_market=True` with zero LOW-PRICE and zero PHYSICAL flags.
  - Rationale: prevents capture-only false positives.
- `Q1_MUSTRUN_SCOPE_LOW_COVERAGE`
  - Reframed from a hard low-threshold warning to contradiction-based warning:
  - Warn only if `coverage < 5%` and `IR > 0.3`.
  - Rationale: low coverage can be normal in flexible systems.
- `Q1_MUSTRUN_SCOPE_HIGH_COVERAGE`
  - Warn if `coverage > 60%`.
  - Rationale: guards against must-run overestimation.

### Q2
- `Q2_NOT_SIGNIFICANT`
  - Downgraded to `INFO` instead of hard warning/fail behavior.
  - Rationale: low significance is a statistical limitation, not necessarily a model defect.
- `Q2_UNLIKELY_SLOPE`
  - Warn when absolute capture slope is unusually high (`abs(slope) > 0.2/year`).
  - Rationale: catches unstable regression outcomes.
- Outlier sensitivity
  - Added explicit all-years vs excluding-outliers outputs and reason codes.
  - Rationale: avoids hidden dependence on one abnormal year.

### Q3
- `Q3_INVERSION_K_DEMAND_LARGE`, `Q3_INVERSION_R_MUSTRUN_LARGE`
  - Retained as warnings for large required levers.
- `Q3_INVERSION_*_BEYOND_BOUNDS`
  - Added explicit beyond-bounds statuses/checks.
  - Rationale: solver no longer saturates silently at max bounds.

### Q4
- `Q4_OBJECTIVE_NOT_REACHED`
  - Warn emitted only when no grid point satisfies objective.
  - Best available pair still returned with explicit recommendation to expand grid.
  - Rationale: keeps output actionable while preserving objective truthfulness.

### Q5
- `Q5_ALPHA_NEGATIVE`
  - Interpreted contextually:
  - If `TTL_obs >= TTL_target`, status becomes informational (`already_above_target`) with required values set to zero.
  - Rationale: avoids false warnings for economically valid situations.
- Distributional anchor confidence
  - Replaced strict correlation-only interpretation with distributional fit error on high quantiles.
  - Rationale: hourly correlation alone is not a robust adequacy criterion for thermal anchor validation.

## Core Physical Invariants
- Enforced runtime and tests for:
  - `0 <= FAR <= 1`, `0 <= SR <= 1`, `IR >= 0`
  - `absorbed <= surplus`, `unabsorbed >= 0`
  - if `surplus == 0` then `FAR == 1` and `unabsorbed == 0`
  - `must_run <= total_generation` when available.

## Notes
- No country-specific hardcoded exception added.
- `ENTSOE_API_KEY` remains environment-variable based (no secret committed).
