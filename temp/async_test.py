#!/usr/bin/env python3

import yaml
import asyncio, asyncssh, sys
import time
import logging

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

logging.basicConfig(level=logging.DEBUG)

stream = open("../.config/config.yaml")
config = yaml.load(stream, Loader=Loader)

host = config['nodes'][0]['host']
username = config['nodes'][0]['username']
port = config['nodes'][0]['port']
password = config['nodes'][0]['password']

async def run_client():
    async with asyncssh.connect(host, port=port, username=username, password=password) as conn:
        result = await conn.run('cd JoJo-Telegram-Bot && python3 reply.py', check=True)
        print(result.stdout, end='')

try:
    asyncio.get_event_loop().run_until_complete(run_client())
except Exception as exc:
    logging.error('Got error %s', exc)
