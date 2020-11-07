Welcome to heiko's documentation!
=================================

``heiko`` is a lightweight load balancer that uses ssh to manage servers running on
low-end hardware such as Raspberry Pis or even mobile phones.

The name heiko is derived from the Japanese term for *equilibrium*.

heiko uses a smart scheduler to run a program on one node from a set of nodes. It is
very robust to node failures and switches to a different node as soon as the current node
fails. The node to run is intelligently selected based on multiple factors such as CPU power,
memory capacity, free memory, current CPU load, past failures and others.

Check out the :ref:`quick_start` to get started.

Note that the scheduler must be run from a master node that must not be restarted or
interruppted.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   cli
   api
   contributing

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
