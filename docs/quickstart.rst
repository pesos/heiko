.. _quick_start:

Quick Start
===========

Installation
------------

From PyPI
^^^^^^^^^

::

    pip install py-heiko

From Git
^^^^^^^^

1. Clone the repository using ``git clone``
2. Go to the repository directory ``cd heiko``
3. (optional) setup a virtualenv or venv
4. Install heiko using ``pip install .``
5. Check if install succeeded by typing ``heiko --help`` in the command line

Usage
-----

heiko, in essence, runs a command or a list of commands on one node at a time
from a set of nodes.

heiko makes daemons that run in the background and schedule a program on the nodes.
All the configuration is specified in a simple YAML config file and the programs are
run over SSH.

1. Set up SSH and the program to run on all the nodes.
2. Create a ``.config`` directory in your current directory.
   heiko must be run from the same directory when managing the daemon.
   ::

        mkdir .config

3. Copy the sample config (from the
   repository) to the newly created ``.config``.
   ::

        cp sample-config.yml .config/heiko.yml

4. Open ``.config/heiko.yml`` in your favourite editor and fill in the required
   information for all nodes and jobs (the examples should be self-explanatory).
   Note that currently only running a single job is supported.
5. Run ``heiko init`` and ensure that your nodes are identified and their information
   is printed.
   ::

        heiko init

6. You can now start the daemon using::

        heiko start --name somename

   where ``somename`` must be a unique name for this daemon.
7. Confirm that the daemon is running using::

        heiko list

8. Check the log to ensure that your program is running correctly! The output
   from your program is piped to this log.::

        heiko logs --name somename -f

   The ``-f`` flag indicates that the log is followed as it is written. Use
   Ctrl+C to stop following the log.
9. That's it, you're now running your program on your cluster. You can look
   at other subcommands in heiko::

        heiko --help
    
   and::

        heiko <subcommand> --help
