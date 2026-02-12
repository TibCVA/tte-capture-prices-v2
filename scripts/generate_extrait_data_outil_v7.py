from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import sys
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config_loader import load_countries


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Extrait Data Outil v7 (docx + markdown) with audited outputs and test ledger."
    )
    parser.add_argument("--run-id", required=True, help="Combined run id under outputs/combined/<run_id>.")
    parser.add_argument("--countries", default="DE,ES,FR", help="Comma-separated country scope.")
    parser.add_argument("--output-docx", default="reports/Extrait Data Outil v7.docx", help="DOCX output path.")
    parser.add_argument(
        "--output-md",
        default="reports/Extrait Data Outil v7.md",
        help="Markdown output path (same content, audit-friendly).",
    )
    return parser.parse_args()


def _read_csv(path: Path, label: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"{label} missing: {path}")
    return pd.read_csv(path)


def _to_num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def _ratio(num: pd.Series, den: pd.Series) -> pd.Series:
    den_num = _to_num(den)
    num_num = _to_num(num)
    out = pd.Series(np.nan, index=num_num.index, dtype=float)
    mask = den_num > 0
    out.loc[mask] = num_num.loc[mask] / den_num.loc[mask]
    return out


def _country_timezones() -> dict[str, str]:
    cfg = load_countries()
    out: dict[str, str] = {}
    for country, params in cfg.get("countries", {}).items():
        out[str(country)] = str(params.get("timezone", "UTC"))
    return out


def _assumption_value(df: pd.DataFrame, param_name: str, default: float = np.nan) -> float:
    if df.empty:
        return default
    m = df["param_name"].astype(str) == str(param_name)
    if not m.any():
        return default
    try:
        return float(pd.to_numeric(df.loc[m, "param_value"], errors="coerce").iloc[0])
    except Exception:
        return default


def _extract_annual_metrics_phase1(run_dir: Path, countries: list[str], tz_map: dict[str, str]) -> pd.DataFrame:
    df = _read_csv(run_dir / "Q1" / "hist" / "tables" / "Q1_year_panel.csv", "Q1_year_panel")
    df = df[df["country"].astype(str).isin(countries)].copy()
    if df.empty:
        return df

    n_hours = _to_num(df["n_hours_expected"])
    load_total_mw_avg = _to_num(df["load_total_twh"]) * 1e6 / n_hours
    psh_pumping_mw_avg = _to_num(df.get("psh_pumping_twh", pd.Series(np.nan, index=df.index))) * 1e6 / n_hours
    load_mw_avg = _to_num(df["load_net_twh"]) * 1e6 / n_hours
    gen_vre_mw_avg = _to_num(df["gen_vre_twh"]) * 1e6 / n_hours
    pv_mw_avg = _to_num(df["gen_solar_twh"]) * 1e6 / n_hours
    wind_on_mw_avg = _to_num(df["gen_wind_on_twh"]) * 1e6 / n_hours
    wind_off_mw_avg = _to_num(df["gen_wind_off_twh"]) * 1e6 / n_hours
    must_run_mw_avg = _to_num(df["gen_must_run_twh"]) * 1e6 / n_hours
    nrl_mw_avg = load_mw_avg - gen_vre_mw_avg - must_run_mw_avg

    out = pd.DataFrame(
        {
            "country": df["country"].astype(str),
            "year": _to_num(df["year"]).astype("Int64"),
            "n_hours": n_hours.astype("Int64"),
            "timezone": df["country"].astype(str).map(tz_map).fillna("UTC"),
            "coverage_price": _ratio(df["n_hours_with_price"], df["n_hours_expected"]),
            "coverage_load_total": _ratio(df["n_hours_with_load"], df["n_hours_expected"]),
            "coverage_net_position": 1.0 - _to_num(df.get("missing_share_net_position", pd.Series(np.nan, index=df.index))),
            "coverage_vre": _ratio(df["n_hours_with_vre"], df["n_hours_expected"]),
            "coverage_must_run": _ratio(df["n_hours_with_must_run"], df["n_hours_expected"]),
            "coverage_psh_pumping": _to_num(df.get("psh_pumping_coverage_share", pd.Series(np.nan, index=df.index))),
            "load_total_mw_avg": load_total_mw_avg,
            "psh_pumping_mw_avg": psh_pumping_mw_avg,
            "load_mw_avg": load_mw_avg,
            "gen_vre_mw_avg": gen_vre_mw_avg,
            "pv_mw_avg": pv_mw_avg,
            "wind_on_mw_avg": wind_on_mw_avg,
            "wind_off_mw_avg": wind_off_mw_avg,
            "must_run_mw_avg": must_run_mw_avg,
            "must_run_nuclear_mw_avg": np.nan,
            "must_run_biomass_mw_avg": np.nan,
            "must_run_ror_mw_avg": np.nan,
            "nrl_mw_avg": nrl_mw_avg,
            "surplus_mwh_total": _to_num(df.get("surplus_twh", pd.Series(np.nan, index=df.index))) * 1e6,
            "sr_energy": _to_num(df.get("sr_energy", pd.Series(np.nan, index=df.index))),
            "sr_hours": _to_num(df.get("sr_hours", pd.Series(np.nan, index=df.index))),
            "far_energy": _to_num(df.get("far_energy", pd.Series(np.nan, index=df.index))),
            "ir_p10": _to_num(df.get("ir_p10", pd.Series(np.nan, index=df.index))),
            "baseload_price_eur_mwh": _to_num(df.get("baseload_price_eur_mwh", pd.Series(np.nan, index=df.index))),
            "ttl_eur_mwh": _to_num(df.get("ttl_eur_mwh", pd.Series(np.nan, index=df.index))),
            "capture_price_pv_eur_mwh": _to_num(df.get("capture_price_pv_eur_mwh", pd.Series(np.nan, index=df.index))),
            "capture_ratio_pv": _to_num(df.get("capture_ratio_pv", pd.Series(np.nan, index=df.index))),
            "capture_ratio_pv_vs_ttl": _to_num(df.get("capture_ratio_pv_vs_ttl", pd.Series(np.nan, index=df.index))),
            "h_negative_obs": _to_num(df.get("h_negative_obs", pd.Series(np.nan, index=df.index))),
            "h_below_5_obs": _to_num(df.get("h_below_5_obs", pd.Series(np.nan, index=df.index))),
            "days_spread_gt50": _to_num(df.get("days_spread_gt50", pd.Series(np.nan, index=df.index))),
            "regime_coherence": _to_num(df.get("regime_coherence", pd.Series(np.nan, index=df.index))),
            "nrl_price_corr": _to_num(df.get("nrl_price_corr", pd.Series(np.nan, index=df.index))),
            "quality_flag": df.get("quality_flag", pd.Series("", index=df.index)).astype(str),
            "quality_notes": df.get("warnings_quality", pd.Series("", index=df.index)).fillna("").astype(str),
        }
    )
    out = out.sort_values(["country", "year"]).reset_index(drop=True)
    return out


def _extract_q1_transition_summary(run_dir: Path, countries: list[str], phase1_assumptions: pd.DataFrame) -> pd.DataFrame:
    df = _read_csv(run_dir / "Q1" / "hist" / "tables" / "Q1_country_summary.csv", "Q1_country_summary")
    df = df[df["country"].astype(str).isin(countries)].copy()
    if df.empty:
        return df

    persistence = _assumption_value(phase1_assumptions, "q1_persistence_window_years", default=np.nan)

    def _stage(row: pd.Series) -> str:
        bm = pd.to_numeric(pd.Series([row.get("bascule_year_market")]), errors="coerce").iloc[0]
        if pd.notna(bm):
            return "2"
        s1 = str(row.get("stage1_detected", "")).strip().lower()
        if s1 in {"true", "1"}:
            return "1"
        return "NA"

    out = pd.DataFrame(
        {
            "country": df["country"].astype(str),
            "transition_year": pd.to_numeric(df.get("bascule_year_market"), errors="coerce").astype("Int64"),
            "stage": df.apply(_stage, axis=1),
            "stage2_score": pd.to_numeric(df.get("stage2_market_score_at_bascule"), errors="coerce"),
            "non_capture_flags_count": (
                pd.to_numeric(df.get("low_price_flags_count_at_bascule"), errors="coerce").fillna(0.0)
                + pd.to_numeric(df.get("physical_flags_count_at_bascule"), errors="coerce").fillna(0.0)
            ).astype("Int64"),
            "reason_codes": df.get("drivers_at_bascule", pd.Series("", index=df.index)).fillna("").astype(str),
            "persistence_window_years": persistence,
            "confidence_level": pd.to_numeric(df.get("bascule_confidence"), errors="coerce"),
        }
    )
    out = out.sort_values(["country"]).reset_index(drop=True)
    return out


def _extract_q2_slope_summary(run_dir: Path, countries: list[str]) -> pd.DataFrame:
    df = _read_csv(run_dir / "Q2" / "hist" / "tables" / "Q2_country_slopes.csv", "Q2_country_slopes")
    df = df[df["country"].astype(str).isin(countries)].copy()
    if df.empty:
        return df

    def _driver_stats(row: pd.Series) -> str:
        payload = {
            "sr_energy_mean": pd.to_numeric(pd.Series([row.get("mean_sr_energy_phase2")]), errors="coerce").iloc[0],
            "far_energy_mean": pd.to_numeric(pd.Series([row.get("mean_far_energy_phase2")]), errors="coerce").iloc[0],
            "ir_p10_mean": pd.to_numeric(pd.Series([row.get("mean_ir_p10_phase2")]), errors="coerce").iloc[0],
            "ttl_mean": pd.to_numeric(pd.Series([row.get("mean_ttl_phase2")]), errors="coerce").iloc[0],
            "corr_vre_load_mean": pd.to_numeric(pd.Series([row.get("corr_vre_load_phase2")]), errors="coerce").iloc[0],
        }
        return json.dumps(payload, ensure_ascii=False)

    out = pd.DataFrame(
        {
            "country": df["country"].astype(str),
            "tech": df["tech"].astype(str),
            "x_var_used": df.get("x_axis_used", pd.Series("", index=df.index)).astype(str),
            "y_var_used": "capture_ratio_" + df["tech"].astype(str),
            "n_points": pd.to_numeric(df.get("n_points", df.get("n", pd.Series(np.nan, index=df.index))), errors="coerce").astype("Int64"),
            "years_used": df.get("years_used", pd.Series("", index=df.index)).astype(str),
            "slope": pd.to_numeric(df.get("slope"), errors="coerce"),
            "intercept": pd.to_numeric(df.get("intercept"), errors="coerce"),
            "r2": pd.to_numeric(df.get("r2"), errors="coerce"),
            "p_value": pd.to_numeric(df.get("p_value"), errors="coerce"),
            "driver_stats_phase2": df.apply(_driver_stats, axis=1),
            "slope_quality_flag": df.get("slope_quality_flag", pd.Series("", index=df.index)).astype(str),
            "slope_quality_notes": df.get("slope_quality_notes", pd.Series("", index=df.index)).astype(str),
        }
    )
    out = out.sort_values(["country", "tech"]).reset_index(drop=True)
    return out


def _extract_q3_inversion_requirements(run_dir: Path, countries: list[str], phase1_assumptions: pd.DataFrame) -> pd.DataFrame:
    df = _read_csv(run_dir / "Q3" / "hist" / "tables" / "Q3_status.csv", "Q3_status")
    df = df[df["country"].astype(str).isin(countries)].copy()
    if df.empty:
        return df

    target_sr = _assumption_value(phase1_assumptions, "stage1_sr_hours_max", default=np.nan)
    target_h_negative = _assumption_value(phase1_assumptions, "stage1_h_negative_max", default=np.nan)

    rows: list[dict[str, Any]] = []
    for _, row in df.iterrows():
        country = str(row.get("country", ""))
        in_phase2 = str(row.get("in_phase2", "")).strip().lower() in {"true", "1"}
        applicability = "APPLICABLE" if in_phase2 else "NA"
        demand_status = str(row.get("inversion_k_demand_status", "")).strip().lower()
        flex_status = str(row.get("inversion_f_flex_status", "")).strip().lower()
        within_demand = demand_status in {"ok", "already_not_phase2_stress", "proxy_from_surplus_gap"}
        within_flex = flex_status in {"ok", "already_not_phase2_stress", "proxy_from_surplus_gap"}

        rows.append(
            {
                "country": country,
                "lever": "demand_uplift",
                "required_uplift": pd.to_numeric(pd.Series([row.get("inversion_k_demand")]), errors="coerce").iloc[0],
                "within_bounds": bool(within_demand),
                "target_sr": target_sr,
                "target_h_negative": target_h_negative,
                "predicted_sr_after": np.nan,
                "predicted_h_negative_after": np.nan,
                "applicability_flag": applicability,
            }
        )
        rows.append(
            {
                "country": country,
                "lever": "export_uplift",
                "required_uplift": np.nan,
                "within_bounds": False,
                "target_sr": target_sr,
                "target_h_negative": target_h_negative,
                "predicted_sr_after": np.nan,
                "predicted_h_negative_after": np.nan,
                "applicability_flag": applicability,
            }
        )
        rows.append(
            {
                "country": country,
                "lever": "flex_uplift",
                "required_uplift": pd.to_numeric(pd.Series([row.get("inversion_f_flex")]), errors="coerce").iloc[0],
                "within_bounds": bool(within_flex),
                "target_sr": target_sr,
                "target_h_negative": target_h_negative,
                "predicted_sr_after": np.nan,
                "predicted_h_negative_after": np.nan,
                "applicability_flag": applicability,
            }
        )

    out = pd.DataFrame(rows)
    out = out.sort_values(["country", "lever"]).reset_index(drop=True)
    return out


def _load_q4_frontier_tables(run_dir: Path) -> pd.DataFrame:
    paths: list[Path] = [run_dir / "Q4" / "hist" / "tables" / "Q4_bess_frontier.csv"]
    scen_root = run_dir / "Q4" / "scen"
    if scen_root.exists():
        for scen_dir in sorted([p for p in scen_root.iterdir() if p.is_dir()]):
            paths.append(scen_dir / "tables" / "Q4_bess_frontier.csv")
    frames: list[pd.DataFrame] = []
    for p in paths:
        if p.exists():
            frames.append(pd.read_csv(p))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def _extract_q4_bess_sizing_curve(run_dir: Path, countries: list[str]) -> pd.DataFrame:
    df = _load_q4_frontier_tables(run_dir)
    if df.empty:
        return df
    df = df[df["country"].astype(str).isin(countries)].copy()
    if df.empty:
        return df

    power_mw = pd.to_numeric(df.get("bess_power_mw_test", df.get("bess_power_mw")), errors="coerce")
    energy_mwh = pd.to_numeric(df.get("bess_energy_mwh_test", df.get("bess_energy_mwh")), errors="coerce")
    discharge_sum = pd.to_numeric(df.get("discharge_sum_mwh"), errors="coerce")

    cycles = pd.Series(np.nan, index=df.index, dtype=float)
    valid_cycles = energy_mwh > 0
    cycles.loc[valid_cycles] = discharge_sum.loc[valid_cycles] / energy_mwh.loc[valid_cycles] / 365.0

    soc_min = pd.to_numeric(df.get("soc_min"), errors="coerce")
    soc_max = pd.to_numeric(df.get("soc_max"), errors="coerce")
    sim_cd = pd.to_numeric(df.get("simultaneous_charge_discharge_hours"), errors="coerce").fillna(0.0)
    charge_violation = pd.to_numeric(df.get("charge_vs_surplus_violation_hours"), errors="coerce").fillna(0.0)
    physics_ok = (soc_min >= -1e-9) & (soc_max <= (energy_mwh.fillna(0.0) + 1e-6)) & (sim_cd <= 0.0) & (charge_violation <= 0.0)

    df["_power_mw"] = power_mw
    df["_surplus_after"] = pd.to_numeric(df.get("surplus_unabs_energy_after"), errors="coerce")
    mono_ok = pd.Series(True, index=df.index)
    group_cols = ["scenario_id", "country", "year", "dispatch_mode"]
    for _, g in df.groupby(group_cols):
        g2 = g.sort_values("_power_mw")
        diffs = g2["_surplus_after"].diff().dropna()
        ok = bool((diffs <= 1e-9).all())
        mono_ok.loc[g2.index] = ok

    out = pd.DataFrame(
        {
            "country": df["country"].astype(str),
            "scenario_id": df.get("scenario_id", pd.Series("", index=df.index)).astype(str),
            "year": pd.to_numeric(df.get("year"), errors="coerce").astype("Int64"),
            "bess_power_gw": power_mw / 1000.0,
            "bess_energy_gwh": energy_mwh / 1000.0,
            "cycles_assumed_per_day": cycles,
            "eta_roundtrip": pd.to_numeric(df.get("eta_roundtrip"), errors="coerce"),
            "far_energy_after": pd.to_numeric(df.get("far_after"), errors="coerce"),
            "surplus_unabsorbed_twh_after": pd.to_numeric(df.get("surplus_unabs_energy_after"), errors="coerce"),
            "h_negative_after": pd.to_numeric(df.get("h_negative_after"), errors="coerce"),
            "monotonicity_check_flag": np.where(mono_ok, "PASS", "FAIL"),
            "physics_check_flag": np.where(physics_ok, "PASS", "FAIL"),
            "notes": (
                "dispatch_mode="
                + df.get("dispatch_mode", pd.Series("", index=df.index)).astype(str)
                + "; objective="
                + df.get("objective", pd.Series("", index=df.index)).astype(str)
            ),
        }
    )
    out = out.sort_values(["country", "scenario_id", "year", "bess_power_gw", "bess_energy_gwh"]).reset_index(drop=True)
    return out


def _load_q5_summary_tables(run_dir: Path) -> pd.DataFrame:
    paths: list[Path] = [run_dir / "Q5" / "hist" / "tables" / "Q5_summary.csv"]
    scen_root = run_dir / "Q5" / "scen"
    if scen_root.exists():
        for scen_dir in sorted([p for p in scen_root.iterdir() if p.is_dir()]):
            paths.append(scen_dir / "tables" / "Q5_summary.csv")
    frames: list[pd.DataFrame] = []
    for p in paths:
        if p.exists():
            frames.append(pd.read_csv(p))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def _extract_q5_anchor_sensitivity(run_dir: Path, countries: list[str]) -> pd.DataFrame:
    df = _load_q5_summary_tables(run_dir)
    if df.empty:
        return df
    df = df[df["country"].astype(str).isin(countries)].copy()
    if df.empty:
        return df

    year = pd.to_numeric(df.get("ttl_reference_year"), errors="coerce").astype("Int64")
    tca = pd.to_numeric(df.get("tca_q95"), errors="coerce")
    ttl = pd.to_numeric(df.get("ttl_anchor"), errors="coerce")
    gas = pd.to_numeric(df.get("assumed_gas_price_eur_mwh_th"), errors="coerce")
    co2 = pd.to_numeric(df.get("assumed_co2_price_eur_t"), errors="coerce")

    out = pd.DataFrame(
        {
            "country": df["country"].astype(str),
            "scenario_id": df.get("scenario_id", pd.Series("", index=df.index)).astype(str),
            "year": year,
            "gas_eur_per_mwh_th": gas,
            "co2_eur_per_t": co2,
            "tca_ccgt_eur_mwh": tca,
            "tca_coal_eur_mwh": np.nan,
            "ttl_eur_mwh": ttl,
        }
    )

    base = out[out["scenario_id"].astype(str).str.upper() == "BASE"][["country", "year", "tca_ccgt_eur_mwh", "ttl_eur_mwh"]].copy()
    base = base.rename(
        columns={
            "tca_ccgt_eur_mwh": "tca_ccgt_base",
            "ttl_eur_mwh": "ttl_base",
        }
    )
    out = out.merge(base, on=["country", "year"], how="left")
    out["delta_ttl_vs_base"] = out["ttl_eur_mwh"] - out["ttl_base"]
    out["delta_tca_vs_base"] = out["tca_ccgt_eur_mwh"] - out["tca_ccgt_base"]

    scen_upper = out["scenario_id"].astype(str).str.upper()
    cond_high = scen_upper.isin(["HIGH_CO2", "HIGH_GAS"])
    monotone_ok = (~cond_high) | (out["tca_ccgt_eur_mwh"] >= out["tca_ccgt_base"])
    sign_ok = (
        out["delta_ttl_vs_base"].fillna(0.0).apply(np.sign)
        == out["delta_tca_vs_base"].fillna(0.0).apply(np.sign)
    ) | (out["delta_ttl_vs_base"].fillna(0.0) == 0.0) | (out["delta_tca_vs_base"].fillna(0.0) == 0.0)
    out["coherence_flag"] = np.where(monotone_ok & sign_ok, "PASS", np.where(monotone_ok, "WARN", "FAIL"))

    keep_cols = [
        "country",
        "scenario_id",
        "year",
        "gas_eur_per_mwh_th",
        "co2_eur_per_t",
        "tca_ccgt_eur_mwh",
        "tca_coal_eur_mwh",
        "ttl_eur_mwh",
        "delta_ttl_vs_base",
        "coherence_flag",
    ]
    out = out[keep_cols].sort_values(["country", "scenario_id", "year"]).reset_index(drop=True)
    return out


def _extract_country_year(msg: str) -> tuple[str, str]:
    text = str(msg or "")
    m = re.search(r"\b([A-Z_]{2,})[- ](\d{4})\b", text)
    if m:
        return m.group(1), m.group(2)
    return "", ""


def _build_test_ledger(run_dir: Path, countries: list[str]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for qid in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        tl_path = run_dir / qid / "test_ledger.csv"
        if tl_path.exists():
            tl = pd.read_csv(tl_path)
            for _, r in tl.iterrows():
                rows.append(
                    {
                        "test_id": str(r.get("test_id", "")),
                        "scope": str(r.get("question_id", qid)),
                        "country": "",
                        "year": "",
                        "scenario_id": str(r.get("scenario_id", "")),
                        "status": str(r.get("status", "")),
                        "metric_name": str(r.get("title", "")),
                        "observed_value": str(r.get("value", "")),
                        "expected_rule": str(r.get("metric_rule", "")),
                        "message": str(r.get("interpretation", "")),
                    }
                )

        summary_path = run_dir / qid / "summary.json"
        if summary_path.exists():
            summary = json.loads(summary_path.read_text(encoding="utf-8"))
            for c in summary.get("checks", []):
                msg = str(c.get("message", ""))
                country, year = _extract_country_year(msg)
                if country and country not in countries:
                    continue
                rows.append(
                    {
                        "test_id": str(c.get("code", "")),
                        "scope": qid,
                        "country": country,
                        "year": year,
                        "scenario_id": str(c.get("scenario_id", "")),
                        "status": str(c.get("status", "")),
                        "metric_name": str(c.get("code", "")),
                        "observed_value": "",
                        "expected_rule": "",
                        "message": msg,
                    }
                )

    ledger = pd.DataFrame(rows)
    if not ledger.empty:
        ledger = ledger.sort_values(["scope", "test_id", "country", "year", "scenario_id"]).reset_index(drop=True)
    return ledger


def _df_csv_block(df: pd.DataFrame) -> str:
    return f"```csv\n{df.to_csv(index=False).rstrip()}\n```"


def _assert_non_empty(outputs: dict[str, pd.DataFrame]) -> None:
    for name, df in outputs.items():
        if df.empty:
            raise ValueError(f"{name} is empty or not computed; export aborted.")


def _add_csv_block_to_doc(doc: Any, title: str, df: pd.DataFrame) -> None:
    doc.add_heading(title, level=2)
    doc.add_paragraph("```csv")
    csv_text = df.to_csv(index=False).rstrip().splitlines()
    for line in csv_text:
        doc.add_paragraph(line)
    doc.add_paragraph("```")


def generate_extrait(run_id: str, countries: list[str], output_docx: Path, output_md: Path) -> dict[str, Any]:
    run_dir = ROOT / "outputs" / "combined" / run_id
    if not run_dir.exists():
        raise FileNotFoundError(f"Run directory not found: {run_dir}")

    phase1_assumptions = _read_csv(ROOT / "data" / "assumptions" / "phase1_assumptions.csv", "phase1_assumptions")
    phase2_assumptions = _read_csv(
        ROOT / "data" / "assumptions" / "phase2" / "phase2_scenario_country_year.csv",
        "phase2_scenario_country_year",
    )
    phase2_scope = phase2_assumptions[phase2_assumptions["country"].astype(str).isin(countries)].copy()
    tz_map = _country_timezones()

    annual_metrics_phase1 = _extract_annual_metrics_phase1(run_dir, countries, tz_map)
    q1_transition_summary = _extract_q1_transition_summary(run_dir, countries, phase1_assumptions)
    q2_slope_summary = _extract_q2_slope_summary(run_dir, countries)
    q3_inversion_requirements = _extract_q3_inversion_requirements(run_dir, countries, phase1_assumptions)
    q4_bess_sizing_curve = _extract_q4_bess_sizing_curve(run_dir, countries)
    q5_anchor_sensitivity = _extract_q5_anchor_sensitivity(run_dir, countries)
    test_ledger = _build_test_ledger(run_dir, countries)

    outputs = {
        "annual_metrics_phase1": annual_metrics_phase1,
        "q1_transition_summary": q1_transition_summary,
        "q2_slope_summary": q2_slope_summary,
        "q3_inversion_requirements": q3_inversion_requirements,
        "q4_bess_sizing_curve": q4_bess_sizing_curve,
        "q5_anchor_sensitivity": q5_anchor_sensitivity,
        "test_ledger": test_ledger,
    }
    _assert_non_empty(outputs)

    q1_summary = json.loads((run_dir / "Q1" / "summary.json").read_text(encoding="utf-8"))
    meta = {
        "run_id": run_id,
        "run_dir": str(run_dir),
        "countries": countries,
        "hist_years": q1_summary.get("selection", {}).get("years", []),
        "scenario_years": q1_summary.get("selection", {}).get("scenario_years", []),
        "scenarios": q1_summary.get("selection", {}).get("scenario_ids", []),
        "method_reference": "AUDIT_METHODS_Q1_Q5.md",
    }

    lines: list[str] = []
    lines.append("# Extrait Data Outil v7")
    lines.append("")
    lines.append("## AUDIT PAYLOAD")
    lines.append("")
    lines.append("### Inputs")
    lines.append("")
    lines.append("#### run_metadata")
    lines.append("```json")
    lines.append(json.dumps(meta, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    lines.append("#### Method Reference")
    lines.append("```text")
    lines.append(str(ROOT / "AUDIT_METHODS_Q1_Q5.md"))
    lines.append("```")
    lines.append("")
    lines.append("#### parameter_catalog")
    lines.append(_df_csv_block(phase1_assumptions))
    lines.append("")
    lines.append("#### Phase 2 assumptions")
    lines.append(_df_csv_block(phase2_scope))
    lines.append("")
    lines.append("## RUN OUTPUTS")
    lines.append("")
    lines.append("### A.1 annual_metrics_phase1")
    lines.append(_df_csv_block(annual_metrics_phase1))
    lines.append("")
    lines.append("### A.2 q1_transition_summary")
    lines.append(_df_csv_block(q1_transition_summary))
    lines.append("")
    lines.append("### A.3 q2_slope_summary")
    lines.append(_df_csv_block(q2_slope_summary))
    lines.append("")
    lines.append("### A.4 q3_inversion_requirements")
    lines.append(_df_csv_block(q3_inversion_requirements))
    lines.append("")
    lines.append("### A.5 q4_bess_sizing_curve")
    lines.append(_df_csv_block(q4_bess_sizing_curve))
    lines.append("")
    lines.append("### A.6 q5_anchor_sensitivity")
    lines.append(_df_csv_block(q5_anchor_sensitivity))
    lines.append("")
    lines.append("## TEST LEDGER")
    lines.append("")
    lines.append(_df_csv_block(test_ledger))
    lines.append("")

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text("\n".join(lines), encoding="utf-8")

    try:
        from docx import Document
    except Exception as exc:
        raise RuntimeError(f"python-docx unavailable: {exc}") from exc

    doc = Document()
    doc.add_heading("Extrait Data Outil v7", level=0)
    doc.add_heading("AUDIT PAYLOAD", level=1)
    doc.add_heading("Inputs", level=2)
    doc.add_heading("run_metadata", level=3)
    doc.add_paragraph("```json")
    for line in json.dumps(meta, ensure_ascii=False, indent=2).splitlines():
        doc.add_paragraph(line)
    doc.add_paragraph("```")

    doc.add_heading("Method Reference", level=3)
    doc.add_paragraph("```text")
    doc.add_paragraph(str(ROOT / "AUDIT_METHODS_Q1_Q5.md"))
    doc.add_paragraph("```")

    _add_csv_block_to_doc(doc, "parameter_catalog", phase1_assumptions)
    _add_csv_block_to_doc(doc, "Phase 2 assumptions", phase2_scope)

    doc.add_heading("RUN OUTPUTS", level=1)
    _add_csv_block_to_doc(doc, "A.1 annual_metrics_phase1", annual_metrics_phase1)
    _add_csv_block_to_doc(doc, "A.2 q1_transition_summary", q1_transition_summary)
    _add_csv_block_to_doc(doc, "A.3 q2_slope_summary", q2_slope_summary)
    _add_csv_block_to_doc(doc, "A.4 q3_inversion_requirements", q3_inversion_requirements)
    _add_csv_block_to_doc(doc, "A.5 q4_bess_sizing_curve", q4_bess_sizing_curve)
    _add_csv_block_to_doc(doc, "A.6 q5_anchor_sensitivity", q5_anchor_sensitivity)

    doc.add_heading("TEST LEDGER", level=1)
    doc.add_paragraph("```csv")
    for line in test_ledger.to_csv(index=False).rstrip().splitlines():
        doc.add_paragraph(line)
    doc.add_paragraph("```")

    output_docx.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_docx))

    return {
        "run_id": run_id,
        "countries": countries,
        "output_docx": str(output_docx),
        "output_md": str(output_md),
        "rows": {k: int(len(v)) for k, v in outputs.items()},
    }


def main() -> int:
    args = _parse_args()
    countries = [c.strip() for c in str(args.countries).split(",") if c.strip()]
    result = generate_extrait(
        run_id=str(args.run_id),
        countries=countries,
        output_docx=Path(args.output_docx),
        output_md=Path(args.output_md),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
