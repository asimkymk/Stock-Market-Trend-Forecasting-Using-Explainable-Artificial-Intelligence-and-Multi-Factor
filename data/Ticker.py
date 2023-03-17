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

    def __init__(self,symbol="",period="6mo",folder_path="one_symbol"):
        self.__symbol = symbol
        self.__period = period
        self.__stock_data = yf.download(self.__symbol,period=self.__period)
        self.__folder_path = folder_path
    
    def set_symbol(self,symbol):
        self.__symbol = symbol

    def get_symbol(self,):
        return self.__symbol

    def set_period(self,period):
        self.__period = period

    def get_period(self,):
        return self.__period
    
    def set_stock_data(self,stock_data):
        self.__stock_data = stock_data

    def get_stock_data(self,):
        return self.__stock_data
    
    def set_folder_path(self,folder_path):
        self.__folder_path = folder_path

    def get_folder_path(self,):
        return self.__folder_path
    
    def create_stock_data(self,period="6mo"):
        try:
            self.__stock_data = yf.download(self.__symbol)
            return True
        except:
            return False

    def to_csv(self,):
        try:
            check_folder_status(self.__folder_path)
            print(self.__stock_data)
            self.__stock_data.to_csv('one_symbol/' + self.__symbol + '_' + self.__period + '_data.csv')
        except:
            raise "Creating csv file error!"

    def get_stock_data_with_symbol(self,):
        data = self.__stock_data.copy()
        data['ticker'] = self.__symbol
        return data


tickers = ['AAPL', 'GOOG', 'MSFT']


df = pd.DataFrame()
for ticker in tickers:
    a = Ticker(symbol=ticker)
    df = pd.concat([df, a.get_stock_data_with_symbol()])
print(df)
print("ok")