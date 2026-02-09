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

## Secrets

Configurer `ENTSOE_API_KEY` en variable d'environnement ou via `.streamlit/secrets.toml`.
