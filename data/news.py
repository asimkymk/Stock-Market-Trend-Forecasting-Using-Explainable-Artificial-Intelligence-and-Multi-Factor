# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 03:17:24 2023

@author: asimk
"""




### TODO
### file and project's struct should be organized!
### TODO END




from GoogleNews import GoogleNews
import pandas as pd


googlenews = GoogleNews(lang='en', period='6m')
googlenews.search('AAPL')
result = googlenews.result()


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

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob

nltk.download('punkt')

nltk.download('stopwords')


nltk.download('wordnet')


df = pd.read_csv('news.csv')


words = []
for text in df['text']:
    tokens = word_tokenize(text)
    
    tokens = [word for word in tokens if word.isalpha() and word not in stopwords.words('english')]
    
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    
    words += tokens


unique_words = set(words)


sentiments = []
for text in df['text']:
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    sentiments.append(sentiment)


scores = []
for text, sentiment in zip(df['text'], sentiments):
    blob = TextBlob(text)

    title_tokens = word_tokenize(df['title'][0])
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


df['score'] = scores
df.to_csv('news_scores.csv', index=False)