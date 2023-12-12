import pandas as pd
import numpy as np
from Clean_donnees import liste_propre

df = liste_propre()

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Supposons que votre DataFrame s'appelle df
# Les colonnes à utiliser pour la régression
features = ["consommation_energie", "estimation_ges", "surface_thermique_lot", "classe_estimation_ges", "annee_construction"]

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

# Entraînement du modèle sur l'ensemble d'entraînement
model.fit(train_data, train_target)

# Prédiction sur l'ensemble de test
predictions = model.predict(test_data)

# Évaluation de la performance du modèle (par exemple, erreur quadratique moyenne)
mse = mean_squared_error(test_target, predictions)
print(f'Erreur quadratique moyenne : {mse}')

# Vous pouvez également imprimer les coefficients du modèle
print('Coefficients du modèle :', model.coef_)
