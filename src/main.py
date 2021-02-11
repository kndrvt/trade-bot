"""
"""

import sys
import yaml
from TraderBot import TraderBot

def main(argv):
    config_file = argv[1]
    with open(config_file) as file:
        configs = yaml.load(file, Loader=yaml.FullLoader)
        bot = TraderBot()
        bot.run(configs['robot'])


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv)
    else:
        print("Usage: python main.py <filename path>")
