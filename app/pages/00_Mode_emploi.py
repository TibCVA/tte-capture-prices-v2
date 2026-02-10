from __future__ import annotations

import streamlit as st


def render() -> None:
    st.title("Mode d'emploi")
    st.markdown(
        """
## Definitions express
- **NRL** = Load - VRE - MustRun
- **Surplus** = max(0, -NRL)
- **SR** = surplus energie / generation energie
- **FAR** = surplus absorbe / surplus
- **IR** = P10(MustRun)/P10(Load)
- **TTL** = Q95 des prix sur regimes C/D
- **Capture price** = moyenne des prix ponderee par la production de la techno

## Lecture des regimes
- A: surplus non absorbe
- B: surplus absorbe
- C: normal (non surplus)
- D: tension (NRL haut)

## Audit
Chaque resultat est exportable (tables + checks + hypotheses).
        """
    )
