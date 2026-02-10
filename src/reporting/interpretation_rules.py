"""Deterministic interpretation helpers for dense, evidence-backed narratives."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any
import math

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
    "Q1": "Identifier de façon auditable la bascule de Phase 1 vers Phase 2 et distinguer la composante marché de la composante physique.",
    "Q2": "Mesurer la pente de cannibalisation, qualifier sa robustesse statistique et isoler les drivers dominants.",
    "Q3": "Déterminer si le système reste en dégradation, se stabilise ou s'améliore, puis chiffrer les ordres de grandeur d'inversion.",
    "Q4": "Quantifier l'effet des batteries sur la physique du surplus et sur la valeur de l'actif selon différents modes de dispatch.",
    "Q5": "Mesurer l'impact CO2/gaz sur l'ancre thermique et traduire ce signal en implications opérationnelles et de scénarisation.",
}


QUESTION_DEFINITIONS: dict[str, list[str]] = {
    "Q1": [
        "SR mesure l'intensité annuelle du surplus ; plus SR augmente, plus la pression structurelle s'accroît.",
        "FAR mesure la part de surplus effectivement absorbée ; FAR faible signale une insuffisance de flexibilité.",
        "IR mesure la rigidité en creux de demande ; IR élevé accroît le risque de surplus récurrent.",
        "La bascule marché s'appuie sur les symptômes prix/capture ; la bascule physique s'appuie sur SR/FAR/IR.",
    ],
    "Q2": [
        "La pente est ici une relation empirique entre pénétration et capture ratio, pas une loi structurelle universelle.",
        "La robustesse statistique repose sur le triplet n, R², p-value et doit être explicitée avant toute conclusion forte.",
        "Les drivers SR/FAR/IR/corrélation VRE-load servent à expliquer, pas à prouver une causalité stricte.",
    ],
    "Q3": [
        "Le statut système (dégradation/stabilisation/amélioration) agrège plusieurs tendances, il ne dépend pas d'un seul KPI.",
        "Les contre-factuels demande, must-run, flex sont des ordres de grandeur statiques, pas une trajectoire d'investissement optimisée.",
        "La condition d'entrée en Phase 3 doit combiner un signal prix et un signal physique cohérent.",
    ],
    "Q4": [
        "SURPLUS_FIRST mesure l'effet système sur l'absorption du surplus ; PRICE_ARBITRAGE_SIMPLE mesure une logique valeur simplifiée.",
        "PV_COLOCATED permet d'évaluer l'amélioration potentielle du capture price d'un actif couplé batterie.",
        "La frontière puissance/durée révèle les rendements décroissants et les zones de sur-dimensionnement.",
    ],
    "Q5": [
        "TTL est une statistique de queue de prix hors surplus ; TCA est une ancre coût explicative, les deux ne sont pas interchangeables.",
        "Les sensibilités dTCA/dCO2 et dTCA/dGas donnent une lecture incrémentale des chocs de commodités.",
        "Le CO2 requis pour un TTL cible est un ordre de grandeur conditionnel aux hypothèses techno et de pass-through.",
    ],
}


def min_words_for_question(question_id: str) -> int:
    return int(QUESTION_MIN_WORDS.get(str(question_id).upper(), 1000))


def _fmt_value(v: Any) -> str:
    if v is None:
        return "n/a"
    try:
        x = float(v)
        if math.isnan(x):
            return "NaN"
        if abs(x) >= 1000:
            return f"{x:,.2f}".replace(",", " ")
        return f"{x:.4f}"
    except Exception:
        return str(v)


def _status_line(status: str) -> str:
    s = str(status).upper()
    if s == "PASS":
        return "Résultat conforme à la règle attendue."
    if s == "WARN":
        return "Résultat exploitable mais nécessitant une lecture prudente."
    if s == "FAIL":
        return "Résultat non conforme ; la conclusion associée ne peut pas être validée en l'état."
    if s == "NON_TESTABLE":
        return "Test non exécutable avec les données disponibles ; la zone reste explicitement ouverte."
    return "Statut non reconnu ; à qualifier manuellement."


def _mode_label(mode: str) -> str:
    m = str(mode).upper()
    if m == "HIST":
        return "historique"
    if m == "SCEN":
        return "prospectif"
    return m.lower()


def _checks_table(block: QuestionTestResultBlock) -> pd.DataFrame:
    df = block.checks.copy() if isinstance(block.checks, pd.DataFrame) else pd.DataFrame()
    if df.empty:
        return pd.DataFrame(columns=["status", "code", "message", "scope", "scenario_id"])
    for col in ["status", "code", "message", "scope", "scenario_id"]:
        if col not in df.columns:
            df[col] = ""
    return df[["status", "code", "message", "scope", "scenario_id"]].copy()


def _build_tests_narrative(block: QuestionTestResultBlock, mode: str) -> list[str]:
    if block.ledger.empty:
        return [
            f"Aucun test {mode.lower()} n'est disponible pour {block.question_id}. "
            "Dans ce cas, la conclusion doit explicitement rester en statut NON_TESTABLE sur ce périmètre."
        ]
    df = block.ledger.copy()
    df = df[df["mode"].astype(str).str.upper() == mode.upper()]
    if df.empty:
        return [
            f"Aucun test {mode.lower()} n'a été exécuté dans le ledger pour {block.question_id}. "
            "La section est maintenue pour expliciter cette absence de preuve."
        ]

    lines: list[str] = []
    for _, row in df.iterrows():
        test_id = str(row.get("test_id", ""))
        scenario_id = str(row.get("scenario_id", "")).strip()
        scenario_txt = f" scénario `{scenario_id}`" if scenario_id else ""
        lines.append(
            f"Test `{test_id}` ({_mode_label(row.get('mode', ''))}{scenario_txt}) : "
            f"l'objectif est \"{row.get('what_is_tested', '')}\". "
            f"La règle de décision est \"{row.get('metric_rule', '')}\". "
            f"Valeur observée = `{_fmt_value(row.get('value'))}` ; seuil/règle = `{row.get('threshold', '')}` ; "
            f"statut = `{row.get('status', '')}`. "
            f"{_status_line(row.get('status', ''))} "
            f"Interprétation métier associée : {row.get('interpretation', '')}. "
            f"[evidence:{test_id}] [source:{row.get('source_ref', '')}]"
        )
    return lines


def _build_comparison_narrative(block: QuestionTestResultBlock) -> list[str]:
    if block.comparison.empty:
        return [
            "Aucune table de comparaison historique/prospectif n'est disponible. "
            "Le rapport conserve ce constat pour éviter toute extrapolation implicite."
        ]

    lines: list[str] = []
    df = block.comparison.copy()
    for _, row in df.iterrows():
        metric = str(row.get("metric", "metric"))
        country = str(row.get("country", "n/a"))
        scenario = str(row.get("scenario_id", "n/a"))
        hist = _fmt_value(row.get("hist_value"))
        scen = _fmt_value(row.get("scen_value"))
        delta = _fmt_value(row.get("delta"))
        lines.append(
            f"Comparaison `{metric}` pour `{country}` sous scénario `{scenario}` : "
            f"historique = `{hist}`, prospectif = `{scen}`, delta = `{delta}`. "
            "Ce delta est descriptif ; il ne constitue pas, à lui seul, une preuve causale. "
            f"[evidence:comparison_{block.question_id}]"
        )
    return lines


def _build_robustness_narrative(block: QuestionTestResultBlock) -> list[str]:
    if block.ledger.empty:
        return ["Le niveau de robustesse ne peut pas être qualifié faute de tests exécutés."]

    counts = block.ledger["status"].astype(str).value_counts().to_dict()
    pass_n = int(counts.get("PASS", 0))
    warn_n = int(counts.get("WARN", 0))
    fail_n = int(counts.get("FAIL", 0))
    nt_n = int(counts.get("NON_TESTABLE", 0))
    total = max(1, pass_n + warn_n + fail_n + nt_n)
    pass_share = pass_n / total

    lines = [
        f"Bilan de robustesse `{block.question_id}` : PASS={pass_n}, WARN={warn_n}, FAIL={fail_n}, NON_TESTABLE={nt_n}, total={total}.",
        "Lecture de gouvernance : un PASS valide le test au regard de sa règle locale ; un WARN impose une prudence d'interprétation ; "
        "un FAIL invalide l'assertion correspondante tant que la cause n'est pas traitée ; un NON_TESTABLE interdit la conclusion.",
        f"Part de tests PASS = `{pass_share:.2%}`. Cette part sert d'indicateur de confiance global, mais ne remplace pas la lecture test par test."
        f" [evidence:ledger_{block.question_id}]",
    ]

    checks = _checks_table(block)
    if not checks.empty:
        warn_checks = checks[checks["status"].astype(str).str.upper().isin(["WARN", "FAIL"])]
        if warn_checks.empty:
            lines.append("Aucun check technique WARN/FAIL n'est remonté en complément du ledger.")
        else:
            for _, row in warn_checks.iterrows():
                lines.append(
                    f"Check `{row.get('code', '')}` (scope={row.get('scope', '')}, scénario={row.get('scenario_id', '')}) : "
                    f"{row.get('message', '')}. [evidence:check_{row.get('code', '')}]"
                )
    return lines


def build_question_narrative(block: QuestionTestResultBlock, country_scope: list[str] | None = None) -> QuestionNarrativeBlock:
    qid = block.question_id.upper()
    country_txt = ", ".join(country_scope) if country_scope else "périmètre du run"

    sections: list[str] = []
    sections.append(f"## {qid} — Analyse détaillée")
    sections.append("")
    sections.append("### Question business")
    sections.append(QUESTION_BUSINESS_TEXT.get(qid, "Question business non documentée."))
    sections.append("")

    sections.append("### Définitions opérationnelles")
    for d in QUESTION_DEFINITIONS.get(qid, []):
        sections.append(f"- {d}")
    sections.append("")

    sections.append("### Périmètre des tests exécutés")
    sections.append(
        f"L'analyse couvre le périmètre `{country_txt}`. "
        f"Le module `{qid}` est lu en mode historique et en mode prospectif à partir d'un run combiné unique, "
        "sans mélange inter-runs, afin de garantir la cohérence de traçabilité."
    )
    sections.append("")

    sections.append("### Résultats historiques test par test")
    sections.extend(_build_tests_narrative(block, "HIST"))
    sections.append("")

    sections.append("### Résultats prospectifs test par test (par scénario)")
    sections.extend(_build_tests_narrative(block, "SCEN"))
    sections.append("")

    sections.append("### Comparaison historique vs prospectif")
    sections.extend(_build_comparison_narrative(block))
    sections.append("")

    sections.append("### Interprétation argumentée")
    sections.append(
        "La lecture stratégique repose sur une discipline simple: "
        "1) qualifier la validité des tests, "
        "2) expliquer les écarts avec les règles attendues, "
        "3) convertir ces écarts en implications décisionnelles. "
        "Tout résultat présenté ici est strictement borné aux preuves chiffrées du ledger et des tables de comparaison. "
        "Aucune extrapolation hors périmètre n'est retenue."
    )
    sections.append(
        "En pratique, un signal convergent entre historique et prospectif renforce la robustesse opérationnelle de la conclusion. "
        "À l'inverse, un signal divergent n'est pas rejeté: il est traité comme une zone d'incertitude à instrumenter, "
        "avec hypothèses explicites et test de sensibilité additionnel."
    )
    sections.append("")

    sections.append("### Robustesse / fragilité")
    sections.extend(_build_robustness_narrative(block))
    sections.append("")

    sections.append("### Risques de mauvaise lecture")
    sections.append(
        "Premier risque: confondre cohérence empirique et causalité stricte. "
        "Le dispositif est construit pour expliquer, pas pour prouver un mécanisme unique."
    )
    sections.append(
        "Deuxième risque: ignorer les tests NON_TESTABLE et surinterpréter un sous-ensemble favorable de résultats."
    )
    sections.append(
        "Troisième risque: lire des niveaux absolus hors de leur contexte (pays, année, scénario, qualité de données)."
    )
    sections.append("")

    sections.append("### Réponse conclusive à la question")
    sections.append(
        "La réponse de cette section est valide dans le cadre des tests exécutés et des statuts associés. "
        "Une conclusion opérationnelle n'est retenue comme robuste que si elle ne contredit aucun FAIL et explicite tout WARN."
    )
    sections.append("")

    sections.append("### Actions / priorités de décision")
    sections.append(
        "Priorité 1: traiter les écarts marqués FAIL avant toute décision engageante. "
        "Priorité 2: encadrer les WARN par un plan de mitigation analytique (sensibilités, qualité data, scénarios complémentaires). "
        "Priorité 3: convertir les résultats robustes en options de pilotage hiérarchisées (court, moyen, long terme)."
    )
    sections.append("")

    markdown = "\n".join(sections).strip() + "\n"
    word_count = len(markdown.split())
    test_ids = block.ledger.get("test_id", pd.Series(dtype=str)).astype(str).dropna().unique().tolist() if not block.ledger.empty else []

    return QuestionNarrativeBlock(
        question_id=qid,
        title=f"{qid} — Analyse détaillée",
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

    checks = {
        "question_id": narrative.question_id,
        "word_count": narrative.word_count,
        "min_words_required": min_words,
        "word_count_ok": narrative.word_count >= min_words,
        "all_test_ids_referenced": len(missing_refs) == 0,
        "missing_test_ids_in_text": missing_refs,
    }
    return checks


def to_dict(obj: Any) -> dict[str, Any]:
    if hasattr(obj, "__dataclass_fields__"):
        return asdict(obj)
    raise TypeError(f"Unsupported object type for to_dict: {type(obj)}")

