# Registre d'Ecarts — SPEC 0 / SPEC 1 / SPEC 2 + Slides

Date de mise a jour: 2026-02-10

## Etat global
- SPEC 0: PARTIEL -> en grande partie cable dans le code (conventions, anti-circularite, checks), mais le document normatif peut encore etre enrichi.
- SPEC 1: OK -> socle ingestion/cache/normalisation/metrics/tests en place.
- SPEC 2 historique: OK -> Q1..Q5 implementes avec checks et exports.
- SPEC 2 prospectif (attendu dans le plan verrouille): OK -> moteur scenario + execution Q1..Q5 en mode SCEN.
- Slides 1-33: OK -> matrice de couverture exportee (`reports/coverage_matrix_slides_q1_q5.csv`).

## Mapping des exigences critiques
| Exigence | Composant | Statut |
|---|---|---|
| Conventions horaires UTC, pas d'imputation silencieuse | `src/data_fetcher.py`, `src/processing.py` | OK |
| Anti-circularite regimes A/B/C/D sans prix | `src/processing.py`, `src/modules/reality_checks.py` | OK |
| Tables canoniques horaires/annuelles | `data/processed/hourly/*`, `data/metrics/annual_metrics.parquet` | OK |
| Quality report + findings | `src/validation_report.py`, `data/metrics/validation_findings.parquet` | OK |
| Q1..Q5 historiques + exports | `src/modules/q*.py`, `outputs/phase1/*` | OK |
| Mode prospectif scenario x pays x annee | `src/scenario/phase2_engine.py`, `data/assumptions/phase2/*` | OK |
| Q1..Q5 prospectifs + exports | pages Q1..Q5 mode SCEN, `outputs/phase2/*` | OK |
| Rapport final detaille long et autoportant | `generate_report.py`, `reports/conclusions_v2_detailed_*.md` | OK |

## Risques residuels
- Les scenarios restent mecanistes (pas de modele d'equilibre complet), conforme au perimetre, mais a rappeler dans chaque conclusion.
- Certaines conclusions economiques Q5 restent sensibles a la qualite des series commodites et a la correlation prix-ancre.
- Les seuils business doivent rester revus periodiquement dans `data/assumptions/phase1_assumptions.csv`.
