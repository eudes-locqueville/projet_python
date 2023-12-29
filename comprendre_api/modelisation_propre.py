def estimation_lettre(consommation_energie, surface, annee_construction, type_batiment, departement):
    """
    Fonction qui prend en entrée une liste de données et retourne la classe de consommation d'énergie
    """
    
    data = pd.DataFrame(columns=data_reg.columns.drop(['classe_consommation_energie', 'estimation_ges', 'classe_estimation_ges']))
    data = pd.DataFrame({col: [0] for col in data.columns})
        
    data['consommation_energie'] = [consommation_energie]
    data['surface_thermique_lot'] = [surface]
    data['annee_construction'] = [annee_construction]
    data['consommation_surface_ratio'] = [consommation_energie/surface]
    data['tr002_type_batiment_description_Logement'] = [1] if type_batiment == 'Logement' else [0]
    data['tr002_type_batiment_description_Maison Individuelle'] = [1] if type_batiment == 'Maison individuelle' else [0]
    data[f'departement_{departement}'] = [1]

    approx = model2.predict(data)[0]
    letters = {'1': 'A', '2': 'B', '3': 'C', '4': 'D', '5': 'E', '6': 'F', '7': 'G'}
    if approx- np.floor(approx) < 0.5 :
        return letters[str(int(np.floor(approx)))]
    else :
        return letters[str(int(np.ceil(approx)))]
