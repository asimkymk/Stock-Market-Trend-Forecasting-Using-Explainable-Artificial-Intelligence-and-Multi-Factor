import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
import shap
import matplotlib.pyplot as plt
from shapash.explainer.smart_explainer import SmartExplainer
import shapash
# Veri dosyasını oku
data = pd.read_csv('tickers.csv')

data = data[(data["symbol"] == 'AAL')]
data['Date'] = pd.to_datetime(data['Date'])
data = data.set_index('Date')
data = data.sort_values('Date')

# Özellikler ve hedef değişkeni ayırma
X = data[['trend_score', 'news_score_model3']]
y = data['Adj Close']

tarih = '2023-01-01'

# Eğitim ve test verilerini ayırma
X_train = X[X.index < tarih]
y_train = y[y.index < tarih]
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

xpl = SmartExplainer(model=xgb_model)
xpl.compile(
    x=X_test,
    
)
#Creating Application
app = xpl.run_app(title_story='Stock Trend')

############## visualizations #############
# feature importance based on SHAP
xpl.plot.features_importance()

# contributions plot
xpl.plot.contribution_plot("worst concave points")

# Local explanation
xpl.plot.local_plot(index=79)

# compare plot 
xpl.plot.compare_plot(index=[X_test.index[79], X_test.index[80]])

# Interactive interactions widget 
xpl.plot.top_interactions_plot(nb_top_interactions=5)

# save contributions
predictor = xpl.to_smartpredictor()
predictor.add_input(x=X_train, ypred=y_train)
detailed_contributions = predictor.detail_contributions()
