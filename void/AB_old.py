# pip install TA_Lib-0.4.24-cp310-cp310-win_amd64.whl

from alice_blue import *
import csv
import datetime
import time
import document_details

username = document_details.username
password = document_details.password
twoFA = document_details.twoFA
api_secret = document_details.api_secret
app_id = document_details.app_id

# access_token = AliceBlue.login_and_get_access_token(username= username, password= password, twoFA= twoFA,  api_secret= api_secret, app_id = app_id)
# print(access_token)

# with open('access_token.txt','w') as wr1:
# 	wr=csv.writer(wr1)
# 	wr.writerow([access_token])
# access_token=open('access_token.txt','r').read().strip()
access_token = "YIchFl25LCNRfj_br6uWqD0pYaektuPY-_ZtVfeVIPA.4uS2QF9GgN8RQG4nPmfxwJpiFOcAqvnwquPIL5XtJbA"
alice=AliceBlue(username= username ,password= password, access_token=access_token, master_contracts_to_download=['NSE', 'MCX'])
# print(alice.get_balance())

socket_opened = False

def event_handler_quote_update(message):
	# gettingDataa(message)
	print(f" Exchange:{message['exchange']}, Token:{message['token']}, Symbol:{message['instrument'].symbol}, Lot_Size:{message['instrument'].lot_size}, LTP:{message['ltp']}, High:{message['high']}, Low:{message['low']}, Volume:{message['volume']}, Time:{datetime.datetime.fromtimestamp(message['exchange_time_stamp'])} ")
	
	# print("manish")



def open_callback():
	global socket_opened
	socket_opened = True
# def main():
alice.start_websocket(subscribe_callback=event_handler_quote_update,
				socket_open_callback=open_callback,
				run_in_background=True)
while(socket_opened==False):
	pass
	alice.subscribe(alice.get_instrument_by_symbol("MCX", "CRUDEOIL22SEPFUT"), LiveFeedType.MARKET_DATA)
	time.sleep(3)
	
# while True:
# 	tickerlist = ["ZEEL", "ITC", "IBULHSGFIN", "SBIN", "DLF", "RBLBANK", "POWERGRID", "EXIDEIND", "PETRONET", "APOLLOTYRE", "INDUSTOWER", "AMBUJACEM", "HINDALCO", "JINDALSTEL", "TORNTPOWER", "BANDHANBNK"]
# 	for i in tickerlist:
# 		instrument = alice.get_instrument_by_symbol('NSE', i)
# 		# print(instrument)
# 		try:
# 			ltpp=alice.subscribe(instrument, LiveFeedType.MARKET_DATA)

# 		except TypeError:
# 			pass
# if __name__ == "__main__":
# 	main()

def gettingDataa(message):
	ltp = message['ltp']
	high= message['high']
	low = message['low']
	openn = message['open']
	vol = message['volume']
	print(f" Exchange:{ltp}")