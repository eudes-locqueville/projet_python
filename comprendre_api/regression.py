import pandas as pd
import numpy as np
from Clean_donnees import liste_propre
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler

# Obtenez le DataFrame à partir de la fonction liste_propre
df = liste_propre(code_commune=None, taille_echantillon=10000)

# Les colonnes à utiliser pour la régression
features = ['consommation_energie', "estimation_ges", "classe_estimation_ges", "annee_construction"]

# La colonne à prédire (cible)
target = "classe_consommation_energie"
# Séparation en ensembles d'entraînement et de test (80% / 20%)
train_data, test_data, train_target, test_target = train_test_split(
    df[features],  # Caractéristiques
    df[target],    # Cible
    test_size=0.2,  # Taille de l'ensemble de test
    random_state=42  # Fixez la graine aléatoire pour la reproductibilité
)

# Initialisation du modèle de régression linéaire
model = LinearRegression()

# Normalisation des données
scaler = StandardScaler()
train_data_scaled = scaler.fit_transform(train_data)
test_data_scaled = scaler.transform(test_data)

# Entraînement du modèle sur l'ensemble d'entraînement normalisé
model.fit(train_data_scaled, train_target)

# Prédiction sur l'ensemble de test normalisé
predictions = model.predict(test_data_scaled)

# Évaluation de la performance du modèle (par exemple, erreur quadratique moyenne)
mse = mean_squared_error(test_target, predictions)
print(f'Erreur quadratique moyenne : {mse}')

# Vous pouvez également imprimer les coefficients du modèle
print('Coefficients du modèle :', model.coef_)
