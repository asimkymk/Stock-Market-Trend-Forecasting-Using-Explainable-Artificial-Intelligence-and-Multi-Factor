'use client'
import React, { useState, useEffect, useRef } from "react";
import Home from "./home";
import axios from 'axios';
import ReactLoading from 'react-loading';


const longNames = {
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

const YourComponent = () => {
  const [inputValue, setInputValue] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [home, setHome] = useState(true);
  const [data, setData] = useState(false);
  const [loading, setLoading] = useState(false);
  const getValueKey = (obj, value) => {
    return Object.keys(obj).find(key => obj[key] === value);
  }
  const handleInputChange = (e) => {

    const value = e.target.value;
    setInputValue(value);
    if (value == '') {
      setSuggestions([]);
    }
    else {
      const matchedNames = Object.entries(longNames).filter(
        ([key, name]) =>
          key.toLowerCase().includes(value.toLowerCase()) ||
          name.toLowerCase().includes(value.toLowerCase())
      );
      setSuggestions(matchedNames);
    }
    // Tamamlama önerilerini oluştur



  };

  const handleSuggestionClick = async (name) => {
    setInputValue(name);
    setSuggestions([]);
    try {
      const response = await axios.get('http://127.0.0.1:5000/model/' + getValueKey(longNames, name));
      setHome(false);
      setLoading(true);
      setData(false);
    } catch (error) {
      console.error(error);
      setHome(false);
      setLoading(true);
      setData(false);
    }
  };

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        await axios.get('http://127.0.0.1:8050/');
        setHome(false);
        setLoading(false);
        setData(true);
      } catch (error) {
        console.log(3)
      }
    }, 1000);


    return () => clearInterval(interval);
  }, []);

  return (
    <main className="flex min-h-screen flex-col px-24 bg-white">
      <nav navbar-main className="relative flex flex-wrap items-center justify-between w-full px-0 py-2 mt-6 transition-all shadow-none bg-gray-950/80 duration-250 ease-soft-in rounded-2xl lg:flex-nowrap lg:justify-start" navbar-scroll="true">
        <div className="flex items-center justify-between w-full px-4 py-1 mx-auto flex-wrap-inherit">
          <nav>
            <ol className="flex flex-wrap pt-1 mr-12 bg-transparent rounded-lg sm:mr-16">
              <li className="leading-normal text-sm breadcrumb-item">
                <a className="opacity-30 text-white" href="javascript:;">
                  <svg width="12px" height="12px" className="mb-1" viewBox="0 0 45 40" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink">
                    <title>shop</title>
                    <g className="fill-white" stroke="none" strokeWidth="1" fill="none" fillRule="evenodd">
                      <g className="fill-white" transform="translate(-1716.000000, -439.000000)" fill="#252f40" fillRule="nonzero">
                        <g className="fill-white" transform="translate(1716.000000, 291.000000)">
                          <g className="fill-white" transform="translate(0.000000, 148.000000)">
                            <path d="M46.7199583,10.7414583 L40.8449583,0.949791667 C40.4909749,0.360605034 39.8540131,0 39.1666667,0 L7.83333333,0 C7.1459869,0 6.50902508,0.360605034 6.15504167,0.949791667 L0.280041667,10.7414583 C0.0969176761,11.0460037 -1.23209662e-05,11.3946378 -1.23209662e-05,11.75 C-0.00758042603,16.0663731 3.48367543,19.5725301 7.80004167,19.5833333 L7.81570833,19.5833333 C9.75003686,19.5882688 11.6168794,18.8726691 13.0522917,17.5760417 C16.0171492,20.2556967 20.5292675,20.2556967 23.494125,17.5760417 C26.4604562,20.2616016 30.9794188,20.2616016 33.94575,17.5760417 C36.2421905,19.6477597 39.5441143,20.1708521 42.3684437,18.9103691 C45.1927731,17.649886 47.0084685,14.8428276 47.0000295,11.75 C47.0000295,11.3946378 46.9030823,11.0460037 46.7199583,10.7414583 Z"></path>
                            <path
                              d="M39.198,22.4912623 C37.3776246,22.4928106 35.5817531,22.0149171 33.951625,21.0951667 L33.92225,21.1107282 C31.1430221,22.6838032 27.9255001,22.9318916 24.9844167,21.7998837 C24.4750389,21.605469 23.9777983,21.3722567 23.4960833,21.1018359 L23.4745417,21.1129513 C20.6961809,22.6871153 17.4786145,22.9344611 14.5386667,21.7998837 C14.029926,21.6054643 13.533337,21.3722507 13.0522917,21.1018359 C11.4250962,22.0190609 9.63246555,22.4947009 7.81570833,22.4912623 C7.16510551,22.4842162 6.51607673,22.4173045 5.875,22.2911849 L5.875,44.7220845 C5.875,45.9498589 6.7517757,46.9451667 7.83333333,46.9451667 L19.5833333,46.9451667 L19.5833333,33.6066734 L27.4166667,33.6066734 L27.4166667,46.9451667 L39.1666667,46.9451667 C40.2482243,46.9451667 41.125,45.9498589 41.125,44.7220845 L41.125,22.2822926 C40.4887822,22.4116582 39.8442868,22.4815492 39.198,22.4912623 Z"
                            ></path>
                          </g>
                        </g>
                      </g>
                    </g>
                  </svg>
                </a>
              </li>
              <li className="text-sm pl-2 leading-normal before:float-left before:pr-2  before:content-['/']">
                <a className="text-white opacity-50" href="javascript:;">Pages</a>
              </li>
              <li className="text-sm pl-2 capitalize leading-normal before:float-left before:pr-2  before:content-['/'] text-white before:text-white" aria-current="page">Ticker Analyze</li>
            </ol>
            <a className="mb-0 font-bold text-white capitalize cursor-pointer" onClick={async () => {
              try {
                await axios.get('http://127.0.0.1:5000/shutdown')
                setHome(true);
                setData(false);
                setLoading(false);
                setInputValue('');
                setSuggestions([])
              }catch{
                setHome(true);
                setData(false);
                setLoading(false);
                setInputValue('');
                setSuggestions([])
              }
              
            }}>Stock Market Trend Forecasting Using Explainable Artificial Intelligence and Multi-Factor</a>
          </nav>

          <div className="flex items-center">
            <a mini-sidenav-burger href="javascript:;" className="hidden p-0 transition-all ease-nav-brand text-sm text-slate-500 xl:block" aria-expanded="false">
              <div className="w-4.5 overflow-hidden">
                <i className="ease-soft mb-0.75 relative block h-0.5 translate-x-[5px] rounded-sm transition-all bg-white"></i>
                <i className="ease-soft mb-0.75 relative block h-0.5 rounded-sm transition-all bg-white"></i>
                <i className="ease-soft relative block h-0.5 translate-x-[5px] rounded-sm transition-all bg-white"></i>
              </div>
            </a>
          </div>

          <div className="flex items-center mt-2 grow sm:mt-0 sm:mr-6 md:mr-0 lg:flex lg:basis-auto" id="navbar">
            <div className="flex items-center md:ml-auto md:pr-4">
              <div className="">

                <input type="text" className="pl-9 text-sm focus:shadow-soft-primary-outline bg-gray-950 placeholder:text-white/80 text-white/80 ease-soft w-1/100 leading-5.6 relative -ml-px block min-w-0 flex-auto rounded-lg border border-solid border-white bg-clip-padding py-2 pr-3 transition-all focus:border-fuchsia-300 focus:outline-none focus:transition-shadow" placeholder="Type ticker here..."
                  value={inputValue}
                  onChange={handleInputChange}
                />
              </div>
            </div>
          </div>
        </div>

      </nav>
      <div className="overflow-y-auto transition-all bg-gray-950/80 ease-soft-in rounded-2xl"
        style={{ maxHeight: '10rem', position: 'absolute', right: 100, top: 90, zIndex: 1, minWidth: 275 }}>
        {suggestions.map(([key, name]) => (
          <button
            key={key}
            className="text-white block mt-1 mb-2 ml-2 bg-gradient-to-r from-blue-500 via-blue-600 to-blue-700 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"

            onClick={() => handleSuggestionClick(name)}
          >
            {name}
          </button>

        ))}
        <div className="mr-5"></div>
      </div>



      {home == true ? <Home></Home>
        : loading == true ? <div className="flex flex-col items-center justify-center">
          <ReactLoading type={'cylon'} color="black" />
          <div className="text-black">Please wait. Calculating ShadowDecTree for each individual decision tree. It may take some time.</div>
        </div>
          : <iframe height={'2850px'} src="http://127.0.0.1:8050/"></iframe>}



    </main>
  );
};

export default YourComponent;
