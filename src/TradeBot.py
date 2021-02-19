"""
This is module with bot. It launches trade bot.
TradeBot class is main project class. It implements trade bot.
Module needs to receive YAML configuration file as argument.
Module start to shut down after SIGINT receiving.
"""

# import random
import sys
from time import sleep
import signal

import yaml
from Exchange import Exchange
from PlotDrawer import PlotDrawer


def SigHandler(signum, frame):
    raise Exception("Terminate exception")


class TradeBot:

    def __init__(self, exchange, drawer, args):
        # set additional objects
        self.exchange = exchange
        self.drawer = drawer

        # set arguments from config file
        self.gap = args['gap']
        self.gap_ignore = args['gap_ignore']
        self.amount = args['amount']
        self.delay = args['delay']

        # # exchange model
        # random.seed()
        # self.current_value = 100

    # run bot forever
    def run(self):
        # set default state
        state = 'buy'

        # get current_price
        current_price = self.request_current_price()

        # set prices
        buy_price = current_price - self.gap / 2
        sell_price = current_price + self.gap

        # set order
        self.place_order(state, buy_price, self.amount)

        # information for plot collecting
        self.drawer.add_price(current_price)
        self.drawer.add_order_price(state, buy_price, sell_price)

        # main cycle
        while (True):
            # get current_price
            current_price = self.request_current_price()

            # conditions checking
            if state == 'buy':
                # buy order
                if current_price <= buy_price:
                    # place new sell order after deal
                    state = 'sell'
                    sell_price = current_price + self.gap
                    self.place_order(state, sell_price, self.amount)

                    # information for plot collecting
                    self.drawer.add_order_price(state, buy_price, sell_price)

                elif current_price > buy_price + self.gap + self.gap_ignore:
                    # cancel old buy order and place new one
                    self.cancel_order()
                    buy_price = current_price - self.gap / 2
                    self.place_order(state, buy_price, self.amount)

                    # information for plot collecting
                    self.drawer.add_order_price(state, buy_price, sell_price)

            elif state == 'sell':
                # sell order
                if current_price >= sell_price:
                    # place new buy order after deal
                    state = 'buy'
                    buy_price = current_price - self.gap / 2
                    self.place_order(state, buy_price, self.amount)

                    # information for plot collecting
                    self.drawer.add_order_price(state, buy_price, sell_price)

                elif current_price < sell_price - self.gap - self.gap_ignore:
                    # cancel old sell order and place new one
                    self.cancel_order()
                    sell_price = current_price + self.gap
                    self.place_order(state, sell_price, self.amount)

                    # information for plot collecting
                    self.drawer.add_order_price(state, buy_price, sell_price)

            else:
                # error
                print("Error of state. Default state is buy.")
                state = 'buy'

            # information for plot collecting
            self.drawer.add_price(current_price)

            # pause
            sleep(self.delay)

    # request and return current mark price
    def request_current_price(self):
        # # exchange model
        # self.current_value += random.normalvariate(0, 2)
        # return self.current_value
        return self.exchange.request_current_price()

    # cancel current order
    def cancel_order(self):
        return self.exchange.cancel_order()

    # place buy/sell order with corresponding price and amount
    def place_order(self, state, price, amount):
        return self.exchange.place_order(state, price, amount)

    # terminate object
    def terminate(self):
        self.exchange.terminate()
        self.drawer.terminate()


def main(argv):
    # signal and arguments configuring
    signal.signal(signal.SIGINT, SigHandler)
    config_file = argv[1]

    # config file opening
    with open(config_file) as file:
        # config file loading
        configs = yaml.load(file, Loader=yaml.FullLoader)

        # bot creating
        bot = TradeBot(Exchange(configs['exchange']), PlotDrawer(), configs['robot'])

        # bot running
        try:
            bot.run()
        except Exception as err:
            print(err)
        finally:
            bot.terminate()


if __name__ == '__main__':
    # arguments count handling
    if len(sys.argv) > 1:
        main(sys.argv)
    else:
        print("Usage: python TradeBot.py <filename path>")
