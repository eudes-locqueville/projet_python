import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import plotly.express as px
from Clean_donnees import liste_propre
from regression import predict_dpe
from graph_test import testgraph

# Charger le scaler préalablement entraîné
scaler_path = "scaler.pkl"
scaler = joblib.load(scaler_path)


# Interface Streamlit
def main():
    st.title("Prédiction DPE")

    # Saisie utilisateur
    surface = st.slider("Surface du logement (m²)", 10, 300, 100)
    consommation_energie = st.slider("Consommation énergétique annuelle", 50, 1000, 500)

    # Entrée pour le code commune
    code_commune = st.text_input("Votre code commune", "")

    # Bouton de prédiction
    if st.button("Prédire"):
        # Obtenir la prédiction
        prediction = predict_dpe(surface, consommation_energie)

        # Afficher la prédiction
        st.success(f"Votre lettre DPE prédite est : {prediction}")

        # Afficher les graphiques côte à côte avec des titres
        st.subheader("Graphique avec votre code commune")
        st.plotly_chart(testgraph(code_commune=code_commune))

        st.subheader("Graphique France")
        st.plotly_chart(testgraph())

# Lancer l'application
if __name__ == "__main__":
    main()
