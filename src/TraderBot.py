"""
"""

# import random
import sys
import time

import yaml
from Exchange import Exchange


# import matplotlib.pyplot as plt


class TraderBot:

    def __init__(self, exchange, args):
        self.exchange = exchange
        self.gap = args['gap']
        self.gap_ignore = args['gap_ignore']
        self.amount = args['amount']
        self.delay = args['delay']

        # # exchange model
        # random.seed()
        # self.current_value = 100

        # # data for plot
        # self.plot_order_buy = {}
        # self.plot_order_sell = {}
        # self.plot_price = {}
        # self.current_time = int(0)

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

        # # information for plot collecting
        # self.plot_price[self.current_time] = current_price
        # self.plot_order_buy[self.current_time] = buy_price

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

                elif current_price > buy_price + self.gap + self.gap_ignore:
                    self.cancel_order(state, buy_price)
                    buy_price = current_price - self.gap / 2
                    self.set_order(state, buy_price, self.amount)
            elif state == 'sell':
                # sell order
                if current_price >= sell_price:
                    state = 'buy'
                    buy_price = current_price - self.gap / 2
                    self.set_order(state, buy_price, self.amount)

                elif current_price < sell_price - self.gap - self.gap_ignore:
                    self.cancel_order(state, sell_price)
                    sell_price = current_price + self.gap
                    self.set_order(state, sell_price, self.amount)
            else:
                # error
                print("Error of state. Default state is buy.")
                state = 'buy'

            # # information for plot collecting
            # self.plot_price[self.current_time] = current_price
            # if state == 'buy':
            #     self.plot_order_buy[self.current_time] = buy_price
            # else:
            #     self.plot_order_sell[self.current_time] = sell_price
            # self.current_time += 1

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
        # # plot creating and saving
        # plt.plot(self.plot_price.keys(), self.plot_price.values(), '-b', label='Price', linewidth=0.8)
        # plt.plot(self.plot_order_buy.keys(), self.plot_order_buy.values(), '.g', label='Buy', markersize=5)
        # plt.plot(self.plot_order_sell.keys(), self.plot_order_sell.values(), '.r', label='Sell', markersize=5)
        # plt.legend()
        # plt.grid()
        # plt.xlabel('Time')
        # plt.ylabel('Value')
        # plt.savefig('result.pdf')
        # plt.close()


def main(argv):
    config_file = argv[1]
    with open(config_file) as file:
        configs = yaml.load(file, Loader=yaml.FullLoader)
        exchange = Exchange(configs['exchange'])
        bot = TraderBot(exchange, configs['robot'])
        try:
            bot.run()
        except:
            bot.terminate()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv)
    else:
        print("Usage: python TraderBot.py <filename path>")
