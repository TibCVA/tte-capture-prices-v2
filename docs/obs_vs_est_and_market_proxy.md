# OBS vs EST and Market Proxy (Q3/Q4)

## Naming contract
- `*_obs_*`: metric computed from observed day-ahead prices of the analyzed year.
- `*_est_*`: metric estimated by the auditable market proxy and used for lever simulations.
- `*_base_*`: baseline reference value for the scenario (typically HIST).

Backward-compatibility aliases are kept temporarily:
- `h_negative_before = h_negative_obs_before`
- `h_negative_after = h_negative_est_after`
- `h_negative_after_source = "est_proxy"`

The same rule applies to `h_below_5`.

## MarketProxyBucketModel
Q3 and Q4 now share a single auditable proxy:
- inputs per hour: `load_mw`, `vre_gen_mw`, `must_run_mw`, `residual_load_mw`, `ir_hour`, observed price.
- bucket definition: `(residual_load_decile, ir_high)` where:
  - residual deciles are fixed from baseline quantiles,
  - `ir_high` is defined with baseline `p90(ir_hour)`.
- outputs per bucket: `p_neg`, `p_low`, `mean_price`, PV/Wind weighted means.

Scenario simulation reuses baseline bucket rates (no recalibration in scenario), and only reassigns hours to buckets after lever-induced hourly changes.

## Reading outputs
- `*_obs_before`: observed baseline market state.
- `*_est_before`: baseline reconstructed by proxy.
- `*_est_after`: simulated state after lever/BESS.
- deltas are interpreted on EST metrics (`after - before`).
- `proxy_quality_status` (`PASS|WARN|FAIL`) is a hard gate:
  - Q3/Q4 return `FAIL` when proxy quality is `FAIL`.

## Schema
- `output_schema_version` is included in Q3/Q4/Q5 outputs to support migration and downstream readers.
- `q1_quality_summary`, `q2_quality_summary`, `q3_quality_summary`, `q4_quality_summary`, `q5_quality_summary`
  provide a normalized gate per `(module_id, country, year, scenario_id)` with `quality_status` in `PASS|WARN|FAIL`.
