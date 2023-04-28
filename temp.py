import nltk
from textblob import TextBlob

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('brown')

def sentiment_analysis(news_text):
    analysis = TextBlob(news_text)
    
    # Polarity: -1 (olumsuz) ile 1 (olumlu) arasında bir değer alır.
    polarity = analysis.sentiment.polarity
    
    if polarity == 0:
        return "Nötr", polarity
    elif polarity > 0:
        return "Olumlu", polarity
    else:
        return "Olumsuz", polarity

# Örnek haber metni
news_text = "The company's new product attracted great interest and its stock value increased."

result, score = sentiment_analysis(news_text)

print(f"Metnin Analizi: {result}")
print(f"Puan: {score}")
