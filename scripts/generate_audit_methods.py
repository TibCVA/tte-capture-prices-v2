"""Auto-generate AUDIT_METHODS_Q1_Q5.md from live Python source code.

This script introspects the actual modules (q1-q5, metrics, constants,
assumptions CSV) to produce an always-in-sync methodology reference.

Can be called:
- As a standalone script: `python scripts/generate_audit_methods.py`
- Programmatically: `from scripts.generate_audit_methods import generate`
"""

from __future__ import annotations

import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUTPUT_PATH = ROOT / "AUDIT_METHODS_Q1_Q5.md"

# ---------------------------------------------------------------------------
# Source files to watch (if any is newer than the .md, regenerate)
# ---------------------------------------------------------------------------
SOURCE_FILES = [
    ROOT / "src" / "metrics.py",
    ROOT / "src" / "constants.py",
    ROOT / "src" / "modules" / "q1_transition.py",
    ROOT / "src" / "modules" / "q2_slope.py",
    ROOT / "src" / "modules" / "q3_exit.py",
    ROOT / "src" / "modules" / "q4_bess.py",
    ROOT / "src" / "modules" / "q5_thermal_anchor.py",
    ROOT / "src" / "modules" / "common.py",
    ROOT / "src" / "modules" / "reality_checks.py",
    ROOT / "src" / "scenario" / "calibration.py",
    ROOT / "src" / "scenario" / "phase2_engine.py",
    ROOT / "data" / "assumptions" / "phase1_assumptions.csv",
]


def is_stale() -> bool:
    """Return True if AUDIT_METHODS_Q1_Q5.md is missing or older than any source file."""
    if not OUTPUT_PATH.exists():
        return True
    md_mtime = OUTPUT_PATH.stat().st_mtime
    for src in SOURCE_FILES:
        if src.exists() and src.stat().st_mtime > md_mtime:
            return True
    return False


# ---------------------------------------------------------------------------
# Read assumptions CSV
# ---------------------------------------------------------------------------
def _read_assumptions() -> list[dict[str, str]]:
    path = ROOT / "data" / "assumptions" / "phase1_assumptions.csv"
    if not path.exists():
        return []
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _format_assumptions_table(rows: list[dict[str, str]], param_names: list[str]) -> str:
    filtered = [r for r in rows if r.get("param_name") in param_names]
    if not filtered:
        return "(aucune hypothese trouvee)\n"
    lines = ["| Parametre | Valeur | Unite | Description |", "|-----------|--------|-------|-------------|"]
    for r in filtered:
        lines.append(f"| `{r.get('param_name','')}` | {r.get('param_value','')} | {r.get('unit','')} | {r.get('description','')} |")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Read module params and docstrings
# ---------------------------------------------------------------------------
def _read_module_params(module_name: str) -> list[str]:
    """Import a Q module and return its Q*_PARAMS list."""
    try:
        import importlib
        mod = importlib.import_module(f"src.modules.{module_name}")
        for attr in dir(mod):
            if attr.endswith("_PARAMS") and attr.startswith("Q"):
                return list(getattr(mod, attr))
    except Exception:
        pass
    return []


def _read_module_docstring(module_name: str) -> str:
    try:
        import importlib
        mod = importlib.import_module(f"src.modules.{module_name}")
        return (mod.__doc__ or "").strip()
    except Exception:
        return ""


def _read_thermal_defaults() -> str:
    try:
        from src.constants import THERMAL_DEFAULTS
        lines = []
        for tech, params in THERMAL_DEFAULTS.items():
            lines.append(f"- **{tech}**: efficiency={params['efficiency']}, "
                         f"emission_factor={params['emission_factor_t_per_mwh_th']} tCO2/MWhth, "
                         f"VOM={params['vom_eur_mwh']} EUR/MWh")
        return "\n".join(lines)
    except Exception:
        return "(impossible de lire THERMAL_DEFAULTS)"


# ---------------------------------------------------------------------------
# Generate the full markdown
# ---------------------------------------------------------------------------
def generate() -> str:
    assumptions = _read_assumptions()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Q params
    q1_params = _read_module_params("q1_transition")
    q2_params = _read_module_params("q2_slope")
    q3_params = _read_module_params("q3_exit")
    q4_params = _read_module_params("q4_bess")
    q5_params = _read_module_params("q5_thermal_anchor")

    thermal = _read_thermal_defaults()

    md = f"""\
# Audit Methods Reference (Q1-Q5)

Last updated: {now}
Auto-generated from Python source code by `scripts/generate_audit_methods.py`.
Regenerated automatically when analysis engine files change.

## 1. Purpose and governance

This document is the methodological reference for formulas, data, hypotheses, and checks used by Q1-Q5 (HIST + SCEN).
It is auto-generated from the live codebase to guarantee synchronization with the analysis engine.

Authoritative code paths:

- `src/metrics.py`
- `src/modules/q1_transition.py`
- `src/modules/q2_slope.py`
- `src/modules/q3_exit.py`
- `src/modules/q4_bess.py`
- `src/modules/q5_thermal_anchor.py`
- `src/scenario/calibration.py`
- `src/scenario/phase2_engine.py`


## 2. Data sources and storage

### 2.1 Historical (HIST)

- ENTSO-E raw cache: `data/raw/entsoe/prices_da/{{country}}/{{year}}.parquet` (+ load_total, generation_by_type, net_position)
- Canonical hourly: `data/processed/hourly/{{country}}/{{year}}.parquet`
- Historical annual metrics: `data/metrics/annual_metrics.parquet`
- Historical daily metrics: `data/metrics/daily_metrics.parquet`
- Validation findings: `data/metrics/validation_findings.parquet`

### 2.2 Prospective (SCEN)

- Scenario assumptions: `data/assumptions/phase2/phase2_scenario_country_year.csv`
- Scenario hourly outputs: `data/processed/scenario/{{scenario_id}}/hourly/{{country}}/{{year}}.parquet`
- Scenario annual metrics: `data/processed/scenario/{{scenario_id}}/annual_metrics.parquet`

### 2.3 Common assumptions

- Phase 1 assumptions: `data/assumptions/phase1_assumptions.csv`
- Country config: `config/countries.yaml`
- PSR mapping: `data/static/entsoe_psr_mapping.csv`


## 3. Canonical physical and market formulas

Implementation: `src/metrics.py` and preprocessing pipeline.

### 3.1 Core hourly variables

- `gen_vre_mw = gen_solar_mw + gen_wind_on_mw + gen_wind_off_mw`
- `nrl_mw = load_mw - gen_vre_mw - gen_must_run_mw`
- `surplus_mw = max(0, -nrl_mw)`
- `exports_mw = max(net_position_mw, 0)`
- `flex_sink_observed_mw = exports_mw + flex_sink_psh_pump_mw`
- `surplus_absorbed_mw = min(surplus_mw, flex_effective_mw)`
- `surplus_unabsorbed_mw = surplus_mw - surplus_absorbed_mw`

### 3.2 Regime classification (anti-circular, no price input)

- A: `surplus_unabsorbed_mw > 0`
- B: `surplus_mw > 0` and `surplus_unabsorbed_mw == 0`
- D: `surplus_mw == 0` and `nrl_mw >= threshold_peak_mw`
- C: remaining hours

Threshold D default: `P90(nrl_mw on positive nrl)` with minimum positive-hour guard.

### 3.3 Annual metrics

- Baseload price: `mean(price_da)`
- Capture price (tech X): `sum(price * gen_X) / sum(gen_X)`
- Capture ratio vs baseload: `capture_X / baseload`
- Capture ratio vs TTL: `capture_X / ttl`
- TTL (price-based): `P95(price)` on regimes C + D
- SR (energy share): `surplus_energy / gen_primary_energy`
- FAR: `surplus_absorbed_energy / surplus_energy` (NaN if denominator = 0)
- IR: `P10(gen_must_run_mw) / P10(load_mw)`

### 3.4 Quality indicators

- Completeness: share of hours without critical missing data
- Quality flag: `OK` if completeness >= 0.98, `WARN` if >= 0.90, `FAIL` otherwise
- Regime coherence: share of hours where price aligns with expected regime pattern
- NRL-price correlation: Pearson correlation on non-missing hours


## 4. Question-by-question analytical logic

## 4.1 Q1 - Transition Phase 1 -> Phase 2

{_read_module_docstring("q1_transition")}

### Objective

Detect transition year with two independent diagnostics: market symptoms and physical stress.

### Configurable parameters (current values)

{_format_assumptions_table(assumptions, q1_params)}

### Calculations

1. `stage2_market_score` from points on: `h_negative_obs`, `h_below_5_obs`, `capture_ratio_pv_vs_ttl`, `days_spread_gt50`
2. Phase2 market condition: score >= 2, with optional non-capture signal gate (`q1_require_non_capture_signal`)
3. Physical stress flags: `sr_energy >= sr_energy_material_min`, `far_energy <= far_energy_tension_max`, `ir_p10 >= ir_p10_high_min`
4. Transition years: market transition year, physical transition year
5. Confidence penalty from coherence/completeness

### Outputs

- `Q1_country_summary`
- `Q1_year_panel`
- checks/warnings on incoherent transition signals

### Robustness

- `quality_flag == FAIL` invalidates strong conclusions
- capture-only signals are warned


## 4.2 Q2 - Phase 2 slope and drivers

{_read_module_docstring("q2_slope")}

### Objective

Estimate cannibalization slope for PV/Wind after Q1 transition, and rank drivers.

### Configurable parameters (current values)

{_format_assumptions_table(assumptions, q2_params)}

### Calculations

1. Build Phase2 subset per country (years >= transition year from Q1)
2. Regression per tech: preferred x = penetration, fallback x = `sr_energy`, y = capture ratio vs TTL
3. Estimator: OLS when data sufficient, `DELTA_2PT` directional slope when only two points
4. Driver features: mean SR/FAR/IR/TTL on phase2 subset, hourly `corr(gen_vre_mw, load_mw)`, surplus share in low-load quartile
5. Cross-country driver correlations against slope

### Outputs

- `Q2_country_slopes`
- `Q2_driver_correlations`
- robustness flag per slope (`ROBUST`, `FRAGILE`, `NON_TESTABLE`)


## 4.3 Q3 - Exit Phase 2 and inversion conditions

{_read_module_docstring("q3_exit")}

### Objective

Classify trend status and estimate static inversion orders of magnitude.

### Configurable parameters (current values)

{_format_assumptions_table(assumptions, q3_params)}

### Calculations

1. Trends on rolling window: `trend_h_negative`, `trend_capture_ratio_pv_vs_ttl`, `trend_sr_energy`, `trend_far_energy`
2. Status assignment: `degradation`, `stabilisation`, `amelioration`, `transition_partielle`, `hors_scope_stage2`
3. Counterfactuals (binary search): demand uplift `k` for SR target, must-run reduction `r` for SR target, additional absorbed energy for FAR target
4. Additional sink power proxy: `P95(surplus_unabsorbed_mw)`

### Outputs

- `Q3_status`

### Interpretation

`hors_scope_stage2` means the scenario is not stressed enough for a phase2-exit statement (explicit non-testability).


## 4.4 Q4 - BESS sizing and impact

{_read_module_docstring("q4_bess")}

### Objective

Quantify battery impact in three dispatch modes and estimate minimum sizing for target objective.

### Dispatch modes

- `SURPLUS_FIRST` (system stress absorption)
- `PRICE_ARBITRAGE_SIMPLE` (simple value spread)
- `PV_COLOCATED` (PV + storage value uplift)

### Configurable parameters (current values)

{_format_assumptions_table(assumptions, q4_params)}

### Calculations

1. Numpy dispatch simulation with daily masks
2. SOC and power constraints enforced each hour
3. Post-BESS absorbed and unabsorbed surplus recomputation
4. Frontier over grid: FAR before/after, unabsorbed energy before/after, capture uplift, price-taker revenue
5. Objective selection: `FAR_TARGET` or `SURPLUS_UNABS_TARGET`, choose minimum feasible by power then energy

### Invariants

- `0 <= SOC <= Emax`
- `charge <= Pmax`, `discharge <= Pmax`
- discharged energy <= charged energy * eta
- monotonic surplus reduction in `SURPLUS_FIRST`

### Outputs

- `Q4_sizing_summary`
- `Q4_bess_frontier`


## 4.5 Q5 - CO2/Gas thermal anchor

{_read_module_docstring("q5_thermal_anchor")}

### Objective

Measure thermal anchor behavior and sensitivities to gas/CO2 on non-surplus hours.

### Thermal defaults (from `src/constants.py`)

{thermal}

### Configurable parameters (current values)

{_format_assumptions_table(assumptions, q5_params)}

### Calculations

1. Thermal anchor: `tca = gas/eff + co2*(ef/eff) + vom`
2. Restrict to regimes C/D for comparison
3. Compute: `ttl_obs = P95(price on C/D)`, `tca_q95 = P95(tca on C/D)`, `alpha = ttl_obs - tca_q95`, `corr_cd = corr(price, tca) on C/D`
4. Sensitivities: `dTCA/dGas = 1/eff`, `dTCA/dCO2 = ef/eff`
5. CO2 required for target TTL: solve from `ttl_target = alpha + tca_q95_scenario`

### Outputs

- `Q5_summary`
- checks on derivative signs and weak/fragile anchor relation


## 5. Prospective engine (SCEN) mechanics

Main code: `src/scenario/calibration.py`, `src/scenario/phase2_engine.py`.

### 5.1 Historical calibration per country

Calibrated values include: must-run floors, export and PSH realization factors, stress penalty, regime-B price fit, C/D levels, NRL quantiles, surplus percentile scaling.

### 5.2 Prospective physical projection

1. Select historical reference year by country
2. Scale load profile to target annual demand
3. Scale VRE profiles to target capacities
4. Build must-run profiles from scenario capacities and calibrated floors/caps
5. Apply conservative flex ordering: exports sink, PSH sink, BESS sink
6. Recompute surplus absorption and unabsorbed surplus
7. Reclassify regimes (A/B/C/D) after BESS
8. Inject synthetic piecewise-affine prices with calibrated regime-B behavior


## 6. Standard evidence outputs

Per question bundle: `outputs/combined/{{run_id}}/Qx/` with summary.json, test_ledger.csv, comparison_hist_vs_scen.csv, hist/tables/*.csv, scen/{{scenario_id}}/tables/*.csv.

Status semantics: `PASS` (test passed), `WARN` (potential fragility), `FAIL` (hard inconsistency), `NON_TESTABLE` (not enough signal/data).


## 7. Known limitations

1. No full equilibrium dispatch model.
2. Scenario logic is pragmatic stress-testing, not market forecast.
3. Some question/scenario pairs can be `NON_TESTABLE` by design when stress is absent.
4. Correlations and slopes are explanatory signals, not automatic causal proof.
"""
    return md


def write() -> Path:
    """Generate and write the .md file. Returns the output path."""
    content = generate()
    OUTPUT_PATH.write_text(content, encoding="utf-8")
    return OUTPUT_PATH


def main() -> int:
    out = write()
    print(f"Generated: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
