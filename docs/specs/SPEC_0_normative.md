# SPEC 0 — Conventions, définitions, règles d'audit (normative)

## Objet
Cette spécification fixe les règles MUST/SHALL communes au socle et aux modules Q1..Q5 en mode HIST et SCEN.

## Règles non négociables
- Granularité unique: horaire (1H).
- Index interne timezone-aware UTC.
- Aucune interpolation silencieuse des prix, load ou génération.
- Régimes A/B/C/D calculés sans utiliser le prix (anti-circularité).
- Clé API ENTSOE uniquement via `ENTSOE_API_KEY` (jamais committée).

## Définitions canoniques
- `NRL = load_mw - gen_vre_mw - gen_must_run_mw`
- `surplus_mw = max(0, -NRL)`
- `surplus_unabsorbed_mw = max(0, surplus_mw - flex_effective_mw)`
- `SR = surplus_energy / generation_energy` (fallback explicite `SR_load` si génération indisponible)
- `FAR = surplus_absorbed_energy / surplus_energy`, NaN si surplus nul
- `IR = P10(must_run_mw) / P10(load_mw)`
- `capture_price_X = sum(price_used * gen_X)/sum(gen_X)`
- `capture_ratio_X = capture_price_X / baseload_price`
- `TTL = P95(price_used | regime in {C,D})`

## Régimes
- A: surplus non absorbé (`surplus_unabsorbed_mw > 0`)
- B: surplus absorbé (`surplus_mw > 0` et `surplus_unabsorbed_mw = 0`)
- D: tension (`NRL > seuil_P90_NRL_positif`)
- C: autre heure non surplus

## Auditabilité
Chaque run doit produire:
- `run_id` déterministe (hash code+config+datasets)
- snapshot des hypothèses utilisées
- manifest des datasets utilisés (source, extraction, checksum)
- export des tables et checks

## Tests minimaux
- invariants physiques (hard)
- qualité données (hard/warn)
- reality checks marché/physique (warn)

## Explicabilité UI
Toute métrique affichée doit fournir:
- définition simple
- formule
- intuition
- limites
- dépendances aux hypothèses
