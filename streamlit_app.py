from __future__ import annotations

from pathlib import Path
import runpy

import streamlit as st

st.set_page_config(page_title="TTE Capture Prices V2", layout="wide")

PAGES = [
    ("Accueil", "app/pages/00_Accueil.py"),
    ("Mode emploi", "app/pages/00_Mode_emploi.py"),
    ("Donnees & Qualite", "app/pages/00_Donnees_Qualite.py"),
    ("Socle Physique", "app/pages/00_Socle_Physique.py"),
    ("Q1 Phase 1 -> 2", "app/pages/01_Q1_Phase1_to_Phase2.py"),
    ("Q2 Pente", "app/pages/02_Q2_Phase2_Slope.py"),
    ("Q3 Sortie Phase 2", "app/pages/03_Q3_Exit_Phase2.py"),
    ("Q4 BESS", "app/pages/04_Q4_BESS_OrderOfMagnitude.py"),
    ("Q5 CO2/Gaz", "app/pages/05_Q5_CO2_Gas_Anchor.py"),
    ("Conclusions", "app/pages/99_Conclusions.py"),
]

st.sidebar.title("Navigation")
labels = [x[0] for x in PAGES]
choice = st.sidebar.radio("Page", labels)
page_path = dict(PAGES)[choice]

namespace = runpy.run_path(str(Path(page_path)))
if "render" in namespace:
    namespace["render"]()
else:
    st.error(f"La page {page_path} ne definit pas render().")
