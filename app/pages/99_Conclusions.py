from __future__ import annotations

from io import BytesIO
from pathlib import Path
import re

import pandas as pd
import streamlit as st

from app.ui_components import (
    guided_header,
    inject_theme,
    render_interpretation,
    render_kpi_cards_styled,
)
from src.reporting.evidence_loader import (
    REQUIRED_QUESTIONS,
    assemble_complete_run_from_fragments,
    discover_complete_runs,
)


def _run_has_all_questions(run_dir: Path) -> bool:
    return all((run_dir / q).exists() for q in REQUIRED_QUESTIONS)


def _report_paths(run_id: str) -> dict[str, Path]:
    rid = str(run_id)
    base = Path("reports")
    return {
        "detailed": base / f"conclusions_v2_detailed_{rid}.md",
        "executive": base / f"conclusions_v2_executive_{rid}.md",
        "evidence_catalog": base / f"evidence_catalog_{rid}.csv",
        "test_traceability": base / f"test_traceability_{rid}.csv",
        "slides_traceability": base / f"slides_traceability_{rid}.csv",
        "report_qc": base / f"report_qc_{rid}.json",
    }


def _safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def _scenario_ids(question_dir: Path) -> list[str]:
    scen_root = question_dir / "scen"
    if not scen_root.exists():
        return []
    return sorted([p.name for p in scen_root.iterdir() if p.is_dir()])


def _collect_question_full_pairs(question_dir: Path) -> list[tuple[str, Path]]:
    pairs: list[tuple[str, Path]] = []
    for path in sorted(question_dir.rglob("*.csv")):
        rel = path.relative_to(question_dir).as_posix().replace("/", "__").replace(".csv", "")
        pairs.append((f"all__{rel}", path))
    return pairs


def _collect_hist_pairs(question_dir: Path) -> list[tuple[str, Path]]:
    pairs: list[tuple[str, Path]] = []
    hist_tables = question_dir / "hist" / "tables"
    if hist_tables.exists():
        for path in sorted(hist_tables.glob("*.csv")):
            pairs.append((f"hist__{path.stem}", path))
    hist_summary = question_dir / "hist" / "summary.csv"
    if hist_summary.exists():
        pairs.append(("hist__summary", hist_summary))
    return pairs


def _collect_audit_pairs(question_dir: Path) -> list[tuple[str, Path]]:
    pairs: list[tuple[str, Path]] = []
    for name in ["test_ledger.csv", "comparison_hist_vs_scen.csv", "checks_filtered.csv", "warnings_filtered.csv"]:
        path = question_dir / name
        if path.exists():
            pairs.append((f"audit__{path.stem}", path))

    for scenario_id in _scenario_ids(question_dir):
        scen_dir = question_dir / "scen" / scenario_id
        for name in ["checks_filtered.csv", "warnings_filtered.csv", "test_ledger.csv", "comparison_hist_vs_scen.csv"]:
            path = scen_dir / name
            if path.exists():
                pairs.append((f"audit__{scenario_id}__{path.stem}", path))
    return pairs


def _collect_scenario_pairs(question_dir: Path, scenario_id: str) -> list[tuple[str, Path]]:
    pairs: list[tuple[str, Path]] = []
    scen_dir = question_dir / "scen" / str(scenario_id)
    tables_dir = scen_dir / "tables"

    if tables_dir.exists():
        for path in sorted(tables_dir.glob("*.csv")):
            pairs.append((f"{scenario_id}__tbl__{path.stem}", path))

    for name in ["checks_filtered.csv", "warnings_filtered.csv", "test_ledger.csv", "comparison_hist_vs_scen.csv"]:
        path = scen_dir / name
        if path.exists():
            pairs.append((f"{scenario_id}__{path.stem}", path))
    return pairs


def _sheet_name(raw_name: str, used: set[str]) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]+", "_", raw_name).strip("_")
    if not cleaned:
        cleaned = "sheet"
    cleaned = cleaned[:31]
    candidate = cleaned
    idx = 2
    while candidate in used:
        suffix = f"_{idx}"
        candidate = f"{cleaned[: max(1, 31 - len(suffix))]}{suffix}"
        idx += 1
    used.add(candidate)
    return candidate


@st.cache_data(show_spinner=False)
def _build_excel_bytes_cached(
    csv_paths: tuple[str, ...],
    csv_mtimes: tuple[int, ...],
    sheet_labels: tuple[str, ...],
) -> bytes:
    _ = csv_mtimes
    buffer = BytesIO()
    used_sheet_names: set[str] = set()
    manifest_rows: list[dict[str, object]] = []

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        for path_str, label in zip(csv_paths, sheet_labels):
            path = Path(path_str)
            df = pd.read_csv(path)
            sheet = _sheet_name(label, used_sheet_names)
            df.to_excel(writer, sheet_name=sheet, index=False)
            manifest_rows.append(
                {
                    "sheet_name": sheet,
                    "source_csv": path_str,
                    "rows": int(len(df)),
                    "columns": int(len(df.columns)),
                }
            )

        manifest_df = pd.DataFrame(manifest_rows)
        manifest_sheet = _sheet_name("_manifest", used_sheet_names)
        manifest_df.to_excel(writer, sheet_name=manifest_sheet, index=False)

    buffer.seek(0)
    return buffer.getvalue()


def _build_excel_bytes_from_pairs(pairs: list[tuple[str, Path]]) -> bytes:
    if not pairs:
        raise ValueError("Aucun fichier CSV a exporter.")

    ordered = sorted(pairs, key=lambda x: x[0])
    csv_paths = tuple(str(path.resolve()) for _, path in ordered)
    csv_mtimes = tuple(int(Path(path).stat().st_mtime_ns) for path in csv_paths)
    labels = tuple(label for label, _ in ordered)
    return _build_excel_bytes_cached(csv_paths, csv_mtimes, labels)


def _source_inventory_df(question_dir: Path) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for path in sorted(question_dir.rglob("*.csv")):
        try:
            df = pd.read_csv(path)
            n_rows = int(len(df))
            n_cols = int(len(df.columns))
        except Exception:
            n_rows = -1
            n_cols = -1
        rows.append(
            {
                "relative_path": path.relative_to(question_dir).as_posix(),
                "rows": n_rows,
                "columns": n_cols,
            }
        )
    return pd.DataFrame(rows)


def render() -> None:
    inject_theme()
    guided_header(
        title="Conclusions - Exports Auditables",
        purpose="Telechargement des resultats bruts en Excel, question par question et analyse par analyse.",
        step_now="Conclusions: export brut auditable",
        step_next="Fin du parcours",
    )

    complete_runs = discover_complete_runs(Path("outputs/combined"))
    if not complete_runs:
        st.warning("Aucun run combine complet (Q1..Q5) detecte dans outputs/combined.")
        st.info("Lance d'abord un run global depuis la page Accueil.")
        return

    run_ids = [p.name for p in complete_runs]
    preferred_run = str(st.session_state.get("last_full_refresh_run_id", ""))
    default_index = run_ids.index(preferred_run) if preferred_run in run_ids else 0
    selected_run = st.selectbox("Run combine", run_ids, index=default_index)
    run_dir = Path("outputs/combined") / selected_run

    questions_available = [q for q in REQUIRED_QUESTIONS if (run_dir / q).exists()]
    if not questions_available:
        st.error(f"Run {selected_run} invalide: aucune question Q1..Q5 trouvee.")
        return

    selected_question = st.selectbox("Question", questions_available, index=0)
    question_dir = run_dir / selected_question
    scenarios = _scenario_ids(question_dir)
    question_csv_count = len(list(question_dir.rglob("*.csv")))

    render_kpi_cards_styled(
        [
            {"label": "Run ID", "value": selected_run, "help": "Run combine source des exports."},
            {"label": "Question", "value": selected_question, "help": "Question audit selectionnee."},
            {"label": "CSV detectes", "value": question_csv_count, "help": "Nombre total de fichiers CSV exportables."},
            {"label": "Scenarios", "value": len(scenarios), "help": "Scenarios prospectifs disponibles pour cette question."},
        ]
    )

    st.markdown("## Export par analyse")
    full_pairs = _collect_question_full_pairs(question_dir)
    hist_pairs = _collect_hist_pairs(question_dir)
    audit_pairs = _collect_audit_pairs(question_dir)

    c1, c2, c3 = st.columns(3)
    with c1:
        if full_pairs:
            st.download_button(
                label=f"Telecharger {selected_question} - COMPLET",
                data=_build_excel_bytes_from_pairs(full_pairs),
                file_name=f"{selected_run}_{selected_question}_FULL.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        else:
            st.info("Aucun CSV disponible pour l'export complet.")
    with c2:
        if hist_pairs:
            st.download_button(
                label=f"Telecharger {selected_question} - HIST",
                data=_build_excel_bytes_from_pairs(hist_pairs),
                file_name=f"{selected_run}_{selected_question}_HIST.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        else:
            st.info("Aucun export historique disponible.")
    with c3:
        if audit_pairs:
            st.download_button(
                label=f"Telecharger {selected_question} - AUDIT",
                data=_build_excel_bytes_from_pairs(audit_pairs),
                file_name=f"{selected_run}_{selected_question}_AUDIT.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        else:
            st.info("Aucun export audit disponible.")

    st.markdown("## Export scenario par scenario")
    if not scenarios:
        st.info("Aucun scenario disponible pour cette question.")
    else:
        for scenario_id in scenarios:
            scen_pairs = _collect_scenario_pairs(question_dir, scenario_id)
            left, right = st.columns([3, 2])
            with left:
                st.markdown(f"**{scenario_id}** - {len(scen_pairs)} fichier(s) CSV")
            with right:
                if scen_pairs:
                    st.download_button(
                        label=f"Telecharger {scenario_id}",
                        data=_build_excel_bytes_from_pairs(scen_pairs),
                        file_name=f"{selected_run}_{selected_question}_{scenario_id}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True,
                        key=f"dl_{selected_run}_{selected_question}_{scenario_id}",
                    )
                else:
                    st.caption("Aucun fichier scenario.")

    st.markdown("## Inventaire des sources CSV")
    inventory = _source_inventory_df(question_dir)
    if inventory.empty:
        st.info("Aucun CSV detecte.")
    else:
        st.dataframe(inventory, use_container_width=True, hide_index=True)

    render_interpretation(
        "Chaque fichier Excel contient un onglet `_manifest` qui trace les feuilles, les chemins CSV sources "
        "et leurs dimensions. Cela permet un audit direct table par table."
    )
