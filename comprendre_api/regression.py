import pandas as pd
import numpy as np
from Clean_donnees import liste_propre
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import joblib


# Obtenez le DataFrame à partir de la fonction liste_propre
df = pd.concat([liste_propre(code_commune=None, taille_echantillon=10000),
                liste_propre(code_commune=None, taille_echantillon=10000),
                liste_propre(code_commune=None, taille_echantillon=10000),
                liste_propre(code_commune=None, taille_echantillon=10000)],
                axis=0, 
                ignore_index=True)

# Les colonnes à utiliser pour la régression
#features = ['consommation_surface_ratio', 'consommation_energie', 'surface_thermique_lot', "estimation_ges", "classe_estimation_ges", "annee_construction"]

features = ['consommation_energie', 'surface_thermique_lot']

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

# Arrondir les prédictions à l'entier le plus proche et limiter à la plage [1, 7]
rounded_predictions = np.clip(np.round(predictions), 1, 7)

# Évaluation de la performance du modèle (par exemple, erreur quadratique moyenne)
mse = mean_squared_error(test_target, rounded_predictions)
print(f'Erreur quadratique moyenne : {mse}')

# Vous pouvez également imprimer les coefficients du modèle
print('Coefficients du modèle :', model.coef_)

# Convertir les prédictions en classes (arrondir à l'entier le plus proche)
rounded_predictions = np.round(predictions).astype(int)

# Comparer les valeurs prédites arrondies avec les valeurs réelles
correct_predictions = (rounded_predictions == test_target)

# Calculer la proportion des estimations correctes
accuracy = correct_predictions.sum() / len(correct_predictions)
print(f'Proportion des estimations correctes : {accuracy}')

# Comparer les valeurs prédites avec les valeurs réelles avec une tolérance de 1
close_predictions = np.abs(predictions - test_target) <= 1

# Calculer la proportion des estimations correctes ou à 1 d'écart
close_accuracy = close_predictions.sum() / len(close_predictions)
print(f'Proportion des estimations correctes ou à 1 d\'écart : {close_accuracy}')

joblib.dump(scaler, 'scaler.pkl')