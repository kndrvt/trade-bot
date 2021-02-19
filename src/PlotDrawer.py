"""
This is class for collecting information and drawing plot
after trade bot starts to shut down.
"""

from time import time
import matplotlib.pyplot as plt


class PlotDrawer:

    def __init__(self):
        # initializing
        self._price = {}
        self._order_buy_price = {}
        self._order_sell_price = {}
        self.initial_time = time()

    # return current time since object creating
    def current_time(self):
        return time() - self.initial_time

    # add price information
    def add_price(self, price):
        self._price[self.current_time()] = price

    # add order information
    def add_order_price(self, state, buy_price, sell_price):
        if state == 'buy':
            self._order_buy_price[self.current_time()] = buy_price
        else:
            self._order_sell_price[self.current_time()] = sell_price

    # terminate object
    def terminate(self):
        # plot creating and saving
        plt.plot(self._price.keys(), self._price.values(), '-b', label='Price', linewidth=0.8)
        plt.plot(self._order_buy_price.keys(), self._order_buy_price.values(), '.g', label='Buy', markersize=4)
        plt.plot(self._order_sell_price.keys(), self._order_sell_price.values(), '.r', label='Sell', markersize=4)
        plt.legend()
        plt.grid()
        plt.xlabel('Time')
        plt.ylabel('Value')
        plt.savefig('result.pdf')
        # plt.show()
        plt.close()
