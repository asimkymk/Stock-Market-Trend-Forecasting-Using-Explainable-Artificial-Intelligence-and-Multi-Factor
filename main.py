from data.Ticker import Ticker
import pandas as pd
import csv
from GoogleNews import GoogleNews
from datetime import datetime
import os
from data.news_scraper import get_detailed_text_data
from data.news_scorer import NewsScorer


longNames = {
    "AAL": "American Airlines",
    "AAPL": "Apple",
    "AGNC": "AGNC Investment",
    "AMC": "AMC Entertainment",
    "AMD": "Advanced Micro Devices",
    "AMZN": "Amazon",
    "ASML": "ASML Holding",
    "ATKR": "Atkore",
    "BAC": "Bank of America",
    "BBBY": "Bed Bath & Beyond",
    "BBIO": "BridgeBio Pharma",
    "BLU": "BELLUS Health",
    "BMEA": "Biomea Fusion",
    "BSGA": "Blue Safari Group Acquisition",
    "CSCO": "Cisco",
    "CTRA": "Coterra Energy",
    "DKNG": "DraftKings",
    "ELYM": "Eliem Therapeutics",
    "ERIC": "Ericsson",
    "ETRN": "Equitrans Midstream",
    "EXTR": "Extreme Networks",
    "FDBC": "Fidelity D&D Bancorp",
    "FRC": "First Republic Bank",
    "GDEN": "Golden Entertainment",
    "GMDA": "Gamida Cell",
    "GMVD": "G Medical Innovations",
    "GNRC": "Generac",
    "GOOG": "Alphabet",
    "GRAB": "Grab Holdings",
    "GRIN": "Grindrod Shipping Holdings",
    "HAIA": "Healthcare AI Acquisition",
    "HBAN": "Huntington Bancshares",
    "HLMN": "Hillman Solutions",
    "HSAI": "Hesai Group",
    "HWCPZ": "Hancock Whitney",
    "HYFM": "Hydrofarm Holdings",
    "IMAQ": "International Media Acquisition",
    "INTC": "Intel",
    "IRMD": "iRadimed",
    "ISRG": "Intuitive Surgical",
    "JBLU": "JetBlue Airways",
    "LCID": "Lucid Group",
    "LUNR": "Intuitive Machines",
    "MRVL": "Marvell Technology",
    "MSFT": "Microsoft",
    "NFLX": "Netflix",
    "NIO": "Nio",
    "NVDA": "Nvidia",
    "PACW": "PacWest Bancorp",
    "PHYS": "Sprott Physical Gold Trust",
    "PSTX": "Poseida Therapeutics",
    "RBLX": "Roblox",
    "RIVN": "Rivian",
    "ROKU": "Roku",
    "RPHM": "Reneo Pharmaceuticals",
    "SCHW": "Charles Schwab",
    "SGHT": "Sight Sciences",
    "SNAP": "Snap",
    "STRO": "Sutro Biopharma",
    "TEAF": "Ecofin Sustainble",
    "TSLA": "Tesla",
    "UAL": "United Airlines",
    "UFAB": "Unique Fabricating",
    "ULBI": "Ultralife",
    "VALE": "Vale",
    "WAL": "Western Alliance",
    "XPEV": "XPeng",
    "XTNT": "Xtant Medical",
    "YCBD": "cbdMD",
}


def create_new_tickers_data():
    # tickers = ['AAL', 'AAPL', 'AGNC', 'AMC', 'AMD', 'AMZN', 'ASML', 'ATKR', 'BAC', 'BBBY', 'BBIO', 'BLU', 'BMEA', 'BSGA', 'CSCO', 'CTRA', 'DKNG', 'ELYM', 'ERIC', 'ETRN', 'EXTR', 'FDBC', 'FRC', 'GDEN', 'GMDA', 'GMVD', 'GNRC', 'GOOG', 'GRAB', 'GRIN', 'HAIA', 'HBAN', 'HLMN', 'HSAI',
    #          'HWCPZ', 'HYFM', 'IMAQ', 'INTC', 'IRMD', 'ISRG', 'JBLU', 'LCID', 'LUNR', 'MRVL', 'MSFT', 'NFLX', 'NIO', 'NVDA', 'PACW', 'PHYS', 'PSTX', 'RBLX', 'RIVN', 'ROKU', 'RPHM', 'SCHW', 'SGHT', 'SNAP', 'STRO', 'TEAF', 'TSLA', 'UAL', 'UFAB', 'ULBI', 'VALE', 'WAL', 'XPEV', 'XTNT', 'YCBD']
    df = pd.DataFrame()
    for symbol, long_name in longNames.items():
        # 1 yıllık verileri tickers.csv ye yaz
        print("Symbol : " + symbol)
        ticker = Ticker(
            symbol=symbol,
            long_name=long_name,
            start_date="2022-03-01",
            end_date="2023-04-26",
        )
        ticker.create_stock_data()

        df = pd.concat([df, ticker.get_stock_data()])

    df.to_csv("tickers.csv", index=False)

    # df.to_csv("news_new.csv",index=False)


def continue_news():
    # Haberleri çekmeye devam et. Ban açıldıkçabu fonk. çalıştır.
    news = []
    df = pd.read_csv("tickers.csv")

    existing_news = {}
    with open("news_new.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            existing_news[(row["date"], row["symbol"])] = True

    x = (df["Date"], df["symbol"])
    for i in range(len(x[0])):
        if (x[0][i], x[1][i]) not in existing_news:
            try:
                print(x[0][i] + " - " + x[1][i])
                tarih = x[0][i]
                date_obj = datetime.strptime(tarih, "%Y-%m-%d")
                yeni_tarih = date_obj.strftime("%m-%d-%Y")
                googlenews = GoogleNews(start=yeni_tarih, end=yeni_tarih)
                googlenews.search("NASDAQ:" + x[1][i])
                # googlenews.search(x[1][i])
                result = googlenews.result()

                for item in result:
                    title = item["title"]
                    text = item["desc"]
                    link = item["link"]
                    detailed_text = ""
                    try:
                        detailed_text = get_detailed_text_data(link)
                    except:
                        detailed_text = "NO_DETAILED_TEXT"
                    news.append([title, text, link, x[0][i], x[1][i], detailed_text])
            except TypeError as e_parser:
                print("Type Error")
                news.append(
                    [
                        "NO_TITLE",
                        "NO_DESC",
                        "NO_LINK",
                        x[0][i],
                        x[1][i],
                        "NO_DETAILED_TEXT",
                    ]
                )
            except:
                break

    df3 = pd.DataFrame(news)
    df3.to_csv("news_new.csv", mode="a", index=False, header=False)


def collab_google_trends_data():
    # nodejs ile toplanan google trend verilerini tek bir csv dosyasına at
    folder_path = "data/google_trends/trend_datas"

    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    combined_csv = pd.concat(
        [pd.read_csv(os.path.join(folder_path, f)) for f in csv_files]
    )

    combined_csv.to_csv(
        "all_trend_datas.csv",
        index=False,
        encoding="utf-8-sig",
        header=["symbol", "Date", "value"],
    )


def combine_tickers_with_trend_scores():
    # toplanan tek csvdeki trend verilerini kullanacağımız ana csv dosyası olan tickers.csv yle birleştir.
    tickers_df = pd.read_csv("tickers.csv")
    trends_df = pd.read_csv("all_trend_datas.csv")

    trends_df = trends_df[["symbol", "Date", "value"]]

    merged_df = pd.merge(tickers_df, trends_df, on=["Date", "symbol"], how="left")

    merged_df["value"] = merged_df["value"].fillna(0)

    merged_df = merged_df.rename(columns={"value": "trend_score"})
    merged_df.to_csv("tickers.csv", index=False)



def create_daily_news_score(start_index):
    df = pd.read_csv("tickers.csv")
    news = pd.read_csv("news_new.csv")
    ns = NewsScorer()
    for index in range(start_index, len(df)):
        try:
            row = df.iloc[index]
            symbol = row["symbol"]
            date = row["Date"]
            long_name = row["long_name"]
            filtered_df = news[(news["symbol"] == symbol) & (news["date"] == date)]
            titles = []
            texts = []
            dates = []
            toplam_metod_1 = 0
            toplam_metod_2 = 0
            for index_nw, row_news in filtered_df.iterrows():
                if row_news["link"] != "NO_LINK":
                    if not pd.isnull(row_news['title']):
                        if (
                            symbol
                            in row_news["title"]
                            + " "
                            + row_news["text"]
                            + " "
                            + row_news["detailed_text"]
                            or long_name
                            in row_news["title"]
                            + row_news["text"]
                            + " "
                            + row_news["detailed_text"]
                        ):
                            titles.append(row_news["title"])
                            texts.append(row_news["text"] + " " + row_news["detailed_text"])
                            dates.append(row_news["date"])
                            toplam_metod_1 += ns.sentiment_analysis_metod_1(str(row_news["title"]) + ' ' + str(row_news["text"]) + " " + str(row_news["detailed_text"]))
                            toplam_metod_2 += ns.sentiment_analysis_metod_2(str(row_news["title"]) + ' ' + str(row_news["text"]) + " " + str(row_news["detailed_text"]))['compound']
                
            data = {
                "date": dates,
                "title": titles,
                "text": texts,
            }
                
            temp_df = pd.DataFrame(data)
            ns.set_news_data(temp_df)
            ns.create_scored_data()
            score = ns.get_average_score()[date]
            
            df.at[index,"news_score_model1"] = score
            df.at[index,"news_score_model2"] = toplam_metod_1
            df.at[index,"news_score_model3"] = toplam_metod_2
            if index % 20 == 0:
                print("CSV Güncelleniyor...")
                df.to_csv('tickers.csv', index=False)
            print(str(index) + ' - ' + symbol + ' - ' + date + ' - ' + str(score) + ' - ' + str(toplam_metod_1) + ' - ' + str(toplam_metod_2))
        except Exception as e:
            print(e)
            df.at[index,"news_score_model1"] = 0
            df.at[index,"news_score_model2"] = 0
            df.at[index,"news_score_model3"] = 0
            print(str(index) + ' - ' + symbol + ' - ' + date + ' - ' + str(0) + ' - ' + str(0) + ' - ' + str(0))
    print("CSV Kaydedildi...")
    df.to_csv('tickers.csv', index=False)


def find_open_and_close_difference(start_index):
    df = pd.read_csv("tickers.csv")
    for index in range(start_index, len(df)):
        try:
            row = df.iloc[index]
            symbol = row["symbol"]
            date = row["Date"]
            openValue = row['Open']
            adjCloseValue = row['Adj Close']
            difference = (adjCloseValue - openValue) / openValue * 100
            if abs(difference) <= 1:
                df.at[index,"difference_value"] = int(0)
            elif adjCloseValue > openValue:
                df.at[index,"difference_value"] = int(1)
            else:
                df.at[index,"difference_value"] = int(-1)
            if index % 100 == 0:
                print("CSV Güncelleniyor...")
                df.to_csv('tickers.csv', index=False)
            print(str(index) + ' / ' + symbol + ' / ' + date + ' / ' + str(openValue) + ' / ' + str(adjCloseValue) + ' / ' + str(difference) )
        except Exception as e:
            print(e)
            print(str(index) + ' / ' + symbol + ' / ' + date + ' / ' + str(openValue) + ' / ' + str(adjCloseValue) + ' / ' + str(difference))
            break
    print("CSV Kaydedildi...")
    df.to_csv('tickers.csv', index=False)
