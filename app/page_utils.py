"""UI helpers for Streamlit pages."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from src.config_loader import load_countries, load_phase2_assumptions
from src.pipeline import build_country_year, load_assumptions_table
from src.scenario.phase2_engine import run_phase2_scenario
from src.storage import (
    hourly_output_path,
    load_hourly,
    load_scenario_annual_metrics,
    load_scenario_hourly,
    load_scenario_validation_findings,
)


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
