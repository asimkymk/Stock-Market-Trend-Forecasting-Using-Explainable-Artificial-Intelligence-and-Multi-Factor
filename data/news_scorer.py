# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 03:17:24 2023

@author: asimk
"""
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import pandas as pd

from nltk.sentiment import SentimentIntensityAnalyzer
class NewsScorer:
    def __init__(self):
        self.news_data = pd.DataFrame()
        self.scored_data = pd.DataFrame()
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        nltk.download('averaged_perceptron_tagger')
        nltk.download('brown')
        nltk.download('vader_lexicon')

    def set_news_data(self, news_data):
        self.news_data = news_data

    def create_scored_data(self):
        words = []
        for text in self.news_data['text']:
            tokens = word_tokenize(text.lower())
            tokens = [word for word in tokens if word.isalpha() and word not in stopwords.words('english')]
            lemmatizer = WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(word) for word in tokens]
            words += tokens

        unique_words = set(words)

        sentiments = []
        for text in self.news_data['text']:
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity
            sentiments.append(sentiment)

        scores = []
        for text, sentiment in zip(self.news_data['text'], sentiments):
            blob = TextBlob(text.lower())
            title_tokens = word_tokenize(self.news_data['title'][0].lower())
            text_tokens = word_tokenize(text.lower())
            title_tokens = [lemmatizer.lemmatize(word) for word in title_tokens]
            text_tokens = [lemmatizer.lemmatize(word) for word in text_tokens]
            title_unique_words = set(title_tokens)
            text_unique_words = set(text_tokens)
            shared_title_words = title_unique_words.intersection(unique_words)
            shared_text_words = text_unique_words.intersection(unique_words)
            title_score = sum([sentiment * blob.words.count(word) for word in shared_title_words])
            text_score = sum([sentiment * blob.words.count(word) for word in shared_text_words])
            score = (title_score*2 + text_score*8)/10
            scores.append(score)

        self.scored_data = self.news_data.copy()
        self.scored_data['news_score'] = scores

    def get_average_score(self):
        daily_mean = self.scored_data.groupby('date')['news_score'].mean()
        return daily_mean

    
    def sentiment_analysis_metod_1(self, news_text):
        analysis = TextBlob(news_text)
        
        # Polarity: -1 (olumsuz) ile 1 (olumlu) arasında bir değer alır.
        return analysis.sentiment.polarity
    
    def sentiment_analysis_metod_2(self,text):
        sia = SentimentIntensityAnalyzer()
        return sia.polarity_scores(text)

        # Haber başlığı ve içeriğinin duyarlılık puanlarını kullanarak genel haber duyarlılık puanını hesaplayın
        return (baslik_duyarlilik['compound'] + metin_duyarlilik['compound']) / 2

        

        
    








