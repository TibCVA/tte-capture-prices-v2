# tte-capture-prices-v2

Outil Capture Prices & Phases (V0->V2) pour analyses historiques multi-pays.

## Lancement

```bash
python -m venv .venv
. .venv/Scripts/Activate.ps1
pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

## Tests

```bash
pytest -q
```

## Reproduction (Q1..Q5 + Extrait)

```bash
python scripts/run_extract.py --run-id FULL_YYYYMMDD_FIXX
```

This command:
- snapshots existing outputs to `outputs/combined/before_fix/`
- rebuilds a full combined run Q1..Q5
- regenerates `reports/Extrait Data Outil v7.md` and `.docx`

## Metric Definitions

- `docs/metric_definitions_q1_q5.md`

## Secrets

Configurer `ENTSOE_API_KEY` en variable d'environnement ou via `.streamlit/secrets.toml`.
