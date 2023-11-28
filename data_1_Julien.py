import requests
'''
url = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-france/api-docs.json"

response = requests.get(url)

if response.status_code == 100:
    # La requête a réussi
    data = response.json()  # Convertir la réponse JSON en objet Python
    print(data)
else:
    # La requête a échoué
    print(f"Erreur {response.status_code}: {response.text}")
'''
import requests

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
        print(column)

else:
    # Afficher un message d'erreur si la requête a échoué
    print(f"Erreur {response.status_code}: {response.text}")


