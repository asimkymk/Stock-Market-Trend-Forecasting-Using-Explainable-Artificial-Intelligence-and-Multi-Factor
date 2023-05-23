import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import SimpleRNN, Dense, Dropout

def rnn_model(time_steps, tarih, symbol, parameters):
    # Veri dosyasını oku
    data = pd.read_csv("tickers.csv")

    data = data[(data["symbol"] == symbol)]
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.set_index("Date")
    data = data.sort_values("Date")

    scaler = MinMaxScaler(feature_range=(0, 1))
    data['Volume'] = scaler.fit_transform(data[['Volume']])
    data['Open'] = scaler.fit_transform(data[['Open']])
    data['High'] = scaler.fit_transform(data[['High']])
    data['Low'] = scaler.fit_transform(data[['Low']])
    data['trend_score']= scaler.fit_transform(data[['trend_score']])
    data['news_score_model1']= scaler.fit_transform(data[['news_score_model1']])
    data['news_score_model3']= scaler.fit_transform(data[['news_score_model3']])
    data['news_score_model2']= scaler.fit_transform(data[['news_score_model2']])
    # Hedef değişken ayırma
    y_rnn = data["Adj Close"]

    # Eğitim ve test verileri ayırma
    y_train_1 = y_rnn[y_rnn.index < tarih]
    y_test_1 = y_rnn[y_rnn.index >= tarih]

    # Regression modelleri için veri özellikleri
    X_rnn = data[parameters]
    X_train_1 = X_rnn[X_rnn.index < tarih]
    X_test_1 = X_rnn[X_rnn.index >= tarih]

    # RNN için veri önişleme
    n_steps = 5
    # Verileri RNN için normalleştirme

    def create_dataset(X, y, time_steps=1):
        Xs, ys = [], []
        for i in range(len(X) - time_steps):
            v = X.iloc[i:(i + time_steps)].values
            Xs.append(v)
            ys.append(y.iloc[i + time_steps])
        return np.array(Xs), np.array(ys)

    # reshape to [samples, time_steps, n_features]
    X_train_rnn, y_train_rnn = create_dataset(X_train_1, y_train_1, time_steps)
    X_test_rnn, y_test_rnn = create_dataset(X_test_1, y_test_1, time_steps)

    print(X_train_rnn.shape, y_train_rnn.shape)

    rnn_model = Sequential()
    rnn_model.add(SimpleRNN(64, activation='relu', input_shape=(X_train_rnn.shape[1], X_train_rnn.shape[2])))
    rnn_model.add(Dropout(0.2))
    rnn_model.add(Dense(1))
    rnn_model.compile(optimizer='adam', loss='mse')

    history = rnn_model.fit(
        X_train_rnn, y_train_rnn,
        epochs=30,
        batch_size=32,
        validation_split=0.1,
        shuffle=False
    )

    rnn_forecast = rnn_model.predict(X_test_rnn)

    return [rnn_forecast, y_test_rnn, y_test_1, time_steps]