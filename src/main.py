"""
This is main module. It launches docker containers with TradeBot.py
and optionally with MySQL server.
Module needs to receive YAML configuration file for TradeBot.py as argument.
Module start to shut down after SIGINT receiving.
"""

import sys
import signal

import docker


def SigHandler(signum, frame):
    return


def main(argv):
    # signal and arguments configuring
    print("Starting")
    signal.signal(signal.SIGINT, SigHandler)
    config_file = argv[1]
    global client, bot, exchange

    # docker containers running
    try:
        # docker enviroment getting
        client = docker.from_env()

        # bot starting
        bot = client.containers.run(name='tradebot', image='tradebot:latest',
                                    command="python src/TradeBot.py {}".format(config_file),
                                    detach=True, auto_remove=True, network_mode='host')

        # # stock exchange starting
        # exchange = client.containers.run(name='exchange', image='mysql/mysql-server:8.0',
        #                                  command="mysql -h 127.0.0.1 -u root", detach=True,
        #                                  auto_remove=True, network_mode='host',
        #                                  hostname='127.0.0.1', publish_all_ports=True)

        # signal waiting
        signal.pause()

    except Exception as err:
        print(err)

    finally:
        # docker stopping and removing
        print("Shutting down")
        bot.kill(signal='SIGINT')
        bot.stop()
        # exchange.stop()
        print("Finished")


if __name__ == '__main__':
    # arguments count handling
    if len(sys.argv) > 1:
        main(sys.argv)
    else:
        print("Usage: python main.py <filename path>")
