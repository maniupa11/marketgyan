import pandas as pd
import asyncio
import aiohttp


def nifty50():

    results = []
    # symbols=['MPS','AHE','API','UTI10','BA06','BAF','BF04','BPC','BTV','BI','C','CI29','DL03','DRL','EM','GI01','HCL02','HDF01','HSL01','HHM','H','HL','HDF','ICI02','IIB','IT','ITC','JVS','KMF','LT','MM','MU01','NI','NTP','ONG','PGC','RI','SLI03','SC12','SBI','SPI','TCS','TT','TEL','TIS','TM4','TI01','UTC','AI10','W']
    symbols=['ABB','KP','ABC07','PFR','ACC','AE01','ADANI54145','MPS','AT18','AL16','GAC','AHE','AL','API','APT02','ADG01','ASF03','AP','AW01','UTI10','BA06','BF04','BA','BAF','BI03','BB09','BOB','BOI','BI01','BE03','BPI02','BFC','BTV','BHE','BL03','MIC','BPC','BI','CB06','CIF01','C','CST','CI29','NII02','CPI','CCI','CF06','CGC01','CI02','DI','OCL','DN','D05','DL03','DT07','D04','AS28','DRL','EM','E05','E','FB','FH','GAI','GP14','GCP','GP11','GI01','GSP02','GGC','HAL','HI01','HCL02','HDF','HAM02','HDF01','HSL01','HHM','H','HPC','HL','HZ','TH','ICI02','ILG','IPL01','IC8','IDF01','IEE','IG04','IHC','II22','IB04','IA05','IIB','BI26','IT','IOC','IL','IRC','ISL03','ITC','JSP','JE02','JVS','JF04','KMF','LFH','DLP01','LL06','LIC','LIC09','BOC','LT','LI09','LTS','LC03','MM','MMF04','MI25','MU01','MHI','MC08','MI','MSS01','BFL','MRF','MSW','MF19','RNL','NAC','IEI01','PRC','NI','NTP','FEV','OR','S11','OI13','ONG','PI35','RSI','OC10','PS15','PLN','PFC02','PGI','PI11','PII','PNB05','PF15','PI41','ML07','PGC','PEP02','MC','REC02','RI','SAI','SCP03','SLI03','SBI','SC12','S','SBP04','SRF','STF','SPI','STV01','SI62','TC','VSN','TT','TEI','TEL','TPC','TIS','TCS','TM4','TIIND54076','TI01','TP06','TP13','L','AI01','HTC02','TVS','UBB','UTC','UBI01','SI10','VB05','SG','V','WI','W','YB','ZT','Z01','CHC']

    async def get_symbols():
        async with aiohttp.ClientSession() as session:
            tasks = [session.get('https://priceapi.moneycontrol.com/pricefeed/nse/equitycash/'+symbol, ssl=False) for symbol in symbols]
            responses = await asyncio.gather(*tasks)
            for response in responses:
                results.append(await response.json())
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_symbols())
    col_names = ['Company','LTP','Change','% Change', 'High','Low','Open','Close','Volume']
    st_data = pd.DataFrame(columns = col_names)
    st_rows = pd.DataFrame(columns = col_names)
    for result in results:
        # print(result)
        st_rows=pd.DataFrame({#'Symbol':[result['data']['symbol']],
            'Company':[result['data']['company']],
            'LTP':[float(result['data']['pricecurrent'])],
            'Change':[result['data']['pricechange']],
            '% Change':[result['data']['pricepercentchange']],
            'Close':[result['data']['priceprevclose']],
            'High':[result['data']['HP']],
            'Low':[result['data']['LP']],
            'Open':[result['data']['OPN']],
            'Volume':[int(result['data']['VOL'])]
            })
        st_data = pd.concat((st_data,st_rows), axis=0, ignore_index=True)
    # print(st_data)    
    return st_data

    # def st_data():
    #     symbol='AE01'
    #     s =requests.Session()
    #     # output= s.get('https://priceapi.moneycontrol.com/techCharts/intra?symbol='+symbol+'&resolution=1&from='+str(st_epoch)+'&to='+str(end_epoch))
    #     output = s.get('https://priceapi.moneycontrol.com/pricefeed/nse/equitycash/'+symbol)
    #     data = output.json()
    #     # print(data)
    #     ltp=data['data']['pricecurrent']
    #     print(ltp)
    #     return ltp