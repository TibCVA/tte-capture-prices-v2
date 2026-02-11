from __future__ import annotations

from pathlib import Path
import runpy
import traceback

import streamlit as st

st.set_page_config(page_title="TTE Capture Prices V2", layout="wide")

PAGES = [
    ("Accueil", "app/pages/00_Accueil.py", "Vue d'ensemble et parcours recommande"),
    ("Mode emploi", "app/pages/00_Mode_emploi.py", "Definitions et limites"),
    ("Donnees & Qualite", "app/pages/00_Donnees_Qualite.py", "Chargement des donnees et checks qualite"),
    ("Socle Physique", "app/pages/00_Socle_Physique.py", "NRL, surplus, flex, regimes"),
    ("Q1 Phase 1 -> 2", "app/pages/01_Q1_Phase1_to_Phase2.py", "Detection de bascule"),
    ("Q2 Pente", "app/pages/02_Q2_Phase2_Slope.py", "Pente et drivers"),
    ("Q3 Sortie Phase 2", "app/pages/03_Q3_Exit_Phase2.py", "Stabilisation et inversion"),
    ("Q4 BESS", "app/pages/04_Q4_BESS_OrderOfMagnitude.py", "Ordres de grandeur stockage"),
    ("Q5 CO2/Gaz", "app/pages/05_Q5_CO2_Gas_Anchor.py", "Sensibilite ancre thermique"),
    ("Scenarios Phase 2", "app/pages/06_Scenarios_Phase2.py", "Projection mecaniste prospective"),
    ("Conclusions", "app/pages/99_Conclusions.py", "Rapport final trace"),
]

st.sidebar.title("Navigation guidee")
labels = [x[0] for x in PAGES]
choice = st.sidebar.radio("Page", labels)
idx = labels.index(choice)

st.sidebar.progress((idx + 1) / len(PAGES), text=f"Etape {idx + 1}/{len(PAGES)}")
st.sidebar.info(PAGES[idx][2])

st.sidebar.markdown("### Parcours")
for i, (label, _, _) in enumerate(PAGES, start=1):
    if i == idx + 1:
        st.sidebar.markdown(f"**{i}. {label}** ←")
    else:
        st.sidebar.markdown(f"{i}. {label}")

page_path = dict((label, path) for label, path, _ in PAGES)[choice]
try:
    namespace = runpy.run_path(str(Path(page_path)))
except Exception as exc:  # pragma: no cover - defensive for Streamlit cloud diagnostics
    st.error(f"Echec de chargement de la page: `{page_path}`")
    st.code(f"{type(exc).__name__}: {exc}")
    st.code(traceback.format_exc())
    st.info("Action recommandee: verifier le dernier deploiement, puis reboot et clear cache Streamlit Cloud.")
    st.stop()

if "render" in namespace:
    namespace["render"]()
else:
    st.error(f"La page {page_path} ne definit pas render().")
