import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


def lstm_model(time_steps,tarih,symbol,parameters):

# Veri dosyasını oku
    data = pd.read_csv("tickers.csv")

    data = data[(data["symbol"] == symbol)]
    data["Date"] = pd.to_datetime(data["Date"])
    data = data.set_index("Date")
    data = data.sort_values("Date")

    scaler = MinMaxScaler(feature_range=(0, 1))
    data['Volume']= scaler.fit_transform(data[['Volume']])
    data['Open']= scaler.fit_transform(data[['Open']])
    data['High']= scaler.fit_transform(data[['High']])
    data['Low']= scaler.fit_transform(data[['Low']])
    data['trend_score']= scaler.fit_transform(data[['trend_score']])
    data['news_score_model1']= scaler.fit_transform(data[['news_score_model1']])
    data['news_score_model3']= scaler.fit_transform(data[['news_score_model3']])
    data['news_score_model2']= scaler.fit_transform(data[['news_score_model2']])
    # Hedef değişken ayırma
    y_lstm = data["Adj Close"]


    # Eğitim ve test verileri ayırma
    y_train_1 = y_lstm[y_lstm.index < tarih]
    y_test_1 = y_lstm[y_lstm.index >= tarih]

    # Regression modelleri için veri özellikleri
    X_lstm = data[parameters]
    X_train_1 = X_lstm[X_lstm.index < tarih]
    X_test_1 = X_lstm[X_lstm.index >= tarih]



    # LSTM için veri önişleme
    n_steps = 5
    # Verileri LSTM için normalleştirme






    def create_dataset(X, y, time_steps=1):
        Xs, ys = [], []
        for i in range(len(X) - time_steps):
            v = X.iloc[i:(i + time_steps)].values
            Xs.append(v)  
            ys.append(y.iloc[i + time_steps])
        return np.array(Xs), np.array(ys)

    

    # reshape to [samples, time_steps, n_features]
    X_train_lstm, y_train_lstm = create_dataset(X_train_1, y_train_1, time_steps)
    X_test_lstm, y_test_lstm = create_dataset(X_test_1, y_test_1, time_steps)

    print(X_train_lstm.shape, y_train_lstm.shape)

    lstm_model = Sequential()
    lstm_model.add(LSTM(64, activation='relu', input_shape=(X_train_lstm.shape[1], X_train_lstm.shape[2])))
    lstm_model.add(Dropout(0.2))
    lstm_model.add(Dense(1))
    lstm_model.compile(optimizer='adam', loss='mse')

    history = lstm_model.fit(
        X_train_lstm, y_train_lstm, 
        epochs=30, 
        batch_size=32, 
        validation_split=0.1,
        shuffle=False
    )

    lstm_forecast = lstm_model.predict(X_test_lstm)

    return [lstm_forecast,y_test_lstm,y_test_1,time_steps]
    # Tahminlerin performansını değerlendirme
    models = {
        "LSTM": lstm_forecast,  # LSTM modelini ekle
    }

    for model_name, forecast in models.items():
        mse = mean_squared_error(y_test_lstm, forecast)
        print(f"{model_name} modeli için Test Kümesi Ortalama Kare Hatası: {mse:.2f}")

    # Tahminleri grafikle gösterme
    plt.figure(figsize=(15, 8))

    for model_name, forecast in models.items():
        plt.plot(y_test_1.index[time_steps:], forecast, label=model_name)  # y_test.index[n_steps:] -> y_test.index[time_steps:]

    plt.plot(y_test_1.index[time_steps:], y_test_1[time_steps:], label='Gerçek Değerler', color='black', linewidth=2)  # y_test.index -> y_test.index[time_steps:], y_test -> y_test[time_steps:]
    plt.xlabel('Date')
    plt.ylabel('Adj Close')
    plt.title('Tahminler ve Gerçek Değerler')
    plt.legend()
    plt.show()