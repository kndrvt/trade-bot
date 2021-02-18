"""
"""

import asyncio
from time import sleep

import websockets
import json
import yaml
import sys


class Exchange:

    def __init__(self, args):
        self.client_id = args['client_id']
        self.client_secret = args['client_secret']
        self._id = 0
        self.uri = args['uri']
        self.instrument = args['instrument']
        self.order_id = None

        msg = \
            {
                "jsonrpc": "2.0",
                "id": self.get_id(),
                "method": "public/auth",
                "params": {
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                }
            }

        async def auth(msg):
            websocket = await websockets.client.connect(self.uri)
            await websocket.send(msg)
            response = await websocket.recv()
            print(json.dumps(json.loads(response), indent=4))
            return websocket

        self.ws = asyncio.get_event_loop().run_until_complete(auth(json.dumps(msg)))

    def get_id(self):
        self._id += 1
        return self._id

    def request_current_price(self):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": self.get_id(),
                "method": "public/ticker",
                "params": {
                    "instrument_name": self.instrument
                }
            }

        async def ticker(websocket, msg):
            await websocket.send(msg)
            response = await websocket.recv()
            print(json.dumps(json.loads(response), indent=4))
            return json.loads(response)['result']['mark_price']

        return asyncio.get_event_loop().run_until_complete(ticker(self.ws, json.dumps(msg)))

    def cancel_order(self, order=None):
        if not order:
            order = self.order_id
        msg = \
            {
                "jsonrpc": "2.0",
                "id": self.get_id(),
                "method": "private/cancel",
                "params": {
                    "order_id": order
                }
            }

        async def cancel(websocket, msg):
            await websocket.send(msg)
            response = await websocket.recv()
            print(json.dumps(json.loads(response), indent=4))
            return

        asyncio.get_event_loop().run_until_complete(cancel(self.ws, json.dumps(msg)))

    def cancel_all(self):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": self.get_id(),
                "method": "private/cancel_all",
                "params": {}
            }

        async def cancel_all(websocket, msg):
            await websocket.send(msg)
            response = await websocket.recv()
            print(json.dumps(json.loads(response), indent=4))
            return

        asyncio.get_event_loop().run_until_complete(cancel_all(self.ws, json.dumps(msg)))

    def set_order(self, state, price, amount):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": self.get_id(),
                "method": "private/" + state,
                "params": {
                    "instrument_name": self.instrument,
                    "amount": amount,
                    "type": "limit",
                    "price": price
                }
            }

        async def order(websocket, msg):
            await websocket.send(msg)
            response = await websocket.recv()
            print(json.dumps(json.loads(response), indent=4))
            return json.loads(response)['result']['order']['order_id']

        self.order_id = asyncio.get_event_loop().run_until_complete(order(self.ws, json.dumps(msg)))

    def terminate(self):
        async def close(websocket):
            await websocket.close()
            return

        self.cancel_all()
        asyncio.get_event_loop().run_until_complete(close(self.ws))


def main(argv):
    config_file = argv[1]
    with open(config_file) as file:
        configs = yaml.load(file, Loader=yaml.FullLoader)
        # authentication test
        exchange = Exchange(configs['exchange'])
        curr = exchange.request_current_price()
        print(curr)
        # test buy
        exchange.set_order('buy', curr - 100, 10)
        sleep(5)
        exchange.cancel_order()
        # test sell
        exchange.set_order('sell', curr + 100, 10)
        sleep(5)
        exchange.cancel_order()
        # test cancel
        exchange.cancel_order(order=5323874219)
        curr = exchange.request_current_price()
        exchange.set_order('buy', curr - 100, 10)
        exchange.set_order('buy', curr - 200, 10)
        exchange.set_order('sell', curr + 100, 10)
        exchange.set_order('sell', curr + 200, 10)
        sleep(5)
        exchange.cancel_all()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv)
    else:
        print("Usage: python Exchange.py <filename path>")
