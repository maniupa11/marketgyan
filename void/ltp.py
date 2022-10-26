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
global ltp

# access_token = AliceBlue.login_and_get_access_token(username= username, password= password, twoFA= twoFA,  api_secret= api_secret, app_id = app_id)
# print(access_token)

# with open('access_token.txt','w') as wr1:
# 	wr=csv.writer(wr1)
# 	wr.writerow([access_token])
# access_token=open('access_token.txt','r').read().strip()
access_token = "0c5KgRZSOlbJ6I6bDesBKjRwKZOVTgFESveWu9d4niY.rZ7O9MuFYZnrB0Iz0UJdlEPW7019fVpO7d3CAd-Fg2I"
alice=AliceBlue(username= username ,password= password, access_token=access_token, master_contracts_to_download=['NSE', 'BSE'])
# print(alice.get_balance())

socket_opened = False

def event_handler_quote_update(message):
	gettingDataa(message)




def open_callback():
	global socket_opened
	socket_opened = True
def main():
	alice.start_websocket(subscribe_callback=event_handler_quote_update,
					socket_open_callback=open_callback,
					run_in_background=True)
	while(socket_opened==False):
		pass
		alice.subscribe(alice.get_instrument_by_symbol('NSE', 'SBIN'), LiveFeedType.MARKET_DATA)
		time.sleep(10)
    return ltp


def gettingDataa(message):
	ltp = message['ltp']
	high= message['high']
	low = message['low']
	openn = message['open']
	vol = message['volume']
	print(f" Exchange:{ltp}")

	
# while True:
# tickerlist = ["ZEEL", "ITC", "IBULHSGFIN", "SBIN", "DLF", "RBLBANK", "POWERGRID", "EXIDEIND", "PETRONET", "APOLLOTYRE", "INDUSTOWER", "AMBUJACEM", "HINDALCO", "JINDALSTEL", "TORNTPOWER", "BANDHANBNK"]
# for i in tickerlist:
# 	instrument = alice.get_instrument_by_symbol('NSE', i)
# 	# print(instrument)
# 	try:
# 		ltpp=alice.subscribe(instrument, LiveFeedType.MARKET_DATA)

# 	except TypeError:
# 		pass
if __name__ == "__main__":
	main()