
import pandas as pd
import requests
import numpy as np
import asyncio
import aiohttp
import os

def nifty200():
    def nsefetch(payload):
        headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'Sec-Fetch-User': '?1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-Mode': 'navigate',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',}
        try:
            output = requests.get(payload,headers=headers).json()
            #print(output)
        except ValueError:
            s =requests.Session()
            output = s.get("http://nseindia.com",headers=headers)
            output = s.get(payload,headers=headers).json()
        return output
        # df = pd.read_csv("https://www1.nseindia.com/content/fo/fo_mktlots.csv")
        # return [x.strip(' ') for x in df.drop(df.index[3]).iloc[:,1].to_list()]

    col_names = ['symbol','lastPrice','open','dayHigh','dayLow',
    'previousClose','pChange','totalTradedVolume']
    stock_data = pd.DataFrame(columns = col_names)
    st_rows = pd.DataFrame(columns = col_names)
    # oi_shortdata = pd.DataFrame(columns = col_names)

    payload = nsefetch('https://www.nseindia.com/api/equity-stockIndices?index=SECURITIES%20IN%20F%26O')
    # stock_data = pd.DataFrame(positions['data'])
    # print(payload)
    m=0
    for m in (payload['data']):
        if(1>0):
            try:
                st_rows=pd.DataFrame({'symbol':[m['symbol']],
                    'open':[m['open']],
                    'dayHigh':[m['dayHigh']],
                    'dayLow':[m['dayLow']],
                    'lastPrice':[m['lastPrice']],
                    'previousClose':[m['previousClose']],
                    'pChange':[m['pChange']],
                    'totalTradedVolume':[m['totalTradedVolume']]                
                    })

            except KeyError:
                pass
        else:
            pass
        stock_data = pd.concat((stock_data,st_rows), axis=0, ignore_index=True)
        stock_data['open'] = stock_data['open'].apply(pd.to_numeric)
        
    return stock_data
    
    # print(stock_data)