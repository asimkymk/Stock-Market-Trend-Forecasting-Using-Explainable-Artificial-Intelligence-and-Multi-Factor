# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 03:17:24 2023

@author: asimk
"""




### TODO
### file and project's struct should be organized!
### write news class for generic usage
### TODO END


#dda2e1dd09a04623a9e74e42a98d2d58



"""
googlenews = GoogleNews(start='02-01-2020',end='02-01-2020')
googlenews.search('AAPL')
result = googlenews.result()

print(googlenews.url)
news = []
for item in result:
    title = item['title']
    text = item['desc']
    date = item['date']
    news.append([title, text, date])

df = pd.DataFrame(news, columns=['title', 'text', 'date'])
print(df)
print(df.info())
df.to_csv("news.csv")
"""
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import pandas as pd
class NewsScorer:

    def __init__(self,):
        self.__news_data = ""
        self.__scored_data = ""
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')

    def set_news_data(self,news_data):
        self.__news_data = news_data
    
    def get_news_data(self):
        return self.__news_data
    
    def set_scored_data(self,scored_data):
        self.__scored_data = scored_data
    
    def get_scored_data(self):
        self.__scored_data

    def create_scored_data(self,):
        words = []
        for text in self.__news_data['text']:
            tokens = word_tokenize(text)
            
            tokens = [word for word in tokens if word.isalpha() and word not in stopwords.words('english')]
            
            lemmatizer = WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(word) for word in tokens]
            
            words += tokens


        unique_words = set(words)


        sentiments = []
        for text in self.__news_data['text']:
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity
            sentiments.append(sentiment)


        scores = []
        for text, sentiment in zip(self.__news_data['text'], sentiments):
            blob = TextBlob(text)

            title_tokens = word_tokenize(self.__news_data['title'][0])
            text_tokens = word_tokenize(text)

            title_tokens = [lemmatizer.lemmatize(word) for word in title_tokens]
            text_tokens = [lemmatizer.lemmatize(word) for word in text_tokens]

            title_unique_words = set(title_tokens)
            text_unique_words = set(text_tokens)

            shared_title_words = title_unique_words.intersection(unique_words)
            shared_text_words = text_unique_words.intersection(unique_words)

            title_score = sum([sentiment * blob.words.count(word) for word in shared_title_words])
            text_score = sum([sentiment * blob.words.count(word) for word in shared_text_words])

            score = title_score + text_score
            scores.append(score)

        self.__scored_data = self.__news_data
        self.__scored_data['news_score'] = scores

    def get_average_score(self):
        daily_mean = self.__scored_data.groupby('date')['news_score'].mean()
        return daily_mean

        
    








