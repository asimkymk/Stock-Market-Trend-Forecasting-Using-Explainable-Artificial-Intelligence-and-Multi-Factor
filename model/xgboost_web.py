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
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, ElasticNet


def random_forest_model(X_train,y_train):
    rf_model = RandomForestRegressor(n_estimators=100, random_state=0)
    rf_model.fit(X_train, y_train)
    return rf_model

def gradient_boost_model(X_train,y_train):
    gb_model = GradientBoostingRegressor(
    n_estimators=100, learning_rate=0.1, max_depth=1, random_state=0
    )
    gb_model.fit(X_train, y_train)
    return gb_model

def linear_regression_model(X_train,y_train):
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    return lr_model

def svr_model(X_train,y_train):
    svr_model = SVR(kernel="linear")
    svr_model.fit(X_train, y_train)
    return svr_model

def decision_tree_model(X_train,y_train):
    dt_model = DecisionTreeRegressor(random_state=0)
    dt_model.fit(X_train, y_train)
    return dt_model

def knn_model(X_train,y_train):
    knn_model = KNeighborsRegressor(n_neighbors=5)
    knn_model.fit(X_train, y_train)
    return knn_model

def xgboost_model(X_train,y_train):
    xgb_model = xgb.XGBRegressor(
    objective="reg:squarederror",
    colsample_bytree=0.3,
    learning_rate=0.1,
    max_depth=10,
    alpha=10,
    n_estimators=100,
    )
    xgb_model.fit(X_train, y_train)
    return xgb_model

def elastic_net_model(X_train,y_train):
    elasticnet_model = ElasticNet(alpha=1, l1_ratio=0.5)
    elasticnet_model.fit(X_train, y_train)
    return elasticnet_model

def ridge_regression_model(X_train,y_train):
    ridge_model = Ridge(alpha= 10)
    ridge_model.fit(X_train, y_train)
    return ridge_model

def run_dashboard(port,symbol,news_model,useOpen,modelName):
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


