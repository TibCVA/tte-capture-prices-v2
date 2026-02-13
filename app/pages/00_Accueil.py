from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json

import pandas as pd
import streamlit as st

_PAGE_UTILS_IMPORT_ERROR: Exception | None = None
_PAGE_UTILS_COMBINED_BUNDLE_AVAILABLE = True

try:
    import app.page_utils as _page_utils

    load_annual_metrics = _page_utils.load_annual_metrics
    load_phase2_assumptions_table = _page_utils.load_phase2_assumptions_table
    refresh_all_analyses_no_cache_ui = _page_utils.refresh_all_analyses_no_cache_ui
    build_bundle_hash = _page_utils.build_bundle_hash

    load_question_bundle_from_combined_run = getattr(_page_utils, "load_question_bundle_from_combined_run", None)
    if callable(load_question_bundle_from_combined_run):
        pass
    else:
        _PAGE_UTILS_COMBINED_BUNDLE_AVAILABLE = False
        load_question_bundle_from_combined_run = None
except Exception as exc:  # pragma: no cover - defensive for Streamlit cloud stale caches
    _PAGE_UTILS_IMPORT_ERROR = exc
    _PAGE_UTILS_COMBINED_BUNDLE_AVAILABLE = False

    def refresh_all_analyses_no_cache_ui(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(f"app.page_utils indisponible (refresh_all_analyses_no_cache_ui). Cause: {exc}")

    def load_annual_metrics(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(f"app.page_utils indisponible (load_annual_metrics). Cause: {exc}")

    def build_bundle_hash(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(f"app.page_utils indisponible (build_bundle_hash). Cause: {exc}")

    def load_question_bundle_from_combined_run(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(f"app.page_utils indisponible (load_question_bundle_from_combined_run). Cause: {exc}")

    def load_phase2_assumptions_table(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError(f"app.page_utils indisponible (load_phase2_assumptions_table). Cause: {exc}")


if not _PAGE_UTILS_COMBINED_BUNDLE_AVAILABLE:
    _PAGE_UTILS_COMBINED_BUNDLE_IMPORT_ERROR = (
        _PAGE_UTILS_IMPORT_ERROR
        if _PAGE_UTILS_IMPORT_ERROR is not None
        else RuntimeError(
            "app.page_utils ne contient pas load_question_bundle_from_combined_run (fallback local activé)."
        )
    )
else:
    _PAGE_UTILS_COMBINED_BUNDLE_IMPORT_ERROR = None

from src.modules.bundle_result import QuestionBundleResult
from src.modules.result import ModuleResult


def _to_abs_project_path(path_like: str | Path) -> Path:
    path = Path(path_like)
    app_root = Path(__file__).resolve().parents[2]
    return path if path.is_absolute() else app_root / path


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
    if not summary:
        raise FileNotFoundError(f"summary.json manquant/invalide: {module_dir / 'summary.json'}")
    checks = summary.get("checks", [])
    if not isinstance(checks, list):
        checks = []
    warnings = summary.get("warnings", [])
    if not isinstance(warnings, list):
        warnings = []
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
        assumptions_used=summary.get("assumptions_used", []),
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


def _load_question_bundle_from_combined_run_local(
    run_id: str,
    question_id: str,
    base_dir: str = "outputs/combined",
) -> tuple[QuestionBundleResult, Path]:
    qid = str(question_id).upper()
    if not str(run_id).strip():
        raise ValueError("run_id vide.")
    q_dir = _to_abs_project_path(base_dir) / str(run_id) / qid
    if not q_dir.exists():
        raise FileNotFoundError(f"Bundle introuvable: {q_dir}")

    bundle_summary = _safe_read_json(q_dir / "summary.json")
    if not bundle_summary:
        raise FileNotFoundError(f"summary.json manquant/invalide: {q_dir / 'summary.json'}")

    default_selection = bundle_summary.get("selection", {})
    if not isinstance(default_selection, dict):
        default_selection = {}

    hist_dir = q_dir / "hist"
    if not hist_dir.exists():
        raise FileNotFoundError(f"Resultat historique introuvable: {hist_dir}")

    hist_result = _load_module_result_from_export(
        hist_dir,
        default_mode="HIST",
        default_run_id=str(bundle_summary.get("run_id", run_id)),
        default_selection=default_selection,
        default_module_id=qid,
        scenario_id=None,
    )

    scen_results: dict[str, ModuleResult] = {}
    scen_root = q_dir / "scen"
    if scen_root.exists():
        for scen_dir in sorted([p for p in scen_root.iterdir() if p.is_dir()]):
            scen_id = str(scen_dir.name)
            scen_results[scen_id] = _load_module_result_from_export(
                scen_dir,
                default_mode="SCEN",
                default_run_id=str(bundle_summary.get("run_id", run_id)),
                default_selection=default_selection,
                default_module_id=qid,
                scenario_id=scen_id,
            )

    checks = bundle_summary.get("checks", [])
    if not isinstance(checks, list):
        checks = []
    warnings = bundle_summary.get("warnings", [])
    if not isinstance(warnings, list):
        warnings = []

    bundle = QuestionBundleResult(
        question_id=qid,
        run_id=str(bundle_summary.get("run_id", run_id)),
        selection=default_selection,
        hist_result=hist_result,
        scen_results=scen_results,
        test_ledger=_safe_read_csv(q_dir / "test_ledger.csv"),
        comparison_table=_safe_read_csv(q_dir / "comparison_hist_vs_scen.csv"),
        checks=checks,
        warnings=[str(w) for w in warnings],
        narrative_md=_safe_read_text(q_dir / "narrative.md"),
    )
    return bundle, q_dir


if load_question_bundle_from_combined_run is None:  # type: ignore[comparison-overlap]
    if _PAGE_UTILS_COMBINED_BUNDLE_IMPORT_ERROR is None:
        _PAGE_UTILS_COMBINED_BUNDLE_IMPORT_ERROR = RuntimeError(
            "app.page_utils ne contient pas load_question_bundle_from_combined_run (fallback local activé)."
        )
    load_question_bundle_from_combined_run = _load_question_bundle_from_combined_run_local

_LLM_BATCH_IMPORT_ERROR: Exception | None = None
try:
    from app.llm_analysis import resolve_openai_api_key
    from app.llm_batch import (
        QUESTION_ORDER,
        build_default_selection,
        prepare_bundle_for_question,
        run_parallel_llm_generation,
    )
    from src.config_loader import load_countries
    from src.pipeline import load_assumptions_table
except Exception as exc:  # pragma: no cover - defensive
    _LLM_BATCH_IMPORT_ERROR = exc
    QUESTION_ORDER = ["Q1", "Q2", "Q3", "Q4", "Q5"]  # type: ignore[assignment]

    def resolve_openai_api_key(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("resolve_openai_api_key indisponible.")

    def build_default_selection(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("build_default_selection indisponible.")

    def prepare_bundle_for_question(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("prepare_bundle_for_question indisponible.")

    def run_parallel_llm_generation(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("run_parallel_llm_generation indisponible.")

    def load_countries(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("load_countries indisponible.")

    def load_assumptions_table(*args, **kwargs):  # type: ignore[no-redef]
        raise RuntimeError("load_assumptions_table indisponible.")

from app.ui_components import (
    guided_header,
    inject_theme,
    render_interpretation,
    render_kpi_cards_styled,
    render_question_box,
)
from src.constants import DEFAULT_COUNTRIES, DEFAULT_YEAR_END, DEFAULT_YEAR_START
from src.modules.bundle_result import export_question_bundle
from src.reporting.interpretation_rules import QUESTION_BUSINESS_TEXT

_RESULT_STATE_KEY_BY_QUESTION = {
    "Q1": "q1_bundle_result",
    "Q2": "q2_bundle_result",
    "Q3": "q3_bundle_result",
    "Q4": "q4_bundle_result",
    "Q5": "q5_bundle_result",
}


def _hydrate_question_pages_from_run(run_id: str) -> tuple[list[str], dict[str, str]]:
    loaded: list[str] = []
    failed: dict[str, str] = {}
    assumptions_phase1 = pd.DataFrame()
    assumptions_phase2 = pd.DataFrame()
    try:
        assumptions_phase1 = load_assumptions_table()
        assumptions_phase2 = load_phase2_assumptions_table()
    except Exception:
        pass
    for qid_raw in QUESTION_ORDER:
        qid = str(qid_raw).upper()
        result_key = _RESULT_STATE_KEY_BY_QUESTION.get(qid)
        if not result_key:
            continue
        try:
            bundle, out_dir = load_question_bundle_from_combined_run(run_id=run_id, question_id=qid)
        except Exception as exc:
            failed[qid] = str(exc)
            continue
        bundle_hash = f"{run_id}_{qid}"
        if isinstance(bundle.selection, dict) and not assumptions_phase1.empty:
            try:
                bundle_hash = build_bundle_hash(qid, bundle.selection, assumptions_phase1, assumptions_phase2)
            except Exception:
                bundle_hash = f"{run_id}_{qid}"
        st.session_state[result_key] = {
            "bundle": bundle,
            "out_dir": str(out_dir),
            "bundle_hash": bundle_hash,
        }
        loaded.append(qid)
    return loaded, failed


def _hydrate_question_pages_from_prepared(prepared_items: list[dict]) -> tuple[list[str], dict[str, str]]:
    loaded: list[str] = []
    failed: dict[str, str] = {}
    for item in prepared_items:
        qid = str(item.get("question_id", "")).upper()
        if not qid:
            continue
        result_key = _RESULT_STATE_KEY_BY_QUESTION.get(qid)
        if not result_key:
            continue
        if str(item.get("status", "")).upper() == "FAILED_PREP":
            failed[qid] = str(item.get("error", "Preparation echouee."))
            continue

        bundle = item.get("bundle", None)
        if bundle is None:
            failed[qid] = "Bundle absent apres preparation."
            continue

        bundle_hash = str(item.get("bundle_hash", "")).strip()
        if not bundle_hash:
            failed[qid] = "Bundle hash absent apres preparation."
            continue

        try:
            out_dir = export_question_bundle(bundle)
        except Exception as exc:
            failed[qid] = f"Export bundle impossible: {exc}"
            continue

        st.session_state[result_key] = {
            "bundle": bundle,
            "out_dir": str(out_dir),
            "bundle_hash": bundle_hash,
        }
        loaded.append(qid)
    return loaded, failed


def render() -> None:
    inject_theme()
    guided_header(
        title="TTE Capture Prices V2",
        purpose="Outil d'analyse historique des capture prices et des phases structurelles, auditable et explicable.",
        step_now="Accueil: comprendre le parcours",
        step_next="Mode d'emploi: definitions et methode",
    )

    render_kpi_cards_styled(
        [
            {"label": "Pays cibles", "value": len(DEFAULT_COUNTRIES), "help": "Perimetre par defaut verrouille a 7 pays."},
            {"label": "Fenetre historique", "value": f"{DEFAULT_YEAR_START}-{DEFAULT_YEAR_END}", "help": "Fenetre par defaut utilisee dans les analyses."},
            {"label": "Resolution", "value": "Horaire UTC", "help": "Aucun calcul infra-horaire (pas 15 min)."},
        ]
    )

    st.markdown("## Ce que fait l'outil")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            '<div class="tte-card" style="min-height:130px;">'
            "<strong>Dynamique des capture prices</strong><br>"
            "Expliquer l'evolution des capture prices PV/Wind sur base horaire pour 7 pays europeens."
            "</div>",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            '<div class="tte-card" style="min-height:130px;">'
            "<strong>Phases structurelles</strong><br>"
            "Identifier les bascules de phase et les drivers physiques/marche (SR, FAR, IR, regimes)."
            "</div>",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            '<div class="tte-card" style="min-height:130px;">'
            "<strong>Tests auditables</strong><br>"
            "Tester les questions Q1..Q5 avec checks automatiques et exports auditables traces au run_id."
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("## Les 5 questions business")
    for qid in ["Q1", "Q2", "Q3", "Q4", "Q5"]:
        text = QUESTION_BUSINESS_TEXT.get(qid, "")
        render_question_box(f"**{qid}** : {text}")

    st.info(
        "Le modele reste volontairement pedestre: il privilegie l'explicabilite et l'auditabilite sur la complexite. "
        "Les conclusions sont toujours conditionnelles aux hypotheses et doivent etre nuancees."
    )

    st.markdown("## Parcours recommande")
    st.markdown(
        "1. **Mode d'emploi**: comprendre les definitions et limites.\n"
        "2. **Donnees & Qualite**: charger ou recalculer les jeux de donnees.\n"
        "3. **Socle Physique**: verifier NRL/surplus/flex avant interpretation.\n"
        "4. **Q1..Q5**: repondre aux questions business module par module.\n"
        "5. **Conclusions**: lire le rapport final trace au run_id."
    )

    st.markdown("## Rafraichissement global des analyses")
    st.caption(
        "Ce bouton reconstruit toutes les analyses (Q1..Q5) sans reutiliser les caches de calculs, "
        "tout en conservant les donnees ENTSO-E brutes deja telechargees en local."
    )
    if _PAGE_UTILS_IMPORT_ERROR is not None:
        st.error("Impossible de charger le module de refresh global.")
        st.code(str(_PAGE_UTILS_IMPORT_ERROR))
    else:
        if st.button("Lancer / rafraichir toutes les analyses (sans cache calcule)", type="primary"):
            with st.spinner("Refresh global en cours (rebuild historique + run combine Q1..Q5)..."):
                try:
                    refresh_summary = refresh_all_analyses_no_cache_ui(
                        countries=DEFAULT_COUNTRIES,
                        hist_year_start=DEFAULT_YEAR_START,
                        hist_year_end=DEFAULT_YEAR_END,
                        scenario_years=list(range(2025, 2036)),
                    )
                except Exception as exc:
                    st.error(f"Echec du refresh global: {exc}")
                else:
                    run_id = str(refresh_summary.get("run_id", "UNKNOWN"))
                    st.session_state["last_full_refresh_run_id"] = run_id
                    st.success(f"Refresh termine. Nouveau run combine: {run_id}")
                    if _PAGE_UTILS_COMBINED_BUNDLE_IMPORT_ERROR is not None:
                        st.warning(
                            "Prechargement auto indisponible: "
                            + str(_PAGE_UTILS_COMBINED_BUNDLE_IMPORT_ERROR)
                        )
                    with st.spinner("Chargement automatique des resultats Q1..Q5 dans les pages..."):
                        loaded_q, failed_q = _hydrate_question_pages_from_run(run_id)
                    if loaded_q:
                        st.info(f"Sections prechargees: {', '.join(loaded_q)}")
                    if failed_q:
                        st.warning(
                            "Prechargement incomplet: "
                            + " | ".join([f"{qid}: {msg}" for qid, msg in failed_q.items()])
                        )
                    with st.expander("Details techniques du refresh", expanded=False):
                        st.json(refresh_summary)

    st.markdown("## Generation IA globale")
    st.caption(
        "Lance en une fois les generations IA Q1->Q5 en parallele, avec les selections par defaut "
        "de chaque page question."
    )
    if _LLM_BATCH_IMPORT_ERROR is not None:
        st.error("Impossible de charger le module de batch IA.")
        st.code(str(_LLM_BATCH_IMPORT_ERROR))
    elif st.button("Generer toutes les analyses IA (Q1->Q5 en parallele)", type="primary"):
        try:
            annual_hist = load_annual_metrics()
        except Exception as exc:
            st.error(f"Impossible de charger annual_metrics: {exc}")
            annual_hist = pd.DataFrame()

        if annual_hist.empty:
            st.error("Aucune metrique annuelle disponible. Le batch IA est bloque.")
        else:
            api_key = resolve_openai_api_key()
            if not api_key:
                st.error("Cle OpenAI manquante. Configure OPENAI_API_KEY dans l'environnement ou les secrets Streamlit.")
            else:
                assumptions_phase1 = load_assumptions_table()
                assumptions_phase2 = load_phase2_assumptions_table()
                countries_cfg = load_countries()

                prepared_items: list[dict] = []
                prep_progress = st.progress(0.0)
                prep_status = st.empty()
                total_q = len(QUESTION_ORDER)

                for idx, qid in enumerate(QUESTION_ORDER, start=1):
                    prep_status.text(f"Preparation bundle {qid} ({idx}/{total_q})...")
                    try:
                        selection = build_default_selection(
                            qid,
                            annual_hist=annual_hist,
                            assumptions_phase2=assumptions_phase2,
                            countries_cfg=countries_cfg,
                        )
                        prepared = prepare_bundle_for_question(
                            qid,
                            selection=selection,
                            assumptions_phase1=assumptions_phase1,
                            assumptions_phase2=assumptions_phase2,
                        )
                    except Exception as exc:
                        prepared = {
                            "question_id": qid,
                            "status": "FAILED_PREP",
                            "bundle_hash": "",
                            "error": str(exc),
                        }
                    prepared_items.append(prepared)
                    prep_progress.progress(idx / max(total_q * 2, 1))

                prep_status.text("Prechargement des sections Q1..Q5...")
                loaded_q, failed_q = _hydrate_question_pages_from_prepared(prepared_items)

                prep_status.text("Generation IA en parallele en cours...")
                with st.spinner("Appels IA Q1->Q5 en execution parallele..."):
                    rows = run_parallel_llm_generation(
                        prepared_items=prepared_items,
                        api_key=api_key,
                        max_workers=5,
                    )
                prep_progress.progress(1.0)
                prep_status.empty()
                prep_progress.empty()

                ok_count = sum(1 for row in rows if row.get("status") == "OK")
                fail_count = len(rows) - ok_count
                st.session_state["last_llm_batch_result"] = {
                    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
                    "rows": rows,
                }
                if loaded_q:
                    st.info(f"Sections prechargees apres batch IA: {', '.join(loaded_q)}")
                if failed_q:
                    st.warning(
                        "Prechargement partiel apres batch IA: "
                        + " | ".join([f"{qid}: {msg}" for qid, msg in failed_q.items()])
                    )
                if fail_count == 0:
                    st.success(f"Generation IA terminee: {ok_count}/{len(rows)} questions traitees.")
                else:
                    st.warning(f"Generation IA terminee avec erreurs: {ok_count} succes, {fail_count} echec(s).")

    last_batch = st.session_state.get("last_llm_batch_result")
    if isinstance(last_batch, dict) and isinstance(last_batch.get("rows"), list):
        ts = str(last_batch.get("generated_at_utc", ""))
        if ts:
            st.caption(f"Derniere execution batch IA: {ts}")
        table_rows = list(last_batch.get("rows", []))
        if table_rows:
            st.dataframe(pd.DataFrame(table_rows), use_container_width=True)

    render_interpretation(
        "Suivre ce parcours dans l'ordre garantit que chaque etape repose sur des donnees validees. "
        "Ne pas sauter directement aux conclusions sans avoir verifie la qualite des donnees."
    )
