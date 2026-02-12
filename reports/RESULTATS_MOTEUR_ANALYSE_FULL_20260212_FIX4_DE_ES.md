# Resultats Moteur d'Analyses - DE/ES

- Run ID: `FULL_20260212_FIX4`
- Source combinee: `outputs/combined/FULL_20260212_FIX4`
- Package extrait DE/ES: `reports/chatgpt52_structured_FULL_20260212_FIX4_DE_ES`
- Payload LLM: `reports/llm_paste_payload_chatgpt52_structured_FULL_20260212_FIX4_DE_ES.md`

## Statut global des tests (aucun FAIL)

- Q1: `PASS=7`, `WARN=1`, `NON_TESTABLE=2`, `FAIL=0`
- Q2: `PASS=5`, `WARN=2`, `FAIL=0`
- Q3: `PASS=4`, `WARN=2`, `FAIL=0`
- Q4: `PASS=6`, `FAIL=0`
- Q5: `PASS=8`, `FAIL=0`

## Verification des points critiques

- Q1:
  - Aucune ligne `phase2_market` sans `LOW_PRICE_FLAG=True` et `CAPTURE_DEGRADATION_FLAG=True`.
  - Cas interdit "Phase2 sans LOW_PRICE et sans PHYSICAL" introuvable.
  - `Q1_STAGE1_HEALTHY_NOT_TAGGED` absent des checks.
  - DE 2019 reste coherent: `phase2_market=True`, `LOW_PRICE_FLAG=True`, `CAPTURE_DEGRADATION_FLAG=True`.
- Q3:
  - Pas de cas `additional_absorbed_needed_TWh_year > 0` avec `additional_sink_power_p95_mw <= 0` sur les scenarios exportes.
  - `scenario_id` et hypotheses scenario presentes dans `Q3_status`.
- Q4:
  - Invariant `BESS=0 => after==before` respecte (ecart max 0 sur heures negatives / capture ratios).
  - Monotonicite dominante respectee sur le run historique de reference (`SURPLUS_FIRST`): aucune violation detectee.
- Q5:
  - Champs audit scenario presents (`scenario_id`, prix CO2/gaz/coal, rendements, facteurs d'emission, techno ancre).
  - `required_co2_abs_eur_t` / `required_gas_abs_eur_mwh_th` non systematiquement nuls.
  - Champs `delta_*_vs_scenario` calcules et coherents avec l'ancre formule.

## Rapport v2 regenere

- Detaille: `reports/conclusions_v2_detailed_FULL_20260212_FIX4.md`
- Executif: `reports/conclusions_v2_executive_FULL_20260212_FIX4.md`
- Traceabilite tests: `reports/test_traceability_FULL_20260212_FIX4.csv`

## Note qualite

- `generate_report --strict` reste bloque par precondition documentaire slides (`.docx` absents), pas par des FAIL analytiques du moteur.
