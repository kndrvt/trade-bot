"""
"""

import random
import sys
import time
import pymysql
import yaml
# import matplotlib.pyplot as plt


class TraderBot:

    def __init__(self):
        # exchange model
        random.seed()
        self.current_value = 100

        # # data for plot
        # self.plot_order_buy = {}
        # self.plot_order_sell = {}
        # self.plot_price = {}
        # self.current_time = int(0)

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

            # # information for plot collecting
            # self.plot_price[self.current_time] = current_price
            # if state == 'buy':
            #     self.plot_order_buy[self.current_time] = buy_price
            # else:
            #     self.plot_order_sell[self.current_time] = sell_price
            # self.current_time += 1

            # pause
            time.sleep(1)

    def request_current_price(self):
        self.current_value += random.normalvariate(0, 2)
        return self.current_value

    def cancel_order(self, state, price):
        pass

    def set_order(self, state, price):
        pass

    def terminate(self):
        pass
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
