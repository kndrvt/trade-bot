"""
"""

import sys
import yaml
import random

class TraderBot:

    def __init__(self):
        pass

    def run(self, args):

        # set arguments
        gap = args['gap']
        gap_ignore = args['gap_ignore']

        # set default state
        state = 'buy'

        # get current_price
        current_price = self.request_current_price()

        # set prices
        buy_price = current_price - gap / 2
        sell_price = current_price + gap

        # set order
        self.set_order(state, buy_price)

        while(True):

            # get current_price
            current_price = self.request_current_price()

            if state == 'buy':
                # buy order
                if current_price <= buy_price:
                    state = 'sell'
                    sell_price = current_price + gap
                    self.set_order(state, sell_price)

                elif current_price > buy_price + gap + gap_ignore:
                    self.cancel_order(state, buy_price)
                    buy_price = current_price - gap / 2
                    self.set_order(state, buy_price)

            elif state == 'sell':
                # sell order
                if current_price >= sell_price:
                    state = 'buy'
                    buy_price = current_price - gap / 2
                    self.set_order(state, buy_price)

                elif current_price < sell_price - gap - gap_ignore:
                    self.cancel_order(state, sell_price)
                    sell_price = current_price + gap
                    self.set_order(state, sell_price)

            else:
                # error
                print("Error of state. Default state is buy.")
                state = 'buy'

    def request_current_price(self):
        value = random.randint(-100, 100)
        print(value)
        return value

    def cancel_order(self, state, price):
        print("(CANCEL) Order:", state, price)

    def set_order(self, state, price):
        print("Order:", state, price)

    def terminate(self):
        pass


def main(argv):
    config_file = argv[1]
    with open(config_file) as file:
        configs = yaml.load(file, Loader=yaml.FullLoader)
        bot = TraderBot()
        try:
            bot.run(configs['robot'])
        except:
            bot.terminate()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv)
    else:
        print("Usage: python TraderBot.py <filename path>")
