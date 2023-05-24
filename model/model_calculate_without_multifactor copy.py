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
from tensorflow.keras.layers import LSTM
from lstm import lstmm
from rnn import rnn
from sklearn.preprocessing import MinMaxScaler
# Veri dosyasını oku
df = pd.read_csv('tickers.csv')  # ajd_close verinizi içeren dosya

# Veriyi doğru formatta hazırlama
df['Date'] = pd.to_datetime(df['Date'])  # Eğer 'date' adında bir sütununuz varsa

df = df.sort_values('Date')
df = df.set_index('Date')
df = df[(df["symbol"] == "AAL")]
tarih = '2023-01-01'

# Lag özellikleri oluşturma
volume_data = df[['Volume']]

# Veriyi ölçeklendir
scaler = MinMaxScaler(feature_range=(0, 1))
df['Volume']= scaler.fit_transform(volume_data)
df['Open']= scaler.fit_transform(df[['Open']])
df['High']= scaler.fit_transform(df[['High']])
df['Low']= scaler.fit_transform(df[['Low']])
delay = 2
for i in range(1, delay):
    df[f'adj_close_lag_{i}'] = df['Adj Close'].shift(i)
    df[f'open_lag_{i}'] = df['Open'].shift(i)
    df[f'high_lag_{i}'] = df['High'].shift(i)
    df[f'low_lag_{i}'] = df['Low'].shift(i)
    df[f'volume_lag_{i}'] = df['Volume'].shift(i)

# NaN değerleri temizleme
df = df.dropna()
parameters=["Open","High","Low","Adj Close","Volume"]
# Özellikler ve hedef değeri belirleme
features = [f'adj_close_lag_{i}' for i in range(1, delay)]  + [f'open_lag_{i}' for i in range(1, delay)] + [f'high_lag_{i}' for i in range(1, delay)] + [f'low_lag_{i}' for i in range(1, delay)] + [f'volume_lag_{i}' for i in range(1, delay)]
target = 'Adj Close'

# Eğitim ve test seti oluşturma
train_df = df[df.index < tarih]
test_df = df[df.index >= tarih]

X_train = train_df[features]
y_train = train_df[target]

X_test = test_df[features]
y_test = test_df[target]


# ARIMA modeli
arima_model = ARIMA(train_df['Adj Close'], order=(5,1,0))
arima_model_fit = arima_model.fit()
arima_forecast = arima_model_fit.forecast(steps=len(test_df))

# ETS modeli eğitme
ets_model = ExponentialSmoothing(train_df['Adj Close'], trend='add', seasonal='add', seasonal_periods=12)
ets_model_fit = ets_model.fit()
ets_forecast = ets_model_fit.forecast(steps=len(test_df))


# Regression modelleri için veri özellikleri


# Random Forest modeli
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_forecast = rf_model.predict(X_test)


# Gradient Boosting modeli
gb_model = GradientBoostingRegressor(
    n_estimators=100, learning_rate=0.1, max_depth=1, random_state=42
)
gb_model.fit(X_train, y_train)
gb_forecast = gb_model.predict(X_test)

# Linear Regression modeli
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_forecast = lr_model.predict(X_test)

# Support Vector Regression modeli

svr_model = SVR()
svr_model.fit(X_train, y_train)
svr_forecast = svr_model.predict(X_test)

# Decision Tree modeli
dt_model = DecisionTreeRegressor(random_state=42)
dt_model.fit(X_train, y_train)
dt_forecast = dt_model.predict(X_test)

# K-Nearest Neighbors modeli
knn_model = KNeighborsRegressor(n_neighbors=5)
knn_model.fit(X_train, y_train)
knn_forecast = knn_model.predict(X_test)

# XGB modeli

""" {'alpha': 30, 'colsample_bytree': 0.1, 'learning_rate': 0.01, 'max_depth': 2, 'n_estimators': 500, 'subsample': 1}"""

xgb_model = xgb.XGBRegressor(
    objective="reg:squarederror",
    colsample_bytree=0.1,
    learning_rate=0.01,
    max_depth=2,
    alpha=30,
    n_estimators=500,
    subsample=1,
)
xgb_model.fit(X_train, y_train)
xgb_forecast = xgb_model.predict(X_test)

# Ridge
ridge_model = Ridge(alpha= 10,random_state=42)
ridge_model.fit(X_train, y_train)
ridge_forecast = ridge_model.predict(X_test)

# ElasticNET
elasticnet_model = ElasticNet(alpha=1, l1_ratio=0.5,random_state=42)
elasticnet_model.fit(X_train, y_train)
elasticnet_forecast = elasticnet_model.predict(X_test)

#lstm

[lstm_forecast,y_test_lstm,y_test_1,time_steps] = lstmm(parameters=parameters,time_steps=delay-1,symbol= 'AAL', tarih=tarih)
[rnn_forecast, y_test_rnn, y_test_2, time_steps2] = rnn(parameters=parameters,time_steps=delay-1,symbol= 'AAL', tarih=tarih)

# Tahminlerin performansını değerlendirme
models = {
    "Random Forest": rf_forecast,
    "Gradient Boosting": gb_forecast,
    "Linear Regression": lr_forecast,
    "Decision Tree": dt_forecast,
    "SVR":svr_forecast,
    "K-Nearest Neighbors": knn_forecast,
    "XGBoost": xgb_forecast,
    "Ridge Regression": ridge_forecast,
    "ElasticNet": elasticnet_forecast,
    "LSTM": lstm_forecast,
    "RNN":rnn_forecast
}
plt.style.use('seaborn-whitegrid')
plt.figure(figsize=(15, 8))


for model_name, forecast in models.items():
    mse = 0
    if model_name=='LSTM':
        mse = mean_squared_error(y_test_lstm, forecast)
    elif model_name=='RNN':
        mse = mean_squared_error(y_test_rnn, forecast)
    else:
        mse = mean_squared_error(y_test, forecast)
    print(f"{mse:.2f}\n")

# Tahminleri grafikle gösterme
for model_name, forecast in models.items():
    if model_name=='LSTM':
        plt.plot(y_test_1.index[time_steps:], forecast, label=model_name)
    elif model_name=='RNN':
        plt.plot(y_test_2.index[time_steps2:], forecast, label=model_name)
    else:
        plt.plot(y_test.index, forecast, label=model_name)

plt.plot(y_test.index, y_test, label='Gerçek Değerler', color='black', linewidth=2)
plt.xlabel('Date')
plt.ylabel('Adj Close')
plt.title('Tahminler ve Gerçek Değerler')
plt.legend()
plt.savefig("./images/figures/third_score_model_all_models_just_adj_close.svg")
plt.show()
