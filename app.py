# from crypt import methods
from flask import Flask, render_template, jsonify
from datetime import datetime
import oc
import FNOstock
import stock
import stockhistory


app = Flask(__name__)
oi_shortdata, oi_data, long_total, short_total, nifty_spot,time_oi,rtime =oc.chain()


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/optionchain")
def optionchain():
    oi_shortdata, oi_data, long_total, short_total, nifty_spot,time_oi, rtime=oc.chain()
    # print(oi_shortdata['PUTS_Net_Chng'])
    to_table=[oi_shortdata.to_html(classes='data', index=False, header=False)]
    return render_template('optionchain.html',oi_shortdata=oi_shortdata, titles=oi_shortdata.columns.values, nifty_spot=nifty_spot, time_oi=time_oi,rtime=rtime)
@app.route("/ocreload", methods=['POST'])
def ocreload():
    oi_shortdata, oi_data, long_total, short_total, nifty_spot,time_oi, rtime=oc.chain()
    # print(oi_shortdata['PUTS_Net_Chng'])
    to_table=[oi_shortdata.to_html(classes='data', index=False, header=False)]
    return jsonify('', render_template('octemp.html',oi_shortdata=oi_shortdata, titles=oi_shortdata.columns.values, nifty_spot=nifty_spot, time_oi=time_oi, rtime=rtime))

@app.route("/stdata")    
def stdata():
    st_data=FNOstock.nifty50()
    global st_history
    st_history=stockhistory.stockhistory()
    volfactor=[]
    highlow10d=[]
    curtime=datetime.now().strftime('%H:%M')
    voltimefactor=min((int(curtime[0:2])*60 +int(curtime[3:5])-555)/375,1)
    for i in range(len(st_data)):
        volfactor.append(round(st_data.iloc[i]['Volume']/st_history.iloc[i]['vol30d_avg']*voltimefactor,2))
        if st_data.iloc[i]['LTP']>st_history.iloc[i]['high10d']:
            highlow10d.append("10 Day High Corss")
        elif st_data.iloc[i]['LTP']<st_history.iloc[i]['low10d']:
            highlow10d.append("10 Day Low Corss")
        else : highlow10d.append("")
    st_history['Vol Factor']=volfactor
    st_history['Signal']=highlow10d
     # to_sttable=[st_data.to_html(classes='sttable', index=False, header=True)]
    return render_template('stdata.html', st_data=st_data, st_history=st_history)
@app.route("/streload", methods=['POST'])    
def streload():
    st_data=FNOstock.nifty50()
    # st_history=stockhistory.stockhistory()
    volfactor=[]
    highlow10d=[]
    curtime=datetime.now().strftime('%H:%M')
    voltimefactor=min((int(curtime[0:2])*60 +int(curtime[3:5])-555)/375,1)
    # print(voltimefactor)
    for i in range(len(st_data)):
        voltemp=st_data.iloc[i]['Volume']/st_history.iloc[i]['vol30d_avg']
        volfactor.append(round(st_data.iloc[i]['Volume']/st_history.iloc[i]['vol30d_avg']*voltimefactor,2))
        if st_data.iloc[i]['LTP']>st_history.iloc[i]['high10d']:
            highlow10d.append("10 Day High Corss")
        elif st_data.iloc[i]['LTP']<st_history.iloc[i]['low10d']:
            highlow10d.append("10 Day Low Corss")
        else : highlow10d.append("")
    # round(volfactor,2)
    st_history['Vol Factor']=volfactor
    st_history['Signal']=highlow10d
    to_sttable=[st_data.to_html(classes='sttable', index=False, header=True)]
    return jsonify('',render_template('stdatatemp.html', st_data=st_data, st_history=st_history))

@app.route("/stockdata")
def stockdata():
    stock_table=stock.nifty200()

    return render_template('stockdata.html',tables=stock_table)
if __name__ == "__main__":
    app.run(debug=True, port=8000)