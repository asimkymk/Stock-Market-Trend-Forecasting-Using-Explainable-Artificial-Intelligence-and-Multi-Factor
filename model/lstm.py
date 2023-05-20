import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Veri dosyasını oku
data = pd.read_csv("tickers.csv")

data = data[(data["symbol"] == "AAL")]
data["Date"] = pd.to_datetime(data["Date"])
data = data.set_index("Date")
data = data.sort_values("Date")

# Hedef değişken ayırma
y = data["Adj Close"]

tarih = "2023-02-01"

# Eğitim ve test verileri ayırma
y_train = y[y.index < tarih]
y_test = y[y.index >= tarih]

# Regression modelleri için veri özellikleri
X = data[["trend_score", "news_score_model1"]]
X_train = X[X.index < tarih]
X_test = X[X.index >= tarih]

# LSTM için veri önişleme
n_steps = 5
X_train_lstm = np.array([X_train.values[i-n_steps:i, :] for i in range(n_steps, len(X_train))])
y_train_lstm = y_train.values[n_steps:]
X_test_lstm = np.array([X_test.values[i-n_steps:i, :] for i in range(n_steps, len(X_test))])
y_test_lstm = y_test.values[n_steps:]

# Verileri LSTM için normalleştirme


# LSTM modelini oluşturma
lstm_model = Sequential()
lstm_model.add(LSTM(50, activation='relu', input_shape=(n_steps, X_train.shape[1])))
lstm_model.add(Dense(1))
lstm_model.compile(optimizer='adam', loss='mse')

# LSTM modelini eğitme
lstm_model.fit(X_train_lstm, y_train_lstm, epochs=10, verbose=0)

# LSTM ile tahmin yapma
lstm_forecast = lstm_model.predict(X_test_lstm)

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
    plt.plot(y_test.index[n_steps:], forecast, label=model_name)

plt.plot(y_test.index, y_test, label='Gerçek Değerler', color='black', linewidth=2)
plt.xlabel('Date')
plt.ylabel('Adj Close')
plt.title('Tahminler ve Gerçek Değerler')
plt.legend()
plt.show()