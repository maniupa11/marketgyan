import csv
from datetime import datetime
import time
import pandas as pd
import requests
import numpy as np
import json

def chain():
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

    symbol='NIFTY'
    def fetch_oi() :
        payload = nsefetch('https://www.nseindia.com/api/option-chain-indices?symbol='+symbol)
        return payload
    # col_names = ['CALLS_OI','CALLS_Chng in OI','CALLS_Volume','CALLS_IV','CALLS_LTP','CALLS_Net Chng',
    # 'Strike Price','PUTS_OI','PUTS_Chng in OI','PUTS_Volume','PUTS_IV','PUTS_LTP','PUTS_Net Chng']

    # scheduler = BackgroundScheduler()
    # payload = scheduler.add_job(fetch_oi, 'interval', minutes=1)
    # payload.start()
    payload=fetch_oi()
    col_names = ['CALLS_OI','CALLS_Chng_in_OI','CALLS_Net_Chng','CALLS_LTP','Strike_Price',
    'PUTS_LTP','PUTS_Net_Chng','PUTS_Chng_in_OI','PUTS_OI']
    oi_data = pd.DataFrame(columns = col_names)
    oi_rows = pd.DataFrame(columns = col_names)
    oi_shortdata = pd.DataFrame(columns = col_names)
    expiry = payload['records']['expiryDates'][0]
    # print(expiry)
    m=0
    for m in range(len(payload['records']['data'])):
        if(payload['records']['data'][m]['expiryDate']==expiry):
            if(1>0):
                try:
                    oi_rows=pd.DataFrame({'CALLS_OI':[payload['records']['data'][m]['CE']['openInterest']],
                        'CALLS_Chng_in_OI':[payload['records']['data'][m]['CE']['changeinOpenInterest']],
                        # 'CALLS_Volume':[payload['records']['data'][m]['CE']['totalTradedVolume']],
                        # 'CALLS_IV':[payload['records']['data'][m]['CE']['impliedVolatility']],
                        'CALLS_Net_Chng':[payload['records']['data'][m]['CE']['change']],
                        'CALLS_LTP':[payload['records']['data'][m]['CE']['lastPrice']],
                        'Strike_Price':[payload['records']['data'][m]['strikePrice']],
                        'PUTS_LTP':[payload['records']['data'][m]['PE']['lastPrice']],
                        'PUTS_Net_Chng':[payload['records']['data'][m]['PE']['change']],
                        'PUTS_Chng_in_OI':[payload['records']['data'][m]['PE']['changeinOpenInterest']],
                        'PUTS_OI':[payload['records']['data'][m]['PE']['openInterest']]
                        # 'PUTS_Volume':[payload['records']['data'][m]['PE']['totalTradedVolume']],
                        # 'PUTS_IV':[payload['records']['data'][m]['PE']['impliedVolatility']],
                        })

                except KeyError:
                    pass
            else:
                pass
            oi_data = pd.concat((oi_data,oi_rows), axis=0, ignore_index=True)
    # print(oi_data)
    # oi_data.to_csv('mm1.csv', index=False)
    # oi_neardata=oi_data.copy()
    nifty_spot=float(payload['records']['underlyingValue'])
    print(nifty_spot)
    time_oi=payload['records']['timestamp']
    # print(time_oi)
    # return oi_data
    # oi_data['PUTS_Net_Chng'].round(decimals=2)
    atm=round(nifty_spot/50)*50
    # print(atm)
    for i in range(atm-500, atm+550, 50):
        oi_shortdata = pd.concat((oi_shortdata,oi_data.loc[oi_data['Strike_Price'] == i]), axis=0, ignore_index=True)
    # print(oi_shortdata)
    sum_short_oi = oi_shortdata.sum(axis=0)
    sum_long_oi = oi_data.sum(axis=0)
    # print(short_oi)
    # print(short_oi.CALLS_Chng_in_OI)
    # short_total=pd.DataFrame({'CALLS_OI':[short_oi.CALLS_OI],
    #                     'CALLS_Chng_in_OI':[short_oi.CALLS_Chng_in_OI],
    #                     'CALLS_Net_Chng':[""],
    #                     'CALLS_LTP':[""],
    #                     'Strike_Price':["Intraday OI"],
    #                     'PUTS_LTP':[""],
    #                     'PUTS_Net_Chng':[""],
    #                     'PUTS_Chng_in_OI':[short_oi.PUTS_Chng_in_OI],
    #                     'PUTS_OI':[short_oi.PUTS_OI]
    #                     })
    # long_total=pd.DataFrame({'CALLS_OI':[long_oi.CALLS_OI],
    #                     'CALLS_Chng_in_OI':[long_oi.CALLS_Chng_in_OI],
    #                     'CALLS_Net_Chng':[""],
    #                     'CALLS_LTP':[""],
    #                     'Strike_Price':["TOTAL OI"],
    #                     'PUTS_LTP':[""],
    #                     'PUTS_Net_Chng':[""],
    #                     'PUTS_Chng_in_OI':[long_oi.PUTS_Chng_in_OI],
    #                     'PUTS_OI':[long_oi.PUTS_OI]
    #                     })                    
    # oi_shortdata = pd.concat((oi_shortdata,short_total,long_total), axis=0,ignore_index=True)
    # print(oi_shortdata['PUTS_Net_Chng'])
    # jsonn = oi_shortdata.to_json()
    # Writing to sample.json
    # with open("templates/sortdata.json", "w") as outfile:
    #   outfile.write(jsonn)
    rtime = datetime.now()
    # print(rtime)
    return oi_shortdata,  oi_data, sum_short_oi, sum_long_oi, nifty_spot,time_oi, rtime

