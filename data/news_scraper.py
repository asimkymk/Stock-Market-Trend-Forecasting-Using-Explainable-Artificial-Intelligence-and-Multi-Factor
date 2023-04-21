import pandas as pd
from newspaper import Article

def add_new_detailed_text_column():
    df = pd.read_csv('news_new.csv')

    df = df.assign(detailed_text='')

    df.to_csv('news_new.csv', index=False)

def get_detailed_text_data(news_link):
    ## todo: custom exception
    try:

        article = Article(news_link)
        article.download()
        article.parse()
        if len(article.text)>0:
            return article.text.replace('\n', ' ')
        else:
            raise Exception
    except:
        raise Exception


def get_news_all_data(start_index):
    df = pd.read_csv("news_new.csv")
    for index in range(start_index,len(df)):
        try:
            row = df.iloc[index]
            news_link = row['link']
            if news_link == "NO_LINK" or pd.isnull(row['link']):
                df.at[index,"detailed_text"] = 'NO_DETAILED_TEXT'
            else:
                if pd.isnull(row['detailed_text']):
                    print(str(index) + ' - ' + row['date'] + ' - ' + row['symbol'])
                    detailed_text = get_detailed_text_data(news_link)
                    
                    df.at[index,"detailed_text"] = detailed_text
            
                
            if index % 20 == 0:
                print("CSV Güncelleniyor...")
                df.to_csv('news_new.csv', index=False)
        except:
            print("Veri Hatası")
            df.at[index,"detailed_text"] = 'NO_DETAILED_TEXT'
            df.to_csv('news_new.csv', index=False)
            continue

#add_new_detailed_text_column()
#get_news_all_data()

#fdonksiyonun çalışmasını herhangi bir csv güncelleniyor yazsısından hemen sonra yap.