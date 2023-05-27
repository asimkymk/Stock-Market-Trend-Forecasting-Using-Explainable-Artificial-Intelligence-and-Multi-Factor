import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing


# Veri dosyasını oku
data = pd.read_csv('tickers.csv')

data = data[(data["symbol"] == 'AAL')]
data['Date'] = pd.to_datetime(data['Date'])
data = data.set_index('Date')
data = data.sort_values('Date')

# Özellikler ve hedef değişken ayırma
X = data[['trend_score', 'news_score_model1','Adj Close']]
y = data['Adj Close']

tarih = '2023-02-01'

X_train = X[X.index < tarih]
y_train = y[y.index < tarih]

X_test = X[X.index >= tarih]
y_test = y[y.index >= tarih]

arima_model = ARIMA(y_train, order=(1, 1, 1))
arima_fit = arima_model.fit()
arima_forecast = arima_fit.forecast(steps=len(y_test))


ets_model = ExponentialSmoothing(y_train, trend='add', seasonal='add', seasonal_periods=12)
ets_fit = ets_model.fit()
ets_forecast = ets_fit.forecast(steps=len(y_test))


print("ARIMA modeli için Test Kümesi Ortalama Kare Hatası: %.2f" % mean_squared_error(y_test, arima_forecast))
print("ETS modeli için Test Kümesi Ortalama Kare Hatası: %.2f" % mean_squared_error(y_test, ets_forecast))
