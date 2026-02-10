"""LLM analysis module — GPT-5.2 Pro reasoning on Q1-Q5 bundles.

Provides:
- Bundle serialization for LLM consumption
- Prompt construction with full TTE methodology context
- OpenAI API call with disk-based persistence
- Streamlit UI rendering (button, report display, date tracking)
"""

from __future__ import annotations

import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from app.llm_slides_context import get_full_methodology_context
from src.modules.bundle_result import QuestionBundleResult
from src.reporting.interpretation_rules import QUESTION_BUSINESS_TEXT, QUESTION_DEFINITIONS

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MODEL = "gpt-5.2-pro"
REASONING_EFFORT = "high"
MAX_COMPLETION_TOKENS = 16_000
LLM_REPORTS_DIR = Path("outputs/llm_reports")

QUESTION_SUB_QUESTIONS: dict[str, str] = {
    "Q1": """\
1. Pour chaque pays, quand la bascule Phase 1 -> Phase 2 a-t-elle lieu (annee marche vs annee physique) ?
2. Les signaux marche (heures negatives, capture ratio, spread) et physiques (SR, FAR, IR) sont-ils concordants ?
3. Quelle est la confiance dans la bascule (nombre d'indicateurs concordants) ?
4. Les seuils utilises sont-ils robustes (sensibilite a +/-50%) ?
5. Comment les scenarios prospectifs (DEMAND_UP, FLEX_UP, LOW_RIGIDITY) modifient-ils l'annee de bascule ?
6. Quels pays sont les plus avances en phase 2 et pourquoi ?""",
    "Q2": """\
1. Quelle est la pente de cannibalisation par pays et par techno (PV, wind) ?
2. Les pentes sont-elles statistiquement robustes (R2, p-value, nombre de points) ?
3. Quels drivers physiques (SR, FAR, IR, correlation VRE-load) expliquent les pentes ?
4. Comment les pentes evoluent-elles en prospectif par scenario ?
5. Y a-t-il des pays ou la pente est non-significative et pourquoi ?""",
    "Q3": """\
1. Quelle est la tendance des heures negatives (aggravation, stabilisation, amelioration) ?
2. Quels ordres de grandeur de leviers sont necessaires (multiplicateur demande, reduction must-run, flex additionnelle) ?
3. Quels pays montrent des signes de transition vers phase 3 ?
4. La flex additionnelle requise est-elle realiste dans les delais 2030-2040 ?
5. Comment les scenarios modifient-ils les conditions d'inversion ?""",
    "Q4": """\
1. Quel sizing BESS (puissance MW, duree h, energie MWh) atteint l'objectif FAR ou surplus ?
2. Y a-t-il un plateau d'efficacite (au-dela duquel ajouter du stockage ne sert plus) ?
3. Quel est l'effet compare des 3 modes de dispatch (SURPLUS_FIRST, PRICE_ARBITRAGE, PV_COLOCATED) ?
4. Les invariants physiques (SOC, puissance, energie) sont-ils respectes ?
5. Comment les besoins evoluent-ils entre historique et prospectif ?""",
    "Q5": """\
1. Quelles sont les sensibilites dTCA/dCO2 et dTCA/dGas ? Sont-elles stables dans le temps ?
2. Alpha (ecart TTL observe vs TCA theorique) est-il stable ? Que signifie sa variation ?
3. Quel prix CO2 est requis pour atteindre le TTL cible ? Est-ce realiste ?
4. Comment les sensibilites changent-elles selon le scenario gaz/CO2 ?
5. Le choix de technologie marginale (CCGT vs COAL) change-t-il significativement les conclusions ?""",
}

SYSTEM_PROMPT_TEMPLATE = """\
Tu es un consultant senior en strategie energetique specialise dans les marches europeens \
de l'electricite et les capture prices des energies renouvelables (PV, eolien).

Tu produis des rapports d'analyse ultra-rigoureux, precis et structures pour des fonds \
d'infrastructure. Ton style est factuel, argumente par les donnees, et tu ne specules jamais \
sans le signaler explicitement.

IMPORTANT — PERIMETRE STRICT :
Tu analyses UNIQUEMENT la question {qid} qui t'est soumise. \
Ne traite PAS les autres questions (Q1-Q5). Ne reponds qu'aux sous-questions \
listees dans le message utilisateur. Tout le rapport doit porter exclusivement sur {qid}.

Tu as recu en contexte la METHODOLOGIE de l'outil TTE Capture Prices V2 pour la question {qid} : \
les slides de methode originales (definitions, hypotheses, tests empiriques, scenarios, \
limites et livrables attendus) ainsi que les regles de calcul normatives (SPEC_0). \
Tu DOIS t'y referer systematiquement dans ton analyse.

REGLES :
1. Chaque affirmation doit etre appuyee par une donnee precise (pays, annee, valeur).
2. Distingue TOUJOURS observation historique (HIST) et projection prospective (SCEN).
3. Les regimes physiques A/B/C/D sont calcules SANS le prix (anti-circularite) — cf. SPEC_0.
4. Correlation != causalite. Signale toujours cette nuance.
5. Si une donnee manque ou un test est NON_TESTABLE, dis-le explicitement.
6. Detecte et signale tout probleme de logique, de coherence ou de qualite des donnees.
7. Verifie que les resultats sont coherents avec les hypotheses de la methodologie slides.
8. Cite les hypotheses et tests des slides quand pertinent.
9. Signale si un livrable attendu (cf. slides) n'est pas couvert par les donnees disponibles.
10. Ne fais AUCUNE reference aux autres questions (Q1-Q5) sauf si les donnees fournies y font explicitement reference.

FORMAT DU RAPPORT :

=== PARTIE 1 : REPONSE STRATEGIQUE (presentable a un CEO) ===

## Reponse a la question business
Redige une reponse argumentee de type conseil en strategie (500 mots maximum). \
Le ton est direct, structure, actionnable. Chaque affirmation cle est appuyee par \
1-2 chiffres issus des donnees. Cette section doit etre autonome : un decideur doit \
pouvoir la lire seule et en tirer une conclusion operationnelle. Pas de jargon technique \
inutile, pas de formules — uniquement la synthese strategique.

=== PARTIE 2 : DETAILS, ANNEXES ET POINTS D'ATTENTION ===

## Details : reponse a chaque sous-question
   (1 sous-section par sous-question, avec donnees chiffrees)
## Analyse de coherence et problemes detectes
   (incoherences donnees, tests en echec, valeurs aberrantes, logique douteuse, \
ecarts par rapport aux hypotheses methodologiques)
## Tableau de synthese par pays
   (1 ligne par pays avec verdict et KPI cles)
## Recommandations et prochaines etapes
## Limites de cette analyse
   (incluant les limites mentionnees dans les slides de methode)
"""


# ---------------------------------------------------------------------------
# OpenAI client
# ---------------------------------------------------------------------------
def get_openai_client():
    """Resolve API key and return OpenAI client, or None if key missing."""
    try:
        key = st.secrets.get("OPENAI_API_KEY", None)
    except Exception:
        key = None
    if not key:
        key = os.getenv("OPENAI_API_KEY")
    if not key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=key)
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------
def _round_floats(obj: Any, digits: int = 4) -> Any:
    """Recursively round floats in dicts/lists."""
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return round(obj, digits)
    if isinstance(obj, dict):
        return {k: _round_floats(v, digits) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_round_floats(i, digits) for i in obj]
    return obj


def _df_to_records(df: pd.DataFrame, max_rows: int = 200) -> list[dict[str, Any]] | str:
    """Convert DataFrame to list of dicts, truncating if needed."""
    if df is None or df.empty:
        return []
    total = len(df)
    if total > max_rows:
        records = df.head(max_rows).to_dict(orient="records")
        records = _round_floats(records)
        return {"rows": records, "note": f"(tronque a {max_rows} lignes, total: {total})"}
    return _round_floats(df.to_dict(orient="records"))


def serialize_bundle_for_llm(bundle: QuestionBundleResult) -> dict[str, Any]:
    """Convert a QuestionBundleResult into a JSON-serializable dict for LLM consumption."""
    qid = bundle.question_id.upper()

    # Hist tables
    hist_tables = {}
    if bundle.hist_result and bundle.hist_result.tables:
        for name, df in bundle.hist_result.tables.items():
            hist_tables[name] = _df_to_records(df)

    # Hist KPIs
    hist_kpis = _round_floats(bundle.hist_result.kpis) if bundle.hist_result else {}

    # Scenario tables
    scen_tables = {}
    for scen_id, scen_result in (bundle.scen_results or {}).items():
        scen_tables[scen_id] = {}
        for name, df in scen_result.tables.items():
            scen_tables[scen_id][name] = _df_to_records(df)

    # Test ledger
    test_ledger = _df_to_records(bundle.test_ledger)
    ledger_summary = {}
    if not bundle.test_ledger.empty and "status" in bundle.test_ledger.columns:
        counts = bundle.test_ledger["status"].value_counts().to_dict()
        ledger_summary = {str(k): int(v) for k, v in counts.items()}

    # Comparison table
    comparison = _df_to_records(bundle.comparison_table)

    return {
        "question_id": qid,
        "run_id": bundle.run_id,
        "business_question": QUESTION_BUSINESS_TEXT.get(qid, ""),
        "definitions": QUESTION_DEFINITIONS.get(qid, []),
        "selection": bundle.selection,
        "hist_tables": hist_tables,
        "hist_kpis": hist_kpis,
        "scen_tables": scen_tables,
        "test_ledger": test_ledger,
        "test_ledger_summary": ledger_summary,
        "comparison_hist_vs_scen": comparison,
        "checks": bundle.checks,
        "warnings": bundle.warnings,
    }


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------
def _dict_to_markdown_sections(data: dict[str, Any], indent: int = 0) -> str:
    """Simple dict-to-text serialization for the LLM prompt."""
    lines = []
    prefix = "  " * indent
    for key, val in data.items():
        if isinstance(val, list) and val and isinstance(val[0], dict):
            lines.append(f"{prefix}### {key}")
            for i, row in enumerate(val[:200]):
                lines.append(f"{prefix}  {json.dumps(row, ensure_ascii=False, default=str)}")
            if len(val) > 200:
                lines.append(f"{prefix}  ... ({len(val)} lignes au total)")
        elif isinstance(val, dict) and val:
            lines.append(f"{prefix}### {key}")
            lines.append(f"{prefix}{json.dumps(val, ensure_ascii=False, indent=2, default=str)}")
        else:
            lines.append(f"{prefix}**{key}**: {val}")
    return "\n".join(lines)


def build_analysis_prompt(question_id: str, bundle_data: dict[str, Any]) -> tuple[str, list[dict[str, str]]]:
    """Build instructions + input items for the Responses API.

    Returns (instructions, input_items) where:
    - instructions = system-level guidance
    - input_items = list of user messages (methodology context + data)
    """
    qid = question_id.upper()

    # Instructions (replaces system message in Responses API)
    instructions = SYSTEM_PROMPT_TEMPLATE.format(qid=qid)

    # Methodology context
    methodology = get_full_methodology_context(qid)

    # Data + sub-questions
    bq = bundle_data.get("business_question", "")
    defs = "\n".join(f"- {d}" for d in bundle_data.get("definitions", []))
    selection = bundle_data.get("selection", {})
    countries = ", ".join(selection.get("countries", selection.get("country", ["?"])) if isinstance(selection.get("countries"), list) else [str(selection.get("country", "?"))])
    years = str(selection.get("years", "?"))
    scenarios = ", ".join(selection.get("scenario_ids", []))

    # Hist tables
    hist_md = ""
    for tname, tdata in bundle_data.get("hist_tables", {}).items():
        hist_md += f"\n### {tname}\n"
        if isinstance(tdata, dict) and "rows" in tdata:
            hist_md += json.dumps(tdata["rows"][:50], ensure_ascii=False, indent=1, default=str)
            hist_md += f"\n{tdata.get('note', '')}\n"
        elif isinstance(tdata, list):
            hist_md += json.dumps(tdata[:50], ensure_ascii=False, indent=1, default=str)
            if len(tdata) > 50:
                hist_md += f"\n... ({len(tdata)} lignes au total)\n"
        else:
            hist_md += str(tdata)

    # Hist KPIs
    kpis_md = json.dumps(bundle_data.get("hist_kpis", {}), ensure_ascii=False, indent=2, default=str)

    # Scen tables
    scen_md = ""
    for scen_id, tables in bundle_data.get("scen_tables", {}).items():
        scen_md += f"\n#### Scenario: {scen_id}\n"
        for tname, tdata in tables.items():
            scen_md += f"##### {tname}\n"
            if isinstance(tdata, dict) and "rows" in tdata:
                scen_md += json.dumps(tdata["rows"][:50], ensure_ascii=False, indent=1, default=str)
                scen_md += f"\n{tdata.get('note', '')}\n"
            elif isinstance(tdata, list):
                scen_md += json.dumps(tdata[:50], ensure_ascii=False, indent=1, default=str)
                if len(tdata) > 50:
                    scen_md += f"\n... ({len(tdata)} lignes au total)\n"
            else:
                scen_md += str(tdata)

    # Test ledger
    test_data = bundle_data.get("test_ledger", [])
    if isinstance(test_data, dict) and "rows" in test_data:
        test_md = json.dumps(test_data["rows"], ensure_ascii=False, indent=1, default=str)
    elif isinstance(test_data, list):
        test_md = json.dumps(test_data, ensure_ascii=False, indent=1, default=str)
    else:
        test_md = str(test_data)
    summary = bundle_data.get("test_ledger_summary", {})
    summary_line = ", ".join(f"{k}: {v}" for k, v in summary.items())

    # Comparison
    comp_data = bundle_data.get("comparison_hist_vs_scen", [])
    if isinstance(comp_data, list):
        comp_md = json.dumps(comp_data[:100], ensure_ascii=False, indent=1, default=str)
    else:
        comp_md = str(comp_data)

    # Checks & warnings
    checks_md = json.dumps(bundle_data.get("checks", []), ensure_ascii=False, indent=1, default=str)
    warnings = "\n".join(bundle_data.get("warnings", [])) or "(aucun warning)"

    sub_questions = QUESTION_SUB_QUESTIONS.get(qid, "")

    user_content = f"""\
IMPORTANT : Tu analyses UNIQUEMENT la question {qid}. Ne traite aucune autre question.

Voici les resultats complets de l'analyse {qid} pour l'outil TTE Capture Prices V2.

**Question business**: {bq}

**Definitions operationnelles**:
{defs}

**Perimetre**: Pays: {countries} | Annees: {years} | Scenarios: {scenarios}

--- KPIs HISTORIQUES ---
{kpis_md}

--- RESULTATS HISTORIQUES (tables) ---
{hist_md}

--- RESULTATS PAR SCENARIO ---
{scen_md}

--- TEST LEDGER (resultats des tests empiriques) ---
{test_md}
Resume: {summary_line}

--- COMPARAISON HIST vs SCEN ---
{comp_md}

--- CHECKS QUALITE ---
{checks_md}

--- WARNINGS ---
{warnings}

SOUS-QUESTIONS AUXQUELLES TU DOIS REPONDRE (exclusivement pour {qid}) :
{sub_questions}

Produis ton rapport en suivant le format defini. Porte UNIQUEMENT sur {qid}. \
Cite systematiquement les donnees (pays, annee, valeur) pour chaque affirmation.
"""

    input_items = [
        {"role": "user", "content": methodology},
        {"role": "user", "content": user_content},
    ]

    return instructions, input_items


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------
def _report_path(question_id: str, bundle_hash: str) -> Path:
    return LLM_REPORTS_DIR / f"{question_id.upper()}_{bundle_hash}.json"


def load_saved_report(question_id: str, bundle_hash: str) -> dict[str, Any] | None:
    """Load a previously saved LLM report from disk."""
    path = _report_path(question_id, bundle_hash)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _save_report(question_id: str, bundle_hash: str, report: dict[str, Any]) -> None:
    """Save an LLM report to disk."""
    LLM_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = _report_path(question_id, bundle_hash)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------
def run_llm_analysis(
    question_id: str,
    bundle_hash: str,
    bundle_data: dict[str, Any],
) -> dict[str, Any]:
    """Call OpenAI Responses API and return the report dict. Saves to disk on success."""
    client = get_openai_client()
    if client is None:
        return {"error": "Cle API OpenAI non configuree. Ajouter OPENAI_API_KEY dans .env ou Streamlit secrets."}

    instructions, input_items = build_analysis_prompt(question_id, bundle_data)

    try:
        response = client.responses.create(
            model=MODEL,
            instructions=instructions,
            input=input_items,
            max_output_tokens=MAX_COMPLETION_TOKENS,
            reasoning={"effort": REASONING_EFFORT},
        )
    except Exception as exc:
        return {"error": f"Erreur API OpenAI: {exc}"}

    report_md = getattr(response, "output_text", None) or ""
    if not report_md:
        return {"error": "Reponse API vide."}

    usage = getattr(response, "usage", None)
    tokens_in = getattr(usage, "input_tokens", 0) if usage else 0
    tokens_out = getattr(usage, "output_tokens", 0) if usage else 0

    selection = bundle_data.get("selection", {})
    countries = selection.get("countries", [selection.get("country", "?")])

    report = {
        "question_id": question_id.upper(),
        "bundle_hash": bundle_hash,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "model": MODEL,
        "reasoning_effort": REASONING_EFFORT,
        "report_md": report_md,
        "tokens_input": tokens_in,
        "tokens_output": tokens_out,
        "selection_summary": {
            "countries": countries if isinstance(countries, list) else [countries],
            "years": selection.get("years", []),
            "scenario_ids": selection.get("scenario_ids", []),
        },
    }

    _save_report(question_id, bundle_hash, report)
    return report


# ---------------------------------------------------------------------------
# Streamlit UI rendering
# ---------------------------------------------------------------------------
def render_llm_analysis_section(
    question_id: str,
    bundle: QuestionBundleResult,
    bundle_hash: str,
) -> None:
    """Render the LLM analysis section in a Q page."""
    qid = question_id.upper()

    st.markdown("---")
    st.markdown("## Analyse IA (GPT reasoning)")

    # Check for existing report
    saved = load_saved_report(qid, bundle_hash)

    if saved and "report_md" in saved and not saved.get("error"):
        gen_date = saved.get("generated_at", "?")
        try:
            dt = datetime.fromisoformat(gen_date)
            gen_label = dt.strftime("%Y-%m-%d %H:%M UTC")
        except Exception:
            gen_label = str(gen_date)

        st.caption(f"Rapport genere le {gen_label} | Modele: {saved.get('model', MODEL)}")

        with st.expander("Rapport d'analyse IA consultant", expanded=True):
            st.markdown(saved["report_md"])

        tokens_in = saved.get("tokens_input", 0)
        tokens_out = saved.get("tokens_output", 0)
        if tokens_in or tokens_out:
            st.caption(f"Tokens: {tokens_in:,} input + {tokens_out:,} output")

        if st.button("Regenerer l'analyse IA", key=f"llm_regen_{qid}"):
            _run_and_display(qid, bundle, bundle_hash)
    else:
        st.info(
            "Aucun rapport IA disponible pour cette execution. "
            "Cliquez ci-dessous pour generer une analyse complete par GPT-5.2 Pro (reasoning high)."
        )
        if st.button("Generer l'analyse IA consultant", key=f"llm_gen_{qid}", type="primary"):
            _run_and_display(qid, bundle, bundle_hash)


def _run_and_display(question_id: str, bundle: QuestionBundleResult, bundle_hash: str) -> None:
    """Execute LLM analysis and display the result."""
    with st.spinner("Analyse IA en cours (GPT-5.2 Pro reasoning high)... Cela peut prendre 1-2 minutes."):
        bundle_data = serialize_bundle_for_llm(bundle)
        report = run_llm_analysis(question_id, bundle_hash, bundle_data)

    if report.get("error"):
        st.error(report["error"])
        return

    st.success("Rapport IA genere avec succes.")
    gen_date = report.get("generated_at", "?")
    try:
        dt = datetime.fromisoformat(gen_date)
        gen_label = dt.strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        gen_label = str(gen_date)

    st.caption(f"Rapport genere le {gen_label} | Modele: {report.get('model', MODEL)}")

    with st.expander("Rapport d'analyse IA consultant", expanded=True):
        st.markdown(report.get("report_md", ""))

    tokens_in = report.get("tokens_input", 0)
    tokens_out = report.get("tokens_output", 0)
    if tokens_in or tokens_out:
        st.caption(f"Tokens: {tokens_in:,} input + {tokens_out:,} output")
