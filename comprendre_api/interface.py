import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import plotly.express as px
from Clean_donnees import liste_propre

# Charger le scaler préalablement entraîné
scaler_path = "scaler.pkl"
scaler = joblib.load(scaler_path)

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

# Fonction pour générer la figure avec Plotly
def testgraph(code_commune=None, taille_echantillon=3000):
    data = liste_propre(code_commune, taille_echantillon)
    value_counts = data['classe_consommation_energie'].value_counts().reset_index()
    value_counts.columns = ['classe_consommation_energie', 'Count']

    fig = px.bar(value_counts, 
                 x='classe_consommation_energie', 
                 y='Count', 
                 title='Value Counts of classe_consommation_energie',
                 template='plotly_dark',
                 color_discrete_sequence=['#F63366'],
                 opacity=0.8,
                 width=800,
                 height=500)
    
    return fig

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
