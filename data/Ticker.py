# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 14:12:54 2023

@author: asimk
"""
import yfinance as yf
import pandas as pd
import os
from GoogleNews import GoogleNews
from news_scorer import NewsScorer
from datetime import datetime
import time
def check_folder_status(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

class Ticker:

    def __init__(self,symbol="",period="6mo",folder_path="one_symbol"):
        self.__symbol = symbol
        self.__period = period
        self.__stock_data = ""
        self.__stock_data = ""
        self.__folder_path = folder_path
        self.__news_data = ""
    
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
    
    def create_stock_data(self,):
        try:
            self.__stock_data = yf.download(self.__symbol,period=self.__period)
            self.__stock_data = self.__stock_data.reset_index()
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

    def create_news_data(self,):
        news_scorer = NewsScorer()
        dates = self.__stock_data['Date'].astype(str)
        scores = []
        for date in dates:
            print("**********************************")
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            formatted_date_str = date_obj.strftime('%m-%d-%Y')
            try:
                print(self.__symbol + ' - ' + formatted_date_str)
                googlenews = GoogleNews(start=formatted_date_str,end=formatted_date_str)
                googlenews.search(self.__symbol)
                
                result = googlenews.result()
                news = []
                for item in result:
                    title = item['title']
                    text = item['desc']
                    news.append([title, text, date])
                __news_data = pd.DataFrame(news, columns=['title', 'text', "date"])
                news_scorer.set_news_data(__news_data)
                news_scorer.create_scored_data()
                scores.append(news_scorer.get_average_score()[date])
                time.sleep(1) # avoid 429 too many request
            except:
                break

        self.__stock_data['date_scores'] = pd.Series(scores)
        return self.__stock_data

tickers = ['AAPL', 'GOOG', 'MSFT']


df = pd.DataFrame()
for symbols in tickers:
    ticker = Ticker(symbol=symbols,)
    ticker.create_stock_data()
    ticker.create_news_data()
    df = pd.concat([df, ticker.get_stock_data_with_symbol()])
print(df)
print("ok")

df.to_csv("tickers.csv",index=False)