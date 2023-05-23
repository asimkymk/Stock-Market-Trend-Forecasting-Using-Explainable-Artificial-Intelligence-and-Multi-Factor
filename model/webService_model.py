from multiprocessing import Process
import pandas as pd
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from explainerdashboard import RegressionExplainer, ExplainerDashboard
import dash_bootstrap_components as dbc
from multiprocessing import Process
from waitress import serve
import os
import signal
from sklearn.preprocessing import MinMaxScaler

from models import *

def run_dashboard(port,symbol,news_model,useTrend,modelName,delay):
    df = pd.read_csv('tickers.csv')  # ajd_close verinizi içeren dosya

    # Veriyi doğru formatta hazırlama
    df['Date'] = pd.to_datetime(df['Date'])  # Eğer 'date' adında bir sütununuz varsa

    df = df.sort_values('Date')
    df = df.set_index('Date')
    df = df[(df["symbol"] == symbol)]
    tarih = '2023-01-01'

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
        
        

    # NaN değerleri temizleme
    df = df.dropna()
    
    parameters=["Open","High","Low","Adj Close","Volume"]
    features = [f'adj_close_lag_{i}' for i in range(1, delay)]  + [f'open_lag_{i}' for i in range(1, delay)] + [f'high_lag_{i}' for i in range(1, delay)] + [f'low_lag_{i}' for i in range(1, delay)] + [f'volume_lag_{i}' for i in range(1, delay)]
    if useTrend:
        df[f'trend_score_lag_{i}'] = df['trend_score'].shift(i)
        parameters.append("trend_score")
        features += [f'trend_score_lag_{i}' for i in range(1, delay)] 
    if not news_model=="none":
        if news_model == "news_score_model1":
            df[f'news_score_model1_lag_{i}'] = df['news_score_model1'].shift(i)
            parameters.append("news_score_model1")
            features += [f'news_score_model1_lag_{i}' for i in range(1, delay)]
        elif news_model == "news_score_model2":
            df[f'news_score_model2_lag_{i}'] = df['news_score_model2'].shift(i)
            parameters.append("news_score_model2")
            features += [f'news_score_model2_lag_{i}' for i in range(1, delay)]
        else:
            df[f'news_score_model3_lag_{i}'] = df['news_score_model3'].shift(i)
            parameters.append("news_score_model3")
            features += [f'news_score_model3_lag_{i}' for i in range(1, delay)]
            

    # Özellikler ve hedef değeri belirleme
    
    target = 'Adj Close'

    # Eğitim ve test seti oluşturma
    train_df = df[df.index < tarih]
    test_df = df[df.index >= tarih]

    X_train = train_df[features]
    y_train = train_df[target]

    X_test = test_df[features]
    y_test = test_df[target]

    models = {
    "Random_Forest": random_forest_model,
    "Gradient_Boosting": gradient_boost_model,
    "Linear_Regression": linear_regression_model,
    "Support_Vector_Regression": svr_model,
    "Decision_Tree": decision_tree_model,
    "KNN_Neighbors": knn_model,
    "XGBoost": xgboost_model,
    "ElasticNet":elastic_net_model,
    "Ridge_Regression":ridge_regression_model
    }

    model = models[modelName](X_train,y_train)

    print(type(model))
    adj_close_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, adj_close_pred)
    print("Mean Squared Error: %.2f" % mse)

    explainer = RegressionExplainer(model, X_train, y_train)
    db = ExplainerDashboard(explainer, mode='dash', use_waitress=False, hide_poweredby=True, header_hide_title=True,
                            header_hide_download=False, header_hide_selector=False, bootstrap=dbc.themes.MATERIA)

    @db.app.server.route('/shutdown', methods=['GET'])
    def shutdown():
        from flask import request
        if request.method == 'GET':
            print('Shutting down gracefully...')
            os.kill(os.getpid(), signal.SIGINT)
            return 'Server shutting down...'
    
    serve(db.app.server, port=port)


