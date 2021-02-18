"""
"""

# import random
import sys
import time
import signal

import yaml
from Exchange import Exchange
from PlotDrawer import PlotDrawer

def SigHandler(signum, frame):
    raise Exception("Terminate exception")

class TraderBot:

    def __init__(self, exchange, drawer, args):
        self.exchange = exchange
        self.drawer = drawer
        self.gap = args['gap']
        self.gap_ignore = args['gap_ignore']
        self.amount = args['amount']
        self.delay = args['delay']

        # # exchange model
        # random.seed()
        # self.current_value = 100

    def run(self):
        # set default state
        state = 'buy'

        # get current_price
        current_price = self.request_current_price()

        # set prices
        buy_price = current_price - self.gap / 2
        sell_price = current_price + self.gap

        # set order
        self.set_order(state, buy_price, self.amount)

        # information for plot collecting
        self.drawer.add_price(current_price)
        self.drawer.add_order_price(state, buy_price, sell_price)

        while (True):
            # get current_price
            current_price = self.request_current_price()
            print(current_price)

            if state == 'buy':
                # buy order
                if current_price <= buy_price:
                    state = 'sell'
                    sell_price = current_price + self.gap
                    self.set_order(state, sell_price, self.amount)
                    # information for plot collecting
                    self.drawer.add_order_price(state, buy_price, sell_price)

                elif current_price > buy_price + self.gap + self.gap_ignore:
                    self.cancel_order(state, buy_price)
                    buy_price = current_price - self.gap / 2
                    self.set_order(state, buy_price, self.amount)
                    # information for plot collecting
                    self.drawer.add_order_price(state, buy_price, sell_price)

            elif state == 'sell':
                # sell order
                if current_price >= sell_price:
                    state = 'buy'
                    buy_price = current_price - self.gap / 2
                    self.set_order(state, buy_price, self.amount)
                    # information for plot collecting
                    self.drawer.add_order_price(state, buy_price, sell_price)

                elif current_price < sell_price - self.gap - self.gap_ignore:
                    self.cancel_order(state, sell_price)
                    sell_price = current_price + self.gap
                    self.set_order(state, sell_price, self.amount)
                    # information for plot collecting
                    self.drawer.add_order_price(state, buy_price, sell_price)
            else:
                # error
                print("Error of state. Default state is buy.")
                state = 'buy'

            # information for plot collecting
            self.drawer.add_price(current_price)

            # pause
            time.sleep(self.delay)

    def request_current_price(self):
        # self.current_value += random.normalvariate(0, 2)
        # return self.current_value
        return self.exchange.request_current_price()

    def cancel_order(self, state, price):
        return self.exchange.cancel_order()

    def set_order(self, state, price, amount):
        return self.exchange.set_order(state, price, amount)

    def terminate(self):
        self.exchange.terminate()
        self.drawer.terminate()


def main(argv):
    signal.signal(signal.SIGINT, SigHandler)
    config_file = argv[1]
    with open(config_file) as file:
        configs = yaml.load(file, Loader=yaml.FullLoader)
        exchange = Exchange(configs['exchange'])
        bot = TraderBot(Exchange(configs['exchange']), PlotDrawer(), configs['robot'])

        try:
            bot.run()
        except Exception as err:
            print(err)
        finally:
            bot.terminate()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv)
    else:
        print("Usage: python TraderBot.py <filename path>")
