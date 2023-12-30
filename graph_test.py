import plotly.express as px
import pandas as pd
from clean_donnees import liste_propre
import streamlit as st
import plotly.graph_objs as go

def get_lettre_dpe(consommation_energie):
    if consommation_energie < 50:
        return 'A'
    elif 51 <= consommation_energie <= 90:
        return 'B'
    elif 91 <= consommation_energie <= 150:
        return 'C'
    elif 151 <= consommation_energie <= 230:
        return 'D'
    elif 231 <= consommation_energie <= 330:
        return 'E'
    elif 331 <= consommation_energie <= 450:
        return 'F'
    else:
        return 'G'

def filter_data_by_year(data, year):
    datac = data.copy()
    if year is not None and str(year).isdigit():
        year = int(year)
    datac['annee_construction'] = datac['annee_construction'].astype(int)
    if year is not None:
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
    value_counts = data['classe_consommation_energie'].value_counts(normalize=True).reset_index()
    value_counts.columns = ['classe_consommation_energie', 'Percentage']

    fig = px.bar(value_counts, 
                 x='classe_consommation_energie', 
                 y='Percentage', 
                 title='Percentage of classe_consommation_energie',
                 template='plotly_dark',
                 color_discrete_sequence=['#F63366'],
                 opacity=0.8,
                 width=800,
                 height=500,
                 labels={'Percentage': 'Percentage'})

    return go.Figure(fig)

def par_annee(code_commune=None, taille_echantillon=3000, year=None):
    data = liste_propre(code_commune, taille_echantillon)
    data = filter_data_by_year(data, year)
    value_counts = data['classe_consommation_energie'].value_counts(normalize=True).reset_index()
    value_counts.columns = ['classe_consommation_energie', 'Percentage']

    fig = px.bar(value_counts, 
                 x='classe_consommation_energie', 
                 y='Percentage', 
                 title=f'Percentage of classe_consommation_energie - Year: {year}',
                 template='plotly_dark',
                 color_discrete_sequence=['#F63366'],
                 opacity=0.8,
                 width=800,
                 height=500,
                 labels={'Percentage': 'Percentage'})

    return go.Figure(fig)

