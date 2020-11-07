# heiko

[![Documentation Status](https://readthedocs.org/projects/browser-history/badge/?version=latest)](https://browser-history.readthedocs.io/en/latest/?badge=latest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

```heiko``` is a lightweight load balancer that uses SSH to manage servers running on
low-end hardware such as Raspberry Pis or even mobile phones.

The name heiko is derived from the Japanese term for *equilibrium*.

heiko uses a smart scheduler to run a program on one node from a set of nodes. It is
very robust to node failures and switches to a different node as soon as the current node
fails. The node to run is intelligently selected based on multiple factors such as CPU power,
memory capacity, free memory, current CPU load, past failures and others.


# Installation and Usage

Installation using pip
```
pip install py-heiko
```

Installation from source
```
git clone https://github.com/psiayn/heiko.git
cd heiko
pip install .
```

Check if the installation succeeded
```
heiko --help
```

Check out the [quickstart](https://heiko.readthedocs.io/en/latest/quickstart.html) section of the documentation.

# License

heiko uses [Apache License 2.0](LICENSE)
