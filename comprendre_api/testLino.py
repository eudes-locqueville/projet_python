import requests
import random

# Lien de l'API
api_url = "https://koumoul.com/data-fair/api/v1/datasets/dpe-france/lines?sort=_id&select=consommation_energie%2Cannee_construction%2Ccode_insee_commune_actualise%2C_id&format=json200"

# Effectuer la requête HTTP
response = requests.get(api_url)

# Vérifier si la requête a réussi (code 200)
if response.status_code == 200:
    # Charger les données JSON
    data = response.json()

    # Prélever un échantillon de 30 éléments
    sample_size = 30
    sample = random.sample(data, min(sample_size, len(data)))

    # Afficher l'échantillon
    for item in sample:
        print(item)

else:
    print(f"Erreur lors de la requête : {response.status_code}")
