from pya3 import *
import csv
import datetime
import time
import document_details
import xlwings as xw
import pandas as pd



TOKEN = 0
OPEN = 0
HIGH = 0
LOW = 0
LTP = 0
instrument_list = ["SBIN-EQ","LT-EQ"]

socket_opened = False
subscribe_flag = False
subscribe_list = []
unsubscribe_list = []

def socket_open(): 
    print("Connected")
    global socket_opened
    socket_opened = True
    if subscribe_flag: 
        alice.subscribe(subscribe_list)

def socket_close(): 
    global socket_opened, LTP
    socket_opened = False
    LTP = 0
    print("Closed")

def socket_error(message):  
    global LTP
    LTP = 0
    print("Error :", message)

def feed_data(message):  
    global LTP, OPEN, HIGH, LOW, TOKEN, subscribe_flag
    feed_message = json.loads(message)
    print(feed_message)
    if feed_message["t"] == "ck":
        print("Connection Acknowledgement status :%s (Websocket Connected)" % feed_message["s"])
        subscribe_flag = True
        print("subscribe_flag :", subscribe_flag)
        print("-------------------------------------------------------------------------------")
        pass
    elif feed_message["t"] == "tk":
        # print("Token Acknowledgement status :%s " % feed_message)
        TOKEN = feed_message['tk']
        OPEN = feed_message['o']
        HIGH = feed_message['h']
        LOW = feed_message['l']
        LTP = feed_message['lp']
        print(f"Token: {TOKEN}, Open: {OPEN}, High: {HIGH}, Low: {LOW}, Ltp; {LTP}")
        print("-------------------------------------------------------------------------------")
        pass
    else:
        # print("Feed :", feed_message)
        TOKEN = feed_message['tk'] if 'tk' in feed_message else TOKEN
        LTP = feed_message['lp'] if 'lp' in feed_message else LTP 
        OPEN = feed_message['o'] if 'o' in feed_message else OPEN
        HIGH = feed_message['h'] if 'h' in feed_message else HIGH
        LOW = feed_message['l'] if 'l' in feed_message else LOW
        print(f"Token: {TOKEN}, Open: {OPEN}, High: {HIGH}, Low: {LOW}, Ltp: {LTP}")

        

def main():
  
    app_key = "N1EivCi2qOiAimMR4HmAPl6a51XR5gcuCkkUenEXHraKY8rukxNk2JWbU3OKuT4BMFbeSOzflVKg6yYQPSRrbJfCaRsLPgx7nCSAqissQ5YriEPilmVhSyAynk84opFA"         # Get from https://a3.aliceblueonline.com      After Login go to "Apps" section and create API
    username = "AB151545"         # Aliceblue login user id

    alice = Aliceblue(user_id=username,api_key=app_key)
    print(alice.get_session_id())
    # alice.download_master_contract(to_csv=True)
    alice.get_contract_master("NSE")
    
    alice.start_websocket(socket_open_callback=socket_open, socket_close_callback=socket_close,
                          socket_error_callback=socket_error, subscription_callback=feed_data, run_in_background=True)

    while not socket_opened:
        pass
    global subscribe_list, unsubscribe_list
    subscribe_list = [alice.get_instrument_by_symbol('NSE', i)for i in instrument_list]
    while True:
        alice.subscribe(subscribe_list)

    # # Closing Time
    # while datetime.time(17, 45) > datetime.datetime.now().time():
    #     sleep(1)

if __name__ == '__main__':
    main()