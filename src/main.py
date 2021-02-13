"""
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

    try:
        # docker enviroment getting
        client = docker.from_env()

        # bot starting
        bot = client.containers.run(name='traderbot', image='traderbot:latest',
                                    command="python src/TraderBot.py {}".format(config_file),
                                    detach=True, auto_remove=True)

        # stock exchange starting
        client.swarm.init(advertise_addr='127.0.0.1:8080')
        exchange = client.services.create(name='exchange', image='mysql:8')

        # signal waiting
        signal.pause()

    except:
        pass

    finally:
        # docker stopping and service removing
        print("Shutting down")
        bot.stop()
        exchange.remove()
        client.swarm.leave(force=True)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv)
    else:
        print("Usage: python main.py <filename path>")
