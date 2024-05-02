import logging
import json
from websocket_server import WebsocketServer
import requests

# Methods
def get_btc_balance(address):
    try:
        response = requests.get(f"https://bitcoin.atomicwallet.io/api/v2/address/{address}")
        data = response.json()
        balance = int(data.get('balance', 0)) / 100000000
        return balance
    except Exception as error:
        return 0

def get_rvn_balance(address):
    try:
        response = requests.get(f"https://ravencoin.atomicwallet.io/api/v2/address/{address}")
        data = response.json()
        balance = int(data.get('balance', 0)) / 100000000
        return balance
    except Exception as error:
        return 0

# Socket
def handler(client, server, message):
    data = json.loads(message)
    method = data.get('method')
    address = data.get('address')
    seed = data.get('seed')
    coin = data.get('coin')

    if method == 'scan.wallet-balance':
        balance = 0

        if(coin == 'BTC'):
            balance = get_btc_balance(address)
        if(coin == 'RVN'):
            balance = get_rvn_balance(address)

        server.send_message(client, msg = json.dumps({"address": address, "seed": seed, "coin": coin, "status": balance > 0, "balance": balance }))

def new_client(client, server):
	server.send_message_to_all("Hey all, a new client has joined us")

server = WebsocketServer(host='0.0.0.0', port=8000, loglevel=logging.INFO)
server.set_fn_message_received(handler)
server.run_forever()

# https://api.blockchain.info/haskoin-store/btc/address/1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD/balance
# https://api.blockcypher.com/v1/btc/main/addrs/1DEP8i3QJCsomS4BSMY2RpU1upv62aGvhD