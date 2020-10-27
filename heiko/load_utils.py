import logging
import asyncssh
import sys
import os
import asyncio

from heiko.config import Node


class HeikoGetNodeDetails:
    def __init__(self, node: Node):
       self.port = node.port
       self.host = node.host
       self.username = node.username
       self.password = node.password
       self.name = node.name
       self.details = dict()
    
    async def getNodeRam(self, conn):
        ram = await conn.run('free', check=True)
        logging.info("Fetching ram of node %s", self.name) 
        return ram
    
    async def getCpuUsage(self, conn):
        usage = await conn.run('uptime', check=True)
        logging.info('Fetching CPU Usage of node %s', self.name)
        return usage

    async def getCpuDetails(self, conn):
        cpu = await conn.run('lscpu -J', check=True)
        logging.info('Fetching CPU details of node %s', self.name)
        return cpu

    async def getDetails(self):
        async with asyncssh.connect(self.host,
                                    port=self.port,
                                    username=self.username,
                                    password=self.password) as conn:
            ram = await self.getNodeRam(conn)
            usage = await self.getCpuUsage(conn)
            cpu = await self.getCpuDetails(conn)
            self.details['ram'] = ram
            self.details['usage'] = usage
            self.details['cpu'] = cpu



