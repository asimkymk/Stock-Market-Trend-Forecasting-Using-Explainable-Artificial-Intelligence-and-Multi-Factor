import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def check_folder(symbol):
    if not os.path.exists('images/'+symbol):
        os.makedirs('images/' + symbol)

def show_all_data(symbol):
    plt.style.use("seaborn-bright")
    data = pd.read_csv('tickers.csv')
    data = data[(data["symbol"] == symbol)]
    data['Date'] = pd.to_datetime(data['Date'])

    # 'Date' sütununa göre sırala
    data = data.sort_values('Date')

    # 'Date' ve 'Adj Close' sütunlarını ayıkla
    adj_close = data[['Date', 'Adj Close']]
    news_score_model1 = data[['Date', 'news_score_model1']]
    news_score_model2 = data[['Date', 'news_score_model2']]
    news_score_model3 = data[['Date', 'news_score_model3']]
    trend_score = data[['Date', 'trend_score']]
    # 'Date' sütununu indeks olarak ayarla
    adj_close = adj_close.set_index('Date')
    news_score_model1 = news_score_model1.set_index('Date')
    news_score_model2 = news_score_model2.set_index('Date')
    news_score_model3 = news_score_model3.set_index('Date')
    trend_score = trend_score.set_index('Date')
    # görselleştirme kodları
    plt.plot(adj_close.index, adj_close['Adj Close'])
    plt.xlabel('Date')
    plt.ylabel('Adj Close')
    plt.title('Adj Close by Date')
    plt.savefig('images/'+ symbol + '/adj_close.svg', format='svg')
    plt.clf()

    # 'news_score_model1' grafiği
    plt.plot(news_score_model1.index, news_score_model1['news_score_model1'])
    plt.xlabel('Date')
    plt.ylabel('News Score Model 1')
    plt.title('News Score Model 1 by Date')
    plt.savefig('images/'+ symbol + '/news_score_model1.svg', format='svg')
    plt.clf()

    # 'news_score_model2' grafiği
    plt.plot(news_score_model1.index, news_score_model2['news_score_model2'])
    plt.xlabel('Date')
    plt.ylabel('News Score Model 2')
    plt.title('News Score Model 2 by Date')
    plt.savefig('images/'+ symbol + '/news_score_model2.svg', format='svg')
    plt.clf()

    # 'news_score_model3' grafiği
    plt.plot(news_score_model1.index, news_score_model3['news_score_model3'])
    plt.xlabel('Date')
    plt.ylabel('News Score Model 3')
    plt.title('News Score Model 3 by Date')
    plt.savefig('images/'+ symbol + '/news_score_model3.svg', format='svg')
    plt.clf()

    # 'news_score_model3' grafiği
    plt.plot(trend_score.index, trend_score['trend_score'])
    plt.xlabel('Date')
    plt.ylabel('Trend Score')
    plt.title('Trend Score by Date')
    plt.savefig('images/'+ symbol + '/trend_score.svg', format='svg')
    plt.clf()