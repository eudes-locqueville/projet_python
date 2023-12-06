import requests
import pandas as pd

# Définir l'URL de l'API
api_url = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-france"

# Définir les paramètres de la requête
params = {
    'field': 'nom_methode_dpe',
    'size': 10,
    'q': 'recherche_textuelle',
    'q_mode': 'simple',
    # Ajoute d'autres paramètres selon tes besoins
}

# Effectuer la requête à l'API
response = requests.get(api_url, params=params)

# Vérifier si la requête a réussi (code 200)
if response.status_code == 200:
    # Convertir la réponse JSON en un DataFrame
    data = response.json()
    df = pd.DataFrame(data['results'])
    # Afficher le DataFrame
    print(df)
else:
    print(f"Erreur lors de la requête à l'API. Code d'erreur : {response.status_code}")
