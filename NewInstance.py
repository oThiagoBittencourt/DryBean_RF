import pandas as pd
from pickle import load

def new_instance(area:float, perimeter:float, majorAxisLength:float, minorAxisLength:float, aspectRation:float, eccentricity:float, convexArea:float, equivDiameter:float, extent:float, solidity:float, roundness:float, compactness:float, shapeFactor1:float, shapeFactor2:float, shapeFactor3:float, shapeFactor4:float):
    dry_bean_RF_model = load(open("Training/Models/Dry_Bean_RF_2024.pkl", "rb"))
    normalizador = load(open("Training/Models/Normalizer.pkl", "rb"))

    dados_numericos = pd.DataFrame([[area, perimeter, majorAxisLength, minorAxisLength, aspectRation, eccentricity, convexArea, equivDiameter, extent, solidity, roundness, compactness, shapeFactor1, shapeFactor2, shapeFactor3, shapeFactor4]], columns=['Area', 'Perimeter', 'MajorAxisLength', 'MinorAxisLength', 'AspectRation', 'Eccentricity', 'ConvexArea', 'EquivDiameter', 'Extent', 'Solidity', 'roundness', 'Compactness', 'ShapeFactor1', 'ShapeFactor2', 'ShapeFactor3', 'ShapeFactor4'])

    # NORMALIZAÇÃO DOS DADOS NUMÉRICOS
    dados_numericos_normalizados = normalizador.transform(dados_numericos)
    dados_numericos_normalizados = pd.DataFrame(data = dados_numericos_normalizados, columns=['Area', 'Perimeter', 'MajorAxisLength', 'MinorAxisLength', 'AspectRation', 'Eccentricity', 'ConvexArea', 'EquivDiameter', 'Extent', 'Solidity', 'roundness', 'Compactness', 'ShapeFactor1', 'ShapeFactor2', 'ShapeFactor3', 'ShapeFactor4'])

    # EXECUÇÃO DO PREDICT
    predict = dry_bean_RF_model.predict(dados_numericos_normalizados)
    predict_proba = dry_bean_RF_model.predict_proba(dados_numericos_normalizados)

    print(f"\nPredict: {predict}")
    print(f"\nProba: {predict_proba}")