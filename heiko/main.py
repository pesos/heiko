import logging
import threading

from heiko.config import Config
from heiko.server import start_http
import heiko.schedulers as schedulers


def main(name):
    config = Config(name)
    if config.http.enabled:
        http_thread = threading.Thread(target=start_http, args=(config.http.port, ))
        http_thread.start()
    sched = schedulers.BasicScheduler(config)
    sched.run()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.DEBUG,
    )
    main()
