import logging
from heiko.config import Config
from heiko.daemon import Daemon
import heiko.schedulers as schedulers

def main():
    config = Config()
    sched = schedulers.BasicScheduler(config)
    sched.run()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
