import requests

symbol = "AAPL"  # hisse senedi sembolü

api_key = "dda2e1dd09a04623a9e74e42a98d2d58"  # Alpha Vantage API anahtarı
from_date = "2022-01-01"  # başlangıç tarihi
to_date = "2022-03-31"  # bitiş tarihi

url = f"https://newsapi.org/v2/everything?q={symbol}&from={from_date}&to={to_date}&apiKey={api_key}"

response = requests.get(url)

news = response.json()

print(news)
