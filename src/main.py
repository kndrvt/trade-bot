"""
"""

import sys
import signal
import docker


def SigHandler(signum, frame):
    return


def main(argv):
    signal.signal(signal.SIGINT, SigHandler)
    config_file = argv[1]
    global client, bot, exchange
    try:
        client = docker.from_env()
        bot = client.containers.run(name='traderbot', image='traderbot:latest',
                                    command="python src/TraderBot.py " + config_file,
                                    detach=True, auto_remove=True)
        client.swarm.init(advertise_addr='127.0.0.1:8080')
        exchange = client.services.create(name='exchange', image='mysql:latest')

        signal.pause()
    except:
        pass
    finally:
        bot.stop()
        exchange.remove()
        client.swarm.leave(force=True)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv)
    else:
        print("Usage: python main.py <filename path>")
