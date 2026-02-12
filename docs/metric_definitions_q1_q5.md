# Metric Definitions (Q1..Q5)

## Scope

This document defines the audited, hourly model conventions used across Q1..Q5.

## Hourly Load Convention

- `load_total_mw`: native system demand (before flexible pumping sink).
- `psh_pumping_mw`: pumping load used as a flexibility sink.
- `load_mw`: net demand used in residual-load logic.

Definition:

```text
load_mw = load_total_mw - psh_pumping_mw
```

Audit identity checked on annual aggregates:

```text
load_total_mw_avg ~= load_mw_avg + psh_pumping_mw_avg
```

## Surplus Ratio (SR)

- `sr_energy`: share of surplus energy over the configured denominator (reported with denominator fields).
- `sr_hours`: share of hours with surplus (`surplus_mw > 0`).

Interpretation:

- higher `sr_energy` or `sr_hours` means more frequent/stronger surplus stress.

## Flex Absorption Ratio (FAR)

- `far_energy`: absorbed surplus energy divided by total surplus energy.
- `FAR = 1` when no unabsorbed surplus remains; `FAR < 1` when curtailment-like residual surplus exists.
- Sinks include exports and pumping/flex sinks; sink composition is exposed via `sink_breakdown_json`.

## Inflexibility Ratio (IR)

- `ir_p10`: must-run pressure indicator based on low-load regime quantiles.
- Stable definition in code: low-load quantile based ratio (must-run vs load) used consistently in Q1/Q2/Q3.

Interpretation:

- larger `ir_p10` indicates stronger structural inflexibility.

## TTL and TCA

- `ttl_observed_eur_mwh`: observed TTL anchor from hourly price distribution (historical reference, C/D regime logic).
- `tca_*_eur_mwh`: thermal cost anchor from fuel/CO2/efficiency/VOM:

```text
TCA = fuel/efficiency + CO2*(emission_factor/efficiency) + VOM
```

- `ttl_model_eur_mwh`: modeled TTL from base observed TTL plus thermal delta pass-through:

```text
ttl_model = ttl_observed_base + (tca_scenario - tca_base) * pass_through_factor
```

- `delta_tca_vs_base`, `delta_ttl_model_vs_base`: explicit deltas vs BASE anchor when BASE reference is available.

## Negative Price and Q3/Q4 Proxies

- `predicted_h_negative_after` in Q3 is explicitly a proxy (`PROXY_SURPLUS_OR_LOW_NRL`), not a full price-model output.
- Q4 exports:
  - `h_negative_proxy_after`
  - `h_negative_reducible_upper_bound`
  - `h_negative_upper_bound_after`

These are auditable proxy bounds to avoid over-claiming exact negative-hour forecasts without a full endogenous price model.

## Missing Data Policy

- No silent zero-fill for critical missing data.
- Missing critical inputs are surfaced via:
  - coverage fields (`coverage_*`)
  - `data_quality_flags`
  - explicit WARN entries in the test ledger.
- CSV exports use explicit `NaN` serialization, not blank strings.
