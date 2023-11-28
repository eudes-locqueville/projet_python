import requests
import pandas as pd
import random

# Tirer au hasard 10 identifiants uniques depuis l'API
random_ids = random.sample(range(1, 10728950), 10)

# Colonnes pertinentes
colonnes_pertinentes = ["_id", "consommation_energie", "classe_consommation_energie", 
                        "estimation_ges", "classe_estimation_ges", 
                        "annee_construction", "tr002_type_batiment_description", 
                        "code_insee_commune_actualise", "geo_adresse"]

# URL de l'API endpoint pour récupérer les valeurs
api_url = "https://koumoul.com/data-fair/api/v1/datasets/dpe-france/values/"

# Création d'un dictionnaire pour stocker les données
data = {}

# Itération sur chaque colonne
for column_name in colonnes_pertinentes:
    # Construction de l'URL spécifique à la colonne
    column_url = f"{api_url}{column_name}"

    # Faire une requête GET à l'API avec les identifiants aléatoires
    response = requests.get(column_url, params={"_id": random_ids})

    # Vérifier si la requête a réussi (code de statut HTTP 200)
    if response.status_code == 200:
        # Convertir la réponse JSON en une liste Python
        values_data = response.json()

        # Ajouter les valeurs de la colonne au dictionnaire
        data[column_name] = values_data

# Création d'un DataFrame à partir du dictionnaire
df = pd.DataFrame(data)

# Sauvegarde du DataFrame au format Excel
df.to_excel("donnees_api.xlsx", index=False)

# Affichage du DataFrame
print("Tableau des 10 valeurs aléatoires de l'API:")
print(df)
