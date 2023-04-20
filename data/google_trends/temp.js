const axios = require("axios");

const options = {
  method: 'GET',
  url: 'https://newscatcher.p.rapidapi.com/v1/search_enterprise',
  params: {
    q: 'NASDAQ:AAPL',
    lang: 'en',
    sort_by: 'relevancy',
    from: '2022/03/01',
    to: '2023/04/03',
    page: '1',
    media: 'True'
  },
  headers: {
    'X-RapidAPI-Key': '66def7c48emsh1c947a8fe7be8e2p1639ccjsnd617b5a5e00f',
    'X-RapidAPI-Host': 'newscatcher.p.rapidapi.com'
  }
};

axios.request(options).then(function (response) {
	console.log(response.data);
}).catch(function (error) {
	console.error(error);
});