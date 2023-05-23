
import xgboost as xgb
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression, Ridge, ElasticNet

def random_forest_model(X_train,y_train):
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    return rf_model

def gradient_boost_model(X_train,y_train):
    gb_model = GradientBoostingRegressor(
    n_estimators=100, learning_rate=0.1, max_depth=1, random_state=42
    )
    gb_model.fit(X_train, y_train)
    return gb_model

def linear_regression_model(X_train,y_train):
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    return lr_model

def svr_model(X_train,y_train):
    svr_model = SVR()
    svr_model.fit(X_train, y_train)
    return svr_model

def decision_tree_model(X_train,y_train):
    dt_model = DecisionTreeRegressor(random_state=42)
    dt_model.fit(X_train, y_train)
    return dt_model

def knn_model(X_train,y_train):
    knn_model = KNeighborsRegressor(n_neighbors=5)
    knn_model.fit(X_train, y_train)
    return knn_model

def xgboost_model(X_train,y_train):
    xgb_model = xgb.XGBRegressor(
    objective="reg:squarederror",
    colsample_bytree=0.1,
    learning_rate=0.01,
    max_depth=2,
    alpha=30,
    n_estimators=500,
    subsample=1,
    )
    xgb_model.fit(X_train, y_train)
    return xgb_model

def elastic_net_model(X_train,y_train):
    elasticnet_model = ElasticNet(alpha=1, l1_ratio=0.5,random_state=42)
    elasticnet_model.fit(X_train, y_train)
    return elasticnet_model

def ridge_regression_model(X_train,y_train):
    ridge_model = Ridge(alpha= 10,random_state=42)
    ridge_model.fit(X_train, y_train)
    return ridge_model