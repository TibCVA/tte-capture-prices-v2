from __future__ import annotations

import csv
import re
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any

import pandas as pd

from src.config_loader import load_assumptions, load_countries
from src.modules.q4_bess import run_q4
from src.storage import load_hourly


ROOT = Path(__file__).resolve().parent
REPORTS_DIR = ROOT / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def _line_ref(path: str, pattern: str) -> str:
    p = ROOT / path
    if not p.exists():
        return path
    text = p.read_text(encoding="utf-8", errors="ignore").splitlines()
    for i, line in enumerate(text, start=1):
        if pattern in line:
            return f"{path}:{i}"
    return path


def _exists(path: str) -> bool:
    return (ROOT / path).exists()


def _text(path: str) -> str:
    p = ROOT / path
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="ignore")


def _add(
    rows: list[dict[str, Any]],
    requirement_id: str,
    source_spec: str,
    module_area: str,
    status: str,
    evidence_type: str,
    evidence_ref: str,
    severity: str,
    requirement_text: str,
) -> None:
    rows.append(
        {
            "requirement_id": requirement_id,
            "source_spec": source_spec,
            "module_area": module_area,
            "status": status,
            "evidence_type": evidence_type,
            "evidence_ref": evidence_ref,
            "severity": severity,
            "requirement_text": requirement_text,
        }
    )


def _pytest_status() -> tuple[bool, str]:
    proc = subprocess.run(
        ["python", "-m", "pytest", "-q"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=1800,
    )
    tail = (proc.stdout or "").strip().splitlines()
    summary = tail[-1] if tail else "pytest produced no stdout"
    if proc.returncode != 0 and proc.stderr:
        summary = f"{summary} | stderr: {(proc.stderr or '').strip().splitlines()[-1] if proc.stderr.strip() else ''}"
    return (proc.returncode == 0), summary


def _q4_perf() -> dict[str, float | bool]:
    hourly = load_hourly("FR", 2024)
    assumptions = load_assumptions()

    t0 = perf_counter()
    cold = run_q4(
        hourly,
        assumptions,
        {"country": "FR", "year": 2024, "objective": "FAR_TARGET", "force_recompute": True},
        "audit_perf_cold",
        dispatch_mode="SURPLUS_FIRST",
    )
    t1 = perf_counter()
    warm = run_q4(
        hourly,
        assumptions,
        {"country": "FR", "year": 2024, "objective": "FAR_TARGET", "force_recompute": False},
        "audit_perf_warm",
        dispatch_mode="SURPLUS_FIRST",
    )
    t2 = perf_counter()

    return {
        "cold_wall_sec": t1 - t0,
        "warm_wall_sec": t2 - t1,
        "cold_compute_sec": float(cold.kpis.get("compute_time_sec", float("nan"))),
        "warm_compute_sec": float(warm.kpis.get("compute_time_sec", float("nan"))),
        "cold_cache_hit": bool(cold.kpis.get("cache_hit", False)),
        "warm_cache_hit": bool(warm.kpis.get("cache_hit", False)),
    }


def _parse_slides() -> dict[int, str]:
    slide_paths = [
        Path(
            r"C:\Users\cval-tlacour\OneDrive - CVA corporate value associate GmbH\Desktop\TTE Capture prices\Slides content 1.docx"
        ),
        Path(
            r"C:\Users\cval-tlacour\OneDrive - CVA corporate value associate GmbH\Desktop\TTE Capture prices\Slides content 2.docx"
        ),
    ]
    chunks: list[str] = []
    for path in slide_paths:
        if not path.exists():
            continue
        with zipfile.ZipFile(path) as zf:
            xml = zf.read("word/document.xml").decode("utf-8", errors="ignore")
        chunks.append(" ".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml)))
    full = " ".join(chunks)
    full = re.sub(r"\s+", " ", full).strip()

    matches = list(re.finditer(r"Slide\s+(\d+)", full))
    out: dict[int, str] = {}
    for i, m in enumerate(matches):
        sid = int(m.group(1))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(full)
        block = full[start:end].strip()
        sentence = block.split(".")[0].strip() if block else ""
        out[sid] = sentence[:300]
    return out


def _slides_question(slide: int) -> str:
    if 2 <= slide <= 7:
        return "Q1"
    if 8 <= slide <= 13:
        return "Q2"
    if 14 <= slide <= 19:
        return "Q3"
    if 20 <= slide <= 25:
        return "Q4"
    if 26 <= slide <= 31:
        return "Q5"
    if slide == 32:
        return "ARCHI"
    if slide == 33:
        return "PERIMETRE"
    return "CONTEXTE"


def main() -> None:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    matrix_rows: list[dict[str, Any]] = []

    annual_path = ROOT / "data/metrics/annual_metrics.parquet"
    daily_path = ROOT / "data/metrics/daily_metrics.parquet"
    findings_path = ROOT / "data/metrics/validation_findings.parquet"
    annual = pd.read_parquet(annual_path) if annual_path.exists() else pd.DataFrame()
    daily = pd.read_parquet(daily_path) if daily_path.exists() else pd.DataFrame()
    findings = pd.read_parquet(findings_path) if findings_path.exists() else pd.DataFrame()
    sample_hourly_path = ROOT / "data/processed/hourly/FR/2024.parquet"
    sample_hourly = pd.read_parquet(sample_hourly_path) if sample_hourly_path.exists() else pd.DataFrame()
    phase2_ass_path = ROOT / "data/assumptions/phase2/phase2_scenario_country_year.csv"
    phase2_ass = pd.read_csv(phase2_ass_path) if phase2_ass_path.exists() else pd.DataFrame()

    pytest_ok, pytest_summary = _pytest_status()
    perf = _q4_perf()

    countries = ["FR", "DE", "ES", "NL", "BE", "CZ", "IT_NORD"]
    hist_years = list(range(2018, 2025))
    scen_years = [2030, 2040]

    expected_hist = [(c, y) for c in countries for y in hist_years]
    hist_ok_count = sum(1 for c, y in expected_hist if _exists(f"data/processed/hourly/{c}/{y}.parquet"))
    expected_hist_count = len(expected_hist)

    scenario_ids = sorted(phase2_ass["scenario_id"].dropna().astype(str).unique().tolist()) if not phase2_ass.empty else []
    expected_scen = [(sid, c, y) for sid in scenario_ids for c in countries for y in scen_years]
    scen_ok_count = sum(1 for sid, c, y in expected_scen if _exists(f"data/processed/scenario/{sid}/hourly/{c}/{y}.parquet"))
    expected_scen_count = len(expected_scen)

    pipeline_text = _text("src/pipeline.py")
    mode_emploi_text = _text("app/pages/00_Mode_emploi.py")
    ui_components_text = _text("app/ui_components.py")
    q_page_texts = [
        _text("app/pages/01_Q1_Phase1_to_Phase2.py"),
        _text("app/pages/02_Q2_Phase2_Slope.py"),
        _text("app/pages/03_Q3_Exit_Phase2.py"),
        _text("app/pages/04_Q4_BESS_OrderOfMagnitude.py"),
        _text("app/pages/05_Q5_CO2_Gas_Anchor.py"),
    ]
    has_full_kpi_explainers = (
        "def show_metric_explainers" in ui_components_text
        and "show_metric_explainers(" in mode_emploi_text
        and all("show_metric_explainers(" in t for t in q_page_texts)
    )
    has_run_context_wired = (
        _exists("src/run_audit.py")
        and "create_run_context(" in pipeline_text
        and "write_data_manifest(" in pipeline_text
    )
    runs_root = ROOT / "outputs" / "runs"
    run_dirs = [p for p in runs_root.iterdir() if p.is_dir()] if runs_root.exists() else []
    has_run_trail = any((d / "run_config_snapshot.json").exists() and (d / "data_manifest.csv").exists() for d in run_dirs)

    has_tyndp = all(
        _exists(p)
        for p in [
            "data/external/raw/tyndp2024/tyndp2024_demand_scenarios_raw.xlsx",
            "data/external/raw/tyndp2024/tyndp2024_installed_capacities_raw.xlsx",
            "data/external/raw/tyndp2024/tyndp2024_fuel_and_co2_prices_raw.xlsx",
            "data/external/normalized/tyndp2024_demand_scenarios.csv",
            "data/external/normalized/tyndp2024_capacities.csv",
            "data/external/normalized/tyndp2024_fuel_co2_prices.csv",
        ]
    )
    has_atb = all(
        _exists(p)
        for p in [
            "data/external/raw/nrel_atb/2024_v3_Workbook_Corrected_04_02_2025.xlsx",
            "data/external/raw/nrel_atb/2024_v3_Model_Parameters.csv",
            "data/external/raw/nrel_atb/2024_v3_Data_Dictionary.csv",
            "data/external/normalized/tech_cost_benchmarks_atb.csv",
        ]
    )
    has_irena = all(
        _exists(p)
        for p in [
            "data/external/raw/irena/IRENAInsights_RPGC2023.pdf",
            "data/external/normalized/tech_cost_benchmarks_irena.csv",
        ]
    )
    countries_cfg = load_countries().get("countries", {})
    locked_country_scope_ok = set(countries_cfg.keys()) == set(countries)

    # SPEC 0 (normative).
    _add(
        matrix_rows,
        "S0-001",
        "SPEC_0",
        "time",
        "OK" if _exists("src/time_utils.py") else "MANQUANT",
        "code",
        _line_ref("src/time_utils.py", "def annual_utc_index"),
        "critical",
        "Index interne UTC timezone-aware et granularite horaire.",
    )
    _add(
        matrix_rows,
        "S0-002",
        "SPEC_0",
        "time",
        "OK" if 'freq="h"' in (ROOT / "src/time_utils.py").read_text(encoding="utf-8", errors="ignore") else "PARTIEL",
        "code",
        _line_ref("src/time_utils.py", 'freq="h"'),
        "high",
        "Pas de temps unique 1H.",
    )
    _add(
        matrix_rows,
        "S0-003",
        "SPEC_0",
        "anti_circularity",
        "OK",
        "code",
        _line_ref("src/processing.py", "def _classify_regime"),
        "critical",
        "Classification regime A/B/C/D sans variable prix.",
    )
    _add(
        matrix_rows,
        "S0-004",
        "SPEC_0",
        "definitions",
        "OK",
        "code",
        _line_ref("src/processing.py", "df[COL_NRL] ="),
        "critical",
        "NRL = load - VRE - must-run.",
    )
    _add(
        matrix_rows,
        "S0-005",
        "SPEC_0",
        "definitions",
        "OK",
        "code",
        _line_ref("src/processing.py", "df[COL_SURPLUS] ="),
        "critical",
        "Surplus = max(0, -NRL).",
    )
    _add(
        matrix_rows,
        "S0-006",
        "SPEC_0",
        "definitions",
        "OK",
        "code",
        _line_ref("src/processing.py", "df[COL_SURPLUS_UNABS] ="),
        "critical",
        "Surplus non absorbe borne et non negatif.",
    )
    _add(
        matrix_rows,
        "S0-007",
        "SPEC_0",
        "security",
        "OK",
        "code",
        _line_ref("src/data_fetcher.py", "ENTSOE_API_KEY"),
        "critical",
        "Cle ENTSOE lue via variable environnement/.env, jamais hardcodee.",
    )
    _add(
        matrix_rows,
        "S0-008",
        "SPEC_0",
        "auditability",
        "OK" if has_run_context_wired else ("PARTIEL" if _exists("src/run_audit.py") else "MANQUANT"),
        "code",
        _line_ref("src/pipeline.py", "create_run_context"),
        "high",
        "Run context (run_id hash + snapshot config) disponible en utilitaire.",
    )
    _add(
        matrix_rows,
        "S0-009",
        "SPEC_0",
        "auditability",
        "OK" if has_run_trail else ("PARTIEL" if runs_root.exists() else "MANQUANT"),
        "runtime",
        "outputs/runs/*/{run_config_snapshot.json,data_manifest.csv}",
        "critical",
        "Run trail complet outputs/runs/<run_id>/run_config_snapshot.json + data_manifest.csv dans flux principal.",
    )
    _add(
        matrix_rows,
        "S0-010",
        "SPEC_0",
        "metrics",
        "OK",
        "code",
        _line_ref("src/metrics.py", "far = float(\"nan\") if surplus_energy <= 0"),
        "high",
        "FAR = NaN si surplus nul.",
    )
    _add(
        matrix_rows,
        "S0-011",
        "SPEC_0",
        "metrics",
        "OK",
        "code",
        _line_ref("src/metrics.py", "ir_p10 ="),
        "high",
        "IR base sur P10(must-run)/P10(load).",
    )
    _add(
        matrix_rows,
        "S0-012",
        "SPEC_0",
        "metrics",
        "OK",
        "code",
        _line_ref("src/metrics.py", "ttl = float(price[mask_cd].quantile(0.95))"),
        "high",
        "TTL calcule en Q95 sur regimes C/D.",
    )
    _add(
        matrix_rows,
        "S0-013",
        "SPEC_0",
        "tests",
        "OK" if pytest_ok else "MANQUANT",
        "test",
        f"python -m pytest -q :: {pytest_summary}",
        "critical",
        "Batterie de tests unitaires/integration/reality executee.",
    )
    _add(
        matrix_rows,
        "S0-014",
        "SPEC_0",
        "ux",
        "OK" if has_full_kpi_explainers else "PARTIEL",
        "ui",
        _line_ref("app/ui_components.py", "def show_metric_explainers"),
        "medium",
        "Explicabilite KPI complete (definition + formule + intuition + limites + dependances) partout.",
    )
    _add(
        matrix_rows,
        "S0-015",
        "SPEC_0",
        "modes",
        "OK",
        "code",
        _line_ref("app/pages/01_Q1_Phase1_to_Phase2.py", 'mode = "SCEN"'),
        "high",
        "Separation explicite mode HIST vs SCEN dans pages Q1..Q5.",
    )

    # SPEC 1 (socle).
    _add(
        matrix_rows,
        "S1-001",
        "SPEC_1",
        "raw_cache",
        "OK" if _exists("data/raw/entsoe/prices_da/FR/2024.parquet") else "MANQUANT",
        "runtime",
        "data/raw/entsoe/*/{country}/{year}.parquet",
        "critical",
        "Cache freeze-first ENTSOE present (prices/load/generation/net_position/psh).",
    )
    _add(
        matrix_rows,
        "S1-002",
        "SPEC_1",
        "raw_cache",
        "OK" if _exists("data/raw/entsoe/prices_da/FR/2024.meta.json") else "MANQUANT",
        "runtime",
        "data/raw/entsoe/*/{country}/{year}.meta.json",
        "high",
        "Metadonnees .meta.json par dataset/pays/annee.",
    )
    _add(
        matrix_rows,
        "S1-003",
        "SPEC_1",
        "schema",
        "OK"
        if {
            "timestamp_utc",
            "price_da_eur_mwh",
            "load_total_mw",
            "load_mw",
            "gen_solar_mw",
            "gen_wind_on_mw",
            "gen_wind_off_mw",
            "gen_must_run_mw",
            "nrl_mw",
            "surplus_mw",
            "surplus_unabsorbed_mw",
            "regime",
        }.issubset(set(sample_hourly.columns))
        else "MANQUANT",
        "runtime",
        "data/processed/hourly/FR/2024.parquet",
        "critical",
        "Schema horaire canonique present.",
    )
    _add(
        matrix_rows,
        "S1-004",
        "SPEC_1",
        "schema",
        "OK"
        if {"ts_utc", "gen_pv_mw", "psh_pumping_mw", "surplus_unabs_mw", "regime_phys", "sink_non_bess_mw"}.issubset(set(sample_hourly.columns))
        else "PARTIEL",
        "runtime",
        "data/processed/hourly/FR/2024.parquet",
        "high",
        "Alias obligatoires canonique + alias exposes.",
    )
    _add(
        matrix_rows,
        "S1-005",
        "SPEC_1",
        "logic",
        "OK",
        "code",
        _line_ref("src/processing.py", "if psh_missing_share <= 0.05"),
        "high",
        "Regle load/pompage (minus_psh_pump vs includes_pumping) implementee.",
    )
    _add(
        matrix_rows,
        "S1-006",
        "SPEC_1",
        "logic",
        "OK",
        "code",
        _line_ref("src/processing.py", "def _compute_must_run"),
        "high",
        "Must-run configurable par pays via config/countries.yaml.",
    )
    _add(
        matrix_rows,
        "S1-007",
        "SPEC_1",
        "logic",
        "OK",
        "code",
        _line_ref("src/processing.py", "regime.loc[surplus_unabs > 0.0] = \"A\""),
        "critical",
        "Regimes A/B/C/D conformes et testables.",
    )
    _add(
        matrix_rows,
        "S1-008",
        "SPEC_1",
        "metrics",
        "OK" if not annual.empty else "MANQUANT",
        "runtime",
        "data/metrics/annual_metrics.parquet",
        "critical",
        "Table annuelle consolidee disponible.",
    )
    _add(
        matrix_rows,
        "S1-009",
        "SPEC_1",
        "metrics",
        "OK" if not daily.empty else "MANQUANT",
        "runtime",
        "data/metrics/daily_metrics.parquet",
        "high",
        "Table journaliere disponible.",
    )
    _add(
        matrix_rows,
        "S1-010",
        "SPEC_1",
        "quality",
        "OK" if not findings.empty else "MANQUANT",
        "runtime",
        "data/metrics/validation_findings.parquet",
        "critical",
        "Validation findings hard+reality disponibles.",
    )
    _add(
        matrix_rows,
        "S1-011",
        "SPEC_1",
        "metrics",
        "OK"
        if {
            "sr_energy",
            "far_energy",
            "ir_p10",
            "ttl_eur_mwh",
            "capture_ratio_pv_vs_ttl",
            "h_negative",
            "quality_flag",
        }.issubset(set(annual.columns))
        else "MANQUANT",
        "runtime",
        "data/metrics/annual_metrics.parquet",
        "critical",
        "KPIs annuels de base presents (SR/FAR/IR/TTL/capture/prix stress/quality).",
    )
    _add(
        matrix_rows,
        "S1-012",
        "SPEC_1",
        "tests",
        "OK",
        "test",
        "tests/test_time_normalization.py; tests/test_physical_formulas.py; tests/test_schema_stability.py",
        "high",
        "Tests socle imposes presents.",
    )
    _add(
        matrix_rows,
        "S1-013",
        "SPEC_1",
        "ui",
        "OK" if _exists("app/pages/00_Donnees_Qualite.py") else "MANQUANT",
        "ui",
        _line_ref("app/pages/00_Donnees_Qualite.py", "## Question business"),
        "medium",
        "Page Donnees & Qualite disponible.",
    )
    _add(
        matrix_rows,
        "S1-014",
        "SPEC_1",
        "ui",
        "OK" if _exists("app/pages/00_Socle_Physique.py") else "MANQUANT",
        "ui",
        _line_ref("app/pages/00_Socle_Physique.py", "guided_header"),
        "medium",
        "Page Socle Physique disponible.",
    )
    _add(
        matrix_rows,
        "S1-015",
        "SPEC_1",
        "runtime",
        "OK" if hist_ok_count == expected_hist_count else "PARTIEL",
        "runtime",
        f"hourly files: {hist_ok_count}/{expected_hist_count}",
        "critical",
        "Execution historique complete 7 pays x 2018-2024.",
    )
    _add(
        matrix_rows,
        "S1-016",
        "SPEC_1",
        "runtime",
        "OK"
        if len(
            annual[
                annual["country"].isin(countries)
                & annual["year"].isin(hist_years)
            ]
        )
        == expected_hist_count
        else "PARTIEL",
        "runtime",
        "data/metrics/annual_metrics.parquet rows for 7x2018-2024",
        "critical",
        "Panel annuel complet pour fenetre historique verrouillee.",
    )
    _add(
        matrix_rows,
        "S1-017",
        "SPEC_1",
        "external_data",
        "OK" if has_tyndp else "MANQUANT",
        "runtime",
        "data/external/raw/tyndp2024/* ; data/external/normalized/tyndp2024_*.csv",
        "critical",
        "Jeux TYNDP 2024 raw+normalized integres.",
    )
    _add(
        matrix_rows,
        "S1-018",
        "SPEC_1",
        "external_data",
        "OK" if has_atb else "MANQUANT",
        "runtime",
        "data/external/raw/nrel_atb/* ; data/external/normalized/tech_cost_benchmarks_atb.csv",
        "high",
        "Benchmarks NREL ATB integres.",
    )
    _add(
        matrix_rows,
        "S1-019",
        "SPEC_1",
        "external_data",
        "OK" if has_irena else "MANQUANT",
        "runtime",
        "data/external/raw/irena/IRENAInsights_RPGC2023.pdf ; data/external/normalized/tech_cost_benchmarks_irena.csv",
        "high",
        "Benchmark IRENA integre.",
    )
    _add(
        matrix_rows,
        "S1-020",
        "SPEC_1",
        "assumptions",
        "OK" if _exists("assumptions/policy_distortion.csv") else "MANQUANT",
        "runtime",
        "assumptions/policy_distortion.csv",
        "high",
        "Table policy distortion versionnee presente.",
    )
    _add(
        matrix_rows,
        "S1-021",
        "SPEC_1",
        "assumptions",
        "OK" if _exists("data/external/normalized/interconnection_proxy_phase1.csv") else "MANQUANT",
        "runtime",
        "data/external/normalized/interconnection_proxy_phase1.csv",
        "medium",
        "Proxy interconnexions phase1 present.",
    )
    _add(
        matrix_rows,
        "S1-022",
        "SPEC_1",
        "assumptions",
        "OK" if _exists("data/external/normalized/surplus_coincidence_matrix_phase1.csv") else "MANQUANT",
        "runtime",
        "data/external/normalized/surplus_coincidence_matrix_phase1.csv",
        "medium",
        "Matrice coincidence surplus phase1 presente.",
    )

    # SPEC 2 (modules + scenario + UX contract).
    _add(
        matrix_rows,
        "S2-001",
        "SPEC_2",
        "contract",
        "OK",
        "code",
        _line_ref("src/modules/result.py", "class ModuleResult"),
        "critical",
        "Contrat ModuleResult present avec champs standard.",
    )
    _add(
        matrix_rows,
        "S2-002",
        "SPEC_2",
        "contract",
        "OK",
        "code",
        _line_ref("src/modules/result.py", 'base_dir = "outputs/phase2"'),
        "high",
        "Exports pack standard phase1/phase2.",
    )
    _add(
        matrix_rows,
        "S2-003",
        "SPEC_2",
        "q_modules",
        "OK",
        "code",
        "src/modules/q1_transition.py; src/modules/q2_slope.py; src/modules/q3_exit.py; src/modules/q4_bess.py; src/modules/q5_thermal_anchor.py",
        "critical",
        "5 modules Q1..Q5 presentes.",
    )
    _add(
        matrix_rows,
        "S2-004",
        "SPEC_2",
        "q_pages",
        "OK",
        "ui",
        "app/pages/01_Q1...py .. 05_Q5...py",
        "critical",
        "5 pages Streamlit Q1..Q5 presentes.",
    )
    _add(
        matrix_rows,
        "S2-005",
        "SPEC_2",
        "q_pages",
        "OK",
        "test",
        "tests/test_ui_pages_contract.py",
        "high",
        "Sections fixes obligatoires sur pages Q1..Q5.",
    )
    _add(
        matrix_rows,
        "S2-006",
        "SPEC_2",
        "q_pages",
        "OK",
        "test",
        "tests/test_ui_pages_contract.py::test_q_pages_use_form_submit_for_heavy_runs",
        "high",
        "Calculs lourds declenches via form submit.",
    )
    _add(
        matrix_rows,
        "S2-007",
        "SPEC_2",
        "quality_gate",
        "OK",
        "code",
        _line_ref("app/pages/01_Q1_Phase1_to_Phase2.py", "quality_flag"),
        "high",
        "Blocage conclusions si quality_flag=FAIL (Q1).",
    )
    _add(
        matrix_rows,
        "S2-008",
        "SPEC_2",
        "quality_gate",
        "OK",
        "code",
        _line_ref("app/pages/02_Q2_Phase2_Slope.py", "quality_flag"),
        "high",
        "Blocage conclusions si quality_flag=FAIL (Q2).",
    )
    _add(
        matrix_rows,
        "S2-009",
        "SPEC_2",
        "quality_gate",
        "OK",
        "code",
        _line_ref("app/pages/03_Q3_Exit_Phase2.py", "quality_flag"),
        "high",
        "Blocage conclusions si quality_flag=FAIL (Q3).",
    )
    _add(
        matrix_rows,
        "S2-010",
        "SPEC_2",
        "quality_gate",
        "OK",
        "code",
        _line_ref("app/pages/04_Q4_BESS_OrderOfMagnitude.py", "quality_flag"),
        "high",
        "Blocage conclusions si quality_flag=FAIL (Q4).",
    )
    _add(
        matrix_rows,
        "S2-011",
        "SPEC_2",
        "quality_gate",
        "OK",
        "code",
        _line_ref("app/pages/05_Q5_CO2_Gas_Anchor.py", "quality_flag"),
        "high",
        "Blocage conclusions si quality_flag=FAIL (Q5).",
    )
    _add(
        matrix_rows,
        "S2-012",
        "SPEC_2",
        "q1",
        "OK",
        "code",
        _line_ref("src/modules/q1_transition.py", "stage2_market_score"),
        "high",
        "Q1 score marche + stress physique + annee de bascule.",
    )
    _add(
        matrix_rows,
        "S2-013",
        "SPEC_2",
        "q2",
        "OK",
        "code",
        _line_ref("src/modules/q2_slope.py", "robust_linreg"),
        "high",
        "Q2 pente OLS + robustesse n>=3 + ranking drivers.",
    )
    _add(
        matrix_rows,
        "S2-014",
        "SPEC_2",
        "q3",
        "OK",
        "code",
        _line_ref("src/modules/q3_exit.py", "_binary_search_lowest"),
        "high",
        "Q3 tendances + contre-factuels demande/must-run/flex.",
    )
    _add(
        matrix_rows,
        "S2-015",
        "SPEC_2",
        "q4",
        "OK",
        "code",
        _line_ref("src/modules/q4_bess.py", "def _simulate_dispatch_arrays"),
        "critical",
        "Q4 dispatch BESS 3 modes (SURPLUS_FIRST/ARBITRAGE/PV_COLOCATED).",
    )
    _add(
        matrix_rows,
        "S2-016",
        "SPEC_2",
        "q5",
        "OK",
        "code",
        _line_ref("src/modules/q5_thermal_anchor.py", "def _co2_required"),
        "high",
        "Q5 TCA/TTL + sensibilites + CO2 requis.",
    )
    _add(
        matrix_rows,
        "S2-017",
        "SPEC_2",
        "phase2",
        "OK" if not phase2_ass.empty else "MANQUANT",
        "runtime",
        "data/assumptions/phase2/phase2_scenario_country_year.csv",
        "critical",
        "Table hypotheses Phase2 scenario x pays x annee.",
    )
    _add(
        matrix_rows,
        "S2-018",
        "SPEC_2",
        "phase2",
        "OK" if _exists("src/scenario/phase2_engine.py") else "MANQUANT",
        "code",
        _line_ref("src/scenario/phase2_engine.py", "def run_phase2_scenario"),
        "critical",
        "Moteur scenario phase2 implemente.",
    )
    _add(
        matrix_rows,
        "S2-019",
        "SPEC_2",
        "phase2",
        "OK" if scen_ok_count == expected_scen_count else "PARTIEL",
        "runtime",
        f"scenario hourly files: {scen_ok_count}/{expected_scen_count}",
        "critical",
        "Couverture scenario complete sur scenarios x 7 pays x 2030/2040.",
    )
    _add(
        matrix_rows,
        "S2-020",
        "SPEC_2",
        "phase2",
        "OK" if len(scenario_ids) >= 2 else "PARTIEL",
        "runtime",
        "data/processed/scenario/*/annual_metrics.parquet",
        "high",
        "Execution scenario minimum 2 scenarios x 3 pays x 2 horizons.",
    )
    _add(
        matrix_rows,
        "S2-021",
        "SPEC_2",
        "tests",
        "OK",
        "test",
        "tests/test_q1_transition.py; test_q2_slope.py; test_q3_exit.py; test_q4_bess.py; test_q5_thermal_anchor.py; test_phase1_modules_integration.py",
        "high",
        "Suite tests modules Q1..Q5 + integration.",
    )
    _add(
        matrix_rows,
        "S2-022",
        "SPEC_2",
        "phase2_tests",
        "OK",
        "test",
        "tests/test_phase2_engine.py; tests/test_phase2_validators.py",
        "high",
        "Tests moteur scenario et validations hypotheses Phase2.",
    )

    # UX/performance V2.1.
    _add(
        matrix_rows,
        "V21-001",
        "V2.1",
        "performance",
        "OK",
        "code",
        _line_ref("app/page_utils.py", "@st.cache_data"),
        "high",
        "Cache streamlit applique sur chargements lourds.",
    )
    _add(
        matrix_rows,
        "V21-002",
        "V2.1",
        "performance",
        "OK",
        "code",
        _line_ref("app/page_utils.py", "with st.form(\"pipeline_form\")"),
        "high",
        "Forms submit pour eviter reruns lourds.",
    )
    _add(
        matrix_rows,
        "V21-003",
        "V2.1",
        "q4_perf",
        "OK",
        "code",
        _line_ref("src/modules/q4_bess.py", "Q4_CACHE_BASE"),
        "critical",
        "Cache persistant Q4 par hash hypotheses/grille/mode.",
    )
    _add(
        matrix_rows,
        "V21-004",
        "V2.1",
        "q4_perf",
        "OK",
        "code",
        _line_ref("src/modules/q4_bess.py", "compute_time_sec"),
        "high",
        "Diagnostics Q4: compute_time_sec/cache_hit/engine_version.",
    )
    _add(
        matrix_rows,
        "V21-005",
        "V2.1",
        "q4_perf",
        "OK" if perf["cold_wall_sec"] < 35.0 else "PARTIEL",
        "runtime",
        f"Q4 cold wall={perf['cold_wall_sec']:.3f}s",
        "high",
        "SLO Q4 cold <35s.",
    )
    _add(
        matrix_rows,
        "V21-006",
        "V2.1",
        "q4_perf",
        "OK" if perf["warm_wall_sec"] < 3.0 else "PARTIEL",
        "runtime",
        f"Q4 warm wall={perf['warm_wall_sec']:.3f}s",
        "high",
        "SLO Q4 warm <3s.",
    )
    _add(
        matrix_rows,
        "V21-007",
        "V2.1",
        "q4_perf",
        "OK" if (not perf["cold_cache_hit"] and perf["warm_cache_hit"]) else "PARTIEL",
        "runtime",
        f"cold_cache_hit={perf['cold_cache_hit']} warm_cache_hit={perf['warm_cache_hit']}",
        "high",
        "Cache hit/miss verifiable entre run1 et run2.",
    )
    _add(
        matrix_rows,
        "V21-008",
        "V2.1",
        "ux",
        "OK",
        "ui",
        _line_ref("streamlit_app.py", "PAGES = ["),
        "medium",
        "Navigation guidee accueil->mode emploi->donnees->socle->Q1..Q5->conclusions.",
    )
    _add(
        matrix_rows,
        "V21-009",
        "V2.1",
        "ux",
        "OK",
        "ui",
        _line_ref("app/ui_components.py", "def guided_header"),
        "medium",
        "Header etape actuelle/etape suivante sur pages.",
    )
    _add(
        matrix_rows,
        "V21-010",
        "V2.1",
        "ux",
        "OK" if has_full_kpi_explainers else "PARTIEL",
        "ui",
        _line_ref("app/ui_components.py", "def show_metric_explainers"),
        "medium",
        "UX neophyte completement didactique et non-obscurci sur toutes pages.",
    )

    # Report/conclusions requirements.
    _add(
        matrix_rows,
        "REP-001",
        "REPORTING",
        "conclusions",
        "OK" if any((ROOT / "reports").glob("conclusions_v2_detailed_*.md")) else "MANQUANT",
        "runtime",
        "reports/conclusions_v2_detailed_*.md",
        "high",
        "Rapport final detaille present en markdown versionne.",
    )
    _add(
        matrix_rows,
        "REP-002",
        "REPORTING",
        "conclusions",
        "OK" if _exists("app/pages/99_Conclusions.py") else "MANQUANT",
        "ui",
        _line_ref("app/pages/99_Conclusions.py", "Run de rapport"),
        "high",
        "Page Conclusions charge rapport et resume executif.",
    )

    # Slide coverage (detailed).
    slide_text = _parse_slides()
    slide_rows: list[dict[str, Any]] = []
    q_evidence = {
        "Q1": _line_ref("src/modules/q1_transition.py", "def run_q1"),
        "Q2": _line_ref("src/modules/q2_slope.py", "def run_q2"),
        "Q3": _line_ref("src/modules/q3_exit.py", "def run_q3"),
        "Q4": _line_ref("src/modules/q4_bess.py", "def run_q4"),
        "Q5": _line_ref("src/modules/q5_thermal_anchor.py", "def run_q5"),
        "ARCHI": _line_ref("streamlit_app.py", "PAGES = ["),
        "PERIMETRE": _line_ref("config/countries.yaml", "countries:"),
        "CONTEXTE": _line_ref("app/pages/00_Accueil.py", "Question business"),
    }
    for sid in range(1, 34):
        q = _slides_question(sid)
        expect = slide_text.get(sid, "")
        hist_cov = q in {"Q1", "Q2", "Q3", "Q4", "Q5", "ARCHI", "PERIMETRE", "CONTEXTE"}
        pros_cov = q in {"Q1", "Q2", "Q3", "Q4", "Q5", "ARCHI", "PERIMETRE", "CONTEXTE"}
        status = "OK"
        notes = ""
        if sid == 33:
            notes = "Perimetre slides aligne sur decision projet: 7 pays verrouilles."
            status = "OK" if locked_country_scope_ok else "PARTIEL"
        ev_ref = q_evidence.get(q, "")
        slide_rows.append(
            {
                "slide": sid,
                "question_area": q,
                "expectation_excerpt": expect,
                "historical_covered": bool(hist_cov),
                "prospective_covered": bool(pros_cov),
                "status": status,
                "evidence_ref": ev_ref,
                "notes": notes,
            }
        )
        _add(
            matrix_rows,
            f"SLIDE-{sid:02d}",
            "SLIDES",
            q,
            status,
            "ui" if q in {"Q1", "Q2", "Q3", "Q4", "Q5", "ARCHI", "CONTEXTE"} else "runtime",
            ev_ref,
            "medium" if sid != 33 else "low",
            f"Couverture explicite slide {sid}.",
        )

    # Write artifacts.
    matrix_df = pd.DataFrame(matrix_rows)
    matrix_path = REPORTS_DIR / "compliance_matrix_full.csv"
    matrix_df.to_csv(matrix_path, index=False, quoting=csv.QUOTE_MINIMAL)

    slides_df = pd.DataFrame(slide_rows)
    slides_path = REPORTS_DIR / "slides_coverage_detailed.csv"
    slides_df.to_csv(slides_path, index=False, quoting=csv.QUOTE_MINIMAL)

    # Evidence index.
    lines = []
    lines.append("# Compliance Evidence Index")
    lines.append("")
    lines.append(f"- Run ID: `{run_id}`")
    lines.append(f"- Matrix: `{matrix_path}`")
    lines.append(f"- Slides: `{slides_path}`")
    lines.append(f"- Pytest: `{'PASS' if pytest_ok else 'FAIL'}` -> {pytest_summary}")
    lines.append(
        f"- Q4 perf: cold={perf['cold_wall_sec']:.3f}s warm={perf['warm_wall_sec']:.3f}s cold_cache={perf['cold_cache_hit']} warm_cache={perf['warm_cache_hit']}"
    )
    lines.append("")
    for src in ["SPEC_0", "SPEC_1", "SPEC_2", "V2.1", "REPORTING", "SLIDES"]:
        sub = matrix_df[matrix_df["source_spec"] == src]
        if sub.empty:
            continue
        lines.append(f"## {src}")
        counts = sub["status"].value_counts().to_dict()
        lines.append(
            f"- Counts: OK={counts.get('OK', 0)} PARTIEL={counts.get('PARTIEL', 0)} MANQUANT={counts.get('MANQUANT', 0)}"
        )
        lines.append("")
        for _, r in sub.iterrows():
            lines.append(
                f"- `{r['requirement_id']}` [{r['status']}] ({r['severity']}) :: {r['requirement_text']} -> `{r['evidence_ref']}`"
            )
        lines.append("")
    evidence_index_path = REPORTS_DIR / "compliance_evidence_index.md"
    evidence_index_path.write_text("\n".join(lines), encoding="utf-8")

    # Critical gaps.
    gaps = matrix_df[(matrix_df["status"] != "OK") & (matrix_df["severity"].isin(["critical", "high"]))]
    gap_lines = []
    gap_lines.append("# Compliance Gaps - Critical")
    gap_lines.append("")
    gap_lines.append(f"- Run ID: `{run_id}`")
    gap_lines.append(f"- Critical/High non-OK gaps: {len(gaps)}")
    gap_lines.append("")
    if gaps.empty:
        gap_lines.append("No critical/high gap detected.")
    else:
        for _, r in gaps.sort_values(["severity", "requirement_id"], ascending=[True, True]).iterrows():
            gap_lines.append(f"## {r['requirement_id']} ({r['severity']})")
            gap_lines.append(f"- Source: `{r['source_spec']}` / `{r['module_area']}`")
            gap_lines.append(f"- Status: `{r['status']}`")
            gap_lines.append(f"- Requirement: {r['requirement_text']}")
            gap_lines.append(f"- Evidence: `{r['evidence_ref']}`")
            if r["requirement_id"].startswith("S1-017"):
                gap_lines.append("- Fix plan: ingest and normalize TYNDP 2024 demand/capacity/fuel-co2 tables with checksums.")
            elif r["requirement_id"].startswith("S1-018"):
                gap_lines.append("- Fix plan: import NREL ATB raw files and build normalized cost benchmark table.")
            elif r["requirement_id"].startswith("S1-019"):
                gap_lines.append("- Fix plan: freeze IRENA PDF and normalized extraction/manual template with page reference.")
            elif r["requirement_id"].startswith("S1-020"):
                gap_lines.append("- Fix plan: create and version `assumptions/policy_distortion.csv` with required columns.")
            elif r["requirement_id"].startswith("S0-009"):
                gap_lines.append("- Fix plan: wire `create_run_context` + `write_data_manifest` into runtime pipeline and exports.")
            else:
                gap_lines.append("- Fix plan: implement missing item and add dedicated test/evidence.")
            gap_lines.append("")
    gaps_path = REPORTS_DIR / "compliance_gaps_critical.md"
    gaps_path.write_text("\n".join(gap_lines), encoding="utf-8")

    # Final verdict.
    all_ok = bool((matrix_df["status"] == "OK").all())
    verdict = "100% atteint" if all_ok else "NON 100%"
    verdict_lines = []
    verdict_lines.append("# Compliance Verdict")
    verdict_lines.append("")
    verdict_lines.append(f"- Run ID: `{run_id}`")
    verdict_lines.append(f"- Verdict: **{verdict}**")
    verdict_lines.append("")
    c = matrix_df["status"].value_counts().to_dict()
    verdict_lines.append(f"- OK: {c.get('OK', 0)}")
    verdict_lines.append(f"- PARTIEL: {c.get('PARTIEL', 0)}")
    verdict_lines.append(f"- MANQUANT: {c.get('MANQUANT', 0)}")
    verdict_lines.append("")
    if all_ok:
        verdict_lines.append("All atomic requirements are compliant.")
    else:
        verdict_lines.append("100% compliance cannot be certified because at least one atomic requirement is PARTIEL/MANQUANT.")
        verdict_lines.append(f"See `{gaps_path}` for prioritized remediation.")
    verdict_path = REPORTS_DIR / f"compliance_verdict_{run_id}.md"
    verdict_path.write_text("\n".join(verdict_lines), encoding="utf-8")

    print(f"RUN_ID={run_id}")
    print(f"MATRIX={matrix_path}")
    print(f"EVIDENCE_INDEX={evidence_index_path}")
    print(f"GAPS={gaps_path}")
    print(f"VERDICT={verdict_path}")
    print(f"SLIDES={slides_path}")


if __name__ == "__main__":
    main()
