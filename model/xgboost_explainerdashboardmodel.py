import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from explainerdashboard import RegressionExplainer, ExplainerDashboard
import dash_bootstrap_components as dbc
data = pd.read_csv('tickers.csv')

data = data[(data["symbol"] == 'AAL')]
data['Date'] = pd.to_datetime(data['Date'])
data = data.set_index('Date')
data = data.sort_values('Date')

# Özellikler ve hedef değişken ayırma
X = data[['trend_score', 'news_score_model3']]
y = data['Adj Close']

tarih = '2023-01-01'

# Eğitim ve test verileri ayırma
X_train = X[X.index < tarih]
y_train = y[y.index < tarih]

# Seçilen tarihten sonraki verileri test verileri olarak kullanın
X_test = X[X.index >= tarih]
y_test = y[y.index >= tarih]

# XGBoost modeli
xgb_model = xgb.XGBRegressor(objective='reg:squarederror', colsample_bytree=0.3, learning_rate=0.1,
                max_depth=10, alpha=10, n_estimators=100)

# Modeli eğitme
xgb_model.fit(X_train, y_train)

# Test verileri üzerinden tahmin yapma
adj_close_pred = xgb_model.predict(X_test)

# Model performansını değerlendirme
mse = mean_squared_error(y_test, adj_close_pred)
print("Mean Squared Error: %.2f" % mse)

# RegressionExplainer oluşturma
explainer = RegressionExplainer(xgb_model, X_train, y_train)

# Görselleştirme
db = ExplainerDashboard(explainer,hide_poweredby=True,header_hide_title=True,header_hide_download=False,header_hide_selector=False, bootstrap=dbc.themes.MATERIA)
db.run()
