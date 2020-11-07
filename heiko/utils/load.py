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

        # regexes
        self.ram_pattern = re.compile(r"Mem:\ +(\d+)\ +\d+\ +\d+\ +\d+\ +\d+\ +(\d+)")
        self.load_pattern = re.compile(r"load average: \d+\.\d+, (\d+\.\d+), \d+\.\d+")

        self.cpu = {"cpus": -1, "cpu_mhz": -1}
        self.load = 100
        self.mem = {"total_mem": -1, "free_mem": -1}

    async def getNodeRam(self, conn):
        """Gets RAM details of the node using the ``free`` command.

        :param conn: asynchssh connection object
        :return: output of the command
        :rtype: str
        """
        ram = await conn.run("free", check=True)
        logging.info("Fetching ram of node %s", self.node.name)
        return ram

    async def getCpuUsage(self, conn):
        """Gets CPU usage (load average) of the node using the ``uptime`` command.

        :param conn: asynchssh connection object
        :return: output of the command
        :rtype: str
        """
        usage = await conn.run("uptime", check=True)
        logging.info("Fetching CPU Usage of node %s", self.node.name)
        return usage

    async def getCpuDetails(self, conn):
        """Gets CPU details of the node using the ``lscpu -J`` command.

        :param conn: asynchssh connection object
        :return: output of the command
        :rtype: str
        """
        cpu = await conn.run("lscpu -J", check=True)
        logging.info("Fetching CPU details of node %s", self.node.name)
        return cpu

    def parserRam(self, ram):
        ram = ram.stdout
        # print(ram.split('\n')[1])
        mem = self.ram_pattern.findall(ram)
        self.mem["total_mem"] = float(mem[0][0])
        self.mem["free_mem"] = float(mem[0][1])

    def parseLoad(self, load):
        load = load.stdout
        # print(load)
        self.load = float(self.load_pattern.findall(load)[0])

    def parseCpuInfo(self, info):
        info = info.stdout
        info = json.loads(info)
        info = info["lscpu"]
        for field in info:
            # print(field)
            # print(field['field'])
            if field["field"] == "CPU(s):":
                self.cpu["cpus"] = int(field["data"])
            elif field["field"] == "CPU max MHz:":
                self.cpu["cpu_mhz"] = float(field["data"])
            elif field["field"] == "CPU MHz:":
                self.cpu["cpu_mhz"] = float(field["data"])

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
