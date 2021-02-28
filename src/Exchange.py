"""
This is class for connecting to stock exchange via API.
It uses websockets and json.
The main function of the module starts testing methods.
"""

import sys
from time import sleep

import yaml
import json
import asyncio
import websockets


class Exchange:

    def __init__(self, args):
        # set arguments from config file
        self.client_id = args['client_id']
        self.client_secret = args['client_secret']
        self._id = 0
        self.uri = args['uri']
        self.instrument = args['instrument']
        self.order_id = None

        # create message for authentication
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

        # authentication
        async def auth(msg):
            websocket = await websockets.client.connect(self.uri)
            await websocket.send(msg)
            response = await websocket.recv()
            print(json.dumps(json.loads(response), indent=4))
            return websocket

        self.ws = asyncio.get_event_loop().run_until_complete(auth(json.dumps(msg)))

    # generate id for jsonrpc
    def get_id(self):
        self._id += 1
        return self._id

    # request and return current mark price
    def request_current_price(self):
        # create message for price requesting
        msg = \
            {
                "jsonrpc": "2.0",
                "id": self.get_id(),
                "method": "public/ticker",
                "params": {
                    "instrument_name": self.instrument
                }
            }

        # price requesting
        async def ticker(websocket, msg):
            await websocket.send(msg)
            response = await websocket.recv()
            print(json.dumps(json.loads(response), indent=4))
            return json.loads(response)['result']['mark_price']

        return asyncio.get_event_loop().run_until_complete(ticker(self.ws, json.dumps(msg)))

    # place buy/sell order with corresponding price and amount
    def place_order(self, state, price, amount):
        # create message for order placement
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

        # order placement
        async def order(websocket, msg):
            await websocket.send(msg)
            response = await websocket.recv()
            print(json.dumps(json.loads(response), indent=4))
            return json.loads(response)['result']['order']['order_id']

        self.order_id = asyncio.get_event_loop().run_until_complete(order(self.ws, json.dumps(msg)))

    # check order completion
    def check_order(self):
        # create message to check order completion
        msg = \
            {
                "jsonrpc": "2.0",
                "id": self.get_id(),
                "method": "private/get_order_state",
                "params": {
                    "order_id": self.order_id
                }
            }

        # order completion check
        async def check(websocket, msg):
            await websocket.send(msg)
            response = await websocket.recv()
            print(json.dumps(json.loads(response), indent=4))
            # return True if order was closed and False another
            return json.loads(response)['result']['order_state'] != 'open'

        return asyncio.get_event_loop().run_until_complete(check(self.ws, json.dumps(msg)))

    # cancel current order or some order from parameters
    def cancel_order(self, order=None):
        # choose order id for canceling
        if not order:
            order = self.order_id

        # create message for order canceling
        msg = \
            {
                "jsonrpc": "2.0",
                "id": self.get_id(),
                "method": "private/cancel",
                "params": {
                    "order_id": order
                }
            }

        # order canceling
        async def cancel(websocket, msg):
            await websocket.send(msg)
            response = await websocket.recv()
            print(json.dumps(json.loads(response), indent=4))
            return

        asyncio.get_event_loop().run_until_complete(cancel(self.ws, json.dumps(msg)))

    # cancel all orders
    def cancel_all(self):
        # create message for all orders canceling
        msg = \
            {
                "jsonrpc": "2.0",
                "id": self.get_id(),
                "method": "private/cancel_all",
                "params": {}
            }

        # all orders canceling
        async def cancel_all(websocket, msg):
            await websocket.send(msg)
            response = await websocket.recv()
            print(json.dumps(json.loads(response), indent=4))
            return

        asyncio.get_event_loop().run_until_complete(cancel_all(self.ws, json.dumps(msg)))

    # terminate object
    def terminate(self):
        async def close(websocket):
            await websocket.close()
            return

        # all orders canceling
        self.cancel_all()
        # connection closing
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
        exchange.place_order('buy', curr - 100, 10)
        sleep(5)
        exchange.cancel_order()
        # test sell
        exchange.place_order('sell', curr + 100, 10)
        sleep(5)
        exchange.cancel_order()
        # test cancel
        exchange.cancel_order(order=5323874219)
        curr = exchange.request_current_price()
        exchange.place_order('buy', curr - 100, 10)
        exchange.place_order('buy', curr - 200, 10)
        exchange.place_order('sell', curr + 100, 10)
        exchange.place_order('sell', curr + 200, 10)
        print(exchange.check_order())
        sleep(5)
        exchange.cancel_all()
        print(exchange.check_order())


if __name__ == '__main__':
    # arguments count handling
    if len(sys.argv) > 1:
        main(sys.argv)
    else:
        print("Usage: python Exchange.py <filename path>")
