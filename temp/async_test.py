#!/usr/bin/env python3

import yaml
import asyncio, asyncssh, sys
import time
import logging
import heapq

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

logging.basicConfig(level=logging.DEBUG)

stream = open("../.config/heiko.yml")
config = yaml.load(stream, Loader=Loader)

host = config['nodes'][0]['host']
username = config['nodes'][0]['username']
port = config['nodes'][0]['port']
password = config['nodes'][0]['password']
commands = config['jobs'][0]['commands']

nodes = config['nodes']

nodelist = []

for i in range(len(nodes)):
    nodelist.append([1, i, nodes[i]])

heapq.heapify(nodelist)

async def run_client(node):
    async with asyncssh.connect(node['host'], port=node['port'], username=node['username'], password=node['password']) as conn:
        result = await conn.run('; '.join(commands), check=True)
        print(result.stdout, end='')

def main():
    while True:
        node = heapq.heappop(nodelist)
        try:
            asyncio.get_event_loop().run_until_complete(run_client(node[2]))
        except Exception as exc:
            logging.error('Got error %s', exc)
        finally:
            if node[0] <= 10:
                node[0] = node[0] * 2
            time.sleep(node[0])
            heapq.heappush(nodelist, node)
