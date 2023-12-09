import requests
import pandas as pd

# URL de l'API endpoint pour récupérer la liste des colonnes
api_url = "https://koumoul.com/data-fair/api/v1/datasets/dpe-france/safe-schema"

# Faire une requête GET à l'API
response = requests.get(api_url)

# Vérifier si la requête a réussi (code de statut HTTP 200)
if response.status_code == 200:
    # Convertir la réponse JSON en une liste Python
    schema_data = response.json()
  # Initialiser un DataFrame vide
    df = pd.DataFrame()
    # Afficher la liste des colonnes
    print("Liste des colonnes:")
    for column in schema_data:
        column= pd.DataFrame.from_dict(column, orient='index')
        df= pd.concat([df,column], axis=1)
    df.to_excel("read_data.xlsx")

else:
    # Afficher un message d'erreur si la requête a échoué
    print(f"Erreur {response.status_code}: {response.text}")


import requests

colonnes_pertinentes = ["consommation_energie", "classe_consommation_energie", "estimation_ges", "classe_estimation_ges", "annee_construction", "tr002_type_batiment_description", "code_insee_commune_actualise", "geo_adresse"]

def obtenir_valeurs_distinctes(liste):
    for column_name in liste:
        # URL de l'API endpoint pour récupérer les valeurs distinctes de la colonne
        api_url = f"https://koumoul.com/data-fair/api/v1/datasets/dpe-france/values/{column_name}"

        # Paramètres de requête (sans filtre)
        params = {"limit": "30"}

        # Faire une requête GET à l'API
        response = requests.get(api_url, params=params)

        # Vérifier si la requête a réussi (code de statut HTTP 200)
        if response.status_code == 200:
            # Convertir la réponse JSON en une liste Python
            values_data = response.json()

            # Afficher les valeurs distinctes
            print(f"Valeurs distinctes pour la colonne '{column_name}':")
            for value in values_data:
                print(value)

        else:
            # Afficher un message d'erreur si la requête a échoué
            print(f"Erreur {response.status_code}: {response.text}")

# Appeler la fonction avec la liste de colonnes pertinentes
obtenir_valeurs_distinctes(colonnes_pertinentes)


