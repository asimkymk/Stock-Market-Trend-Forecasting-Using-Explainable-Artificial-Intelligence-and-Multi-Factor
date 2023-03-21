from data.ticker import Ticker
import pandas as pd
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