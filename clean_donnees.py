import pandas as pd
import numpy as np
from api_request import liste_donnees

def liste_propre(code_commune=None, taille_echantillon=3000):

    tableau_propre = liste_donnees(code_commune, taille_echantillon)

    # Définir la correspondance entre les lettres et les chiffres
    correspondance = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}

    # Remplacer les lettres par les chiffres dans les colonnes spécifiées, les autres valeurs par NaN
    for col in ['classe_consommation_energie', 'classe_estimation_ges']:
        tableau_propre[col] = tableau_propre[col].map(correspondance).where(
            tableau_propre[col].isin(correspondance.keys())
        )

    tableau_propre.replace('N', np.nan, inplace=True)  # Remplacer 'N' par NaN
    tableau_propre.replace(0, np.nan, inplace=True)
    tableau_propre = tableau_propre.dropna()
    tableau_propre['consommation_surface_ratio'] = tableau_propre['consommation_energie'] / tableau_propre['surface_thermique_lot']

    # Afficher le DataFrame après les remplacements
    return tableau_propre





