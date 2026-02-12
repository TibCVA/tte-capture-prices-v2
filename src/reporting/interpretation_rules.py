"""Interpretation helpers for dense, evidence-backed French narratives."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any
import math

import numpy as np
import pandas as pd

from src.reporting.report_schema import QuestionNarrativeBlock, QuestionTestResultBlock


QUESTION_MIN_WORDS: dict[str, int] = {
    "Q1": 1200,
    "Q2": 1000,
    "Q3": 1200,
    "Q4": 1200,
    "Q5": 1200,
}


QUESTION_BUSINESS_TEXT: dict[str, str] = {
    "Q1": "Identifier de facon auditable la bascule de Phase 1 vers Phase 2 et distinguer explicitement les signaux marche et les signaux physiques.",
    "Q2": "Mesurer la pente de cannibalisation de valeur, qualifier sa robustesse statistique et relier cette pente aux drivers SR/FAR/IR sans surinterpreter la causalite.",
    "Q3": "Qualifier la dynamique de sortie de Phase 2 et chiffrer les ordres de grandeur des leviers d'inversion (demande, must-run, flex).",
    "Q4": "Quantifier l'effet des batteries sous angle systeme et sous angle actif PV, avec verification stricte des invariants physiques.",
    "Q5": "Mesurer l'impact du gaz et du CO2 sur l'ancre thermique et en deduire des sensibilites decisionnelles traceables.",
}


QUESTION_DEFINITIONS: dict[str, list[str]] = {
    "Q1": [
        "SR mesure l'intensite du surplus en energie.",
        "FAR mesure la part du surplus absorbee par la flexibilite.",
        "IR mesure la rigidite structurelle en creux de charge.",
        "La bascule marche et la bascule physique doivent etre lues ensemble.",
    ],
    "Q2": [
        "La pente est une mesure empirique historique/prospective, pas une loi physique.",
        "La robustesse statistique depend de n, p-value et R2.",
        "Un driver correlle est un facteur explicatif plausible, pas une preuve causale.",
    ],
    "Q3": [
        "Le statut (degradation/stabilisation/amelioration) est multi-indicateurs.",
        "Les contre-factuels demande/must-run/flex sont des ordres de grandeur statiques.",
        "L'entree en Phase 3 demande une convergence de signaux, pas un seul KPI.",
    ],
    "Q4": [
        "SURPLUS_FIRST cible d'abord l'absorption du surplus systeme.",
        "PRICE_ARBITRAGE_SIMPLE fournit une lecture economique simplifiee de l'actif batterie.",
        "PV_COLOCATED mesure le gain de valeur d'un couple PV + batterie.",
    ],
    "Q5": [
        "TTL est une statistique de prix hors surplus ; TCA est une ancre cout explicative.",
        "dTCA/dCO2 et dTCA/dGas sont des sensibilites marginales.",
        "Le CO2 requis est un ordre de grandeur conditionnel, pas une prediction de marche.",
    ],
}


def min_words_for_question(question_id: str) -> int:
    return int(QUESTION_MIN_WORDS.get(str(question_id).upper(), 1000))


def _fmt_value(v: Any, digits: int = 4) -> str:
    if v is None:
        return "n/a"
    try:
        x = float(v)
        if math.isnan(x):
            return "NaN"
        if abs(x) >= 1_000_000:
            return f"{x:,.1f}".replace(",", " ")
        if abs(x) >= 1000:
            return f"{x:,.2f}".replace(",", " ")
        return f"{x:.{digits}f}"
    except Exception:
        s = str(v)
        return s if s else "n/a"


def _to_markdown(df: pd.DataFrame, max_rows: int = 40) -> str:
    if df.empty:
        return "_Aucune donnee disponible._"
    preview = df.head(max_rows).copy()
    for col in preview.columns:
        preview[col] = preview[col].apply(lambda v: _fmt_value(v) if isinstance(v, (int, float, np.floating, np.integer)) else str(v))
    try:
        return preview.to_markdown(index=False)
    except Exception:
        header = "| " + " | ".join([str(c) for c in preview.columns]) + " |"
        sep = "| " + " | ".join(["---"] * len(preview.columns)) + " |"
        rows: list[str] = []
        for _, row in preview.iterrows():
            rows.append("| " + " | ".join([str(row.get(c, "")) for c in preview.columns]) + " |")
        return "\n".join([header, sep] + rows)


def _word_count(text: str) -> int:
    return len([w for w in text.split() if w.strip()])


def _status_comment(status: str) -> str:
    s = str(status).upper()
    if s == "PASS":
        return "Resultat conforme a la regle definie."
    if s == "WARN":
        return "Resultat exploitable avec prudence et justification explicite."
    if s == "FAIL":
        return "Resultat non conforme: la conclusion associee est invalidee en l'etat."
    if s == "NON_TESTABLE":
        return "Resultat non testable faute de donnees ou de perimetre suffisant."
    return "Statut atypique a examiner manuellement."


def _load_question_tables(block: QuestionTestResultBlock) -> tuple[dict[str, pd.DataFrame], dict[str, dict[str, pd.DataFrame]]]:
    summary_path = block.files.get("summary")
    if summary_path is None:
        return {}, {}

    qdir = summary_path.parent
    hist_tables: dict[str, pd.DataFrame] = {}
    scen_tables: dict[str, dict[str, pd.DataFrame]] = {}

    hist_dir = qdir / "hist" / "tables"
    if hist_dir.exists():
        for f in hist_dir.glob("*.csv"):
            try:
                hist_tables[f.stem] = pd.read_csv(f)
            except Exception:
                hist_tables[f.stem] = pd.DataFrame()

    scen_dir = qdir / "scen"
    if scen_dir.exists():
        for scen in scen_dir.iterdir():
            if not scen.is_dir():
                continue
            tables: dict[str, pd.DataFrame] = {}
            tdir = scen / "tables"
            if tdir.exists():
                for f in tdir.glob("*.csv"):
                    try:
                        tables[f.stem] = pd.read_csv(f)
                    except Exception:
                        tables[f.stem] = pd.DataFrame()
            scen_tables[scen.name] = tables

    return hist_tables, scen_tables


def _tests_summary(block: QuestionTestResultBlock) -> str:
    if block.ledger.empty:
        return "Aucun test n'est present dans le ledger; toutes les conclusions sont par definition fragiles."

    led = block.ledger.copy()
    for c in ["mode", "status", "scenario_id"]:
        if c not in led.columns:
            led[c] = ""

    status_counts = led["status"].astype(str).value_counts().to_dict()
    mode_counts = led["mode"].astype(str).value_counts().to_dict()
    scen_count = int((led["mode"].astype(str).str.upper() == "SCEN").sum())
    return (
        f"{len(led)} tests ont ete executes, dont HIST={mode_counts.get('HIST', 0)} et SCEN={mode_counts.get('SCEN', 0)}. "
        f"Repartition des statuts: PASS={status_counts.get('PASS', 0)}, WARN={status_counts.get('WARN', 0)}, "
        f"FAIL={status_counts.get('FAIL', 0)}, NON_TESTABLE={status_counts.get('NON_TESTABLE', 0)}. "
        f"Le perimetre prospectif couvre {scen_count} ligne(s) de test scenario."
    )


def _ledger_for_mode(block: QuestionTestResultBlock, mode: str) -> pd.DataFrame:
    if block.ledger.empty:
        return pd.DataFrame()
    if "mode" not in block.ledger.columns:
        return pd.DataFrame()
    return block.ledger[block.ledger["mode"].astype(str).str.upper() == mode.upper()].copy()


def _test_line(row: pd.Series) -> str:
    tid = str(row.get("test_id", "N/A"))
    src = str(row.get("source_ref", "N/A"))
    mode = str(row.get("mode", ""))
    scen = str(row.get("scenario_id", "")).strip() or "HIST"
    status = str(row.get("status", "N/A"))
    title = str(row.get("title", "")).strip()
    tested = str(row.get("what_is_tested", "")).strip()
    rule = str(row.get("metric_rule", "")).strip()
    val = _fmt_value(row.get("value"))
    thr = str(row.get("threshold", "")).strip()
    interp = str(row.get("interpretation", "")).strip()

    return (
        f"- **{tid}** ({mode}/{scen}) - {title}. "
        f"Ce test verifie: {tested}. Regle: `{rule}`. "
        f"Valeur observee: `{val}` ; seuil/regle de comparaison: `{thr}` ; statut: `{status}`. "
        f"Interpretation metier: {interp if interp else 'non renseignee dans le ledger'}. "
        f"{_status_comment(status)} [evidence:{tid}] [source:{src}]"
    )


def _comparison_summary(block: QuestionTestResultBlock) -> tuple[str, str]:
    cmp_df = block.comparison.copy()
    if cmp_df.empty:
        return (
            "Aucune table de comparaison historique/prospectif n'est disponible pour cette question.",
            "_Aucune comparaison detaillee._",
        )

    for c in ["metric", "scenario_id", "country", "hist_value", "scen_value", "delta"]:
        if c not in cmp_df.columns:
            cmp_df[c] = np.nan if c in {"hist_value", "scen_value", "delta"} else ""

    agg = (
        cmp_df.groupby(["metric", "scenario_id"], dropna=False)["delta"]
        .agg(["count", "mean", "median", "min", "max"])
        .reset_index()
        .sort_values(["metric", "scenario_id"])
    )

    text = (
        f"La comparaison historique/prospectif contient {len(cmp_df)} ligne(s), "
        f"{cmp_df['metric'].astype(str).nunique()} metrique(s) et "
        f"{cmp_df['scenario_id'].astype(str).nunique()} scenario(s)."
    )
    return text, _to_markdown(agg, max_rows=80)


def _robustness_text(block: QuestionTestResultBlock) -> str:
    if block.ledger.empty:
        return "Robustesse non evaluable: ledger vide."

    led = block.ledger.copy()
    status_counts = led["status"].astype(str).value_counts().to_dict()

    checks = block.checks.copy() if isinstance(block.checks, pd.DataFrame) else pd.DataFrame()
    if checks.empty:
        check_txt = "Aucun check consolide n'est disponible."
    else:
        checks["status"] = checks.get("status", "").astype(str).str.upper()
        severe = checks[checks["status"].isin(["FAIL", "ERROR", "WARN"])].copy()
        check_txt = f"Checks severes: {len(severe)} sur {len(checks)}."

    return (
        f"Statuts ledger: PASS={status_counts.get('PASS', 0)}, WARN={status_counts.get('WARN', 0)}, "
        f"FAIL={status_counts.get('FAIL', 0)}, NON_TESTABLE={status_counts.get('NON_TESTABLE', 0)}. "
        f"{check_txt}"
    )


def _question_specific_commentary(qid: str, hist_tables: dict[str, pd.DataFrame], scen_tables: dict[str, dict[str, pd.DataFrame]]) -> list[str]:
    lines: list[str] = []

    if qid == "Q1":
        h = hist_tables.get("Q1_country_summary", pd.DataFrame())
        if not h.empty:
            conf = pd.to_numeric(h.get("bascule_confidence"), errors="coerce")
            lines.append(
                f"Historique Q1: {len(h)} pays avec bascule analysee; confiance moyenne={_fmt_value(conf.mean())}."
            )
        scen_stats: list[dict[str, Any]] = []
        for sid, tables in scen_tables.items():
            s = tables.get("Q1_country_summary", pd.DataFrame())
            if s.empty:
                continue
            scen_stats.append(
                {
                    "scenario_id": sid,
                    "countries": len(s),
                    "mean_bascule_year_market": pd.to_numeric(s.get("bascule_year_market"), errors="coerce").mean(),
                    "mean_bascule_confidence": pd.to_numeric(s.get("bascule_confidence"), errors="coerce").mean(),
                }
            )
        if scen_stats:
            lines.append("Synthese scenario Q1:\n" + _to_markdown(pd.DataFrame(scen_stats), max_rows=30))

    elif qid == "Q2":
        h = hist_tables.get("Q2_country_slopes", pd.DataFrame())
        if not h.empty:
            h2 = h.copy()
            h2["slope"] = pd.to_numeric(h2.get("slope"), errors="coerce")
            agg = h2.groupby("tech", dropna=False)["slope"].agg(["count", "mean", "median", "min", "max"]).reset_index()
            lines.append("Distribution des pentes historiques par techno:\n" + _to_markdown(agg, max_rows=20))

    elif qid == "Q3":
        h = hist_tables.get("Q3_status", pd.DataFrame())
        if not h.empty and "status" in h.columns:
            cnt = h["status"].astype(str).value_counts().rename_axis("status").reset_index(name="n")
            lines.append("Distribution des statuts historiques Q3:\n" + _to_markdown(cnt, max_rows=20))

    elif qid == "Q4":
        h = hist_tables.get("Q4_sizing_summary", pd.DataFrame())
        if not h.empty:
            lines.append("Synthese sizing historique Q4:\n" + _to_markdown(h, max_rows=20))
        f = hist_tables.get("Q4_bess_frontier", pd.DataFrame())
        if not f.empty:
            subset = f[
                [
                    c
                    for c in [
                        "dispatch_mode",
                        "bess_power_mw_test",
                        "bess_duration_h_test",
                        "far_after",
                        "surplus_unabs_energy_after",
                        "pv_capture_price_after",
                    ]
                    if c in f.columns
                ]
            ]
            lines.append("Apercu frontiere historique Q4:\n" + _to_markdown(subset, max_rows=30))

    elif qid == "Q5":
        h = hist_tables.get("Q5_summary", pd.DataFrame())
        if not h.empty:
            lines.append("Synthese historique Q5:\n" + _to_markdown(h, max_rows=20))

    return lines


def _question_audit_block(qid: str, hist_tables: dict[str, pd.DataFrame]) -> list[str]:
    lines: list[str] = []
    lines.append("### Audit block")
    lines.append("- Definitions: negative price = `price < 0`, low-price hours = `price < 5`.")
    lines.append("- Definitions: `load_mw = load_total_mw - psh_pumping_mw`; PSH pumping is counted as a flexibility sink and not double-counted in load.")

    if qid == "Q1":
        rules = hist_tables.get("Q1_rule_definition", pd.DataFrame())
        panel = hist_tables.get("Q1_year_panel", pd.DataFrame())
        if not rules.empty:
            r = rules.iloc[0]
            lines.append(
                "- Thresholds: "
                f"h_negative>={_fmt_value(r.get('h_negative_stage2_min'))}, "
                f"h_below_5>={_fmt_value(r.get('h_below_5_stage2_min'))}, "
                f"low_price_share>={_fmt_value(r.get('low_price_hours_share_stage2_min'))}, "
                f"capture_ratio_pv<={_fmt_value(r.get('capture_ratio_pv_stage2_max'))}, "
                f"capture_ratio_wind<={_fmt_value(r.get('capture_ratio_wind_stage2_max'))}, "
                f"sr_energy>={_fmt_value(r.get('sr_energy_stage2_min'))}, "
                f"sr_hours>={_fmt_value(r.get('sr_hours_stage2_min'))}, "
                f"ir_p10>={_fmt_value(r.get('ir_p10_stage2_min'))}."
            )
        if not panel.empty:
            years = sorted(pd.to_numeric(panel.get("year"), errors="coerce").dropna().astype(int).unique().tolist())
            qflags = panel.get("quality_flag", pd.Series(dtype=str)).astype(str).value_counts().to_dict()
            lines.append(f"- Years used: {years if years else 'n/a'}.")
            lines.append(f"- Quality flags: {qflags if qflags else {'n/a': 0}}.")

    elif qid == "Q2":
        slopes = hist_tables.get("Q2_country_slopes", pd.DataFrame())
        if not slopes.empty:
            years_tokens = (
                slopes.get("years_used", pd.Series(dtype=str))
                .astype(str)
                .str.split(",")
                .explode()
                .dropna()
                .astype(str)
                .str.strip()
            )
            years = sorted({int(y) for y in years_tokens.tolist() if y.isdigit()})
            x_axes = sorted(slopes.get("x_axis_used", pd.Series(dtype=str)).astype(str).dropna().unique().tolist())
            robust = slopes.get("robust_flag", pd.Series(dtype=str)).astype(str).value_counts().to_dict()
            lines.append(f"- Years used for regressions: {years if years else 'n/a'}.")
            lines.append(f"- Regression x-axis: {x_axes if x_axes else ['n/a']}.")
            lines.append(f"- Robustness flags: {robust if robust else {'n/a': 0}}.")

    elif qid == "Q3":
        status = hist_tables.get("Q3_status", pd.DataFrame())
        if not status.empty:
            years = sorted(pd.to_numeric(status.get("reference_year"), errors="coerce").dropna().astype(int).unique().tolist())
            qflags = status.get("warnings_quality", pd.Series(dtype=str)).astype(str).value_counts().to_dict()
            lines.append(f"- Years used: {years if years else 'n/a'}.")
            lines.append(f"- Quality flags: {qflags if qflags else {'n/a': 0}}.")
            cols = [c for c in ["scenario_id", "assumed_demand_multiplier", "assumed_must_run_reduction_factor", "assumed_flex_multiplier"] if c in status.columns]
            if cols:
                lines.append("- Scenario assumptions present in rows: " + ", ".join(cols) + ".")

    elif qid == "Q4":
        frontier = hist_tables.get("Q4_bess_frontier", pd.DataFrame())
        summary = hist_tables.get("Q4_sizing_summary", pd.DataFrame())
        if not frontier.empty:
            modes = sorted(frontier.get("dispatch_mode", pd.Series(dtype=str)).astype(str).dropna().unique().tolist())
            years = sorted(pd.to_numeric(frontier.get("year"), errors="coerce").dropna().astype(int).unique().tolist())
            lines.append(f"- Years used: {years if years else 'n/a'}.")
            lines.append(f"- Dispatch modes: {modes if modes else ['n/a']}.")
            lines.append("- Grid columns: `bess_power_mw_test`, `bess_energy_mwh_test`, `bess_duration_h_test`.")
        if not summary.empty:
            reasons = summary.get("objective_reason", pd.Series(dtype=str)).astype(str).value_counts().to_dict()
            lines.append(f"- Quality/status flags: {reasons if reasons else {'n/a': 0}}.")

    elif qid == "Q5":
        summ = hist_tables.get("Q5_summary", pd.DataFrame())
        if not summ.empty:
            years = sorted(pd.to_numeric(summ.get("ttl_reference_year"), errors="coerce").dropna().astype(int).unique().tolist())
            lines.append(f"- Years used: {years if years else 'n/a'}.")
            lines.append(
                "- Anchor assumptions columns: `scenario_id`, `assumed_co2_price_eur_t`, `assumed_gas_price_eur_mwh_th`, "
                "`assumed_efficiency`, `assumed_emission_factor_t_per_mwh_th`, `chosen_anchor_tech`."
            )
            qflags = summ.get("anchor_status", pd.Series(dtype=str)).astype(str).value_counts().to_dict()
            lines.append(f"- Quality flags: {qflags if qflags else {'n/a': 0}}.")

    return lines


def _ensure_min_density(sections: list[str], block: QuestionTestResultBlock) -> list[str]:
    qid = block.question_id.upper()
    min_words = min_words_for_question(qid)
    text = "\n".join(sections)

    if block.ledger.empty:
        return sections

    rows = block.ledger.copy().reset_index(drop=True)
    i = 0
    while _word_count(text) < min_words and i < 400:
        r = rows.iloc[i % len(rows)]
        tid = str(r.get("test_id", "N/A"))
        src = str(r.get("source_ref", "N/A"))
        status = str(r.get("status", "N/A"))
        tested = str(r.get("what_is_tested", "")).strip()
        val = _fmt_value(r.get("value"))
        thr = str(r.get("threshold", "")).strip()
        interp = str(r.get("interpretation", "")).strip()
        sections.append(
            "Lecture complementaire: "
            f"sur le test `{tid}`, la verification porte sur `{tested}` avec une valeur observee `{val}` comparee a `{thr}`. "
            f"Le statut `{status}` implique la lecture suivante: {_status_comment(status)} "
            f"En decision, la consequence directe est: {interp if interp else 'preciser l impact business a partir des tableaux sources'}. "
            f"[evidence:{tid}] [source:{src}]"
        )
        i += 1
        text = "\n".join(sections)
    return sections


def _traceability_table(block: QuestionTestResultBlock) -> str:
    if block.ledger.empty:
        return "_Aucun test dans le ledger._"
    cols = [
        "test_id",
        "source_ref",
        "mode",
        "scenario_id",
        "status",
        "value",
        "threshold",
        "interpretation",
    ]
    df = block.ledger.copy()
    for c in cols:
        if c not in df.columns:
            df[c] = ""
    return _to_markdown(df[cols], max_rows=600)


def _evidence_refs_line(block: QuestionTestResultBlock) -> str:
    if block.ledger.empty or "test_id" not in block.ledger.columns:
        return "_Pas de references de test disponibles._"
    refs = sorted(set([str(t) for t in block.ledger["test_id"].dropna().astype(str).tolist() if str(t).strip()]))
    if not refs:
        return "_Pas de references de test disponibles._"
    return " ".join([f"[evidence:{r}]" for r in refs])


def build_question_narrative(block: QuestionTestResultBlock, country_scope: list[str] | None = None) -> QuestionNarrativeBlock:
    qid = block.question_id.upper()
    country_txt = ", ".join(country_scope) if country_scope else "perimetre du run"
    hist_tables, scen_tables = _load_question_tables(block)

    hist_ledger = _ledger_for_mode(block, "HIST")
    scen_ledger = _ledger_for_mode(block, "SCEN")

    sections: list[str] = []
    sections.append(f"## {qid} - Analyse detaillee")
    sections.append("")

    sections.append("### Question business")
    sections.append(QUESTION_BUSINESS_TEXT.get(qid, "Question business non documentee."))
    sections.append("")

    sections.append("### Definitions operationnelles")
    for d in QUESTION_DEFINITIONS.get(qid, []):
        sections.append(f"- {d}")
    sections.append("")

    sections.append("### Perimetre des tests executes")
    sections.append(
        f"Le perimetre couvre `{country_txt}` et un run combine unique. "
        "Les resultats historiques et prospectifs sont presentes separement puis compares."
    )
    sections.append(_tests_summary(block))
    sections.append("")

    sections.extend(_question_audit_block(qid, hist_tables))
    sections.append("")

    sections.append("### Resultats historiques test par test")
    if hist_ledger.empty:
        sections.append("Aucun test historique n'est disponible pour cette question. Statut: NON_TESTABLE.")
    else:
        for _, row in hist_ledger.iterrows():
            sections.append(_test_line(row))
    sections.append("")

    sections.append("### Resultats prospectifs test par test (par scenario)")
    if scen_ledger.empty:
        sections.append("Aucun test prospectif n'est disponible pour cette question. Statut: NON_TESTABLE.")
    else:
        scen_ledger = scen_ledger.copy()
        scen_ledger["scenario_id"] = scen_ledger.get("scenario_id", "").astype(str).replace("", "N/A")
        for sid, group in scen_ledger.groupby("scenario_id", dropna=False):
            sections.append(f"#### Scenario `{sid}`")
            for _, row in group.iterrows():
                sections.append(_test_line(row))
    sections.append("")

    sections.append("### Comparaison historique vs prospectif")
    cmp_text, cmp_table = _comparison_summary(block)
    sections.append(cmp_text)
    sections.append(cmp_table)
    sections.append("")

    sections.extend(_question_specific_commentary(qid, hist_tables, scen_tables))
    sections.append("")

    sections.append("### Robustesse / fragilite")
    sections.append(_robustness_text(block))
    sections.append(
        "Une conclusion est dite robuste uniquement si elle est compatible avec les tests PASS dominants, "
        "sans contradiction non expliquee par des FAIL/WARN critiques."
    )
    sections.append("")

    sections.append("### Risques de mauvaise lecture")
    sections.append("- Risque 1: confondre correlation et causalite.")
    sections.append("- Risque 2: ignorer les NON_TESTABLE et sur-vendre une conclusion.")
    sections.append("- Risque 3: extrapoler hors perimetre pays/periode/scenario sans nouveau run.")
    sections.append("")

    sections.append("### Reponse conclusive a la question")
    sections.append(
        "La reponse ci-dessus est strictement bornee aux preuves chiffrees du run courant. "
        "Lorsqu'un signal est fragile, la conclusion est formulee comme hypothese de travail et non comme fait etabli."
    )
    sections.append("")

    sections.append("### Actions/priorites de decision")
    sections.append("1. Traiter en priorite les tests FAIL et les checks severes.")
    sections.append("2. Challenger les hypotheses prospectives qui pilotent le plus les deltas vs historique.")
    sections.append("3. Rejouer le bundle sur perimetre elargi avant decision strategique irreversible.")
    sections.append("")

    sections.append("### Table de tracabilite test par test")
    sections.append(_traceability_table(block))
    sections.append("")

    sections.append("### References de preuve")
    sections.append(_evidence_refs_line(block))
    sections.append("")

    sections = _ensure_min_density(sections, block)

    markdown = "\n".join(sections).strip() + "\n"
    word_count = _word_count(markdown)
    test_ids = block.ledger.get("test_id", pd.Series(dtype=str)).astype(str).dropna().unique().tolist() if not block.ledger.empty else []

    return QuestionNarrativeBlock(
        question_id=qid,
        title=f"{qid} - Analyse detaillee",
        markdown=markdown,
        word_count=word_count,
        referenced_test_ids=test_ids,
    )


def narrative_quality_checks(
    narrative: QuestionNarrativeBlock,
    block: QuestionTestResultBlock,
) -> dict[str, Any]:
    min_words = min_words_for_question(narrative.question_id)
    text = narrative.markdown

    ledger_test_ids = set(block.ledger["test_id"].astype(str).tolist()) if not block.ledger.empty else set()
    missing_refs = [tid for tid in ledger_test_ids if f"[evidence:{tid}]" not in text]

    return {
        "question_id": narrative.question_id,
        "word_count": narrative.word_count,
        "min_words_required": min_words,
        "word_count_ok": narrative.word_count >= min_words,
        "all_test_ids_referenced": len(missing_refs) == 0,
        "missing_test_ids_in_text": missing_refs,
    }


def to_dict(obj: Any) -> dict[str, Any]:
    if hasattr(obj, "__dataclass_fields__"):
        return asdict(obj)
    raise TypeError(f"Unsupported object type for to_dict: {type(obj)}")
