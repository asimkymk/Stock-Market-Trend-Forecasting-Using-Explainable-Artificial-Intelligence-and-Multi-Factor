import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
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
plt.plot(X_test.index, adj_close_pred,color='blue')
plt.plot(X_test.index, y_test,color='red')
plt.xlabel('Date')
plt.ylabel('News Score Model 1')
plt.title('News Score Model 1 by Date')
plt.show()

import shap
X = X.reset_index(drop=True)
explainer = shap.TreeExplainer(xgb_model)
shap_values = explainer.shap_values(X)
expected_value = explainer.expected_value

############## visualizations #############
# Generate summary dot plot
shap.summary_plot(shap_values, X,title="SHAP summary plot") 

# Generate summary bar plot 
shap.summary_plot(shap_values, X,plot_type="bar") 

# Generate waterfall plot  
shap.plots._waterfall.waterfall_legacy(expected_value, shap_values[79], features=X.loc[79,:], feature_names=X.columns, max_display=15, show=True)

# Generate dependence plot
shap.dependence_plot("Adj Close", shap_values, X)

# Generate multiple dependence plots
for name in X_train.columns:
     shap.dependence_plot(name, shap_values, X)
shap.dependence_plot("Adj Close", shap_values, X)

# Generate force plot - Multiple rows 
shap.force_plot(explainer.expected_value, shap_values[:100,:], X.iloc[:100,:])

# Generate force plot - Single
shap.force_plot(explainer.expected_value, shap_values[0,:], X.iloc[0,:])

# Generate Decision plot 
shap.decision_plot(expected_value, shap_values[79],link='logit' ,features=X.loc[79,:], feature_names=(X.columns.tolist()),show=True,title="Decision Plot")



