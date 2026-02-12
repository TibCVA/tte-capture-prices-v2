# Resultats Moteur d'Analyses - DE/ES

- Run ID: `FULL_20260211_191955`
- Source: `c:/Users/cval-tlacour/OneDrive - CVA corporate value associate GmbH/Desktop/automation-stack/projects/tte-capture-prices-v2/outputs/combined/FULL_20260211_191955`
- Pays: `DE, ES`
- Genere le: `2026-02-11 20:25:02 UTC`

Ce document compile les resultats question par question et analyse par analyse (GLOBAL, HIST, SCEN), filtres sur DE/ES quand la colonne `country` existe.

## Q1

### GLOBAL

#### Summary (question)
```json
{
  "question_id": "Q1",
  "run_id": "FULL_20260211_191955",
  "selection": {
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "years": [
      2018,
      2019,
      2020,
      2021,
      2022,
      2023,
      2024
    ],
    "scenario_ids": [
      "BASE",
      "DEMAND_UP",
      "FLEX_UP",
      "LOW_RIGIDITY"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ]
  },
  "hist_module_id": "Q1",
  "scenarios": [
    "BASE",
    "DEMAND_UP",
    "FLEX_UP",
    "LOW_RIGIDITY"
  ],
  "n_checks": 238,
  "n_warnings": 0,
  "n_test_rows": 16,
  "n_compare_rows": 28,
  "checks": [
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "BE 2018: annee saine non marquee stage1.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "Q1_CAPTURE_ONLY_SIGNAL",
      "message": "BE 2020: capture-only sans low-price ni stress physique.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "Q1_CAPTURE_ONLY_SIGNAL",
      "message": "DE 2018: capture-only sans low-price ni stress physique.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "Q1_NO_FALSE_PHASE2_WITHOUT_LOW_PRICE",
      "message": "DE 2021: Phase2 detectee sans LOW-PRICE ni PHYSICAL flags.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "IT_NORD 2018: annee saine non marquee stage1.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "IT_NORD 2019: annee saine non marquee stage1.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "IT_NORD 2020: annee saine non marquee stage1.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "NL 2018: annee saine non marquee stage1.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "NL 2019: annee saine non marquee stage1.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "Q1_CAPTURE_ONLY_SIGNAL",
      "message": "NL 2020: capture-only sans low-price ni stress physique.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "Q1_NO_FALSE_PHASE2_WITHOUT_LOW_PRICE",
      "message": "NL 2021: Phase2 detectee sans LOW-PRICE ni PHYSICAL flags.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "BE: coverage max=61.72% (>60%), possible surestimation must-run.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "CZ: coverage max=84.76% (>60%), possible surestimation must-run.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "FR: coverage max=87.11% (>60%), possible surestimation must-run.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "BE-2018: 0.0% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "BE-2018: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=963.0, p50=1143.1, p90=1639.7; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "BE-2019: 26.8% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "BE-2019: 26.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-1098.4, p50=442.5, p90=1330.8; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "BE-2020: 61.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-1170.1, p50=-331.5, p90=935.4; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "BE-2024: 65.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-1890.1, p50=-475.8, p90=1240.2; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "CZ-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=6181.66, p10_load_mw=5946.48.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "CZ-2018: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2018: must_run_share=79.3% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "CZ-2018: 0.0% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "CZ-2018: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=740.2, p50=973.9, p90=1568.4; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_D_NOT_ABOVE_C",
      "message": "CZ-2018: median(price|D) <= median(price|C).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2019: must_run_share=78.2% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "CZ-2019: 36.2% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "CZ-2019: 36.2% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-603.6, p50=411.4, p90=754.4; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2020: must_run_share=76.3% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "CZ-2020: 28.6% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "CZ-2020: 28.6% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-768.9, p50=241.3, p90=1210.1; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2021: must_run_share=76.1% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "CZ-2021: 0.0% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "CZ-2021: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=418.7, p50=1039.2, p90=1706.2; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "CZ-2022: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=5874.35, p10_load_mw=5645.40.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "CZ-2022: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2022: must_run_share=79.6% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2023: must_run_share=79.6% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "CZ-2023: 46.3% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "CZ-2023: 46.3% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-751.1, p50=119.7, p90=1134.0; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_D_NOT_ABOVE_C",
      "message": "CZ-2023: median(price|D) <= median(price|C).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2024: must_run_share=78.6% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "CZ-2024: 20.6% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "CZ-2024: 20.6% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-466.3, p50=418.8, p90=1353.6; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "DE-2018: 33.8% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "DE-2018: 33.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-3039.5, p50=2341.7, p90=8765.7; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "DE-2019: 44.1% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "DE-2019: 44.1% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-4050.2, p50=580.8, p90=5229.3; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "DE-2020: 36.9% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "DE-2020: 36.9% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-3662.8, p50=1184.0, p90=5399.3; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "DE-2021: 41.0% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "DE-2021: 41.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-4056.4, p50=598.4, p90=5182.9; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41354.50, p10_load_mw=39303.40.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2018: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2018: must_run_share=82.4% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "FR-2018: 27.3% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "FR-2018: 27.3% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-7350.0, p50=375.0, p90=2173.0; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2019: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=40635.00, p10_load_mw=39530.00.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2019: must_run_share=80.7% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2020: must_run_share=77.9% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "FR-2020: 52.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-5301.0, p50=-216.0, p90=2362.8; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2021: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41252.00, p10_load_mw=39284.00.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2021: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2021: must_run_share=79.4% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2022: must_run_share=73.5% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2023: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2023: must_run_share=75.9% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2024: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=39406.20, p10_load_mw=37062.60.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2024: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2024: must_run_share=79.2% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2018: must_run_share=0.0% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2019: must_run_share=0.0% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "NL-2019: 0.0% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "NL-2019: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=8995.7, p50=9175.7, p90=9192.9; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2020: must_run_share=0.1% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "NL-2020: 0.0% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "NL-2020: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6769.6, p50=7430.8, p90=8315.3; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2021: must_run_share=0.1% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "NL-2021: 0.0% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "NL-2021: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6325.9, p50=7246.4, p90=8079.5; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2022: must_run_share=0.1% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "NL-2022: 0.0% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "NL-2022: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=5037.0, p50=5902.3, p90=7074.9; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2023: must_run_share=0.2% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "NL-2023: 0.0% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "NL-2023: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6180.9, p50=8241.0, p90=10256.6; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2024: must_run_share=0.2% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "NL-2024: 0.0% des heures negatives en regime A/B (check legacy).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "NL-2024: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6637.0, p50=9062.7, p90=11059.5; causes=price_or_regime_mapping).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "CZ 2030: annee saine non marquee stage1.",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "BE: coverage max=80.22% (>60%), possible surestimation must-run.",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "CZ: coverage max=89.16% (>60%), possible surestimation must-run.",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "CZ 2030: annee saine non marquee stage1.",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "BE: coverage max=80.22% (>60%), possible surestimation must-run.",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "CZ: coverage max=89.16% (>60%), possible surestimation must-run.",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "CZ 2028: annee saine non marquee stage1.",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "CZ 2030: annee saine non marquee stage1.",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "BE: coverage max=80.22% (>60%), possible surestimation must-run.",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "CZ: coverage max=89.16% (>60%), possible surestimation must-run.",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "BE 2030: annee saine non marquee stage1.",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "BE: coverage max=75.59% (>60%), possible surestimation must-run.",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "CZ: coverage max=68.01% (>60%), possible surestimation must-run.",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=68.0% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=67.9% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=67.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=67.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=67.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=67.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=67.3% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=67.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=67.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=67.0% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=66.9% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=62.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=62.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=62.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=62.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=62.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=62.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=62.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=62.3% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=62.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=62.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=62.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "PASS",
      "code": "BUNDLE_LEDGER_STATUS",
      "message": "ledger: FAIL=0, WARN=0",
      "scope": "BUNDLE",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "BUNDLE_INFORMATIVENESS",
      "message": "share_tests_informatifs=100.00% ; share_compare_informatifs=21.43%",
      "scope": "BUNDLE",
      "scenario_id": ""
    },
    {
      "status": "PASS",
      "code": "Q1_S02_NO_SENSITIVITY",
      "message": "Q1-S-02: au moins un scenario non-BASE montre une sensibilite observable.",
      "scope": "BUNDLE",
      "scenario_id": ""
    }
  ],
  "warnings": []
}
```

#### Narratif (question)
Analyse complete Q1: historique + prospectif en un seul run. Statut global=FAIL. Tests PASS=16, WARN=0, FAIL=0, NON_TESTABLE=0. Les resultats sont separes entre historique et scenarios, puis compares dans une table unique.

#### Table `Q1/test_ledger.csv`
Lignes: `16`

```csv
test_id,question_id,source_ref,mode,scenario_group,title,what_is_tested,metric_rule,severity_if_fail,scenario_id,status,value,threshold,interpretation
Q1-S-01,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Bascule projetee par scenario,Chaque scenario fournit un diagnostic de bascule projetee.,Q1_country_summary non vide en SCEN,HIGH,BASE,PASS,7,>0 lignes,La bascule projetee est produite.
Q1-S-02,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY,Les leviers scenario modifient la bascule vs BASE.,delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share),MEDIUM,BASE,PASS,reference_scenario,scenario de reference,BASE est la reference explicite pour le calcul de sensibilite; pas de delta attendu.
Q1-S-03,Q1,SPEC2-Q1,SCEN,DEFAULT,Qualite de causalite,Le regime_coherence respecte le seuil d'interpretation.,part regime_coherence >= seuil min,MEDIUM,BASE,PASS,100.00%,>=50% lignes >=0.55,La coherence scenario est lisible.
Q1-S-01,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Bascule projetee par scenario,Chaque scenario fournit un diagnostic de bascule projetee.,Q1_country_summary non vide en SCEN,HIGH,DEMAND_UP,PASS,7,>0 lignes,La bascule projetee est produite.
Q1-S-02,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY,Les leviers scenario modifient la bascule vs BASE.,delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share),MEDIUM,DEMAND_UP,PASS,finite_share=14.29%; nonzero_share=0.00%; req_defined=100.00%; n_countries=7,nonzero_share >= 20% (scenarios non-BASE),"Delta nul vs BASE, mais required_lever renseigne (interpretabilite preservee)."
Q1-S-03,Q1,SPEC2-Q1,SCEN,DEFAULT,Qualite de causalite,Le regime_coherence respecte le seuil d'interpretation.,part regime_coherence >= seuil min,MEDIUM,DEMAND_UP,PASS,100.00%,>=50% lignes >=0.55,La coherence scenario est lisible.
Q1-S-01,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Bascule projetee par scenario,Chaque scenario fournit un diagnostic de bascule projetee.,Q1_country_summary non vide en SCEN,HIGH,FLEX_UP,PASS,7,>0 lignes,La bascule projetee est produite.
Q1-S-02,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY,Les leviers scenario modifient la bascule vs BASE.,delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share),MEDIUM,FLEX_UP,PASS,finite_share=28.57%; nonzero_share=0.00%; req_defined=100.00%; n_countries=7,nonzero_share >= 20% (scenarios non-BASE),"Delta nul vs BASE, mais required_lever renseigne (interpretabilite preservee)."
Q1-S-03,Q1,SPEC2-Q1,SCEN,DEFAULT,Qualite de causalite,Le regime_coherence respecte le seuil d'interpretation.,part regime_coherence >= seuil min,MEDIUM,FLEX_UP,PASS,100.00%,>=50% lignes >=0.55,La coherence scenario est lisible.
Q1-S-01,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Bascule projetee par scenario,Chaque scenario fournit un diagnostic de bascule projetee.,Q1_country_summary non vide en SCEN,HIGH,LOW_RIGIDITY,PASS,7,>0 lignes,La bascule projetee est produite.
Q1-S-02,Q1,SPEC2-Q1/Slides 5,SCEN,DEFAULT,Effets DEMAND_UP/FLEX_UP/LOW_RIGIDITY,Les leviers scenario modifient la bascule vs BASE.,delta bascule_year_market vs BASE effectivement observable (finite_share/nonzero_share),MEDIUM,LOW_RIGIDITY,PASS,finite_share=14.29%; nonzero_share=0.00%; req_defined=100.00%; n_countries=7,nonzero_share >= 20% (scenarios non-BASE),"Delta nul vs BASE, mais required_lever renseigne (interpretabilite preservee)."
Q1-S-03,Q1,SPEC2-Q1,SCEN,DEFAULT,Qualite de causalite,Le regime_coherence respecte le seuil d'interpretation.,part regime_coherence >= seuil min,MEDIUM,LOW_RIGIDITY,PASS,100.00%,>=50% lignes >=0.55,La coherence scenario est lisible.
Q1-H-01,Q1,SPEC2-Q1/Slides 2-4,HIST,HIST_BASE,Score marche de bascule,La signature marche de phase 2 est calculee et exploitable.,stage2_market_score present et non vide,HIGH,nan,PASS,1.4489795918367347,score present,Le score de bascule marche est exploitable.
Q1-H-02,Q1,SPEC2-Q1/Slides 3-4,HIST,HIST_BASE,Stress physique SR/FAR/IR,La bascule physique est fondee sur SR/FAR/IR.,sr_energy/far_energy/ir_p10 presentes,CRITICAL,nan,PASS,"far_energy,ir_p10,sr_energy",SR/FAR/IR presents,Le stress physique est calculable.
Q1-H-03,Q1,SPEC2-Q1,HIST,HIST_BASE,Concordance marche vs physique,La relation entre bascule marche et bascule physique est mesurable.,bascule_year_market et bascule_year_physical comparables,MEDIUM,nan,PASS,strict=14.29%; concordant_ou_explique=85.71%; n=7; explained=6; reasons=physical_not_reached_but_explained:3;both_not_reached_in_window:1;market_physical_gap_flag:1;strict_equal_year:1;year_gap_unexplained:1,concordant_ou_explique >= 80%,Concordance satisfaisante en comptant les divergences expliquees.
Q1-H-04,Q1,Slides 4-6,HIST,HIST_BASE,Robustesse seuils,Le diagnostic reste stable sous variation raisonnable de seuils.,delta bascules sous choc de seuil <= 50%,MEDIUM,nan,PASS,0.771,confidence moyenne >=0.60,Proxy de robustesse du diagnostic de bascule.
```


#### Table `Q1/comparison_hist_vs_scen.csv`
Lignes totales: `28` | Lignes DE/ES: `8`

##### DE (4 lignes)
```csv
country,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
DE,BASE,bascule_year_market,2019,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,DEMAND_UP,bascule_year_market,2019,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,FLEX_UP,bascule_year_market,2019,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,LOW_RIGIDITY,bascule_year_market,2019,,,,NON_TESTABLE,delta_non_interpretable_nan
```

##### ES (4 lignes)
```csv
country,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
ES,BASE,bascule_year_market,2023,2025,2,,INFORMATIVE,delta_interpretable
ES,DEMAND_UP,bascule_year_market,2023,2025,2,,INFORMATIVE,delta_interpretable
ES,FLEX_UP,bascule_year_market,2023,2025,2,,INFORMATIVE,delta_interpretable
ES,LOW_RIGIDITY,bascule_year_market,2023,2025,2,,INFORMATIVE,delta_interpretable
```


### HIST

#### Summary (hist)
```json
{
  "module_id": "Q1",
  "run_id": "FULL_20260211_191955_HIST",
  "selection": {
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "years": [
      2018,
      2019,
      2020,
      2021,
      2022,
      2023,
      2024
    ],
    "scenario_ids": [
      "BASE",
      "DEMAND_UP",
      "FLEX_UP",
      "LOW_RIGIDITY"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "mode": "HIST",
    "run_id": "FULL_20260211_191955"
  },
  "assumptions_used": [
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "capture_ratio_pv_stage2_max",
      "param_value": 0.8,
      "unit": "ratio",
      "description": "Seuil capture ratio PV vs baseload en declenchement phase2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "capture_ratio_wind_stage2_max",
      "param_value": 0.9,
      "unit": "ratio",
      "description": "Seuil capture ratio Wind vs baseload en declenchement phase2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "days_spread_gt50_stage2_min",
      "param_value": 150.0,
      "unit": "days",
      "description": "Seuil jours spread>50",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "avg_daily_spread_crisis_min",
      "param_value": 50.0,
      "unit": "EUR/MWh",
      "description": "Seuil spread journalier moyen pour tagger une annee de crise",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "h_below_5_stage2_min",
      "param_value": 500.0,
      "unit": "hours",
      "description": "Seuil heures basses",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "h_negative_stage2_min",
      "param_value": 200.0,
      "unit": "hours",
      "description": "Seuil heures negatives stage2",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_capture_ratio_pv_min",
      "param_value": 0.85,
      "unit": "ratio",
      "description": "Stage1 min capture ratio PV vs baseload",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_capture_ratio_wind_min",
      "param_value": 0.9,
      "unit": "ratio",
      "description": "Stage1 min capture ratio Wind vs baseload",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_h_below_5_max",
      "param_value": 500.0,
      "unit": "hours",
      "description": "Stage1 max hours below 5 (doit rester sous seuil stage2)",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_h_negative_max",
      "param_value": 200.0,
      "unit": "hours",
      "description": "Stage1 max negative hours (doit rester sous seuil stage2)",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHYSICS_THRESHOLDS",
      "param_name": "far_stage2_min",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Seuil FAR minimal pour eviter stress physique stage2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHYSICS_THRESHOLDS",
      "param_name": "ir_p10_stage2_min",
      "param_value": 1.5,
      "unit": "ratio",
      "description": "Alias seuil inflexibilite haute stage2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHYSICS_THRESHOLDS",
      "param_name": "sr_hours_stage2_min",
      "param_value": 0.1,
      "unit": "share",
      "description": "Seuil part d'heures de surplus pour stress physique stage2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_sr_hours_max",
      "param_value": 0.05,
      "unit": "share",
      "description": "Stage1 max part d'heures de surplus",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_far_min",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Stage1 min FAR",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_ir_p10_max",
      "param_value": 1.5,
      "unit": "ratio",
      "description": "Stage1 max IR P10",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "QUALITY",
      "param_name": "regime_coherence_min_for_causality",
      "param_value": 0.55,
      "unit": "ratio",
      "description": "Seuil coherence minimale causalite",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "q1_persistence_window_years",
      "param_value": 2.0,
      "unit": "years",
      "description": "Q1: nombre d'annees consecutives requises pour valider une bascule",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "q1_lever_max_uplift",
      "param_value": 1.0,
      "unit": "ratio",
      "description": "Q1: borne max d'uplift pour solveurs required_demand/flex",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    }
  ],
  "kpis": {
    "n_countries": 7,
    "n_bascule_market": 6,
    "n_bascule_physical": 3,
    "n_scope_rows": 49
  },
  "checks": [
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "BE 2018: annee saine non marquee stage1."
    },
    {
      "status": "INFO",
      "code": "Q1_CAPTURE_ONLY_SIGNAL",
      "message": "BE 2020: capture-only sans low-price ni stress physique."
    },
    {
      "status": "INFO",
      "code": "Q1_CAPTURE_ONLY_SIGNAL",
      "message": "DE 2018: capture-only sans low-price ni stress physique."
    },
    {
      "status": "WARN",
      "code": "Q1_NO_FALSE_PHASE2_WITHOUT_LOW_PRICE",
      "message": "DE 2021: Phase2 detectee sans LOW-PRICE ni PHYSICAL flags."
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "IT_NORD 2018: annee saine non marquee stage1."
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "IT_NORD 2019: annee saine non marquee stage1."
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "IT_NORD 2020: annee saine non marquee stage1."
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "NL 2018: annee saine non marquee stage1."
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "NL 2019: annee saine non marquee stage1."
    },
    {
      "status": "INFO",
      "code": "Q1_CAPTURE_ONLY_SIGNAL",
      "message": "NL 2020: capture-only sans low-price ni stress physique."
    },
    {
      "status": "WARN",
      "code": "Q1_NO_FALSE_PHASE2_WITHOUT_LOW_PRICE",
      "message": "NL 2021: Phase2 detectee sans LOW-PRICE ni PHYSICAL flags."
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "BE: coverage max=61.72% (>60%), possible surestimation must-run."
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "CZ: coverage max=84.76% (>60%), possible surestimation must-run."
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "FR: coverage max=87.11% (>60%), possible surestimation must-run."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "BE-2018: 0.0% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "BE-2018: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=963.0, p50=1143.1, p90=1639.7; causes=price_or_regime_mapping)."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "BE-2019: 26.8% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "BE-2019: 26.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-1098.4, p50=442.5, p90=1330.8; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "BE-2020: 61.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-1170.1, p50=-331.5, p90=935.4; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "BE-2024: 65.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-1890.1, p50=-475.8, p90=1240.2; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "CZ-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=6181.66, p10_load_mw=5946.48."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "CZ-2018: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2018: must_run_share=79.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "CZ-2018: 0.0% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "CZ-2018: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=740.2, p50=973.9, p90=1568.4; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_D_NOT_ABOVE_C",
      "message": "CZ-2018: median(price|D) <= median(price|C)."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2019: must_run_share=78.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "CZ-2019: 36.2% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "CZ-2019: 36.2% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-603.6, p50=411.4, p90=754.4; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2020: must_run_share=76.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "CZ-2020: 28.6% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "CZ-2020: 28.6% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-768.9, p50=241.3, p90=1210.1; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2021: must_run_share=76.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "CZ-2021: 0.0% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "CZ-2021: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=418.7, p50=1039.2, p90=1706.2; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "CZ-2022: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=5874.35, p10_load_mw=5645.40."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "CZ-2022: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2022: must_run_share=79.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2023: must_run_share=79.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "CZ-2023: 46.3% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "CZ-2023: 46.3% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-751.1, p50=119.7, p90=1134.0; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_D_NOT_ABOVE_C",
      "message": "CZ-2023: median(price|D) <= median(price|C)."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2024: must_run_share=78.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "CZ-2024: 20.6% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "CZ-2024: 20.6% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-466.3, p50=418.8, p90=1353.6; causes=price_or_regime_mapping)."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "DE-2018: 33.8% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "DE-2018: 33.8% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-3039.5, p50=2341.7, p90=8765.7; causes=price_or_regime_mapping)."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "DE-2019: 44.1% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "DE-2019: 44.1% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-4050.2, p50=580.8, p90=5229.3; causes=price_or_regime_mapping)."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "DE-2020: 36.9% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "DE-2020: 36.9% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-3662.8, p50=1184.0, p90=5399.3; causes=price_or_regime_mapping)."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "DE-2021: 41.0% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "DE-2021: 41.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-4056.4, p50=598.4, p90=5182.9; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41354.50, p10_load_mw=39303.40."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2018: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2018: must_run_share=82.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "FR-2018: 27.3% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "FR-2018: 27.3% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-7350.0, p50=375.0, p90=2173.0; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2019: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=40635.00, p10_load_mw=39530.00."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2019: must_run_share=80.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2020: must_run_share=77.9% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "FR-2020: 52.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=-5301.0, p50=-216.0, p90=2362.8; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2021: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41252.00, p10_load_mw=39284.00."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2021: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2021: must_run_share=79.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2022: must_run_share=73.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2023: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2023: must_run_share=75.9% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2024: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=39406.20, p10_load_mw=37062.60."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2024: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2024: must_run_share=79.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2018: must_run_share=0.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2019: must_run_share=0.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "NL-2019: 0.0% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "NL-2019: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=8995.7, p50=9175.7, p90=9192.9; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2020: must_run_share=0.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "NL-2020: 0.0% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "NL-2020: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6769.6, p50=7430.8, p90=8315.3; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2021: must_run_share=0.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "NL-2021: 0.0% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "NL-2021: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6325.9, p50=7246.4, p90=8079.5; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2022: must_run_share=0.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "NL-2022: 0.0% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "NL-2022: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=5037.0, p50=5902.3, p90=7074.9; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2023: must_run_share=0.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "NL-2023: 0.0% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "NL-2023: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6180.9, p50=8241.0, p90=10256.6; causes=price_or_regime_mapping)."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2024: must_run_share=0.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "INFO",
      "code": "RC_NEG_NOT_IN_AB",
      "message": "NL-2024: 0.0% des heures negatives en regime A/B (check legacy)."
    },
    {
      "status": "WARN",
      "code": "RC_NEG_NOT_IN_AB_OR_LOW_RESIDUAL",
      "message": "NL-2024: 0.0% des heures negatives expliquees par A/B ou low residual (nrl_neg_p10=6637.0, p50=9062.7, p90=11059.5; causes=price_or_regime_mapping)."
    }
  ],
  "warnings": [],
  "mode": "HIST",
  "scenario_id": null,
  "horizon_year": null
}
```

#### Narratif (hist)
Q1 identifie la bascule Phase 1 -> Phase 2 avec gating explicite: >=2 familles LOW_PRICE/VALUE/PHYSICAL, hors annees de crise configurees, et qualite data uniquement. Les diagnostics NEG_NOT_IN_SURPLUS restent visibles via market_physical_gap_flag mais ne bloquent pas la classification.

#### Table HIST `Q1/hist/tables/Q1_before_after_bascule.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,bascule_year_market,pre_window_start_year,pre_window_end_year,post_window_start_year,post_window_end_year,n_pre_years,n_post_years,pre_mean_capture_ratio_pv,post_mean_capture_ratio_pv,delta_post_minus_pre_capture_ratio_pv,pre_mean_capture_ratio_wind,post_mean_capture_ratio_wind,delta_post_minus_pre_capture_ratio_wind,pre_mean_h_negative_obs,post_mean_h_negative_obs,delta_post_minus_pre_h_negative_obs,pre_mean_sr_hours_share,post_mean_sr_hours_share,delta_post_minus_pre_sr_hours_share,pre_mean_far_observed,post_mean_far_observed,delta_post_minus_pre_far_observed,pre_mean_ir_p10,post_mean_ir_p10,delta_post_minus_pre_ir_p10
DE,2019,2016,2018,2019,2021,1,3,0.984256,0.836698,-0.147558,0.858448,0.852612,-0.00583554,133,216,83,0.00890411,0.0134558,0.00455165,1,0.995883,-0.00411679,0.379494,0.266152,-0.113342
```

##### ES (1 lignes)
```csv
country,bascule_year_market,pre_window_start_year,pre_window_end_year,post_window_start_year,post_window_end_year,n_pre_years,n_post_years,pre_mean_capture_ratio_pv,post_mean_capture_ratio_pv,delta_post_minus_pre_capture_ratio_pv,pre_mean_capture_ratio_wind,post_mean_capture_ratio_wind,delta_post_minus_pre_capture_ratio_wind,pre_mean_h_negative_obs,post_mean_h_negative_obs,delta_post_minus_pre_h_negative_obs,pre_mean_sr_hours_share,post_mean_sr_hours_share,delta_post_minus_pre_sr_hours_share,pre_mean_far_observed,post_mean_far_observed,delta_post_minus_pre_far_observed,pre_mean_ir_p10,post_mean_ir_p10,delta_post_minus_pre_ir_p10
ES,2023,2020,2022,2023,2025,3,2,0.928433,0.758926,-0.169506,0.946362,0.879115,-0.0672472,0,123.5,123.5,0.0276491,0.150339,0.12269,1,0.999481,-0.000519462,0.298971,0.295142,-0.00382883
```


#### Table HIST `Q1/hist/tables/Q1_country_summary.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,bascule_year_market,bascule_year_market_country,bascule_year_market_pv,bascule_year_market_wind,bascule_year_physical,bascule_year_market_observed,bascule_year_physical_observed,bascule_status_market,bascule_status_market_pv,bascule_status_market_wind,bascule_status_physical,stage1_bascule_year,stage1_detected,bascule_confidence,families_active_at_bascule_pv,families_active_at_bascule_wind,families_active_at_bascule_country,drivers_at_bascule,low_price_flags_count_at_bascule,physical_flags_count_at_bascule,capture_flags_count_at_bascule,stage2_market_score_at_bascule,score_breakdown_at_bascule,required_demand_uplift_to_avoid_phase2,required_demand_uplift_status,required_flex_uplift_to_avoid_phase2,required_flex_uplift_status,bascule_rationale,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,capture_ratio_pv_at_bascule,capture_ratio_wind_at_bascule,market_physical_gap_at_bascule,neg_price_explained_by_surplus_ratio_at_bascule,h_negative_at_bascule,notes_quality
DE,2019,2019,2021,2019,,2019,,transition_observed,transition_observed,transition_observed,not_reached_in_window,,False,0.8,"LOW_PRICE,VALUE_PV","LOW_PRICE,VALUE_WIND","LOW_PRICE,VALUE_WIND",LOW_PRICE:h_negative_obs>=200.0 (211.0); VALUE:capture_ratio_wind<=0.90 (0.870),1,0,1,2,low=1;value=1;physical=0;crisis=0,0.604553,ok,0.755676,ok,Bascule validee: >=2 familles actives (LOW_PRICE/VALUE/PHYSICAL) sur 2 annees consecutives hors crise.,0.000554157,0.98765,0.284325,58.38,0.597913,0.926638,0.870449,True,0.441,211,ok
```

##### ES (1 lignes)
```csv
country,bascule_year_market,bascule_year_market_country,bascule_year_market_pv,bascule_year_market_wind,bascule_year_physical,bascule_year_market_observed,bascule_year_physical_observed,bascule_status_market,bascule_status_market_pv,bascule_status_market_wind,bascule_status_physical,stage1_bascule_year,stage1_detected,bascule_confidence,families_active_at_bascule_pv,families_active_at_bascule_wind,families_active_at_bascule_country,drivers_at_bascule,low_price_flags_count_at_bascule,physical_flags_count_at_bascule,capture_flags_count_at_bascule,stage2_market_score_at_bascule,score_breakdown_at_bascule,required_demand_uplift_to_avoid_phase2,required_demand_uplift_status,required_flex_uplift_to_avoid_phase2,required_flex_uplift_status,bascule_rationale,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,capture_ratio_pv_at_bascule,capture_ratio_wind_at_bascule,market_physical_gap_at_bascule,neg_price_explained_by_surplus_ratio_at_bascule,h_negative_at_bascule,notes_quality
ES,2023,2023,2023,2023,2023,2023,2023,transition_observed,transition_observed,transition_observed,transition_observed,2018,True,1,"LOW_PRICE,PHYSICAL","LOW_PRICE,PHYSICAL,VALUE_WIND","LOW_PRICE,PHYSICAL,VALUE_WIND",LOW_PRICE:h_below_5_obs>=500.0 (558.0); VALUE:capture_ratio_wind<=0.90 (0.876); PHYSICAL:sr_hours>=0.10 (0.132),1,1,1,3,low=1;value=1;physical=1;crisis=0,0.315125,ok,,beyond_plausible_bounds,Bascule validee: >=2 familles actives (LOW_PRICE/VALUE/PHYSICAL) sur 2 annees consecutives hors crise.,0.011513,0.999559,0.295085,149.328,0.489386,0.838895,0.876094,False,,0,ok
```


#### Table HIST `Q1/hist/tables/Q1_ir_diagnostics.csv`
Lignes totales: `49` | Lignes DE/ES: `14`

##### DE (7 lignes)
```csv
country,year,ir_p10,p10_must_run_mw,p10_load_mw,p50_must_run_mw,p50_load_mw,ir_case_class
DE,2018,0.379494,18673.5,49206.2,24085.1,63728.1,mixed
DE,2019,0.284325,12582,44252.3,18371.4,56884.9,mixed
DE,2020,0.243976,10407.2,42656.7,16086.9,55683.2,mixed
DE,2021,0.270155,12313.6,45579.8,17753,58128.3,mixed
DE,2022,0.310415,13295.2,42830.5,18020.8,55575.8,mixed
DE,2023,0.239046,9778.61,40906.8,14321.2,52824.7,mixed
DE,2024,0.226305,9425.89,41651.3,14138.2,53520,mixed
```

##### ES (7 lignes)
```csv
country,year,ir_p10,p10_must_run_mw,p10_load_mw,p50_must_run_mw,p50_load_mw,ir_case_class
ES,2018,0.294198,6753.9,22957,7745,29172,mixed
ES,2019,0.291358,6596,22638.8,7890,28751,mixed
ES,2020,0.305952,6471,21150.4,8122,26795,mixed
ES,2021,0.285968,6379.9,22309.8,7873,28039,mixed
ES,2022,0.304992,6500,21312,7812,27172,mixed
ES,2023,0.295085,6100,20672,7672,26108,mixed
ES,2024,0.295199,6237.2,21128.8,7532,26556,mixed
```


#### Table HIST `Q1/hist/tables/Q1_residual_diagnostics.csv`
Lignes totales: `49` | Lignes DE/ES: `14`

##### DE (7 lignes)
```csv
country,year,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_median_eur_mwh,residual_negative_p10_mw,residual_negative_p50_mw,residual_negative_p90_mw
DE,2018,9289.37,22544.1,36885.1,,-6.62,-3039.45,2341.71,8765.7
DE,2019,8099.61,20232.8,33446.4,,-7.28,-4050.23,580.79,5229.33
DE,2020,7622.74,19835.7,32423,,-5.945,-3662.8,1184.04,5399.32
DE,2021,9379.87,22625.3,36199.1,,-8.74,-4056.36,598.38,5182.94
DE,2022,3460.24,17086.4,31549.4,,-0.59,-5123.22,-2017.6,2587.5
DE,2023,1477.44,15314.7,29366.9,,-1.9,-9251.72,-4153.59,1129.41
DE,2024,2067.58,16648.5,30191.5,,-2.01,-9454.47,-4275.17,2650.1
```

##### ES (7 lignes)
```csv
country,year,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_median_eur_mwh,residual_negative_p10_mw,residual_negative_p50_mw,residual_negative_p90_mw
ES,2018,7900,14426,20948,,,,,
ES,2019,6986,13083,19455.4,,,,,
ES,2020,4301.4,10807,17307.6,,,,,
ES,2021,3616,10696,17260.8,,,,,
ES,2022,1999.8,9036,15849.4,,,,,
ES,2023,-888,7320,15264,,,,,
ES,2024,-1664,7040,15556,,-0.1,-5209.6,-1372,1914.4
```


#### Table HIST `Q1/hist/tables/Q1_rule_application.csv`
Lignes totales: `49` | Lignes DE/ES: `14`

##### DE (7 lignes)
```csv
country,year,capture_ratio_pv,capture_ratio_wind,stage2_market_score,score_breakdown,crisis_year,quality_flag,quality_ok,stage2_candidate_year,stage1_candidate_year,phase2_candidate_year,low_price_flags_count,physical_flags_count,capture_flags_count,active_flags,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_low_residual_high,flag_sr_high,flag_far_low,flag_ir_high,flag_spread_high,market_physical_gap_flag,neg_price_explained_by_surplus_ratio,low_price_family,value_family,value_family_pv,value_family_wind,physical_family,family_count_pv,family_count_wind,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,physical_candidate_year,flag_capture_only_stage2,is_stage1_criteria,is_phase2_market,is_phase2_physical,phase_market,stress_phys_state
DE,2018,0.984256,0.858448,1,low=0;value=1;physical=0;crisis=0,False,OK,True,False,False,False,0,0,1,"value_family,flag_capture_wind_low",False,False,False,True,False,False,False,False,False,False,True,0.338,False,True,False,True,False,0,1,False,False,False,False,True,False,False,False,uncertain,pas_de_surplus_structurel
DE,2019,0.926638,0.870449,2,low=1;value=1;physical=0;crisis=0,False,OK,True,True,False,True,1,0,1,"low_price_family,value_family,flag_h_negative_stage2,flag_capture_wind_low",True,False,False,True,False,False,False,False,False,False,True,0.441,True,True,False,True,False,1,2,False,True,True,False,False,False,True,False,phase2,pas_de_surplus_structurel
DE,2020,0.804416,0.82851,2,low=1;value=1;physical=0;crisis=0,False,OK,True,True,False,True,2,0,1,"low_price_family,value_family,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_wind_low",True,True,False,True,False,False,False,False,False,False,True,0.369,True,True,False,True,False,1,2,False,True,True,False,False,False,True,False,phase2,pas_de_surplus_structurel
DE,2021,0.779039,0.858878,2,low=1;value=1;physical=0;crisis=0,False,OK,True,True,False,True,0,0,2,"low_price_family,value_family,flag_capture_pv_low,flag_capture_wind_low,flag_spread_high",False,False,True,True,False,False,False,False,False,True,True,0.41,True,True,True,True,False,2,2,True,True,True,False,False,False,True,False,phase2,pas_de_surplus_structurel
DE,2022,0.943954,0.736851,2,low=1;value=1;physical=0;crisis=1,True,OK,True,False,False,False,0,0,1,"low_price_family,value_family,flag_capture_wind_low,flag_spread_high",False,False,False,True,False,False,False,False,False,True,False,,True,True,False,True,False,1,2,False,False,False,False,False,False,False,False,uncertain,pas_de_surplus_structurel
DE,2023,0.758353,0.83955,2,low=1;value=1;physical=0;crisis=0,False,OK,True,True,False,True,2,0,2,"low_price_family,value_family,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_spread_high",True,True,True,True,False,False,False,False,False,True,False,,True,True,True,True,False,2,2,True,True,True,False,False,False,True,False,phase2,pas_de_surplus_structurel
DE,2024,0.588775,0.838449,2,low=1;value=1;physical=0;crisis=0,False,OK,True,True,False,True,2,0,2,"low_price_family,value_family,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_spread_high",True,True,True,True,False,False,False,False,False,True,False,,True,True,True,True,False,2,2,True,True,True,False,False,False,True,False,phase2,pas_de_surplus_structurel
```

##### ES (7 lignes)
```csv
country,year,capture_ratio_pv,capture_ratio_wind,stage2_market_score,score_breakdown,crisis_year,quality_flag,quality_ok,stage2_candidate_year,stage1_candidate_year,phase2_candidate_year,low_price_flags_count,physical_flags_count,capture_flags_count,active_flags,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_low_residual_high,flag_sr_high,flag_far_low,flag_ir_high,flag_spread_high,market_physical_gap_flag,neg_price_explained_by_surplus_ratio,low_price_family,value_family,value_family_pv,value_family_wind,physical_family,family_count_pv,family_count_wind,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,physical_candidate_year,flag_capture_only_stage2,is_stage1_criteria,is_phase2_market,is_phase2_physical,phase_market,stress_phys_state
ES,2018,1.03564,0.9266,0,low=0;value=0;physical=0;crisis=0,False,OK,True,False,True,False,0,0,0,nan,False,False,False,False,False,False,False,False,False,False,False,,False,False,False,False,False,0,0,False,False,False,False,False,True,False,False,phase1,pas_de_surplus_structurel
ES,2019,1.01885,0.957449,0,low=0;value=0;physical=0;crisis=0,False,OK,True,False,True,False,0,0,0,nan,False,False,False,False,False,False,False,False,False,False,False,,False,False,False,False,False,0,0,False,False,False,False,False,True,False,False,phase1,pas_de_surplus_structurel
ES,2020,0.968728,0.953361,0,low=0;value=0;physical=0;crisis=0,False,OK,True,False,True,False,0,0,0,nan,False,False,False,False,False,False,False,False,False,False,False,,False,False,False,False,False,0,0,False,False,False,False,False,True,False,False,phase1,pas_de_surplus_structurel
ES,2021,0.914737,0.927116,0,low=0;value=0;physical=0;crisis=0,False,OK,True,False,True,False,0,0,0,nan,False,False,False,False,False,False,False,False,False,False,False,,False,False,False,False,False,0,0,False,False,False,False,False,True,False,False,phase1,pas_de_surplus_structurel
ES,2022,0.901833,0.95861,1,low=1;value=0;physical=0;crisis=1,True,OK,True,False,False,False,0,0,0,"low_price_family,flag_spread_high",False,False,False,False,False,False,False,False,False,True,False,,True,False,False,False,False,1,1,False,False,False,False,False,False,False,False,uncertain,pas_de_surplus_structurel
ES,2023,0.838895,0.876094,3,low=1;value=1;physical=1;crisis=0,False,OK,True,True,False,True,1,1,1,"low_price_family,value_family,physical_family,flag_h_below_5_stage2,flag_capture_wind_low,flag_sr_hours_high,flag_spread_high",False,True,False,True,True,False,True,False,False,True,False,,True,True,False,True,True,2,3,True,True,True,True,False,False,True,True,phase2,surplus_present_mais_absorbe
ES,2024,0.678957,0.882136,3,low=1;value=1;physical=1;crisis=0,False,OK,True,True,False,True,2,1,2,"low_price_family,value_family,physical_family,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_spread_high",True,True,True,True,True,False,True,False,False,True,False,,True,True,True,True,True,3,3,True,True,True,True,False,False,True,True,phase2,surplus_present_mais_absorbe
```


#### Table HIST `Q1/hist/tables/Q1_rule_definition.csv`
Lignes: `1`

```csv
q1_rule_version,h_negative_stage2_min,h_below_5_stage2_min,capture_ratio_pv_stage2_max,capture_ratio_wind_stage2_max,sr_hours_stage2_min,low_residual_hours_stage2_min,far_stage2_min,ir_p10_stage2_min,days_spread_gt50_stage2_min,avg_daily_spread_crisis_min,stage1_capture_ratio_pv_min,stage1_capture_ratio_wind_min,stage1_sr_hours_max,stage1_far_min,stage1_ir_p10_max,persistence_window_years,crisis_years_explicit,rule_logic
q1_rule_v4_2026_02_11,200,500,0.8,0.9,0.1,0.1,0.95,1.5,150,50,0.85,0.9,0.05,0.95,1.5,2,2022,"stage2_candidate_tech=(>=2 familles actives parmi LOW_PRICE/PHYSICAL/VALUE_TECH) avec persistence sur 2 annees non-crise; bascule_country=min(bascule_pv,bascule_wind). stage1_candidate=(familles toutes inactives) hors crise. NEG_NOT_IN_AB reste informatif; RC principal=AB_OR_LOW_RESIDUAL."
```


#### Table HIST `Q1/hist/tables/Q1_scope_audit.csv`
Lignes totales: `49` | Lignes DE/ES: `14`

##### DE (7 lignes)
```csv
country,year,must_run_scope_coverage,lowload_p20_mw,ir_p10,scope_status,scope_reason,load_net_mode,must_run_mode_hourly
DE,2018,0.401714,52822.2,0.379494,INFO,coverage_coherent,entsoe_total_load_no_pumping_adjust,observed
DE,2019,0.337731,47620.4,0.284325,INFO,coverage_coherent,entsoe_total_load_no_pumping_adjust,observed
DE,2020,0.308007,46146.9,0.243976,INFO,coverage_coherent,entsoe_total_load_no_pumping_adjust,observed
DE,2021,0.344422,48880.6,0.270155,INFO,coverage_coherent,entsoe_total_load_no_pumping_adjust,observed
DE,2022,0.379683,46234.3,0.310415,INFO,coverage_coherent,entsoe_total_load_no_pumping_adjust,observed
DE,2023,0.331958,43869.7,0.239046,INFO,coverage_coherent,entsoe_total_load_no_pumping_adjust,observed
DE,2024,0.347684,44640.7,0.226305,INFO,coverage_coherent,entsoe_total_load_no_pumping_adjust,observed
```

##### ES (7 lignes)
```csv
country,year,must_run_scope_coverage,lowload_p20_mw,ir_p10,scope_status,scope_reason,load_net_mode,must_run_mode_hourly
ES,2018,0.323439,24478.2,0.294198,INFO,coverage_coherent,entsoe_total_load_no_pumping_adjust,observed
ES,2019,0.324256,24006.6,0.291358,INFO,coverage_coherent,entsoe_total_load_no_pumping_adjust,observed
ES,2020,0.340365,22690.4,0.305952,INFO,coverage_coherent,entsoe_total_load_no_pumping_adjust,observed
ES,2021,0.321734,23684.6,0.285968,INFO,coverage_coherent,entsoe_total_load_no_pumping_adjust,observed
ES,2022,0.305217,22744.8,0.304992,INFO,coverage_coherent,entsoe_total_load_no_pumping_adjust,observed
ES,2023,0.299913,21968,0.295085,INFO,coverage_coherent,entsoe_total_load_no_pumping_adjust,observed
ES,2024,0.310927,22372,0.295199,INFO,coverage_coherent,entsoe_total_load_no_pumping_adjust,observed
```


#### Table HIST `Q1/hist/tables/Q1_year_panel.csv`
Lignes totales: `49` | Lignes DE/ES: `14`

##### DE (7 lignes)
```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative_obs,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,h_negative,h_below_5,vre_penetration_share_gen,pv_penetration_share_gen,wind_penetration_share_gen,sr_hours_share,p10_load_mw,p10_must_run_mw,p50_load_mw,p50_must_run_mw,ir_p10_excess,low_residual_hours_share,share_neg_price_hours_in_AB,share_neg_price_hours_in_low_residual,share_neg_price_hours_in_AB_OR_LOW_RESIDUAL,psh_pumping_twh,psh_pumping_coverage_share,psh_pumping_data_status,flex_sink_exports_twh,flex_sink_psh_twh,flex_sink_total_twh,surplus_energy_twh,absorbed_surplus_twh,unabsorbed_surplus_twh,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_sr_high,flag_low_residual_high,flag_far_low,flag_ir_high,flag_spread_high,crisis_year,low_price_family,value_family_pv,value_family_wind,value_family,physical_family,low_price_flags_count,capture_flags_count,physical_flags_count,family_count,family_count_pv,family_count_wind,stage2_points_low_price,stage2_points_capture,stage2_points_physical,stage2_points_vol,stage2_market_score,score_breakdown,quality_ok,neg_price_explained_by_surplus_ratio,market_physical_gap_flag,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,stage2_candidate_year,phase2_candidate_year,flag_capture_only_stage2,is_phase2_market,physical_candidate_year,is_phase2_physical,signal_low_price,signal_value,signal_physical,flag_non_capture_stage2,active_flags,is_stage1_criteria,stage1_candidate_year,phase_market,stress_phys_state
DE,2018,8760,8760,8750,8760,8760,0,0.00114155,0,0.000114155,entsoe_total_load_no_pumping_adjust,observed,"DE_AT_LU,DE_LU",fc4a9d60921bdf9622584b73439596dab0669c58debc359b7973c02885ab6e05,559.953,559.953,42.5352,93.843,19.0655,155.444,575.977,205.217,34.1149,26.9878,7.38487,19.6029,0.277601,44.4728,52.1182,40.2181,43.7726,38.1775,0.984256,0.858448,43.7726,38.1775,0.984256,0.858448,0.605534,0.528135,133,232,38,38,32.1473,99.53,0.153892,0,0.00027483,0.000267184,0.000267184,0.00890411,1,1,0.379494,0.366072,72.2875,72.2875,,none,0,78,7814,868,0.988813,0.696481,0.998858,OK,133,232,0.269878,0.0738487,0.196029,0.00890411,49206.2,18673.5,63728.1,24085.1,-0.620506,,,,,0,,missing,0,0,0,0.153892,,0,False,False,False,True,False,False,False,False,False,False,False,False,False,True,True,False,0,1,0,1,0,1,0,1,0,0,1,low=0;value=1;physical=0;crisis=0,True,0.338,True,False,False,False,False,False,True,False,False,False,False,True,False,0,"value_family,flag_capture_wind_low",False,False,uncertain,pas_de_surplus_structurel
DE,2019,8760,8759,8759,8760,8760,0.000114155,0.000114155,0,0.000114155,entsoe_total_load_no_pumping_adjust,observed,"DE_AT_LU,DE_LU",2ead0a9da339783edacd7f22b12d41c625e65a2a99af6562cf4fed8867550224,502.479,502.479,41.8331,99.9898,24.3805,166.203,515.692,156.967,34.1901,32.2292,8.11203,24.1172,0.330767,37.6697,44.4556,33.8926,34.9062,32.7895,0.926638,0.870449,34.9062,32.7895,0.926638,0.870449,0.597913,0.561657,211,335,31,31,29.9504,117.32,0.285774,0.00352942,0.000568729,0.000554157,0.000554157,0.0156393,0.98765,0.98765,0.284325,0.312349,58.38,58.38,,none,6,131,7760,863,0.999087,0.813246,0.999772,OK,211,335,0.322292,0.0811203,0.241172,0.0156393,44252.3,12582,56884.9,18371.4,-0.715675,,,,,0,,missing,0,0,0,0.285774,,0.00352942,True,False,False,True,False,False,False,False,False,False,False,True,False,True,True,False,1,1,0,2,1,2,1,1,0,0,2,low=1;value=1;physical=0;crisis=0,True,0.441,True,False,True,True,True,True,False,True,False,False,True,True,False,1,"low_price_family,value_family,flag_h_negative_stage2,flag_capture_wind_low",False,False,phase2,pas_de_surplus_structurel
DE,2020,8784,8783,8783,8784,8784,0.000113843,0.000113843,0,0.000113843,entsoe_total_load_no_pumping_adjust,observed,"DE_AT_LU,DE_LU",733a5defd1c10d00b64d81cb5fa9bb20285eaf0bdddb0211a2dd1080991d5985,490.254,490.254,45.9374,103.415,26.8826,176.235,493.926,138.03,21.1321,35.6804,9.30047,26.3799,0.359476,30.4708,37.4649,26.5713,24.5112,25.2454,0.804416,0.82851,24.5112,25.2454,0.804416,0.82851,0.442936,0.456203,298,598,42,42,32.3822,164.58,0.345343,0,0.000704416,0.000699179,0.000699179,0.0159381,1,1,0.243976,0.281516,55.338,55.338,,none,0,140,7779,865,0.998292,0.790311,0.999772,OK,298,598,0.356804,0.0930047,0.263799,0.0159381,42656.7,10407.2,55683.2,16086.9,-0.756024,,,,,0,,missing,0,0,0,0.345343,,0,True,True,False,True,False,False,False,False,False,False,False,True,False,True,True,False,2,1,0,2,1,2,1,1,0,0,2,low=1;value=1;physical=0;crisis=0,True,0.369,True,False,True,True,True,True,False,True,False,False,True,True,False,1,"low_price_family,value_family,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_wind_low",False,False,phase2,pas_de_surplus_structurel
DE,2021,8760,8759,8759,8760,8760,0.000114155,0.000114155,0,0.000114155,entsoe_total_load_no_pumping_adjust,observed,"DE_AT_LU,DE_LU",ebf5faacd8e60ed01f73a092174fa747eb7fb51517519a8ad7c85c1342ac6ff9,509.697,509.697,46.4221,89.8692,24.0099,160.301,504.186,150.066,23.4871,31.794,9.20733,22.5867,0.314503,96.8602,115.52,86.4743,75.4579,83.1911,0.779039,0.858878,75.4579,83.1911,0.779039,0.858878,0.301875,0.332813,139,248,202,202,80.0863,351.21,0.185329,0,0.000363606,0.00036758,0.00036758,0.00878995,1,1,0.270155,0.294388,249.964,249.964,,none,0,77,7814,869,0.973741,0.522158,0.999772,OK,139,248,0.31794,0.0920733,0.225867,0.00878995,45579.8,12313.6,58128.3,17753,-0.729845,,,,,0,,missing,0,0,0,0.185329,,0,False,False,True,True,False,False,False,False,False,True,False,True,True,True,True,False,0,2,0,2,2,2,1,1,0,0,2,low=1;value=1;physical=0;crisis=0,True,0.41,True,True,True,True,True,True,False,True,False,False,True,True,False,1,"low_price_family,value_family,flag_capture_pv_low,flag_capture_wind_low,flag_spread_high",False,False,phase2,pas_de_surplus_structurel
DE,2022,8760,8759,8759,8760,8760,0.000114155,0.000114155,0,0.000114155,entsoe_total_load_no_pumping_adjust,observed,"DE_AT_LU,DE_LU",8779e3327f0c26a267f8af48323efa726e51ef11fa8e9466e79634f0f6afb9d1,487.251,487.251,55.9875,101.267,24.7437,181.999,490.922,152.848,28.8383,37.0728,11.4046,25.6682,0.373522,235.467,267.36,217.82,222.27,173.504,0.943954,0.736851,222.27,173.504,0.943954,0.736851,0.432759,0.337812,69,161,358,358,186.481,687.46,0.904995,0,0.00185735,0.00184346,0.00184346,0.0425799,1,1,0.310415,0.31366,513.611,513.611,,none,0,373,7548,839,0.973399,0.590912,0.999772,OK,69,161,0.370728,0.114046,0.256682,0.0425799,42830.5,13295.2,55575.8,18020.8,-0.689585,,,,,0,,missing,0,0,0,0.904995,,0,False,False,False,True,False,False,False,False,False,True,True,True,False,True,True,False,0,1,0,2,1,2,1,1,0,1,2,low=1;value=1;physical=0;crisis=1,True,,False,False,False,False,False,False,False,False,False,False,True,True,False,1,"low_price_family,value_family,flag_capture_wind_low,flag_spread_high",False,False,uncertain,pas_de_surplus_structurel
DE,2023,8760,8759,8759,8760,8760,0.000114155,0.000114155,0,0.000114155,entsoe_total_load_no_pumping_adjust,observed,"DE_AT_LU,DE_LU",665add90b6dbd1e6064d153dc4fc9879ade96a1336b5746ce7f0ed15e4701e76,463.04,463.04,55.7987,119.466,23.5168,198.782,444.473,128.784,16.7475,44.723,12.5539,32.1691,0.429297,95.1827,106.238,89.0659,72.1821,79.9107,0.758353,0.83955,72.1821,79.9107,0.758353,0.83955,0.429644,0.475646,300,530,340,340,97.5813,594.9,2.55673,0,0.00552162,0.00575227,0.00575227,0.0775114,1,1,0.239046,0.278096,168.004,168.004,,none,0,679,7273,808,0.986756,0.841934,0.999772,OK,300,530,0.44723,0.125539,0.321691,0.0775114,40906.8,9778.61,52824.7,14321.2,-0.760954,,,,,0,,missing,0,0,0,2.55673,,0,True,True,True,True,False,False,False,False,False,True,False,True,True,True,True,False,2,2,0,2,2,2,1,1,0,0,2,low=1;value=1;physical=0;crisis=0,True,,False,True,True,True,True,True,False,True,False,False,True,True,False,1,"low_price_family,value_family,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_spread_high",False,False,phase2,pas_de_surplus_structurel
DE,2024,8784,8783,8783,8784,8784,0.000113843,0.000113843,0,0.000113843,entsoe_total_load_no_pumping_adjust,observed,"DE_AT_LU,DE_LU",b93be6909a4bd71719b1711c2cd72a4765db54dc541bc67c20b93bca4544aa88,470.357,470.357,63.444,112.997,25.6617,202.103,428.492,123.195,11.7972,47.166,14.8063,32.3597,0.429679,78.5155,87.8549,73.3083,46.228,65.8312,0.588775,0.838449,46.228,65.8312,0.588775,0.838449,0.31648,0.450686,457,756,315,315,110.902,828.93,2.94844,0,0.0062685,0.00688095,0.00688095,0.0757058,1,1,0.226305,0.261889,146.069,146.069,,none,0,665,7307,812,0.993966,0.798725,0.999772,OK,457,756,0.47166,0.148063,0.323597,0.0757058,41651.3,9425.89,53520,14138.2,-0.773695,,,,,0,,missing,0,0,0,2.94844,,0,True,True,True,True,False,False,False,False,False,True,False,True,True,True,True,False,2,2,0,2,2,2,1,1,0,0,2,low=1;value=1;physical=0;crisis=0,True,,False,True,True,True,True,True,False,True,False,False,True,True,False,1,"low_price_family,value_family,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_spread_high",False,False,phase2,pas_de_surplus_structurel
```

##### ES (7 lignes)
```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative_obs,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,h_negative,h_below_5,vre_penetration_share_gen,pv_penetration_share_gen,wind_penetration_share_gen,sr_hours_share,p10_load_mw,p10_must_run_mw,p50_load_mw,p50_must_run_mw,ir_p10_excess,low_residual_hours_share,share_neg_price_hours_in_AB,share_neg_price_hours_in_low_residual,share_neg_price_hours_in_AB_OR_LOW_RESIDUAL,psh_pumping_twh,psh_pumping_coverage_share,psh_pumping_data_status,flex_sink_exports_twh,flex_sink_psh_twh,flex_sink_total_twh,surplus_energy_twh,absorbed_surplus_twh,unabsorbed_surplus_twh,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_sr_high,flag_low_residual_high,flag_far_low,flag_ir_high,flag_spread_high,crisis_year,low_price_family,value_family_pv,value_family_wind,value_family,physical_family,low_price_flags_count,capture_flags_count,physical_flags_count,family_count,family_count_pv,family_count_wind,stage2_points_low_price,stage2_points_capture,stage2_points_physical,stage2_points_vol,stage2_market_score,score_breakdown,quality_ok,neg_price_explained_by_surplus_ratio,market_physical_gap_flag,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,stage2_candidate_year,phase2_candidate_year,flag_capture_only_stage2,is_phase2_market,physical_candidate_year,is_phase2_physical,signal_low_price,signal_value,signal_physical,flag_non_capture_stage2,active_flags,is_stage1_criteria,stage1_candidate_year,phase_market,stress_phys_state
ES,2018,8760,8759,8757,8760,8760,0.000114155,0.000342466,0,0.000114155,entsoe_total_load_no_pumping_adjust,observed,ES,bf4812e74b6b6f0f9588f795fbd3ecc39b9eb06714642c121e1f300e2a1b750f,254.516,254.516,12.0237,48.9029,0,60.9266,246.073,66.9327,1.62648,24.7596,4.88625,19.8733,0.239382,57.3001,61.4936,54.9659,59.342,53.0943,1.03564,0.9266,59.342,53.0943,1.03564,0.9266,0.803793,0.719166,0,57,5,5,18.3453,63.3,0.001484,0,5.83067e-06,6.03073e-06,6.03073e-06,0.000342466,1,1,0.294198,0.26289,73.8275,73.8275,,none,0,3,7881,876,0.993835,0.717322,0.999543,OK,0,57,0.247596,0.0488625,0.198733,0.000342466,22957,6753.9,29172,7745,-0.705802,,,,,0,,missing,0,0,0,0.001484,,0,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,low=0;value=0;physical=0;crisis=0,True,,False,False,False,False,False,False,False,False,False,False,False,False,False,0,nan,True,True,phase1,pas_de_surplus_structurel
ES,2019,8760,8759,8759,8760,8760,0.000114155,0.000114155,0,0.000114155,entsoe_total_load_no_pumping_adjust,observed,ES,586a010942020321b15fdadb915addba7ab6e7e6969ee7d40e9b3f149b11363c,249.964,249.964,14.4213,52.3465,0,66.7679,246.324,67.5731,2.53937,27.1057,5.85461,21.2511,0.26711,47.6796,51.2434,45.696,48.5785,45.6508,1.01885,0.957449,48.5785,45.6508,1.01885,0.957449,0.756475,0.710884,0,69,2,2,16.8376,55.23,0.003224,0,1.28978e-05,1.30884e-05,1.30884e-05,0.000570776,1,1,0.291358,0.2703,64.217,64.217,,none,0,5,7879,876,0.995662,0.681918,0.999772,OK,0,69,0.271057,0.0585461,0.212511,0.000570776,22638.8,6596,28751,7890,-0.708642,,,,,0,,missing,0,0,0,0.003224,,0,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,low=0;value=0;physical=0;crisis=0,True,,False,False,False,False,False,False,False,False,False,False,False,False,False,0,nan,True,True,phase1,pas_de_surplus_structurel
ES,2020,8784,8783,8783,8784,8784,0.000113843,0.000113843,0,0.000113843,entsoe_total_load_no_pumping_adjust,observed,ES,aadf283bd90c9fdd7a58c5c8b1b316a5eeddca6e50f69b1cc7effcd15ec82f04,237.905,237.905,20.0309,53.1487,0,73.1796,238.657,69.7405,5.57993,30.6631,8.39319,22.2699,0.307601,33.9581,37.3739,32.0536,32.8961,32.3743,0.968728,0.953361,32.8961,32.3743,0.968728,0.953361,0.632874,0.622835,0,60,0,0,16.8201,49.49,0.143823,0,0.000604541,0.000602635,0.000602635,0.0159381,1,1,0.305952,0.293112,51.979,51.979,,none,0,140,7779,865,0.997609,0.726787,0.999772,OK,0,60,0.306631,0.0839319,0.222699,0.0159381,21150.4,6471,26795,8122,-0.694048,,,,,0,,missing,0,0,0,0.143823,,0,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,low=0;value=0;physical=0;crisis=0,True,,False,False,False,False,False,False,False,False,False,False,False,False,False,0,nan,True,True,phase1,pas_de_surplus_structurel
ES,2021,8760,8759,8759,8760,8760,0.000114155,0.000114155,0,0.000114155,entsoe_total_load_no_pumping_adjust,observed,ES,100694b77bd2a9e8920e497fba215c1e06c075b891317874e8e9cdfd7345d628,243.929,243.929,25.3544,59.0079,0,84.3623,247.292,66.8754,6.87946,34.1145,10.2528,23.8617,0.345848,111.941,119.243,107.876,102.396,103.782,0.914737,0.927116,102.396,103.782,0.914737,0.927116,0.401463,0.406896,0,202,130,130,49.4865,248.98,0.318652,0,0.00130633,0.00128857,0.00128857,0.0231735,1,1,0.285968,0.274128,255.058,255.058,,none,0,203,7701,856,0.958899,0.375181,0.999772,OK,0,202,0.341145,0.102528,0.238617,0.0231735,22309.8,6379.9,28039,7873,-0.714032,,,,,0,,missing,0,0,0,0.318652,,0,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,low=0;value=0;physical=0;crisis=0,True,,False,False,False,False,False,False,False,False,False,False,False,False,False,0,nan,True,True,phase1,pas_de_surplus_structurel
ES,2022,8760,8759,8759,8760,8760,0.000114155,0.000114155,0,0.00285388,entsoe_total_load_no_pumping_adjust,observed,ES,993b2f6bf63272da8ed52aa372e273a53d53ad25106904b3c1c5bb6c86a628d3,236.075,236.075,31.0918,58.8177,0,89.9095,261.421,66.9527,19.3091,34.3926,11.8934,22.4993,0.380852,167.524,170.574,165.837,151.079,160.59,0.901833,0.95861,151.079,160.59,0.901833,0.95861,0.559545,0.594773,0,114,329,329,94.1782,281.45,0.626367,0,0.00265326,0.00239601,0.00239601,0.0438356,1,1,0.304992,0.283576,270.003,270.003,,none,0,384,7538,838,0.950908,0.478698,0.999772,OK,0,114,0.343926,0.118934,0.224993,0.0438356,21312,6500,27172,7812,-0.695008,,,,,0,,missing,0,0,0,0.626367,,0,False,False,False,False,False,False,False,False,False,True,True,True,False,False,False,False,0,0,0,1,1,1,1,0,0,1,1,low=1;value=0;physical=0;crisis=1,True,,False,False,False,False,False,False,False,False,False,False,True,False,False,1,"low_price_family,flag_spread_high",False,False,uncertain,pas_de_surplus_structurel
ES,2023,8760,8759,8759,8760,8760,0.000114155,0.000114155,0,0.000114155,entsoe_total_load_no_pumping_adjust,observed,ES,47d6bf442268d0ea68a7fc82f3687b7f79f3cb6586c171c8bc47168d36d8f00f,229.124,229.124,40.4262,61.0518,0,101.478,244.851,64.7024,13.4489,41.4448,16.5105,24.9343,0.442896,87.1135,87.7177,86.7792,73.0791,76.3196,0.838895,0.876094,73.0791,76.3196,0.838895,0.876094,0.489386,0.511087,0,558,273,273,73.0757,190,2.81898,0.0012438,0.0123033,0.011513,0.011513,0.131507,0.999559,0.999559,0.295085,0.282358,149.328,149.328,,none,3,1149,6847,761,0.936637,0.747881,0.999772,OK,0,558,0.414448,0.165105,0.249343,0.131507,20672,6100,26108,7672,-0.704915,,,,,0,,missing,0,0,0,2.81898,,0.0012438,False,True,False,True,True,True,False,False,False,True,False,True,False,True,True,True,1,1,1,3,2,3,1,1,1,0,3,low=1;value=1;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,True,True,2,"low_price_family,value_family,physical_family,flag_h_below_5_stage2,flag_capture_wind_low,flag_sr_hours_high,flag_spread_high",False,False,phase2,surplus_present_mais_absorbe
ES,2024,8784,8783,8783,8784,8784,0.000113843,0.000113843,0,0.000113843,entsoe_total_load_no_pumping_adjust,observed,ES,660eff69331b9d10038666327666bba9968b079ac4f8085b82a208d451a26b9e,232.025,232.025,47.2525,58.9115,0,106.164,242.173,64.5469,12.3539,43.8381,19.5119,24.3262,0.457554,63.0395,60.2145,64.6146,42.8012,55.6095,0.678957,0.882136,42.8012,55.6095,0.678957,0.882136,0.305723,0.397211,247,1690,271,271,71.0679,173.81,3.56701,0.002132,0.0153734,0.0147292,0.0147292,0.169171,0.999402,0.999402,0.295199,0.278158,140,140,,none,5,1481,6568,730,0.946146,0.693152,0.999772,OK,247,1690,0.438381,0.195119,0.243262,0.169171,21128.8,6237.2,26556,7532,-0.704801,,,,,0,,missing,0,0,0,3.56701,,0.002132,True,True,True,True,True,True,False,False,False,True,False,True,True,True,True,True,2,2,1,3,3,3,1,1,1,0,3,low=1;value=1;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,True,True,2,"low_price_family,value_family,physical_family,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_spread_high",False,False,phase2,surplus_present_mais_absorbe
```


### SCEN

#### Scenario `BASE`

#### Summary (BASE)
```json
{
  "module_id": "Q1",
  "run_id": "FULL_20260211_191955_BASE",
  "selection": {
    "countries": [
      "FR",
      "DE",
      "ES",
      "NL",
      "BE",
      "CZ",
      "IT_NORD"
    ],
    "years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "scenario_ids": [
      "BASE",
      "DEMAND_UP",
      "FLEX_UP",
      "LOW_RIGIDITY"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955",
    "mode": "SCEN",
    "scenario_id": "BASE",
    "horizon_year": 2035
  },
  "assumptions_used": [
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "capture_ratio_pv_stage2_max",
      "param_value": 0.8,
      "unit": "ratio",
      "description": "Seuil capture ratio PV vs baseload en declenchement phase2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "capture_ratio_wind_stage2_max",
      "param_value": 0.9,
      "unit": "ratio",
      "description": "Seuil capture ratio Wind vs baseload en declenchement phase2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "days_spread_gt50_stage2_min",
      "param_value": 150.0,
      "unit": "days",
      "description": "Seuil jours spread>50",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "avg_daily_spread_crisis_min",
      "param_value": 50.0,
      "unit": "EUR/MWh",
      "description": "Seuil spread journalier moyen pour tagger une annee de crise",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "h_below_5_stage2_min",
      "param_value": 500.0,
      "unit": "hours",
      "description": "Seuil heures basses",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "h_negative_stage2_min",
      "param_value": 200.0,
      "unit": "hours",
      "description": "Seuil heures negatives stage2",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_capture_ratio_pv_min",
      "param_value": 0.85,
      "unit": "ratio",
      "description": "Stage1 min capture ratio PV vs baseload",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_capture_ratio_wind_min",
      "param_value": 0.9,
      "unit": "ratio",
      "description": "Stage1 min capture ratio Wind vs baseload",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_h_below_5_max",
      "param_value": 500.0,
      "unit": "hours",
      "description": "Stage1 max hours below 5 (doit rester sous seuil stage2)",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_h_negative_max",
      "param_value": 200.0,
      "unit": "hours",
      "description": "Stage1 max negative hours (doit rester sous seuil stage2)",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHYSICS_THRESHOLDS",
      "param_name": "far_stage2_min",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Seuil FAR minimal pour eviter stress physique stage2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHYSICS_THRESHOLDS",
      "param_name": "ir_p10_stage2_min",
      "param_value": 1.5,
      "unit": "ratio",
      "description": "Alias seuil inflexibilite haute stage2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHYSICS_THRESHOLDS",
      "param_name": "sr_hours_stage2_min",
      "param_value": 0.1,
      "unit": "share",
      "description": "Seuil part d'heures de surplus pour stress physique stage2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_sr_hours_max",
      "param_value": 0.05,
      "unit": "share",
      "description": "Stage1 max part d'heures de surplus",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_far_min",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Stage1 min FAR",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_ir_p10_max",
      "param_value": 1.5,
      "unit": "ratio",
      "description": "Stage1 max IR P10",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "QUALITY",
      "param_name": "regime_coherence_min_for_causality",
      "param_value": 0.55,
      "unit": "ratio",
      "description": "Seuil coherence minimale causalite",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "q1_persistence_window_years",
      "param_value": 2.0,
      "unit": "years",
      "description": "Q1: nombre d'annees consecutives requises pour valider une bascule",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "q1_lever_max_uplift",
      "param_value": 1.0,
      "unit": "ratio",
      "description": "Q1: borne max d'uplift pour solveurs required_demand/flex",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    }
  ],
  "kpis": {
    "n_countries": 7,
    "n_bascule_market": 2,
    "n_bascule_physical": 7,
    "n_scope_rows": 77
  },
  "checks": [
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "CZ 2030: annee saine non marquee stage1."
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "BE: coverage max=80.22% (>60%), possible surestimation must-run."
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "CZ: coverage max=89.16% (>60%), possible surestimation must-run."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%]."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "BASE",
  "horizon_year": 2035
}
```

#### Narratif (BASE)
Q1 identifie la bascule Phase 1 -> Phase 2 avec gating explicite: >=2 familles LOW_PRICE/VALUE/PHYSICAL, hors annees de crise configurees, et qualite data uniquement. Les diagnostics NEG_NOT_IN_SURPLUS restent visibles via market_physical_gap_flag mais ne bloquent pas la classification.

#### Table SCEN BASE `Q1/scen/BASE/tables/Q1_before_after_bascule.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,bascule_year_market,pre_window_start_year,pre_window_end_year,post_window_start_year,post_window_end_year,n_pre_years,n_post_years,pre_mean_capture_ratio_pv,post_mean_capture_ratio_pv,delta_post_minus_pre_capture_ratio_pv,pre_mean_capture_ratio_wind,post_mean_capture_ratio_wind,delta_post_minus_pre_capture_ratio_wind,pre_mean_h_negative_obs,post_mean_h_negative_obs,delta_post_minus_pre_h_negative_obs,pre_mean_sr_hours_share,post_mean_sr_hours_share,delta_post_minus_pre_sr_hours_share,pre_mean_far_observed,post_mean_far_observed,delta_post_minus_pre_far_observed,pre_mean_ir_p10,post_mean_ir_p10,delta_post_minus_pre_ir_p10
DE,,,,,,0,0,,,,,,,,,,,,,,,,,,
```

##### ES (1 lignes)
```csv
country,bascule_year_market,pre_window_start_year,pre_window_end_year,post_window_start_year,post_window_end_year,n_pre_years,n_post_years,pre_mean_capture_ratio_pv,post_mean_capture_ratio_pv,delta_post_minus_pre_capture_ratio_pv,pre_mean_capture_ratio_wind,post_mean_capture_ratio_wind,delta_post_minus_pre_capture_ratio_wind,pre_mean_h_negative_obs,post_mean_h_negative_obs,delta_post_minus_pre_h_negative_obs,pre_mean_sr_hours_share,post_mean_sr_hours_share,delta_post_minus_pre_sr_hours_share,pre_mean_far_observed,post_mean_far_observed,delta_post_minus_pre_far_observed,pre_mean_ir_p10,post_mean_ir_p10,delta_post_minus_pre_ir_p10
ES,2025,2022,2024,2025,2027,0,3,,0.92885,,,0.972303,,,0,,,0,,,1,,,0.0883357,
```


#### Table SCEN BASE `Q1/scen/BASE/tables/Q1_country_summary.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,bascule_year_market,bascule_year_market_country,bascule_year_market_pv,bascule_year_market_wind,bascule_year_physical,bascule_year_market_observed,bascule_year_physical_observed,bascule_status_market,bascule_status_market_pv,bascule_status_market_wind,bascule_status_physical,stage1_bascule_year,stage1_detected,bascule_confidence,families_active_at_bascule_pv,families_active_at_bascule_wind,families_active_at_bascule_country,drivers_at_bascule,low_price_flags_count_at_bascule,physical_flags_count_at_bascule,capture_flags_count_at_bascule,stage2_market_score_at_bascule,score_breakdown_at_bascule,required_demand_uplift_to_avoid_phase2,required_demand_uplift_status,required_flex_uplift_to_avoid_phase2,required_flex_uplift_status,bascule_rationale,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,capture_ratio_pv_at_bascule,capture_ratio_wind_at_bascule,market_physical_gap_at_bascule,neg_price_explained_by_surplus_ratio_at_bascule,h_negative_at_bascule,notes_quality
DE,,,,,2025,,,not_reached_in_window,not_reached_in_window,not_reached_in_window,already_phase2_at_window_start,2025,True,0,PHYSICAL,PHYSICAL,PHYSICAL,nan,0,1,0,1,low=0;value=0;physical=1;crisis=0,0,already_not_phase2,0,already_not_phase2,Pas de bascule persistante sur la fenetre.,0,1,0.0437047,212.658,0.596371,0.964117,0.959978,False,,0,ok
```

##### ES (1 lignes)
```csv
country,bascule_year_market,bascule_year_market_country,bascule_year_market_pv,bascule_year_market_wind,bascule_year_physical,bascule_year_market_observed,bascule_year_physical_observed,bascule_status_market,bascule_status_market_pv,bascule_status_market_wind,bascule_status_physical,stage1_bascule_year,stage1_detected,bascule_confidence,families_active_at_bascule_pv,families_active_at_bascule_wind,families_active_at_bascule_country,drivers_at_bascule,low_price_flags_count_at_bascule,physical_flags_count_at_bascule,capture_flags_count_at_bascule,stage2_market_score_at_bascule,score_breakdown_at_bascule,required_demand_uplift_to_avoid_phase2,required_demand_uplift_status,required_flex_uplift_to_avoid_phase2,required_flex_uplift_status,bascule_rationale,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,capture_ratio_pv_at_bascule,capture_ratio_wind_at_bascule,market_physical_gap_at_bascule,neg_price_explained_by_surplus_ratio_at_bascule,h_negative_at_bascule,notes_quality
ES,2025,2025,2025,2025,2025,2025,,transition_observed,already_phase2_at_window_start,already_phase2_at_window_start,already_phase2_at_window_start,2025,True,1,"LOW_PRICE,PHYSICAL","LOW_PRICE,PHYSICAL","LOW_PRICE,PHYSICAL",nan,0,1,0,2,low=1;value=0;physical=1;crisis=0,0.300049,ok,,beyond_plausible_bounds,Bascule validee: >=2 familles actives (LOW_PRICE/VALUE/PHYSICAL) sur 2 annees consecutives hors crise.,0,1,0.090003,156.602,0.548304,0.928951,0.972073,False,,0,ok
```


#### Table SCEN BASE `Q1/scen/BASE/tables/Q1_ir_diagnostics.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,ir_p10,p10_must_run_mw,p10_load_mw,p50_must_run_mw,p50_load_mw,ir_case_class
DE,2025,0.0520842,2208.4,42400.5,2244.17,54677.6,must_run_floor_effect
DE,2026,0.0511039,2208.4,43213.8,2244.17,55722,must_run_floor_effect
DE,2027,0.0501599,2208.4,44027.2,2244.17,56763.8,must_run_floor_effect
DE,2028,0.0493581,2207.77,44729.6,2243.2,57648.6,must_run_floor_effect
DE,2029,0.0483738,2208.4,45652.8,2244.17,58847.4,must_run_floor_effect
DE,2030,0.0475271,2208.4,46466.1,2244.17,59889.6,must_run_floor_effect
DE,2031,0.0467095,2208.4,47279.4,2244.17,60932.4,must_run_floor_effect
DE,2032,0.0460227,2207.77,47971.3,2243.2,61807,must_run_floor_effect
DE,2033,0.0451559,2208.4,48906,2244.17,63018,must_run_floor_effect
DE,2034,0.0444172,2208.4,49719.4,2244.17,64060.9,must_run_floor_effect
DE,2035,0.0437047,2208.4,50530,2244.17,65104.8,must_run_floor_effect
```

##### ES (11 lignes)
```csv
country,year,ir_p10,p10_must_run_mw,p10_load_mw,p50_must_run_mw,p50_load_mw,ir_case_class
ES,2025,0.090003,1907.18,21190.1,1945.18,26705,must_run_floor_effect
ES,2026,0.0883157,1907.18,21595,1945.18,27219.4,must_run_floor_effect
ES,2027,0.0866883,1907.18,22000.4,1945.18,27732.4,must_run_floor_effect
ES,2028,0.0853506,1907.1,22344.3,1944.67,28171,must_run_floor_effect
ES,2029,0.083598,1907.18,22813.7,1945.18,28755.7,must_run_floor_effect
ES,2030,0.0821305,1907.18,23221.3,1945.18,29267,must_run_floor_effect
ES,2031,0.0807177,1907.18,23627.7,1945.18,29778.3,must_run_floor_effect
ES,2032,0.079568,1907.1,23968.1,1944.67,30210,must_run_floor_effect
ES,2033,0.0780194,1907.18,24444.9,1945.18,30801.7,must_run_floor_effect
ES,2034,0.0767475,1907.18,24850,1945.18,31315.5,must_run_floor_effect
ES,2035,0.0755063,1907.18,25258.5,1945.18,31829.5,must_run_floor_effect
```


#### Table SCEN BASE `Q1/scen/BASE/tables/Q1_residual_diagnostics.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_median_eur_mwh,residual_negative_p10_mw,residual_negative_p50_mw,residual_negative_p90_mw
DE,2025,21243.4,35606.1,50014.8,107.735,,,,
DE,2026,21924.5,36478.7,51133.1,108.754,,,,
DE,2027,22591.6,37357,52256.6,109.763,,,,
DE,2028,23125.4,38061.5,53157.8,110.746,,,,
DE,2029,23957.1,39116.9,54400.3,111.778,,,,
DE,2030,24621.2,40036.6,55480.9,112.784,,,,
DE,2031,25239.5,40847.1,56542.6,113.777,,,,
DE,2032,25684.1,41474.8,57389.8,114.74,,,,
DE,2033,26456.9,42473.4,58655.5,115.763,,,,
DE,2034,27072.1,43285,59699.3,116.764,,,,
DE,2035,27654.7,44092.2,60771,117.746,,,,
```

##### ES (11 lignes)
```csv
country,year,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_median_eur_mwh,residual_negative_p10_mw,residual_negative_p50_mw,residual_negative_p90_mw
ES,2025,10211.8,16025,23312,82.1274,,,,
ES,2026,10504.4,16409.8,23822.3,82.7142,,,,
ES,2027,10800.6,16793.4,24323.5,83.3022,,,,
ES,2028,11031,17131.4,24786.5,83.8658,,,,
ES,2029,11383.4,17568.4,25361.9,84.4891,,,,
ES,2030,11678.8,17951.8,25879.5,85.0821,,,,
ES,2031,11973,18347.9,26389.5,85.6709,,,,
ES,2032,12201.2,18676.5,26849.9,86.2251,,,,
ES,2033,12569,19125.3,27424.1,86.852,,,,
ES,2034,12863.3,19512.9,27935.5,87.4407,,,,
ES,2035,13157.1,19909.9,28464.2,88.0397,,,,
```


#### Table SCEN BASE `Q1/scen/BASE/tables/Q1_rule_application.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,capture_ratio_pv,capture_ratio_wind,stage2_market_score,score_breakdown,crisis_year,quality_flag,quality_ok,stage2_candidate_year,stage1_candidate_year,phase2_candidate_year,low_price_flags_count,physical_flags_count,capture_flags_count,active_flags,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_low_residual_high,flag_sr_high,flag_far_low,flag_ir_high,flag_spread_high,market_physical_gap_flag,neg_price_explained_by_surplus_ratio,low_price_family,value_family,value_family_pv,value_family_wind,physical_family,family_count_pv,family_count_wind,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,physical_candidate_year,flag_capture_only_stage2,is_stage1_criteria,is_phase2_market,is_phase2_physical,phase_market,stress_phys_state
DE,2025,0.96095,0.958046,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2026,0.961672,0.958243,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2027,0.962867,0.958233,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2028,0.963185,0.958323,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2029,0.963632,0.958612,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2030,0.964499,0.958773,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2031,0.964428,0.958967,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2032,0.964541,0.959013,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2033,0.96428,0.959397,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2034,0.964296,0.959586,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2035,0.964117,0.959978,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
```

##### ES (11 lignes)
```csv
country,year,capture_ratio_pv,capture_ratio_wind,stage2_market_score,score_breakdown,crisis_year,quality_flag,quality_ok,stage2_candidate_year,stage1_candidate_year,phase2_candidate_year,low_price_flags_count,physical_flags_count,capture_flags_count,active_flags,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_low_residual_high,flag_sr_high,flag_far_low,flag_ir_high,flag_spread_high,market_physical_gap_flag,neg_price_explained_by_surplus_ratio,low_price_family,value_family,value_family_pv,value_family_wind,physical_family,family_count_pv,family_count_wind,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,physical_candidate_year,flag_capture_only_stage2,is_stage1_criteria,is_phase2_market,is_phase2_physical,phase_market,stress_phys_state
ES,2025,0.928951,0.972073,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2026,0.928882,0.972334,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2027,0.928716,0.972501,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2028,0.928405,0.972346,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2029,0.928573,0.972972,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2030,0.928339,0.973169,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2031,0.928277,0.973305,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2032,0.928092,0.973127,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2033,0.928178,0.973561,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2034,0.928119,0.97379,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2035,0.928055,0.973945,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
```


#### Table SCEN BASE `Q1/scen/BASE/tables/Q1_rule_definition.csv`
Lignes: `1`

```csv
q1_rule_version,h_negative_stage2_min,h_below_5_stage2_min,capture_ratio_pv_stage2_max,capture_ratio_wind_stage2_max,sr_hours_stage2_min,low_residual_hours_stage2_min,far_stage2_min,ir_p10_stage2_min,days_spread_gt50_stage2_min,avg_daily_spread_crisis_min,stage1_capture_ratio_pv_min,stage1_capture_ratio_wind_min,stage1_sr_hours_max,stage1_far_min,stage1_ir_p10_max,persistence_window_years,crisis_years_explicit,rule_logic
q1_rule_v4_2026_02_11,200,500,0.8,0.9,0.1,0.1,0.95,1.5,150,50,0.85,0.9,0.05,0.95,1.5,2,2022,"stage2_candidate_tech=(>=2 familles actives parmi LOW_PRICE/PHYSICAL/VALUE_TECH) avec persistence sur 2 annees non-crise; bascule_country=min(bascule_pv,bascule_wind). stage1_candidate=(familles toutes inactives) hors crise. NEG_NOT_IN_AB reste informatif; RC principal=AB_OR_LOW_RESIDUAL."
```


#### Table SCEN BASE `Q1/scen/BASE/tables/Q1_scope_audit.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,must_run_scope_coverage,lowload_p20_mw,ir_p10,scope_status,scope_reason,load_net_mode,must_run_mode_hourly
DE,2025,0.1522,45497.4,0.0520842,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2026,0.150922,46368.7,0.0511039,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2027,0.149666,47240.4,0.0501599,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2028,0.148212,47984.5,0.0493581,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2029,0.147214,48985,0.0483738,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2030,0.146019,49857.3,0.0475271,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2031,0.144651,50727.2,0.0467095,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2032,0.143076,51460.8,0.0460227,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2033,0.141954,52465.6,0.0451559,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2034,0.140725,53334.4,0.0444172,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2035,0.139544,54203.1,0.0437047,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
```

##### ES (11 lignes)
```csv
country,year,must_run_scope_coverage,lowload_p20_mw,ir_p10,scope_status,scope_reason,load_net_mode,must_run_mode_hourly
ES,2025,0.172188,22488.9,0.090003,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2026,0.171066,22919.6,0.0883157,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2027,0.170024,23353.5,0.0866883,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2028,0.169109,23719.6,0.0853506,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2029,0.167778,24214.5,0.083598,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2030,0.166716,24647.2,0.0821305,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2031,0.165664,25079.8,0.0807177,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2032,0.164805,25441.1,0.079568,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2033,0.163535,25939.9,0.0780194,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2034,0.162492,26369.1,0.0767475,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2035,0.161486,26801.6,0.0755063,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
```


#### Table SCEN BASE `Q1/scen/BASE/tables/Q1_year_panel.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative,h_negative_obs,h_below_5,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,scenario_id,mode,horizon_year,calib_mustrun_scale,calib_vre_scale_pv,calib_vre_scale_wind_on,calib_vre_scale_wind_off,calib_export_cap_eff_gw,calib_export_coincidence_used,calib_flex_realization_factor,calib_price_b_floor,calib_price_b_intercept,calib_price_b_slope_surplus_norm,vre_penetration_share_gen,pv_penetration_share_gen,wind_penetration_share_gen,sr_hours_share,p10_load_mw,p10_must_run_mw,p50_load_mw,p50_must_run_mw,ir_p10_excess,must_run_scope_coverage,core_sanity_issue_count,core_sanity_issues,psh_pumping_twh,psh_pumping_coverage_share,psh_pumping_data_status,flex_sink_exports_twh,flex_sink_psh_twh,flex_sink_total_twh,share_neg_price_hours_in_AB,share_neg_price_hours_in_low_residual,share_neg_price_hours_in_AB_OR_LOW_RESIDUAL,surplus_energy_twh,absorbed_surplus_twh,unabsorbed_surplus_twh,low_residual_hours_share,low_residual_threshold_mw,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_hours_median_eur_mwh,residual_load_p50_on_negative_price_mw,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_sr_high,flag_low_residual_high,flag_far_low,flag_ir_high,flag_spread_high,crisis_year,low_price_family,value_family_pv,value_family_wind,value_family,physical_family,low_price_flags_count,capture_flags_count,physical_flags_count,family_count,family_count_pv,family_count_wind,stage2_points_low_price,stage2_points_capture,stage2_points_physical,stage2_points_vol,stage2_market_score,score_breakdown,quality_ok,neg_price_explained_by_surplus_ratio,market_physical_gap_flag,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,stage2_candidate_year,phase2_candidate_year,flag_capture_only_stage2,is_phase2_market,physical_candidate_year,is_phase2_physical,signal_low_price,signal_value,signal_physical,flag_non_capture_stage2,active_flags,is_stage1_criteria,stage1_candidate_year,phase_market,stress_phys_state
DE,2025,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,c985e9bb69900db8fb870ee7b1b180dbf501d51a1ab556c9ac0c6e6e0cd74161,480.173,478.693,31.6975,93.7283,19.9439,145.37,169.714,19.582,3.45865,85.6559,18.677,66.9788,0.30368,120.277,124.33,118.021,115.58,115.231,0.96095,0.958046,115.58,115.231,0.96095,0.958046,0.591634,0.589846,0,0,0,0,125,125,32.0553,91.7737,0,0,0,0,0,0,1,1,0.0520842,0.0409073,195.357,195.357,,none,0,0,7884,876,1,0.671377,1,OK,BASE,SCEN,2025,9425.89,19.4667,36.463,5.37175,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.856559,0.18677,0.669788,0,42400.5,2208.4,54677.6,2244.17,-0.947916,0.1522,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,21243.4,21243.4,35606.1,50014.8,107.735,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2026,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,2a41e76b67674d7e951b3e646551eb4feaada7a0cd0170b501d736e4aa1ba630,489.319,487.839,31.6975,94.7325,20.3065,146.736,171.08,19.582,3.45865,85.7705,18.5278,67.2427,0.300789,121.411,123.161,120.437,116.758,116.341,0.961672,0.958243,116.758,116.341,0.961672,0.958243,0.592387,0.590274,0,0,0,0,125,125,32.3323,92.5605,0,0,0,0,0,0,1,1,0.0511039,0.0401403,197.097,197.097,,none,0,0,7884,876,1,0.671901,1,OK,BASE,SCEN,2026,9425.89,19.8053,36.8537,5.46942,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.857705,0.185278,0.672427,0,43213.8,2208.4,55722,2244.17,-0.948896,0.150922,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,21924.5,21924.5,36478.7,51133.1,108.754,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2027,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,22ad3803e14b4da8baec5ea305f29dc6c2d29a005dd71770a7eaad2e07b2ad8f,498.465,496.985,31.6975,95.7368,20.6691,148.103,172.447,19.582,3.45865,85.8832,18.381,67.5023,0.298004,122.545,123.576,121.972,117.995,117.427,0.962867,0.958233,117.995,117.427,0.962867,0.958233,0.593414,0.590558,0,0,0,0,124,124,32.3955,93.3473,0,0,0,0,0,0,1,1,0.0501599,0.0394016,198.841,198.841,,none,0,0,7884,876,1,0.672404,1,OK,BASE,SCEN,2027,9425.89,20.1438,37.2444,5.56709,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.858832,0.18381,0.675023,0,44027.2,2208.4,56763.8,2244.17,-0.94984,0.149666,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,22591.6,22591.6,37357,52256.6,109.763,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2028,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,29d611a69fe93991a04966c411378dbe1da60c1527af8a0235f63a31d13aaf5f,507.611,506.128,31.722,97.1985,21.088,150.008,174.417,19.6256,3.4966,86.0055,18.1874,67.818,0.296385,123.636,126.136,122.259,119.084,118.483,0.963185,0.958323,119.084,118.483,0.963185,0.958323,0.594024,0.591025,0,0,0,0,124,124,32.5725,94.0795,0,0,0,0,0,0,1,1,0.0493581,0.0387759,200.471,200.471,,none,0,0,7905,879,1,0.673083,1,OK,BASE,SCEN,2028,9425.89,20.4824,37.635,5.66476,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.860055,0.181874,0.67818,0,44729.6,2207.77,57648.6,2243.2,-0.950642,0.148212,0,,1.48351,1,ok,3.4966,0,0,,,,0,0,0,0.100068,23125.4,23125.4,38061.5,53157.8,110.746,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2029,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,f4db436aa12e48aa38bf19378bcdc969dc55c4161e41a67697adc437bc37df3d,516.757,515.277,31.6975,97.7453,21.3943,150.837,175.181,19.582,3.45865,86.1035,18.0941,68.0094,0.29273,124.814,135.508,118.863,120.275,119.648,0.963632,0.958612,120.275,119.648,0.963632,0.958612,0.594526,0.59143,0,0,0,0,124,124,32.9521,94.9208,0,0,0,0,0,0,1,1,0.0483738,0.0380029,202.304,202.304,,none,0,0,7884,876,1,0.673319,1,OK,BASE,SCEN,2029,9425.89,20.8209,38.0257,5.76243,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.861035,0.180941,0.680094,0,45652.8,2208.4,58847.4,2244.17,-0.951626,0.147214,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,23957.1,23957.1,39116.9,54400.3,111.778,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2030,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,e1336949e7081e0a05dd749ba75f370b9ff2f270daf2ada50721d38e4508bfa0,525.903,524.423,31.6975,98.7495,21.757,152.204,176.548,19.582,3.45865,86.2111,17.954,68.2571,0.290231,125.948,133.95,121.496,121.477,120.756,0.964499,0.958773,121.477,120.756,0.964499,0.958773,0.59537,0.591835,0,0,0,0,123,123,33.0182,95.7076,0,0,0,0,0,0,1,1,0.0475271,0.0373401,204.036,204.036,,none,0,0,7884,876,1,0.673737,1,OK,BASE,SCEN,2030,9425.89,21.1595,38.4164,5.8601,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.862111,0.17954,0.682571,0,46466.1,2208.4,59889.6,2244.17,-0.952473,0.146019,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,24621.2,24621.2,40036.6,55480.9,112.784,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2031,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,bb0bc5d8035052c590034a13c56ec0407913070a2d72bd31ff14b13ddcfc62d9,535.05,533.569,32.1598,99.7538,22.1196,154.033,178.377,19.582,3.45865,86.3525,18.0291,68.3234,0.288684,127.069,131.572,124.562,122.548,121.854,0.964428,0.958967,122.548,121.854,0.964428,0.958967,0.595588,0.592215,0,0,0,0,123,123,33.3027,96.4943,0,0,0,0,0,0,1,1,0.0467095,0.0367,205.76,205.76,,none,0,0,7884,876,1,0.674552,1,OK,BASE,SCEN,2031,9425.89,21.4981,38.8071,5.95777,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.863525,0.180291,0.683234,0,47279.4,2208.4,60932.4,2244.17,-0.953291,0.144651,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,25239.5,25239.5,40847.1,56542.6,113.777,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2032,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,425e73fda24d1faa936c3beefa0c801eeff7750eb9895bf0adc309fd76aa81c4,544.196,542.712,32.6953,101.234,22.5423,156.472,180.881,19.6256,3.4966,86.5055,18.0756,68.43,0.288315,128.14,130.236,126.971,123.596,122.888,0.964541,0.959013,123.596,122.888,0.964541,0.959013,0.595997,0.592582,0,0,0,0,123,123,33.4783,97.2226,0,0,0,0,0,0,1,1,0.0460227,0.036162,207.377,207.377,,none,0,0,7905,879,1,0.675583,1,OK,BASE,SCEN,2032,9425.89,21.8366,39.1978,6.05544,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.865055,0.180756,0.6843,0,47971.3,2207.77,61807,2243.2,-0.953977,0.143076,0,,1.48351,1,ok,3.4966,0,0,,,,0,0,0,0.100068,25684.1,25684.1,41474.8,57389.8,114.74,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2033,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,0ee17a4266c35a4da95f96c84f2e43b9dcf06fa205f25b8b1f40ae89e493fcea,553.342,551.862,33.1728,101.762,22.8448,157.78,182.124,19.582,3.45865,86.6333,18.2144,68.4189,0.285905,129.306,131.983,127.825,124.687,124.056,0.96428,0.959397,124.687,124.056,0.96428,0.959397,0.596006,0.592988,0,0,0,0,123,123,33.8681,98.0678,0,0,0,0,0,0,1,1,0.0451559,0.0354835,209.204,209.204,,none,0,0,7884,876,1,0.676187,1,OK,BASE,SCEN,2033,9425.89,22.1752,39.5884,6.15311,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.866333,0.182144,0.684189,0,48906,2208.4,63018,2244.17,-0.954844,0.141954,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,26456.9,26456.9,42473.4,58655.5,115.763,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2034,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,c530d8c69ceaae405f30a65bac964abea4c7fc96089d3fc29cdb98610a69e02b,562.488,561.008,33.6792,102.766,23.2075,159.653,183.997,19.582,3.45865,86.7694,18.3042,68.4652,0.284583,130.425,138.109,126.173,125.768,125.153,0.964296,0.959586,125.768,125.153,0.964296,0.959586,0.596265,0.593353,0,0,0,0,123,123,34.1533,98.8545,0,0,0,0,0,0,1,1,0.0444172,0.0349051,210.926,210.926,,none,0,0,7884,876,1,0.676974,1,OK,BASE,SCEN,2034,9425.89,22.5137,39.9791,6.25078,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.867694,0.183042,0.684652,0,49719.4,2208.4,64060.9,2244.17,-0.955583,0.140725,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,27072.1,27072.1,43285,59699.3,116.764,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2035,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,a77e943a1e04f7928661559bb66c39abb18841344d0d2cb591d34e007f5d10c6,571.634,570.154,34.1857,103.771,23.5701,161.527,185.87,19.582,3.45865,86.9027,18.3922,68.5105,0.283303,131.543,143.02,125.156,126.823,126.279,0.964117,0.959978,126.823,126.279,0.964117,0.959978,0.596371,0.593811,0,0,0,0,122,122,34.2128,99.6412,0,0,0,0,0,0,1,1,0.0437047,0.0343451,212.658,212.658,,none,0,0,7884,876,1,0.67774,1,OK,BASE,SCEN,2035,9425.89,22.8523,40.3698,6.34845,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.869027,0.183922,0.685105,0,50530,2208.4,65104.8,2244.17,-0.956295,0.139544,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,27654.7,27654.7,44092.2,60771,117.746,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
```

##### ES (11 lignes)
```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative,h_negative_obs,h_below_5,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,scenario_id,mode,horizon_year,calib_mustrun_scale,calib_vre_scale_pv,calib_vre_scale_wind_on,calib_vre_scale_wind_off,calib_export_cap_eff_gw,calib_export_coincidence_used,calib_flex_realization_factor,calib_price_b_floor,calib_price_b_intercept,calib_price_b_slope_surplus_norm,vre_penetration_share_gen,pv_penetration_share_gen,wind_penetration_share_gen,sr_hours_share,p10_load_mw,p10_must_run_mw,p50_load_mw,p50_must_run_mw,ir_p10_excess,must_run_scope_coverage,core_sanity_issue_count,core_sanity_issues,psh_pumping_twh,psh_pumping_coverage_share,psh_pumping_data_status,flex_sink_exports_twh,flex_sink_psh_twh,flex_sink_total_twh,share_neg_price_hours_in_AB,share_neg_price_hours_in_low_residual,share_neg_price_hours_in_AB_OR_LOW_RESIDUAL,surplus_energy_twh,absorbed_surplus_twh,unabsorbed_surplus_twh,low_residual_hours_share,low_residual_threshold_mw,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_hours_median_eur_mwh,residual_load_p50_on_negative_price_mw,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_sr_high,flag_low_residual_high,flag_far_low,flag_ir_high,flag_spread_high,crisis_year,low_price_family,value_family_pv,value_family_wind,value_family,physical_family,low_price_flags_count,capture_flags_count,physical_flags_count,family_count,family_count_pv,family_count_wind,stage2_points_low_price,stage2_points_capture,stage2_points_physical,stage2_points_vol,stage2_market_score,score_breakdown,quality_ok,neg_price_explained_by_surplus_ratio,market_physical_gap_flag,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,stage2_candidate_year,phase2_candidate_year,flag_capture_only_stage2,is_phase2_market,physical_candidate_year,is_phase2_physical,signal_low_price,signal_value,signal_physical,flag_non_capture_stage2,active_flags,is_stage1_criteria,stage1_candidate_year,phase_market,stress_phys_state
ES,2025,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,3c170c03139207b7a1e67fa0256c315f7dae7a1e3949b9310dc39caefeebc1b9,234.28,232.927,28.6131,43.9453,0,72.5584,115.734,16.8792,6.66768,62.694,24.7231,37.9709,0.311507,92.4323,89.5715,94.0244,85.8652,89.851,0.928951,0.972073,85.8652,89.851,0.928951,0.972073,0.548304,0.573755,0,0,0,0,191,191,40.7608,80.4881,0,0,0,0,0,0,1,1,0.090003,0.0724653,156.602,156.602,,none,0,0,7884,876,1,0.709362,1,OK,BASE,SCEN,2025,6237.2,12.5165,13.3741,1.9703,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.62694,0.247231,0.379709,0,21190.1,1907.18,26705,1945.18,-0.909997,0.172188,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,10211.8,10211.8,16025,23312,82.1274,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2026,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,f3339004bdd1853715aaa143861459744f474b9961bd74d5459dd11b35726e86,238.743,237.39,29.1108,44.4161,0,73.5269,116.703,16.8792,6.66768,63.0036,24.9444,38.0592,0.309731,93.1246,89.905,94.9164,86.5018,90.5483,0.928882,0.972334,86.5018,90.5483,0.928882,0.972334,0.548392,0.574046,0,0,0,0,191,191,41.0749,81.1182,0,0,0,0,0,0,1,1,0.0883157,0.0711031,157.737,157.737,,none,0,0,7884,876,1,0.71011,1,OK,BASE,SCEN,2026,6237.2,12.7342,13.5173,2.00612,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.630036,0.249444,0.380592,0,21595,1907.18,27219.4,1945.18,-0.911684,0.171066,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,10504.4,10504.4,16409.8,23822.3,82.7142,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2027,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,f3e241047a9947d90cfff6e9a11bd3b3b2425a8aecc5cf9a13b39c1383e83f6d,243.205,241.852,29.6084,44.887,0,74.4953,117.671,16.8792,6.66768,63.308,25.162,38.1461,0.30802,93.8169,90.3609,95.7402,87.1293,91.2371,0.928716,0.972501,87.1293,91.2371,0.928716,0.972501,0.54849,0.574349,0,0,0,0,192,192,41.5705,81.7483,0,0,0,0,0,0,1,1,0.0866883,0.0697912,158.853,158.853,,none,0,0,7884,876,1,0.710843,1,OK,BASE,SCEN,2027,6237.2,12.9519,13.6606,2.04194,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.63308,0.25162,0.381461,0,22000.4,1907.18,27732.4,1945.18,-0.913312,0.170024,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,10800.6,10800.6,16793.4,24323.5,83.3022,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2028,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,a35726282b8bfe7dd285baccda4da070f7d7fd448a0e019ec67de296352408a9,247.668,246.313,30.1557,45.3917,0,75.5474,118.831,16.9195,6.67103,63.5754,25.3769,38.1985,0.306713,94.4802,91.213,96.2799,87.7159,91.8674,0.928405,0.972346,87.7159,91.8674,0.928405,0.972346,0.548557,0.57452,0,0,0,0,193,193,41.9491,82.3145,0,0,0,0,0,0,1,1,0.0853506,0.0686908,159.903,159.903,,none,0,0,7905,879,1,0.711188,1,OK,BASE,SCEN,2028,6237.2,13.1695,13.8039,2.07776,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.635754,0.253769,0.381985,0,22344.3,1907.1,28171,1944.67,-0.914649,0.169109,0,,1.35454,1,ok,6.67103,0,0,,,,0,0,0,0.100068,11031,11031,17131.4,24786.5,83.8658,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2029,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,c353feaa4040fd0402d24239acb6fb2aeb97a63556581e58613416aa91fdd89b,252.13,250.777,30.6036,45.8286,0,76.4323,119.608,16.8792,6.66768,63.9022,25.5866,38.3157,0.304782,95.2015,95.4465,95.0652,88.4015,92.6284,0.928573,0.972972,88.4015,92.6284,0.928573,0.972972,0.548814,0.575055,0,0,0,0,194,194,42.5691,83.0085,0,0,0,0,0,0,1,1,0.083598,0.0673074,161.077,161.077,,none,0,0,7884,876,1,0.712258,1,OK,BASE,SCEN,2029,6237.2,13.3872,13.9472,2.11358,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.639022,0.255866,0.383157,0,22813.7,1907.18,28755.7,1945.18,-0.916402,0.167778,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,11383.4,11383.4,17568.4,25361.9,84.4891,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2030,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,4ae2b97b7d0af5b1e5df5016e3fc94de04c445bd68ea763e5c02e29aa6dd63fe,256.593,255.24,31.1012,46.2995,0,77.4007,120.577,16.8792,6.66768,64.1922,25.7938,38.3984,0.303247,95.8938,94.5818,96.624,89.022,93.3209,0.928339,0.973169,89.022,93.3209,0.928339,0.973169,0.548867,0.575372,0,0,0,0,193,193,42.7005,83.6387,0,0,0,0,0,0,1,1,0.0821305,0.0661306,162.192,162.192,,none,0,0,7884,876,1,0.712949,1,OK,BASE,SCEN,2030,6237.2,13.6049,14.0905,2.1494,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.641922,0.257938,0.383984,0,23221.3,1907.18,29267,1945.18,-0.917869,0.166716,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,11678.8,11678.8,17951.8,25879.5,85.0821,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2031,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,5a6edba10cd060d7e27fdd137fff68c0df2e20efe2f87b5842f0bddccfa47aaf,261.055,259.702,31.5989,46.7703,0,78.3692,121.545,16.8792,6.66768,64.4775,25.9977,38.4798,0.301766,96.5861,93.52,98.2925,89.6587,94.0078,0.928277,0.973305,89.6587,94.0078,0.928277,0.973305,0.549044,0.575676,0,0,0,0,193,193,43.0172,84.2688,0,0,0,0,0,0,1,1,0.0807177,0.0649943,163.3,163.3,,none,0,0,7884,876,1,0.713624,1,OK,BASE,SCEN,2031,6237.2,13.8226,14.2338,2.18522,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.644775,0.259977,0.384798,0,23627.7,1907.18,29778.3,1945.18,-0.919282,0.165664,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,11973,11973,18347.9,26389.5,85.6709,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2032,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,3bdd9dde08b287d7926441c02d58422950d6934ca8b7b727a575d7deaebcc096,265.518,264.163,32.1495,47.2764,0,79.4259,122.71,16.9195,6.67103,64.7267,26.1996,38.527,0.30067,97.2469,93.7892,99.1743,90.2541,94.6335,0.928092,0.973127,90.2541,94.6335,0.928092,0.973127,0.549138,0.575784,0,0,0,0,194,194,43.3954,84.8304,0,0,0,0,0,0,1,1,0.079568,0.0640493,164.356,164.356,,none,0,0,7905,879,1,0.713908,1,OK,BASE,SCEN,2032,6237.2,14.0403,14.3771,2.22104,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.647267,0.261996,0.38527,0,23968.1,1907.1,30210,1944.67,-0.920432,0.164805,0,,1.35454,1,ok,6.67103,0,0,,,,0,0,0,0.100068,12201.2,12201.2,18676.5,26849.9,86.2251,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2033,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,49e598eb6767c14f2047091aaecc5b6fe4410b81d8abe15ab7623e204a92a4be,269.98,268.627,32.5941,47.712,0,80.3061,123.482,16.8792,6.66768,65.0347,26.3959,38.6388,0.29895,97.9707,94.5495,99.8633,90.9343,95.3805,0.928178,0.973561,90.9343,95.3805,0.928178,0.973561,0.549376,0.576237,0,0,0,0,195,195,44.0265,85.529,0,0,0,0,0,0,1,1,0.0780194,0.0628349,165.523,165.523,,none,0,0,7884,876,1,0.71493,1,OK,BASE,SCEN,2033,6237.2,14.2579,14.5204,2.25686,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.650347,0.263959,0.386388,0,24444.9,1907.18,30801.7,1945.18,-0.921981,0.163535,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,12569,12569,19125.3,27424.1,86.852,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2034,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,09e4ea92aee5afaee8a073bed1e1661375c983871c865064ec3993371150347e,274.443,273.09,33.0917,48.1828,0,81.2745,124.45,16.8792,6.66768,65.3068,26.5903,38.7165,0.297611,98.6631,97.4357,99.342,91.5711,96.0771,0.928119,0.97379,91.5711,96.0771,0.928119,0.97379,0.549505,0.576545,0,0,0,0,195,195,44.3451,86.1592,0,0,0,0,0,0,1,1,0.0767475,0.0618081,166.643,166.643,,none,0,0,7884,876,1,0.715566,1,OK,BASE,SCEN,2034,6237.2,14.4756,14.6637,2.29268,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.653068,0.265903,0.387165,0,24850,1907.18,31315.5,1945.18,-0.923253,0.162492,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,12863.3,12863.3,19512.9,27935.5,87.4407,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2035,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:BASE,ca6b2204d35d2e73e3b8c5e49dbda2f8e7f86d918777f196624442f7d6d17c89,278.905,277.552,33.5894,48.6536,0,82.243,125.419,16.8792,6.66768,65.5747,26.7818,38.7929,0.296315,99.3554,99.5768,99.2321,92.2072,96.7666,0.928055,0.973945,92.2072,96.7666,0.928055,0.973945,0.549627,0.576805,0,0,0,0,196,196,44.8535,86.7893,0,0,0,0,0,0,1,1,0.0755063,0.0608144,167.763,167.763,,none,0,0,7884,876,1,0.716191,1,OK,BASE,SCEN,2035,6237.2,14.6933,14.807,2.3285,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.655747,0.267818,0.387929,0,25258.5,1907.18,31829.5,1945.18,-0.924494,0.161486,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,13157.1,13157.1,19909.9,28464.2,88.0397,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
```


#### Scenario `DEMAND_UP`

#### Summary (DEMAND_UP)
```json
{
  "module_id": "Q1",
  "run_id": "FULL_20260211_191955_DEMAND_UP",
  "selection": {
    "countries": [
      "FR",
      "DE",
      "ES",
      "NL",
      "BE",
      "CZ",
      "IT_NORD"
    ],
    "years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "scenario_ids": [
      "BASE",
      "DEMAND_UP",
      "FLEX_UP",
      "LOW_RIGIDITY"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955",
    "mode": "SCEN",
    "scenario_id": "DEMAND_UP",
    "horizon_year": 2035
  },
  "assumptions_used": [
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "capture_ratio_pv_stage2_max",
      "param_value": 0.8,
      "unit": "ratio",
      "description": "Seuil capture ratio PV vs baseload en declenchement phase2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "capture_ratio_wind_stage2_max",
      "param_value": 0.9,
      "unit": "ratio",
      "description": "Seuil capture ratio Wind vs baseload en declenchement phase2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "days_spread_gt50_stage2_min",
      "param_value": 150.0,
      "unit": "days",
      "description": "Seuil jours spread>50",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "avg_daily_spread_crisis_min",
      "param_value": 50.0,
      "unit": "EUR/MWh",
      "description": "Seuil spread journalier moyen pour tagger une annee de crise",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "h_below_5_stage2_min",
      "param_value": 500.0,
      "unit": "hours",
      "description": "Seuil heures basses",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "h_negative_stage2_min",
      "param_value": 200.0,
      "unit": "hours",
      "description": "Seuil heures negatives stage2",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_capture_ratio_pv_min",
      "param_value": 0.85,
      "unit": "ratio",
      "description": "Stage1 min capture ratio PV vs baseload",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_capture_ratio_wind_min",
      "param_value": 0.9,
      "unit": "ratio",
      "description": "Stage1 min capture ratio Wind vs baseload",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_h_below_5_max",
      "param_value": 500.0,
      "unit": "hours",
      "description": "Stage1 max hours below 5 (doit rester sous seuil stage2)",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_h_negative_max",
      "param_value": 200.0,
      "unit": "hours",
      "description": "Stage1 max negative hours (doit rester sous seuil stage2)",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHYSICS_THRESHOLDS",
      "param_name": "far_stage2_min",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Seuil FAR minimal pour eviter stress physique stage2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHYSICS_THRESHOLDS",
      "param_name": "ir_p10_stage2_min",
      "param_value": 1.5,
      "unit": "ratio",
      "description": "Alias seuil inflexibilite haute stage2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHYSICS_THRESHOLDS",
      "param_name": "sr_hours_stage2_min",
      "param_value": 0.1,
      "unit": "share",
      "description": "Seuil part d'heures de surplus pour stress physique stage2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_sr_hours_max",
      "param_value": 0.05,
      "unit": "share",
      "description": "Stage1 max part d'heures de surplus",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_far_min",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Stage1 min FAR",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_ir_p10_max",
      "param_value": 1.5,
      "unit": "ratio",
      "description": "Stage1 max IR P10",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "QUALITY",
      "param_name": "regime_coherence_min_for_causality",
      "param_value": 0.55,
      "unit": "ratio",
      "description": "Seuil coherence minimale causalite",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "q1_persistence_window_years",
      "param_value": 2.0,
      "unit": "years",
      "description": "Q1: nombre d'annees consecutives requises pour valider une bascule",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "q1_lever_max_uplift",
      "param_value": 1.0,
      "unit": "ratio",
      "description": "Q1: borne max d'uplift pour solveurs required_demand/flex",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    }
  ],
  "kpis": {
    "n_countries": 7,
    "n_bascule_market": 1,
    "n_bascule_physical": 6,
    "n_scope_rows": 77
  },
  "checks": [
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "CZ 2030: annee saine non marquee stage1."
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "BE: coverage max=80.22% (>60%), possible surestimation must-run."
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "CZ: coverage max=89.16% (>60%), possible surestimation must-run."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%]."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "DEMAND_UP",
  "horizon_year": 2035
}
```

#### Narratif (DEMAND_UP)
Q1 identifie la bascule Phase 1 -> Phase 2 avec gating explicite: >=2 familles LOW_PRICE/VALUE/PHYSICAL, hors annees de crise configurees, et qualite data uniquement. Les diagnostics NEG_NOT_IN_SURPLUS restent visibles via market_physical_gap_flag mais ne bloquent pas la classification.

#### Table SCEN DEMAND_UP `Q1/scen/DEMAND_UP/tables/Q1_before_after_bascule.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,bascule_year_market,pre_window_start_year,pre_window_end_year,post_window_start_year,post_window_end_year,n_pre_years,n_post_years,pre_mean_capture_ratio_pv,post_mean_capture_ratio_pv,delta_post_minus_pre_capture_ratio_pv,pre_mean_capture_ratio_wind,post_mean_capture_ratio_wind,delta_post_minus_pre_capture_ratio_wind,pre_mean_h_negative_obs,post_mean_h_negative_obs,delta_post_minus_pre_h_negative_obs,pre_mean_sr_hours_share,post_mean_sr_hours_share,delta_post_minus_pre_sr_hours_share,pre_mean_far_observed,post_mean_far_observed,delta_post_minus_pre_far_observed,pre_mean_ir_p10,post_mean_ir_p10,delta_post_minus_pre_ir_p10
DE,,,,,,0,0,,,,,,,,,,,,,,,,,,
```

##### ES (1 lignes)
```csv
country,bascule_year_market,pre_window_start_year,pre_window_end_year,post_window_start_year,post_window_end_year,n_pre_years,n_post_years,pre_mean_capture_ratio_pv,post_mean_capture_ratio_pv,delta_post_minus_pre_capture_ratio_pv,pre_mean_capture_ratio_wind,post_mean_capture_ratio_wind,delta_post_minus_pre_capture_ratio_wind,pre_mean_h_negative_obs,post_mean_h_negative_obs,delta_post_minus_pre_h_negative_obs,pre_mean_sr_hours_share,post_mean_sr_hours_share,delta_post_minus_pre_sr_hours_share,pre_mean_far_observed,post_mean_far_observed,delta_post_minus_pre_far_observed,pre_mean_ir_p10,post_mean_ir_p10,delta_post_minus_pre_ir_p10
ES,2025,2022,2024,2025,2027,0,3,,0.931073,,,0.973984,,,0,,,0,,,1,,,0.0802492,
```


#### Table SCEN DEMAND_UP `Q1/scen/DEMAND_UP/tables/Q1_country_summary.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,bascule_year_market,bascule_year_market_country,bascule_year_market_pv,bascule_year_market_wind,bascule_year_physical,bascule_year_market_observed,bascule_year_physical_observed,bascule_status_market,bascule_status_market_pv,bascule_status_market_wind,bascule_status_physical,stage1_bascule_year,stage1_detected,bascule_confidence,families_active_at_bascule_pv,families_active_at_bascule_wind,families_active_at_bascule_country,drivers_at_bascule,low_price_flags_count_at_bascule,physical_flags_count_at_bascule,capture_flags_count_at_bascule,stage2_market_score_at_bascule,score_breakdown_at_bascule,required_demand_uplift_to_avoid_phase2,required_demand_uplift_status,required_flex_uplift_to_avoid_phase2,required_flex_uplift_status,bascule_rationale,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,capture_ratio_pv_at_bascule,capture_ratio_wind_at_bascule,market_physical_gap_at_bascule,neg_price_explained_by_surplus_ratio_at_bascule,h_negative_at_bascule,notes_quality
DE,,,,,2025,,,not_reached_in_window,not_reached_in_window,not_reached_in_window,already_phase2_at_window_start,2025,True,0,PHYSICAL,PHYSICAL,PHYSICAL,,0,1,0,1,low=0;value=0;physical=1;crisis=0,0,already_not_phase2,0,already_not_phase2,Pas de bascule persistante sur la fenetre.,0,1,0.0397103,216.403,0.595215,0.965438,0.962369,False,,0,ok
```

##### ES (1 lignes)
```csv
country,bascule_year_market,bascule_year_market_country,bascule_year_market_pv,bascule_year_market_wind,bascule_year_physical,bascule_year_market_observed,bascule_year_physical_observed,bascule_status_market,bascule_status_market_pv,bascule_status_market_wind,bascule_status_physical,stage1_bascule_year,stage1_detected,bascule_confidence,families_active_at_bascule_pv,families_active_at_bascule_wind,families_active_at_bascule_country,drivers_at_bascule,low_price_flags_count_at_bascule,physical_flags_count_at_bascule,capture_flags_count_at_bascule,stage2_market_score_at_bascule,score_breakdown_at_bascule,required_demand_uplift_to_avoid_phase2,required_demand_uplift_status,required_flex_uplift_to_avoid_phase2,required_flex_uplift_status,bascule_rationale,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,capture_ratio_pv_at_bascule,capture_ratio_wind_at_bascule,market_physical_gap_at_bascule,neg_price_explained_by_surplus_ratio_at_bascule,h_negative_at_bascule,notes_quality
ES,2025,2025,2025,2025,2025,2025,,transition_observed,already_phase2_at_window_start,already_phase2_at_window_start,already_phase2_at_window_start,2025,True,1,"LOW_PRICE,PHYSICAL","LOW_PRICE,PHYSICAL","LOW_PRICE,PHYSICAL",,0,1,0,2,low=1;value=0;physical=1;crisis=0,0.300049,ok,,beyond_plausible_bounds,Bascule validee: >=2 familles actives (LOW_PRICE/VALUE/PHYSICAL) sur 2 annees consecutives hors crise.,0,1,0.0817746,159.347,0.548552,0.93117,0.973825,False,,0,ok
```


#### Table SCEN DEMAND_UP `Q1/scen/DEMAND_UP/tables/Q1_ir_diagnostics.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,ir_p10,p10_must_run_mw,p10_load_mw,p50_must_run_mw,p50_load_mw,ir_case_class
DE,2025,0.04732,2208.4,46669.4,2244.17,60150.3,must_run_floor_effect
DE,2026,0.0464299,2208.4,47564.1,2244.17,61297.4,must_run_floor_effect
DE,2027,0.0455727,2208.4,48458.7,2244.17,62444.5,must_run_floor_effect
DE,2028,0.044849,2207.77,49226.7,2243.2,63420,must_run_floor_effect
DE,2029,0.0439515,2208.4,50246.2,2244.17,64739,must_run_floor_effect
DE,2030,0.0431837,2208.4,51139.6,2244.17,65887.6,must_run_floor_effect
DE,2031,0.0424412,2208.4,52034.2,2244.17,67034.6,must_run_floor_effect
DE,2032,0.0418175,2207.77,52795.3,2243.2,68001.4,must_run_floor_effect
DE,2033,0.0410304,2208.4,53823.4,2244.17,69331.3,must_run_floor_effect
DE,2034,0.0403596,2208.4,54718,2244.17,70481,must_run_floor_effect
DE,2035,0.0397103,2208.4,55612.6,2244.17,71631.9,must_run_floor_effect
```

##### ES (11 lignes)
```csv
country,year,ir_p10,p10_must_run_mw,p10_load_mw,p50_must_run_mw,p50_load_mw,ir_case_class
ES,2025,0.0817746,1907.18,23322.4,1945.18,29395,must_run_floor_effect
ES,2026,0.0802316,1907.18,23770.9,1945.18,29957.6,must_run_floor_effect
ES,2027,0.0787416,1907.18,24220.7,1945.18,30520,must_run_floor_effect
ES,2028,0.0775275,1907.1,24599,1944.67,31002.1,must_run_floor_effect
ES,2029,0.0759361,1907.18,25115.5,1945.18,31649.6,must_run_floor_effect
ES,2030,0.0746037,1907.18,25564.1,1945.18,32215.1,must_run_floor_effect
ES,2031,0.0733272,1907.18,26009.1,1945.18,32777.2,must_run_floor_effect
ES,2032,0.0723022,1907.1,26376.8,1944.67,33254.4,must_run_floor_effect
ES,2033,0.0709005,1907.18,26899.3,1945.18,33906.4,must_run_floor_effect
ES,2034,0.0697456,1907.18,27344.8,1945.18,34470.4,must_run_floor_effect
ES,2035,0.06862,1907.18,27793.3,1945.18,35032.6,must_run_floor_effect
```


#### Table SCEN DEMAND_UP `Q1/scen/DEMAND_UP/tables/Q1_residual_diagnostics.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_median_eur_mwh,residual_negative_p10_mw,residual_negative_p50_mw,residual_negative_p90_mw
DE,2025,26054.5,40936.5,56321.2,108.956,,,,
DE,2026,26830.6,41927.8,57553.4,109.99,,,,
DE,2027,27609.8,42908.6,58773.7,111.035,,,,
DE,2028,28211.5,43684.2,59783.1,112.047,,,,
DE,2029,29146.5,44877.9,61214.7,113.113,,,,
DE,2030,29938,45871.4,62423.6,114.148,,,,
DE,2031,30643.4,46782.9,63632,115.151,,,,
DE,2032,31192.5,47481.4,64578.1,116.119,,,,
DE,2033,32075.2,48599.4,65966.1,117.166,,,,
DE,2034,32779.2,49530.1,67170.8,118.184,,,,
DE,2035,33445.6,50449,68375.3,119.191,,,,
```

##### ES (11 lignes)
```csv
country,year,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_median_eur_mwh,residual_negative_p10_mw,residual_negative_p50_mw,residual_negative_p90_mw
ES,2025,12587.1,18574.8,26349.9,83.2753,,,,
ES,2026,12935.6,19016.7,26933.5,83.886,,,,
ES,2027,13288.4,19442.6,27524.7,84.4997,,,,
ES,2028,13567.3,19821.3,28011.7,85.0774,,,,
ES,2029,13979.6,20315.8,28667.8,85.7209,,,,
ES,2030,14315.9,20751.7,29257.3,86.3321,,,,
ES,2031,14655.6,21184.9,29834.9,86.941,,,,
ES,2032,14926.2,21561.5,30326,87.5191,,,,
ES,2033,15336.4,22073.9,30989.4,88.1657,,,,
ES,2034,15679.4,22508.3,31566.4,88.7757,,,,
ES,2035,16023.3,22943.4,32131.8,89.3848,,,,
```


#### Table SCEN DEMAND_UP `Q1/scen/DEMAND_UP/tables/Q1_rule_application.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,capture_ratio_pv,capture_ratio_wind,stage2_market_score,score_breakdown,crisis_year,quality_flag,quality_ok,stage2_candidate_year,stage1_candidate_year,phase2_candidate_year,low_price_flags_count,physical_flags_count,capture_flags_count,active_flags,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_low_residual_high,flag_sr_high,flag_far_low,flag_ir_high,flag_spread_high,market_physical_gap_flag,neg_price_explained_by_surplus_ratio,low_price_family,value_family,value_family_pv,value_family_wind,physical_family,family_count_pv,family_count_wind,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,physical_candidate_year,flag_capture_only_stage2,is_stage1_criteria,is_phase2_market,is_phase2_physical,phase_market,stress_phys_state
DE,2025,0.962281,0.960473,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2026,0.962963,0.96065,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2027,0.963606,0.960741,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2028,0.964676,0.960785,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2029,0.965351,0.961006,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2030,0.965789,0.961227,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2031,0.965748,0.961676,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2032,0.965732,0.961778,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2033,0.965687,0.962041,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2034,0.965608,0.962172,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2035,0.965438,0.962369,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
```

##### ES (11 lignes)
```csv
country,year,capture_ratio_pv,capture_ratio_wind,stage2_market_score,score_breakdown,crisis_year,quality_flag,quality_ok,stage2_candidate_year,stage1_candidate_year,phase2_candidate_year,low_price_flags_count,physical_flags_count,capture_flags_count,active_flags,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_low_residual_high,flag_sr_high,flag_far_low,flag_ir_high,flag_spread_high,market_physical_gap_flag,neg_price_explained_by_surplus_ratio,low_price_family,value_family,value_family_pv,value_family_wind,physical_family,family_count_pv,family_count_wind,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,physical_candidate_year,flag_capture_only_stage2,is_stage1_criteria,is_phase2_market,is_phase2_physical,phase_market,stress_phys_state
ES,2025,0.93117,0.973825,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2026,0.931116,0.973956,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2027,0.930932,0.974172,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2028,0.930529,0.974066,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2029,0.930792,0.974687,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2030,0.930519,0.974974,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2031,0.930488,0.97514,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2032,0.930258,0.974991,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2033,0.93037,0.975497,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2034,0.930553,0.975596,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2035,0.9305,0.975639,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
```


#### Table SCEN DEMAND_UP `Q1/scen/DEMAND_UP/tables/Q1_rule_definition.csv`
Lignes: `1`

```csv
q1_rule_version,h_negative_stage2_min,h_below_5_stage2_min,capture_ratio_pv_stage2_max,capture_ratio_wind_stage2_max,sr_hours_stage2_min,low_residual_hours_stage2_min,far_stage2_min,ir_p10_stage2_min,days_spread_gt50_stage2_min,avg_daily_spread_crisis_min,stage1_capture_ratio_pv_min,stage1_capture_ratio_wind_min,stage1_sr_hours_max,stage1_far_min,stage1_ir_p10_max,persistence_window_years,crisis_years_explicit,rule_logic
q1_rule_v4_2026_02_11,200,500,0.8,0.9,0.1,0.1,0.95,1.5,150,50,0.85,0.9,0.05,0.95,1.5,2,2022,"stage2_candidate_tech=(>=2 familles actives parmi LOW_PRICE/PHYSICAL/VALUE_TECH) avec persistence sur 2 annees non-crise; bascule_country=min(bascule_pv,bascule_wind). stage1_candidate=(familles toutes inactives) hors crise. NEG_NOT_IN_AB reste informatif; RC principal=AB_OR_LOW_RESIDUAL."
```


#### Table SCEN DEMAND_UP `Q1/scen/DEMAND_UP/tables/Q1_scope_audit.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,must_run_scope_coverage,lowload_p20_mw,ir_p10,scope_status,scope_reason,load_net_mode,must_run_mode_hourly
DE,2025,0.1522,50075.3,0.04732,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2026,0.150922,51031.4,0.0464299,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2027,0.149666,51987.6,0.0455727,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2028,0.148212,52805.4,0.044849,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2029,0.147405,53899,0.0439515,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2030,0.146263,54856.5,0.0431837,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2031,0.144894,55812.5,0.0424412,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2032,0.14333,56620.5,0.0418175,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2033,0.142209,57722.9,0.0410304,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2034,0.140898,58677.8,0.0403596,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2035,0.139611,59633.1,0.0397103,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
```

##### ES (11 lignes)
```csv
country,year,must_run_scope_coverage,lowload_p20_mw,ir_p10,scope_status,scope_reason,load_net_mode,must_run_mode_hourly
ES,2025,0.172394,24755.1,0.0817746,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2026,0.171235,25231.4,0.0802316,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2027,0.170091,25703.8,0.0787416,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2028,0.169176,26105.2,0.0775275,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2029,0.167871,26649.8,0.0759361,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2030,0.166846,27125.3,0.0746037,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2031,0.165804,27598.8,0.0733272,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2032,0.164951,27999.5,0.0723022,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2033,0.163683,28552.7,0.0709005,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2034,0.16264,29029.6,0.0697456,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2035,0.161765,29506,0.06862,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
```


#### Table SCEN DEMAND_UP `Q1/scen/DEMAND_UP/tables/Q1_year_panel.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative,h_negative_obs,h_below_5,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,scenario_id,mode,horizon_year,calib_mustrun_scale,calib_vre_scale_pv,calib_vre_scale_wind_on,calib_vre_scale_wind_off,calib_export_cap_eff_gw,calib_export_coincidence_used,calib_flex_realization_factor,calib_price_b_floor,calib_price_b_intercept,calib_price_b_slope_surplus_norm,vre_penetration_share_gen,pv_penetration_share_gen,wind_penetration_share_gen,sr_hours_share,p10_load_mw,p10_must_run_mw,p50_load_mw,p50_must_run_mw,ir_p10_excess,must_run_scope_coverage,core_sanity_issue_count,core_sanity_issues,psh_pumping_twh,psh_pumping_coverage_share,psh_pumping_data_status,flex_sink_exports_twh,flex_sink_psh_twh,flex_sink_total_twh,share_neg_price_hours_in_AB,share_neg_price_hours_in_low_residual,share_neg_price_hours_in_AB_OR_LOW_RESIDUAL,surplus_energy_twh,absorbed_surplus_twh,unabsorbed_surplus_twh,low_residual_hours_share,low_residual_threshold_mw,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_hours_median_eur_mwh,residual_load_p50_on_negative_price_mw,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_sr_high,flag_low_residual_high,flag_far_low,flag_ir_high,flag_spread_high,crisis_year,low_price_family,value_family_pv,value_family_wind,value_family,physical_family,low_price_flags_count,capture_flags_count,physical_flags_count,family_count,family_count_pv,family_count_wind,stage2_points_low_price,stage2_points_capture,stage2_points_physical,stage2_points_vol,stage2_market_score,score_breakdown,quality_ok,neg_price_explained_by_surplus_ratio,market_physical_gap_flag,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,stage2_candidate_year,phase2_candidate_year,flag_capture_only_stage2,is_phase2_market,physical_candidate_year,is_phase2_physical,signal_low_price,signal_value,signal_physical,flag_non_capture_stage2,active_flags,is_stage1_criteria,stage1_candidate_year,phase_market,stress_phys_state
DE,2025,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,c3ceb86a5b7e2f50b4793807b0a65033659f27cdedabe1c144828e86bf14813c,528.19,526.71,31.6975,93.7283,19.9439,145.37,169.714,19.582,3.45865,85.6559,18.677,66.9788,0.275996,121.85,126.333,119.356,117.254,117.034,0.962281,0.960473,117.254,117.034,0.962281,0.960473,0.590698,0.589588,0,0,0,0,122,122,32.234,93.8067,0,0,0,0,0,0,1,1,0.04732,0.037178,198.501,198.501,,none,0,0,7884,876,1,0.677016,1,OK,DEMAND_UP,SCEN,2025,9425.89,19.4667,36.463,5.37175,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.856559,0.18677,0.669788,0,46669.4,2208.4,60150.3,2244.17,-0.95268,0.1522,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,26054.5,26054.5,40936.5,56321.2,108.956,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2026,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,3b5af24fcf630b4bf549c52a69b1146d4781f7d45e5e0fbd047d13d19b27bc60,538.251,536.771,31.6975,94.7325,20.3065,146.736,171.08,19.582,3.45865,85.7705,18.5278,67.2427,0.273369,123.015,125.253,121.769,118.459,118.174,0.962963,0.96065,118.459,118.174,0.962963,0.96065,0.591486,0.590065,0,0,0,0,123,123,32.7403,94.6322,0,0,0,0,0,0,1,1,0.0464299,0.0364812,200.273,200.273,,none,0,0,7884,876,1,0.677452,1,OK,DEMAND_UP,SCEN,2026,9425.89,19.8053,36.8537,5.46942,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.857705,0.185278,0.672427,0,47564.1,2208.4,61297.4,2244.17,-0.95357,0.150922,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,26830.6,26830.6,41927.8,57553.4,109.99,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2027,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,a337a335c33ffbae1ee656a31cacae0909bef64720929e378cfcf310143173d5,548.311,546.831,31.6975,95.7368,20.6691,148.103,172.447,19.582,3.45865,85.8832,18.381,67.5023,0.270839,124.179,125.685,123.341,119.66,119.304,0.963606,0.960741,119.66,119.304,0.963606,0.960741,0.592137,0.590376,0,0,0,0,123,123,33.032,95.4577,0,0,0,0,0,0,1,1,0.0455727,0.03581,202.081,202.081,,none,0,0,7884,876,1,0.677859,1,OK,DEMAND_UP,SCEN,2027,9425.89,20.1438,37.2444,5.56709,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.858832,0.18381,0.675023,0,48458.7,2208.4,62444.5,2244.17,-0.954427,0.149666,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,27609.8,27609.8,42908.6,58773.7,111.035,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2028,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,b149db03be0914c87e929264b90cce755b4041640617922674c3ee525f921de7,558.372,556.889,31.722,97.1985,21.088,150.008,174.417,19.6256,3.4966,86.0055,18.1874,67.818,0.269369,125.295,128.028,123.79,120.869,120.382,0.964676,0.960785,120.869,120.382,0.964676,0.960785,0.593161,0.590768,0,0,0,0,123,123,33.2225,96.2232,0,0,0,0,0,0,1,1,0.044849,0.0352414,203.772,203.772,,none,0,0,7905,879,1,0.67846,1,OK,DEMAND_UP,SCEN,2028,9425.89,20.4824,37.635,5.66476,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.860055,0.181874,0.67818,0,49226.7,2207.77,63420,2243.2,-0.955151,0.148212,0,,1.48351,1,ok,3.4966,0,0,,,,0,0,0,0.100068,28211.5,28211.5,43684.2,59783.1,112.047,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2029,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,144c0215df6b93de786624318b69a5865ce8f0ae9c6fbd1ced31ba3194240e0c,568.433,566.953,31.6975,97.7453,21.3943,150.837,175.181,19.582,3.45865,86.1035,18.0941,68.0094,0.266049,126.508,138.193,120.005,122.125,121.575,0.965351,0.961006,122.125,121.575,0.965351,0.961006,0.593731,0.591058,0,0,0,0,122,122,33.4035,97.1087,0,0,0,0,0,0,1,1,0.0439515,0.034539,205.69,205.69,,none,0,0,7884,876,1,0.678613,1,OK,DEMAND_UP,SCEN,2029,9425.89,20.8209,38.0257,5.76243,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.861035,0.180941,0.680094,0,50246.2,2208.4,64739,2244.17,-0.956049,0.147405,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,29146.5,29146.5,44877.9,61214.7,113.113,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2030,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,8c27da0ecab8764960bd040452cf697aa0fab13480f3972abe5187db2f190b97,578.494,577.014,31.6975,98.7495,21.757,152.204,176.548,19.582,3.45865,86.2111,17.954,68.2571,0.263779,127.672,136.484,122.769,123.305,122.722,0.965789,0.961227,123.305,122.722,0.965789,0.961227,0.594296,0.591489,0,0,0,0,122,122,33.7049,97.9342,0,0,0,0,0,0,1,1,0.0431837,0.0339368,207.48,207.48,,none,0,0,7884,876,1,0.678959,1,OK,DEMAND_UP,SCEN,2030,9425.89,21.1595,38.4164,5.8601,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.862111,0.17954,0.682571,0,51139.6,2208.4,65887.6,2244.17,-0.956816,0.146263,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,29938,29938,45871.4,62423.6,114.148,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2031,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,d9569f57ed8a4fe9b2c839496f104426b3a11baa6fc4d3e1e6729b33491a096c,588.554,587.074,32.1598,99.7538,22.1196,154.033,178.377,19.582,3.45865,86.3525,18.0291,68.3234,0.262374,128.822,133.974,125.956,124.41,123.885,0.965748,0.961676,124.41,123.885,0.965748,0.961676,0.594529,0.592023,0,0,0,0,122,122,34.0048,98.7597,0,0,0,0,0,0,1,1,0.0424412,0.0333552,209.258,209.258,,none,0,0,7884,876,1,0.679725,1,OK,DEMAND_UP,SCEN,2031,9425.89,21.4981,38.8071,5.95777,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.863525,0.180291,0.683234,0,52034.2,2208.4,67034.6,2244.17,-0.957559,0.144894,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,30643.4,30643.4,46782.9,63632,115.151,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2032,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,09820de994258c8c9432615f30a10b4ee0d6002db2efcdd87ce43d8fa17cdf23,598.615,597.132,32.6953,101.234,22.5423,156.472,180.881,19.6256,3.4966,86.5055,18.0756,68.43,0.26204,129.919,132.589,128.431,125.467,124.953,0.965732,0.961778,125.467,124.953,0.965732,0.961778,0.594864,0.592429,0,0,0,0,122,122,34.1905,99.5207,0,0,0,0,0,0,1,1,0.0418175,0.0328664,210.917,210.917,,none,0,0,7905,879,1,0.680734,1,OK,DEMAND_UP,SCEN,2032,9425.89,21.8366,39.1978,6.05544,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.865055,0.180756,0.6843,0,52795.3,2207.77,68001.4,2243.2,-0.958182,0.14333,0,,1.48351,1,ok,3.4966,0,0,,,,0,0,0,0.100068,31192.5,31192.5,47481.4,64578.1,116.119,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2033,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,f6e21203deaf6293aaba2a3143c62a8d3348871bb80ce7fb11792b4f2f50fda6,608.676,607.196,33.1728,101.762,22.8448,157.78,182.124,19.582,3.45865,86.6333,18.2144,68.4189,0.25985,131.12,134.153,129.442,126.621,126.143,0.965687,0.962041,126.621,126.143,0.965687,0.962041,0.594966,0.59272,0,0,0,0,120,120,34.1458,100.411,0,0,0,0,0,0,1,1,0.0410304,0.0322499,212.82,212.82,,none,0,0,7884,876,1,0.681278,1,OK,DEMAND_UP,SCEN,2033,9425.89,22.1752,39.5884,6.15311,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.866333,0.182144,0.684189,0,53823.4,2208.4,69331.3,2244.17,-0.95897,0.142209,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,32075.2,32075.2,48599.4,65966.1,117.166,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2034,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,5d60fedfbfc83dd0f82e2be5aadc6ec151d4fca03c154b0c132231c369278496,618.737,617.257,33.6792,102.766,23.2075,159.653,183.997,19.582,3.45865,86.7694,18.3042,68.4652,0.25865,132.269,140.591,127.665,127.72,127.265,0.965608,0.962172,127.72,127.265,0.965608,0.962172,0.595121,0.593003,0,0,0,0,120,120,34.4429,101.236,0,0,0,0,0,0,1,1,0.0403596,0.0317243,214.611,214.611,,none,0,0,7884,876,1,0.682022,1,OK,DEMAND_UP,SCEN,2034,9425.89,22.5137,39.9791,6.25078,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.867694,0.183042,0.684652,0,54718,2208.4,70481,2244.17,-0.95964,0.140898,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,32779.2,32779.2,49530.1,67170.8,118.184,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2035,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,e2a49f4b722dec9d431c1698ddebc2b276ab1447307f24122b6a32fc240acd0e,628.798,627.317,34.1857,103.771,23.5701,161.527,185.87,19.582,3.45865,86.9027,18.3922,68.5105,0.257488,133.417,145.824,126.513,128.806,128.397,0.965438,0.962369,128.806,128.397,0.965438,0.962369,0.595215,0.593324,0,0,0,0,120,120,34.74,102.062,0,0,0,0,0,0,1,1,0.0397103,0.0312155,216.403,216.403,,none,0,0,7884,876,1,0.682744,1,OK,DEMAND_UP,SCEN,2035,9425.89,22.8523,40.3698,6.34845,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.869027,0.183922,0.685105,0,55612.6,2208.4,71631.9,2244.17,-0.96029,0.139611,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,33445.6,33445.6,50449,68375.3,119.191,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
```

##### ES (11 lignes)
```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative,h_negative_obs,h_below_5,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,scenario_id,mode,horizon_year,calib_mustrun_scale,calib_vre_scale_pv,calib_vre_scale_wind_on,calib_vre_scale_wind_off,calib_export_cap_eff_gw,calib_export_coincidence_used,calib_flex_realization_factor,calib_price_b_floor,calib_price_b_intercept,calib_price_b_slope_surplus_norm,vre_penetration_share_gen,pv_penetration_share_gen,wind_penetration_share_gen,sr_hours_share,p10_load_mw,p10_must_run_mw,p50_load_mw,p50_must_run_mw,ir_p10_excess,must_run_scope_coverage,core_sanity_issue_count,core_sanity_issues,psh_pumping_twh,psh_pumping_coverage_share,psh_pumping_data_status,flex_sink_exports_twh,flex_sink_psh_twh,flex_sink_total_twh,share_neg_price_hours_in_AB,share_neg_price_hours_in_low_residual,share_neg_price_hours_in_AB_OR_LOW_RESIDUAL,surplus_energy_twh,absorbed_surplus_twh,unabsorbed_surplus_twh,low_residual_hours_share,low_residual_threshold_mw,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_hours_median_eur_mwh,residual_load_p50_on_negative_price_mw,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_sr_high,flag_low_residual_high,flag_far_low,flag_ir_high,flag_spread_high,crisis_year,low_price_family,value_family_pv,value_family_wind,value_family,physical_family,low_price_flags_count,capture_flags_count,physical_flags_count,family_count,family_count_pv,family_count_wind,stage2_points_low_price,stage2_points_capture,stage2_points_physical,stage2_points_vol,stage2_market_score,score_breakdown,quality_ok,neg_price_explained_by_surplus_ratio,market_physical_gap_flag,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,stage2_candidate_year,phase2_candidate_year,flag_capture_only_stage2,is_phase2_market,physical_candidate_year,is_phase2_physical,signal_low_price,signal_value,signal_physical,flag_non_capture_stage2,active_flags,is_stage1_criteria,stage1_candidate_year,phase_market,stress_phys_state
ES,2025,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,54f5410d17fe3750b2dcf5f46700f6b102b5bf133b9ff21ebc6046a404a7fc8c,257.708,256.355,28.6131,43.9453,0,72.5584,115.734,16.8792,6.66768,62.694,24.7231,37.9709,0.283039,93.8709,90.9879,95.4754,87.4098,91.4138,0.93117,0.973825,87.4098,91.4138,0.93117,0.973825,0.548552,0.57368,0,0,0,0,195,195,42.4317,82.7599,0,0,0,0,0,0,1,1,0.0817746,0.0658428,159.347,159.347,,none,0,0,7884,876,1,0.714564,1,OK,DEMAND_UP,SCEN,2025,6237.2,12.5165,13.3741,1.9703,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.62694,0.247231,0.379709,0,23322.4,1907.18,29395,1945.18,-0.918225,0.172394,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,12587.1,12587.1,18574.8,26349.9,83.2753,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2026,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,41eeee8f0bb20ea782ba521739e60a79529ad06c01f79cbd9087ed003b1363db,262.617,261.264,29.1108,44.4161,0,73.5269,116.703,16.8792,6.66768,63.0036,24.9444,38.0592,0.281428,94.5907,91.3385,96.4005,88.0749,92.1272,0.931116,0.973956,88.0749,92.1272,0.931116,0.973956,0.548719,0.573966,0,0,0,0,195,195,42.7688,83.4345,0,0,0,0,0,0,1,1,0.0802316,0.0646058,160.51,160.51,,none,0,0,7884,876,1,0.715302,1,OK,DEMAND_UP,SCEN,2026,6237.2,12.7342,13.5173,2.00612,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.630036,0.249444,0.380592,0,23770.9,1907.18,29957.6,1945.18,-0.919768,0.171235,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,12935.6,12935.6,19016.7,26933.5,83.886,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2027,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,98cb0f26944a1ecfa5a69d9ef38fb4f68fb61f79e781e5ad0ffde69ff5bf82ae,267.526,266.173,29.6084,44.887,0,74.4953,117.671,16.8792,6.66768,63.308,25.162,38.1461,0.279876,95.3104,91.8601,97.2305,88.7275,92.8487,0.930932,0.974172,88.7275,92.8487,0.930932,0.974172,0.548765,0.574254,0,0,0,0,195,195,43.106,84.1091,0,0,0,0,0,0,1,1,0.0787416,0.0634143,161.686,161.686,,none,0,0,7884,876,1,0.716023,1,OK,DEMAND_UP,SCEN,2027,6237.2,12.9519,13.6606,2.04194,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.63308,0.25162,0.381461,0,24220.7,1907.18,30520,1945.18,-0.921258,0.170091,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,13288.4,13288.4,19442.6,27524.7,84.4997,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2028,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,f9657be1f00bc51f9357ad4f4459255825ea51de07eac1117e7d8a41d9fd9a37,272.434,271.08,30.1557,45.3917,0,75.5474,118.831,16.9195,6.67103,63.5754,25.3769,38.1985,0.27869,95.997,92.657,97.8368,89.328,93.5074,0.930529,0.974066,89.328,93.5074,0.930529,0.974066,0.548725,0.574398,0,0,0,0,196,196,43.5034,84.7128,0,0,0,0,0,0,1,1,0.0775275,0.062415,162.792,162.792,,none,0,0,7905,879,1,0.716354,1,OK,DEMAND_UP,SCEN,2028,6237.2,13.1695,13.8039,2.07776,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.635754,0.253769,0.381985,0,24599,1907.1,31002.1,1944.67,-0.922472,0.169176,0,,1.35454,1,ok,6.67103,0,0,,,,0,0,0,0.100068,13567.3,13567.3,19821.3,28011.7,85.0774,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2029,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,7a32435566dd3a735e89cdc660a978744b53fa7b8d8db328c5ef02eb08a37bdb,277.343,275.99,30.6036,45.8286,0,76.4323,119.608,16.8792,6.66768,63.9022,25.5866,38.3157,0.276938,96.7499,97.1279,96.5395,90.0541,94.3008,0.930792,0.974687,90.0541,94.3008,0.930792,0.974687,0.548918,0.574804,0,0,0,0,195,195,43.7812,85.4582,0,0,0,0,0,0,1,1,0.0759361,0.0611585,164.057,164.057,,none,0,0,7884,876,1,0.717418,1,OK,DEMAND_UP,SCEN,2029,6237.2,13.3872,13.9472,2.11358,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.639022,0.255866,0.383157,0,25115.5,1907.18,31649.6,1945.18,-0.924064,0.167871,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,13979.6,13979.6,20315.8,28667.8,85.7209,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2030,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,d4eb0e60d99f55443d19dc5143362501659295756c416f0d243c928303633672,282.252,280.899,31.1012,46.2995,0,77.4007,120.577,16.8792,6.66768,64.1922,25.7938,38.3984,0.275547,97.4696,96.1199,98.2208,90.6974,95.0304,0.930519,0.974974,90.6974,95.0304,0.930519,0.974974,0.54893,0.575155,0,0,0,0,195,195,44.1177,86.1328,0,0,0,0,0,0,1,1,0.0746037,0.0600898,165.226,165.226,,none,0,0,7884,876,1,0.7181,1,OK,DEMAND_UP,SCEN,2030,6237.2,13.6049,14.0905,2.1494,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.641922,0.257938,0.383984,0,25564.1,1907.18,32215.1,1945.18,-0.925396,0.166846,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,14315.9,14315.9,20751.7,29257.3,86.3321,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2031,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,2367844c8ec04519e758f6b15f19c7e8d82649004b307620fa31343743d9021b,287.161,285.808,31.5989,46.7703,0,78.3692,121.545,16.8792,6.66768,64.4775,25.9977,38.4798,0.274203,98.1894,95.0552,99.9336,91.3641,95.7484,0.930488,0.97514,91.3641,95.7484,0.930488,0.97514,0.549043,0.575391,0,0,0,0,195,195,44.4551,86.8074,0,0,0,0,0,0,1,1,0.0733272,0.0590578,166.406,166.406,,none,0,0,7884,876,1,0.718769,1,OK,DEMAND_UP,SCEN,2031,6237.2,13.8226,14.2338,2.18522,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.644775,0.259977,0.384798,0,26009.1,1907.18,32777.2,1945.18,-0.926673,0.165804,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,14655.6,14655.6,21184.9,29834.9,86.941,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2032,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,d676dd969c025c9ccaa64c3c76652584afda569bce86cb7883e053727cdd0f72,292.069,290.715,32.1495,47.2764,0,79.4259,122.71,16.9195,6.67103,64.7267,26.1996,38.527,0.273209,98.8731,95.446,100.784,91.9774,96.4004,0.930258,0.974991,91.9774,96.4004,0.930258,0.974991,0.549124,0.57553,0,0,0,0,194,194,44.4727,87.4061,0,0,0,0,0,0,1,1,0.0723022,0.0581995,167.498,167.498,,none,0,0,7905,879,1,0.719047,1,OK,DEMAND_UP,SCEN,2032,6237.2,14.0403,14.3771,2.22104,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.647267,0.261996,0.38527,0,26376.8,1907.1,33254.4,1944.67,-0.927698,0.164951,0,,1.35454,1,ok,6.67103,0,0,,,,0,0,0,0.100068,14926.2,14926.2,21561.5,30326,87.5191,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2033,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,bdc2898a85609adcc4f2ff1674a52f411c01d6820cd21a1b9e01d4ac4b58f68c,296.978,295.625,32.5941,47.712,0,80.3061,123.482,16.8792,6.66768,65.0347,26.3959,38.6388,0.271648,99.6289,96.1092,101.576,92.6917,97.1876,0.93037,0.975497,92.6917,97.1876,0.93037,0.975497,0.54927,0.575912,0,0,0,0,195,195,45.1307,88.1566,0,0,0,0,0,0,1,1,0.0709005,0.0570965,168.754,168.754,,none,0,0,7884,876,1,0.72007,1,OK,DEMAND_UP,SCEN,2033,6237.2,14.2579,14.5204,2.25686,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.650347,0.263959,0.386388,0,26899.3,1907.18,33906.4,1945.18,-0.929099,0.163683,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,15336.4,15336.4,22073.9,30989.4,88.1657,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2034,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,df6c4979a216d67c3b407f7d5c5d2c2aaaa4607f555367b6f0c9568ae7d2536a,301.887,300.534,33.0917,48.1828,0,81.2745,124.45,16.8792,6.66768,65.3068,26.5903,38.7165,0.270434,100.349,99.1083,101.035,93.3797,97.8998,0.930553,0.975596,93.3797,97.8998,0.930553,0.975596,0.549539,0.57614,0,0,0,0,194,194,45.2758,88.8312,0,0,0,0,0,0,1,1,0.0697456,0.0561639,169.924,169.924,,none,0,0,7884,876,1,0.720702,1,OK,DEMAND_UP,SCEN,2034,6237.2,14.4756,14.6637,2.29268,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.653068,0.265903,0.387165,0,27344.8,1907.18,34470.4,1945.18,-0.930254,0.16264,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,15679.4,15679.4,22508.3,31566.4,88.7757,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2035,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:DEMAND_UP,eb11c8c9d46d270e6b4904cd53f58ad0a9574c229f7c265a9b11b40c081dbb10,306.795,305.443,33.5894,48.6536,0,82.243,125.419,16.8792,6.66768,65.5747,26.7818,38.7929,0.269258,101.068,101.46,100.85,94.0442,98.6063,0.9305,0.975639,94.0442,98.6063,0.9305,0.975639,0.549626,0.576289,0,0,0,0,194,194,45.6122,89.5058,0,0,0,0,0,0,1,1,0.06862,0.0552613,171.106,171.106,,none,0,0,7884,876,1,0.721321,1,OK,DEMAND_UP,SCEN,2035,6237.2,14.6933,14.807,2.3285,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.655747,0.267818,0.387929,0,27793.3,1907.18,35032.6,1945.18,-0.93138,0.161765,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,16023.3,16023.3,22943.4,32131.8,89.3848,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
```


#### Scenario `FLEX_UP`

#### Summary (FLEX_UP)
```json
{
  "module_id": "Q1",
  "run_id": "FULL_20260211_191955_FLEX_UP",
  "selection": {
    "countries": [
      "FR",
      "DE",
      "ES",
      "NL",
      "BE",
      "CZ",
      "IT_NORD"
    ],
    "years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "scenario_ids": [
      "BASE",
      "DEMAND_UP",
      "FLEX_UP",
      "LOW_RIGIDITY"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955",
    "mode": "SCEN",
    "scenario_id": "FLEX_UP",
    "horizon_year": 2035
  },
  "assumptions_used": [
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "capture_ratio_pv_stage2_max",
      "param_value": 0.8,
      "unit": "ratio",
      "description": "Seuil capture ratio PV vs baseload en declenchement phase2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "capture_ratio_wind_stage2_max",
      "param_value": 0.9,
      "unit": "ratio",
      "description": "Seuil capture ratio Wind vs baseload en declenchement phase2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "days_spread_gt50_stage2_min",
      "param_value": 150.0,
      "unit": "days",
      "description": "Seuil jours spread>50",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "avg_daily_spread_crisis_min",
      "param_value": 50.0,
      "unit": "EUR/MWh",
      "description": "Seuil spread journalier moyen pour tagger une annee de crise",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "h_below_5_stage2_min",
      "param_value": 500.0,
      "unit": "hours",
      "description": "Seuil heures basses",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "h_negative_stage2_min",
      "param_value": 200.0,
      "unit": "hours",
      "description": "Seuil heures negatives stage2",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_capture_ratio_pv_min",
      "param_value": 0.85,
      "unit": "ratio",
      "description": "Stage1 min capture ratio PV vs baseload",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_capture_ratio_wind_min",
      "param_value": 0.9,
      "unit": "ratio",
      "description": "Stage1 min capture ratio Wind vs baseload",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_h_below_5_max",
      "param_value": 500.0,
      "unit": "hours",
      "description": "Stage1 max hours below 5 (doit rester sous seuil stage2)",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_h_negative_max",
      "param_value": 200.0,
      "unit": "hours",
      "description": "Stage1 max negative hours (doit rester sous seuil stage2)",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHYSICS_THRESHOLDS",
      "param_name": "far_stage2_min",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Seuil FAR minimal pour eviter stress physique stage2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHYSICS_THRESHOLDS",
      "param_name": "ir_p10_stage2_min",
      "param_value": 1.5,
      "unit": "ratio",
      "description": "Alias seuil inflexibilite haute stage2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHYSICS_THRESHOLDS",
      "param_name": "sr_hours_stage2_min",
      "param_value": 0.1,
      "unit": "share",
      "description": "Seuil part d'heures de surplus pour stress physique stage2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_sr_hours_max",
      "param_value": 0.05,
      "unit": "share",
      "description": "Stage1 max part d'heures de surplus",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_far_min",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Stage1 min FAR",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_ir_p10_max",
      "param_value": 1.5,
      "unit": "ratio",
      "description": "Stage1 max IR P10",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "QUALITY",
      "param_name": "regime_coherence_min_for_causality",
      "param_value": 0.55,
      "unit": "ratio",
      "description": "Seuil coherence minimale causalite",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "q1_persistence_window_years",
      "param_value": 2.0,
      "unit": "years",
      "description": "Q1: nombre d'annees consecutives requises pour valider une bascule",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "q1_lever_max_uplift",
      "param_value": 1.0,
      "unit": "ratio",
      "description": "Q1: borne max d'uplift pour solveurs required_demand/flex",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    }
  ],
  "kpis": {
    "n_countries": 7,
    "n_bascule_market": 2,
    "n_bascule_physical": 7,
    "n_scope_rows": 77
  },
  "checks": [
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "CZ 2028: annee saine non marquee stage1."
    },
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "CZ 2030: annee saine non marquee stage1."
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "BE: coverage max=80.22% (>60%), possible surestimation must-run."
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "CZ: coverage max=89.16% (>60%), possible surestimation must-run."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%]."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "FLEX_UP",
  "horizon_year": 2035
}
```

#### Narratif (FLEX_UP)
Q1 identifie la bascule Phase 1 -> Phase 2 avec gating explicite: >=2 familles LOW_PRICE/VALUE/PHYSICAL, hors annees de crise configurees, et qualite data uniquement. Les diagnostics NEG_NOT_IN_SURPLUS restent visibles via market_physical_gap_flag mais ne bloquent pas la classification.

#### Table SCEN FLEX_UP `Q1/scen/FLEX_UP/tables/Q1_before_after_bascule.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,bascule_year_market,pre_window_start_year,pre_window_end_year,post_window_start_year,post_window_end_year,n_pre_years,n_post_years,pre_mean_capture_ratio_pv,post_mean_capture_ratio_pv,delta_post_minus_pre_capture_ratio_pv,pre_mean_capture_ratio_wind,post_mean_capture_ratio_wind,delta_post_minus_pre_capture_ratio_wind,pre_mean_h_negative_obs,post_mean_h_negative_obs,delta_post_minus_pre_h_negative_obs,pre_mean_sr_hours_share,post_mean_sr_hours_share,delta_post_minus_pre_sr_hours_share,pre_mean_far_observed,post_mean_far_observed,delta_post_minus_pre_far_observed,pre_mean_ir_p10,post_mean_ir_p10,delta_post_minus_pre_ir_p10
DE,,,,,,0,0,,,,,,,,,,,,,,,,,,
```

##### ES (1 lignes)
```csv
country,bascule_year_market,pre_window_start_year,pre_window_end_year,post_window_start_year,post_window_end_year,n_pre_years,n_post_years,pre_mean_capture_ratio_pv,post_mean_capture_ratio_pv,delta_post_minus_pre_capture_ratio_pv,pre_mean_capture_ratio_wind,post_mean_capture_ratio_wind,delta_post_minus_pre_capture_ratio_wind,pre_mean_h_negative_obs,post_mean_h_negative_obs,delta_post_minus_pre_h_negative_obs,pre_mean_sr_hours_share,post_mean_sr_hours_share,delta_post_minus_pre_sr_hours_share,pre_mean_far_observed,post_mean_far_observed,delta_post_minus_pre_far_observed,pre_mean_ir_p10,post_mean_ir_p10,delta_post_minus_pre_ir_p10
ES,2025,2022,2024,2025,2027,0,3,,0.928681,,,0.972285,,,0,,,0,,,1,,,0.0884361,
```


#### Table SCEN FLEX_UP `Q1/scen/FLEX_UP/tables/Q1_country_summary.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,bascule_year_market,bascule_year_market_country,bascule_year_market_pv,bascule_year_market_wind,bascule_year_physical,bascule_year_market_observed,bascule_year_physical_observed,bascule_status_market,bascule_status_market_pv,bascule_status_market_wind,bascule_status_physical,stage1_bascule_year,stage1_detected,bascule_confidence,families_active_at_bascule_pv,families_active_at_bascule_wind,families_active_at_bascule_country,drivers_at_bascule,low_price_flags_count_at_bascule,physical_flags_count_at_bascule,capture_flags_count_at_bascule,stage2_market_score_at_bascule,score_breakdown_at_bascule,required_demand_uplift_to_avoid_phase2,required_demand_uplift_status,required_flex_uplift_to_avoid_phase2,required_flex_uplift_status,bascule_rationale,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,capture_ratio_pv_at_bascule,capture_ratio_wind_at_bascule,market_physical_gap_at_bascule,neg_price_explained_by_surplus_ratio_at_bascule,h_negative_at_bascule,notes_quality
DE,,,,,2025,,,not_reached_in_window,not_reached_in_window,not_reached_in_window,already_phase2_at_window_start,2025,True,0,PHYSICAL,PHYSICAL,PHYSICAL,nan,0,1,0,1,low=0;value=0;physical=1;crisis=0,0,already_not_phase2,0,already_not_phase2,Pas de bascule persistante sur la fenetre.,0,1,0.0437608,212.658,0.596289,0.964054,0.959969,False,,0,ok
```

##### ES (1 lignes)
```csv
country,bascule_year_market,bascule_year_market_country,bascule_year_market_pv,bascule_year_market_wind,bascule_year_physical,bascule_year_market_observed,bascule_year_physical_observed,bascule_status_market,bascule_status_market_pv,bascule_status_market_wind,bascule_status_physical,stage1_bascule_year,stage1_detected,bascule_confidence,families_active_at_bascule_pv,families_active_at_bascule_wind,families_active_at_bascule_country,drivers_at_bascule,low_price_flags_count_at_bascule,physical_flags_count_at_bascule,capture_flags_count_at_bascule,stage2_market_score_at_bascule,score_breakdown_at_bascule,required_demand_uplift_to_avoid_phase2,required_demand_uplift_status,required_flex_uplift_to_avoid_phase2,required_flex_uplift_status,bascule_rationale,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,capture_ratio_pv_at_bascule,capture_ratio_wind_at_bascule,market_physical_gap_at_bascule,neg_price_explained_by_surplus_ratio_at_bascule,h_negative_at_bascule,notes_quality
ES,2025,2025,2025,2025,2025,2025,,transition_observed,already_phase2_at_window_start,already_phase2_at_window_start,already_phase2_at_window_start,2025,True,1,"LOW_PRICE,PHYSICAL","LOW_PRICE,PHYSICAL","LOW_PRICE,PHYSICAL",nan,0,1,0,2,low=1;value=0;physical=1;crisis=0,0.300049,ok,,beyond_plausible_bounds,Bascule validee: >=2 familles actives (LOW_PRICE/VALUE/PHYSICAL) sur 2 annees consecutives hors crise.,0,1,0.0901141,156.602,0.548109,0.928782,0.972055,False,,0,ok
```


#### Table SCEN FLEX_UP `Q1/scen/FLEX_UP/tables/Q1_ir_diagnostics.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,ir_p10,p10_must_run_mw,p10_load_mw,p50_must_run_mw,p50_load_mw,ir_case_class
DE,2025,0.052171,2208.4,42330,2244.17,54653.7,must_run_floor_effect
DE,2026,0.051187,2208.4,43143.7,2244.17,55698.1,must_run_floor_effect
DE,2027,0.0502394,2208.4,43957.4,2244.17,56741.9,must_run_floor_effect
DE,2028,0.0494294,2207.77,44665.1,2243.2,57629.8,must_run_floor_effect
DE,2029,0.0484458,2208.4,45584.8,2244.17,58831.8,must_run_floor_effect
DE,2030,0.0475974,2208.4,46397.4,2244.17,59876.6,must_run_floor_effect
DE,2031,0.0467776,2208.4,47210.6,2244.17,60919,must_run_floor_effect
DE,2032,0.0460793,2207.77,47912.3,2243.2,61790.9,must_run_floor_effect
DE,2033,0.0452189,2208.4,48837.9,2244.17,63003.4,must_run_floor_effect
DE,2034,0.0444779,2208.4,49651.5,2244.17,64048.2,must_run_floor_effect
DE,2035,0.0437608,2208.4,50465.2,2244.17,65091.4,must_run_floor_effect
```

##### ES (11 lignes)
```csv
country,year,ir_p10,p10_must_run_mw,p10_load_mw,p50_must_run_mw,p50_load_mw,ir_case_class
ES,2025,0.0901141,1907.18,21164,1945.18,26650.1,must_run_floor_effect
ES,2026,0.0884139,1907.18,21571,1945.18,27163,must_run_floor_effect
ES,2027,0.0867805,1907.18,21977,1945.18,27676.5,must_run_floor_effect
ES,2028,0.0854349,1907.1,22322.2,1944.67,28113.4,must_run_floor_effect
ES,2029,0.0836799,1907.18,22791.3,1945.18,28698,must_run_floor_effect
ES,2030,0.0822229,1907.18,23195.2,1945.18,29209.5,must_run_floor_effect
ES,2031,0.0808095,1907.18,23600.9,1945.18,29723.8,must_run_floor_effect
ES,2032,0.0796599,1907.1,23940.5,1944.67,30156.1,must_run_floor_effect
ES,2033,0.0781136,1907.18,24415.4,1945.18,30747.7,must_run_floor_effect
ES,2034,0.0768319,1907.18,24822.7,1945.18,31261,must_run_floor_effect
ES,2035,0.0755906,1907.18,25230.3,1945.18,31775.4,must_run_floor_effect
```


#### Table SCEN FLEX_UP `Q1/scen/FLEX_UP/tables/Q1_residual_diagnostics.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_median_eur_mwh,residual_negative_p10_mw,residual_negative_p50_mw,residual_negative_p90_mw
DE,2025,21186.6,35576.8,50014.8,107.714,,,,
DE,2026,21841.7,36451.7,51129.2,108.733,,,,
DE,2027,22518.7,37330.3,52242.4,109.744,,,,
DE,2028,23061.1,38027.2,53157.8,110.723,,,,
DE,2029,23896.1,39082.1,54400.3,111.758,,,,
DE,2030,24562.2,39978.6,55480.9,112.761,,,,
DE,2031,25171.2,40804.4,56531.5,113.753,,,,
DE,2032,25633.9,41433.1,57387.5,114.717,,,,
DE,2033,26404.3,42426.7,58652.6,115.742,,,,
DE,2034,26986.6,43236.2,59699.3,116.741,,,,
DE,2035,27598,44049.2,60771,117.724,,,,
```

##### ES (11 lignes)
```csv
country,year,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_median_eur_mwh,residual_negative_p10_mw,residual_negative_p50_mw,residual_negative_p90_mw
ES,2025,10136.3,16003.5,23312,82.0837,,,,
ES,2026,10424.3,16389.3,23822.3,82.6704,,,,
ES,2027,10719.6,16769.6,24323.5,83.2588,,,,
ES,2028,10950.6,17104.6,24786.5,83.8219,,,,
ES,2029,11303.3,17542.1,25361.9,84.4447,,,,
ES,2030,11595.7,17932.4,25879.5,85.0377,,,,
ES,2031,11889.2,18315.9,26389.5,85.628,,,,
ES,2032,12123.3,18647.2,26849.9,86.1807,,,,
ES,2033,12493.2,19107.3,27424.1,86.8076,,,,
ES,2034,12778.1,19494.8,27935.5,87.3964,,,,
ES,2035,13072.2,19880,28464.2,87.9954,,,,
```


#### Table SCEN FLEX_UP `Q1/scen/FLEX_UP/tables/Q1_rule_application.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,capture_ratio_pv,capture_ratio_wind,stage2_market_score,score_breakdown,crisis_year,quality_flag,quality_ok,stage2_candidate_year,stage1_candidate_year,phase2_candidate_year,low_price_flags_count,physical_flags_count,capture_flags_count,active_flags,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_low_residual_high,flag_sr_high,flag_far_low,flag_ir_high,flag_spread_high,market_physical_gap_flag,neg_price_explained_by_surplus_ratio,low_price_family,value_family,value_family_pv,value_family_wind,physical_family,family_count_pv,family_count_wind,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,physical_candidate_year,flag_capture_only_stage2,is_stage1_criteria,is_phase2_market,is_phase2_physical,phase_market,stress_phys_state
DE,2025,0.960882,0.958036,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2026,0.961575,0.958198,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2027,0.962399,0.958328,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2028,0.963118,0.958313,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2029,0.963566,0.958603,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2030,0.964434,0.958763,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2031,0.964466,0.958961,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2032,0.964479,0.959066,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2033,0.964273,0.959386,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2034,0.964233,0.959576,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2035,0.964054,0.959969,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
```

##### ES (11 lignes)
```csv
country,year,capture_ratio_pv,capture_ratio_wind,stage2_market_score,score_breakdown,crisis_year,quality_flag,quality_ok,stage2_candidate_year,stage1_candidate_year,phase2_candidate_year,low_price_flags_count,physical_flags_count,capture_flags_count,active_flags,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_low_residual_high,flag_sr_high,flag_far_low,flag_ir_high,flag_spread_high,market_physical_gap_flag,neg_price_explained_by_surplus_ratio,low_price_family,value_family,value_family_pv,value_family_wind,physical_family,family_count_pv,family_count_wind,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,physical_candidate_year,flag_capture_only_stage2,is_stage1_criteria,is_phase2_market,is_phase2_physical,phase_market,stress_phys_state
ES,2025,0.928782,0.972055,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2026,0.928713,0.972317,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2027,0.928548,0.972483,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2028,0.928239,0.972328,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2029,0.928408,0.972955,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2030,0.928176,0.973152,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2031,0.928115,0.973289,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2032,0.927931,0.97311,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2033,0.928018,0.973544,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2034,0.92796,0.973774,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2035,0.927897,0.973928,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
```


#### Table SCEN FLEX_UP `Q1/scen/FLEX_UP/tables/Q1_rule_definition.csv`
Lignes: `1`

```csv
q1_rule_version,h_negative_stage2_min,h_below_5_stage2_min,capture_ratio_pv_stage2_max,capture_ratio_wind_stage2_max,sr_hours_stage2_min,low_residual_hours_stage2_min,far_stage2_min,ir_p10_stage2_min,days_spread_gt50_stage2_min,avg_daily_spread_crisis_min,stage1_capture_ratio_pv_min,stage1_capture_ratio_wind_min,stage1_sr_hours_max,stage1_far_min,stage1_ir_p10_max,persistence_window_years,crisis_years_explicit,rule_logic
q1_rule_v4_2026_02_11,200,500,0.8,0.9,0.1,0.1,0.95,1.5,150,50,0.85,0.9,0.05,0.95,1.5,2,2022,"stage2_candidate_tech=(>=2 familles actives parmi LOW_PRICE/PHYSICAL/VALUE_TECH) avec persistence sur 2 annees non-crise; bascule_country=min(bascule_pv,bascule_wind). stage1_candidate=(familles toutes inactives) hors crise. NEG_NOT_IN_AB reste informatif; RC principal=AB_OR_LOW_RESIDUAL."
```


#### Table SCEN FLEX_UP `Q1/scen/FLEX_UP/tables/Q1_scope_audit.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,must_run_scope_coverage,lowload_p20_mw,ir_p10,scope_status,scope_reason,load_net_mode,must_run_mode_hourly
DE,2025,0.151555,45449,0.052171,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2026,0.150282,46319.1,0.051187,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2027,0.149064,47191.9,0.0502394,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2028,0.147708,47934.6,0.0494294,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2029,0.146804,48931.8,0.0484458,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2030,0.145612,49801.8,0.0475974,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2031,0.144246,50672.1,0.0467776,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2032,0.142747,51408.2,0.0460793,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2033,0.141625,52415.2,0.0452189,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2034,0.140316,53284.4,0.0444779,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2035,0.139031,54153,0.0437608,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
```

##### ES (11 lignes)
```csv
country,year,must_run_scope_coverage,lowload_p20_mw,ir_p10,scope_status,scope_reason,load_net_mode,must_run_mode_hourly
ES,2025,0.171564,22449.7,0.0901141,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2026,0.170466,22880.1,0.0884139,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2027,0.169402,23311.1,0.0867805,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2028,0.168541,23676.6,0.0854349,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2029,0.167244,24172.4,0.0836799,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2030,0.166161,24601.1,0.0822229,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2031,0.165135,25035.4,0.0808095,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2032,0.164273,25396.9,0.0796599,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2033,0.162973,25900.4,0.0781136,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2034,0.162047,26330.8,0.0768319,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2035,0.16107,26763.5,0.0755906,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
```


#### Table SCEN FLEX_UP `Q1/scen/FLEX_UP/tables/Q1_year_panel.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative,h_negative_obs,h_below_5,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,scenario_id,mode,horizon_year,calib_mustrun_scale,calib_vre_scale_pv,calib_vre_scale_wind_on,calib_vre_scale_wind_off,calib_export_cap_eff_gw,calib_export_coincidence_used,calib_flex_realization_factor,calib_price_b_floor,calib_price_b_intercept,calib_price_b_slope_surplus_norm,vre_penetration_share_gen,pv_penetration_share_gen,wind_penetration_share_gen,sr_hours_share,p10_load_mw,p10_must_run_mw,p50_load_mw,p50_must_run_mw,ir_p10_excess,must_run_scope_coverage,core_sanity_issue_count,core_sanity_issues,psh_pumping_twh,psh_pumping_coverage_share,psh_pumping_data_status,flex_sink_exports_twh,flex_sink_psh_twh,flex_sink_total_twh,share_neg_price_hours_in_AB,share_neg_price_hours_in_low_residual,share_neg_price_hours_in_AB_OR_LOW_RESIDUAL,surplus_energy_twh,absorbed_surplus_twh,unabsorbed_surplus_twh,low_residual_hours_share,low_residual_threshold_mw,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_hours_median_eur_mwh,residual_load_p50_on_negative_price_mw,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_sr_high,flag_low_residual_high,flag_far_low,flag_ir_high,flag_spread_high,crisis_year,low_price_family,value_family_pv,value_family_wind,value_family,physical_family,low_price_flags_count,capture_flags_count,physical_flags_count,family_count,family_count_pv,family_count_wind,stage2_points_low_price,stage2_points_capture,stage2_points_physical,stage2_points_vol,stage2_market_score,score_breakdown,quality_ok,neg_price_explained_by_surplus_ratio,market_physical_gap_flag,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,stage2_candidate_year,phase2_candidate_year,flag_capture_only_stage2,is_phase2_market,physical_candidate_year,is_phase2_physical,signal_low_price,signal_value,signal_physical,flag_non_capture_stage2,active_flags,is_stage1_criteria,stage1_candidate_year,phase_market,stress_phys_state
DE,2025,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,1ec94ff0b8dd1b9fb977e5874b300d2d99c5adcba48a978b0e05c37487d0ee35,480.173,478.375,31.6975,93.7283,19.9439,145.37,169.714,19.582,4.81902,85.6559,18.677,66.9788,0.303882,120.267,124.319,118.012,115.563,115.22,0.960882,0.958036,115.563,115.22,0.960882,0.958036,0.591584,0.589832,0,0,0,0,125,125,32.0753,91.7972,0,0,0,0,0,0,1,1,0.052171,0.0409344,195.344,195.344,,none,0,0,7884,876,1,0.671326,1,OK,FLEX_UP,SCEN,2025,9425.89,19.4667,36.463,5.37175,2.4375,0.35,0.9,-43.87,-0.03,-9.36265,0.856559,0.18677,0.669788,0,42330,2208.4,54653.7,2244.17,-0.947829,0.151555,0,,1.79762,1,ok,4.81902,0,0,,,,0,0,0,0.1,21186.6,21186.6,35576.8,50014.8,107.714,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2026,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,30d9d0cfffb41461c713e2583456fc2bd6a90a6419a8ca358dd158c8f0b4584b,489.319,487.521,31.6975,94.7325,20.3065,146.736,171.08,19.582,4.81902,85.7705,18.5278,67.2427,0.300985,121.402,123.175,120.414,116.737,116.327,0.961575,0.958198,116.737,116.327,0.961575,0.958198,0.592284,0.590204,0,0,0,0,125,125,32.3521,92.584,0,0,0,0,0,0,1,1,0.051187,0.0401665,197.096,197.096,,none,0,0,7884,876,1,0.671856,1,OK,FLEX_UP,SCEN,2026,9425.89,19.8053,36.8537,5.46942,2.4375,0.35,0.9,-43.87,-0.03,-9.36265,0.857705,0.185278,0.672427,0,43143.7,2208.4,55698.1,2244.17,-0.948813,0.150282,0,,1.79762,1,ok,4.81902,0,0,,,,0,0,0,0.1,21841.7,21841.7,36451.7,51129.2,108.733,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2027,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,149655d8b730cf5c392db5596d50c50f0a153447a2f4c527e90aaf0d1324d5b8,498.465,496.667,31.6975,95.7368,20.6691,148.103,172.447,19.582,4.81902,85.8832,18.381,67.5023,0.298194,122.536,123.565,121.963,117.928,117.43,0.962399,0.958328,117.928,117.43,0.962399,0.958328,0.593079,0.59057,0,0,0,0,124,124,32.4151,93.3708,0,0,0,0,0,0,1,1,0.0502394,0.0394268,198.841,198.841,,none,0,0,7884,876,1,0.672359,1,OK,FLEX_UP,SCEN,2027,9425.89,20.1438,37.2444,5.56709,2.4375,0.35,0.9,-43.87,-0.03,-9.36265,0.858832,0.18381,0.675023,0,43957.4,2208.4,56741.9,2244.17,-0.949761,0.149064,0,,1.79762,1,ok,4.81902,0,0,,,,0,0,0,0.1,22518.7,22518.7,37330.3,52242.4,109.744,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2028,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,dd0bdc6020003f148e576380082d6469c62b28ea483e1de8282a017ec3eed20c,507.611,505.81,31.722,97.1985,21.088,150.008,174.417,19.6256,4.87409,86.0055,18.1874,67.818,0.296571,123.627,126.125,122.25,119.067,118.473,0.963118,0.958313,119.067,118.473,0.963118,0.958313,0.593937,0.590974,0,0,0,0,124,124,32.592,94.103,0,0,0,0,0,0,1,1,0.0494294,0.0388003,200.471,200.471,,none,0,0,7905,879,1,0.673044,1,OK,FLEX_UP,SCEN,2028,9425.89,20.4824,37.635,5.66476,2.4375,0.35,0.9,-43.87,-0.03,-9.36265,0.860055,0.181874,0.67818,0,44665.1,2207.77,57629.8,2243.2,-0.950571,0.147708,0,,1.80141,1,ok,4.87409,0,0,,,,0,0,0,0.100068,23061.1,23061.1,38027.2,53157.8,110.723,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2029,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,a6ed456c0659333d4c8a74fb331bfac30bf97c9d262bfd395e4e587727f54cf9,516.757,514.96,31.6975,97.7453,21.3943,150.837,175.181,19.582,4.81902,86.1035,18.0941,68.0094,0.29291,124.805,135.499,118.853,120.257,119.638,0.963566,0.958603,120.257,119.638,0.963566,0.958603,0.59444,0.591378,0,0,0,0,124,124,32.9715,94.9443,0,0,0,0,0,0,1,1,0.0484458,0.0380263,202.304,202.304,,none,0,0,7884,876,1,0.673284,1,OK,FLEX_UP,SCEN,2029,9425.89,20.8209,38.0257,5.76243,2.4375,0.35,0.9,-43.87,-0.03,-9.36265,0.861035,0.180941,0.680094,0,45584.8,2208.4,58831.8,2244.17,-0.951554,0.146804,0,,1.79762,1,ok,4.81902,0,0,,,,0,0,0,0.1,23896.1,23896.1,39082.1,54400.3,111.758,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2030,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,11a62b110ac7f949cf2af8f9ebf333ff4f4411db63b99a333467135021478f18,525.903,524.106,31.6975,98.7495,21.757,152.204,176.548,19.582,4.81902,86.2111,17.954,68.2571,0.290407,125.939,133.94,121.487,121.46,120.746,0.964434,0.958763,121.46,120.746,0.964434,0.958763,0.595285,0.591785,0,0,0,0,123,123,33.0376,95.7311,0,0,0,0,0,0,1,1,0.0475974,0.0373627,204.036,204.036,,none,0,0,7884,876,1,0.673708,1,OK,FLEX_UP,SCEN,2030,9425.89,21.1595,38.4164,5.8601,2.4375,0.35,0.9,-43.87,-0.03,-9.36265,0.862111,0.17954,0.682571,0,46397.4,2208.4,59876.6,2244.17,-0.952403,0.145612,0,,1.79762,1,ok,4.81902,0,0,,,,0,0,0,0.1,24562.2,24562.2,39978.6,55480.9,112.761,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2031,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,d5c1487c1aae8958aa566f6bea921c38deb6feac2698a8c8bb79216d1e6fc4d6,535.05,533.252,32.1598,99.7538,22.1196,154.033,178.377,19.582,4.81902,86.3525,18.0291,68.3234,0.288856,127.059,131.561,124.553,122.544,121.845,0.964466,0.958961,122.544,121.845,0.964466,0.958961,0.595566,0.592167,0,0,0,0,123,123,33.3222,96.5178,0,0,0,0,0,0,1,1,0.0467776,0.0367219,205.76,205.76,,none,0,0,7884,876,1,0.674523,1,OK,FLEX_UP,SCEN,2031,9425.89,21.4981,38.8071,5.95777,2.4375,0.35,0.9,-43.87,-0.03,-9.36265,0.863525,0.180291,0.683234,0,47210.6,2208.4,60919,2244.17,-0.953222,0.144246,0,,1.79762,1,ok,4.81902,0,0,,,,0,0,0,0.1,25171.2,25171.2,40804.4,56531.5,113.753,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2032,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,c4583852538ba1afdb7b27c94d2e33a1f56c12e28b0ce7691cd18fdcb122c910,544.196,542.394,32.6953,101.234,22.5423,156.472,180.881,19.6256,4.87409,86.5055,18.0756,68.43,0.288484,128.13,130.226,126.963,123.579,122.886,0.964479,0.959066,123.579,122.886,0.964479,0.959066,0.595915,0.592571,0,0,0,0,123,123,33.4976,97.2461,0,0,0,0,0,0,1,1,0.0460793,0.0361832,207.377,207.377,,none,0,0,7905,879,1,0.675554,1,OK,FLEX_UP,SCEN,2032,9425.89,21.8366,39.1978,6.05544,2.4375,0.35,0.9,-43.87,-0.03,-9.36265,0.865055,0.180756,0.6843,0,47912.3,2207.77,61790.9,2243.2,-0.953921,0.142747,0,,1.80141,1,ok,4.87409,0,0,,,,0,0,0,0.100068,25633.9,25633.9,41433.1,57387.5,114.717,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2033,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,982651f24b2a65050f6bacfcb29af682a309502173ab5b29e8cee91072102729,553.342,551.544,33.1728,101.762,22.8448,157.78,182.124,19.582,4.81902,86.6333,18.2144,68.4189,0.286069,129.296,131.998,127.802,124.677,124.045,0.964273,0.959386,124.677,124.045,0.964273,0.959386,0.595958,0.592938,0,0,0,0,123,123,33.8875,98.0913,0,0,0,0,0,0,1,1,0.0452189,0.035504,209.204,209.204,,none,0,0,7884,876,1,0.67616,1,OK,FLEX_UP,SCEN,2033,9425.89,22.1752,39.5884,6.15311,2.4375,0.35,0.9,-43.87,-0.03,-9.36265,0.866333,0.182144,0.684189,0,48837.9,2208.4,63003.4,2244.17,-0.954781,0.141625,0,,1.79762,1,ok,4.81902,0,0,,,,0,0,0,0.1,26404.3,26404.3,42426.7,58652.6,115.742,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2034,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,e767573357aced854daf94537f970b6980c5731dfaeb2f8b128f489a4085505e,562.488,560.69,33.6792,102.766,23.2075,159.653,183.997,19.582,4.81902,86.7694,18.3042,68.4652,0.284744,130.415,138.099,126.164,125.75,125.143,0.964233,0.959576,125.75,125.143,0.964233,0.959576,0.596183,0.593304,0,0,0,0,123,123,34.1727,98.878,0,0,0,0,0,0,1,1,0.0444779,0.0349248,210.926,210.926,,none,0,0,7884,876,1,0.676947,1,OK,FLEX_UP,SCEN,2034,9425.89,22.5137,39.9791,6.25078,2.4375,0.35,0.9,-43.87,-0.03,-9.36265,0.867694,0.183042,0.684652,0,49651.5,2208.4,64048.2,2244.17,-0.955522,0.140316,0,,1.79762,1,ok,4.81902,0,0,,,,0,0,0,0.1,26986.6,26986.6,43236.2,59699.3,116.741,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2035,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,a607c90d533467bd8f9b94b3cf15f1a7677248fb93c7dd99bb1b90259cb4517e,571.634,569.836,34.1857,103.771,23.5701,161.527,185.87,19.582,4.81902,86.9027,18.3922,68.5105,0.283461,131.534,143.011,125.146,126.806,126.268,0.964054,0.959969,126.806,126.268,0.964054,0.959969,0.596289,0.593762,0,0,0,0,122,122,34.2321,99.6647,0,0,0,0,0,0,1,1,0.0437608,0.0343643,212.658,212.658,,none,0,0,7884,876,1,0.677713,1,OK,FLEX_UP,SCEN,2035,9425.89,22.8523,40.3698,6.34845,2.4375,0.35,0.9,-43.87,-0.03,-9.36265,0.869027,0.183922,0.685105,0,50465.2,2208.4,65091.4,2244.17,-0.956239,0.139031,0,,1.79762,1,ok,4.81902,0,0,,,,0,0,0,0.1,27598,27598,44049.2,60771,117.724,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
```

##### ES (11 lignes)
```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative,h_negative_obs,h_below_5,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,scenario_id,mode,horizon_year,calib_mustrun_scale,calib_vre_scale_pv,calib_vre_scale_wind_on,calib_vre_scale_wind_off,calib_export_cap_eff_gw,calib_export_coincidence_used,calib_flex_realization_factor,calib_price_b_floor,calib_price_b_intercept,calib_price_b_slope_surplus_norm,vre_penetration_share_gen,pv_penetration_share_gen,wind_penetration_share_gen,sr_hours_share,p10_load_mw,p10_must_run_mw,p50_load_mw,p50_must_run_mw,ir_p10_excess,must_run_scope_coverage,core_sanity_issue_count,core_sanity_issues,psh_pumping_twh,psh_pumping_coverage_share,psh_pumping_data_status,flex_sink_exports_twh,flex_sink_psh_twh,flex_sink_total_twh,share_neg_price_hours_in_AB,share_neg_price_hours_in_low_residual,share_neg_price_hours_in_AB_OR_LOW_RESIDUAL,surplus_energy_twh,absorbed_surplus_twh,unabsorbed_surplus_twh,low_residual_hours_share,low_residual_threshold_mw,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_hours_median_eur_mwh,residual_load_p50_on_negative_price_mw,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_sr_high,flag_low_residual_high,flag_far_low,flag_ir_high,flag_spread_high,crisis_year,low_price_family,value_family_pv,value_family_wind,value_family,physical_family,low_price_flags_count,capture_flags_count,physical_flags_count,family_count,family_count_pv,family_count_wind,stage2_points_low_price,stage2_points_capture,stage2_points_physical,stage2_points_vol,stage2_market_score,score_breakdown,quality_ok,neg_price_explained_by_surplus_ratio,market_physical_gap_flag,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,stage2_candidate_year,phase2_candidate_year,flag_capture_only_stage2,is_phase2_market,physical_candidate_year,is_phase2_physical,signal_low_price,signal_value,signal_physical,flag_non_capture_stage2,active_flags,is_stage1_criteria,stage1_candidate_year,phase_market,stress_phys_state
ES,2025,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,a8f775a18eb0ffa2f81e4cdb96c5d5a7983ab9dcc2092a96033637778134014e,234.28,232.643,28.6131,43.9453,0,72.5584,115.734,16.8792,8.71766,62.694,24.7231,37.9709,0.311887,92.4164,89.546,94.0137,85.8346,89.8338,0.928782,0.972055,85.8346,89.8338,0.928782,0.972055,0.548109,0.573646,0,0,0,0,191,191,40.7989,80.5324,0,0,0,0,0,0,1,1,0.0901141,0.0725538,156.602,156.602,,none,0,0,7884,876,1,0.708402,1,OK,FLEX_UP,SCEN,2025,6237.2,12.5165,13.3741,1.9703,2.4375,0.35,0.899462,-0.36,3.32,-12.5665,0.62694,0.247231,0.379709,0,21164,1907.18,26650.1,1945.18,-0.909886,0.171564,0,,1.63696,1,ok,8.71766,0,0,,,,0,0,0,0.1,10136.3,10136.3,16003.5,23312,82.0837,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2026,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,01350eb1da34a82fb3b6e8bbee75f16080f84a6a701ac2fa35031cec6304dbb4,238.743,237.106,29.1108,44.4161,0,73.5269,116.703,16.8792,8.71766,63.0036,24.9444,38.0592,0.310102,93.1086,89.8798,94.9055,86.4712,90.5311,0.928713,0.972317,86.4712,90.5311,0.928713,0.972317,0.548199,0.573937,0,0,0,0,191,191,41.113,81.1625,0,0,0,0,0,0,1,1,0.0884139,0.0711883,157.737,157.737,,none,0,0,7884,876,1,0.70917,1,OK,FLEX_UP,SCEN,2026,6237.2,12.7342,13.5173,2.00612,2.4375,0.35,0.899462,-0.36,3.32,-12.5665,0.630036,0.249444,0.380592,0,21571,1907.18,27163,1945.18,-0.911586,0.170466,0,,1.63696,1,ok,8.71766,0,0,,,,0,0,0,0.1,10424.3,10424.3,16389.3,23822.3,82.6704,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2027,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,2066ecad1279b2426107f6ee2fcd2ceaf734c3285e72c95d0420b6d634cf4939,243.205,241.568,29.6084,44.887,0,74.4953,117.671,16.8792,8.71766,63.308,25.162,38.1461,0.308382,93.8009,90.3355,95.7295,87.0987,91.2199,0.928548,0.972483,87.0987,91.2199,0.928548,0.972483,0.548298,0.574241,0,0,0,0,192,192,41.6086,81.7927,0,0,0,0,0,0,1,1,0.0867805,0.0698733,158.853,158.853,,none,0,0,7884,876,1,0.709922,1,OK,FLEX_UP,SCEN,2027,6237.2,12.9519,13.6606,2.04194,2.4375,0.35,0.899462,-0.36,3.32,-12.5665,0.63308,0.25162,0.381461,0,21977,1907.18,27676.5,1945.18,-0.91322,0.169402,0,,1.63696,1,ok,8.71766,0,0,,,,0,0,0,0.1,10719.6,10719.6,16769.6,24323.5,83.2588,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2028,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,38ba972ec8791c0374d34e2c7d8f0cf353504ae215a8f32904b8d37f86a533af,247.668,246.029,30.1557,45.3917,0,75.5474,118.831,16.9195,8.721,63.5754,25.3769,38.1985,0.307067,94.4643,91.1873,96.2693,87.6855,91.8502,0.928239,0.972328,87.6855,91.8502,0.928239,0.972328,0.548366,0.574412,0,0,0,0,193,193,41.9871,82.3589,0,0,0,0,0,0,1,1,0.0854349,0.0687702,159.903,159.903,,none,0,0,7905,879,1,0.710283,1,OK,FLEX_UP,SCEN,2028,6237.2,13.1695,13.8039,2.07776,2.4375,0.35,0.899462,-0.36,3.32,-12.5665,0.635754,0.253769,0.381985,0,22322.2,1907.1,28113.4,1944.67,-0.914565,0.168541,0,,1.63864,1,ok,8.721,0,0,,,,0,0,0,0.100068,10950.6,10950.6,17104.6,24786.5,83.8219,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2029,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,be54e7317a2f963b27816003698126d0b0962bdbce509165c0fa4a02c914eba2,252.13,250.493,30.6036,45.8286,0,76.4323,119.608,16.8792,8.71766,63.9022,25.5866,38.3157,0.305127,95.1855,95.4253,95.0521,88.371,92.6112,0.928408,0.972955,88.371,92.6112,0.928408,0.972955,0.548624,0.574948,0,0,0,0,194,194,42.6072,83.0529,0,0,0,0,0,0,1,1,0.0836799,0.0673837,161.077,161.077,,none,0,0,7884,876,1,0.711375,1,OK,FLEX_UP,SCEN,2029,6237.2,13.3872,13.9472,2.11358,2.4375,0.35,0.899462,-0.36,3.32,-12.5665,0.639022,0.255866,0.383157,0,22791.3,1907.18,28698,1945.18,-0.91632,0.167244,0,,1.63696,1,ok,8.71766,0,0,,,,0,0,0,0.1,11303.3,11303.3,17542.1,25361.9,84.4447,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2030,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,c774b8a10d7b7368d2155a19f518367385fe0c8b4c9926c73d020b33ea5a1c03,256.593,254.956,31.1012,46.2995,0,77.4007,120.577,16.8792,8.71766,64.1922,25.7938,38.3984,0.303585,95.8778,94.5578,96.6125,88.9915,93.3037,0.928176,0.973152,88.9915,93.3037,0.928176,0.973152,0.548679,0.575266,0,0,0,0,193,193,42.7387,83.683,0,0,0,0,0,0,1,1,0.0822229,0.0662043,162.192,162.192,,none,0,0,7884,876,1,0.712083,1,OK,FLEX_UP,SCEN,2030,6237.2,13.6049,14.0905,2.1494,2.4375,0.35,0.899462,-0.36,3.32,-12.5665,0.641922,0.257938,0.383984,0,23195.2,1907.18,29209.5,1945.18,-0.917777,0.166161,0,,1.63696,1,ok,8.71766,0,0,,,,0,0,0,0.1,11595.7,11595.7,17932.4,25879.5,85.0377,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2031,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,e948d9fce34b3210aa8848f170dfe0aa3bd6b09d17cc6ba246f6ec607e8b3904,261.055,259.418,31.5989,46.7703,0,78.3692,121.545,16.8792,8.71766,64.4775,25.9977,38.4798,0.302096,96.5701,93.4945,98.2817,89.6282,93.9906,0.928115,0.973289,89.6282,93.9906,0.928115,0.973289,0.548857,0.575571,0,0,0,0,193,193,43.0554,84.3131,0,0,0,0,0,0,1,1,0.0808095,0.0650655,163.3,163.3,,none,0,0,7884,876,1,0.712776,1,OK,FLEX_UP,SCEN,2031,6237.2,13.8226,14.2338,2.18522,2.4375,0.35,0.899462,-0.36,3.32,-12.5665,0.644775,0.259977,0.384798,0,23600.9,1907.18,29723.8,1945.18,-0.919191,0.165135,0,,1.63696,1,ok,8.71766,0,0,,,,0,0,0,0.1,11889.2,11889.2,18315.9,26389.5,85.628,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2032,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,17d9ff2a1343d67730b86ecbf9040edf290813df9c70a7203a932ba3c2f7b795,265.518,263.879,32.1495,47.2764,0,79.4259,122.71,16.9195,8.721,64.7267,26.1996,38.527,0.300994,97.2309,93.7642,99.1635,90.2236,94.6164,0.927931,0.97311,90.2236,94.6164,0.927931,0.97311,0.548953,0.57568,0,0,0,0,194,194,43.4335,84.8747,0,0,0,0,0,0,1,1,0.0796599,0.0641182,164.356,164.356,,none,0,0,7905,879,1,0.713073,1,OK,FLEX_UP,SCEN,2032,6237.2,14.0403,14.3771,2.22104,2.4375,0.35,0.899462,-0.36,3.32,-12.5665,0.647267,0.261996,0.38527,0,23940.5,1907.1,30156.1,1944.67,-0.92034,0.164273,0,,1.63864,1,ok,8.721,0,0,,,,0,0,0,0.100068,12123.3,12123.3,18647.2,26849.9,86.1807,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2033,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,3e681df6657155dc9ce4706f214f97b0f93a83db22800b779a8889f76d66ee66,269.98,268.343,32.5941,47.712,0,80.3061,123.482,16.8792,8.71766,65.0347,26.3959,38.6388,0.299266,97.9548,94.5238,99.8527,90.9038,95.3633,0.928018,0.973544,90.9038,95.3633,0.928018,0.973544,0.549191,0.576133,0,0,0,0,195,195,44.0647,85.5734,0,0,0,0,0,0,1,1,0.0781136,0.0629014,165.523,165.523,,none,0,0,7884,876,1,0.714115,1,OK,FLEX_UP,SCEN,2033,6237.2,14.2579,14.5204,2.25686,2.4375,0.35,0.899462,-0.36,3.32,-12.5665,0.650347,0.263959,0.386388,0,24415.4,1907.18,30747.7,1945.18,-0.921886,0.162973,0,,1.63696,1,ok,8.71766,0,0,,,,0,0,0,0.1,12493.2,12493.2,19107.3,27424.1,86.8076,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2034,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,706d16cdf216d0b396f5d3e58b5beb38660891b065ce0806b63345f8fec4a520,274.443,272.806,33.0917,48.1828,0,81.2745,124.45,16.8792,8.71766,65.3068,26.5903,38.7165,0.297921,98.6471,97.4129,99.3298,91.5405,96.0599,0.92796,0.973774,91.5405,96.0599,0.92796,0.973774,0.549322,0.576442,0,0,0,0,195,195,44.3833,86.2035,0,0,0,0,0,0,1,1,0.0768319,0.0618725,166.643,166.643,,none,0,0,7884,876,1,0.714767,1,OK,FLEX_UP,SCEN,2034,6237.2,14.4756,14.6637,2.29268,2.4375,0.35,0.899462,-0.36,3.32,-12.5665,0.653068,0.265903,0.387165,0,24822.7,1907.18,31261,1945.18,-0.923168,0.162047,0,,1.63696,1,ok,8.71766,0,0,,,,0,0,0,0.1,12778.1,12778.1,19494.8,27935.5,87.3964,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2035,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:FLEX_UP,68a57efc482be932f0a24550ea6d0193592836a4b23d9a6645bfe95de2abd7ff,278.905,277.268,33.5894,48.6536,0,82.243,125.419,16.8792,8.71766,65.5747,26.7818,38.7929,0.296619,99.3394,99.5556,99.2191,92.1767,96.7495,0.927897,0.973928,92.1767,96.7495,0.927897,0.973928,0.549445,0.576703,0,0,0,0,196,196,44.8916,86.8336,0,0,0,0,0,0,1,1,0.0755906,0.0608767,167.763,167.763,,none,0,0,7884,876,1,0.715407,1,OK,FLEX_UP,SCEN,2035,6237.2,14.6933,14.807,2.3285,2.4375,0.35,0.899462,-0.36,3.32,-12.5665,0.655747,0.267818,0.387929,0,25230.3,1907.18,31775.4,1945.18,-0.924409,0.16107,0,,1.63696,1,ok,8.71766,0,0,,,,0,0,0,0.1,13072.2,13072.2,19880,28464.2,87.9954,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
```


#### Scenario `LOW_RIGIDITY`

#### Summary (LOW_RIGIDITY)
```json
{
  "module_id": "Q1",
  "run_id": "FULL_20260211_191955_LOW_RIGIDITY",
  "selection": {
    "countries": [
      "FR",
      "DE",
      "ES",
      "NL",
      "BE",
      "CZ",
      "IT_NORD"
    ],
    "years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "scenario_ids": [
      "BASE",
      "DEMAND_UP",
      "FLEX_UP",
      "LOW_RIGIDITY"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955",
    "mode": "SCEN",
    "scenario_id": "LOW_RIGIDITY",
    "horizon_year": 2035
  },
  "assumptions_used": [
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "capture_ratio_pv_stage2_max",
      "param_value": 0.8,
      "unit": "ratio",
      "description": "Seuil capture ratio PV vs baseload en declenchement phase2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "capture_ratio_wind_stage2_max",
      "param_value": 0.9,
      "unit": "ratio",
      "description": "Seuil capture ratio Wind vs baseload en declenchement phase2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "days_spread_gt50_stage2_min",
      "param_value": 150.0,
      "unit": "days",
      "description": "Seuil jours spread>50",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "avg_daily_spread_crisis_min",
      "param_value": 50.0,
      "unit": "EUR/MWh",
      "description": "Seuil spread journalier moyen pour tagger une annee de crise",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "h_below_5_stage2_min",
      "param_value": 500.0,
      "unit": "hours",
      "description": "Seuil heures basses",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "h_negative_stage2_min",
      "param_value": 200.0,
      "unit": "hours",
      "description": "Seuil heures negatives stage2",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_capture_ratio_pv_min",
      "param_value": 0.85,
      "unit": "ratio",
      "description": "Stage1 min capture ratio PV vs baseload",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_capture_ratio_wind_min",
      "param_value": 0.9,
      "unit": "ratio",
      "description": "Stage1 min capture ratio Wind vs baseload",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_h_below_5_max",
      "param_value": 500.0,
      "unit": "hours",
      "description": "Stage1 max hours below 5 (doit rester sous seuil stage2)",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_h_negative_max",
      "param_value": 200.0,
      "unit": "hours",
      "description": "Stage1 max negative hours (doit rester sous seuil stage2)",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHYSICS_THRESHOLDS",
      "param_name": "far_stage2_min",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Seuil FAR minimal pour eviter stress physique stage2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHYSICS_THRESHOLDS",
      "param_name": "ir_p10_stage2_min",
      "param_value": 1.5,
      "unit": "ratio",
      "description": "Alias seuil inflexibilite haute stage2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHYSICS_THRESHOLDS",
      "param_name": "sr_hours_stage2_min",
      "param_value": 0.1,
      "unit": "share",
      "description": "Seuil part d'heures de surplus pour stress physique stage2",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_sr_hours_max",
      "param_value": 0.05,
      "unit": "share",
      "description": "Stage1 max part d'heures de surplus",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_far_min",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Stage1 min FAR",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "stage1_ir_p10_max",
      "param_value": 1.5,
      "unit": "ratio",
      "description": "Stage1 max IR P10",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "QUALITY",
      "param_name": "regime_coherence_min_for_causality",
      "param_value": 0.55,
      "unit": "ratio",
      "description": "Seuil coherence minimale causalite",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "q1_persistence_window_years",
      "param_value": 2.0,
      "unit": "years",
      "description": "Q1: nombre d'annees consecutives requises pour valider une bascule",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    },
    {
      "param_group": "PHASE_THRESHOLDS",
      "param_name": "q1_lever_max_uplift",
      "param_value": 1.0,
      "unit": "ratio",
      "description": "Q1: borne max d'uplift pour solveurs required_demand/flex",
      "source": "spec_alignment",
      "last_updated": "2026-02-11",
      "owner": "codex"
    }
  ],
  "kpis": {
    "n_countries": 7,
    "n_bascule_market": 1,
    "n_bascule_physical": 7,
    "n_scope_rows": 77
  },
  "checks": [
    {
      "status": "FAIL",
      "code": "Q1_STAGE1_HEALTHY_NOT_TAGGED",
      "message": "BE 2030: annee saine non marquee stage1."
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "BE: coverage max=75.59% (>60%), possible surestimation must-run."
    },
    {
      "status": "WARN",
      "code": "Q1_MUSTRUN_SCOPE_HIGH_COVERAGE",
      "message": "CZ: coverage max=68.01% (>60%), possible surestimation must-run."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=68.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=67.9% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=67.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=67.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=67.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=67.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=67.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=67.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=67.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=67.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=66.9% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=62.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=62.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=62.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=62.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=62.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=62.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=62.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=62.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=62.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=62.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=62.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.6% hors plage plausible [5%,60%]."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "LOW_RIGIDITY",
  "horizon_year": 2035
}
```

#### Narratif (LOW_RIGIDITY)
Q1 identifie la bascule Phase 1 -> Phase 2 avec gating explicite: >=2 familles LOW_PRICE/VALUE/PHYSICAL, hors annees de crise configurees, et qualite data uniquement. Les diagnostics NEG_NOT_IN_SURPLUS restent visibles via market_physical_gap_flag mais ne bloquent pas la classification.

#### Table SCEN LOW_RIGIDITY `Q1/scen/LOW_RIGIDITY/tables/Q1_before_after_bascule.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,bascule_year_market,pre_window_start_year,pre_window_end_year,post_window_start_year,post_window_end_year,n_pre_years,n_post_years,pre_mean_capture_ratio_pv,post_mean_capture_ratio_pv,delta_post_minus_pre_capture_ratio_pv,pre_mean_capture_ratio_wind,post_mean_capture_ratio_wind,delta_post_minus_pre_capture_ratio_wind,pre_mean_h_negative_obs,post_mean_h_negative_obs,delta_post_minus_pre_h_negative_obs,pre_mean_sr_hours_share,post_mean_sr_hours_share,delta_post_minus_pre_sr_hours_share,pre_mean_far_observed,post_mean_far_observed,delta_post_minus_pre_far_observed,pre_mean_ir_p10,post_mean_ir_p10,delta_post_minus_pre_ir_p10
DE,,,,,,0,0,,,,,,,,,,,,,,,,,,
```

##### ES (1 lignes)
```csv
country,bascule_year_market,pre_window_start_year,pre_window_end_year,post_window_start_year,post_window_end_year,n_pre_years,n_post_years,pre_mean_capture_ratio_pv,post_mean_capture_ratio_pv,delta_post_minus_pre_capture_ratio_pv,pre_mean_capture_ratio_wind,post_mean_capture_ratio_wind,delta_post_minus_pre_capture_ratio_wind,pre_mean_h_negative_obs,post_mean_h_negative_obs,delta_post_minus_pre_h_negative_obs,pre_mean_sr_hours_share,post_mean_sr_hours_share,delta_post_minus_pre_sr_hours_share,pre_mean_far_observed,post_mean_far_observed,delta_post_minus_pre_far_observed,pre_mean_ir_p10,post_mean_ir_p10,delta_post_minus_pre_ir_p10
ES,2025,2022,2024,2025,2027,0,3,,0.928905,,,0.97231,,,0,,,0,,,1,,,0.0674564,
```


#### Table SCEN LOW_RIGIDITY `Q1/scen/LOW_RIGIDITY/tables/Q1_country_summary.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,bascule_year_market,bascule_year_market_country,bascule_year_market_pv,bascule_year_market_wind,bascule_year_physical,bascule_year_market_observed,bascule_year_physical_observed,bascule_status_market,bascule_status_market_pv,bascule_status_market_wind,bascule_status_physical,stage1_bascule_year,stage1_detected,bascule_confidence,families_active_at_bascule_pv,families_active_at_bascule_wind,families_active_at_bascule_country,drivers_at_bascule,low_price_flags_count_at_bascule,physical_flags_count_at_bascule,capture_flags_count_at_bascule,stage2_market_score_at_bascule,score_breakdown_at_bascule,required_demand_uplift_to_avoid_phase2,required_demand_uplift_status,required_flex_uplift_to_avoid_phase2,required_flex_uplift_status,bascule_rationale,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,capture_ratio_pv_at_bascule,capture_ratio_wind_at_bascule,market_physical_gap_at_bascule,neg_price_explained_by_surplus_ratio_at_bascule,h_negative_at_bascule,notes_quality
DE,,,,,2025,,,not_reached_in_window,not_reached_in_window,not_reached_in_window,already_phase2_at_window_start,2025,True,0,PHYSICAL,PHYSICAL,PHYSICAL,,0,1,0,1,low=0;value=0;physical=1;crisis=0,0,already_not_phase2,0,already_not_phase2,Pas de bascule persistante sur la fenetre.,0,1,0.0333745,212.907,0.596345,0.964109,0.959982,False,,0,ok
```

##### ES (1 lignes)
```csv
country,bascule_year_market,bascule_year_market_country,bascule_year_market_pv,bascule_year_market_wind,bascule_year_physical,bascule_year_market_observed,bascule_year_physical_observed,bascule_status_market,bascule_status_market_pv,bascule_status_market_wind,bascule_status_physical,stage1_bascule_year,stage1_detected,bascule_confidence,families_active_at_bascule_pv,families_active_at_bascule_wind,families_active_at_bascule_country,drivers_at_bascule,low_price_flags_count_at_bascule,physical_flags_count_at_bascule,capture_flags_count_at_bascule,stage2_market_score_at_bascule,score_breakdown_at_bascule,required_demand_uplift_to_avoid_phase2,required_demand_uplift_status,required_flex_uplift_to_avoid_phase2,required_flex_uplift_status,bascule_rationale,sr_energy_at_bascule,far_energy_at_bascule,ir_p10_at_bascule,ttl_at_bascule,capture_ratio_pv_vs_ttl_at_bascule,capture_ratio_pv_at_bascule,capture_ratio_wind_at_bascule,market_physical_gap_at_bascule,neg_price_explained_by_surplus_ratio_at_bascule,h_negative_at_bascule,notes_quality
ES,2025,2025,2025,2025,2025,2025,,transition_observed,already_phase2_at_window_start,already_phase2_at_window_start,already_phase2_at_window_start,2025,True,1,"LOW_PRICE,PHYSICAL","LOW_PRICE,PHYSICAL","LOW_PRICE,PHYSICAL",,0,1,0,2,low=1;value=0;physical=1;crisis=0,0.300049,ok,,beyond_plausible_bounds,Bascule validee: >=2 familles actives (LOW_PRICE/VALUE/PHYSICAL) sur 2 annees consecutives hors crise.,0,1,0.0687296,157,0.548413,0.929074,0.972076,False,,0,ok
```


#### Table SCEN LOW_RIGIDITY `Q1/scen/LOW_RIGIDITY/tables/Q1_ir_diagnostics.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,ir_p10,p10_must_run_mw,p10_load_mw,p50_must_run_mw,p50_load_mw,ir_case_class
DE,2025,0.0397734,1686.41,42400.5,1713.73,54677.6,must_run_floor_effect
DE,2026,0.0390248,1686.41,43213.8,1713.73,55722,must_run_floor_effect
DE,2027,0.0383039,1686.41,44027.2,1713.73,56763.8,must_run_floor_effect
DE,2028,0.0376917,1685.93,44729.6,1712.99,57648.6,must_run_floor_effect
DE,2029,0.03694,1686.41,45652.8,1713.73,58847.4,must_run_floor_effect
DE,2030,0.0362934,1686.41,46466.1,1713.73,59889.6,must_run_floor_effect
DE,2031,0.0356691,1686.41,47279.4,1713.73,60932.4,must_run_floor_effect
DE,2032,0.0351446,1685.93,47971.3,1712.99,61807,must_run_floor_effect
DE,2033,0.0344827,1686.41,48906,1713.73,63018,must_run_floor_effect
DE,2034,0.0339186,1686.41,49719.4,1713.73,64060.9,must_run_floor_effect
DE,2035,0.0333745,1686.41,50530,1713.73,65104.8,must_run_floor_effect
```

##### ES (11 lignes)
```csv
country,year,ir_p10,p10_must_run_mw,p10_load_mw,p50_must_run_mw,p50_load_mw,ir_case_class
ES,2025,0.0687296,1456.39,21190.1,1485.41,26705,must_run_floor_effect
ES,2026,0.0674411,1456.39,21595,1485.41,27219.4,must_run_floor_effect
ES,2027,0.0661984,1456.39,22000.4,1485.41,27732.4,must_run_floor_effect
ES,2028,0.0651768,1456.33,22344.3,1485.02,28171,must_run_floor_effect
ES,2029,0.0638385,1456.39,22813.7,1485.41,28755.7,must_run_floor_effect
ES,2030,0.0627179,1456.39,23221.3,1485.41,29267,must_run_floor_effect
ES,2031,0.061639,1456.39,23627.7,1485.41,29778.3,must_run_floor_effect
ES,2032,0.060761,1456.33,23968.1,1485.02,30210,must_run_floor_effect
ES,2033,0.0595785,1456.39,24444.9,1485.41,30801.7,must_run_floor_effect
ES,2034,0.0586072,1456.39,24850,1485.41,31315.5,must_run_floor_effect
ES,2035,0.0576593,1456.39,25258.5,1485.41,31829.5,must_run_floor_effect
```


#### Table SCEN LOW_RIGIDITY `Q1/scen/LOW_RIGIDITY/tables/Q1_residual_diagnostics.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_median_eur_mwh,residual_negative_p10_mw,residual_negative_p50_mw,residual_negative_p90_mw
DE,2025,21773.8,36135.1,50545.3,107.87,,,,
DE,2026,22451.3,37009.2,51663.6,108.892,,,,
DE,2027,23119,37887.4,52787,109.9,,,,
DE,2028,23652.1,38588.8,53678.7,110.88,,,,
DE,2029,24487.6,39647.3,54930.8,111.913,,,,
DE,2030,25150.4,40566.8,56011.4,112.923,,,,
DE,2031,25770,41372.8,57073,113.914,,,,
DE,2032,26208.4,41998.3,57913.5,114.876,,,,
DE,2033,26987.3,43003.9,59186,115.898,,,,
DE,2034,27602.1,43814.6,60229.7,116.897,,,,
DE,2035,28185.1,44622.4,61301.5,117.885,,,,
```

##### ES (11 lignes)
```csv
country,year,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_median_eur_mwh,residual_negative_p10_mw,residual_negative_p50_mw,residual_negative_p90_mw
ES,2025,10671.6,16480.3,23756.8,82.3528,,,,
ES,2026,10959.7,16868,24281.2,82.9388,,,,
ES,2027,11260.3,17250.9,24782.7,83.5246,,,,
ES,2028,11482.7,17587.4,25246.1,84.0865,,,,
ES,2029,11840.7,18022.4,25819.9,84.713,,,,
ES,2030,12135.3,18408.5,26339.2,85.3074,,,,
ES,2031,12429.4,18802.2,26849.2,85.8947,,,,
ES,2032,12659.2,19133.5,27308.9,86.45,,,,
ES,2033,13028.7,19584.1,27883.7,87.0745,,,,
ES,2034,13319.5,19972.4,28395.2,87.6644,,,,
ES,2035,13613,20360.9,28923.1,88.2599,,,,
```


#### Table SCEN LOW_RIGIDITY `Q1/scen/LOW_RIGIDITY/tables/Q1_rule_application.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,capture_ratio_pv,capture_ratio_wind,stage2_market_score,score_breakdown,crisis_year,quality_flag,quality_ok,stage2_candidate_year,stage1_candidate_year,phase2_candidate_year,low_price_flags_count,physical_flags_count,capture_flags_count,active_flags,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_low_residual_high,flag_sr_high,flag_far_low,flag_ir_high,flag_spread_high,market_physical_gap_flag,neg_price_explained_by_surplus_ratio,low_price_family,value_family,value_family_pv,value_family_wind,physical_family,family_count_pv,family_count_wind,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,physical_candidate_year,flag_capture_only_stage2,is_stage1_criteria,is_phase2_market,is_phase2_physical,phase_market,stress_phys_state
DE,2025,0.960943,0.958051,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2026,0.961665,0.958248,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2027,0.96286,0.958238,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2028,0.963233,0.958347,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2029,0.963624,0.958617,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2030,0.964491,0.958778,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2031,0.96442,0.958971,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2032,0.964535,0.959088,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2033,0.964272,0.959401,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2034,0.964288,0.95959,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
DE,2035,0.964109,0.959982,1,low=0;value=0;physical=1;crisis=0,False,OK,True,False,True,False,0,1,0,"physical_family,flag_low_residual_high",False,False,False,False,False,True,False,False,False,False,False,,False,False,False,False,True,1,1,False,False,False,True,False,True,False,True,phase1,pas_de_surplus_structurel
```

##### ES (11 lignes)
```csv
country,year,capture_ratio_pv,capture_ratio_wind,stage2_market_score,score_breakdown,crisis_year,quality_flag,quality_ok,stage2_candidate_year,stage1_candidate_year,phase2_candidate_year,low_price_flags_count,physical_flags_count,capture_flags_count,active_flags,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_low_residual_high,flag_sr_high,flag_far_low,flag_ir_high,flag_spread_high,market_physical_gap_flag,neg_price_explained_by_surplus_ratio,low_price_family,value_family,value_family_pv,value_family_wind,physical_family,family_count_pv,family_count_wind,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,physical_candidate_year,flag_capture_only_stage2,is_stage1_criteria,is_phase2_market,is_phase2_physical,phase_market,stress_phys_state
ES,2025,0.929074,0.972076,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2026,0.928918,0.972349,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2027,0.928723,0.972505,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2028,0.928442,0.97236,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2029,0.928588,0.973005,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2030,0.928375,0.973182,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2031,0.928313,0.973319,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2032,0.928129,0.973141,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2033,0.928214,0.973574,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2034,0.928155,0.973803,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
ES,2035,0.92809,0.973957,2,low=1;value=0;physical=1;crisis=0,False,OK,True,True,True,True,0,1,0,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",False,False,False,False,False,True,False,False,False,True,False,,True,False,False,False,True,2,2,True,True,True,True,False,True,True,True,phase2,pas_de_surplus_structurel
```


#### Table SCEN LOW_RIGIDITY `Q1/scen/LOW_RIGIDITY/tables/Q1_rule_definition.csv`
Lignes: `1`

```csv
q1_rule_version,h_negative_stage2_min,h_below_5_stage2_min,capture_ratio_pv_stage2_max,capture_ratio_wind_stage2_max,sr_hours_stage2_min,low_residual_hours_stage2_min,far_stage2_min,ir_p10_stage2_min,days_spread_gt50_stage2_min,avg_daily_spread_crisis_min,stage1_capture_ratio_pv_min,stage1_capture_ratio_wind_min,stage1_sr_hours_max,stage1_far_min,stage1_ir_p10_max,persistence_window_years,crisis_years_explicit,rule_logic
q1_rule_v4_2026_02_11,200,500,0.8,0.9,0.1,0.1,0.95,1.5,150,50,0.85,0.9,0.05,0.95,1.5,2,2022,"stage2_candidate_tech=(>=2 familles actives parmi LOW_PRICE/PHYSICAL/VALUE_TECH) avec persistence sur 2 annees non-crise; bascule_country=min(bascule_pv,bascule_wind). stage1_candidate=(familles toutes inactives) hors crise. NEG_NOT_IN_AB reste informatif; RC principal=AB_OR_LOW_RESIDUAL."
```


#### Table SCEN LOW_RIGIDITY `Q1/scen/LOW_RIGIDITY/tables/Q1_scope_audit.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,must_run_scope_coverage,lowload_p20_mw,ir_p10,scope_status,scope_reason,load_net_mode,must_run_mode_hourly
DE,2025,0.121088,45497.4,0.0397734,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2026,0.12003,46368.7,0.0390248,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2027,0.118989,47240.4,0.0383039,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2028,0.117789,47984.5,0.0376917,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2029,0.116962,48985,0.03694,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2030,0.115974,49857.3,0.0362934,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2031,0.114844,50727.2,0.0356691,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2032,0.113547,51460.8,0.0351446,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2033,0.11262,52465.6,0.0344827,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2034,0.111608,53334.4,0.0339186,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
DE,2035,0.110636,54203.1,0.0333745,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
```

##### ES (11 lignes)
```csv
country,year,must_run_scope_coverage,lowload_p20_mw,ir_p10,scope_status,scope_reason,load_net_mode,must_run_mode_hourly
ES,2025,0.138867,22488.9,0.0687296,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2026,0.137913,22919.6,0.0674411,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2027,0.137024,23353.5,0.0661984,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2028,0.13625,23719.6,0.0651768,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2029,0.135115,24214.5,0.0638385,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2030,0.134212,24647.2,0.0627179,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2031,0.13332,25079.8,0.061639,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2032,0.132595,25441.1,0.060761,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2033,0.131516,25939.9,0.0595785,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2034,0.130632,26369.1,0.0586072,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
ES,2035,0.129782,26801.6,0.0576593,INFO,coverage_coherent,net_of_psh_pump,floor_quantile
```


#### Table SCEN LOW_RIGIDITY `Q1/scen/LOW_RIGIDITY/tables/Q1_year_panel.csv`
Lignes totales: `77` | Lignes DE/ES: `22`

##### DE (11 lignes)
```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative,h_negative_obs,h_below_5,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,scenario_id,mode,horizon_year,calib_mustrun_scale,calib_vre_scale_pv,calib_vre_scale_wind_on,calib_vre_scale_wind_off,calib_export_cap_eff_gw,calib_export_coincidence_used,calib_flex_realization_factor,calib_price_b_floor,calib_price_b_intercept,calib_price_b_slope_surplus_norm,vre_penetration_share_gen,pv_penetration_share_gen,wind_penetration_share_gen,sr_hours_share,p10_load_mw,p10_must_run_mw,p50_load_mw,p50_must_run_mw,ir_p10_excess,must_run_scope_coverage,core_sanity_issue_count,core_sanity_issues,psh_pumping_twh,psh_pumping_coverage_share,psh_pumping_data_status,flex_sink_exports_twh,flex_sink_psh_twh,flex_sink_total_twh,share_neg_price_hours_in_AB,share_neg_price_hours_in_low_residual,share_neg_price_hours_in_AB_OR_LOW_RESIDUAL,surplus_energy_twh,absorbed_surplus_twh,unabsorbed_surplus_twh,low_residual_hours_share,low_residual_threshold_mw,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_hours_median_eur_mwh,residual_load_p50_on_negative_price_mw,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_sr_high,flag_low_residual_high,flag_far_low,flag_ir_high,flag_spread_high,crisis_year,low_price_family,value_family_pv,value_family_wind,value_family,physical_family,low_price_flags_count,capture_flags_count,physical_flags_count,family_count,family_count_pv,family_count_wind,stage2_points_low_price,stage2_points_capture,stage2_points_physical,stage2_points_vol,stage2_market_score,score_breakdown,quality_ok,neg_price_explained_by_surplus_ratio,market_physical_gap_flag,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,stage2_candidate_year,phase2_candidate_year,flag_capture_only_stage2,is_phase2_market,physical_candidate_year,is_phase2_physical,signal_low_price,signal_value,signal_physical,flag_non_capture_stage2,active_flags,is_stage1_criteria,stage1_candidate_year,phase_market,stress_phys_state
DE,2025,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,8a9355fb42fe7477adffdc38f8e98c01bed0373698c866f1e5e773c2e36ce953,480.173,478.693,31.6975,93.7283,19.9439,145.37,164.361,14.9535,3.45865,88.4452,19.2852,69.16,0.30368,120.426,124.484,118.168,115.723,115.374,0.960943,0.958051,115.723,115.374,0.960943,0.958051,0.591602,0.589822,0,0,0,0,125,125,32.0951,91.8872,0,0,0,0,0,0,1,1,0.0397734,0.0312383,195.609,195.609,,none,0,0,7884,876,1,0.671277,1,OK,LOW_RIGIDITY,SCEN,2025,9425.89,19.4667,36.463,5.37175,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.884452,0.192852,0.6916,0,42400.5,1686.41,54677.6,1713.73,-0.960227,0.121088,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,21773.8,21773.8,36135.1,50545.3,107.87,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2026,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,7b13dd01975b6cae6d8b5386c6100b54e6194db0cc82a6be974efc07036e88ed,489.319,487.839,31.6975,94.7325,20.3065,146.736,165.728,14.9535,3.45865,88.5405,19.1262,69.4143,0.300789,121.56,123.313,120.585,116.9,116.485,0.961665,0.958248,116.9,116.485,0.961665,0.958248,0.592361,0.590257,0,0,0,0,125,125,32.3721,92.6739,0,0,0,0,0,0,1,1,0.0390248,0.0306526,197.346,197.346,,none,0,0,7884,876,1,0.671803,1,OK,LOW_RIGIDITY,SCEN,2026,9425.89,19.8053,36.8537,5.46942,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.885405,0.191262,0.694143,0,43213.8,1686.41,55722,1713.73,-0.960975,0.12003,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,22451.3,22451.3,37009.2,51663.6,108.892,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2027,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,f975393ee706b39789ded23d161be85848838b67f14599902260a0244b44cdb5,498.465,496.985,31.6975,95.7368,20.6691,148.103,167.095,14.9535,3.45865,88.6342,18.9697,69.6645,0.298004,122.695,123.726,122.121,118.138,117.571,0.96286,0.958238,118.138,117.571,0.96286,0.958238,0.593383,0.590534,0,0,0,0,124,124,32.4349,93.4607,0,0,0,0,0,0,1,1,0.0383039,0.0300885,199.092,199.092,,none,0,0,7884,876,1,0.672306,1,OK,LOW_RIGIDITY,SCEN,2027,9425.89,20.1438,37.2444,5.56709,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.886342,0.189697,0.696645,0,44027.2,1686.41,56763.8,1713.73,-0.961696,0.118989,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,23119,23119,37887.4,52787,109.9,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2028,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,c39155d1f34aa34211df7508e95d601bfebe684736220cc3f1cb447335e465f4,507.611,506.128,31.722,97.1985,21.088,150.008,169.05,14.9868,3.4966,88.736,18.7648,69.9711,0.296385,123.785,126.289,122.406,119.234,118.629,0.963233,0.958347,119.234,118.629,0.963233,0.958347,0.594024,0.591011,0,0,0,0,124,124,32.6118,94.1929,0,0,0,0,0,0,1,1,0.0376917,0.0296107,200.723,200.723,,none,0,0,7905,879,1,0.672977,1,OK,LOW_RIGIDITY,SCEN,2028,9425.89,20.4824,37.635,5.66476,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.88736,0.187648,0.699711,0,44729.6,1685.93,57648.6,1712.99,-0.962308,0.117789,0,,1.48351,1,ok,3.4966,0,0,,,,0,0,0,0.100068,23652.1,23652.1,38588.8,53678.7,110.88,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2029,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,1fae15fc5609f566b84f58483a16ad7f9fea9e244a03a5ffdb7ce9ca66c259c8,516.757,515.277,31.6975,97.7453,21.3943,150.837,169.829,14.9535,3.45865,88.8172,18.6644,70.1528,0.29273,124.963,135.67,119.005,120.418,119.792,0.963624,0.958617,120.418,119.792,0.963624,0.958617,0.594492,0.591403,0,0,0,0,124,124,32.9916,95.0343,0,0,0,0,0,0,1,1,0.03694,0.0290204,202.556,202.556,,none,0,0,7884,876,1,0.673222,1,OK,LOW_RIGIDITY,SCEN,2029,9425.89,20.8209,38.0257,5.76243,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.888172,0.186644,0.701528,0,45652.8,1686.41,58847.4,1713.73,-0.96306,0.116962,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,24487.6,24487.6,39647.3,54930.8,111.913,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2030,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,f1152bd5c0fa267560e0f091dfe16e09f36f39b27d631b5155575efffa43e197,525.903,524.423,31.6975,98.7495,21.757,152.204,171.196,14.9535,3.45865,88.9065,18.5154,70.3911,0.290231,126.098,134.108,121.64,121.62,120.9,0.964491,0.958778,121.62,120.9,0.964491,0.958778,0.595336,0.591809,0,0,0,0,123,123,33.0573,95.821,0,0,0,0,0,0,1,1,0.0362934,0.0285142,204.288,204.288,,none,0,0,7884,876,1,0.673641,1,OK,LOW_RIGIDITY,SCEN,2030,9425.89,21.1595,38.4164,5.8601,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.889065,0.185154,0.703911,0,46466.1,1686.41,59889.6,1713.73,-0.963707,0.115974,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,25150.4,25150.4,40566.8,56011.4,112.923,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2031,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,b38b38035d052ec5dc319b9d65afe95bce4f07578465fc6cb254f6661fc37c86,535.05,533.569,32.1598,99.7538,22.1196,154.033,173.025,14.9535,3.45865,89.0238,18.5868,70.4369,0.288684,127.218,131.727,124.709,122.691,121.998,0.96442,0.958971,122.691,121.998,0.96442,0.958971,0.595553,0.592189,0,0,0,0,123,123,33.3418,96.6078,0,0,0,0,0,0,1,1,0.0356691,0.0280255,206.012,206.012,,none,0,0,7884,876,1,0.674456,1,OK,LOW_RIGIDITY,SCEN,2031,9425.89,21.4981,38.8071,5.95777,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.890238,0.185868,0.704369,0,47279.4,1686.41,60932.4,1713.73,-0.964331,0.114844,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,25770,25770,41372.8,57073,113.914,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2032,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,4e85a4976dd26ce5f76894e2753e6136087c35f0b284ba98517232eb4b993cea,544.196,542.712,32.6953,101.234,22.5423,156.472,175.514,14.9868,3.4966,89.1508,18.6283,70.5225,0.288315,128.289,130.388,127.119,123.739,123.041,0.964535,0.959088,123.739,123.041,0.964535,0.959088,0.595972,0.592606,0,0,0,0,123,123,33.5173,97.336,0,0,0,0,0,0,1,1,0.0351446,0.0276146,207.626,207.626,,none,0,0,7905,879,1,0.675488,1,OK,LOW_RIGIDITY,SCEN,2032,9425.89,21.8366,39.1978,6.05544,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.891508,0.186283,0.705225,0,47971.3,1685.93,61807,1712.99,-0.964855,0.113547,0,,1.48351,1,ok,3.4966,0,0,,,,0,0,0,0.100068,26208.4,26208.4,41998.3,57913.5,114.876,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2033,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,6cd440b6da363c76edc6e04a4d721cc63f9dccccb916912e82dcd049d80b9f67,553.342,551.862,33.1728,101.762,22.8448,157.78,176.771,14.9535,3.45865,89.2564,18.7659,70.4905,0.285905,129.455,132.135,127.973,124.83,124.199,0.964272,0.959401,124.83,124.199,0.964272,0.959401,0.595974,0.592963,0,0,0,0,123,123,33.9072,98.1812,0,0,0,0,0,0,1,1,0.0344827,0.0270965,209.455,209.455,,none,0,0,7884,876,1,0.676091,1,OK,LOW_RIGIDITY,SCEN,2033,9425.89,22.1752,39.5884,6.15311,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.892564,0.187659,0.704905,0,48906,1686.41,63018,1713.73,-0.965517,0.11262,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,26987.3,26987.3,43003.9,59186,115.898,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2034,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,36b59f9b0243f7a57fa815bdd703fc772bf186dd8cccd5b8b1770dd42597fa39,562.488,561.008,33.6792,102.766,23.2075,159.653,178.645,14.9535,3.45865,89.3691,18.8526,70.5164,0.284583,130.574,138.267,126.318,125.911,125.297,0.964288,0.95959,125.911,125.297,0.964288,0.95959,0.596231,0.593327,0,0,0,0,123,123,34.1924,98.968,0,0,0,0,0,0,1,1,0.0339186,0.0266548,211.178,211.178,,none,0,0,7884,876,1,0.676879,1,OK,LOW_RIGIDITY,SCEN,2034,9425.89,22.5137,39.9791,6.25078,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.893691,0.188526,0.705164,0,49719.4,1686.41,64060.9,1713.73,-0.966081,0.111608,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,27602.1,27602.1,43814.6,60229.7,116.897,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
DE,2035,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,f1dfb49beeda353cb52a13e71a9c7a9d58679257e888bc16224d4964e3951240,571.634,570.154,34.1857,103.771,23.5701,161.527,180.518,14.9535,3.45865,89.4794,18.9376,70.5418,0.283303,131.692,143.182,125.298,126.966,126.422,0.964109,0.959982,126.966,126.422,0.964109,0.959982,0.596345,0.593793,0,0,0,0,122,122,34.2516,99.7547,0,0,0,0,0,0,1,1,0.0333745,0.0262272,212.907,212.907,,none,0,0,7884,876,1,0.677645,1,OK,LOW_RIGIDITY,SCEN,2035,9425.89,22.8523,40.3698,6.34845,1.65,0.45,0.9,-43.87,-0.03,-9.36265,0.894794,0.189376,0.705418,0,50530,1686.41,65104.8,1713.73,-0.966626,0.110636,0,,1.48009,1,ok,3.45865,0,0,,,,0,0,0,0.1,28185.1,28185.1,44622.4,61301.5,117.885,,,False,False,False,False,False,False,True,False,False,False,False,False,False,False,False,True,0,0,1,1,1,1,0,0,1,0,1,low=0;value=0;physical=1;crisis=0,True,,False,False,False,False,False,False,False,False,True,True,False,False,True,1,"physical_family,flag_low_residual_high",True,True,phase1,pas_de_surplus_structurel
```

##### ES (11 lignes)
```csv
country,year,n_hours_expected,n_hours_with_price,n_hours_with_load,n_hours_with_vre,n_hours_with_must_run,missing_share_price,missing_share_load,missing_share_generation,missing_share_net_position,load_net_mode,must_run_mode,entsoe_code_used,data_version_hash,load_total_twh,load_net_twh,gen_solar_twh,gen_wind_on_twh,gen_wind_off_twh,gen_vre_twh,gen_primary_twh,gen_must_run_twh,exports_twh,vre_penetration_pct_gen,pv_penetration_pct_gen,wind_penetration_pct_gen,vre_penetration_proxy,baseload_price_eur_mwh,peakload_price_eur_mwh,offpeak_price_eur_mwh,capture_rate_pv_eur_mwh,capture_rate_wind_eur_mwh,capture_ratio_pv,capture_ratio_wind,capture_price_pv_eur_mwh,capture_price_wind_eur_mwh,capture_ratio_pv_vs_baseload,capture_ratio_wind_vs_baseload,capture_ratio_pv_vs_ttl,capture_ratio_wind_vs_ttl,h_negative,h_negative_obs,h_below_5,h_below_5_obs,days_spread_50_obs,days_spread_gt50,avg_daily_spread_obs,max_daily_spread_obs,surplus_twh,surplus_unabsorbed_twh,sr_energy_share_load,sr_energy_share_gen,sr_energy,sr_hours,far_observed,far_energy,ir_p10,ir_mean,ttl_price_based_eur_mwh,ttl_eur_mwh,tca_ccgt_median_eur_mwh,tca_method,h_regime_a,h_regime_b,h_regime_c,h_regime_d,regime_coherence,nrl_price_corr,completeness,quality_flag,scenario_id,mode,horizon_year,calib_mustrun_scale,calib_vre_scale_pv,calib_vre_scale_wind_on,calib_vre_scale_wind_off,calib_export_cap_eff_gw,calib_export_coincidence_used,calib_flex_realization_factor,calib_price_b_floor,calib_price_b_intercept,calib_price_b_slope_surplus_norm,vre_penetration_share_gen,pv_penetration_share_gen,wind_penetration_share_gen,sr_hours_share,p10_load_mw,p10_must_run_mw,p50_load_mw,p50_must_run_mw,ir_p10_excess,must_run_scope_coverage,core_sanity_issue_count,core_sanity_issues,psh_pumping_twh,psh_pumping_coverage_share,psh_pumping_data_status,flex_sink_exports_twh,flex_sink_psh_twh,flex_sink_total_twh,share_neg_price_hours_in_AB,share_neg_price_hours_in_low_residual,share_neg_price_hours_in_AB_OR_LOW_RESIDUAL,surplus_energy_twh,absorbed_surplus_twh,unabsorbed_surplus_twh,low_residual_hours_share,low_residual_threshold_mw,residual_load_p10_mw,residual_load_p50_mw,residual_load_p90_mw,price_low_residual_median_eur_mwh,price_negative_hours_median_eur_mwh,residual_load_p50_on_negative_price_mw,flag_h_negative_stage2,flag_h_below_5_stage2,flag_capture_pv_low,flag_capture_wind_low,flag_sr_hours_high,flag_sr_high,flag_low_residual_high,flag_far_low,flag_ir_high,flag_spread_high,crisis_year,low_price_family,value_family_pv,value_family_wind,value_family,physical_family,low_price_flags_count,capture_flags_count,physical_flags_count,family_count,family_count_pv,family_count_wind,stage2_points_low_price,stage2_points_capture,stage2_points_physical,stage2_points_vol,stage2_market_score,score_breakdown,quality_ok,neg_price_explained_by_surplus_ratio,market_physical_gap_flag,stage2_candidate_year_pv,stage2_candidate_year_wind,stage2_candidate_year_country,stage2_candidate_year,phase2_candidate_year,flag_capture_only_stage2,is_phase2_market,physical_candidate_year,is_phase2_physical,signal_low_price,signal_value,signal_physical,flag_non_capture_stage2,active_flags,is_stage1_criteria,stage1_candidate_year,phase_market,stress_phys_state
ES,2025,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,14f556c8ca867dbcda2572cb590ab6b2289e33c382bae72925b06db2fed02315,234.28,232.927,28.6131,43.9453,0,72.5584,110.382,12.8895,6.66768,65.734,25.9219,39.812,0.311507,92.6739,89.8286,94.2573,86.1009,90.086,0.929074,0.972076,86.1009,90.086,0.929074,0.972076,0.548413,0.573795,0,0,0,0,191,191,40.8505,80.6602,0,0,0,0,0,0,1,1,0.0687296,0.0553372,157,157,,none,0,0,7884,876,1,0.709218,1,OK,LOW_RIGIDITY,SCEN,2025,6237.2,12.5165,13.3741,1.9703,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.65734,0.259219,0.39812,0,21190.1,1456.39,26705,1485.41,-0.93127,0.138867,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,10671.6,10671.6,16480.3,23756.8,82.3528,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2026,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,343d5f6c79bb1bc0f622d4b53261ddd3b9a390c0619e32b34fcaed330baaa6df,238.743,237.39,29.1108,44.4161,0,73.5269,111.35,12.8895,6.66768,66.032,26.1434,39.8886,0.309731,93.3662,90.1402,95.1614,86.7295,90.7845,0.928918,0.972349,86.7295,90.7845,0.928918,0.972349,0.54845,0.574092,0,0,0,0,191,191,41.1645,81.2903,0,0,0,0,0,0,1,1,0.0674411,0.0542969,158.136,158.136,,none,0,0,7884,876,1,0.709965,1,OK,LOW_RIGIDITY,SCEN,2026,6237.2,12.7342,13.5173,2.00612,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.66032,0.261434,0.398886,0,21595,1456.39,27219.4,1485.41,-0.932559,0.137913,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,10959.7,10959.7,16868,24281.2,82.9388,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2027,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,33434feea8111410119bb6b67c184585919ca3e45137cd339d0309cc214e751b,243.205,241.852,29.6084,44.887,0,74.4953,112.319,12.8895,6.66768,66.3249,26.361,39.9639,0.30802,94.0585,90.5956,95.9855,87.3543,91.4724,0.928723,0.972505,87.3543,91.4724,0.928723,0.972505,0.548537,0.574396,0,0,0,0,192,192,41.6606,81.9205,0,0,0,0,0,0,1,1,0.0661984,0.0532951,159.25,159.25,,none,0,0,7884,876,1,0.710697,1,OK,LOW_RIGIDITY,SCEN,2027,6237.2,12.9519,13.6606,2.04194,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.663249,0.26361,0.399639,0,22000.4,1456.39,27732.4,1485.41,-0.933802,0.137024,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,11260.3,11260.3,17250.9,24782.7,83.5246,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2028,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,1b76db075f1cefd003c9097b78ac48428217b61823503b3d3f1aaba710daf346,247.668,246.313,30.1557,45.3917,0,75.5474,113.464,12.9203,6.67103,66.5826,26.5773,40.0053,0.306713,94.7217,91.4483,96.5248,87.9436,92.1036,0.928442,0.97236,87.9436,92.1036,0.928442,0.97236,0.548613,0.574564,0,0,0,0,193,193,42.0394,82.4866,0,0,0,0,0,0,1,1,0.0651768,0.0524548,160.302,160.302,,none,0,0,7905,879,1,0.711024,1,OK,LOW_RIGIDITY,SCEN,2028,6237.2,13.1695,13.8039,2.07776,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.665826,0.265773,0.400053,0,22344.3,1456.33,28171,1485.02,-0.934823,0.13625,0,,1.35454,1,ok,6.67103,0,0,,,,0,0,0,0.100068,11482.7,11482.7,17587.4,25246.1,84.0865,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2029,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,b83118ecffdfd8be88c74e9adc39e9992c780213d3ded958d17ce62fcb8f76f7,252.13,250.777,30.6036,45.8286,0,76.4323,114.256,12.8895,6.66768,66.8958,26.7852,40.1106,0.304782,95.4431,95.6888,95.3063,88.6273,92.8666,0.928588,0.973005,88.6273,92.8666,0.928588,0.973005,0.548857,0.57511,0,0,0,0,194,194,42.6602,83.1807,0,0,0,0,0,0,1,1,0.0638385,0.0513984,161.476,161.476,,none,0,0,7884,876,1,0.712111,1,OK,LOW_RIGIDITY,SCEN,2029,6237.2,13.3872,13.9472,2.11358,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.668958,0.267852,0.401106,0,22813.7,1456.39,28755.7,1485.41,-0.936162,0.135115,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,11840.7,11840.7,18022.4,25819.9,84.713,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2030,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,2eb871f6e5b69582dc22abf19d7cd2b6cadab891d0ed4e9eca9fa3051cbfb8c4,256.593,255.24,31.1012,46.2995,0,77.4007,115.224,12.8895,6.66768,67.174,26.9919,40.1821,0.303247,96.1354,94.8213,96.8666,89.2497,93.5572,0.928375,0.973182,89.2497,93.5572,0.928375,0.973182,0.548922,0.575415,0,0,0,0,193,193,42.7911,83.8108,0,0,0,0,0,0,1,1,0.0627179,0.0504997,162.591,162.591,,none,0,0,7884,876,1,0.712801,1,OK,LOW_RIGIDITY,SCEN,2030,6237.2,13.6049,14.0905,2.1494,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.67174,0.269919,0.401821,0,23221.3,1456.39,29267,1485.41,-0.937282,0.134212,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,12135.3,12135.3,18408.5,26339.2,85.3074,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2031,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,53f86d8fc270cdc060642ffcc7b0bfc3a837055762d4762825026a425350bd46,261.055,259.702,31.5989,46.7703,0,78.3692,116.193,12.8895,6.66768,67.4476,27.1952,40.2524,0.301766,96.8277,93.756,98.537,89.8864,94.2442,0.928313,0.973319,89.8864,94.2442,0.928313,0.973319,0.549097,0.575718,0,0,0,0,193,193,43.1078,84.4409,0,0,0,0,0,0,1,1,0.061639,0.049632,163.698,163.698,,none,0,0,7884,876,1,0.713476,1,OK,LOW_RIGIDITY,SCEN,2031,6237.2,13.8226,14.2338,2.18522,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.674476,0.271952,0.402524,0,23627.7,1456.39,29778.3,1485.41,-0.938361,0.13332,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,12429.4,12429.4,18802.2,26849.2,85.8947,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2032,8784,8784,8784,8784,8784,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,01ef121343dad41048c75c558af7184994f72bbcd9db0912179c0151f03666d2,265.518,264.163,32.1495,47.2764,0,79.4259,117.343,12.9203,6.67103,67.6871,27.398,40.2892,0.30067,97.4883,94.0243,99.4193,90.4817,94.8698,0.928129,0.973141,90.4817,94.8698,0.928129,0.973141,0.549191,0.575825,0,0,0,0,194,194,43.4862,85.0025,0,0,0,0,0,0,1,1,0.060761,0.0489104,164.755,164.755,,none,0,0,7905,879,1,0.713743,1,OK,LOW_RIGIDITY,SCEN,2032,6237.2,14.0403,14.3771,2.22104,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.676871,0.27398,0.402892,0,23968.1,1456.33,30210,1485.02,-0.939239,0.132595,0,,1.35454,1,ok,6.67103,0,0,,,,0,0,0,0.100068,12659.2,12659.2,19133.5,27308.9,86.45,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2033,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,dcf9cbd7316a1d68671ebc2193273ebc104d7eb38119fdbdb9825ea5926c9b00,269.98,268.627,32.5941,47.712,0,80.3061,118.13,12.8895,6.66768,67.9813,27.5918,40.3895,0.29895,98.2123,94.7848,100.108,91.162,95.6169,0.928214,0.973574,91.162,95.6169,0.928214,0.973574,0.549438,0.576288,0,0,0,0,195,195,44.118,85.7012,0,0,0,0,0,0,1,1,0.0595785,0.047983,165.919,165.919,,none,0,0,7884,876,1,0.71478,1,OK,LOW_RIGIDITY,SCEN,2033,6237.2,14.2579,14.5204,2.25686,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.679813,0.275918,0.403895,0,24444.9,1456.39,30801.7,1485.41,-0.940422,0.131516,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,13028.7,13028.7,19584.1,27883.7,87.0745,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2034,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,18f5d359fb098a49a5bfe00d8b514d006243678673733984b552f76d8ccc2978,274.443,273.09,33.0917,48.1828,0,81.2745,119.098,12.8895,6.66768,68.2417,27.7853,40.4564,0.297611,98.9046,97.6752,99.5847,91.7988,96.3136,0.928155,0.973803,91.7988,96.3136,0.928155,0.973803,0.549562,0.576591,0,0,0,0,195,195,44.4367,86.3313,0,0,0,0,0,0,1,1,0.0586072,0.0471989,167.04,167.04,,none,0,0,7884,876,1,0.715416,1,OK,LOW_RIGIDITY,SCEN,2034,6237.2,14.4756,14.6637,2.29268,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.682417,0.277853,0.404564,0,24850,1456.39,31315.5,1485.41,-0.941393,0.130632,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,13319.5,13319.5,19972.4,28395.2,87.6644,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
ES,2035,8760,8760,8760,8760,8760,0,0,0,0,net_of_psh_pump,floor_quantile,SCEN:LOW_RIGIDITY,1fd79914d150d0600b62cd8c51537571b0a8f79c9b7a9aae6d3367d5f65b07c2,278.905,277.552,33.5894,48.6536,0,82.243,120.066,12.8895,6.66768,68.4979,27.9756,40.5222,0.296315,99.5969,99.819,99.4733,92.4349,97.0031,0.92809,0.973957,92.4349,97.0031,0.92809,0.973957,0.549688,0.576854,0,0,0,0,196,196,44.9455,86.9614,0,0,0,0,0,0,1,1,0.0576593,0.0464401,168.159,168.159,,none,0,0,7884,876,1,0.71604,1,OK,LOW_RIGIDITY,SCEN,2035,6237.2,14.6933,14.807,2.3285,1.65,0.45,0.899462,-0.36,3.32,-12.5665,0.684979,0.279756,0.405222,0,25258.5,1456.39,31829.5,1485.41,-0.942341,0.129782,0,,1.35291,1,ok,6.66768,0,0,,,,0,0,0,0.1,13613,13613,20360.9,28923.1,88.2599,,,False,False,False,False,False,False,True,False,False,True,False,True,False,False,False,True,0,0,1,2,2,2,1,0,1,0,2,low=1;value=0;physical=1;crisis=0,True,,False,True,True,True,True,True,False,True,True,True,True,False,True,2,"low_price_family,physical_family,flag_low_residual_high,flag_spread_high",True,True,phase2,pas_de_surplus_structurel
```


## Q2

### GLOBAL

#### Summary (question)
```json
{
  "question_id": "Q2",
  "run_id": "FULL_20260211_191955",
  "selection": {
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "years": [
      2018,
      2019,
      2020,
      2021,
      2022,
      2023,
      2024
    ],
    "scenario_ids": [
      "BASE",
      "HIGH_CO2",
      "HIGH_GAS"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ]
  },
  "hist_module_id": "Q2",
  "scenarios": [
    "BASE",
    "HIGH_CO2",
    "HIGH_GAS"
  ],
  "n_checks": 137,
  "n_warnings": 32,
  "n_test_rows": 9,
  "n_compare_rows": 42,
  "checks": [
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "CZ-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=6181.66, p10_load_mw=5946.48.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "CZ-2018: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2018: must_run_share=79.3% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2019: must_run_share=78.2% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2020: must_run_share=76.3% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2021: must_run_share=76.1% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "CZ-2022: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=5874.35, p10_load_mw=5645.40.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "CZ-2022: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2022: must_run_share=79.6% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2023: must_run_share=79.6% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2024: must_run_share=78.6% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41354.50, p10_load_mw=39303.40.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2018: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2018: must_run_share=82.4% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2019: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=40635.00, p10_load_mw=39530.00.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2019: must_run_share=80.7% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2020: must_run_share=77.9% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2021: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41252.00, p10_load_mw=39284.00.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2021: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2021: must_run_share=79.4% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2022: must_run_share=73.5% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2023: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2023: must_run_share=75.9% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2024: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=39406.20, p10_load_mw=37062.60.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2024: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2024: must_run_share=79.2% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2018: must_run_share=0.0% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2019: must_run_share=0.0% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2020: must_run_share=0.1% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2021: must_run_share=0.1% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2022: must_run_share=0.1% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2023: must_run_share=0.2% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2024: must_run_share=0.2% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "Q2_POSITIVE_ROBUST_SLOPE",
      "message": "ES-WIND: pente robuste positive (exception possible meteo/structure).",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "Q2_POSITIVE_ROBUST_SLOPE",
      "message": "ES-WIND: pente robuste positive (exception possible meteo/structure).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "Q2_POSITIVE_ROBUST_SLOPE",
      "message": "ES-WIND: pente robuste positive (exception possible meteo/structure).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "PASS",
      "code": "BUNDLE_LEDGER_STATUS",
      "message": "ledger: FAIL=0, WARN=0",
      "scope": "BUNDLE",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "BUNDLE_INFORMATIVENESS",
      "message": "share_tests_informatifs=100.00% ; share_compare_informatifs=28.57%",
      "scope": "BUNDLE",
      "scenario_id": ""
    }
  ],
  "warnings": [
    "IT_NORD-PV: bascule Q1 absente, pente non calculee.",
    "IT_NORD-WIND: bascule Q1 absente, pente non calculee.",
    "BASE: CZ-PV: bascule Q1 absente, pente non calculee.",
    "BASE: CZ-WIND: bascule Q1 absente, pente non calculee.",
    "BASE: DE-PV: bascule Q1 absente, pente non calculee.",
    "BASE: DE-WIND: bascule Q1 absente, pente non calculee.",
    "BASE: FR-PV: bascule Q1 absente, pente non calculee.",
    "BASE: FR-WIND: bascule Q1 absente, pente non calculee.",
    "BASE: IT_NORD-PV: bascule Q1 absente, pente non calculee.",
    "BASE: IT_NORD-WIND: bascule Q1 absente, pente non calculee.",
    "BASE: NL-PV: bascule Q1 absente, pente non calculee.",
    "BASE: NL-WIND: bascule Q1 absente, pente non calculee.",
    "HIGH_CO2: CZ-PV: bascule Q1 absente, pente non calculee.",
    "HIGH_CO2: CZ-WIND: bascule Q1 absente, pente non calculee.",
    "HIGH_CO2: DE-PV: bascule Q1 absente, pente non calculee.",
    "HIGH_CO2: DE-WIND: bascule Q1 absente, pente non calculee.",
    "HIGH_CO2: FR-PV: bascule Q1 absente, pente non calculee.",
    "HIGH_CO2: FR-WIND: bascule Q1 absente, pente non calculee.",
    "HIGH_CO2: IT_NORD-PV: bascule Q1 absente, pente non calculee.",
    "HIGH_CO2: IT_NORD-WIND: bascule Q1 absente, pente non calculee.",
    "HIGH_CO2: NL-PV: bascule Q1 absente, pente non calculee.",
    "HIGH_CO2: NL-WIND: bascule Q1 absente, pente non calculee.",
    "HIGH_GAS: CZ-PV: bascule Q1 absente, pente non calculee.",
    "HIGH_GAS: CZ-WIND: bascule Q1 absente, pente non calculee.",
    "HIGH_GAS: DE-PV: bascule Q1 absente, pente non calculee.",
    "HIGH_GAS: DE-WIND: bascule Q1 absente, pente non calculee.",
    "HIGH_GAS: FR-PV: bascule Q1 absente, pente non calculee.",
    "HIGH_GAS: FR-WIND: bascule Q1 absente, pente non calculee.",
    "HIGH_GAS: IT_NORD-PV: bascule Q1 absente, pente non calculee.",
    "HIGH_GAS: IT_NORD-WIND: bascule Q1 absente, pente non calculee.",
    "HIGH_GAS: NL-PV: bascule Q1 absente, pente non calculee.",
    "HIGH_GAS: NL-WIND: bascule Q1 absente, pente non calculee."
  ]
}
```

#### Narratif (question)
Analyse complete Q2: historique + prospectif en un seul run. Statut global=WARN. Tests PASS=9, WARN=0, FAIL=0, NON_TESTABLE=0. Les resultats sont separes entre historique et scenarios, puis compares dans une table unique.

#### Table `Q2/test_ledger.csv`
Lignes: `9`

```csv
test_id,question_id,source_ref,mode,scenario_group,title,what_is_tested,metric_rule,severity_if_fail,scenario_id,status,value,threshold,interpretation
Q2-S-01,Q2,SPEC2-Q2/Slides 11,SCEN,DEFAULT,Pentes projetees,Les pentes sont reproduites en mode scenario.,Q2_country_slopes non vide en SCEN,HIGH,BASE,PASS,14,>0 lignes,Pentes prospectives calculees.
Q2-S-02,Q2,SPEC2-Q2,SCEN,DEFAULT,Delta pente vs BASE,Les differences de pente vs BASE sont calculables.,delta slope par pays/tech vs BASE,MEDIUM,BASE,PASS,finite=28.57%; robust=14.29%; reason_known=100.00%,finite_share >= 20%,Delta de pente exploitable directionnellement; robustesse statistique a lire a part.
Q2-S-01,Q2,SPEC2-Q2/Slides 11,SCEN,DEFAULT,Pentes projetees,Les pentes sont reproduites en mode scenario.,Q2_country_slopes non vide en SCEN,HIGH,HIGH_CO2,PASS,14,>0 lignes,Pentes prospectives calculees.
Q2-S-02,Q2,SPEC2-Q2,SCEN,DEFAULT,Delta pente vs BASE,Les differences de pente vs BASE sont calculables.,delta slope par pays/tech vs BASE,MEDIUM,HIGH_CO2,PASS,finite=28.57%; robust=14.29%; reason_known=100.00%,finite_share >= 20%,Delta de pente exploitable directionnellement; robustesse statistique a lire a part.
Q2-S-01,Q2,SPEC2-Q2/Slides 11,SCEN,DEFAULT,Pentes projetees,Les pentes sont reproduites en mode scenario.,Q2_country_slopes non vide en SCEN,HIGH,HIGH_GAS,PASS,14,>0 lignes,Pentes prospectives calculees.
Q2-S-02,Q2,SPEC2-Q2,SCEN,DEFAULT,Delta pente vs BASE,Les differences de pente vs BASE sont calculables.,delta slope par pays/tech vs BASE,MEDIUM,HIGH_GAS,PASS,finite=28.57%; robust=14.29%; reason_known=100.00%,finite_share >= 20%,Delta de pente exploitable directionnellement; robustesse statistique a lire a part.
Q2-H-01,Q2,SPEC2-Q2/Slides 10,HIST,HIST_BASE,Pentes OLS post-bascule,Les pentes PV/Wind sont estimees en historique.,Q2_country_slopes non vide,HIGH,nan,PASS,14,>0 lignes,Les pentes historiques sont calculees.
Q2-H-02,Q2,SPEC2-Q2/Slides 10-12,HIST,HIST_BASE,Robustesse statistique,R2/p-value/n sont disponibles pour qualifier la robustesse.,"colonnes r2,p_value,n presentes",MEDIUM,nan,PASS,"n,p_value,r2","r2,p_value,n disponibles",La robustesse statistique est lisible.
Q2-H-03,Q2,Slides 10-13,HIST,HIST_BASE,Drivers physiques,Les drivers SR/FAR/IR/corr VRE-load sont exploites.,driver correlations non vides,MEDIUM,nan,PASS,4,>0 lignes,Les drivers de pente sont disponibles.
```


#### Table `Q2/comparison_hist_vs_scen.csv`
Lignes totales: `42` | Lignes DE/ES: `12`

##### DE (6 lignes)
```csv
country,tech,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
DE,PV,BASE,slope,-0.0318441,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,WIND,BASE,slope,-0.00235043,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,PV,HIGH_CO2,slope,-0.0318441,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,WIND,HIGH_CO2,slope,-0.00235043,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,PV,HIGH_GAS,slope,-0.0318441,,,,NON_TESTABLE,delta_non_interpretable_nan
DE,WIND,HIGH_GAS,slope,-0.00235043,,,,NON_TESTABLE,delta_non_interpretable_nan
```

##### ES (6 lignes)
```csv
country,tech,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
ES,PV,BASE,slope,-0.0532886,-0.000446851,0.0528418,,INFORMATIVE,delta_interpretable
ES,WIND,BASE,slope,-0.00993688,0.00226091,0.0121978,,INFORMATIVE,delta_interpretable
ES,PV,HIGH_CO2,slope,-0.0532886,-0.000308119,0.0529805,,INFORMATIVE,delta_interpretable
ES,WIND,HIGH_CO2,slope,-0.00993688,0.00231496,0.0122518,,INFORMATIVE,delta_interpretable
ES,PV,HIGH_GAS,slope,-0.0532886,-0.000292372,0.0529963,,INFORMATIVE,delta_interpretable
ES,WIND,HIGH_GAS,slope,-0.00993688,0.00224312,0.01218,,INFORMATIVE,delta_interpretable
```


### HIST

#### Summary (hist)
```json
{
  "module_id": "Q2",
  "run_id": "FULL_20260211_191955_HIST",
  "selection": {
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "years": [
      2018,
      2019,
      2020,
      2021,
      2022,
      2023,
      2024
    ],
    "scenario_ids": [
      "BASE",
      "HIGH_CO2",
      "HIGH_GAS"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "mode": "HIST",
    "run_id": "FULL_20260211_191955"
  },
  "assumptions_used": [
    {
      "param_group": "Q2",
      "param_name": "exclude_year_2022",
      "param_value": 0.0,
      "unit": "bool",
      "description": "Exclude 2022 from regressions (1=yes)",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q2",
      "param_name": "min_points_regression",
      "param_value": 3.0,
      "unit": "count",
      "description": "Nombre minimal de points regression",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    }
  ],
  "kpis": {
    "n_slopes": 14,
    "n_robust": 2
  },
  "checks": [
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "CZ-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=6181.66, p10_load_mw=5946.48."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "CZ-2018: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2018: must_run_share=79.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2019: must_run_share=78.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2020: must_run_share=76.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2021: must_run_share=76.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "CZ-2022: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=5874.35, p10_load_mw=5645.40."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "CZ-2022: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2022: must_run_share=79.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2023: must_run_share=79.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2024: must_run_share=78.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41354.50, p10_load_mw=39303.40."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2018: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2018: must_run_share=82.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2019: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=40635.00, p10_load_mw=39530.00."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2019: must_run_share=80.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2020: must_run_share=77.9% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2021: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41252.00, p10_load_mw=39284.00."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2021: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2021: must_run_share=79.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2022: must_run_share=73.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2023: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2023: must_run_share=75.9% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2024: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=39406.20, p10_load_mw=37062.60."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2024: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2024: must_run_share=79.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2018: must_run_share=0.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2019: must_run_share=0.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2020: must_run_share=0.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2021: must_run_share=0.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2022: must_run_share=0.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2023: must_run_share=0.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2024: must_run_share=0.2% hors plage plausible [5%,60%]."
    }
  ],
  "warnings": [
    "IT_NORD-PV: bascule Q1 absente, pente non calculee.",
    "IT_NORD-WIND: bascule Q1 absente, pente non calculee."
  ],
  "mode": "HIST",
  "scenario_id": null,
  "horizon_year": null
}
```

#### Narratif (hist)
Q2 estime la pente de cannibalisation sur la fenetre post-bascule Q1 (phase 2), en excluant annees de crise et qualite insuffisante; OLS si n>=3, two-point delta si n=2.

#### Table HIST `Q2/hist/tables/Q2_country_slopes.csv`
Lignes totales: `14` | Lignes DE/ES: `4`

##### DE (2 lignes)
```csv
country,tech,phase2_start_year_for_slope,phase2_start_reason,phase2_end_year,years_used,n_points,x_axis_used,x_unit,slope,intercept,r2,p_value,n,slope_method,method,insufficient_points,robust_flag,reason_code,outlier_years_count,slope_all_years,slope_excluding_outliers,mean_sr_energy_phase2,mean_far_energy_phase2,mean_ir_p10_phase2,mean_ttl_phase2,vre_load_corr_phase2,surplus_load_trough_share_phase2
DE,PV,2021,q1_bascule_pv,2024,"2021,2023,2024",3,pv_penetration_pct_gen,pct_point,-0.0318441,1.09688,0.738568,0.341675,3,ols,ols,False,NOT_SIGNIFICANT,ok,0,-0.0318441,-0.0318441,0.0043336,1,0.245169,188.012,,
DE,WIND,2019,q1_bascule_wind,2024,"2019,2020,2021,2023,2024",5,wind_penetration_pct_gen,pct_point,-0.00235043,0.911857,0.391296,0.259064,5,ols,ols,False,NOT_SIGNIFICANT,ok,0,-0.00235043,-0.00235043,0.00285083,0.99753,0.252761,135.551,,
```

##### ES (2 lignes)
```csv
country,tech,phase2_start_year_for_slope,phase2_start_reason,phase2_end_year,years_used,n_points,x_axis_used,x_unit,slope,intercept,r2,p_value,n,slope_method,method,insufficient_points,robust_flag,reason_code,outlier_years_count,slope_all_years,slope_excluding_outliers,mean_sr_energy_phase2,mean_far_energy_phase2,mean_ir_p10_phase2,mean_ttl_phase2,vre_load_corr_phase2,surplus_load_trough_share_phase2
ES,PV,2023,q1_bascule_pv,2024,"2023,2024",2,pv_penetration_pct_gen,pct_point,-0.0532886,1.71872,,,2,two_point,two_point,True,FRAGILE,insufficient_points,0,-0.0532886,-0.0532886,0.0131211,0.999481,0.295142,144.664,,
ES,WIND,2023,q1_bascule_wind,2024,"2023,2024",2,wind_penetration_pct_gen,pct_point,-0.00993688,1.12386,,,2,two_point,two_point,True,FRAGILE,insufficient_points,0,-0.00993688,-0.00993688,0.0131211,0.999481,0.295142,144.664,,
```


#### Table HIST `Q2/hist/tables/Q2_driver_correlations.csv`
Lignes: `4`

```csv
driver_name,corr_with_slope_pv,corr_with_slope_wind,n_countries,expected_sign,sign_conflict_share
far_energy,-0.016913,,7,,0
ir_p10,0.371472,,7,,0
sr_energy,0.156802,,7,,0
vre_penetration_share_gen,0.431966,,7,,0
```


#### Table HIST `Q2/hist/tables/Q2_driver_diagnostics.csv`
Lignes totales: `28` | Lignes DE/ES: `8`

##### DE (4 lignes)
```csv
country,driver_name,corr_capture_pv,elasticity_capture_pv,expected_sign,observed_sign,sign_conflict
DE,sr_energy,-0.707316,-0.129712,,-1,False
DE,far_energy,,,,0,False
DE,vre_penetration_share_gen,-0.69704,-0.512416,,-1,False
DE,ir_p10,0.788993,1.26311,,1,False
```

##### ES (4 lignes)
```csv
country,driver_name,corr_capture_pv,elasticity_capture_pv,expected_sign,observed_sign,sign_conflict
ES,sr_energy,,,,0,False
ES,far_energy,,,,0,False
ES,vre_penetration_share_gen,,,,0,False
ES,ir_p10,,,,0,False
```


### SCEN

#### Scenario `BASE`

#### Summary (BASE)
```json
{
  "module_id": "Q2",
  "run_id": "FULL_20260211_191955_BASE",
  "selection": {
    "countries": [
      "FR",
      "DE",
      "ES",
      "NL",
      "BE",
      "CZ",
      "IT_NORD"
    ],
    "years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "scenario_ids": [
      "BASE",
      "HIGH_CO2",
      "HIGH_GAS"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955",
    "mode": "SCEN",
    "scenario_id": "BASE",
    "horizon_year": 2035
  },
  "assumptions_used": [
    {
      "param_group": "Q2",
      "param_name": "exclude_year_2022",
      "param_value": 0.0,
      "unit": "bool",
      "description": "Exclude 2022 from regressions (1=yes)",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q2",
      "param_name": "min_points_regression",
      "param_value": 3.0,
      "unit": "count",
      "description": "Nombre minimal de points regression",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    }
  ],
  "kpis": {
    "n_slopes": 14,
    "n_robust": 2
  },
  "checks": [
    {
      "status": "WARN",
      "code": "Q2_POSITIVE_ROBUST_SLOPE",
      "message": "ES-WIND: pente robuste positive (exception possible meteo/structure)."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%]."
    }
  ],
  "warnings": [
    "CZ-PV: bascule Q1 absente, pente non calculee.",
    "CZ-WIND: bascule Q1 absente, pente non calculee.",
    "DE-PV: bascule Q1 absente, pente non calculee.",
    "DE-WIND: bascule Q1 absente, pente non calculee.",
    "FR-PV: bascule Q1 absente, pente non calculee.",
    "FR-WIND: bascule Q1 absente, pente non calculee.",
    "IT_NORD-PV: bascule Q1 absente, pente non calculee.",
    "IT_NORD-WIND: bascule Q1 absente, pente non calculee.",
    "NL-PV: bascule Q1 absente, pente non calculee.",
    "NL-WIND: bascule Q1 absente, pente non calculee."
  ],
  "mode": "SCEN",
  "scenario_id": "BASE",
  "horizon_year": 2035
}
```

#### Narratif (BASE)
Q2 estime la pente de cannibalisation sur la fenetre post-bascule Q1 (phase 2), en excluant annees de crise et qualite insuffisante; OLS si n>=3, two-point delta si n=2.

#### Table SCEN BASE `Q2/scen/BASE/tables/Q2_country_slopes.csv`
Lignes totales: `14` | Lignes DE/ES: `4`

##### DE (2 lignes)
```csv
country,tech,phase2_start_year_for_slope,phase2_start_reason,phase2_end_year,years_used,n_points,x_axis_used,x_unit,slope,intercept,r2,p_value,n,slope_method,method,insufficient_points,robust_flag,reason_code,outlier_years_count,slope_all_years,slope_excluding_outliers,mean_sr_energy_phase2,mean_far_energy_phase2,mean_ir_p10_phase2,mean_ttl_phase2,vre_load_corr_phase2,surplus_load_trough_share_phase2
DE,PV,,q1_no_bascule,,nan,0,none,pct_point,,,,,0,none,none,True,NON_TESTABLE,q1_no_bascule,0,,,,,,,,
DE,WIND,,q1_no_bascule,,nan,0,none,pct_point,,,,,0,none,none,True,NON_TESTABLE,q1_no_bascule,0,,,,,,,,
```

##### ES (2 lignes)
```csv
country,tech,phase2_start_year_for_slope,phase2_start_reason,phase2_end_year,years_used,n_points,x_axis_used,x_unit,slope,intercept,r2,p_value,n,slope_method,method,insufficient_points,robust_flag,reason_code,outlier_years_count,slope_all_years,slope_excluding_outliers,mean_sr_energy_phase2,mean_far_energy_phase2,mean_ir_p10_phase2,mean_ttl_phase2,vre_load_corr_phase2,surplus_load_trough_share_phase2
ES,PV,2025,q1_bascule_pv,2035,"2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035",11,pv_penetration_pct_gen,pct_point,-0.000446851,0.939936,0.90945,5.43903e-06,11,ols,ols,False,ROBUST,ok,0,-0.000446851,-0.000446851,0,1,0.0824223,162.177,,
ES,WIND,2025,q1_bascule_wind,2035,"2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035",11,wind_penetration_pct_gen,pct_point,0.00226091,0.886224,0.963525,8.87845e-08,11,ols,ols,False,ROBUST,ok,0,0.00226091,0.00226091,0,1,0.0824223,162.177,,
```


#### Table SCEN BASE `Q2/scen/BASE/tables/Q2_driver_correlations.csv`
Lignes: `4`

```csv
driver_name,corr_with_slope_pv,corr_with_slope_wind,n_countries,expected_sign,sign_conflict_share
far_energy,,,7,,0
ir_p10,1,,7,,0
sr_energy,,,7,,0
vre_penetration_share_gen,-1,,7,,0
```


#### Table SCEN BASE `Q2/scen/BASE/tables/Q2_driver_diagnostics.csv`
Lignes totales: `28` | Lignes DE/ES: `8`

##### DE (4 lignes)
```csv
country,driver_name,corr_capture_pv,elasticity_capture_pv,expected_sign,observed_sign,sign_conflict
DE,sr_energy,,,,0,False
DE,far_energy,,,,0,False
DE,vre_penetration_share_gen,,,,0,False
DE,ir_p10,,,,0,False
```

##### ES (4 lignes)
```csv
country,driver_name,corr_capture_pv,elasticity_capture_pv,expected_sign,observed_sign,sign_conflict
ES,sr_energy,,,,0,False
ES,far_energy,,,,0,False
ES,vre_penetration_share_gen,-0.949979,-0.0219845,,-1,False
ES,ir_p10,0.95304,0.00563195,,1,False
```


#### Scenario `HIGH_CO2`

#### Summary (HIGH_CO2)
```json
{
  "module_id": "Q2",
  "run_id": "FULL_20260211_191955_HIGH_CO2",
  "selection": {
    "countries": [
      "FR",
      "DE",
      "ES",
      "NL",
      "BE",
      "CZ",
      "IT_NORD"
    ],
    "years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "scenario_ids": [
      "BASE",
      "HIGH_CO2",
      "HIGH_GAS"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955",
    "mode": "SCEN",
    "scenario_id": "HIGH_CO2",
    "horizon_year": 2035
  },
  "assumptions_used": [
    {
      "param_group": "Q2",
      "param_name": "exclude_year_2022",
      "param_value": 0.0,
      "unit": "bool",
      "description": "Exclude 2022 from regressions (1=yes)",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q2",
      "param_name": "min_points_regression",
      "param_value": 3.0,
      "unit": "count",
      "description": "Nombre minimal de points regression",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    }
  ],
  "kpis": {
    "n_slopes": 14,
    "n_robust": 2
  },
  "checks": [
    {
      "status": "WARN",
      "code": "Q2_POSITIVE_ROBUST_SLOPE",
      "message": "ES-WIND: pente robuste positive (exception possible meteo/structure)."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%]."
    }
  ],
  "warnings": [
    "CZ-PV: bascule Q1 absente, pente non calculee.",
    "CZ-WIND: bascule Q1 absente, pente non calculee.",
    "DE-PV: bascule Q1 absente, pente non calculee.",
    "DE-WIND: bascule Q1 absente, pente non calculee.",
    "FR-PV: bascule Q1 absente, pente non calculee.",
    "FR-WIND: bascule Q1 absente, pente non calculee.",
    "IT_NORD-PV: bascule Q1 absente, pente non calculee.",
    "IT_NORD-WIND: bascule Q1 absente, pente non calculee.",
    "NL-PV: bascule Q1 absente, pente non calculee.",
    "NL-WIND: bascule Q1 absente, pente non calculee."
  ],
  "mode": "SCEN",
  "scenario_id": "HIGH_CO2",
  "horizon_year": 2035
}
```

#### Narratif (HIGH_CO2)
Q2 estime la pente de cannibalisation sur la fenetre post-bascule Q1 (phase 2), en excluant annees de crise et qualite insuffisante; OLS si n>=3, two-point delta si n=2.

#### Table SCEN HIGH_CO2 `Q2/scen/HIGH_CO2/tables/Q2_country_slopes.csv`
Lignes totales: `14` | Lignes DE/ES: `4`

##### DE (2 lignes)
```csv
country,tech,phase2_start_year_for_slope,phase2_start_reason,phase2_end_year,years_used,n_points,x_axis_used,x_unit,slope,intercept,r2,p_value,n,slope_method,method,insufficient_points,robust_flag,reason_code,outlier_years_count,slope_all_years,slope_excluding_outliers,mean_sr_energy_phase2,mean_far_energy_phase2,mean_ir_p10_phase2,mean_ttl_phase2,vre_load_corr_phase2,surplus_load_trough_share_phase2
DE,PV,,q1_no_bascule,,nan,0,none,pct_point,,,,,0,none,none,True,NON_TESTABLE,q1_no_bascule,0,,,,,,,,
DE,WIND,,q1_no_bascule,,nan,0,none,pct_point,,,,,0,none,none,True,NON_TESTABLE,q1_no_bascule,0,,,,,,,,
```

##### ES (2 lignes)
```csv
country,tech,phase2_start_year_for_slope,phase2_start_reason,phase2_end_year,years_used,n_points,x_axis_used,x_unit,slope,intercept,r2,p_value,n,slope_method,method,insufficient_points,robust_flag,reason_code,outlier_years_count,slope_all_years,slope_excluding_outliers,mean_sr_energy_phase2,mean_far_energy_phase2,mean_ir_p10_phase2,mean_ttl_phase2,vre_load_corr_phase2,surplus_load_trough_share_phase2
ES,PV,2025,q1_bascule_pv,2035,"2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035",11,pv_penetration_pct_gen,pct_point,-0.000308119,0.93812,0.832975,8.85803e-05,11,ols,ols,False,ROBUST,ok,0,-0.000308119,-0.000308119,0,1,0.0824223,167.962,,
ES,WIND,2025,q1_bascule_wind,2035,"2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035",11,wind_penetration_pct_gen,pct_point,0.00231496,0.88479,0.96746,5.30328e-08,11,ols,ols,False,ROBUST,ok,0,0.00231496,0.00231496,0,1,0.0824223,167.962,,
```


#### Table SCEN HIGH_CO2 `Q2/scen/HIGH_CO2/tables/Q2_driver_correlations.csv`
Lignes: `4`

```csv
driver_name,corr_with_slope_pv,corr_with_slope_wind,n_countries,expected_sign,sign_conflict_share
far_energy,,,7,,0
ir_p10,1,,7,,0
sr_energy,,,7,,0
vre_penetration_share_gen,-1,,7,,0
```


#### Table SCEN HIGH_CO2 `Q2/scen/HIGH_CO2/tables/Q2_driver_diagnostics.csv`
Lignes totales: `28` | Lignes DE/ES: `8`

##### DE (4 lignes)
```csv
country,driver_name,corr_capture_pv,elasticity_capture_pv,expected_sign,observed_sign,sign_conflict
DE,sr_energy,,,,0,False
DE,far_energy,,,,0,False
DE,vre_penetration_share_gen,,,,0,False
DE,ir_p10,,,,0,False
```

##### ES (4 lignes)
```csv
country,driver_name,corr_capture_pv,elasticity_capture_pv,expected_sign,observed_sign,sign_conflict
ES,sr_energy,,,,0,False
ES,far_energy,,,,0,False
ES,vre_penetration_share_gen,-0.907743,-0.0151068,,-1,False
ES,ir_p10,0.912052,0.00387591,,1,False
```


#### Scenario `HIGH_GAS`

#### Summary (HIGH_GAS)
```json
{
  "module_id": "Q2",
  "run_id": "FULL_20260211_191955_HIGH_GAS",
  "selection": {
    "countries": [
      "FR",
      "DE",
      "ES",
      "NL",
      "BE",
      "CZ",
      "IT_NORD"
    ],
    "years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "scenario_ids": [
      "BASE",
      "HIGH_CO2",
      "HIGH_GAS"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955",
    "mode": "SCEN",
    "scenario_id": "HIGH_GAS",
    "horizon_year": 2035
  },
  "assumptions_used": [
    {
      "param_group": "Q2",
      "param_name": "exclude_year_2022",
      "param_value": 0.0,
      "unit": "bool",
      "description": "Exclude 2022 from regressions (1=yes)",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q2",
      "param_name": "min_points_regression",
      "param_value": 3.0,
      "unit": "count",
      "description": "Nombre minimal de points regression",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    }
  ],
  "kpis": {
    "n_slopes": 14,
    "n_robust": 2
  },
  "checks": [
    {
      "status": "WARN",
      "code": "Q2_POSITIVE_ROBUST_SLOPE",
      "message": "ES-WIND: pente robuste positive (exception possible meteo/structure)."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%]."
    }
  ],
  "warnings": [
    "CZ-PV: bascule Q1 absente, pente non calculee.",
    "CZ-WIND: bascule Q1 absente, pente non calculee.",
    "DE-PV: bascule Q1 absente, pente non calculee.",
    "DE-WIND: bascule Q1 absente, pente non calculee.",
    "FR-PV: bascule Q1 absente, pente non calculee.",
    "FR-WIND: bascule Q1 absente, pente non calculee.",
    "IT_NORD-PV: bascule Q1 absente, pente non calculee.",
    "IT_NORD-WIND: bascule Q1 absente, pente non calculee.",
    "NL-PV: bascule Q1 absente, pente non calculee.",
    "NL-WIND: bascule Q1 absente, pente non calculee."
  ],
  "mode": "SCEN",
  "scenario_id": "HIGH_GAS",
  "horizon_year": 2035
}
```

#### Narratif (HIGH_GAS)
Q2 estime la pente de cannibalisation sur la fenetre post-bascule Q1 (phase 2), en excluant annees de crise et qualite insuffisante; OLS si n>=3, two-point delta si n=2.

#### Table SCEN HIGH_GAS `Q2/scen/HIGH_GAS/tables/Q2_country_slopes.csv`
Lignes totales: `14` | Lignes DE/ES: `4`

##### DE (2 lignes)
```csv
country,tech,phase2_start_year_for_slope,phase2_start_reason,phase2_end_year,years_used,n_points,x_axis_used,x_unit,slope,intercept,r2,p_value,n,slope_method,method,insufficient_points,robust_flag,reason_code,outlier_years_count,slope_all_years,slope_excluding_outliers,mean_sr_energy_phase2,mean_far_energy_phase2,mean_ir_p10_phase2,mean_ttl_phase2,vre_load_corr_phase2,surplus_load_trough_share_phase2
DE,PV,,q1_no_bascule,,nan,0,none,pct_point,,,,,0,none,none,True,NON_TESTABLE,q1_no_bascule,0,,,,,,,,
DE,WIND,,q1_no_bascule,,nan,0,none,pct_point,,,,,0,none,none,True,NON_TESTABLE,q1_no_bascule,0,,,,,,,,
```

##### ES (2 lignes)
```csv
country,tech,phase2_start_year_for_slope,phase2_start_reason,phase2_end_year,years_used,n_points,x_axis_used,x_unit,slope,intercept,r2,p_value,n,slope_method,method,insufficient_points,robust_flag,reason_code,outlier_years_count,slope_all_years,slope_excluding_outliers,mean_sr_energy_phase2,mean_far_energy_phase2,mean_ir_p10_phase2,mean_ttl_phase2,vre_load_corr_phase2,surplus_load_trough_share_phase2
ES,PV,2025,q1_bascule_pv,2035,"2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035",11,pv_penetration_pct_gen,pct_point,-0.000292372,0.939805,0.826872,0.000104412,11,ols,ols,False,ROBUST,ok,0,-0.000292372,-0.000292372,0,1,0.0824223,175.541,,
ES,WIND,2025,q1_bascule_wind,2035,"2025,2026,2027,2028,2029,2030,2031,2032,2033,2034,2035",11,wind_penetration_pct_gen,pct_point,0.00224312,0.888311,0.967292,5.42778e-08,11,ols,ols,False,ROBUST,ok,0,0.00224312,0.00224312,0,1,0.0824223,175.541,,
```


#### Table SCEN HIGH_GAS `Q2/scen/HIGH_GAS/tables/Q2_driver_correlations.csv`
Lignes: `4`

```csv
driver_name,corr_with_slope_pv,corr_with_slope_wind,n_countries,expected_sign,sign_conflict_share
far_energy,,,7,,0
ir_p10,1,,7,,0
sr_energy,,,7,,0
vre_penetration_share_gen,-1,,7,,0
```


#### Table SCEN HIGH_GAS `Q2/scen/HIGH_GAS/tables/Q2_driver_diagnostics.csv`
Lignes totales: `28` | Lignes DE/ES: `8`

##### DE (4 lignes)
```csv
country,driver_name,corr_capture_pv,elasticity_capture_pv,expected_sign,observed_sign,sign_conflict
DE,sr_energy,,,,0,False
DE,far_energy,,,,0,False
DE,vre_penetration_share_gen,,,,0,False
DE,ir_p10,,,,0,False
```

##### ES (4 lignes)
```csv
country,driver_name,corr_capture_pv,elasticity_capture_pv,expected_sign,observed_sign,sign_conflict
ES,sr_energy,,,,0,False
ES,far_energy,,,,0,False
ES,vre_penetration_share_gen,-0.90432,-0.0143011,,-1,False
ES,ir_p10,0.908737,0.0036697,,1,False
```


## Q3

### GLOBAL

#### Summary (question)
```json
{
  "question_id": "Q3",
  "run_id": "FULL_20260211_191955",
  "selection": {
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "years": [
      2018,
      2019,
      2020,
      2021,
      2022,
      2023,
      2024
    ],
    "scenario_ids": [
      "BASE",
      "DEMAND_UP",
      "FLEX_UP",
      "LOW_RIGIDITY"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ]
  },
  "hist_module_id": "Q3",
  "scenarios": [
    "BASE",
    "DEMAND_UP",
    "FLEX_UP",
    "LOW_RIGIDITY"
  ],
  "n_checks": 167,
  "n_warnings": 0,
  "n_test_rows": 10,
  "n_compare_rows": 56,
  "checks": [
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "CZ-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=6181.66, p10_load_mw=5946.48.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "CZ-2018: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2018: must_run_share=79.3% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2019: must_run_share=78.2% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2020: must_run_share=76.3% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2021: must_run_share=76.1% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "CZ-2022: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=5874.35, p10_load_mw=5645.40.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "CZ-2022: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2022: must_run_share=79.6% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2023: must_run_share=79.6% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2024: must_run_share=78.6% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41354.50, p10_load_mw=39303.40.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2018: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2018: must_run_share=82.4% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2019: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=40635.00, p10_load_mw=39530.00.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2019: must_run_share=80.7% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2020: must_run_share=77.9% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2021: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41252.00, p10_load_mw=39284.00.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2021: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2021: must_run_share=79.4% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2022: must_run_share=73.5% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2023: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2023: must_run_share=75.9% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2024: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=39406.20, p10_load_mw=37062.60.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2024: regime_coherence < 0.55.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2024: must_run_share=79.2% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2018: must_run_share=0.0% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2019: must_run_share=0.0% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2020: must_run_share=0.1% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2021: must_run_share=0.1% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2022: must_run_share=0.1% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2023: must_run_share=0.2% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2024: must_run_share=0.2% hors plage plausible [5%,60%].",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "DEMAND_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=68.0% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=67.9% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=67.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=67.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=67.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=67.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=67.3% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=67.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=67.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=67.0% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=66.9% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=62.8% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=62.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=62.7% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=62.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=62.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=62.5% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=62.4% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=62.3% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=62.2% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=62.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=62.1% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.6% hors plage plausible [5%,60%].",
      "scope": "SCEN",
      "scenario_id": "LOW_RIGIDITY"
    },
    {
      "status": "PASS",
      "code": "BUNDLE_LEDGER_STATUS",
      "message": "ledger: FAIL=0, WARN=0",
      "scope": "BUNDLE",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "BUNDLE_INFORMATIVENESS",
      "message": "share_tests_informatifs=100.00% ; share_compare_informatifs=16.07%",
      "scope": "BUNDLE",
      "scenario_id": ""
    }
  ],
  "warnings": []
}
```

#### Narratif (question)
Analyse complete Q3: historique + prospectif en un seul run. Statut global=WARN. Tests PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0. Les resultats sont separes entre historique et scenarios, puis compares dans une table unique.

#### Table `Q3/test_ledger.csv`
Lignes: `10`

```csv
test_id,question_id,source_ref,mode,scenario_group,title,what_is_tested,metric_rule,severity_if_fail,scenario_id,status,value,threshold,interpretation
Q3-S-01,Q3,SPEC2-Q3/Slides 17,SCEN,DEFAULT,Conditions minimales d'inversion,Les besoins demande/must-run/flex sont quantifies en scenario.,"inversion_k, inversion_r et additional_absorbed presentes",HIGH,BASE,PASS,7,colonnes inversion presentes,Les ordres de grandeur d'inversion sont quantifies.
Q3-S-02,Q3,Slides 17-19,SCEN,DEFAULT,Validation entree phase 3,Le statut prospectif est interpretable pour la transition phase 3.,status non vide en SCEN,MEDIUM,BASE,PASS,3,status renseignes,La lecture de transition phase 3 est possible.
Q3-S-01,Q3,SPEC2-Q3/Slides 17,SCEN,DEFAULT,Conditions minimales d'inversion,Les besoins demande/must-run/flex sont quantifies en scenario.,"inversion_k, inversion_r et additional_absorbed presentes",HIGH,DEMAND_UP,PASS,7,colonnes inversion presentes,Les ordres de grandeur d'inversion sont quantifies.
Q3-S-02,Q3,Slides 17-19,SCEN,DEFAULT,Validation entree phase 3,Le statut prospectif est interpretable pour la transition phase 3.,status non vide en SCEN,MEDIUM,DEMAND_UP,PASS,3,status renseignes,La lecture de transition phase 3 est possible.
Q3-S-01,Q3,SPEC2-Q3/Slides 17,SCEN,DEFAULT,Conditions minimales d'inversion,Les besoins demande/must-run/flex sont quantifies en scenario.,"inversion_k, inversion_r et additional_absorbed presentes",HIGH,FLEX_UP,PASS,7,colonnes inversion presentes,Les ordres de grandeur d'inversion sont quantifies.
Q3-S-02,Q3,Slides 17-19,SCEN,DEFAULT,Validation entree phase 3,Le statut prospectif est interpretable pour la transition phase 3.,status non vide en SCEN,MEDIUM,FLEX_UP,PASS,3,status renseignes,La lecture de transition phase 3 est possible.
Q3-S-01,Q3,SPEC2-Q3/Slides 17,SCEN,DEFAULT,Conditions minimales d'inversion,Les besoins demande/must-run/flex sont quantifies en scenario.,"inversion_k, inversion_r et additional_absorbed presentes",HIGH,LOW_RIGIDITY,PASS,7,colonnes inversion presentes,Les ordres de grandeur d'inversion sont quantifies.
Q3-S-02,Q3,Slides 17-19,SCEN,DEFAULT,Validation entree phase 3,Le statut prospectif est interpretable pour la transition phase 3.,status non vide en SCEN,MEDIUM,LOW_RIGIDITY,PASS,3,status renseignes,La lecture de transition phase 3 est possible.
Q3-H-01,Q3,SPEC2-Q3/Slides 16,HIST,HIST_BASE,Tendances glissantes,Les tendances h_negative et capture_ratio sont estimees.,Q3_status non vide,HIGH,nan,PASS,7,>0 lignes,Les tendances historiques sont calculees.
Q3-H-02,Q3,SPEC2-Q3,HIST,HIST_BASE,Statuts sortie phase 2,Les statuts degradation/stabilisation/amelioration sont attribues.,status dans ensemble attendu,MEDIUM,nan,PASS,3,status valides,Les statuts business sont renseignes.
```


#### Table `Q3/comparison_hist_vs_scen.csv`
Lignes totales: `56` | Lignes DE/ES: `16`

##### DE (8 lignes)
```csv
country,scenario_id,metric,hist_value,scen_value,delta,hist_status,scen_status,interpretability_status,interpretability_reason
DE,BASE,inversion_k_demand,0,0,0,CONTINUES,BACK_TO_STAGE1,FRAGILE,delta_quasi_nul_vs_historique
DE,BASE,inversion_r_mustrun,,,,CONTINUES,BACK_TO_STAGE1,NON_TESTABLE,delta_non_interpretable_nan
DE,DEMAND_UP,inversion_k_demand,0,0,0,CONTINUES,BACK_TO_STAGE1,FRAGILE,delta_quasi_nul_vs_historique
DE,DEMAND_UP,inversion_r_mustrun,,,,CONTINUES,BACK_TO_STAGE1,NON_TESTABLE,delta_non_interpretable_nan
DE,FLEX_UP,inversion_k_demand,0,0,0,CONTINUES,BACK_TO_STAGE1,FRAGILE,delta_quasi_nul_vs_historique
DE,FLEX_UP,inversion_r_mustrun,,,,CONTINUES,BACK_TO_STAGE1,NON_TESTABLE,delta_non_interpretable_nan
DE,LOW_RIGIDITY,inversion_k_demand,0,0,0,CONTINUES,BACK_TO_STAGE1,FRAGILE,delta_quasi_nul_vs_historique
DE,LOW_RIGIDITY,inversion_r_mustrun,,,,CONTINUES,BACK_TO_STAGE1,NON_TESTABLE,delta_non_interpretable_nan
```

##### ES (8 lignes)
```csv
country,scenario_id,metric,hist_value,scen_value,delta,hist_status,scen_status,interpretability_status,interpretability_reason
ES,BASE,inversion_k_demand,0.0053734,0,-0.0053734,CONTINUES,STOP_CONFIRMED,INFORMATIVE,delta_interpretable
ES,BASE,inversion_r_mustrun,,,,CONTINUES,STOP_CONFIRMED,NON_TESTABLE,delta_non_interpretable_nan
ES,DEMAND_UP,inversion_k_demand,0.0053734,0,-0.0053734,CONTINUES,STOP_CONFIRMED,INFORMATIVE,delta_interpretable
ES,DEMAND_UP,inversion_r_mustrun,,,,CONTINUES,STOP_CONFIRMED,NON_TESTABLE,delta_non_interpretable_nan
ES,FLEX_UP,inversion_k_demand,0.0053734,0,-0.0053734,CONTINUES,STOP_CONFIRMED,INFORMATIVE,delta_interpretable
ES,FLEX_UP,inversion_r_mustrun,,,,CONTINUES,STOP_CONFIRMED,NON_TESTABLE,delta_non_interpretable_nan
ES,LOW_RIGIDITY,inversion_k_demand,0.0053734,0,-0.0053734,CONTINUES,STOP_CONFIRMED,INFORMATIVE,delta_interpretable
ES,LOW_RIGIDITY,inversion_r_mustrun,,,,CONTINUES,STOP_CONFIRMED,NON_TESTABLE,delta_non_interpretable_nan
```


### HIST

#### Summary (hist)
```json
{
  "module_id": "Q3",
  "run_id": "FULL_20260211_191955_HIST",
  "selection": {
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "years": [
      2018,
      2019,
      2020,
      2021,
      2022,
      2023,
      2024
    ],
    "scenario_ids": [
      "BASE",
      "DEMAND_UP",
      "FLEX_UP",
      "LOW_RIGIDITY"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "mode": "HIST",
    "run_id": "FULL_20260211_191955"
  },
  "assumptions_used": [
    {
      "param_group": "Q3",
      "param_name": "demand_k_max",
      "param_value": 0.3,
      "unit": "ratio",
      "description": "Borne max hausse demande",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "far_target",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Cible FAR inversion",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "require_recent_stage2",
      "param_value": 1.0,
      "unit": "bool",
      "description": "Require recent stage2 stress",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "sr_energy_target",
      "param_value": 0.01,
      "unit": "ratio",
      "description": "Cible SR inversion",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "stage2_recent_h_negative_min",
      "param_value": 200.0,
      "unit": "hours",
      "description": "Recent stage2 threshold on negative hours",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "trend_capture_ratio_min",
      "param_value": 0.0,
      "unit": "ratio/year",
      "description": "Improvement threshold for capture trend",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "trend_h_negative_max",
      "param_value": -10.0,
      "unit": "hours/year",
      "description": "Improvement threshold for h_negative trend",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "trend_window_years",
      "param_value": 3.0,
      "unit": "years",
      "description": "Fenetre tendance Q3",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "h_negative_target",
      "param_value": 100.0,
      "unit": "hours",
      "description": "Target max negative hours for phase3 inversion proxy",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "h_below_5_target",
      "param_value": 300.0,
      "unit": "hours",
      "description": "Target max hours below 5 EUR/MWh for phase3 inversion proxy",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "slope_capture_target",
      "param_value": 0.0,
      "unit": "ratio/year",
      "description": "Target minimum capture-ratio slope for phase3 trend status",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "stage2_recent_h_negative_min_scen",
      "param_value": 80.0,
      "unit": "h/an",
      "description": "Q3 SCEN: seuil h_negative recent pour qualifier un contexte Stage2 en prospectif.",
      "source": "codex_adjustment",
      "last_updated": "2026-02-10",
      "owner": "codex"
    },
    {
      "param_group": "Q3",
      "param_name": "stage2_recent_sr_energy_min_scen",
      "param_value": 0.02,
      "unit": "ratio",
      "description": "Q3 SCEN: seuil SR recent pour qualifier un contexte Stage2 meme si h_negative reste faible.",
      "source": "codex_adjustment",
      "last_updated": "2026-02-10",
      "owner": "codex"
    }
  ],
  "kpis": {
    "n_countries": 7,
    "n_in_phase2": 6,
    "n_stop_possible": 0,
    "n_stop_confirmed": 1
  },
  "checks": [
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "CZ-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=6181.66, p10_load_mw=5946.48."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "CZ-2018: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2018: must_run_share=79.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2019: must_run_share=78.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2020: must_run_share=76.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2021: must_run_share=76.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "CZ-2022: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=5874.35, p10_load_mw=5645.40."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "CZ-2022: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2022: must_run_share=79.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2023: must_run_share=79.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2024: must_run_share=78.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2018: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41354.50, p10_load_mw=39303.40."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2018: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2018: must_run_share=82.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2019: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=40635.00, p10_load_mw=39530.00."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2019: must_run_share=80.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2020: must_run_share=77.9% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2021: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=41252.00, p10_load_mw=39284.00."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2021: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2021: must_run_share=79.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2022: must_run_share=73.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2023: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2023: must_run_share=75.9% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_IR_GT_1",
      "message": "FR-2024: IR > 1 (must-run tres eleve en creux). p10_must_run_mw=39406.20, p10_load_mw=37062.60."
    },
    {
      "status": "WARN",
      "code": "RC_LOW_REGIME_COHERENCE",
      "message": "FR-2024: regime_coherence < 0.55."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "FR-2024: must_run_share=79.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2018: must_run_share=0.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2019: must_run_share=0.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2020: must_run_share=0.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2021: must_run_share=0.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2022: must_run_share=0.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2023: must_run_share=0.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2024: must_run_share=0.2% hors plage plausible [5%,60%]."
    }
  ],
  "warnings": [],
  "mode": "HIST",
  "scenario_id": null,
  "horizon_year": null
}
```

#### Narratif (hist)
Q3 compare les familles actives a la bascule avec l'etat courant et classe CONTINUES / STOP_POSSIBLE / STOP_CONFIRMED / BACK_TO_STAGE1. En mode SCEN, la bascule historique est prioritaire comme reference.

#### Table HIST `Q3/hist/tables/Q3_status.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,reference_year,in_phase2,status,reason_code,status_explanation,stage3_ready_year,phase2_slope_capture_ratio_pv,phase2_slope_method,trend_capture_ratio_pv,trend_h_negative,stop_possible_if,stop_condition_detail,surplus_energy_twh_recent,target_absorption_twh,demand_uplift_twh,inversion_k_demand,inversion_k_demand_status,inversion_r_mustrun,inversion_r_mustrun_status,inversion_f_flex,inversion_f_flex_status,additional_absorbed_needed_TWh_year,additional_sink_power_p95_mw,warnings_quality,bascule_reference_year,bascule_reference_source,families_active_at_bascule,turned_off_low_price,turned_off_physical,turned_off_value_pv,turned_off_value_wind,turned_off_family_any,turned_off_family_persistent_2y,q2_slope_above_target
DE,2024,True,CONTINUES,no_family_turned_off,Aucune famille active a la bascule n'est eteinte.,False,-0.0318441,ols,-0.0634213,106,False,none,2.94844,4.70357,0,0,proxy_from_surplus_gap,,proxy_not_computed,,proxy_not_computed,0,0,nan,2019,current_mode,"LOW_PRICE,VALUE_WIND",False,False,False,False,False,False,False
```

##### ES (1 lignes)
```csv
country,reference_year,in_phase2,status,reason_code,status_explanation,stage3_ready_year,phase2_slope_capture_ratio_pv,phase2_slope_method,trend_capture_ratio_pv,trend_h_negative,stop_possible_if,stop_condition_detail,surplus_energy_twh_recent,target_absorption_twh,demand_uplift_twh,inversion_k_demand,inversion_k_demand_status,inversion_r_mustrun,inversion_r_mustrun_status,inversion_f_flex,inversion_f_flex_status,additional_absorbed_needed_TWh_year,additional_sink_power_p95_mw,warnings_quality,bascule_reference_year,bascule_reference_source,families_active_at_bascule,turned_off_low_price,turned_off_physical,turned_off_value_pv,turned_off_value_wind,turned_off_family_any,turned_off_family_persistent_2y,q2_slope_above_target
ES,2024,True,CONTINUES,no_family_turned_off,Aucune famille active a la bascule n'est eteinte.,False,-0.0532886,two_point,-0.159938,247,False,none,3.56701,2.32025,1.24676,0.0053734,proxy_from_surplus_gap,,proxy_not_computed,,proxy_not_computed,1.24676,0,nan,2023,current_mode,"LOW_PRICE,PHYSICAL,VALUE_WIND",False,False,False,False,False,False,False
```


### SCEN

#### Scenario `BASE`

#### Summary (BASE)
```json
{
  "module_id": "Q3",
  "run_id": "FULL_20260211_191955_BASE",
  "selection": {
    "countries": [
      "FR",
      "DE",
      "ES",
      "NL",
      "BE",
      "CZ",
      "IT_NORD"
    ],
    "years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "scenario_ids": [
      "BASE",
      "DEMAND_UP",
      "FLEX_UP",
      "LOW_RIGIDITY"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955",
    "mode": "SCEN",
    "scenario_id": "BASE",
    "horizon_year": 2035
  },
  "assumptions_used": [
    {
      "param_group": "Q3",
      "param_name": "demand_k_max",
      "param_value": 0.3,
      "unit": "ratio",
      "description": "Borne max hausse demande",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "far_target",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Cible FAR inversion",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "require_recent_stage2",
      "param_value": 1.0,
      "unit": "bool",
      "description": "Require recent stage2 stress",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "sr_energy_target",
      "param_value": 0.01,
      "unit": "ratio",
      "description": "Cible SR inversion",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "stage2_recent_h_negative_min",
      "param_value": 200.0,
      "unit": "hours",
      "description": "Recent stage2 threshold on negative hours",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "trend_capture_ratio_min",
      "param_value": 0.0,
      "unit": "ratio/year",
      "description": "Improvement threshold for capture trend",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "trend_h_negative_max",
      "param_value": -10.0,
      "unit": "hours/year",
      "description": "Improvement threshold for h_negative trend",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "trend_window_years",
      "param_value": 3.0,
      "unit": "years",
      "description": "Fenetre tendance Q3",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "h_negative_target",
      "param_value": 100.0,
      "unit": "hours",
      "description": "Target max negative hours for phase3 inversion proxy",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "h_below_5_target",
      "param_value": 300.0,
      "unit": "hours",
      "description": "Target max hours below 5 EUR/MWh for phase3 inversion proxy",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "slope_capture_target",
      "param_value": 0.0,
      "unit": "ratio/year",
      "description": "Target minimum capture-ratio slope for phase3 trend status",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "stage2_recent_h_negative_min_scen",
      "param_value": 80.0,
      "unit": "h/an",
      "description": "Q3 SCEN: seuil h_negative recent pour qualifier un contexte Stage2 en prospectif.",
      "source": "codex_adjustment",
      "last_updated": "2026-02-10",
      "owner": "codex"
    },
    {
      "param_group": "Q3",
      "param_name": "stage2_recent_sr_energy_min_scen",
      "param_value": 0.02,
      "unit": "ratio",
      "description": "Q3 SCEN: seuil SR recent pour qualifier un contexte Stage2 meme si h_negative reste faible.",
      "source": "codex_adjustment",
      "last_updated": "2026-02-10",
      "owner": "codex"
    }
  ],
  "kpis": {
    "n_countries": 7,
    "n_in_phase2": 6,
    "n_stop_possible": 0,
    "n_stop_confirmed": 3
  },
  "checks": [
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%]."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "BASE",
  "horizon_year": 2035
}
```

#### Narratif (BASE)
Q3 compare les familles actives a la bascule avec l'etat courant et classe CONTINUES / STOP_POSSIBLE / STOP_CONFIRMED / BACK_TO_STAGE1. En mode SCEN, la bascule historique est prioritaire comme reference.

#### Table SCEN BASE `Q3/scen/BASE/tables/Q3_status.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,reference_year,in_phase2,status,reason_code,status_explanation,stage3_ready_year,phase2_slope_capture_ratio_pv,phase2_slope_method,trend_capture_ratio_pv,trend_h_negative,stop_possible_if,stop_condition_detail,surplus_energy_twh_recent,target_absorption_twh,demand_uplift_twh,inversion_k_demand,inversion_k_demand_status,inversion_r_mustrun,inversion_r_mustrun_status,inversion_f_flex,inversion_f_flex_status,additional_absorbed_needed_TWh_year,additional_sink_power_p95_mw,warnings_quality,bascule_reference_year,bascule_reference_source,families_active_at_bascule,turned_off_low_price,turned_off_physical,turned_off_value_pv,turned_off_value_wind,turned_off_family_any,turned_off_family_persistent_2y,q2_slope_above_target
DE,2035,True,BACK_TO_STAGE1,all_families_turned_off,Toutes les familles actives a la bascule sont eteintes.,True,,none,-8.14809e-05,0,True,LOW_PRICE;VALUE_WIND,0,5.70154,0,0,proxy_from_surplus_gap,,proxy_not_computed,,proxy_not_computed,0,0,nan,2019,historical,"LOW_PRICE,VALUE_WIND",True,False,False,True,True,True,False
```

##### ES (1 lignes)
```csv
country,reference_year,in_phase2,status,reason_code,status_explanation,stage3_ready_year,phase2_slope_capture_ratio_pv,phase2_slope_method,trend_capture_ratio_pv,trend_h_negative,stop_possible_if,stop_condition_detail,surplus_energy_twh_recent,target_absorption_twh,demand_uplift_twh,inversion_k_demand,inversion_k_demand_status,inversion_r_mustrun,inversion_r_mustrun_status,inversion_f_flex,inversion_f_flex_status,additional_absorbed_needed_TWh_year,additional_sink_power_p95_mw,warnings_quality,bascule_reference_year,bascule_reference_source,families_active_at_bascule,turned_off_low_price,turned_off_physical,turned_off_value_pv,turned_off_value_wind,turned_off_family_any,turned_off_family_persistent_2y,q2_slope_above_target
ES,2035,True,STOP_CONFIRMED,family_turned_off_confirmed,Au moins une famille basculee est eteinte de facon persistante.,True,-0.000446851,ols,-6.19482e-05,0,True,VALUE_WIND,0,2.77552,0,0,proxy_from_surplus_gap,,proxy_not_computed,,proxy_not_computed,0,0,nan,2023,historical,"LOW_PRICE,PHYSICAL,VALUE_WIND",False,False,False,True,True,True,False
```


#### Scenario `DEMAND_UP`

#### Summary (DEMAND_UP)
```json
{
  "module_id": "Q3",
  "run_id": "FULL_20260211_191955_DEMAND_UP",
  "selection": {
    "countries": [
      "FR",
      "DE",
      "ES",
      "NL",
      "BE",
      "CZ",
      "IT_NORD"
    ],
    "years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "scenario_ids": [
      "BASE",
      "DEMAND_UP",
      "FLEX_UP",
      "LOW_RIGIDITY"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955",
    "mode": "SCEN",
    "scenario_id": "DEMAND_UP",
    "horizon_year": 2035
  },
  "assumptions_used": [
    {
      "param_group": "Q3",
      "param_name": "demand_k_max",
      "param_value": 0.3,
      "unit": "ratio",
      "description": "Borne max hausse demande",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "far_target",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Cible FAR inversion",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "require_recent_stage2",
      "param_value": 1.0,
      "unit": "bool",
      "description": "Require recent stage2 stress",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "sr_energy_target",
      "param_value": 0.01,
      "unit": "ratio",
      "description": "Cible SR inversion",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "stage2_recent_h_negative_min",
      "param_value": 200.0,
      "unit": "hours",
      "description": "Recent stage2 threshold on negative hours",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "trend_capture_ratio_min",
      "param_value": 0.0,
      "unit": "ratio/year",
      "description": "Improvement threshold for capture trend",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "trend_h_negative_max",
      "param_value": -10.0,
      "unit": "hours/year",
      "description": "Improvement threshold for h_negative trend",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "trend_window_years",
      "param_value": 3.0,
      "unit": "years",
      "description": "Fenetre tendance Q3",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "h_negative_target",
      "param_value": 100.0,
      "unit": "hours",
      "description": "Target max negative hours for phase3 inversion proxy",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "h_below_5_target",
      "param_value": 300.0,
      "unit": "hours",
      "description": "Target max hours below 5 EUR/MWh for phase3 inversion proxy",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "slope_capture_target",
      "param_value": 0.0,
      "unit": "ratio/year",
      "description": "Target minimum capture-ratio slope for phase3 trend status",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "stage2_recent_h_negative_min_scen",
      "param_value": 80.0,
      "unit": "h/an",
      "description": "Q3 SCEN: seuil h_negative recent pour qualifier un contexte Stage2 en prospectif.",
      "source": "codex_adjustment",
      "last_updated": "2026-02-10",
      "owner": "codex"
    },
    {
      "param_group": "Q3",
      "param_name": "stage2_recent_sr_energy_min_scen",
      "param_value": 0.02,
      "unit": "ratio",
      "description": "Q3 SCEN: seuil SR recent pour qualifier un contexte Stage2 meme si h_negative reste faible.",
      "source": "codex_adjustment",
      "last_updated": "2026-02-10",
      "owner": "codex"
    }
  ],
  "kpis": {
    "n_countries": 7,
    "n_in_phase2": 6,
    "n_stop_possible": 0,
    "n_stop_confirmed": 2
  },
  "checks": [
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%]."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "DEMAND_UP",
  "horizon_year": 2035
}
```

#### Narratif (DEMAND_UP)
Q3 compare les familles actives a la bascule avec l'etat courant et classe CONTINUES / STOP_POSSIBLE / STOP_CONFIRMED / BACK_TO_STAGE1. En mode SCEN, la bascule historique est prioritaire comme reference.

#### Table SCEN DEMAND_UP `Q3/scen/DEMAND_UP/tables/Q3_status.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,reference_year,in_phase2,status,reason_code,status_explanation,stage3_ready_year,phase2_slope_capture_ratio_pv,phase2_slope_method,trend_capture_ratio_pv,trend_h_negative,stop_possible_if,stop_condition_detail,surplus_energy_twh_recent,target_absorption_twh,demand_uplift_twh,inversion_k_demand,inversion_k_demand_status,inversion_r_mustrun,inversion_r_mustrun_status,inversion_f_flex,inversion_f_flex_status,additional_absorbed_needed_TWh_year,additional_sink_power_p95_mw,warnings_quality,bascule_reference_year,bascule_reference_source,families_active_at_bascule,turned_off_low_price,turned_off_physical,turned_off_value_pv,turned_off_value_wind,turned_off_family_any,turned_off_family_persistent_2y,q2_slope_above_target
DE,2035,True,BACK_TO_STAGE1,all_families_turned_off,Toutes les familles actives a la bascule sont eteintes.,True,,none,-0.000124667,0,True,LOW_PRICE;VALUE_WIND,0,6.27317,0,0,proxy_from_surplus_gap,,proxy_not_computed,,proxy_not_computed,0,0,nan,2019,historical,"LOW_PRICE,VALUE_WIND",True,False,False,True,True,True,False
```

##### ES (1 lignes)
```csv
country,reference_year,in_phase2,status,reason_code,status_explanation,stage3_ready_year,phase2_slope_capture_ratio_pv,phase2_slope_method,trend_capture_ratio_pv,trend_h_negative,stop_possible_if,stop_condition_detail,surplus_energy_twh_recent,target_absorption_twh,demand_uplift_twh,inversion_k_demand,inversion_k_demand_status,inversion_r_mustrun,inversion_r_mustrun_status,inversion_f_flex,inversion_f_flex_status,additional_absorbed_needed_TWh_year,additional_sink_power_p95_mw,warnings_quality,bascule_reference_year,bascule_reference_source,families_active_at_bascule,turned_off_low_price,turned_off_physical,turned_off_value_pv,turned_off_value_wind,turned_off_family_any,turned_off_family_persistent_2y,q2_slope_above_target
ES,2035,True,STOP_CONFIRMED,family_turned_off_confirmed,Au moins une famille basculee est eteinte de facon persistante.,True,-0.000363758,ols,6.52971e-05,0,True,VALUE_WIND,0,3.05443,0,0,proxy_from_surplus_gap,,proxy_not_computed,,proxy_not_computed,0,0,nan,2023,historical,"LOW_PRICE,PHYSICAL,VALUE_WIND",False,False,False,True,True,True,False
```


#### Scenario `FLEX_UP`

#### Summary (FLEX_UP)
```json
{
  "module_id": "Q3",
  "run_id": "FULL_20260211_191955_FLEX_UP",
  "selection": {
    "countries": [
      "FR",
      "DE",
      "ES",
      "NL",
      "BE",
      "CZ",
      "IT_NORD"
    ],
    "years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "scenario_ids": [
      "BASE",
      "DEMAND_UP",
      "FLEX_UP",
      "LOW_RIGIDITY"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955",
    "mode": "SCEN",
    "scenario_id": "FLEX_UP",
    "horizon_year": 2035
  },
  "assumptions_used": [
    {
      "param_group": "Q3",
      "param_name": "demand_k_max",
      "param_value": 0.3,
      "unit": "ratio",
      "description": "Borne max hausse demande",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "far_target",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Cible FAR inversion",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "require_recent_stage2",
      "param_value": 1.0,
      "unit": "bool",
      "description": "Require recent stage2 stress",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "sr_energy_target",
      "param_value": 0.01,
      "unit": "ratio",
      "description": "Cible SR inversion",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "stage2_recent_h_negative_min",
      "param_value": 200.0,
      "unit": "hours",
      "description": "Recent stage2 threshold on negative hours",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "trend_capture_ratio_min",
      "param_value": 0.0,
      "unit": "ratio/year",
      "description": "Improvement threshold for capture trend",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "trend_h_negative_max",
      "param_value": -10.0,
      "unit": "hours/year",
      "description": "Improvement threshold for h_negative trend",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "trend_window_years",
      "param_value": 3.0,
      "unit": "years",
      "description": "Fenetre tendance Q3",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "h_negative_target",
      "param_value": 100.0,
      "unit": "hours",
      "description": "Target max negative hours for phase3 inversion proxy",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "h_below_5_target",
      "param_value": 300.0,
      "unit": "hours",
      "description": "Target max hours below 5 EUR/MWh for phase3 inversion proxy",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "slope_capture_target",
      "param_value": 0.0,
      "unit": "ratio/year",
      "description": "Target minimum capture-ratio slope for phase3 trend status",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "stage2_recent_h_negative_min_scen",
      "param_value": 80.0,
      "unit": "h/an",
      "description": "Q3 SCEN: seuil h_negative recent pour qualifier un contexte Stage2 en prospectif.",
      "source": "codex_adjustment",
      "last_updated": "2026-02-10",
      "owner": "codex"
    },
    {
      "param_group": "Q3",
      "param_name": "stage2_recent_sr_energy_min_scen",
      "param_value": 0.02,
      "unit": "ratio",
      "description": "Q3 SCEN: seuil SR recent pour qualifier un contexte Stage2 meme si h_negative reste faible.",
      "source": "codex_adjustment",
      "last_updated": "2026-02-10",
      "owner": "codex"
    }
  ],
  "kpis": {
    "n_countries": 7,
    "n_in_phase2": 6,
    "n_stop_possible": 0,
    "n_stop_confirmed": 2
  },
  "checks": [
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=73.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=73.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=73.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=73.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=73.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=73.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=72.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=72.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=72.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=72.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=84.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=84.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=84.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=84.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=84.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=84.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=84.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=84.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.7% hors plage plausible [5%,60%]."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "FLEX_UP",
  "horizon_year": 2035
}
```

#### Narratif (FLEX_UP)
Q3 compare les familles actives a la bascule avec l'etat courant et classe CONTINUES / STOP_POSSIBLE / STOP_CONFIRMED / BACK_TO_STAGE1. En mode SCEN, la bascule historique est prioritaire comme reference.

#### Table SCEN FLEX_UP `Q3/scen/FLEX_UP/tables/Q3_status.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,reference_year,in_phase2,status,reason_code,status_explanation,stage3_ready_year,phase2_slope_capture_ratio_pv,phase2_slope_method,trend_capture_ratio_pv,trend_h_negative,stop_possible_if,stop_condition_detail,surplus_energy_twh_recent,target_absorption_twh,demand_uplift_twh,inversion_k_demand,inversion_k_demand_status,inversion_r_mustrun,inversion_r_mustrun_status,inversion_f_flex,inversion_f_flex_status,additional_absorbed_needed_TWh_year,additional_sink_power_p95_mw,warnings_quality,bascule_reference_year,bascule_reference_source,families_active_at_bascule,turned_off_low_price,turned_off_physical,turned_off_value_pv,turned_off_value_wind,turned_off_family_any,turned_off_family_persistent_2y,q2_slope_above_target
DE,2035,True,BACK_TO_STAGE1,all_families_turned_off,Toutes les familles actives a la bascule sont eteintes.,True,,none,-0.000109279,0,True,LOW_PRICE;VALUE_WIND,0,5.69836,0,0,proxy_from_surplus_gap,,proxy_not_computed,,proxy_not_computed,0,0,nan,2019,historical,"LOW_PRICE,VALUE_WIND",True,False,False,True,True,True,False
```

##### ES (1 lignes)
```csv
country,reference_year,in_phase2,status,reason_code,status_explanation,stage3_ready_year,phase2_slope_capture_ratio_pv,phase2_slope_method,trend_capture_ratio_pv,trend_h_negative,stop_possible_if,stop_condition_detail,surplus_energy_twh_recent,target_absorption_twh,demand_uplift_twh,inversion_k_demand,inversion_k_demand_status,inversion_r_mustrun,inversion_r_mustrun_status,inversion_f_flex,inversion_f_flex_status,additional_absorbed_needed_TWh_year,additional_sink_power_p95_mw,warnings_quality,bascule_reference_year,bascule_reference_source,families_active_at_bascule,turned_off_low_price,turned_off_physical,turned_off_value_pv,turned_off_value_wind,turned_off_family_any,turned_off_family_persistent_2y,q2_slope_above_target
ES,2035,True,STOP_CONFIRMED,family_turned_off_confirmed,Au moins une famille basculee est eteinte de facon persistante.,True,-0.000441177,ols,-6.08413e-05,0,True,VALUE_WIND,0,2.77268,0,0,proxy_from_surplus_gap,,proxy_not_computed,,proxy_not_computed,0,0,nan,2023,historical,"LOW_PRICE,PHYSICAL,VALUE_WIND",False,False,False,True,True,True,False
```


#### Scenario `LOW_RIGIDITY`

#### Summary (LOW_RIGIDITY)
```json
{
  "module_id": "Q3",
  "run_id": "FULL_20260211_191955_LOW_RIGIDITY",
  "selection": {
    "countries": [
      "FR",
      "DE",
      "ES",
      "NL",
      "BE",
      "CZ",
      "IT_NORD"
    ],
    "years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "scenario_ids": [
      "BASE",
      "DEMAND_UP",
      "FLEX_UP",
      "LOW_RIGIDITY"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955",
    "mode": "SCEN",
    "scenario_id": "LOW_RIGIDITY",
    "horizon_year": 2035
  },
  "assumptions_used": [
    {
      "param_group": "Q3",
      "param_name": "demand_k_max",
      "param_value": 0.3,
      "unit": "ratio",
      "description": "Borne max hausse demande",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "far_target",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Cible FAR inversion",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "require_recent_stage2",
      "param_value": 1.0,
      "unit": "bool",
      "description": "Require recent stage2 stress",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "sr_energy_target",
      "param_value": 0.01,
      "unit": "ratio",
      "description": "Cible SR inversion",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "stage2_recent_h_negative_min",
      "param_value": 200.0,
      "unit": "hours",
      "description": "Recent stage2 threshold on negative hours",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "trend_capture_ratio_min",
      "param_value": 0.0,
      "unit": "ratio/year",
      "description": "Improvement threshold for capture trend",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "trend_h_negative_max",
      "param_value": -10.0,
      "unit": "hours/year",
      "description": "Improvement threshold for h_negative trend",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "trend_window_years",
      "param_value": 3.0,
      "unit": "years",
      "description": "Fenetre tendance Q3",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "h_negative_target",
      "param_value": 100.0,
      "unit": "hours",
      "description": "Target max negative hours for phase3 inversion proxy",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "h_below_5_target",
      "param_value": 300.0,
      "unit": "hours",
      "description": "Target max hours below 5 EUR/MWh for phase3 inversion proxy",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "slope_capture_target",
      "param_value": 0.0,
      "unit": "ratio/year",
      "description": "Target minimum capture-ratio slope for phase3 trend status",
      "source": "default",
      "last_updated": "2026-02-10",
      "owner": "system"
    },
    {
      "param_group": "Q3",
      "param_name": "stage2_recent_h_negative_min_scen",
      "param_value": 80.0,
      "unit": "h/an",
      "description": "Q3 SCEN: seuil h_negative recent pour qualifier un contexte Stage2 en prospectif.",
      "source": "codex_adjustment",
      "last_updated": "2026-02-10",
      "owner": "codex"
    },
    {
      "param_group": "Q3",
      "param_name": "stage2_recent_sr_energy_min_scen",
      "param_value": 0.02,
      "unit": "ratio",
      "description": "Q3 SCEN: seuil SR recent pour qualifier un contexte Stage2 meme si h_negative reste faible.",
      "source": "codex_adjustment",
      "last_updated": "2026-02-10",
      "owner": "codex"
    }
  ],
  "kpis": {
    "n_countries": 7,
    "n_in_phase2": 6,
    "n_stop_possible": 0,
    "n_stop_confirmed": 3
  },
  "checks": [
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2025: must_run_share=68.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2026: must_run_share=67.9% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2027: must_run_share=67.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2028: must_run_share=67.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2029: must_run_share=67.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2030: must_run_share=67.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2031: must_run_share=67.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2032: must_run_share=67.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2033: must_run_share=67.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2034: must_run_share=67.0% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "BE-2035: must_run_share=66.9% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2025: must_run_share=62.8% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2026: must_run_share=62.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2027: must_run_share=62.7% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2028: must_run_share=62.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2029: must_run_share=62.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2030: must_run_share=62.5% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2031: must_run_share=62.4% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2032: must_run_share=62.3% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2033: must_run_share=62.2% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2034: must_run_share=62.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "CZ-2035: must_run_share=62.1% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2025: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2026: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2027: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2028: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2029: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2030: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2031: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2032: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2033: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2034: must_run_share=0.6% hors plage plausible [5%,60%]."
    },
    {
      "status": "WARN",
      "code": "RC_MR_SHARE_IMPLAUSIBLE",
      "message": "NL-2035: must_run_share=0.6% hors plage plausible [5%,60%]."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "LOW_RIGIDITY",
  "horizon_year": 2035
}
```

#### Narratif (LOW_RIGIDITY)
Q3 compare les familles actives a la bascule avec l'etat courant et classe CONTINUES / STOP_POSSIBLE / STOP_CONFIRMED / BACK_TO_STAGE1. En mode SCEN, la bascule historique est prioritaire comme reference.

#### Table SCEN LOW_RIGIDITY `Q3/scen/LOW_RIGIDITY/tables/Q3_status.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,reference_year,in_phase2,status,reason_code,status_explanation,stage3_ready_year,phase2_slope_capture_ratio_pv,phase2_slope_method,trend_capture_ratio_pv,trend_h_negative,stop_possible_if,stop_condition_detail,surplus_energy_twh_recent,target_absorption_twh,demand_uplift_twh,inversion_k_demand,inversion_k_demand_status,inversion_r_mustrun,inversion_r_mustrun_status,inversion_f_flex,inversion_f_flex_status,additional_absorbed_needed_TWh_year,additional_sink_power_p95_mw,warnings_quality,bascule_reference_year,bascule_reference_source,families_active_at_bascule,turned_off_low_price,turned_off_physical,turned_off_value_pv,turned_off_value_wind,turned_off_family_any,turned_off_family_persistent_2y,q2_slope_above_target
DE,2035,True,BACK_TO_STAGE1,all_families_turned_off,Toutes les familles actives a la bascule sont eteintes.,True,,none,-8.14398e-05,0,True,LOW_PRICE;VALUE_WIND,0,5.70154,0,0,proxy_from_surplus_gap,,proxy_not_computed,,proxy_not_computed,0,0,nan,2019,historical,"LOW_PRICE,VALUE_WIND",True,False,False,True,True,True,False
```

##### ES (1 lignes)
```csv
country,reference_year,in_phase2,status,reason_code,status_explanation,stage3_ready_year,phase2_slope_capture_ratio_pv,phase2_slope_method,trend_capture_ratio_pv,trend_h_negative,stop_possible_if,stop_condition_detail,surplus_energy_twh_recent,target_absorption_twh,demand_uplift_twh,inversion_k_demand,inversion_k_demand_status,inversion_r_mustrun,inversion_r_mustrun_status,inversion_f_flex,inversion_f_flex_status,additional_absorbed_needed_TWh_year,additional_sink_power_p95_mw,warnings_quality,bascule_reference_year,bascule_reference_source,families_active_at_bascule,turned_off_low_price,turned_off_physical,turned_off_value_pv,turned_off_value_wind,turned_off_family_any,turned_off_family_persistent_2y,q2_slope_above_target
ES,2035,True,STOP_CONFIRMED,family_turned_off_confirmed,Au moins une famille basculee est eteinte de facon persistante.,True,-0.00046355,ols,-6.20539e-05,0,True,VALUE_WIND,0,2.77552,0,0,proxy_from_surplus_gap,,proxy_not_computed,,proxy_not_computed,0,0,nan,2023,historical,"LOW_PRICE,PHYSICAL,VALUE_WIND",False,False,False,True,True,True,False
```


## Q4

### GLOBAL

#### Summary (question)
```json
{
  "question_id": "Q4",
  "run_id": "FULL_20260211_191955",
  "selection": {
    "country": "FR",
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "year": 2024,
    "years": [
      2024
    ],
    "horizon_year": 2035,
    "objective": "LOW_PRICE_TARGET",
    "power_grid": [
      0.0,
      250.0,
      500.0,
      750.0,
      1000.0,
      1500.0
    ],
    "duration_grid": [
      2.0,
      4.0,
      6.0,
      8.0
    ],
    "scenario_ids": [
      "BASE",
      "FLEX_UP",
      "HIGH_CO2",
      "HIGH_GAS"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ]
  },
  "hist_module_id": "Q4",
  "scenarios": [
    "BASE",
    "FLEX_UP",
    "HIGH_CO2",
    "HIGH_GAS"
  ],
  "n_checks": 50,
  "n_warnings": 0,
  "n_test_rows": 10,
  "n_compare_rows": 98,
  "checks": [
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes.",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4.",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4.",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes.",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes.",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes.",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4.",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4.",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes.",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes.",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4.",
      "scope": "SCEN",
      "scenario_id": "FLEX_UP"
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4.",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4.",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes.",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes.",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes.",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4.",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4.",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes.",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes.",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes.",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "PASS",
      "code": "BUNDLE_LEDGER_STATUS",
      "message": "ledger: FAIL=0, WARN=0",
      "scope": "BUNDLE",
      "scenario_id": ""
    },
    {
      "status": "PASS",
      "code": "BUNDLE_INFORMATIVENESS",
      "message": "share_tests_informatifs=100.00% ; share_compare_informatifs=69.39%",
      "scope": "BUNDLE",
      "scenario_id": ""
    }
  ],
  "warnings": []
}
```

#### Narratif (question)
Analyse complete Q4: historique + prospectif en un seul run. Statut global=WARN. Tests PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0. Les resultats sont separes entre historique et scenarios, puis compares dans une table unique.

#### Table `Q4/test_ledger.csv`
Lignes: `10`

```csv
test_id,question_id,source_ref,mode,scenario_group,title,what_is_tested,metric_rule,severity_if_fail,scenario_id,status,value,threshold,interpretation
Q4-S-01,Q4,SPEC2-Q4/Slides 23,SCEN,DEFAULT,Comparaison effet batteries par scenario,Impact FAR/surplus/capture compare entre scenarios utiles.,Q4 summary non vide pour >=1 scenario,HIGH,BASE,PASS,7,>0 lignes,Resultats Q4 prospectifs disponibles.
Q4-S-02,Q4,Slides 23-25,SCEN,DEFAULT,Sensibilite valeur commodites,Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.,delta pv_capture ou revenus vs BASE,MEDIUM,BASE,PASS,share_finite=100.00%,>=80% valeurs finies,Sensibilite valeur exploitable sur le panel.
Q4-S-01,Q4,SPEC2-Q4/Slides 23,SCEN,DEFAULT,Comparaison effet batteries par scenario,Impact FAR/surplus/capture compare entre scenarios utiles.,Q4 summary non vide pour >=1 scenario,HIGH,FLEX_UP,PASS,7,>0 lignes,Resultats Q4 prospectifs disponibles.
Q4-S-02,Q4,Slides 23-25,SCEN,DEFAULT,Sensibilite valeur commodites,Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.,delta pv_capture ou revenus vs BASE,MEDIUM,FLEX_UP,PASS,share_finite=100.00%,>=80% valeurs finies,Sensibilite valeur exploitable sur le panel.
Q4-S-01,Q4,SPEC2-Q4/Slides 23,SCEN,DEFAULT,Comparaison effet batteries par scenario,Impact FAR/surplus/capture compare entre scenarios utiles.,Q4 summary non vide pour >=1 scenario,HIGH,HIGH_CO2,PASS,7,>0 lignes,Resultats Q4 prospectifs disponibles.
Q4-S-02,Q4,Slides 23-25,SCEN,DEFAULT,Sensibilite valeur commodites,Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.,delta pv_capture ou revenus vs BASE,MEDIUM,HIGH_CO2,PASS,share_finite=100.00%,>=80% valeurs finies,Sensibilite valeur exploitable sur le panel.
Q4-S-01,Q4,SPEC2-Q4/Slides 23,SCEN,DEFAULT,Comparaison effet batteries par scenario,Impact FAR/surplus/capture compare entre scenarios utiles.,Q4 summary non vide pour >=1 scenario,HIGH,HIGH_GAS,PASS,7,>0 lignes,Resultats Q4 prospectifs disponibles.
Q4-S-02,Q4,Slides 23-25,SCEN,DEFAULT,Sensibilite valeur commodites,Les scenarios HIGH_CO2/HIGH_GAS modifient les indicateurs de valeur.,delta pv_capture ou revenus vs BASE,MEDIUM,HIGH_GAS,PASS,share_finite=100.00%,>=80% valeurs finies,Sensibilite valeur exploitable sur le panel.
Q4-H-01,Q4,SPEC2-Q4/Slides 22,HIST,HIST_BASE,Simulation BESS 3 modes,"SURPLUS_FIRST, PRICE_ARBITRAGE_SIMPLE et PV_COLOCATED sont executes.",3 modes executes avec sorties non vides,CRITICAL,nan,PASS,"HIST_PRICE_ARBITRAGE_SIMPLE,HIST_PV_COLOCATED",3 modes executes,Les trois modes Q4 sont disponibles.
Q4-H-02,Q4,SPEC2-Q4,HIST,HIST_BASE,Invariants physiques BESS,Bornes SOC/puissance/energie respectees.,aucun check FAIL Q4,CRITICAL,nan,PASS,WARN,aucun FAIL physique,Les invariants physiques batterie sont respectes. Des avertissements non-physiques peuvent subsister (objectif/scenario).
```


#### Table `Q4/comparison_hist_vs_scen.csv`
Lignes totales: `98` | Lignes DE/ES: `28`

##### DE (14 lignes)
```csv
country,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
DE,BASE,far_after,1,1,0,,FRAGILE,delta_quasi_nul_vs_historique
DE,BASE,pv_capture_price_after,58.909,124.282,65.3728,,INFORMATIVE,delta_interpretable
DE,BASE,surplus_unabs_energy_after,0,0,0,,FRAGILE,delta_quasi_nul_vs_historique
DE,FLEX_UP,far_after,1,1,0,,FRAGILE,delta_quasi_nul_vs_historique
DE,FLEX_UP,pv_capture_price_after,58.909,124.263,65.3545,,INFORMATIVE,delta_interpretable
DE,FLEX_UP,surplus_unabs_energy_after,0,0,0,,FRAGILE,delta_quasi_nul_vs_historique
DE,HIGH_CO2,far_after,1,1,0,,FRAGILE,delta_quasi_nul_vs_historique
DE,HIGH_CO2,pv_capture_price_after,58.909,135.576,76.667,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,surplus_unabs_energy_after,0,0,0,,FRAGILE,delta_quasi_nul_vs_historique
DE,HIGH_GAS,far_after,1,1,0,,FRAGILE,delta_quasi_nul_vs_historique
DE,HIGH_GAS,pv_capture_price_after,58.909,139.186,80.2772,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,surplus_unabs_energy_after,0,0,0,,FRAGILE,delta_quasi_nul_vs_historique
DE,HIST_PRICE_ARBITRAGE_SIMPLE,far_after,1,1,0,,FRAGILE,delta_quasi_nul_vs_historique
DE,HIST_PV_COLOCATED,far_after,1,1,0,,FRAGILE,delta_quasi_nul_vs_historique
```

##### ES (14 lignes)
```csv
country,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
ES,BASE,far_after,0.999402,1,0.000597699,,INFORMATIVE,delta_interpretable
ES,BASE,pv_capture_price_after,30.0369,91.5458,61.5088,,INFORMATIVE,delta_interpretable
ES,BASE,surplus_unabs_energy_after,0.002132,0,-0.002132,,INFORMATIVE,delta_interpretable
ES,FLEX_UP,far_after,0.999402,1,0.000597699,,INFORMATIVE,delta_interpretable
ES,FLEX_UP,pv_capture_price_after,30.0369,91.5166,61.4796,,INFORMATIVE,delta_interpretable
ES,FLEX_UP,surplus_unabs_energy_after,0.002132,0,-0.002132,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,far_after,0.999402,1,0.000597699,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,pv_capture_price_after,30.0369,96.1499,66.113,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,surplus_unabs_energy_after,0.002132,0,-0.002132,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,far_after,0.999402,1,0.000597699,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,pv_capture_price_after,30.0369,101.802,71.7656,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,surplus_unabs_energy_after,0.002132,0,-0.002132,,INFORMATIVE,delta_interpretable
ES,HIST_PRICE_ARBITRAGE_SIMPLE,far_after,0.999402,0.999402,0,,FRAGILE,delta_quasi_nul_vs_historique
ES,HIST_PV_COLOCATED,far_after,0.999402,0.999402,0,,FRAGILE,delta_quasi_nul_vs_historique
```


### HIST

#### Summary (hist)
```json
{
  "module_id": "Q4",
  "run_id": "FULL_20260211_191955_HIST",
  "selection": {
    "country": "FR",
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "year": 2024,
    "years": [
      2024
    ],
    "horizon_year": 2035,
    "objective": "LOW_PRICE_TARGET",
    "power_grid": [
      0.0,
      250.0,
      500.0,
      750.0,
      1000.0,
      1500.0
    ],
    "duration_grid": [
      2.0,
      4.0,
      6.0,
      8.0
    ],
    "scenario_ids": [
      "BASE",
      "FLEX_UP",
      "HIGH_CO2",
      "HIGH_GAS"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "mode": "HIST",
    "run_id": "FULL_20260211_191955"
  },
  "assumptions_used": [
    {
      "param_group": "Q4",
      "param_name": "bess_eta_roundtrip",
      "param_value": 0.88,
      "unit": "ratio",
      "description": "Rendement roundtrip BESS",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "bess_max_cycles_per_day",
      "param_value": 1.0,
      "unit": "cycles/day",
      "description": "Cycles max journaliers BESS",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "bess_soc_init_frac",
      "param_value": 0.5,
      "unit": "ratio",
      "description": "SOC initial fraction",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "target_far",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Cible FAR pour sizing",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "target_surplus_unabs_energy_twh",
      "param_value": 0.0,
      "unit": "TWh",
      "description": "Cible surplus non absorbe",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    }
  ],
  "kpis": {
    "n_runs": 7,
    "n_countries": 7,
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "compute_time_sec_total": 6.844544899995526,
    "cache_hit_share": 0.2857142857142857
  },
  "checks": [
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E)."
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4."
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E)."
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4."
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E)."
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes."
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes."
    }
  ],
  "warnings": [],
  "mode": "HIST",
  "scenario_id": null,
  "horizon_year": 2024
}
```

#### Narratif (hist)
Q4 historique: aggregation multi-pays (7 pays). Les tables detaillees conservent les lignes par pays.

#### Table HIST `Q4/hist/tables/Q4_bess_frontier.csv`
Lignes totales: `168` | Lignes DE/ES: `48`

##### DE (24 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,False,False,457,88,756,130,-369,-626,78.5155,77.9767,0.588775,0.755469,0.838449,0.888002,0.166694,0.049553,0,0,46.228,58.909,65.8312,69.2435,319,217,112.006,57.7412,0.0925546,0.0925546,0.0757058,0.0757058,0.226305,0.226305,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,0,2,0
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,4,1,1,False,False,457,88,756,130,-369,-626,78.5155,77.9767,0.588775,0.755469,0.838449,0.888002,0.166694,0.049553,0,0,46.228,58.909,65.8312,69.2435,319,217,112.006,57.7412,0.0925546,0.0925546,0.0757058,0.0757058,0.226305,0.226305,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,0,4,0
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,6,1,1,False,False,457,88,756,130,-369,-626,78.5155,77.9767,0.588775,0.755469,0.838449,0.888002,0.166694,0.049553,0,0,46.228,58.909,65.8312,69.2435,319,217,112.006,57.7412,0.0925546,0.0925546,0.0757058,0.0757058,0.226305,0.226305,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,0,6,0
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,8,1,1,False,False,457,88,756,130,-369,-626,78.5155,77.9767,0.588775,0.755469,0.838449,0.888002,0.166694,0.049553,0,0,46.228,58.909,65.8312,69.2435,319,217,112.006,57.7412,0.0925546,0.0925546,0.0757058,0.0757058,0.226305,0.226305,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,0,8,0
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,250,500,2,1,1,False,False,457,87,756,129,-370,-627,78.5155,77.9886,0.588775,0.756121,0.838449,0.888047,0.167346,0.0495978,0,0,46.228,58.9688,65.8312,69.2576,319,216,112.006,57.5754,0.0925546,0.0948315,0.0757058,0.0745674,0.226305,0.226305,False,False,False,False,False,1.16398e+06,0,500,0,0,0,250,250,56285.9,49531.6,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,250,2,500
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1000,4,1,1,False,False,457,85,756,125,-372,-631,78.5155,77.9976,0.588775,0.756626,0.838449,0.888119,0.167851,0.0496699,0,0,46.228,59.015,65.8312,69.2712,319,215,112.006,57.4626,0.0925546,0.095173,0.0757058,0.0742259,0.226305,0.226297,False,False,False,False,False,3.29357e+06,0,1000,0,0,0,250,250,99847,87865.4,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,250,4,1000
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1500,6,1,1,False,False,457,82,756,119,-375,-637,78.5155,78.0027,0.588775,0.756945,0.838449,0.888168,0.16817,0.0497184,0,0,46.228,59.0438,65.8312,69.2795,319,215,112.006,57.4074,0.0925546,0.0954007,0.0757058,0.074112,0.226305,0.226112,False,False,False,False,False,4.77433e+06,0,1500,0,0,0,250,250,129076,113587,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,250,6,1500
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,250,2000,8,1,1,False,False,457,81,756,119,-376,-637,78.5155,78.0063,0.588775,0.757123,0.838449,0.888207,0.168348,0.0497578,0,0,46.228,59.0604,65.8312,69.2857,319,215,112.006,57.3889,0.0925546,0.0954007,0.0757058,0.074112,0.226305,0.226252,False,False,False,False,False,5.5112e+06,0,2000,0,0,0,250,250,146538,128953,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,250,8,2000
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,500,1000,2,1,1,False,False,457,86,756,128,-371,-628,78.5155,78.0006,0.588775,0.756776,0.838449,0.888093,0.168001,0.0496433,0,0,46.228,59.029,65.8312,69.2718,319,214,112.006,57.4201,0.0925546,0.0973361,0.0757058,0.0726321,0.226305,0.226305,False,False,False,False,False,2.23006e+06,0,1000,0,0,0,500,500,111101,97769.2,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,500,2,1000
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,500,2000,4,1,1,False,False,457,80,756,119,-377,-637,78.5155,78.0188,0.588775,0.757811,0.838449,0.888232,0.169035,0.0497828,0,0,46.228,59.1235,65.8312,69.2988,319,213,112.006,57.188,0.0925546,0.0979053,0.0757058,0.0720628,0.226305,0.22617,False,False,False,False,False,6.36264e+06,0,2000,0,0,0,500,500,197463,173767,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,500,4,2000
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,500,3000,6,1,1,False,False,457,75,756,111,-382,-645,78.5155,78.0289,0.588775,0.758452,0.838449,0.888324,0.169676,0.0498749,0,0,46.228,59.1811,65.8312,69.3149,319,213,112.006,57.0779,0.0925546,0.0984745,0.0757058,0.0716075,0.226305,0.225999,False,False,False,False,False,9.18014e+06,0,3000,0,0,0,500,500,254605,224053,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,500,6,3000
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,500,4000,8,1,1,False,False,457,73,756,110,-384,-646,78.5155,78.036,0.588775,0.758806,0.838449,0.888403,0.170031,0.0499536,0,0,46.228,59.2142,65.8312,69.3274,319,213,112.006,57.0424,0.0925546,0.0987022,0.0757058,0.0713798,0.226305,0.225999,False,False,False,False,False,1.05795e+07,0,4000,0,0,0,500,500,288789,254134,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,500,8,4000
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,750,1500,2,1,1,False,False,457,84,756,128,-373,-628,78.5155,78.0123,0.588775,0.757417,0.838449,0.88814,0.168642,0.0496903,0,0,46.228,59.0878,65.8312,69.2858,319,214,112.006,57.2771,0.0925546,0.0994991,0.0757058,0.0709244,0.226305,0.226297,False,False,False,False,False,3.16629e+06,0,1500,0,0,0,750,750,164743,144974,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,750,2,1500
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,750,3000,4,1,1,False,False,457,75,756,114,-382,-642,78.5155,78.0396,0.588775,0.758995,0.838449,0.888338,0.17022,0.049889,0,0,46.228,59.2317,65.8312,69.3255,319,212,112.006,56.9197,0.0925546,0.100865,0.0757058,0.0696721,0.226305,0.226095,False,False,False,False,False,9.16655e+06,0,3000,0,0,0,750,750,292688,257566,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,750,4,3000
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,750,4500,6,1,1,False,False,457,66,756,103,-391,-653,78.5155,78.0548,0.588775,0.759965,0.838449,0.888474,0.17119,0.0500249,0,0,46.228,59.319,65.8312,69.3497,319,212,112.006,56.7501,0.0925546,0.101548,0.0757058,0.0692168,0.226305,0.225962,False,False,False,False,False,1.32172e+07,0,4500,0,0,0,750,750,377028,331785,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,750,6,4500
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,750,6000,8,1,1,False,False,457,64,756,101,-393,-655,78.5155,78.0653,0.588775,0.760491,0.838449,0.888588,0.171716,0.050139,0,0,46.228,59.368,65.8312,69.3679,319,212,112.006,56.701,0.0925546,0.10189,0.0757058,0.0688752,0.226305,0.225956,False,False,False,False,False,1.519e+07,0,6000,0,0,0,750,750,427165,375905,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,750,8,6000
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,2000,2,1,1,False,False,457,83,756,126,-374,-630,78.5155,78.0236,0.588775,0.758041,0.838449,0.888186,0.169266,0.0497372,0,0,46.228,59.1451,65.8312,69.2995,319,214,112.006,57.1579,0.0925546,0.102345,0.0757058,0.0685337,0.226305,0.226305,False,False,False,False,False,3.96384e+06,0,2000,0,0,0,1000,1000,216504,190524,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,1000,2,2000
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,4000,4,1,1,False,False,457,71,756,109,-386,-647,78.5155,78.06,0.588775,0.760184,0.838449,0.88844,0.171409,0.0499912,0,0,46.228,59.34,65.8312,69.3517,319,212,112.006,56.6679,0.0925546,0.104167,0.0757058,0.066826,0.226305,0.226112,False,False,False,False,False,1.1696e+07,0,4000,0,0,0,1000,1000,384635,338479,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,1000,4,4000
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,6000,6,1,1,False,False,457,59,756,97,-398,-659,78.5155,78.081,0.588775,0.761519,0.838449,0.888618,0.172744,0.0501684,0,0,46.228,59.4602,65.8312,69.3842,319,212,112.006,56.4192,0.0925546,0.10485,0.0757058,0.0662568,0.226305,0.225999,False,False,False,False,False,1.68978e+07,0,6000,0,0,0,1000,1000,495519,436057,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,1000,6,6000
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,8000,8,1,1,False,False,457,56,756,95,-401,-661,78.5155,78.0944,0.588775,0.762209,0.838449,0.888761,0.173434,0.0503117,0,0,46.228,59.5242,65.8312,69.4072,319,212,112.006,56.3606,0.0925546,0.105533,0.0757058,0.0655738,0.226305,0.225999,False,False,False,False,False,1.93378e+07,0,8000,0,0,0,1000,1000,559750,492580,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,1000,8,8000
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,3000,2,1,1,False,False,457,81,756,123,-376,-633,78.5155,78.0456,0.588775,0.759308,0.838449,0.888274,0.170533,0.0498243,0,0,46.228,59.2607,65.8312,69.3259,319,214,112.006,56.9616,0.0925546,0.10872,0.0757058,0.0643215,0.226305,0.226331,False,False,False,False,False,5.3763e+06,0,3000,0,0,0,1500,1500,314849,277067,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,1500,2,3000
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,6000,4,1,1,False,False,457,64,756,97,-393,-659,78.5155,78.0991,0.588775,0.762572,0.838449,0.888634,0.173797,0.0501849,0,0,46.228,59.5562,65.8312,69.4015,319,211,112.006,56.1838,0.0925546,0.111225,0.0757058,0.0619308,0.226305,0.226112,False,False,False,False,False,1.62442e+07,0,6000,0,0,0,1500,1500,559692,492529,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,1500,4,6000
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,9000,6,1,1,False,False,457,47,756,81,-410,-675,78.5155,78.1312,0.588775,0.764673,0.838449,0.888866,0.175898,0.0504163,0,0,46.228,59.7448,65.8312,69.4482,319,211,112.006,55.8172,0.0925546,0.112477,0.0757058,0.0609062,0.226305,0.226006,False,False,False,False,False,2.3352e+07,0,9000,0,0,0,1500,1500,719026,632743,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,1500,6,9000
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,12000,8,1,1,False,False,457,42,756,76,-415,-680,78.5155,78.1493,0.588775,0.765667,0.838449,0.889051,0.176891,0.0506013,0,0,46.228,59.8363,65.8312,69.4787,319,211,112.006,55.6991,0.0925546,0.113957,0.0757058,0.0594262,0.226305,0.226028,False,False,False,False,False,2.64555e+07,0,12000,0,0,0,1500,1500,806020,709297,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,1500,8,12000
```

##### ES (24 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,0.999402,0.999402,False,False,247,0,1690,694,-247,-996,63.0395,60.3017,0.678957,0.498111,0.882136,0.921005,-0.180847,0.0388682,0.002132,0.002132,42.8012,30.0369,55.6095,55.5381,272,355,71.5241,85.7176,0.0837887,0.0837887,0.169171,0.169171,0.295199,0.295199,False,False,False,True,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,0,2,0
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,4,0.999402,0.999402,False,False,247,0,1690,694,-247,-996,63.0395,60.3017,0.678957,0.498111,0.882136,0.921005,-0.180847,0.0388682,0.002132,0.002132,42.8012,30.0369,55.6095,55.5381,272,355,71.5241,85.7176,0.0837887,0.0837887,0.169171,0.169171,0.295199,0.295199,False,False,False,True,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,0,4,0
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,6,0.999402,0.999402,False,False,247,0,1690,694,-247,-996,63.0395,60.3017,0.678957,0.498111,0.882136,0.921005,-0.180847,0.0388682,0.002132,0.002132,42.8012,30.0369,55.6095,55.5381,272,355,71.5241,85.7176,0.0837887,0.0837887,0.169171,0.169171,0.295199,0.295199,False,False,False,True,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,0,6,0
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,8,0.999402,0.999402,False,False,247,0,1690,694,-247,-996,63.0395,60.3017,0.678957,0.498111,0.882136,0.921005,-0.180847,0.0388682,0.002132,0.002132,42.8012,30.0369,55.6095,55.5381,272,355,71.5241,85.7176,0.0837887,0.0837887,0.169171,0.169171,0.295199,0.295199,False,False,False,True,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,0,8,0
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,250,500,2,0.999402,0.999402,False,False,247,0,1690,673,-247,-1017,63.0395,60.2959,0.678957,0.499165,0.882136,0.920686,-0.179793,0.0385495,0.002132,0.002132,42.8012,30.0976,55.6095,55.5136,272,354,71.5241,85.4918,0.0837887,0.092327,0.169171,0.162796,0.295199,0.295087,False,False,False,True,True,3.03836e+06,0,469.042,0,0,0,250,250,104618,92063.8,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,250,2,500
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1000,4,0.999402,0.999596,False,False,247,0,1690,656,-247,-1034,63.0395,60.2839,0.678957,0.50055,0.882136,0.920334,-0.178407,0.0381979,0.002132,0.001442,42.8012,30.1751,55.6095,55.4814,272,354,71.5241,85.0777,0.0837887,0.0938069,0.169171,0.161316,0.295199,0.294864,False,False,False,True,True,8.82656e+06,0,938.083,0,0,0,250,250,195152,171734,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,250,4,1000
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1500,6,0.999402,0.999712,False,False,247,0,1690,647,-247,-1043,63.0395,60.2701,0.678957,0.501703,0.882136,0.920048,-0.177255,0.0379118,0.002132,0.001027,42.8012,30.2377,55.6095,55.4514,272,354,71.5241,84.8781,0.0837887,0.0946038,0.169171,0.160519,0.295199,0.294814,False,False,False,True,True,1.35197e+07,0,1407.12,0,0,0,250,250,272236,239568,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,250,6,1500
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,250,2000,8,0.999402,0.999712,False,False,247,0,1690,638,-247,-1052,63.0395,60.2557,0.678957,0.502418,0.882136,0.919871,-0.176539,0.0377343,0.002132,0.001027,42.8012,30.2735,55.6095,55.4274,272,354,71.5241,84.8414,0.0837887,0.0948315,0.169171,0.160291,0.295199,0.294897,False,False,False,True,True,1.60804e+07,0,1876.17,0,0,0,250,250,325370,286326,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,250,8,2000
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,500,1000,2,0.999402,0.999402,False,False,247,0,1690,665,-247,-1025,63.0395,60.2904,0.678957,0.500283,0.882136,0.920353,-0.178674,0.0382167,0.002132,0.002132,42.8012,30.1623,55.6095,55.4884,272,354,71.5241,85.28,0.0837887,0.10189,0.169171,0.155738,0.295199,0.295031,False,False,False,True,True,5.78922e+06,0,938.083,0,0,0,500,500,203980,179502,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,500,2,1000
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,500,2000,4,0.999402,0.999758,False,False,247,0,1690,626,-247,-1064,63.0395,60.2678,0.678957,0.503074,0.882136,0.919658,-0.175884,0.0375219,0.002132,0.000863,42.8012,30.3191,55.6095,55.4257,272,353,71.5241,84.4731,0.0837887,0.104053,0.169171,0.153802,0.295199,0.294586,False,False,False,True,True,1.68714e+07,0,1876.17,0,0,0,500,500,381492,335713,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,500,4,2000
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,500,3000,6,0.999402,0.999944,False,False,247,0,1690,603,-247,-1087,63.0395,60.2415,0.678957,0.505361,0.882136,0.919111,-0.173597,0.0369744,0.002132,0.000198,42.8012,30.4437,55.6095,55.3686,272,352,71.5241,84.0692,0.0837887,0.106899,0.169171,0.150956,0.295199,0.294541,False,False,False,True,True,2.5659e+07,0,2814.25,0,0,0,500,500,530628,466953,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,500,6,3000
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,500,4000,8,0.999402,0.999944,False,False,247,0,1690,580,-247,-1110,63.0395,60.2141,0.678957,0.506764,0.882136,0.918762,-0.172193,0.0366258,0.002132,0.000198,42.8012,30.5144,55.6095,55.3225,272,352,71.5241,83.9866,0.0837887,0.10781,0.169171,0.150159,0.295199,0.294686,False,False,False,True,True,3.02924e+07,0,3752.33,0,0,0,500,500,632120,556266,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,500,8,4000
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,750,1500,2,0.999402,0.999402,False,False,247,0,1690,653,-247,-1037,63.0395,60.2872,0.678957,0.501536,0.882136,0.920014,-0.177422,0.0378774,0.002132,0.002132,42.8012,30.2362,55.6095,55.465,272,354,71.5241,85.0837,0.0837887,0.109517,0.169171,0.149818,0.295199,0.295043,False,False,False,True,True,8.28147e+06,0,1407.12,0,0,0,750,750,299536,263592,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,750,2,1500
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,750,3000,4,0.999402,0.999803,False,False,247,0,1690,594,-247,-1096,63.0395,60.2563,0.678957,0.505787,0.882136,0.918994,-0.17317,0.036858,0.002132,0.000702,42.8012,30.4768,55.6095,55.3752,272,353,71.5241,83.8805,0.0837887,0.113957,0.169171,0.145719,0.295199,0.294541,False,False,False,True,True,2.42187e+07,0,2814.25,0,0,0,750,750,560728,493441,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,750,4,3000
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,750,4500,6,0.999402,1,False,False,247,0,1690,557,-247,-1133,63.0395,60.2173,0.678957,0.509132,0.882136,0.918188,-0.169825,0.0360514,0.002132,0,42.8012,30.6586,55.6095,55.2908,272,352,71.5241,83.293,0.0837887,0.117942,0.169171,0.141735,0.295199,0.294541,False,False,False,True,True,3.64271e+07,0,4221.37,0,0,0,750,750,775268,682236,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,750,6,4500
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,750,6000,8,0.999402,1,False,False,247,0,1690,520,-247,-1170,63.0395,60.1784,0.678957,0.5112,0.882136,0.917675,-0.167758,0.0355389,0.002132,0,42.8012,30.7631,55.6095,55.2242,272,352,71.5241,83.1539,0.0837887,0.118966,0.169171,0.140938,0.295199,0.294586,False,False,False,True,True,4.27441e+07,0,5628.5,0,0,0,750,750,921620,811026,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,750,8,6000
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,2000,2,0.999402,0.999402,False,False,247,0,1690,635,-247,-1055,63.0395,60.2848,0.678957,0.502843,0.882136,0.919686,-0.176115,0.0375502,0.002132,0.002132,42.8012,30.3138,55.6095,55.4432,272,354,71.5241,84.9414,0.0837887,0.119308,0.169171,0.141849,0.295199,0.294987,False,False,False,True,True,1.05524e+07,0,1876.17,0,0,0,1000,1000,392124,345069,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,1000,2,2000
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,4000,4,0.999402,0.999803,False,False,247,0,1690,556,-247,-1134,63.0395,60.2456,0.678957,0.508448,0.882136,0.918368,-0.17051,0.0362316,0.002132,0.000702,42.8012,30.6318,55.6095,55.3277,272,352,71.5241,83.3249,0.0837887,0.127618,0.169171,0.133766,0.295199,0.294541,False,False,False,True,True,3.06437e+07,0,3752.33,0,0,0,1000,1000,728916,641446,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,1000,4,4000
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,6000,6,0.999402,1,False,False,247,0,1690,505,-247,-1185,63.0395,60.1948,0.678957,0.512707,0.882136,0.917331,-0.16625,0.0351947,0.002132,0,42.8012,30.8623,55.6095,55.2186,272,352,71.5241,82.6073,0.0837887,0.132058,0.169171,0.12944,0.295199,0.29453,False,False,False,True,True,4.55115e+07,0,5628.5,0,0,0,1000,1000,1.00056e+06,880489,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,1000,6,6000
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,8000,8,0.999402,1,False,False,247,0,1690,457,-247,-1233,63.0395,60.1457,0.678957,0.515453,0.882136,0.916665,-0.163504,0.0345285,0.002132,0,42.8012,31.0023,55.6095,55.1334,272,352,71.5241,82.4071,0.0837887,0.134221,0.169171,0.127846,0.295199,0.294541,False,False,False,True,True,5.32246e+07,0,7504.67,0,0,0,1000,1000,1.18942e+06,1.04669e+06,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,1000,8,8000
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,3000,2,0.999402,0.999402,False,False,247,0,1690,602,-247,-1088,63.0395,60.2775,0.678957,0.505439,0.882136,0.919006,-0.173519,0.0368697,0.002132,0.002132,42.8012,30.4666,55.6095,55.3954,272,353,71.5241,84.5745,0.0837887,0.134904,0.169171,0.128188,0.295199,0.294819,False,False,False,True,True,1.45811e+07,0,2814.25,0,0,0,1500,1500,570112,501699,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,1500,2,3000
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,6000,4,0.999402,0.999803,False,False,247,0,1690,508,-247,-1182,63.0395,60.2246,0.678957,0.5135,0.882136,0.917194,-0.165458,0.0350577,0.002132,0.000702,42.8012,30.9253,55.6095,55.2377,272,351,71.5241,82.3735,0.0837887,0.145719,0.169171,0.117714,0.295199,0.294485,False,False,False,True,True,4.09956e+07,0,5628.5,0,0,0,1500,1500,1.03401e+06,909931,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,1500,4,6000
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,9000,6,0.999402,1,False,False,247,0,1690,431,-247,-1259,63.0395,60.1528,0.678957,0.519505,0.882136,0.915702,-0.159452,0.0335656,0.002132,0,42.8012,31.2497,55.6095,55.082,272,350,71.5241,81.4551,0.0837887,0.151526,0.169171,0.112022,0.295199,0.294541,False,False,False,True,True,5.96777e+07,0,8442.75,0,0,0,1500,1500,1.40507e+06,1.23646e+06,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,1500,6,9000
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,12000,8,0.999402,1,False,False,247,0,1690,366,-247,-1324,63.0395,60.0912,0.678957,0.523588,0.882136,0.914834,-0.15537,0.0326978,0.002132,0,42.8012,31.463,55.6095,54.9734,272,350,71.5241,81.105,0.0837887,0.155055,0.169171,0.109517,0.295199,0.294764,False,False,False,True,True,6.90685e+07,0,11257,0,0,0,1500,1500,1.66712e+06,1.46706e+06,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,1500,8,12000
```


#### Table HIST `Q4/hist/tables/Q4_sizing_summary.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh,objective_met,objective_reason,objective_not_reached,objective_target_value,objective_recommendation,pv_capacity_proxy_mw,power_grid_max_mw,duration_grid_max_h,grid_expansions_used,notes_quality
HIST,DE,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,False,False,457,88,756,130,-369,-626,78.5155,77.9767,0.588775,0.755469,0.838449,0.888002,0.166694,0.049553,0,0,46.228,58.909,65.8312,69.2435,319,217,112.006,57.7412,0.0925546,0.0925546,0.0757058,0.0757058,0.226305,0.226305,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.03372,True,0,2,0,True,already_met,False,200,,40714.2,1500,8,0,ok
```

##### ES (1 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh,objective_met,objective_reason,objective_not_reached,objective_target_value,objective_recommendation,pv_capacity_proxy_mw,power_grid_max_mw,duration_grid_max_h,grid_expansions_used,notes_quality
HIST,ES,2024,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,0.999402,0.999402,False,False,247,0,1690,694,-247,-996,63.0395,60.3017,0.678957,0.498111,0.882136,0.921005,-0.180847,0.0388682,0.002132,0.002132,42.8012,30.0369,55.6095,55.5381,272,355,71.5241,85.7176,0.0837887,0.0837887,0.169171,0.169171,0.295199,0.295199,False,False,False,True,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.980045,True,0,2,0,True,already_met,False,200,,20284,1500,8,0,ok
```


### SCEN

#### Scenario `BASE`

#### Summary (BASE)
```json
{
  "module_id": "Q4",
  "run_id": "FULL_20260211_191955_BASE",
  "selection": {
    "country": "FR",
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "year": 2024,
    "years": [
      2024
    ],
    "horizon_year": 2035,
    "objective": "LOW_PRICE_TARGET",
    "power_grid": [
      0.0,
      250.0,
      500.0,
      750.0,
      1000.0,
      1500.0
    ],
    "duration_grid": [
      2.0,
      4.0,
      6.0,
      8.0
    ],
    "scenario_ids": [
      "BASE",
      "FLEX_UP",
      "HIGH_CO2",
      "HIGH_GAS"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955"
  },
  "assumptions_used": [
    {
      "param_group": "Q4",
      "param_name": "bess_eta_roundtrip",
      "param_value": 0.88,
      "unit": "ratio",
      "description": "Rendement roundtrip BESS",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "bess_max_cycles_per_day",
      "param_value": 1.0,
      "unit": "cycles/day",
      "description": "Cycles max journaliers BESS",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "bess_soc_init_frac",
      "param_value": 0.5,
      "unit": "ratio",
      "description": "SOC initial fraction",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "target_far",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Cible FAR pour sizing",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "target_surplus_unabs_energy_twh",
      "param_value": 0.0,
      "unit": "TWh",
      "description": "Cible surplus non absorbe",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    }
  ],
  "kpis": {
    "n_runs": 7,
    "n_countries": 7,
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "compute_time_sec_total": 10.681184300006862,
    "cache_hit_share": 0.2857142857142857
  },
  "checks": [
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E)."
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4."
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4."
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes."
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes."
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "BASE",
  "horizon_year": 2035
}
```

#### Narratif (BASE)
Q4 scenario BASE: aggregation multi-pays (7 pays). Les tables detaillees conservent les lignes par pays.

#### Table SCEN BASE `Q4/scen/BASE/tables/Q4_bess_frontier.csv`
Lignes totales: `168` | Lignes DE/ES: `48`

##### DE (24 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,0,2,0
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,4,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,0,4,0
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,6,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,0,6,0
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,8,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,0,8,0
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,500,2,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,250,2,500
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1000,4,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,250,4,1000
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1500,6,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,250,6,1500
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,2000,8,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,250,8,2000
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,1000,2,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,500,2,1000
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,2000,4,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,500,4,2000
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,3000,6,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,500,6,3000
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,4000,8,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,500,8,4000
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,1500,2,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,750,2,1500
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,3000,4,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,750,4,3000
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,4500,6,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,750,6,4500
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,6000,8,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,750,8,6000
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,2000,2,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,1000,2,2000
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,4000,4,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,1000,4,4000
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,6000,6,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,1000,6,6000
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,8000,8,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,1000,8,8000
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,3000,2,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,1500,2,3000
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,6000,4,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,1500,4,6000
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,9000,6,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,1500,6,9000
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,12000,8,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,1500,8,12000
```

##### ES (24 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,0,2,0
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,4,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,0,4,0
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,6,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,0,6,0
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,8,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,0,8,0
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,500,2,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,250,2,500
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1000,4,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,250,4,1000
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1500,6,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,250,6,1500
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,2000,8,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,250,8,2000
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,1000,2,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,500,2,1000
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,2000,4,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,500,4,2000
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,3000,6,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,500,6,3000
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,4000,8,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,500,8,4000
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,1500,2,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,750,2,1500
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,3000,4,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,750,4,3000
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,4500,6,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,750,6,4500
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,6000,8,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,750,8,6000
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,2000,2,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,1000,2,2000
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,4000,4,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,1000,4,4000
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,6000,6,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,1000,6,6000
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,8000,8,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,1000,8,8000
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,3000,2,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,1500,2,3000
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,6000,4,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,1500,4,6000
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,9000,6,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,1500,6,9000
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,12000,8,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,1500,8,12000
```


#### Table SCEN BASE `Q4/scen/BASE/tables/Q4_sizing_summary.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh,objective_met,objective_reason,objective_not_reached,objective_target_value,objective_recommendation,pv_capacity_proxy_mw,power_grid_max_mw,duration_grid_max_h,grid_expansions_used,notes_quality
BASE,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,131.543,126.736,0.964117,0.980637,0.959978,0.977473,0.0165204,0.0174954,0,0,126.823,124.282,126.279,123.881,122,38,34.5894,16.0235,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.88463,True,0,2,0,True,already_met,False,200,,21963.6,1500,8,0,ok
```

##### ES (1 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh,objective_met,objective_reason,objective_not_reached,objective_target_value,objective_recommendation,pv_capacity_proxy_mw,power_grid_max_mw,duration_grid_max_h,grid_expansions_used,notes_quality
BASE,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,99.3554,94.978,0.928055,0.963863,0.973945,0.984476,0.0358087,0.0105315,0,0,92.2072,91.5458,96.7666,93.5035,195,53,44.7589,21.6075,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.827961,True,0,2,0,True,already_met,False,200,,14442.7,1500,8,0,ok
```


#### Scenario `FLEX_UP`

#### Summary (FLEX_UP)
```json
{
  "module_id": "Q4",
  "run_id": "FULL_20260211_191955_FLEX_UP",
  "selection": {
    "country": "FR",
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "year": 2024,
    "years": [
      2024
    ],
    "horizon_year": 2035,
    "objective": "LOW_PRICE_TARGET",
    "power_grid": [
      0.0,
      250.0,
      500.0,
      750.0,
      1000.0,
      1500.0
    ],
    "duration_grid": [
      2.0,
      4.0,
      6.0,
      8.0
    ],
    "scenario_ids": [
      "BASE",
      "FLEX_UP",
      "HIGH_CO2",
      "HIGH_GAS"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955"
  },
  "assumptions_used": [
    {
      "param_group": "Q4",
      "param_name": "bess_eta_roundtrip",
      "param_value": 0.88,
      "unit": "ratio",
      "description": "Rendement roundtrip BESS",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "bess_max_cycles_per_day",
      "param_value": 1.0,
      "unit": "cycles/day",
      "description": "Cycles max journaliers BESS",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "bess_soc_init_frac",
      "param_value": 0.5,
      "unit": "ratio",
      "description": "SOC initial fraction",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "target_far",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Cible FAR pour sizing",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "target_surplus_unabs_energy_twh",
      "param_value": 0.0,
      "unit": "TWh",
      "description": "Cible surplus non absorbe",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    }
  ],
  "kpis": {
    "n_runs": 7,
    "n_countries": 7,
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "compute_time_sec_total": 8.760316799995053,
    "cache_hit_share": 0.42857142857142855
  },
  "checks": [
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E)."
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4."
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4."
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes."
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes."
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "FLEX_UP",
  "horizon_year": 2035
}
```

#### Narratif (FLEX_UP)
Q4 scenario FLEX_UP: aggregation multi-pays (7 pays). Les tables detaillees conservent les lignes par pays.

#### Table SCEN FLEX_UP `Q4/scen/FLEX_UP/tables/Q4_bess_frontier.csv`
Lignes totales: `168` | Lignes DE/ES: `48`

##### DE (24 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,0,2,0
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,4,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,0,4,0
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,6,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,0,6,0
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,8,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,0,8,0
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,500,2,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,250,2,500
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1000,4,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,250,4,1000
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1500,6,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,250,6,1500
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,2000,8,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,250,8,2000
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,1000,2,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,500,2,1000
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,2000,4,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,500,4,2000
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,3000,6,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,500,6,3000
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,4000,8,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,500,8,4000
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,1500,2,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,750,2,1500
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,3000,4,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,750,4,3000
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,4500,6,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,750,6,4500
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,6000,8,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,750,8,6000
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,2000,2,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,1000,2,2000
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,4000,4,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,1000,4,4000
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,6000,6,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,1000,6,6000
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,8000,8,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,1000,8,8000
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,3000,2,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,1500,2,3000
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,6000,4,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,1500,4,6000
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,9000,6,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,1500,6,9000
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,12000,8,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,1500,8,12000
```

##### ES (24 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,0,2,0
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,4,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,0,4,0
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,6,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,0,6,0
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,8,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,0,8,0
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,500,2,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,250,2,500
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1000,4,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,250,4,1000
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1500,6,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,250,6,1500
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,2000,8,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,250,8,2000
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,1000,2,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,500,2,1000
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,2000,4,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,500,4,2000
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,3000,6,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,500,6,3000
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,4000,8,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,500,8,4000
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,1500,2,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,750,2,1500
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,3000,4,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,750,4,3000
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,4500,6,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,750,6,4500
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,6000,8,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,750,8,6000
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,2000,2,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,1000,2,2000
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,4000,4,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,1000,4,4000
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,6000,6,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,1000,6,6000
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,8000,8,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,1000,8,8000
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,3000,2,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,1500,2,3000
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,6000,4,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,1500,4,6000
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,9000,6,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,1500,6,9000
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,12000,8,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,1500,8,12000
```


#### Table SCEN FLEX_UP `Q4/scen/FLEX_UP/tables/Q4_sizing_summary.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh,objective_met,objective_reason,objective_not_reached,objective_target_value,objective_recommendation,pv_capacity_proxy_mw,power_grid_max_mw,duration_grid_max_h,grid_expansions_used,notes_quality
FLEX_UP,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,131.534,126.723,0.964054,0.980588,0.959969,0.977475,0.0165341,0.017506,0,0,126.806,124.263,126.268,123.869,122,38,34.6085,16.0375,0.1,0.1,0,0,0.0437608,0.0437608,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.974888,True,0,2,0,True,already_met,False,200,,21963.6,1500,8,0,ok
```

##### ES (1 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh,objective_met,objective_reason,objective_not_reached,objective_target_value,objective_recommendation,pv_capacity_proxy_mw,power_grid_max_mw,duration_grid_max_h,grid_expansions_used,notes_quality
FLEX_UP,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,99.3394,94.9608,0.927897,0.96373,0.973928,0.984461,0.0358335,0.0105323,0,0,92.1767,91.5166,96.7495,93.4851,195,53,44.7969,21.6413,0.1,0.1,0,0,0.0755906,0.0755906,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,1.28971,True,0,2,0,True,already_met,False,200,,14442.7,1500,8,0,ok
```


#### Scenario `HIGH_CO2`

#### Summary (HIGH_CO2)
```json
{
  "module_id": "Q4",
  "run_id": "FULL_20260211_191955_HIGH_CO2",
  "selection": {
    "country": "FR",
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "year": 2024,
    "years": [
      2024
    ],
    "horizon_year": 2035,
    "objective": "LOW_PRICE_TARGET",
    "power_grid": [
      0.0,
      250.0,
      500.0,
      750.0,
      1000.0,
      1500.0
    ],
    "duration_grid": [
      2.0,
      4.0,
      6.0,
      8.0
    ],
    "scenario_ids": [
      "BASE",
      "FLEX_UP",
      "HIGH_CO2",
      "HIGH_GAS"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955"
  },
  "assumptions_used": [
    {
      "param_group": "Q4",
      "param_name": "bess_eta_roundtrip",
      "param_value": 0.88,
      "unit": "ratio",
      "description": "Rendement roundtrip BESS",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "bess_max_cycles_per_day",
      "param_value": 1.0,
      "unit": "cycles/day",
      "description": "Cycles max journaliers BESS",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "bess_soc_init_frac",
      "param_value": 0.5,
      "unit": "ratio",
      "description": "SOC initial fraction",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "target_far",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Cible FAR pour sizing",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "target_surplus_unabs_energy_twh",
      "param_value": 0.0,
      "unit": "TWh",
      "description": "Cible surplus non absorbe",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    }
  ],
  "kpis": {
    "n_runs": 7,
    "n_countries": 7,
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "compute_time_sec_total": 9.01799630000096,
    "cache_hit_share": 0.2857142857142857
  },
  "checks": [
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E)."
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4."
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4."
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes."
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes."
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "HIGH_CO2",
  "horizon_year": 2035
}
```

#### Narratif (HIGH_CO2)
Q4 scenario HIGH_CO2: aggregation multi-pays (7 pays). Les tables detaillees conservent les lignes par pays.

#### Table SCEN HIGH_CO2 `Q4/scen/HIGH_CO2/tables/Q4_bess_frontier.csv`
Lignes totales: `168` | Lignes DE/ES: `48`

##### DE (24 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,0,2,0
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,4,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,0,4,0
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,6,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,0,6,0
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,8,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,0,8,0
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,500,2,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,250,2,500
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1000,4,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,250,4,1000
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1500,6,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,250,6,1500
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,2000,8,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,250,8,2000
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,1000,2,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,500,2,1000
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,2000,4,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,500,4,2000
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,3000,6,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,500,6,3000
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,4000,8,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,500,8,4000
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,1500,2,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,750,2,1500
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,3000,4,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,750,4,3000
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,4500,6,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,750,6,4500
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,6000,8,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,750,8,6000
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,2000,2,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,1000,2,2000
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,4000,4,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,1000,4,4000
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,6000,6,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,1000,6,6000
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,8000,8,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,1000,8,8000
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,3000,2,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,1500,2,3000
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,6000,4,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,1500,4,6000
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,9000,6,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,1500,6,9000
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,12000,8,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,1500,8,12000
```

##### ES (24 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,0,2,0
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,4,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,0,4,0
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,6,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,0,6,0
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,8,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,0,8,0
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,500,2,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,250,2,500
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1000,4,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,250,4,1000
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1500,6,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,250,6,1500
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,2000,8,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,250,8,2000
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,1000,2,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,500,2,1000
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,2000,4,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,500,4,2000
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,3000,6,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,500,6,3000
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,4000,8,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,500,8,4000
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,1500,2,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,750,2,1500
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,3000,4,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,750,4,3000
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,4500,6,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,750,6,4500
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,6000,8,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,750,8,6000
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,2000,2,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,1000,2,2000
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,4000,4,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,1000,4,4000
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,6000,6,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,1000,6,6000
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,8000,8,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,1000,8,8000
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,3000,2,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,1500,2,3000
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,6000,4,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,1500,4,6000
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,9000,6,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,1500,6,9000
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,12000,8,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,1500,8,12000
```


#### Table SCEN HIGH_CO2 `Q4/scen/HIGH_CO2/tables/Q4_sizing_summary.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh,objective_met,objective_reason,objective_not_reached,objective_target_value,objective_recommendation,pv_capacity_proxy_mw,power_grid_max_mw,duration_grid_max_h,grid_expansions_used,notes_quality
HIGH_CO2,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,143.209,138.147,0.965435,0.981389,0.96174,0.978553,0.0159537,0.0168136,0,0,138.259,135.576,137.73,135.184,122,42,36.0891,16.6449,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.889166,True,0,2,0,True,already_met,False,200,,21963.6,1500,8,0,ok
```

##### ES (1 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh,objective_met,objective_reason,objective_not_reached,objective_target_value,objective_recommendation,pv_capacity_proxy_mw,power_grid_max_mw,duration_grid_max_h,grid_expansions_used,notes_quality
HIGH_CO2,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,104.13,99.6442,0.929953,0.964932,0.974606,0.984895,0.0349794,0.010289,0,0,96.8359,96.1499,101.486,98.139,195,55,45.74,22.0486,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.882604,True,0,2,0,True,already_met,False,200,,14442.7,1500,8,0,ok
```


#### Scenario `HIGH_GAS`

#### Summary (HIGH_GAS)
```json
{
  "module_id": "Q4",
  "run_id": "FULL_20260211_191955_HIGH_GAS",
  "selection": {
    "country": "FR",
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "year": 2024,
    "years": [
      2024
    ],
    "horizon_year": 2035,
    "objective": "LOW_PRICE_TARGET",
    "power_grid": [
      0.0,
      250.0,
      500.0,
      750.0,
      1000.0,
      1500.0
    ],
    "duration_grid": [
      2.0,
      4.0,
      6.0,
      8.0
    ],
    "scenario_ids": [
      "BASE",
      "FLEX_UP",
      "HIGH_CO2",
      "HIGH_GAS"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955"
  },
  "assumptions_used": [
    {
      "param_group": "Q4",
      "param_name": "bess_eta_roundtrip",
      "param_value": 0.88,
      "unit": "ratio",
      "description": "Rendement roundtrip BESS",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "bess_max_cycles_per_day",
      "param_value": 1.0,
      "unit": "cycles/day",
      "description": "Cycles max journaliers BESS",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "bess_soc_init_frac",
      "param_value": 0.5,
      "unit": "ratio",
      "description": "SOC initial fraction",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "target_far",
      "param_value": 0.95,
      "unit": "ratio",
      "description": "Cible FAR pour sizing",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q4",
      "param_name": "target_surplus_unabs_energy_twh",
      "param_value": 0.0,
      "unit": "TWh",
      "description": "Cible surplus non absorbe",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    }
  ],
  "kpis": {
    "n_runs": 7,
    "n_countries": 7,
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "compute_time_sec_total": 9.614141299996845,
    "cache_hit_share": 0.2857142857142857
  },
  "checks": [
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_SURPLUS_NON_MONOTONIC_DOMINANCE",
      "message": "Surplus non absorbe non monotone en dominance (P,E)."
    },
    {
      "status": "WARN",
      "code": "Q4_FAR_NON_MONOTONIC_DOMINANCE",
      "message": "FAR non monotone en dominance (P,E)."
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4."
    },
    {
      "status": "INFO",
      "code": "Q4_CACHE_HIT",
      "message": "Resultat charge depuis cache persistant Q4."
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes."
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes."
    },
    {
      "status": "PASS",
      "code": "Q4_PASS",
      "message": "Q4 invariants et checks passes."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "HIGH_GAS",
  "horizon_year": 2035
}
```

#### Narratif (HIGH_GAS)
Q4 scenario HIGH_GAS: aggregation multi-pays (7 pays). Les tables detaillees conservent les lignes par pays.

#### Table SCEN HIGH_GAS `Q4/scen/HIGH_GAS/tables/Q4_bess_frontier.csv`
Lignes totales: `168` | Lignes DE/ES: `48`

##### DE (24 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,0,2,0
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,4,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,0,4,0
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,6,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,0,6,0
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,8,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,0,8,0
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,500,2,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,250,2,500
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1000,4,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,250,4,1000
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1500,6,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,250,6,1500
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,2000,8,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,250,8,2000
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,1000,2,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,500,2,1000
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,2000,4,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,500,4,2000
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,3000,6,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,500,6,3000
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,4000,8,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,500,8,4000
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,1500,2,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,750,2,1500
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,3000,4,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,750,4,3000
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,4500,6,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,750,6,4500
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,6000,8,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,750,8,6000
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,2000,2,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,1000,2,2000
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,4000,4,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,1000,4,4000
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,6000,6,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,1000,6,6000
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,8000,8,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,1000,8,8000
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,3000,2,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,1500,2,3000
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,6000,4,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,1500,4,6000
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,9000,6,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,1500,6,9000
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,12000,8,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,1500,8,12000
```

##### ES (24 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,0,2,0
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,4,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,0,4,0
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,6,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,0,6,0
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,8,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,0,8,0
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,500,2,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,250,2,500
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1000,4,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,250,4,1000
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,1500,6,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,250,6,1500
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,250,2000,8,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,250,8,2000
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,1000,2,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,500,2,1000
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,2000,4,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,500,4,2000
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,3000,6,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,500,6,3000
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,500,4000,8,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,500,8,4000
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,1500,2,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,750,2,1500
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,3000,4,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,750,4,3000
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,4500,6,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,750,6,4500
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,750,6000,8,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,750,8,6000
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,2000,2,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,1000,2,2000
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,4000,4,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,1000,4,4000
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,6000,6,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,1000,6,6000
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1000,8000,8,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,1000,8,8000
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,3000,2,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,1500,2,3000
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,6000,4,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,1500,4,6000
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,9000,6,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,1500,6,9000
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,1500,12000,8,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,1500,8,12000
```


#### Table SCEN HIGH_GAS `Q4/scen/HIGH_GAS/tables/Q4_sizing_summary.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh,objective_met,objective_reason,objective_not_reached,objective_target_value,objective_recommendation,pv_capacity_proxy_mw,power_grid_max_mw,duration_grid_max_h,grid_expansions_used,notes_quality
HIGH_GAS,DE,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,146.938,141.795,0.965812,0.981603,0.962244,0.978862,0.0157911,0.0166181,0,0,141.914,139.186,141.39,138.797,122,43,36.5685,16.8435,0.1,0.1,0,0,0.0437047,0.0437047,False,False,False,False,False,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.930724,True,0,2,0,True,already_met,False,200,,21963.6,1500,8,0,ok
```

##### ES (1 lignes)
```csv
scenario_id,country,year,dispatch_mode,objective,required_bess_power_mw,required_bess_energy_mwh,required_bess_duration_h,far_before,far_after,far_before_trivial,far_after_trivial,h_negative_before,h_negative_after,h_below_5_before,h_below_5_after,delta_h_negative,delta_h_below_5,baseload_price_before,baseload_price_after,capture_ratio_pv_before,capture_ratio_pv_after,capture_ratio_wind_before,capture_ratio_wind_after,delta_capture_ratio_pv,delta_capture_ratio_wind,surplus_unabs_energy_before,surplus_unabs_energy_after,pv_capture_price_before,pv_capture_price_after,wind_capture_price_before,wind_capture_price_after,days_spread_gt50_before,days_spread_gt50_after,avg_daily_spread_before,avg_daily_spread_after,low_residual_share_before,low_residual_share_after,sr_hours_share_before,sr_hours_share_after,ir_p10_before,ir_p10_after,turned_off_family_low_price,turned_off_family_physical,turned_off_family_value_pv,turned_off_family_value_wind,turned_off_family_any,revenue_bess_price_taker,soc_min,soc_max,soc_start_mwh,soc_end_mwh,soc_end_target_mwh,charge_max,discharge_max,charge_sum_mwh,discharge_sum_mwh,simultaneous_charge_discharge_hours,eta_roundtrip,eta_charge,eta_discharge,soc_boundary_mode,engine_version,compute_time_sec,cache_hit,bess_power_mw,duration_h,bess_energy_mwh,objective_met,objective_reason,objective_not_reached,objective_target_value,objective_recommendation,pv_capacity_proxy_mw,power_grid_max_mw,duration_grid_max_h,grid_expansions_used,notes_quality
HIGH_GAS,ES,2035,SURPLUS_FIRST,LOW_PRICE_TARGET,0,0,2,1,1,True,True,0,0,0,0,0,0,109.992,105.373,0.932058,0.966115,0.975338,0.985357,0.0340571,0.0100191,0,0,102.519,101.802,107.279,103.83,195,56,46.9444,22.5902,0.1,0.1,0,0,0.0755063,0.0755063,True,False,False,False,True,0,0,0,0,0,0,0,0,0,0,0,0.88,0.938083,0.938083,ZERO_END,v2.2.1,0.944639,True,0,2,0,True,already_met,False,200,,14442.7,1500,8,0,ok
```


## Q5

### GLOBAL

#### Summary (question)
```json
{
  "question_id": "Q5",
  "run_id": "FULL_20260211_191955",
  "selection": {
    "country": "FR",
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "years": [
      2018,
      2019,
      2020,
      2021,
      2022,
      2023,
      2024
    ],
    "marginal_tech": "CCGT",
    "marginal_tech_by_country": {
      "FR": "CCGT",
      "DE": "COAL",
      "ES": "CCGT",
      "NL": "CCGT",
      "BE": "CCGT",
      "CZ": "COAL",
      "IT_NORD": "CCGT"
    },
    "ttl_target_eur_mwh": 160.0,
    "scenario_ids": [
      "BASE",
      "HIGH_CO2",
      "HIGH_GAS",
      "HIGH_BOTH"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ]
  },
  "hist_module_id": "Q5",
  "scenarios": [
    "BASE",
    "HIGH_BOTH",
    "HIGH_CO2",
    "HIGH_GAS"
  ],
  "n_checks": 64,
  "n_warnings": 0,
  "n_test_rows": 10,
  "n_compare_rows": 84,
  "checks": [
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=13.6 EUR/MWh (acceptable).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=26.8 EUR/MWh (acceptable).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=8.0 EUR/MWh (acceptable).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=21.5 EUR/MWh (acceptable).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=36.4 EUR/MWh (acceptable).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "WARN",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=39.2 EUR/MWh (a revoir).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=20.5 EUR/MWh (acceptable).",
      "scope": "HIST",
      "scenario_id": ""
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=23.1 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=18.5 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=38.5 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=32.3 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=46.5 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=16.8 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=27.1 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "BASE"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=10.9 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "INFO",
      "code": "Q5_ALPHA_NEGATIVE",
      "message": "Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=25.2 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=40.5 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=33.1 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=33.8 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=15.5 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=28.0 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_CO2"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=10.9 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=20.8 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=41.2 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=34.1 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=22.9 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=16.6 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=29.0 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_GAS"
    },
    {
      "status": "WARN",
      "code": "Q5_ALPHA_NEGATIVE",
      "message": "Alpha negatif hors cas already_above_target.",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=36.1 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "INFO",
      "code": "Q5_ALPHA_NEGATIVE",
      "message": "Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=71.7 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "INFO",
      "code": "Q5_ALPHA_NEGATIVE",
      "message": "Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=62.1 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "INFO",
      "code": "Q5_ALPHA_NEGATIVE",
      "message": "Alpha negatif mais TTL deja au-dessus de la cible (lecture normale).",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=45.3 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=21.1 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "WARN",
      "code": "Q5_ALPHA_NEGATIVE",
      "message": "Alpha negatif hors cas already_above_target.",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=42.5 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "WARN",
      "code": "Q5_ALPHA_NEGATIVE",
      "message": "Alpha negatif hors cas already_above_target.",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=50.9 EUR/MWh (acceptable).",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire).",
      "scope": "SCEN",
      "scenario_id": "HIGH_BOTH"
    },
    {
      "status": "PASS",
      "code": "BUNDLE_LEDGER_STATUS",
      "message": "ledger: FAIL=0, WARN=0",
      "scope": "BUNDLE",
      "scenario_id": ""
    },
    {
      "status": "PASS",
      "code": "BUNDLE_INFORMATIVENESS",
      "message": "share_tests_informatifs=100.00% ; share_compare_informatifs=95.24%",
      "scope": "BUNDLE",
      "scenario_id": ""
    }
  ],
  "warnings": []
}
```

#### Narratif (question)
Analyse complete Q5: historique + prospectif en un seul run. Statut global=WARN. Tests PASS=10, WARN=0, FAIL=0, NON_TESTABLE=0. Les resultats sont separes entre historique et scenarios, puis compares dans une table unique.

#### Table `Q5/test_ledger.csv`
Lignes: `10`

```csv
test_id,question_id,source_ref,mode,scenario_group,title,what_is_tested,metric_rule,severity_if_fail,scenario_id,status,value,threshold,interpretation
Q5-S-01,Q5,SPEC2-Q5/Slides 29,SCEN,DEFAULT,Sensibilites scenarisees,BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.,Q5_summary non vide sur scenarios selectionnes,HIGH,BASE,PASS,7,>0 lignes,Sensibilites scenario calculees.
Q5-S-02,Q5,SPEC2-Q5/Slides 31,SCEN,DEFAULT,CO2 requis pour TTL cible,Le CO2 requis est calcule et interpretable.,co2_required_* non NaN,MEDIUM,BASE,PASS,share_finite=100.00%,>=80% valeurs finies,CO2 requis interpretable sur le panel.
Q5-S-01,Q5,SPEC2-Q5/Slides 29,SCEN,DEFAULT,Sensibilites scenarisees,BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.,Q5_summary non vide sur scenarios selectionnes,HIGH,HIGH_BOTH,PASS,7,>0 lignes,Sensibilites scenario calculees.
Q5-S-02,Q5,SPEC2-Q5/Slides 31,SCEN,DEFAULT,CO2 requis pour TTL cible,Le CO2 requis est calcule et interpretable.,co2_required_* non NaN,MEDIUM,HIGH_BOTH,PASS,share_finite=100.00%,>=80% valeurs finies,CO2 requis interpretable sur le panel.
Q5-S-01,Q5,SPEC2-Q5/Slides 29,SCEN,DEFAULT,Sensibilites scenarisees,BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.,Q5_summary non vide sur scenarios selectionnes,HIGH,HIGH_CO2,PASS,7,>0 lignes,Sensibilites scenario calculees.
Q5-S-02,Q5,SPEC2-Q5/Slides 31,SCEN,DEFAULT,CO2 requis pour TTL cible,Le CO2 requis est calcule et interpretable.,co2_required_* non NaN,MEDIUM,HIGH_CO2,PASS,share_finite=100.00%,>=80% valeurs finies,CO2 requis interpretable sur le panel.
Q5-S-01,Q5,SPEC2-Q5/Slides 29,SCEN,DEFAULT,Sensibilites scenarisees,BASE/HIGH_CO2/HIGH_GAS/HIGH_BOTH sont compares.,Q5_summary non vide sur scenarios selectionnes,HIGH,HIGH_GAS,PASS,7,>0 lignes,Sensibilites scenario calculees.
Q5-S-02,Q5,SPEC2-Q5/Slides 31,SCEN,DEFAULT,CO2 requis pour TTL cible,Le CO2 requis est calcule et interpretable.,co2_required_* non NaN,MEDIUM,HIGH_GAS,PASS,share_finite=100.00%,>=80% valeurs finies,CO2 requis interpretable sur le panel.
Q5-H-01,Q5,SPEC2-Q5/Slides 28,HIST,HIST_BASE,Ancre thermique historique,TTL/TCA/alpha/corr sont estimes hors surplus.,Q5_summary non vide avec ttl_obs et tca_q95,HIGH,nan,PASS,share_fini=100.00%,>=80% lignes ttl/tca finies,L'ancre thermique est quantifiable sur la majorite des pays.
Q5-H-02,Q5,SPEC2-Q5,HIST,HIST_BASE,Sensibilites analytiques,dTCA/dCO2 et dTCA/dGas sont positives.,dTCA_dCO2 > 0 et dTCA_dGas > 0,CRITICAL,nan,PASS,share_positive=100.00%,100% lignes >0,Sensibilites analytiques globalement coherentes.
```


#### Table `Q5/comparison_hist_vs_scen.csv`
Lignes totales: `84` | Lignes DE/ES: `24`

##### DE (12 lignes)
```csv
country,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
DE,BASE,co2_required_base_non_negative,98.1965,0,-98.1965,,INFORMATIVE,delta_interpretable
DE,BASE,tca_q95,131.52,158.868,27.3489,,INFORMATIVE,delta_interpretable
DE,BASE,ttl_obs,146.069,212.658,66.589,,INFORMATIVE,delta_interpretable
DE,HIGH_BOTH,co2_required_base_non_negative,98.1965,0,-98.1965,,INFORMATIVE,delta_interpretable
DE,HIGH_BOTH,tca_q95,131.52,236.303,104.783,,INFORMATIVE,delta_interpretable
DE,HIGH_BOTH,ttl_obs,146.069,212.658,66.589,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,co2_required_base_non_negative,98.1965,0,-98.1965,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,tca_q95,131.52,203.737,72.2173,,INFORMATIVE,delta_interpretable
DE,HIGH_CO2,ttl_obs,146.069,228.362,82.293,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,co2_required_base_non_negative,98.1965,0,-98.1965,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,tca_q95,131.52,191.434,59.9147,,INFORMATIVE,delta_interpretable
DE,HIGH_GAS,ttl_obs,146.069,233.382,87.3127,,INFORMATIVE,delta_interpretable
```

##### ES (12 lignes)
```csv
country,scenario_id,metric,hist_value,scen_value,delta,scen_status,interpretability_status,interpretability_reason
ES,BASE,co2_required_base_non_negative,194.703,0,-194.703,,INFORMATIVE,delta_interpretable
ES,BASE,tca_q95,113.009,121.545,8.53691,,INFORMATIVE,delta_interpretable
ES,BASE,ttl_obs,140,167.763,27.7631,,INFORMATIVE,delta_interpretable
ES,HIGH_BOTH,co2_required_base_non_negative,194.703,0,-194.703,,INFORMATIVE,delta_interpretable
ES,HIGH_BOTH,tca_q95,113.009,180.818,67.8096,,INFORMATIVE,delta_interpretable
ES,HIGH_BOTH,ttl_obs,140,167.763,27.7631,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,co2_required_base_non_negative,194.703,0,-194.703,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,tca_q95,113.009,139.909,26.9005,,INFORMATIVE,delta_interpretable
ES,HIGH_CO2,ttl_obs,140,174.19,34.1904,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,co2_required_base_non_negative,194.703,0,-194.703,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,tca_q95,113.009,162.455,49.446,,INFORMATIVE,delta_interpretable
ES,HIGH_GAS,ttl_obs,140,182.081,42.0813,,INFORMATIVE,delta_interpretable
```


### HIST

#### Summary (hist)
```json
{
  "module_id": "Q5",
  "run_id": "FULL_20260211_191955_HIST",
  "selection": {
    "country": "FR",
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "years": [
      2018,
      2019,
      2020,
      2021,
      2022,
      2023,
      2024
    ],
    "marginal_tech": "CCGT",
    "marginal_tech_by_country": {
      "FR": "CCGT",
      "DE": "COAL",
      "ES": "CCGT",
      "NL": "CCGT",
      "BE": "CCGT",
      "CZ": "COAL",
      "IT_NORD": "CCGT"
    },
    "ttl_target_eur_mwh": 160.0,
    "scenario_ids": [
      "BASE",
      "HIGH_CO2",
      "HIGH_GAS",
      "HIGH_BOTH"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "mode": "HIST",
    "run_id": "FULL_20260211_191955"
  },
  "assumptions_used": [
    {
      "param_group": "Q5",
      "param_name": "ccgt_ef_t_per_mwh_th",
      "param_value": 0.202,
      "unit": "tCO2/MWhth",
      "description": "Facteur emission CCGT",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "ccgt_efficiency",
      "param_value": 0.55,
      "unit": "ratio",
      "description": "Rendement CCGT",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "ccgt_vom_eur_mwh",
      "param_value": 3.0,
      "unit": "EUR/MWh",
      "description": "VOM CCGT",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "coal_ef_t_per_mwh_th",
      "param_value": 0.341,
      "unit": "tCO2/MWhth",
      "description": "Facteur emission charbon",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "coal_efficiency",
      "param_value": 0.38,
      "unit": "ratio",
      "description": "Rendement charbon",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "coal_vom_eur_mwh",
      "param_value": 4.0,
      "unit": "EUR/MWh",
      "description": "VOM charbon",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    }
  ],
  "kpis": {
    "n_runs": 7,
    "n_countries": 7,
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "compute_time_sec_total": 0.0
  },
  "checks": [
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=13.6 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=26.8 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=8.0 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=21.5 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=36.4 EUR/MWh (acceptable)."
    },
    {
      "status": "WARN",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=39.2 EUR/MWh (a revoir)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=20.5 EUR/MWh (acceptable)."
    }
  ],
  "warnings": [],
  "mode": "HIST",
  "scenario_id": null,
  "horizon_year": 2024
}
```

#### Narratif (hist)
Q5 historique: aggregation multi-pays (7 pays). Les tables detaillees conservent les lignes par pays.

#### Table HIST `Q5/hist/tables/Q5_summary.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,year_range_used,ttl_reference_mode,ttl_reference_year,marginal_tech,chosen_anchor_tech,fuel_used,ttl_obs,ttl_obs_price_cd,ttl_annual_metrics_same_year,ttl_anchor,ttl_physical,ttl_regression,ttl_method,tca_q95,alpha,alpha_effective,corr_cd,anchor_confidence,anchor_distribution_error_p90_p95,anchor_error_p90,anchor_error_p95,anchor_status,dTCA_dCO2,dTCA_dFuel,dTCA_dGas,eta_implicit_from_dTCA_dFuel,ef_implicit_t_per_mwh_e,ttl_target,required_co2_eur_t,required_gas_eur_mwh_th,co2_required_base,co2_required_gas_override,co2_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality
DE,2018-2024,year_specific,2024,COAL,COAL,coal,146.069,146.069,146.069,131.52,131.52,,anchor_distributional,131.52,14.5495,14.5495,0.278699,0.900605,7.95163,-1.35079,14.5525,ok,0.897368,2.63158,1.44737,0.38,0.897368,160,98.1965,63.8672,98.1965,,98.1965,,
```

##### ES (1 lignes)
```csv
country,year_range_used,ttl_reference_mode,ttl_reference_year,marginal_tech,chosen_anchor_tech,fuel_used,ttl_obs,ttl_obs_price_cd,ttl_annual_metrics_same_year,ttl_anchor,ttl_physical,ttl_regression,ttl_method,tca_q95,alpha,alpha_effective,corr_cd,anchor_confidence,anchor_distribution_error_p90_p95,anchor_error_p90,anchor_error_p95,anchor_status,dTCA_dCO2,dTCA_dFuel,dTCA_dGas,eta_implicit_from_dTCA_dFuel,ef_implicit_t_per_mwh_e,ttl_target,required_co2_eur_t,required_gas_eur_mwh_th,co2_required_base,co2_required_gas_override,co2_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality
ES,2018-2024,year_specific,2024,CCGT,CCGT,gas,140,140,140,113.009,113.009,,anchor_distributional,113.009,26.9915,26.9915,0.632851,0.731868,21.4505,15.9096,26.9915,ok,0.367273,1.81818,1.81818,0.55,0.367273,160,194.703,72.0706,194.703,,194.703,,
```


### SCEN

#### Scenario `BASE`

#### Summary (BASE)
```json
{
  "module_id": "Q5",
  "run_id": "FULL_20260211_191955_BASE",
  "selection": {
    "country": "FR",
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "years": [
      2018,
      2019,
      2020,
      2021,
      2022,
      2023,
      2024
    ],
    "marginal_tech": "CCGT",
    "marginal_tech_by_country": {
      "FR": "CCGT",
      "DE": "COAL",
      "ES": "CCGT",
      "NL": "CCGT",
      "BE": "CCGT",
      "CZ": "COAL",
      "IT_NORD": "CCGT"
    },
    "ttl_target_eur_mwh": 160.0,
    "scenario_ids": [
      "BASE",
      "HIGH_CO2",
      "HIGH_GAS",
      "HIGH_BOTH"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955"
  },
  "assumptions_used": [
    {
      "param_group": "Q5",
      "param_name": "ccgt_ef_t_per_mwh_th",
      "param_value": 0.202,
      "unit": "tCO2/MWhth",
      "description": "Facteur emission CCGT",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "ccgt_efficiency",
      "param_value": 0.55,
      "unit": "ratio",
      "description": "Rendement CCGT",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "ccgt_vom_eur_mwh",
      "param_value": 3.0,
      "unit": "EUR/MWh",
      "description": "VOM CCGT",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "coal_ef_t_per_mwh_th",
      "param_value": 0.341,
      "unit": "tCO2/MWhth",
      "description": "Facteur emission charbon",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "coal_efficiency",
      "param_value": 0.38,
      "unit": "ratio",
      "description": "Rendement charbon",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "coal_vom_eur_mwh",
      "param_value": 4.0,
      "unit": "EUR/MWh",
      "description": "VOM charbon",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    }
  ],
  "kpis": {
    "n_runs": 7,
    "n_countries": 7,
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "compute_time_sec_total": 0.0
  },
  "checks": [
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=23.1 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=18.5 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=38.5 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=32.3 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=46.5 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=16.8 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=27.1 EUR/MWh (acceptable)."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "BASE",
  "horizon_year": 2035
}
```

#### Narratif (BASE)
Q5 scenario BASE: aggregation multi-pays (7 pays). Les tables detaillees conservent les lignes par pays.

#### Table SCEN BASE `Q5/scen/BASE/tables/Q5_summary.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,year_range_used,ttl_reference_mode,ttl_reference_year,marginal_tech,chosen_anchor_tech,fuel_used,ttl_obs,ttl_obs_price_cd,ttl_annual_metrics_same_year,ttl_anchor,ttl_physical,ttl_regression,ttl_method,tca_q95,alpha,alpha_effective,corr_cd,anchor_confidence,anchor_distribution_error_p90_p95,anchor_error_p90,anchor_error_p95,anchor_status,dTCA_dCO2,dTCA_dFuel,dTCA_dGas,eta_implicit_from_dTCA_dFuel,ef_implicit_t_per_mwh_e,ttl_target,required_co2_eur_t,required_gas_eur_mwh_th,co2_required_base,co2_required_gas_override,co2_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality
DE,2025-2035,year_specific,2035,COAL,COAL,coal,212.658,212.658,212.658,158.868,158.868,,anchor_distributional,158.868,53.7896,53.7896,3.62873e-16,0.518831,38.4935,-23.1975,53.7896,already_above_target,0.897368,2.63158,1.44737,0.38,0.897368,160,0,0,0,,0,,
```

##### ES (1 lignes)
```csv
country,year_range_used,ttl_reference_mode,ttl_reference_year,marginal_tech,chosen_anchor_tech,fuel_used,ttl_obs,ttl_obs_price_cd,ttl_annual_metrics_same_year,ttl_anchor,ttl_physical,ttl_regression,ttl_method,tca_q95,alpha,alpha_effective,corr_cd,anchor_confidence,anchor_distribution_error_p90_p95,anchor_error_p90,anchor_error_p95,anchor_status,dTCA_dCO2,dTCA_dFuel,dTCA_dGas,eta_implicit_from_dTCA_dFuel,ef_implicit_t_per_mwh_e,ttl_target,required_co2_eur_t,required_gas_eur_mwh_th,co2_required_base,co2_required_gas_override,co2_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality
ES,2025-2035,year_specific,2035,CCGT,CCGT,gas,167.763,167.763,167.763,121.545,121.545,,anchor_distributional,121.545,46.2176,46.2176,,0.596614,32.2709,-18.3241,46.2176,already_above_target,0.367273,1.81818,1.81818,0.55,0.367273,160,0,0,0,,0,,
```


#### Scenario `HIGH_BOTH`

#### Summary (HIGH_BOTH)
```json
{
  "module_id": "Q5",
  "run_id": "FULL_20260211_191955_HIGH_BOTH",
  "selection": {
    "country": "FR",
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "years": [
      2018,
      2019,
      2020,
      2021,
      2022,
      2023,
      2024
    ],
    "marginal_tech": "CCGT",
    "marginal_tech_by_country": {
      "FR": "CCGT",
      "DE": "COAL",
      "ES": "CCGT",
      "NL": "CCGT",
      "BE": "CCGT",
      "CZ": "COAL",
      "IT_NORD": "CCGT"
    },
    "ttl_target_eur_mwh": 160.0,
    "scenario_ids": [
      "BASE",
      "HIGH_CO2",
      "HIGH_GAS",
      "HIGH_BOTH"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955"
  },
  "assumptions_used": [
    {
      "param_group": "Q5",
      "param_name": "ccgt_ef_t_per_mwh_th",
      "param_value": 0.202,
      "unit": "tCO2/MWhth",
      "description": "Facteur emission CCGT",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "ccgt_efficiency",
      "param_value": 0.55,
      "unit": "ratio",
      "description": "Rendement CCGT",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "ccgt_vom_eur_mwh",
      "param_value": 3.0,
      "unit": "EUR/MWh",
      "description": "VOM CCGT",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "coal_ef_t_per_mwh_th",
      "param_value": 0.341,
      "unit": "tCO2/MWhth",
      "description": "Facteur emission charbon",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "coal_efficiency",
      "param_value": 0.38,
      "unit": "ratio",
      "description": "Rendement charbon",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "coal_vom_eur_mwh",
      "param_value": 4.0,
      "unit": "EUR/MWh",
      "description": "VOM charbon",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    }
  ],
  "kpis": {
    "n_runs": 7,
    "n_countries": 7,
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "compute_time_sec_total": 0.0
  },
  "checks": [
    {
      "status": "WARN",
      "code": "Q5_ALPHA_NEGATIVE",
      "message": "Alpha negatif hors cas already_above_target."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=36.1 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "INFO",
      "code": "Q5_ALPHA_NEGATIVE",
      "message": "Alpha negatif mais TTL deja au-dessus de la cible (lecture normale)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=71.7 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_ALPHA_NEGATIVE",
      "message": "Alpha negatif mais TTL deja au-dessus de la cible (lecture normale)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=62.1 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_ALPHA_NEGATIVE",
      "message": "Alpha negatif mais TTL deja au-dessus de la cible (lecture normale)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=45.3 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=21.1 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "WARN",
      "code": "Q5_ALPHA_NEGATIVE",
      "message": "Alpha negatif hors cas already_above_target."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=42.5 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "WARN",
      "code": "Q5_ALPHA_NEGATIVE",
      "message": "Alpha negatif hors cas already_above_target."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=50.9 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "HIGH_BOTH",
  "horizon_year": 2035
}
```

#### Narratif (HIGH_BOTH)
Q5 scenario HIGH_BOTH: aggregation multi-pays (7 pays). Les tables detaillees conservent les lignes par pays.

#### Table SCEN HIGH_BOTH `Q5/scen/HIGH_BOTH/tables/Q5_summary.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,year_range_used,ttl_reference_mode,ttl_reference_year,marginal_tech,chosen_anchor_tech,fuel_used,ttl_obs,ttl_obs_price_cd,ttl_annual_metrics_same_year,ttl_anchor,ttl_physical,ttl_regression,ttl_method,tca_q95,alpha,alpha_effective,corr_cd,anchor_confidence,anchor_distribution_error_p90_p95,anchor_error_p90,anchor_error_p95,anchor_status,dTCA_dCO2,dTCA_dFuel,dTCA_dGas,eta_implicit_from_dTCA_dFuel,ef_implicit_t_per_mwh_e,ttl_target,required_co2_eur_t,required_gas_eur_mwh_th,co2_required_base,co2_required_gas_override,co2_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality
DE,2025-2035,year_specific,2035,COAL,COAL,coal,212.658,212.658,212.658,236.303,236.303,,anchor_distributional,236.303,-23.6446,-23.6446,,0.223273,62.1382,-100.632,-23.6446,already_above_target,0.897368,2.63158,1.44737,0.38,0.897368,160,0,0,0,,0,,
```

##### ES (1 lignes)
```csv
country,year_range_used,ttl_reference_mode,ttl_reference_year,marginal_tech,chosen_anchor_tech,fuel_used,ttl_obs,ttl_obs_price_cd,ttl_annual_metrics_same_year,ttl_anchor,ttl_physical,ttl_regression,ttl_method,tca_q95,alpha,alpha_effective,corr_cd,anchor_confidence,anchor_distribution_error_p90_p95,anchor_error_p90,anchor_error_p95,anchor_status,dTCA_dCO2,dTCA_dFuel,dTCA_dGas,eta_implicit_from_dTCA_dFuel,ef_implicit_t_per_mwh_e,ttl_target,required_co2_eur_t,required_gas_eur_mwh_th,co2_required_base,co2_required_gas_override,co2_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality
ES,2025-2035,year_specific,2035,CCGT,CCGT,gas,167.763,167.763,167.763,180.818,180.818,,anchor_distributional,180.818,-13.0551,-13.0551,-3.10166e-16,0.433426,45.3259,-77.5968,-13.0551,already_above_target,0.367273,1.81818,1.81818,0.55,0.367273,160,0,0,0,,0,,
```


#### Scenario `HIGH_CO2`

#### Summary (HIGH_CO2)
```json
{
  "module_id": "Q5",
  "run_id": "FULL_20260211_191955_HIGH_CO2",
  "selection": {
    "country": "FR",
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "years": [
      2018,
      2019,
      2020,
      2021,
      2022,
      2023,
      2024
    ],
    "marginal_tech": "CCGT",
    "marginal_tech_by_country": {
      "FR": "CCGT",
      "DE": "COAL",
      "ES": "CCGT",
      "NL": "CCGT",
      "BE": "CCGT",
      "CZ": "COAL",
      "IT_NORD": "CCGT"
    },
    "ttl_target_eur_mwh": 160.0,
    "scenario_ids": [
      "BASE",
      "HIGH_CO2",
      "HIGH_GAS",
      "HIGH_BOTH"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955"
  },
  "assumptions_used": [
    {
      "param_group": "Q5",
      "param_name": "ccgt_ef_t_per_mwh_th",
      "param_value": 0.202,
      "unit": "tCO2/MWhth",
      "description": "Facteur emission CCGT",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "ccgt_efficiency",
      "param_value": 0.55,
      "unit": "ratio",
      "description": "Rendement CCGT",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "ccgt_vom_eur_mwh",
      "param_value": 3.0,
      "unit": "EUR/MWh",
      "description": "VOM CCGT",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "coal_ef_t_per_mwh_th",
      "param_value": 0.341,
      "unit": "tCO2/MWhth",
      "description": "Facteur emission charbon",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "coal_efficiency",
      "param_value": 0.38,
      "unit": "ratio",
      "description": "Rendement charbon",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "coal_vom_eur_mwh",
      "param_value": 4.0,
      "unit": "EUR/MWh",
      "description": "VOM charbon",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    }
  ],
  "kpis": {
    "n_runs": 7,
    "n_countries": 7,
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "compute_time_sec_total": 0.0
  },
  "checks": [
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=10.9 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_ALPHA_NEGATIVE",
      "message": "Alpha negatif mais TTL deja au-dessus de la cible (lecture normale)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=25.2 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=40.5 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=33.1 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=33.8 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=15.5 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=28.0 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "HIGH_CO2",
  "horizon_year": 2035
}
```

#### Narratif (HIGH_CO2)
Q5 scenario HIGH_CO2: aggregation multi-pays (7 pays). Les tables detaillees conservent les lignes par pays.

#### Table SCEN HIGH_CO2 `Q5/scen/HIGH_CO2/tables/Q5_summary.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,year_range_used,ttl_reference_mode,ttl_reference_year,marginal_tech,chosen_anchor_tech,fuel_used,ttl_obs,ttl_obs_price_cd,ttl_annual_metrics_same_year,ttl_anchor,ttl_physical,ttl_regression,ttl_method,tca_q95,alpha,alpha_effective,corr_cd,anchor_confidence,anchor_distribution_error_p90_p95,anchor_error_p90,anchor_error_p95,anchor_status,dTCA_dCO2,dTCA_dFuel,dTCA_dGas,eta_implicit_from_dTCA_dFuel,ef_implicit_t_per_mwh_e,ttl_target,required_co2_eur_t,required_gas_eur_mwh_th,co2_required_base,co2_required_gas_override,co2_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality
DE,2025-2035,year_specific,2035,COAL,COAL,coal,228.362,228.362,228.362,203.737,203.737,,anchor_distributional,203.737,24.6251,24.6251,-3.28773e-17,0.493592,40.5126,-56.4001,24.6251,already_above_target,0.897368,2.63158,1.44737,0.38,0.897368,160,0,0,0,,0,,
```

##### ES (1 lignes)
```csv
country,year_range_used,ttl_reference_mode,ttl_reference_year,marginal_tech,chosen_anchor_tech,fuel_used,ttl_obs,ttl_obs_price_cd,ttl_annual_metrics_same_year,ttl_anchor,ttl_physical,ttl_regression,ttl_method,tca_q95,alpha,alpha_effective,corr_cd,anchor_confidence,anchor_distribution_error_p90_p95,anchor_error_p90,anchor_error_p95,anchor_status,dTCA_dCO2,dTCA_dFuel,dTCA_dGas,eta_implicit_from_dTCA_dFuel,ef_implicit_t_per_mwh_e,ttl_target,required_co2_eur_t,required_gas_eur_mwh_th,co2_required_base,co2_required_gas_override,co2_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality
ES,2025-2035,year_specific,2035,CCGT,CCGT,gas,174.19,174.19,174.19,139.909,139.909,,anchor_distributional,139.909,34.2813,34.2813,-1.53141e-16,0.586285,33.0972,-31.9132,34.2813,already_above_target,0.367273,1.81818,1.81818,0.55,0.367273,160,0,0,0,,0,,
```


#### Scenario `HIGH_GAS`

#### Summary (HIGH_GAS)
```json
{
  "module_id": "Q5",
  "run_id": "FULL_20260211_191955_HIGH_GAS",
  "selection": {
    "country": "FR",
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "years": [
      2018,
      2019,
      2020,
      2021,
      2022,
      2023,
      2024
    ],
    "marginal_tech": "CCGT",
    "marginal_tech_by_country": {
      "FR": "CCGT",
      "DE": "COAL",
      "ES": "CCGT",
      "NL": "CCGT",
      "BE": "CCGT",
      "CZ": "COAL",
      "IT_NORD": "CCGT"
    },
    "ttl_target_eur_mwh": 160.0,
    "scenario_ids": [
      "BASE",
      "HIGH_CO2",
      "HIGH_GAS",
      "HIGH_BOTH"
    ],
    "scenario_years": [
      2025,
      2026,
      2027,
      2028,
      2029,
      2030,
      2031,
      2032,
      2033,
      2034,
      2035
    ],
    "run_id": "FULL_20260211_191955"
  },
  "assumptions_used": [
    {
      "param_group": "Q5",
      "param_name": "ccgt_ef_t_per_mwh_th",
      "param_value": 0.202,
      "unit": "tCO2/MWhth",
      "description": "Facteur emission CCGT",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "ccgt_efficiency",
      "param_value": 0.55,
      "unit": "ratio",
      "description": "Rendement CCGT",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "ccgt_vom_eur_mwh",
      "param_value": 3.0,
      "unit": "EUR/MWh",
      "description": "VOM CCGT",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "coal_ef_t_per_mwh_th",
      "param_value": 0.341,
      "unit": "tCO2/MWhth",
      "description": "Facteur emission charbon",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "coal_efficiency",
      "param_value": 0.38,
      "unit": "ratio",
      "description": "Rendement charbon",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    },
    {
      "param_group": "Q5",
      "param_name": "coal_vom_eur_mwh",
      "param_value": 4.0,
      "unit": "EUR/MWh",
      "description": "VOM charbon",
      "source": "default",
      "last_updated": "2026-02-09",
      "owner": "system"
    }
  ],
  "kpis": {
    "n_runs": 7,
    "n_countries": 7,
    "countries": [
      "BE",
      "CZ",
      "DE",
      "ES",
      "FR",
      "IT_NORD",
      "NL"
    ],
    "compute_time_sec_total": 0.0
  },
  "checks": [
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=10.9 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=20.8 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=41.2 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=34.1 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=22.9 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=16.6 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    },
    {
      "status": "INFO",
      "code": "Q5_DISTRIBUTIONAL_FIT",
      "message": "Erreur distributionnelle p90/p95=29.0 EUR/MWh (acceptable)."
    },
    {
      "status": "INFO",
      "code": "Q5_LOW_CORR_CD",
      "message": "Corr horaire faible mais non bloquante (fit distributionnel prioritaire)."
    }
  ],
  "warnings": [],
  "mode": "SCEN",
  "scenario_id": "HIGH_GAS",
  "horizon_year": 2035
}
```

#### Narratif (HIGH_GAS)
Q5 scenario HIGH_GAS: aggregation multi-pays (7 pays). Les tables detaillees conservent les lignes par pays.

#### Table SCEN HIGH_GAS `Q5/scen/HIGH_GAS/tables/Q5_summary.csv`
Lignes totales: `7` | Lignes DE/ES: `2`

##### DE (1 lignes)
```csv
country,year_range_used,ttl_reference_mode,ttl_reference_year,marginal_tech,chosen_anchor_tech,fuel_used,ttl_obs,ttl_obs_price_cd,ttl_annual_metrics_same_year,ttl_anchor,ttl_physical,ttl_regression,ttl_method,tca_q95,alpha,alpha_effective,corr_cd,anchor_confidence,anchor_distribution_error_p90_p95,anchor_error_p90,anchor_error_p95,anchor_status,dTCA_dCO2,dTCA_dFuel,dTCA_dGas,eta_implicit_from_dTCA_dFuel,ef_implicit_t_per_mwh_e,ttl_target,required_co2_eur_t,required_gas_eur_mwh_th,co2_required_base,co2_required_gas_override,co2_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality
DE,2025-2035,year_specific,2035,COAL,COAL,coal,233.382,233.382,233.382,191.434,191.434,,anchor_distributional,191.434,41.9475,41.9475,-2.43791e-17,0.485525,41.158,-40.3685,41.9475,already_above_target,0.897368,2.63158,1.44737,0.38,0.897368,160,0,0,0,,0,,
```

##### ES (1 lignes)
```csv
country,year_range_used,ttl_reference_mode,ttl_reference_year,marginal_tech,chosen_anchor_tech,fuel_used,ttl_obs,ttl_obs_price_cd,ttl_annual_metrics_same_year,ttl_anchor,ttl_physical,ttl_regression,ttl_method,tca_q95,alpha,alpha_effective,corr_cd,anchor_confidence,anchor_distribution_error_p90_p95,anchor_error_p90,anchor_error_p95,anchor_status,dTCA_dCO2,dTCA_dFuel,dTCA_dGas,eta_implicit_from_dTCA_dFuel,ef_implicit_t_per_mwh_e,ttl_target,required_co2_eur_t,required_gas_eur_mwh_th,co2_required_base,co2_required_gas_override,co2_required_base_non_negative,co2_required_gas_override_non_negative,warnings_quality
ES,2025-2035,year_specific,2035,CCGT,CCGT,gas,182.081,182.081,182.081,162.455,162.455,,anchor_distributional,162.455,19.6267,19.6267,2.34011e-16,0.573603,34.1118,-48.5968,19.6267,already_above_target,0.367273,1.81818,1.81818,0.55,0.367273,160,0,0,0,,0,,
```

