# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:30:42 2023

@author: asimk
"""

import yfinance as yf
import pandas as pd

tickers = ['AAPL', 'GOOG', 'MSFT']


df = pd.DataFrame()
for ticker in tickers:
    tickerData = yf.Ticker(ticker)
    tickerDf = tickerData.history(period='6mo')
    tickerDf['ticker'] = ticker
    df = pd.concat([df, tickerDf])

df.to_csv('tickers.csv', index=True)