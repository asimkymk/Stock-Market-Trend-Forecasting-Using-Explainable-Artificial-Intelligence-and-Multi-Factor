const googleTrends = require('google-trends-api');
const fs = require('fs');
const { Parser } = require('json2csv');

const tickers =['AAL', 'AAPL', 'AGNC', 'AMC', 'AMD', 'AMZN', 'ASML', 'ATKR', 'BAC', 'BBBY', 'BBIO', 'BLU', 'BMEA', 'BSGA', 'CSCO', 'CTRA', 'DKNG', 'ELYM', 'ERIC', 'ETRN', 'EXTR', 'FDBC', 'FRC', 'GDEN', 'GMDA', 'GMVD', 'GNRC', 'GOOG', 'GRAB', 'GRIN', 'HAIA', 'HBAN', 'HLMN', 'HSAI',
       'HWCPZ', 'HYFM', 'IMAQ', 'INTC', 'IRMD', 'ISRG', 'JBLU', 'LCID', 'LUNR', 'MRVL', 'MSFT', 'NFLX', 'NIO', 'NVDA', 'PACW', 'PHYS', 'PSTX', 'RBLX', 'RIVN', 'ROKU', 'RPHM', 'SCHW', 'SGHT', 'SNAP', 'STRO', 'TEAF', 'TSLA', 'UAL', 'UFAB', 'ULBI', 'VALE', 'WAL', 'XPEV', 'XTNT', 'YCBD']
;
const dateIntervals = [{ startDate: '2022-03-01', endDate: '2022-03-31' },
{ startDate: '2022-04-01', endDate: '2022-04-30' },
{ startDate: '2022-05-01', endDate: '2022-05-31' },
{ startDate: '2022-06-01', endDate: '2022-06-30' },
{ startDate: '2022-07-01', endDate: '2022-07-31' },
{ startDate: '2022-08-01', endDate: '2022-08-31' },
{ startDate: '2022-09-01', endDate: '2022-09-30' },
{ startDate: '2022-10-01', endDate: '2022-10-31' },
{ startDate: '2022-11-01', endDate: '2022-11-30' },
{ startDate: '2022-12-01', endDate: '2022-12-31' },
{ startDate: '2023-01-01', endDate: '2023-01-31' },
{ startDate: '2023-02-01', endDate: '2023-02-28' },
{ startDate: '2023-03-01', endDate: '2023-03-31' },
{ startDate: '2023-04-01', endDate: '2023-04-30' }]
    ;

async function fetchTrendData(keyword, startDate, endDate) {
    const result = await googleTrends.interestOverTime({
        keyword,
        startTime: new Date(startDate),
        endTime: new Date(endDate) // Dünya genelinde veri almak için geo parametresini boş bir string olarak ayarla
    });

    return JSON.parse(result).default.timelineData;
}

function formatDate(timestamp) {
    const date = new Date(timestamp);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');

    return `${year}-${month}-${day}`;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchAllTrends(ticker, interval) {
    let allTrends = [];




    try {
        console.log(`Fetching data for ${ticker} between ${interval.startDate} and ${interval.endDate}...`);
        let search =  ticker;
        search=ticker;
        const trendData = await fetchTrendData(search, interval.startDate, interval.endDate);
        console.log(search);
        const formattedData = trendData.map((item) => {
            return {
                keyword: ticker,
                time: formatDate(item.time * 1000),
                value: item.value[0],
            };
        });

        allTrends = allTrends.concat(formattedData);


    } catch (error) {
        console.log(error)
        return allTrends;
    }




    return allTrends;
}

async function main() {
    for (let ticker of tickers) {
        for (let interval of dateIntervals) {

            const allTrends = await fetchAllTrends(ticker, interval);
            console.log(allTrends.length)
            console.log("------------------------")
            
            // Verileri CSV'ye dönüştür
            const json2csvParser = new Parser({ quote: '' }); // quote opsiyonunu boş bir string olarak ayarla
            const csvData = json2csvParser.parse(allTrends);

            // CSV verisini dosyaya yaz
            fs.writeFile('trend_datas/' + ticker + '_' + interval.startDate + '_' + interval.endDate + '.csv', csvData, (err) => {
                if (err) {
                    console.error('Hata:', err);
                } else {
                    console.log('CSV dosyası başarıyla oluşturuldu!');
                }
            });
        }
    }

}

main();
