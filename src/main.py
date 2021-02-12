"""
"""

import sys
import docker


def run_bot(config_file):
    client = docker.from_env()
    client.containers.run(image='traderbot', command="python src/TraderBot.py " + config_file)


def run_stock_exchange(config_file):
    pass


def main(argv):
    config_file = argv[1]
    run_bot(config_file)
    run_stock_exchange(config_file)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv)
    else:
        print("Usage: python main.py <filename path>")
