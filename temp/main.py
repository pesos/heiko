import sys, os, time, atexit
from signal import SIGTERM

import argparse
from pathlib import Path
import glob

from async_test import main

class Daemon:
        """
        A generic daemon class.

        Usage: subclass the Daemon class and override the run() method
        """
        def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
                self.stdin = stdin
                self.stdout = stdout
                self.stderr = stderr
                self.pidfile = pidfile

        def daemonize(self):
                """
                do the UNIX double-fork magic, see Stevens' "Advanced
                Programming in the UNIX Environment" for details (ISBN 0201563177)
                http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
                """
                try:
                        pid = os.fork()
                        if pid > 0:
                                # exit first parent
                                sys.exit(0)
                except OSError as e:
                        sys.stderr.write("fork #1 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)

                # decouple from parent environment
                os.chdir("/")
                os.setsid()
                os.umask(0)

                # do second fork
                try:
                        pid = os.fork()
                        if pid > 0:
                                # exit from second parent
                                sys.exit(0)
                except OSError as e:
                        sys.stderr.write("fork #2 failed: %d (%s)\n" % (e.errno, e.strerror))
                        sys.exit(1)

                # redirect standard file descriptors
                sys.stdout.flush()
                sys.stderr.flush()
                si = open(self.stdin, 'r')
                so = open(self.stdout, 'a+')
                se = open(self.stderr, 'a+')
                os.dup2(si.fileno(), sys.stdin.fileno())
                os.dup2(so.fileno(), sys.stdout.fileno())
                os.dup2(se.fileno(), sys.stderr.fileno())

                # write pidfile
                atexit.register(self.delpid)
                pid = str(os.getpid())
                open(self.pidfile,'w+').write("%s\n" % pid)

        def delpid(self):
                os.remove(self.pidfile)

        def start(self):
                """
                Start the daemon
                """
                # Check for a pidfile to see if the daemon already runs
                try:
                        pf = open(self.pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None

                if pid:
                        message = "pidfile %s already exist. Daemon already running?\n"
                        sys.stderr.write(message % self.pidfile)
                        sys.exit(1)

                # Start the daemon
                self.daemonize()
                self.run()

        def stop(self):
                """
                Stop the daemon
                """
                # Get the pid from the pidfile
                try:
                        pf = open(self.pidfile,'r')
                        pid = int(pf.read().strip())
                        pf.close()
                except IOError:
                        pid = None

                if not pid:
                        message = "pidfile %s does not exist. Daemon not running?\n"
                        sys.stderr.write(message % self.pidfile)
                        return # not an error in a restart

                # Try killing the daemon process
                try:
                        while 1:
                                os.kill(pid, SIGTERM)
                                time.sleep(0.1)
                except OSError as err:
                        err = str(err)
                        if err.find("No such process") > 0:
                                if os.path.exists(self.pidfile):
                                        os.remove(self.pidfile)
                        else:
                                print(err)
                                sys.exit(1)

        def restart(self):
                """
                Restart the daemon
                """
                self.stop()
                self.start()

        def run(self):
                """
                You should override this method when you subclass Daemon. It will be called after the process has been
                daemonized by start() or restart().
                """

class HeikoDaemon(Daemon):
    def run(self):
        main()

# Parse CLI args
parser = argparse.ArgumentParser(prog='heiko')
subparsers = parser.add_subparsers(dest='command')

parser_run = subparsers.add_parser('start', help='Starts heiko daemon')
parser_run.add_argument('--name', help='a unique name for the daemon', required=True)

parser_stop = subparsers.add_parser('stop', help='Stops heiko daemon')
parser_stop.add_argument('--name', help='a unique name for the daemon', required=True)

parser_restart = subparsers.add_parser('restart', help='Restarts heiko daemon')
parser_restart.add_argument('--name', help='a unique name for the daemon', required=True)

parser_list = subparsers.add_parser('list', help='lists all running heiko daemons')

args = parser.parse_args()

# Get config directory

heiko_home = Path.home() / '.config' / 'heiko'
os.makedirs(heiko_home, exist_ok=True)

if args.command == 'list':
    pid_files = glob.glob(str(heiko_home / '*.pid'))
    # store PIDs
    pids = []
    for pid_file in pid_files:
        with open(pid_file, "r") as f:
            pids.append(f.read())
    # get names
    names = [pid_file.split('/')[-1].split('_', 1)[-1].split('.')[0] for pid_file in pid_files]
    print("Currently running daemons:")
    for name, pid in zip(names, pids):
        print(f'{name}\t{pid}')

else:
    # Manage daemon
    daemon = HeikoDaemon(heiko_home / f'heiko_{args.name}.pid',
                        stdout=heiko_home / f'heiko_{args.name}.out',
                        stderr=heiko_home / f'heiko_{args.name}.out')
    if args.command == 'start':
        daemon.start()
    elif args.command == 'stop':
        daemon.stop()
    elif args.command == 'restart':
        daemon.restart()
