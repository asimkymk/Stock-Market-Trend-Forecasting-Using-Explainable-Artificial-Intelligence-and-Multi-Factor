from newsapi import NewsApiClient

# Init
import yfinance as yf
import pandas_datareader as pdr
from datetime import datetime

# tarihte yayınlanan tüm haberleri getirin
print(pdr.get_components_yahoo(idx_sym="GOOG"))