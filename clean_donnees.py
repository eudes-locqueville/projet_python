import pandas as pd
import numpy as np
from api_request import liste_donnees

#L'objectif ici est de transformer le df obtenu dans api_request
#afin d'obtenir un set de données exploitables.
#On va par exemple transformer les lettres en chiffres afin de pouvoir réaliser des
#régressions plus facilement.

def liste_propre(code_commune=None, taille_echantillon=3000):

    tableau_propre = liste_donnees(code_commune, taille_echantillon)

    # Création du dictionnaire de correspondance
    correspondance = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}

    # Application du dictionnaire + on se débarasse des lignes avec des valeurs manquantes
    for col in ['classe_consommation_energie', 'classe_estimation_ges']:
        tableau_propre[col] = tableau_propre[col].map(correspondance).where(
            tableau_propre[col].isin(correspondance.keys())
        )

    tableau_propre.replace('N', np.nan, inplace=True)  #
    tableau_propre.replace(0, np.nan, inplace=True)
    tableau_propre = tableau_propre.dropna()
    tableau_propre['consommation_surface_ratio'] = tableau_propre['consommation_energie'] / tableau_propre['surface_thermique_lot']

    return tableau_propre





