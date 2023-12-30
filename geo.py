import folium
from streamlit_folium import folium_static
from clean_donnees import liste_propre
import numpy as np

#Ici, on crée la cartographie qui sera affichée en bas du site streamlit
#Elle permettra à l'utilisateur de se balader et de voir les notes DPE
#De ses voisins ce qui peut être utile si on veut prendre conscience des atouts / faiblesses
#De notre bien dans l'optique de le vendre (ou de l'acheter)

def map_number_to_letter(number):
    #Dictionnaire inverse
    mapping = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G'}
    return mapping.get(number, '-')

def interactive_map_dpe(dpe):
    #On commence par définir le cadre (centre et coordonnées extrêmes de la carte)
    center = dpe[['latitude', 'longitude']].mean().values.tolist()
    sw = dpe[['latitude', 'longitude']].min().values.tolist()
    ne = dpe[['latitude', 'longitude']].max().values.tolist()

    m = folium.Map(location=center, tiles='OpenStreetMap')

    #Ensuite, on sélectionne un ensemble d'éléments du dataframe qu'on replacera avec
    #leurs notes sur la carte

    random_indices = np.random.choice(len(dpe), min(300, len(dpe)), replace=False)
    for i in random_indices:  
        classe_energie = map_number_to_letter(int(dpe.iloc[i]['classe_consommation_energie']))

        # On crée une icône pour chaque élément
        custom_icon = folium.Icon(icon='home')

        # Enfin, on ajoute les marqueurs et on place sur la carte les éléments
        folium.Marker([dpe.iloc[i]['latitude'], dpe.iloc[i]['longitude']],
                      popup=f"Année de construction : {dpe.iloc[i]['annee_construction']}, <br>DPE : {classe_energie}",
                      icon=custom_icon).add_to(m)

    m.fit_bounds([sw, ne])

    return m

