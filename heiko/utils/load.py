import logging
import re
import json
import asyncssh

from heiko.config import Node


class NodeDetails:
    """Class to store details of a node such as CPU frequency, no of virtual CPUs,
    load average, total memory, memory usage, etc.

    :param node: node to store details of
    :type node: :py:class:`heiko.config.Node`.
    """

    def __init__(self, node: Node):
        self.node = node

        # regexes:
        #   two different patterns for free and total memory to account for the
        #   fact that the order in which they appear in /proc/meminfo might not
        #   be fixed.
        self._ram_free_pattern = re.compile(r"MemFree:.*?(\d+)")
        self._ram_total_pattern = re.compile(r"MemTotal:.*?(\d+)")

        self.cpu = {"cpus": -1, "cpu_mhz": -1}
        self.load = 100
        self.mem = {"total_mem": -1, "free_mem": -1}

    async def getNodeRam(self, conn):
        """Gets RAM details of the node using the ``/proc/meminfo`` file.

        :param conn: asynchssh connection object
        :return: output of the command
        :rtype: str
        """
        ram = await conn.run("cat /proc/meminfo", check=True)
        logging.info("Fetching ram of node %s", self.node.name)
        return ram

    async def getCpuUsage(self, conn):
        """Gets CPU usage (load average) of the node using the ``/proc/loadavg`` file.

        :param conn: asynchssh connection object
        :return: output of the command
        :rtype: str
        """
        usage = await conn.run("cat /proc/loadavg", check=True)
        logging.info("Fetching CPU Usage of node %s", self.node.name)
        return usage

    async def getCpuDetails(self, conn):
        """Gets CPU details of the node using the ``sysfs`` subsystem.

        :param conn: asynchssh connection object
        :return: output of the command
        :rtype: str
        """
        cpu = await conn.run(
            "cat /sys/devices/system/cpu/cpu*/cpufreq/cpuinfo_max_freq",
            check=True,
        )
        logging.info("Fetching CPU details of node %s", self.node.name)
        return cpu

    def parserRam(self, ram):
        ram = ram.stdout
        free_mem = self._ram_free_pattern.search(ram)
        total_mem = self._ram_total_pattern.search(ram)
        self.mem["total_mem"] = float(total_mem.groups()[0])
        self.mem["free_mem"] = float(free_mem.groups()[0])

    def parseLoad(self, load):
        load = load.stdout
        self.load = float(load.split()[1])

    def parseCpuInfo(self, info):
        info = info.stdout.split()
        len_info = len(info)

        # One max CPU frequency per logical core will be
        # present. Max CPU frequencies will be in KHz.
        num_cpus = len_info

        # Get the maximum CPU frequency across all logical CPUs.
        # Doing a max over the list of values incase the device
        # sets different max frequencies per core.
        max_freq = max([float(i) for i in info]) / 1000

        self.cpu["cpus"] = num_cpus
        self.cpu["cpu_mhz"] = max_freq

    async def getDetails(self):
        """Gets and saves all details of the node"""
        async with asyncssh.connect(
            self.node.host,
            port=self.node.port,
            username=self.node.username,
            password=self.node.password,
        ) as conn:
            ram = await self.getNodeRam(conn)
            usage = await self.getCpuUsage(conn)
            cpu = await self.getCpuDetails(conn)

            self.parserRam(ram)
            self.parseLoad(usage)
            self.parseCpuInfo(cpu)

    def __lt__(self, other):
        if (
            self.load < other.load
            or self.mem["free_mem"] > other.mem["free_mem"]
            or self.cpu["cpu_mhz"] > other.cpu["cpu_mhz"]
            or self.cpu["cpus"] > other.cpu["cpus"]
            or self.mem["total_mem"] > other.mem["total_mem"]
        ):
            return True
        return False

    def __repr__(self):
        return (
            f"<NodeDetails load={self.load} free_mem={self.mem['free_mem']}"
            f" total_mem={self.mem['total_mem']}"
            f" cpu_mhz={self.cpu['cpu_mhz']} cpus={self.cpu['cpus']}"
        )
