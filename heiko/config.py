import os
from typing import List
from dataclasses import dataclass
import yaml

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

CONFIG_LOCATION = os.path.join(os.getcwd(), ".config/heiko.yml")


@dataclass
class Node:
    """Class to store data about a single node"""

    name: str
    host: str
    username: str
    password: str
    port: str


@dataclass
class Job:
    """Class to store data about a job"""

    name: str
    commands: List


class Config:
    """Class to read and parse configuration files file(s)

    The configuration files should be plain YAML files.

    :param config_file: location of configuration file.
        default is ``./.config/heiko.yml``.
    """

    def __init__(self, config_file=None):
        if config_file is None:
            config_file = CONFIG_LOCATION

        with open(config_file, "rt") as stream:
            self.config = yaml.load(stream, Loader=Loader)

        self.nodes = []
        for node in self.config["nodes"]:
            self.nodes.append(Node(**node))

        self.jobs = []
        for job in self.config["jobs"]:
            self.jobs.append(Job(**job))

    @property
    def first_node(self):
        """Returns the first node from the config"""
        return self.nodes[0]

    @property
    def first_job(self):
        """Returns the first job"""
        return self.jobs[0]
