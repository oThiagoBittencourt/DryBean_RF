from sklearn import preprocessing
from pickle import dump
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_validate
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

dados = pd.read_csv('Training/CSV/Dry_Bean_Dataset.csv', sep=';')

classe = dados[['Class']]
dados_numericos = dados.drop(columns=['Class'])
dados_numericos = dados_numericos.replace(',', '.', regex=True)

# NORMALIZAÇÃO DADOS NUMÉRICOS
normalizador = preprocessing.MinMaxScaler()
modelo_normalizador = normalizador.fit(dados_numericos)
dump(modelo_normalizador, open('Training/Models/Normalizer.pkl', 'wb'))

# CRIAR UM DATAFRAME COM OS DADOS NORMALIZADOS
dados_numericos_normalizados = modelo_normalizador.fit_transform(dados_numericos)
dados_numericos_normalizados = pd.DataFrame(data = dados_numericos_normalizados, columns=['Area', 'Perimeter', 'MajorAxisLength', 'MinorAxisLength', 'AspectRation', 'Eccentricity', 'ConvexArea', 'EquivDiameter', 'Extent', 'Solidity', 'roundness', 'Compactness', 'ShapeFactor1', 'ShapeFactor2', 'ShapeFactor3', 'ShapeFactor4'])

# BALANCEAMENTO
# SEGMENTAR OS DADOS EM ATRIBUTOS E CLASSES
dados_atributos = dados_numericos_normalizados

# IMPRIMIR AS FRQUÊNCIAS DAS CLASSES ANTES DE BALANCEAR
print('Frequencia de classes antes do balanceamento')
classes_count = classe.value_counts()
print(classes_count)

# CONSTRUIR UM OBJETO A PARTIR DO SMOTE
resampler = SMOTE()

# EXECUTAR O BALANCEAMENTO
dados_atributos_b, dados_classes_b = resampler.fit_resample(dados_atributos, classe)

# VERIFICAR A FREQUENCIA DAS CLASSES APÓS O BALANCEAMENTO
print('Frequencia de classes após balanceamento')
classes_count = dados_classes_b.value_counts()
print(classes_count)

# CONVERTER OS DADOS BALANCEADOS EM DATAFRAMES
dados_atributos_b = pd.DataFrame(dados_atributos_b)
dados_atributos_b.columns = dados_atributos.columns

dados_classes_b = pd.DataFrame(dados_classes_b)
dados_classes_b.columns = ['Class']

dados_finais_b = dados_atributos_b.join(dados_classes_b, how='left')

# HIPERPARAMETRIZAÇÃO

# Calculo Amostral para realização das hiperparametrizações
# População pós balanceamento: 24.822
# Erro amostral: 3%
# Nível de confiança: 95%
# Distribuição da população: 80/20
### Resultado: 665

dados_finais_b_train = dados_finais_b.sample(665)
class_train_b = dados_finais_b_train['Class']
atr_train_b = dados_finais_b_train.drop(columns=['Class'])

# Montagem da grade de parâmentros
# Número de árvores na floresta
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 300, num = 3)]
# Número de atributos considerados em cada segmento
max_features = ['log2', 'sqrt']
# Número máximo de folhas em cada árvore
max_depth = [int(x) for x in np.linspace(10,110, num = 3)]
max_depth.append(None)
# Número mínimo de instâncias requeridas para segmentar cada nó
min_samples_split = [2,5,10]
# Número mínimo de amostras necessárias em cada nó
min_samples_leaf = [1,2,4]
# Método de seleção de amostras para treinar cada árvore
bootstrap = [True, False]

random_grid = { 'n_estimators' : n_estimators,
                'max_features' : max_features,
                'max_depth' : max_depth,
                'min_samples_split' : min_samples_split,
                'min_samples_leaf' : min_samples_leaf,
                'bootstrap' : bootstrap,}

# INICIAR A BUSCA PELOS MELHORES HIPERPARAMETROS
rf_grid = RandomForestClassifier()
rf_grid = GridSearchCV(rf_grid,random_grid,refit=True,verbose=0)
rf_grid.fit(atr_train_b, class_train_b)

print("MELHORES HIPERPARÂMETROS")
print(rf_grid.best_params_)

# TREINAR O MODELO
rf = RandomForestClassifier(n_estimators=rf_grid.best_params_['n_estimators'], max_features=rf_grid.best_params_['max_features'], max_depth=rf_grid.best_params_['max_depth'], min_samples_split=rf_grid.best_params_['min_samples_split'], min_samples_leaf=rf_grid.best_params_['min_samples_leaf'], bootstrap=rf_grid.best_params_['bootstrap'])
FinancialFraudRF = rf.fit(dados_atributos_b, dados_classes_b.values.ravel())
dump(FinancialFraudRF, open('Training/Models/Dry_Bean_RF_2024.pkl', 'wb'))

# CROSS VALIDATION
scoring = ['precision_macro', 'recall_macro']
scores_cross = cross_validate(FinancialFraudRF, dados_atributos_b, dados_classes_b.values.ravel(), scoring=scoring)
print(scores_cross['test_precision_macro'].mean())
print(scores_cross['test_recall_macro'].mean())

x = np.array(["test_precision_macro", "test_recall_macro"])
y = np.array([scores_cross['test_precision_macro'].mean(), scores_cross['test_recall_macro'].mean()])

plt.bar(x, y)
plt.savefig('Training/CrossValidation.png')

plt.show()