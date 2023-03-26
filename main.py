from data.ticker import Ticker
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

    #df.to_csv("tickers.csv",index=False)

    df.to_csv("news_new.csv",index=False)

def continue_news():
    news = []
    df = pd.read_csv("tickers.csv")
    df2 = pd.read_csv("news_new.csv")
    x = (df['Date'], df['ticker'])
    for i in range(len(x[0])):


        with open('news_new.csv', 'r',encoding='utf-8') as file:
            reader = csv.DictReader(file)
            status = True
            for row in reader:
                if (re.search(x[0][i], row['date']) and re.search(x[1][i], row['symbol'])):
                    status = False
                    break
            if status:
                try:
                    print(x[0][i] + ' - ' + x[1][i])
                    tarih = x[0][i]
                    date_obj = datetime.strptime(tarih, '%Y-%m-%d')
                    yeni_tarih = date_obj.strftime('%m-%d-%Y')
                    googlenews = GoogleNews(start=yeni_tarih,end=yeni_tarih)
                    googlenews.search(x[1][i])
                    
                    result = googlenews.result()
                    
                    for item in result:
                        title = item['title']
                        text = item['desc']
                        link = item['link']
                        news.append([title, text, link,x[0][i],x[1][i]])
                except:
                    
                    break
            
                
    df3 = pd.DataFrame(news)        
    df3.to_csv("news_new.csv",mode="a",index=False,header=False)




continue_news()