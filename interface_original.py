import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import folium
import plotly.express as px
from clean_donnees import liste_propre
from graph_test import testgraph, par_annee, filter_data_by_year, get_lettre_dpe
from geo import map_number_to_letter, interactive_map_dpe
from streamlit_folium import folium_static
import numpy as np
from modelisation_propre import estimation_lettre
import os 

folder_path = "details"
scaler_filename = "scaler.pkl"
scaler_path = os.path.join(folder_path, scaler_filename)
scaler = joblib.load(scaler_path)

# Charger le scaler préalablement entraîné

# Interface Streamlit
def main():
    st.title("Prédiction de la classe de votre logement et comparaison par rapport aux autres biens immobiliers")
    # Saisie utilisateur
    surface = st.slider("Surface du logement (m²)", 10, 300, 100)
    consommation = st.slider("Consommation énergétique annuelle en kilo Watt heure d'énergie primaire par an", 500, 100000, 500)
    consommation_energie = consommation/surface
    year = st.number_input("Entrez l'année de construction :")
    type_batiment_options = ["Logement", "Bâtiment collectif", "Maison Individuelle"]
    type_batiment = st.selectbox("Entrez le type de bâtiment dans lequel vous vivez :", type_batiment_options)
    # Entrée pour le code commune
    code_commune = st.text_input("Votre code commune", "")
    if get_lettre_dpe(consommation_energie) == 'A':
        prediction = 1
    elif get_lettre_dpe(consommation_energie) == 'B':
        prediction = 2
    elif get_lettre_dpe(consommation_energie) == 'C':
        prediction = 3
    elif get_lettre_dpe(consommation_energie) == 'D':
        prediction = 4
    elif get_lettre_dpe(consommation_energie) == 'E':
        prediction = 5
    elif get_lettre_dpe(consommation_energie) == 'F':
        prediction = 6
    elif get_lettre_dpe(consommation_energie) == 'G':
        prediction = 7
    # Bouton de prédiction
    ges = estimation_lettre(consommation_energie, surface, year, type_batiment, code_commune)    
    if st.button("Obtenir mon analyse énergétique"):
        # Obtenir la prédiction
        # Afficher la prédiction
        st.info(f"La lettre DPE correspondante à votre consommation d'énergie est : {get_lettre_dpe(consommation_energie)}")
        st.info(f"Compte tenu des informations entrées, nous estimons votre note d'émission de gaz à effet de serre à : {ges}")
        # Couleur pour la valeur de l'utilisateur
        user_color = 'rgba(66, 135, 245, 0.8)'  # Bleu
        other_color = 'rgba(246, 51, 102, 0.8)'  # Rose

        # Afficher le graphique global en France
        st.subheader("Comparez vos biens aux autres biens en France")
        fig_france = testgraph()  # Utiliser testgraph avec ou sans code commune
        fig_france.update_traces(marker_color=[user_color if col == prediction else other_color for col in fig_france.data[0].x])
        st.plotly_chart(fig_france)
        # Afficher le graphique en fonction du département
        if code_commune:
            st.subheader(f"Comparez votre bien à ceux de votre commune {code_commune}")
            fig_departement = testgraph(code_commune=code_commune)
            fig_departement.update_traces(marker_color=[user_color if col == prediction else other_color for col in fig_departement.data[0].x])
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
            # Ajouter la personnalisation de la couleur pour la colonne de l'utilisateur
            fig_annee = par_annee(year=year)
            for trace in fig_annee.data:
                trace.update(marker_color=[user_color if col == prediction else other_color for col in trace.x])

            st.plotly_chart(fig_annee)

            st.subheader("Carte interactive")
            donnees = liste_propre(code_commune, taille_echantillon=3000)
            folium_static(interactive_map_dpe(donnees))

# Lancer l'application
if __name__ == "__main__":
    main()