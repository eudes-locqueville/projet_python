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

# Charger le scaler préalablement entraîné
scaler_path = "scaler.pkl"
scaler = joblib.load(scaler_path)

# Fonction pour générer la figure avec Plotly
# def testgraph(code_commune=None, taille_echantillon=3000):
#     data = liste_propre(code_commune, taille_echantillon)
#     value_counts = data['classe_consommation_energie'].value_counts().reset_index()
#     value_counts.columns = ['classe_consommation_energie', 'Count']

#     fig = px.bar(value_counts, 
#                  x='classe_consommation_energie', 
#                  y='Count', 
#                  title='Value Counts of classe_consommation_energie',
#                  template='plotly_dark',
#                  color_discrete_sequence=['#F63366'],
#                  background_color='rgba(0,0,0,0)',
#                  opacity=0.8,
#                  width=800,
#                  height=500)
    
    # return fig

def testgraph(code_commune=None, taille_echantillon=3000):
    data = liste_propre(code_commune, taille_echantillon)
    value_counts = data['classe_consommation_energie'].value_counts().reset_index()
    value_counts.columns = ['classe_consommation_energie', 'Count']

    fig = px.bar(value_counts, 
                 x='classe_consommation_energie', 
                 y='Count', 
                 title='Distribution des classes de consommation d\'énergie',
                 template='plotly_dark',
                 color_discrete_sequence=px.colors.qualitative.Plotly,
                 labels={'classe_consommation_energie': 'Classe de Consommation d\'Énergie', 'Count': 'Nombre'},
                 opacity=0.8,
                 width=800,
                 height=500)
        
    # Ajuster la mise en page
    fig.update_layout(
        margin=dict(l=20, r=20, t=50, b=20),
        font=dict(family="Arial", size=12, color="black"),
        paper_bgcolor="white",
        plot_bgcolor="white"
    )

    return fig


# Interface Streamlit
def main():
    st.title("Prédiction de la classe de votre logement et comparaison par rapport aux autres biens immobiliers")

    # Saisie utilisateur
    surface = st.slider("Surface du logement (m²)", 10, 300, 100)
    consommation = st.slider("Consommation énergétique annuelle en kilo Watt heure d'énergie primaire par an", 500, 100000, 500)
    consommation_energie = consommation/surface
    year = st.text_input("Entrez l'année de construction :")
    type_batiment_options = ["Logement", "Bâtiment collectif", "Maison Individuelle"]
    type_batiment = st.selectbox("Entrez le type de bâtiment dans lequel vous vivez :", type_batiment_options)

    # Entrée pour le code commune
    code_commune = st.text_input("Votre numéro de département", "")

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
    if st.button("Obtenir mon analyse énergétique"):
        # Obtenir la prédiction
        prediction = estimation_lettre(consommation_energie, surface, int(year), type_batiment, code_commune)
        
        # Afficher la prédiction

        st.info(f"La lettre DPE correspondante à votre consommation d'énergie est : {get_lettre_dpe(consommation_energie)}")
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

# Lancer l'application
if __name__ == "__main__":
    main()
