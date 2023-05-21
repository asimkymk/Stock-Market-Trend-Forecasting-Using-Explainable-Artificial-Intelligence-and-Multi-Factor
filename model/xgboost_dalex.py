import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import dalex as dx
import datatable as dt # data table factory
from sklearn.metrics import f1_score,confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import shap
import ipywidgets
from ipywidgets import IntProgress
import statsmodels
import lime
import warnings
import flask
import flask_cors
import requests


# Veri dosyasını oku
data = pd.read_csv('tickers.csv')

data = data[(data["symbol"] == 'AAL')]
data['Date'] = pd.to_datetime(data['Date'])
data = data.set_index('Date')
data = data.sort_values('Date')
# Özellikler ve hedef değişken ayırma
X = data[['trend_score', 'news_score_model1']]
y = data['Adj Close']

tarih = '2023-01-01'
# Eğitim ve test verileri ayırma

X_train = X[X.index < tarih]
y_train = y[y.index < tarih]

# Seçilen tarihten sonraki verileri test verileri olarak kullanın
X_test = X[X.index >= tarih]
y_test = y[y.index >= tarih]
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# XGBoost modeli
xgb_model = xgb.XGBRegressor(objective='reg:squarederror', colsample_bytree=0.3, learning_rate=0.1,
                max_depth=10, alpha=10, n_estimators=100)

# Modeli eğitme
xgb_model.fit(X_train, y_train)

# Test verileri üzerinden tahmin yapma
adj_close_pred = xgb_model.predict(X_test)
print(y_test)
print(adj_close_pred)
# Model performansını değerlendirme
mse = mean_squared_error(y_test, adj_close_pred)
print("Mean Squared Error: %.2f" % mse)

explainer = dx.Explainer(xgb_model,X,y) # create explainer from Dalex

############## visualizations #############
# Generate importance plot showing top 30
explainer.model_parts().plot(max_vars=30)

# Generate ROC curve for xgboost model object
explainer.model_performance(model_type='regression').plot(geom='roc')

# Generate breakdown plot
explainer.predict_parts(X.iloc[79, :]).plot(max_vars=15)

# Generate SHAP plot 
explainer.predict_parts(X.iloc[79, :],type="shap").plot(min_max=[0,1],max_vars=15)

# Generate breakdown interactions plot 
explainer.predict_parts(X.iloc[79, :], type='break_down_interactions').plot(max_vars=20)

# Generate residual plots
explainer.model_performance(model_type = 'classification').plot()

# Generate PDP plots for all variables 
explainer.model_profile(type = 'partial', label="pdp").plot()

# Generate Accumulated Local Effects plots for all variables 
explainer.model_profile(type = 'ale', label="pdp").plot()

# Generate Individual Conditional Expectation plots for worst texture variable 
explainer.model_profile(type = 'conditional', label="conditional",variables="worst texture")

# Generate lime breakdown plot
explainer.predict_surrogate(X.iloc[[79]]).plot()

####### start Arena dashboard #############
# create empty Arena
arena=dx.Arena()

# push created explainer
arena.push_model(explainer)

# push whole test dataset (including target column)
arena.push_observations(X_test)

# run server on port 9294
arena.run_server(port=9291)