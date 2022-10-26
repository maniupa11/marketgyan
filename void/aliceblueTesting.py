# pip install TA_Lib-0.4.24-cp310-cp310-win_amd64.whl

from AliceBlue_V2 import *
import csv
import datetime
import time
import document_details

api_key = "N1EivCi2qOiAimMR4HmAPl6a51XR5gcuCkkUenEXHraKY8rukxNk2JWbU3OKuT4BMFbeSOzflVKg6yYQPSRrbJfCaRsLPgx7nCSAqissQ5YriEPilmVhSyAynk84opFA"         # Get from https://a3.aliceblueonline.com      After Login go to "Apps" section and create API
user_id = "AB151545"         # Aliceblue login user id

alice = Alice(user_id=user_id, api_key=api_key)
alice.create_session()       # Must "log in" to Alice platform before create session
# alice.download_master_contract(to_csv=True)         # Download initially once a day
# print(alice.get_holdings())
alice.get_master_contract("MCX")
alice.get_master_contract("NSE")

a=alice.get_instrument_by_symbol("NSE", "SBIN-EQ")

print(a)

socket_opened = False


def event_handler_quote_update(message):
    print(message)


def open_callback():
    global socket_opened
    socket_opened = True


alice.invalidate_socket_session()
alice.create_socket_session()
alice.start_websocket(subscribe_callback=event_handler_quote_update,
                      socket_open_callback=open_callback,
                      run_in_background=True)
while not socket_opened:
    pass
print("Websocket : Connected")
alice.subscribe(alice.get_instrument_by_symbol("NSE", "SBIN-EQ"))
time.sleep(5)
# alice.unsubscribe([alice.get_instrument_by_symbol("NSE", i) for i in ["ACC-EQ", "RELIANCE-EQ"]])
# time.sleep(10)
