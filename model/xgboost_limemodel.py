import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from lime import lime_tabular

# Veri dosyasını oku
data = pd.read_csv('tickers.csv')

data = data[(data["symbol"] == 'MSFT')]
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
print(y_test)
print(adj_close_pred)

# Model performansını değerlendirme
mse = mean_squared_error(y_test, adj_close_pred)
print("Mean Squared Error: %.2f" % mse)

# Lime ile model açıklaması yapma
explainer = lime_tabular.LimeTabularExplainer(X_train.values, feature_names=X_train.columns.values, 
                                              class_names=['Adj Close'], mode='regression')
                                             
instance_to_explain = X_test.iloc[0].values
exp = explainer.explain_instance(instance_to_explain, xgb_model.predict, num_features=len(X_train.columns))
print(exp.as_list())
plt.bar([x[0] for x in exp.as_list()], [x[1] for x in exp.as_list()])
plt.xlabel('Features')
plt.ylabel('Contribution')
plt.savefig('lime_explanation.png')
plt.show()