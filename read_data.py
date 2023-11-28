import requests

url = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-france/api-docs.json"

response = requests.get(url)

if response.status_code == 100:
    # La requête a réussi
    data = response.json()  # Convertir la réponse JSON en objet Python
    print(data)
else:
    # La requête a échoué
    print(f"Erreur {response.status_code}: {response.text}")
