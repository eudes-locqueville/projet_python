import plotly.express as px
import pandas as pd
from Clean_donnees import liste_propre
import streamlit as st

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
    
    # Afficher la figure dans Streamlit
    st.plotly_chart(fig)

# Test de la fonction
testgraph()
