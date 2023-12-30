import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import  r2_score, mean_squared_error
from  Clean_donnees import liste_propre
from sklearn.preprocessing import OneHotEncoder
import xgboost as xgb
import matplotlib.pyplot as plt

data = pd.concat([liste_propre(code_commune=None, taille_echantillon=10000)],
                axis=0, 
                ignore_index=True)
data.dropna(inplace=True)

data['departement']=data['code_insee_commune_actualise'].astype(str).str[:-3]
data['departement'] = data['departement'].apply(lambda x: int(x) if x.isnumeric() else int(x[0]))

encoder = OneHotEncoder(sparse=False, drop='first')
building_type_encoded = pd.DataFrame(
    encoder.fit_transform(data[['tr002_type_batiment_description']]), 
    columns=encoder.get_feature_names_out(['tr002_type_batiment_description'])
    )
data_reg = pd.concat([data, building_type_encoded], axis=1)

zip_code_encoded = pd.DataFrame(
    encoder.fit_transform(data_reg[['departement']]), 
    columns=encoder.get_feature_names_out(['departement'])
    )
data_reg = pd.concat([data_reg, zip_code_encoded], axis=1)

# Step 2: Drop the original zip_code column
data_reg  = data_reg .drop(['tr002_type_batiment_description',
                            'code_insee_commune_actualise',
                            'geo_adresse',
                            '_id',
                            'departement',
                            'classe_consommation_energie',
                            'estimation_ges'], 
                            axis=1)


X= data_reg.drop(['classe_estimation_ges'], axis=1)
y = data_reg['classe_estimation_ges']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = xgb.XGBRegressor()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print(f"le R2 est: {r2_score(y_test, predictions)}")
print(f'la MSE est: {mean_squared_error(y_test, predictions)}')

def estimation_lettre(consommation_energie, surface, annee_construction, type_batiment, departement):
    """
    Fonction qui prend en entrée une liste de données et retourne la classe de consommation d'énergie
    """
    
    data = pd.DataFrame(columns=data_reg.columns.drop(['classe_estimation_ges']))
    data = pd.DataFrame({col: [0] for col in data.columns})
        
    data['consommation_energie'] = [consommation_energie]
    data['surface_thermique_lot'] = [surface]
    data['annee_construction'] = [int(annee_construction)]
    data['consommation_surface_ratio'] = [consommation_energie/surface]
    data['tr002_type_batiment_description_Logement'] = [1] if type_batiment == 'Logement' else [0]
    data['tr002_type_batiment_description_Maison Individuelle'] = [1] if type_batiment == 'Maison individuelle' else [0]
    data[f'departement_{departement}'] = [1]

    approx = model.predict(data)[0]
    letters = {'1': 'A', '2': 'B', '3': 'C', '4': 'D', '5': 'E', '6': 'F', '7': 'G'}
    if approx- np.floor(approx) < 0.5 :
        return letters[str(int(np.floor(approx)))]
    else :
        return letters[str(int(np.ceil(approx)))]


xgb.plot_importance(model, ax=plt.gca(), max_num_features=20)

