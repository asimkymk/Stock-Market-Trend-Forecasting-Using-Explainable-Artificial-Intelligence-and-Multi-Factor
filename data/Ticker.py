# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:12:54 2023

@author: asimk
"""
import yfinance as yf
import pandas as pd
import os

def check_folder_status(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

class Ticker:

    def __init__(self,symbol,period="6mo"):
        self.symbol = symbol
        self.stock_data = yf.download(self.symbol)

    def create_stock_data(self,period="6mo"):
        try:
            self.stock_data = yf.download(self.symbol)
            return True
        except:
            return False

    def to_csv(self,):
        try:
            check_folder_status("one_symbol")
            print(self.stock_data)
            self.stock_data.to_csv('one_symbol/' + self.symbol + '_' + self.period + '_data.csv')
        except:
            raise "Creating csv file error!"

    def get_stock_data_with_symbol(self,):
        data = self.stock_data.copy()
        data['ticker'] = self.symbol
        return data


tickers = ['AAPL', 'GOOG', 'MSFT']


df = pd.DataFrame()
for ticker in tickers:
    a = Ticker(ticker)
    df = pd.concat([df, a.get_stock_data_with_symbol()])
print(df)
print("ok")