import http.client

conn = http.client.HTTPSConnection("news-api14.p.rapidapi.com")

headers = {
    'x-rapidapi-subscription': "ultra",
    'x-rapidapi-proxy-secret': "c02cea90-4588-11eb-add9-c577b8ecdc8e",
    'x-rapidapi-user': "suprikurniyanto",
    'X-RapidAPI-Key': "66def7c48emsh1c947a8fe7be8e2p1639ccjsnd617b5a5e00f",
    'X-RapidAPI-Host': "news-api14.p.rapidapi.com"
    }

conn.request("GET", "/search?q=AAPL&language=en&pageSize=100&from=2022-03-01&to=2023-04-03&sortBy=timestamp", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


veri = data.decode("utf-8")


import json
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(veri, f)