import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

# Charger le scaler préalablement entraîné
scaler = joblib.load("/Users/eudeslocqueville/Documents/ENSAE/M1_S1/PYTHON/projet_python/comprendre_api/scaler.pkl")

# Fonction pour prédire la lettre DPE en fonction de la surface et de la consommation_energie
def predict_dpe(surface, consommation_energie):
    # Normaliser les données d'entrée
    input_data = scaler.transform([[consommation_energie, surface]])

    # Appliquer la formule de régression linéaire
    prediction = 1.17 * input_data[0, 0] - 0.06 * input_data[0, 1]

    # Inverser la normalisation sur la prédiction
    prediction = scaler.inverse_transform([[0, prediction]])[0, 1]

    # Arrondir la prédiction à l'entier le plus proche et limiter à la plage [1, 7]
    rounded_prediction = np.clip(np.round(prediction), 1, 7)

    return rounded_prediction

# Interface Streamlit
def main():
    st.title("Prédiction DPE")

    # Saisie utilisateur
    surface = st.slider("Surface du logement (m²)", 10, 300, 100)
    consommation_energie = st.slider("Consommation énergétique annuelle", 50, 1000, 500)

    # Bouton de prédiction
    if st.button("Prédire"):
        # Obtenir la prédiction
        prediction = predict_dpe(surface, consommation_energie)

        # Afficher la prédiction
        st.success(f"Votre lettre DPE prédite est : {prediction}")

# Lancer l'application
if __name__ == "__main__":
    main()
