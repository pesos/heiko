import os
import time
import sys
import argparse
from pathlib import Path
import glob
import asyncio
import logging
from typing import Iterator


from heiko.daemon import Daemon
from heiko.main import main
from heiko.utils.load import NodeDetails
from heiko.config import Config, CONFIG_LOCATION

logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p",
    level=logging.INFO,
)


class HeikoDaemon(Daemon):
    def run(self):
        main()


# Parse CLI args
def make_parser():
    """Creates an ArgumentParser, configures and returns it.

    This was made into a separate function to be used with sphinx-argparse

    :rtype: :py:class:`argparse.ArgumentParser`
    """
    parser_ = argparse.ArgumentParser(prog="heiko")
    subparsers = parser_.add_subparsers(dest="command")

    parser_run = subparsers.add_parser("start", help="Starts heiko daemon")
    parser_run.add_argument(
        "--name", help="a unique name for the daemon", required=True
    )

    parser_stop = subparsers.add_parser("stop", help="Stops heiko daemon")
    parser_stop.add_argument(
        "--name", help="a unique name for the daemon", required=True
    )

    parser_restart = subparsers.add_parser("restart", help="Restarts heiko daemon")
    parser_restart.add_argument(
        "--name", help="a unique name for the daemon", required=True
    )

    parser_list = subparsers.add_parser("list", help="lists all running heiko daemons")

    parser_init = subparsers.add_parser(
        "init", help="initialize and benchmark all nodes"
    )

    parser_logs = subparsers.add_parser("logs", help="view logs of a daemon")
    parser_logs.add_argument("--name", help="name of the daemon", required=True)
    parser_logs.add_argument(
        "-f",
        "--follow",
        help="follow log file as it is updated",
        action="store_true",
        dest="follow",
        default=False,
    )
    parser_logs.add_argument(
        "--clear",
        help="clear the log file before reading",
        action="store_true",
        dest="clear",
        default=False
    )

    return parser_


parser = make_parser()


def follow(file) -> Iterator[str]:
    """ Yield each line from a file as they are written. """
    line = ""
    i = 0
    while True:
        tmp = file.readline()
        if tmp is not None:
            line += tmp
            i += 1
            if line.endswith("\n") or i >= 5:
                yield line
                line = ""
                i = 0
        else:
            time.sleep(0.1)


def cli():
    """Entrypoint to the command-line interface (CLI) of heiko.

    It parses arguments from sys.argv and performs the appropriate actions.
    """
    args = parser.parse_args()

    # Get config directory
    heiko_home = Path.home() / ".config" / "heiko"
    os.makedirs(heiko_home, exist_ok=True)

    # list running daemons
    if args.command == "list":
        pid_files = glob.glob(str(heiko_home / "*.pid"))
        # store PIDs
        pids = []
        for pid_file in pid_files:
            with open(pid_file, "r") as f:
                pids.append(f.read())
        # get names
        names = [
            pid_file.split("/")[-1].split("_", 1)[-1].split(".")[0]
            for pid_file in pid_files
        ]
        print("Currently running daemons:")
        print("name\tPID")
        for name, pid in zip(names, pids):
            print(f"{name}\t{pid}")

    elif args.command == "init":

        c = Config(CONFIG_LOCATION)

        for node in c.nodes:
            # Initialization and Benchmarking
            try:
                utils = NodeDetails(node=node)
                asyncio.get_event_loop().run_until_complete(utils.getDetails())
                print("Printing node details")
                print("CPU:\n", utils.details["cpu"])
                print("\nRAM:\n", utils.details["ram"])
                print("\nCPU Usage:\n", utils.details["usage"])
            except Exception as e:
                logging.error("%s", e)

    elif args.command == "logs":
        mode = "rt"
        if args.clear:
            mode = "wt+"
        with open(heiko_home / f"heiko_{args.name}.out", mode) as f:
            if args.follow:
                for line in follow(f):
                    print(line, end="")
            else:
                print(f.read())
    else:
        if "name" not in args:
            parser.print_usage()
            sys.exit(1)

        # Manage daemon
        daemon = HeikoDaemon(
            heiko_home / f"heiko_{args.name}.pid",
            stdout=heiko_home / f"heiko_{args.name}.out",
            stderr=heiko_home / f"heiko_{args.name}.out",
        )

        if args.command == "start":
            daemon.start()
        elif args.command == "stop":
            daemon.stop()
        elif args.command == "restart":
            daemon.restart()
