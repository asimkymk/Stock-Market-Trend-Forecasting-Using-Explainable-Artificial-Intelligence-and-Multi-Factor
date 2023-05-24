import pandas as pd
from lime import lime_tabular

import matplotlib.pyplot as plt
import pandas as pd

from sklearn.metrics import mean_squared_error

import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler

from model.models import *
def plot_lime_models(symbol,tarih = '2023-02-01',useTrend=False,news_model=False,delay=2):
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
     
    
    explainer = lime_tabular.LimeTabularExplainer(X_train.values, feature_names=X_train.columns.values, 
                                              class_names=['Adj Close'], mode='regression')
                                             
    instance_to_explain = X_test.iloc[0].values
    exp = explainer.explain_instance(instance_to_explain, xgb_model.predict, num_features=len(X_train.columns))
    plt.figure(figsize=(20,8))
    print(exp.as_list())
    plt.bar([x[0] for x in exp.as_list()], [x[1] for x in exp.as_list()])
    plt.xlabel('Features')
    plt.ylabel('Contribution')
    plt.savefig('./images/figures/lime_explanation.svg')
    plt.show()


