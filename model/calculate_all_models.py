import pandas as pd

from sklearn.metrics import mean_squared_error

import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler

from model.lstm import lstm_model
from model.rnn import rnn_model
from model.models import *
def calculate_all_models(symbol,tarih = '2023-01-01',useTrend=False,news_model=False,delay=2):
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

    # Random Forest modeli
    rf_forecast = random_forest_model(X_train,y_train).predict(X_test)

    # Gradient Boosting modeli
    gb_forecast = gradient_boost_model(X_train,y_train).predict(X_test)

    # Linear Regression modeli
    lr_forecast = linear_regression_model(X_train,y_train).predict(X_test)

    # Support Vector Regression modeli
    svr_forecast = svr_model(X_train,y_train).predict(X_test)

    # Decision Tree modeli
    dt_forecast = decision_tree_model(X_train,y_train).predict(X_test)

    # K-Nearest Neighbors modeli
    knn_forecast = knn_model(X_train,y_train).predict(X_test)

    # XGB modeli
    xgb_forecast = xgboost_model(X_train,y_train).predict(X_test)

    # Ridge
    ridge_forecast = ridge_regression_model(X_train,y_train).predict(X_test)

    # ElasticNET
    elasticnet_forecast = elastic_net_model(X_train,y_train).predict(X_test)

    #lstm
    [lstm_forecast,y_test_lstm,y_test_1,time_steps] = lstm_model(parameters=parameters,time_steps=delay-1,symbol= symbol, tarih=tarih)

    #RNN
    [rnn_forecast, y_test_rnn, y_test_2, time_steps2] = rnn_model(parameters=parameters,time_steps=delay-1,symbol= symbol, tarih=tarih)

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

    total = 0
    for model_name, forecast in models.items():
        mse = 0
        if model_name=='LSTM':
            mse = mean_squared_error(y_test_lstm, forecast)
        elif model_name=='RNN':
            mse = mean_squared_error(y_test_rnn, forecast)
        else:
            mse = mean_squared_error(y_test, forecast)
        total = total + mse 
        print(f"{mse:.2f}\n")
    print("Average: ",total/len(models))

    # Tahminleri grafikle gösterme
    for model_name, forecast in models.items():
        if model_name=='LSTM':
            plt.plot(y_test_1.index[time_steps:], forecast, label=model_name)
        elif model_name=='RNN':
            plt.plot(y_test_2.index[time_steps2:], forecast, label=model_name)
        else:
            plt.plot(y_test.index, forecast, label=model_name)

    real_df = df[df.index >= '2022-12-10']
    plt.plot(real_df.index, real_df['Adj Close'], label='Gerçek Değerler', color='black', linewidth=2)
    plt.xlabel('Date')
    plt.ylabel('Adj Close')
    plt.title('Tahminler ve Gerçek Değerler')
    plt.legend()
    if useTrend:
        if news_model == False:

            plt.savefig("./images/figures/" + str(delay) + "_days_just_trend_score_" + symbol + ".svg")
        
        elif news_model == "news_score_model1":
            plt.savefig("./images/figures/" + str(delay) + "_days_with_trend_score_and_news_score_model_1_" + symbol + ".svg")
        elif news_model == "news_score_model2":
            plt.savefig("./images/figures/" + str(delay) + "_days_with_trend_score_and_news_score_model_2_" + symbol + ".svg")
        else:
            plt.savefig("./images/figures/" + str(delay) + "_days_with_trend_score_and_news_score_model_3_" + symbol + ".svg")
    else:
        if news_model == False:

            plt.savefig("./images/figures/" + str(delay) + "_days_without_mf_" + symbol + ".svg")
        
        elif news_model == "news_score_model1":
            plt.savefig("./images/figures/" + str(delay) + "_days_just_news_score_model_1_" + symbol + ".svg")
        elif news_model == "news_score_model2":
            plt.savefig("./images/figures/" + str(delay) + "_days_just_news_score_model_2_" + symbol + ".svg")
        else:
            plt.savefig("./images/figures/" + str(delay) + "_days_just_news_score_model_3_" + symbol + ".svg")
    plt.show()
