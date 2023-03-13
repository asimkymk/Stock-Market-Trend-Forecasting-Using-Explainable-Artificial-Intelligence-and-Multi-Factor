# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:12:54 2023

@author: asimk
"""
import yfinance as yf
import pandas as pd
import os


class Ticker:
    def __init__(self,symbol):
        self.symbol = symbol
        self.stock_data = ""

    def check_folder_status(self,folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    def create_own_data(self,period="6mo"):
        try:
            self.stock_data = yf.download(self.symbol, period="6mo")
            self.check_folder_status("one_symbol")
            print(self.stock_data)
            self.stock_data.to_csv('one_symbol/' + self.symbol + '_' + period + '_data.csv')
            return True
        except:
            return False
        
    
ticker = Ticker("AAPL")

print("ok")