import streamlit as st
import numpy as np
import pandas as pd
import joblib
import plotly.express as px
from Clean_donnees import liste_propre
from regression import predict_dpe
from graph_test import testgraph, par_annee, filter_data_by_year

# Charger le scaler préalablement entraîné
scaler_path = "scaler.pkl"
scaler = joblib.load(scaler_path)

# Interface Streamlit
def main():
    st.title("Prédiction de la classe de consommation d'énergie de votre logement et comparaison par rapport aux autres biens immobiliers")

    # Saisie utilisateur
    surface = st.slider("Surface du logement (m²)", 10, 300, 100)
    consommation_energie = st.slider("Consommation énergétique annuelle en kilo Watt heure d'énergie primaire, par m² et par an", 50, 1000, 500)
    year = st.text_input("Entrez l'année de construction :")
    type_batiment_options = ["Logement", "Bâtiment collectif", "Maison Individuelle"]
    type_batiment = st.selectbox("Entrez le type de bâtiment dans lequel vous vivez :", type_batiment_options)

    # Entrée pour le code commune
    code_commune = st.text_input("Votre code commune", "")

    # Bouton de prédiction
    if st.button("Prédire"):
        # Obtenir la prédiction
        prediction = predict_dpe(surface, consommation_energie)

        # Afficher la prédiction
        st.success(f"Votre lettre DPE prédite est : {prediction}")

        # Afficher le graphique global en France
        st.subheader("Graphique France")
        fig_france = testgraph()  # Utiliser testgraph avec ou sans code commune
        st.plotly_chart(fig_france)

        # Afficher le graphique en fonction du département
        if code_commune:
            st.subheader(f"Comparez votre bien à ceux de votre commune {code_commune}")
            fig_departement = testgraph(code_commune=code_commune)
            st.plotly_chart(fig_departement)

        # Afficher les graphiques par année de construction
        if year:
            year_ = int(year)
            if year_ <= 1945:
                st.subheader("Comparez votre bien à ceux construits à la même époque (avant 1945)")
            elif (year_ >= 1946) and (year_ <= 1975):
                st.subheader(f"Comparez votre bien à ceux construits entre 1946 et 1975")
            elif (year_ >= 1976) and (year_ <= 2000):
                st.subheader(f"Comparez votre bien à ceux construits entre 1976 et 2000")
            elif year_ >= 2001:
                st.subheader(f"Comparez votre bien à ceux construits après 2000")
            fig_annee = par_annee(year=year)
            st.plotly_chart(fig_annee)

# Lancer l'application
if __name__ == "__main__":
    main()
