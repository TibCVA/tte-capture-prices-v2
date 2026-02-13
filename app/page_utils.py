"""UI helpers for Streamlit pages."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys

import pandas as pd
import streamlit as st

from src.config_loader import load_countries, load_phase2_assumptions
from src.hash_utils import hash_object
from src.modules.bundle_result import QuestionBundleResult
from src.modules.question_bundle_runner import run_question_bundle
from src.modules.result import ModuleResult
from src.pipeline import build_country_year, load_assumptions_table
from src.scenario.phase2_engine import run_phase2_scenario
from src.storage import (
    hourly_output_path,
    load_hourly,
    load_scenario_annual_metrics,
    load_scenario_hourly,
    load_scenario_validation_findings,
)
try:
    from src.reporting.evidence_loader import (
        load_question_bundle_from_combined_run_verified as _load_question_bundle_from_combined_run_verified,
        validate_combined_run,
    )
except Exception:
    _load_question_bundle_from_combined_run_verified = None  # type: ignore[assignment]
    validate_combined_run = None  # type: ignore[assignment]

APP_ROOT = Path(__file__).resolve().parents[1]


def _to_abs_project_path(path_like: str | Path) -> Path:
    """Resolve a project-relative path relative to APP_ROOT."""
    base_path = Path(path_like)
    return base_path if base_path.is_absolute() else APP_ROOT / base_path


def _mtime_ns(path: Path) -> int:
    return int(path.stat().st_mtime_ns)


@st.cache_data(show_spinner=False)
def _read_parquet_cached(path_str: str, mtime_ns: int) -> pd.DataFrame:
    _ = mtime_ns
    return pd.read_parquet(path_str)


@st.cache_data(show_spinner=False)
def _read_csv_cached(path_str: str, mtime_ns: int) -> pd.DataFrame:
    _ = mtime_ns
    return pd.read_csv(path_str)


@st.cache_data(show_spinner=False)
def _load_hourly_cached(country: str, year: int, mtime_ns: int) -> pd.DataFrame:
    _ = mtime_ns
    return load_hourly(country, year)


def country_year_selector(default_country: str = "FR", default_year: int = 2024) -> tuple[str, int]:
    countries_cfg = load_countries()
    country_list = sorted(countries_cfg["countries"].keys())
    c = st.selectbox(
        "Pays",
        country_list,
        index=country_list.index(default_country) if default_country in country_list else 0,
    )
    years = list(range(2018, 2025))
    y = st.selectbox(
        "Annee",
        years,
        index=years.index(default_year) if default_year in years else len(years) - 1,
    )
    return c, y


def run_pipeline_ui(country: str, year: int) -> dict | None:
    with st.form("pipeline_form"):
        col1, col2 = st.columns(2)
        with col1:
            use_cache = st.checkbox("Utiliser cache gele", value=True)
        with col2:
            force_refresh = st.checkbox("Force refresh ENTSO-E", value=False)
        submit = st.form_submit_button("Charger / recalculer", type="primary")

    if submit:
        with st.spinner("Calcul en cours..."):
            res = build_country_year(country, year, force_refresh=force_refresh, use_cache_only=use_cache)
        st.success("Pipeline termine")
        st.write(res)
        return res
    return None


def all_configured_countries() -> list[str]:
    countries_cfg = load_countries()
    return sorted(str(c) for c in countries_cfg.get("countries", {}).keys())


def _extract_run_id_from_stdout(stdout: str) -> str:
    match = re.search(r"^RUN_ID\s+(\S+)", stdout, flags=re.MULTILINE)
    if not match:
        raise RuntimeError("RUN_ID introuvable dans la sortie de build_full_combined_run.py")
    return str(match.group(1)).strip()


def refresh_all_analyses_no_cache_ui(
    countries: list[str] | None = None,
    hist_year_start: int = 2018,
    hist_year_end: int = 2024,
    scenario_years: list[int] | None = None,
) -> dict[str, object]:
    selected_countries = [str(c) for c in (countries or all_configured_countries()) if str(c).strip()]
    if not selected_countries:
        raise ValueError("Aucun pays selectionne pour le refresh global.")

    hist_years = list(range(int(hist_year_start), int(hist_year_end) + 1))
    if not hist_years:
        raise ValueError("Fenetre historique invalide.")

    scen_years = [int(y) for y in (scenario_years or list(range(2025, 2036)))]
    if not scen_years:
        raise ValueError("Aucune annee scenario selectionnee.")

    total_jobs = len(selected_countries) * len(hist_years)
    hard_error_total = 0

    progress = st.progress(0.0)
    status = st.empty()

    done = 0
    for country in selected_countries:
        for year in hist_years:
            done += 1
            status.text(f"Recalcul historique {country}-{year} ({done}/{total_jobs}) via raw ENTSO-E local")
            result = build_country_year(
                country=country,
                year=year,
                force_refresh=False,
                use_cache_only=True,
            )
            hard_error_total += int(result.get("hard_error_count", 0))
            progress.progress(done / total_jobs)

    status.text("Execution du run combine Q1..Q5...")
    cmd = [
        sys.executable,
        "scripts/build_full_combined_run.py",
        "--countries",
        ",".join(selected_countries),
        "--hist-year-start",
        str(hist_year_start),
        "--hist-year-end",
        str(hist_year_end),
        "--scenario-years",
        ",".join(str(y) for y in scen_years),
    ]
    proc = subprocess.run(
        cmd,
        cwd=str(APP_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        stderr_tail = (proc.stderr or "").strip()
        stdout_tail = (proc.stdout or "").strip()
        raise RuntimeError(
            "Echec build_full_combined_run.py\n"
            + f"Command: {' '.join(cmd)}\n"
            + f"STDOUT:\n{stdout_tail}\nSTDERR:\n{stderr_tail}"
        )

    run_id = _extract_run_id_from_stdout(proc.stdout or "")
    progress.progress(1.0)
    status.empty()
    progress.empty()

    st.cache_data.clear()

    return {
        "run_id": run_id,
        "countries": selected_countries,
        "hist_year_start": int(hist_year_start),
        "hist_year_end": int(hist_year_end),
        "scenario_years": scen_years,
        "historical_jobs": total_jobs,
        "historical_hard_error_total": hard_error_total,
        "command": " ".join(cmd),
        "stdout": proc.stdout,
    }


def load_hourly_safe(country: str, year: int) -> pd.DataFrame | None:
    path = hourly_output_path(country, year)
    if not path.exists():
        return None
    try:
        return _load_hourly_cached(country, year, _mtime_ns(path))
    except Exception:
        return None


def load_annual_metrics() -> pd.DataFrame:
    p = Path("data/metrics/annual_metrics.parquet")
    if not p.exists():
        return pd.DataFrame()
    return _read_parquet_cached(str(p), _mtime_ns(p))


def load_validation_findings(country: str | None = None, year: int | None = None) -> pd.DataFrame:
    p = Path("data/metrics/validation_findings.parquet")
    if not p.exists():
        return pd.DataFrame()
    df = _read_parquet_cached(str(p), _mtime_ns(p))
    if country is not None and "country" in df.columns:
        df = df[df["country"] == country]
    if year is not None and "year" in df.columns:
        df = df[df["year"] == year]
    return df


def load_commodity_daily_ui() -> pd.DataFrame | None:
    p = Path("data/external/commodity_prices_daily.csv")
    if not p.exists():
        return None
    df = _read_csv_cached(str(p), _mtime_ns(p))
    req = {"date", "gas_price_eur_mwh_th", "co2_price_eur_t"}
    if not req.issubset(df.columns):
        return None
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df.dropna(subset=["date"])


def load_phase2_assumptions_table() -> pd.DataFrame:
    return load_phase2_assumptions()


def available_phase2_years(
    assumptions_phase2: pd.DataFrame,
    scenario_ids: list[str] | None = None,
    countries: list[str] | None = None,
) -> list[int]:
    if assumptions_phase2 is None or assumptions_phase2.empty:
        return []
    scoped = assumptions_phase2.copy()
    if scenario_ids:
        scoped = scoped[scoped["scenario_id"].astype(str).isin([str(s) for s in scenario_ids])]
    if countries:
        scoped = scoped[scoped["country"].astype(str).isin([str(c) for c in countries])]
    years = pd.to_numeric(scoped.get("year", pd.Series(dtype=float)), errors="coerce").dropna().astype(int).unique().tolist()
    return sorted(set(years))


def default_analysis_scenario_years(available_years: list[int], start: int = 2025, end: int = 2035) -> list[int]:
    if not available_years:
        return list(range(start, end + 1))
    preferred = [int(y) for y in available_years if start <= int(y) <= end]
    return preferred if preferred else sorted(set([int(y) for y in available_years]))


def phase2_assumptions_editor(key_prefix: str = "phase2") -> pd.DataFrame:
    try:
        df = load_phase2_assumptions_table()
    except Exception as exc:
        st.error(f"Impossible de charger les hypotheses Phase 2: {exc}")
        return pd.DataFrame()

    st.subheader("Hypotheses Phase 2 (scenario x pays x annee)")
    edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, key=f"{key_prefix}_assumptions_editor")
    if st.button("Sauvegarder hypotheses Phase 2", key=f"{key_prefix}_save_assumptions"):
        out_path = Path("data/assumptions/phase2/phase2_scenario_country_year.csv")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        edited.to_csv(out_path, index=False)
        st.cache_data.clear()
        st.success("Hypotheses Phase 2 sauvegardees.")
        return edited
    return df


@st.cache_data(show_spinner=False)
def _load_scenario_annual_cached(scenario_id: str, mtime_ns: int) -> pd.DataFrame:
    _ = mtime_ns
    return load_scenario_annual_metrics(scenario_id)


def load_scenario_annual_metrics_ui(scenario_id: str) -> pd.DataFrame:
    p = Path(f"data/processed/scenario/{scenario_id}/annual_metrics.parquet")
    if not p.exists():
        return pd.DataFrame()
    return _load_scenario_annual_cached(scenario_id, _mtime_ns(p))


@st.cache_data(show_spinner=False)
def _load_scenario_findings_cached(scenario_id: str, mtime_ns: int) -> pd.DataFrame:
    _ = mtime_ns
    return load_scenario_validation_findings(scenario_id)


def load_scenario_validation_findings_ui(scenario_id: str) -> pd.DataFrame:
    p = Path(f"data/processed/scenario/{scenario_id}/validation_findings.parquet")
    if not p.exists():
        return pd.DataFrame()
    return _load_scenario_findings_cached(scenario_id, _mtime_ns(p))


@st.cache_data(show_spinner=False)
def _load_scenario_hourly_cached(scenario_id: str, country: str, year: int, mtime_ns: int) -> pd.DataFrame:
    _ = mtime_ns
    return load_scenario_hourly(scenario_id, country, year)


def load_scenario_hourly_safe(scenario_id: str, country: str, year: int) -> pd.DataFrame | None:
    p = Path(f"data/processed/scenario/{scenario_id}/hourly/{country}/{year}.parquet")
    if not p.exists():
        return None
    try:
        return _load_scenario_hourly_cached(scenario_id, country, year, _mtime_ns(p))
    except Exception:
        return None


def collect_hourly_map(countries: list[str], years: list[int], scenario_id: str | None = None) -> dict[tuple[str, int], pd.DataFrame]:
    out: dict[tuple[str, int], pd.DataFrame] = {}
    for country in countries:
        for year in years:
            if scenario_id:
                h = load_scenario_hourly_safe(scenario_id, country, year)
            else:
                h = load_hourly_safe(country, year)
            if h is not None and not h.empty:
                out[(country, year)] = h
    return out


def run_phase2_scenario_ui(scenario_id: str, countries: list[str], years: list[int]) -> dict | None:
    if not scenario_id:
        st.warning("Selectionne un scenario_id.")
        return None
    if not countries or not years:
        st.warning("Selectionne au moins un pays et une annee.")
        return None

    with st.form("phase2_run_form"):
        st.caption("Ce calcul construit les tables prospectives (horaire + annuel + findings) pour la selection.")
        submit = st.form_submit_button("Executer scenario Phase 2", type="primary")

    if not submit:
        return None

    assumptions = load_phase2_assumptions_table()
    annual_hist = load_annual_metrics()
    if annual_hist.empty:
        st.error("Impossible d'executer la Phase 2 sans annual_metrics historiques.")
        return None

    hist_map = collect_hourly_map(countries, list(range(2018, 2025)))
    with st.spinner("Execution scenario Phase 2 en cours..."):
        res = run_phase2_scenario(
            scenario_id=scenario_id,
            countries=countries,
            years=years,
            assumptions_phase2=assumptions,
            annual_hist=annual_hist,
            hourly_hist_map=hist_map,
        )
    st.success(f"Scenario {scenario_id} termine.")
    st.cache_data.clear()
    return res


def to_plot_frame(df: pd.DataFrame, timestamp_col: str = "timestamp_utc") -> pd.DataFrame:
    """Return a plotting-safe dataframe with a single timestamp column.

    Handles common case where `timestamp_utc` exists both as index name and as column.
    """
    out = df.copy()

    if timestamp_col in out.columns:
        # Avoid duplicate insertion when index shares the same name.
        return out.reset_index(drop=True)

    if isinstance(out.index, pd.DatetimeIndex):
        out = out.reset_index()
        first_col = str(out.columns[0])
        if first_col != timestamp_col:
            out = out.rename(columns={first_col: timestamp_col})
        return out

    out = out.reset_index(drop=False)
    if timestamp_col not in out.columns:
        out[timestamp_col] = out.index
    return out


def assumptions_editor() -> pd.DataFrame:
    df = load_assumptions_table()
    st.subheader("Hypotheses Phase 1")
    edited = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    if st.button("Sauvegarder hypotheses"):
        edited.to_csv("data/assumptions/phase1_assumptions.csv", index=False)
        st.cache_data.clear()
        st.success("Hypotheses sauvegardees")
    return edited


def assumptions_editor_for(param_names: list[str], key_prefix: str) -> pd.DataFrame:
    df = load_assumptions_table()
    if df.empty:
        st.warning("Aucune table d'hypotheses disponible.")
        return df

    subset = df[df["param_name"].isin(param_names)].copy()
    st.subheader("Hypotheses utilisees")
    st.caption("Parametres effectivement consommes par ce module.")
    edited_subset = st.data_editor(
        subset,
        num_rows="fixed",
        use_container_width=True,
        key=f"{key_prefix}_assumptions_editor",
    )

    if st.button("Sauvegarder ces hypotheses", key=f"{key_prefix}_save_assumptions"):
        merged = df.set_index("param_name")
        for _, row in edited_subset.iterrows():
            pname = str(row["param_name"])
            if pname in merged.index:
                for col in [
                    "param_group",
                    "param_value",
                    "unit",
                    "description",
                    "source",
                    "last_updated",
                    "owner",
                ]:
                    if col in row:
                        merged.loc[pname, col] = row[col]
        merged_df = merged.reset_index()
        merged_df.to_csv("data/assumptions/phase1_assumptions.csv", index=False)
        st.cache_data.clear()
        st.success("Hypotheses module sauvegardees.")
        return merged_df

    return df


def _phase1_signature(df: pd.DataFrame) -> list[dict[str, str]]:
    if df is None or df.empty:
        return []
    req = [c for c in ["param_name", "param_value"] if c in df.columns]
    if not req:
        return []
    out = df[req].copy()
    out["param_name"] = out["param_name"].astype(str)
    out = out.sort_values("param_name")
    return out.to_dict(orient="records")


def _phase2_signature(df: pd.DataFrame, selection: dict) -> list[dict]:
    if df is None or df.empty:
        return []
    scenarios = [str(s) for s in selection.get("scenario_ids", [])]
    countries = [str(c) for c in selection.get("countries", [])]
    years = [int(y) for y in selection.get("scenario_years", [])]
    scoped = df.copy()
    if scenarios:
        scoped = scoped[scoped["scenario_id"].astype(str).isin(scenarios)]
    if countries:
        scoped = scoped[scoped["country"].astype(str).isin(countries)]
    if years:
        scoped = scoped[pd.to_numeric(scoped["year"], errors="coerce").isin(years)]
    keep_cols = [
        c
        for c in [
            "scenario_id",
            "country",
            "year",
            "demand_total_twh",
            "cap_pv_gw",
            "cap_wind_on_gw",
            "must_run_min_output_factor",
            "interconnection_export_gw",
            "export_coincidence_factor",
            "bess_power_gw",
            "bess_energy_gwh",
            "co2_eur_per_t",
            "gas_eur_per_mwh_th",
            "marginal_tech",
        ]
        if c in scoped.columns
    ]
    if not keep_cols:
        return []
    scoped = scoped[keep_cols].sort_values([c for c in ["scenario_id", "country", "year"] if c in keep_cols])
    return scoped.to_dict(orient="records")


def build_bundle_hash(question_id: str, selection: dict, assumptions_phase1: pd.DataFrame, assumptions_phase2: pd.DataFrame) -> str:
    payload = {
        "question_id": str(question_id).upper(),
        "selection": selection,
        "phase1_signature": _phase1_signature(assumptions_phase1),
        "phase2_signature": _phase2_signature(assumptions_phase2, selection),
    }
    return hash_object(payload)


@st.cache_data(show_spinner=False)
def run_question_bundle_cached(question_id: str, bundle_hash: str, selection: dict, cache_bust: str = "") -> QuestionBundleResult:
    _ = bundle_hash
    _ = cache_bust
    annual_hist = load_annual_metrics()
    assumptions_phase1 = load_assumptions_table()
    assumptions_phase2 = load_phase2_assumptions()
    countries = [str(c) for c in selection.get("countries", [])]
    if not countries and not annual_hist.empty:
        countries = sorted(annual_hist["country"].dropna().astype(str).unique().tolist())
    hist_years = list(range(2018, 2025))
    hourly_hist_map = collect_hourly_map(countries, hist_years)
    run_id = f"{str(question_id).upper()}_{bundle_hash[:12]}"
    return run_question_bundle(
        question_id=question_id,
        annual_hist=annual_hist,
        hourly_hist_map=hourly_hist_map,
        assumptions_phase1=assumptions_phase1,
        assumptions_phase2=assumptions_phase2,
        selection=selection,
        run_id=run_id,
    )


def _safe_read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _safe_read_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _safe_read_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def _load_tables_dir(tables_dir: Path) -> dict[str, pd.DataFrame]:
    out: dict[str, pd.DataFrame] = {}
    if not tables_dir.exists():
        return out
    for csv_path in sorted(tables_dir.glob("*.csv")):
        out[csv_path.stem] = _safe_read_csv(csv_path)
    return out


def _load_module_result_from_export(
    module_dir: Path,
    *,
    default_mode: str,
    default_run_id: str,
    default_selection: dict,
    default_module_id: str,
    scenario_id: str | None = None,
) -> ModuleResult:
    summary = _safe_read_json(module_dir / "summary.json")
    checks = summary.get("checks", [])
    if not isinstance(checks, list):
        checks = []
    warnings = summary.get("warnings", [])
    if not isinstance(warnings, list):
        warnings = []
    assumptions_used = summary.get("assumptions_used", [])
    if not isinstance(assumptions_used, list):
        assumptions_used = []
    kpis = summary.get("kpis", {})
    if not isinstance(kpis, dict):
        kpis = {}
    selection = summary.get("selection", default_selection)
    if not isinstance(selection, dict):
        selection = default_selection

    horizon_year_raw = summary.get("horizon_year", None)
    try:
        horizon_year = int(horizon_year_raw) if horizon_year_raw is not None else None
    except Exception:
        horizon_year = None

    scenario = summary.get("scenario_id", scenario_id)
    if scenario is not None:
        scenario = str(scenario)

    return ModuleResult(
        module_id=str(summary.get("module_id", default_module_id)),
        run_id=str(summary.get("run_id", default_run_id)),
        selection=selection,
        assumptions_used=assumptions_used,
        kpis=kpis,
        tables=_load_tables_dir(module_dir / "tables"),
        figures=[],
        narrative_md=_safe_read_text(module_dir / "narrative.md"),
        checks=checks,
        warnings=[str(w) for w in warnings],
        mode=str(summary.get("mode", default_mode)).upper(),
        scenario_id=scenario,
        horizon_year=horizon_year,
    )


def load_question_bundle_from_combined_run(
    run_id: str,
    question_id: str,
    base_dir: str = "outputs/combined",
) -> tuple[QuestionBundleResult, Path]:
    if _load_question_bundle_from_combined_run_verified is None:
        return _load_question_bundle_from_combined_run_local(
            run_id=run_id,
            question_id=question_id,
            base_dir=base_dir,
        )
    return _load_question_bundle_from_combined_run_verified(
        run_id=run_id,
        question_id=question_id,
        base_dir=base_dir,
    )


def load_question_bundle_from_combined_run_safe(
    run_id: str,
    question_id: str,
    base_dir: str = "outputs/combined",
) -> tuple[QuestionBundleResult, Path]:
    if _load_question_bundle_from_combined_run_verified is None:
        return _load_question_bundle_from_combined_run_local(
            run_id=run_id,
            question_id=question_id,
            base_dir=base_dir,
        )
    return load_question_bundle_from_combined_run(
        run_id=run_id,
        question_id=question_id,
        base_dir=base_dir,
    )
