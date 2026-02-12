"""Question test registry mapped to SPEC/Slides references."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class QuestionTestSpec:
    test_id: str
    question_id: str
    source_ref: str
    mode: str
    scenario_group: str
    title: str
    what_is_tested: str
    metric_rule: str
    severity_if_fail: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


QUESTION_DEFAULT_SCENARIOS: dict[str, list[str]] = {
    "Q1": ["BASE", "DEMAND_UP", "LOW_RIGIDITY"],
    "Q2": ["BASE", "HIGH_CO2", "HIGH_GAS"],
    "Q3": ["BASE", "DEMAND_UP", "LOW_RIGIDITY"],
    "Q4": ["BASE", "HIGH_CO2", "HIGH_GAS"],
    "Q5": ["BASE", "HIGH_CO2", "HIGH_GAS", "HIGH_BOTH"],
}


_REGISTRY: list[QuestionTestSpec] = [
    # Q1
    QuestionTestSpec(
        test_id="Q1-H-01",
        question_id="Q1",
        source_ref="SPEC2-Q1/Slides 2-4",
        mode="HIST",
        scenario_group="HIST_BASE",
        title="Score marche de bascule",
        what_is_tested="La signature marche de phase 2 est calculee et exploitable.",
        metric_rule="stage2_market_score present et non vide",
        severity_if_fail="HIGH",
    ),
    QuestionTestSpec(
        test_id="Q1-H-02",
        question_id="Q1",
        source_ref="SPEC2-Q1/Slides 3-4",
        mode="HIST",
        scenario_group="HIST_BASE",
        title="Stress physique SR/FAR/IR",
        what_is_tested="La bascule physique est fondee sur SR/FAR/IR.",
        metric_rule="sr_energy/far_energy/ir_p10 presentes",
        severity_if_fail="CRITICAL",
    ),
    QuestionTestSpec(
        test_id="Q1-H-03",
        question_id="Q1",
        source_ref="SPEC2-Q1",
        mode="HIST",
        scenario_group="HIST_BASE",
        title="Concordance marche vs physique",
        what_is_tested="La relation entre bascule marche et bascule physique est mesurable.",
        metric_rule="bascule_year_market et bascule_year_physical comparables",
        severity_if_fail="MEDIUM",
    ),
    QuestionTestSpec(
        test_id="Q1-H-04",
        question_id="Q1",
        source_ref="Slides 4-6",
        mode="HIST",
        scenario_group="HIST_BASE",
        title="Robustesse seuils",
        what_is_tested="Le diagnostic reste stable sous variation raisonnable de seuils.",
        metric_rule="delta bascules sous choc de seuil <= 50%",
        severity_if_fail="MEDIUM",
    ),
    QuestionTestSpec(
        test_id="Q1-S-01",
        question_id="Q1",
        source_ref="SPEC2-Q1/Slides 5",
        mode="SCEN",
        scenario_group="DEFAULT",
        title="Bascule projetee par scenario",
        what_is_tested="Chaque scenario fournit un diagnostic de bascule projetee.",
        metric_rule="Q1_country_summary non vide en SCEN",
        severity_if_fail="HIGH",
    ),
    QuestionTestSpec(
        test_id="Q1-S-02",
        question_id="Q1",
        source_ref="SPEC2-Q1/Slides 5",
        mode="SCEN",
        scenario_group="DEFAULT",
        title="Effets DEMAND_UP/LOW_RIGIDITY",
        what_is_tested="Les leviers scenario modifient la bascule vs BASE.",
        metric_rule="delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share)",
        severity_if_fail="MEDIUM",
    ),
    QuestionTestSpec(
        test_id="Q1-S-03",
        question_id="Q1",
        source_ref="SPEC2-Q1",
        mode="SCEN",
        scenario_group="DEFAULT",
        title="Qualite de causalite",
        what_is_tested="Le regime_coherence respecte le seuil d'interpretation.",
        metric_rule="part regime_coherence >= seuil min",
        severity_if_fail="MEDIUM",
    ),
    # Q2
    QuestionTestSpec(
        test_id="Q2-H-01",
        question_id="Q2",
        source_ref="SPEC2-Q2/Slides 10",
        mode="HIST",
        scenario_group="HIST_BASE",
        title="Pentes OLS post-bascule",
        what_is_tested="Les pentes PV/Wind sont estimees en historique.",
        metric_rule="Q2_country_slopes non vide",
        severity_if_fail="HIGH",
    ),
    QuestionTestSpec(
        test_id="Q2-H-02",
        question_id="Q2",
        source_ref="SPEC2-Q2/Slides 10-12",
        mode="HIST",
        scenario_group="HIST_BASE",
        title="Robustesse statistique",
        what_is_tested="R2/p-value/n sont disponibles pour qualifier la robustesse.",
        metric_rule="colonnes r2,p_value,n presentes",
        severity_if_fail="MEDIUM",
    ),
    QuestionTestSpec(
        test_id="Q2-H-03",
        question_id="Q2",
        source_ref="Slides 10-13",
        mode="HIST",
        scenario_group="HIST_BASE",
        title="Drivers physiques",
        what_is_tested="Les drivers SR/FAR/IR/corr VRE-load sont exploites.",
        metric_rule="driver correlations non vides",
        severity_if_fail="MEDIUM",
    ),
    QuestionTestSpec(
        test_id="Q2-S-01",
        question_id="Q2",
        source_ref="SPEC2-Q2/Slides 11",
        mode="SCEN",
        scenario_group="DEFAULT",
        title="Pentes projetees",
        what_is_tested="Les pentes sont reproduites en mode scenario.",
        metric_rule="Q2_country_slopes non vide en SCEN",
        severity_if_fail="HIGH",
    ),
    QuestionTestSpec(
        test_id="Q2-S-02",
        question_id="Q2",
        source_ref="SPEC2-Q2",
        mode="SCEN",
        scenario_group="DEFAULT",
        title="Delta pente vs BASE",
        what_is_tested="Les differences de pente vs BASE sont calculables.",
        metric_rule="delta slope par pays/tech vs BASE",
        severity_if_fail="MEDIUM",
    ),
    # Q3
    QuestionTestSpec(
        test_id="Q3-H-01",
        question_id="Q3",
        source_ref="SPEC2-Q3/Slides 16",
        mode="HIST",
        scenario_group="HIST_BASE",
        title="Tendances glissantes",
        what_is_tested="Les tendances h_negative et capture_ratio sont estimees.",
        metric_rule="Q3_status non vide",
        severity_if_fail="HIGH",
    ),
    QuestionTestSpec(
        test_id="Q3-H-02",
        question_id="Q3",
        source_ref="SPEC2-Q3",
        mode="HIST",
        scenario_group="HIST_BASE",
        title="Statuts sortie phase 2",
        what_is_tested="Les statuts degradation/stabilisation/amelioration sont attribues.",
        metric_rule="status dans ensemble attendu",
        severity_if_fail="MEDIUM",
    ),
    QuestionTestSpec(
        test_id="Q3-S-01",
        question_id="Q3",
        source_ref="SPEC2-Q3/Slides 17",
        mode="SCEN",
        scenario_group="DEFAULT",
        title="Conditions minimales d'inversion",
        what_is_tested="Les besoins demande/must-run/flex sont quantifies en scenario.",
        metric_rule="inversion_k, inversion_r et additional_absorbed presentes",
        severity_if_fail="HIGH",
    ),
    QuestionTestSpec(
        test_id="Q3-S-02",
        question_id="Q3",
        source_ref="Slides 17-19",
        mode="SCEN",
        scenario_group="DEFAULT",
        title="Validation entree phase 3",
        what_is_tested="Le statut prospectif est interpretable pour la transition phase 3.",
        metric_rule="status non vide en SCEN",
        severity_if_fail="MEDIUM",
    ),
    # Q4
    QuestionTestSpec(
        test_id="Q4-H-01",
        question_id="Q4",
        source_ref="SPEC2-Q4/Slides 22",
        mode="HIST",
        scenario_group="HIST_BASE",
        title="Simulation BESS 3 modes",
        what_is_tested="SURPLUS_FIRST, PRICE_ARBITRAGE_SIMPLE et PV_COLOCATED sont executes.",
        metric_rule="3 modes executes avec sorties non vides",
        severity_if_fail="CRITICAL",
    ),
    QuestionTestSpec(
        test_id="Q4-H-02",
        question_id="Q4",
        source_ref="SPEC2-Q4",
        mode="HIST",
        scenario_group="HIST_BASE",
        title="Invariants physiques BESS",
        what_is_tested="Bornes SOC/puissance/energie respectees (mode physique de reference) avec garde-fous structurels sur modes alternatifs.",
        metric_rule="aucun FAIL physique/structurel pertinent",
        severity_if_fail="CRITICAL",
    ),
    QuestionTestSpec(
        test_id="Q4-S-01",
        question_id="Q4",
        source_ref="SPEC2-Q4/Slides 23",
        mode="SCEN",
        scenario_group="DEFAULT",
        title="Comparaison effet batteries par scenario",
        what_is_tested="Impact FAR/surplus/capture compare entre scenarios utiles.",
        metric_rule="Q4 summary non vide pour >=1 scenario",
        severity_if_fail="HIGH",
    ),
    QuestionTestSpec(
        test_id="Q4-S-02",
        question_id="Q4",
        source_ref="Slides 23-25",
        mode="SCEN",
        scenario_group="DEFAULT",
        title="Sensibilite valeur commodites",
        what_is_tested="Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.",
        metric_rule="delta pv_capture ou revenus vs BASE",
        severity_if_fail="MEDIUM",
    ),
    # Q5
    QuestionTestSpec(
        test_id="Q5-H-01",
        question_id="Q5",
        source_ref="SPEC2-Q5/Slides 28",
        mode="HIST",
        scenario_group="HIST_BASE",
        title="Ancre thermique historique",
        what_is_tested="TTL/TCA/alpha/corr sont estimes hors surplus.",
        metric_rule="Q5_summary non vide avec ttl_obs et tca_q95",
        severity_if_fail="HIGH",
    ),
    QuestionTestSpec(
        test_id="Q5-H-02",
        question_id="Q5",
        source_ref="SPEC2-Q5",
        mode="HIST",
        scenario_group="HIST_BASE",
        title="Sensibilites analytiques",
        what_is_tested="dTCA/dCO2 et dTCA/dGas sont positives.",
        metric_rule="dTCA_dCO2 > 0 et dTCA_dGas > 0",
        severity_if_fail="CRITICAL",
    ),
    QuestionTestSpec(
        test_id="Q5-S-01",
        question_id="Q5",
        source_ref="SPEC2-Q5/Slides 29",
        mode="SCEN",
        scenario_group="DEFAULT",
        title="Sensibilites scenarisees",
        what_is_tested="BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.",
        metric_rule="Q5_summary non vide sur scenarios selectionnes",
        severity_if_fail="HIGH",
    ),
    QuestionTestSpec(
        test_id="Q5-S-02",
        question_id="Q5",
        source_ref="SPEC2-Q5/Slides 31",
        mode="SCEN",
        scenario_group="DEFAULT",
        title="CO2 requis pour TTL cible",
        what_is_tested="Le CO2 requis est calcule et interpretable.",
        metric_rule="co2_required_* non NaN",
        severity_if_fail="MEDIUM",
    ),
]


def get_default_scenarios(question_id: str) -> list[str]:
    qid = str(question_id).upper()
    return list(QUESTION_DEFAULT_SCENARIOS.get(qid, ["BASE"]))


def get_question_tests(question_id: str, mode: str | None = None) -> list[QuestionTestSpec]:
    qid = str(question_id).upper()
    out = [t for t in _REGISTRY if t.question_id == qid]
    if mode is not None:
        m = str(mode).upper()
        out = [t for t in out if t.mode == m]
    return out


def all_tests() -> list[QuestionTestSpec]:
    return list(_REGISTRY)
