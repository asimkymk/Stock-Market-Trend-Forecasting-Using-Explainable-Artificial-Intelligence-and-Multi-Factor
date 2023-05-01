import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
import distutils
print(distutils.__file__)
# Veri dosyasını oku
data = pd.read_csv('tickers.csv')

data = data[(data["symbol"] == 'AAPL')]
data['Date'] = pd.to_datetime(data['Date'])
data = data.set_index('Date')
data = data.sort_values('Date')

# Özellikler ve hedef değişken ayırma
X = data[['trend_score', 'news_score_model2','Adj Close']]
y = data['Adj Close']

tarih = '2023-03-01'

# Eğitim ve test verileri ayırma
X_train = X[X.index < tarih]
y_train = y[y.index < tarih]

# Seçilen tarihten sonraki verileri test verileri olarak kullanın
X_test = X[X.index >= tarih]
y_test = y[y.index >= tarih]

# Modelleri tanımla
models = [
    ('XGBoost', xgb.XGBRegressor(objective='reg:squarederror', colsample_bytree=0.3, learning_rate=0.1,
                max_depth=10, alpha=10, n_estimators=100)),
    ('Random Forest', RandomForestRegressor(n_estimators=100)),
    ('Gradient Boosting', GradientBoostingRegressor(n_estimators=100)),
    ('Linear Regression', LinearRegression()),
    ('Lasso Regression', Lasso(alpha=0.1)),
    ('Ridge Regression', Ridge(alpha=0.1)),
    ('Elastic Net', ElasticNet(alpha=0.1, l1_ratio=0.5)),
    ('Support Vector Regression', SVR(kernel='linear')),
    ('Decision Tree', DecisionTreeRegressor()),
    ('K-Nearest Neighbors', KNeighborsRegressor(n_neighbors=5))
]

# Her modeli eğit ve performansını yazdır
for name, model in models:
    model.fit(X_train, y_train)
    train_mse = mean_squared_error(y_train, model.predict(X_train))
    test_mse = mean_squared_error(y_test, model.predict(X_test))
    print(f"{name} modeli için Eğitim Kümesi Ortalama Kare Hatası: {train_mse:.2f}")
    print(f"{name} modeli için Test Kümesi Ortalama Kare Hatası: {test_mse:.2f}\n")
