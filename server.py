import logging
import json
from websocket_server import WebsocketServer
import requests

# Load file
# wget https://github.com/Pymmdrza/Rich-Address-Wallet/releases/download/Bitcoin-Addr_Sep-2023/Just_All_P2PKH_Bitcoin_Addresses.txt.zip
filename = 'btc.txt'
with open(filename) as f :
    addresses = set(f.read().split())
print(f"Loaded {len(addresses)} addresses!")

def handler(client, server, message):
    data = json.loads(message)
    id = data.get('id')
    method = data.get('method')
    params = data.get('params')
    address = params.get('address')
    coin = params.get('coin')

    if method == 'wallet_includeRich':
        if (coin == 'BTC'):
            status = address in addresses
            server.send_message(client, msg = json.dumps({"id": id, "address": address, "coin": coin, "status": status}))
            

def new_client(client, server):
	server.send_message_to_all("Hey all, a new client has joined us")

server = WebsocketServer(host='0.0.0.0', port=8000, loglevel=logging.INFO)
server.set_fn_message_received(handler)
server.run_forever()
