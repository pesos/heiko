import logging
import asyncssh
import sys
import os
import re
import asyncio
import json

from heiko.config import Node


class NodeDetails:
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
    
    def parserRam(self, ram):
        ram = ram.stdout
        # print(ram.split('\n')[1])
        pattern = re.compile(r"Mem:\ +(\d+)\ +\d+\ +\d+\ +\d+\ +\d+\ +(\d+)")
        mem = pattern.findall(ram)
        mem = {'total_mem': mem[0][0], 'free_mem': mem[0][1]}
        return mem


    def parseLoad(self, load):
        load = load.stdout
        # print(load)
        pattern = re.compile(r"load average: \d+\.\d+, (\d+\.\d+), \d+\.\d+")
        load = pattern.findall(load)
        return load[0]

    def parseCpuInfo(self, info):
        info = info.stdout
        info = json.loads(info)
        info = info['lscpu']
        cpu_info = {'cpus': '', 'cpu_max': '', 'cpu_mhz': ''}
        for field in info:
            # print(field)
            # print(field['field'])
            if field['field'] == "CPU(s):":
                cpu_info['cpus'] = field['data']
            elif field['field'] == "CPU max MHz:":
                cpu_info['cpu_max'] = field['data']
            elif field['field'] == "CPU MHz:":
                cpu_info['cpu_mhz'] = field['data']

        return cpu_info

    async def getDetails(self):
        async with asyncssh.connect(self.host,
                                    port=self.port,
                                    username=self.username,
                                    password=self.password) as conn:
            ram = await self.getNodeRam(conn)
            usage = await self.getCpuUsage(conn)
            cpu = await self.getCpuDetails(conn)

            mem = self.parserRam(ram)
            load = self.parseLoad(usage)
            info = self.parseCpuInfo(cpu)
            self.details['ram'] = mem
            self.details['usage'] = load
            self.details['cpu'] = info



