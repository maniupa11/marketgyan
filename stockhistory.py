from datetime import datetime
import time
import symbol
import pandas as pd
import asyncio
import aiohttp
from statistics import mean


def stockhistory():
    results = []
    epochend=int(time.mktime(datetime.now().timetuple()))
    epochstart=epochend-(84600*50)
    # print(epochend)
    # print(epochstart)
    tickerlist = []
    mcsymbol=[]
    mcsymbolkey=symbol.symbolkey
    for keys in mcsymbolkey:
        tickerlist.append(mcsymbolkey[keys])
        mcsymbol.append(keys)
    # print(tickerlist)
    async def get_symbols():
        async with aiohttp.ClientSession() as session:
            tasks = [session.get('https://priceapi.moneycontrol.com/techCharts/indianMarket/stock/history?symbol='+symbol+'&resolution=1D&from='+str(epochstart)+'&to='+ str(epochend), ssl=False) for symbol in tickerlist]
            responses = await asyncio.gather(*tasks)
            for response in responses:
                results.append(await response.json())
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_symbols())
    col_names = ['mcsymbol','ticker','high10d','low10d', 'vol30d_avg']
    st_history = pd.DataFrame(columns = col_names)
    st_rows = pd.DataFrame(columns = col_names)
    m=0
    # print(results)
    for result in results:
        # print(result)
        # print(tickerlist[m])
        st_rows=pd.DataFrame({#'Symbol':[result['data']['symbol']],
            'mcsymbol':[mcsymbol[m]],
            'ticker':[tickerlist[m]],
            'high10d':[max(result['h'][-11:-1])],
            'low10d':[min(result['l'][-11:-1])],
            'vol30d_avg':[int(mean(result['v'][-30:-1]))],
            })
        m=m+1
        st_history = pd.concat((st_history,st_rows), axis=0, ignore_index=True)
    return st_history