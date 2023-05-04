import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, ElasticNet
from sklearn.metrics import mean_squared_error
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import xgboost as xgb

# Veri dosyasını oku
data = pd.read_csv("tickers.csv")

data = data[(data["symbol"] == "AAL")]
data["Date"] = pd.to_datetime(data["Date"])
data = data.set_index("Date")
data = data.sort_values("Date")

# Hedef değişken ayırma
y = data["Adj Close"]

tarih = "2023-02-01"

# Eğitim ve test verileri ayırma
y_train = y[y.index < tarih]
y_test = y[y.index >= tarih]

# ARIMA modeli
arima_model = ARIMA(y_train, order=(1, 1, 1))
arima_fit = arima_model.fit()
arima_forecast = arima_fit.forecast(steps=len(y_test))

# ETS modeli
ets_model = ExponentialSmoothing(
    y_train, trend="add", seasonal="add", seasonal_periods=12
)
ets_fit = ets_model.fit()
ets_forecast = ets_fit.forecast(steps=len(y_test))


# Regression modelleri için veri özellikleri
X = data[["trend_score", "news_score_model3", "Adj Close"]]
X_train = X[X.index < tarih]
X_test = X[X.index >= tarih]

# Random Forest modeli
rf_model = RandomForestRegressor(n_estimators=100, random_state=0)
rf_model.fit(X_train, y_train)
rf_forecast = rf_model.predict(X_test)

# Gradient Boosting modeli
gb_model = GradientBoostingRegressor(
    n_estimators=100, learning_rate=0.1, max_depth=1, random_state=0
)
gb_model.fit(X_train, y_train)
gb_forecast = gb_model.predict(X_test)

# Linear Regression modeli
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_forecast = lr_model.predict(X_test)

# Support Vector Regression modeli
svr_model = SVR(kernel="linear")
svr_model.fit(X_train, y_train)
svr_forecast = svr_model.predict(X_test)

# Decision Tree modeli
dt_model = DecisionTreeRegressor(random_state=0)
dt_model.fit(X_train, y_train)
dt_forecast = dt_model.predict(X_test)

# K-Nearest Neighbors modeli
knn_model = KNeighborsRegressor(n_neighbors=5)
knn_model.fit(X_train, y_train)
knn_forecast = knn_model.predict(X_test)

# XGB modeli
xgb_model = xgb.XGBRegressor(
    objective="reg:squarederror",
    colsample_bytree=0.3,
    learning_rate=0.1,
    max_depth=10,
    alpha=10,
    n_estimators=100,
)
xgb_model.fit(X_train, y_train)
xgb_forecast = xgb_model.predict(X_test)

# Ridge
ridge_model = Ridge(alpha=1)
ridge_model.fit(X_train, y_train)
ridge_forecast = ridge_model.predict(X_test)

# ElasticNET
elasticnet_model = ElasticNet(alpha=1, l1_ratio=0.5)
elasticnet_model.fit(X_train, y_train)
elasticnet_forecast = elasticnet_model.predict(X_test)
# Tahminlerin performansını değerlendirme
models = {
    "ARIMA": arima_forecast,
    "ETS": ets_forecast,
    "Random Forest": rf_forecast,
    "Gradient Boosting": gb_forecast,
    "Linear Regression": lr_forecast,
    "Support Vector Regression": svr_forecast,
    "Decision Tree": dt_forecast,
    "K-Nearest Neighbors": knn_forecast,
    "XGBoost": xgb_forecast,
    "Ridge Regression": ridge_forecast,
    "ElasticNet": elasticnet_forecast,
}

for model_name, forecast in models.items():
    mse = mean_squared_error(y_test, forecast)
    print(f"{model_name} modeli için Test Kümesi Ortalama Kare Hatası: {mse:.2f}")

# Tahminleri grafikle gösterme
plt.figure(figsize=(15, 8))

for model_name, forecast in models.items():
    plt.plot(y_test.index, forecast, label=model_name)

plt.plot(y_test.index, y_test, label='Gerçek Değerler', color='black', linewidth=2)
plt.xlabel('Date')
plt.ylabel('Adj Close')
plt.title('Tahminler ve Gerçek Değerler')
plt.legend()
plt.show()
