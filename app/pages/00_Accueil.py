from __future__ import annotations

import streamlit as st


def render() -> None:
    st.title("TTE Capture Prices V2")
    st.markdown(
        """
Outil d'analyse historique des capture prices et des phases structurelles.

- Mode **HIST**: preuves empiriques multi-pays.
- Modèle **horaire UTC** auditable.
- Modules **Q1..Q5** avec checks de cohérence physique/marché.

Utilise la page **Données & Qualité** pour reconstruire/charger les données.
        """
    )
