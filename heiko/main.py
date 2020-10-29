import logging
from heiko.config import Config
import heiko.schedulers as schedulers


def main():
    config = Config()
    sched = schedulers.BasicScheduler(config)
    sched.run()


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.DEBUG,
    )
    main()
