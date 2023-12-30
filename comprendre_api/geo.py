import folium
from streamlit_folium import folium_static
from Clean_donnees import liste_propre
import numpy as np

def map_number_to_letter(number):
    # Mapper les valeurs numériques aux lettres correspondantes (A pour 1, B pour 2, etc.)
    mapping = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G'}
    return mapping.get(number, '-')

def interactive_map_dpe(dpe):
    center = dpe[['latitude', 'longitude']].mean().values.tolist()
    sw = dpe[['latitude', 'longitude']].min().values.tolist()
    ne = dpe[['latitude', 'longitude']].max().values.tolist()

    m = folium.Map(location=center, tiles='OpenStreetMap')

    random_indices = np.random.choice(len(dpe), min(300, len(dpe)), replace=False)
    for i in random_indices:  # Afficher seulement les 100 premières lignes
        # Convertir la valeur numérique en chaîne et mapper à la lettre correspondante
        classe_energie = map_number_to_letter(int(dpe.iloc[i]['classe_consommation_energie']))

        # Créer une icône personnalisée
        custom_icon = folium.Icon(icon='home')

        # Ajouter le marqueur avec l'icône personnalisée
        folium.Marker([dpe.iloc[i]['latitude'], dpe.iloc[i]['longitude']],
                      popup=f"Année de construction : {dpe.iloc[i]['annee_construction']}, <br>DPE : {classe_energie}",
                      icon=custom_icon).add_to(m)

    m.fit_bounds([sw, ne])

    return m

