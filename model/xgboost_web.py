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



def run_dashboard(port,symbol,news_model,useOpen):
    data = pd.read_csv('tickers.csv')

    data = data[(data["symbol"] == symbol)]
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.set_index('Date')
    data = data.sort_values('Date')

    if useOpen:

        X = data[['trend_score', news_model,"Open"]]
    else:
        X = data[['trend_score', news_model]]
    y = data['Adj Close']

    tarih = '2023-02-01'

    X_train = X[X.index < tarih]
    y_train = y[y.index < tarih]

    X_test = X[X.index >= tarih]
    y_test = y[y.index >= tarih]

    xgb_model = xgb.XGBRegressor(objective='reg:squarederror', colsample_bytree=0.3, learning_rate=0.1,
                    max_depth=10, alpha=10, n_estimators=1000)

    xgb_model.fit(X_train, y_train)

    adj_close_pred = xgb_model.predict(X_test)

    mse = mean_squared_error(y_test, adj_close_pred)
    print("Mean Squared Error: %.2f" % mse)

    explainer = RegressionExplainer(xgb_model, X_train, y_train)
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


