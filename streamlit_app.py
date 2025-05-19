"""Streamlit MVP – Confronto recensioni strutture (Google & TripAdvisor – mock)

ISTRUZIONI:
1. Installa le dipendenze minime:
   pip install streamlit pandas altair

2. Avvia l'app localmente con:
   streamlit run streamlit_app.py

3. Per pubblicarla gratis su Streamlit Cloud:
   • Crea un nuovo repo GitHub e carica questo file
   • Vai su https://share.streamlit.io, collega il repo e premi Deploy
   • Ottieni subito il link pubblico da condividere (es. https://tuo-progetto.streamlit.app)

NB: I dati sono simulati. Il motore di sentiment è semplificato per restare leggero; all'occorrenza puoi sostituirlo con un modello ML (es. transformers) aggiungendo la dipendenza.
"""

import streamlit as st
import pandas as pd
import altair as alt
from typing import List, Dict

# --- Mock recensioni ---------------------------------------------------------
review_data: Dict[str, List[str]] = {
    "Hotel Sole": [
        "Personale gentile e posizione centrale, camera pulita.",
        "Colazione ottima ma le stanze sono un po' datate.",
        "Servizio eccellente, tornerò sicuramente!",
        "Rumoroso di notte: non ho dormito bene.",
    ],
    "Hotel Luna": [
        "Vista spettacolare sul mare e camere moderne.",
        "Prezzi troppo alti per quello che offre.",
        "Letti comodi e staff disponibile.",
        "La piscina era chiusa, deluso!",
    ],
    "Ristorante Mare": [
        "Pesce freschissimo e porzioni abbondanti!",
        "Servizio lento ma qualità del cibo eccezionale.",
        "Prezzi onesti, tornerò di sicuro.",
        "Tavoli troppo vicini, poco spazio.",
    ],
    "Ristorante Monte": [
        "Atmosfera accogliente e cucina tipica eccellente.",
        "Porzioni piccole per il prezzo pagato.",
        "Personale poco cortese.",
        "Dessert fantastici, consiglio la torta di mele!",
    ],
}

# --- Sentiment Analysis (naive rule‑based) -----------------------------------
positive_words = {
    "eccellente",
    "ottima",
    "fantastici",
    "comodi",
    "gentile",
    "freschissimo",
    "moderne",
    "spettacolare",
    "pulita",
    "accogliente",
    "onesti",
    "tornerò",
    "consiglio",
}
negative_words = {
    "rumoroso",
    "deluso",
    "chiusa",
    "lento",
    "caro",
    "piccole",
    "datate",
    "poco",
    "troppo",
}


def score_review(text: str) -> int:
    """Restituisce un punteggio 1‑5 basato sul conteggio naive di parole positive/negative."""
    text = text.lower()
    score = 0
    for w in positive_words:
        if w in text:
            score += 1
    for w in negative_words:
        if w in text:
            score -= 1
    # Mappa il punteggio (…‑2,‑1,0,1,2,…) nell'intervallo 1‑5 con offset 3
    return max(1, min(5, 3 + score))


def average_rating(reviews: List[str]) -> float:
    ratings = [score_review(r) for r in reviews]
    return round(sum(ratings) / len(ratings), 2)


# --- Streamlit UI ------------------------------------------------------------
st.set_page_config(page_title="Confronta strutture", layout="centered")

st.title("\U0001F4CA Confronto Recensioni – MVP")
st.write("Seleziona due strutture e scopri quale ha le recensioni migliori (dati simulati).")

structure_names = list(review_data.keys())
col1, col2 = st.columns(2)
with col1:
    left_choice = st.selectbox("Struttura A", structure_names, index=0)
with col2:
    right_choice = st.selectbox("Struttura B", structure_names, index=1)

if left_choice == right_choice:
    st.warning("Seleziona due strutture diverse per il confronto.")
    st.stop()

if st.button("Confronta 🔍"):
    left_score = average_rating(review_data[left_choice])
    right_score = average_rating(review_data[right_choice])

    df_scores = pd.DataFrame(
        {
            "Struttura": [left_choice, right_choice],
            "Punteggio medio (1‑5)": [left_score, right_score],
        }
    )

    # Bar chart
    chart = (
        alt.Chart(df_scores)
        .mark_bar()
        .encode(x="Struttura", y="Punteggio medio (1‑5)")
        .properties(width=400, height=300)
    )

    st.altair_chart(chart, use_container_width=True)

    # Mostra tabella con le recensioni e il relativo rating per trasparenza
    with st.expander("Dettaglio recensioni e punteggi"):
        detailed_rows = []
        for place in [left_choice, right_choice]:
            for rv in review_data[place]:
                detailed_rows.append({
                    "Struttura": place,
                    "Recensione": rv,
                    "Rating (1‑5)": score_review(rv),
                })
        st.write(pd.DataFrame(detailed_rows))

    # Risultato finale
    if left_score > right_score:
        winner = left_choice
    elif right_score > left_score:
        winner = right_choice
    else:
        winner = None

    if winner:
        st.success(f"\U0001F3C6 **{winner}** risulta migliore con un punteggio medio superiore!")
    else:
        st.info("Le due strutture sono in parità in base alle recensioni analizzate.")
