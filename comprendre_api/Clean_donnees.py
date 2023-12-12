import pandas as pd
import numpy as np
from Extracteur_Donnees import liste_donnees

def liste_propre():

    tableau_propre = liste_donnees()

    # Afficher les différents éléments de la colonne 'classe_consommation_energie'
    #elements_consommation_energie = tableau_propre['classe_consommation_energie'].unique()
    #print(f"Colonnes 'classe_consommation_energie': {elements_consommation_energie}")

    # Afficher les différents éléments de la colonne 'classe_estimation_ges'
    #elements_estimation_ges = tableau_propre['classe_estimation_ges'].unique()
    #print(f"Colonnes 'classe_estimation_ges': {elements_estimation_ges}")

    #type_batiment = tableau_propre['tr002_type_batiment_description'].unique()
    #print(f"Colonnes 'tr002_type_batiment_description': {type_batiment}")

    # Définir la correspondance entre les lettres et les chiffres
    correspondance = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}

    # Remplacer les lettres par les chiffres dans les colonnes spécifiées, les autres valeurs par NaN
    for col in ['classe_consommation_energie', 'classe_estimation_ges']:
        tableau_propre[col] = tableau_propre[col].map(correspondance).where(
            tableau_propre[col].isin(correspondance.keys())
        )

    tableau_propre.replace(0, np.nan, inplace=True)
    tableau_propre = tableau_propre.dropna()

    # Afficher le DataFrame après les remplacements
    return tableau_propre


