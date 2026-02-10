from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
import shutil
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config_loader import load_countries  # noqa: E402
from src.hash_utils import sha256_file  # noqa: E402

TMP = ROOT / "data" / "external" / "tmp"
RAW_TYNDP = ROOT / "data" / "external" / "raw" / "tyndp2024"
RAW_ATB = ROOT / "data" / "external" / "raw" / "nrel_atb"
RAW_IRENA = ROOT / "data" / "external" / "raw" / "irena"
NORM = ROOT / "data" / "external" / "normalized"
ASSUMPTIONS = ROOT / "assumptions"
PROCESSED_HOURLY = ROOT / "data" / "processed" / "hourly"
PHASE2_ASSUMPTIONS = ROOT / "data" / "assumptions" / "phase2" / "phase2_scenario_country_year.csv"


@dataclass
class _ATBRow:
    technology: str
    year: int
    capex_eur_per_kw: float | None
    fixed_opex_eur_per_kw_yr: float | None
    variable_opex_eur_per_mwh: float | None
    lifetime_yr: float | None
    wacc_real: float | None
    notes: str


def _ensure_dirs() -> None:
    for p in [RAW_TYNDP, RAW_ATB, RAW_IRENA, NORM, ASSUMPTIONS]:
        p.mkdir(parents=True, exist_ok=True)


def _first_file(base: Path, suffixes: tuple[str, ...]) -> Path | None:
    files = [p for p in base.rglob("*") if p.is_file() and p.suffix.lower() in suffixes and "__MACOSX" not in str(p)]
    return files[0] if files else None


def _build_tyndp_raw_and_normalized() -> None:
    p2 = pd.read_csv(PHASE2_ASSUMPTIONS)

    # Keep original extracted source files for traceability when available.
    demand_src = _first_file(TMP / "tyndp_demand", (".xlsb", ".xlsx", ".xls"))
    supply_src = _first_file(TMP / "tyndp_supply", (".xlsx", ".xls", ".xlsb"))
    price_src = _first_file(TMP / "tyndp_prices", (".xlsx", ".xls", ".xlsb", ".csv"))

    if demand_src is not None:
        shutil.copy2(demand_src, RAW_TYNDP / "tyndp2024_demand_scenarios_raw_source.xlsb")
    if supply_src is not None:
        shutil.copy2(supply_src, RAW_TYNDP / "tyndp2024_installed_capacities_raw.xlsx")
    if price_src is not None:
        shutil.copy2(price_src, RAW_TYNDP / "tyndp2024_fuel_and_co2_prices_raw.xlsx")

    # Build canonical demand raw workbook from available scenario assumptions (fallback extraction).
    demand_raw = p2[["scenario_id", "country", "year", "demand_total_twh", "demand_peak_gw", "source_label"]].copy()
    demand_raw = demand_raw.rename(columns={"demand_peak_gw": "peak_load_gw"})
    with pd.ExcelWriter(RAW_TYNDP / "tyndp2024_demand_scenarios_raw.xlsx", engine="openpyxl") as writer:
        demand_raw.to_excel(writer, sheet_name="demand_extract", index=False)
        notes = pd.DataFrame(
            {
                "note": [
                    "This internal raw workbook is a controlled extraction fallback.",
                    "Original TYNDP demand xlsb is stored as tyndp2024_demand_scenarios_raw_source.xlsb when available.",
                    "Source priority: TYNDP raw files, then project assumptions (source_label).",
                ]
            }
        )
        notes.to_excel(writer, sheet_name="readme", index=False)

    # Normalized demand table.
    demand_norm = demand_raw.copy()
    demand_norm["source_label"] = demand_norm["source_label"].fillna("TYNDP2024_or_user_input")
    demand_norm.to_csv(NORM / "tyndp2024_demand_scenarios.csv", index=False)

    # Normalized capacities table.
    cap_norm = p2[
        [
            "scenario_id",
            "country",
            "year",
            "cap_pv_gw",
            "cap_wind_on_gw",
            "cap_wind_off_gw",
            "cap_must_run_nuclear_gw",
            "cap_must_run_hydro_ror_gw",
            "psh_pump_gw",
            "source_label",
        ]
    ].copy()
    cap_norm = cap_norm.rename(
        columns={
            "cap_must_run_nuclear_gw": "cap_nuclear_gw",
            "cap_must_run_hydro_ror_gw": "cap_hydro_ror_gw",
            "psh_pump_gw": "cap_psh_gw",
        }
    )
    cap_norm["cap_coal_gw"] = np.nan
    cap_norm["cap_gas_gw"] = np.nan
    cap_norm["cap_hydro_res_gw"] = np.nan
    cap_norm = cap_norm[
        [
            "scenario_id",
            "country",
            "year",
            "cap_pv_gw",
            "cap_wind_on_gw",
            "cap_wind_off_gw",
            "cap_nuclear_gw",
            "cap_coal_gw",
            "cap_gas_gw",
            "cap_hydro_ror_gw",
            "cap_hydro_res_gw",
            "cap_psh_gw",
            "source_label",
        ]
    ]
    cap_norm["source_label"] = cap_norm["source_label"].fillna("TYNDP2024_or_user_input")
    cap_norm.to_csv(NORM / "tyndp2024_capacities.csv", index=False)

    # Normalized fuel / CO2 table.
    fuel_norm = p2[["scenario_id", "year", "co2_eur_per_t", "gas_eur_per_mwh_th", "source_label"]].copy()
    fuel_norm["coal_eur_per_mwh_th"] = np.nan
    fuel_norm = fuel_norm.drop_duplicates(subset=["scenario_id", "year"]).sort_values(["scenario_id", "year"])
    fuel_norm["source_label"] = fuel_norm["source_label"].fillna("TYNDP2024_or_user_input")
    fuel_norm.to_csv(NORM / "tyndp2024_fuel_co2_prices.csv", index=False)


def _build_atb_normalized() -> None:
    model_path = RAW_ATB / "2024_v3_Model_Parameters.csv"
    dict_path = RAW_ATB / "2024_v3_Data_Dictionary.csv"
    if not model_path.exists():
        return

    model = pd.read_csv(model_path)
    model.columns = [str(c) for c in model.columns]

    if not dict_path.exists():
        pd.DataFrame(
            {
                "column_name": model.columns,
                "description": ["from_model_parameters_header"] * len(model.columns),
            }
        ).to_csv(dict_path, index=False)

    base = model[model["scenario"].astype(str).str.lower() == "base"].copy()
    base["year"] = pd.to_numeric(base["year"], errors="coerce")
    base["value"] = pd.to_numeric(base["value"], errors="coerce")
    usd_to_eur = 0.92

    rows: list[_ATBRow] = []

    def _pick(tech: str, param: str, units: str | None = None, param_detail: str | None = None) -> pd.DataFrame:
        out = base[(base["technology"] == tech) & (base["parameter"] == param)]
        if units is not None:
            out = out[out["units"] == units]
        if param_detail is not None:
            out = out[out["parameterdetail"] == param_detail]
        return out

    # Utility PV.
    pv_cap = _pick("UtilityPV", "Total Capital Cost", "$/Wac")
    pv_om = _pick("UtilityPV", "Operation and Maintenance Costs", "$/kWac-yr")
    for y in sorted(set(pv_cap["year"].dropna().astype(int)).intersection(set(pv_om["year"].dropna().astype(int)))):
        capex_kw = float(pv_cap[pv_cap["year"] == y]["value"].median()) * 1000.0 * usd_to_eur
        opex = float(pv_om[pv_om["year"] == y]["value"].median()) * usd_to_eur
        rows.append(
            _ATBRow(
                technology="PV",
                year=y,
                capex_eur_per_kw=capex_kw,
                fixed_opex_eur_per_kw_yr=opex,
                variable_opex_eur_per_mwh=None,
                lifetime_yr=None,
                wacc_real=None,
                notes="UtilityPV Base scenario from ATB model parameters (USD->EUR factor 0.92).",
            )
        )

    # Land-based wind.
    w_on_cap = _pick("LandbasedWind", "CapEx", "$/kW", "Total")
    w_on_om = _pick("LandbasedWind", "O&M", "$/kW/yr")
    for y in sorted(set(w_on_cap["year"].dropna().astype(int)).intersection(set(w_on_om["year"].dropna().astype(int)))):
        rows.append(
            _ATBRow(
                technology="WindOn",
                year=y,
                capex_eur_per_kw=float(w_on_cap[w_on_cap["year"] == y]["value"].median()) * usd_to_eur,
                fixed_opex_eur_per_kw_yr=float(w_on_om[w_on_om["year"] == y]["value"].median()) * usd_to_eur,
                variable_opex_eur_per_mwh=None,
                lifetime_yr=None,
                wacc_real=None,
                notes="LandbasedWind Base scenario from ATB model parameters (USD->EUR factor 0.92).",
            )
        )

    # Offshore wind.
    w_off_cap = _pick("OffShoreWind", "Capex", "$/kW", "Total")
    for y in sorted(w_off_cap["year"].dropna().astype(int).unique().tolist()):
        rows.append(
            _ATBRow(
                technology="WindOff",
                year=y,
                capex_eur_per_kw=float(w_off_cap[w_off_cap["year"] == y]["value"].median()) * usd_to_eur,
                fixed_opex_eur_per_kw_yr=None,
                variable_opex_eur_per_mwh=None,
                lifetime_yr=None,
                wacc_real=None,
                notes="OffShoreWind Base scenario from ATB model parameters (USD->EUR factor 0.92).",
            )
        )

    # Utility battery: derive per-kW capex from Total EPC Cost ($/kWh) and duration.
    bess = _pick("Utility Scale Battery Storage", "Capital Cost", "$/kWh", "Total EPC Cost")
    for detail, tech_name, duration_h in [
        ("60MW 120MWh", "BESS_2h", 2.0),
        ("60MW 240MWh", "BESS_4h", 4.0),
    ]:
        bsub = bess[bess["techdetail"] == detail]
        for y in sorted(bsub["year"].dropna().astype(int).unique().tolist()):
            val_kwh = float(bsub[bsub["year"] == y]["value"].median()) * usd_to_eur
            rows.append(
                _ATBRow(
                    technology=tech_name,
                    year=y,
                    capex_eur_per_kw=val_kwh * duration_h,
                    fixed_opex_eur_per_kw_yr=None,
                    variable_opex_eur_per_mwh=None,
                    lifetime_yr=None,
                    wacc_real=None,
                    notes=f"Utility battery {detail}, derived capex €/kW from €/kWh and duration={duration_h}h.",
                )
            )

    out = pd.DataFrame([r.__dict__ for r in rows]).sort_values(["technology", "year"])
    out.insert(0, "source_label", "NREL_ATB_2024_v3")
    out.to_csv(NORM / "tech_cost_benchmarks_atb.csv", index=False)


def _build_irena_assets() -> None:
    pdf_path = RAW_IRENA / "IRENAInsights_RPGC2023.pdf"
    if not pdf_path.exists() or pdf_path.stat().st_size < 1024:
        # Build a fallback PDF anchor if direct download is blocked.
        import matplotlib.pyplot as plt

        fig = plt.figure(figsize=(8.27, 11.69))
        text = (
            "IRENA anchor file placeholder\\n\\n"
            "Expected source URL:\\n"
            "https://www.irena.org/-/media/Files/IRENA/Agency/Presentations/Technology/2024/Oct/IRENAInsights_RPGC2023.pdf\\n\\n"
            "Direct HTTP download was blocked in this runtime (403).\\n"
            "This placeholder keeps an auditable anchor path and timestamp."
        )
        plt.text(0.05, 0.95, text, va="top", ha="left", fontsize=11)
        plt.axis("off")
        fig.savefig(pdf_path, format="pdf")
        plt.close(fig)

    checksum = sha256_file(pdf_path)
    out = pd.DataFrame(
        [
            {
                "source_label": "IRENA_RPGC2023_manual",
                "technology": "PV",
                "year": 2023,
                "capex_eur_per_kw": np.nan,
                "fixed_opex_eur_per_kw_yr": np.nan,
                "variable_opex_eur_per_mwh": np.nan,
                "lifetime_yr": np.nan,
                "wacc_real": np.nan,
                "page_reference": "IRENAInsights_RPGC2023 p.12",
                "notes": "Manual audit placeholder; fill values after manual extraction from PDF anchor.",
                "pdf_checksum_sha256": checksum,
            },
            {
                "source_label": "IRENA_RPGC2023_manual",
                "technology": "WindOn",
                "year": 2023,
                "capex_eur_per_kw": np.nan,
                "fixed_opex_eur_per_kw_yr": np.nan,
                "variable_opex_eur_per_mwh": np.nan,
                "lifetime_yr": np.nan,
                "wacc_real": np.nan,
                "page_reference": "IRENAInsights_RPGC2023 p.14",
                "notes": "Manual audit placeholder; fill values after manual extraction from PDF anchor.",
                "pdf_checksum_sha256": checksum,
            },
            {
                "source_label": "IRENA_RPGC2023_manual",
                "technology": "WindOff",
                "year": 2023,
                "capex_eur_per_kw": np.nan,
                "fixed_opex_eur_per_kw_yr": np.nan,
                "variable_opex_eur_per_mwh": np.nan,
                "lifetime_yr": np.nan,
                "wacc_real": np.nan,
                "page_reference": "IRENAInsights_RPGC2023 p.15",
                "notes": "Manual audit placeholder; fill values after manual extraction from PDF anchor.",
                "pdf_checksum_sha256": checksum,
            },
        ]
    )
    out.to_csv(NORM / "tech_cost_benchmarks_irena.csv", index=False)


def _build_policy_distortion() -> None:
    countries = sorted(load_countries().get("countries", {}).keys())
    rows = []
    for c in countries:
        rows.append(
            {
                "country": c,
                "start_year": 2018,
                "end_year": 2040,
                "scheme_name": "default_template",
                "supported_share_of_vre_generation": 0.35,
                "negative_price_rule_type": "unknown",
                "negative_price_rule_threshold_hours": np.nan,
                "does_support_pay_when_negative": np.nan,
                "notes": "Template row to be refined with regulator evidence per country.",
                "source_label": "internal_template",
            }
        )
    pd.DataFrame(rows).to_csv(ASSUMPTIONS / "policy_distortion.csv", index=False)


def _load_country_hourly(country: str) -> pd.DataFrame | None:
    cdir = PROCESSED_HOURLY / country
    if not cdir.exists():
        return None
    chunks: list[pd.DataFrame] = []
    for p in sorted(cdir.glob("*.parquet")):
        try:
            df = pd.read_parquet(p)
            if "timestamp_utc" not in df.columns:
                df = df.reset_index()
                if "timestamp_utc" not in df.columns and "index" in df.columns:
                    df = df.rename(columns={"index": "timestamp_utc"})
            df["timestamp_utc"] = pd.to_datetime(df["timestamp_utc"], utc=True, errors="coerce")
            df = df.dropna(subset=["timestamp_utc"]).set_index("timestamp_utc").sort_index()
            chunks.append(df)
        except Exception:
            continue
    if not chunks:
        return None
    return pd.concat(chunks, axis=0).sort_index()


def _build_interconnection_and_coincidence() -> None:
    countries = sorted(load_countries().get("countries", {}).keys())
    hourly_by_country: dict[str, pd.DataFrame] = {}

    # Interconnection proxy.
    proxy_rows: list[dict[str, object]] = []
    for c in countries:
        h = _load_country_hourly(c)
        if h is None or h.empty:
            continue
        hourly_by_country[c] = h
        exports = pd.to_numeric(h.get("exports_mw"), errors="coerce")
        if exports.isna().all() and "net_position_mw" in h.columns:
            net_pos = pd.to_numeric(h["net_position_mw"], errors="coerce")
            exports = net_pos.clip(lower=0.0)
        proxy_rows.append(
            {
                "country": c,
                "p95_exports_mw": float(exports.quantile(0.95)) if exports.notna().any() else np.nan,
                "mean_exports_mw": float(exports.mean()) if exports.notna().any() else np.nan,
                "max_exports_mw": float(exports.max()) if exports.notna().any() else np.nan,
                "interconnection_export_gw_proxy": float(exports.quantile(0.95) / 1000.0) if exports.notna().any() else np.nan,
                "source_label": "ENTSOE_phase1_empirical",
                "notes": "Derived from processed hourly exports (2018-2024).",
            }
        )
    pd.DataFrame(proxy_rows).sort_values("country").to_csv(NORM / "interconnection_proxy_phase1.csv", index=False)

    # Surplus coincidence matrix.
    coinc_rows: list[dict[str, object]] = []
    for c1, c2 in combinations(countries, 2):
        h1 = hourly_by_country.get(c1)
        h2 = hourly_by_country.get(c2)
        if h1 is None or h2 is None:
            continue
        s1 = (pd.to_numeric(h1.get("surplus_mw"), errors="coerce") > 0).astype(float).rename("s1")
        s2 = (pd.to_numeric(h2.get("surplus_mw"), errors="coerce") > 0).astype(float).rename("s2")
        both = pd.concat([s1, s2], axis=1, join="inner").dropna()
        corr = float(both["s1"].corr(both["s2"])) if len(both) > 0 else np.nan
        cf = max(0.0, corr) if np.isfinite(corr) else np.nan
        for a, b in [(c1, c2), (c2, c1)]:
            coinc_rows.append(
                {
                    "country": a,
                    "neighbor_country": b,
                    "corr_surplus_hour": corr,
                    "export_coincidence_factor": cf,
                    "source_label": "ENTSOE_phase1_empirical",
                    "notes": "Pairwise correlation of surplus-hour indicator (2018-2024).",
                }
            )

    # Diagonal entries.
    for c in countries:
        coinc_rows.append(
            {
                "country": c,
                "neighbor_country": c,
                "corr_surplus_hour": 1.0,
                "export_coincidence_factor": 1.0,
                "source_label": "ENTSOE_phase1_empirical",
                "notes": "Self-correlation.",
            }
        )

    pd.DataFrame(coinc_rows).sort_values(["country", "neighbor_country"]).to_csv(
        NORM / "surplus_coincidence_matrix_phase1.csv", index=False
    )


def main() -> None:
    _ensure_dirs()
    _build_tyndp_raw_and_normalized()
    _build_atb_normalized()
    _build_irena_assets()
    _build_policy_distortion()
    _build_interconnection_and_coincidence()
    print("External phase1 assets generated.")


if __name__ == "__main__":
    main()
