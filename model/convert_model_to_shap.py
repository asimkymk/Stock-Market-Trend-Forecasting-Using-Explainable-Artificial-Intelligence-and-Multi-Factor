import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
# Veri dosyasını oku
import pandas as pd

from sklearn.metrics import mean_squared_error

import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler

from model.lstm import lstm_model
from model.rnn import rnn_model
from model.models import *
def plot_shap_models(symbol,tarih = '2023-02-01',useTrend=False,news_model=False,delay=2):
     # Veri dosyasını oku
     df = pd.read_csv('tickers.csv')  # ajd_close verinizi içeren dosya

     # Veriyi doğru formatta hazırlama
     df['Date'] = pd.to_datetime(df['Date'])  # Eğer 'date' adında bir sütununuz varsa

     df = df.sort_values('Date')
     df = df.set_index('Date')
     df = df[(df["symbol"] == symbol)]

     # Lag özellikleri oluşturma
     volume_data = df[['Volume']]

     # Veriyi ölçeklendir
     scaler = MinMaxScaler(feature_range=(0, 1))
     df['Volume']= scaler.fit_transform(volume_data)
     df['Open']= scaler.fit_transform(df[['Open']])
     df['High']= scaler.fit_transform(df[['High']])
     df['Low']= scaler.fit_transform(df[['Low']])
     df['trend_score']= scaler.fit_transform(df[['trend_score']])
     df['news_score_model1']= scaler.fit_transform(df[['news_score_model1']])
     df['news_score_model2']= scaler.fit_transform(df[['news_score_model2']])
     df['news_score_model3']= scaler.fit_transform(df[['news_score_model3']])

    
     for i in range(1, delay):
          df[f'adj_close_lag_{i}'] = df['Adj Close'].shift(i)
          df[f'open_lag_{i}'] = df['Open'].shift(i)
          df[f'high_lag_{i}'] = df['High'].shift(i)
          df[f'low_lag_{i}'] = df['Low'].shift(i)
          df[f'volume_lag_{i}'] = df['Volume'].shift(i)
          df[f'news_score_model1_lag_{i}'] = df['news_score_model1'].shift(i)
          df[f'news_score_model2_lag_{i}'] = df['news_score_model2'].shift(i)
          df[f'news_score_model3_lag_{i}'] = df['news_score_model3'].shift(i)
          df[f'trend_score_lag_{i}'] = df['trend_score'].shift(i)
        
        

    # NaN değerleri temizleme
    
     parameters=["Open","High","Low","Adj Close","Volume"]
     features = [f'adj_close_lag_{i}' for i in range(1, delay)]  + [f'open_lag_{i}' for i in range(1, delay)] + [f'high_lag_{i}' for i in range(1, delay)] + [f'low_lag_{i}' for i in range(1, delay)] + [f'volume_lag_{i}' for i in range(1, delay)]
     if useTrend:
          parameters.append("trend_score")
          features += [f'trend_score_lag_{i}' for i in range(1, delay)] 
     if not news_model==False:
          if news_model == "news_score_model1":
               parameters.append("news_score_model1")
               features += [f'news_score_model1_lag_{i}' for i in range(1, delay)]
          elif news_model == "news_score_model2":
               parameters.append("news_score_model2")
               features += [f'news_score_model2_lag_{i}' for i in range(1, delay)]
          else:
               parameters.append("news_score_model3")
               features += [f'news_score_model3_lag_{i}' for i in range(1, delay)]
     target = 'Adj Close'
     df = df.dropna()
     # Eğitim ve test seti oluşturma
     train_df = df[df.index < tarih]
     test_df = df[df.index >= tarih]

     X_train = train_df[features]
     y_train = train_df[target]

     X_test = test_df[features]
     y_test = test_df[target]
     print(X_train)

     xgb_model = xgboost_model(X_train,y_train)

     # Tahminlerin performansını değerlendirme

     plt.style.use('seaborn-whitegrid')
     

     import shap
     X = X_train.reset_index(drop=True)
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
     #shap.dependence_plot("Open", shap_values, X)

     # Generate multiple dependence plots
     for name in X_train.columns:
          shap.dependence_plot(name, shap_values, X)
     #shap.dependence_plot("Open", shap_values, X)

     # Generate force plot - Multiple rows 
     shap.force_plot(explainer.expected_value, shap_values[:100,:], X.iloc[:100,:])

     # Generate force plot - Single
     shap.force_plot(explainer.expected_value, shap_values[0,:], X.iloc[0,:])

     # Generate Decision plot 
     shap.decision_plot(expected_value, shap_values[79],link='logit' ,features=X.loc[79,:], feature_names=(X.columns.tolist()),show=True,title="Decision Plot")



