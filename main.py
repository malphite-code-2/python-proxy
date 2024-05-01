import logging
import json
from websocket_server import WebsocketServer
import requests

# Load file
filename = 'https://github.com/Pymmdrza/Rich-Address-Wallet/releases/download/Rich_Bitcoin_Addresses_08_2023/P2PKH.txt'
response = requests.get(filename)
response.encoding = "utf-8"
addresses = set(response.text.split())

print(f"Loaded {len(addresses)} addresses!")

def handler(client, server, message):
    data = json.loads(message)
    method = data.get('method')
    address = data.get('address')
    if method == 'scan.wallet-check':
        status = address in addresses
        server.send_message(client, msg = json.dumps({"address": address, "status": status}))
            

def new_client(client, server):
	server.send_message_to_all("Hey all, a new client has joined us")

server = WebsocketServer(host='0.0.0.0', port=8000, loglevel=logging.INFO)
server.set_fn_message_received(handler)
server.run_forever()
