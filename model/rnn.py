import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, ElasticNet
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import xgboost as xgb
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, SimpleRNN, Dropout

from sklearn.metrics import accuracy_score
import os
import time

# Veri dosyasını oku
data = pd.read_csv("tickers.csv")

data = data[(data["symbol"] == "TSLA")]
data["Date"] = pd.to_datetime(data["Date"])
data = data.set_index("Date")
data = data.sort_values("Date")

# Hedef değişken ayırma
y = data["Adj Close"]

tarih = "2023-02-01"

# Eğitim ve test verileri ayırma
y_train = y[y.index < tarih]
y_test = y[y.index >= tarih]

X = data[["trend_score", "news_score_model3"]]
X_train = X[X.index < tarih]
X_test = X[X.index >= tarih]

# RNN
rnn_units = 128
dense_units = 64
optimizer = 'RMSprop'
epochs = 200
batch_size = 16

def train_rnn_model():
    rnn_model = Sequential()
    rnn_model.add(SimpleRNN(rnn_units, input_shape=(X_train.shape[1], 1), activation='tanh'))
    rnn_model.add(Dense(dense_units))
    rnn_model.compile(optimizer=optimizer, loss='mse')
    X_train_rnn = X_train.values.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test_rnn = X_test.values.reshape(X_test.shape[0], X_test.shape[1], 1)
    rnn_model.fit(X_train_rnn, y_train, epochs=epochs, batch_size=batch_size)
    rnn_forecast = rnn_model.predict(X_test_rnn)
    return rnn_model, rnn_forecast

model_dosya_adi = "rnn_model_tsla.h5"
yeni_mse = 10000

while yeni_mse > 0.5:
    time.sleep(1)
    rnn_model, rnn_forecast = train_rnn_model()
    X_test_rnn = X_test.values.reshape(X_test.shape[0], X_test.shape[1], 1)
    if os.path.exists(model_dosya_adi):
        mevcut_model = tf.keras.models.load_model(model_dosya_adi)
        mevcut_model.evaluate(X_test_rnn, y_test, verbose=0)
        mevcut_mse = mevcut_model.evaluate(X_test_rnn, y_test, verbose=0)

        yeni_mse = rnn_model.evaluate(X_test_rnn, y_test, verbose=0)
        print("Yüklenen Modelinin Ortalama Karesel Hata (MSE):", mevcut_mse)
        print("Yeni Modelin Ortalama Karesel Hata (MSE):", yeni_mse)

        if yeni_mse < mevcut_mse:
            rnn_model.save(model_dosya_adi)
            print("Yeni model, mevcut kaydedilen modele göre daha iyi. Yeni model kaydedildi.")
        else:
            print("Yeni model, mevcut kaydedilen modele göre daha kötü veya aynı performans. Yeni model kaydedilmedi.")
    else:
        rnn_model.save(model_dosya_adi)
        mse = rnn_model.evaluate(X_test_rnn, y_test, verbose=0)
        print("RNN Modelinin Ortalama Karesel Hata (MSE):", mse)
        print("İlk kez çalıştırılıyor. Yeni model kaydedildi.")