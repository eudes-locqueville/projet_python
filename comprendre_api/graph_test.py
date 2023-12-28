import plotly.express as px
import pandas as pd
from Clean_donnees import liste_propre
import streamlit as st
import plotly.graph_objs as go

def filter_data_by_year(data, year):
    datac = data.copy()
    if year is not None:
        # Filtrer les données en fonction de l'année fournie
        if year <= 1945:
            datac = datac[datac['annee_construction'] <= 1945]
        elif (year > 1945) & (year <= 1975) :
            datac = datac[(datac['annee_construction'] > 1945) & (datac['annee_construction'] <= 1975)]
        elif (year > 1975) & (year <= 2000):
            datac = datac[(datac['annee_construction'] > 1975) & (datac['annee_construction'] <= 2000)]
        elif year > 2000:
            datac = datac[datac['annee_construction'] > 2000]

    return datac

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

    # Convertir la figure en instance de plotly.graph_objs.Figure
    return go.Figure(fig)




# Nouvelle fonction pour la visualisation par année de construction
def par_annee(code_commune=None, taille_echantillon=3000, year=None):
    data = liste_propre(code_commune, taille_echantillon)

    # Filtrer les données en fonction de l'année de construction
    data = filter_data_by_year(data, year)

    # Créer un graphique à barres
    value_counts = data['classe_consommation_energie'].value_counts().reset_index()
    value_counts.columns = ['classe_consommation_energie', 'Count']

    fig = px.bar(value_counts, 
                 x='classe_consommation_energie', 
                 y='Count', 
                 title=f'Value Counts of classe_consommation_energie - Year: {year}',
                 template='plotly_dark',
                 color_discrete_sequence=['#F63366'],
                 opacity=0.8,
                 width=800,
                 height=500)

    # Convertir la figure en instance de plotly.graph_objs.Figure
    return go.Figure(fig)


    