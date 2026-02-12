"""Validators for phase2 scenario assumptions."""

from __future__ import annotations

from typing import Any

import pandas as pd


PHASE2_REQUIRED_COLUMNS = [
    "scenario_id",
    "country",
    "year",
    "demand_total_twh",
    "demand_peak_gw",
    "demand_shape_reference",
    "cap_pv_gw",
    "cap_wind_on_gw",
    "cap_wind_off_gw",
    "cap_must_run_nuclear_gw",
    "cap_must_run_chp_gw",
    "cap_must_run_biomass_gw",
    "cap_must_run_hydro_ror_gw",
    "must_run_min_output_factor",
    "interconnection_export_gw",
    "export_coincidence_factor",
    "psh_pump_gw",
    "bess_power_gw",
    "bess_energy_gwh",
    "bess_eta_roundtrip",
    "co2_eur_per_t",
    "gas_eur_per_mwh_th",
    "marginal_tech",
    "marginal_efficiency",
    "marginal_emission_factor_t_per_mwh",
    "supported_vre_share",
    "negative_price_rule",
    "negative_price_rule_threshold_hours",
    "price_exposure_share",
    "source_label",
    "notes",
]

SCENARIO_UNITARY_IDS = {"HIGH_CO2", "HIGH_GAS", "DEMAND_UP", "LOW_RIGIDITY"}
SCENARIO_NON_CONFOUNDING_MAX_FIELDS = 3
SCENARIO_DIFF_EXCLUDED_COLUMNS = {"source_label", "notes"}


def _to_num(df: pd.DataFrame, col: str) -> pd.Series:
    return pd.to_numeric(df[col], errors="coerce")


def _value_changed(base_value: Any, scen_value: Any, tol: float = 1e-9) -> bool:
    if pd.isna(base_value) and pd.isna(scen_value):
        return False
    base_num = pd.to_numeric(pd.Series([base_value]), errors="coerce").iloc[0]
    scen_num = pd.to_numeric(pd.Series([scen_value]), errors="coerce").iloc[0]
    if pd.notna(base_num) and pd.notna(scen_num):
        return abs(float(base_num) - float(scen_num)) > tol
    return str(base_value) != str(scen_value)


def _run_non_confounding_check(df: pd.DataFrame) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    scenario_col = df["scenario_id"].astype(str).str.upper()
    base_df = df.loc[scenario_col == "BASE"].copy()
    if base_df.empty:
        findings.append(
            {
                "severity": "WARN",
                "code": "TEST_SCEN_001",
                "message": "BASE scenario absent: non-confounding check skipped.",
            }
        )
        return findings

    compare_cols = [c for c in df.columns if c not in {"scenario_id", "country", "year"} | SCENARIO_DIFF_EXCLUDED_COLUMNS]
    scenario_ids = sorted(set(scenario_col.unique()) - {"BASE"})
    if not scenario_ids:
        findings.append(
            {
                "severity": "WARN",
                "code": "TEST_SCEN_001",
                "message": "No non-BASE scenarios available for non-confounding check.",
            }
        )
        return findings

    had_violation = False
    for scen_id in scenario_ids:
        scen_df = df.loc[scenario_col == scen_id].copy()
        merged = scen_df.merge(
            base_df,
            on=["country", "year"],
            how="left",
            suffixes=("_scen", "_base"),
        )
        missing_base = int(merged[[f"{compare_cols[0]}_base"]].isna().all(axis=1).sum()) if compare_cols else 0
        if missing_base > 0:
            findings.append(
                {
                    "severity": "WARN",
                    "code": "TEST_SCEN_001",
                    "message": f"{scen_id}: {missing_base} row(s) have no BASE match on (country, year).",
                }
            )

        changed_counts: list[int] = []
        changed_field_counter = {col: 0 for col in compare_cols}
        for _, row in merged.iterrows():
            row_changed = 0
            for col in compare_cols:
                scen_value = row.get(f"{col}_scen")
                base_value = row.get(f"{col}_base")
                changed = _value_changed(base_value, scen_value)
                if changed:
                    row_changed += 1
                    changed_field_counter[col] += 1
            changed_counts.append(row_changed)

        max_changed = int(max(changed_counts)) if changed_counts else 0
        mean_changed = float(sum(changed_counts) / len(changed_counts)) if changed_counts else 0.0
        top_changed = sorted(changed_field_counter.items(), key=lambda kv: kv[1], reverse=True)
        top_changed = [f"{name}:{count}" for name, count in top_changed if count > 0][:5]
        top_changed_text = ", ".join(top_changed) if top_changed else "none"

        if scen_id in SCENARIO_UNITARY_IDS and max_changed > SCENARIO_NON_CONFOUNDING_MAX_FIELDS:
            had_violation = True
            findings.append(
                {
                    "severity": "ERROR",
                    "code": "TEST_SCEN_001",
                    "message": (
                        f"{scen_id}: max changed fields vs BASE={max_changed} "
                        f"(limit={SCENARIO_NON_CONFOUNDING_MAX_FIELDS}); top={top_changed_text}"
                    ),
                }
            )
        elif max_changed > SCENARIO_NON_CONFOUNDING_MAX_FIELDS:
            findings.append(
                {
                    "severity": "WARN",
                    "code": "TEST_SCEN_001",
                    "message": (
                        f"{scen_id}: max changed fields vs BASE={max_changed}; top={top_changed_text}"
                    ),
                }
            )
        else:
            findings.append(
                {
                    "severity": "PASS",
                    "code": "TEST_SCEN_001",
                    "message": (
                        f"{scen_id}: non-confounding OK "
                        f"(max={max_changed}, mean={mean_changed:.2f}, limit={SCENARIO_NON_CONFOUNDING_MAX_FIELDS})."
                    ),
                }
            )

    if not had_violation and not findings:
        findings.append(
            {
                "severity": "PASS",
                "code": "TEST_SCEN_001",
                "message": "Non-confounding check passed.",
            }
        )
    return findings


def validate_phase2_assumptions(df: pd.DataFrame) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    missing = [c for c in PHASE2_REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        findings.append(
            {
                "severity": "ERROR",
                "code": "P2_MISSING_COLUMNS",
                "message": f"Missing columns: {missing}",
            }
        )
        return findings

    if df.empty:
        findings.append({"severity": "ERROR", "code": "P2_EMPTY", "message": "Phase2 assumptions table is empty"})
        return findings

    dup = df.duplicated(subset=["scenario_id", "country", "year"]).sum()
    if int(dup) > 0:
        findings.append({"severity": "ERROR", "code": "P2_DUP_KEY", "message": f"Duplicate keys: {int(dup)}"})

    # Trajectory quality checks (advisory, non-blocking).
    year_num = pd.to_numeric(df["year"], errors="coerce")
    traj_df = df.copy()
    traj_df["__year_num"] = year_num
    for (scenario_id, country), gp in traj_df.groupby(["scenario_id", "country"], dropna=False):
        years = sorted(gp["__year_num"].dropna().astype(int).unique().tolist())
        label = f"{scenario_id}/{country}"
        if len(years) < 3:
            findings.append(
                {
                    "severity": "WARN",
                    "code": "P2_TRAJECTORY_SPARSE",
                    "message": f"{label}: trajectory too sparse ({len(years)} years).",
                }
            )
        if len(years) >= 2:
            gaps = [b - a for a, b in zip(years[:-1], years[1:])]
            max_gap = max(gaps)
            if max_gap > 1:
                findings.append(
                    {
                        "severity": "WARN",
                        "code": "P2_TRAJECTORY_GAPS",
                        "message": f"{label}: trajectory has year gaps (max_gap={max_gap}).",
                    }
                )

    bounded_01 = [
        "must_run_min_output_factor",
        "export_coincidence_factor",
        "bess_eta_roundtrip",
        "supported_vre_share",
        "price_exposure_share",
    ]
    for col in bounded_01:
        s = _to_num(df, col)
        bad = int((s.notna() & ((s < 0) | (s > 1))).sum())
        if bad > 0:
            findings.append({"severity": "ERROR", "code": "P2_RANGE_01", "message": f"{col} out of [0,1]: {bad}"})

    positive_cols = [
        "demand_total_twh",
        "cap_pv_gw",
        "cap_wind_on_gw",
        "interconnection_export_gw",
        "bess_power_gw",
        "bess_energy_gwh",
        "co2_eur_per_t",
        "gas_eur_per_mwh_th",
    ]
    for col in positive_cols:
        s = _to_num(df, col)
        bad = int((s.notna() & (s < 0)).sum())
        if bad > 0:
            findings.append({"severity": "ERROR", "code": "P2_NEG_VALUE", "message": f"{col} negative values: {bad}"})

    tech_allowed = {"gas_ccgt", "coal", "mixed"}
    bad_tech = int((~df["marginal_tech"].astype(str).str.lower().isin(tech_allowed)).sum())
    if bad_tech > 0:
        findings.append({"severity": "WARN", "code": "P2_UNKNOWN_TECH", "message": f"Unknown marginal_tech rows: {bad_tech}"})

    rules_allowed = {"none", "support_suspension", "curtailment_trigger"}
    bad_rules = int((~df["negative_price_rule"].astype(str).str.lower().isin(rules_allowed)).sum())
    if bad_rules > 0:
        findings.append({"severity": "WARN", "code": "P2_UNKNOWN_RULE", "message": f"Unknown negative_price_rule rows: {bad_rules}"})

    findings.extend(_run_non_confounding_check(df))

    if not findings:
        findings.append({"severity": "PASS", "code": "P2_OK", "message": "Phase2 assumptions validation passed"})
    return findings
