import requests
import pandas as pd
'''
url = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-france/api-docs.json"

response = requests.get(url)

if response.status_code == 100:
    # La requête a réussi
    data = response.json()  # Convertir la réponse JSON en objet Python
    print(data)
else:
    # La requête a échoué
    print(f"Erreur {response.status_code}: {response.text}")'''

import requests
df=pd.DataFrame()
# URL de l'API endpoint pour récupérer la liste des colonnes
api_url = "https://koumoul.com/data-fair/api/v1/datasets/dpe-france/safe-schema"

# Faire une requête GET à l'API
response = requests.get(api_url)

# Vérifier si la requête a réussi (code de statut HTTP 200)
if response.status_code == 200:
    # Convertir la réponse JSON en une liste Python
    schema_data = response.json()

    # Afficher la liste des colonnes
    print("Liste des colonnes:")
    for column in schema_data:
        column= pd.DataFrame.from_dict(column, orient='index')
        df= pd.concat([df,column], axis=1)
    df.to_excel("data_1_Julien.xlsx")

else:
    # Afficher un message d'erreur si la requête a échoué
    print(f"Erreur {response.status_code}: {response.text}")


'''import requests

# Nom de la colonne que vous souhaitez explorer
column_name = "tr001_modele_dpe_type_libelle"

# URL de l'API endpoint pour récupérer les valeurs distinctes de la colonne
api_url = f"https://koumoul.com/data-fair/api/v1/datasets/dpe-france/values/{column_name}"

# Paramètres de requête (sans filtre)
params = {"limit": 10}

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
    print(f"Erreur {response.status_code}: {response.text}")'''
