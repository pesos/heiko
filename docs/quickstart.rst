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


Requirements
------------

 - A **master** device that will run heiko. This needs to be always active.
   Requirements of a master are:

   - Linux or Unix based OS
   - Python 3.7+
   - ``heiko`` installed (from above)
   - SSH client
   - rsync client
   - sshpass (optional - required for password based login to nodes)

 - A set of **node** devices to run your application. Nodes need not be
   always active, they can be disconnected or terminated at any time, your
   application will run given you have at least one node active.
   Requirements of a node are:

   - SSH Server
   - rsync client
   - Linux-based OS

Usage
-----

heiko, in essence, runs a command or a list of commands on one node at a time
from a set of nodes.

heiko makes daemons that run in the background and schedule a program on the nodes.
All the configuration is specified in a simple YAML config file and the programs are
run over SSH.

1. Ensure you have all the requirements for the master and the nodes.
2. Create a ``.heiko`` directory in your project's directory.
   heiko must be run from the same directory when managing the daemon.
   ::

        mkdir .heiko

3. Copy the sample config (from the
   repository) to the newly created ``.heiko``.
   ::

        cp sample-config.yml .heiko/config.yml

4. Open ``.heiko/config.yml`` in your favourite editor and fill in the required
   information for all nodes and jobs (the examples should be self-explanatory).
   Note that currently only running a single job is supported.

    - The following fields are required for every node: ``name`` (a unique name for the node),
      ``host`` (hostname of the node, can be an IP addresss), ``username`` (name of the SSH user
      to log in as, on the node)
    - If you don't want to store your node's password in plaintext and you want to use
      public key auth, configure the node using the `SSH config file <https://www.ssh.com/ssh/config/>`_.
      Specifically the ``Host`` directive is considered a hostname. For example, if your SSH config file
      contains this::

          Host node1
            HostName 255.255.255.255
            User some_user_name
            IdentityFile ~/.ssh/id_rsa
            Port 22

      And ``ssh node1`` on the command line works, your heiko config.yml file can have

      .. code-block:: yaml

          nodes:
            - name: node1
              host: node1
              username: some_user_name

    - The list of commands under ``init`` will run on the nodes when ``heiko init`` is run and the
      commands under ``commands`` will be run on the nodes, by the daemon, after ``heiko start``.
5. Run ``heiko init --name somename``: this will rsync your project directory to a directory inside
   ``~/.heiko`` on the node. Optionally add a ``.heiko/rsync-ignore`` file listing the files to be
   ignored when rsync'ing (similar to a ``.gitignore``).
   ::

        heiko init --name somename

   where ``somename`` must be a unique name for this daemon.

6. You can now start the daemon using::

        heiko start --name somename

7. Confirm that the daemon is running using::

        heiko list

8. Check the log to ensure that your program is running correctly! The output
   from your program is piped to this log.::

        heiko logs --name somename -f

   The ``-f`` flag indicates that the log is followed as it is written (warning:
   this flag currently uses unnecessary CPU power, ensure that isn't left running). Use
   Ctrl+C to stop following the log.
9. That's it, you're now running your program on your cluster. You can look
   at other subcommands in heiko::

        heiko --help
    
   and::

        heiko <subcommand> --help
