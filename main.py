from data.Ticker import Ticker
import pandas as pd
import csv
import re
from GoogleNews import GoogleNews
from datetime import datetime
def testt():
    tickers = ['AAPL', 'GOOG', 'MSFT']


    df = pd.DataFrame()
    for symbols in tickers:
        ticker = Ticker(symbol=symbols,)
        ticker.create_stock_data()
        
        df = pd.concat([df, ticker.create_news_data()])
    print(df)
    print("ok")

    df.to_csv("tickers.csv",index=False,mode="a")

    df.to_csv("news_new.csv",index=False)



def create_new_tickers_data():
    tickers = ['AAPL', 'AGNC', 'AMC', 'AMD', 'AMZN', 'APE', 'ATKR', 'BAC', 'BSGA', 'CSCO', 'CTRA', 'DKNG', 'ETRN', 'FDBC', 'FRC', 'GDEN', 'GMDA', 'GMVD', 'GNRC', 'GOOG', 'GRAB', 'HAIA', 'HBAN', 'HLMN', 'HSAI', 'HWCPZ', 'HYFM', 'IMAQ', 'INTC', 'IRMD', 'JBLU', 'MRVL', 'MSFT', 'NIO', 'NVDA', 'PHYS', 'RBLX', 'RIVN', 'ROKU', 'RPHM', 'SCHW', 'SNAP', 'TEAF', 'TSLA', 'UFAB', 'ULBI', 'VALE', 'XPEV', 'XTNT', 'YCBD']
    df = pd.DataFrame()
    for symbols in tickers:
        ticker = Ticker(symbol=symbols,start_date='2022-03-01',end_date='2023-04-04')
        ticker.create_stock_data()
        
        df = pd.concat([df, ticker.get_stock_data()])
    print(df)
    print("ok")

    df.to_csv("tickers.csv",index=False)

    #df.to_csv("news_new.csv",index=False)

def continue_news():
    news = []
    df = pd.read_csv("tickers.csv")

    existing_news = {}
    with open('news_new.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_news[(row['date'], row['symbol'])] = True

    x = (df['Date'], df['symbol'])
    for i in range(len(x[0])):
        if (x[0][i], x[1][i]) not in existing_news:
            try:
                print(x[0][i] + ' - ' + x[1][i])
                tarih = x[0][i]
                date_obj = datetime.strptime(tarih, '%Y-%m-%d')
                yeni_tarih = date_obj.strftime('%m-%d-%Y')
                googlenews = GoogleNews(start=yeni_tarih, end=yeni_tarih)
                googlenews.search('NASDAQ:' + x[1][i])

                result = googlenews.result()

                for item in result:
                    title = item['title']
                    text = item['desc']
                    link = item['link']
                    news.append([title, text, link, x[0][i], x[1][i]])
            except TypeError as e_parser:
                print('Type Error')
                news.append(['NO_TITLE', 'NO_DESC', 'NO_LINK', x[0][i], x[1][i]])
            except:
                break

    df3 = pd.DataFrame(news)
    df3.to_csv("news_new.csv", mode="a", index=False, header=False)




continue_news()
#create_new_tickers_data()
