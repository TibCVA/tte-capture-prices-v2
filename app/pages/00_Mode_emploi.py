from __future__ import annotations

import streamlit as st


def render() -> None:
    st.title("Mode d'emploi")
    st.markdown(
        """
## Définitions express
- **NRL** = Load - VRE - MustRun
- **Surplus** = max(0, -NRL)
- **SR** = surplus énergie / génération énergie
- **FAR** = surplus absorbé / surplus
- **IR** = P10(MustRun)/P10(Load)
- **TTL** = Q95 des prix sur régimes C/D
- **Capture price** = moyenne des prix pondérée par la production de la techno

## Lecture des régimes
- A: surplus non absorbé
- B: surplus absorbé
- C: normal (non surplus)
- D: tension (NRL haut)

## Audit
Chaque résultat est exportable (tables + checks + hypothèses).
        """
    )
